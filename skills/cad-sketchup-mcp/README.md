# CAD → SketchUp MCP 建模教学规范

首版 v0.1.0 · Windows + 本机 Codex · 技术核实日期：2026-10-08。

**Skill 提供建模方法和工作流程；要让 Codex 控制 SketchUp，还需要安装并配置 SU MCP。安装 Skill 不等于已经接通 MCP。**

本包教你连接现成工具、准备 CAD 底图、说明任务、分步检查；不包含 MCP 源码、服务端、替代实现或软件安装器。

## 下载入口

- Skill：[本仓库 v0.1.0 ZIP](https://github.com/kakaluote1014/cad-sketchup-modeling-skill/blob/main/dist/cad-sketchup-mcp-v0.1.0.zip)，打开文件页后下载原始文件；解压得到 `cad-sketchup-mcp/SKILL.md`。私有仓库需要访问权限。
- SU MCP：[sketchup-mcp2 维护者仓库](https://github.com/zinin/sketchup-mcp2)、[v0.3.1 发布页](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.3.1)。这是社区项目，不是 SketchUp／Trimble 官方产品；“项目官方来源”指维护者发布来源。
- SketchUp 侧：[v0.3.1 签名 RBZ 扩展](https://github.com/zinin/sketchup-mcp2/releases/download/v0.3.1/mcp_for_sketchup_v0.3.1-signed.rbz)。
- Codex 侧：[PyPI sketchup-mcp2 0.3.1](https://pypi.org/project/sketchup-mcp2/0.3.1/)，按连接教程用 uvx 运行。

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

## 学习路线

1. [安装与连接](references/install-connect.md)：成功读取当前模型。
2. [CAD → SU 底图准备](references/cad-preparation.md)：得到干净、尺寸正确、可编辑的 SKP。
3. [分阶段建模与检查](references/modeling.md)：完成指定的一层白模，关键尺寸可复核。

提供原图尺寸依据、目标楼层／副本、本次要做的构件即可；未知尺寸先列出，不必填复杂表格。

方法旨在用尺寸校验和阶段检查减少返工，但尚无真实学生试用，未证明效率提升或返工率降低。实机与兼容性边界见 [验证说明](references/validation.md)。
