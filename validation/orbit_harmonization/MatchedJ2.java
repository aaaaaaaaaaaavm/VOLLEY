import java.util.*;import java.nio.file.*;import java.io.*;
import org.hipparchus.CalculusFieldElement;
import org.hipparchus.geometry.euclidean.threed.*;
import org.hipparchus.ode.nonstiff.DormandPrince853Integrator;
import org.orekit.frames.*;import org.orekit.orbits.*;
import org.orekit.propagation.*;import org.orekit.propagation.numerical.*;
import org.orekit.forces.gravity.J2OnlyPerturbation;
import org.orekit.time.*;import org.orekit.utils.*;
public class MatchedJ2 {
 public static void main(String[] a)throws Exception {
 Locale.setDefault(Locale.ROOT);var rows=new ArrayList<double[]>();
 for(String line:Files.readAllLines(Path.of(a[0])))if(!line.isBlank()&&Character.isDigit(line.strip().charAt(0))){var s=line.strip().split("\\s+");double[] z=new double[s.length];for(int i=0;i<s.length;i++)z[i]=Double.parseDouble(s[i]);rows.add(z);}
 final var epoch=new AbsoluteDate(2026,9,29,0,0,0.,TimeScalesFactory.getTAI());
 var frame=FramesFactory.getEME2000();
 TransformProvider provider=new TransformProvider(){
 public Transform getTransform(AbsoluteDate d){double t=d.durationFrom(epoch);int i=Math.max(0,Math.min(rows.size()-2,(int)Math.floor(t/60)));var p=rows.get(i);var q=rows.get(i+1);double f=(t-p[0])/(q[0]-p[0]);var k=new Vector3D(p[9]+f*(q[9]-p[9]),p[10]+f*(q[10]-p[10]),p[11]+f*(q[11]-p[11])).normalize();return new Transform(d,new Rotation(k,Vector3D.PLUS_K));}
 public <T extends CalculusFieldElement<T>> FieldTransform<T> getTransform(FieldAbsoluteDate<T>d){return new FieldTransform<T>(d.getField(),getTransform(d.toAbsoluteDate()));}
 };
 var axis=new Frame(frame,provider,"GMAT_exported_pole",false);double[] x=rows.get(0);double mu=3.986004415e14;
 var orbit=new CartesianOrbit(new PVCoordinates(new Vector3D(x[1]*1000,x[2]*1000,x[3]*1000),new Vector3D(x[4]*1000,x[5]*1000,x[6]*1000)),frame,epoch,mu);
 var integ=new DormandPrince853Integrator(.00001,Double.parseDouble(a[2]),1e-8,2e-14);var prop=new NumericalPropagator(integ);prop.setOrbitType(OrbitType.CARTESIAN);prop.setInitialState(new SpacecraftState(orbit));
 prop.addForceModel(new J2OnlyPerturbation(mu,6378136.3,Math.sqrt(5)*4.8416539e-4,axis));
 var times=new ArrayList<Double>(); if(a.length>3){for(String line:Files.readAllLines(Path.of(a[3])))if(!line.isBlank()&&Character.isDigit(line.strip().charAt(0)))times.add(Double.parseDouble(line.strip().split("\\s+")[0]));}else{for(int tt=0;tt<=86400;tt+=60)times.add((double)tt);}
 try(var w=new PrintWriter(a[1])){w.println("t_s,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s");for(double t:times){var pv=prop.propagate(epoch.shiftedBy(t)).getPVCoordinates();var p=pv.getPosition();var v=pv.getVelocity();w.printf("%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f%n",t,p.getX(),p.getY(),p.getZ(),v.getX(),v.getY(),v.getZ());}}
 System.out.println("Orekit 13.1.6 completed matched JGM2/prescribed-pole J2 history");
 }
}
