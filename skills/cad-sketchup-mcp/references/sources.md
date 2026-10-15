# 技术核实与边界

核实日期：2026-10-08。以下是教程依据和维护记录，学生不必全部阅读。本 Skill 不包含第三方源码，不实现、改造或替代 MCP。

2026-10-09 练习补充：DXF 的 INSUNITS=4 是毫米标记，依据 [Autodesk INSUNITS 文档](https://help.autodesk.com/cloudhelp/2023/ENU/AutoCAD-Core/files/GUID-A58A87BB-482B-4042-A00A-EEF55A2B4FD8.htm)；文件读写与单位查询依据 [ezdxf 单位文档](https://ezdxf.readthedocs.io/en/stable/concepts/units.html)。标记仍不能替代导入后的两段实际尺寸检查。练习几何与图示为本仓库原创、明确的教学数据，不是网上项目或真实软件截图；软件实机导入未验证。

| 核实事项 | 一手来源 | 边界 |
|---|---|---|
| 社区 sketchup-mcp2 由 zinin 维护，源于 mhyrr/sketchup-mcp；不是 Trimble 官方产品 | [维护者仓库](https://github.com/zinin/sketchup-mcp2)、[PyPI](https://pypi.org/project/sketchup-mcp2/0.3.1/) | 不混用同名项目的配置 |
| 当前查询最新发布 v0.3.1，有同版 signed.rbz、wheel、源码包 | [发布页](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.3.1) | 教程固定已查证版本，不自动升级 |
| Python ≥3.10，依赖 mcp[cli]>=1.27,<2 | [依赖声明](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/pyproject.toml) | 依赖声明不等于各电脑实机验证 |
| 安装 RBZ、Start Server、Settings；Host／Port 发布默认 127.0.0.1／9876 | [项目 README](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/README.md)、[菜单定义](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/mcp_for_sketchup/mcp_for_sketchup/main.rb) | 以本机设置为准，不抄个人路径 |
| 两端有版本握手，同版配对避免混版陷阱 | [兼容声明](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/src/sketchup_mcp/compat.py) | 不仅看单侧范围推断混版可用 |
| get_model_info.units 固定为 mm；ruby_version 指扩展版本 | [模型查询](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/mcp_for_sketchup/mcp_for_sketchup/handlers/model.rb)、[版本查询](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/mcp_for_sketchup/mcp_for_sketchup/handlers/system.rb) | 不能证明尺度或 Ruby 语言版本 |
| 视口截图要求 SU 2026+；PNG 导出是另一方式 | [工具说明](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/src/sketchup_mcp/tools.py)、[导出实现](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/mcp_for_sketchup/mcp_for_sketchup/handlers/export.rb) | 旧版功能需实机验证，不强制升级 |
| SKP 导出到临时路径；未命名文件会用 save 改变路径，已有路径用 save_copy | [导出实现](https://github.com/zinin/sketchup-mcp2/blob/v0.3.1/mcp_for_sketchup/mcp_for_sketchup/handlers/export.rb) | 不把临时导出当最终保存 |
| Codex MCP 的 command／args／env TOML、可信项目范围、CLI add | [OpenAI MCP 文档](https://developers.openai.com/codex/mcp) | 不用别的客户端 JSON 替代 TOML，界面可能不同 |
| Codex 的 .agents/skills 与 ~/.agents/skills 本地发现目录、$skill 调用 | [OpenAI Skill 文档](https://developers.openai.com/codex/skills) | 只创建目录，未自动安装到全局 |
| uv 的 Windows 安装、隔离工具环境、Python 管理 | [安装](https://docs.astral.sh/uv/getting-started/installation/)、[工具](https://docs.astral.sh/uv/concepts/tools/)、[Python](https://docs.astral.sh/uv/guides/install-python/) | 安装由学生选择，制作时不运行 |
| CAD 导入单位、卷尺调整模型大小 | [SketchUp CAD 教程](https://help.sketchup.com/en/sketchup/importing-and-exporting-cad-files)、[缩放教程](https://help.sketchup.com/en/sketchup/scaling-your-model-or-parts-your-model) | 模板单位不代替导入单位，全模型缩放限空白准备文件 |
| 面方向、共享实例与保存行为 | [Face](https://ruby.sketchup.com/Sketchup/Face.html)、[ComponentInstance](https://ruby.sketchup.com/Sketchup/ComponentInstance.html)、[Model](https://ruby.sketchup.com/Sketchup/Model.html) | 支撑 AI 操作规则，不要求学生学习开发 |

副本清理、天正“文件布图 → 局部导出”、空格确认、天正3／AutoCAD 2004／全部内容、导入后反复重选炸开、两段尺寸复核、封面与正反面以及分阶段习惯，来自本次用户确认的交接。天正菜单与选项的跨版本一致性尚无足够官方证据，保留原流程并标注待核；不能用整图导出教程代替局部导出。[天正官方入口](https://www.tangent.com.cn/tzt30jz)

胚子助手封面是可选辅助；本轮未验证版本、下载来源与兼容性，不给未经核实的下载包、不列为必装依赖。

来源查证不证明所有 SU／Windows／DWG 都兼容，也不等于实机安装或建模精度验证。历史电脑成功不能当学生电脑已通过。本轮不调用真实 SU，不声称学生试用、效率提升或返工率降低已完成。
