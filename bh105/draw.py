import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, FancyArrowPatch, Polygon
W,D=3.60,5.80
fig,ax=plt.subplots(figsize=(11,13)); ax.set_aspect('equal')
T=0.23
def wall(x,y,w,h): ax.add_patch(Rectangle((x,y),w,h,fc='#444',ec='none',zorder=2))
# walls with openings (E wall opening y2.7-3.7, W wall door y0.1-1.0 & window 2.5-4.1, N wall door x2.7-3.6)
wall(-T,-T,W+2*T,T)                      # south (party wall w/ 106)
wall(-T,0,T,0.1); wall(-T,1.0,T,1.5); wall(-T,4.1,T,D-4.1)   # west
wall(-T,D,W-0.9+T,T)                      # north, solid part
wall(W,0,T,2.7); wall(W,3.7,T,D-3.7)      # east
# window W1 (west)
ax.add_patch(Rectangle((-T,2.5),T,1.6,fc='white',ec='#1565c0',lw=2,zorder=3))
ax.plot([-T/2,-T/2],[2.5,4.1],color='#1565c0',lw=1.5,zorder=4)
ax.text(-0.45,3.3,'W1 window\n1.60 m',rotation=90,ha='center',va='center',fontsize=8,color='#1565c0')
# doors
def door(hx,hy,r,a0,a1,label,lx,ly):
    ax.add_patch(Arc((hx,hy),2*r,2*r,theta1=a0,theta2=a1,ls='--',color='#c62828',lw=1.3,zorder=5))
    ax.text(lx,ly,label,fontsize=8,color='#c62828',ha='center',va='center',zorder=6)
door(0,1.0,0.9,270,360,'',0,0); ax.plot([0,0.9],[1.0,1.0],color='#c62828',lw=2,zorder=5)
ax.text(0.45,0.38,'D1 ENTRANCE\n(opens in)',fontsize=7,color='#c62828',ha='center')
door(2.7,D,0.9,270,360,'',0,0); ax.plot([2.7,2.7],[D-0.9,D],color='#c62828',lw=2,zorder=5)
ax.text(4.35,5.2,'D1 balcony\n(opens in)',fontsize=7,color='#c62828',ha='center')
ax.text(W+0.45,3.2,'OPENING\nto 1.00 m\npassage',fontsize=7.5,ha='center',va='center',rotation=90,color='#555')
ax.text(W+0.45,1.35,'Bath / WC /\nduct wall',fontsize=7.5,ha='center',va='center',rotation=90,color='#555')
ax.text(W+0.45,4.75,'Kitchen wall',fontsize=7.5,ha='center',va='center',rotation=90,color='#555')
ax.text(1.4,D+0.45,'BALCONY (0.715 m deep)',fontsize=8.5,ha='center',color='#555')
ax.text(1.8,-0.45,'Party wall with B/H-106',fontsize=8,ha='center',color='#555')
# furniture
def f(x,y,w,h,label,fc,fs=7.5,rot=0,ec='#333'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=1,zorder=3))
    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,rotation=rot,zorder=4)
f(1.0,0.0,0.9,0.35,'Shoe cab.\n0.90x0.35','#d7ccc8',6.5)
f(0.0,1.05,0.95,2.0,'3-SEAT SOFA\n2.00 x 0.90','#90a4ae',8,90)
f(1.3,1.75,0.5,1.0,'Coffee\ntable\n1.00x0.50','#ffe0b2',7,90)
f(3.25,1.2,0.35,1.45,'TV unit 1.50x0.35\n(43-55" TV)','#a1887f',7,90)
f(0.85,4.65,1.6,0.85,'DINING TABLE\n1.60 x 0.85','#bcaaa4',8)
f(0.85,5.4,1.6,0.4,'Storage bench 1.60x0.40 (3 seats)','#d7ccc8',6.5)
for i in range(3): f(0.95+i*0.5,4.15,0.42,0.42,'','#cfd8dc')
ax.text(1.65,3.98,'3 chairs',fontsize=7,ha='center')
f(0.0,4.3,0.4,1.4,'Crockery unit\n1.40x0.40 (opt.)','#efebe9',6.5,90,ec='#999')
f(3.2,3.85,0.4,0.85,'MANDIR\n0.85x0.40','#ffcc80',7,90,ec='#e65100')
# prayer direction
ax.add_patch(FancyArrowPatch((2.75,4.28),(3.15,4.28),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))
ax.text(2.8,3.88,'worshipper\nfaces EAST',fontsize=7,color='#e65100',ha='center')
# circulation
for p,q in [((1.05,0.7),(2.5,0.7)),((2.5,0.7),(2.5,3.2)),((2.5,3.2),(3.55,3.2)),((2.5,3.3),(2.5,4.45))]:
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
ax.text(2.45,0.9,'walkway',fontsize=7,color='#2e7d32',ha='right')
# dims
ax.annotate('',(0,-0.8),(W,-0.8),arrowprops=dict(arrowstyle='<->'));ax.text(W/2,-0.72,'3.60 m',ha='center',va='bottom',fontsize=9)
ax.annotate('',(-0.95,0),(-0.95,D),arrowprops=dict(arrowstyle='<->'));ax.text(-1.05,D/2,'5.80 m',rotation=90,ha='right',va='center',fontsize=9)
ax.text(1.8,3.55,'LIVING  |  DINING',fontsize=8,color='#37474f',ha='center',alpha=.55)
# north arrow
ax.add_patch(FancyArrowPatch((-1.9,5.2),(-1.9,6.0),arrowstyle='-|>',mutation_scale=22,color='k',lw=2))
ax.text(-1.9,6.1,'N',ha='center',fontsize=14,weight='bold')
ax.text(-1.9,5.0,'S',ha='center',va='top',fontsize=9);
ax.set_xlim(-2.4,4.6); ax.set_ylim(-1.2,6.6); ax.axis('off')
ax.set_title("B/H-105 - Living & Dining: Proposed 2D Furniture Layout (North-up)\nScale ~1:50 | clear room 3.60 x 5.80 m | dashed red = door swing | green = circulation",fontsize=11)
fig.savefig('living_dining_layout.png',dpi=130,bbox_inches='tight')
