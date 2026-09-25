FeatureScript 3083;
import(path : "onshape/std/common.fs", version : "3083.0");

// NOMAD P0.1 geometry layer (D-001: FeatureScript for P0.1 only).
// Round A: parameter block, frames, base skeleton, keyboard/trackpad envelopes,
// lid skeleton, display envelope, lid poses. Envelope level only.
// Every TBD dimension here is a provisional WORKING input, not an engineering value
// (see NOMAD_PARAM_BASIS and CAD/parameters/nomad.yaml).
//
// WORLD FRAME: origin at the base bottom-front edge on the chassis centreline.
// +X right, +Y rear (toward the hinge), +Z up. Lateral offset 0 = centreline (D-003).

// BEGIN GENERATED PARAMS
// Generated from CAD/parameters/nomad.yaml by CAD/tools/yaml_to_featurescript.py.
// DO NOT EDIT. The YAML is the source of truth (D-002).
// Labels: VALUE = authoritative value (with its status); WORKING / FORMULA = P0.1
// working input for a TBD parameter: provisional, not an engineering value.
// --- body ---
export const BODY_WIDTH = 301 * millimeter; // WORKING via FORMULA KEYBOARD_WIDTH + 2 * (BASE_SIDE_MARGIN + WALL_THICKNESS) = 301 (status TBD)
export const BODY_DEPTH = 235 * millimeter; // WORKING via FORMULA BASE_FRONT_MARGIN + TRACKPAD_DEPTH + TRACKPAD_KEYBOARD_GAP + KEYBOARD_DEPTH + BASE_REAR_ZONE_DEPTH = 235 (status TBD)
export const BODY_HEIGHT = 40 * millimeter; // WORKING (status TBD)
export const WALL_THICKNESS = 2.5 * millimeter; // WORKING (status TBD)
export const BASE_SIDE_MARGIN = 8 * millimeter; // WORKING (status TBD)
export const BASE_FRONT_MARGIN = 15 * millimeter; // WORKING (status TBD)
export const BASE_REAR_ZONE_DEPTH = 30 * millimeter; // WORKING (status TBD)
export const HINGE_AXIS_OFFSET = 0 * millimeter; // WORKING (status TBD)
export const HINGE_AXIS_HEIGHT = 0 * millimeter; // WORKING (status TBD)
// --- lid ---
export const LID_THICKNESS = 25 * millimeter; // WORKING (status TBD)
export const LID_CLOSED_GAP = 2 * millimeter; // WORKING (status TBD)
export const LID_ANGLE_NOMINAL = 105 * degree; // WORKING (status TBD)
export const LID_ANGLE_MAX = 135 * degree; // WORKING (status TBD)
// --- display ---
export const DISPLAY_DIAGONAL = 256.5 * millimeter; // VALUE (provisional)
export const DISPLAY_ACTIVE_WIDTH = 217.5 * millimeter; // VALUE (derived)
export const DISPLAY_ACTIVE_HEIGHT = 136 * millimeter; // VALUE (derived)
export const DISPLAY_WIDTH = 235 * millimeter; // WORKING (status TBD)
export const DISPLAY_HEIGHT = 150 * millimeter; // WORKING (status TBD)
export const DISPLAY_THICKNESS = 5 * millimeter; // WORKING (status TBD)
export const DISPLAY_VERTICAL_OFFSET = 0 * millimeter; // WORKING (status TBD)
// --- controls ---
export const KEYBOARD_WIDTH = 280 * millimeter; // VALUE (provisional)
export const KEYBOARD_DEPTH = 105 * millimeter; // VALUE (provisional)
export const KEYBOARD_THICKNESS = 8 * millimeter; // VALUE (provisional)
export const TRACKPAD_WIDTH = 86 * millimeter; // WORKING (status TBD)
export const TRACKPAD_DEPTH = 75 * millimeter; // WORKING (status TBD)
export const TRACKPAD_THICKNESS = 13 * millimeter; // WORKING (status TBD)
// --- layout ---
export const KEYBOARD_LATERAL_OFFSET = 0 * millimeter; // WORKING (status TBD)
export const TRACKPAD_LATERAL_OFFSET = 0 * millimeter; // WORKING (status TBD)
export const TRACKPAD_KEYBOARD_GAP = 10 * millimeter; // WORKING (status TBD)
export const KEYBOARD_TOP_RECESS = 1 * millimeter; // WORKING (status TBD)
export const TRACKPAD_TOP_RECESS = 1 * millimeter; // WORKING (status TBD)
// --- computer ---
export const PI_WIDTH = 85 * millimeter; // VALUE (provisional)
export const PI_DEPTH = 56 * millimeter; // VALUE (provisional)
export const NVME_FORMAT = "2230"; // VALUE (provisional)
// --- clearances ---
export const CLEARANCE = 0.3 * millimeter; // WORKING (status TBD)
export const MIN_GAP = 1 * millimeter; // WORKING (status TBD)
// --- fasteners ---
export const FASTENER_SIZE = ["M3", "M2.5"]; // VALUE (provisional)
// --- solar ---
export const SOLAR_CASSETTE_WIDTH = 147.5 * millimeter; // WORKING via FORMULA (BODY_WIDTH - 2 * WALL_THICKNESS - MIN_GAP) / 2 = 147.5 (status TBD)
export const SOLAR_CASSETTE_HEIGHT = 200 * millimeter; // WORKING (status TBD)
export const SOLAR_CASSETTE_THICKNESS = 8 * millimeter; // WORKING (status TBD)
export const SOLAR_ROTATION_LIMIT = { "min" : 60 * degree, "max" : 75 * degree }; // VALUE (provisional)
export const SOLAR_ROTATION_AXIS = "slide_direction"; // VALUE (provisional)
export const SOLAR_DEPLOY_CLEARANCE = 5 * millimeter; // WORKING (status TBD)
export const SOLAR_SLIDE_TRAVEL = 155 * millimeter; // WORKING via FORMULA SOLAR_CASSETTE_WIDTH + WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE = 155 (status TBD)
export const SOLAR_RAIL_ENGAGEMENT = 40 * millimeter; // WORKING (status TBD)
export const SOLAR_CARRIAGE_WIDTH = 12 * millimeter; // WORKING (status TBD)
export const SOLAR_CARRIAGE_HEIGHT = 8 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_LINK_LENGTH = 8.5 * millimeter; // WORKING via FORMULA WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE + MIN_GAP = 8.5 (status TBD)
export const SOLAR_HUB_AXIS_OFFSET_Y = 100 * millimeter; // WORKING via FORMULA SOLAR_CASSETTE_HEIGHT / 2 = 100 (status TBD)
export const SOLAR_HUB_AXIS_OFFSET_Z = 4 * millimeter; // WORKING via FORMULA SOLAR_CASSETTE_THICKNESS / 2 = 4 (status TBD)
export const SOLAR_INDEX_STEP = 15 * degree; // WORKING (status TBD)
export const SOLAR_HUB_PIN_DIAMETER = 5 * millimeter; // WORKING (status TBD)
export const NOMAD_PARAM_BASIS = { "BODY_WIDTH" : "formula", "BODY_DEPTH" : "formula", "BODY_HEIGHT" : "working", "WALL_THICKNESS" : "working", "BASE_SIDE_MARGIN" : "working", "BASE_FRONT_MARGIN" : "working", "BASE_REAR_ZONE_DEPTH" : "working", "HINGE_AXIS_OFFSET" : "working", "HINGE_AXIS_HEIGHT" : "working", "LID_THICKNESS" : "working", "LID_CLOSED_GAP" : "working", "LID_ANGLE_NOMINAL" : "working", "LID_ANGLE_MAX" : "working", "DISPLAY_DIAGONAL" : "value", "DISPLAY_ACTIVE_WIDTH" : "value", "DISPLAY_ACTIVE_HEIGHT" : "value", "DISPLAY_WIDTH" : "working", "DISPLAY_HEIGHT" : "working", "DISPLAY_THICKNESS" : "working", "DISPLAY_VERTICAL_OFFSET" : "working", "KEYBOARD_WIDTH" : "value", "KEYBOARD_DEPTH" : "value", "KEYBOARD_THICKNESS" : "value", "TRACKPAD_WIDTH" : "working", "TRACKPAD_DEPTH" : "working", "TRACKPAD_THICKNESS" : "working", "KEYBOARD_LATERAL_OFFSET" : "working", "TRACKPAD_LATERAL_OFFSET" : "working", "TRACKPAD_KEYBOARD_GAP" : "working", "KEYBOARD_TOP_RECESS" : "working", "TRACKPAD_TOP_RECESS" : "working", "PI_WIDTH" : "value", "PI_DEPTH" : "value", "NVME_FORMAT" : "value", "CLEARANCE" : "working", "MIN_GAP" : "working", "FASTENER_SIZE" : "value", "SOLAR_CASSETTE_WIDTH" : "formula", "SOLAR_CASSETTE_HEIGHT" : "working", "SOLAR_CASSETTE_THICKNESS" : "working", "SOLAR_ROTATION_LIMIT" : "value", "SOLAR_ROTATION_AXIS" : "value", "SOLAR_DEPLOY_CLEARANCE" : "working", "SOLAR_SLIDE_TRAVEL" : "formula", "SOLAR_RAIL_ENGAGEMENT" : "working", "SOLAR_CARRIAGE_WIDTH" : "working", "SOLAR_CARRIAGE_HEIGHT" : "working", "SOLAR_HUB_LINK_LENGTH" : "formula", "SOLAR_HUB_AXIS_OFFSET_Y" : "formula", "SOLAR_HUB_AXIS_OFFSET_Z" : "formula", "SOLAR_INDEX_STEP" : "working", "SOLAR_HUB_PIN_DIAMETER" : "working" };
export const NOMAD_UNRESOLVED = ["SERVICE_PANEL_THICKNESS", "PI_STACK_HEIGHT", "GNSS_ANTENNA_KEEPOUT", "MIN_WALL", "CABLE_CLEARANCE", "OVERHANG_LIMIT", "INSERT_SIZE", "BATTERY_BAY_WIDTH", "BATTERY_BAY_DEPTH", "BATTERY_BAY_HEIGHT"];
// END GENERATED PARAMS

