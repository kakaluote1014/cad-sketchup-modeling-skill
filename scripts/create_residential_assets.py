"""Generate original residential teaching DXFs/PNG only; never control CAD/SU.

Maintainers use existing ezdxf/Pillow/CJK font; students use the files directly.
All dimensions below belong to this exercise, never to a real project default.
"""
from __future__ import annotations

import math
import os
from pathlib import Path

import ezdxf
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "skills/cad-sketchup-mcp/assets/residential"
WALLS = {
    "WALL_EXTERNAL": [
        (0, 0, 1200, 200), (2400, 0, 7500, 200), (9300, 0, 10000, 200),
        (0, 7800, 4000, 8000), (5500, 7800, 8000, 8000), (9500, 7800, 10000, 8000),
        (0, 200, 200, 5000), (0, 6500, 200, 7800), (9800, 200, 10000, 7800),
    ],
    "WALL_SHARED": [(3200, 200, 3400, 1800), (3200, 2700, 3400, 7800)],
    "WALL_INTERNAL": [(3400, 4000, 4500, 4120), (5400, 4000, 8000, 4120),
                      (8900, 4000, 9800, 4120), (6640, 4120, 6760, 7800)],
}
DOORS = [
    (0, 1200, 0, 2400, 200), (1, 3200, 1800, 3400, 2700),
    (2, 4500, 4000, 5400, 4120), (3, 8000, 4000, 8900, 4120),
    (4, 7500, 0, 9300, 200),
]
WINDOWS = [(4000, 7800, 5500, 8000), (8000, 7800, 9500, 8000), (0, 5000, 200, 6500)]
COLORS = {"WALL_EXTERNAL": 7, "WALL_SHARED": 6, "WALL_INTERNAL": 8,
          "DOOR_SYMBOL": 30, "WINDOW_SYMBOL": 4, "SLAB_BOUNDARY": 8,
          "VOID": 1, "BALCONY": 3, "STAIR_SYMBOL": 5, "ANNOTATION": 3}


def rect_segments(rect):
    x0, y0, x1, y1 = rect
    p = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    return list(zip(p, p[1:] + p[:1]))


def union_boundary(rects):
    """Grid union removes internal seams between same-layer rectangles."""
    xs = sorted({r[i] for r in rects for i in (0, 2)})
    ys = sorted({r[i] for r in rects for i in (1, 3)})
    edges = set()
    for x0, x1 in zip(xs, xs[1:]):
        for y0, y1 in zip(ys, ys[1:]):
            x, y = (x0+x1)/2, (y0+y1)/2
            if any(a < x < c and b < y < d for a, b, c, d in rects):
                for edge in rect_segments((x0, y0, x1, y1)):
                    key = tuple(sorted(edge))
                    if key in edges:
                        edges.remove(key)
                    else:
                        edges.add(key)
    return sorted(edges)


