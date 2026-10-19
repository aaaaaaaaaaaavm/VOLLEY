from pathlib import Path
import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
H=Path(__file__).resolve().parent;O=H/"release";F=O/"figures";F.mkdir(exist_ok=True)
d=json.loads((O/"RESULTS.json").read_text())
plt.rcParams.update({"font.family":"DejaVu Sans","font.size":10,"axes.spines.top":False,"axes.spines.right":False,"svg.fonttype":"none","pdf.fonttype":42})
fig,ax=plt.subplots(1,2,figsize=(8.8,3.6))
for mass,color in [(5,"#315f7a"),(15,"#718d4a"),(40,"#aa582b")]:
    rows=[x for x in d["capture_cases"] if x["cartridge_kg"]==mass and x["assumed_stopping_m"]==.01 and x["pitch_rate_deg_s"]==0]
    ax[0].plot([x["relative_m_s"] for x in rows],[x["mean_energy_force_N"] for x in rows],"o-",label=f"{mass} kg cartridge",color=color)
ax[0].set(xlabel="Relative approach speed [m/s]",ylabel="Mean energy-equivalent force [N]",title="10 mm assumed stop · no rotation");ax[0].legend(fontsize=8)
for offset,color in [(.5,"#315f7a"),(2,"#718d4a"),(4,"#aa582b")]:
    rows=[x for x in d["insertion_cases"] if x["offset_mm"]==offset and x["radial_clearance_mm"]==5]
    ax[1].plot([x["angle_deg"] for x in rows],[x["remaining_mm"] for x in rows],"o-",label=f"{offset} mm offset",color=color)
ax[1].axhline(0,color="black",ls="--",lw=1);ax[1].set(xlabel="Angular insertion error [deg]",ylabel="Residual radial clearance [mm]",title="5 mm gap · assumed allowances");ax[1].legend(fontsize=8)
fig.tight_layout()
for ext in ["png","svg","pdf"]:fig.savefig(F/("replenishment."+ext),bbox_inches="tight")
