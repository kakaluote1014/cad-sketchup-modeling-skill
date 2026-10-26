# CAD → SketchUp MCP 建模教学规范

面向 Windows 建筑学生、首版适配 Codex。教同学从连接现成 SU MCP、准备 CAD 底图开始，分阶段完成尺寸可核对、能继续编辑的一层建筑白模。

**Skill 提供建模方法和工作流程；要让 Codex 控制 SketchUp，还需要安装并配置 SU MCP。安装 Skill 不等于已经接通 MCP。**

## 先选你现在的进度

| 我现在的情况 | 直接从这里开始 | 这一阶段要得到什么 |
|---|---|---|
| 未连接／不确定是否连接 | [检查环境、安装与排查](skills/cad-sketchup-mcp/references/install-connect.md) | 成功读取我的当前模型 |
| 已接通，但底图未准备 | [CAD → SU 底图准备](skills/cad-sketchup-mcp/references/cad-preparation.md) | 干净、尺度正确、可编辑的底图 SKP |
| 已接通，底图已准备 | [目标与尺寸检查、分阶段建模](skills/cad-sketchup-mcp/references/modeling.md) | 只修改指定楼层，阶段结果可检查、可编辑 |

想先练一遍？使用 [第一次练习](skills/cad-sketchup-mcp/references/practice.md)：原创 DXF 原图、清理参照、尺寸与洞口示意，以及每阶段可复制的指令。练习尺寸只用于练习，不是其他项目的默认参数。

本仓库维护教学规范与 AI 协作规则。建模控制由现成的 SU MCP 提供；仓库不包含 MCP 服务端或第三方实现，不替代人的设计和结构判断。

## 下载与安装

当前迭代 v0.1.2：[取得 Skill ZIP](dist/cad-sketchup-mcp-v0.1.2.zip)。GitHub 文件页可下载原始文件，私有仓库需要访问权限；保留 [v0.1.1 包](dist/cad-sketchup-mcp-v0.1.1.zip) 与 [v0.1.0 首版包](dist/cad-sketchup-mcp-v0.1.0.zip)。

给同学试用：把上面的 ZIP 与 [v0.1.2 完整试用提示词](docs/给同学Codex的试用提示词_v0.1.2.md) 一起提供给他的 Codex，先检查实际环境，不固定 SU 年份、套餐或模型。坯子插件是可选辅助工具。旧的 SU2020 提示词仅用于对应的历史环境。

解压后把整个 `cad-sketchup-mcp` 目录复制到你的学习项目 `.agents/skills/` 下，最终为 `.agents/skills/cad-sketchup-mcp/SKILL.md`。保留所有引用文件，不覆盖已有同名 Skill。用 Codex 打开该学习项目，调用 `$cad-sketchup-mcp`；未出现时重新打开聊天或重启 Codex。

也可克隆仓库后，复制 `skills/cad-sketchup-mcp`。仓库本身不会自动安装软件、接通 MCP 或修改全局配置。

SU MCP 来源：[sketchup-mcp2 维护者仓库](https://github.com/zinin/sketchup-mcp2)、[v0.3.1 发布页](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.3.1)。这是社区项目，不是 SketchUp／Trimble 官方产品。

## 从当前进度开始

1. [安装、启用、配置与连接排查](skills/cad-sketchup-mcp/references/install-connect.md)：已有连接跳过安装，终点是成功读取当前模型。
2. [完整 CAD → SU 底图准备](skills/cad-sketchup-mcp/references/cad-preparation.md)：副本清理 → 天正局部导出 → 毫米模板导入 → 反复重选炸开 → 两段尺寸复核 → 封面与正反面 → 保存 SKP。
3. [分阶段建模与检查](skills/cad-sketchup-mcp/references/modeling.md)：先检查或做样板，再推进指定楼层和副本；保留人工改动，每阶段备份、保存和预览。

第一次可以说：

> 使用 $cad-sketchup-mcp。我第一次使用 SU MCP，请先只读检查环境，按教程引导连接；先不要安装或改配置。

底图已准备可以说：

> 使用 $cad-sketchup-mcp。只做选中的二层墙体，尺寸以附图为准。先读当前模型、核对两段尺寸和目标，再做样板；检查通过后继续这层墙体，其他副本保留。

更多示例见 [学生快速开始](skills/cad-sketchup-mcp/README.md)。

已进入多栋多层、独立外观方案或场景交付时，在分阶段建模教程中按需读取 [进阶执行细节](skills/cad-sketchup-mcp/references/advanced-execution.md)。小任务只做相关检查，不要求学生先准备 JSON 或哈希报告。

## 已验证与待验证

v0.1.0 已完成文件静态校验、ZIP 隔离解压检查、12 个合成场景的独立行为演练及定向复测。v0.1.1 新增三个进度入口与原创练习资产，已完成文件打包检查、DXF 独立静态几何检查、图示目检及 C1–C6 合成行为演练。演练验证的是规范引导下的决策，不是实际 MCP 调用或几何建模。

v0.1.2 把项目经验整理成按任务影响选择检查、差异化批量展开、墙板楼梯联动、源模型与场景保护及安全保存切换规则。文件检查与本轮合成桌面演练见 [迭代验收](validation/review-v0.1.2.md)；不是 MCP 或真实建模测试。

已有一位使用 SU2023 与 Codex Luna 的同学提供了练习截图和反馈：可见建模进展，Agent 报告了保存与尺寸回读；最终 SKP 和完整调用日志尚未独立验收。另有骑楼及社区项目经验交接，不是本轮重做的实机测试。v0.1.2 的新电脑安装、跨版本兼容、自动发现与真实模型验收仍待验证，没有对照数据证明效率提升或返工率降低。

详见 [验证说明](skills/cad-sketchup-mcp/references/validation.md)、[本次迭代验收](validation/review-v0.1.1.md)、[练习几何验收](validation/practice-geometry.md)、[首版演练验收](validation/review.md)与 [技术来源](skills/cad-sketchup-mcp/references/sources.md)。

## 持续推进

教学源文件在 `skills/cad-sketchup-mcp/`，合成演练证据在 `validation/`。后续任务和反馈方式见 [推进记录](docs/持续推进.md)。

修改后可使用已有 Python 3.11+ 运行：

```powershell
python scripts/check_and_package.py
```

它仅检查仓库内教学文件并生成 `dist/` 的 13 文件 Skill ZIP（含练习与按需参考），不连接 CAD／SU、不安装依赖。输出到 `validation/package-check.json`；打包不代表行为测试或实机验证已通过。

学生直接用已生成的练习，不必运行代码。维护者如需重建练习文件，可用已有 ezdxf、Pillow 和中文字体运行 `scripts/create_practice_assets.py`；它只生成原创教学文件，不控制 CAD／SU。

不要上传真实项目图纸、模型、私人配置、密钥或个人绝对路径。学生试用资料先脱敏，模型写入和系统安装另行说明目标与影响并取得授权。
