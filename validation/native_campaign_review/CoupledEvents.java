import java.nio.file.*;
import java.io.*;
import java.util.*;
import org.hipparchus.geometry.euclidean.threed.Vector3D;
import org.hipparchus.geometry.euclidean.threed.Rotation;
import org.hipparchus.geometry.euclidean.threed.RotationConvention;
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

/** Replay every prescribed burn/release from one initial host state.
 * Fixed inertial-axis J2 and ideal impulses; no actual release or host rating.
 */
public class CoupledEvents {
    static final double MU = 3.986004418e14;
    static final double RE = 6378137.0;
    static final double J2 = 1.08262668e-3;
    static final double ISP = 220.0;
    static final double G0 = 9.80665;
    static final double FINAL_TIME = 90000.0;
    static final ReplayContext CONFIG = new ReplayContext();
    static class ReplayContext {
        final org.orekit.frames.Frame frame = FramesFactory.getEME2000();
        final AbsoluteDate epoch = new AbsoluteDate(2026,9,29,0,0,0.0,TimeScalesFactory.getTAI());
    }
    static Vector3D vec(String[] a, int offset) {
        return new Vector3D(Double.parseDouble(a[offset]),Double.parseDouble(a[offset+1]),Double.parseDouble(a[offset+2]));
    }
    static PVCoordinates expected(String[] a, int offset) {
        return new PVCoordinates(vec(a,offset),vec(a,offset+3));
    }
    static PVCoordinates coast(PVCoordinates pv, double start, double end, double maxStep) {
        if (end < start - 1e-8) throw new IllegalArgumentException("Nonmonotonic event time");
        if (Math.abs(end-start) < 1e-10) return pv;
        var orbit = new CartesianOrbit(pv,CONFIG.frame,CONFIG.epoch.shiftedBy(start),MU);
        var integrator = new DormandPrince853Integrator(0.00001,maxStep,1e-8,2e-14);
        var propagator = new NumericalPropagator(integrator);
        propagator.setOrbitType(OrbitType.CARTESIAN);
        propagator.setInitialState(new SpacecraftState(orbit));
        propagator.addForceModel(new J2OnlyPerturbation(MU,RE,J2,CONFIG.frame));
        return propagator.propagate(CONFIG.epoch.shiftedBy(end)).getPVCoordinates();
    }
    public static void main(String[] args) throws Exception {
        Locale.setDefault(Locale.ROOT);
        String source = args[0]; String prefix = args[1];
        double maxStep = Double.parseDouble(args[2]);
        double fuel = Double.parseDouble(args[3]);
        double shotScale = args.length>4 ? Double.parseDouble(args[4]) : 1.0;
        double burnScale = args.length>5 ? Double.parseDouble(args[5]) : 1.0;
        double pitch = args.length>6 ? Math.toRadians(Double.parseDouble(args[6])) : 0.0;
        double yaw = args.length>7 ? Math.toRadians(Double.parseDouble(args[7])) : 0.0;
        double delay = args.length>8 ? Double.parseDouble(args[8]) : 0.0;
        List<String[]> events = new ArrayList<>();
        for (String line : Files.readAllLines(Path.of(source))) {
            if (!line.isBlank() && !line.startsWith("t_s")) events.add(line.split(","));
        }
        String[] first = events.get(0);
        if (!first[1].equals("initial")) throw new IllegalArgumentException("Initial state missing");
        PVCoordinates host = expected(first,9);
        PVCoordinates finalHostTarget = expected(first,15);
        double mass = Double.parseDouble(first[6]);
        double now = 0.0;
        double initialFuel = fuel;
        int releases = 0;
        double maxMomentumResidual = 0.0;
        double maxEnergyResidual = 0.0;
        try (PrintWriter hw = new PrintWriter(prefix+"_host.csv");
             PrintWriter pw = new PrintWriter(prefix+"_payload.csv")) {
            hw.println("t_s,event,position_residual_m,velocity_residual_m_s,mass_kg,mass_residual_kg,fuel_remaining_kg,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s");
            pw.println("payload,release_s,mass_kg,position_target_error_m,velocity_target_error_m_s,momentum_residual_kg_m_s,energy_identity_residual_J,relative_energy_J,x_m,y_m,z_m,vx_m_s,vy_m_s,vz_m_s");
            for (int k=1;k<events.size();k++) {
                String[] row = events.get(k);
                String kind = row[1];
                boolean transfer = kind.equals("burn") && row.length > 21 && row[21].startsWith("transfer ");
                // Keep the stipulated 20 s coast after the actual delayed release.
                // Later pre-burns/restoration remain frozen; no retargeting is implied.
                double time = Double.parseDouble(row[0]) + ((kind.equals("shot") || transfer) ? delay : 0.0);
                host = coast(host,now,time,maxStep);
                now = time;
                Vector3D command = vec(row,3);
                if (kind.equals("burn")) {
                    Vector3D dv = command.scalarMultiply(burnScale);
                    double consumed = -mass*Math.expm1(-dv.getNorm()/(ISP*G0));
                    if (consumed > fuel+1e-10) throw new IllegalArgumentException("Native fuel exhausted at "+time);
                    fuel -= consumed; mass -= consumed;
                    host = new PVCoordinates(host.getPosition(),host.getVelocity().add(dv));
                } else if (kind.equals("shot")) {
                    Vector3D axis = host.getPosition().crossProduct(command).normalize();
                    Vector3D radial = command.crossProduct(axis).normalize();
                    Vector3D relative = command.scalarMultiply(shotScale);
                    relative = new Rotation(axis,pitch,RotationConvention.VECTOR_OPERATOR).applyTo(relative);
                    relative = new Rotation(radial,yaw,RotationConvention.VECTOR_OPERATOR).applyTo(relative);
                    double childMass = Double.parseDouble(row[8]);
                    Vector3D prior = host.getVelocity();
                    Vector3D childVelocity = prior.add(relative.scalarMultiply(1.0-childMass/mass));
                    Vector3D parentVelocity = prior.subtract(relative.scalarMultiply(childMass/mass));
                    double momentum = childVelocity.scalarMultiply(childMass)
                        .add(parentVelocity.scalarMultiply(mass-childMass))
                        .subtract(prior.scalarMultiply(mass)).getNorm();
                    // Comoving calculation avoids cancellation of large orbital kinetic energies.
                    double gain = 0.5*childMass*childVelocity.subtract(prior).getNormSq()
                        +0.5*(mass-childMass)*parentVelocity.subtract(prior).getNormSq();
                    double relativeEnergy = 0.5*childMass*(mass-childMass)/mass*relative.getNormSq();
                    double energyError = Math.abs(gain-relativeEnergy);
                    maxMomentumResidual = Math.max(maxMomentumResidual,momentum);
                    maxEnergyResidual = Math.max(maxEnergyResidual,energyError);
                    PVCoordinates child = new PVCoordinates(host.getPosition(),childVelocity);
                    PVCoordinates delivered = coast(child,time,FINAL_TIME,maxStep);
                    PVCoordinates target = expected(row,15);
                    Vector3D r=delivered.getPosition(),v=delivered.getVelocity();
                    pw.printf("%s,%.12f,%.12f,%.12g,%.12g,%.12g,%.12g,%.12g,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f%n",
                        row[2],time,childMass,r.distance(target.getPosition()),v.distance(target.getVelocity()),
                        momentum,energyError,relativeEnergy,r.getX(),r.getY(),r.getZ(),v.getX(),v.getY(),v.getZ());
                    mass -= childMass;
                    host = new PVCoordinates(host.getPosition(),parentVelocity);
                    releases++;
                } else throw new IllegalArgumentException("Unknown event kind "+kind);
                PVCoordinates target = expected(row,9);
                Vector3D r=host.getPosition(),v=host.getVelocity();
                hw.printf("%.12f,%s,%.12g,%.12g,%.12f,%.12g,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f%n",
                    time,kind,r.distance(target.getPosition()),v.distance(target.getVelocity()),mass,
                    mass-Double.parseDouble(row[7]),fuel,r.getX(),r.getY(),r.getZ(),v.getX(),v.getY(),v.getZ());
            }
            host = coast(host,now,FINAL_TIME,maxStep);
            Vector3D r=host.getPosition(),v=host.getVelocity();
            hw.printf("%.12f,final_epoch,%.12g,%.12g,%.12f,NaN,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f,%.12f%n",
                FINAL_TIME,r.distance(finalHostTarget.getPosition()),v.distance(finalHostTarget.getVelocity()),mass,fuel,
                r.getX(),r.getY(),r.getZ(),v.getX(),v.getY(),v.getZ());
        }
        System.out.printf("Orekit13.1.6 full event replay: releases=%d fuel_used_kg=%.12f momentum_residual=%.12g energy_residual_J=%.12g%n",
            releases,initialFuel-fuel,maxMomentumResidual,maxEnergyResidual);
    }
}
