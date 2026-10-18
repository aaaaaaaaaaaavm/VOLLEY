/** Orekit 13.1.6 propagation of explicitly prescribed release states. */
import java.util.Locale;
import java.io.PrintWriter;
import org.hipparchus.geometry.euclidean.threed.Vector3D;
import org.hipparchus.ode.nonstiff.DormandPrince853Integrator;
import org.orekit.frames.FramesFactory;
import org.orekit.orbits.CartesianOrbit;
import org.orekit.orbits.OrbitType;
import org.orekit.propagation.SpacecraftState;
import org.orekit.propagation.numerical.NumericalPropagator;
import org.orekit.forces.gravity.J2OnlyPerturbation;
import org.orekit.time.AbsoluteDate;
import org.orekit.time.TimeScalesFactory;
import org.orekit.utils.PVCoordinates;

public class OrbitEvidence {
 public static void main(String[] args) throws Exception {
  Locale.setDefault(Locale.ROOT);
  String output=args[0];double maxStep=Double.parseDouble(args[1]);
  double mu=3.986004418e14,re=6378137.,r=re+450000.,inc=Math.toRadians(51.6);
  double dynamicsMu=args.length>2?Double.parseDouble(args[2]):mu;
  var frame=FramesFactory.getGCRF();
  var date=new AbsoluteDate(2026,9,29,0,0,0.,TimeScalesFactory.getTAI());
  try(var writer=new PrintWriter(output)) {
   writer.println("model,relative_speed_m_s,t_s,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s,a_m,e");
   for(boolean j2:new boolean[]{false,true}) for(double u:new double[]{0.,2.5,12.448437,16.029}) {
    if(args.length>2 && (j2 || u!=16.029))continue;
    double dv=300./304.*u,v=Math.sqrt(mu/r)+dv;
    var orbit=new CartesianOrbit(new PVCoordinates(new Vector3D(r,0.,0.),new Vector3D(0.,v*Math.cos(inc),v*Math.sin(inc))),frame,date,dynamicsMu);
    var integrator=new DormandPrince853Integrator(.0001,maxStep,1e-7,1e-13);
    var prop=new NumericalPropagator(integrator);
    prop.setOrbitType(OrbitType.CARTESIAN);
    prop.setInitialState(new SpacecraftState(orbit).withMass(4.));
    if(j2)prop.addForceModel(new J2OnlyPerturbation(dynamicsMu,re,1.08262668e-3,frame));
    for(int t=0;t<=86400;t+=60) {
     var state=prop.propagate(date.shiftedBy(t));var pv=state.getPVCoordinates();var p=pv.getPosition();var vel=pv.getVelocity();
     writer.printf("%s,%.9f,%d,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.14g%n",j2?"J2":"two_body",u,t,p.getX(),p.getY(),p.getZ(),vel.getX(),vel.getY(),vel.getZ(),state.getOrbit().getA(),state.getOrbit().getE());
    }
   }
  }
  System.out.println("Orekit 13.1.6: eight one-day histories, 60 s output; maximum integration step "+maxStep+" s");
 }
}
