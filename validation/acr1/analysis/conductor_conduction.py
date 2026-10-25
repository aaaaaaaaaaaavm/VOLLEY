"""DC conduction FEM on an exported actual phase-A copper solid.

Gmsh tetrahedral mesh; linear potential elements; scipy sparse solve.
One-volt terminal conditions, insulating remaining surfaces, uniform resistivity.
Sharp-corner peak current density is mesh dependent; no AC/skin/thermal rating.
"""
from pathlib import Path
import argparse,hashlib,json,time
import numpy as np
from scipy.sparse import coo_matrix
from scipy.sparse.linalg import spsolve
from scipy.sparse.csgraph import connected_components
import gmsh

ROOT=Path(__file__).resolve().parents[1]

def main():
    ap=argparse.ArgumentParser();ap.add_argument('step');ap.add_argument('--h',type=float,default=2.5)
    ap.add_argument('--phase',choices=['A','B','C'],default='A')
    a=ap.parse_args();src=Path(a.step);out=ROOT/'analysis/conduction'/('phase_'+a.phase)/f'h{a.h:g}';out.mkdir(parents=True,exist_ok=True)
    started=time.perf_counter();raw=src.read_bytes()
    p=json.loads((ROOT/'cad/PARAMETERS.json').read_text());m=p['magnetic']
    interface_raw=(ROOT/'cad/WINDING_INTERFACE.json').read_bytes()
    interface=json.loads(interface_raw);faces=interface['terminals'][a.phase]
    term_centers=[faces['start_face_center'],faces['end_face_center']]
    gmsh.initialize();gmsh.logger.start();gmsh.option.setNumber('General.NumThreads',2)
    gmsh.model.occ.importShapes(str(src));gmsh.model.occ.synchronize()
    assert len(gmsh.model.getEntities(3))==1,'A connected single phase solid is required'
    terminals=[[],[]]
    for _,tag in gmsh.model.getEntities(2):
        bb=np.array(gmsh.model.getBoundingBox(2,tag));area=gmsh.model.occ.getMass(2,tag)
        if abs(area-42)<1e-3:
            for j,(x,y,z) in enumerate(term_centers):
                if max(abs(bb[0]-x+3.5),abs(bb[3]-x-3.5),abs(bb[1]-y),abs(bb[4]-y),abs(bb[2]-z+3),abs(bb[5]-z-3))<1e-4:
                    terminals[j].append(tag)
    assert all(len(t)==1 for t in terminals),('Unexpected terminal faces',terminals,term_centers)
    gmsh.option.setNumber('Mesh.MeshSizeMin',a.h/2);gmsh.option.setNumber('Mesh.MeshSizeMax',a.h)
    gmsh.option.setNumber('Mesh.ElementOrder',1);gmsh.model.mesh.generate(3)
    tags,coords,_=gmsh.model.mesh.getNodes();xyz=np.asarray(coords).reshape(-1,3)*.001
    lookup={int(t):i for i,t in enumerate(tags)}
    typ,_,conn=gmsh.model.mesh.getElements(3);assert list(typ)==[4],typ
    tet=np.array([[lookup[int(v)]for v in row] for row in np.asarray(conn[0]).reshape(-1,4)])
    terminal_nodes=[]
    for faces in terminals:
        ts=gmsh.model.mesh.getNodes(2,faces[0],includeBoundary=True)[0]
        terminal_nodes.append(np.array(sorted({lookup[int(t)] for t in ts})))
    gmsh.write(str(out/'phase_A.msh'));version=gmsh.option.getString('General.Version')
    (out/'gmsh.log').write_text('\n'.join(gmsh.logger.get())+'\n');gmsh.logger.stop();gmsh.finalize()
    nodes=xyz[tet];M=np.concatenate([np.ones((len(tet),4,1)),nodes],axis=2)
    volume=abs(np.linalg.det(M))/6;assert np.all(volume>1e-20)
    grads=np.linalg.inv(M)[:,1:,:];sigma=1/1.7e-8
    ke=sigma*volume[:,None,None]*np.einsum('eki,ekj->eij',grads,grads)
    ii=np.repeat(tet,4,axis=1).ravel();jj=np.tile(tet,(1,4)).ravel()
    K=coo_matrix((ke.ravel(),(ii,jj)),shape=(len(tags),len(tags))).tocsr()
    n_components=connected_components(K,directed=False,return_labels=False);assert n_components==1,n_components
    fixed=np.r_[terminal_nodes[0],terminal_nodes[1]];V=np.zeros(len(tags));V[terminal_nodes[0]]=1
    free=np.setdiff1d(np.arange(len(tags)),fixed)
    V[free]=spsolve(K[free][:,free],-(K[free][:,fixed]@V[fixed]))
    reaction=K@V;current=float(reaction[terminal_nodes[0]].sum())
    ground=float(reaction[terminal_nodes[1]].sum());assert current>0
    gradV=np.einsum('eki,ei->ek',grads,V[tet]);J=-sigma*gradV
    energy=float(np.sum(sigma*volume*np.einsum('ei,ei->e',gradV,gradV)))
    assert abs(energy-current)/current<1e-6,(energy,current)
    assert abs(current+ground)/current<1e-6,(current,ground)
    np.savez_compressed(out/'solution.npz',xyz_m=xyz,tetrahedra=tet,potential_V=V,
        centroid_m=nodes.mean(axis=1),J_A_m2_at1V=J,element_volume_m3=volume)
    result=dict(configuration_id=p['configuration_id'],phase=a.phase,method='Linear tetrahedral DC conduction FEM',
        input_step_sha256=hashlib.sha256(raw).hexdigest(),model_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        interface_sha256=hashlib.sha256(interface_raw).hexdigest(),
        gmsh_version=version,max_mesh_size_mm=a.h,nodes=len(tags),elements=len(tet),
        connected_mesh_components=int(n_components),terminal_faces=terminals,
        resistance_ohm_at20C=1/current,current_at1V_A=current,ground_current_A=ground,
        energy_at1V_W=energy,current_balance_relative_error=abs(current+ground)/current,
        energy_balance_relative_error=abs(energy-current)/current,
        copper_volume_m3=float(volume.sum()),resistivity_ohm_m=1.7e-8,
        potential_range_V=[float(V.min()),float(V.max())],wall_seconds=time.perf_counter()-started,
        limitations=['Uniform copper resistivity and perfect continuous CAD joints',
            'DC only; no skin/proximity/eddy-current or temperature coupling',
            'Zero-radius corner peak current densities require mesh/fillet interpretation',
            'Phase-A result cannot silently be assigned to other phases without a geometry check'])
    (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result),flush=True)
    (out/'model_capture.py').write_bytes(Path(__file__).read_bytes())
    (out/'interface_capture.json').write_bytes(interface_raw)

if __name__=='__main__':main()
