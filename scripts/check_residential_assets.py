"""Read-only independent static checks against the residential teaching brief.

No generator imports, CAD/SU/MCP, install or network. Corruption probes modify
in-memory documents only. Vertical dimensions are not measured from 2D DXFs.
"""
from __future__ import annotations

from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

import ezdxf
from PIL import Image

from check_practice_assets import bounds, inside_rect, noded_graph, parity, point, signature

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "skills/cad-sketchup-mcp/assets/residential"
EPS = 1e-7
WALL_LAYERS = {"WALL_EXTERNAL", "WALL_SHARED", "WALL_INTERNAL"}


def key(a, b):
    return tuple(sorted((tuple(a), tuple(b))))


def rect_edges(rect):
    a, b, c, d = rect
    pts = [(a, b, 0.), (c, b, 0.), (c, d, 0.), (a, d, 0.)]
    return Counter(key(p, q) for p, q in zip(pts, pts[1:]+pts[:1]))


def expected_wall(layer, x, y):
    r = lambda box: inside_rect(x, y, box)
    if layer == "WALL_EXTERNAL":
        return (r((0, 0, 10000, 8000)) and not r((200, 200, 9800, 7800))
                and not any(r(b) for b in ((1200, 0, 2400, 200), (7500, 0, 9300, 200),
                    (4000, 7800, 5500, 8000), (8000, 7800, 9500, 8000), (0, 5000, 200, 6500))))
    if layer == "WALL_SHARED":
        return r((3200, 200, 3400, 7800)) and not r((3200, 1800, 3400, 2700))
    return ((r((3400, 4000, 9800, 4120)) and not r((4500, 4000, 5400, 4120))
             and not r((8000, 4000, 8900, 4120))) or r((6640, 4120, 6760, 7800)))


def inspect(doc):
    entities = list(doc.modelspace())
    lines = defaultdict(list)
    z_values, types_ok, arcs_ok = [], True, True
    for e in entities:
        typ = e.dxftype()
        if typ == "LINE":
            a, b = point(e.dxf.start), point(e.dxf.end)
            lines[e.dxf.layer].append((a, b))
            z_values.extend((a[2], b[2]))
        elif typ == "ARC":
            z_values.append(float(e.dxf.center.z))
            arcs_ok &= point(e.dxf.extrusion) == (0., 0., 1.)
        elif typ == "TEXT":
            z_values.append(float(e.dxf.insert.z))
        else:
            types_ok = False
    edges = {layer: Counter(key(a, b) for a, b in pairs) for layer, pairs in lines.items()}
    checks = {
        "r2004_mm": doc.dxfversion == "AC1018" and doc.header.get("$INSUNITS") == 4,
        "metric": doc.header.get("$MEASUREMENT") == 1,
        "supported_types": types_ok,
        "coplanar_z0": bool(z_values) and all(abs(z) < EPS for z in z_values),
        "arc_normals": arcs_ok,
        "body_controls_10000_8000": bounds(sum((lines[k] for k in WALL_LAYERS), [])) == [0, 0, 10000, 8000],
    }
    areas, mismatches = {}, {}
    # Expected boundaries plus all actual endpoints detect shifted edges and missing areas.
    base_x = {0, 200, 1200, 2400, 3200, 3400, 4000, 4500, 5400, 5500, 6640, 6760, 7500, 8000, 8900, 9300, 9500, 9800, 10000}
    base_y = {0, 200, 1800, 2700, 4000, 4120, 5000, 6500, 7800, 8000}
    for layer in sorted(WALL_LAYERS):
        pairs = lines[layer]
        xs = sorted(base_x | {p[0] for ab in pairs for p in ab})
        ys = sorted(base_y | {p[1] for ab in pairs for p in ab})
        actual_area, wrong = 0, []
        for x0, x1 in zip(xs, xs[1:]):
            for y0, y1 in zip(ys, ys[1:]):
                x, y = (x0+x1)/2, (y0+y1)/2
                actual, expected = parity(x, y, pairs), expected_wall(layer, x, y)
                if actual:
                    actual_area += (x1-x0)*(y1-y0)
                if actual != expected:
                    wrong.append([x0, y0, x1, y1])
        checks[f"{layer}_region"] = not wrong
        checks[f"{layer}_closed_orthogonal"] = bool(pairs) and all(
            abs(a[0]-b[0]) < EPS or abs(a[1]-b[1]) < EPS for a, b in pairs
        ) and not noded_graph(pairs)["dangling_vertices"]
        checks[f"{layer}_no_duplicate_edges"] = all(n == 1 for n in edges.get(layer, {}).values())
        areas[layer], mismatches[layer] = actual_area, wrong
    for layer, rect in (("SLAB_BOUNDARY", (0, 0, 10000, 8000)),
                        ("VOID", (400, 3600, 3000, 7100)),
                        ("BALCONY", (6000, -1500, 10000, 0))):
        checks[f"{layer}_exact_outline"] = edges.get(layer) == rect_edges(rect)
    door_edges = Counter()
    for rect in ((1200, 0, 2400, 200), (3200, 1800, 3400, 2700),
                 (4500, 4000, 5400, 4120), (8000, 4000, 8900, 4120), (7500, 0, 9300, 200)):
        door_edges.update(rect_edges(rect))
    checks["all_five_door_boundaries"] = not (door_edges - edges.get("DOOR_SYMBOL", Counter()))
    win_edges = Counter()
    for rect in ((4000, 7800, 5500, 8000), (8000, 7800, 9500, 8000), (0, 5000, 200, 6500)):
        win_edges.update(rect_edges(rect))
    checks["all_three_window_boundaries"] = not (win_edges - edges.get("WINDOW_SYMBOL", Counter()))
    noses = Counter(key((a, 3600+300*i, 0.), (b, 3600+300*i, 0.))
                    for a, b in ((400, 1500), (1900, 3000)) for i in range(9))
    actual_noses = Counter({k: v for k, v in edges.get("STAIR_SYMBOL", {}).items()
                           if k[0][1] == k[1][1] and abs(k[0][0]-k[1][0]) == 1100})
    checks["two_flights_nine_nose_lines_each"] = actual_noses == noses
    checks["middle_landing_outline"] = not (rect_edges((400, 6000, 3000, 7100)) - edges.get("STAIR_SYMBOL", Counter()))
    audit = doc.audit()  # in memory; no save
    checks["dxf_audit_no_errors_or_fixes"] = not audit.errors and not audit.fixes
    return {"checks": checks, "pass": all(checks.values()), "entity_count": len(entities),
            "layers": dict(Counter(e.dxf.layer for e in entities)), "wall_area_mm2": areas,
            "mismatched_cells": mismatches,
            "audit_errors": len(audit.errors), "audit_fixes": len(audit.fixes)}, Counter(
                signature(e) for e in entities if e.dxf.layer != "ANNOTATION")


