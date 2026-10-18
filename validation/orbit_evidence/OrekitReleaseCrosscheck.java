/*
Orekit 13.1.x single-release J2 cross-check.
STATUS: executed with Orekit 13.1.6 on 18 October 2026; see ORBIT_RESULTS.json.

Compile/run in a Maven project with org.orekit:orekit:13.1.6 and hipparchus dependencies.
This intentionally uses constants and J2OnlyPerturbation rather than VOLLEY helper code.
*/
import org.hipparchus.geometry.euclidean.threed.Vector3D;
import org.hipparchus.ode.nonstiff.DormandPrince853Integrator;
import org.orekit.frames.Frame;
import org.orekit.frames.FramesFactory;
import org.orekit.orbits.CartesianOrbit;
import org.orekit.orbits.Orbit;
import org.orekit.propagation.SpacecraftState;
import org.orekit.propagation.numerical.NumericalPropagator;
import org.orekit.forces.gravity.J2OnlyPerturbation;
import org.orekit.time.AbsoluteDate;
import org.orekit.time.TimeScalesFactory;
import org.orekit.utils.PVCoordinates;

public class OrekitReleaseCrosscheck {
    public static void main(String[] args) {
        final double mu=3.986004418e14;
        final double re=6378137.0;
        final double j2=1.08262668e-3;
        final double alt=450e3;
        final double inc=Math.toRadians(51.6);
        final double r=re+alt;
        final double vc=Math.sqrt(mu/r);
        final double u=16.029;
        final double dv=300.0/(300.0+4.0)*u;

        Frame frame=FramesFactory.getGCRF();
        AbsoluteDate date=new AbsoluteDate(2026,9,29,0,0,0.0,TimeScalesFactory.getTAI());
        Vector3D pos=new Vector3D(r,0,0);
        Vector3D vel=new Vector3D(0,(vc+dv)*Math.cos(inc),(vc+dv)*Math.sin(inc));
        Orbit orbit=new CartesianOrbit(new PVCoordinates(pos,vel),frame,date,mu);

        double[][] tol=NumericalPropagator.tolerances(0.001, orbit, orbit.getType());
        DormandPrince853Integrator integ=new DormandPrince853Integrator(0.001,60.0,tol[0],tol[1]);
        NumericalPropagator prop=new NumericalPropagator(integ);
        prop.setInitialState(new SpacecraftState(orbit,4.0));
        prop.addForceModel(new J2OnlyPerturbation(mu,re,j2,frame));

        double period=orbit.getKeplerianPeriod();
        SpacecraftState end=prop.propagate(date.shiftedBy(period));
        System.out.printf("initial a km %.9f e %.12g%n",orbit.getA()/1000.0,orbit.getE());
        System.out.printf("final   a km %.9f e %.12g%n",end.getOrbit().getA()/1000.0,end.getOrbit().getE());
        System.out.printf("period s %.6f dv m/s %.9f%n",period,dv);
    }
}

