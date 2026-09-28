"""C0-S3A: independent potential-gradient check of archived lunar harmonics."""
import argparse
import hashlib
import json
import math
from pathlib import Path

import numpy as np
import pyshtools

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT/'validation/data/lunar'
OUT = ROOT/'analysis/results/lunar_gravity_check.json'
DOC = ROOT/'docs/LUNAR_GRAVITY_VALIDATION.md'


def load():
    manifest = json.loads((DATA/'grgm1200a_manifest.json').read_text())
    raw = (DATA/'grgm1200a_degree200.tab').read_bytes()
    if hashlib.sha256(raw).hexdigest()!=manifest['subset_sha256']:
        raise ValueError('COEFFICIENT_HASH_MISMATCH')
    lines = raw.decode().splitlines()
    header = [float(x) for x in lines[0].split(',')]
    rows = np.loadtxt(lines[1:],delimiter=',')
    pairs = [(int(r[0]),int(r[1])) for r in rows]
    expected = [(n,m) for n in range(1,201) for m in range(n+1)]
    if pairs != expected or not np.isfinite(rows).all():
        raise ValueError('INCOMPLETE_OR_INVALID_COEFFICIENTS')
    if header[0]!=1738. or header[3:6]!=[1200.,1200.,1.]:
        raise ValueError('UNEXPECTED_MODEL_HEADER')
    c = np.zeros((2,201,201));c[0,0,0]=1.
    for row in rows:
        n,m=map(int,row[:2]);c[:,n,m]=row[2:4]
    return c,header[1],header[0],manifest


def potential(position,c,gm,r0,degree):
    x,y,z=np.asarray(position)
    r=np.linalg.norm(position);s=z/r;cl=math.hypot(x,y)/r;lon=math.atan2(y,x)
    p=np.zeros((degree+1,degree+1));p[0,0]=1.
    if degree:p[1,1]=math.sqrt(3)*cl
    for m in range(2,degree+1):
        p[m,m]=math.sqrt((2*m+1)/(2*m))*cl*p[m-1,m-1]
    for m in range(degree):p[m+1,m]=math.sqrt(2*m+3)*s*p[m,m]
    for m in range(degree+1):
        for n in range(m+2,degree+1):
            a=math.sqrt((2*n-1)*(2*n+1)/((n-m)*(n+m)))
            b=math.sqrt((2*n+1)*(n+m-1)*(n-m-1)/((2*n-3)*(n-m)*(n+m)))
            p[n,m]=a*s*p[n-1,m]-b*p[n-2,m]
    orders=np.arange(degree+1)
    trig=c[0,:degree+1,:degree+1]*np.cos(orders*lon)+c[1,:degree+1,:degree+1]*np.sin(orders*lon)
    return gm/r*float(np.sum((r0/r)**orders*np.sum(p*trig,axis=1)))


def gradient(position,c,gm,r0,degree,step):
    result=[]
    for axis in np.eye(3):
        f=lambda t:potential(position+t*axis,c,gm,r0,degree)
        result.append((-f(2*step)+8*f(step)-8*f(-step)+f(-2*step))/(12*step))
    return np.array(result)


def reference(position,c,gm,r0,degree):
    r=float(np.linalg.norm(position));lat=math.asin(position[2]/r);lon=math.atan2(position[1],position[0])
    ar,at,ap=pyshtools.gravmag.MakeGravGridPoint(c,gm,r0,r,math.degrees(lat),math.degrees(lon),lmax=degree,omega=0.)
    er=np.array([math.cos(lat)*math.cos(lon),math.cos(lat)*math.sin(lon),math.sin(lat)])
    et=np.array([math.sin(lat)*math.cos(lon),math.sin(lat)*math.sin(lon),-math.cos(lat)])
    ep=np.array([-math.sin(lon),math.cos(lon),0.])
    return ar*er+at*et+ap*ep


def source_hashes():
    files=['analysis/lunar_gravity_check.py','validation/C0_S3A_gravity_ingestion.md',
           'validation/data/lunar/grgm1200a_manifest.json','validation/data/lunar/grgm1200a_degree200.tab',
           'validation/data/lunar/gggrx_1200a_sha.lbl']
    return {p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}


