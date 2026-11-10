import re
s=open('draw.py').read()
head=s[:s.index("# furniture")]; tail=s[s.index("# dims"):]
FDEF='''def f(x,y,w,h,label,fc,fs=7.5,rot=0,ec='#333'):
    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=1,zorder=3))
    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,rotation=rot,zorder=4)
'''
COMMON='''
f(1.0,0.0,0.9,0.35,'Shoe cab.\\n0.90x0.35','#d7ccc8',6.5)
f(2.6,0.0,0.85,0.4,'MANDIR 0.85x0.40','#ffcc80',7,0,ec='#e65100')
ax.add_patch(FancyArrowPatch((3.0,1.0),(3.0,0.5),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))
ax.text(2.55,0.95,'worshipper\\nfaces EAST',fontsize=7,color='#e65100',ha='right')
f(0.85,4.65,1.6,0.85,'DINING TABLE\\n1.60 x 0.85','#bcaaa4',8)
f(0.85,5.4,1.6,0.4,'Storage bench 1.60x0.40 (3 seats)','#d7ccc8',6.5)
for i in range(3): f(0.95+i*0.5,4.15,0.42,0.42,'','#cfd8dc')
f(0.0,4.3,0.4,1.4,'Crockery unit\\n1.40x0.40 (opt.)','#efebe9',6.5,90,ec='#999')
def walk(pts):
    for p,q in zip(pts,pts[1:]):
        ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
'''
V={}
V['D']=("Option D - L-shaped sectional sofa, east-facing mandir","living_dining_option_D.png",'''
f(0.0,1.05,0.9,2.0,'SECTIONAL 2.00 m leg','#90a4ae',7.5,90)
f(0.9,2.3,0.9,0.75,'Chaise\\n0.9x0.75','#78909c',7)
f(3.25,1.2,0.35,1.45,'TV unit 1.50x0.35\\n(43-55" TV)','#a1887f',7,90)
f(1.95,1.5,0.5,0.9,'Table','#ffe0b2',7,90)
walk([(1.05,0.75),(2.75,0.75),(2.75,1.0)]); walk([(2.6,1.05),(2.6,3.2),(3.55,3.2)]); walk([(2.6,3.3),(2.6,4.0)])
''')
V['E']=("Option E - TV on west wall, loveseat on bath wall, east-facing mandir","living_dining_option_E.png",'''
f(2.75,1.15,0.85,1.5,'2-SEAT SOFA\\n1.50 x 0.85','#90a4ae',7.5,90)
f(0.0,1.1,0.35,1.35,'TV unit 1.30x0.35\\n(43" TV)','#a1887f',7,90)
f(1.2,1.4,0.9,0.5,'Coffee table','#ffe0b2',7)
f(1.0,2.2,0.55,0.55,'','#cfd8dc'); ax.text(1.27,2.47,'Arm-\\nchair',fontsize=6,ha='center',va='center')
walk([(1.05,0.75),(2.2,0.75)]); walk([(2.2,0.75),(2.2,3.2),(3.55,3.2)]); walk([(2.2,3.3),(2.2,4.0)])
''')
V['F']=("Option F - Traditional diwan with armchairs, east-facing mandir","living_dining_option_F.png",'''
f(0.0,1.05,0.8,1.95,'DIWAN w/ storage\\n1.95 x 0.80\\n+ bolsters','#a1887f',7,90)
f(1.2,1.2,0.55,0.55,'','#cfd8dc'); ax.text(1.47,1.47,'Arm-\\nchair',fontsize=6,ha='center',va='center')
f(1.2,2.25,0.55,0.55,'','#cfd8dc'); ax.text(1.47,2.52,'Arm-\\nchair',fontsize=6,ha='center',va='center')
f(1.2,1.8,0.4,0.4,'','#ffe0b2'); ax.text(1.4,2.0,'side\\ntbl',fontsize=5.5,ha='center',va='center')
f(3.25,1.2,0.35,1.45,'TV unit 1.50x0.35\\n(43-55" TV)','#a1887f',7,90)
walk([(1.05,0.75),(2.2,0.75)]); walk([(2.2,0.75),(2.2,3.2),(3.55,3.2)]); walk([(2.2,3.3),(2.2,4.0)])
''')
for k,(title,fn,body) in V.items():
    code=head+FDEF+COMMON+body+tail
    code=code.replace("B/H-105 - Living & Dining: Proposed 2D Furniture Layout (true N = right)","B/H-105 Living & Dining - "+title).replace("living_dining_layout.png",fn)
    exec(code,{'re':re})
