FeatureScript 3083;
import(path : "onshape/std/common.fs", version : "3083.0");

// NOMAD P0.1 physical test coupons: Feature Studio NOMAD_P01_Coupons (custom feature "P0.1 Coupons").
// Onshape is the CAD master for this geometry; this file is its snapshot (Onshape wins on conflict).
// References and cross-checks:
//   CAD/coupons/P0.1/generate_coupons.py   same dimensions -> reference STL / OpenSCAD
//   CAD/coupons/P0.1/onshape_crosscheck.py exact expected part sizes and volumes (true round holes)
//   prototypes/P0.1/coupons/P01_test_coupons.md   test design and procedure
// These are TEST ARTICLES on the provisional Concept C basis, not NOMAD lid parts. Their dimensions are
// local P0.1 test-rig constants and deliberately NOT in CAD/parameters/nomad.yaml: D-002 holds NOMAD
// product parameters, and a coupon constant must not be read as one.
//
// FRAME: every part is built in its PRINT orientation (Z = build direction, resting on Z = 0) with its
// min corner at the origin, then laid out side by side on the XY plane, CPN_LAYOUT_GAP apart.
// TEST = changing it changes what is measured. FIXTURE = test-rig only.

// ================= Coupon A: solar rail =================
export const CPN_RAIL_CHANNEL_LEN = 198 * millimeter;   // TEST: V1+fix rail = travel 158 + carriage 40
export const CPN_RAIL_END_STOP = 2 * millimeter;        // TEST: closed end BEYOND the channel (keeps the 149.5 arm)
export const CPN_RAIL_FLOOR_T = 2.5 * millimeter;       // TEST
export const CPN_RAIL_LIP_T = 2.5 * millimeter;         // TEST: retaining-lip thickness (Z)
export const CPN_RAIL_WALL_A1 = 2.5 * millimeter;       // TEST: A1 side wall
export const CPN_RAIL_WALL_A2 = 4.1 * millimeter;       // TEST: A2 side wall, thickened to host the strip slot
export const CPN_CHANNEL_W = 22.6 * millimeter;         // TEST: carriage channel width
export const CPN_CHANNEL_H = 8 * millimeter;            // TEST: carriage channel height
export const CPN_SLOT_W = 17.6 * millimeter;            // TEST: top slot; lip width = wall + (CHANNEL_W - SLOT_W) / 2
export const CPN_EAR_W = 12 * millimeter;               // TEST: side ear hosting the pad inserts
export const CPN_PAD_LEN = 28.5 * millimeter;           // TEST: ear length = pad overlap; the cantilever starts at rail X 28.5
export const CPN_INSERT_X = [7 * millimeter, 21.5 * millimeter]; // TEST: ear insert positions along the rail

// A2 flat-strip slots (10 x 2 aluminium or 10 x 1.5 steel; no strip material chosen)
export const CPN_STRIP_T = 2 * millimeter;              // TEST: strip envelope thickness
export const CPN_STRIP_H = 10 * millimeter;             // TEST: strip envelope height
export const CPN_STRIP_CLR_T = 0.3 * millimeter;        // TEST: slot = strip + clearance (2.3)
export const CPN_STRIP_CLR_H = 0.4 * millimeter;        // TEST: slot = strip + clearance (10.4)
export const CPN_STRIP_Z0 = 1.3 * millimeter;           // TEST: slot floor above the rail underside

// Carriage + load post
export const CPN_CAR_LEN = 40 * millimeter;             // TEST
export const CPN_CAR_CLR_Y = 0.3 * millimeter;          // TEST (fit): per side in the channel
export const CPN_CAR_CLR_Z = 0.6 * millimeter;          // TEST (fit): total vertical in the channel
export const CPN_POST_CLR = 0.5 * millimeter;           // TEST (fit): per side in the top slot
export const CPN_POST_H = 12.6 * millimeter;            // FIXTURE: load rod clears the lips by 1.75
export const CPN_LOAD_HOLE_D = 5.5 * millimeter;        // FIXTURE: M5 rod, teardrop (support-free)
export const CPN_LOAD_HOLE_BELOW_TOP = 5 * millimeter;  // FIXTURE: hole centre below the post top
export const CPN_EDGE_RELIEF = 0.5 * millimeter;        // FIXTURE: 0.5 x 0.5 relief on the body's long edges

