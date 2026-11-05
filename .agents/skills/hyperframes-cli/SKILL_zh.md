---
name: hyperframes-cli
description: HyperFrames CLI 开发循环。在运行 npx hyperframes init、add、catalog、capture、lint、validate、inspect、layout、snapshot、preview、play、render、publish、lambda、doctor、browser、info、upgrade、skills、compositions、docs、benchmark、telemetry、transcribe、tts 或 remove-background，或排查 HyperFrames 构建/渲染环境时使用。AWS Lambda 云端渲染（`hyperframes lambda deploy / render / progress / destroy / policies`）的入口。
---

# HyperFrames CLI

除非项目说明指定本地包装脚本，否则一切命令均通过 `npx hyperframes` 运行。请严格遵循本地包装脚本的约定。需要 Node.js >= 22 与 FFmpeg。

## 工作流

1. **脚手架** — `npx hyperframes init my-video`（或从 URL 使用 `capture`）。`init` 还会对照 GitHub 上最新版本检查已安装 skills，若有过期则更新全局 skill 集。`--skip-skills` 标志目前已被禁用（临时措施，待 skills.sh  registry 跟上），因此每次 `init` 都会执行该检查并拉取我们最新的 skills。
2. **编写** — 撰写 HTML composition（见 `hyperframes-core` skill）
3. **Lint** — `npx hyperframes lint`
4. **Validate** — `npx hyperframes validate`（运行时错误 + 对比度）
5. **视觉检查** — `npx hyperframes inspect`
6. **Preview** — `npx hyperframes preview` 会打开 **Studio**，即时间轴编辑器，用户可在其中手动编辑任意内容（不仅是观看）。请在该处审阅，渲染前务必询问用户。
7. **Render** — 按需选择变体：
   - 迭代：`npx hyperframes render --quality draft`
   - 交付：`npx hyperframes render --quality high --output out.mp4`
   - CI / 跨主机可复现：`npx hyperframes render --docker --strict --output out.mp4`
   - 云端（长片 / 大项目）：`npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait`（见下文 Lambda）

在 preview 之前运行 lint、validate 与 inspect。`lint` 会捕获缺失的 `data-composition-id`、重叠轨道与未注册的时间轴。`validate` 在无头 Chrome 中加载 composition 并报告运行时控制台错误及 WCAG 对比度问题。`inspect` 会在时间轴上 seek，报告文本溢出气泡/容器或画布边界的情况；当存在 `*.motion.json` 侧车文件时，还会在同一 seek 时间轴上对照 motion 意图（入场在 seek 下是否触发、stagger 顺序、是否在帧内、活跃度）进行校验。

对于 motion 密集型工作，优先采用 snapshot 驱动迭代及 `*.motion.json` 侧车 — 规范与 motion 校验说明见 `references/lint-validate-inspect.md`。

## Agent 约定

适用于各命令的横切规则：

- **除 `render`、`preview`、`play` 外，所有命令均支持 `--json`。** 在 agent / CI 调用受支持命令时使用；输出包含 `_meta` 信封（CLI 版本、最新可用版本、更新建议）。`render` 仅通过 stdout + 退出码报告状态 — 成功请用下文渲染后检查验证；`preview` / `play` 为服务器，无 JSON。
- **`doctor --json` 始终以退出码 0 结束**，即使环境已损坏。请根据载荷中的 `ok` 字段做门禁：`npx hyperframes doctor --json | jq -e '.ok' > /dev/null`。这可隔离流水线免受 CLI 发布节奏影响。
- **非 TTY 模式自动检测。** 当 `stdout` 非 TTY（CI、agent、管道输出）时，CLI 自动切换为非交互；此时 `init` **必须带 `--example`**。在 TTY 上也可传 `--non-interactive` 强制该模式。
- **CI 对 render 的门禁**：`--strict` 在 lint 错误时失败，`--strict-all` 在警告时也失败，`--strict-variables` 在 `--variables` 含未声明键时失败。
- **`--json` 中的路径会被脱敏** — `$HOME` 变为字面量 `$HOME`，便于粘贴到 bug 报告与 agent 上下文。
- **Render 需用户确认。** 检查通过后切勿自动 render。在 `preview` 处暂停，告知用户可在 Studio 中编辑视频，仅在用户批准后 render。
- **渲染后验证。** `render` 返回退出码 0 后，确认输出文件存在且大小合理再报告成功：`[ -s "$OUTPUT" ] || echo "render produced no output"`。成功时 CLI 会打印 `◇  <path>`；长片渲染还可用 `ffprobe -i "$OUTPUT" -show_format -v error`  sanity-check 时长。