def corruption_probes(path):
    result = []
    for case in ("wrong_units", "missing_wall_edge", "missing_void_edge", "shifted_balcony",
                 "missing_stair_nose", "shifted_door_boundary", "noncoplanar_wall"):
        doc = ezdxf.readfile(path)
        msp = doc.modelspace()
        def first_line(layer):
            return next(e for e in msp if e.dxftype() == "LINE" and e.dxf.layer == layer)
        if case == "wrong_units":
            doc.header["$INSUNITS"] = 1
        elif case.startswith("missing_"):
            layer = {"missing_wall_edge": "WALL_SHARED", "missing_void_edge": "VOID",
                     "missing_stair_nose": "STAIR_SYMBOL"}[case]
            e = (next(e for e in msp if e.dxftype() == "LINE" and e.dxf.layer == layer
                      and abs(e.dxf.start.x-e.dxf.end.x) == 1100) if case == "missing_stair_nose"
                 else first_line(layer))
            msp.delete_entity(e)
        else:
            layer = {"shifted_balcony": "BALCONY", "shifted_door_boundary": "DOOR_SYMBOL",
                     "noncoplanar_wall": "WALL_EXTERNAL"}[case]
            e = first_line(layer)
            e.translate(0, 0, 10) if case == "noncoplanar_wall" else e.translate(100, 0, 0)
        report, _ = inspect(doc)
        failed = [k for k, v in report["checks"].items() if not v]
        result.append({"case": case, "rejected": not report["pass"], "failed_checks": failed})
    return result


def main():
    reports, geometry = [], []
    for name in ("residential-source.dxf", "residential-clean-reference.dxf"):
        path = ASSETS / name
        report, sig = inspect(ezdxf.readfile(path))
        report.update(file=name, sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        reports.append(report)
        geometry.append(sig)
    probes = corruption_probes(ASSETS / "residential-clean-reference.dxf")
    with Image.open(ASSETS / "residential-reference.png") as im:
        image = {"size": list(im.size), "mode": im.mode}
        im.verify()
    result = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Static DXF geometry, PNG decode and in-memory corruption probes; no CAD/SU/MCP.",
        "files": reports, "same_non_annotation_geometry": geometry[0] == geometry[1],
        "source_annotated_clean_unannotated": reports[0]["layers"].get("ANNOTATION", 0) > 0 and
            reports[1]["layers"].get("ANNOTATION", 0) == 0,
        "image": image, "corruption_probes": probes,
        "vertical_brief_arithmetic_only": {"door_head": 2850-2100,
            "window_head": 2850-900-1500, "stair_mid": 9*3000/18,
            "stair_top": 18*3000/18, "flight_run": 8*300,
            "slab_hole_area_mm2": 2600*3500, "three_storey_roof_top": 3*3000},
        "not_verified": ["Real CAD/SU import or faces/normals", "3D walls, stairs or openings",
                         "SKP save/reopen/editability", "Student trial or efficiency", "Design/code compliance"],
    }
    result["all_static_checks_pass"] = (all(r["pass"] for r in reports) and
        result["same_non_annotation_geometry"] and result["source_annotated_clean_unannotated"] and
        all(p["rejected"] for p in probes))
    (ROOT / "validation/residential-geometry.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in ("all_static_checks_pass", "same_non_annotation_geometry", "image", "corruption_probes")}, ensure_ascii=False, indent=2))
    return 0 if result["all_static_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
