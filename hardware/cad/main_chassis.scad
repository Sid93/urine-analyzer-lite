/*
 * Urine Analyzer Lite — Main Enclosure & Optical Assembly
 * Levram Lifesciences
 *
 * Modules:
 *   chassis_base()        — main shell with motor tray, PCB stand-offs
 *   optical_chamber()     — light-tight black chamber for LED + TCS34725 pair
 *   dipstick_tray()       — single-strip 6mm channel with acrylic guard slot
 *   mcu_tray()            — snap-fit bracket for ESP32-S3-DevKitC-1
 *   printer_bracket()     — mount for CSN-A2 thermal printer
 *   display_bezel()       — front panel with 4.3" LCD cutout
 *   uvc_shield()          — internal UV-C LED shroud
 *   belt_tensioner()      — adjustable GT2 belt idler arm
 *   limit_switch_bracket() — adjustable KW12-3 mount (use for home + end)
 *
 * Print settings:
 *   chassis_base, mcu_tray, dipstick_tray → PLA, 20% infill, 0.2mm layer
 *   optical_chamber, uvc_shield           → Black PLA, 100% infill, 0.1mm
 *   sensor mounts, printer_bracket        → PETG, 30% infill, 0.2mm, 4 perimeters
 */

// ── Global parameters ─────────────────────────────────────────────────────────
$fn = 48;

WALL   = 2.0;    // shell wall thickness
SCREW  = 3.2;    // M3 clearance hole diameter
INSERT = 4.2;    // M3 heat-set insert hole diameter
DRAFT  = 2;      // 2° draft for injection-mould compatibility

// ── Utility ───────────────────────────────────────────────────────────────────
module m3_hole(h=10)       { cylinder(d=SCREW,  h=h+1, center=false); }
module m3_insert(h=6)      { cylinder(d=INSERT, h=h,   center=false); }
module standoff(h=5, d=6)  { difference() { cylinder(d=d, h=h); m3_hole(h=h); } }
module fillet_cube(x,y,z,r=1) {
    minkowski() { cube([x-2*r, y-2*r, z], center=false); cylinder(r=r, h=0.01); }
}

// ── Chassis base ─────────────────────────────────────────────────────────────
module chassis_base() {
    W=160; D=120; H=55;
    difference() {
        // outer shell
        fillet_cube(W, D, H, r=3);
        // inner pocket
        translate([WALL, WALL, WALL])
            cube([W-2*WALL, D-2*WALL, H]);
        // strip tray slot on top front
        translate([25, D-30, H-WALL-0.1])
            cube([110, 20, WALL+1]);
        // USB-C cutout on right side
        translate([W-WALL-0.1, 50, 10])
            cube([WALL+1, 12, 8]);
        // display cutout on front
        translate([15, -0.1, 15])
            cube([130, WALL+1, 40]);
    }
    // PCB stand-offs (4×)
    for(pos=[[10,10],[10,D-22],[W-16,10],[W-16,D-22]])
        translate([pos[0], pos[1], WALL])
            standoff(h=8);
    // motor mount slot
    translate([W/2-20, 15, WALL])
        cube([40, 15, 6]);
}

// ── Optical chamber ──────────────────────────────────────────────────────────
module optical_chamber() {
    OW=65; OD=30; OH=45;
    difference() {
        cube([OW, OD, OH]);
        // sensor cavity (2× TCS34725 side by side, 10mm apart)
        for(sx=[5, 30])
            translate([sx, OD-12, OH-18])
                cube([20, 12+1, 18+1]);
        // LED window with diffuser slot
        translate([5, -0.1, 5])
            cube([OW-10, 6, OH-10]);
        translate([5, 4, 5])          // 2mm diffuser slot
            cube([OW-10, 2.1, OH-10]);
        // cable routing channel
        translate([OW-8, 5, 5])
            cube([6, OD-10, OH-10]);
        // M3 insert pockets (4 corners)
        for(pos=[[3,3],[3,OD-7],[OW-7,3],[OW-7,OD-7]])
            translate([pos[0], pos[1], 0])
                m3_insert(h=6);
    }
}

// ── Dipstick tray ─────────────────────────────────────────────────────────────
module dipstick_tray() {
    TW=120; TD=18; TH=8;
    difference() {
        cube([TW, TD, TH]);
        // 6mm channel for single reagent strip
        translate([5, (TD-6)/2, 2])
            cube([TW-10, 6, TH]);
        // acrylic guard slot (2mm deep, 2mm thick)
        translate([5, (TD-10)/2, TH-2])
            cube([TW-10, 10, 2.1]);
        // filter paper retainer ribs (leave 2mm every 15mm)
        for(i=[0:7])
            translate([5+i*15, (TD-6)/2, 0])
                cube([2, 6, 2]);
    }
    // end wall
    translate([TW-5, 0, 0]) cube([5, TD, TH]);
}

