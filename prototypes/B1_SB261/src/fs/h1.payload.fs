FeatureScript 3083;
import(path : "onshape/std/common.fs", version : "3083.0");

const AY = 4.0;
const AZ = 63.5;
const RB = 3.524;
const RS = 2.381;
const REACH = 12.7;
const HOLE = 7.95;
const HOLER = 1.753;
const SHAFTH = 16.891;
const BANDS = [[-15.487, -8.347, false], [-8.220, -1.080, true], [1.080, 8.220, true], [8.347, 15.487, false]];
const CRINGS = [[-1.080, -0.699], [0.699, 1.080]];
const CRR = 3.111;
const HCX = [-115.0, 115.0];
const ZF = 42.0;
const ZB = 61.0;
const ZP0 = 67.0;
const ZP1 = 71.0;
const ZT = 73.0;
const W2 = 150.5;
const DD = 235.0;
const PE = 9.0;
const LF = 9.0;
const CH = 9.0;
const LCH = 3.0;
const RG = 4.024;
const RP = 15.0;
const ZPF = 57.3;
const PKX = 8.82;
const HD = 5.7;
const HK = 1.65;
const INSR = 2.3;
const INSL = 5.7;
const INSS = 4.0;
const LSL = 6.0;
const FSL = 5.0;
const FZ0 = AZ - RB;
const FZ1 = AZ - RS;
const BLK = 7.6;
const BLKY = 17.5;
const SLV = [12.0, 76.0, 3.75, 2.75];
const CABR = 2.0;
const BENDR = 12.0;
const LEAFCAB = [[0, 40, 64], [0, 4, 63.5], [12, 4, 63.5]];
const LIDCAB = [[76, 4, 63.5], [88, 4, 63.5], [88, 30, 64], [88, 54, 53], [141, 54, 53], [141, 193.5, 53]];
function V(x is number, y is number, z is number) returns Vector
{
return vector(x, y, z) * millimeter;
}
function VA(p is array) returns Vector
{
return vector(p[0], p[1], p[2]) * millimeter;
}
function bx(context is Context, id is Id, x0 is number, y0 is number, z0 is number, x1 is number, y1 is number, z1 is number)
{
fCuboid(context, id, { "corner1" : V(x0, y0, z0), "corner2" : V(x1, y1, z1) });
}
function cx(context is Context, id is Id, x0 is number, x1 is number, y is number, z is number, r is number)
{
fCylinder(context, id, { "bottomCenter" : V(x0, y, z), "topCenter" : V(x1, y, z), "radius" : r * millimeter });
}
function cz(context is Context, id is Id, x is number, y is number, z0 is number, z1 is number, r is number)
{
fCylinder(context, id, { "bottomCenter" : V(x, y, z0), "topCenter" : V(x, y, z1), "radius" : r * millimeter });
}
function bq(id is Id) returns Query
{
return qCreatedBy(id, EntityType.BODY);
}
function sub(context is Context, id is Id, tools is Query, targets is Query)
{
opBoolean(context, id, { "tools" : tools, "targets" : targets, "operationType" : BooleanOperationType.SUBTRACTION });
}
function diamond(context is Context, id is Id, x0 is number, x1 is number, yc is number, zc is number, h is number)
{
const a = h / sqrt(2);
bx(context, id + "b", x0, -a, -a, x1, a, a);
opTransform(context, id + "t", { "bodies" : bq(id + "b"),
"transform" : transform(V(0, yc, zc)) * rotationAround(line(V(0, 0, 0), vector(1, 0, 0)), 45 * degree) });
}
function band(context is Context, id is Id, c is number, b is array)
{
const x0 = c + b[0];
const x1 = c + b[1];
cx(context, id + "w", x0, x1, AY, AZ, RB);
bx(context, id + "f", x0, AY, FZ0, x1, AY + REACH, FZ1);
cz(context, id + "h", (x0 + x1) / 2, AY + HOLE, FZ0 - 0.2, FZ1 + 0.2, HOLER);
sub(context, id + "s", bq(id + "h"), bq(id + "f"));
opBoolean(context, id + "u", { "tools" : qUnion([bq(id + "w"), bq(id + "f")]), "operationType" : BooleanOperationType.UNION });
}
function tube(context is Context, id is Id, pts is array, R is number, rc is number)
{
const n = size(pts);
var s0 = VA(pts[0]);
var k = 0;
for (var i = 1; i < n - 1; i += 1)
{
const P = VA(pts[i]);
const u1 = normalize(P - VA(pts[i - 1]));
const u2 = normalize(VA(pts[i + 1]) - P);
const th = angleBetween(u1, u2);
const t = R * tan(th / 2) * millimeter;
const T1 = P - u1 * t;
const T2 = P + u2 * t;
if (norm(T1 - s0) > 0.001 * millimeter)
{
fCylinder(context, id + ("s" ~ k), { "bottomCenter" : s0, "topCenter" : T1, "radius" : rc * millimeter });
}
const C = P + normalize(u2 - u1) * (R / cos(th / 2)) * millimeter;
const a = normalize(cross(u1, u2));
const sk = newSketchOnPlane(context, id + ("k" ~ k), { "sketchPlane" : plane(T1, u1) });
skCircle(sk, "c", { "center" : vector(0, 0) * millimeter, "radius" : rc * millimeter });
skSolve(sk);
opRevolve(context, id + ("r" ~ k), { "entities" : qSketchRegion(id + ("k" ~ k)), "axis" : line(C, a), "angleForward" : th });
if (evDistance(context, { "side0" : bq(id + ("r" ~ k)), "side1" : T2 }).distance > 0.01 * millimeter)
{
opDeleteBodies(context, id + ("x" ~ k), { "entities" : bq(id + ("r" ~ k)) });
opRevolve(context, id + ("q" ~ k), { "entities" : qSketchRegion(id + ("k" ~ k)), "axis" : line(C, -a), "angleForward" : th });
}
opDeleteBodies(context, id + ("d" ~ k), { "entities" : bq(id + ("k" ~ k)) });
k += 1;
s0 = T2;
}
const PL = VA(pts[n - 1]);
if (norm(PL - s0) > 0.001 * millimeter)
{
fCylinder(context, id + ("s" ~ k), { "bottomCenter" : s0, "topCenter" : PL, "radius" : rc * millimeter });
}
}
function lidCore(context is Context, id is Id)
{
bx(context, id + "core", -W2, 0, ZF, W2, DD, ZB);
var tools = [];
diamond(context, id + "ch", -W2 - 1, W2 + 1, 0, ZB, CH);
tools = append(tools, bq(id + "ch"));
for (var i = 0; i < 2; i += 1)
{
const c = HCX[i];
cx(context, id + ("g" ~ i), c - SHAFTH - 2, c + SHAFTH + 2, AY, AZ, RG);
tools = append(tools, bq(id + ("g" ~ i)));
for (var k in [0, 3])
{
const b = BANDS[k];
bx(context, id + ("st" ~ (i * 4 + k)), c + b[0] - 0.3, AY, FZ0, c + b[1] + 0.3, AY + REACH + 0.5, ZB + 1);
tools = append(tools, bq(id + ("st" ~ (i * 4 + k))));
}
cx(context, id + ("pk" ~ i), c - PKX, c + PKX, AY, AZ, RP);
bx(context, id + ("pf" ~ i), c - PKX - 1, AY - RP - 1, ZPF - 20, c + PKX + 1, AY + RP + 1, ZPF);
sub(context, id + ("pb" ~ i), bq(id + ("pf" ~ i)), bq(id + ("pk" ~ i)));
tools = append(tools, bq(id + ("pk" ~ i)));
}
cx(context, id + "gc", -3, 89, AY, AZ, RG);
tools = append(tools, bq(id + "gc"));
bx(context, id + "rc", -3, 0, 59.5, 13, 18, ZB + 1);
tools = append(tools, bq(id + "rc"));
sub(context, id + "cut", qUnion(tools), bq(id + "core"));
}
function leafStr(context is Context, id is Id)
{
bx(context, id + "pan", -136.5, PE, ZP0, 136.5, PE + 223, ZP1);
bx(context, id + "beam", -136.5, LF, ZB, 136.5, LF + 9, ZP0);
var tools = [];
for (var i = 0; i < 2; i += 1)
{
const c = HCX[i];
bx(context, id + ("na" ~ i), c - 15.987, LF - 1, ZB - 1, c - 7.847, LF + 10, FZ1 + HK + 1.0);
bx(context, id + ("nb" ~ i), c + 7.847, LF - 1, ZB - 1, c + 15.987, LF + 10, FZ1 + HK + 1.0);
bx(context, id + ("nc" ~ i), c - 8.4, LF - 1, ZB - 1, c + 8.4, LF + 10, FZ1);
tools = concatenateArrays([tools, [bq(id + ("na" ~ i)), bq(id + ("nb" ~ i)), bq(id + ("nc" ~ i))]]);
}
bx(context, id + "nle", -3, LF - 1, ZB - 1, 8, LF + 10, ZP0 + 1);
bx(context, id + "nlx", 74, LF - 1, ZB - 1, 92, LF + 10, ZP0 + 1);
tools = concatenateArrays([tools, [bq(id + "nle"), bq(id + "nlx")]]);
sub(context, id + "bcut", qUnion(tools), bq(id + "beam"));
for (var i = 0; i < 2; i += 1)
{
const c = HCX[i];
bx(context, id + ("blk" ~ i), c - BLK, AY, FZ1, c + BLK, BLKY, ZP0);
cx(context, id + ("bc" ~ i), c - BLK - 0.1, c + BLK + 0.1, AY, AZ, RB);
cx(context, id + ("br" ~ i), c - 1.3, c + 1.3, AY, AZ, RG);
sub(context, id + ("bs" ~ i), qUnion([bq(id + ("bc" ~ i)), bq(id + ("br" ~ i))]), bq(id + ("blk" ~ i)));
}
bx(context, id + "swr", 136.5, LF, ZB, 144.5, DD, ZT);
bx(context, id + "swl", -144.5, LF, ZB, -136.5, DD, ZT);
diamond(context, id + "swc", -146, 146, LF, ZT, LCH);
sub(context, id + "sws", bq(id + "swc"), qUnion([bq(id + "swr"), bq(id + "swl")]));
bx(context, id + "rw", -144.5, 232, ZB, 144.5, DD, ZT);
}
function buildAll(context is Context, id is Id, withAcc is boolean) returns map
{
const idL = id + "L";
const idF = id + "F";
lidCore(context, idL + "c");
bx(context, idL + "d", -117.5, 42.5, 43, 117.5, 192.5, 48);
var shafts = [];
var fixBands = [];
for (var i = 0; i < 2; i += 1)
{
const c = HCX[i];
cx(context, idL + "h" + ("sh" ~ i), c - SHAFTH, c + SHAFTH, AY, AZ, RS);
shafts = append(shafts, bq(idL + "h" + ("sh" ~ i)));
for (var j = 0; j < 2; j += 1)
{
cx(context, idL + "h" + ("cr" ~ (i * 2 + j)), c + CRINGS[j][0], c + CRINGS[j][1], AY, AZ, CRR);
}
for (var k in [0, 3])
{
band(context, idL + "h" + ("b" ~ (i * 4 + k)), c, BANDS[k]);
fixBands = append(fixBands, bq(idL + "h" + ("b" ~ (i * 4 + k))));
}
}
var lidHeads = [];
var lidIns = [];
for (var i = 0; i < 2; i += 1)
{
for (var k in [0, 3])
{
const xm = HCX[i] + (BANDS[k][0] + BANDS[k][1]) / 2;
const tg = "" ~ (i * 4 + k);
cz(context, idL + "w" + ("hd" ~ tg), xm, AY + HOLE, FZ1, FZ1 + HK, HD / 2);
cz(context, idL + "w" + ("sk" ~ tg), xm, AY + HOLE, FZ1 - LSL, FZ1, 1.5);
cz(context, idL + "w" + ("in" ~ tg), xm, AY + HOLE, FZ0 - INSL, FZ0, INSR);
lidHeads = append(lidHeads, bq(idL + "w" + ("hd" ~ tg)));
lidIns = append(lidIns, bq(idL + "w" + ("in" ~ tg)));
}
}
cx(context, idL + "s" + "tube", SLV[0], SLV[1], AY, AZ, SLV[2]);
cx(context, idL + "s" + "bore", SLV[0] - 0.1, SLV[1] + 0.1, AY, AZ, SLV[3]);
sub(context, idL + "s" + "cut", bq(idL + "s" + "bore"), bq(idL + "s" + "tube"));
cx(context, idL + "s" + "cab", SLV[0], SLV[1], AY, AZ, CABR);
tube(context, idL + "k", LIDCAB, BENDR, CABR);
leafStr(context, idF + "s");
for (var i = 0; i < 2; i += 1)
{
for (var k in [1, 2])
{
band(context, idF + "b" + ("b" ~ (i * 4 + k)), HCX[i], BANDS[k]);
}
}
var leafHeads = [];
var leafIns = [];
for (var i = 0; i < 2; i += 1)
{
for (var k in [1, 2])
{
const xm = HCX[i] + (BANDS[k][0] + BANDS[k][1]) / 2;
const tg = "" ~ (i * 4 + k);
cz(context, idF + "w" + ("hd" ~ tg), xm, AY + HOLE, FZ0 - HK, FZ0, HD / 2);
cz(context, idF + "w" + ("sk" ~ tg), xm, AY + HOLE, FZ0, FZ0 + FSL, 1.5);
cz(context, idF + "w" + ("in" ~ tg), xm, AY + HOLE, FZ1, FZ1 + INSS, INSR);
leafHeads = append(leafHeads, bq(idF + "w" + ("hd" ~ tg)));
leafIns = append(leafIns, bq(idF + "w" + ("in" ~ tg)));
}
}
tube(context, idF + "k", LEAFCAB, BENDR, CABR);
var q = {
"Lc" : bq(idL + "c"), "Ld" : bq(idL + "d"), "Lw" : bq(idL + "w"), "Lh" : bq(idL + "h"), "Ls" : bq(idL + "s"),
"Lk" : bq(idL + "k"), "Lall" : bq(idL),
"Fs" : bq(idF + "s"), "Fw" : bq(idF + "w"), "Fb" : bq(idF + "b"), "Fk" : bq(idF + "k"), "Fall" : bq(idF),
"pan" : bq(idF + "s" + "pan"), "beam" : bq(idF + "s" + "beam"),
"blk" : qUnion([bq(idF + "s" + "blk0"), bq(idF + "s" + "blk1")]),
"lidHead" : qUnion(lidHeads), "leafHead" : qUnion(leafHeads), "leafIns" : qUnion(leafIns), "lidIns" : qUnion(lidIns),
"shaft" : qUnion(shafts), "fixBand" : qUnion(fixBands), "Frot" : bq(idF) };
if (withAcc)
{
var accL = [];
var accF = [];
for (var i = 0; i < 2; i += 1)
{
for (var k = 0; k < 4; k += 1)
{
const xm = HCX[i] + (BANDS[k][0] + BANDS[k][1]) / 2;
const tg = "" ~ (i * 4 + k);
if (BANDS[k][2])
{
cz(context, id + "A" + ("f" ~ tg), xm, AY + HOLE, FZ0 - HK - 60, FZ0 - HK, 3.5);
accF = append(accF, bq(id + "A" + ("f" ~ tg)));
}
else
{
cz(context, id + "A" + ("l" ~ tg), xm, AY + HOLE, FZ1 + HK, FZ1 + HK + 60, 3.5);
accL = append(accL, bq(id + "A" + ("l" ~ tg)));
}
}
}
q.accL = qUnion(accL);
q.accF = qUnion(accF);
q.Frot = qUnion([bq(idF), qUnion(accF)]);
}
return q;
}
function leafAxis() returns Line
{
return line(V(0, AY, AZ), vector(1, 0, 0));
}
function rotLeaf(context is Context, id is Id, q is map, dpsi is number)
{
opTransform(context, id, { "bodies" : q.Frot, "transform" : rotationAround(leafAxis(), dpsi * degree) });
}
function dmm(context is Context, a is Query, b is Query) returns number
{
return evDistance(context, { "side0" : a, "side1" : b }).distance / millimeter;
}
function f2(x is number) returns string
{
var v = round(x * 100);
var sg = "";
if (v < 0)
{
sg = "-";
v = -v;
}
const ip = floor(v / 100);
const dp = v - ip * 100;
var ds = "" ~ dp;
if (dp < 10)
{
ds = "0" ~ dp;
}
return sg ~ ip ~ "." ~ ds;
}
function pairList(q is map) returns array
{
const F = [["s", q.Fs], ["w", q.Fw], ["b", q.Fb], ["c", q.Fk]];
const L = [["C", q.Lc], ["D", q.Ld], ["W", q.Lw], ["H", q.Lh], ["S", q.Ls], ["K", q.Lk]];
var out = [];
for (var f in F)
{
for (var l in L)
{
if ((f[0] == "b" && l[0] == "H") || (f[0] == "c" && l[0] == "S"))
{
continue;
}
out = append(out, [f[0] ~ l[0], f[1], l[1]]);
}
}
return out;
}
function pairMin(context is Context, pl is array, rest is boolean) returns array
{
var best = 1e9;
var tag = "";
for (var p in pl)
{
if (rest && p[0] == "sC")
{
continue;
}
const d = dmm(context, p[1], p[2]);
if (d < best)
{
best = d;
tag = p[0];
}
}
return [best, tag];
}
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
