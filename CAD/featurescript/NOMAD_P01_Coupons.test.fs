// NOMAD P0.1 coupons: scratch validation harness for NOMAD_P01_Coupons.fs. NEVER written to the NOMAD
// document. Payload (one test_feature call; the production feature is stripped so the payload defines one
// feature):  py CAD/tools/build_test_payload.py OUT NOMAD_P01_Coupons.test.fs NOMAD_P01_Coupons.fs
// Reports through a deliberate regenError (test_feature returns notices only, truncated at ~330 chars).
//   1. Runs the production build exactly as the feature does (laid out): body count, names,
//      bounding boxes, print orientation (Z min 0), volumes vs onshape_crosscheck.py, pairwise overlaps.
//   2. Builds a second, un-laid-out set and probes it point by point (the generate_coupons.py probes and more).
//   3. Assembles the rigs (rail on pad stub, surrogate, carriage in A1/A2; plates on the B frame, block,
//      load pad) and measures the fits with evCollision / evDistance.
// Run 1 (2026-09-25): 185/192 probes, 16/16 rig checks; the 7 misses were misplaced probes (A2 channel
// edge probed at Y 16.05 < 16.1; B2 rib-side probes at X 115 sat on the mid-span transverse rib), and the
// reference model is solid at all 7 points too. Corrected here (Y 16.15; X 60); not re-run.
// Report: CPN n<bodies> nm<names ok> bb<bbox ok> z<on bed> v<max vol dev %> ov<overlaps> ab<touches>
//   P<probe pass/total> A<assembly pass/total> dRS dC dBP arm eng F:<first failures>

// [name, bbox X, Y, Z, volume mm3] from `py CAD/coupons/P0.1/onshape_crosscheck.py` (true round holes).
const CPN_EXPECT = [
    ["CPN_A1_rail", 200, 39.6, 13, 31544.804],
    ["CPN_A2_rail_stiffener_slots", 200, 42.8, 13, 30392.484],
    ["CPN_A_carriage_load_post", 40, 22, 20, 14417.072],
    ["CPN_A_load_platform", 60, 60, 6, 19505.040],
    ["CPN_A_pad_stub", 60, 70, 6, 24922.322],
    ["CPN_A_display_surrogate", 170, 30, 5, 25500.000],
    ["CPN_B_supports", 230, 90, 14, 107698.407],
    ["CPN_B_clearance_block", 60, 60, 9, 32400.000],
    ["CPN_B1_plate", 230, 90, 2.5, 51659.208],
    ["CPN_B2_h6_plate", 230, 90, 8.5, 62027.208],
    ["CPN_B2_h8_plate", 230, 90, 10.5, 65483.208],
    ["CPN_B2_h11_plate", 230, 90, 13.5, 70667.208],
    ["CPN_B_load_pad", 20, 20, 5, 2000.000]
];