// Load platform (FIXTURE; pocket fits over the post, printed pocket up)
export const CPN_PLATFORM_X = 60 * millimeter;
export const CPN_PLATFORM_Y = 60 * millimeter;
export const CPN_PLATFORM_T = 6 * millimeter;
export const CPN_PLATFORM_POCKET_DEPTH = 3 * millimeter;
export const CPN_PLATFORM_CLR = 0.3 * millimeter;

// Pad stub (front-frame pad: bezel 2.5 + pad 3.5)
export const CPN_PAD_STUB_X = 60 * millimeter;          // FIXTURE: footprint incl. clamp zone
export const CPN_PAD_STUB_Y = 70 * millimeter;          // FIXTURE
export const CPN_PAD_STUB_T = 6 * millimeter;           // TEST: sets the display gap
export const CPN_PAD_CLAMP_LEN = 31.5 * millimeter;     // FIXTURE: stub length outboard of the rail end
export const CPN_PAD_Y_OFFSET = 21 * millimeter;        // FIXTURE: rail ear outer face at stub Y 9
export const CPN_SCREW_CLEAR_D = 3.4 * millimeter;      // M3 clearance
export const CPN_CBORE_D = 6.5 * millimeter;            // M3 head counterbore (on the bed side)
export const CPN_CBORE_DEPTH = 3.5 * millimeter;

// Display surrogate: thickness = pad stub - display clearance
export const CPN_DISPLAY_CLEARANCE = 1 * millimeter;    // TEST: rail underside to display
export const CPN_SURROGATE_X = 170 * millimeter;        // FIXTURE
export const CPN_SURROGATE_Y = 30 * millimeter;         // FIXTURE

// Stowed carriage (at the end stop): centre to pad edge. Derived; the feature refuses to build if the
// constants above stop giving it.
export const CPN_STOWED_ARM = 149.5 * millimeter;       // = CHANNEL_LEN - CAR_LEN / 2 - PAD_LEN
export const CPN_TRAVEL = 158 * millimeter;             // = CHANNEL_LEN - CAR_LEN

// ================= Coupon B: rear shell =================
export const CPN_B_SPAN = 202 * millimeter;             // TEST: clear span between the supports
export const CPN_B_BAND = 14 * millimeter;              // TEST: support (screw) band each end
export const CPN_B_WIDTH = 90 * millimeter;             // TEST: strip width
export const CPN_B_PLATE_T = 2.5 * millimeter;          // TEST: plate / skin
export const CPN_B_BASE_T = 4 * millimeter;             // FIXTURE: frame base
export const CPN_B_SHELF_H = 10 * millimeter;           // TEST: shelf height above the base (seat plane Z 14)
export const CPN_B_SCREW_POS = [[7 * millimeter, 10 * millimeter], [7 * millimeter, 80 * millimeter]]; // TEST: per band, mirrored
export const CPN_B_RIB_T = 2 * millimeter;              // TEST: rib thickness
export const CPN_B_RIB_COUNT = 3;                       // TEST: longitudinal ribs, centred on the strip width
export const CPN_B_RIB_PITCH = 30 * millimeter;         // TEST: -> ribs at Y 15 / 45 / 75
// Transverse ribs: at both support edges and mid-span (fixed by the span/band; see cpnBuildPlate).
export const CPN_B_CLEARANCE = 1 * millimeter;          // TEST: clearance block top below the plate seat
export const CPN_B_BLOCK_X = 60 * millimeter;           // FIXTURE
export const CPN_B_BLOCK_Y = 60 * millimeter;           // FIXTURE
export const CPN_B_LOAD_PAD_X = 20 * millimeter;        // FIXTURE
export const CPN_B_LOAD_PAD_Y = 20 * millimeter;        // FIXTURE
export const CPN_B_LOAD_PAD_T = 5 * millimeter;         // FIXTURE

// ================= Layout / modelling =================
export const CPN_LAYOUT_GAP = 20 * millimeter;          // spacing between laid-out parts
export const CPN_TOOL_OVERRUN = 1 * millimeter;         // cutters run this far past open faces (not a part dimension)

