import re
g={}
src2=open('draw_vastu2.py').read()
exec(src2[:src2.index("V={}")],g)
head,tail,build=g['head'],g['tail'],g['build']
MAND=[("f(2.45,0.0,0.85,0.4,","f(3.2,3.85,0.4,0.85,'MANDIR\\n0.85x0.40\\n(closed doors)','#ffcc80',6,90,ec='#e65100')\nf(2.9,0.0,0.6,0.55,'Plant /\\nlamp\\nNE: keep\\nlight','#c8e6c9',5.5)"),
("ax.add_patch(FancyArrowPatch((2.88,1.0)","ax.add_patch(FancyArrowPatch((2.7,4.28),(3.15,4.28),arrowstyle='-|>',mutation_scale=16,color='#e65100',lw=2,zorder=6))"),
("ax.text(2.3,0.95,'worshipper","ax.text(2.55,3.95,'worshipper\\nfaces NORTH',fontsize=7,color='#e65100',ha='center')")]
V={}
V['V5']=("VASTU option 5 - mandir on dining wall (hidden from entrance), sofa","living_dining_vastu_5.png",build(MAND))
V['V6']=("VASTU option 6 - mandir on dining wall, traditional diwan","living_dining_vastu_6.png",build(MAND+[
 ("f(0.0,1.95,0.9,1.9,","f(0.0,1.95,0.8,1.9,'DIWAN 1.90x0.80\\nstorage + bolsters\\n(S wall, faces N)','#a1887f',7,90)\nf(1.05,2.1,0.5,0.5,'Arm-\\nchair','#cfd8dc',6)\nf(1.05,3.2,0.5,0.5,'Arm-\\nchair','#cfd8dc',6)"),
 ("f(1.05,2.65","pass"),
 ("ax.add_patch(Circle","ax.add_patch(Circle((1.95,2.9),0.25,fc='none',ec='#2e7d32',ls=':',lw=1.5,zorder=5))"),
 ("ax.text(1.8,2.9,'centre","ax.text(1.95,2.9,'centre\\nopen',fontsize=5.5,color='#2e7d32',ha='center',va='center',zorder=6)")]))
V['V7']=("VASTU option 7 - mandir on dining wall, sectional sofa","living_dining_vastu_7.png",build(MAND+[
 ("f(0.0,1.95,0.9,1.9,","f(0.0,1.95,0.9,1.9,'SECTIONAL leg 1.90\\n(S wall, sitters face N)','#90a4ae',7,90)\nf(0.9,3.15,0.9,0.7,'Chaise 0.9x0.7','#78909c',7)"),
 ("f(1.05,2.65","f(1.05,2.1,0.5,0.5,'Side\\ntable','#ffe0b2',6.5)"),
 ("ax.add_patch(Circle","ax.add_patch(Circle((1.95,2.75),0.25,fc='none',ec='#2e7d32',ls=':',lw=1.5,zorder=5))"),
 ("ax.text(1.8,2.9,'centre","ax.text(1.95,2.75,'centre\\nopen',fontsize=5.5,color='#2e7d32',ha='center',va='center',zorder=6)")]))
for k,(title,fn,b) in V.items():
    code=head+b+tail
    code=code.replace("B/H-105 - Living & Dining: Proposed 2D Furniture Layout (true N = right)","B/H-105 Living & Dining - "+title).replace("living_dining_layout.png",fn).replace("set_xlim(-2.6,4.6)","set_xlim(-2.6,4.8)")
    exec(code,{'re':re})
