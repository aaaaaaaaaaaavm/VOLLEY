"""Prepare English text/provenance and verify the rendered film without rerunning studies."""
from pathlib import Path
import hashlib,json,math,subprocess
import numpy as np
H=Path(__file__).resolve().parent
CUES=[(0, 5, 'A generic restart-capable upper stage supplies the coarse move from 500 km circular.'), (5, 10, 'A +27.42 m/s tangential burn enters the transfer ellipse.'), (10, 15, 'Coast for 47.82 minutes in the same orbital plane.'), (15, 20, 'A second +27.32 m/s burn circularizes the host at 600 km.'), (20, 25, 'At delivery, VOLLEY sets the relative release vector; the host supplies maneuver authority.'), (25, 30, 'Current ACR1 computations evaluate command points 1, 2 and 3 m/s.'), (30, 35, 'The 3 m/s command gives a modeled payload inertial kick of 2.92694 m/s.'), (35, 40, 'Retained sled motion and host recoil are included. The local schematic is not to scale.'), (40, 45, 'Compare the same 600 km host state with a representative 1 m/s passive spring.'), (45, 50, 'The 1 m/s P-POD-style example is a comparison choice, not a universal product rating.'), (50, 55, 'An ideal ground-preset spring can match the same kick and the same ideal trajectory.'), (55, 60, 'The 24-hour co-rotating zoom has separately scaled axes. It is not navigation accuracy.'), (60, 65, 'The 3 m/s command example creates a 600 by 610.82 km ellipse.'), (65, 70, 'Perigee remains at 600 km. The orbital period is about 96.80 minutes.'), (70, 75, 'A circle at apogee requires another propulsion event: about +2.926 m/s here.'), (75, 80, 'Coast follows the ellipse. Circularization requires a separate burn.'), (80, 84, '0.2 m/s is an illustration outside the current evaluated command points.'), (84, 88, 'Current modeled points are 1, 2 and 3 m/s. This view shows the 3 m/s command.'), (88, 92, 'About 16 m/s is a historical periodic-model result, not a current ACR1 rating.'), (92, 96, '1 km/s is future kinematic research, shown separately from the current rail.'), (96, 100, '3.5 km/s gives an unbound path: a future kinematic case, not current rail capability.')]

