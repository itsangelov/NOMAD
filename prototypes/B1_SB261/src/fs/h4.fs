annotation { "Feature Type Name" : "B1 H4" }
export const b1H4 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const q = buildAll(context, id, false);
        var r = "S bm" ~ f2(dmm(context, q.beam, q.fixBand)) ~ " kb" ~ f2(dmm(context, q.blk, q.fixBand)) ~ " cr" ~ f2(dmm(context, q.Fs, q.Lh)) ~ " fh" ~ f2(dmm(context, q.leafHead, q.Lc)) ~ " hl" ~ f2(dmm(context, q.lidHead, q.Fs)) ~ " ic" ~ f2(dmm(context, q.leafIns, q.pan)) ~ " li" ~ f2(dmm(context, q.lidIns, q.Fall)) ~
            " rg" ~ f2(dmm(context, q.Fb, q.Lc)) ~ " lc" ~ f2(dmm(context, q.Fk, q.Lc)) ~ "|";
        const pl = pairList(q);
        var mins = makeArray(size(pl), 1e9);
        var prev = 0;
        for (var p in [0, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 190])
        {
            if (p != prev)
            {
                rotLeaf(context, id + ("rot" ~ p), q, p - prev);
                prev = p;
            }
            var sc = -1;
            for (var j = 0; j < size(pl); j += 1)
            {
                if (p == 0 && pl[j][0] == "sC")
                {
                    continue;
                }
                const d = dmm(context, pl[j][1], pl[j][2]);
                if (pl[j][0] == "sC")
                {
                    sc = d;
                }
                if (p >= 30 && d < mins[j])
                {
                    mins[j] = d;
                }
            }
            if (p == 30 || p == 60 || p == 90 || p == 120 || p == 150 || p == 180 || p == 190)
            {
                r = r ~ p ~ ":" ~ f2(sc) ~ " ";
            }
        }
        r = r ~ "|";
        for (var j = 0; j < size(pl); j += 1)
        {
            r = r ~ pl[j][0] ~ f2(mins[j]) ~ " ";
        }
        var hit = -1;
        var htag = "";
        var a = 190;
        while (a < 240 && hit < 0)
        {
            a += 1;
            rotLeaf(context, id + ("sx" ~ a), q, 1);
            for (var j = 0; j < size(pl); j += 1)
            {
                const tg = pl[j][0];
                if (tg == "sC" || tg == "cC" || tg == "wC" || tg == "bC" || tg == "sK" || tg == "sW" || tg == "sS")
                {
                    if (hit < 0 && dmm(context, pl[j][1], pl[j][2]) <= 0.02)
                    {
                        hit = a;
                        htag = tg;
                    }
                }
            }
        }
        r = r ~ "|X" ~ hit ~ htag;
        throw regenError(r);
    });
