from pathlib import Path
from html import escape
out=Path(__file__).resolve().parent


def start(width,height):
    return [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
    '<defs><marker id="arrow" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0,0 L7,3.5 L0,7" fill="#374151"/></marker></defs>',
    '<rect width="100%" height="100%" fill="white"/>']


def text(items,x,y,value,size=18,anchor='middle',color='#111827'):
    items.append(f'<text x="{x}" y="{y}" font-family="Times New Roman, serif" font-size="{size}" text-anchor="{anchor}" fill="{color}">{escape(value)}</text>')


def node(items,x,y,label,fill='#ffffff',radius=7):
    items.append(f'<circle cx="{x}" cy="{y}" r="{radius}" fill="{fill}" stroke="#374151" stroke-width="1.5"/>')
    if label:text(items,x,y-15,label)


def line(items,x1,y1,x2,y2):
    dx,dy=x2-x1,y2-y1;length=(dx*dx+dy*dy)**0.5
    items.append(f'<path d="M{x1+8*dx/length},{y1+8*dy/length} L{x2-10*dx/length},{y2-10*dy/length}" fill="none" stroke="#374151" stroke-width="1.6" marker-end="url(#arrow)"/>')


def curve(items,path):
    items.append(f'<path d="{path}" fill="none" stroke="#374151" stroke-width="1.5" marker-end="url(#arrow)"/>')


def save(name,items):
    (out/name).write_text('\n'.join(items+['</svg>']))


s=start(700,230)
points={'in1':(70,115),'in2':(285,40),'p0':(180,115),'p1':(285,115),'p2':(390,115),'p3':(495,115),'out1':(390,195),'out2':(630,115),'x':(180,195),'y':(495,40)}
arcs=[('in1','p0'),('in2','p1'),('p0','p1'),('p1','p2'),('p2','p3'),('p2','out1'),('p3','out2'),('p0','x'),('p3','y')]
for u,v in arcs:line(s,*points[u],*points[v])
labels={'in1':'incoming 1','in2':'incoming 2','p0':'s₀','p1':'s₁','p2':'s₂','p3':'s₃','out1':'outgoing 1','out2':'outgoing 2','x':'x','y':'y'}
for v,(x,y) in points.items():
    node(s,x,y,'', '#dbeafe' if v.startswith('p') else '#ffffff')
    text(s,x,y+26 if v in ['p1','p3','x','out1'] else y-15,labels[v])
assert [sum(v==n for u,v in arcs) for n in ['p0','p1','p2','p3']]==[1,2,1,1]
assert [sum(u==n for u,v in arcs) for n in ['p0','p1','p2','p3']]==[2,1,2,2]
save('binary-spine.svg',s)

s=start(720,250)
text(s,180,25,'Incidence network G',21);text(s,540,25,'Reference network H',21)
# Explicit example with one three-element clause; auxiliary taxa and paths omitted.
a={'R':(45,115),'A':(145,65),'U':(145,175),'X₁':(240,65),'X₂':(240,120),'X₃':(240,175),'B':(335,65),'V':(335,175)}
garcs=[('R','A'),('R','U'),('R','B'),('A','B')]+[e for x in ['X₁','X₂','X₃'] for e in [('A',x),('U',x),(x,'B'),(x,'V')]]
# Direct R->B and A->B take separate upper arcs to avoid intersecting vertices.
for u,v in garcs:
 if (u,v)==('R','B'):curve(s,'M45,107 C45,35 325,30 335,56')
 elif (u,v)==('A','B'):curve(s,'M151,59 C190,25 292,25 329,58')
 else:line(s,*a[u],*a[v])
for v,(x,y) in a.items():
    node(s,x,y,'' if v=='X₁' else v,'#dbeafe' if v in ['A','U'] else '#ffedd5' if v in ['B','V'] else '#ffffff')
    if v=='X₁':text(s,x,y+25,v)
b={'R':(400,115),'A':(475,65),'B':(665,65),'X₁':(570,65),'X₂':(570,120),'X₃':(570,175)}
harcs=[('R','A'),('R','B'),('A','B')]+[e for x in ['X₁','X₂','X₃'] for e in [('A',x),(x,'B')]]
for u,v in harcs:
 if (u,v)==('R','B'):curve(s,'M400,107 C400,35 655,30 665,56')
 elif (u,v)==('A','B'):curve(s,'M481,59 C520,25 622,25 659,58')
 else:line(s,*b[u],*b[v])
for v,(x,y) in b.items():
    node(s,x,y,'' if v=='X₁' else v,'#dbeafe' if v=='A' else '#ffedd5' if v=='B' else '#ffffff')
    if v=='X₁':text(s,x,y+25,v)
text(s,180,228,'U must connect to A; V must connect to B',16)
text(s,540,228,'A variable bag may remain unassigned',16)
save('incidence-reference.svg',s)

s=start(700,260)
points={'R':(55,80),'A':(350,80),'B':(645,80)}
for prefix,lo,hi in [('RA',55,350),('AB',350,645)]:
 prev='R' if prefix=='RA' else 'A'
 for i in range(3):
  x=lo+(hi-lo)*(i+1)/4;v=prefix+str(i);points[v]=(x,145);points[v+'leaf']=(x,210)
  line(s,*points[prev],*points[v]);line(s,*points[v],*points[v+'leaf']);prev=v
 line(s,*points[prev],*points['A' if prefix=='RA' else 'B'])
for u,v in [('R','A'),('A','B')]:line(s,*points[u],*points[v])
curve(s,'M55,71 C130,5 570,5 645,71')
for v,(x,y) in points.items():node(s,x,y,v if v in ['R','A','B'] else '', '#dbeafe' if v=='A' else '#ffedd5' if v=='B' else '#ffffff')
text(s,205,248,'L marked internal vertices',17);text(s,495,248,'L marked internal vertices',17)
save('separation-paths.svg',s)
print('Three vector figures written; local spine degree assertions pass. Other figures are labeled schematics.')
