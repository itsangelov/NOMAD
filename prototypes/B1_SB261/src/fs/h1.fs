annotation { "Feature Type Name" : "B1 H1" }
export const b1H1 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const q = buildAll(context, id, false);
        var r = "n" ~ size(evaluateQuery(context, q.Lall)) ~ "/" ~ size(evaluateQuery(context, q.Fall)) ~ " ";
        const st = [["pb", q.pan, q.fixBand], ["bm", q.beam, q.fixBand], ["kb", q.blk, q.fixBand], ["kw", q.blk, q.Lw],
                ["hl", q.lidHead, q.Fs], ["hp", q.lidHead, q.pan], ["fh", q.leafHead, q.Lc], ["rg", q.Fb, q.Lc],
                ["ic", q.leafIns, q.pan], ["sb", q.Ls, q.Fs], ["lc", q.Fk, q.Lc], ["kp", q.Lk, q.Fs], ["kd", q.Lk, q.Ld],
                ["sh", q.shaft, q.Fs], ["fd", q.Fall, q.Ld], ["ch", qUnion([q.Lk, q.Ls, q.Fk]), qUnion([q.fixBand, q.Fb])]];
        for (var s in st)
        {
            r = r ~ s[0] ~ f2(dmm(context, s[1], s[2])) ~ " ";
        }
        r = r ~ "|";
        const pl = pairList(q);
        var prev = 0;
        for (var p in [0, 30, 60, 90, 120, 150, 180, 190])
        {
            if (p != prev)
            {
                rotLeaf(context, id + ("rot" ~ p), q, p - prev);
                prev = p;
            }
            const m = pairMin(context, pl, p == 0);
            r = r ~ p ~ ":" ~ f2(m[0]) ~ m[1] ~ " ";
        }
        throw regenError(r);
    });
