// NOMAD V1 visual model - kernel QA harness (test_feature payload part; NOT a Feature Studio on its own).
// Payload = CAD/featurescript/NOMAD_V1_Visual.onshape.fs with "export const nomadV1Visual" -> "const nomadV1Visual",
// followed by this file (py CAD/tools/fs_compact.py on it first). ~9 Onshape API requests per run. Output: the
// response "console" (println; the harness must NOT throw): per pose body count / unnamed / leaf lowest z / lid-core
// to base / leaf to base / leaf to lid core; multi-body parts; cut volumes vs a "+"-only rebuild; cable bends present;
// pairwise overlaps (closed pose). Results 2026-10-08: docs/V1-VISUAL-MODEL.md "Onshape QA".


function qaR(v is number) returns string
{
    return toString(roundToPrecision(v, 2));
}

function qaVol(context is Context, q is Query) returns number
{
    return evVolume(context, { "entities" : q }) / millimeter ^ 3;
}

function qaOverlap(context is Context, a is Query, b is Query) returns boolean
{
    for (var c in evCollision(context, { "tools" : a, "targets" : b }))
    {
        const t = c["type"] != undefined ? c["type"] : c["clashType"];
        if (t == ClashType.INTERFERE || t == ClashType.TARGET_IN_TOOL || t == ClashType.TOOL_IN_TARGET)
        {
            return true;
        }
    }
    return false;
}

