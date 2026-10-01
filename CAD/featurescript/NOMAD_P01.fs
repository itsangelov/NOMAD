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
export const SERVICE_PANEL_THICKNESS = 2.5 * millimeter; // WORKING (status TBD)
export const MOUNT_PLATE_THICKNESS = 2 * millimeter; // WORKING (status TBD)
export const INPUT_TRAY_LIP = 3 * millimeter; // WORKING (status TBD)
export const TRACKPAD_BAY_MARGIN = 5 * millimeter; // WORKING (status TBD)
export const BOSS_DIAMETER = 7 * millimeter; // WORKING (status TBD)
export const TRAY_POST_DIAMETER = 5 * millimeter; // WORKING (status TBD)
export const HINGE_MOUNT_WIDTH = 28 * millimeter; // WORKING (status TBD)
export const HINGE_MOUNT_DEPTH = 21 * millimeter; // WORKING (status TBD)
export const BASE_SIDE_MARGIN = 8 * millimeter; // WORKING (status TBD)
export const BASE_FRONT_MARGIN = 15 * millimeter; // WORKING (status TBD)
export const BASE_REAR_ZONE_DEPTH = 30 * millimeter; // WORKING (status TBD)
export const HINGE_AXIS_OFFSET = 0 * millimeter; // WORKING (status TBD)
export const HINGE_AXIS_HEIGHT = 0 * millimeter; // WORKING (status TBD)
export const HINGE_BARREL_DIAMETER = 8 * millimeter; // WORKING (status TBD)
// --- lid ---
export const LID_THICKNESS = 37.6 * millimeter; // WORKING via FORMULA DISPLAY_BEZEL_LIP + DISPLAY_THICKNESS + MIN_GAP + SOLAR_RAIL_LAYER_HEIGHT + MIN_GAP + SOLAR_CASSETTE_THICKNESS + LID_BACK_GAP + LID_REAR_SHELL_DEPTH = 37.6 (status TBD)
export const LID_BACK_GAP = 2 * millimeter; // WORKING (status TBD)
export const LID_REAR_SHELL_DEPTH = 6.6 * millimeter; // WORKING (status TBD)
export const LID_SANDWICH_SKIN = 1.2 * millimeter; // WORKING (status TBD)
export const LID_SANDWICH_WEB = 2 * millimeter; // WORKING (status TBD)
export const LID_SANDWICH_WEB_SPACING = 30 * millimeter; // WORKING (status TBD)
export const LID_EDGE_BAND = 14 * millimeter; // WORKING via FORMULA (BODY_DEPTH - SOLAR_CASSETTE_HEIGHT) / 2 - MIN_GAP - WALL_THICKNESS = 14 (status TBD)
export const LID_MID_PLATE_THICKNESS = 2 * millimeter; // WORKING (status TBD)
export const LID_RIB_SKIN = 2.5 * millimeter; // WORKING (status TBD)
export const LID_RIB_HEIGHT = 8.5 * millimeter; // WORKING (status TBD)
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
export const DISPLAY_BEZEL_LIP = 1 * millimeter; // WORKING (status TBD)
export const DISPLAY_CONTROLLER_THICKNESS = 12 * millimeter; // WORKING (status TBD)
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
export const PI_STACK_HEIGHT = 30 * millimeter; // WORKING (status TBD)
export const PI_ENVELOPE_MARGIN = 4 * millimeter; // WORKING (status TBD)
export const PI_HAT_ZONE_HEIGHT = 10 * millimeter; // WORKING (status TBD)
export const COMPUTE_POWER_WIDTH = 50 * millimeter; // WORKING (status TBD)
export const COMPUTE_POWER_DEPTH = 30 * millimeter; // WORKING (status TBD)
export const COMPUTE_POWER_HEIGHT = 15 * millimeter; // WORKING (status TBD)
export const COOLING_DUCT_DEPTH = 20 * millimeter; // WORKING (status TBD)
export const GNSS_MODULE_WIDTH = 70 * millimeter; // WORKING (status TBD)
export const GNSS_MODULE_DEPTH = 35 * millimeter; // WORKING (status TBD)
export const GNSS_MODULE_HEIGHT = 12 * millimeter; // WORKING (status TBD)
export const NVME_FORMAT = "2230"; // VALUE (provisional)
// --- clearances ---
export const CLEARANCE = 0.3 * millimeter; // WORKING (status TBD)
export const MIN_GAP = 1 * millimeter; // WORKING (status TBD)
export const MIN_WALL = 2 * millimeter; // WORKING (status TBD)
export const CABLE_CORRIDOR_WIDTH = 15 * millimeter; // WORKING (status TBD)
export const CABLE_CORRIDOR_HEIGHT = 10 * millimeter; // WORKING (status TBD)
// --- fasteners ---
export const FASTENER_SIZE = ["M3", "M2.5"]; // VALUE (provisional)
// --- solar ---
export const SOLAR_CASSETTE_WIDTH = 147.5 * millimeter; // WORKING via FORMULA (BODY_WIDTH - 2 * WALL_THICKNESS - MIN_GAP) / 2 = 147.5 (status TBD)
export const SOLAR_CASSETTE_HEIGHT = 200 * millimeter; // WORKING (status TBD)
export const SOLAR_CASSETTE_THICKNESS = 8 * millimeter; // WORKING (status TBD)
export const SOLAR_ROTATION_LIMIT = { "min" : 60 * degree, "max" : 75 * degree }; // VALUE (provisional)
export const SOLAR_ROTATION_AXIS = "slide_direction"; // VALUE (provisional)
export const SOLAR_DEPLOY_CLEARANCE = 8 * millimeter; // WORKING via FORMULA SOLAR_CABLE_DIAMETER + 2 * MIN_GAP = 8 (status TBD)
export const SOLAR_SLIDE_TRAVEL = 158 * millimeter; // WORKING via FORMULA SOLAR_CASSETTE_WIDTH + WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE = 158 (status TBD)
export const SOLAR_RAIL_ENGAGEMENT = 40 * millimeter; // WORKING (status TBD)
export const SOLAR_CARRIAGE_WIDTH = 22.6 * millimeter; // WORKING via FORMULA SOLAR_RAIL_SLOT_WIDTH + 2 * WALL_THICKNESS = 22.6 (status TBD)
export const SOLAR_CARRIAGE_HEIGHT = 8 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_LINK_LENGTH = 11.5 * millimeter; // WORKING via FORMULA WALL_THICKNESS + SOLAR_DEPLOY_CLEARANCE + MIN_GAP = 11.5 (status TBD)
export const SOLAR_HUB_AXIS_OFFSET_Y = 114.3 * millimeter; // WORKING via FORMULA SOLAR_CASSETTE_HEIGHT / 2 + SOLAR_RAIL_WIDTH / 2 + SOLAR_CABLE_CORRIDOR / 2 - SOLAR_HUB_CABLE_OFFSET = 114.3 (status TBD)
export const SOLAR_HUB_AXIS_OFFSET_Z = -5.5 * millimeter; // WORKING via FORMULA WALL_THICKNESS + MIN_GAP + SOLAR_BRACKET_WALL + SOLAR_HUB_PIN_DIAMETER / 2 - (SOLAR_RAIL_LAYER_HEIGHT + MIN_GAP) = -5.5 (status TBD)
export const SOLAR_RAIL_SLOT_WIDTH = 17.6 * millimeter; // WORKING via FORMULA SOLAR_BRACKET_WIDTH + 2 * CLEARANCE = 17.6 (status TBD)
export const SOLAR_RAIL_WIDTH = 27.6 * millimeter; // WORKING via FORMULA SOLAR_CARRIAGE_WIDTH + 2 * WALL_THICKNESS = 27.6 (status TBD)
export const SOLAR_RAIL_LAYER_HEIGHT = 13 * millimeter; // WORKING via FORMULA SOLAR_CARRIAGE_HEIGHT + 2 * WALL_THICKNESS = 13 (status TBD)
export const SOLAR_BRACKET_WIDTH = 17 * millimeter; // WORKING via FORMULA SOLAR_HUB_PIN_DIAMETER + MIN_GAP + SOLAR_CABLE_DIAMETER + 2 * WALL_THICKNESS = 17 (status TBD)
export const SOLAR_BRACKET_LENGTH = 10 * millimeter; // WORKING (status TBD)
export const SOLAR_BRACKET_WALL = 2.5 * millimeter; // WORKING via FORMULA WALL_THICKNESS = 2.5 (status TBD)
export const SOLAR_HUB_CABLE_OFFSET = 3.5 * millimeter; // WORKING via FORMULA (MIN_GAP + SOLAR_CABLE_DIAMETER) / 2 = 3.5 (status TBD)
export const SOLAR_CABLE_DIAMETER = 6 * millimeter; // WORKING (status TBD)
export const SOLAR_CABLE_BEND_RADIUS = 20 * millimeter; // WORKING (status TBD)
export const SOLAR_CABLE_CORRIDOR = 8 * millimeter; // WORKING via FORMULA SOLAR_CABLE_DIAMETER + 2 * MIN_GAP = 8 (status TBD)
export const SOLAR_INDEX_STEP = 15 * degree; // WORKING (status TBD)
export const SOLAR_HUB_PIN_DIAMETER = 5 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_RANGE = 75 * degree; // WORKING (status TBD)
export const SOLAR_INDEX_POSITIONS = 11; // WORKING via FORMULA 2 * SOLAR_INDEX_RANGE / SOLAR_INDEX_STEP + 1 = 11 (status TBD)
export const SOLAR_INDEX_RADIUS = 10 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_PIN_ANGLE = 57.5 * degree; // WORKING (status TBD)
export const SOLAR_INDEX_PIN_DIAMETER = 1.5 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_PIN_LENGTH = 16 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_HOLE_DIAMETER = 1.6 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_PLATE_THICKNESS = 1.5 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_PLATE_OUTER_RADIUS = 11.75 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_GROOVE_CLEARANCE = 0.5 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE = 0.25 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_ENGAGEMENT = 3 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_PIN_STROKE = 6 * millimeter; // WORKING via FORMULA SOLAR_INDEX_ENGAGEMENT + SOLAR_INDEX_GROOVE_CLEARANCE + SOLAR_INDEX_PLATE_THICKNESS + MIN_GAP = 6 (status TBD)
export const SOLAR_INDEX_SLEEVE_OD = 2.5 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_SLEEVE_LENGTH = 4 * millimeter; // WORKING via FORMULA SOLAR_INDEX_ENGAGEMENT + MIN_GAP = 4 (status TBD)
export const SOLAR_INDEX_GUIDE_LENGTH = 6 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_CARRIER_LENGTH = 4 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_CARRIER_WIDTH = 3.6 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_SPRING_OD = 3.4 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_SPRING_POCKET_WIDTH = 3.8 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_SPRING_INSTALLED_LENGTH = 12 * millimeter; // WORKING (status TBD)
export const SOLAR_INDEX_SPRING_PRELOAD = 0.6; // WORKING (status TBD)
export const SOLAR_INDEX_COVER_END = 3 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_PIN_KEY_ACROSS_FLATS = 3 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_PIN_LENGTH = 53.5 * millimeter; // WORKING via FORMULA SOLAR_RAIL_ENGAGEMENT - SOLAR_ANTIROT_PLATE_INSET + SOLAR_HUB_LINK_LENGTH + SOLAR_BRACKET_LENGTH + SOLAR_INDEX_GROOVE_CLEARANCE + SOLAR_INDEX_PLATE_THICKNESS = 53.5 (status TBD)
export const SOLAR_HUB_SCREW_HEAD_DIAMETER = 3.8 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_SCREW_HEAD_HEIGHT = 2 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_WASHER_DIAMETER = 5 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_WASHER_THICKNESS = 0.3 * millimeter; // WORKING (status TBD)
export const SOLAR_HUB_ACCESS_DIAMETER = 5.5 * millimeter; // WORKING via FORMULA SOLAR_HUB_WASHER_DIAMETER + 2 * SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE = 5.5 (status TBD)
export const SOLAR_ANTIROT_PLATE_INSET = 10 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_PLATE_THICKNESS = 1.5 * millimeter; // WORKING via FORMULA SOLAR_INDEX_PLATE_THICKNESS = 1.5 (status TBD)
export const SOLAR_LOCK_SLOT_CLEARANCE = 0.1 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_LIGAMENT = 1.3 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_SKIN = 0.5 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_CABLE_WALL = 0.6 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_DOWEL_DIAMETER = 3 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_DOWEL_LENGTH = 24 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_DOWEL_OFFSET_Y = 5 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_DOWEL_OFFSET_Z = -2.5 * millimeter; // WORKING (status TBD)
export const SOLAR_ANTIROT_PUSHOUT_DIAMETER = 2 * millimeter; // WORKING (status TBD)
// --- io ---
export const PORT_PANEL_WIDTH = 90 * millimeter; // WORKING (status TBD)
export const PORT_PANEL_HEIGHT = 15 * millimeter; // WORKING (status TBD)
export const PORT_PANEL_BOTTOM = 4 * millimeter; // WORKING (status TBD)
export const PORT_PANEL_INSET = 20 * millimeter; // WORKING (status TBD)
export const PORT_KEEPOUT_DEPTH = 25 * millimeter; // WORKING (status TBD)
export const PLUG_KEEPOUT_LENGTH = 45 * millimeter; // WORKING (status TBD)
// --- battery ---
export const BATTERY_BAY_WIDTH = 90 * millimeter; // WORKING (status TBD)
export const BATTERY_BAY_DEPTH = 82 * millimeter; // WORKING (status TBD)
export const BATTERY_BAY_HEIGHT = 30 * millimeter; // WORKING (status TBD)
export const POWER_ELEC_WIDTH = 90 * millimeter; // WORKING (status TBD)
export const POWER_ELEC_DEPTH = 45 * millimeter; // WORKING (status TBD)
export const POWER_ELEC_HEIGHT = 20 * millimeter; // WORKING (status TBD)
export const NOMAD_PARAM_BASIS = { "BODY_WIDTH" : "formula", "BODY_DEPTH" : "formula", "BODY_HEIGHT" : "working", "WALL_THICKNESS" : "working", "SERVICE_PANEL_THICKNESS" : "working", "MOUNT_PLATE_THICKNESS" : "working", "INPUT_TRAY_LIP" : "working", "TRACKPAD_BAY_MARGIN" : "working", "BOSS_DIAMETER" : "working", "TRAY_POST_DIAMETER" : "working", "HINGE_MOUNT_WIDTH" : "working", "HINGE_MOUNT_DEPTH" : "working", "BASE_SIDE_MARGIN" : "working", "BASE_FRONT_MARGIN" : "working", "BASE_REAR_ZONE_DEPTH" : "working", "HINGE_AXIS_OFFSET" : "working", "HINGE_AXIS_HEIGHT" : "working", "HINGE_BARREL_DIAMETER" : "working", "LID_THICKNESS" : "formula", "LID_BACK_GAP" : "working", "LID_REAR_SHELL_DEPTH" : "working", "LID_SANDWICH_SKIN" : "working", "LID_SANDWICH_WEB" : "working", "LID_SANDWICH_WEB_SPACING" : "working", "LID_EDGE_BAND" : "formula", "LID_MID_PLATE_THICKNESS" : "working", "LID_RIB_SKIN" : "working", "LID_RIB_HEIGHT" : "working", "LID_CLOSED_GAP" : "working", "LID_ANGLE_NOMINAL" : "working", "LID_ANGLE_MAX" : "working", "DISPLAY_DIAGONAL" : "value", "DISPLAY_ACTIVE_WIDTH" : "value", "DISPLAY_ACTIVE_HEIGHT" : "value", "DISPLAY_WIDTH" : "working", "DISPLAY_HEIGHT" : "working", "DISPLAY_THICKNESS" : "working", "DISPLAY_VERTICAL_OFFSET" : "working", "DISPLAY_BEZEL_LIP" : "working", "DISPLAY_CONTROLLER_THICKNESS" : "working", "KEYBOARD_WIDTH" : "value", "KEYBOARD_DEPTH" : "value", "KEYBOARD_THICKNESS" : "value", "TRACKPAD_WIDTH" : "working", "TRACKPAD_DEPTH" : "working", "TRACKPAD_THICKNESS" : "working", "KEYBOARD_LATERAL_OFFSET" : "working", "TRACKPAD_LATERAL_OFFSET" : "working", "TRACKPAD_KEYBOARD_GAP" : "working", "KEYBOARD_TOP_RECESS" : "working", "TRACKPAD_TOP_RECESS" : "working", "PI_WIDTH" : "value", "PI_DEPTH" : "value", "PI_STACK_HEIGHT" : "working", "PI_ENVELOPE_MARGIN" : "working", "PI_HAT_ZONE_HEIGHT" : "working", "COMPUTE_POWER_WIDTH" : "working", "COMPUTE_POWER_DEPTH" : "working", "COMPUTE_POWER_HEIGHT" : "working", "COOLING_DUCT_DEPTH" : "working", "GNSS_MODULE_WIDTH" : "working", "GNSS_MODULE_DEPTH" : "working", "GNSS_MODULE_HEIGHT" : "working", "NVME_FORMAT" : "value", "CLEARANCE" : "working", "MIN_GAP" : "working", "MIN_WALL" : "working", "CABLE_CORRIDOR_WIDTH" : "working", "CABLE_CORRIDOR_HEIGHT" : "working", "FASTENER_SIZE" : "value", "SOLAR_CASSETTE_WIDTH" : "formula", "SOLAR_CASSETTE_HEIGHT" : "working", "SOLAR_CASSETTE_THICKNESS" : "working", "SOLAR_ROTATION_LIMIT" : "value", "SOLAR_ROTATION_AXIS" : "value", "SOLAR_DEPLOY_CLEARANCE" : "formula", "SOLAR_SLIDE_TRAVEL" : "formula", "SOLAR_RAIL_ENGAGEMENT" : "working", "SOLAR_CARRIAGE_WIDTH" : "formula", "SOLAR_CARRIAGE_HEIGHT" : "working", "SOLAR_HUB_LINK_LENGTH" : "formula", "SOLAR_HUB_AXIS_OFFSET_Y" : "formula", "SOLAR_HUB_AXIS_OFFSET_Z" : "formula", "SOLAR_RAIL_SLOT_WIDTH" : "formula", "SOLAR_RAIL_WIDTH" : "formula", "SOLAR_RAIL_LAYER_HEIGHT" : "formula", "SOLAR_BRACKET_WIDTH" : "formula", "SOLAR_BRACKET_LENGTH" : "working", "SOLAR_BRACKET_WALL" : "formula", "SOLAR_HUB_CABLE_OFFSET" : "formula", "SOLAR_CABLE_DIAMETER" : "working", "SOLAR_CABLE_BEND_RADIUS" : "working", "SOLAR_CABLE_CORRIDOR" : "formula", "SOLAR_INDEX_STEP" : "working", "SOLAR_HUB_PIN_DIAMETER" : "working", "SOLAR_INDEX_RANGE" : "working", "SOLAR_INDEX_POSITIONS" : "formula", "SOLAR_INDEX_RADIUS" : "working", "SOLAR_INDEX_PIN_ANGLE" : "working", "SOLAR_INDEX_PIN_DIAMETER" : "working", "SOLAR_INDEX_PIN_LENGTH" : "working", "SOLAR_INDEX_HOLE_DIAMETER" : "working", "SOLAR_INDEX_PLATE_THICKNESS" : "working", "SOLAR_INDEX_PLATE_OUTER_RADIUS" : "working", "SOLAR_INDEX_GROOVE_CLEARANCE" : "working", "SOLAR_INDEX_GROOVE_RADIAL_CLEARANCE" : "working", "SOLAR_INDEX_ENGAGEMENT" : "working", "SOLAR_INDEX_PIN_STROKE" : "formula", "SOLAR_INDEX_SLEEVE_OD" : "working", "SOLAR_INDEX_SLEEVE_LENGTH" : "formula", "SOLAR_INDEX_GUIDE_LENGTH" : "working", "SOLAR_INDEX_CARRIER_LENGTH" : "working", "SOLAR_INDEX_CARRIER_WIDTH" : "working", "SOLAR_INDEX_SPRING_OD" : "working", "SOLAR_INDEX_SPRING_POCKET_WIDTH" : "working", "SOLAR_INDEX_SPRING_INSTALLED_LENGTH" : "working", "SOLAR_INDEX_SPRING_PRELOAD" : "working", "SOLAR_INDEX_COVER_END" : "working", "SOLAR_HUB_PIN_KEY_ACROSS_FLATS" : "working", "SOLAR_HUB_PIN_LENGTH" : "formula", "SOLAR_HUB_SCREW_HEAD_DIAMETER" : "working", "SOLAR_HUB_SCREW_HEAD_HEIGHT" : "working", "SOLAR_HUB_WASHER_DIAMETER" : "working", "SOLAR_HUB_WASHER_THICKNESS" : "working", "SOLAR_HUB_ACCESS_DIAMETER" : "formula", "SOLAR_ANTIROT_PLATE_INSET" : "working", "SOLAR_ANTIROT_PLATE_THICKNESS" : "formula", "SOLAR_LOCK_SLOT_CLEARANCE" : "working", "SOLAR_ANTIROT_LIGAMENT" : "working", "SOLAR_ANTIROT_SKIN" : "working", "SOLAR_ANTIROT_CABLE_WALL" : "working", "SOLAR_ANTIROT_DOWEL_DIAMETER" : "working", "SOLAR_ANTIROT_DOWEL_LENGTH" : "working", "SOLAR_ANTIROT_DOWEL_OFFSET_Y" : "working", "SOLAR_ANTIROT_DOWEL_OFFSET_Z" : "working", "SOLAR_ANTIROT_PUSHOUT_DIAMETER" : "working", "PORT_PANEL_WIDTH" : "working", "PORT_PANEL_HEIGHT" : "working", "PORT_PANEL_BOTTOM" : "working", "PORT_PANEL_INSET" : "working", "PORT_KEEPOUT_DEPTH" : "working", "PLUG_KEEPOUT_LENGTH" : "working", "BATTERY_BAY_WIDTH" : "working", "BATTERY_BAY_DEPTH" : "working", "BATTERY_BAY_HEIGHT" : "working", "POWER_ELEC_WIDTH" : "working", "POWER_ELEC_DEPTH" : "working", "POWER_ELEC_HEIGHT" : "working" };
export const NOMAD_UNRESOLVED = ["GNSS_ANTENNA_KEEPOUT", "CABLE_CLEARANCE", "OVERHANG_LIMIT", "INSERT_SIZE", "SOLAR_TILT_STOP_ANGLE"];
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

