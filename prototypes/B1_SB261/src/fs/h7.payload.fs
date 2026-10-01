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
const ZB = 61.0;
const ZP0 = 67.0;
const ZT = 73.0;
const RG = 4.024;
const FZ0 = AZ - RB;
const FZ1 = AZ - RS;
const LIDX = 24.0;
const LIDY = 40.0;
const LIDZ0 = 47.0;
const LEAFX = 22.0;
const LEAFY = 110.0;
function V(x is number, y is number, z is number) returns Vector
{
return vector(x, y, z) * millimeter;
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
function pocket(context is Context, id is Id, hx is number, zf is number)
{
cx(context, id + "c", -hx, hx, AY, AZ, 15.0);
bx(context, id + "f", -hx - 1, AY - 16, zf - 20, hx + 1, AY + 16, zf);
sub(context, id + "s", bq(id + "f"), bq(id + "c"));
}
function band(context is Context, id is Id, b is array)
{
cx(context, id + "w", b[0], b[1], AY, AZ, RB);
bx(context, id + "f", b[0], AY, FZ0, b[1], AY + REACH, FZ1);
cz(context, id + "h", (b[0] + b[1]) / 2, AY + HOLE, FZ0 - 0.2, FZ1 + 0.2, HOLER);
sub(context, id + "s", bq(id + "h"), bq(id + "f"));
opBoolean(context, id + "u", { "tools" : qUnion([bq(id + "w"), bq(id + "f")]), "operationType" : BooleanOperationType.UNION });
}
function lidCoupon(context is Context, id is Id, lidHoleD is number)
{
bx(context, id + "core", -LIDX, 0, LIDZ0, LIDX, LIDY, ZB);
diamond(context, id + "ch", -LIDX - 1, LIDX + 1, 0, ZB, 9.0);
cx(context, id + "g", -SHAFTH - 2, SHAFTH + 2, AY, AZ, RG);
bx(context, id + "s0", BANDS[0][0] - 0.3, AY, FZ0, BANDS[0][1] + 0.3, AY + REACH + 0.5, ZB + 1);
bx(context, id + "s3", BANDS[3][0] - 0.3, AY, FZ0, BANDS[3][1] + 0.3, AY + REACH + 0.5, ZB + 1);
pocket(context, id + "pd", 8.15, 56.9);
pocket(context, id + "ps", 9.2, 59.0);
cz(context, id + "h0", -11.917, AY + HOLE, 52.4, ZB + 1, lidHoleD / 2);
cz(context, id + "h3", 11.917, AY + HOLE, 52.4, ZB + 1, lidHoleD / 2);
cz(context, id + "m0", -16, 32, LIDZ0 - 1, ZB + 1, 2.75);
cz(context, id + "m1", 16, 32, LIDZ0 - 1, ZB + 1, 2.75);
sub(context, id + "cut", qUnion([bq(id + "ch"), bq(id + "g"), bq(id + "s0"), bq(id + "s3"), bq(id + "pd"), bq(id + "ps"),
bq(id + "h0"), bq(id + "h3"), bq(id + "m0"), bq(id + "m1")]), bq(id + "core"));
}
function leafCoupon(context is Context, id is Id, gap is number, leafHoleD is number, leafDepth is number)
{
const blk = BANDS[3][0] - gap;
bx(context, id + "pl", -LEAFX, 9, ZP0, LEAFX, LEAFY, ZT);
bx(context, id + "bm", -LEAFX, 9, ZB, LEAFX, 18, ZP0);
bx(context, id + "r0", -LEAFX, 18, ZB, -LEAFX + 4, LEAFY, ZP0);
bx(context, id + "r1", LEAFX - 4, 18, ZB, LEAFX, LEAFY, ZP0);
bx(context, id + "bk", -blk, AY, FZ1, blk, 17.5, ZP0);
opBoolean(context, id + "un", { "tools" : qUnion([bq(id + "bm"), bq(id + "r0"), bq(id + "r1"), bq(id + "bk")]), "targets" : bq(id + "pl"),
"operationType" : BooleanOperationType.UNION });
diamond(context, id + "fc", -LEAFX - 1, LEAFX + 1, 9, ZT, 3.0);
bx(context, id + "na", -16.487, 8, ZB - 1, -7.347, 19, FZ1 + 1.65 + 1.0);
bx(context, id + "nb", 7.347, 8, ZB - 1, 16.487, 19, FZ1 + 1.65 + 1.0);
bx(context, id + "nc", -8.4, 8, ZB - 1, 8.4, 19, FZ1);
cx(context, id + "bc", -blk - 0.1, blk + 0.1, AY, AZ, RB);
cx(context, id + "br", -2.0, 2.0, AY, AZ, RG + 0.5);
cz(context, id + "h1", -4.65, AY + HOLE, FZ1 - 0.1, FZ1 + leafDepth, leafHoleD / 2);
cz(context, id + "h2", 4.65, AY + HOLE, FZ1 - 0.1, FZ1 + leafDepth, leafHoleD / 2);
cz(context, id + "l50", 0, 54, ZP0 - 1, ZT + 1, 2.0);
cz(context, id + "l75", 0, 79, ZP0 - 1, ZT + 1, 2.0);
cz(context, id + "l100", 0, 104, ZP0 - 1, ZT + 1, 2.0);
sub(context, id + "cut", qUnion([bq(id + "fc"), bq(id + "na"), bq(id + "nb"), bq(id + "nc"), bq(id + "bc"), bq(id + "br"),
bq(id + "h1"), bq(id + "h2"), bq(id + "l50"), bq(id + "l75"), bq(id + "l100")]), bq(id + "pl"));
}
function buildCoupon(context is Context, id is Id, gap is number, leafHoleD is number, leafDepth is number, lidHoleD is number, hw is boolean) returns map
{
lidCoupon(context, id + "L" + "c", lidHoleD);
if (hw)
{
cx(context, id + "L" + "h" + "sh", -SHAFTH, SHAFTH, AY, AZ, RS);
cx(context, id + "L" + "h" + "cr0", CRINGS[0][0], CRINGS[0][1], AY, AZ, 3.111);
cx(context, id + "L" + "h" + "cr1", CRINGS[1][0], CRINGS[1][1], AY, AZ, 3.111);
band(context, id + "L" + "h" + "b0", BANDS[0]);
band(context, id + "L" + "h" + "b3", BANDS[3]);
for (var k in [0, 3])
{
const xm = (BANDS[k][0] + BANDS[k][1]) / 2;
cz(context, id + "L" + "w" + ("hd" ~ k), xm, AY + HOLE, FZ1, FZ1 + 1.65, 2.85);
cz(context, id + "L" + "w" + ("sk" ~ k), xm, AY + HOLE, FZ1 - 8, FZ1, 1.5);
cz(context, id + "L" + "w" + ("in" ~ k), xm, AY + HOLE, FZ0 - 1 - 5.7, FZ0 - 1, 2.3);
}
}
leafCoupon(context, id + "F" + "c", gap, leafHoleD, leafDepth);
if (hw)
{
band(context, id + "F" + "b" + "b1", BANDS[1]);
band(context, id + "F" + "b" + "b2", BANDS[2]);
for (var k in [1, 2])
{
const xm = (BANDS[k][0] + BANDS[k][1]) / 2;
cz(context, id + "F" + "w" + ("hd" ~ k), xm, AY + HOLE, FZ0 - 2.0, FZ0, 2.5);
cz(context, id + "F" + "w" + ("sk" ~ k), xm, AY + HOLE, FZ0, FZ0 + 4.5, 1.25);
cz(context, id + "F" + "w" + ("in" ~ k), xm, AY + HOLE, FZ1 + 0.1, FZ1 + 4.1, 1.775);
}
}
return { "Lc" : bq(id + "L" + "c"), "Lh" : bq(id + "L" + "h"), "Lw" : bq(id + "L" + "w"), "Lall" : bq(id + "L"),
"Fc" : bq(id + "F" + "c"), "Fb" : bq(id + "F" + "b"), "Fw" : bq(id + "F" + "w"), "Fall" : bq(id + "F") };
}
function leafAxis() returns Line
{
return line(V(0, AY, AZ), vector(1, 0, 0));
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