// ================= Dialog parameters (bounds: min, default, max) =================
export const CPN_RIB_H1_BOUNDS = { (millimeter) : [1, 6, 30] } as LengthBoundSpec;
export const CPN_RIB_H2_BOUNDS = { (millimeter) : [1, 8, 30] } as LengthBoundSpec;
export const CPN_RIB_H3_BOUNDS = { (millimeter) : [1, 11, 30] } as LengthBoundSpec;
export const CPN_INSERT_D_BOUNDS = { (millimeter) : [3, 4, 6] } as LengthBoundSpec;     // set per insert datasheet
export const CPN_INSERT_DEPTH_BOUNDS = { (millimeter) : [3, 6, 10] } as LengthBoundSpec;

// BEGIN PRODUCTION FEATURES
annotation { "Feature Type Name" : "P0.1 Coupons" }
export const nomadP01Coupons = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "B2 rib height, plate 1" }
        isLength(definition.ribHeight1, CPN_RIB_H1_BOUNDS);
        annotation { "Name" : "B2 rib height, plate 2" }
        isLength(definition.ribHeight2, CPN_RIB_H2_BOUNDS);
        annotation { "Name" : "B2 rib height, plate 3" }
        isLength(definition.ribHeight3, CPN_RIB_H3_BOUNDS);
        annotation { "Name" : "Heat-set insert hole diameter" }
        isLength(definition.insertDiameter, CPN_INSERT_D_BOUNDS);
        annotation { "Name" : "Heat-set insert hole depth" }
        isLength(definition.insertDepth, CPN_INSERT_DEPTH_BOUNDS);
    }
    {
        cpnBuildAll(context, id, definition, true);
    }, { "ribHeight1" : 6 * millimeter, "ribHeight2" : 8 * millimeter, "ribHeight3" : 11 * millimeter,
            "insertDiameter" : 4 * millimeter, "insertDepth" : 6 * millimeter });
// END PRODUCTION FEATURES

// ================= Builders =================

// Builds all 13 coupons as separate named solids. layout = false leaves every part at the origin
// (validation harness); true lays them out side by side. Returns part name -> body query.
export function cpnBuildAll(context is Context, id is Id, definition is map, layout is boolean) returns map
{
    if (abs(CPN_RAIL_CHANNEL_LEN - CPN_CAR_LEN / 2 - CPN_PAD_LEN - CPN_STOWED_ARM) > 1e-6 * millimeter ||
        abs(CPN_RAIL_CHANNEL_LEN - CPN_CAR_LEN - CPN_TRAVEL) > 1e-6 * millimeter)
        throw regenError("P0.1 Coupons: constants no longer give the 149.5 stowed arm / 158 travel");

    const g = CPN_LAYOUT_GAP;
    const zero = 0 * millimeter;
    const ribs = [definition.ribHeight1, definition.ribHeight2, definition.ribHeight3];
    const bLen = CPN_B_SPAN + 2 * CPN_B_BAND;
    const wA1 = cpnRailWidth(false);
    const wA2 = cpnRailWidth(true);
    const xA = cpnRailLength() + g;
    const colA1 = wA1 + wA2 + CPN_SURROGATE_Y + 2 * g;
    const colA2 = CPN_PAD_STUB_Y + cpnCarriageWidth() + CPN_PLATFORM_Y + 2 * g;
    const yB = max(colA1, colA2) + 2 * g;
    const pitchB = CPN_B_WIDTH + g;
    const xB = bLen + g;

    // [id tag, part name, body, colour, layout origin]
    var specs = [
        ["a1", "CPN_A1_rail", cpnBuildRail(context, id + "a1", definition, false), cpnColorA(), [zero, zero]],
        ["a2", "CPN_A2_rail_stiffener_slots", cpnBuildRail(context, id + "a2", definition, true), cpnColorA(), [zero, wA1 + g]],
        ["sur", "CPN_A_display_surrogate", cpnBuildBlock(context, id + "sur", CPN_SURROGATE_X, CPN_SURROGATE_Y,
                    CPN_PAD_STUB_T - CPN_DISPLAY_CLEARANCE), cpnColorA(), [zero, wA1 + wA2 + 2 * g]],
        ["pad", "CPN_A_pad_stub", cpnBuildPadStub(context, id + "pad"), cpnColorA(), [xA, zero]],
        ["car", "CPN_A_carriage_load_post", cpnBuildCarriage(context, id + "car"), cpnColorFixture(), [xA, CPN_PAD_STUB_Y + g]],
        ["plat", "CPN_A_load_platform", cpnBuildPlatform(context, id + "plat"), cpnColorFixture(),
            [xA, CPN_PAD_STUB_Y + cpnCarriageWidth() + 2 * g]],
        ["bfr", "CPN_B_supports", cpnBuildFrame(context, id + "bfr", definition), cpnColorB(), [zero, yB]],
        ["blk", "CPN_B_clearance_block", cpnBuildBlock(context, id + "blk", CPN_B_BLOCK_X, CPN_B_BLOCK_Y,
                    CPN_B_SHELF_H - CPN_B_CLEARANCE), cpnColorB(), [xB, yB]],
        ["lpad", "CPN_B_load_pad", cpnBuildBlock(context, id + "lpad", CPN_B_LOAD_PAD_X, CPN_B_LOAD_PAD_Y, CPN_B_LOAD_PAD_T),
            cpnColorFixture(), [xB, yB + CPN_B_BLOCK_Y + g]],
        ["b1", "CPN_B1_plate", cpnBuildPlate(context, id + "b1", zero), cpnColorB(), [zero, yB + pitchB]]
    ];
    for (var i = 0; i < size(ribs); i += 1)
    {
        const tag = "b2" ~ i;
        specs = append(specs, [tag, cpnRibPlateName(ribs[i]), cpnBuildPlate(context, id + tag, ribs[i]), cpnColorB(),
                    [zero, yB + (i + 2) * pitchB]]);
    }

    var parts = {};
    for (var s in specs)
    {
        const q = s[2];
        if (size(evaluateQuery(context, qBodyType(q, BodyType.SOLID))) != 1)
            throw regenError("P0.1 Coupons: " ~ s[1] ~ " did not build as exactly one solid");
        setProperty(context, { "entities" : q, "propertyType" : PropertyType.NAME, "value" : s[1] });
        setProperty(context, { "entities" : q, "propertyType" : PropertyType.APPEARANCE, "value" : s[3] });
        if (layout)
            opTransform(context, id + ("place" ~ s[0]), { "bodies" : q, "transform" : transform(vector(s[4][0], s[4][1], zero)) });
        parts[s[1]] = q;
    }
    return parts;
}