// ================= Solar skeleton (Round B, D-004 kinematics) =================
// Kinematic envelopes only: cassette body, hub pin, carriage, fixed rail keep-out. No hardware.
// Built in closed-lid world coordinates, tilted about the hub axis (parallel to X), then moved
// with the lid. Slide is along X; the carriage stays SOLAR_HUB_LINK_LENGTH inboard of the cassette.

// Current working layout (V0): cassette against the lid back plate with MIN_GAP, centred in Y,
// hub axis at SOLAR_HUB_AXIS_OFFSET_Y/Z inside the cassette, rail coaxial with the hub.
export function nomadSolarLayout() returns map
{
    const back = BODY_HEIGHT + LID_CLOSED_GAP + LID_THICKNESS - WALL_THICKNESS;
    const cz0 = back - MIN_GAP - SOLAR_CASSETTE_THICKNESS;
    const cy0 = (BODY_DEPTH - SOLAR_CASSETTE_HEIGHT) / 2;
    const hub = [cy0 + SOLAR_HUB_AXIS_OFFSET_Y, cz0 + SOLAR_HUB_AXIS_OFFSET_Z];
    return { "cy0" : cy0, "cz0" : cz0, "hubR" : hub, "hubL" : hub };
}

function nomadSolarColor() returns Color
{
    return color(0.95, 0.65, 0.15, 1);
}