export const NOMAD_ATTRIBUTE = "nomad";
export const NOMAD_ROUND_A_BODIES = ["SKEL_BASE", "ENV_KEYBOARD", "ENV_TRACKPAD", "SKEL_LID", "ENV_DISPLAY"];
// Envelope -> skeleton it must sit inside (checked in the rigid closed pose).
export const NOMAD_PARENTS = { "ENV_KEYBOARD" : "SKEL_BASE", "ENV_TRACKPAD" : "SKEL_BASE", "ENV_DISPLAY" : "SKEL_LID" };

// ================= Frames =================

// A hinge definition: axis inset from the base rear face and height above the base top surface.
export function nomadDefaultHinge() returns map
{
    return { "offset" : HINGE_AXIS_OFFSET, "height" : HINGE_AXIS_HEIGHT };
}

export function nomadHingePoint(hinge is map) returns Vector
{
    return vector(0 * millimeter, BODY_DEPTH - hinge.offset, BODY_HEIGHT + hinge.height);
}

// Axis direction is -X so that a positive angle raises the lid's free (front) edge.
export function nomadHingeLine(hinge is map) returns Line
{
    return line(nomadHingePoint(hinge), vector(-1, 0, 0));
}

export function nomadLidTransform(angle is ValueWithUnits, hinge is map) returns Transform
{
    return rotationAround(nomadHingeLine(hinge), angle);
}

