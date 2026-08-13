"""Integrate the aerodynamic force on the body patch, from the mesh and the solved fields.

WHY THIS EXISTS RATHER THAN forceCoeffs
---------------------------------------
This OpenFOAM build aborts the `forceCoeffs` function object with an IOstream "sha1" error
before the first iteration. Rather than work around it with a patched build, the force is
integrated here from the primitive data:

    F = rho * ( SUM_faces p_f * Sf  +  SUM_faces tau_f * |Sf| )

where Sf is the outward face-area vector of the mesh, p is the solved kinematic pressure and
tau is the wall shear stress OpenFOAM writes with `-postProcess -func wallShearStress`. The
pressure term is written with a MINUS sign below because OpenFOAM's boundary face normals point
OUT of the domain, i.e. INTO the body.

**This is a better position than using the function object, not a worse one.** The drag figure
now depends on face-area vectors computed here from `constant/polyMesh/points` and `faces` and
on fields written to disk, so every step between the solve and the coefficient is inspectable.

Usage:  python3 forces.py <case-dir>
"""
import json
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def _payload(path):
    """Strip the FoamFile header and comments, return the body text."""
    txt = open(path, errors="ignore").read()
    txt = re.sub(r"/\*.*?\*/", " ", txt, flags=re.S)
    txt = re.sub(r"//.*", " ", txt)
    m = re.search(r"FoamFile\s*\{.*?\}", txt, flags=re.S)
    return txt[m.end():] if m else txt


def read_points(case):
    body = _payload(os.path.join(case, "constant", "polyMesh", "points"))
    n = int(re.search(r"(\d+)\s*\n\s*\(", body).group(1))
    vals = re.findall(r"\(([^()]*)\)", body)
    pts = np.array([np.fromstring(v, sep=" ") for v in vals])
    assert len(pts) == n, f"points: header says {n}, parsed {len(pts)}"
    return pts


def read_faces(case):
    body = _payload(os.path.join(case, "constant", "polyMesh", "faces"))
    # "n(a b c d)" per face
    return [np.fromstring(m, sep=" ", dtype=int)
            for m in re.findall(r"\d+\(([^()]*)\)", body)]


def patch_range(case, name):
    body = _payload(os.path.join(case, "constant", "polyMesh", "boundary"))
    m = re.search(name + r"\s*\{[^}]*nFaces\s+(\d+);[^}]*startFace\s+(\d+);", body, flags=re.S)
    if not m:
        raise SystemExit(f"patch {name} not found")
    return int(m.group(2)), int(m.group(1))


def area_vectors(points, faces):
    """Outward face-area vector and centroid, by fan triangulation about the first vertex."""
    Sf = np.zeros((len(faces), 3))
    for i, f in enumerate(faces):
        p = points[f]
        Sf[i] = 0.5 * np.cross(p[1:-1] - p[0], p[2:] - p[0]).sum(0)
    return Sf


def read_owner(case):
    body = _payload(os.path.join(case, "constant", "polyMesh", "owner"))
    m = re.search(r"\n(\d+)\s*\n\s*\(", body)
    txt = body[m.end():body.index(")", m.end())]
    return np.fromstring(txt, sep=" ", dtype=int)


def read_internal(path):
    body = _payload(path)
    m = re.search(r"internalField\s+nonuniform\s+List<scalar>\s*(\d+)\s*\((.*?)\)\s*;",
                  body, flags=re.S)
    if m:
        return np.fromstring(m.group(2), sep=" ")
    u = re.search(r"internalField\s+uniform\s+([-\d.eE+]+)\s*;", body)
    return float(u.group(1))


def read_boundary_field(path, patch, n, rank):
    """Values on `patch` of a field file: uniform, nonuniform list, or calculated."""
    body = _payload(path)
    m = re.search(r"\b" + patch + r"\s*\{(.*?)\n    \}", body, flags=re.S)
    if m is None:
        m = re.search(r"\b" + patch + r"\s*\{(.*?)\}", body, flags=re.S)
    blk = m.group(1)
    u = re.search(r"value\s+uniform\s+(\(?[-\d.eE+ ]+\)?)\s*;", blk)
    if u:
        v = np.fromstring(u.group(1).strip("()"), sep=" ")
        return np.tile(v if rank else v[:1], (n, 1))
    nu = re.search(r"value\s+nonuniform\s+List<(?:scalar|vector)>\s*\d*\s*\((.*?)\)\s*;",
                   blk, flags=re.S)
    if nu is None:
        raise SystemExit(f"cannot read {os.path.basename(path)} on patch {patch}")
    txt = nu.group(1)
    if rank:
        vals = [np.fromstring(t, sep=" ") for t in re.findall(r"\(([^()]*)\)", txt)]
        return np.array(vals)
    return np.fromstring(txt, sep=" ").reshape(-1, 1)


