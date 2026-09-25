// NOMAD P0.1 hinge feasibility map: Onshape cross-check of selected grid points.
// Never written to the Onshape document. Appended to NOMAD_P01.fs (minus its production
// features) by: py CAD/tools/build_test_payload.py OUT NOMAD_P01.hingemap.test.fs
//
// The full grid is computed by CAD/tools/hinge_feasibility_2d.py (exact 2D model). This harness
// recomputes selected points with the Onshape kernel: for each hinge (inset, height) the solid lid
// envelope is rotated through 0..LID_ANGLE_MAX in NOMAD_SWEEP_STEP steps against the solid base
// envelope. Report (one line via a deliberate regenError, because test_feature returns notices only):
//   <inset>/<height>:<min gap over non-overlapping samples, mm>@<angle>n<overlapping samples>

const NOMAD_SWEEP_STEP = 5 * degree;

function nomadR2(x is number) returns string
{
    return toString(roundToPrecision(x, 2));
}

function nomadEnvOverlap(context is Context, a is Query, b is Query) returns boolean
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

annotation { "Feature Type Name" : "NOMAD Hinge Map Check" }
export const nomadHingeMapCheck = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const points = [[-6, -4], [-2, 14], [0, -2], [0, 0], [0, 2], [0, 26], [2, 26], [4, 10], [6, 12], [6, 14], [10, 26]];
        const halfW = BODY_WIDTH / 2;
        const zero = 0 * millimeter;
        const z0 = BODY_HEIGHT + LID_CLOSED_GAP;
        const baseEnv = nomadBox(context, id + "baseEnv", vector(-halfW, zero, zero), vector(halfW, BODY_DEPTH, BODY_HEIGHT));
        var out = "M";
        for (var n = 0; n < size(points); n += 1)
        {
            const hinge = { "offset" : points[n][0] * millimeter, "height" : points[n][1] * millimeter };
            const lid = nomadBox(context, id + ("lid" ~ toString(n)), vector(-halfW, zero, z0), vector(halfW, BODY_DEPTH, z0 + LID_THICKNESS));
            var best = 1e9;
            var bestAngle = 0;
            var hits = 0;
            for (var k = 0; k * NOMAD_SWEEP_STEP <= LID_ANGLE_MAX + 1e-6 * degree; k += 1)
            {
                if (k > 0)
                    opTransform(context, id + ("r" ~ toString(n) ~ "k" ~ toString(k)), { "bodies" : lid, "transform" : nomadLidTransform(NOMAD_SWEEP_STEP, hinge) });
                if (nomadEnvOverlap(context, lid, baseEnv))
                    hits += 1;
                else
                {
                    const gap = evDistance(context, { "side0" : lid, "side1" : baseEnv }).distance / millimeter;
                    if (gap < best)
                    {
                        best = gap;
                        bestAngle = roundToPrecision(k * NOMAD_SWEEP_STEP / degree, 0);
                    }
                }
            }
            out = out ~ " " ~ toString(points[n][0]) ~ "/" ~ toString(points[n][1]) ~ ":" ~ nomadR2(best) ~ "@" ~ toString(bestAngle) ~ "n" ~ toString(hits);
        }
        throw regenError(out);
    }, {});
