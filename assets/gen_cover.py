#!/usr/bin/env python3
# DeepSeek Harness 封面 v4：白底 + 金属丝拉边科技风（无光晕），中心为 Cordis 底座
import math

W, H = 1400, 468
OX, OY = 1000, 132
TW, TH, ZH = 60, 31, 34

def iso(x, y, z=0.0):
    return (OX + (x - y) * TW, OY + (x + y) * TH - z * ZH)

def pts(seq):
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in seq)

GOLD, GOLD2, DKGOLD = "#c79a3c", "#e9cf82", "#9a751f"
INK = "#20242c"

out = []
out.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
           f'font-family="-apple-system,\'Helvetica Neue\',\'PingFang SC\',\'Segoe UI\',sans-serif">')

out.append(f'''<defs>
  <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset="0.6" stop-color="#f4f5f8"/><stop offset="1" stop-color="#eceef2"/>
  </linearGradient>
  <linearGradient id="wire" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#f6e7b0"/><stop offset="0.35" stop-color="{GOLD}"/>
    <stop offset="0.7" stop-color="{DKGOLD}"/><stop offset="1" stop-color="{GOLD2}"/>
  </linearGradient>
  <linearGradient id="wireH" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="#8a6a1f"/><stop offset="0.5" stop-color="#f6e7b0"/><stop offset="1" stop-color="{GOLD}"/>
  </linearGradient>
  <linearGradient id="topcore" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#fbf3d8"/><stop offset="1" stop-color="#f0dc9c"/>
  </linearGradient>
  <linearGradient id="topface" x1="0" y1="0" x2="0" y2="1">
    <stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#eef1f5"/>
  </linearGradient>
</defs>''')

out.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')

# 点阵网格（很淡）
out.append('<g fill="#9aa3b2" fill-opacity="0.16">')
for gy in range(0, H, 28):
    for gx in range(0, W, 28):
        out.append(f'<circle cx="{gx}" cy="{gy}" r="1"/>')
out.append('</g>')

# 金属丝背景走线（直角 + 焊盘，金色细线）
def wire(path, w=1.1, op=0.7):
    return f'<path d="{path}" fill="none" stroke="url(#wireH)" stroke-opacity="{op}" stroke-width="{w}"/>'
out.append('<g>')
for p in ["M0 92 H120 L150 122 H320", "M0 200 H70 L100 170 H230 L255 195 H360",
          "M0 330 H90 L120 360 H250", "M40 428 H180 L205 403 H330",
          "M1400 66 H1250 L1220 96 H1120", "M1400 300 H1300 L1270 270 H1180",
          "M1400 400 H1320 L1295 375 H1210"]:
    out.append(wire(p))
for x, y in [(120,92),(150,122),(320,92),(230,170),(360,195),(250,330),(330,403),
             (180,428),(1120,96),(1180,270),(1210,375)]:
    out.append(f'<rect x="{x-2.5}" y="{y-2.5}" width="5" height="5" rx="1" fill="{GOLD}" fill-opacity="0.85"/>')
out.append('</g>')

# 背景悬浮代码（很淡）
code_tokens = [(70,60,15,'cordis.yml'),(150,250,13,'ctx.effect()'),(60,300,13,'waterfall(next)'),
    (250,410,14,'agent-loop'),(120,150,12,'everything is a plugin'),(40,360,12,'SessionEvent'),
    (640,40,13,'deriveMessages()'),(900,432,13,'provider swap'),(1210,140,12,'ctx.llm'),(1250,360,12,'capability seam')]
out.append('<g font-family="ui-monospace,Menlo,Consolas,monospace" fill="#8a94a6">')
for x, y, s, t in code_tokens:
    out.append(f'<text x="{x}" y="{y}" font-size="{s}" opacity="0.26" transform="rotate(-6 {x} {y})">{t}</text>')
out.append('</g>')

# 下方堆叠层：仅金属丝描边（无填充光晕）
base = [(-0.6,-0.6),(4.6,-0.6),(4.6,4.6),(-0.6,4.6)]
for i, z in enumerate([-1.7,-1.05,-0.45]):
    op = 0.30 + i*0.18
    out.append(f'<polygon points="{pts([iso(x,y,z) for x,y in base])}" fill="none" stroke="url(#wire)" stroke-opacity="{op:.2f}" stroke-width="1.1"/>')

# 主板：极浅填充 + 金属丝描边
out.append(f'<polygon points="{pts([iso(x,y,0) for x,y in base])}" fill="#f7f8fb" fill-opacity="0.7" stroke="url(#wire)" stroke-width="2"/>')
out.append('<g stroke="url(#wireH)" stroke-opacity="0.28" stroke-width="0.9">')
for g in range(0,5):
    a,b = iso(g,-0.6,0), iso(g,4.6,0); out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    a,b = iso(-0.6,g,0), iso(4.6,g,0); out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
