"""FM-01 common custody hypothesis. Millimetres; FreeCAD exact solids.

Gate crossbolt and fork-carried blocking strip are physical geometry. The
receiving restraints belong to a connected sled, rather than a Boolean external
support. Actuation, contact stiffness and qualification remain separate checks.
"""
from dataclasses import dataclass, replace
from pathlib import Path
import sys
import FreeCAD as App
import Part
sys.path.insert(0, str(Path(__file__).parent/'reference'))
from ct_geometry import boxes, State as OldState

REVISION='FM-01'
@dataclass(frozen=True)
class State:
    feed: float=0
    gate: float=0
    bolt: float=32  # withdrawn by32; zero means inserted
    receiver: float=120
    front: float=0
    payload_feed: float=0
    sled: float=0

def cycle():
    return [
      ('stored',State()),
      ('gate_open',State(gate=120)),
      ('bolt_inserted',State(gate=120,bolt=0)),
      ('transfer',State(feed=200,gate=120,bolt=0,payload_feed=200)),
      ('sled_captured',State(feed=200,gate=120,bolt=0,receiver=0,payload_feed=200)),
      ('fork_open',State(feed=200,gate=120,bolt=0,receiver=0,front=105,payload_feed=200)),
      ('fork_home',State(gate=120,bolt=0,receiver=0,front=105,payload_feed=200)),
      ('bolt_withdrawn',State(gate=120,receiver=0,front=105,payload_feed=200)),
      ('cell_closed',State(receiver=0,front=105,payload_feed=200)),
      ('fork_reset',State(receiver=0,payload_feed=200)),
      ('sled_translation',State(receiver=0,payload_feed=200,sled=80)),
      ('sled_return',State(receiver=0,payload_feed=200)),
    ]

def interpolate(a,b,f):
    return State(**{k:getattr(a,k)+(getattr(b,k)-getattr(a,k))*f for k in a.__dataclass_fields__})

def B(d,p):return Part.makeBox(*d,App.Vector(*p))
def C(r,l,p,axis=(0,1,0)):return Part.makeCylinder(r,l,App.Vector(*p),App.Vector(*axis))
def fuse(parts):return parts[0].multiFuse(parts[1:]).removeSplitter() if len(parts)>1 else parts[0]