// [part, x, y, z (mm, part frame), 1 = solid expected / 0 = empty expected]
const CPN_PROBES = [
    // A1: channel 22.6 x 8.0 (Y 14.5..37.1, Z 2.5..10.5), slot 17.6 (Y 17..34.6), lips 2.5, end stop, inserts
    ["CPN_A1_rail", 100, 25.8, 6.5, 0], ["CPN_A1_rail", 100, 14.45, 5, 1], ["CPN_A1_rail", 100, 14.55, 5, 0],
    ["CPN_A1_rail", 100, 37.05, 5, 0], ["CPN_A1_rail", 100, 37.15, 5, 1], ["CPN_A1_rail", 100, 25.8, 2.45, 1],
    ["CPN_A1_rail", 100, 25.8, 2.55, 0], ["CPN_A1_rail", 100, 25.8, 10.45, 0], ["CPN_A1_rail", 100, 16, 10.45, 0],
    ["CPN_A1_rail", 100, 16, 10.55, 1], ["CPN_A1_rail", 100, 16, 12.95, 1], ["CPN_A1_rail", 100, 17.05, 12, 0],
    ["CPN_A1_rail", 100, 16.95, 12, 1], ["CPN_A1_rail", 100, 34.55, 12, 0], ["CPN_A1_rail", 100, 34.65, 12, 1],
    ["CPN_A1_rail", 199, 25.8, 5, 1], ["CPN_A1_rail", 197.9, 25.8, 5, 0], ["CPN_A1_rail", 0.05, 25.8, 5, 0],
    ["CPN_A1_rail", 7, 6, 3, 0], ["CPN_A1_rail", 7, 6, 5.95, 0], ["CPN_A1_rail", 7, 6, 6.05, 1],
    ["CPN_A1_rail", 21.5, 6, 3, 0], ["CPN_A1_rail", 21.5, 6, 6.05, 1], ["CPN_A1_rail", 8.95, 6, 3, 0],
    ["CPN_A1_rail", 9.05, 6, 3, 1], ["CPN_A1_rail", 28.45, 6, 6, 1], ["CPN_A1_rail", 28.55, 6, 6, 0],
    // A2: channel Y 16.1..38.7, slot Y 18.6..36.2, strip slots Y 12.9..15.2 / 39.6..41.9, Z 1.3..11.7
    ["CPN_A2_rail_stiffener_slots", 100, 27.4, 6.5, 0], ["CPN_A2_rail_stiffener_slots", 100, 16.15, 5, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 15.95, 5, 1], ["CPN_A2_rail_stiffener_slots", 100, 38.65, 5, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 38.75, 5, 1], ["CPN_A2_rail_stiffener_slots", 100, 18.65, 12, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 18.55, 12, 1], ["CPN_A2_rail_stiffener_slots", 100, 36.15, 12, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 36.25, 12, 1], ["CPN_A2_rail_stiffener_slots", 100, 12.95, 6, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 12.85, 6, 1], ["CPN_A2_rail_stiffener_slots", 100, 15.15, 6, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 15.25, 6, 1], ["CPN_A2_rail_stiffener_slots", 100, 14, 1.35, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 14, 1.25, 1], ["CPN_A2_rail_stiffener_slots", 100, 14, 11.65, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 14, 11.75, 1], ["CPN_A2_rail_stiffener_slots", 100, 39.65, 6, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 39.55, 6, 1], ["CPN_A2_rail_stiffener_slots", 100, 41.85, 6, 0],
    ["CPN_A2_rail_stiffener_slots", 100, 41.95, 6, 1], ["CPN_A2_rail_stiffener_slots", 0.05, 14, 6, 0],
    ["CPN_A2_rail_stiffener_slots", 197.95, 14, 6, 0], ["CPN_A2_rail_stiffener_slots", 199, 14, 6, 1],
    ["CPN_A2_rail_stiffener_slots", 0.05, 40.75, 6, 0], ["CPN_A2_rail_stiffener_slots", 197.95, 40.75, 6, 0],
    ["CPN_A2_rail_stiffener_slots", 199, 40.75, 6, 1], ["CPN_A2_rail_stiffener_slots", 199, 27.4, 5, 1],
    ["CPN_A2_rail_stiffener_slots", 0.05, 27.4, 5, 0], ["CPN_A2_rail_stiffener_slots", 7, 6, 3, 0],
    ["CPN_A2_rail_stiffener_slots", 21.5, 6, 3, 0], ["CPN_A2_rail_stiffener_slots", 7, 6, 6.05, 1],
    // carriage: body 40 x 22 x 7.4, post Y 2.7..19.3 to Z 20, edge reliefs, teardrop centre (20, Z 15), apex Z 18.89
    ["CPN_A_carriage_load_post", 20, 11, 3, 1], ["CPN_A_carriage_load_post", 5, 2.65, 12, 0],
    ["CPN_A_carriage_load_post", 5, 2.75, 12, 1], ["CPN_A_carriage_load_post", 5, 19.25, 12, 1],
    ["CPN_A_carriage_load_post", 5, 19.35, 12, 0], ["CPN_A_carriage_load_post", 5, 11, 19.95, 1],
    ["CPN_A_carriage_load_post", 20, 0.25, 0.25, 0], ["CPN_A_carriage_load_post", 20, 0.75, 0.75, 1],
    ["CPN_A_carriage_load_post", 20, 21.75, 0.25, 0], ["CPN_A_carriage_load_post", 20, 0.25, 7.15, 0],
    ["CPN_A_carriage_load_post", 20, 21.75, 7.15, 0], ["CPN_A_carriage_load_post", 20, 0.75, 6.65, 1],
    ["CPN_A_carriage_load_post", 20, 11, 15, 0], ["CPN_A_carriage_load_post", 20, 11, 18.8, 0],
    ["CPN_A_carriage_load_post", 20, 11, 18.95, 1], ["CPN_A_carriage_load_post", 20, 11, 12.35, 0],
    ["CPN_A_carriage_load_post", 20, 11, 12.15, 1], ["CPN_A_carriage_load_post", 22.7, 11, 15, 0],
    ["CPN_A_carriage_load_post", 22.8, 11, 15, 1],
    // platform: pocket X 9.7..50.3, Y 21.4..38.6, Z 3..6
    ["CPN_A_load_platform", 30, 30, 4, 0], ["CPN_A_load_platform", 30, 30, 2.95, 1],
    ["CPN_A_load_platform", 9.75, 30, 4, 0], ["CPN_A_load_platform", 9.65, 30, 4, 1],
    ["CPN_A_load_platform", 50.25, 30, 4, 0], ["CPN_A_load_platform", 50.35, 30, 4, 1],
    ["CPN_A_load_platform", 30, 21.45, 4, 0], ["CPN_A_load_platform", 30, 21.35, 4, 1],
    ["CPN_A_load_platform", 30, 38.55, 4, 0], ["CPN_A_load_platform", 30, 38.65, 4, 1],
    // pad stub: holes at (38.5, 15) and (53, 15): counterbore r 3.25 to Z 3.5, clearance r 1.7
    ["CPN_A_pad_stub", 38.5, 15, 1, 0], ["CPN_A_pad_stub", 38.5, 18.2, 1, 0], ["CPN_A_pad_stub", 38.5, 18.3, 1, 1],
    ["CPN_A_pad_stub", 38.5, 15, 5, 0], ["CPN_A_pad_stub", 38.5, 16.65, 5, 0], ["CPN_A_pad_stub", 38.5, 16.75, 5, 1],
    ["CPN_A_pad_stub", 38.5, 18.2, 3.45, 0], ["CPN_A_pad_stub", 38.5, 18.2, 3.55, 1], ["CPN_A_pad_stub", 53, 15, 1, 0],
    ["CPN_A_pad_stub", 53, 15, 5, 0], ["CPN_A_pad_stub", 53, 16.75, 5, 1], ["CPN_A_pad_stub", 53, 18.3, 1, 1],
    ["CPN_A_pad_stub", 30, 35, 3, 1],
    // B frame: shelves X 0..14 / 216..230 to Z 14, base Z 4, inserts r 2 from Z 8 at (7|223, 10|80)
    ["CPN_B_supports", 13.95, 45, 10, 1], ["CPN_B_supports", 14.05, 45, 10, 0], ["CPN_B_supports", 215.95, 45, 10, 0],
    ["CPN_B_supports", 216.05, 45, 10, 1], ["CPN_B_supports", 115, 45, 3.95, 1], ["CPN_B_supports", 115, 45, 4.05, 0],
    ["CPN_B_supports", 7, 45, 13.95, 1], ["CPN_B_supports", 7, 10, 12, 0], ["CPN_B_supports", 7, 10, 8.05, 0],
    ["CPN_B_supports", 7, 10, 7.95, 1], ["CPN_B_supports", 7, 80, 12, 0], ["CPN_B_supports", 223, 10, 12, 0],
    ["CPN_B_supports", 223, 80, 12, 0], ["CPN_B_supports", 223, 80, 7.95, 1], ["CPN_B_supports", 9.05, 10, 12, 1],
    ["CPN_B_supports", 8.95, 10, 12, 0],
    // B1: plate 2.5, clearance holes r 1.7 at the four screw positions
    ["CPN_B1_plate", 115, 45, 1.25, 1], ["CPN_B1_plate", 7, 10, 1.25, 0], ["CPN_B1_plate", 7, 80, 1.25, 0],
    ["CPN_B1_plate", 223, 10, 1.25, 0], ["CPN_B1_plate", 223, 80, 1.25, 0], ["CPN_B1_plate", 8.65, 10, 1.25, 0],
    ["CPN_B1_plate", 8.75, 10, 1.25, 1]
];