def report(d):
    return '\n'.join(['# Archived lunar gravity force validation — C0-S3A','',
        'Adityavardhan Mishra · 26 September 2026','',
        f"The complete GRGM1200A table was downloaded ({d['archive']['source_bytes']:,} bytes) and hashed. An exact degree/order-200 prefix and PDS label are retained with the reproducible retrieval URL. The parser validates all {d['archive']['subset_records']:,} coefficient records through degree 200.",'',
        f"An independently coded normalized Legendre potential and five-point Cartesian derivative were compared against SHTOOLS at twenty off-axis points, three degree limits and two derivative step sizes: {len(d['comparisons'])} comparisons. Maximum relative vector error: {max(r['relative_error'] for r in d['comparisons']):.3e}; limit 1e-8. Central-field check maximum: {max(d['central_errors']):.3e}; limit 1e-10.",'',
        f"Force-check disposition: {'PASS' if d['passed'] else 'FAIL'}. Units are km, seconds, km³/s² and km/s² consistently; no centrifugal term is included.",'',
        f"The coefficient header gives GM={d['gm_km3_s2']:.13f} km³/s² and radius={d['reference_radius_km']:g} km. The earlier contract quoted GM=4902.80011526323 from metadata. These differ; this force check uses the table header with its own coefficients, and preserves the earlier contract. Orientation compatibility and the discrepancy must be reviewed before a mission propagation.",'',
        'This validates local gravity evaluation only. No 90-day orbit, DE430 orientation, Earth/Sun perturbation, surface access, SRP bound or lunar lifetime has been validated. The C0-S3 mission gate remains open.','',
        '[Criteria](../validation/C0_S3A_gravity_ingestion.md) · [Full comparisons](../analysis/results/lunar_gravity_check.json) · [Data manifest](../validation/data/lunar/grgm1200a_manifest.json)',''])


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    c,gm,r0,archive=load()
    if args.check:
        d=json.loads(OUT.read_text());assert d['source_sha256']==source_hashes(),'STALE_SOURCE'
        assert DOC.read_text()==report(d),'STALE_REPORT'
        assert len(d['comparisons'])==120 and len(d['central_errors'])==20
        for row in d['comparisons']:
            pos=np.array(row['position_km']);degree=row['degree'];step=row['step_km']
            ref=reference(pos,c,gm,r0,degree)
            own=gradient(pos,c,gm,r0,degree,step)
            assert np.linalg.norm(own-ref)/np.linalg.norm(ref)<=1e-8,'FORCE_RECHECK_FAILED'
            assert np.linalg.norm(ref-np.array(row['reference_km_s2']))/np.linalg.norm(ref)<=1e-12,'REFERENCE_DRIFT'
    else:
        points=[]
        for radius in (1838.,2738.):
            for j in range(10):
                lat=math.radians(-75+150*j/9);lon=math.radians(17+36*j)
                points.append(radius*np.array([math.cos(lat)*math.cos(lon),math.cos(lat)*math.sin(lon),math.sin(lat)]))
        rows=[];central=[]
        for p in points:
            exact=-gm*p/np.linalg.norm(p)**3
            central.append(float(np.linalg.norm(gradient(p,c,gm,r0,0,.1)-exact)/np.linalg.norm(exact)))
            for degree in (100,150,200):
                ref=reference(p,c,gm,r0,degree)
                for step in (.1,.05):
                    own=gradient(p,c,gm,r0,degree,step)
                    error=float(np.linalg.norm(own-ref)/np.linalg.norm(ref))
                    rows.append(dict(position_km=p.tolist(),degree=degree,step_km=step,
                                     reference_km_s2=ref.tolist(),independent_km_s2=own.tolist(),relative_error=error))
        d=dict(study='C0-S3A',archive=archive,gm_km3_s2=gm,reference_radius_km=r0,
               source_sha256=source_hashes(),runtime=dict(numpy=np.__version__,pyshtools=pyshtools.__version__),
               comparisons=rows,central_errors=central,passed=bool(max(central)<=1e-10 and all(r['relative_error']<=1e-8 for r in rows)))
        OUT.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');DOC.write_text(report(d))
    print({'passed':d['passed'],'comparisons':len(d['comparisons']),'maximum_relative_error':max(r['relative_error'] for r in d['comparisons'])})
    assert d['passed'],'FORCE_VALIDATION_FAILED'
