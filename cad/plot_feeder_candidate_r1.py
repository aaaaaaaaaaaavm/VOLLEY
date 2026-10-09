"""Parameter-derived review section for the unselected R1 feeder candidate."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

ROOT=Path(__file__).resolve().parent
d=json.loads((ROOT/"FEEDER_CANDIDATE_R1.json").read_text())
g=json.loads((ROOT/"parameters.json").read_text())["groups"]
fig,ax=plt.subplots(figsize=(8.8,6.2),dpi=160)
half=d["external_width_mm"]/2
inner=d["internal_width_mm"]/2
ax.add_patch(Rectangle((-half,-207),2*half,914,fill=False,lw=2,ec="#334f5d",label="R1 enclosure outer envelope"))
ax.add_patch(Rectangle((-g["track"]["overall_width"]/2,-45),g["track"]["overall_width"],65,
                       facecolor="#b5c8d0",edgecolor="#496576",label="Gen5 track envelope"))
for side in (-1,1):
 y=side*190.5
 ax.add_patch(Rectangle((y-83,0),166,690,facecolor="#dde6e8",edgecolor="#437183",alpha=.75,
                        label="R1 open-side cassette" if side==1 else None))
 for i in range(6):
  z=26+104*i
  ax.add_patch(Rectangle((y-50,z),100,100,facecolor="#70afad",edgecolor="#176a70",alpha=.7))
ax.add_patch(Rectangle((-50,26),100,100,facecolor="#eda660",edgecolor="#a15d20",alpha=.75,label="3U release pose"))
ax.annotate("",xy=(0,596),xytext=(190.5,596),arrowprops=dict(arrowstyle="->",color="#ad4a30",lw=2))
ax.text(105,606,"side transfer",ha="center",color="#ad4a30",fontsize=8)
ax.annotate("",xy=(0,76),xytext=(0,596),arrowprops=dict(arrowstyle="->",color="#ad4a30",lw=2))
ax.text(-12,350,"central lift",ha="right",va="center",color="#ad4a30",fontsize=8)
ax.set(xlim=(-310,310),ylim=(-75,735),xlabel="Lateral y (mm)",ylabel="Vertical z (mm)",
       title="R1 feeder candidate section at payload station — geometry only")
ax.axvline(-inner,color="#334f5d",ls=":",lw=.8);ax.axvline(inner,color="#334f5d",ls=":",lw=.8)
ax.grid(alpha=.15);ax.legend(fontsize=7,loc="lower center",ncol=2,bbox_to_anchor=(.5,-.18))
fig.tight_layout()
for suffix in ("png","svg"):
 fig.savefig(ROOT.parent/"figures"/f"gen5_feeder_candidate_r1.{suffix}")
plt.close(fig)
print("R1 feeder section written; CAD-derived schematic, not a solver screenshot")
