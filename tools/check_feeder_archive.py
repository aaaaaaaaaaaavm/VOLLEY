"""Verify the standalone feeder archive and its repository-local reading copies.

Executes the dependency-free captured-evidence check, not FreeCAD or CalculiX.
"""

from pathlib import Path
import hashlib, json, subprocess, sys, tempfile, zipfile

R = Path(__file__).resolve().parents[1]
H = R / "validation/feeder_review"
p = H / "FEEDER_SOURCE_AND_CAD.zip"
d = json.loads((H / "ARCHIVE_RECORD.json").read_text())
assert hashlib.sha256(p.read_bytes()).hexdigest() == d["archive_sha256"]
for name, sha in d["reading_copies"].items():
    assert hashlib.sha256((H / name).read_bytes()).hexdigest() == sha, name
with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    assert sum(x.file_size for x in z.infolist()) < 200_000_000
    assert all(
        not Path(n).is_absolute() and ".." not in Path(n).parts for n in z.namelist()
    )
    with tempfile.TemporaryDirectory() as t:
        z.extractall(t)
        base = Path(t) / "experiments/feeder-design-review"
        subprocess.run([sys.executable, str(base / "check_capture.py")], check=True)
        for name in d["reading_copies"]:
            # Wrapper README adds standalone-reader navigation; other captured files match.
            if name != "README.md":
                assert (H / name).read_bytes() == (base / name).read_bytes(), name
print(
    "PASS: complete source/CAD archive and local reading copies; no live flagship dependency or hardware pass."
)