// Rail A1 (stiffener = false) or A2 (true). Floor on the bed, top slot up, channel open at X 0,
// end stop beyond X = CHANNEL_LEN, ear at Y 0..EAR_W over X 0..PAD_LEN with blind inserts from below.
function cpnBuildRail(context is Context, id is Id, definition is map, stiffener is boolean) returns Query
{
    const zero = 0 * millimeter;
    const o = CPN_TOOL_OVERRUN;
    const wall = stiffener ? CPN_RAIL_WALL_A2 : CPN_RAIL_WALL_A1;
    const y0 = CPN_EAR_W;
    const y1 = cpnRailWidth(stiffener);
    const h = cpnRailHeight();
    const lip = (y1 - y0 - CPN_SLOT_W) / 2;
    cpnBox(context, id + "add" + "body", vector(zero, y0, zero), vector(cpnRailLength(), y1, h));
    cpnBox(context, id + "add" + "ear", vector(zero, zero, zero), vector(CPN_PAD_LEN, CPN_EAR_W, h));
    cpnBox(context, id + "sub" + "channel", vector(-o, y0 + wall, CPN_RAIL_FLOOR_T),
            vector(CPN_RAIL_CHANNEL_LEN, y0 + wall + CPN_CHANNEL_W, CPN_RAIL_FLOOR_T + CPN_CHANNEL_H));
    cpnBox(context, id + "sub" + "slot", vector(-o, y0 + lip, CPN_RAIL_FLOOR_T + CPN_CHANNEL_H),
            vector(CPN_RAIL_CHANNEL_LEN, y0 + lip + CPN_SLOT_W, h + o));
    for (var i = 0; i < size(CPN_INSERT_X); i += 1)
    {
        cpnCylZ(context, id + "sub" + ("insert" ~ i), CPN_INSERT_X[i], CPN_EAR_W / 2, definition.insertDiameter,
                -o, definition.insertDepth);
    }
    if (stiffener)
    {
        const st = CPN_STRIP_T + CPN_STRIP_CLR_T;
        const sh = CPN_STRIP_H + CPN_STRIP_CLR_H;
        const walls = [y0, y1 - wall];
        for (var i = 0; i < size(walls); i += 1)
        {
            const ys = walls[i] + (wall - st) / 2;
            cpnBox(context, id + "sub" + ("strip" ~ i), vector(-o, ys, CPN_STRIP_Z0),
                    vector(CPN_RAIL_CHANNEL_LEN, ys + st, CPN_STRIP_Z0 + sh));
        }
    }
    return cpnFinish(context, id);
}

