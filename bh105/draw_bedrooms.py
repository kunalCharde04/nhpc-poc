import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Arc, FancyArrowPatch
T=0.2
def setup(W,H,title,fn_title):
    fig,ax=plt.subplots(figsize=(10,9)); ax.set_aspect('equal')
    def wall(x,y,w,h): ax.add_patch(Rectangle((x,y),w,h,fc='#444',ec='none',zorder=2))
    def f(x,y,w,h,label,fc,fs=7.5,rot=0,ec='#333',ls='-',z=3):
        ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=1,ls=ls,zorder=z))
        if label: ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,rotation=rot,zorder=z+1)
    def win(x,y,w,h,label,rot=0):
        ax.add_patch(Rectangle((x,y),w,h,fc='white',ec='#1565c0',lw=2,zorder=3))
        ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=7,color='#1565c0',rotation=rot,zorder=5)
    def arrow(p,q,c='#2e7d32',lw=1.5,ms=12): ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=ms,color=c,lw=lw,zorder=6))
    for (x,y,t,c) in [(-0.7,-0.4,'SE','#e65100'),(W+0.7,-0.4,'NE','#1565c0'),(-0.7,H+0.4,'SW','#6d4c41'),(W+0.7,H+0.4,'NW','#546e7a')]:
        ax.text(x,y,t,fontsize=12,weight='bold',color=c,ha='center',va='center')
    ax.annotate('',(0,-0.75),(W,-0.75),arrowprops=dict(arrowstyle='<->')); ax.text(W/2,-0.7,f'{W:.2f} m',ha='center',va='bottom',fontsize=9)
    ax.annotate('',(-0.95,0),(-0.95,H),arrowprops=dict(arrowstyle='<->')); ax.text(-1.05,H/2,f'{H:.2f} m',rotation=90,ha='right',va='center',fontsize=9)
    ax.add_patch(FancyArrowPatch((-2.3,H*0.7),(-1.5,H*0.7),arrowstyle='-|>',mutation_scale=22,color='k',lw=2)); ax.text(-1.35,H*0.7,'N',va='center',fontsize=14,weight='bold')
    ax.text(-1.9,H*0.7+0.25,'TRUE NORTH',ha='center',fontsize=7); ax.text(-1.9,H*0.7-0.25,'(W = top, S = left,\nE = bottom)',ha='center',va='top',fontsize=6.5)
    ax.set_title(title,fontsize=10.5)
    return fig,ax,wall,f,win,arrow
def door(ax,cx,cy,r,a0,a1,p1,p2):
    ax.add_patch(Arc((cx,cy),2*r,2*r,theta1=a0,theta2=a1,ls='--',color='#c62828',lw=1.3,zorder=5))
    ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color='#c62828',lw=2,zorder=5)

