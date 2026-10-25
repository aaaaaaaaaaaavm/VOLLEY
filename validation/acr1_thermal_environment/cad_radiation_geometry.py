"""CAD-derived diffuse view factors and direct-solar projected areas.

Actual frozen STEP solids are mapped to the accepted BOM by volume/centroid.
Contact surfaces inside another solid are excluded. Seeded cosine-weighted rays
produce area exchange and finite-Earth-disc irradiance factors. Symmetric matrix
balancing enforces radiation reciprocity and retains measured escape fractions.
No source/inverter package surface is invented for its unlocated7kg allocation.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
from scipy.optimize import linear_sum_assignment

HERE=Path(__file__).resolve().parent
NAMES=['mount_ladder','copper','gfrp','sled','magnets','pallet','capacitor_cells','electronics']+[f'payload_{i+1:02d}' for i in range(12)]+['track_frame','north_bank','south_bank','lift_frame']
NN=len(NAMES)


def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def node_of(row,payloads):
    if row['material']=='payload':return 8+payloads.index(row['name'])
    if row['material']=='copper':return 1
    if row['material']=='insulator':return 2
    if row['material']=='ndfeb':return 4
    if row['subsystem']=='sled_pallet':return 5
    if row['subsystem'].startswith('sled'):return 3
    if row['name'].startswith('Bank_north'):return 21
    if row['name'].startswith('Bank_south'):return 22
    if row['subsystem']=='bank_mount':return 22 if row['name'].endswith('-1') else 21
    if row['subsystem']in['track','release_cam']:return 20
    if row['subsystem']=='fixed':return 0
    return 23


def build_mesh(step):
    import cadquery as cq
    bom=json.loads((HERE/'inputs/VOLLEY_G5_ACR1_home.json').read_text())['BOM']
    payloads=sorted(r['name'] for r in bom if r['material']=='payload')
    solids=cq.importers.importStep(str(step)).val().Solids()
    assert len(solids)==len(bom)==387
    centers=np.array([s.Center().toTuple() for s in solids]);volumes=np.array([s.Volume() for s in solids])
    target=np.array([r['CG_mm'] for r in bom]);tv=np.array([r['volume_mm3'] for r in bom])
    cost=np.linalg.norm(centers[:,None]-target[None,:],axis=2)+1000*abs(volumes[:,None]-tv[None,:])/np.maximum(tv[None,:],1e-12)
    si,bi=linear_sum_assignment(cost);mapping=dict(zip(si,bi));errors=cost[si,bi]
    assert errors.max()<.01,errors.max()
    vertices=[];faces=[];owners=[];part_ids=[];count=0;heat_capacity=np.zeros(NN);masses=np.zeros(NN);area_native=np.zeros(NN)
    cp=dict(aluminium=900,copper=385,insulator=1000,steel=470,polymer=1200,catalog=800,payload=900,ndfeb=460)
    for index,solid in enumerate(solids):
        row=bom[mapping[index]];node=node_of(row,payloads)
        vs,fs=solid.tessellate(1.0,.3);v=np.array([x.toTuple() for x in vs])/1000;f=np.asarray(fs,dtype=int)
        sign=np.einsum('ij,ij->i',v[f[:,0]],np.cross(v[f[:,1]],v[f[:,2]])).sum()
        if sign<0:f=f[:,::-1]
        vertices.append(v);faces.append(f+count);owners.extend([node]*len(f));part_ids.extend([index]*len(f));count+=len(v)
        masses[node]+=row['mass_kg'];heat_capacity[node]+=row['mass_kg']*cp[row['material']];area_native[node]+=solid.Area()/1e6
    # Installed allowances are explicit in the accepted mass ledger but unlocated.
    masses[6]=1.28;heat_capacity[6]=1280
    masses[7]=5.72;heat_capacity[7]=5.72*800
    mesh=dict(vertices=np.vstack(vertices),faces=np.vstack(faces),owners=np.array(owners),part_ids=np.array(part_ids),masses=masses,heat_capacity=heat_capacity,area_native=area_native,payload_names=payloads)
    return mesh,dict(solids=len(solids),max_mapping_cost_mm=float(errors.max()),input_step_sha256=sha(step),cadquery_version=cq.__version__,tessellation_linear_tolerance_mm=1,angular_tolerance_rad=.3)


def cosine_directions(normals,rng):
    helper=np.tile([0.,0.,1.],(len(normals),1));helper[abs(normals[:,2])>.9]=[0,1,0]
    tangent=np.cross(helper,normals);tangent/=np.linalg.norm(tangent,axis=1)[:,None];bitangent=np.cross(normals,tangent)
    u=rng.random((len(normals),2));rho=np.sqrt(u[:,0]);phi=2*np.pi*u[:,1]
    return tangent*(rho*np.cos(phi))[:,None]+bitangent*(rho*np.sin(phi))[:,None]+normals*np.sqrt(1-u[:,0])[:,None]


def radiation(mesh,samples,seed,step,removed=()):
    import trimesh
    import cadquery as cq
    from OCP.BRepClass3d import BRepClass3d_SolidClassifier
    from OCP.gp import gp_Pnt
    from OCP.TopAbs import TopAbs_IN
    from trimesh.ray.ray_pyembree import RayMeshIntersector
    active_faces=~np.isin(mesh['owners'],removed)
    owner=mesh['owners'][active_faces];part_ids=mesh['part_ids'][active_faces]
    surf=trimesh.Trimesh(vertices=mesh['vertices'],faces=mesh['faces'][active_faces],process=False)
    scene=RayMeshIntersector(surf);area=surf.area_faces;normals=surf.face_normals
    solids=cq.importers.importStep(str(step)).val().Solids()
    classifiers=[BRepClass3d_SolidClassifier(s.wrapped) for s in solids]
    removed_parts=set(mesh['part_ids'][np.isin(mesh['owners'],removed)].tolist())
    boxes=np.array([[b.xmin,b.ymin,b.zmin,b.xmax,b.ymax,b.zmax] for b in (s.BoundingBox() for s in solids)])/1000
    areas=np.zeros(NN);escape=np.zeros(NN);exchanges=np.zeros((NN,NN));earth=np.zeros(NN)
    beta=np.radians([0,30,60,90]);theta=np.linspace(0,2*np.pi,73)
    solar=np.zeros((len(beta),len(theta),NN));albedo=np.zeros_like(solar)
    thermal_inputs=json.loads((HERE/'THERMAL_INPUTS.json').read_text())
    radius=thermal_inputs['earth_radius_m']+thermal_inputs['earth_emission_altitude_m']
    orbital=thermal_inputs['earth_radius_m']+thermal_inputs['orbit_altitude_m'];records=[]
    for node in range(NN):
        rng=np.random.default_rng(seed+node*1000)
        idx=np.flatnonzero(owner==node)
        if not len(idx):continue
        gross=float(area[idx].sum());chosen=rng.choice(idx,samples,p=area[idx]/gross)
        tri=surf.triangles[chosen];u=rng.random((samples,2));sqrt=np.sqrt(u[:,0]);points=(1-sqrt)[:,None]*tri[:,0]+(sqrt*(1-u[:,1]))[:,None]*tri[:,1]+(sqrt*u[:,1])[:,None]*tri[:,2]
        nn=normals[chosen];origins=points+nn*2e-5
        # Near coplanar contacting STEP faces, parity of a compound triangle
        # soup can be ambiguous. Classify against individual native BReps after
        # an AABB candidate filter; never reject the originating curved solid
        # merely because its triangulation is an approximate chord.
        origin_part=part_ids[chosen]
        cache=HERE/'geometry'/f'contacts_{samples}_node{node:02d}.npz'
        sample_identity=hashlib.sha256(origins.tobytes()+nn.tobytes()).hexdigest()
        if cache.exists():
            saved=np.load(cache);assert str(saved['sample_identity'])==sample_identity
            blocked=saved['blocked_by_part']
        else:
            blocked=np.full(len(origins),-1,dtype=int)
            for part,(box,classifier) in enumerate(zip(boxes,classifiers)):
                candidate=np.flatnonzero((blocked<0)&(origin_part!=part)&np.all(origins>box[:3]+1e-10,axis=1)&np.all(origins<box[3:]-1e-10,axis=1))
                for index in candidate:
                    classifier.Perform(gp_Pnt(*map(float,origins[index]*1000)),1e-6)
                    if classifier.State()==TopAbs_IN:blocked[index]=part
            np.savez_compressed(cache,sample_identity=sample_identity,blocked_by_part=blocked)
        outside=(blocked<0)|np.isin(blocked,list(removed_parts))
        origins=origins[outside];nn=nn[outside]
        weight=gross/samples;areas[node]=weight*len(origins)
        directions=cosine_directions(nn,rng);hit=scene.intersects_first(origins,directions);is_escape=hit<0
        counts=np.bincount(owner[hit[~is_escape]],minlength=NN)
        exchanges[node]=weight*counts;escape[node]=weight*is_escape.sum()
        d=directions[is_escape];disc=orbital**2*d[:,2]**2-(orbital**2-radius**2);planet=(d[:,2]<0)&(disc>=0)
        dp=d[planet];dist=-orbital*dp[:,2]-np.sqrt(disc[planet]);surface_norm=dp*dist[:,None];surface_norm[:,2]+=orbital;surface_norm/=radius
        earth[node]=weight*planet.sum()
        for ib,b in enumerate(beta):
            for it,t in enumerate(theta):
                sun=np.array([-math.sin(t)*math.cos(b),math.sin(b),math.cos(t)*math.cos(b)])
                cosine=nn@sun;positive=cosine>0
                visible=np.zeros(len(origins),dtype=bool)
                if positive.any():visible[positive]=scene.intersects_first(origins[positive],np.tile(sun,(positive.sum(),1)))<0
                solar[ib,it,node]=weight*np.sum(cosine[visible])
                albedo[ib,it,node]=weight*np.maximum(surface_norm@sun,0).sum()
        records.append(dict(node=NAMES[node],gross_mesh_area_m2=gross,contact_free_area_m2=areas[node],contact_free_samples=len(origins),escape_area_m2=escape[node],earth_view_area_m2=earth[node]))
    # Preserve MonteCarlo escape areas while imposing A_iFij=A_jFji exactly.
    active=areas>0;B=(exchanges+exchanges.T)/2;target=areas-escape;scale=np.ones(NN)
    for _ in range(10000):
        current=scale*(B@scale);ratio=np.divide(target,current,out=np.ones(NN),where=current>0)
        scale*=np.sqrt(ratio)
        if np.max(abs(current[active]-target[active])/areas[active])<1e-10:break
    balanced=scale[:,None]*B*scale[None,:]
    F=np.divide(balanced,areas[:,None],out=np.zeros_like(B),where=areas[:,None]>0)
    row=np.max(abs(balanced.sum(axis=1)+escape-areas))
    assert row<1e-8 and abs(balanced-balanced.T).max()<1e-12
    return dict(areas=areas,view_factors=F,escape_areas=escape,earth_areas=earth,theta=theta,beta=beta,solar=solar,albedo=albedo),dict(nodes=records,samples_per_represented_node=samples,seed=seed,
                 reciprocity_max_area_error_m2=float(abs(balanced-balanced.T).max()),row_closure_max_area_error_m2=float(row),
                 diffuse_exchange_projection_relative_norm=float(np.linalg.norm(balanced-exchanges)/np.linalg.norm(exchanges)),
                 method='Individual native-BRep contact exclusion plusseeded actual-CAD diffuse ray tracing withEmbree; symmetric balancing preserves sampled escape area. FiniteEarth-disc ray intersections produce IR/albedo view factors; solar rays include represented-part self-shadowing.',
                 limitations=['Static home-state geometry between movements; loading/dynamic shadows andunrepresentedhost geometry are bounded separately.',
                             'Unlocated7kg source/control allowance receives no invented CAD area orradiator credit.',
                             'Approximate1mm tessellation andfiniteMonteCarlo rays; geometry refinement is evaluated separately,not claimed exact.'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--step',required=True,type=Path);p.add_argument('--samples',type=int,default=4096);p.add_argument('--all-stages',action='store_true');p.add_argument('--stage',type=int,default=0);args=p.parse_args()
    out=HERE/'geometry';out.mkdir(exist_ok=True)
    cache=out/'cad_mesh.npz'
    if cache.exists():
        mesh=dict(np.load(cache,allow_pickle=False));identity=json.loads((out/'CAD_SOURCE.json').read_text())
        assert identity['input_step_sha256']==sha(args.step)
    else:
        mesh,identity=build_mesh(args.step);np.savez_compressed(cache,**mesh);(out/'CAD_SOURCE.json').write_text(json.dumps(identity,indent=2)+'\n')
    # Top-down,alternating south/north source-cell order; node payload names
    # are alphabetical northL0..L5 then southL0..L5.
    order=[value for level in range(5,-1,-1) for value in [14+level,8+level]]
    stages=range(13) if args.all_stages else [args.stage]
    for stage in stages:
        result,record=radiation(mesh,args.samples,20261025,args.step,order[:stage])
        stem=f'radiation_{args.samples}' if stage==0 else f'radiation_s{stage:02d}_{args.samples}'
        np.savez_compressed(out/(stem+'.npz'),**result)
        record.update(generator_sha256=sha(__file__),thermal_geometry_inputs_sha256=sha(HERE/'THERMAL_INPUTS.json'),cad_mesh_sha256=sha(cache),source_identity=identity,node_names=NAMES,
                      stage_released_payloads=stage,release_node_order=order,
                      masses_kg=mesh['masses'].tolist(),heat_capacities_J_K=mesh['heat_capacity'].tolist(),native_gross_areas_m2=mesh['area_native'].tolist())
        (out/(stem.upper()+'.json')).write_text(json.dumps(record,indent=2)+'\n')
        print(json.dumps(dict(samples=args.samples,stage=stage,row_error=record['row_closure_max_area_error_m2'])),flush=True)


if __name__=='__main__':main()