// Carriage body + load post, body on the bed. Teardrop load hole along Y through the post.
function cpnBuildCarriage(context is Context, id is Id) returns Query
{
    const zero = 0 * millimeter;
    const o = CPN_TOOL_OVERRUN;
    const e = CPN_EDGE_RELIEF;
    const len = CPN_CAR_LEN;
    const bw = cpnCarriageWidth();
    const bh = CPN_CHANNEL_H - CPN_CAR_CLR_Z;
    const pw = CPN_SLOT_W - 2 * CPN_POST_CLR;
    const zTop = bh + CPN_POST_H;
    cpnBox(context, id + "add" + "body", vector(zero, zero, zero), vector(len, bw, bh));
    cpnBox(context, id + "add" + "post", vector(zero, (bw - pw) / 2, bh), vector(len, (bw + pw) / 2, zTop));
    cpnBox(context, id + "sub" + "r0", vector(-o, -o, -o), vector(len + o, e, e));
    cpnBox(context, id + "sub" + "r1", vector(-o, bw - e, -o), vector(len + o, bw + o, e));
    cpnBox(context, id + "sub" + "r2", vector(-o, -o, bh - e), vector(len + o, e, bh + o));
    cpnBox(context, id + "sub" + "r3", vector(-o, bw - e, bh - e), vector(len + o, bw + o, bh + o));
    cpnTeardropY(context, id + "sub" + "loadHole", len / 2, zTop - CPN_LOAD_HOLE_BELOW_TOP, CPN_LOAD_HOLE_D, -o, bw + o);
    return cpnFinish(context, id);
}

// Weight platform: plate with a pocket (printed up) that fits over the post.
function cpnBuildPlatform(context is Context, id is Id) returns Query
{
    const zero = 0 * millimeter;
    const o = CPN_TOOL_OVERRUN;
    const pw = CPN_SLOT_W - 2 * CPN_POST_CLR + 2 * CPN_PLATFORM_CLR;
    const pl = CPN_CAR_LEN + 2 * CPN_PLATFORM_CLR;
    cpnBox(context, id + "add" + "plate", vector(zero, zero, zero), vector(CPN_PLATFORM_X, CPN_PLATFORM_Y, CPN_PLATFORM_T));
    cpnBox(context, id + "sub" + "pocket", vector((CPN_PLATFORM_X - pl) / 2, (CPN_PLATFORM_Y - pw) / 2, CPN_PLATFORM_T - CPN_PLATFORM_POCKET_DEPTH),
            vector((CPN_PLATFORM_X + pl) / 2, (CPN_PLATFORM_Y + pw) / 2, CPN_PLATFORM_T + o));
    return cpnFinish(context, id);
}

// Pad stub: counterbored M3 clearance holes under the rail-ear inserts; counterbores on the bed side.
function cpnBuildPadStub(context is Context, id is Id) returns Query
{
    const zero = 0 * millimeter;
    const o = CPN_TOOL_OVERRUN;
    cpnBox(context, id + "add" + "plate", vector(zero, zero, zero), vector(CPN_PAD_STUB_X, CPN_PAD_STUB_Y, CPN_PAD_STUB_T));
    const y = CPN_PAD_Y_OFFSET - CPN_EAR_W / 2;
    for (var i = 0; i < size(CPN_INSERT_X); i += 1)
    {
        const x = CPN_PAD_CLAMP_LEN + CPN_INSERT_X[i];
        cpnCylZ(context, id + "sub" + ("screw" ~ i), x, y, CPN_SCREW_CLEAR_D, -o, CPN_PAD_STUB_T + o);
        cpnCylZ(context, id + "sub" + ("cbore" ~ i), x, y, CPN_CBORE_D, -o, CPN_CBORE_DEPTH);
    }
    return cpnFinish(context, id);
}

