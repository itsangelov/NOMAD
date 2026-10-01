# NON-PRODUCTION analysis helper for the D-010 B1 cable pass (2026-09-29). Reads the route from CAD/featurescript/NOMAD_D010_Concepts.fs.
import math, re, json
def route_from_fs(path):
    s=open(path,encoding="utf-8").read()
    blk=re.search(r"export const D010_ROUTE_B1 = \[(.*?)\n    \];",s,re.S).group(1)
    return [(m[0],tuple(float(x) for x in m[1].split(",")),m[2]) for m in re.findall(r'\["(\w+)", \[([^\]]+)\], "(\w*)"\]',blk)]
def fillet(pts,R=12.0):
    n=len(pts); tl=[0.0]*n; info=[None]*n; rmin=R; rows=[]
    for i in range(1,n-1):
        v1=[pts[i][k]-pts[i-1][k] for k in range(3)]; v2=[pts[i+1][k]-pts[i][k] for k in range(3)]
        l1=math.dist(pts[i],pts[i-1]); l2=math.dist(pts[i+1],pts[i])
        c=max(-1,min(1,sum(a*b for a,b in zip(v1,v2))/(l1*l2))); th=math.acos(c)
        if math.degrees(th)<0.5: continue
        tmax=min(l1*(1 if i==1 else .5), l2*(1 if i==n-2 else .5))
        t=R*math.tan(th/2); re=R
        if t>tmax: t=tmax; re=t/math.tan(th/2)
        rmin=min(rmin,re); tl[i]=t; rows.append((i,round(math.degrees(th),1),round(re,2),round(t,2)))
    length=sum(math.dist(pts[i],pts[i+1]) for i in range(n-1))
    # centreline length with fillets: subtract 2t-arc per corner
    for i,thd,re,t in rows:
        th=math.radians(thd); length+= re*th-2*t
    return rmin,length,rows
if __name__=="__main__":
    import sys
    r=route_from_fs(sys.argv[1]); 
    for i,p in enumerate(r): print(i,p)
    print(fillet([p[1] for p in r]))
