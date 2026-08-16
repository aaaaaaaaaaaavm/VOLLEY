// VOLLEY Gen5 -- an independent geometry implementation.
//
// WHY THIS EXISTS
// ---------------
// cad/build_gen5.py builds this machine with CadQuery, a B-rep kernel, and exports STEP.
// This file builds the same eight documents with OpenSCAD, a CSG kernel, and exports STL.
// Neither reads the other. Both read cad/scad/parameters.scad, which is built from
// cad/parameters.json, so the only thing they share is the parameter file that is supposed
// to be the single source of truth.
//
// That is the point. Everywhere else this project cross-checks a result by computing it a
// second way -- analytic against magpylib, both against a meshed FEM, orbit-averaged against
// Cowell. The geometry has never had that treatment: cad/parameters.json has been checked
// against exactly one model built from it. A disagreement between these two is either a bug
// in one of them or an ambiguity in the parameter file, and all three are worth knowing.
//
// A CSG model is not a manufacturing model, and neither is the B-rep one: no fillets,
// fasteners, harness routing or tolerancing exist in either.
//
// Usage:  openscad -D 'PART="track"' -o out.stl cad/scad/gen5.scad

include <parameters.scad>

$fn = 96;
PART = "all";

// ---------------------------------------------------------------- interface / ESPA

module interface_espa() {
    difference() {
        union() {
            // Flange ring, swept along +x from x_min.
            translate([interface_espa_x_min, 0, 0])
                rotate([0, 90, 0])
                    cylinder(h = interface_espa_flange_thickness,
                             d = interface_espa_flange_outer_diameter);
            // Hub plate at x = 0.
            rotate([0, 90, 0])
                cylinder(h = interface_espa_hub_plate_thickness,
                         d = interface_espa_hub_plate_diameter);
            // Four radial gussets at 45 deg, missing the track longerons.
            for (a = [45, 135, 225, 315])
                rotate([a, 0, 0])
                    translate([0, interface_espa_gusset_inner_radius,
                               -interface_espa_gusset_thickness / 2])
                        cube([interface_espa_hub_plate_thickness,
                              interface_espa_gusset_outer_radius
                                - interface_espa_gusset_inner_radius,
                              interface_espa_gusset_thickness]);
        }
        // Bolt circle, drilled through the flange only.
        for (i = [0 : interface_espa_bolt_hole_count - 1])
            rotate([360 * i / interface_espa_bolt_hole_count, 0, 0])
                translate([interface_espa_x_min - 1,
                           0, interface_espa_bolt_circle_diameter / 2])
                    rotate([0, 90, 0])
                        cylinder(h = interface_espa_flange_thickness + 2,
                                 d = interface_espa_bolt_hole_diameter);
    }
}

// ---------------------------------------------------------------- track

module track() {
    yo = track_overall_width / 2;        // beam runs to the track's overall width;
                                        // roller_channel_y_outer (90) is where the CHANNEL
                                        // ends, not where the longeron does.
    for (s = [1, -1]) {
        // Longeron beam.
        translate([0, s > 0 ? track_roller_channel_y_inner : -yo, track_longeron_z_min])
            cube([track_longeron_length, yo - track_roller_channel_y_inner,
                  track_longeron_z_max - track_longeron_z_min]);
        // Two guide rails per side, full length, inside the channel.
        for (zc = [track_guide_rail_z_contact, -track_guide_rail_z_contact])
            translate([0, s > 0 ? track_guide_rail_y_inner : -track_guide_rail_y_outer, zc])
                cube([track_longeron_length,
                      track_guide_rail_y_outer - track_guide_rail_y_inner,
                      track_guide_rail_z_outer - track_guide_rail_z_contact]);
        // Launch lock.
        translate([track_launch_lock_x_start,
                   s > 0 ? track_launch_lock_y_inner : -track_launch_lock_y_outer,
                   -track_launch_lock_z_half_height])
            cube([track_launch_lock_x_end - track_launch_lock_x_start,
                  track_launch_lock_y_outer - track_launch_lock_y_inner,
                  2 * track_launch_lock_z_half_height]);
    }
}

