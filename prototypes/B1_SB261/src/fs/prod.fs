const ANG_B = { (degree) : [-360, 0, 360], (radian) : 0 } as AngleBoundSpec;

function nm(context is Context, q is Query, s is string)
{
    setProperty(context, { "entities" : q, "propertyType" : PropertyType.NAME, "value" : s });
}

annotation { "Feature Type Name" : "B1HingeValidation" }
export const b1HingeValidation = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Leaf angle psi (0 = stowed on the lid back)" }
        isAngle(definition.psi, ANG_B);
        annotation { "Name" : "Lid angle phi (0 = closed)" }
        isAngle(definition.phi, ANG_B);
        annotation { "Name" : "Show base, plug keep-out, table and stays" }
        definition.surround is boolean;
        annotation { "Name" : "Report clearances at this pose" }
        definition.check is boolean;
    }
    {
        const q = buildAll(context, id, false);
        nm(context, q.Lc, "LID hinge rail + lid core (scratch)");
        nm(context, q.Ld, "ENV display");
        nm(context, q.Lh, "SB-261 shaft / C-ring");
        nm(context, q.fixBand, "SB-261 band FIXED (lid)");
        nm(context, q.Lw, "M3x8 ISO7380 + M3 insert L5.7, recessed 1 mm (lid)");
        nm(context, q.Ls, "Cable sleeve OD7.5/ID5.5 + twist zone");
        nm(context, q.Lk, "Cable lid side R12");
        nm(context, q.Fs, "Leaf frame (scratch)");
        nm(context, q.pan, "PV panel P108 (stock)");
        nm(context, q.blk, "Leaf hinge block");
        nm(context, q.Fb, "SB-261 band ROTATING (leaf)");
        nm(context, q.Fw, "M2.5x5 ISO7380 + DIN433 washer + M2.5 insert L4 (leaf)");
        nm(context, q.Fk, "Cable leaf side R12");
        const psi = definition.psi / degree;
        const phi = definition.phi / degree;
        if (abs(psi) > 1e-9)
        {
            rotLeaf(context, id + "psi", q, psi);
        }
        var msg = "psi " ~ psi ~ " phi " ~ phi ~ ":";
        if (definition.check)
        {
            const pl = pairList(q);
            const m = pairMin(context, pl, abs(psi) < 1e-9);
            msg = msg ~ " leaf-lid structure " ~ (abs(psi) < 1e-9 ? "rest" : f2(dmm(context, q.Fs, q.Lc))) ~ ", min cross pair " ~ f2(m[0]) ~ " (" ~ m[1] ~ ")" ~
                ", leaf-display " ~ f2(dmm(context, q.Fall, q.Ld));
        }
        if (abs(phi) > 1e-9)
        {
            opTransform(context, id + "phi", { "bodies" : qUnion([q.Lall, q.Fall]), "transform" : rotationAround(line(V(0, DD, 40), vector(1, 0, 0)), -phi * degree) });
        }
        if (definition.surround)
        {
            const idS = id + "W";
            bx(context, idS + "base", -W2, 0, 0, W2, DD, 40);
            bx(context, idS + "plug", -W2, DD, 4, W2, DD + 45, 19);
            bx(context, idS + "tab", -260, -120, -14, 260, 420, -4);
            bx(context, idS + "st0", 117, 210, -3.5, 133, 327, -0.5);
            bx(context, idS + "st1", -133, 210, -3.5, -117, 327, -0.5);
            nm(context, bq(idS + "base"), "ENV base");
            nm(context, bq(idS + "plug"), "KEEPOUT rear plug");
            nm(context, bq(idS + "tab"), "ENV table (z -4)");
            nm(context, qUnion([bq(idS + "st0"), bq(idS + "st1")]), "Stay arm (deployed)");
            if (definition.check)
            {
                msg = msg ~ " | base " ~ f2(dmm(context, q.Fall, bq(idS + "base"))) ~ " plug " ~ f2(dmm(context, q.Fall, bq(idS + "plug"))) ~
                    " table " ~ f2(dmm(context, q.Fall, bq(idS + "tab"))) ~ " stay " ~ f2(dmm(context, q.Fall, qUnion([bq(idS + "st0"), bq(idS + "st1")])));
            }
        }
        if (definition.check)
        {
            reportFeatureInfo(context, id, msg);
        }
    }, { "psi" : 100 * degree, "phi" : 0 * degree, "surround" : true, "check" : true });
