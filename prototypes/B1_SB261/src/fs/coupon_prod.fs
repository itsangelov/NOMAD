const ANG_B = { (degree) : [-360, 0, 360], (radian) : 0 } as AngleBoundSpec;

function nm(context is Context, q is Query, s is string)
{
    setProperty(context, { "entities" : q, "propertyType" : PropertyType.NAME, "value" : s });
}

annotation { "Feature Type Name" : "B1HingeCoupon" }
export const b1HingeCoupon = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Leaf angle psi (0 = closed)" }
        isAngle(definition.psi, ANG_B);
        annotation { "Name" : "Lid / rig angle phi (90 = lid back vertical, torque test)" }
        isAngle(definition.phi, ANG_B);
        annotation { "Name" : "Running gap leaf block to fixed band" }
        isLength(definition.gap, NONNEGATIVE_LENGTH_BOUNDS);
        annotation { "Name" : "Lid insert hole dia (M3, Ruthex RX-M3x5.7)" }
        isLength(definition.lidHole, NONNEGATIVE_LENGTH_BOUNDS);
        annotation { "Name" : "Leaf insert hole dia (M2.5x4, OD 3.55)" }
        isLength(definition.leafHole, NONNEGATIVE_LENGTH_BOUNDS);
        annotation { "Name" : "Leaf insert hole depth from flag face" }
        isLength(definition.leafDepth, NONNEGATIVE_LENGTH_BOUNDS);
        annotation { "Name" : "Print layout (both parts on the bed, no hardware)" }
        definition.printLayout is boolean;
        annotation { "Name" : "Show SB-261 hinge + screws + inserts" }
        definition.hw is boolean;
    }
    {
        const pl = definition.printLayout;
        const q = buildCoupon(context, id, definition.gap / millimeter, definition.leafHole / millimeter, definition.leafDepth / millimeter,
            definition.lidHole / millimeter, definition.hw && !pl);
        nm(context, q.Lc, "COUPON-LID (print PETG)");
        nm(context, q.Fc, "COUPON-LEAF (print PETG)");
        if (definition.hw && !pl)
        {
            nm(context, q.Lh, "SB-261-6 shaft / C-ring / band FIXED (purchased)");
            nm(context, q.Lw, "M3x8 ISO7380 + Ruthex RX-M3x5.7 (recessed 1 mm)");
            nm(context, q.Fb, "SB-261-6 band ROTATING (purchased)");
            nm(context, q.Fw, "M2.5x5 ISO7380 + DIN433 + M2.5x4 OD3.55 insert");
        }
        if (pl)
        {
            opTransform(context, id + "pL", { "bodies" : q.Lc, "transform" : transform(V(0, 0, -47)) });
            opTransform(context, id + "pF", { "bodies" : q.Fc,
                        "transform" : transform(V(60, 0, 73)) * rotationAround(line(V(0, 0, 0), vector(0, 1, 0)), 180 * degree) });
        }
        else
        {
            if (abs(definition.psi / degree) > 1e-9)
            {
                opTransform(context, id + "psi", { "bodies" : q.Fall, "transform" : rotationAround(leafAxis(), definition.psi) });
            }
            if (abs(definition.phi / degree) > 1e-9)
            {
                opTransform(context, id + "phi", { "bodies" : qUnion([q.Lall, q.Fall]), "transform" : rotationAround(leafAxis(), -definition.phi) });
            }
        }
        reportFeatureInfo(context, id, "Coupon: gap " ~ definition.gap / millimeter ~ " mm, lid hole " ~ definition.lidHole / millimeter ~
                ", leaf hole " ~ definition.leafHole / millimeter ~ " x " ~ definition.leafDepth / millimeter ~ ". Lever holes at 50/75/100 mm from the hinge axis.");
    }, { "psi" : 0 * degree, "phi" : 0 * degree, "gap" : 0.5 * millimeter, "lidHole" : 4.0 * millimeter, "leafHole" : 3.1 * millimeter,
        "leafDepth" : 4.5 * millimeter, "printLayout" : false, "hw" : true });