// Coupon B frame: base + two shelves (bands) leaving CPN_B_SPAN clear; blind inserts in the shelf tops.
function cpnBuildFrame(context is Context, id is Id, definition is map) returns Query
{
    const zero = 0 * millimeter;
    const o = CPN_TOOL_OVERRUN;
    const bLen = CPN_B_SPAN + 2 * CPN_B_BAND;
    const zTop = CPN_B_BASE_T + CPN_B_SHELF_H;
    cpnBox(context, id + "add" + "base", vector(zero, zero, zero), vector(bLen, CPN_B_WIDTH, CPN_B_BASE_T));
    cpnBox(context, id + "add" + "shelf0", vector(zero, zero, CPN_B_BASE_T), vector(CPN_B_BAND, CPN_B_WIDTH, zTop));
    cpnBox(context, id + "add" + "shelf1", vector(bLen - CPN_B_BAND, zero, CPN_B_BASE_T), vector(bLen, CPN_B_WIDTH, zTop));
    const screws = cpnBScrewXY();
    for (var i = 0; i < size(screws); i += 1)
    {
        cpnCylZ(context, id + "sub" + ("insert" ~ i), screws[i][0], screws[i][1], definition.insertDiameter,
                zTop - definition.insertDepth, zTop + o);
    }
    return cpnFinish(context, id);
}

// Coupon B plate: ribH = 0 -> B1 plain plate; ribH > 0 -> B2, skin on the bed, ribs up. Longitudinal ribs
// run the clear span between the support edges; transverse ribs sit on both support edges and mid-span.
// The screw bands stay rib-free.
function cpnBuildPlate(context is Context, id is Id, ribH is ValueWithUnits) returns Query
{
    const zero = 0 * millimeter;
    const o = CPN_TOOL_OVERRUN;
    const t = CPN_B_RIB_T;
    const bLen = CPN_B_SPAN + 2 * CPN_B_BAND;
    cpnBox(context, id + "add" + "plate", vector(zero, zero, zero), vector(bLen, CPN_B_WIDTH, CPN_B_PLATE_T));
    if (ribH > zero)
    {
        const zRib = CPN_B_PLATE_T + ribH;
        const firstY = (CPN_B_WIDTH - (CPN_B_RIB_COUNT - 1) * CPN_B_RIB_PITCH) / 2;
        for (var i = 0; i < CPN_B_RIB_COUNT; i += 1)
        {
            const y = firstY + i * CPN_B_RIB_PITCH;
            cpnBox(context, id + "add" + ("ribL" ~ i), vector(CPN_B_BAND, y - t / 2, CPN_B_PLATE_T),
                    vector(CPN_B_BAND + CPN_B_SPAN, y + t / 2, zRib));
        }
        const xs = [CPN_B_BAND, CPN_B_BAND + CPN_B_SPAN / 2, CPN_B_BAND + CPN_B_SPAN];
        for (var i = 0; i < size(xs); i += 1)
        {
            cpnBox(context, id + "add" + ("ribT" ~ i), vector(xs[i] - t / 2, zero, CPN_B_PLATE_T),
                    vector(xs[i] + t / 2, CPN_B_WIDTH, zRib));
        }
    }
    const screws = cpnBScrewXY();
    for (var i = 0; i < size(screws); i += 1)
    {
        cpnCylZ(context, id + "sub" + ("screw" ~ i), screws[i][0], screws[i][1], CPN_SCREW_CLEAR_D,
                -o, CPN_B_PLATE_T + ribH + o);
    }
    return cpnFinish(context, id);
}

// Plain rectangular block, min corner at the origin.
function cpnBuildBlock(context is Context, id is Id, x is ValueWithUnits, y is ValueWithUnits, z is ValueWithUnits) returns Query
{
    const zero = 0 * millimeter;
    cpnBox(context, id + "add" + "block", vector(zero, zero, zero), vector(x, y, z));
    return cpnFinish(context, id);
}

// ================= Helpers =================

function cpnRailLength() returns ValueWithUnits
{
    return CPN_RAIL_CHANNEL_LEN + CPN_RAIL_END_STOP;
}

