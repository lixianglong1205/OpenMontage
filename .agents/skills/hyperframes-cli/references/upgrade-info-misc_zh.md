# info、upgrade、compositions、docs、benchmark、telemetry、资产预处理

不适用主开发闭环的命令的汇总参考。

## info

```bash
npx hyperframes info                   # project metadata
npx hyperframes info ./my-video        # specific project
npx hyperframes info --json
```

打印**项目（project）**元数据：名称、分辨率、时长、按类型统计的元素数量、轨道数量以及项目总大小。面向项目级别——而非运行环境。若要检查环境健康状况，请使用 `doctor`。

## upgrade

```bash
npx hyperframes upgrade                # check + interactive prompt
npx hyperframes upgrade --check        # check and exit, no prompt (agent-friendly)
npx hyperframes upgrade --check --json # machine-readable: current / latest / updateAvailable
npx hyperframes upgrade --yes          # print upgrade commands without prompting
```

将已安装的 CLI 版本与 npm 上的最新版本进行比较。

## compositions, docs

```bash
npx hyperframes compositions           # list compositions in project
npx hyperframes compositions --json
npx hyperframes docs                   # list available topics
npx hyperframes docs rendering         # print one topic inline in the terminal
```

`compositions` 会列出项目中每一个 `data-composition-id`（含子 composition），并附带时长、分辨率与元素数量。

`docs` 在**终端内**打印内联文档——不会打开浏览器。主题包括：`data-attributes`、`examples`、`rendering`、`gsap`、`troubleshooting`、`compositions`。不带主题参数运行即可查看列表。

## benchmark

```bash
npx hyperframes benchmark              # run the preset matrix in current project
npx hyperframes benchmark ./my-video   # specific project
npx hyperframes benchmark --runs 5     # repeat each config N times (default 3)
npx hyperframes benchmark --json
```

使用 5 种预设配置渲染项目——`30fps draft 2w`、`30fps standard 2w`、`30fps high 2w`、`30fps standard 4w`、`60fps standard 4w`——并输出渲染速度与输出文件大小的对比。可用于在你的机器上找到可接受的最快预设。这不是单次渲染并分阶段拆解的流程。

## telemetry

```bash
npx hyperframes telemetry status      # show telemetry state
npx hyperframes telemetry disable     # disable anonymous usage telemetry
npx hyperframes telemetry enable      # re-enable telemetry
```

遥测仅包含匿名的使用计数。若更偏好通过环境变量控制，而非子命令，可在全局设置 `HYPERFRAMES_NO_TELEMETRY=1` 以禁用。

事件包含两个指纹属性，用于区分托管沙箱运行与真实笔记本电脑——不含 PII，不记录环境变量**值**，仅做存在性检查：

- **`sandbox_runtime`**：`gvisor` / `firecracker` / `docker` / `kvm` / `wsl` / `null`。gVisor 通过内核字符串与 `/proc/version` 识别。Firecracker 通过 `/dev/vsock` 与 DMI sys_vendor 识别。Docker 通过 `/.dockerenv` 与 cgroup 识别。
- **`agent_runtime`**：`claude_code` / `codex` / `cursor` / `copilot_agent` / `jules` / `replit` / `devin` / `aider` / `gemini_cli` / `hermes` / `openclaw` / `null`。通过检测常见厂商环境变量是否存在来识别；变量本身的值从不读取。

## Asset Preprocessing

```bash
npx hyperframes tts
npx hyperframes transcribe
npx hyperframes remove-background
```

这些命令会生成可放入 composition 的资产（旁白音频、词级转录、透明背景视频）。首次运行时，各自可能会下载对应的模型。

关于音色选择、Whisper 模型规则、输出格式选择以及 TTS → 转录 → 字幕链路，请调用 `hyperframes-media` 技能。本技能专注于开发闭环。