// ---------------------------------------------------------------- stator

module stator() {
    for (i = [0 : stator_conductor_count - 1])
        translate([stator_active_span_start + i * stator_belt_pitch,
                   -stator_active_width_y / 2, stator_belt_z_min])
            cube([stator_belt_width, stator_active_width_y,
                  stator_belt_z_max - stator_belt_z_min]);
}

// ---------------------------------------------------------------- sled

module sled() {
    L = sled_overall_length;
    W = sled_overall_width;
    H = sled_overall_height;
    a_off = (L - sled_halbach_array_length) / 2;
    x_aft = sled_halbach_array_x_start - a_off;
    zo = sled_halbach_array_z_outer;
    zi = sled_halbach_array_z_inner;

    for (s = [1, -1]) {
        // Chassis plate outboard of the magnets.
        translate([x_aft, -W / 2,
                   s > 0 ? zo : -zo - sled_chassis_plate_thickness])
            cube([L, W, sled_chassis_plate_thickness]);
        // Halbach array.
        translate([x_aft + a_off, -sled_halbach_array_width_y / 2, s > 0 ? zi : -zo])
            cube([sled_halbach_array_length, sled_halbach_array_width_y, zo - zi]);
    }
    // Side webs, outboard of the stator depth.
    for (s = [1, -1])
        translate([x_aft, s > 0 ? sled_chassis_web_y_inner : -sled_chassis_web_y_outer,
                   -(zo + sled_chassis_plate_thickness)])
            cube([L, sled_chassis_web_y_outer - sled_chassis_web_y_inner,
                  2 * (zo + sled_chassis_plate_thickness)]);
    // Backstop: the face the payload is pushed by.
    translate([x_aft, -W / 2, -H / 2])
        cube([sled_backstop_thickness, W, H]);
    // Four rollers.
    ry = (sled_roller_y_inner + sled_roller_y_outer) / 2;
    xc = x_aft + L / 2;
    for (dx = [-sled_roller_x_offset_from_centre, sled_roller_x_offset_from_centre])
        for (s = [1, -1])
            translate([xc + dx, s * ry - sled_roller_width / 2, 0])
                rotate([-90, 0, 0])
                    cylinder(h = sled_roller_width, d = sled_roller_diameter);
}

// ---------------------------------------------------------------- magazine cassette

module magazine_cassette() {
    lx = magazine_cassette_length_x;
    wy = magazine_cassette_width_y;
    hz = magazine_cassette_height_z;
    t  = magazine_shell_panel_thickness;
    union() {
        // Shell: closed panels, open at +Z (shell(-t) on the >Z face).
        difference() {
            translate([0, -wy / 2, 0]) cube([lx, wy, hz]);
            translate([t, -wy / 2 + t, t]) cube([lx - 2 * t, wy - 2 * t, hz]);
        }
        // Septa, one per cell boundary.
        for (i = [1 : magazine_satellites_per_cassette - 1]) {
            z = magazine_septum_z_min + i * magazine_satellite_pitch_z;
            if (z <= magazine_septum_z_max)
                translate([magazine_septum_x_min, -(wy - 2 * t) / 2, z])
                    cube([magazine_septum_x_max - magazine_septum_x_min,
                          wy - 2 * t, magazine_septum_thickness]);
        }
        // Retention gate frame.
        translate([0, -wy / 2, magazine_gate_frame_z_min])
            cube([lx, t, magazine_gate_frame_z_max - magazine_gate_frame_z_min]);
        // Two A-286 gate pins.
        for (x = magazine_gate_pin_x_positions)
            translate([x, -wy / 2, magazine_gate_frame_z_min
                       + (magazine_gate_frame_z_max - magazine_gate_frame_z_min) / 2])
                rotate([-90, 0, 0])
                    cylinder(h = wy, d = magazine_gate_pin_diameter);
    }
}

