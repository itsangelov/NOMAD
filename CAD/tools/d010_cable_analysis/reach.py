# NON-PRODUCTION: grid reachability of a tube of radius r from the knuckle axis into the open pocket (proves the 3.04 mm passage).
import math, itertools, collections
from cabmodel import OBS, CYL, dbox, dcyl
def free(p,r):
    for nm in ("frame","panel","plate","foil","lid"):
        if any(dbox(p,b)<r for b in OBS[nm]): return False
    if dcyl(p,CYL["barrel"])<r: return False
    return True
def reach(start,goals,r,x0,x1,y0,y1,z0,z1,h=0.5):
    q=collections.deque([start]); seen={start}
    def P(i): return (x0+i[0]*h,y0+i[1]*h,z0+i[2]*h)
    while q:
        c=q.popleft()
        if P(c) in goals or any(math.dist(P(c),g)<h for g in goals): return True,P(c)
        for d in ((1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)):
            n=(c[0]+d[0],c[1]+d[1],c[2]+d[2])
            if n in seen: continue
            p=P(n)
            if not(x0<=p[0]<=x1 and y0<=p[1]<=y1 and z0<=p[2]<=z1): continue
            seen.add(n)
            if free(p,r): q.append(n)
    return False,len(seen)
# region: leaf/lid space between the twist axis and the lid interior: axis points x in 74..135 (barrel excluded), target = anywhere below the lid back skin (z<=58) or gap pocket y>=30
h=0.5
for r in (2.0,1.9,1.5):
    for xs in (80,100,120):
        start=((xs-70)/h,(4-(-2))/h,(69-56)/h)   # index of (xs,4,69) with origin x0=70,y0=-2,z0=56
        start=(int(start[0]),int(start[1]),int(start[2]))
        # goal: any point with y>=14 and z<=66 (open pocket) or z<=58 (inside lid)
        goals=[(x,y,z) for x in (xs,) for y in (16,) for z in (63,64,65)]
        ok=reach(start,goals,r,70,146,-2,40,56,76,h)
        print("r",r,"x-start",xs,"reach pocket:",ok)
