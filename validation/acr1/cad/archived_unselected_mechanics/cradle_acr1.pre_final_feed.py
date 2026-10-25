"""Captive vertical transfer cradle; all coordinates derive from the controlled assembly."""
def build(b,floor=46,keepers_open=False,fork_withdraw=0,incoming_side=None):
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
    gxlist=[XA-86,XF+100]
    for x in gxlist:
        for y in [-60,300]:
            moving.append(box(20,12,156,x-10,y,floor-20))
            col=left if x<XA else right
            moving.append(box(abs(x-col)+20,12,12,min(x,col)-10,y,floor+124))
    fx=40
    for y in [-65,305]:
        moving += [box(30,12,162,fx-15,y-2,floor-26),box(left-fx+10,12,12,fx,y-2,floor+124)]
    moving += [box(50,12,176,fx-25,330,floor-40),box(left-fx+10,12,12,fx,330,floor+124)]
    for y in ys:
        moving += [box(36,36,34,sx-18,y-18,floor-34),box(60,20,20,sx,y-10,floor-30)]
    frame=join(moving)
    for x in [left,right]:
        for y in ys:frame=frame.cut(box(20.5,20.5,200,x-10.25,y-10.25,floor-50))
    for y in ys:frame=frame.cut(cyl(14.1,40,sx,y,floor-36))
    for x in gxlist:
        for y in [-60,300]:frame=frame.cut(cyl(5.1,12,x,y,floor-12,(0,1,0)))
    for y in [-65,305]:frame=frame.cut(cyl(11.1,12,fx,y-2,floor-12,(0,1,0)))
    frame=frame.cut(cyl(20.2,12,fx,330,floor-12,(0,1,0)))
    pp.append(row('Lift_connected_carriage',frame.removeSplitter(),'aluminium','cradle','High endcrossheads, central topbridge, bored outboard nut brackets'))
    for y in ys:
        pp.append(row('Lift_Tr16x4_nut_'+str(y),cyl(14,28,sx,y,floor-31).cut(cyl(8.1,28,sx,y,floor-31)),'polymer','cradle','Nominal captive nut; load/life rating separate'))
    for x in gxlist:pp.append(row('Fork_guide_'+str(x),cyl(5,350,x,-50,floor-12,(0,1,0)),'steel','cradle'))
    parts=[box(gxlist[1]-gxlist[0]+20,20,6,gxlist[0]-10,-10+fork_withdraw,floor-8)]
    for u in [90,230]:
        parts.append(box(24,100,6,XA+u,-50+fork_withdraw,floor-8))
        for y in [-50,42]:parts.append(box(24,8,2,XA+u,y+fork_withdraw,floor-2))
    for u in [70,270]:parts.append(box(14,111,6,XA+u-3,-55.5+fork_withdraw,floor-8))
    for x in gxlist:parts.append(cyl(10,30,x,-15+fork_withdraw,floor-12,(0,1,0)))
    for x in gxlist:
        pp.append(row('Fork_guide_bush_'+str(x),cyl(8,30,x,-15+fork_withdraw,floor-12,(0,1,0)).cut(cyl(5.1,30,x,-15+fork_withdraw,floor-12,(0,1,0))),'polymer','cradle_fork'))
    for x,lead in [(XA-1.9,False),(XF+.3,True)]:
        wall=(box(1.5,99,110,x,-49.5+fork_withdraw,floor).cut(box(3,84,80,x-.5,-42+fork_withdraw,floor+12)) if lead else
              box(1.5,84,110,x,-42+fork_withdraw,floor).cut(box(3,60,80,x-.5,-30+fork_withdraw,floor+12)))
        # Endwalls occupy the actual clearance between payload and sled
        # retention hardware: rear262.1..263.6 and front604.8..606.3.
        # Continuous walls maintain custody throughout the complete lift stroke.
        lip=box(10,99,6,x-8 if lead else x,-49.5+fork_withdraw,floor+108)
        foot=box(12,20,8,x-8 if lead else x,-10+fork_withdraw,floor-8)
        parts += [wall,lip,foot]
    for u in [70,270]:
        for side in [-1,1]:
            opened=keepers_open or incoming_side==side
            z=floor-10 if opened else floor+2;y=-54 if side<0 else 51
            cy=-53.5 if side<0 else 53.5
            tab=box(8,3,6,XA+u,y+fork_withdraw,z)
            stem=cyl(1.5,30,XA+u+4,cy+fork_withdraw,z+4)
            pp.append(row('Cradle_Y_keeper_'+str(u)+'_'+str(side),join([tab,stem]),'steel','cradle_keeper','12mm vertical keeper stroke; fail-safe holding actuation requirement'))
            housing=box(8,4,14,XA+u,cy-2+fork_withdraw,floor+10).cut(cyl(1.6,14,XA+u+4,cy+fork_withdraw,floor+10))
            parts += [housing,box(8,1,12,XA+u,(54.5 if side>0 else -55.5)+fork_withdraw,floor-2)]
    # Nut housing and its continuous transverse link drive the fork positively.
    fx=40
    parts += [box(28,22,28,fx-14,-11+fork_withdraw,floor-26),box(gxlist[0]-fx,20,6,fx,-10+fork_withdraw,floor-8)]
    fork=join(parts)
    for x in gxlist:fork=fork.cut(cyl(8.1,30,x,-15+fork_withdraw,floor-12,(0,1,0)))
    fork=fork.cut(cyl(9.65,24,fx,-12+fork_withdraw,floor-12,(0,1,0)))
    for u in [70,270]:
        for side in [-1,1]:
            fork=fork.cut(cyl(1.6,60,XA+u+4,side*53.5+fork_withdraw,floor-10))
            fork=fork.cut(box(8.2,3.2,20,XA+u-.1,(-54.1 if side<0 else 50.9)+fork_withdraw,floor-10))
    pp.append(row('Cradle_retractable_floor',fork.removeSplitter(),'aluminium','cradle_fork','CentralY0 crossbar; interleaved rail-only pads,110mm endwalls,roof+108;150mm withdrawal only at low dock'))
    # A separate outboard lead screw positively drives the horizontal fork carriage.
    pp.append(row('Fork_Tr10x2_screw',join([cyl(5,350,fx,-50,floor-12,(0,1,0)),cyl(4,20,fx,-70,floor-12,(0,1,0)),cyl(4,20,fx,300,floor-12,(0,1,0))]),'steel','cradle','Nominal10x2 supported fork-withdraw screw'))
    nut=cyl(9.55,19.1,fx,-9.55+fork_withdraw,floor-12,(0,1,0)).cut(cyl(5.1,19.1,fx,-9.55+fork_withdraw,floor-12,(0,1,0)))
    pp.append(row('Fork_drive_nut',nut,'polymer','cradle_fork'))
    # Separate supported bearings and a normally applied brake mount complete the drive.
    for y in [-65,305]:
        bearing=cyl(11,8,fx,y,floor-12,(0,1,0)).cut(cyl(4.1,8,fx,y,floor-12,(0,1,0)))
        pp.append(row('Fork_screw_bearing_'+str(y),bearing,'steel','cradle'))
    pp.append(row('Fork_drive_coupler',cyl(4,5,fx,320,floor-12,(0,1,0)),'steel','cradle'))
    pp.append(row('Fork_holding_brake',cyl(20,35,fx,325,floor-12,(0,1,0)),'catalog','cradle','0.12Nm BXW01 reference normally applied',.2))
    pp.append(row('Fork_motor_gear9',cyl(16,78.9,fx,360,floor-12,(0,1,0)),'catalog','cradle','3242BX4+32GPT9:1 reference;30s withdraw command',.336))
    return pp
