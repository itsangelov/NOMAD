annotation { "Feature Type Name" : "B1 coupon H6" }
export const b1CouponH6 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const q = buildCoupon(context, id, 0.5, 3.1, 4.5, 4.0, true);
        const vl = evVolume(context, { "entities" : q.Lc }) / (centimeter ^ 3);
        const vf = evVolume(context, { "entities" : q.Fc }) / (centimeter ^ 3);
        const cg = evApproximateCentroid(context, { "entities" : q.Fc }) / millimeter;
        const P = id + "P";
        cz(context, P + "li", 11.917, AY + HOLE, FZ0 - 1 - 5.7, FZ0 - 1, 2.3);
        diamond(context, P + "vch", -25, 25, 0, ZB, 9.0);
        pocket(context, P + "vpd", 8.15, 56.9);
        cx(context, P + "vg", -SHAFTH - 2, SHAFTH + 2, AY, AZ, RG);
        cz(context, P + "f40", 4.65, AY + HOLE, FZ1, FZ1 + 4, 2.0);
        cz(context, P + "f35", 4.65, AY + HOLE, FZ1, FZ1 + 4, 1.775);
        bx(context, P + "ve", BANDS[3][0] - 0.5, AY, FZ1, BANDS[3][0] - 0.5 + 1, 17.5, ZP0);
        var r = "n" ~ size(evaluateQuery(context, q.Fc)) ~ "/" ~ size(evaluateQuery(context, q.Lc)) ~ " V lid " ~ f2(vl) ~ " leaf " ~ f2(vf) ~ " cg " ~ f2(cg[1]) ~ "," ~ f2(cg[2]) ~
            " | W pk " ~ f2(dmm(context, bq(P + "li"), bq(P + "vpd"))) ~ " ch " ~ f2(dmm(context, bq(P + "li"), bq(P + "vch"))) ~
            " gr " ~ f2(dmm(context, bq(P + "li"), bq(P + "vg"))) ~ " f40 " ~ f2(dmm(context, bq(P + "f40"), bq(P + "ve"))) ~
            " f355 " ~ f2(dmm(context, bq(P + "f35"), bq(P + "ve"))) ~
            " | gap " ~ f2(dmm(context, q.Fc, q.Lh)) ~ " hdL " ~ f2(dmm(context, q.Lw, q.Fc)) ~ " hdF " ~ f2(dmm(context, q.Fw, q.Lc)) ~ " |";
        opDeleteBodies(context, id + "dp", { "entities" : bq(P) });
        const pl = [["cc", q.Fc, q.Lc], ["ch", q.Fc, q.Lh], ["cw", q.Fc, q.Lw], ["bc", q.Fb, q.Lc], ["bw", q.Fb, q.Lw],
                ["wc", q.Fw, q.Lc], ["wh", q.Fw, q.Lh], ["ww", q.Fw, q.Lw]];
        var mins = makeArray(size(pl), 1e9);
        var prev = 0;
        for (var p in [30, 60, 90, 120, 150, 180, 190])
        {
            opTransform(context, id + ("r" ~ p), { "bodies" : q.Fall, "transform" : rotationAround(leafAxis(), (p - prev) * degree) });
            prev = p;
            r = r ~ " " ~ p ~ ":" ~ f2(dmm(context, q.Fc, q.Lc));
            for (var j = 0; j < size(pl); j += 1)
            {
                const d = dmm(context, pl[j][1], pl[j][2]);
                if (d < mins[j])
                {
                    mins[j] = d;
                }
            }
        }
        r = r ~ " |";
        for (var j = 0; j < size(pl); j += 1)
        {
            r = r ~ " " ~ pl[j][0] ~ f2(mins[j]);
        }
        var hit = -1;
        var htag = "";
        var a = 190;
        while (a < 240 && hit < 0)
        {
            a += 1;
            opTransform(context, id + ("x" ~ a), { "bodies" : q.Fall, "transform" : rotationAround(leafAxis(), 1 * degree) });
            for (var j = 0; j < size(pl); j += 1)
            {
                if (hit < 0 && dmm(context, pl[j][1], pl[j][2]) <= 0.02)
                {
                    hit = a;
                    htag = pl[j][0];
                }
            }
        }
        throw regenError(r ~ " | X" ~ hit ~ htag);
    });
