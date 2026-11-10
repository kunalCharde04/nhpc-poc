import re
s=open('draw.py').read()
head=s[:s.index("# furniture")]; tail=s[s.index("# dims"):]
body='''
def f(x,y,w,h,label,fc,fs=7.5,rot=0,ec='#333'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=1,zorder=3))
    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,rotation=rot,zorder=4)
from matplotlib.patches import Circle
# Vastu corner/zone tags (true directions)
for (x,y,t,c) in [(-0.75,5.95,'SW','#6d4c41'),(W+0.75,5.95,'NW','#546e7a'),(-0.75,-0.35,'SE','#e65100'),(W+0.75,-0.35,'NE','#1565c0')]:
    ax.text(x,y,t,fontsize=12,weight='bold',color=c,ha='center',va='center')
ax.text(3.35,-0.5,'(= EAST wall)',fontsize=7.5,color='#1565c0',ha='center')
ax.text(-1.25,0.0,'SOUTH wall',fontsize=7.5,color='#6d4c41',rotation=90,ha='center')
# furniture
f(0.0,1.05,0.3,0.8,'Shoe cab.\\n0.80x0.30','#d7ccc8',6,90)
f(0.0,1.95,0.9,1.9,'3-SEAT SOFA 1.90x0.90\\n(heavy item on S wall)\\nsitters face NORTH','#90a4ae',7,90)
f(1.05,2.65,0.45,0.5,'Side\\ntable','#ffe0b2',6.5)
ax.add_patch(Circle((1.8,2.9),0.28,fc='none',ec='#2e7d32',ls=':',lw=1.5,zorder=5))
ax.text(1.8,2.9,'centre\\nopen',fontsize=6,color='#2e7d32',ha='center',va='center',zorder=6)
f(3.25,1.15,0.35,1.5,'TV unit 1.50x0.35\\n(NW end of N wall)','#a1887f',6.5,90)
f(2.45,0.0,0.85,0.4,'MANDIR 0.85x0.40\\n(NE corner)','#ffcc80',6.5,0,ec='#e65100')
ax.add_patch(FancyArrowPatch((2.88,1.0),(2.88,0.5),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))
ax.text(2.3,0.95,'worshipper\\nfaces EAST',fontsize=7,color='#e65100',ha='right')
f(0.85,4.65,1.6,0.85,'DINING TABLE\\n1.60 x 0.85','#bcaaa4',8)
f(0.85,5.4,1.6,0.4,'Bench (WEST side): head of family faces EAST','#d7ccc8',5.8)
for i in range(3): f(0.95+i*0.5,4.15,0.42,0.42,'','#cfd8dc')
f(0.0,4.3,0.4,1.4,'Crockery /\\nstorage\\n(SW corner)','#efebe9',6,90,ec='#999')
for p,q in [((1.05,0.75),(2.25,0.75)),((2.25,0.75),(2.25,3.2)),((2.25,3.2),(3.55,3.2)),((2.25,3.3),(2.25,4.0))]:
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
'''
code=head+body+tail
code=code.replace("B/H-105 - Living & Dining: Proposed 2D Furniture Layout (true N = right)","B/H-105 Living & Dining - VASTU layout (true N = right)").replace("living_dining_layout.png","living_dining_vastu.png").replace("set_xlim(-2.6,4.6)","set_xlim(-2.6,4.8)")
exec(code,{'re':re})