out.append('</g>')

CENTER = (2,2)
mods = [(2,2,'Cordis',True),(2,0,'AGENT LOOP',False),(0,2,'TOOLS',False),(4,2,'SESSION LOG',False),
        (2,4,'SANDBOX',False),(0,0,'LLM',False),(4,4,'CAP. SEAM',False)]

# 金属丝走线（crisp，无 blur）
out.append('<g>')
for cx, cy, lbl, core in mods:
    if (cx,cy)==CENTER: continue
    a,b = iso(*CENTER,0.04), iso(cx,cy,0.04)
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="url(#wireH)" stroke-width="1.6"/>')
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2
    out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="2.6" fill="{GOLD}"/>')
out.append('</g>')

def cuboid(cx, cy, core):
    half, h = 0.44, 0.46
    top=[iso(cx-half,cy-half,h),iso(cx+half,cy-half,h),iso(cx+half,cy+half,h),iso(cx-half,cy+half,h)]
    right=[iso(cx+half,cy-half,h),iso(cx+half,cy+half,h),iso(cx+half,cy+half,0),iso(cx+half,cy-half,0)]
    front=[iso(cx-half,cy+half,h),iso(cx+half,cy+half,h),iso(cx+half,cy+half,0),iso(cx-half,cy+half,0)]
    tface='url(#topcore)' if core else 'url(#topface)'
    rface='#efe2b8' if core else '#dfe3ea'
    fface='#e6d5a0' if core else '#d4d9e1'
    sw = 2.2 if core else 1.3
    s=[]
    s.append(f'<polygon points="{pts(front)}" fill="{fface}" stroke="url(#wire)" stroke-width="{sw*0.6:.1f}"/>')
    s.append(f'<polygon points="{pts(right)}" fill="{rface}" stroke="url(#wire)" stroke-width="{sw*0.6:.1f}"/>')
    s.append(f'<polygon points="{pts(top)}" fill="{tface}" stroke="url(#wire)" stroke-width="{sw}"/>')
    return "".join(s)

for cx, cy, lbl, core in sorted(mods, key=lambda m:(m[0]+m[1])):
    out.append(cuboid(cx,cy,core))

# 标签
out.append('<g font-family="ui-monospace,Menlo,Consolas,monospace">')
for cx, cy, lbl, core in mods:
    px, py = iso(cx,cy,0.46); py -= 18
    fs = 16 if core else 12
    w = len(lbl)*(fs*0.64)+20
    if core: bg,tc,sc,sw = "#f3d98a","#2a1e05","url(#wire)",1.6
    else:    bg,tc,sc,sw = "#ffffff","#3a4150","url(#wire)",1.2
    out.append(f'<rect x="{px-w/2:.1f}" y="{py-fs:.1f}" width="{w:.1f}" height="{fs+10:.1f}" rx="{(fs+10)/2:.1f}" fill="{bg}" stroke="{sc}" stroke-width="{sw}"/>')
    out.append(f'<text x="{px:.1f}" y="{py+1:.1f}" text-anchor="middle" font-size="{fs}" font-weight="700" fill="{tc}">{lbl}</text>')
out.append('</g>')

# 左侧标题
out.append(f'''
  <g>
    <rect x="72" y="120" width="50" height="50" rx="12" fill="none" stroke="url(#wire)" stroke-width="2.6"/>
    <text x="97" y="156" text-anchor="middle" font-size="28" font-weight="800" fill="{INK}">D</text>
    <text x="140" y="157" font-size="30" font-weight="600" fill="{GOLD}" letter-spacing="7">dsh</text>
    <text x="70" y="238" font-size="66" font-weight="800" fill="{INK}">DeepSeek Harness</text>
    <text x="72" y="306" font-size="66" font-weight="800" fill="{INK}">Source Analysis</text>
    <text x="76" y="356" font-size="24" fill="#5b6472">源码深度解析 · Deep Dive into Agent-Harness Engineering</text>
    <rect x="76" y="378" width="470" height="2.5" fill="url(#wireH)"/>
    <text x="76" y="410" font-size="18" fill="#7b8493" font-family="ui-monospace,Menlo,monospace">Everything is a Plugin · Cordis 时空可组合 · 能力接缝可替换</text>
  </g>''')

out.append(f'<text x="{W-28}" y="{H-22}" text-anchor="end" font-size="17" fill="#8a94a6" font-family="ui-monospace,Menlo,monospace">xiaonan.cs@gmail.com</text>')

# 金属丝拉边：整体细金框
out.append(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" rx="14" fill="none" stroke="url(#wire)" stroke-width="1.6" stroke-opacity="0.8"/>')
out.append('</svg>')
open('cover.svg','w').write("\n".join(out))
print("wrote cover.svg")