# ---------------- Bedroom 1 ----------------
W,H=3.60,2.72
fig,ax,wall,f,win,arrow=setup(W,H,"B/H-105 - Bedroom 1 (NW zone): guest / children's room (true N = right)\nclear room 3.60 x 2.72 m | dashed red = door swing | green = circulation","")
wall(-T,-T,0.1+T,T); wall(1.0,-T,W-1.0+T,T)                 # east (bottom) wall, D2 gap x0.1-1.0
wall(-T,0,T,H)                                                # south (left)
wall(-T,H,1.23+T,T); wall(2.4,H,W-2.4+T,T)                    # west (top) wall, window gap
win(1.23,H,1.17,T,'W2 1.2 m')
wall(W,-T,T,0.12+T); wall(W,1.0,T,0.4); wall(W,2.55,T,H-2.55+T)  # north (right) wall
win(W,1.4,T,1.15,'W2',90)
door(ax,0.1,0,0.9,0,90,(0.1,0),(0.1,0.9)); ax.text(0.8,0.95,'D2 (opens in)',fontsize=6.5,color='#c62828',ha='center')
door(ax,W,0.1,0.9,90,180,(W,0.1),(W-0.9,0.1)); ax.text(2.95,1.1,'D1 balcony\n(opens in)',fontsize=6.5,color='#c62828',ha='center')
ax.text(W+0.55,0.55,'balcony',rotation=90,fontsize=7.5,color='#555',ha='center',va='center')
ax.text(1.8,H+0.55,'sunshade / outside',fontsize=7,color='#555',ha='center')
ax.text(0.5,-0.4,'passage',fontsize=7.5,color='#555',ha='center')
f(0.0,1.15,1.9,1.5,'QUEEN BED 1.50 x 1.90\n(head SOUTH)','#b0bec5',8)
f(0.0,1.15,0.1,1.5,'','#455a64')
f(1.05,0.0,1.5,0.55,'SLIDING WARDROBE\n1.50 x 0.55 x 2.1 h','#bcaaa4',7)
f(2.0,1.3,0.9,0.5,'','none',ec='#999',ls=':'); ax.text(2.45,1.55,'clear floor\n/ yoga mat',fontsize=6,color='#777',ha='center',va='center')
ax.text(0.5,1.05,'wall-hung bedside shelf',fontsize=5.5,color='#555',ha='center')
arrow((0.55,1.9),(0.1,1.9),c='#6d4c41',ms=14)
arrow((0.8,0.8),(1.4,0.8)); arrow((1.4,0.8),(2.65,0.8))
ax.set_xlim(-2.6,4.4); ax.set_ylim(-1.0,H+1.1); ax.axis('off')
fig.savefig('bedroom1_layout.png',dpi=130,bbox_inches='tight'); plt.close(fig)

# ---------------- Bedroom 2 ----------------
W,H=3.30,3.68
fig,ax,wall,f,win,arrow=setup(W,H,"B/H-105 - Bedroom 2 (NE zone): master bedroom (true N = right)\nclear room 3.30 x 3.68 m | dashed red = door swing | green = circulation","")
wall(-T,-T,W+2*T,T)                                         # east (bottom) wall solid
wall(-T,0,T,H)                                              # south (left) wall (toilet side)
wall(0.8,H,W-0.8+T,T); wall(-T,H,T,T)                       # west (top) wall, door gap x0-0.8
wall(W,-T,T,1.7+T); wall(W,2.95,T,H-2.95+T)                 # north (right) wall, window gap
win(W,1.7,T,1.25,'W2 1.25 m',90)
door(ax,0.8,H,0.8,180,270,(0.8,H),(0.8,H-0.8)); ax.text(1.55,2.75,'D2 (opens in)',fontsize=6.5,color='#c62828',ha='center')
ax.text(0.4,H+0.5,'passage',fontsize=7.5,color='#555',ha='center')
ax.text(-0.45,1.0,'toilet\nwall',fontsize=7,color='#555',rotation=90,ha='center',va='center')
f(1.0,0.0,1.5,1.95,'QUEEN BED\n1.50 x 1.95\n(head EAST)','#b0bec5',8)
f(0.5,0.0,0.4,0.4,'','#d7ccc8'); f(2.6,0.0,0.4,0.4,'','#d7ccc8')
ax.text(0.7,0.55,'side\ntbl',fontsize=5.5,ha='center'); ax.text(2.8,0.55,'side\ntbl',fontsize=5.5,ha='center')
f(0.85,3.08,2.0,0.6,'SLIDING WARDROBE 2.00 x 0.60 x 2.1 h','#bcaaa4',7)
f(0.0,1.9,0.45,0.9,'Dresser /\ndesk 0.9x0.45','#d7ccc8',6,90)
arrow((1.75,-0.45),(1.75,-0.05),c='#6d4c41',ms=14); ax.text(2.45,-0.28,'head EAST',fontsize=7,color='#6d4c41')
ax.add_patch(FancyArrowPatch((0.6,2.7),(1.6,2.4),arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
ax.set_xlim(-2.6,4.2); ax.set_ylim(-1.0,H+1.0); ax.axis('off')
fig.savefig('bedroom2_layout.png',dpi=130,bbox_inches='tight'); plt.close(fig)
