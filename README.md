# CAD → SketchUp MCP 建模教学规范

把 CAD 平面图整理成底图，配合 AI 分阶段完成尺寸可核对、能继续编辑的 SketchUp 建筑模型。

这份 Skill 面向建筑学生，目前以 **Windows + Codex** 为主要使用环境，重点覆盖住宅建模和已有模型的局部修改。它整理的是实际建模中的操作习惯、协作方法和检查步骤。

> **Skill 提供建模方法和工作流程；要让 Codex 控制 SketchUp，还需要安装并配置 SU MCP。安装 Skill 不等于已经接通 MCP。**

## 下载

当前版本：**v0.2.0 教学试用版（Pre-release）**。

- [下载 Skill 压缩包](https://github.com/kakaluote1014/cad-sketchup-modeling-skill/releases/download/v0.2.0/cad-sketchup-mcp-v0.2.0.zip)
- [下载给同学 Codex 的完整试用提示词](https://github.com/kakaluote1014/cad-sketchup-modeling-skill/releases/download/v0.2.0/student-trial-prompt-v0.2.0.md)
- [发布说明与校验文件](https://github.com/kakaluote1014/cad-sketchup-modeling-skill/releases/tag/v0.2.0)

第一次给同学使用，把 **压缩包和提示词 MD** 一起发给他即可。提示词会引导他的 Agent 先检查实际环境，再从合适的阶段开始。

## 三步开始使用

1. **安装 Skill。** 解压后，将整个 `cad-sketchup-mcp` 文件夹放进学习项目的 `.agents/skills/`，最终路径为 `.agents/skills/cad-sketchup-mcp/SKILL.md`。保留全部教程与素材；已有同名 Skill 时先比较，保留自己的记录。
2. **检查 MCP 连接。** 用 Codex 打开学习项目，输入 `$cad-sketchup-mcp`。尚未连接就按教程检查环境；已连接则成功读取当前模型后跳过安装。
3. **说明本次任务。** 提供图纸或标注截图，指出目标楼层、要做的构件和需要保留的内容。先检查或做一处样板，再处理已确认的同类构件。

首次使用可以直接说：

> 使用 $cad-sketchup-mcp。我第一次使用 SU MCP，请先只读检查环境，带我确认连接和底图准备；需要安装软件或修改配置时先说明。

详细安装与更多示例见 [学生使用指南](skills/cad-sketchup-mcp/README.md)。

## 从你现在的进度开始

| 当前情况 | 下一步 |
|---|---|
| 还没接通，或不确定是否接通 | [检查环境、安装连接与排查](skills/cad-sketchup-mcp/references/install-connect.md)，直到能读到目标模型 |
| 已接通，CAD 底图还没准备 | [CAD → SU 底图准备](skills/cad-sketchup-mcp/references/cad-preparation.md)，保留原图、清理副本、核对比例并保存 SKP |
| 底图已准备，开始建模 | [分阶段建模与检查](skills/cad-sketchup-mcp/references/modeling.md)，只处理指定楼层和构件 |
| 已有模型，想修改某个位置 | [圈选截图＋参考样板](skills/cad-sketchup-mcp/references/local-edit.md)，先定位对象，再做局部修改 |

CAD 准备沿用这条路线：**复制清理 → 天正局部导出 → 毫米模板导入 → 反复重选炸开 → 两段尺寸核对 → 封面与正反面检查 → 保存底图。** 天正局部导出是有天正时的操作方式；坯子插件可辅助封面，二者都不是 MCP 连接的必要依赖。

## 可以怎样配合 AI 建模

**按住宅建模阶段推进。** 从单户到标准层，再按实际需要处理首层、顶层和整栋差异。检查共墙、门窗上下墙、楼板、楼梯洞口与阳台，保留人工移动、复制和炸开后的修改。[住宅路线 →](skills/cad-sketchup-mcp/references/residential.md)

**画框说明要改哪里。** 圈出目标 A、提供参考 B，说明要改的内容和保留条件。例如：

> 把 A 的门框样式改成 B 那样，保留 A 的洞口尺寸、位置和开启方式。只改这一层的 A，B、旁边栏板和其他楼层保留，给我局部前后对照。

**按需分配模型任务。** 可以先用 DeepSeek V4.1 Flash 做基础白模，再由 GPT‑6.1 Sol 接手审查和优化。交接当前 SKP、已定尺寸和待改清单，接手后重新读现场；同一时刻只让一个 Agent 写入。也可以用一个模型完成全程。[分工与两段提示词 →](skills/cad-sketchup-mcp/references/model-handoff.md)

**保留自己的协作习惯。** Skill 在当前学习项目的 `.su-modeling/preferences.md` 中记录你明确表达的偏好，下次使用时读取。你可以纠正、停用或要求忘记某条；本次明确指令优先。私人记录留在本地，不提交或随包分享，项目尺寸也不会成为通用默认值。[本地习惯记录 →](skills/cad-sketchup-mcp/references/preferences.md)

## 想先练一遍？

随包提供两组原创练习，不必用真实项目试错，也不用运行生成脚本。

- [入门练习](skills/cad-sketchup-mcp/references/practice.md)：一间房、一个门洞、一个窗洞，走通底图准备到保存白模的流程。
- [住宅进阶练习](skills/cad-sketchup-mcp/references/residential-practice.md)：一户教学片段、楼梯、板洞和阳台，先做一层，再自选三层差异任务。

每组都有原图 DXF、清理参照和尺寸示意。练习是简化教学数据，尺寸只用于该练习，不是完整住宅设计或其他项目的默认参数。

## 试用范围与验证进展

本版已完成文件与打包检查、原创 DXF 的静态几何检查，以及文本桌面推演。旧版有同学提供过过程截图和反馈；这些材料与新版的独立实机验收分别记录。

**v0.2.0 新增练习的真实 CAD／SU 导入、三维建模、保存重开、跨模型交接和学生独立完成情况仍待验证。** 目前没有对照数据证明耗时、费用、准确率或返工率改善。建模结果仍需要人工核对，不替代设计、结构或合规判断。

[版本说明](docs/版本说明_v0.2.0.md) · [本版检查记录](validation/review-v0.2.0.md) · [技术来源](skills/cad-sketchup-mcp/references/sources.md)

## 工具来源与反馈

建模控制由第三方社区项目 [sketchup-mcp2](https://github.com/zinin/sketchup-mcp2) 提供。本仓库维护教学方法与 AI 协作规则，不包含 MCP 实现或软件安装器；SU MCP 也不是 SketchUp／Trimble 官方产品。连接教程固定核对到 [MCP v0.4.0](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0)，已有可用连接不强制升级。

遇到问题，可以在 [Issues](https://github.com/kakaluote1014/cad-sketchup-modeling-skill/issues) 中说明软件版本、进行到哪一步、期望与实际结果，并附脱敏截图。请勿上传真实项目模型、私人习惯记录、账号配置或密钥。

维护者入口：[教学源文件](skills/cad-sketchup-mcp/SKILL.md) · [持续推进记录](docs/持续推进.md)。修改教学文件后，可用已有 Python 3.11+ 运行 `python scripts/check_and_package.py` 检查并打包；普通使用者直接下载发布包即可。