// ── MCU tray ──────────────────────────────────────────────────────────────────
module mcu_tray() {
    // ESP32-S3-DevKitC-1 footprint: 68.6 × 28.8mm, 2.1mm holes on 58.4×17.8mm
    BRDW=69; BRDD=29; TH=4;
    W2=BRDW+4; D2=BRDD+4;
    difference() {
        cube([W2, D2, TH]);
        // board pocket (0.5mm clearance)
        translate([2, 2, 1]) cube([BRDW, BRDD, TH]);
        // M3 mounting holes (4 corners)
        for(pos=[[0,0],[W2-5,0],[0,D2-5],[W2-5,D2-5]])
            translate([pos[0]+2.5, pos[1]+2.5, 0])
                m3_hole(h=TH);
    }
    // snap clips on long edges
    for(x=[15, W2-20])
        translate([x, D2, TH-2])
            cube([5, 3, 4]);
}

// ── Printer bracket ──────────────────────────────────────────────────────────
module printer_bracket() {
    // CSN-A2: 57.5mm wide, 37mm tall, 40mm deep
    PW=58; PD=40; PH=37;
    BWALL=2.5;
    difference() {
        cube([PW+2*BWALL, PD+BWALL, PH+BWALL]);
        translate([BWALL, 0, BWALL]) cube([PW, PD+1, PH]);
        // paper exit slot (top)
        translate([BWALL+5, PD-5, PH-5])
            cube([PW-10, BWALL+6, 5+1]);
        // USB access cutout (bottom rear)
        translate([BWALL+20, PD-6, 0])
            cube([18, BWALL+7, 10]);
        // 4× M3 mounting holes
        for(pos=[[3,5],[3,PD-5],[PW+BWALL-3,5],[PW+BWALL-3,PD-5]])
            translate([pos[0], pos[1], 0])
                m3_hole(h=PH);
    }
}

// ── Display bezel ─────────────────────────────────────────────────────────────
module display_bezel() {
    // Waveshare 4.3in DSI: 105 × 67mm active area
    BW=135; BH=80; BD=4;
    difference() {
        cube([BW, BH, BD]);
        // viewport
        translate([15, 7, -0.1]) cube([105, 66, BD+0.2]);
        // M3 holes (4 corners of bezel)
        for(pos=[[5,5],[5,BH-8],[BW-8,5],[BW-8,BH-8]])
            translate([pos[0], pos[1], 0])
                m3_hole(h=BD);
    }
}

// ── UV-C safety shroud ───────────────────────────────────────────────────────
module uvc_shield() {
    SW=30; SD=25; SH=20;
    difference() {
        cube([SW, SD, SH]);
        translate([WALL, WALL, WALL]) cube([SW-2*WALL, SD-2*WALL, SH]);
        // LED pocket top
        translate([SW/2-5, SD/2-5, 0]) cube([10, 10, 5]);
        // aluminium strip channel on face (for reflector)
        translate([-0.1, SD/2-2, 5]) cube([WALL+0.2, 4, SH-10]);
    }
}

// ── Belt tensioner ────────────────────────────────────────────────────────────
module belt_tensioner() {
    difference() {
        union() {
            cube([30, 12, 6]);
            translate([25, 6, 0]) cylinder(d=12, h=6);  // idler hub
        }
        // Idler bearing hole (625ZZ: 5mm ID)
        translate([25, 6, -0.1]) cylinder(d=5.1, h=6+0.2);
        // Slot for adjustment (4mm wide, 15mm long)
        translate([4, 4, -0.1]) cube([15, 4, 6+0.2]);
        // M3 bolt through slot
        translate([11, 6, -0.1]) m3_hole(h=6);
    }
}

// ── Limit switch bracket ──────────────────────────────────────────────────────
module limit_switch_bracket() {
    // KW12-3: 20×10×6mm body, 2×M2.5 at 9.5mm spacing
    difference() {
        cube([30, 18, 8]);
        // switch pocket
        translate([5, 4, 2]) cube([20, 10, 6+1]);
        // M2.5 mounting holes
        for(sx=[9, 18.5])
            translate([sx, 9, -0.1]) cylinder(d=2.7, h=8+0.2);
        // M3 chassis mount slot
        translate([0, 7, 4]) rotate([0, 90, 0])
            hull() {
                cylinder(d=SCREW, h=8);
                translate([0, 0, 20]) cylinder(d=SCREW, h=8);
            }
    }
}

// ── Render all parts spaced on build plate ────────────────────────────────────
translate([0,   0,  0])  chassis_base();
translate([170, 0,  0])  optical_chamber();
translate([170, 50, 0])  dipstick_tray();
translate([0,   130,0])  mcu_tray();
translate([80,  130,0])  printer_bracket();
translate([0,   170,0])  display_bezel();
translate([170, 90, 0])  uvc_shield();
translate([220, 90, 0])  belt_tensioner();
translate([260, 90, 0])  limit_switch_bracket();
