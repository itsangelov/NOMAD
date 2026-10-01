# NON-PRODUCTION: numeric obstacle model of the B1 leaf/lid (boxes + cylinders) and cable clearance sampler; matches the Onshape kernel within 0.01 mm.
import math, itertools
R_CAB=2.0
def sub(a,b):
    """box a minus box b -> list of boxes. boxes (x0,y0,z0,x1,y1,z1)"""
    ix=[max(a[i],b[i]) for i in range(3)]+[min(a[i+3],b[i+3]) for i in range(3)]
    if any(ix[i]>=ix[i+3] for i in range(3)): return [a]
    out=[]; cur=list(a)
    for ax in range(3):
        if cur[ax]<ix[ax]:
            t=list(cur); t[ax+3]=ix[ax]; out.append(tuple(t)); cur[ax]=ix[ax]
        if cur[ax+3]>ix[ax+3]:
            t=list(cur); t[ax]=ix[ax+3]; out.append(tuple(t)); cur[ax+3]=ix[ax+3]
    return out
def subs(boxes,cuts):
    for c in cuts:
        nb=[]
        for b in boxes: nb+=sub(b,c)
        boxes=nb
    return boxes
def frame_right():
    px=136.5; py0=6; Dp=235; zc=61; z0=67; zt=73; lw=144.5; hingeX=55
    fr=[(0.25,0,zc,lw,Dp,zt)]
    cuts=[(-1,py0+3,zc-1,px-2.5,Dp-py0-3,zt+1),(-1,py0-.5,zc-1,px+.5,Dp-py0+.5,z0+4),(-1,-1,zc-1,30,py0,z0),(-1,Dp-py0,zc-1,110,Dp+1,z0),
          (hingeX-16,-1,64,lw-3,9.5,zt+1),(-1,-1,zc-1,lw+1,4,63.3)]
    return subs(fr,cuts)
def lid_shell():
    b=[(-150.5,0,42,150.5,235,61)]
    return subs(b,[(-148,2.5,44.5,148,232.5,58.5),(-117.5,42.5,41,117.5,192.5,44.51)])
OBS={}
OBS["frame"]=frame_right()
OBS["panel"]=[(-136.5,6,67,136.5,229,71)]
OBS["plate"]=[(43,.5,62,67,24,64.5)]
OBS["conn"]=[(30,10,61.5,46,18,66.5)]
OBS["foil"]=[(-135,12,61,135,223,61.3)]
OBS["lid"]=lid_shell()
OBS["ctl"]=[(8.5,197.1,44.5,119,232.5,56.5)]
OBS["disp"]=[(-117.5,42.5,43,117.5,192.5,48)]
OBS["pad"]=[(-71.5,188.25,57.5,71.5,211.75,58.5)]
OBS["latch"]=[(-10,226,61.5,10,234,67),(-8,227,58.5,8,233,61)]
CYL={"barrel":(40,70,4,69,4.0)}   # x0,x1,y,z,r
def dbox(p,b):
    dx=max(b[0]-p[0],0,p[0]-b[3]); dy=max(b[1]-p[1],0,p[1]-b[4]); dz=max(b[2]-p[2],0,p[2]-b[5])
    return math.sqrt(dx*dx+dy*dy+dz*dz)
def dcyl(p,c):
    x0,x1,y,z,r=c
    dr=max(math.hypot(p[1]-y,p[2]-z)-r,0); dx=max(x0-p[0],0,p[0]-x1)
    return math.hypot(dr,dx)
def centerline(pts,R=12.0,step=0.5):
    n=len(pts); tl=[0]*n; info=[None]*n; rmin=R
    for i in range(1,n-1):
        v1=[pts[i][k]-pts[i-1][k] for k in range(3)]; v2=[pts[i+1][k]-pts[i][k] for k in range(3)]
        l1=math.dist(pts[i],pts[i-1]); l2=math.dist(pts[i+1],pts[i])
        c=max(-1,min(1,sum(a*b for a,b in zip(v1,v2))/(l1*l2))); th=math.acos(c)
        if math.degrees(th)<0.5: continue
        tmax=min(l1*(1 if i==1 else .5),l2*(1 if i==n-2 else .5))
        t=R*math.tan(th/2); re=R
        if t>tmax: t=tmax; re=t/math.tan(th/2)
        rmin=min(rmin,re); tl[i]=t
        u1=[a/l1 for a in v1]; u2=[a/l2 for a in v2]
        info[i]=(u1,u2,th,re,t)
    out=[]  # list of (point, segment index tag)
    for i in range(n-1):
        u=[pts[i+1][k]-pts[i][k] for k in range(3)]; L=math.sqrt(sum(a*a for a in u)); u=[a/L for a in u]
        a=[pts[i][k]+u[k]*tl[i] for k in range(3)]; b=[pts[i+1][k]-u[k]*tl[i+1] for k in range(3)]
        seg=math.dist(a,b); m=max(2,int(seg/step))
        for j in range(m+1): out.append((tuple(a[k]+(b[k]-a[k])*j/m for k in range(3)),i))
        if i+1<n-1 and info[i+1]:
            u1,u2,th,re,t=info[i+1]; t1=[pts[i+1][k]-u1[k]*t for k in range(3)]
            dotp=sum(u1[k]*u2[k] for k in range(3)); nrm=[u2[k]-u1[k]*dotp for k in range(3)]; ln=math.sqrt(sum(a*a for a in nrm)); nrm=[a/ln for a in nrm]
            ctr=[t1[k]+nrm[k]*re for k in range(3)]
            m2=max(3,int(re*th/step))
            for j in range(1,m2):
                ang=th*j/m2
                p=[ctr[k]-nrm[k]*re*math.cos(ang)+u1[k]*re*math.sin(ang) for k in range(3)]
                out.append((tuple(p),i+0.5))
    return out,rmin
def clearances(cl,skip=("conn",)):
    res={}
    for p,seg in cl:
        for name,boxes in OBS.items():
            d=min(dbox(p,b) for b in boxes)-R_CAB
            if d<res.get(name,(1e9,))[0]: res[name]=(d,tuple(round(v,1) for v in p),seg)
        d=dcyl(p,CYL["barrel"])-R_CAB
        if d<res.get("barrel",(1e9,))[0]: res["barrel"]=(d,tuple(round(v,1) for v in p),seg)
    return res
if __name__=="__main__":
    import sys
    from cabmath import route_from_fs
    r=route_from_fs(sys.argv[1]); cl,rm=centerline([p[1] for p in r])
    print("rmin",round(rm,2))
    for k,v in sorted(clearances(cl).items(),key=lambda kv:kv[1][0]): print(k,round(v[0],2),v[1],"seg",v[2])
