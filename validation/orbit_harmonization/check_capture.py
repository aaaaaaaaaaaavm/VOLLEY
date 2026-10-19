"""Pure-Python independent arithmetic and hash checks of captured native histories."""

from pathlib import Path
import csv, json, hashlib, math

H = Path(__file__).resolve().parent
d = json.loads((H / "RESULTS.json").read_text())
g = [
    [float(x) for x in l.split()]
    for l in (H / "gmat_J2_continuous.txt").read_text().splitlines()
    if l.strip() and l.strip()[0].isdigit()
]
with (H / "orekit_matched_native.csv").open() as f:
    o = [[float(x) for x in r] for r in list(csv.reader(f))[1:]]
assert len(g) == len(o) == 2881 and g[0][0] == 0 and abs(g[-1][0] - 86400) < 1e-6
errors = []
for a, b in zip(g, o):
    assert abs(a[0] - b[0]) < 1e-8
    errors.append(math.sqrt(sum((1000 * a[i] - b[i]) ** 2 for i in range(1, 4))))
assert abs(max(errors) - d["max_gmat_orekit_position_m"]) < 1e-9
assert (
    d["max_gmat_orekit_position_m"] < 0.002 and d["max_orekit_step_refinement_m"] < 1e-5
)
for name, sha in json.loads((H / "MANIFEST.json").read_text())["files"].items():
    assert hashlib.sha256((H / name).read_bytes()).hexdigest() == sha, name
print(
    "PASS:2881 shared-epoch native rows,independent residual arithmetic and exact evidence hashes; no physical accuracy claim."
)
