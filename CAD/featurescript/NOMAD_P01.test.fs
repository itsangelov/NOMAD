// NOMAD P0.1 Round A test harness. Never written to the Onshape document.
// Appended to NOMAD_P01.fs (minus its production features) by CAD/tools/build_test_payload.py.
// Builds Round A at lid angles 0, LID_ANGLE_NOMINAL and LID_ANGLE_MAX in one scratch context
// and checks each pose.
//
// test_feature returns evaluation notices only (no console output), and notice messages are
// truncated after roughly 330 characters. The report is therefore one compact line delivered as
// the message of a deliberate regenError at the very end: the error is the report channel.
//
// Report format:
//   w<working params> u<unresolved params> C<containment flag per envelope, 1 = inside>
//   g:<closed-pose gaps, mm>  |<lid angle>:<overall X x Y x Z> z<min z> <pair findings>...
// Body codes: B SKEL_BASE, K ENV_KEYBOARD, T ENV_TRACKPAD, L SKEL_LID, D ENV_DISPLAY.
// Pair findings: AB!<overlap region XxYxZ>/<volume cc> = overlap;  AB=<gap> gap below MIN_GAP
// (suffix e = expected closed-lid seating contact).

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

// Bounding size and volume of the overlap between two bodies (kept-tools intersection).
function nomadOverlapText(context is Context, id is Id, a is Query, b is Query) returns string
{
    var text = "?";
    try silent
    {
        opBoolean(context, id, { "tools" : qUnion([a, b]), "operationType" : BooleanOperationType.INTERSECTION, "keepTools" : true });
        const region = qCreatedBy(id, EntityType.BODY);
        const cc = evVolume(context, { "entities" : region }) / (centimeter ^ 3);
        text = nomadSizeText(nomadBoxReport(context, region).size) ~ "/" ~ nomadR1(cc) ~ "cc";
    }
    return text;
}

annotation { "Feature Type Name" : "NOMAD Round A Test" }
export const nomadRoundATest = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const angles = [0 * degree, LID_ANGLE_NOMINAL, LID_ANGLE_MAX];
        var out = "w" ~ toString(nomadWorkingCount()) ~ "u" ~ toString(size(NOMAD_UNRESOLVED));
        var poseText = "";
        for (var i = 0; i < size(angles); i += 1)
        {
            const poseId = id + ("pose" ~ toString(i));
            nomadBuildRoundA(context, poseId, angles[i]);
            const bodies = nomadCollect(context, qCreatedBy(poseId, EntityType.BODY));
            const res = nomadCheckPose(context, bodies, angles[i]);
            if (i == 0)
            {
                out = out ~ " C";
                for (var r in nomadContainment(context, bodies))
                    out = out ~ (r.inside_bbox ? "1" : "0");
                out = out ~ " g:";
                for (var p in res.pairs)
                {
                    const tag = nomadCode(p.a) ~ nomadCode(p.b);
                    if (isIn(tag, ["BK", "BT", "KT", "LD"]))
                        out = out ~ tag ~ nomadR1(p.gap_mm) ~ " ";
                }
            }
            poseText = poseText ~ "|" ~ toString(res.lid_angle_deg) ~ ":" ~ nomadSizeText(res.overall.size) ~ " z" ~ nomadR1(res.overall.min[2]);
            for (var p in res.pairs)
            {
                const tag = nomadCode(p.a) ~ nomadCode(p.b);
                if (p.state == "overlap")
                    poseText = poseText ~ " " ~ tag ~ "!" ~ nomadOverlapText(context, id + ("ov" ~ toString(i) ~ tag), bodies[p.a], bodies[p.b]);
                else if (p.gap_mm < MIN_GAP / millimeter - 1e-6)
                    poseText = poseText ~ " " ~ tag ~ "=" ~ nomadR1(p.gap_mm) ~ (i == 0 && tag == "BL" ? "e" : "");
            }
            poseText = poseText ~ " ";
        }
        throw regenError("R " ~ out ~ poseText);
    }, {});
