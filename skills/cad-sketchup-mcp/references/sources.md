# 技术核实与边界

最近资料复核：2026-10-29，安装教程固定 sketchup-mcp2 v0.4.0。以下是依据与边界，学生不必全部阅读。本 Skill 不包含第三方源码，不实现、改造或替代 MCP。

本轮核对维护者0.4.0发布说明、固定标签源码和PyPI元数据；下载入口、依赖及升级／导出规则以这些来源为准。另按 OpenAI Docs 流程复核 Codex MCP 配置与本地 Skill 目录。本轮不安装、不接通或修改真实模型；历史本机连接结果不能当作新电脑或新练习的验收。

2026-10-26 历史增量核实：[Numeric 单位](https://ruby.sketchup.com/Numeric.html#mm-instance_method)、[Model 保存副本](https://ruby.sketchup.com/Sketchup/Model.html#save_copy-instance_method)与 [operation](https://ruby.sketchup.com/Sketchup/Model.html#start_operation-instance_method)、[ComponentInstance 独立化](https://ruby.sketchup.com/Sketchup/ComponentInstance.html#make_unique-instance_method)、[Page 场景与标签](https://ruby.sketchup.com/Sketchup/Page.html#layers-instance_method)。`page.layers` 表示偏离默认可见性的标签，非一概隐藏；场景未存标签时可能为 nil。operation 不能嵌套；保存副本的 API 能力不能推导出所有插件／切文件行为都安全。这些API本轮没有重做实机操作。

增量方法来自用户确认的骑楼经验及社区项目交接，适配后只保留通用决策和条件，不复制项目脚本、真实模型或个人路径。社区原项目的恢复、批量、重开和保护结论在本轮只作经验来源，没有重新执行；数字、配色和设备参数不能当教学默认值。

2026-10-09 练习补充：DXF 的 INSUNITS=4 是毫米标记，依据 [Autodesk INSUNITS 文档](https://help.autodesk.com/cloudhelp/2023/ENU/AutoCAD-Core/files/GUID-A58A87BB-482B-4042-A00A-EEF55A2B4FD8.htm)；文件读写与单位查询依据 [ezdxf 单位文档](https://ezdxf.readthedocs.io/en/stable/concepts/units.html)。标记仍不能替代导入后的两段实际尺寸检查。练习几何与图示为本仓库原创、明确的教学数据，不是网上项目或真实软件截图；软件实机导入未验证。

| 核实事项 | 一手来源 | 边界 |
|---|---|---|
| 社区 sketchup-mcp2 由 zinin 维护，源于 mhyrr/sketchup-mcp；不是 Trimble 官方产品 | [维护者仓库](https://github.com/zinin/sketchup-mcp2)、[PyPI0.4.0](https://pypi.org/project/sketchup-mcp2/0.4.0/) | 不混用同名项目的配置 |
| 教程固定0.4.0；从0.3.x升级要两端配套，旧扩展卸载并重启后安装新版，不能直接覆盖 | [0.4.0发布页与签名RBZ](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0) | 已接通跳过安装，升级须另有授权 |
| Python ≥3.10，mcp>=1.30,<2，pydantic>=2.11；支持Python3.14 | [依赖声明](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/pyproject.toml) | 不固定作者补丁版，不等于新电脑安装通过 |
| 安装RBZ、Start Server、Settings；默认127.0.0.1／9876；TCP无认证 | [项目README](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/README.md) | 按现场端口配置，保留回环地址 |
| 两端报告最低兼容版本，无旧max字段；0.3.x与0.4.0混用握手失败 | [兼容说明](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0) | 依实际compatible／错误判断，不自行预测未来版本兼容 |
| get_model_info.units 固定mm；ruby_version为扩展版本 | [模型查询](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/mcp_for_sketchup/mcp_for_sketchup/handlers/model.rb)、[版本查询](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/mcp_for_sketchup/mcp_for_sketchup/handlers/system.rb) | 不证明尺度或Ruby语言版本 |
| 视口截图要求SU2026+；PNG导出为另一方式 | [工具说明](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/src/sketchup_mcp/tools.py)、[导出实现](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/mcp_for_sketchup/mcp_for_sketchup/handlers/export.rb) | 旧版功能待各电脑实机验证，不强制升级 |
| 0.4.0拒绝导出未保存SKP（-32602）；已保存模型用save_copy导出临时副本 | [导出实现](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/mcp_for_sketchup/mcp_for_sketchup/handlers/export.rb) | 先明确保存，不把临时路径当最终交付 |
| 修改超时仍可能提交；嵌套／面／边bbox可能是容器坐标 | [已知边界](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0) | 先读现场再重试；组合实际实例变换，不能只凭bbox字段猜坐标系 |
| Codex MCP的command／args／env TOML、项目范围、CLI add与重启 | [OpenAI MCP文档](https://learn.chatgpt.com/docs/extend/mcp) | 不用其他客户端JSON替代TOML，界面可能不同 |
| Codex .agents/skills与~/.agents/skills发现目录、$skill调用 | [OpenAI Skill文档](https://learn.chatgpt.com/docs/build-skills) | 本轮只做隔离解压，不安装到全局 |
| uv 的 Windows 安装、隔离工具环境、Python 管理 | [安装](https://docs.astral.sh/uv/getting-started/installation/)、[工具](https://docs.astral.sh/uv/concepts/tools/)、[Python](https://docs.astral.sh/uv/guides/install-python/) | 安装由学生选择，制作时不运行 |
| CAD 导入单位、卷尺调整模型大小 | [SketchUp CAD 教程](https://help.sketchup.com/en/sketchup/importing-and-exporting-cad-files)、[缩放教程](https://help.sketchup.com/en/sketchup/scaling-your-model-or-parts-your-model) | 模板单位不代替导入单位，全模型缩放限空白准备文件 |
| 面方向、共享实例与保存行为 | [Face](https://ruby.sketchup.com/Sketchup/Face.html)、[ComponentInstance](https://ruby.sketchup.com/Sketchup/ComponentInstance.html)、[Model](https://ruby.sketchup.com/Sketchup/Model.html) | 支撑 AI 操作规则，不要求学生学习开发 |

副本清理、天正“文件布图 → 局部导出”、空格确认、天正3／AutoCAD 2004／全部内容、导入后反复重选炸开、两段尺寸复核、封面与正反面以及分阶段习惯，来自本次用户确认的交接。天正菜单与选项的跨版本一致性尚无足够官方证据，保留原流程并标注待核；不能用整图导出教程代替局部导出。[天正官方入口](https://www.tangent.com.cn/tzt30jz)

坯子插件／坯子助手封面是可选辅助（历史交接写作“胚子助手”）；本轮未验证版本、下载来源与兼容性，不给未经核实的下载包、不列为必装依赖。

2026-10-29住宅练习为本仓库原创教学数据，单位仍按上述Autodesk／ezdxf依据检查。未引用住宅规范来确定其尺寸；简化片段和三层任务不是完整设计、结构或合规方案。二维数据不能证明楼梯净高、洞口贯通或三维实体正确。

同日补充的 [圈选截图与参考样板方法](local-edit.md) 来自用户与朋友的正常聊天，以及用户确认的改进方向；只作为方法来源，不登记为v0.2.0实机验收。保留“圈位置、定动作、按样板局部修改”的用法，未把原聊天截图、姓名、项目模型或私人文件路径放入分发包。

同日经用户确认加入 [可选模型分工与交接](model-handoff.md)。DeepSeek V4.1 Flash和GPT‑6.1 Sol名称分别核对 [DeepSeek官方说明](https://api-docs.deepseek.com/news/news260910/)与 [OpenAI官方型号页](https://developers.openai.com/api/docs/models/gpt-6.1-sol)。型号资料不证明两者在SU中谁更准确、交接必然成功或更省钱；分工是针对用户习惯的可选方法，本轮未调用两款模型做对比或真实建模。

来源查证不证明所有 SU／Windows／DWG 都兼容，也不等于实机安装或建模精度验证。历史电脑成功不能当学生电脑已通过。本轮不调用真实 SU；用户提供的有限试用反馈与独立实机验收分开，不能宣称效率提升或返工率降低已得到证明。
