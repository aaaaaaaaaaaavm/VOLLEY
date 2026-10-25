"""Captive slide guides, nominal screw drives and independent cap locking pins."""
def build(b,xa,xf,zf,caps_open,fore_open):
    box,cyl,join,row=b.box,b.cyl,b.join,b.row
    fixed=[];parts=[];bores=[]
    def orient(shape,side):return shape if side>0 else b.reflected(shape)
    for u in [24,296.5]:
        for side in [-1,1]:
            dy=50 if caps_open else 0;x=xa+u
            rail=[box(20,96,6,x,58,zf+96)]
            for yy in [120,140]:
                rail.append(box(12,4,20,x+4,yy,zf+102).cut(cyl(2.1,4,x+10,yy,zf+114,(0,1,0))))
            rail += [box(25,8,2,x-5,61,zf+100),box(4,8,26,x-5,61,zf+96),box(25,8,2,x-5,61,zf+120)]
            rail_shape=join(rail).cut(cyl(1.6,54,x+3,63,zf+72))
            fixed.append(orient(rail_shape,side))
            bores.append(orient(cyl(1.6,54,x+3,63,zf+72),side))
            cap=join([box(20,24,6,x,42+dy,zf+102),box(8,6,12,x+6,62+dy,zf+106)])
            cap=cap.cut(cyl(2.1,8,x+10,61+dy,zf+114,(0,1,0)))
            cap=cap.cut(cyl(1.6,24,x+3,63+dy,zf+100))
            parts.append(row(f'Sled_cap_{u}_{side}',orient(cap,side),'aluminium','sled_gate','Tr4x1 driven captive slide with independent3mm positive locking pin'))
            parts.append(row(f'Sled_cap_screw_{u}_{side}',orient(cyl(2,90,x+10,56,zf+114,(0,1,0)),side),'steel','sled_latch_drive','Nominal4x1 drive; thread contact idealized'))
            pinz=zf+74 if caps_open else zf+100
            parts.append(row(f'Sled_cap_lockpin_{u}_{side}',orient(cyl(1.5,24,x+3,63,pinz),side),'steel','sled_latch_pin','Normally engaged spring plunger specification; retract26mm before cap motion'))
            parts.append(row(f'Sled_cap_motor_reference_{u}_{side}',orient(cyl(6,30,x+10,146,zf+114,(0,1,0)),side),'catalog','sled_catalog','Design allocation12mmODx30; purchased actuator and space qualification not selected',.03))
    for side in [-1,1]:
        dy=float(fore_open);x=xf+2
        # The keeper remains across the payload's positive-X corner until the
        # fixed ramp draws this integral rod/follower outward. No screw timing.
        keeper=join([box(6,8,8,x,42+dy,zf+4),
                     cyl(1.5,56,xf+5,50+dy,zf+8,(0,1,0)),
                     cyl(2.7,2,xf+5,54+dy,zf+8,(0,1,0))])
        parts.append(row(f'Sled_fore_keeper_{side}',orient(keeper,side),'steel','sled_gate',
            'Spring closed;12mm transverse stroke;inner edge42 closed/54 open;fixed50mm track ramp completes5mm before release'))
        rail=[box(10,42,4,x,54,zf-2)]
        for yy in [78,90]:
            rail.append(box(10,4,12,x,yy,zf+2).cut(cyl(1.6,4,xf+5,yy,zf+8,(0,1,0))))
        fixed.append(orient(join(rail),side))
        spring=cyl(2.5,22-dy,xf+5,56+dy,zf+8,(0,1,0)).cut(cyl(1.6,22-dy,xf+5,56+dy,zf+8,(0,1,0)))
        parts.append(row(f'Sled_fore_spring_reference_{side}',orient(spring,side),'steel','sled_latch_spring',
            'Annular spring envelope;closed preload5N;rate0.5N/mm;open force11N;22/10mm working lengths;wire/qualification selection separate',.002))
        follower=cyl(2,8,xf+5,106+dy,zf+6)
        # The follower is attached to the rod at an actual overlapping seat.
        parts[-2]['shape']=join([parts[-2]['shape'],orient(follower,side)])
    return parts,fixed,bores
