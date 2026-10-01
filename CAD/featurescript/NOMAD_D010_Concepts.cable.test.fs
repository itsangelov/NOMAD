// NOMAD D010 Concepts — scratch B1 CABLE clearance diagnostic. Appended to NOMAD_D010_Concepts.fs for test_feature
// only; NEVER written to Onshape. Builds the 6 B1 gallery states (wordmark ON, internals ON so the controller exists,
// envelopes OFF) and lists every body that comes within D010_DIAG_MAX mm of the cable, with the nearest cable point.
// Reported through a deliberate regenError (test_feature returns notices only; ~400 characters survive).

const D010_DIAG_MAX = 1.5;

function d010ShortName(context is Context, q is Query) returns string
{
    const nm = "" ~ getProperty(context, { "entity" : q, "propertyType" : PropertyType.NAME });
    const i = indexOf(nm, "| ");
    const s = i < 0 ? 0 : i + 2;
    return d010Slice(nm, s, 22);
}

// strings have no size(): slice through the character array
function d010Slice(str is string, start is number, n is number) returns string
{
    const ch = splitIntoCharacters(str);
    var out = "";
    for (var j = start; j < min(size(ch), start + n); j += 1)
        out = out ~ ch[j];
    return out;
}

function d010CabDiag(context is Context, id is Id) returns string
{
    var names = [];
    var dist = [];
    var where = [];
    var rNote = "";
    for (var k = 0; k < 6; k += 1)
    {
        const eb = D010_STATES_B1[k];
        const o = { "cables" : true, "cg" : false, "env" : false, "internals" : true, "wm" : true };
        const b = id + ("b" ~ k);
        const off = vector(k * D010_GALLERY_DX, D010_GALLERY_DY, 0);
        d010Instance(context, b, "B1", d010StatePose(eb), off * millimeter, "S" ~ (k + 1), eb[8], o);
        const cab = qCreatedBy(b + "cB", EntityType.BODY);
        if (k == 0)
        {
            for (var c in evaluateQuery(context, cab))
            {
                const cn = "" ~ getProperty(context, { "entity" : c, "propertyType" : PropertyType.NAME });
                const j = indexOf(cn, "bend R ");
                if (j >= 0)
                    rNote = d010Slice(cn, j + 7, 5);
            }
        }
        const others = evaluateQuery(context, qSubtraction(qCreatedBy(b, EntityType.BODY), cab));
        for (var q in others)
        {
            const sn = d010ShortName(context, q);
            if (indexOf(sn, "SUPPORT") >= 0 || indexOf(sn, "AIR GAP") >= 0 || indexOf(sn, "B1 HOLLOW CABLE") >= 0 || indexOf(sn, "IDLER") >= 0 ||
                indexOf(sn, "BASE_REF foot") >= 0 || indexOf(sn, "CG ") >= 0 ||
                indexOf(sn, "BASE_REF shell") >= 0 || indexOf(sn, "DISPLAY HINGE AXIS") >= 0 || indexOf(sn, "LID B1 core") >= 0)
                continue;
            const r = evDistance(context, { "side0" : cab, "side1" : q });
            const d = r.distance / millimeter;
            if (d > D010_DIAG_MAX)
                continue;
            const p = (r.sides[0].point / millimeter) - off;
            var idx = -1;
            for (var m = 0; m < size(names); m += 1)
                if (names[m] == sn)
                    idx = m;
            const tag = "s" ~ (k + 1) ~ " " ~ roundToPrecision(p[0], 0) ~ "," ~ roundToPrecision(p[1], 0) ~ "," ~ roundToPrecision(p[2], 0);
            if (idx < 0)
            {
                names = append(names, sn);
                dist = append(dist, d);
                where = append(where, tag);
            }
            else if (d < dist[idx])
            {
                dist[idx] = d;
                where[idx] = tag;
            }
        }
    }
    var msg = "CABDIAG R" ~ rNote;
    for (var m = 0; m < size(names); m += 1)
        msg = msg ~ "|" ~ names[m] ~ " " ~ roundToPrecision(dist[m], 1) ~ " " ~ where[m];
    return msg;
}

annotation { "Feature Type Name" : "D010 Cable Diag" }
export const d010CableDiag = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
    }
    {
        throw regenError(d010CabDiag(context, id + "g"));
    }, {});
