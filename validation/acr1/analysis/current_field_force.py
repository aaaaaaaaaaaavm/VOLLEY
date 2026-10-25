"""J×B using actual DC conduction FE current distributions and cuboid PM field."""
from pathlib import Path
import hashlib,json,math
import numpy as np
import finite_motor as model
ROOT=Path(__file__).resolve().parents[1]

def main():
    raw=(ROOT/'cad/PARAMETERS.json').read_bytes();p=json.loads(raw);field=model.make_field(p)
    x=.65;centre=(p['launch']['home_aft_x']+sum(p['magnetic']['array_active_relative_x'])/2)/1000+x
    coefficients=[];receipts=[]
    for phase,h in [('A',2),('B',3),('C',3)]:
        path=ROOT/'analysis/conduction'/('phase_'+phase)/('h'+str(h))
        data=np.load(path/'solution.npz');receipt=json.loads((path/'RESULT.json').read_text())
        points=data['centroid_m'];volume=data['element_volume_m3'];current=data['J_A_m2_at1V']/receipt['current_at1V_A']
        force=0.
        for start in range(0,len(points),4000):
            q=points[start:start+4000];j=current[start:start+4000]
            # Proper right-handed rotation: CADX=fieldX,CADZ=fieldY,CADY=-fieldZ.
            xyz=np.stack([q[:,0]-centre,q[:,2],-q[:,1]],axis=1)
            J=np.stack([j[:,0],j[:,2],-j[:,1]],axis=1)
            B=field.getB(xyz)
            force-=float(np.sum(np.cross(J,B)[:,0]*volume[start:start+4000]))
        coefficients.append(force)
        receipts.append({'phase':phase,'FE_result_sha256':hashlib.sha256((path/'RESULT.json').read_bytes()).hexdigest(),
            'solution_sha256':hashlib.sha256((path/'solution.npz').read_bytes()).hexdigest(),'phase_force_N_per_A':force})
        print(phase,force,flush=True)
    phases=np.array([0,-2*np.pi/3,2*np.pi/3]);amplitude=float(abs(np.sum(np.array(coefficients)*np.exp(1j*phases))))
    reference=model.amplitude(model.active_coefficients(field,p,x,(3,3,5))+model.return_coefficients(field,p,x,7,3))
    d={'configuration_id':p['configuration_id'],'CAD_parameter_sha256':hashlib.sha256(raw).hexdigest(),
        'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'displacement_m':x,'phases':receipts,
        'force_amplitude_N_per_peak_phase_A':amplitude,'uniform_bar_and_approximate_return_N_per_A':reference,
        'relative_difference':(amplitude-reference)/reference,
        'method':'Volume integration of actual linear-tetrahedron DC current density with analytic PM field at element centroids',
        'scope':'One interior station, all three actual connected phases. MeshesA2mm/B,C3mm. Not a transient electromagnetic or hardware test.',
        'limitations':['Centroid quadrature and linear current elements; sharp-corner current concentrations mesh dependent',
            'Detailed lead currents, AC skin/proximity and conductive/magnetic reaction omitted',
            'This cross-check does not replace the full position map or its stated uncertainty']}
    (ROOT/'analysis/CURRENT_FIELD_FORCE.json').write_text(json.dumps(d,indent=2)+'\n')
    (ROOT/'analysis/CURRENT_FIELD_INPUT.json').write_bytes(raw)
    print(json.dumps(d),flush=True)

if __name__=='__main__':main()
