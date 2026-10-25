"""Captive vertical transfer cradle; all coordinates derive from the controlled assembly."""
def build(b,floor=46,keepers_open=False,fork_withdraw=0,incoming_side=None,grips_open=False):
    box,cyl,tube,join,row=b.box,b.cyl,b.tube,b.join,b.row
    XA,XF=b.XA,b.XF;pp=[];left=XA-134;right=XF+140;ys=[-200,220]
    fixed=[]
    for x in [left,right]:
        for y in ys:fixed.append(tube(20,20,1240,3,x-10,y-10,-150))
        fixed.append(box(20,440,20,x-10,-210,1060))
    for y in ys:fixed.append(box(right-left+20,20,20,left-10,y-10,1060))
    sx=left-60
    for y in ys:
        screw=join([cyl(8,1100,sx,y,-100),cyl(6,20,sx,y,-120),cyl(6,38,sx,y,1000)])
        pp.append(row('Lift_Tr16x4_screw_'+str(y),screw,'steel','lift_drive','16x4 nominal screw;12mm journals; source-backed rating separate'))
        for zz in [-114,1006]:
            bearing=cyl(14,8,sx,y,zz).cut(cyl(6.1,8,sx,y,zz))
            pp.append(row('Lift_bearing_'+str(y)+'_'+str(zz),bearing,'steel','lift_fixed','6001 nominal12x28x8 bearing envelope'))
            fixed += [box(36,36,12,sx-18,y-18,zz-2).cut(cyl(14.1,12,sx,y,zz-2)),box(60,16,12,sx,y-8,zz-2)]
        fixed += [box(12,20,46,left-6,y-10,1014),box(12,20,24,left-6,y-10,-138)]
        pp.append(row('Lift_sync_pulley_'+str(y),cyl(18,6,sx,y,1030).cut(cyl(6.1,6,sx,y,1030)),'aluminium','lift_drive'))
    belt=[box(2,420,6,sx-20,-200,1030),box(2,420,6,sx+18,-200,1030)]
    for y,upper in [(-200,False),(220,True)]:
        ring=cyl(20,6,sx,y,1030).cut(cyl(18,6,sx,y,1030))
        belt.append(ring.common(box(50,25,8,sx-25,y if upper else y-25,1029)))
    pp.append(row('Lift_sync_belt',join(belt),'polymer','lift_drive','Twin-screw synchronization; teeth/tension rating separate'))
    pp.append(row('Lift_holding_brake_reference',cyl(40,40,sx,-200,1040),'catalog','lift_catalog','2Nm BXW05 normally applied reference; adapters required',.8))
    pp.append(row('Lift_motor_gear_reference',cyl(16,78.9,sx,-200,1080),'catalog','lift_catalog','3242BX4+32GPT20 exact19.8:1 reference;120s traverse sizing',.336))
    fixed_frame=join(fixed)
    for y in ys:
        fixed_frame=fixed_frame.cut(cyl(8.1,1160,sx,y,-130))
        for zz in [-114,1006]:fixed_frame=fixed_frame.cut(cyl(14.1,12,sx,y,zz-2))
    pp.append(row('Lift_connected_fixed_frame',fixed_frame.removeSplitter(),'aluminium','lift_fixed'))
    # The only X-spanning bridge lies above the payload in central free Y space.
    moving=[]
    for x in [left,right]:
        moving.append(box(20,570,12,x-10,-210,floor+124))
        for y in ys:moving.append(box(32,32,176,x-16,y-16,floor-40))
    moving.append(box(right-left+20,20,12,left-10,-10,floor+124))
    for y in ys:
        moving += [box(36,36,34,sx-18,y-18,floor-34),box(60,20,20,sx,y-10,floor-30)]
    grip_x=[XA-86,XF+100]
    for x in grip_x:
        moving += [box(20,6,152,x-10,-18,floor-16),box(20,8,12,x-10,-18,floor+124),
                   box(20,62,4,x-10,-74,floor-16),box(16,6,14,x-8,-74,floor-12)]
        py=-18-(26 if grips_open is True else float(grips_open))
        pin=join([cyl(3,24,x,py,floor-5,(0,1,0)),cyl(1.5,26,x,py-26,floor-5,(0,1,0))])
        pp.append(row('Lift_pallet_grip_pin_'+str(x),pin,'steel','cradle_grip',
                      '26mm captive Y withdrawal;16mm pallet engagement;open only after both pallet bayonet locks are engaged'))
        actuator=cyl(5,30,x,-74,floor-5,(0,1,0)).cut(cyl(1.6,30,x,-74,floor-5,(0,1,0)))
        pp.append(row('Lift_pallet_grip_actuator_reference_'+str(x),actuator,'catalog','cradle_catalog',
                      '10mmODx30mm allocation;26mm stroke;normally engaged positive holding pin;selection separate',.03))
    # End retention and Y keepers stay on the lift while only the comb withdraws.
    for base_x,lead in [(XA-1.9,False),(XF+.3,True)]:
        x=XF+.5 if lead else XA-1.5
        wall=(box(1,99,110,x,-49.5,floor).cut(box(3,84,80,x-.5,-42,floor+12)) if lead else
              box(1,83,110,x,-41.5,floor).cut(box(3,60,80,x-.5,-30,floor+12)))
        moving += [wall,box(10,99,6,base_x-8 if lead else base_x,-49.5,floor+108),box(1,20,28,x,-10,floor+108)]
    for u in [70,270]:
        moving.append(box(8,111,12,XA+u,-55.5,floor+124))
        for side in [-1,1]:
            opened=keepers_open or incoming_side==side
            stroke=(110 if keepers_open is True else float(keepers_open))if keepers_open else (110 if incoming_side==side else 0)
            z=floor+2+stroke;y=-54 if side<0 else 51;cy=side*53.5
            tab=box(8,3,6,XA+u,y,z);stem=cyl(1.5,130,XA+u+4,cy,z+4)
            pp.append(row('Cradle_Y_keeper_'+str(u)+'_'+str(side),join([tab,stem]),'steel','cradle_keeper',
                '110mm upward retraction;3mm rod in3.2mm overhead guide;tab clears payload top by12mm when open;positive holding linear actuator required'))
            moving.append(box(8,4,16,XA+u,cy-2,floor+120))
            # A central screw actuator operates a guided push/pull cable. Its
            # outer tube stays inside |Y|55.4 throughout vertical travel.
            # This is a reference envelope and interface, not selected hardware.
            mx=XA+u+(-10 if side<0 else 18);rx=XA+u+4
            motor=cyl(6,160,mx,0,floor+136)
            vertical=cyl(1.9,161,rx,cy,floor+136).cut(cyl(1.6,161,rx,cy,floor+136))
            length=((rx-mx)**2+cy**2)**.5;axis=((rx-mx)/length,cy/length,0)
            route=cyl(1.9,length,mx,0,floor+297,axis).cut(cyl(1.6,length,mx,0,floor+297,axis))
            pp.append(row('Cradle_keeper_actuator_reference_'+str(u)+'_'+str(side),join([motor,vertical,route]),
                'catalog','cradle_catalog','110mm stroke;12mmODx160mm central actuator allocation;3.8mmOD guided push/pull cable;self-locking screw plus normally applied holding brake required;hardware/load/life selection separate',.12))
    frame=join(moving)
    for x in [left,right]:
        for y in ys:frame=frame.cut(box(20.5,20.5,200,x-10.25,y-10.25,floor-50))
    for y in ys:frame=frame.cut(cyl(14.1,40,sx,y,floor-36))
    for x in grip_x:
        frame=frame.cut(cyl(3.1,6,x,-18,floor-5,(0,1,0)))
        frame=frame.cut(cyl(5.1,6,x,-74,floor-5,(0,1,0)))
    for u in [70,270]:
        for side in [-1,1]:frame=frame.cut(cyl(1.6,20,XA+u+4,side*53.5,floor+120))
    pp.append(row('Lift_connected_carriage',frame.removeSplitter(),'aluminium','cradle','High endcrossheads, central topbridge, bored outboard nut brackets'))
    for y in ys:
        pp.append(row('Lift_Tr16x4_nut_'+str(y),cyl(14,28,sx,y,floor-31).cut(cyl(8.1,28,sx,y,floor-31)),'polymer','cradle','Nominal captive nut; load/life rating separate'))
    return pp