export enum NomadLidPose
{
    annotation { "Name" : "Closed" }
    CLOSED,
    annotation { "Name" : "Nominal open" }
    NOMINAL,
    annotation { "Name" : "Maximum open" }
    MAX
}

export function nomadLidPoseAngle(pose is NomadLidPose) returns ValueWithUnits
{
    if (pose == NomadLidPose.CLOSED)
        return 0 * degree;
    if (pose == NomadLidPose.NOMINAL)
        return LID_ANGLE_NOMINAL;
    return LID_ANGLE_MAX;
}

// ================= Helpers =================

function nomadSkelColor() returns Color
{
    return color(0.72, 0.74, 0.78, 0.35);
}

function nomadEnvColor() returns Color
{
    return color(0.22, 0.45, 0.85, 1);
}

function nomadTag(context is Context, body is Query, name is string, col is Color)
{
    setProperty(context, { "entities" : body, "propertyType" : PropertyType.NAME, "value" : name });
    setProperty(context, { "entities" : body, "propertyType" : PropertyType.APPEARANCE, "value" : col });
    setAttribute(context, { "entities" : body, "name" : NOMAD_ATTRIBUTE, "attribute" : name });
}

function nomadBox(context is Context, id is Id, c1 is Vector, c2 is Vector) returns Query
{
    fCuboid(context, id, { "corner1" : c1, "corner2" : c2 });
    return qCreatedBy(id, EntityType.BODY);
}

