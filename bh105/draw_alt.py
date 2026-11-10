import re
FDEF="def f(x,y,w,h,label,fc,fs=7.5,rot=0,ec='#333'):\n    ax.add_patch(Rectangle((x,y),w,h,fc=fc,ec=ec,lw=1,zorder=3))\n    ax.text(x+w/2,y+h/2,label,ha='center',va='center',fontsize=fs,rotation=rot,zorder=4)\n"
s=open('draw.py').read()
head=s[:s.index("# furniture")]
tail=s[s.index("# dims"):]
V={}
V['B']=("Option B - Sofa on east wall, TV on west wall","living_dining_option_B.png","""
f(1.0,0.0,0.9,0.35,'Shoe cab.\\n0.90x0.35','#d7ccc8',6.5)
f(2.7,0.5,0.9,2.1,'3-SEAT SOFA\\n2.10 x 0.90','#90a4ae',8,90)
f(1.55,1.35,0.5,1.0,'Coffee\\ntable','#ffe0b2',7,90)
f(0.0,1.15,0.35,1.3,'TV unit 1.30x0.35\\n(43" TV)','#a1887f',7,90)
f(0.85,4.65,1.6,0.85,'DINING TABLE\\n1.60 x 0.85','#bcaaa4',8)
f(0.85,5.4,1.6,0.4,'Storage bench 1.60x0.40 (3 seats)','#d7ccc8',6.5)
for i in range(3): f(0.95+i*0.5,4.15,0.42,0.42,'','#cfd8dc')
f(0.0,4.3,0.4,1.4,'Crockery unit\\n1.40x0.40 (opt.)','#efebe9',6.5,90,ec='#999')
f(3.2,3.85,0.4,0.85,'MANDIR\\n0.85x0.40','#ffcc80',7,90,ec='#e65100')
ax.add_patch(FancyArrowPatch((2.75,4.28),(3.15,4.28),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))
ax.text(2.8,3.88,'worshipper\\nfaces EAST',fontsize=7,color='#e65100',ha='center')
for p,q in [((1.05,0.7),(1.3,0.7)),((1.3,0.7),(1.3,3.2)),((1.3,3.2),(3.55,3.2)),((1.3,3.3),(1.3,4.0))]:
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
""")
V['C']=("Option C - Sofa as living/dining divider, TV on south wall","living_dining_option_C.png","""
f(1.6,0.0,1.5,0.35,'TV unit 1.50x0.35\\n(43-55" TV)','#a1887f',7)
f(1.0,0.0,0.55,0.35,'Shoe\\ncab.','#d7ccc8',6)
f(0.15,3.0,2.0,0.85,'3-SEAT SOFA 2.00x0.85 (back to dining)','#90a4ae',7.5)
f(1.1,1.5,0.9,0.5,'Coffee table','#ffe0b2',7)
f(0.1,2.0,0.5,0.5,'','#cfd8dc'); ax.text(0.35,2.25,'Arm-\\nchair',fontsize=6,ha='center',va='center')
f(0.85,4.75,1.6,0.85,'DINING TABLE\\n1.60 x 0.85','#bcaaa4',8)
f(0.85,5.45,1.6,0.35,'Storage bench (3 seats)','#d7ccc8',6.5)
for i in range(3): f(0.95+i*0.5,4.3,0.42,0.42,'','#cfd8dc')
f(3.2,3.95,0.4,0.8,'MANDIR\\n0.80x0.40','#ffcc80',7,90,ec='#e65100')
ax.add_patch(FancyArrowPatch((2.75,4.35),(3.15,4.35),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))
ax.text(2.8,3.98,'worshipper\\nfaces EAST',fontsize=7,color='#e65100',ha='center')
for p,q in [((1.05,0.7),(2.7,0.7)),((2.7,0.7),(2.7,3.2)),((2.7,3.2),(3.55,3.2)),((2.7,3.3),(2.7,4.4))]:
    ax.add_patch(FancyArrowPatch(p,q,arrowstyle='-|>',mutation_scale=12,color='#2e7d32',lw=1.5,zorder=6))
""")

for k,(title,fn,body) in V.items():
    code=head+FDEF+body+tail
    code=re.sub(r'ax\.set_title\(.*?\)\n','ax.set_title("B/H-105 Living & Dining - %s\\nclear room 3.60 x 5.80 m | dashed red = door swing | green = circulation",fontsize=11)\n'%title,code,flags=re.S) if False else code
    code=code.replace("B/H-105 - Living & Dining: Proposed 2D Furniture Layout (North-up)","B/H-105 Living & Dining - "+title).replace("living_dining_layout.png",fn)
    exec(code,{'re':re})
