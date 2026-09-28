"""Focused reproducibility and physical-limit checks; no external publication."""
import subprocess,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
for args in (["analysis/mission_cartridges.py","--check"],
             ["analysis/finite_burn_departure.py","--check"],
             ["analysis/manifest_finite_burn.py","--check"],
             ["analysis/lunar_gravity_check.py","--check"],
             ["analysis/test_article_requirements.py","--check"],
             ["analysis/installed_trade.py","--check"],
             ["analysis/instrument_r1.py","--check"],
             ["-m","unittest","discover","-s","tests","-p","test_mc_l2_bench.py"],
             ["-m","unittest","discover","-s","tests","-p","test_continuation_s5_s11.py"]):
    subprocess.run([sys.executable,*args],cwd=root,check=True)
print("PASS: focused local continuation checks; full programme remains open")