// Axis-aligned box on one side: x range a..b for the right side (side = 1), mirrored for the left.
function nomadSideBox(context is Context, id is Id, side is number, a is ValueWithUnits, b is ValueWithUnits,
    y0 is ValueWithUnits, y1 is ValueWithUnits, z0 is ValueWithUnits, z1 is ValueWithUnits) returns Query
{
    const x0 = side > 0 ? a : -b;
    const x1 = side > 0 ? b : -a;
    return nomadBox(context, id, vector(x0, y0, z0), vector(x1, y1, z1));
}

// One cassette assembly at slide extension 0 (stowed) .. 1 (deployed) and tilt, in the given lid pose.
export function nomadBuildSolarSide(context is Context, id is Id, side is number, extension is number, tilt is ValueWithUnits,
    lidAngle is ValueWithUnits, hinge is map, lay is map) returns map
{
    const tag = side > 0 ? "R" : "L";
    const hub = side > 0 ? lay.hubR : lay.hubL;
    const xi = MIN_GAP / 2 + extension * SOLAR_SLIDE_TRAVEL;
    const kx1 = xi - SOLAR_HUB_LINK_LENGTH;
    const railHalfW = SOLAR_CARRIAGE_WIDTH / 2 + WALL_THICKNESS;
    const railHalfH = SOLAR_CARRIAGE_HEIGHT / 2 + WALL_THICKNESS;
    const pinHalf = SOLAR_HUB_PIN_DIAMETER / 2;
    const cassette = nomadSideBox(context, id + "cassette", side, xi, xi + SOLAR_CASSETTE_WIDTH,
            lay.cy0, lay.cy0 + SOLAR_CASSETTE_HEIGHT, lay.cz0, lay.cz0 + SOLAR_CASSETTE_THICKNESS);
    const pin = nomadSideBox(context, id + "pin", side, kx1, xi,
            hub[0] - pinHalf, hub[0] + pinHalf, hub[1] - pinHalf, hub[1] + pinHalf);
    const carriage = nomadSideBox(context, id + "carriage", side, kx1 - SOLAR_RAIL_ENGAGEMENT, kx1,
            hub[0] - SOLAR_CARRIAGE_WIDTH / 2, hub[0] + SOLAR_CARRIAGE_WIDTH / 2, hub[1] - SOLAR_CARRIAGE_HEIGHT / 2, hub[1] + SOLAR_CARRIAGE_HEIGHT / 2);
    const rail = nomadSideBox(context, id + "rail", side,
            MIN_GAP / 2 - SOLAR_HUB_LINK_LENGTH - SOLAR_RAIL_ENGAGEMENT, MIN_GAP / 2 + SOLAR_SLIDE_TRAVEL - SOLAR_HUB_LINK_LENGTH,
            hub[0] - railHalfW, hub[0] + railHalfW, hub[1] - railHalfH, hub[1] + railHalfH);
    if (abs(tilt) > 1e-9 * degree)
        opTransform(context, id + "tilt", { "bodies" : cassette,
                    "transform" : rotationAround(line(vector(0 * millimeter, hub[0], hub[1]), vector(-1, 0, 0)), tilt) });
    opTransform(context, id + "pose", { "bodies" : qUnion([cassette, pin, carriage, rail]), "transform" : nomadLidTransform(lidAngle, hinge) });
    nomadTag(context, cassette, "SOLAR_CASSETTE_" ~ tag, nomadSolarColor());
    nomadTag(context, pin, "SOLAR_HUB_PIN_" ~ tag, nomadEnvColor());
    nomadTag(context, carriage, "SOLAR_CARRIAGE_" ~ tag, nomadEnvColor());
    nomadTag(context, rail, "KEEPOUT_SOLAR_RAIL_" ~ tag, nomadSkelColor());
    return { ("C" ~ tag) : cassette, ("P" ~ tag) : pin, ("K" ~ tag) : carriage, ("R" ~ tag) : rail };
}

