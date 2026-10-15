"""Create our synthetic teaching DXF and diagram; never connect to CAD/SU.

Optional maintainer dependencies: existing ezdxf and Pillow. Students use the
generated files directly and do not need to run this script.
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import ezdxf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skills/cad-sketchup-mcp/assets/practice"
# Exercise facts only. Never import these values as project defaults.
W, D, T, H = 6000, 4200, 180, 2800
DOOR_X, DOOR_W, DOOR_H = 900, 900, 2100
WINDOW_Y, WINDOW_W, WINDOW_SILL, WINDOW_H = 1500, 1500, 900, 1200
WALLS = [
    (0, D-T, W, D), (0, 0, T, D-T),
    (T, 0, DOOR_X, T), (DOOR_X+DOOR_W, 0, W-T, T),
    (W-T, 0, W, WINDOW_Y), (W-T, WINDOW_Y+WINDOW_W, W, D-T),
]


def rect_lines(msp, rect, layer):
    x1, y1, x2, y2 = rect
    pts = [(x1,y1,0),(x2,y1,0),(x2,y2,0),(x1,y2,0)]
    for a, b in zip(pts, pts[1:]+pts[:1]):
        msp.add_line(a,b,dxfattribs={"layer":layer})


def create_dxf(annotated: bool) -> None:
    doc = ezdxf.new("R2004", units=ezdxf.units.MM)
    doc.header["$MEASUREMENT"] = 1
    doc.header["$LUNITS"] = 2
    for layer, color in [("WALL",7),("DOOR_SYMBOL",30),("WINDOW_SYMBOL",4),
                         ("ROOM_REFERENCE",8),("ANNOTATION",3)]:
        doc.layers.new(layer,dxfattribs={"color":color})
    msp = doc.modelspace()
    for rect in WALLS:
        rect_lines(msp,rect,"WALL")
    rect_lines(msp,(T,T,W-T,D-T),"ROOM_REFERENCE")
    msp.add_line((DOOR_X,T,0),(DOOR_X,T+DOOR_W,0),dxfattribs={"layer":"DOOR_SYMBOL"})
    msp.add_arc((DOOR_X,T,0),DOOR_W,0,90,dxfattribs={"layer":"DOOR_SYMBOL"})
    rect_lines(msp,(W-T,WINDOW_Y,W,WINDOW_Y+WINDOW_W),"WINDOW_SYMBOL")
    for x in [W-T+T/3,W-T+2*T/3]:
        msp.add_line((x,WINDOW_Y,0),(x,WINDOW_Y+WINDOW_W,0),dxfattribs={"layer":"WINDOW_SYMBOL"})
    if annotated:
        labels = [
            ((0,D+700),"SYNTHETIC TEACHING EXERCISE - NOT A REAL PROJECT"),
            ((0,D+430),"All dimensions in mm; not universal project defaults."),
            ((900,D+170),"A=6000 mm (outer X)"),
            ((6500,3300),"B=4200 mm (outer Y)"),
            ((6500,2800),"T=180 mm; H=2800 mm"),
            ((DOOR_X,-520),"D1: width=900; height=2100; left x=900"),
            ((6500,2100),"W1: width=1500; height=1200"),
            ((6500,1800),"sill=900; bottom y=1500"),
            ((1700,2100),"ROOM REFERENCE - DO NOT EXTRUDE"),
        ]
        for pos,label in labels:
            msp.add_text(label,dxfattribs={"layer":"ANNOTATION","height":120,"insert":(*pos,0)})
        def dim(a,b,offset):
            oa=(a[0]+offset[0],a[1]+offset[1],0)
            ob=(b[0]+offset[0],b[1]+offset[1],0)
            for p,q in [(a,oa),(b,ob),(oa,ob)]:
                msp.add_line(p,q,dxfattribs={"layer":"ANNOTATION"})
            for p in [oa,ob]:
                msp.add_line((p[0]-60,p[1]-60,0),(p[0]+60,p[1]+60,0),dxfattribs={"layer":"ANNOTATION"})
        dim((0,D,0),(W,D,0),(0,160))
        dim((W,0,0),(W,D,0),(350,0))
    doc.set_modelspace_vport(height=6500,center=(4000,2000))
    name = "practice-source.dxf" if annotated else "practice-clean-reference.dxf"
    doc.saveas(OUT/name)
    # Canonical line endings also make tracked text and package bytes agree.
    path=OUT/name
    path.write_text(path.read_text(encoding="cp1252"),encoding="ascii",newline="\n")


def create_diagram() -> None:
    image = Image.new("RGB",(1500,1140),"#f5f7fa")
    draw=ImageDraw.Draw(image)
    font_dir=Path(os.environ["WINDIR"])/"Fonts"
    regular=font_dir/"msyh.ttc"
    bold=font_dir/"msyhbd.ttc"
    if not regular.is_file():
        raise RuntimeError("Maintainer: provide a CJK font before generating the diagram")
    def text(x,y,value,size=24,color="#263445",strong=False):
        draw.text((x,y),value,font=ImageFont.truetype(str(bold if strong else regular),size),fill=color)
    def line(a,b,color="#536374",width=2):
        draw.line([a,b],fill=color,width=width)
    text(50,30,"第一次练习：一间房、一个门洞、一个窗洞",38,strong=True)
    text(50,87,"原创教学示意 · 单位 mm · 不是软件界面或 SketchUp 截图",23,"#626f80")
    draw.rounded_rectangle((36,140,952,739),radius=18,fill="white")
    draw.rounded_rectangle((980,140,1464,739),radius=18,fill="white")
    s=.115
    ox,oy=130,670
    def point(x,y): return (round(ox+x*s),round(oy-y*s))
    def rect(r,color,outline=None):
        x1,y1,x2,y2=r
        draw.rectangle((point(x1,y2),point(x2,y1)),fill=color,outline=outline,width=2)
    rect((T,T,W-T,D-T),"#edf2f7")
    for r in WALLS: rect(r,"#7c8fa6","#34465c")
    for x in [W-T,W-T+T/3,W-T+2*T/3,W]:
        line(point(x,WINDOW_Y),point(x,WINDOW_Y+WINDOW_W),"#0a8d9e",3)
    for y in [WINDOW_Y,WINDOW_Y+WINDOW_W]:
        line(point(W-T,y),point(W,y),"#0a8d9e",3)
    line(point(DOOR_X,T),point(DOOR_X,T+DOOR_W),"#d27917",3)
    arc=[point(DOOR_X+DOOR_W*math.cos(math.radians(a)),T+DOOR_W*math.sin(math.radians(a))) for a in range(0,91,3)]
    draw.line(arc,fill="#d27917",width=3)
    # Reference dimensions use the outer wall endpoints, not text extents.
    ay=165
    line((ox,ay),(ox+W*s,ay))
    for x in [ox,ox+W*s]:
        line((x,ay-8),(x,ay+8)); line((x,ay+8),(x,oy-D*s))
    draw.rectangle((346,143,535,181),fill="white")
    text(365,147,"A = 6000",24,strong=True)
    bx=855
    line((bx,oy),(bx,oy-D*s))
    for y in [oy,oy-D*s]:
        line((bx-8,y),(bx+8,y)); line((ox+W*s,y),(bx-8,y))
    text(860,386,"B",24,strong=True); text(845,425,"4200",21)
    text(355,405,"房间区域",29,strong=True)
    text(317,450,"不要把地面一起拉高",23,"#68788d")
    text(250,690,"D1",22,"#b76a12",True)
    text(754,335,"W1",22,"#0a8d9e",True)
    text(92,690,"(0,0)",18,"#68788d"); text(808,690,"X →",18)
    text(68,199,"Y ↑",18)
    text(1005,164,"仅适用于本练习",28,strong=True)
    rows=["外轮廓：6000 × 4200","墙厚：180；墙高：2800",
          "D1：门洞宽 900，高 2100","门洞左端：X = 900",
          "W1：窗洞宽 1500，高 1200","窗台：距本层底 900",
          "窗洞下端：Y = 1500"]
    for i,row in enumerate(rows): text(1005,224+i*48,row,23)
    text(1005,598,"灰色：墙体　青色：窗符号",21)
    text(1005,637,"橙色：开门示意，不建成墙",21)
    text(1005,685,"截图不代替实际尺寸测量",20,"#68788d")
    draw.rounded_rectangle((36,768,1464,1057),radius=18,fill="white")
    text(59,784,"洞口竖向检查：先留空，再分别补上下墙",27,strong=True)
    zscale=.060; top=855; bottom=top+H*zscale
    def opening(x,width,sill,height,color):
        right=x+width*zscale
        draw.rectangle((x,top,right,bottom),fill="#7c8fa6",outline="#34465c",width=2)
        hole_top=bottom-(sill+height)*zscale; hole_bottom=bottom-sill*zscale
        draw.rectangle((x,hole_top,right,hole_bottom),fill="white",outline=color,width=3)
        return right,hole_top,hole_bottom
    r,ht,hb=opening(103,DOOR_W,0,DOOR_H,"#d27917")
    text(184,852,"D1：门上墙 700",24,strong=True)
    text(184,905,"门洞高 2100",22)
    text(184,950,"门洞下方不补窗台墙",21,"#68788d")
    r,ht,hb=opening(726,WINDOW_W,WINDOW_SILL,WINDOW_H,"#0a8d9e")
    text(852,849,"W1：窗上墙 700",24,strong=True)
    text(852,900,"窗洞高 1200",22)
    text(852,950,"窗台墙高 900",24,strong=True)
    text(50,1080,"先查底图与目标 → 墙体样板 → 同类墙 → 洞口上下墙 → 保存可编辑 SKP",24,strong=True)
    image.save(OUT/"plan-reference.png")


def main():
    OUT.mkdir(parents=True,exist_ok=True)
    create_dxf(True)
    create_dxf(False)
    create_diagram()
    print("Created: 2 editable synthetic DXF files and 1 teaching diagram; no CAD/SU calls")


if __name__ == "__main__":
    main()