annotation { "Feature Type Name" : "V1 QA" }
export const v1QA = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const poses = [V1Pose.POSE_CLOSED, V1Pose.POSE_OPEN, V1Pose.POSE_LEAF90, V1Pose.POSE_LEAF120, V1Pose.POSE_LEAF180,
                V1Pose.POSE_LEAF190, V1Pose.POSE_LIDMAX, V1Pose.POSE_TABLELIMIT, V1Pose.POSE_SERVICE, V1Pose.POSE_CUSTOM];
        var out = "P";
        for (var k = 0; k < size(poses); k += 1)
        {
            const d = { "pose" : poses[k], "lidAngle" : 60 * degree, "leafAngle" : 45 * degree, "stay" : true, "explodeCustom" : false,
                    "showCables" : true, "showKeepouts" : true, "showAirflow" : true, "showTable" : true, "xray" : true,
                    "statusColors" : true, "check" : true };
            const vid = id + ("v" ~ k);
            nomadV1Visual(context, vid, d);
            const allB = evaluateQuery(context, qCreatedBy(vid, EntityType.BODY));
            const solids = evaluateQuery(context, qBodyType(qCreatedBy(vid, EntityType.BODY), BodyType.SOLID));
            var unnamed = 0;
            for (var b in allB)
            {
                const nm = getProperty(context, { "entity" : b, "propertyType" : PropertyType.NAME });
                if (indexOf(nm, "V1 |") != 0)
                {
                    unnamed += 1;
                }
            }
            const leafQ = qCreatedBy(vid + "B1" + "F", EntityType.BODY);
            const lcQ = qCreatedBy(vid + "B1" + "L" + "c", EntityType.BODY);
            const shQ = qCreatedBy(vid + "p0", EntityType.BODY);
            const zmin = evBox3d(context, { "topology" : leafQ, "tight" : true }).minCorner[2] / millimeter;
            out = out ~ " " ~ k ~ ":" ~ size(allB) ~ "/" ~ size(solids) ~ "u" ~ unnamed ~ " z" ~ qaR(zmin);
            if (k != 8)
            {
                out = out ~ " lb" ~ qaR(dmm(context, lcQ, shQ)) ~ " fb" ~ qaR(dmm(context, leafQ, shQ)) ~ " fl" ~ qaR(dmm(context, qCreatedBy(vid + "B1" + "F" + "s", EntityType.BODY), lcQ));
            }
            out = out ~ ";";
            opDeleteBodies(context, id + ("del" ~ k), { "entities" : qCreatedBy(vid, EntityType.BODY) });
        }
        println(out);

        // ---- closed pose, detailed ----
        const cd = { "pose" : V1Pose.POSE_CLOSED, "lidAngle" : 0 * degree, "leafAngle" : 0 * degree, "stay" : false, "explodeCustom" : false,
                "showCables" : true, "showKeepouts" : false, "showAirflow" : false, "showTable" : false, "xray" : false,
                "statusColors" : false, "check" : false };
        const cid = id + "c";
        nomadV1Visual(context, cid, cd);
        var multi = "M";
        var groups = [];
        var gnames = [];
        for (var i = 0; i < size(V1_PARTS); i += 1)
        {
            const p = V1_PARTS[i];
            const pq = qCreatedBy(cid + ("p" ~ i), EntityType.BODY);
            const n = size(evaluateQuery(context, pq));
            if (n == 0)
            {
                continue;
            }
            groups = append(groups, pq);
            gnames = append(gnames, p[0]);
            if (n != 1)
            {
                multi = multi ~ " " ~ p[0] ~ "=" ~ n;
            }
        }
        const b1keys = ["Lc", "Lh", "Lw", "Ls", "Lk", "Fs", "Fb", "Fw", "Fk"];
        const b1ids = [["L", "c"], ["L", "h"], ["L", "w"], ["L", "s"], ["L", "k"], ["F", "s"], ["F", "b"], ["F", "w"], ["F", "k"]];
        for (var j = 0; j < size(b1keys); j += 1)
        {
            const bqq = qCreatedBy(cid + "B1" + b1ids[j][0] + b1ids[j][1], EntityType.BODY);
            groups = append(groups, bqq);
            gnames = append(gnames, "B1" ~ b1keys[j]);
            multi = multi ~ " B1" ~ b1keys[j] ~ "=" ~ size(evaluateQuery(context, bqq));
        }
        for (var i = 0; i < size(V1_ROUTES); i += 1)
        {
            groups = append(groups, qCreatedBy(cid + ("cab" ~ i), EntityType.BODY));
            gnames = append(gnames, "cab" ~ i);
        }
        println(multi);

        // cuts actually applied? compare with a "+"-only rebuild
        var cutm = "C";
        for (var i = 0; i < size(V1_PARTS); i += 1)
        {
            const p = V1_PARTS[i];
            var plusSt = [];
            var hasMinus = false;
            for (var st in p[6])
            {
                if (st[0] == "+")
                {
                    plusSt = append(plusSt, st);
                }
                else
                {
                    hasMinus = true;
                }
            }
            if (!hasMinus)
            {
                continue;
            }
            const pp = [p[0], p[1], p[2], p[3], p[4], p[5], plusSt];
            const rq = v1BuildPart(context, id + ("r" ~ i), pp).q;
            const v0 = qaVol(context, rq);
            const v1 = qaVol(context, qCreatedBy(cid + ("p" ~ i), EntityType.BODY));
            cutm = cutm ~ " " ~ p[0] ~ ":" ~ qaR(v0 - v1);
            opDeleteBodies(context, id + ("rd" ~ i), { "entities" : rq });
        }
        // lid cuts
        lidCore(context, id + "lcref");
        cutm = cutm ~ " lid:" ~ qaR(qaVol(context, qCreatedBy(id + "lcref", EntityType.BODY)) - qaVol(context, qCreatedBy(cid + "B1" + "L" + "c", EntityType.BODY)));
        opDeleteBodies(context, id + "lcdel", { "entities" : qCreatedBy(id + "lcref", EntityType.BODY) });
        println(cutm);

        // cable bends present?
        var bend = "B";
        for (var i = 0; i < size(V1_ROUTES); i += 1)
        {
            const r = V1_ROUTES[i];
            const n = size(r[5]);
            var miss = 0;
            var nexp = 0;
            for (var j = 1; j < n - 1; j += 1)
            {
                const a0 = v1V(r[5][j - 1][1], r[5][j - 1][2], r[5][j - 1][3]);
                const a1 = v1V(r[5][j][1], r[5][j][2], r[5][j][3]);
                const a2 = v1V(r[5][j + 1][1], r[5][j + 1][2], r[5][j + 1][3]);
                const th = angleBetween(normalize(a1 - a0), normalize(a2 - a1));
                if (th < 0.5 * degree)
                {
                    continue;
                }
                nexp += 1;
                if (size(evaluateQuery(context, qCreatedBy(cid + ("cab" ~ i) + ("a" ~ j), EntityType.BODY))) != 1)
                {
                    miss += 1;
                }
            }
            bend = bend ~ " " ~ i ~ ":" ~ (nexp - miss) ~ "/" ~ nexp;
        }
        println(bend);

        // pairwise overlaps (closed pose, solids + cables)
        var ov = "O";
        var nov = 0;
        for (var i = 0; i < size(groups) - 1; i += 1)
        {
            if (!qaOverlap(context, groups[i], qUnion(subArray(groups, i + 1, size(groups)))))
            {
                continue;
            }
            for (var j = i + 1; j < size(groups); j += 1)
            {
                if (qaOverlap(context, groups[i], groups[j]))
                {
                    ov = ov ~ " " ~ gnames[i] ~ "-" ~ gnames[j];
                    nov += 1;
                }
            }
        }
        println(ov);
        println("n" ~ nov);
    });
