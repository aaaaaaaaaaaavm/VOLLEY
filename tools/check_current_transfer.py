"""Check the locally held CT-01 and RPL-01 captured studies."""
from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1]
for name in ["captive_transfer_review","replenishment_feasibility","native_campaign_review"]:
    subprocess.run([sys.executable,str(R/"validation"/name/"check_capture.py")],check=True,cwd=R)
