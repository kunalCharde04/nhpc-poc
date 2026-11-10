import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, FancyArrowPatch
W,H=3.03,2.72; T=0.2
fig,ax=plt.subplots(figsize=(11,10)); ax.set_aspect('equal')
def wall(x,y,w,h): ax.add_patch(Rectangle((x,y),w,h,fc='#444',ec='none',zorder=2))
# image orientation: bottom = EAST wall, left = SOUTH wall, top = WEST wall, right = NORTH wall
wall(-T,-T,2.0+T,T)                       # east wall (bottom) solid x0-2.0
wall(-T,0,T,H)                            # south wall (left) shared with dining
wall(W,-T,T,H+2*T)                        # north wall (right)
wall(-T,H,0.47+T,T); wall(1.75,H,0.35,T)  # west wall (top) pieces
wall(2.95,H,W-2.95+T,T)
ax.add_patch(Rectangle((0.47,H),1.28,T,fc='white',ec='#1565c0',lw=2,zorder=3))
ax.text(1.11,H+0.1,'W3 window 1.28 m',ha='center',va='center',fontsize=7.5,color='#1565c0',zorder=5)
# door D1 (hinge east side at x=2.95), opens into kitchen
ax.add_patch(Arc((2.95,H),1.7,1.7,theta1=180,theta2=270,ls='--',color='#c62828',lw=1.3,zorder=5))
ax.plot([2.95,2.95],[H,H-0.85],color='#c62828',lw=2,zorder=5)
ax.text(2.4,H-0.45,'D1 to balcony\n(opens in)',fontsize=7,color='#c62828',ha='center')
ax.text(1.5,H+0.55,'KITCHEN BALCONY (0.9 m deep) - utility / washing machine (optional)',ha='center',fontsize=8,color='#555')
ax.text(2.5,-0.12,'',fontsize=7)
ax.text(2.52,-0.35,'OPEN DOORWAY ~1.0 m to passage',ha='center',fontsize=7.5,color='#555')
ax.text(-0.45,H/2,'SOUTH wall - shared with dining',rotation=90,ha='center',va='center',fontsize=7.5,color='#555')
ax.text(W+0.45,H/2,'NORTH wall',rotation=90,ha='center',va='center',fontsize=7.5,color='#555')
ax.text(1.0,-0.35,'EAST wall (solid)',ha='center',fontsize=7.5,color='#555')
def f(x,y,w,h,label,fc,fs=7.5,rot=0,ec='#333',ls='-',z=3,lw=1):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=lw,ls=ls,zorder=z))
    if label: ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,rotation=rot,zorder=z+1)
# base counters (0.60 deep)
f(0.0,0.0,0.4,0.6,'Corner\nbase +\ngas\ncylinder','#d7ccc8',5.5)
f(0.4,0.0,0.6,0.6,'HOB\n3-burner','#ef9a9a',7)
f(1.0,0.0,1.0,0.6,'Prep counter +\nmicrowave','#d7ccc8',7)
f(0.0,0.6,0.6,1.4,'Base units\n(storage,\ndrawers)','#d7ccc8',7,90)
f(0.7,H-0.6,0.2,0.6,'','#d7ccc8')
f(0.9,H-0.6,0.85,0.6,'SINK + drainboard','#90caf9',7)
f(1.75,H-0.6,0.25,0.6,'','#d7ccc8')
f(0.0,2.0,0.7,0.72,'FRIDGE\n0.65x0.70','#cfd8dc',7)
# wall units (dashed)
f(0.0,0.0,2.0,0.35,'','none',ec='#8d6e63',ls='--',z=4)
ax.text(1.2,0.17,'wall units 0.35 deep above (chimney over hob optional)',fontsize=5.5,ha='center',va='center',color='#8d6e63',zorder=6)
f(0.0,0.6,0.35,1.4,'','none',5.5,90,ec='#8d6e63',ls='--',z=4)
# cook position/arrow
ax.add_patch(FancyArrowPatch((0.7,0.95),(0.7,0.65),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))
ax.text(1.0,0.9,'cook faces EAST',fontsize=7.5,color='#e65100',zorder=6)
# circulation
for p,q in [((2.5,-0.05),(2.5,0.9)),((2.5,0.9),(1.3,1.35))]:
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
ax.text(1.75,1.55,'1.50 m aisle',fontsize=7.5,color='#2e7d32')
for (x,y,t,c) in [(-0.7,-0.4,'SE','#e65100'),(W+0.7,-0.4,'NE','#1565c0'),(-0.7,H+0.4,'SW','#6d4c41'),(W+0.7,H+0.4,'NW','#546e7a')]:
    ax.text(x,y,t,fontsize=12,weight='bold',color=c,ha='center',va='center')
ax.annotate('',(0,-0.75),(W,-0.75),arrowprops=dict(arrowstyle='<->')); ax.text(W/2,-0.7,'3.03 m',ha='center',va='bottom',fontsize=9)
ax.annotate('',(-0.95,0),(-0.95,H),arrowprops=dict(arrowstyle='<->')); ax.text(-1.05,H/2,'2.72 m',rotation=90,ha='right',va='center',fontsize=9)
ax.add_patch(FancyArrowPatch((-2.3,2.0),(-1.5,2.0),arrowstyle='-|>',mutation_scale=22,color='k',lw=2)); ax.text(-1.35,2.0,'N',va='center',fontsize=14,weight='bold')
ax.text(-1.9,2.25,'TRUE NORTH',ha='center',fontsize=7); ax.text(-1.9,1.75,'(W = top, S = left,\nE = bottom)',ha='center',va='top',fontsize=6.5)
ax.set_xlim(-2.6,4.0); ax.set_ylim(-1.0,3.7); ax.axis('off')
ax.set_title("B/H-105 - Kitchen: Vastu-aligned L/U layout (true N = right)\nclear room 3.03 x 2.72 m | counters 0.60 deep | dashed brown = wall units | dashed red = door swing",fontsize=10.5)
fig.savefig('kitchen_layout.png',dpi=130,bbox_inches='tight')