// ================= Base V0.1 (Round C, proposed D-007) =================
// Engineering envelope model of the NOMAD Mechanical V0.1 base: structural shell (walls, deck with
// keyboard/trackpad openings, bulkheads, bosses), separate trays / compute sled / service panels /
// port panels, component envelopes, hinge-mount reserves, cooling and connector keep-outs, cable
// corridors. Reserves are not hardware. Layout: CAD/tools/base_v01_layout.py (generated block below);
// report: prototypes/P0.1/base_v01_architecture.md.

// BEGIN GENERATED BASE V0.1 LAYOUT
// Generated from CAD/tools/base_v01_layout.py (Round C base V0.1 layout). DO NOT EDIT.
// Parametric: every coordinate is an expression over the GENERATED PARAMS constants.
// Envelopes / keep-outs are reserves, not hardware; see prototypes/P0.1/base_v01_architecture.md.
export const BV_W2 = BODY_WIDTH / 2;
export const BV_IX = BV_W2 - WALL_THICKNESS;
export const BV_IY0 = WALL_THICKNESS;
export const BV_IY1 = BODY_DEPTH - WALL_THICKNESS;
export const BV_IZ0 = SERVICE_PANEL_THICKNESS;
export const BV_IZ1 = BODY_HEIGHT - WALL_THICKNESS;
export const BV_OFF = BOSS_DIAMETER / 2 - WALL_THICKNESS / 2;
export const BV_TPC = TRACKPAD_LATERAL_OFFSET;
export const BV_KBC = KEYBOARD_LATERAL_OFFSET;
export const BV_TPY0 = BASE_FRONT_MARGIN;
export const BV_TPY1 = BV_TPY0 + TRACKPAD_DEPTH;
export const BV_TPZ1 = BODY_HEIGHT - TRACKPAD_TOP_RECESS;
export const BV_TPZ0 = BV_TPZ1 - TRACKPAD_THICKNESS;
export const BV_KBY0 = BV_TPY1 + TRACKPAD_KEYBOARD_GAP;
export const BV_KBY1 = BV_KBY0 + KEYBOARD_DEPTH;
export const BV_KBZ1 = BODY_HEIGHT - KEYBOARD_TOP_RECESS;
export const BV_KBZ0 = BV_KBZ1 - KEYBOARD_THICKNESS;
export const BV_KTY0 = BV_KBY0 - INPUT_TRAY_LIP;
export const BV_KTY1 = BV_KBY1 + INPUT_TRAY_LIP;
export const BV_KTZ0 = BV_KBZ0 - MOUNT_PLATE_THICKNESS;
export const BV_KTX = BV_IX - CLEARANCE;
export const BV_TTY0 = BV_TPY0 - INPUT_TRAY_LIP;
export const BV_TTY1 = BV_TPY1 + INPUT_TRAY_LIP;
export const BV_TTZ0 = BV_TPZ0 - MOUNT_PLATE_THICKNESS;
export const BV_BHR0 = BV_TPC + TRACKPAD_WIDTH / 2 + TRACKPAD_BAY_MARGIN;
export const BV_BHR1 = BV_BHR0 + WALL_THICKNESS;
export const BV_BHL1 = BV_TPC - TRACKPAD_WIDTH / 2 - TRACKPAD_BAY_MARGIN;
export const BV_BHL0 = BV_BHL1 - WALL_THICKNESS;
export const BV_BAYRC = (BV_BHR1 + BV_IX) / 2;
export const BV_BAYLC = (BV_BHL0 - BV_IX) / 2;
export const BV_FBY = BV_IY0 + BV_OFF;
export const BV_SLZ0 = BV_IZ0 + MIN_GAP;
export const BV_SLZ1 = BV_SLZ0 + MOUNT_PLATE_THICKNESS;
export const BV_SLY0 = BV_FBY + BOSS_DIAMETER / 2 + CLEARANCE;
export const BV_SLY1 = BV_KTY0 - CLEARANCE;
export const BV_PIW = PI_WIDTH + 2 * PI_ENVELOPE_MARGIN;
export const BV_PID = PI_DEPTH + 2 * PI_ENVELOPE_MARGIN;
export const BV_PIX0 = BV_BAYRC - BV_PIW / 2;
export const BV_PIX1 = BV_BAYRC + BV_PIW / 2;
export const BV_PIY1 = BV_KTY0 - BOSS_DIAMETER - MIN_GAP;
export const BV_PIY0 = BV_PIY1 - BV_PID;
export const BV_PIZ1 = BV_SLZ1 + PI_STACK_HEIGHT;
export const BV_SBYF = BV_FBY + BOSS_DIAMETER + MIN_GAP;
export const BV_SBYR = BV_PIY1 + MIN_GAP + BOSS_DIAMETER / 2;
export const BV_DUX0 = BV_BHR1 + BV_OFF + BOSS_DIAMETER / 2 + MIN_GAP;
export const BV_DUX1 = BV_IX - BV_OFF - BOSS_DIAMETER / 2 - MIN_GAP;
export const BV_DUY0 = BV_PIY0 - COOLING_DUCT_DEPTH;
export const BV_DUZ1 = BV_IZ1 - MIN_GAP;
export const BV_RIBY1 = BV_KTY0 - CLEARANCE;
export const BV_RIBY0 = BV_RIBY1 - WALL_THICKNESS;
export const BV_BATY1 = BV_RIBY0 - MIN_GAP;
export const BV_BATY0 = BV_BATY1 - BATTERY_BAY_DEPTH;
export const BV_BATX0 = BV_BAYLC - BATTERY_BAY_WIDTH / 2;
export const BV_BATX1 = BV_BAYLC + BATTERY_BAY_WIDTH / 2;
export const BV_BATZ0 = BV_IZ0 + MIN_GAP;
export const BV_BATZ1 = BV_BATZ0 + BATTERY_BAY_HEIGHT;
export const BV_PEY0 = BV_RIBY1 + MIN_GAP;
export const BV_PEY1 = BV_PEY0 + POWER_ELEC_DEPTH;
export const BV_PEX0 = BV_BAYLC - POWER_ELEC_WIDTH / 2;
export const BV_PEX1 = BV_BAYLC + POWER_ELEC_WIDTH / 2;
export const BV_CZ0 = BV_IZ0 + MIN_GAP;
export const BV_CZ1 = BV_CZ0 + CABLE_CORRIDOR_HEIGHT;
export const BV_PEZ1 = BV_CZ0 + POWER_ELEC_HEIGHT;
export const BV_TRY1 = BV_KBY1;
export const BV_TRY0 = BV_TRY1 - CABLE_CORRIDOR_WIDTH;
export const BV_BLX0 = BV_BAYLC - CABLE_CORRIDOR_WIDTH / 2;
export const BV_BLX1 = BV_BAYLC + CABLE_CORRIDOR_WIDTH / 2;
export const BV_CCX1 = BV_IX - BV_OFF - BOSS_DIAMETER / 2 - MIN_GAP;
export const BV_CCX0 = BV_CCX1 - CABLE_CORRIDOR_WIDTH;
export const BV_CCZ0 = BV_SLZ1 + MIN_GAP;
export const BV_CCZ1 = BV_CCZ0 + CABLE_CORRIDOR_HEIGHT;
export const BV_CPX1 = BV_CCX0;
export const BV_CPX0 = BV_CPX1 - COMPUTE_POWER_WIDTH;
export const BV_CPY0 = BV_KTY0 + MIN_GAP;
export const BV_CPY1 = BV_CPY0 + COMPUTE_POWER_DEPTH;
export const BV_CPZ1 = BV_CZ0 + COMPUTE_POWER_HEIGHT;
export const BV_GNX1 = BV_TPC - CABLE_CORRIDOR_WIDTH / 2 - MIN_GAP;
export const BV_GNX0 = BV_GNX1 - GNSS_MODULE_WIDTH;
export const BV_GNY1 = BV_TRY0;
export const BV_GNY0 = BV_GNY1 - GNSS_MODULE_DEPTH;
export const BV_GNZ1 = BV_CZ0 + GNSS_MODULE_HEIGHT;
export const BV_CW2 = CABLE_CORRIDOR_WIDTH / 2;
export const BV_RSY0 = BV_KTY1 + MIN_GAP;
export const BV_RSY1 = BV_IY1 - MIN_GAP;
export const BV_SBSY = BV_KBY0 + KEYBOARD_DEPTH / 2;
export const BV_NOTX = BV_IX - BV_OFF - BOSS_DIAMETER / 2 - CLEARANCE;
export const BV_NOTY0 = BV_SBSY - BOSS_DIAMETER / 2 - CLEARANCE;
export const BV_NOTY1 = BV_SBSY + BOSS_DIAMETER / 2 + CLEARANCE;
export const BV_POSTX = KEYBOARD_WIDTH / 2 + BASE_SIDE_MARGIN / 2;
export const BV_POSTY0 = BV_KBY0 + KEYBOARD_DEPTH / 6;
export const BV_POSTY1 = BV_KBY0 + KEYBOARD_DEPTH * 5 / 6;
export const BV_STDX = KEYBOARD_WIDTH / 8;
export const BV_STDY = BV_KBY0 + KEYBOARD_DEPTH / 4;
export const BV_PX0 = PORT_PANEL_INSET;
export const BV_PX1 = BV_PX0 + PORT_PANEL_WIDTH;
export const BV_PZ0 = PORT_PANEL_BOTTOM;
export const BV_PZ1 = BV_PZ0 + PORT_PANEL_HEIGHT;
export const BV_HX0 = BV_IX - HINGE_MOUNT_WIDTH;
export const BV_HY0 = BV_IY1 - HINGE_MOUNT_DEPTH;
export const BV_RBX = (BV_PX1 + BV_HX0) / 2;
export const BV_RCX = CABLE_CORRIDOR_WIDTH / 2 + MIN_GAP + BOSS_DIAMETER / 2;
export const BV_RBY = BV_IY1 - BV_OFF;
export const BV_SEAMX = BV_BHL0 + WALL_THICKNESS / 2;
export const BV_SEAMY = (BV_RIBY0 + BV_RIBY1) / 2;
// [part name, category, [["box", label, x0, y0, z0, x1, y1, z1] | ["cyl", label, cx, cy, d, z0, z1], ...]]
export function nomadBaseV01Parts() returns array
{
    return [
        ["BASE_SHELL", "S", [
            ["box", "wall_front", -BV_W2, 0 * millimeter, 0 * millimeter, BV_W2, BV_IY0, BODY_HEIGHT],
            ["box", "wall_left", -BV_W2, BV_IY0, 0 * millimeter, -BV_IX, BV_IY1, BODY_HEIGHT],
            ["box", "wall_right", BV_IX, BV_IY0, 0 * millimeter, BV_W2, BV_IY1, BODY_HEIGHT],
            ["box", "wall_rear_high", -BV_W2, BV_IY1, BV_PZ1, BV_W2, BODY_DEPTH, BODY_HEIGHT],
            ["box", "wall_rear_l", -BV_W2, BV_IY1, 0 * millimeter, -BV_PX1, BODY_DEPTH, BV_PZ1],
            ["box", "wall_rear_c", -BV_PX0, BV_IY1, 0 * millimeter, BV_PX0, BODY_DEPTH, BV_PZ1],
            ["box", "wall_rear_r", BV_PX1, BV_IY1, 0 * millimeter, BV_W2, BODY_DEPTH, BV_PZ1],
            ["box", "deck_front", -BV_IX, BV_IY0, BV_IZ1, BV_IX, BV_TPY0 - CLEARANCE, BODY_HEIGHT],
            ["box", "deck_tp_l", -BV_IX, BV_TPY0 - CLEARANCE, BV_IZ1, BV_TPC - TRACKPAD_WIDTH / 2 - CLEARANCE, BV_TPY1 + CLEARANCE, BODY_HEIGHT],
            ["box", "deck_tp_r", BV_TPC + TRACKPAD_WIDTH / 2 + CLEARANCE, BV_TPY0 - CLEARANCE, BV_IZ1, BV_IX, BV_TPY1 + CLEARANCE, BODY_HEIGHT],
            ["box", "deck_mid", -BV_IX, BV_TPY1 + CLEARANCE, BV_IZ1, BV_IX, BV_KBY0 - CLEARANCE, BODY_HEIGHT],
            ["box", "deck_kb_l", -BV_IX, BV_KBY0 - CLEARANCE, BV_IZ1, BV_KBC - KEYBOARD_WIDTH / 2 - CLEARANCE, BV_KBY1 + CLEARANCE, BODY_HEIGHT],
            ["box", "deck_kb_r", BV_KBC + KEYBOARD_WIDTH / 2 + CLEARANCE, BV_KBY0 - CLEARANCE, BV_IZ1, BV_IX, BV_KBY1 + CLEARANCE, BODY_HEIGHT],
            ["box", "deck_rear", -BV_IX, BV_KBY1 + CLEARANCE, BV_IZ1, BV_IX, BV_IY1, BODY_HEIGHT],
            ["box", "bulkhead_l", BV_BHL0, BV_IY0, BV_IZ0, BV_BHL1, BV_KTY0, BV_IZ1],
            ["box", "bulkhead_r", BV_BHR0, BV_IY0, BV_IZ0, BV_BHR1, BV_KTY0, BV_IZ1],
            ["box", "battery_wall_1", -BV_IX, BV_RIBY0, BV_IZ0, BV_BLX0 - MIN_GAP, BV_RIBY1, BV_IZ1],
            ["box", "battery_wall_2", BV_BLX1 + MIN_GAP, BV_RIBY0, BV_IZ0, BV_BHL0, BV_RIBY1, BV_IZ1],
            ["cyl", "boss_front_lo", -(BV_IX - BV_OFF), BV_FBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_front_li", BV_BHL0 - BV_OFF, BV_FBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_front_c", BV_TPC, BV_FBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_front_ri", BV_BHR1 + BV_OFF, BV_FBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_front_ro", BV_IX - BV_OFF, BV_FBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_side_l", -(BV_IX - BV_OFF), BV_SBSY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_side_r", BV_IX - BV_OFF, BV_SBSY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_rear_lo", -BV_RBX, BV_RBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_rear_li", -BV_RCX, BV_RBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_rear_ri", BV_RCX, BV_RBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_rear_ro", BV_RBX, BV_RBY, BOSS_DIAMETER, BV_IZ0, BV_IZ1],
            ["cyl", "boss_sled_fi", BV_BHR1 + BV_OFF, BV_SBYF, BOSS_DIAMETER, BV_SLZ1, BV_IZ1],
            ["cyl", "boss_sled_fo", BV_IX - BV_OFF, BV_SBYF, BOSS_DIAMETER, BV_SLZ1, BV_IZ1],
            ["cyl", "boss_sled_ri", BV_BHR1 + BV_OFF, BV_SBYR, BOSS_DIAMETER, BV_SLZ1, BV_IZ1],
            ["cyl", "boss_sled_ro", BV_IX - BV_OFF, BV_SBYR, BOSS_DIAMETER, BV_SLZ1, BV_IZ1]
        ]],
        ["KEYBOARD_TRAY", "S", [
            ["box", "plate", -BV_NOTX, BV_KTY0, BV_KTZ0, BV_NOTX, BV_KTY1, BV_KBZ0],
            ["box", "strip_l_front", -BV_KTX, BV_KTY0, BV_KTZ0, -BV_NOTX, BV_NOTY0, BV_KBZ0],
            ["box", "strip_l_rear", -BV_KTX, BV_NOTY1, BV_KTZ0, -BV_NOTX, BV_KTY1, BV_KBZ0],
            ["box", "strip_r_front", BV_NOTX, BV_KTY0, BV_KTZ0, BV_KTX, BV_NOTY0, BV_KBZ0],
            ["box", "strip_r_rear", BV_NOTX, BV_NOTY1, BV_KTZ0, BV_KTX, BV_KTY1, BV_KBZ0],
            ["cyl", "post_lf", BV_KBC - BV_POSTX, BV_POSTY0, TRAY_POST_DIAMETER, BV_KBZ0, BV_IZ1],
            ["cyl", "post_lr", BV_KBC - BV_POSTX, BV_POSTY1, TRAY_POST_DIAMETER, BV_KBZ0, BV_IZ1],
            ["cyl", "post_rf", BV_KBC + BV_POSTX, BV_POSTY0, TRAY_POST_DIAMETER, BV_KBZ0, BV_IZ1],
            ["cyl", "post_rr", BV_KBC + BV_POSTX, BV_POSTY1, TRAY_POST_DIAMETER, BV_KBZ0, BV_IZ1]
        ]],
        ["TRACKPAD_TRAY", "S", [
            ["box", "plate", BV_BHL1, BV_TTY0, BV_TTZ0, BV_BHR0, BV_TTY1, BV_TPZ0]
        ]],
        ["COMPUTE_SLED", "S", [
            ["box", "plate", BV_BHR1 + CLEARANCE, BV_SLY0, BV_SLZ0, BV_IX - CLEARANCE, BV_SLY1, BV_SLZ1]
        ]],
        ["SERVICE_PANEL_MAIN", "S", [
            ["box", "main", BV_SEAMX + CLEARANCE / 2, BV_IY0 + CLEARANCE, 0 * millimeter, BV_IX - CLEARANCE, BV_IY1 - CLEARANCE, BV_IZ0],
            ["box", "rear_left", -BV_IX + CLEARANCE, BV_SEAMY + CLEARANCE / 2, 0 * millimeter, BV_SEAMX + CLEARANCE / 2, BV_IY1 - CLEARANCE, BV_IZ0]
        ]],
        ["BATTERY_DOOR", "S", [
            ["box", "plate", -BV_IX + CLEARANCE, BV_IY0 + CLEARANCE, 0 * millimeter, BV_SEAMX - CLEARANCE / 2, BV_SEAMY - CLEARANCE / 2, BV_IZ0]
        ]],
        ["PORT_PANEL_MAIN", "S", [
            ["box", "plate", BV_PX0 + CLEARANCE, BV_IY1, 0 * millimeter, BV_PX1 - CLEARANCE, BODY_DEPTH, BV_PZ1 - CLEARANCE]
        ]],
        ["PORT_PANEL_AUX", "S", [
            ["box", "plate", -BV_PX1 + CLEARANCE, BV_IY1, 0 * millimeter, -BV_PX0 - CLEARANCE, BODY_DEPTH, BV_PZ1 - CLEARANCE]
        ]],
        ["PANEL_STANDOFF_L", "S", [
            ["cyl", "standoff", BV_KBC - BV_STDX, BV_STDY, TRAY_POST_DIAMETER, BV_IZ0, BV_KTZ0]
        ]],
        ["PANEL_STANDOFF_R", "S", [
            ["cyl", "standoff", BV_KBC + BV_STDX, BV_STDY, TRAY_POST_DIAMETER, BV_IZ0, BV_KTZ0]
        ]],
        ["ENV_KEYBOARD", "E", [
            ["box", "env", BV_KBC - KEYBOARD_WIDTH / 2, BV_KBY0, BV_KBZ0, BV_KBC + KEYBOARD_WIDTH / 2, BV_KBY1, BV_KBZ1]
        ]],
        ["ENV_TRACKPAD", "E", [
            ["box", "env", BV_TPC - TRACKPAD_WIDTH / 2, BV_TPY0, BV_TPZ0, BV_TPC + TRACKPAD_WIDTH / 2, BV_TPY1, BV_TPZ1]
        ]],
        ["ENV_PI_STACK", "E", [
            ["box", "env", BV_PIX0, BV_PIY0, BV_SLZ1, BV_PIX1, BV_PIY1, BV_PIZ1]
        ]],
        ["ENV_COMPUTE_POWER", "E", [
            ["box", "env", BV_CPX0, BV_CPY0, BV_CZ0, BV_CPX1, BV_CPY1, BV_CPZ1]
        ]],
        ["ENV_POWER_ELECTRONICS", "E", [
            ["box", "env", BV_PEX0, BV_PEY0, BV_CZ0, BV_PEX1, BV_PEY1, BV_PEZ1]
        ]],
        ["ENV_BATTERY_BAY", "E", [
            ["box", "env", BV_BATX0, BV_BATY0, BV_BATZ0, BV_BATX1, BV_BATY1, BV_BATZ1]
        ]],
        ["ENV_GNSS_MODULE", "E", [
            ["box", "env", BV_GNX0, BV_GNY0, BV_CZ0, BV_GNX1, BV_GNY1, BV_GNZ1]
        ]],
        ["KEEPOUT_HINGE_MOUNT_L", "H", [
            ["box", "reserve", -BV_IX, BV_HY0, BV_IZ0, -BV_HX0, BV_IY1, BV_IZ1]
        ]],
        ["KEEPOUT_HINGE_MOUNT_R", "H", [
            ["box", "reserve", BV_HX0, BV_HY0, BV_IZ0, BV_IX, BV_IY1, BV_IZ1]
        ]],
        ["KEEPOUT_COOLING_DUCT", "K", [
            ["box", "duct", BV_DUX0, BV_DUY0, BV_SLZ1, BV_DUX1, BV_PIY0, BV_DUZ1]
        ]],
        ["KEEPOUT_PORTS_MAIN", "K", [
            ["box", "connectors", BV_PX0, BV_TRY1, BV_PZ0, BV_PX1, BV_IY1, BV_PZ1]
        ]],
        ["KEEPOUT_PORTS_AUX", "K", [
            ["box", "connectors", -BV_PX1, BV_TRY1, BV_PZ0, -BV_PX0, BV_IY1, BV_PZ1]
        ]],
        ["CABLE_TRUNK", "C", [
            ["box", "trunk", BV_BLX0, BV_TRY0, BV_CZ0, BV_CCX1, BV_TRY1, BV_CZ1]
        ]],
        ["CABLE_COMPUTE", "C", [
            ["box", "run", BV_CCX0, BV_PIY1, BV_CCZ0, BV_CCX1, BV_TRY1, BV_CCZ1]
        ]],
        ["CABLE_TRACKPAD", "C", [
            ["box", "drop", BV_TPC - BV_CW2, BV_TTY1 - CABLE_CORRIDOR_WIDTH, BV_CZ1, BV_TPC + BV_CW2, BV_TTY1, BV_TTZ0],
            ["box", "run", BV_TPC - BV_CW2, BV_TTY1 - CABLE_CORRIDOR_WIDTH, BV_CZ0, BV_TPC + BV_CW2, BV_TRY1, BV_CZ1]
        ]],
        ["CABLE_KEYBOARD", "C", [
            ["box", "drop", BV_KBC - BV_CW2, BV_TRY0, BV_CZ1, BV_KBC + BV_CW2, BV_TRY1, BV_KTZ0]
        ]],
        ["CABLE_DISPLAY", "C", [
            ["box", "run", -BV_CW2, BV_TRY0, BV_CZ0, BV_CW2, BV_RSY0 + CABLE_CORRIDOR_WIDTH, BV_CZ1],
            ["box", "riser", -BV_CW2, BV_RSY0, BV_CZ1, BV_CW2, BV_RSY1, BV_IZ1]
        ]],
        ["CABLE_POWER", "C", [
            ["box", "run", BV_BLX0, BV_PEY1, BV_CZ0, BV_BLX1, BV_TRY1, BV_CZ1]
        ]],
        ["CABLE_BATTERY", "C", [
            ["box", "run", BV_BLX0, BV_BATY1, BV_CZ0, BV_BLX1, BV_PEY0, BV_CZ1]
        ]],
        ["KEEPOUT_VENT_INTAKE", "W", [
            ["box", "zone", BV_DUX0, 0 * millimeter, BV_SLZ1, BV_DUX1, BV_IY0, BV_DUZ1]
        ]],
        ["KEEPOUT_VENT_EXHAUST", "W", [
            ["box", "zone", BV_IX, BV_PIY0, BV_SLZ1, BV_W2, BV_PIY1, BV_PIZ1]
        ]],
        ["KEEPOUT_DISPLAY_PASS", "W", [
            ["box", "zone", -BV_CW2, BV_IY1, BV_IZ1 - CABLE_CORRIDOR_HEIGHT, BV_CW2, BODY_DEPTH, BODY_HEIGHT]
        ]],
        ["KEEPOUT_PLUGS_MAIN", "X", [
            ["box", "zone", BV_PX0, BODY_DEPTH, BV_PZ0, BV_PX1, BODY_DEPTH + PLUG_KEEPOUT_LENGTH, BV_PZ1]
        ]],
        ["KEEPOUT_PLUGS_AUX", "X", [
            ["box", "zone", -BV_PX1, BODY_DEPTH, BV_PZ0, -BV_PX0, BODY_DEPTH + PLUG_KEEPOUT_LENGTH, BV_PZ1]
        ]]
    ];
}
// END GENERATED BASE V0.1 LAYOUT