// ---------------------------------------------------------------- brake

module brake() {
    z = sled_halbach_array_z_outer + 10;
    t = brake_pole_plate_thickness;
    for (s = [1, -1])
        translate([0, -brake_pole_width_y / 2, s * z])
            rotate([90, 0, 0])
                translate([0, 0, -brake_pole_width_y])
                    linear_extrude(height = brake_pole_width_y)
                        polygon([[brake_x_start, 0],
                                 [brake_x_start + brake_pole_taper_entry_length, s * t],
                                 [brake_x_end, s * t],
                                 [brake_x_end, 0]]);
}

// ---------------------------------------------------------------- payload proxy

module payload_3u() {
    lx = payload_3u_length_x;
    wy = payload_3u_width_y;
    hz = payload_3u_height_z;
    r  = payload_3u_corner_rail_size;
    union() {
        translate([0, -(wy - 2 * r) / 2, -(hz - 2 * r) / 2])
            cube([lx, wy - 2 * r, hz - 2 * r]);
        for (sy = [1, -1])
            for (sz = [1, -1])
                translate([0, sy * (wy - r) / 2 - r / 2, sz * (hz - r) / 2 - r / 2])
                    cube([lx, r, r]);
    }
}

// ---------------------------------------------------------------- enclosure

module enclosure() {
    x0 = enclosure_x_min;
    x1 = enclosure_x_max;
    yh = enclosure_y_half_width;
    zb = enclosure_z_bottom_skin_outer;
    zt = enclosure_z_top_skin_outer;
    t  = enclosure_skin_thickness;
    union() {
        difference() {
            // Skins: shelled from the >X face, so the +x end is open before the muzzle
            // panel is cut -- matching build_gen5.py's .faces(">X").shell(-t).
            translate([x0, -yh, zb]) cube([x1 - x0, 2 * yh, zt - zb]);
            translate([x0 + t, -yh + t, zb + t])
                cube([x1 - x0, 2 * (yh - t), zt - zb - 2 * t]);
            // Muzzle aperture, genuinely open on the exit line.
            translate([enclosure_muzzle_panel_x - t,
                       enclosure_muzzle_aperture_centre_y
                         - enclosure_muzzle_aperture_width_y / 2,
                       enclosure_muzzle_aperture_centre_z
                         - enclosure_muzzle_aperture_height_z / 2])
                cube([3 * t, enclosure_muzzle_aperture_width_y,
                      enclosure_muzzle_aperture_height_z]);
            // Aft flange cutout: a horseshoe, breaching the lower edge by design.
            translate([x0 - t, 0, 0]) rotate([0, 90, 0])
                cylinder(h = 3 * t, d = enclosure_aft_flange_cutout_diameter);
        }
        // Radiator on the top skin.
        translate([enclosure_radiator_x_start, -enclosure_radiator_width / 2,
                   enclosure_radiator_z])
            cube([enclosure_radiator_length, enclosure_radiator_width,
                  enclosure_radiator_thickness]);
    }
}

// ---------------------------------------------------------------- dispatch

if      (PART == "interface_espa")    interface_espa();
else if (PART == "track")             track();
else if (PART == "stator")            stator();
else if (PART == "sled")              sled();
else if (PART == "magazine_cassette") magazine_cassette();
else if (PART == "brake")             brake();
else if (PART == "payload_3u")        payload_3u();
else if (PART == "enclosure")         enclosure();
else if (PART == "mechanism") {
    // Everything the enclosure hides. The closed machine is a box; this is the object.
    interface_espa(); track(); stator(); sled(); magazine_cassette(); brake();
}
else {
    interface_espa(); track(); stator(); sled();
    magazine_cassette(); brake(); payload_3u(); enclosure();
}
