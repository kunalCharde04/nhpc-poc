import re
src=open('draw_vastu.py').read()
body=src[src.index("body='''")+8:src.index("'''\ncode=")]
s=open('draw.py').read()
head=s[:s.index("# furniture")]; tail=s[s.index("# dims"):]
body=body.replace('\\\\n','\\n')
lines=body.split('\n')
def sub(prefix,new):
    out=[]
    for l in lines:
        out.append(new if l.startswith(prefix) else l)
    return out
def build(rep,add=''):
    ls=list(lines)
    for pre,new in rep:
        ls=[new if l.startswith(pre) else l for l in ls]
    return '\n'.join(ls)+'\n'+add
V={}
V['V2']=("VASTU option 2 - sectional sofa (S wall + chaise)","living_dining_vastu_2.png",build([
 ("f(0.0,1.95,0.9,1.9,","f(0.0,1.95,0.9,1.9,'SECTIONAL leg 1.90\\n(S wall, sitters face N)','#90a4ae',7,90)\nf(0.9,3.15,0.9,0.7,'Chaise 0.9x0.7','#78909c',7)"),
 ("f(1.05,2.65","f(1.05,2.1,0.5,0.5,'Side\\ntable','#ffe0b2',6.5)"),
 ("ax.add_patch(Circle","ax.add_patch(Circle((1.95,2.75),0.25,fc='none',ec='#2e7d32',ls=':',lw=1.5,zorder=5))"),
 ("ax.text(1.8,2.9,'centre","ax.text(1.95,2.75,'centre\\nopen',fontsize=5.5,color='#2e7d32',ha='center',va='center',zorder=6)")]))
V['V3']=("VASTU option 3 - traditional diwan + armchairs","living_dining_vastu_3.png",build([
 ("f(0.0,1.95,0.9,1.9,","f(0.0,1.95,0.8,1.9,'DIWAN 1.90x0.80\\nstorage + bolsters\\n(S wall, faces N)','#a1887f',7,90)\nf(1.05,2.1,0.5,0.5,'Arm-\\nchair','#cfd8dc',6)\nf(1.05,3.2,0.5,0.5,'Arm-\\nchair','#cfd8dc',6)"),
 ("f(1.05,2.65","pass"),
 ("ax.add_patch(Circle","ax.add_patch(Circle((1.95,2.9),0.25,fc='none',ec='#2e7d32',ls=':',lw=1.5,zorder=5))"),
 ("ax.text(1.8,2.9,'centre","ax.text(1.95,2.9,'centre\\nopen',fontsize=5.5,color='#2e7d32',ha='center',va='center',zorder=6)")]))
V['V4']=("VASTU option 4 - sofa + asan/prayer-mat zone at mandir","living_dining_vastu_4.png",build([],
 "ax.add_patch(Rectangle((2.45,0.42),0.9,0.65,fc='#fff3e0',ec='#e65100',ls='--',lw=1,zorder=2))\nax.text(2.9,0.75,'asan / mat',fontsize=6,color='#e65100',ha='center',va='center',zorder=3)"))
for k,(title,fn,b) in V.items():
    code=head+b+tail
    code=code.replace("B/H-105 - Living & Dining: Proposed 2D Furniture Layout (true N = right)","B/H-105 Living & Dining - "+title).replace("living_dining_layout.png",fn).replace("set_xlim(-2.6,4.6)","set_xlim(-2.6,4.8)")
    exec(code,{'re':re})
