// NOMAD P0.1 Round A.1 test harness. Never written to the Onshape document.
// Appended to NOMAD_P01.fs (minus its production features) by CAD/tools/build_test_payload.py.
//
// Controlled hinge experiment (no option is chosen here):
//   A  hinge axis at the base rear edge (inset 0, height 0)
//   B  hinge axis at the default inset, raised to the closed lid's mid-thickness
//   C  default hinge axis (HINGE_AXIS_OFFSET / HINGE_AXIS_HEIGHT) + modeled base relief
//      (the base minus the lid's swept envelope)
// For each option: the lid envelope is swept 0..LID_ANGLE_MAX in NOMAD_SWEEP_STEP samples to find
// intrusion into the base envelope between the check poses, then Round A is built and checked at
// 0, LID_ANGLE_NOMINAL and LID_ANGLE_MAX.
//
// test_feature returns evaluation notices only, truncated after roughly 330 characters, so the
// report is one compact line delivered as the message of a deliberate regenError.
// Format:
//   R C<closed overall XxYxZ> g:<closed gaps> h:<clear height under keyboard>/<under trackpad>
//   |<opt>@y<axis y>z<axis z> i<sweep intrusion into base: cc/XxYxZ@y<min y>z<min z>, or 0>
//     <angle>o<rear overhang>z<max height> ...  ok | x: <angle><pair>!(overlap) or =<gap>
// Body codes: B SKEL_BASE, K ENV_KEYBOARD, T ENV_TRACKPAD, L SKEL_LID, D ENV_DISPLAY.

// Sampling resolution of the test sweep only; not a design dimension.
const NOMAD_SWEEP_STEP = 5 * degree;

function nomadCode(name is string) returns string
{
    const codes = { "SKEL_BASE" : "B", "ENV_KEYBOARD" : "K", "ENV_TRACKPAD" : "T", "SKEL_LID" : "L", "ENV_DISPLAY" : "D" };
    return codes[name];
}

function nomadR1(x is number) returns string
{
    return toString(roundToPrecision(x, 1));
}

function nomadSizeText(sz is array) returns string
{
    return nomadR1(sz[0]) ~ "x" ~ nomadR1(sz[1]) ~ "x" ~ nomadR1(sz[2]);
}

function nomadOverlapping(context is Context, a is Query, b is Query) returns boolean
{
    const overlapTypes = [ClashType.INTERFERE, ClashType.TARGET_IN_TOOL, ClashType.TOOL_IN_TARGET];
    for (var c in evCollision(context, { "tools" : a, "targets" : b }))
    {
        const t = c["type"] != undefined ? c["type"] : c["clashType"];
        if (isIn(t, overlapTypes))
            return true;
    }
    return false;
}

// Solid (unhollowed) lid envelope at one angle.
function nomadLidEnvelope(context is Context, id is Id, angle is ValueWithUnits, hinge is map) returns Query
{
    const halfW = BODY_WIDTH / 2;
    const z0 = BODY_HEIGHT + LID_CLOSED_GAP;
    const q = nomadBox(context, id + "box", vector(-halfW, 0 * millimeter, z0), vector(halfW, BODY_DEPTH, z0 + LID_THICKNESS));
    opTransform(context, id + "pose", { "bodies" : q, "transform" : nomadLidTransform(angle, hinge) });
    return q;
}

// Union of sampled lid envelopes from 0 to LID_ANGLE_MAX.
function nomadLidSweep(context is Context, id is Id, hinge is map) returns Query
{
    var lids = [];
    for (var k = 0; k * NOMAD_SWEEP_STEP <= LID_ANGLE_MAX + 1e-6 * degree; k += 1)
        lids = append(lids, nomadLidEnvelope(context, id + ("s" ~ toString(k)), k * NOMAD_SWEEP_STEP, hinge));
    opBoolean(context, id + "union", { "tools" : qUnion(lids), "operationType" : BooleanOperationType.UNION });
    const sweep = qUnion(lids);
    if (size(evaluateQuery(context, sweep)) != 1)
        throw regenError("NOMAD test: lid sweep did not merge into one body");
    return sweep;
}