// B2 probes for each dialog rib height: rib tops, rib thickness 2, rib ends at the support edges
// (transverse rib X 13..15 / 215..217), mid-span transverse rib, rib-free screw bands, fused skin.
function cpnRibProbes(d is map) returns array
{
    var out = [];
    for (var h in [d.ribHeight1, d.ribHeight2, d.ribHeight3])
    {
        const n = cpnRibPlateName(h);
        const zt = 2.5 + h / millimeter;
        const zm = 2.5 + h / millimeter / 2;
        out = concatenateArrays([out, [[n, 115, 45, zt - 0.05, 1], [n, 60, 46.05, zm, 0], [n, 60, 45.95, zm, 1],
                [n, 60, 43.95, zm, 0], [n, 60, 15, zm, 1], [n, 60, 75, zm, 1], [n, 60, 30, zm, 0], [n, 13.05, 45, zm, 1],
                [n, 12.95, 45, zm, 0], [n, 216.95, 45, zm, 1], [n, 217.05, 45, zm, 0], [n, 115, 5, zm, 1], [n, 60, 5, zm, 0],
                [n, 13.5, 5, zm, 1], [n, 7, 10, 1.25, 0], [n, 7, 10, zm, 0], [n, 223, 80, zm, 0], [n, 115, 45, 1.25, 1],
                [n, 60, 30, 2.45, 1], [n, 60, 30, 2.55, 0]]]);
    }
    return out;
}

