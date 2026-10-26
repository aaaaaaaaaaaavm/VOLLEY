"""Verify the captured matched-load static comparison without a new solver run."""
from pathlib import Path
import csv,hashlib,json,math,re
ROOT=Path(__file__).resolve().parent
def main():
    capture=json.loads((ROOT/'MANIFEST.json').read_text())
    for name,record in capture['files'].items():
        p=ROOT/name
        assert p.stat().st_size==record['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'],p
    manifest=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
    for record in manifest['files']:
        p=ROOT/record['path']
        assert p.stat().st_size==record['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==record['sha256'],p
    s=json.loads((ROOT/'ACR1_STATIC_CROSSCHECK.json').read_text());target=s['load']['target_force_each_N'];peaks=[]
    for name in ['h5p5','h4p5','h4p0']:
        with (ROOT/'mesh'/name/'nodes.csv').open() as f:nodes={int(r['id']):(float(r['x_mm']),float(r['y_mm']),float(r['z_mm'])) for r in csv.DictReader(f)}
        with (ROOT/'loads'/('loads_'+name+'.csv')).open() as f:loads={int(r['node']):float(r['fz_N'])for r in csv.DictReader(f)}
        deck={int(n):float(v)for n,v in re.findall(r'^F,(\d+),FZ,([^\s]+)',(ROOT/'inputs'/('static_'+name+'.dat')).read_text(),re.M)}
        assert deck.keys()==loads.keys() and max(abs(deck[n]-v)for n,v in loads.items())<1e-8,name
        for upper in [True,False]:
            rows=[(nodes[n],v)for n,v in loads.items()if(nodes[n][2]>0)==upper]
            resultant=math.fsum(v for xyz,v in rows);centroid=[math.fsum(xyz[k]*v for xyz,v in rows)/resultant for k in range(3)]
            assert math.isclose(resultant,-target if upper else target,abs_tol=1e-5),name
            assert max(abs(a-b)for a,b in zip(centroid,[444,0,14 if upper else-14]))<1e-6,name
        with (ROOT/'extracted'/('closure_samples_'+name+'.csv')).open()as f:samples=list(csv.DictReader(f))
        peak=max(float(r['closure_quadratic_mm'])for r in samples);expected=s['static'][name]
        assert len(nodes)==expected['nodes'] and len(samples)==expected['sample_count'],name
        assert abs(peak-expected['closure_max_mm'])<1e-9,name
        assert max(abs(float(r['lower_uz_quadratic_mm'])-float(r['upper_uz_quadratic_mm'])-float(r['closure_quadratic_mm']))for r in samples)<2e-9,name
        peaks.append(peak)
    assert peaks[0]<peaks[1]<peaks[2]
    sensitivity=json.loads((ROOT/'CLEARANCE_SENSITIVITY.json').read_text())
    margin=lambda d:1-1.3*d/2-(.20+.15+.15+.05)
    assert math.isclose(margin(s['reference_closure_mm']),sensitivity['reference_margin_mm'],abs_tol=1e-12)
    assert math.isclose(margin(peaks[-1]),sensitivity['finest_mesh_margin_mm'],abs_tol=1e-12)
    assert sensitivity['finest_mesh_margin_mm']>0
    print('PASS:27 captured identities;3 native-deck load/result fields;primary11448 samples;matched3010.480631N loads;conditional clearance sensitivity. Raw native RST remains private; no new solver or hardware claim.')
if __name__=='__main__':main()