// Part of the lid sweep that lies inside the base outer envelope.
function nomadIntrusion(context is Context, id is Id, sweep is Query) returns string
{
    const halfW = BODY_WIDTH / 2;
    const zero = 0 * millimeter;
    const baseEnv = nomadBox(context, id + "env", vector(-halfW, zero, zero), vector(halfW, BODY_DEPTH, BODY_HEIGHT));
    if (!nomadOverlapping(context, sweep, baseEnv))
        return "0";
    opBoolean(context, id + "int", { "tools" : qUnion([sweep, baseEnv]), "operationType" : BooleanOperationType.INTERSECTION, "keepTools" : true });
    const region = qCreatedBy(id + "int", EntityType.BODY);
    const cc = evVolume(context, { "entities" : region }) / (centimeter ^ 3);
    const extent = nomadBoxReport(context, region);
    return nomadR1(cc) ~ "cc/" ~ nomadSizeText(extent.size) ~ "@y" ~ nomadR1(extent.min[1]) ~ "z" ~ nomadR1(extent.min[2]);
}

annotation { "Feature Type Name" : "NOMAD Round A1 Test" }
export const nomadRoundA1Test = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const angles = [0 * degree, LID_ANGLE_NOMINAL, LID_ANGLE_MAX];
        const options = [
                { "code" : "A", "hinge" : { "offset" : 0 * millimeter, "height" : 0 * millimeter }, "relief" : false },
                { "code" : "B", "hinge" : { "offset" : HINGE_AXIS_OFFSET, "height" : LID_CLOSED_GAP + LID_THICKNESS / 2 }, "relief" : false },
                { "code" : "C", "hinge" : nomadDefaultHinge(), "relief" : true }
            ];
        var head = "R";
        var report = "";
        for (var opt in options)
        {
            const oid = id + opt.code;
            const hp = nomadHingePoint(opt.hinge);
            const sweep = nomadLidSweep(context, oid + "sweep", opt.hinge);
            var text = "|" ~ opt.code ~ "@y" ~ nomadR1(hp[1] / millimeter) ~ "z" ~ nomadR1(hp[2] / millimeter) ~
                " i" ~ nomadIntrusion(context, oid + "intr", sweep);
            var issues = "";
            for (var i = 0; i < size(angles); i += 1)
            {
                const poseId = oid + ("p" ~ toString(i));
                nomadBuildRoundA(context, poseId, angles[i], opt.hinge);
                const bodies = nomadCollect(context, qCreatedBy(poseId, EntityType.BODY));
                if (opt.relief)
                    opBoolean(context, poseId + "relief", { "tools" : sweep, "targets" : bodies.SKEL_BASE,
                                "operationType" : BooleanOperationType.SUBTRACTION, "keepTools" : true });
                const res = nomadCheckPose(context, bodies, angles[i]);
                const deg = toString(res.lid_angle_deg);
                if (i > 0)
                    text = text ~ " " ~ deg ~ "o" ~ nomadR1(res.overall.max[1] - BODY_DEPTH / millimeter) ~ "z" ~ nomadR1(res.overall.max[2]);
                for (var p in res.pairs)
                {
                    const tag = nomadCode(p.a) ~ nomadCode(p.b);
                    if (p.state == "overlap")
                        issues = issues ~ " " ~ deg ~ tag ~ "!";
                    else if (p.gap_mm < MIN_GAP / millimeter - 1e-6)
                        issues = issues ~ " " ~ deg ~ tag ~ "=" ~ nomadR1(p.gap_mm);
                }
                if (res.overall.min[2] < -1e-3)
                    issues = issues ~ " " ~ deg ~ "G";
                if (i == 0 && opt.code == "A")
                {
                    head = head ~ " C" ~ nomadSizeText(res.overall.size) ~ " g:";
                    for (var p in res.pairs)
                    {
                        const tag = nomadCode(p.a) ~ nomadCode(p.b);
                        if (isIn(tag, ["BL", "KD", "TD"]))
                            head = head ~ tag ~ nomadR1(p.gap_mm) ~ " ";
                    }
                    const floorTop = WALL_THICKNESS / millimeter;
                    head = head ~ "h:" ~ nomadR1(nomadBoxReport(context, bodies.ENV_KEYBOARD).min[2] - floorTop) ~ "/" ~
                        nomadR1(nomadBoxReport(context, bodies.ENV_TRACKPAD).min[2] - floorTop);
                }
            }
            report = report ~ text ~ (issues == "" ? " ok " : " x:" ~ issues ~ " ");
        }
        throw regenError(head ~ " " ~ report);
    }, {});
