#!/usr/bin/env python3
# 封面 v5：白底 + 金属丝科技风（不变），基于论文《时空可组合性》加复杂度：
# Cordis 插件板(更密) + 生命周期环(Inactive/Reloading/Active/Unloading) + 时空两维轴
# + 可逆effect/响应式coeffect + 背景公式(∂Γ / Γ∞ / effect / σ|=d / notify)
import math
W, H = 1400, 468
OX, OY = 980, 120
TW, TH, ZH = 56, 29, 34
def iso(x, y, z=0.0): return (OX + (x - y) * TW, OY + (x + y) * TH - z * ZH)
def pts(seq): return " ".join(f"{px:.1f},{py:.1f}" for px, py in seq)
GOLD, GOLD2, DKGOLD, INK = "#c79a3c", "#e9cf82", "#9a751f", "#20242c"
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
  <linearGradient id="topcore" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fbf3d8"/><stop offset="1" stop-color="#f0dc9c"/></linearGradient>
  <linearGradient id="topface" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#eef1f5"/></linearGradient>
  <marker id="ah" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6z" fill="{GOLD}"/></marker>
</defs>''')
out.append(f'<rect width="{W}" height="{H}" fill="url(#bg)"/>')
# 点阵
out.append('<g fill="#9aa3b2" fill-opacity="0.15">')
for gy in range(0, H, 28):
    for gx in range(0, W, 28): out.append(f'<circle cx="{gx}" cy="{gy}" r="1"/>')
out.append('</g>')
# 背景金属丝走线
def wireln(path, w=1.1, op=0.6): return f'<path d="{path}" fill="none" stroke="url(#wireH)" stroke-opacity="{op}" stroke-width="{w}"/>'
out.append('<g>')
for p in ["M0 88 H110 L140 118 H300","M0 210 H70 L100 180 H230","M0 340 H90 L120 368 H250",
          "M40 430 H170 L196 404 H320","M1400 60 H1250 L1220 90 H1120","M1400 300 H1300 L1270 272 H1180","M1400 408 H1320 L1296 384 H1210"]:
    out.append(wireln(p))
for x,y in [(110,88),(140,118),(300,88),(230,180),(250,368),(320,404),(1120,90),(1180,272),(1210,384)]:
    out.append(f'<rect x="{x-2.3}" y="{y-2.3}" width="4.6" height="4.6" rx="1" fill="{GOLD}" fill-opacity="0.8"/>')
out.append('</g>')
# 背景论文公式 / 术语（淡金）
math_tokens = [
    (60,58,15,'∂Γ := Γ × (Γ→Γ)'),(150,250,13,'ctx.effect()'),(56,300,13,'revertible effect'),
    (250,412,13,'reactive coeffect'),(120,150,12,'Γ∞ := μΓ. Γ×(Γ→Γ)×Σ'),(40,360,12,'σ |= d'),
    (300,92,12,'cordis.yml'),(210,342,12,'notify → activating'),(150,196,12,'f ∘ g  (LIFO φ⁻¹)'),
    (628,40,13,'effect : Γ → Γ × (Γ→Γ)'),(900,432,12,'provider swap'),(1170,140,12,'Preservation · Progress · Confluence'),
    (1210,352,12,'L-Reload / L-Unload'),
]
out.append('<g font-family="ui-monospace,Menlo,Consolas,monospace" fill="#8a7a4a">')
for x,y,s,t in math_tokens:
    out.append(f'<text x="{x}" y="{y}" font-size="{s}" opacity="0.28" transform="rotate(-5 {x} {y})">{t}</text>')
out.append('</g>')

# ---- 插件板（更密：中心 Cordis + 8 模块）----
base=[(-0.6,-0.6),(4.6,-0.6),(4.6,4.6),(-0.6,4.6)]
for i,z in enumerate([-1.7,-1.05,-0.45]):
    op=0.11+i*0.09
    out.append(f'<polygon points="{pts([iso(x,y,z) for x,y in base])}" fill="none" stroke="url(#wire)" stroke-opacity="{op:.2f}" stroke-width="1.1"/>')
out.append(f'<polygon points="{pts([iso(x,y,0) for x,y in base])}" fill="#f7f8fb" fill-opacity="0.65" stroke="url(#wire)" stroke-width="1.8"/>')
out.append('<g stroke="url(#wireH)" stroke-opacity="0.24" stroke-width="0.9">')
for g in range(0,5):
    a,b=iso(g,-0.6,0),iso(g,4.6,0); out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
    a,b=iso(-0.6,g,0),iso(4.6,g,0); out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}"/>')
out.append('</g>')
CENTER=(2,2)
mods=[(2,2,'Cordis',True),(2,0,'AGENT LOOP',False),(0,2,'TOOLS',False),(4,2,'SESSION',False),
      (2,4,'SANDBOX',False),(0,0,'LLM',False),(4,4,'FS / PTY',False),(0,4,'SKILL',False),(4,0,'MCP',False)]
# 走线
out.append('<g>')
for cx,cy,lbl,core in mods:
    if (cx,cy)==CENTER: continue
    a,b=iso(*CENTER,0.04),iso(cx,cy,0.04)
    out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="url(#wireH)" stroke-width="1.5"/>')
    mx,my=(a[0]+b[0])/2,(a[1]+b[1])/2; out.append(f'<circle cx="{mx:.1f}" cy="{my:.1f}" r="2.4" fill="{GOLD}"/>')
# provider swap 虚线到 Remote
a=iso(4,4,0.04); rmt=(a[0]+70,a[1]+70)
out.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{rmt[0]:.1f}" y2="{rmt[1]:.1f}" stroke="{DKGOLD}" stroke-width="1.6" stroke-dasharray="6 5"/>')
out.append('</g>')
def cuboid(cx,cy,core):
    half,h=0.42,0.46
    top=[iso(cx-half,cy-half,h),iso(cx+half,cy-half,h),iso(cx+half,cy+half,h),iso(cx-half,cy+half,h)]
    right=[iso(cx+half,cy-half,h),iso(cx+half,cy+half,h),iso(cx+half,cy+half,0),iso(cx+half,cy-half,0)]
    front=[iso(cx-half,cy+half,h),iso(cx+half,cy+half,h),iso(cx+half,cy+half,0),iso(cx-half,cy+half,0)]
    tf='url(#topcore)' if core else 'url(#topface)'
    rf='#efe2b8' if core else '#c2c7d0'; ff='#e6d5a0' if core else '#b3b9c3'; sw=2.2 if core else 1.2
    return (f'<polygon points="{pts(front)}" fill="{ff}" stroke="url(#wire)" stroke-width="{sw*0.6:.1f}"/>'
            f'<polygon points="{pts(right)}" fill="{rf}" stroke="url(#wire)" stroke-width="{sw*0.6:.1f}"/>'
            f'<polygon points="{pts(top)}" fill="{tf}" stroke="url(#wire)" stroke-width="{sw}"/>')
for cx,cy,lbl,core in sorted(mods,key=lambda m:(m[0]+m[1])): out.append(cuboid(cx,cy,core))
# Remote 节点（虚线金框小块）
out.append(f'<rect x="{rmt[0]-46:.1f}" y="{rmt[1]-14:.1f}" width="92" height="26" rx="13" fill="#ffffff" stroke="{DKGOLD}" stroke-width="1.2" stroke-dasharray="5 4"/>')
out.append(f'<text x="{rmt[0]:.1f}" y="{rmt[1]+4:.1f}" text-anchor="middle" font-size="12" font-weight="700" fill="{DKGOLD}" font-family="ui-monospace,Menlo,monospace">Remote · E2B</text>')
# 标签
out.append('<g font-family="ui-monospace,Menlo,Consolas,monospace">')
for cx,cy,lbl,core in mods:
    px,py=iso(cx,cy,0.46); py-=18; fs=15 if core else 11
    w=len(lbl)*(fs*0.62)+18
    bg,tc=("#f3d98a","#2a1e05") if core else ("#ffffff","#3a4150")
    out.append(f'<rect x="{px-w/2:.1f}" y="{py-fs:.1f}" width="{w:.1f}" height="{fs+9:.1f}" rx="{(fs+9)/2:.1f}" fill="{bg}" stroke="url(#wire)" stroke-width="1.1"/>')
    out.append(f'<text x="{px:.1f}" y="{py+1:.1f}" text-anchor="middle" font-size="{fs}" font-weight="700" fill="{tc}">{lbl}</text>')
out.append('</g>')

# ---- 时空两维轴（板上方两条金箭头 + 标签）----
tl=iso(-0.6,-0.6,0); tr=iso(4.6,-0.6,0); ll=iso(-0.6,4.6,0)
out.append(f'<line x1="{tl[0]:.0f}" y1="{tl[1]-10:.0f}" x2="{tr[0]:.0f}" y2="{tr[1]-10:.0f}" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#ah)" opacity="0.85"/>')
out.append(f'<text x="{(tl[0]+tr[0])/2:.0f}" y="{tr[1]-16:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="{DKGOLD}">时间维 · 可逆 effect（φ⁻¹ 回滚）</text>')
out.append(f'<line x1="{tl[0]-10:.0f}" y1="{tl[1]:.0f}" x2="{ll[0]-10:.0f}" y2="{ll[1]:.0f}" stroke="{GOLD}" stroke-width="1.4" marker-end="url(#ah)" opacity="0.85"/>')
out.append(f'<text x="{tl[0]-16:.0f}" y="{(tl[1]+ll[1])/2:.0f}" text-anchor="middle" font-size="13" font-weight="700" fill="{DKGOLD}" transform="rotate(-90 {tl[0]-16:.0f} {(tl[1]+ll[1])/2:.0f})">空间维 · 响应式 coeffect（notify）</text>')

# ---- 生命周期环（右上角小母题，论文 Fig1/2）----
lx,ly,r=1300,86,40
ring=[('Inactive',-90),('Reloading',0),('Active',90),('Unloading',180)]
import math as _m
pos={}
for name,ang in ring:
    a=_m.radians(ang); pos[name]=(lx+r*_m.cos(a), ly+r*_m.sin(a))
order=['Inactive','Reloading','Active','Unloading','Inactive']
for i in range(4):
    p1=pos[order[i]]; p2=pos[order[i+1]]
    out.append(f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="{GOLD}" stroke-width="1.3" marker-end="url(#ah)" opacity="0.8"/>')
for name,(px,py) in pos.items():
    core = name in ('Reloading','Unloading')
    out.append(f'<circle cx="{px:.1f}" cy="{py:.1f}" r="6" fill="{"#f3d98a" if core else "#ffffff"}" stroke="url(#wire)" stroke-width="1.3"/>')
    out.append(f'<text x="{px:.1f}" y="{py-10:.1f}" text-anchor="middle" font-size="10" fill="#5b4a1f" font-family="ui-monospace,Menlo,monospace">{name}</text>')
out.append(f'<text x="{lx:.0f}" y="{ly+58:.0f}" text-anchor="middle" font-size="11" fill="{DKGOLD}">component lifecycle</text>')

# ---- 左侧标题（不变）----
out.append(f'''
  <g>
    <rect x="66" y="118" width="48" height="48" rx="12" fill="none" stroke="url(#wire)" stroke-width="2.6"/>
    <text x="90" y="152" text-anchor="middle" font-size="27" font-weight="800" fill="{INK}">D</text>
    <text x="130" y="153" font-size="29" font-weight="600" fill="{GOLD}" letter-spacing="7">dsh</text>
    <text x="64" y="232" font-size="62" font-weight="800" fill="{INK}">DeepSeek Harness</text>
    <text x="66" y="298" font-size="62" font-weight="800" fill="{INK}">Source Analysis</text>
    <text x="70" y="346" font-size="22" fill="#5b6472">源码深度解析 · Deep Dive into Agent-Harness Engineering</text>
    <rect x="70" y="366" width="470" height="2.5" fill="url(#wireH)"/>
    <text x="70" y="396" font-size="16" fill="#7b8493" font-family="ui-monospace,Menlo,monospace">Everything is a Plugin · 时空可组合性 · 可逆 effect ⊕ 响应式 coeffect</text>
    <text x="70" y="420" font-size="13" fill="#9a8a5a" font-family="ui-monospace,Menlo,monospace">Cordis 底座 · ∂Γ / Γ∞ · Preservation·Progress·Confluence</text>
  </g>''')
out.append(f'<text x="{W-26}" y="{H-20}" text-anchor="end" font-size="16" fill="#8a94a6" font-family="ui-monospace,Menlo,monospace">xiaonan.cs@gmail.com</text>')
out.append(f'<rect x="12" y="12" width="{W-24}" height="{H-24}" rx="14" fill="none" stroke="url(#wire)" stroke-width="1.6" stroke-opacity="0.8"/>')
out.append('</svg>')
open('cover.svg','w').write("\n".join(out)); print("wrote cover.svg (v5)")
