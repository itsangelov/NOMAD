annotation { "Feature Type Name" : "B1 coupon H7" }
export const b1CouponH7 = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        const q = buildCoupon(context, id, 0.5, 3.1, 4.5, 4.0, true);
        var r = "nFc " ~ size(evaluateQuery(context, q.Fc)) ~ " ax " ~ f2(evDistance(context, { "side0" : q.Fc, "side1" : V(0, AY, AZ) }).distance / millimeter);
        for (var nmk in ["sh", "cr0", "cr1", "b0", "b3"])
        {
            r = r ~ " " ~ nmk ~ f2(dmm(context, q.Fc, bq(id + "L" + "h" + nmk)));
        }
        r = r ~ " w" ~ f2(dmm(context, q.Fc, q.Lw)) ~ " pt " ~ f2(evDistance(context, { "side0" : q.Fc, "side1" : V(11.917, 11.95, 62.0) }).distance / millimeter);
        throw regenError(r);
    });
