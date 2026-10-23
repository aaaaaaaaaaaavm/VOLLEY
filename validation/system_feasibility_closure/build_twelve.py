"""Twelve-cell scaling assembly generated from the selected four-cell source.

One indexed receiver, twelve dedicated fixed cells, one extended rail corridor.
No host envelope, bending stiffness or installed motor chain is certified.
"""
from pathlib import Path
import argparse,hashlib,importlib.util,json,sys

H=Path(__file__).resolve().parent


def main(source):
    spec=importlib.util.spec_from_file_location('fm08_selected_source',source)
    b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
    b.O=H/'cad_twelve';b.O.mkdir(exist_ok=True)
    four=list(b.CELLS)
    assert [x[1] for x in four]==['1U','3U','1U','3U']
    assert [x[2] for x in four]==[0,250,650,900]
    b.CELLS=[]
    for bank in range(3):
        for cid,fmt,x,side in four:
            b.CELLS.append((f'Bank{bank+1}_{cid}',fmt,x+1300*bank,side))
    original_rail=b.rail
    def rail12(dock=0):
        p=[]
        for original in original_rail(None):
            q={**original,'shape':original['shape'].copy()}
            n=q['name']
            if n.startswith(('Profile_rail_','Rail_support_','Receiver_drive_belt_')):
                bb=q['shape'].BoundBox
                # These specific source members are rectangular constant sections.
                expected=bb.XLength*bb.YLength*bb.ZLength
                assert abs(q['shape'].Volume-expected)<max(.001,expected*1e-9),n
                q['shape']=b.box((bb.XLength+2600,bb.YLength,bb.ZLength),(bb.XMin,bb.YMin,bb.ZMin))
                q['notes']+=';extended2600mmsamecrosssection;loadedstiffnessnotqualified'
            elif n=='Receiver_pulley_1420':
                q['shape'].translate(b.V(2600,0,0));q['name']='Receiver_pulley_4020'
            elif n.startswith('Rail_standoff_'):
                continue
            elif n.startswith(('Dock_socket_','Station_dock_pin_')):
                for bank in range(3):
                    qq={**q,'shape':q['shape'].copy(),'name':f'Bank{bank+1}__'+n}
                    qq['shape'].translate(b.V(1300*bank,0,0));p.append(qq)
                    if n.startswith('Station_dock_pin_'):
                        station=float(n.rsplit('_',2)[1])+1300*bank
                        if dock is not None and abs(dock-station)<1e-8:qq['shape'].translate(b.V(0,0,36))
                continue
            p.append(q)
        for yy in [-25,125]:
            for xx in [-60,*[110+250*k for k in range(16)],4040]:
                stand=b.box((16,16,140),(xx-8,yy-8,-140)).cut(b.box((12,12,140),(xx-6,yy-6,-140))).removeSplitter()
                p.append(b.row('Rail_standoff_'+str(yy)+'_'+str(xx),stand,'aluminium','rail',
                    '250mmapproxsupportspacing;generic16x16x2hollowfixtureatZ-140;loadedhostinterfaceunqualified'))
        return p
    b.rail=rail12
    caps=[]
    for stem,active,u,phase,fmt,dock in [
        ('FM08_R3_twelve_cell_stowed',None,0,'stored','3U',0),
        ('FM08_R3_twelve_cell_far_3U_seated','Bank3_CellD_3U',200,'captured','3U',3500),
    ]:
        items=b.assembly(active,u,phase,False,fmt,dock)
        cap=b.export(stem,items)
        cap['including_catalog_envelopes_audit']=b.audit(items,False,True)
        byname={q['name']:q for q in items}
        fullhits=cap['including_catalog_envelopes_audit']['positive_volume_interferences']
        materialhits=[h for h in fullhits if byname[h['a']]['material']!='catalog_envelope' and byname[h['b']]['material']!='catalog_envelope']
        payloadhits=[h for h in fullhits if byname[h['a']]['role']=='payload' or byname[h['b']]['role']=='payload']
        cap['static_interference_audit']={'derived_from':'including_catalog_envelopes_audit','positive_volume_interferences':materialhits,'pass':not materialhits}
        cap['payload_interference_audit']={'derived_from':'including_catalog_envelopes_audit','positive_volume_interferences':payloadhits,'pass':not payloadhits}
        cap['catalog_envelope_count']=sum(q['material']=='catalog_envelope' for q in items)
        cap['component_bounds_mm']={q['name']:[q['shape'].BoundBox.XMin,q['shape'].BoundBox.XMax,
            q['shape'].BoundBox.YMin,q['shape'].BoundBox.YMax,q['shape'].BoundBox.ZMin,q['shape'].BoundBox.ZMax] for q in items}
        loaded=[];payload_total=0.
        for q in items:
            qq={**q}
            if q['role']=='payload':
                mass=1.33 if q['name'].endswith('1U') else 4.
                material='Uniform_surrogate_'+('1U' if mass==1.33 else '3U')
                b.RHO[material]=mass/q['shape'].Volume
                qq['material']=material;payload_total+=mass
            loaded.append(qq)
        props=b.massprops(loaded)
        props['mass_boundary']='Representedcustommaterialplusuniform1.33/4kgpayloadenvelopes;catalog/sensors/completeinstalledhardwareexcluded'
        props['uniform_payload_mass_kg']=payload_total
        cap['uniform_payload_loaded_properties']=props
        assert abs(payload_total-31.98)<1e-8
        cap['cell_count']=12
        cap['receiver_count']=1
        cap['source_sha256']=hashlib.sha256(Path(source).read_bytes()).hexdigest()
        caps.append(cap)
        (b.O/(stem+'.json')).write_text(json.dumps(cap,indent=2)+'\n')
        print(stem,'parts',cap['parts'],'payloadhits',len(cap['payload_interference_audit']['positive_volume_interferences']),flush=True)
    report=dict(study='CAP-12 selected-feeder scaling assembly',source_revision='FM08-R3',
        builder_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        original_four_cell_source_sha256=hashlib.sha256(Path(source).read_bytes()).hexdigest(),
        manifest=dict(one_U=6,three_U=6),receiver_count=1,receiver_travel_mm=3500,rail_length_mm=4200,
        stations_X_mm=[x[2] for x in b.CELLS],captures=caps,
        design_boundary='ExplicitCADscalingassemblywithcustommaterialmass;catalog/sensor/gateactuator/harnessmassnotcomplete;notinstalledsystemmass',
        limitations=['No named host or provider;4.2mrail is a packaging requirement,notcompatibilityproof',
          'No full12stationmotion/loadedclearance/stiffnessverification;twoexportedstatesonly',
          'SourceR3nominalmodelanditsunresolvedlimitationsareinherited',
          'No coupled electromagnetic/circuit/thermal qualification or achieved3–6m/s claim'])
    sweep=[]
    for cid,fmt,dock,side in b.CELLS:
        items=b.assembly(cid,0,'transfer',False,fmt,dock)
        payload=next(q for q in items if q['name'].startswith(cid+'__Payload_'))
        bb=payload['shape'].BoundBox
        ymin=bb.YMin if side=='south' else bb.YMin-200
        corridor=b.box((bb.XLength,bb.YLength+200,bb.ZLength),(bb.XMin,ymin,bb.ZMin))
        hits=[];checked=0
        for q in items:
            if q is payload:continue
            if q['name'].startswith(cid+'__') and q['role'] in ('moving','moving_gate'):continue
            if not corridor.BoundBox.intersect(q['shape'].BoundBox):continue
            checked+=1;vol=corridor.common(q['shape']).Volume
            if vol>1e-5:hits.append(dict(component=q['name'],positive_volume_mm3=vol))
        sweep.append(dict(cell=cid,format=fmt,dock_X_mm=dock,feed_stroke_mm=200,
            method='ExactrectangularpayloadMinkowskisweepagainstfrozenfeed-phaseenvironment;activeforkexcluded',
            tested_bounding_box_pairs=checked,positive_volume_interferences=hits,pass_no_positive_volume_interference=not hits))
        print('continuous_payload_sweep',cid,'hits',len(hits),flush=True)
    report['continuous_payload_corridor_sweeps']=sweep
    report['continuous_payload_corridor_pass']=all(r['pass_no_positive_volume_interference'] for r in sweep)
    (H/'TWELVE_ASSEMBLY_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);a=p.parse_args();main(a.source)
