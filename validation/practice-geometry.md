# 原创练习资产静态几何验收

仅检查实际 DXF 与 PNG 文件；未调用 CAD、SU、MCP、网络、安装或配置。

数值来自 practice.md，作为命令参数输入。算术 epsilon 不是项目施工容差。

脚本静态检查全部成立：True。以下是实测证据。

| 文件 | DXF版本 | INSUNITS | 实体数 | WALL面积 mm² |
|---|---|---|---|---|
| practice-source.dxf | AC1018 | 4 | 55 | 3110400.0 |
| practice-clean-reference.dxf | AC1018 | 4 | 36 | 3110400.0 |

- 给定外墙边界：0…6000 × 0…4200；实际外墙与室内净边界详见 JSON。
- 墙域按网格单元逐区与给定外轮廓减室内、D1、W1核对，不依赖固定面数。
- 去除 ANNOTATION 后两份实体几何一致：True。
- 原图有标注／清理参照无标注实体：True／True。
- PNG 解码成功，尺寸 [1500, 1140]，模式 RGB。

## practice-source.dxf

分层计数：`{"WALL": 24, "ROOM_REFERENCE": 4, "DOOR_SYMBOL": 2, "WINDOW_SYMBOL": 6, "ANNOTATION": 19}`。

审计错误／修复：0／0；分割共线端点后的墙图拓扑：`{'noded_edges': 24, 'vertices': 20, 'dangling_vertices': [], 'degree_counts': {2: 12, 3: 8}}`。

跨语义层共线重叠 9 对，逐段证据在 JSON；导入合并或封面时须保留分类意识。

| 检查 | 实际结果 |
|---|---|
| millimetre_units | True |
| metric_measurement | True |
| wall_bounds | True |
| room_bounds | True |
| wall_axis_aligned | True |
| all_supported_entities_z0 | True |
| arc_plane_normal | True |
| all_entity_types_examined | True |
| wall_region_matches_brief | True |
| wall_area_matches_brief | True |
| wall_no_dangling_endpoints_after_noding | True |
| room_closed_reference | True |
| door_arc_matches_opening | True |
| door_leaf_matches_opening | True |
| window_bounds_match_opening | True |
| window_two_interior_symbol_lines | True |
| semantic_layers_present | True |
| semantic_entity_types | True |

## practice-clean-reference.dxf

分层计数：`{"WALL": 24, "ROOM_REFERENCE": 4, "DOOR_SYMBOL": 2, "WINDOW_SYMBOL": 6}`。

审计错误／修复：0／0；分割共线端点后的墙图拓扑：`{'noded_edges': 24, 'vertices': 20, 'dangling_vertices': [], 'degree_counts': {2: 12, 3: 8}}`。

跨语义层共线重叠 9 对，逐段证据在 JSON；导入合并或封面时须保留分类意识。

| 检查 | 实际结果 |
|---|---|
| millimetre_units | True |
| metric_measurement | True |
| wall_bounds | True |
| room_bounds | True |
| wall_axis_aligned | True |
| all_supported_entities_z0 | True |
| arc_plane_normal | True |
| all_entity_types_examined | True |
| wall_region_matches_brief | True |
| wall_area_matches_brief | True |
| wall_no_dangling_endpoints_after_noding | True |
| room_closed_reference | True |
| door_arc_matches_opening | True |
| door_leaf_matches_opening | True |
| window_bounds_match_opening | True |
| window_two_interior_symbol_lines | True |
| semantic_layers_present | True |
| semantic_entity_types | True |

## 未验证范围

- CAD／天正打开、转换 DWG、SU 导入、曲线离散及共边合并。
- SU 自动封面、面正反朝向、三维墙高与洞口贯通、保存可编辑 SKP。
- 软件兼容性、真实学生完成能力或效率。
- 高度数值只由教学依据作算术核对，不是二维 DXF 中的实测三维构件。

## 独立视觉观察与具体验收判断

本节由评估者直接查看实际 `plan-reference.png` 后记录，不是脚本 OCR 或 PNG 解码检查的结论。另重读了当前 `references/practice.md` 中新增的局部／世界坐标、共边合并说明，没有读取生成资产的脚本或其他评估答案。

图示在实际 1500×1140 分辨率下可读：标题、单位 mm、原创教学示意及非软件截图说明完整；灰墙、青窗、橙门的图例与实际平面一致。A=6000、B=4200、墙厚180、墙高2800、D1宽900高2100和左端X=900、W1宽1500高1200和下端Y=1500均能清楚阅读，无明显遮挡、裁切或数值冲突。房间区域有“不要把地面一起拉高”的提示，门弧也标明不建成墙。下方竖向示意可区分门上墙700、门洞2100、窗上墙700、窗洞1200和窗台墙900；不以像素比例替代实际尺寸。