function cpnClash(context is Context, a is Query, b is Query) returns boolean
{
    for (var c in evCollision(context, { "tools" : a, "targets" : b }))
    {
        const t = c["type"] != undefined ? c["type"] : c["clashType"];
        if (t == ClashType.INTERFERE || t == ClashType.TARGET_IN_TOOL || t == ClashType.TOOL_IN_TARGET)
            return true;
    }
    return false;
}

function cpnDist(context is Context, a is Query, b is Query) returns number
{
    return evDistance(context, { "side0" : a, "side1" : b }).distance / millimeter;
}

function cpnNear(a is number, b is number) returns boolean
{
    return abs(a - b) < 1e-4;
}

// Moves a body so its tight bounding-box min corner lands on p (mm).
function cpnMoveTo(context is Context, id is Id, q is Query, p is array)
{
    const b = evBox3d(context, { "topology" : q, "tight" : true });
    opTransform(context, id, { "bodies" : q, "transform" : transform(vector(p[0], p[1], p[2]) * millimeter - b.minCorner) });
}

// Point probe: a 0.02 mm cube at p; solid if it collides with the body.
function cpnProbeAll(context is Context, id is Id, parts is map, probes is array, tag is string, st is map) returns map
{
    var s = st;
    const h = 0.01 * millimeter;
    for (var n = 0; n < size(probes); n += 1)
    {
        const p = probes[n];
        const c = vector(p[1], p[2], p[3]) * millimeter;
        fCuboid(context, id + (tag ~ n), { "corner1" : c - vector(h, h, h), "corner2" : c + vector(h, h, h) });
        const hit = cpnClash(context, qCreatedBy(id + (tag ~ n), EntityType.BODY), parts[p[0]]);
        s.total = s.total + 1;
        if (hit == (p[4] == 1))
            s.pass = s.pass + 1;
        else
            s.fails = append(s.fails, tag ~ n);
    }
    return s;
}

function cpnAssert(st is map, ok is boolean, code is string) returns map
{
    var s = st;
    s.atotal = s.atotal + 1;
    if (ok)
        s.apass = s.apass + 1;
    else
        s.fails = append(s.fails, code);
    return s;
}

function cpnS(v is number) returns string
{
    return toString(roundToPrecision(v, 4));
}