def shapes(L,s):
    def far_side(sh):
        return sh.mirror(App.Vector(L/2,0,0),App.Vector(1,0,0))
    groups={};meta={}
    old=OldState(feed=s.feed,storage_lift=s.gate,receiver_lift=s.receiver,front_lift=s.front,payload_feed=s.payload_feed,payload_exit=s.sled)
    for b in boxes(L,old):
        n=b['name'];d=b['size'][:];p=b['lo'][:]
        if n.startswith('receiver_'):continue
        if n=='support_floor' and p[1]>=-95:continue # receiver is now a moving sled
        # Open 1.5mm between the fork rear surfaces and the receiver capture bar.
        if n=='fork_body' and d[1]==3 and p[1]==-204+s.feed:p[1]-=2
        if n=='fork_body' and d[1]==4 and d[2]==5 and p[1]==-95+s.feed:
            continue # U-frame: closed front crossmember obstructed latch withdrawal.
        groups.setdefault(n,[]).append(B(d,p));meta[n]=(b['material'],b['role'])
    ss={n:fuse(v) for n,v in groups.items()}
    def add(n,sh,mat='aluminium',role='fixed'):
        ss[n]=sh;meta[n]=(mat,role)
    # Outboard gate wing: through-bored for a six-millimetre form-locking crossbolt.
    wing=fuse([B((10,12,20),(-65,-97,91-s.gate)),B((66,12,4),(-65,-97,107-s.gate)),B((4,12,43),(-3,-97,91-s.gate))])
    wing=wing.cut(C(3.2,68,(-66,-91,95-s.gate),(1,0,0)))
    ss['storage_gate']=ss['storage_gate'].fuse(far_side(wing)).removeSplitter()
    window=far_side(B((68,14,145),(-66,-98,0)))
    for n in ['support_floor','cassette_L_'+str(L+4)]:
        ss[n]=ss[n].cut(window).removeSplitter()
    far_wall='cassette_L_'+str(L+4)
    arch=[B((4,10,4),(L+4,yy,124)) for yy in [-108,-84]]+[B((4,34,4),(L+4,-108,128))]
    ss[far_wall]=ss[far_wall].multiFuse(arch).removeSplitter()
    # Crossbolt guide: two cheeks provide an identified, double-support load path.
    guide=fuse([B((10,24,20),(-82,-103,-12)),B((10,24,20),(-47,-103,-12)),B((45,24,5),(-82,-103,-17))])
    guide=guide.cut(C(3.15,47,(-83,-91,-2),(1,0,0)))
    # Gate travels in the gap between the cheeks; remove its swept wing material.
    guide=guide.cut(B((29,14,30),(-72,-98,-12))).removeSplitter()
    guide.translate(App.Vector(0,0,-23))
    add('gate_bolt_guide',far_side(guide),'steel')
    bolt=C(3,48,(-84-s.bolt,-91,-25),(1,0,0)).fuse(C(5,6,(-90-s.bolt,-91,-25),(1,0,0)))
    add('gate_crossbolt',far_side(bolt.removeSplitter()),'steel','crossbolt')
    # Carried strip blocks bolt-head withdrawal after the first2mm of feed.
    # A3mm nominal head-to-strip gap permits limited lost motion, not bolt release.
    strip=B((4,204,10),(-97,-302+s.feed,-30))
    leg=B((5,16,169),(-122,-224+s.feed,-30))
    web=B((29,16,5),(-122,-224+s.feed,-30))
    upper=B((108,16,5),(-122,-224+s.feed,134))
    ss['fork_body']=ss['fork_body'].multiFuse([far_side(x) for x in [strip,leg,web,upper]]).removeSplitter()
    # Source-sized3242drive envelope; ACT-01 supplies the full catalogue screen.
    axis=(-94,0,70)
    def CY(r,l,y):return C(r,l,(-94,y,70))
    add('motor_3242_envelope',CY(16,44.2,-339.2),'catalogue','drive')
    add('motor_shaft_envelope',CY(2.5,13,-295),'steel','drive')
    add('shaft_extension',CY(5,29,-279),'steel','drive')
    add('screw_major_envelope',CY(5,295,-250),'steel','drive')
    add('coupling_envelope',CY(8,13,-285).cut(CY(2.55,6,-285).fuse(CY(5.05,7,-279))),'aluminium','drive')
    add('bearing_housing',B((32,24,32),(-110,-266,54)).cut(CY(12.1,24,-266)))
    for n,y in [('A',-262),('B',-253)]:add('bearing_ring_'+n,CY(12,9,y).cut(CY(5.05,9,y)),'steel')
    for n,y in [('A',-264),('B',-244)]:add('shaft_collar_'+n,CY(6,2,y).cut(CY(5.05,2,y)),'steel')
    yn=-225.55+s.feed
    add('nut_SB3700_envelope',CY(9.55,19.1,yn).cut(CY(5.2,19.1,yn)),'catalogue','drive')
    cage=B((28,23.1,28),(-108,yn-2,56)).cut(CY(9.65,19.1,yn)).cut(CY(5.2,23.1,yn-2))
    arm=B((64,16,5),(-108,-224+s.feed,63)).cut(CY(9.65,23.1,yn-2))
    ss['fork_body']=ss['fork_body'].multiFuse([cage,arm]).removeSplitter()
    add('drive_mount',B((6,66,38),(-116,-276,16)).fuse(B((104,8,6),(-116,-216,16))))
    add('motor_mount_envelope',B((40,5,40),(-114,-295,50)).cut(CY(8.05,5,-295)))
    # Receiver restraints and support now move with a single identifiable sled.
    # Rail contact bands are envelope assumptions pending an actual payload ICD.
    xx=s.sled
    base=B((L+28,114,6),(-14+xx,-7,10))
    rails=[B((L+4,10,6),(-2+xx,yy,16)) for yy in [0,90]]
    backstop=B((2,82,18),(-3+xx,10,22))
    farrail=B((L+8,2,14),(-4+xx,101,22))
    towers=[B((8,5,112),(x+xx,103,16)) for x in [5,L-13]]
    caps=[B((8,108,4),(x+xx,0,124)) for x in [5,L-13]]
    add('sled_body',fuse([base,backstop,farrail]+rails+towers+caps),'aluminium','sled')
    # Passive front Xstop and rear/Y capture frame. Both are material, not signals.
    frontstop=B((2,82,18),(L+1+xx,10,22))
    add('sled_front_stop',frontstop,'steel','sled')
    dogs=[B((8,1,124),(x+xx,-1.5,22+s.receiver)) for x in [5,L-13]]
    bar=B((L-10,6,5),(5+xx,-6,144+s.receiver))
    arms=[B((8,123,5),(x+xx,-6,144+s.receiver)) for x in [5,L-13]]
    carriages=[B((8,6,16),(x+xx,111,134+s.receiver)) for x in [5,L-13]]
    add('sled_entry_bar',fuse(dogs+[bar]+arms+carriages),'steel','sled_entry')
    # The rear-bar vertical guide remains connected to the sled through two tubes.
    for i,x in enumerate([5,L-13]):
        tube=B((12,9,254),(x-2+xx,110,16)).cut(B((8.4,7.2,142),(x-.2+xx,109.9,130)))
        tube=tube.fuse(B((12,2,6),(x-2+xx,108,16))).removeSplitter()
        # Leave the full side-feed aperture clear: towers are beyond the fork Xbands.
        add('sled_bar_guide_'+str(i),tube,'aluminium','sled')
    # Stipulated launcher guide shoes attached to the sled, using two captive C rails.
    for i,yy in enumerate([18,76]):
        shoe=B((L+8,10,6),(-4+xx,yy,2))
        bridge=B((L+8,4,2),(-4+xx,yy+3,8))
        add('sled_guide_shoe_'+str(i),shoe.fuse(bridge).removeSplitter(),'steel','sled')
        track=fuse([B((L+140,18,3),(-20,yy-4,-2)),B((L+140,3,9),(-20,yy-4,1)),B((L+140,3,9),(-20,yy+11,1)),B((L+140,3,2),(-20,yy-1,8)),B((L+140,3,2),(-20,yy+8,8))])
        add('launcher_guide_'+str(i),track,'steel')
    return ss,meta