function nomadBaseV01Color(cat is string) returns Color
{
    const colors = { "S" : color(0.72, 0.74, 0.78, 1), "E" : color(0.22, 0.45, 0.85, 1), "H" : color(0.85, 0.2, 0.2, 0.4),
            "K" : color(0.95, 0.6, 0.1, 0.4), "C" : color(0.2, 0.7, 0.3, 0.4), "W" : color(0.6, 0.3, 0.8, 0.5),
            "X" : color(0.95, 0.85, 0.1, 0.3) };
    return colors[cat];
}

// Builds every base V0.1 part as one named solid (union of its primitives). withReserves = false builds
// only the structural parts (category S). Returns part name -> body query.
export function nomadBuildBaseV01(context is Context, id is Id, withReserves is boolean) returns map
{
    var parts = {};
    const table = nomadBaseV01Parts();
    for (var i = 0; i < size(table); i += 1)
    {
        const spec = table[i];
        if (withReserves || spec[1] == "S")
        {
            const pid = id + ("part" ~ i);
            const prims = spec[2];
            for (var j = 0; j < size(prims); j += 1)
            {
                const q = prims[j];
                if (q[0] == "box")
                    fCuboid(context, pid + ("p" ~ j), { "corner1" : vector(q[2], q[3], q[4]), "corner2" : vector(q[5], q[6], q[7]) });
                else
                    fCylinder(context, pid + ("p" ~ j), { "bottomCenter" : vector(q[2], q[3], q[5]),
                                "topCenter" : vector(q[2], q[3], q[6]), "radius" : q[4] / 2 });
            }
            if (size(prims) > 1)
                opBoolean(context, pid + "union", { "tools" : qCreatedBy(pid, EntityType.BODY), "operationType" : BooleanOperationType.UNION });
            const body = qCreatedBy(pid, EntityType.BODY);
            nomadTag(context, body, spec[0], nomadBaseV01Color(spec[1]));
            parts[spec[0]] = body;
        }
    }
    return parts;
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
annotation { "Feature Type Name" : "NOMAD Base V0.1" }
export const nomadBaseV01 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Show envelopes and keep-outs" }
        definition.showReserves is boolean;
    }
    {
        nomadBuildBaseV01(context, id, definition.showReserves);
    }, { "showReserves" : true });
// END PRODUCTION FEATURES