def stamp(t):return f'{int(t)//3600:02d}:{int(t)%3600//60:02d}:{int(t)%60:02d}.000'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    (H/'ENGLISH.vtt').write_text('WEBVTT\n\n'+''.join(f'{i+1}\n{stamp(a)} --> {stamp(b)}\n{s}\n\n' for i,(a,b,s) in enumerate(CUES)))
    text='# Orbital delivery and fair comparison — English transcript\n\n100 seconds,24 fps,1280×720,no audio. The VTT supplies timed English captions.\n\n'
    for a,b,s in CUES:text+=f'**{stamp(a)[:8]}–{stamp(b)[:8]}** {s}\n\n'
    (H/'TRANSCRIPT.md').write_text(text)
    physics=json.loads((H/'PHYSICS_RESULTS.json').read_text());cases={r['id']:r for r in physics['cases']}
    readme=f'''# VOLLEY orbital/comparison film chapter

26 October2026. Final: **VOLLEY_orbit_comparison_100s.mp4**. Five independently encoded20-second segments are in `segments/`. Delivery is1280×720,24fps,H.264/yuv420p,CRF20,without audio. RGB frames stream directly to ffmpeg; no raw frame series is retained. `ENGLISH.vtt`, `TRANSCRIPT.md`, `POSTER.png` and `CONTACT_SHEET.jpg` accompany the film.

## Scientific basis

This is a new bounded scientific illustration, not a rerun or revision of an accepted engineering study. `PHYSICS_RESULTS.json` pins the accepted source files and states every numerical convention. `TRAJECTORIES.npz` contains the actual planar position/velocity histories used by the renderer. Constants are Earth mu3.986004418e14m³/s² and reference sphere6378137m. All release examples begin from the same600km circular state and are tangential/in-plane.

The ideal500→600km Hohmann needs **27.420512m/s** followed by **27.321742m/s**, with **2869.496408s** transfer coast. A generic maneuverable restart-capable upper-stage host is a surrogate; no rocket/provider or actual engine/service is selected. The transfer is impulsive two-body illustration, not a finite-engine performance commitment.

Current ACR1's source-supported modeled command points are1,2 and3m/s. The illustrated3m/s command maps to a **2.926937159m/s** payload inertial kick after finite-host/sled accounting at the source mass snapshot. Its depicted new600km orbit has600km perigee,610.820178km apogee and96.799659min period. Wrapped relative Earth-centered azimuth after24h is−6.291574°. A second ideal2.926m/s-class burn is required to circularize at apogee. No mechanism for that later burn is assigned to the passive payload.

The passive spring example uses a declared1m/s payload-retained-host relative speed at620kg total mass, giving0.993548387m/s inertial kick. This is a representative P-POD-style comparator, not a universal product rating or supplier claim. The ideal ground-preset comparator uses{physics['ideal_preset_spring']['relative_speed_m_s']:.9f}m/s relative speed to match ACR1's same inertial kick. Its plotted trajectory overlaps exactly. No superiority over ideal pretrim is claimed. Actual complete installed-system comparison remains governed by accepted source results, not this illustrative graphic alone.

The low0.2m/s case is illustrative and outside the evaluated current points. The16.029m/s scenario uses a historical periodic-model value as a kinematic input and is not a current rating. Future1000m/s and3500m/s cases are distinct inertial-kick research scenarios; no current rail appears in these scenes. At1000m/s, apogee is{cases['future1000']['apogee_altitude_km']:.3f}km. At3500m/s, specific energy is positive and the path is unbound. Higher-speed scenes never imply present hardware achievement.

## Scale and display

Main orbit shapes preserve physical position ratios. Because metre-per-second changes produce tiny offsets at Earth-orbit scale, the film also uses an explicit altitude zoom and co-rotating position-difference plot. The latter projects payload minus unburned circular chief into the chief's instantaneous radial/along-track directions, with independent labelled axes. The two-body orbit circles/ellipses and their curves are computed, not arbitrary diagram paths.

The24h phase statistic is signed Earth-centered azimuth relative to the circular chief, wrapped to±180°. It is neither an unwrapped count of revolutions nor target/navigation accuracy. Future hyperbolic scenes show the first2h; bound scenes animate one actual orbital period, compressed into each four-second case. Actual playback time is illustrative time compression, with physical shapes preserved. The release-interface drawing is explicitly a local schematic, not scaled current CAD. The coarse transfer stays in one orbital plane; no plane change or corrected navigation accuracy is implied.

## Verification and reproduction

Eight numerical propagations use DOP853 and an independently solved elliptic/hyperbolic Kepler equation. Energy and angular momentum relative changes must be below1e−9; numerical/analytic positions agree below0.1m over24h. Checks also cover zero-kick circular behavior, exact equal-kick preset overlap, Hohmann apogee arrival, circularization speed and positive escape energy. `DELIVERY_CHECKS.json` records actual media/physics checks. These are numerical invariants, not physical validation.

```bash
OPENBLAS_NUM_THREADS=1 python3 physics.py --source-root /path/to/VOLLEY
OPENBLAS_NUM_THREADS=1 python3 orbit_film.py
python3 prepare_delivery.py
```

Scientific runtime:Python3.12,NumPy/SciPy,Pillow and ffmpeg. Font source:system DejaVu Sans/Bold. Renderer uses charcoal#11161c,off-white,teal current,gray spring andamber future. Key values use32–43px type; titles42px. Small axes/footers use24–28px. Sidecar English captions preserve fuller explanation. All source pin URLs are in PHYSICS_RESULTS; no third-party document,binary or image is redistributed. Accepted sources/PDFs are untouched.
'''
    (H/'README.md').write_text(readme)
    outputs=[H/'VOLLEY_orbit_comparison_100s.mp4']+sorted((H/'segments').glob('*.mp4'))
    media=[]
    for p in outputs:
        r=subprocess.run(['ffprobe','-v','error','-show_streams','-show_format','-of','json',str(p)],text=True,capture_output=True,check=True)
        actual=json.loads(r.stdout);v=next(s for s in actual['streams'] if s['codec_type']=='video')
        expected=100 if p.parent==H else 20
        assert v['width']==1280 and v['height']==720 and v['avg_frame_rate']=='24/1'
        assert int(v['nb_frames'])==expected*24 and abs(float(actual['format']['duration'])-expected)<.01
        assert not any(s['codec_type']=='audio' for s in actual['streams'])
        media.append(dict(file=str(p.relative_to(H)),width=v['width'],height=v['height'],fps=v['avg_frame_rate'],frames=int(v['nb_frames']),duration_s=float(actual['format']['duration']),audio=False,sha256=sha(p),bytes=p.stat().st_size))
    assert physics['all_checks_passed'] and len(physics['checks'])==8
    assert CUES[0][0]==0 and CUES[-1][1]==100 and all(a<b for a,b,s in CUES)
    assert all(CUES[i][1]==CUES[i+1][0] for i in range(len(CUES)-1))
    report=dict(passed=True,media=media,caption_cues=len(CUES),caption_span_s=100,
        physics=physics['checks'],readability_review='Full-size stills reviewed across all5 chapters; key type32px+,footers/axes24–28px; Earth/curve overlap removed in final layout; tiny offsets explicitly zoomed.',
        limiting_checks=['zero-kick circular','preset/current equal-kick exact overlap','ideal Hohmann arrival/circularization','3500m/s positive energy escape'],
        accepted_sources_modified=False,original_studies_rerun=False)
    (H/'DELIVERY_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
    files={str(p.relative_to(H)):{'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(H.rglob('*')) if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts}
    (H/'MANIFEST.json').write_text(json.dumps(dict(packet='VOLLEY-ORBIT-FILM-20261026',files=files),indent=2)+'\n')
    print('PASS:100s final;5×20s segments;2400 native24fps frames;1280×720;no audio;21 English cues;8 invariant-checked source-backed scenarios.')
if __name__=='__main__':main()