实际原始 DXF 证据如下：

- 两份 `$INSUNITS=4`（毫米）、`$MEASUREMENT=1`，DXF版本为 AC1018。原图55实体，清理参照36实体；差额为 ANNOTATION 层的9段文字与10条辅助线。
- 两份非标注实体一致：WALL 24条直线，ROOM_REFERENCE 4条直线，DOOR_SYMBOL 1条直线及1段圆弧，WINDOW_SYMBOL 6条直线。清理参照仍保留空的 ANNOTATION 图层定义，但没有该层实体，符合“删除文字与尺寸辅助线”的清理要求。
- WALL 实际边界为 (0,0)…(6000,4200)，ROOM_REFERENCE 为 (180,180)…(5820,4020)，净尺寸5640×3840。墙区域网格占用和图纸指定的180厚外墙区域一致，墙域面积3,110,400 mm²；不是仅比较包围盒就认定墙厚正确。
- D1的墙域缺口为 X=900…1800、Y=0…180；W1的墙域缺口为 X=5820…6000、Y=1500…3000，均未误封为 WALL。门弧中心为 (900,180)、半径900、角度0°…90°，门叶示意线至 (900,1080)；窗口两条内部符号线位于X=5880、5940，与洞口的平面范围一致。
- 所有已检查实体的几何／插入点位于 Z=0，圆弧法向为 +Z；WALL 在分割共线端点后没有悬空端点，ROOM_REFERENCE 闭合。实际 DXF 是边线而非 SU 的面，不能由这些结果推断面正反朝向已经正确。
- 两份 DXF 的 ezdxf 审计均为0错误、0修复。去掉 ANNOTATION 后的实体类型、图层、坐标和圆弧参数逐项相同，没有观察到清理参照偷改底图几何。

在本次实际检查覆盖范围内，没有发现尺寸、位置、共面、清理一致性或文件解码错误。这个结论不承诺所有 CAD 实现的解释行为相同，也不把二维文件视为已完成的三维模型。

## 实际观察到的歧义与使用风险

存在9对跨语义层的共线重叠（两份文件相同）：WALL与ROOM_REFERENCE 6对，WALL与WINDOW_SYMBOL 2对，WINDOW_SYMBOL与ROOM_REFERENCE 1对。窗口上下端线分别与墙端线完全重合；房间参照沿墙内边并在门窗开口处延续；窗口内侧线和房间右边线在Y=1500…3000重合。JSON保存了每段起止坐标。

这些重叠不造成实际尺寸偏差，但导入 SU 后可能被合并，WINDOW_SYMBOL 的封闭边框及内部双线还可能生成分割面；房间参照也可能在开口边界形成额外面。不能按原始 DXF 图层或36个实体期待导入后保留同样的边／面分类，也不能将窗口框内面与房间面一起拉高。当前教学文件已经明示共边可能合并并要求读现场分类；此风险需要真实导入时检查，不应伪写为已经排除。

原图尺寸文字是英文，中文 PNG 和 practice.md 能对应，但仅打开 DXF 的中文初学者可能需要对照；这属于可读性提示，未发现损坏或乱码。高度仅在文字／教学说明中给定，二维 DXF 没有门上墙、窗台墙或窗上墙实体；须在建模阶段另行验证。图示采用教学表达，不替代局部坐标到真实导入目标变换的映射；当前文档已说明这一点。

## 本次脚本执行证据与复现

已实际运行本次新建的检查脚本，最终运行退出码0，`all_static_checks_pass=true`，不是预填结果。脚本不引用本机路径，不调用模型或 CAD，不安装依赖，只读取指定目录两份 DXF 与 PNG，并写入指定 JSON／Markdown。使用现有 ezdxf 和 Pillow；审计仅在内存进行，不保存或修改 DXF。

在交付目录下可用已具备依赖的 Python 复现：

```powershell
python scripts/check_practice_assets.py skills/cad-sketchup-mcp/assets/practice --width 6000 --height 4200 --thickness 180 --door 900 1800 --window 1500 3000 --wall-height 2800 --door-height 2100 --sill 900 --window-height 1200 --out-json validation/practice-geometry.json --out-md validation/practice-geometry.md
```

脚本是矩形外墙、单门单窗这类正交练习的检查器，尺寸均由参数提供，不是任意 DWG／曲墙／复杂图纸的通用验收器。重新运行会生成自动检查报告，本节独立视觉观察需重新补记；自动结果不能代替图示目检。

本轮仅新建本脚本、JSON和此报告，未修改练习资产、Skill或其他文件。真实 CAD／天正打开和DWG转换、SU导入及合并、封面法向、三维拉高与洞口上下墙、模型备份／SKP保存和学生试用仍未进行。