// Box c1..c2 (c1 < c2 on every axis) hollowed by `wall` on all sides except one Z face:
// openSide > 0 leaves the max-Z face open, openSide < 0 the min-Z face.
function nomadTray(context is Context, id is Id, c1 is Vector, c2 is Vector, wall is ValueWithUnits, openSide is number) returns Query
{
    const outer = nomadBox(context, id + "outer", c1, c2);
    const lo = vector(c1[0] + wall, c1[1] + wall, openSide < 0 ? c1[2] - wall : c1[2] + wall);
    const hi = vector(c2[0] - wall, c2[1] - wall, openSide > 0 ? c2[2] + wall : c2[2] - wall);
    const cavity = nomadBox(context, id + "cavity", lo, hi);
    opBoolean(context, id + "cut", { "tools" : cavity, "targets" : outer, "operationType" : BooleanOperationType.SUBTRACTION });
    return outer;
}

// ================= Builders =================

export function nomadBuildBase(context is Context, id is Id) returns map
{
    const halfW = BODY_WIDTH / 2;
    const zero = 0 * millimeter;
    const base = nomadTray(context, id + "shell", vector(-halfW, zero, zero), vector(halfW, BODY_DEPTH, BODY_HEIGHT), WALL_THICKNESS, 1);
    nomadTag(context, base, "SKEL_BASE", nomadSkelColor());

    // D-003: trackpad centred below the keyboard; both on the centreline at offset 0.
    const tpY0 = BASE_FRONT_MARGIN;
    const kbY0 = tpY0 + TRACKPAD_DEPTH + TRACKPAD_KEYBOARD_GAP;
    const kbTop = BODY_HEIGHT - KEYBOARD_TOP_RECESS;
    const keyboard = nomadBox(context, id + "keyboard",
            vector(KEYBOARD_LATERAL_OFFSET - KEYBOARD_WIDTH / 2, kbY0, kbTop - KEYBOARD_THICKNESS),
            vector(KEYBOARD_LATERAL_OFFSET + KEYBOARD_WIDTH / 2, kbY0 + KEYBOARD_DEPTH, kbTop));
    nomadTag(context, keyboard, "ENV_KEYBOARD", nomadEnvColor());

    const tpTop = BODY_HEIGHT - TRACKPAD_TOP_RECESS;
    const trackpad = nomadBox(context, id + "trackpad",
            vector(TRACKPAD_LATERAL_OFFSET - TRACKPAD_WIDTH / 2, tpY0, tpTop - TRACKPAD_THICKNESS),
            vector(TRACKPAD_LATERAL_OFFSET + TRACKPAD_WIDTH / 2, tpY0 + TRACKPAD_DEPTH, tpTop));
    nomadTag(context, trackpad, "ENV_TRACKPAD", nomadEnvColor());

    return { "SKEL_BASE" : base, "ENV_KEYBOARD" : keyboard, "ENV_TRACKPAD" : trackpad };
}

// Built in the closed pose (resting LID_CLOSED_GAP above the base, display face down),
// then rotated about the hinge.
export function nomadBuildLid(context is Context, id is Id, angle is ValueWithUnits, hinge is map) returns map
{
    const halfW = BODY_WIDTH / 2;
    const zero = 0 * millimeter;
    const lidZ0 = BODY_HEIGHT + LID_CLOSED_GAP;
    const lid = nomadTray(context, id + "shell", vector(-halfW, zero, lidZ0), vector(halfW, BODY_DEPTH, lidZ0 + LID_THICKNESS), WALL_THICKNESS, -1);
    nomadTag(context, lid, "SKEL_LID", nomadSkelColor());

    // Closed pose: the lid free edge is at y = 0, so a positive offset moves toward -Y.
    const displayCentreY = BODY_DEPTH / 2 - DISPLAY_VERTICAL_OFFSET;
    const display = nomadBox(context, id + "display",
            vector(-DISPLAY_WIDTH / 2, displayCentreY - DISPLAY_HEIGHT / 2, lidZ0),
            vector(DISPLAY_WIDTH / 2, displayCentreY + DISPLAY_HEIGHT / 2, lidZ0 + DISPLAY_THICKNESS));
    nomadTag(context, display, "ENV_DISPLAY", nomadEnvColor());

    opTransform(context, id + "pose", { "bodies" : qUnion([lid, display]), "transform" : nomadLidTransform(angle, hinge) });
    return { "SKEL_LID" : lid, "ENV_DISPLAY" : display };
}