## 路由

| 想要…                                                                                                   | 阅读                                  |
| ---------------------------------------------------------------------------------------------------------- | ------------------------------------- |
| 搭建项目（`init`、`capture`、`skills`）                                                           | `references/init-and-scaffold.md`     |
| 检查正确性（`lint`、`validate`、`inspect`、`snapshot`）                                              | `references/lint-validate-inspect.md` |
| 预览或渲染（`preview`、`play`、`render`、`publish`）                                                 | `references/preview-render.md`        |
| 诊断环境（`doctor`、`browser`）                                                             | `references/doctor-browser.md`        |
| AWS Lambda 云端渲染（`lambda deploy / sites / render / progress / destroy / policies`）              | `references/lambda.md`                |
| 其他（`info`、`upgrade`、`compositions`、`docs`、`benchmark`、`telemetry`、资源预处理） | `references/upgrade-info-misc.md`     |

## 跨 Skill 交接

- **Tailwind 项目**（`init --tailwind`）→ 编辑 class 或 theme token 前先使用 `hyperframes-core`（Tailwind 参考）。
- **Registry 块/组件**（`hyperframes add`、`hyperframes catalog`）→ 安装路径、子 composition 接线与 snippet 合并见 `hyperframes-registry`。
- **资源预处理**（`tts`、`transcribe`、`remove-background`）→ 音色选择、Whisper 模型规则、字幕及 TTS 到字幕链路见 `hyperframes-media`。
- **参数化渲染**（`--variables`）→ 通过 `<html>` 上的 `data-composition-variables` 声明；完整 schema 见 `hyperframes-core`。

## Lambda（云端渲染）

`hyperframes lambda` 将分布式渲染部署到 AWS Lambda，并从本机或 CI 驱动渲染。端到端三条命令：

```bash
npx hyperframes lambda deploy                                             # provision SAM stack (Lambda + Step Functions + S3)
npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait
npx hyperframes lambda destroy                                            # tear down (S3 bucket is retained)
```

当渲染过长/过大不适合单机（多分钟视频、4K、大批量并行）且已配置 AWS 凭证时使用 Lambda。开发循环迭代请继续用本地 `render`。

前置条件、全部 6 个子命令（`deploy`、`sites create`、`render`、`progress`、`destroy`、`policies`）、IAM 策略校验、状态文件及成本/清理规则见 `references/lambda.md`。

## 最低完成门禁

### 静态门禁

```bash
npx hyperframes lint
npx hyperframes validate
```

布局敏感的工作请加上 `inspect`；CI 中使用 `render --strict` 以便 lint 错误时失败。

### 视觉冒烟测试 — 项目使用子 composition 时必填

`lint` / `validate` / `inspect` 分别**独立**评估每个 composition。它们不会加载 `index.html`，也不会通过 `data-composition-src` 挂载子 composition，因此无法捕获跨文件挂载失败（见 `hyperframes-core` → `references/sub-compositions.md` 中 “Common pitfalls”）。唯一能捕获的门禁是实际加载 `index.html` 并在时间轴上 seek 的流程。

使用 `hyperframes snapshot` — 它与 `render` 以相同方式加载项目（走相同挂载路径），但只捕获你指定的时间戳，因此只需数秒而非完整渲染：

```bash
# Capture one frame at the midpoint of every sub-composition.
# Midpoints = data-start + data-duration/2 for each host slot in index.html.
npx hyperframes snapshot --at <t1>,<t2>,<t3>,...

# Or, if you don't need per-scene targeting, an evenly-spaced sample:
npx hyperframes snapshot --frames 9
```

输出位于 `snapshots/frame-NN-at-Xs.png`。对照场景计划逐帧目视检查。

逐帧红旗（各对应静态门禁无法捕获的特定失败模式）：

| 你看到的情况                                                                       | 根因                                                                                  |
| ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| 文本在左上角显示极小且无样式                               | `<style>` 块留在 `<head>` 中、位于 `<template>` 外（Pitfall 1）— CSS 未进入 live DOM |
| SVG/图标元素被放大到画布尺寸                                          | 同上 — 未应用 width/height 约束                                         |
| 场景主元素完全缺失；仅背景与水印可见 | Host-id ≠ template id（Pitfall 2）— 时间轴未运行，帧停留在初始状态     |
| Snapshot 命令日志出现 `Sub-composition timelines not registered after 45000ms`     | Pitfall 2 — 直接确认                                                             |

目视检查完成后可删除 `snapshots/`；面向用户的最终渲染是单独一步 `npx hyperframes render`。
