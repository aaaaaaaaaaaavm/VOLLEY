import java.nio.file.*;
import java.io.*;
import java.util.*;
import org.hipparchus.CalculusFieldElement;
import org.hipparchus.geometry.euclidean.threed.Vector3D;
import org.hipparchus.geometry.euclidean.threed.FieldVector3D;
import org.hipparchus.ode.nonstiff.DormandPrince853Integrator;
import org.orekit.frames.FramesFactory;
import org.orekit.orbits.CartesianOrbit;
import org.orekit.orbits.OrbitType;
import org.orekit.propagation.SpacecraftState;
import org.orekit.propagation.FieldSpacecraftState;
import org.orekit.propagation.numerical.NumericalPropagator;
import org.orekit.forces.ForceModel;
import org.orekit.forces.gravity.J2OnlyPerturbation;
import org.orekit.time.AbsoluteDate;
import org.orekit.time.TimeScalesFactory;
import org.orekit.utils.PVCoordinates;
import org.orekit.utils.ParameterDriver;

/** Native Orekit replay: no targeter imports, no later host-state resets.
 * Constant inertial force, integrated mass flow, fixed-axis J2, point release.
 */
public class FiniteReplay {
    static final double MU=3.986004418e14,RE=6378137.,J2=1.08262668e-3,ISP=220.,G0=9.80665;
    static final varFrame FRAME = new varFrame();
    static class varFrame {
        final org.orekit.frames.Frame frame=FramesFactory.getEME2000();
        final AbsoluteDate epoch=new AbsoluteDate(2026,9,29,0,0,0.,TimeScalesFactory.getTAI());
    }
    static class Force implements ForceModel {
        final Vector3D force;
        Force(Vector3D f){force=f;}
        public boolean dependsOnPositionOnly(){return false;}
        public List<ParameterDriver> getParametersDrivers(){return List.of();}
        public Vector3D acceleration(SpacecraftState s,double[] p){return force.scalarMultiply(1/s.getMass());}
        public <T extends CalculusFieldElement<T>> FieldVector3D<T> acceleration(FieldSpacecraftState<T> s,T[] p){
            return new FieldVector3D<T>(s.getMass().reciprocal(),force);
        }
        public double getMassDerivative(SpacecraftState s,double[] p){return -force.getNorm()/(ISP*G0);}
        public <T extends CalculusFieldElement<T>> T getMassDerivative(FieldSpacecraftState<T> s,T[] p){
            return s.getMass().newInstance(-force.getNorm()/(ISP*G0));
        }
    }
    static Vector3D v(String[] r,int o){return new Vector3D(Double.parseDouble(r[o]),Double.parseDouble(r[o+1]),Double.parseDouble(r[o+2]));}
    static PVCoordinates pv(String[] r,int o){return new PVCoordinates(v(r,o),v(r,o+3));}
    static SpacecraftState state(PVCoordinates pv,double mass,double t){
        return new SpacecraftState(new CartesianOrbit(pv,FRAME.frame,FRAME.epoch.shiftedBy(t),MU)).withMass(mass);
    }
    static SpacecraftState propagate(SpacecraftState s,double end,Vector3D force,double step){
        if(Math.abs(end-s.getDate().durationFrom(FRAME.epoch))<1e-9)return s;
        var integ=new DormandPrince853Integrator(1e-6,step,1e-9,2e-14);
        var prop=new NumericalPropagator(integ);prop.setOrbitType(OrbitType.CARTESIAN);prop.setInitialState(s);
        prop.addForceModel(new J2OnlyPerturbation(MU,RE,J2,FRAME.frame));
        if(force.getNorm()>0)prop.addForceModel(new Force(force));
        return prop.propagate(FRAME.epoch.shiftedBy(end));
    }
    public static void main(String[] args)throws Exception{
        Locale.setDefault(Locale.ROOT);
        String source=args[0],prefix=args[1];double step=Double.parseDouble(args[2]);
        double forceScale=args.length>3?Double.parseDouble(args[3]):1.;
        double shotScale=args.length>4?Double.parseDouble(args[4]):1.;
        double initialDx=args.length>5?Double.parseDouble(args[5]):0.;
        List<String[]> rows=new ArrayList<>();
        for(String l:Files.readAllLines(Path.of(source)))if(!l.isBlank()&&!l.startsWith("start_s"))rows.add(l.split(","));
        String[] first=rows.get(0);PVCoordinates p=pv(first,9);
        p=new PVCoordinates(p.getPosition().add(new Vector3D(initialDx,0,0)),p.getVelocity());
        var host=state(p,Double.parseDouble(first[8]),Double.parseDouble(first[0]));
        PVCoordinates finalTarget=pv(first,15);
        double initialMass=host.getMass(),payloadSum=0.;int delivered=0;
        try(PrintWriter h=new PrintWriter(prefix+"_host.csv");PrintWriter c=new PrintWriter(prefix+"_payload.csv")){
            h.println("t_s,event,position_difference_m,velocity_difference_m_s,mass_difference_kg,mass_kg,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s");
            c.println("payload,t_s,position_target_error_m,velocity_target_error_m_s,momentum_residual_kg_m_s,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s");
            for(int i=1;i<rows.size();i++){
                String[] r=rows.get(i);String kind=r[2];double t=Double.parseDouble(r[1]);
                if(kind.equals("arc")){
                    double start=Double.parseDouble(r[0]);
                    if(Math.abs(host.getDate().durationFrom(FRAME.epoch)-start)>1e-6)throw new IllegalArgumentException("Noncontiguous arc");
                    host=propagate(host,t,v(r,5).scalarMultiply(forceScale),step);
                }else if(kind.equals("shot")){
                    if(Math.abs(host.getDate().durationFrom(FRAME.epoch)-t)>1e-6)throw new IllegalArgumentException("Shot time mismatch");
                    double m=Double.parseDouble(r[4]),M=host.getMass();Vector3D u=v(r,5).scalarMultiply(shotScale);
                    PVCoordinates prior=host.getPVCoordinates();Vector3D vc=prior.getVelocity().add(u.scalarMultiply(1-m/M));
                    Vector3D vp=prior.getVelocity().subtract(u.scalarMultiply(m/M));
                    Vector3D momentum=vc.scalarMultiply(m).add(vp.scalarMultiply(M-m)).subtract(prior.getVelocity().scalarMultiply(M));
                    var child=propagate(state(new PVCoordinates(prior.getPosition(),vc),m,t),90000.,Vector3D.ZERO,step).getPVCoordinates();
                    var goal=pv(r,15);Vector3D cr=child.getPosition(),cv=child.getVelocity();
                    c.printf("%s,%.12f,%.12g,%.12g,%.12g,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f%n",r[3],t,cr.distance(goal.getPosition()),cv.distance(goal.getVelocity()),momentum.getNorm(),cr.getX(),cr.getY(),cr.getZ(),cv.getX(),cv.getY(),cv.getZ());
                    host=state(new PVCoordinates(prior.getPosition(),vp),M-m,t);payloadSum+=m;delivered++;
                }else throw new IllegalArgumentException("Unknown event");
                PVCoordinates actual=host.getPVCoordinates(),expected=pv(r,9);Vector3D hr=actual.getPosition(),hv=actual.getVelocity();
                h.printf("%.12f,%s,%.12g,%.12g,%.12g,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f%n",t,kind,hr.distance(expected.getPosition()),hv.distance(expected.getVelocity()),host.getMass()-Double.parseDouble(r[8]),host.getMass(),hr.getX(),hr.getY(),hr.getZ(),hv.getX(),hv.getY(),hv.getZ());
            }
            PVCoordinates f=host.getPVCoordinates();
            System.out.printf("Native Orekit finite-force replay delivered=%d fuel_used_kg=%.12f host_target_position_m=%.12g host_target_velocity_m_s=%.12g force_scale=%.12g shot_scale=%.12g initial_dx_m=%.12g%n",delivered,initialMass-host.getMass()-payloadSum,f.getPosition().distance(finalTarget.getPosition()),f.getVelocity().distance(finalTarget.getVelocity()),forceScale,shotScale,initialDx);
        }
    }
}