def pallet(b,floor=46,aft=200,lifted=False):
    """One captive connected pallet; no horizontal withdrawal mechanism."""
    box,cyl,join,row=b.box,b.cyl,b.join,b.row
    xa=aft+64;xf=xa+340.5;ends=[xa-86,xf+100]
    parts=[box(ends[1]-ends[0]+20,20,6,ends[0]-10,-10,floor-8)]
    for u in [90,230]:
        parts.append(box(24,100,6,xa+u,-50,floor-8))
        for y in [-50,42]:parts.append(box(24,8,2,xa+u,y,floor-2))
    for u in [70,270]:
        parts.append(box(14,111,6,xa+u-3,-55.5,floor-8))
        for y in [-50,42]:parts.append(box(14,8,8,xa+u-3,y,floor-16))
    for x in ends:parts.append(box(20,20,11.5,x-10,-10,floor-12))
    for x in [aft+40,aft+468]:parts.append(box(16,99.5,6,x-8,-99.5,floor-8))
    shape=join(parts)
    for x in ends:shape=shape.cut(cyl(3.1,20,x,-10,floor-5,(0,1,0)))
    for x in [aft+40,aft+468]:
        slot=join([cyl(3.5,20,x,-90,floor-12),box(13,5,20,x-6.5,-92.5,floor-12)])
        shape=shape.cut(slot)
    return [row('Captive_payload_pallet',shape.removeSplitter(),'aluminium','cradle_pallet'if lifted else'sled_pallet',
                'One physical pallet;four8mm feet seat on carrier top30;Y0 crossbar;outboard6.2mm lift-grip bores;two keyed positiveZ bayonet lock interfaces;stays on carrier through shot andreturn')]
