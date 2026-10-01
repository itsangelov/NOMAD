annotation { "Feature Type Name" : "B1 H3" }
export const b1H3 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const q = buildAll(context, id, true);
        var rmin = 1e9;
        var rmax = 0;
        var nt = 0;
        for (var f in evaluateQuery(context, qGeometry(qUnion([qCreatedBy(id + "L" + "k", EntityType.FACE), qCreatedBy(id + "F" + "k", EntityType.FACE)]), GeometryType.TORUS)))
        {
            const sd = evSurfaceDefinition(context, { "face" : f });
            rmin = min(rmin, sd.radius / millimeter);
            rmax = max(rmax, sd.radius / millimeter);
            nt += 1;
        }
        var r = "R" ~ nt ~ ":" ~ f2(rmin) ~ "-" ~ f2(rmax);
        var prev = 0;
        for (var p in [90, 120, 180])
        {
            rotLeaf(context, id + ("ra" ~ p), q, p - prev);
            prev = p;
            r = r ~ " A" ~ p ~ ":" ~ f2(dmm(context, q.accL, q.Fall)) ~ "/" ~ f2(dmm(context, q.accF, q.Lall));
        }
        const idS = id + "W";
        bx(context, idS + "base", -W2, 0, 0, W2, DD, 40);
        bx(context, idS + "plug", -W2, DD, 4, W2, DD + 45, 19);
        bx(context, idS + "tab", -400, -400, -54, 400, 900, -4);
        bx(context, idS + "st0", 117, 210, -3.5, 133, 327, -0.5);
        bx(context, idS + "st1", -133, 210, -3.5, -117, 327, -0.5);
        const S = [["B", bq(idS + "base")], ["P", bq(idS + "plug")], ["T", bq(idS + "tab")], ["S", qUnion([bq(idS + "st0"), bq(idS + "st1")])]];
        const hinge = line(V(0, DD, 40), vector(1, 0, 0));
        var ph0 = 0;
        for (var ph in [90, 105, 110, 125])
        {
            opTransform(context, id + ("ph" ~ ph), { "bodies" : bq(idS), "transform" : rotationAround(hinge, (ph - ph0) * degree) });
            ph0 = ph;
            var mins = [1e9, 1e9, 1e9, 1e9];
            var at = [0, 0, 0, 0];
            for (var p in [0, 30, 60, 90, 120, 150, 180, 190])
            {
                if (p != prev)
                {
                    rotLeaf(context, id + ("w" ~ ph ~ "p" ~ p), q, p - prev);
                    prev = p;
                }
                for (var j = 0; j < 4; j += 1)
                {
                    const d = dmm(context, q.Fall, S[j][1]);
                    if (d < mins[j])
                    {
                        mins[j] = d;
                        at[j] = p;
                    }
                }
            }
            r = r ~ " " ~ ph ~ ":";
            for (var j = 0; j < 4; j += 1)
            {
                r = r ~ S[j][0] ~ f2(mins[j]) ~ "@" ~ at[j];
            }
        }
        throw regenError(r);
    });
