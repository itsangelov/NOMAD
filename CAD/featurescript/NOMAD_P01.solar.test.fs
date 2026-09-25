// NOMAD P0.1 Round B: Onshape kernel cross-check of the solar skeleton model (V0 working layout).
// Never written to the Onshape document. Payload:
//   py CAD/tools/build_test_payload.py OUT NOMAD_P01.solar.test.fs
// Mirrors CROSSCHECK in CAD/tools/solar_skeleton_model.py. For each state, lists overlapping pairs
// (same exclusions as the model) and the solar parts' minimum world z, in one line delivered via a
// deliberate regenError (test_feature returns notices only):
//   <label>:<pairs or ->z<min z>

annotation { "Feature Type Name" : "NOMAD Round B Check" }
export const nomadRoundBCheck = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        // label, lid angle (deg), right extension, left extension, tilt (deg)
        const states = [["S", 105, 0, 0, 0], ["D", 105, 1, 1, 0], ["a", 0, 1, 1, 30], ["b", 0, 1, 1, 45],
                ["c", 135, 1, 1, 75], ["d", 135, 1, 1, -75]];
        const names = ["B", "CL", "CR", "D", "KL", "KR", "PL", "PR", "RL", "RR"];
        const attached = ["KP", "PK", "PR", "RP", "KR", "RK", "CP", "PC"];
        const overlapTypes = [ClashType.INTERFERE, ClashType.TARGET_IN_TOOL, ClashType.TOOL_IN_TARGET];
        const lay = nomadSolarLayout();
        const hinge = nomadDefaultHinge();
        var out = "X";
        for (var n = 0; n < size(states); n += 1)
        {
            const st = states[n];
            const sid = id + ("s" ~ toString(n));
            const lidAngle = st[1] * degree;
            const roundA = nomadBuildRoundA(context, sid + "a", lidAngle, hinge);
            var parts = mergeMaps(nomadBuildSolarSide(context, sid + "r", 1, st[2], st[4] * degree, lidAngle, hinge, lay),
                    nomadBuildSolarSide(context, sid + "l", -1, st[3], st[4] * degree, lidAngle, hinge, lay));
            parts["D"] = roundA.ENV_DISPLAY;
            parts["B"] = roundA.SKEL_BASE;
            var pairs = "";
            for (var i = 0; i < size(names); i += 1)
            {
                for (var j = i + 1; j < size(names); j += 1)
                {
                    const a = names[i];
                    const b = names[j];
                    var skip = a == "B" && b == "D";
                    if (!isIn(a, ["B", "D"]) && !isIn(b, ["B", "D"]))
                    {
                        const ca = splitIntoCharacters(a);
                        const cb = splitIntoCharacters(b);
                        if (ca[1] == cb[1] && isIn(ca[0] ~ cb[0], attached))
                            skip = true;
                    }
                    if (!skip)
                    {
                        var hit = false;
                        for (var c in evCollision(context, { "tools" : parts[a], "targets" : parts[b] }))
                        {
                            const t = c["type"] != undefined ? c["type"] : c["clashType"];
                            if (isIn(t, overlapTypes))
                                hit = true;
                        }
                        if (hit)
                            pairs = pairs ~ a ~ b;
                    }
                }
            }
            const solar = qUnion([parts.CL, parts.CR, parts.KL, parts.KR, parts.PL, parts.PR, parts.RL, parts.RR]);
            const zmin = evBox3d(context, { "topology" : solar, "tight" : true }).minCorner[2] / millimeter;
            out = out ~ " " ~ st[0] ~ ":" ~ (pairs == "" ? "-" : pairs) ~ "z" ~ toString(roundToPrecision(zmin, 1));
        }
        throw regenError(out);
    }, {});