def make_dxf(annotated):
    doc = ezdxf.new("R2004", units=ezdxf.units.MM)
    doc.header["$MEASUREMENT"] = 1
    for layer, color in COLORS.items():
        doc.layers.new(layer, dxfattribs={"color": color})
    msp = doc.modelspace()

    def line(a, b, layer):
        msp.add_line((*a, 0), (*b, 0), dxfattribs={"layer": layer})

    def rect(r, layer):
        for a, b in rect_segments(r):
            line(a, b, layer)

    for layer, rects in WALLS.items():
        for a, b in union_boundary(rects):
            line(a, b, layer)
    for number, x0, y0, x1, y1 in DOORS:
        rect((x0, y0, x1, y1), "DOOR_SYMBOL")
        if number == 4:
            for y in (y0+(y1-y0)/3, y0+2*(y1-y0)/3):
                line((x0, y), (x1, y), "DOOR_SYMBOL")
        elif number == 1:
            line((x1, y0), (x1+(y1-y0), y0), "DOOR_SYMBOL")
            msp.add_arc((x1, y0, 0), y1-y0, 0, 90, dxfattribs={"layer": "DOOR_SYMBOL"})
        else:
            line((x0, y1), (x0, y1+x1-x0), "DOOR_SYMBOL")
            msp.add_arc((x0, y1, 0), x1-x0, 0, 90, dxfattribs={"layer": "DOOR_SYMBOL"})
    for r in WINDOWS:
        rect(r, "WINDOW_SYMBOL")
        x0, y0, x1, y1 = r
        for f in (1/3, 2/3):
            if x1-x0 > y1-y0:
                line((x0, y0+(y1-y0)*f), (x1, y0+(y1-y0)*f), "WINDOW_SYMBOL")
            else:
                line((x0+(x1-x0)*f, y0), (x0+(x1-x0)*f, y1), "WINDOW_SYMBOL")
    rect((0, 0, 10000, 8000), "SLAB_BOUNDARY")
    rect((400, 3600, 3000, 7100), "VOID")
    rect((6000, -1500, 10000, 0), "BALCONY")
    rect((400, 6000, 3000, 7100), "STAIR_SYMBOL")
    for x0, x1 in ((400, 1500), (1900, 3000)):
        for i in range(9):
            y = 3600+300*i
            line((x0, y), (x1, y), "STAIR_SYMBOL")
        for x in (x0, x1):
            line((x, 3600), (x, 6000), "STAIR_SYMBOL")
    for x, y0, y1 in ((950, 3900, 5700), (2450, 5700, 3900)):
        line((x, y0), (x, y1), "STAIR_SYMBOL")
        dy = -180 if y1 > y0 else 180
        for dx in (-120, 120):
            line((x, y1), (x+dx, y1+dy), "STAIR_SYMBOL")
    if annotated:
        labels = [((0, 9000), "ORIGINAL RESIDENTIAL TEACHING FRAGMENT - NOT A COMPLETE DESIGN"),
                  ((0, 8650), "mm; body=10000x8000; storey=3000; wall=2850; slab=150"),
                  ((4000, 8200), "W1/W2: 1500x1500; sill=900"),
                  ((10100, 4000), "B=8000 (body only)"),
                  ((4000, 8450), "A=10000 (body only)"),
                  ((3700, 2500), "LIVING ZONE - DO NOT EXTRUDE ROOM"),
                  ((3800, 6000), "ROOM A"), ((7600, 6000), "ROOM B"),
                  ((400, 7600), "VOID=2600x3500; stair 2x9 risers"),
                  ((6000, -2000), "BALCONY=4000x1500; separate slab/guard"),
                  ((400, 800), "D0=1200; D1/D2/D3=900; D4=1800; all H=2100"),
                  ((0, -2500), "Use residential-practice.md for opening positions and vertical dimensions.")]
        for pos, value in labels:
            msp.add_text(value, dxfattribs={"layer": "ANNOTATION", "height": 130, "insert": (*pos, 0)})
    doc.set_modelspace_vport(height=13000, center=(5500, 3500))
    path = OUT / ("residential-source.dxf" if annotated else "residential-clean-reference.dxf")
    doc.saveas(path)
    path.write_text(path.read_text(encoding="cp1252"), encoding="ascii", newline="\n")