annotation { "Feature Type Name" : "CPN Check" }
export const cpnCheck = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const d = { "ribHeight1" : 6 * millimeter, "ribHeight2" : 8 * millimeter, "ribHeight3" : 11 * millimeter,
                "insertDiameter" : 4 * millimeter, "insertDepth" : 6 * millimeter };
        var st = { "pass" : 0, "total" : 0, "apass" : 0, "atotal" : 0, "fails" : [] };

        // ---- 1. production build, laid out (the body of the P0.1 Coupons feature; the payload may define
        //         only one feature, so the feature wrapper itself is compile-checked by put_featurescript) ----
        cpnBuildAll(context, id + "prod", d, true);
        const allProd = evaluateQuery(context, qCreatedBy(id + "prod", EntityType.BODY));
        var byName = {};
        for (var b in allProd)
        {
            const nm = getProperty(context, { "entity" : b, "propertyType" : PropertyType.NAME });
            byName[nm] = byName[nm] == undefined ? [b] : append(byName[nm], b);
        }
        var nNm = 0;
        var nBb = 0;
        var nZ = 0;
        var volDev = 0;
        var prodList = [];
        for (var k = 0; k < size(CPN_EXPECT); k += 1)
        {
            const e = CPN_EXPECT[k];
            const lst = byName[e[0]];
            if (lst != undefined && size(lst) == 1)
            {
                nNm += 1;
                const q = lst[0];
                prodList = append(prodList, q);
                const bx = evBox3d(context, { "topology" : q, "tight" : true });
                const sz = (bx.maxCorner - bx.minCorner) / millimeter;
                if (cpnNear(sz[0], e[1]) && cpnNear(sz[1], e[2]) && cpnNear(sz[2], e[3]))
                    nBb += 1;
                else
                    st.fails = append(st.fails, "bb" ~ k);
                if (cpnNear(bx.minCorner[2] / millimeter, 0) && size(evaluateQuery(context, qBodyType(q, BodyType.SOLID))) == 1)
                    nZ += 1;
                const v = evVolume(context, { "entities" : q }) / (millimeter ^ 3);
                volDev = max(volDev, abs(v - e[4]) / e[4]);
            }
            else
                st.fails = append(st.fails, "nm" ~ k);
        }
        var ov = 0;
        var ab = 0;
        for (var i = 0; i < size(prodList); i += 1)
        {
            for (var j = i + 1; j < size(prodList); j += 1)
            {
                for (var c in evCollision(context, { "tools" : prodList[i], "targets" : prodList[j] }))
                {
                    const t = c["type"] != undefined ? c["type"] : c["clashType"];
                    if (t == ClashType.INTERFERE || t == ClashType.TARGET_IN_TOOL || t == ClashType.TOOL_IN_TARGET)
                        ov += 1;
                    else if (t != ClashType.NONE)
                        ab += 1;
                }
            }
        }

        // ---- 2. point probes on an un-laid-out set ----
        const raw = cpnBuildAll(context, id + "raw", d, false);
        st = cpnProbeAll(context, id + "pa", raw, CPN_PROBES, "p", st);
        st = cpnProbeAll(context, id + "pb", raw, cpnRibProbes(d), "r", st);

        // ---- 3. rigs ----
        const A1 = raw["CPN_A1_rail"];
        const A2 = raw["CPN_A2_rail_stiffener_slots"];
        const PAD = raw["CPN_A_pad_stub"];
        const SUR = raw["CPN_A_display_surrogate"];
        const CAR = raw["CPN_A_carriage_load_post"];
        // Coupon A: stub on the table; rail X 0 at stub X 31.5, ear inserts over the stub holes; rail on top.
        cpnMoveTo(context, id + "m1", A1, [31.5, 9, 6]);
        st = cpnAssert(st, !cpnClash(context, A1, PAD) && cpnNear(cpnDist(context, A1, PAD), 0), "a1seat");
        st = cpnProbeAll(context, id + "pc", raw, [["CPN_A1_rail", 38.5, 15, 9, 0], ["CPN_A1_rail", 53, 15, 9, 0],
                    ["CPN_A1_rail", 59.95, 15, 12, 1], ["CPN_A1_rail", 60.05, 15, 12, 0]], "q", st);
        cpnMoveTo(context, id + "m2", SUR, [61.5, 19.8, 0]);
        const dRS = cpnDist(context, A1, SUR);
        st = cpnAssert(st, cpnNear(dRS, 1) && !cpnClash(context, SUR, PAD) && !cpnClash(context, SUR, A1), "gapA");
        // carriage stowed: on the floor, centred in Y, against the end stop
        const c0 = [31.5 + 158, 9 + 12 + 2.5 + 0.3, 6 + 2.5];
        cpnMoveTo(context, id + "m3", CAR, c0);
        st = cpnAssert(st, !cpnClash(context, CAR, A1) && cpnNear(cpnDist(context, CAR, A1), 0), "stow");
        const cb = evBox3d(context, { "topology" : CAR, "tight" : true });
        const pb = evBox3d(context, { "topology" : PAD, "tight" : true });
        const arm = ((cb.minCorner[0] + cb.maxCorner[0]) / 2 - pb.maxCorner[0]) / millimeter;
        st = cpnAssert(st, cpnNear(arm, 149.5), "arm");
        const eng = ((cb.maxCorner[1] - cb.minCorner[1]) - CPN_SLOT_W) / 2 / millimeter;
        // centred in the channel, 1 mm off the stop: every clearance 0.3 (Y per side, Z each way), post 0.5
        cpnMoveTo(context, id + "m4", CAR, [c0[0] - 1, c0[1], c0[2] + 0.3]);
        const dC = cpnDist(context, CAR, A1);
        st = cpnAssert(st, cpnNear(dC, 0.3), "ctr");
        // pushed to the +Y wall and up against the lips: touches, no interference
        cpnMoveTo(context, id + "m5", CAR, [c0[0] - 1, c0[1] + 0.3, c0[2] + 0.6]);
        st = cpnAssert(st, !cpnClash(context, CAR, A1) && cpnNear(cpnDist(context, CAR, A1), 0), "extreme");
        // 0.05 further up must hit the lips (retention)
        cpnMoveTo(context, id + "m6", CAR, [c0[0] - 1, c0[1] + 0.3, c0[2] + 0.65]);
        st = cpnAssert(st, cpnClash(context, CAR, A1), "lipRet");
        // A2 (at its origin): stowed and centred
        cpnMoveTo(context, id + "m7", CAR, [158, 16.4, 2.5]);
        st = cpnAssert(st, !cpnClash(context, CAR, A2) && cpnNear(cpnDist(context, CAR, A2), 0), "a2stow");
        cpnMoveTo(context, id + "m8", CAR, [157, 16.4, 2.8]);
        st = cpnAssert(st, cpnNear(cpnDist(context, CAR, A2), 0.3), "a2ctr");

        // Coupon B: plate on the shelves, clearance block centred on the base, load pad at plate centre.
        const FR = raw["CPN_B_supports"];
        const B1 = raw["CPN_B1_plate"];
        const BLK = raw["CPN_B_clearance_block"];
        const LP = raw["CPN_B_load_pad"];
        cpnMoveTo(context, id + "m9", B1, [0, 0, 14]);
        cpnMoveTo(context, id + "m10", BLK, [85, 15, 4]);
        st = cpnAssert(st, !cpnClash(context, B1, FR) && cpnNear(cpnDist(context, B1, FR), 0), "b1seat");
        st = cpnAssert(st, !cpnClash(context, BLK, FR) && cpnNear(cpnDist(context, BLK, FR), 0), "blkseat");
        const dBP = cpnDist(context, BLK, B1);
        st = cpnAssert(st, cpnNear(dBP, 1), "gapB1");
        st = cpnProbeAll(context, id + "pd", raw, [["CPN_B1_plate", 7, 10, 15.25, 0], ["CPN_B1_plate", 7, 80, 15.25, 0],
                    ["CPN_B1_plate", 223, 10, 15.25, 0], ["CPN_B1_plate", 223, 80, 15.25, 0]], "s", st);
        cpnMoveTo(context, id + "m11", LP, [105, 35, 16.5]);
        st = cpnAssert(st, !cpnClash(context, LP, B1) && cpnNear(cpnDist(context, LP, B1), 0), "lpad");
        const b2 = [cpnRibPlateName(d.ribHeight1), cpnRibPlateName(d.ribHeight2), cpnRibPlateName(d.ribHeight3)];
        for (var i = 0; i < size(b2); i += 1)
        {
            const P = raw[b2[i]];
            cpnMoveTo(context, id + ("mb" ~ i), P, [0, 0, 14]);
            st = cpnAssert(st, !cpnClash(context, P, FR) && cpnNear(cpnDist(context, P, FR), 0)
                        && !cpnClash(context, P, BLK) && cpnNear(cpnDist(context, P, BLK), 1), "b2seat" ~ i);
        }

        var msg = "CPN n" ~ size(allProd) ~ " nm" ~ nNm ~ " bb" ~ nBb ~ " z" ~ nZ ~ " v" ~ cpnS(volDev * 100) ~ "% ov" ~ ov
            ~ " ab" ~ ab ~ " P" ~ st.pass ~ "/" ~ st.total ~ " A" ~ st.apass ~ "/" ~ st.atotal ~ " dRS" ~ cpnS(dRS)
            ~ " dC" ~ cpnS(dC) ~ " dBP" ~ cpnS(dBP) ~ " arm" ~ cpnS(arm) ~ " eng" ~ cpnS(eng) ~ " F:";
        for (var k = 0; k < min(size(st.fails), 10); k += 1)
            msg = msg ~ " " ~ st.fails[k];
        throw regenError(msg);
    }, {});