function cpnRailHeight() returns ValueWithUnits
{
    return CPN_RAIL_FLOOR_T + CPN_CHANNEL_H + CPN_RAIL_LIP_T;
}

// Overall rail width in Y, ear included.
function cpnRailWidth(stiffener is boolean) returns ValueWithUnits
{
    return CPN_EAR_W + CPN_CHANNEL_W + 2 * (stiffener ? CPN_RAIL_WALL_A2 : CPN_RAIL_WALL_A1);
}

function cpnCarriageWidth() returns ValueWithUnits
{
    return CPN_CHANNEL_W - 2 * CPN_CAR_CLR_Y;
}

// B screw / insert positions: CPN_B_SCREW_POS in the first band, mirrored into the second.
function cpnBScrewXY() returns array
{
    const bLen = CPN_B_SPAN + 2 * CPN_B_BAND;
    var out = [];
    for (var p in CPN_B_SCREW_POS)
        out = append(out, p);
    for (var p in CPN_B_SCREW_POS)
        out = append(out, [bLen - p[0], p[1]]);
    return out;
}

// "CPN_B2_h6_plate" for a 6 mm rib height.
function cpnRibPlateName(ribH is ValueWithUnits) returns string
{
    return "CPN_B2_h" ~ toString(roundToPrecision(ribH / millimeter, 2)) ~ "_plate";
}

function cpnColorA() returns Color
{
    return color(0.90, 0.55, 0.15, 1);
}

function cpnColorB() returns Color
{
    return color(0.20, 0.50, 0.80, 1);
}

function cpnColorFixture() returns Color
{
    return color(0.62, 0.62, 0.62, 1);
}

function cpnBox(context is Context, id is Id, lo is Vector, hi is Vector)
{
    fCuboid(context, id, { "corner1" : lo, "corner2" : hi });
}

function cpnCylZ(context is Context, id is Id, cx is ValueWithUnits, cy is ValueWithUnits, d is ValueWithUnits,
    z0 is ValueWithUnits, z1 is ValueWithUnits)
{
    fCylinder(context, id, { "bottomCenter" : vector(cx, cy, z0), "topCenter" : vector(cx, cy, z1), "radius" : d / 2 });
}

// Hole along +Y that prints without support: circle of diameter d plus a square of side d/2 standing on
// its corner at the circle centre, so the roof apex is d/2 * sqrt(2) above the centre at 45 degrees.
function cpnTeardropY(context is Context, id is Id, cx is ValueWithUnits, cz is ValueWithUnits, d is ValueWithUnits,
    y0 is ValueWithUnits, y1 is ValueWithUnits)
{
    const r = d / 2;
    fCylinder(context, id + "round", { "bottomCenter" : vector(cx, y0, cz), "topCenter" : vector(cx, y1, cz), "radius" : r });
    fCuboid(context, id + "roof", { "corner1" : vector(-r / 2, y0, -r / 2), "corner2" : vector(r / 2, y1, r / 2) });
    const yAxis = line(vector(0, 0, 0) * millimeter, vector(0, 1, 0));
    opTransform(context, id + "roofPose", { "bodies" : qCreatedBy(id + "roof", EntityType.BODY),
                "transform" : transform(vector(cx, 0 * millimeter, cz + r / sqrt(2))) * rotationAround(yAxis, 45 * degree) });
}

// CSG: union of the bodies under id + "add", minus the bodies under id + "sub". Returns every body the
// part ends up as (exactly one if the part is sound; cpnBuildAll checks).
function cpnFinish(context is Context, id is Id) returns Query
{
    const adds = qCreatedBy(id + "add", EntityType.BODY);
    if (size(evaluateQuery(context, adds)) > 1)
        opBoolean(context, id + "union", { "tools" : adds, "operationType" : BooleanOperationType.UNION });
    const cutters = qCreatedBy(id + "sub", EntityType.BODY);
    if (size(evaluateQuery(context, cutters)) > 0)
        opBoolean(context, id + "cut", { "tools" : cutters, "targets" : adds, "operationType" : BooleanOperationType.SUBTRACTION });
    return qUnion([adds, qCreatedBy(id + "union", EntityType.BODY), qCreatedBy(id + "cut", EntityType.BODY)]);
}