export function nomadBuildRoundA(context is Context, id is Id, lidAngle is ValueWithUnits, hinge is map) returns map
{
    return mergeMaps(nomadBuildBase(context, id + "base"), nomadBuildLid(context, id + "lid", lidAngle, hinge));
}

// Finds each Round A body by its NOMAD attribute within `scope`; exactly one must exist.
export function nomadCollect(context is Context, scope is Query) returns map
{
    var bodies = {};
    for (var name in NOMAD_ROUND_A_BODIES)
    {
        const q = qHasAttributeWithValue(scope, NOMAD_ATTRIBUTE, name);
        if (size(evaluateQuery(context, q)) != 1)
            throw regenError("NOMAD: expected exactly one body tagged " ~ name);
        bodies[name] = q;
    }
    return bodies;
}

// ================= Checks =================

function nomadMm(v is ValueWithUnits) returns number
{
    return roundToPrecision(v / millimeter, 3);
}

export function nomadBoxReport(context is Context, q is Query) returns map
{
    const b = evBox3d(context, { "topology" : q, "tight" : true });
    var mn = [];
    var mx = [];
    var sz = [];
    for (var k = 0; k < 3; k += 1)
    {
        mn = append(mn, nomadMm(b.minCorner[k]));
        mx = append(mx, nomadMm(b.maxCorner[k]));
        sz = append(sz, nomadMm(b.maxCorner[k] - b.minCorner[k]));
    }
    return { "min" : mn, "max" : mx, "size" : sz };
}

function nomadPair(context is Context, nameA is string, a is Query, nameB is string, b is Query) returns map
{
    const overlapTypes = [ClashType.INTERFERE, ClashType.TARGET_IN_TOOL, ClashType.TOOL_IN_TARGET];
    const clashes = evCollision(context, { "tools" : a, "targets" : b });
    var state = "clear";
    var types = [];
    for (var c in clashes)
    {
        const t = c["type"] != undefined ? c["type"] : c["clashType"];
        types = append(types, toString(t));
        if (isIn(t, overlapTypes))
            state = "overlap";
        else if (state == "clear" && t != ClashType.NONE)
            state = "contact";
    }
    const gap = state == "overlap" ? 0 : nomadMm(evDistance(context, { "side0" : a, "side1" : b }).distance);
    return { "a" : nameA, "b" : nameB, "state" : state, "gap_mm" : gap, "clash_types" : types };
}

// Pairwise overlap/gap check of all Round A bodies in one pose, plus ground and extents.
export function nomadCheckPose(context is Context, bodies is map, angle is ValueWithUnits) returns map
{
    const names = NOMAD_ROUND_A_BODIES;
    const closed = abs(angle) < 1e-6 * degree;
    var pairs = [];
    var issues = [];
    var expected = [];
    var allBodies = [];
    for (var i = 0; i < size(names); i += 1)
    {
        allBodies = append(allBodies, bodies[names[i]]);
        for (var j = i + 1; j < size(names); j += 1)
        {
            const p = nomadPair(context, names[i], bodies[names[i]], names[j], bodies[names[j]]);
            pairs = append(pairs, p);
            const seating = closed && p.a == "SKEL_BASE" && p.b == "SKEL_LID";
            if (p.state == "overlap")
                issues = append(issues, "OVERLAP " ~ p.a ~ " x " ~ p.b);
            else if (p.gap_mm < MIN_GAP / millimeter - 1e-6)
            {
                const msg = p.a ~ " x " ~ p.b ~ " gap " ~ toString(p.gap_mm) ~ " mm < MIN_GAP";
                if (seating)
                    expected = append(expected, "closed-lid seating contact: " ~ msg);
                else
                    issues = append(issues, "GAP " ~ msg);
            }
        }
    }
    const overall = nomadBoxReport(context, qUnion(allBodies));
    if (overall.min[2] < -1e-3)
        issues = append(issues, "BELOW GROUND: min z " ~ toString(overall.min[2]) ~ " mm");
    return { "lid_angle_deg" : roundToPrecision(angle / degree, 3), "issues" : issues, "expected_contacts" : expected,
            "overall" : overall, "pairs" : pairs };
}

