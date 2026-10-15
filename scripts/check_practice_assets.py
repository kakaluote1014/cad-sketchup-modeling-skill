"""Read-only orthogonal DXF teaching-asset checks; never calls CAD or a model.

All paths and exercise dimensions are CLI arguments. JSON/Markdown are the only
outputs. Numerical epsilon is arithmetic comparison, not a construction tolerance.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import ezdxf
from PIL import Image

EPS = 1e-7
SEMANTIC = {"WALL", "ROOM_REFERENCE", "DOOR_SYMBOL", "WINDOW_SYMBOL"}


def point(v):
    return tuple(round(float(x), 8) for x in v)


def signature(entity):
    typ = entity.dxftype()
    layer = entity.dxf.layer
    if typ == "LINE":
        return (layer, typ, *sorted((point(entity.dxf.start), point(entity.dxf.end))))
    if typ == "ARC":
        return (layer, typ, point(entity.dxf.center), float(entity.dxf.radius),
                float(entity.dxf.start_angle), float(entity.dxf.end_angle),
                point(entity.dxf.extrusion))
    return (layer, typ, str(entity.dxf.all_existing_dxf_attribs()))


def inside_rect(x, y, rect):
    x0, y0, x1, y1 = rect
    return x0 < x < x1 and y0 < y < y1


def parity(x, y, lines):
    """Even-odd fill across closed outline edges, retaining shared edge parity."""
    hits = 0
    for a, b in lines:
        if (a[1] > y) != (b[1] > y):
            cross_x = a[0] + (y - a[1]) * (b[0] - a[0]) / (b[1] - a[1])
            hits += cross_x > x
    return bool(hits % 2)


def noded_graph(lines):
    """Split at all collinear endpoints; deduplicate graph edges for topology."""
    vertices = {p for line in lines for p in line}
    edges = set()
    for a, b in lines:
        axis = 0 if abs(a[1] - b[1]) < EPS else 1
        other = 1 - axis
        cuts = sorted((p for p in vertices if abs(p[other] - a[other]) < EPS
                       and min(a[axis], b[axis]) - EPS <= p[axis]
                       <= max(a[axis], b[axis]) + EPS), key=lambda p: p[axis])
        edges.update(tuple(sorted((p, q))) for p, q in zip(cuts, cuts[1:]) if p != q)
    graph = defaultdict(set)
    for a, b in edges:
        graph[a].add(b)
        graph[b].add(a)
    return {"noded_edges": len(edges), "vertices": len(graph),
            "dangling_vertices": [p for p, near in graph.items() if len(near) == 1],
            "degree_counts": dict(Counter(len(v) for v in graph.values()))}


def bounds(lines):
    pts = [p for pair in lines for p in pair]
    return [min(p[0] for p in pts), min(p[1] for p in pts),
            max(p[0] for p in pts), max(p[1] for p in pts)] if pts else None


def overlap(a, b, c, d):
    horizontal = abs(a[1] - b[1]) < EPS and abs(c[1] - d[1]) < EPS
    vertical = abs(a[0] - b[0]) < EPS and abs(c[0] - d[0]) < EPS
    if horizontal and abs(a[1] - c[1]) < EPS:
        lo, hi = max(min(a[0], b[0]), min(c[0], d[0])), min(max(a[0], b[0]), max(c[0], d[0]))
        return [[lo, a[1]], [hi, a[1]]] if hi - lo > EPS else None
    if vertical and abs(a[0] - c[0]) < EPS:
        lo, hi = max(min(a[1], b[1]), min(c[1], d[1])), min(max(a[1], b[1]), max(c[1], d[1]))
        return [[a[0], lo], [a[0], hi]] if hi - lo > EPS else None
    return None


def inspect_dxf(path, spec):
    doc = ezdxf.readfile(path)
    ents = list(doc.modelspace())
    lines = defaultdict(list)
    z_values, unsupported, invalid_arcs = [], [], []
    for e in ents:
        typ, layer = e.dxftype(), e.dxf.layer
        if typ == "LINE":
            a, b = point(e.dxf.start), point(e.dxf.end)
            lines[layer].append((a, b))
            z_values.extend((a[2], b[2]))
        elif typ == "ARC":
            z_values.append(float(e.dxf.center.z))
            if point(e.dxf.extrusion) != (0.0, 0.0, 1.0):
                invalid_arcs.append(e.dxf.handle)
        elif typ == "TEXT":
            z_values.append(float(e.dxf.insert.z))
        else:
            unsupported.append({"type": typ, "layer": layer})
    wall = lines["WALL"]
    orthogonal = all(abs(a[0] - b[0]) < EPS or abs(a[1] - b[1]) < EPS for a, b in wall)
    w, h, t = spec["width"], spec["height"], spec["thickness"]
    d0, d1 = spec["door"]
    v0, v1 = spec["window"]
    # Authoritative area relation from the brief, independent of LINE ordering/count.
    outer, room = [0, 0, w, h], [t, t, w-t, h-t]
    door, window = [d0, 0, d1, t], [w-t, v0, w, v1]
    xs = sorted({0, t, d0, d1, w-t, w, *(p[0] for pair in wall for p in pair)})
    ys = sorted({0, t, v0, v1, h-t, h, *(p[1] for pair in wall for p in pair)})
    area, mismatch = 0.0, []
    for x0, x1 in zip(xs, xs[1:]):
        for y0, y1 in zip(ys, ys[1:]):
            x, y = (x0+x1)/2, (y0+y1)/2
            occupied = parity(x, y, wall)
            expected = (inside_rect(x, y, outer) and not inside_rect(x, y, room)
                        and not inside_rect(x, y, door) and not inside_rect(x, y, window))
            if occupied:
                area += (x1-x0)*(y1-y0)
            if occupied != expected:
                mismatch.append({"cell": [x0,y0,x1,y1], "actual_wall": occupied,
                                 "expected_wall": expected})
    intersections = []
    flat = [(layer, a, b) for layer in sorted(SEMANTIC) for a, b in lines[layer]]
    for i, (la, a, b) in enumerate(flat):
        for lb, c, d in flat[i+1:]:
            if la != lb:
                segment = overlap(a, b, c, d)
                if segment:
                    intersections.append({"layers": [la, lb], "segment": segment})
    door_arc = [e for e in ents if e.dxf.layer == "DOOR_SYMBOL" and e.dxftype() == "ARC"]
    expected_arc = (d0, t, d1-d0, 0.0, 90.0)
    actual_arcs = [(float(e.dxf.center.x),float(e.dxf.center.y),float(e.dxf.radius),
                   float(e.dxf.start_angle),float(e.dxf.end_angle)) for e in door_arc]
    window_lines = lines["WINDOW_SYMBOL"]
    interior_window = sorted(a[0] for a,b in window_lines if abs(a[0]-b[0])<EPS
                             and w-t+EPS<a[0]<w-EPS
                             and sorted((a[1],b[1])) == [v0,v1])
    expected_area = w*h-(w-2*t)*(h-2*t)-(d1-d0)*t-(v1-v0)*t
    check = {
        "millimetre_units": doc.header.get("$INSUNITS") == 4,
        "metric_measurement": doc.header.get("$MEASUREMENT") == 1,
        "wall_bounds": bounds(wall) == outer,
        "room_bounds": bounds(lines["ROOM_REFERENCE"]) == room,
        "wall_axis_aligned": orthogonal,
        "all_supported_entities_z0": bool(z_values) and max(abs(z) for z in z_values)<EPS,
        "arc_plane_normal": not invalid_arcs,
        "all_entity_types_examined": not unsupported,
        "wall_region_matches_brief": not mismatch,
        "wall_area_matches_brief": abs(area-expected_area)<EPS,
        "wall_no_dangling_endpoints_after_noding": orthogonal and not noded_graph(wall)["dangling_vertices"],
        "room_closed_reference": len(lines["ROOM_REFERENCE"]) == 4 and
                                  not noded_graph(lines["ROOM_REFERENCE"])["dangling_vertices"],
        "door_arc_matches_opening": actual_arcs == [expected_arc],
        "door_leaf_matches_opening": lines["DOOR_SYMBOL"] == [((d0,t,0.0),(d0,t+d1-d0,0.0))],
        "window_bounds_match_opening": bounds(window_lines) == window,
        "window_two_interior_symbol_lines": len(interior_window) == 2,
        "semantic_layers_present": SEMANTIC <= {e.dxf.layer for e in ents},
        "semantic_entity_types": all(e.dxftype() in ({"LINE", "ARC"} if e.dxf.layer == "DOOR_SYMBOL"
                                     else {"LINE"}) for e in ents if e.dxf.layer in SEMANTIC),
    }
    audit = doc.audit()  # In-memory audit only; never save the document.
    texts = [e.dxf.text for e in ents if e.dxftype()=="TEXT"]
    return {
        "file":path.name, "sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
        "dxf_version":doc.dxfversion, "insunits":doc.header.get("$INSUNITS"),
        "measurement":doc.header.get("$MEASUREMENT"),
        "entity_count":len(ents), "types":dict(Counter(e.dxftype() for e in ents)),
        "layers":dict(Counter(e.dxf.layer for e in ents)), "texts":texts,
        "wall_bounds":bounds(wall), "room_bounds":bounds(lines["ROOM_REFERENCE"]),
        "wall_area_mm2":area, "expected_wall_area_mm2":expected_area,
        "wall_topology":noded_graph(wall) if orthogonal else None,
        "window_interior_lines_x":interior_window, "checks":check,
        "wall_region_mismatches":mismatch, "cross_layer_overlaps":intersections,
        "unsupported_entities":unsupported,
        "audit_error_count":len(audit.errors), "audit_fix_count":len(audit.fixes),
    }, Counter(signature(e) for e in ents if e.dxf.layer != "ANNOTATION")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("asset_dir",type=Path)
    p.add_argument("--width",type=float,required=True)
    p.add_argument("--height",type=float,required=True)
    p.add_argument("--thickness",type=float,required=True)
    p.add_argument("--door",nargs=2,type=float,required=True,metavar=("X0","X1"))
    p.add_argument("--window",nargs=2,type=float,required=True,metavar=("Y0","Y1"))
    p.add_argument("--wall-height",type=float,required=True)
    p.add_argument("--door-height",type=float,required=True)
    p.add_argument("--sill",type=float,required=True)
    p.add_argument("--window-height",type=float,required=True)
    p.add_argument("--out-json",type=Path,required=True)
    p.add_argument("--out-md",type=Path,required=True)
    args = p.parse_args()
    spec = {k:getattr(args,k) for k in ("width","height","thickness","door","window",
            "wall_height","door_height","sill","window_height")}
    reports, keys = [], []
    for name in ("practice-source.dxf","practice-clean-reference.dxf"):
        report, key = inspect_dxf(args.asset_dir/name,spec)
        reports.append(report)
        keys.append(key)
    image_path = args.asset_dir/"plan-reference.png"
    with Image.open(image_path) as im:
        image_report = {"size":list(im.size),"mode":im.mode,"format":im.format}
        im.verify()
    image_report["sha256"] = hashlib.sha256(image_path.read_bytes()).hexdigest()
    image_report["decode_verified"] = True
    result = {
        "timestamp_utc":datetime.now(timezone.utc).isoformat(),
        "scope":"Local static DXF geometry and PNG decode; no CAD/SU/MCP execution.",
        "expected_from_teaching_brief":spec,"arithmetic_epsilon_mm":EPS,
        "files":reports,"non_annotation_geometry_identical":keys[0]==keys[1],
        "source_has_annotations":reports[0]["layers"].get("ANNOTATION",0)>0,
        "clean_has_no_annotation_entities":reports[1]["layers"].get("ANNOTATION",0)==0,
        "image":image_report,
        "vertical_relations_from_brief_only":{
            "door_lintel_height":args.wall_height-args.door_height,
            "window_sill_height":args.sill,
            "window_lintel_height":args.wall_height-args.sill-args.window_height},
        "limits":["No CAD/SU import, DWG conversion, face generation or SKP save verified.",
                  "2D DXF does not verify real 3D opening heights or face normals.",
                  "PNG dimensions/text require separate visual inspection.",
                  "Area fill check assumes orthogonal closed WALL outlines; unsupported entities fail coverage."]
    }
    result["all_static_checks_pass"] = (all(all(r["checks"].values()) and r["audit_error_count"]==0
             and r["audit_fix_count"]==0 for r in reports)
             and result["non_annotation_geometry_identical"]
             and result["source_has_annotations"] and result["clean_has_no_annotation_entities"])
    args.out_json.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    rows = ["# 原创练习资产静态几何验收", "",
            "仅检查实际 DXF 与 PNG 文件；未调用 CAD、SU、MCP、网络、安装或配置。", "",
            "数值来自 practice.md，作为命令参数输入。算术 epsilon 不是项目施工容差。", "",
            f"脚本静态检查全部成立：{result['all_static_checks_pass']}。以下是实测证据。", "",
            "| 文件 | DXF版本 | INSUNITS | 实体数 | WALL面积 mm² |", "|---|---|---|---|---|"]
    for r in reports:
        rows.append(f"| {r['file']} | {r['dxf_version']} | {r['insunits']} | {r['entity_count']} | {r['wall_area_mm2']} |")
    rows += ["", f"- 给定外墙边界：0…{args.width:g} × 0…{args.height:g}；实际外墙与室内净边界详见 JSON。",
             "- 墙域按网格单元逐区与给定外轮廓减室内、D1、W1核对，不依赖固定面数。",
             f"- 去除 ANNOTATION 后两份实体几何一致：{result['non_annotation_geometry_identical']}。",
             f"- 原图有标注／清理参照无标注实体：{result['source_has_annotations']}／{result['clean_has_no_annotation_entities']}。",
             f"- PNG 解码成功，尺寸 {image_report['size']}，模式 {image_report['mode']}。", ""]
    for r in reports:
        rows += [f"## {r['file']}", "", f"分层计数：`{json.dumps(r['layers'],ensure_ascii=False)}`。", "",
                 f"审计错误／修复：{r['audit_error_count']}／{r['audit_fix_count']}；分割共线端点后的墙图拓扑：`{r['wall_topology']}`。", "",
                 f"跨语义层共线重叠 {len(r['cross_layer_overlaps'])} 对，逐段证据在 JSON；导入合并或封面时须保留分类意识。", "",
                 "| 检查 | 实际结果 |", "|---|---|"]
        rows.extend(f"| {k} | {v} |" for k,v in r["checks"].items())
        rows.append("")
    rows += ["## 未验证范围", "", "- CAD／天正打开、转换 DWG、SU 导入、曲线离散及共边合并。",
             "- SU 自动封面、面正反朝向、三维墙高与洞口贯通、保存可编辑 SKP。",
             "- 软件兼容性、真实学生完成能力或效率。",
             "- 高度数值只由教学依据作算术核对，不是二维 DXF 中的实测三维构件。", ""]
    args.out_md.write_text("\n".join(rows),encoding="utf-8")
    print(json.dumps({"static_checks_pass":result["all_static_checks_pass"],
                      "files":[{"file":r["file"],"checks":r["checks"],
                                "overlaps":len(r["cross_layer_overlaps"])} for r in reports],
                      "image":image_report},ensure_ascii=False,indent=2))
    return 0 if result["all_static_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
