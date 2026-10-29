# CAD → SketchUp MCP 建模教学规范

当前迭代 v0.2.0 · Windows + 本机 Codex · 教学更新与MCP0.4.0资料核实：2026-10-29；本轮未做真实安装或模型操作。

**Skill 提供建模方法和工作流程；要让 Codex 控制 SketchUp，还需要安装并配置 SU MCP。安装 Skill 不等于已经接通 MCP。**

## 先选你现在的进度

| 我现在的情况 | 下一步 | 怎样确认成功 |
|---|---|---|
| 没接通 MCP／不知道是否接通 | 从 [安装与连接](references/install-connect.md) 的现有环境检查开始 | Codex 成功读到我的当前模型，不只是显示服务已启用 |
| MCP 已接通，CAD 底图还没准备 | 按 [底图准备](references/cad-preparation.md) 保留原图、清理副本并准备 SKP | 两段已知尺寸正确，必要区域已封面、正面朝上，SKP 已保存 |
| MCP 已接通，底图也已准备 | 先读现场、核对目标和尺寸，再按 [分阶段建模](references/modeling.md) 处理指定构件 | 只改指定副本，关键尺寸可核对，阶段 SKP 可编辑 |

已有模型只想改局部：直接用 [圈选截图＋参考样板](references/local-edit.md)。圈出位置，再说要改什么、保留什么；目标A和参考B可以分别标出，不必重新准备CAD。

想先用DeepSeek V4.1 Flash建基础白模，再由GPT‑6.1 Sol审查和优化，可选 [模型分工与交接](references/model-handoff.md)，内含分别给两阶段使用的提示词。按阶段完成情况和返工信号交接，单模型也能沿原路线做，不把换模型当作必经步骤。

想先练一遍？打开 [第一次练习：一间房、一个门洞、一个窗洞](references/practice.md)。随包提供原图 DXF、清理参照和尺寸示意；不需要拿真实项目试错，也不用执行生成脚本。

已会入门练习，或要做住宅作业？读 [住宅路线](references/residential.md)。可选 [住宅教学片段](references/residential-practice.md)，依次练墙、板洞、楼梯、阳台，再自选三层差异；参数只用于这份简化教学片段。

本包教你连接现成工具、准备 CAD 底图、说明任务、分步检查；不包含 MCP 源码、服务端、替代实现或软件安装器。

使用中可把明确偏好记在本项目`.su-modeling/preferences.md`，下次实际调用Skill时读取；首次按 [本地习惯记录](references/preferences.md) 初始化，已有文件保留，用户可纠正、停用或要求忘记某条。不自动上传记录，不修改模型权重，也不代替本次指令与图纸依据。

## 下载入口

- Skill：本次教学试用包为 `cad-sketchup-mcp-v0.2.0.zip`，从 [v0.2.0发布页](https://github.com/kakaluote1014/cad-sketchup-modeling-skill/releases/tag/v0.2.0) 或仓库 `dist/` 取得；解压得到 `cad-sketchup-mcp/SKILL.md`。
- SU MCP：[sketchup-mcp2 维护者仓库](https://github.com/zinin/sketchup-mcp2)、[v0.4.0 发布页](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0)。这是社区项目，不是 SketchUp／Trimble 官方产品；“项目官方来源”指维护者发布来源。
- SketchUp 侧：[v0.4.0 签名 RBZ 扩展](https://github.com/zinin/sketchup-mcp2/releases/download/v0.4.0/mcp_for_sketchup_v0.4.0-signed.rbz)。
- Codex 侧：[PyPI sketchup-mcp2 0.4.0](https://pypi.org/project/sketchup-mcp2/0.4.0/)，按连接教程用 uvx 运行。

MCP 和 Skill 分别取得，包内不捆绑第三方软件。已接通者跳过安装，直接检查底图。

## 安装 Skill

建议先在自己的学习项目内使用：将整个 `cad-sketchup-mcp` 文件夹复制到项目的 `.agents/skills/`，最终结构为：

```text
你的学习项目/
  .agents/skills/cad-sketchup-mcp/
    SKILL.md
    README.md
    agents/openai.yaml
    references/...
    assets/practice/...
    assets/residential/...
```

保留所有引用文件，不只复制 SKILL.md。同名 Skill 已存在时先比较或另存，不直接覆盖。用 Codex 打开该学习项目，在 Skill 选择器找“CAD → SketchUp 建模教学规范”；CLI／IDE 可输入 `/skills` 或 `$cad-sketchup-mcp`。若未出现，重新打开聊天或重启 Codex。往任意目录解压不等于已安装。[Codex 官方 Skill 文档](https://developers.openai.com/codex/skills)

供所有项目使用时，可由学生自行放到个人目录 `~/.agents/skills/`；这份交付不替你安装或改全局配置。不需要开发 MCP 或制作插件。

## 下一句话可以这样说

尚未连接：

> 使用 $cad-sketchup-mcp。我第一次使用 SU MCP，请先只读检查我的 Windows、SketchUp 和 Codex 环境，按教程引导连接；先不要安装或改配置。

已连接、尚未准备底图：

> 使用 $cad-sketchup-mcp。我已接通 MCP，有天正平面图。请按“副本清理 → 局部导出 → 毫米 SU 导入 → 炸开 → 两段尺寸校验 → 封面”的流程指导我准备底图。

底图已准备：

> 使用 $cad-sketchup-mcp。只做我选中的二层副本墙体，其他副本保留。墙高以附图剖面标注为准；先读当前模型并核对附图两段尺寸，再做一处样板给我检查。

人工改过模型：

> 使用 $cad-sketchup-mcp。我刚移动并炸开了右侧首层副本。请重新读取现场、保留我的改动；这次只补指定窗洞的窗台墙和窗上墙，尺寸见标注图。

画框精准修改：

> 使用 $cad-sketchup-mcp。把A的门框样式改成B那样，保留A的洞口尺寸、位置和开启方式。只改这一层的A，B、玻璃栏板及其他楼层保留；先对应当前模型，改后给局部前后对照。

## 学习路线

1. [安装与连接](references/install-connect.md)：成功读取当前模型。
2. [CAD → SU 底图准备](references/cad-preparation.md)：得到干净、尺寸正确、可编辑的 SKP。
3. [分阶段建模与检查](references/modeling.md)：完成指定的一层白模，关键尺寸可复核。
4. [住宅路线](references/residential.md)：按本次要求走单户、标准层、首层／顶层或整栋；不默认做后续任务。

提供原图尺寸依据、目标楼层／副本、本次要做的构件即可；未知尺寸先列出，不必填复杂表格。

进入多栋多层或场景交付后，按 [分阶段建模](references/modeling.md) 的任务表选择检查深度；复杂保存、嵌套和场景问题才读 [进阶执行细节](references/advanced-execution.md)。小任务不必填写数据表或做全项目审计。

方法旨在通过尺寸校验和阶段检查减少返工。已有旧版的有限学生截图与反馈，但未独立验收最终 SKP，也没有证明效率提升或返工率降低的对照数据；v0.2.0 尚未实机试用。具体边界见 [验证说明](references/validation.md)。
