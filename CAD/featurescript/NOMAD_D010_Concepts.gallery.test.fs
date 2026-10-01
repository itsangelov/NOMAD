// NOMAD D010 Concepts — scratch GALLERY regression harness (wordmark repair, 2026-09-29). Appended to
// NOMAD_D010_Concepts.fs + NOMAD_D010_Concepts.test.fs for test_feature only; NEVER written to Onshape.
// Rebuilds the 12 gallery instances exactly as the GALLERY layout does (same poses, offsets, labels and options),
// with the wordmark ON or OFF (D010_SWEEP_WM, set by the payload builder), and reports through a deliberate regenError.
// ON: wordmark / pad / foil-window / lid sanity and the minimum clearance from the wordmark + pad to every other
// B1 part over the 6 B1 states. OFF: body counts for the pre-wordmark regression, plus the D010 Check results.

function d010ErrText(err) returns string
{
    if (err is map && err.message != undefined)
        return "" ~ err.message;
    return "" ~ err;
}

function d010MinD(context is Context, a is Query, b is Query, cur) returns map
{
    if (size(evaluateQuery(context, a)) == 0 || size(evaluateQuery(context, b)) == 0)
        return cur;
    const r = evDistance(context, { "side0" : a, "side1" : b });
    const d = r.distance / millimeter;
    if (cur.d != undefined && cur.d <= d)
        return cur;
    return { "d" : d, "i" : r.sides[1].index };
}