// Bounding-box containment of each envelope in its skeleton (valid in any rigid pose; used closed).
export function nomadContainment(context is Context, bodies is map) returns array
{
    var out = [];
    const eps = TOLERANCE.zeroLength * meter;
    for (var child, parent in NOMAD_PARENTS)
    {
        const c = evBox3d(context, { "topology" : bodies[child], "tight" : true });
        const p = evBox3d(context, { "topology" : bodies[parent], "tight" : true });
        var inside = true;
        var margins = [];
        for (var k = 0; k < 3; k += 1)
        {
            const lo = c.minCorner[k] - p.minCorner[k];
            const hi = p.maxCorner[k] - c.maxCorner[k];
            margins = append(margins, [nomadMm(lo), nomadMm(hi)]);
            if (lo < -eps || hi < -eps)
                inside = false;
        }
        out = append(out, { "child" : child, "parent" : parent, "inside_bbox" : inside, "margins_mm_xyz" : margins });
    }
    return out;
}

export function nomadWorkingCount() returns number
{
    var n = 0;
    for (var name, basis in NOMAD_PARAM_BASIS)
    {
        if (basis != "value")
            n += 1;
    }
    return n;
}

export function nomadJson(v) returns string
{
    if (v == undefined)
        return "null";
    if (v is boolean)
        return v ? "true" : "false";
    if (v is number)
        return toString(v);
    if (v is string)
        return "\"" ~ v ~ "\"";
    if (v is array)
    {
        var s = "[";
        for (var i = 0; i < size(v); i += 1)
            s = s ~ (i == 0 ? "" : ",") ~ nomadJson(v[i]);
        return s ~ "]";
    }
    if (v is map && !(v is ValueWithUnits))
    {
        var s = "{";
        var first = true;
        for (var k, e in v)
        {
            s = s ~ (first ? "" : ",") ~ "\"" ~ toString(k) ~ "\":" ~ nomadJson(e);
            first = false;
        }
        return s ~ "}";
    }
    return "\"" ~ toString(v) ~ "\"";
}

// BEGIN PRODUCTION FEATURES
annotation { "Feature Type Name" : "NOMAD Skeleton" }
export const nomadSkeleton = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const published = { "BODY_WIDTH" : BODY_WIDTH, "BODY_DEPTH" : BODY_DEPTH, "BODY_HEIGHT" : BODY_HEIGHT,
                "WALL_THICKNESS" : WALL_THICKNESS, "LID_THICKNESS" : LID_THICKNESS };
        for (var name, value in published)
            setVariable(context, name, value);
        reportFeatureInfo(context, id, "NOMAD P0.1: " ~ toString(nomadWorkingCount()) ~
                    " parameters are provisional working inputs, not engineering values");
    }, {});

annotation { "Feature Type Name" : "NOMAD Base" }
export const nomadBase = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        nomadBuildBase(context, id);
    }, {});

annotation { "Feature Type Name" : "NOMAD Lid" }
export const nomadLid = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Lid pose" }
        definition.lidPose is NomadLidPose;
    }
    {
        const angle = nomadLidPoseAngle(definition.lidPose);
        nomadBuildLid(context, id, angle, nomadDefaultHinge());
        setVariable(context, "NOMAD_LID_ANGLE", angle);
    }, { "lidPose" : NomadLidPose.NOMINAL });

annotation { "Feature Type Name" : "NOMAD Clearance Check" }
export const nomadClearanceCheck = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const bodies = nomadCollect(context, qEverything(EntityType.BODY));
        const result = nomadCheckPose(context, bodies, getVariable(context, "NOMAD_LID_ANGLE"));
        println("NOMAD_CHECK " ~ nomadJson(result));
        if (size(result.issues) > 0)
            reportFeatureWarning(context, id, "NOMAD: " ~ toString(size(result.issues)) ~ " clearance issue(s); see FeatureScript notices");
        else
            reportFeatureInfo(context, id, "NOMAD: no clearance issues in this pose");
    }, {});
// END PRODUCTION FEATURES
