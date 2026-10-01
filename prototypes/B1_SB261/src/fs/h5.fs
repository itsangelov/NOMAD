annotation { "Feature Type Name" : "B1 H5" }
export const b1H5 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const q = buildAll(context, id, false);
        const pl = pairList(q);
        rotLeaf(context, id + "r190", q, 190);
        var hit = -1;
        var htag = "";
        var s195 = -1;
        var s200 = -1;
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
                    const d = dmm(context, pl[j][1], pl[j][2]);
                    if (tg == "sC" && a == 195)
                    {
                        s195 = d;
                    }
                    if (tg == "sC" && a == 200)
                    {
                        s200 = d;
                    }
                    if (hit < 0 && d <= 0.02)
                    {
                        hit = a;
                        htag = tg;
                    }
                }
            }
        }
        throw regenError("X" ~ hit ~ htag ~ " sC195 " ~ f2(s195) ~ " sC200 " ~ f2(s200));
    });