def make_diagram():
    im = Image.new("RGB", (1920, 1440), "#edf2f5")
    d = ImageDraw.Draw(im)
    fonts = Path(os.environ["WINDIR"]) / "Fonts"
    regular, bold = fonts / "msyh.ttc", fonts / "msyhbd.ttc"
    if not regular.is_file():
        raise RuntimeError("Maintainer: existing CJK font required")

    def text(x, y, value, size=27, color="#24354a", strong=False):
        d.text((x, y), value, font=ImageFont.truetype(str(bold if strong else regular), size), fill=color)

    def p(x, y):
        return round(150+x*.085), round(1060-y*.085)

    def line(a, b, color, width=2):
        d.line((p(*a), p(*b)), fill=color, width=width)

    def box(r, fill, outline=None):
        x0, y0, x1, y1 = r
        d.rectangle((p(x0, y1), p(x1, y0)), fill=fill, outline=outline, width=3)

    text(55, 34, "住宅进阶练习：一户片段 + 楼梯交通核 + 阳台", 42, strong=True)
    text(55, 96, "原创教学示意 · 单位 mm · 非完整住宅方案 · 非软件截图 · 所有数值仅用于本练习", 25)
    d.rounded_rectangle((35, 165, 1080, 1290), radius=20, fill="white")
    d.rounded_rectangle((1105, 165, 1885, 1290), radius=20, fill="white")
    box((0, 0, 10000, 8000), "#f4f6f8")
    box((400, 3600, 3000, 7100), "#ffefec", "#c45d52")
    box((6000, -1500, 10000, 0), "#d9eee7", "#337963")
    for layer, color in (("WALL_EXTERNAL", "#52667f"), ("WALL_SHARED", "#8a6c9e"), ("WALL_INTERNAL", "#96a4b6")):
        for r in WALLS[layer]:
            box(r, color)
    for number, x0, y0, x1, y1 in DOORS:
        box((x0, y0, x1, y1), "#fff2d9", "#b97822")
        if number != 4:
            if number == 1:
                cx, cy, radius, orientation = x1, y0, y1-y0, "east"
                line((cx, cy), (cx+radius, cy), "#b97822", 2)
            else:
                cx, cy, radius, orientation = x0, y1, x1-x0, "north"
                line((cx, cy), (cx, cy+radius), "#b97822", 2)
            arc = [p(cx+radius*math.cos(math.radians(a)), cy+radius*math.sin(math.radians(a))) for a in range(0, 91, 3)]
            d.line(arc, fill="#b97822", width=2)
    for r in WINDOWS:
        box(r, "#bfe5e9", "#158799")
    for x0, x1 in ((400, 1500), (1900, 3000)):
        for i in range(9):
            line((x0, 3600+300*i), (x1, 3600+300*i), "#526da8", 2)
        for x in (x0, x1):
            line((x, 3600), (x, 6000), "#526da8", 2)
    for a, b in rect_segments((400, 6000, 3000, 7100)):
        line(a, b, "#526da8", 2)
    for x, y0, y1 in ((950, 3900, 5700), (2450, 5700, 3900)):
        line((x, y0), (x, y1), "#526da8", 4)
        dy = -180 if y1 > y0 else 180
        for dx in (-120, 120):
            line((x, y1), (x+dx, y1+dy), "#526da8", 4)
    text(200, 463, "平台", 24)
    text(505, 510, "房间 A", 29, strong=True)
    text(792, 510, "房间 B", 29, strong=True)
    text(550, 880, "起居教学区域", 32, strong=True)
    text(555, 928, "房间不拉成墙", 25)
    text(180, 857, "交通核", 27, strong=True)
    text(720, 1127, "阳台板另组", 28, "#337963", True)
    for x, y, value in ((195, 1075, "D0"), (394, 836, "D1"), (539, 775, "D2"), (833, 775, "D3"),
                        (800, 1078, "D4"), (496, 385, "W1"), (836, 385, "W2"), (73, 550, "W3")):
        text(x, y, value, 23)
    d.line((150, 335, 1000, 335), fill="#52667f", width=2)
    for x in (150, 1000):
        d.line((x, 325, x, 380), fill="#52667f", width=2)
    text(442, 283, "A = 10000", 31, strong=True)
    d.line((1040, 380, 1040, 1060), fill="#52667f", width=2)
    for y in (380, 1060):
        d.line((1000, y, 1050, y), fill="#52667f", width=2)
    text(1008, 680, "B", 23, strong=True)
    text(1000, 724, "8000", 19)
    text(65, 1220, "紫：共墙   灰：墙   橙／青：门窗符号   红框：板洞", 24)
    text(1140, 200, "先核主体两段，再做构件", 34, strong=True)
    rows = ["主体 10000 × 8000；阳台另计", "外墙／共墙 200；内墙 120", "层高 3000；墙高 2850；板厚 150", "门洞高 2100 → 门上墙 750", "窗台 900 + 窗洞 1500 + 上墙 450", "VOID：2600 × 3500，不拉高、不盖住", "阳台：4000 × 1500；栏板高 1100"]
    for i, row in enumerate(rows):
        text(1140, 270+i*60, row, 27)
    text(1140, 730, "楼梯：两跑 × 9 踢面", 32, strong=True)
    text(1140, 790, "每级高 3000/18；每跑投影 2400", 27)
    text(1140, 839, "鼻线 9 条，踏面间距 8 × 300", 27)
    d.line((1190, 1060, 1460, 1060, 1460, 960, 1725, 960, 1725, 860), fill="#526da8", width=5)
    text(1150, 1080, "本层 0", 25)
    text(1400, 1000, "平台 1500", 25)
    text(1660, 896, "上层 3000", 25)
    text(1140, 1160, "单独编组；看板洞与出梯口", 29, strong=True)
    text(1140, 1210, "竖向折线仅示高差，不是施工剖面", 24)
    text(55, 1320, "一层练习 → 人工修改后续建 → 自选三层差异练习；先保存，再进入下一任务", 31, strong=True)
    text(55, 1375, "DXF 与图片不是已完成模型；CAD/SU 导入、楼梯连通、可编辑 SKP 与学生试用待实际验证。", 25)
    im.save(OUT / "residential-reference.png")


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    make_dxf(True)
    make_dxf(False)
    make_diagram()
    print("Created 2 original residential DXFs + 1 teaching PNG; no CAD/SU calls")
