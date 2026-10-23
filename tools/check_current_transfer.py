"""Verify the repository-local captured mechanical and system studies."""
from pathlib import Path
import subprocess,sys
R=Path(__file__).resolve().parents[1]
for name in ["feeder_actuation_review","captive_transfer_review","replenishment_feasibility","native_campaign_review","feeder_rotary_clearance","feeder_contact_diagnosis","extended_feasibility_bounds","feeder_common_boundary","selected_feeder","system_feasibility_closure","lunar_native_coast"]:
    subprocess.run([sys.executable,str(R/"validation"/name/"check_capture.py")],check=True,cwd=R)