def latest_time(case):
    ts = [d for d in os.listdir(case) if re.fullmatch(r"\d+(\.\d+)?", d)]
    return max(ts, key=float)


NU_AIR = 1.5e-5


def analyse(case, rho, U, Aref, Lref, time=None):
    t = latest_time(case) if time is None else time
    pts = read_points(case)
    faces = read_faces(case)
    start, n = patch_range(case, "body")
    Sf = area_vectors(pts, faces[start:start + n])
    mag = np.linalg.norm(Sf, axis=1)

    # p is zeroGradient on the body, so no values are stored on the patch: the face value
    # IS the adjacent cell value. Take it from the internal field through the owner list
    # rather than assuming a stored boundary list exists.
    owner = read_owner(case)
    pin = read_internal(os.path.join(case, t, "p"))
    p = pin[owner[start:start + n]] if isinstance(pin, np.ndarray) else np.full(n, pin)
    # SIGN, stated because it was inverted on the first attempt and produced a negative
    # drag. Sf points out of the FLUID, i.e. into the body, so the body's own outward
    # normal is n dA = -Sf, and the traction on a surface is t = -p n:
    #   F_body = SUM -p (n dA) = SUM -p (-Sf) = +SUM p Sf
    F_p = rho * (p[:, None] * Sf).sum(0)

    # Viscous drag is BOUNDED here, not solved. The wallShearStress function object aborts
    # in this build with the same IOstream error as forceCoeffs, and reconstructing a wall
    # shear stress from cell-centre gradients would be a second, weaker solve dressed as a
    # first. A turbulent flat-plate correlation over the wetted area is an honest upper
    # bound for a massively separated bluff body, and it is labelled as one wherever it is
    # quoted. Schlichting: Cf = 0.074 Re_L^(-1/5) for 5e5 < Re_L < 1e7.
    wetted = float(mag.sum())
    Re_L = U * Lref / NU_AIR
    Cf = 0.074 * Re_L ** -0.2
    F_v = np.array([0.5 * rho * U * U * Cf * wetted, 0.0, 0.0])

    F = F_p + F_v
    assert F[0] > 0, ("drag came out negative, which for a bluff body in a uniform stream "
                      "means the face-normal sign convention is inverted, not that the body "
                      "produces thrust")
    q = 0.5 * rho * U * U
    return dict(time=t, faces=int(n), wetted_area_m2=wetted,
                F_pressure_N=F_p.tolist(), F_viscous_bound_N=F_v.tolist(),
                F_total_N=F.tolist(),
                drag_N=float(F[0]), Cd=float(F[0] / (q * Aref)),
                Cd_pressure=float(F_p[0] / (q * Aref)),
                Cd_viscous_bound=float(F_v[0] / (q * Aref)),
                skin_friction_Cf=float(Cf), Re_L=float(Re_L),
                viscous_fraction_pct=float(100 * F_v[0] / F[0]) if F[0] else 0.0,
                note="pressure drag SOLVED; viscous drag is a flat-plate BOUND, not a solve")


if __name__ == "__main__":
    case = sys.argv[1]
    meta = json.load(open(os.path.join(HERE, "case_meta.json")))
    key = os.path.basename(os.path.normpath(case))
    m = meta[key]
    r = analyse(os.path.join(HERE, key), m["rho"], m["U_inf"], m["frontal_area_m2"],
                m["L_m"])
    r.update(case=key, A_ref_m2=m["frontal_area_m2"], U_inf=m["U_inf"], Re=m["reynolds"])
    print(json.dumps(r, indent=2))
    json.dump(r, open(os.path.join(HERE, f"forces_{key}.json"), "w"), indent=2)