function d010GalleryMsg(context is Context, id is Id, wm is boolean) returns string
{
    var fails = "";
    var okA = 0;
    var okB = 0;
    var bp = makeArray(6, undefined);
    for (var k = 0; k < 6; k += 1)
    {
        const ea = D010_STATES_A[k];
        const eb = D010_STATES_B1[k];
        const o = { "cables" : true, "cg" : true, "env" : k == 3, "internals" : k == 0, "wm" : wm };
        try
        {
            d010Instance(context, id + ("a" ~ k), "A", d010StatePose(ea), vector(k * D010_GALLERY_DX, 0, 0) * millimeter,
                (k + 1) ~ " " ~ ea[0], ea[8], o);
            okA += 1;
        }
        catch (err)
        {
            fails = fails ~ " A" ~ (k + 1) ~ ":" ~ d010ErrText(err);
        }
        try
        {
            bp[k] = d010Instance(context, id + ("b" ~ k), "B1", d010StatePose(eb), vector(k * D010_GALLERY_DX, D010_GALLERY_DY, 0) * millimeter,
                (k + 1) ~ " " ~ eb[0], eb[8], o);
            okB += 1;
        }
        catch (err)
        {
            fails = fails ~ " B" ~ (k + 1) ~ ":" ~ d010ErrText(err);
        }
    }
    var nA = 0;
    var nB = 0;
    for (var k = 0; k < 6; k += 1)
    {
        nA += size(evaluateQuery(context, qCreatedBy(id + ("a" ~ k), EntityType.BODY)));
        nB += size(evaluateQuery(context, qCreatedBy(id + ("b" ~ k), EntityType.BODY)));
    }
    var msg = "GAL wm=" ~ wm ~ " ok A" ~ okA ~ " B" ~ okB ~ " bodies A" ~ nA ~ " B" ~ nB ~ " fail:" ~ (fails == "" ? "none" : fails);
    if (bp[0] != undefined && wm)
        msg = msg ~ " lidV0 " ~ roundToPrecision(evVolume(context, { "entities" : bp[0]["lidShell"] }) / millimeter ^ 3, 0);
    if (!wm)
    {
        // locate cable contacts with the leaf hinges / leaf frame in STOWED (closed frame; instance offset y -800 removed)
        if (bp[0] != undefined)
        {
            const b = id + "b0";
            const cab = qCreatedBy(b + "cB", EntityType.BODY);
            const hng = qUnion([qCreatedBy(b + "B" + "hbar0", EntityType.BODY), qCreatedBy(b + "B" + "hbar1", EntityType.BODY),
                    qCreatedBy(b + "B" + "hleaf0", EntityType.BODY), qCreatedBy(b + "B" + "hleaf1", EntityType.BODY)]);
            const lf = qUnion([qCreatedBy(b + "B" + "frame0", EntityType.BODY), qCreatedBy(b + "B" + "frame1", EntityType.BODY)]);
            for (var t in [["hitH", hng], ["hitL", lf]])
            {
                const r = evDistance(context, { "side0" : cab, "side1" : t[1] });
                const q = r.sides[0].point / millimeter;
                msg = msg ~ " " ~ t[0] ~ " " ~ roundToPrecision(r.distance / millimeter, 2) ~ "@" ~ roundToPrecision(q[0], 0) ~ "," ~
                    roundToPrecision(q[1] + 800, 0) ~ "," ~ roundToPrecision(q[2], 0);
            }
        }
        return msg;
    }

    // ---- wordmark sanity over the 6 B1 states ----
    var nWm = "";
    var nPad = 0;
    var nLid = 0;
    var foilF = "";
    const ks = ["hng", "dh", "sty", "cab", "knk", "leaf", "ctl", "any"];
    var best = {};
    var cabD = {};
    var worstAnyName = "";
    for (var k = 0; k < 6; k += 1)
    {
        if (bp[k] == undefined)
            continue;
        const p = bp[k];
        const b = id + ("b" ~ k);
        nWm = nWm ~ size(evaluateQuery(context, p["wm"]));
        nPad += size(evaluateQuery(context, p["wmPad"]));
        nLid += size(evaluateQuery(context, p["lidShell"]));
        foilF = foilF ~ size(evaluateQuery(context, qOwnedByBody(qCreatedBy(b + "B" + "foil", EntityType.BODY), EntityType.FACE))) ~ (k < 5 ? "," : "");
        const w = qUnion([p["wm"], p["wmPad"]]);
        const sets = {
                "hng" : qUnion([qCreatedBy(b + "B" + "hbar0", EntityType.BODY), qCreatedBy(b + "B" + "hbar1", EntityType.BODY),
                        qCreatedBy(b + "B" + "hleaf0", EntityType.BODY), qCreatedBy(b + "B" + "hleaf1", EntityType.BODY)]),
                "dh" : qCreatedBy(b + "hingeBarrel", EntityType.BODY),
                "sty" : qCreatedBy(b + "stay", EntityType.BODY),
                "cab" : qCreatedBy(b + "cB", EntityType.BODY),
                "knk" : qUnion([qCreatedBy(b + "B" + "knuckle", EntityType.BODY), qCreatedBy(b + "B" + "idler", EntityType.BODY)]),
                "leaf" : qUnion([qCreatedBy(b + "B" + "frame0", EntityType.BODY), qCreatedBy(b + "B" + "frame1", EntityType.BODY),
                        qCreatedBy(b + "B" + "pv", EntityType.BODY), qCreatedBy(b + "B" + "splice", EntityType.BODY),
                        qCreatedBy(b + "B" + "latchLeaf", EntityType.BODY), qCreatedBy(b + "B" + "conn", EntityType.BODY)]),
                "ctl" : qCreatedBy(b + "ctl", EntityType.BODY)
            };
        for (var kk in ks)
        {
            if (kk == "any")
                continue;
            best[kk] = d010MinD(context, w, sets[kk], best[kk] == undefined ? {} : best[kk]);
        }
        // everything else in the instance except the wordmark, its pad and the lid shell it is cut into (designed contact)
        // cable vs leaf hinges / leaf (frames, PV, splice, latch; the panel connector is the cable's own end) / stay
        const cab = qCreatedBy(b + "cB", EntityType.BODY);
        const leafNoConn = qUnion([qCreatedBy(b + "B" + "frame0", EntityType.BODY), qCreatedBy(b + "B" + "frame1", EntityType.BODY),
                qCreatedBy(b + "B" + "pv", EntityType.BODY), qCreatedBy(b + "B" + "splice", EntityType.BODY),
                qCreatedBy(b + "B" + "latchLeaf", EntityType.BODY)]);
        cabD["h"] = d010MinD(context, cab, sets["hng"], cabD["h"] == undefined ? {} : cabD["h"]);
        cabD["l"] = d010MinD(context, cab, leafNoConn, cabD["l"] == undefined ? {} : cabD["l"]);
        cabD["s"] = d010MinD(context, cab, sets["sty"], cabD["s"] == undefined ? {} : cabD["s"]);
        if (p["ctl"] != undefined)
            cabD["c"] = d010MinD(context, cab, p["ctl"], cabD["c"] == undefined ? {} : cabD["c"]);
        const others = evaluateQuery(context, qSubtraction(qCreatedBy(b, EntityType.BODY), qUnion([w, p["lidShell"]])));
        const prev = best["any"] == undefined ? {} : best["any"];
        const r = d010MinD(context, w, qUnion(others), prev);
        if (r.d != undefined && (prev.d == undefined || r.d < prev.d))
            worstAnyName = getProperty(context, { "entity" : others[r.i], "propertyType" : PropertyType.NAME });
        best["any"] = r;
    }
    msg = msg ~ "|cab";
    for (var kk in ["h", "l", "s", "c"])
        msg = msg ~ " " ~ kk ~ (cabD[kk] == undefined || cabD[kk].d == undefined ? "-" : roundToPrecision(cabD[kk].d, 2));
    msg = msg ~ "|wmN " ~ nWm ~ " pad " ~ nPad ~ " lidN " ~ nLid ~ " foilF " ~ foilF;
    // recess depth, residual skin and text size in the STOWED state (lid frame == world, offset z 0)
    if (bp[0] != undefined)
    {
        const wb = evBox3d(context, { "topology" : bp[0]["wm"] });
        const zc = D010.ZF + D010.B1_CORE;
        const under = evDistance(context, { "side0" : bp[0]["wm"], "side1" : bp[0]["wmPad"] }).distance / millimeter + D010_WM.pad;
        msg = msg ~ " recess " ~ roundToPrecision(zc - wb.minCorner[2] / millimeter, 2) ~ " under " ~ roundToPrecision(under, 2) ~
            " txt " ~ roundToPrecision((wb.maxCorner[0] - wb.minCorner[0]) / millimeter, 1) ~ "x" ~ roundToPrecision((wb.maxCorner[1] - wb.minCorner[1]) / millimeter, 1) ~
            " inlayV " ~ roundToPrecision(evVolume(context, { "entities" : bp[0]["wm"] }) / millimeter ^ 3, 1);
    }
    // letter counters: all sketch regions vs glyph (outer) regions of the same text
    const sk = newSketchOnPlane(context, id + "cnt", { "sketchPlane" : plane(vector(0, 0, -500) * millimeter, vector(0, 0, 1), -D010_X) });
    skText(sk, "t", { "text" : D010_WM.text, "fontName" : D010_WM.font, "firstCorner" : vector(0, 0) * millimeter,
                "secondCorner" : vector(10, D010_WM.height) * millimeter });
    skSolve(sk);
    msg = msg ~ " reg " ~ size(evaluateQuery(context, qSketchRegion(id + "cnt"))) ~ "/" ~
        size(evaluateQuery(context, qSketchRegion(id + "cnt", true)));
    opDeleteBodies(context, id + "cntd", { "entities" : qCreatedBy(id + "cnt") });
    msg = msg ~ "|clr";
    for (var kk in ks)
        msg = msg ~ " " ~ kk ~ (best[kk] == undefined || best[kk].d == undefined ? "-" : roundToPrecision(best[kk].d, 2));
    return msg ~ " near " ~ worstAnyName;
}

annotation { "Feature Type Name" : "D010 Gallery Check" }
export const d010GalleryCheck = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        var msg = d010GalleryMsg(context, id + "g", D010_SWEEP_WM);
        if (!D010_SWEEP_WM)
            msg = msg ~ " || " ~ d010CheckMsg(context, id + "c");
        throw regenError(msg);
    }, {});
