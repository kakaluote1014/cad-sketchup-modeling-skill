# Windows：连接现成 SU MCP

Skill 提供建模方法和工作流程；要让 Codex 控制 SketchUp，还需要安装并配置 SU MCP。安装 Skill 不等于已经接通 MCP。

这是现成工具的安装使用教程，不是 MCP 开发教程。已接通者跳到第 5 步只读确认，随后进入底图准备。

## 1. 先检查已有环境

查看 SketchUp 桌面版版本／构建号、“文件 → 导入”是否能选 DWG、扩展管理器是否已有 MCP 及其版本、Codex 是否已登记连接。保留现有 SketchUp，不覆盖配置。

PowerShell 只读检查：

```powershell
Get-Command uv, uvx, python, codex -ErrorAction SilentlyContinue |
  Select-Object Name, Source
```

Python 指向 WindowsApps 别名不等于解释器已安装。已有 uv 可用 `uv python list --only-installed` 看现有解释器；已有 Codex CLI 可用 `codex mcp list` 看登记状态。没有 CLI 查看 Codex 设置的 MCP 列表，不必专门安装 CLI。分享结果删私人路径或敏感内容。

本教程使用桌面 Ruby 扩展，浏览器版 SketchUp 不适用。DWG 导入受产品版本／许可能力影响，先看本机是否可导入，不能假装导入成功。[SketchUp 官方 CAD 教程](https://help.sketchup.com/en/sketchup/importing-and-exporting-cad-files)

本教程于2026-10-29复核 sketchup-mcp2 v0.4.0 的来源、依赖和功能边界，并固定该版本以便复现，不自动跟随 latest。维护者报告的实机版本为 SU2026.1，没有覆盖所有 SketchUp 年份的兼容矩阵。视口截图工具要求 SU2026+，不表示全部建模都须升级到2026；保留学生现有版本，以实际读取及所需操作验收为准。[发布说明](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0)

## 2. 下载与运行依赖

从 [维护者 v0.4.0 发布页](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0) 下载 [mcp_for_sketchup_v0.4.0-signed.rbz](https://github.com/zinin/sketchup-mcp2/releases/download/v0.4.0/mcp_for_sketchup_v0.4.0-signed.rbz)，Codex 侧使用 [PyPI 0.4.0](https://pypi.org/project/sketchup-mcp2/0.4.0/)。这是社区项目，不是 SketchUp 官方产品；不要混用同名的其他 MCP。已接通者先读取版本与目标，跳过安装，不为使用本 Skill 强制升级。

服务端要求 Python ≥3.10，依赖 `mcp>=1.30,<2`、`pydantic>=2.11`，不再要求 mcp 的 cli extra；解析器会按 Python 版本解析更高的依赖下限。无需学生逐包手装，uvx 会解析依赖。SketchUp 内部 Ruby 随 SketchUp 提供，无需另装系统 Ruby 或构建源码。[依赖声明](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/pyproject.toml)

推荐 uvx：它管理工具隔离环境与依赖。首次运行会下载包，缺适用 Python 时也可能下载解释器；先告知并由学生选择，不把检查当安装授权。[uv 工具说明](https://docs.astral.sh/uv/concepts/tools/)

没有 uv 时按 [Astral 官方 Windows 安装页](https://docs.astral.sh/uv/getting-started/installation/) 操作。以下为官方 PowerShell 命令，**仅在学生明确选择安装后执行**：

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

重新打开终端，用 `Get-Command uvx` 确认。不为此修改全局执行策略。Python 参照 [uv 官方指引](https://docs.astral.sh/uv/guides/install-python/)，不强制用作者电脑补丁版本。

## 3. SketchUp 侧安装、启用、启动

先保存已有工作；重启由学生确认所有未保存文档已处理，AI 不擅自关窗口。

**只有决定从0.3.x升级到0.4.0时**：先备份现有配置及扩展，记录两端版本和回退方式；依维护者要求，在扩展管理器卸载旧 MCP、重启 SU，再安装新版，不能直接覆盖旧扩展目录，否则可能残留旧文件。Codex 侧包也需改到0.4.0并重启对应连接。两端不能混用；这是升级操作，需学生明确授权，不是教学包更新就自动执行。[升级依据](https://github.com/zinin/sketchup-mcp2/releases/tag/v0.4.0)

1. “窗口 → 扩展管理器（Extension Manager）→ 安装扩展”选择下载的 RBZ；较新界面可从“扩展”菜单或扩展管理器图标进入。
2. 检查 MCP 扩展已启用，根据提示重启 SketchUp。
3. “扩展／插件（Extensions／Plugins）→ MCP Server → Settings...”查看 Host、Port、Ruby evaluation。
4. 选择 `MCP Server → Start Server`。无错误、Start Server 变灰／Stop Server 可用是运行提示，仍需读取模型。

中文菜单随 SU 版本变化，MCP 子菜单按项目 v0.4.0。安装见 [SketchUp 手动安装扩展教程](https://help.sketchup.com/en/extension-warehouse/installing-trial-extension)，启动与设置见 [维护者说明](https://github.com/zinin/sketchup-mcp2/blob/v0.4.0/README.md)。

`127.0.0.1`、`9876` 是发布默认值，不是所有电脑固定配置。已有端口不同就沿用，Codex 侧需一致。插件 TCP 端口无认证，保持本机回环连接，不为连通性开放整个局域网。

多开 SU 窗口先确定哪个进程启动服务；不同进程不能共用监听端口。读到错误文件先匹配窗口和连接，不杀进程、不停其他服务。

项目默认启用 `eval_ruby`，可执行任意 Ruby。复杂底图查询／面操作可能需要它；先看设置，不自动开启。关闭时说明能力限制，学生选择手工处理或明确选择启用。不要承诺每台 Codex 都有逐次审批框。

## 4. Codex 侧连接配置

Codex 用 STDIO 启动 Python 服务端，后者连接 SU 扩展。不要把 Ruby TCP 端口填为 Codex 的 HTTP MCP URL。

优先学习项目的 `.codex/config.toml`（可信项目才生效）。已有文件先备份，只合并对应段，不覆盖全文件或重复同名表。已有全局连接可直接用，不新增重复连接。

新配置示例，现场 SU 设置确认为默认值时才沿用地址／端口：

```toml
[mcp_servers.sketchup]
command = "uvx"
args = ["sketchup-mcp2==0.4.0"]
startup_timeout_sec = 60
tool_timeout_sec = 90

[mcp_servers.sketchup.env]
SKETCHUP_MCP_HOST = "127.0.0.1"
SKETCHUP_MCP_PORT = "9876"
SKETCHUP_MCP_TIMEOUT = "60"
SKETCHUP_MCP_LOG_LEVEL = "INFO"
```

Codex 的 60／90 秒是教程等待示例，不是兼容保证；包侧 60 秒是项目默认。首次下载慢先看日志，不无限提高超时。

找不到 uvx，将 `command` 换为本机 `Get-Command uvx` 返回的完整路径。TOML 双引号字符串里可把 Windows 路径的反斜杠改成 `/`，不复制别人路径。指定已有 Python 时可用 `args = ["--python", "本机已确认的解释器路径", "sketchup-mcp2==0.4.0"]`，占位文字必须替换。[Codex 官方 MCP 配置](https://learn.chatgpt.com/docs/extend/mcp)

保存后重新打开聊天或按设置提示重启 MCP。当前 Codex 有“设置 → MCP servers → Add server”时可选择 STDIO，填同样 command／args／env；界面不同用 TOML。

学生主动希望全局配置且已备份时可选 CLI，它会写配置，本 Skill 不默认执行：

```powershell
codex mcp add sketchup --env SKETCHUP_MCP_HOST=127.0.0.1 --env SKETCHUP_MCP_PORT=9876 --env SKETCHUP_MCP_TIMEOUT=60 --env SKETCHUP_MCP_LOG_LEVEL=INFO -- uvx sketchup-mcp2==0.4.0
```

按本机修改 Host／Port。CLI 与 TOML 二选一避免重复连接；不需要 OAuth 或 API 密钥。[Codex 官方 MCP 命令](https://developers.openai.com/codex/mcp)

## 5. 确认连接并读取当前模型

发送：

> 请只读检查 SketchUp MCP：先调用 get_version，再调用 get_model_info，报告实际版本兼容性、标题／路径、实体数量与包围盒。不要创建、移动、删除、保存或改变当前模型。

通过标准：两次调用真实成功、配对兼容、模型信息与学生目标文件一致。错误文本、isError、空工具列表、显示“启用”或端口可达均不算通过。未命名路径为空要进一步确认目标；空模型实体少可以正常。

`get_version.ruby_version` 指扩展版本，不是 Ruby 语言版本。0.4.0 两端用最低兼容版本判断，返回 `min_compatible_ruby`、`ruby_min_compatible_python`，不再返回最大兼容版本字段；不要因缺少旧 max 字段就判失败，仍须检查实际 `compatible` 与错误。`get_model_info.units` 固定为 mm，是输出单位，不证明底图尺度或模板显示单位，仍需测两段尺寸。[技术依据](sources.md)

“连接且可读”之后，住宅任务进入 [住宅路线](residential.md)。连接成功、执行过修改、保存文件、模型达到要求是不同状态，逐项给证据。

通过后才说“已连接并可读当前模型”，不擅自创建测试方块。进入 [底图准备](cad-preparation.md)或 [建模检查](modeling.md)。

## 6. 简洁排查

| 症状 | 检查与处理 |
|---|---|
| 没有工具 | 查作用域、可信项目、启用状态、日志、command 路径、TOML；重启对应 MCP，不重装 SU |
| uvx／Python 找不到 | 查本机路径与 WindowsApps 别名；需要安装由学生选择 |
| 下载失败 | 查网络、日志、Python ≥3.10 和包版本；不无限重试或随机换镜像 |
| SketchUp not running or extension not started | 查目标进程、扩展启用并 Start Server、Host／Port；修复后只读重试 |
| 端口占用／错误文档 | 确定启动服务的窗口和对应连接，不杀进程、不停其他服务 |
| IncompatibleVersionError／JSON-RPC -32001 | 查包与 RBZ 两端；0.3.x与0.4.0不可混用，授权升级时按第3步成对处理，不反复换端口 |
| Ruby evaluation 关闭 | 说明缺少哪种能力，学生选择手工处理或启用，不假装深层检查完成 |
| 截图要求新版本 | 用现有 PNG 导出或手工截图，不因截图强制升级 |
| 修改超时／SU 无响应 | 恢复后先读实际状态，不重发同次修改、不盲目 undo |

仍失败提供脱敏后的具体错误、版本和连接阶段。日志可看 MCP Server → Show Log（启用文件日志后）或 Ruby 控制台；不上传整份私人配置。
