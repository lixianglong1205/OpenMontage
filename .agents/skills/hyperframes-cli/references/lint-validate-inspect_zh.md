# lint、validate、inspect、snapshot

正确性流水线。按此顺序运行：`lint`（静态、快速）→ `validate`（运行时、无头 Chrome）→ `inspect`（布局扫描）。`snapshot` 是用于截取静帧的独立工具。

## 规范（动效密集型工作）

当作品以动画驱动时，在调用 `preview` 或 `render` 之前先跑检查：

- 第一版 HTML 完成后就运行 `lint`——越早越好，不要拖到最后。
- 在有意义的 timeline 状态处捕获 `snapshot`；查看 PNG。
- 在调整自动化告警之前先检查快照——肉眼能发现审计器漏掉的问题。
- 将布局告警视为缺陷，除非快照证明溢出是有意的，此时用 `data-layout-allow-overflow` 标记。
- 在 `*.motion.json` 侧车文件中声明动效意图，以便 `inspect` 自动校验——seek 下的入场、交错顺序、在画幅内、是否仍在动。这是「看 MP4」最接近的自动化替代，能发现肉眼容易漏掉的 render≠preview 问题（见下文 **动效验证**）。

## lint

```bash
npx hyperframes lint                  # current directory
npx hyperframes lint ./my-project     # specific project
npx hyperframes lint --verbose        # info-level findings
npx hyperframes lint --json           # machine-readable
```

对 `index.html` 以及 `compositions/` 下所有文件进行 lint。报告 error（必须修复）、warning（应当修复）以及 info（需配合 `--verbose`）。会捕获缺少 `data-composition-id`、同一 `data-track-index` 上轨道重叠、未注册的 timeline 等问题。

**盲点——子 composition 内的媒体（尚无 lint 规则）。** 放在 `compositions/*.html` 的 `<template>` 内（或嵌套在任意包装 `<div>` 中）的 `<video>`/`<audio>` 不会被 seek/解码，渲染为空白/黑屏；`lint`/`validate`/`inspect` 仍会通过。媒体必须是宿主根节点（`index.html`）的直接子节点——见 `hyperframes-core` → `variables-and-media.md`。在规则落地前，render 前请手动检查：

```bash
grep -nE '<(video|audio)\b' compositions/*.html   # expect NO matches; media belongs in index.html
```

非空结果即缺陷。然后对每个含视频的场景 `snapshot`，确认面板确实显示画面（本应有片段却空白/黑屏是 bug，不是占位——视为阻塞 render）。

## validate

```bash
npx hyperframes validate              # current directory
npx hyperframes validate ./my-project # specific project
npx hyperframes validate --json       # agent-readable findings
npx hyperframes validate --timeout 5000  # ms to wait for scripts (default 3000)
npx hyperframes validate --no-contrast   # skip WCAG contrast audit while iterating
```

静态 lint 很快，但对运行时失败视而不见。`validate` 在无头 Chrome 中加载 composition，播放一遍并报告：

- JavaScript 控制台错误与未捕获异常
- 失败的 network 请求（媒体文件的 `ERR_ABORTED` 会过滤掉）
- 可见文本的 WCAG AA 对比度违规——在 timeline 上 5 个时间点采样。可用 `--no-contrast` 关闭。

**修复对比度 warning**——阈值为普通文本 4.5:1，大文本 3:1（24px+，或 19px+ 粗体）：

- 深色背景上，将失败颜色调亮直至达标；浅色背景则调暗。
- 保持在色板族内——不要发明新色，微调现有色即可。
- 重复运行 `validate` 直至干净。

当动画含脚本、拉取数据或主题时，在 `inspect` 之前运行 `validate`。在 CI 中与 `render --strict` 组合使用。

## inspect

```bash
npx hyperframes inspect                 # inspect rendered layout over the timeline
npx hyperframes inspect ./my-project    # specific project
npx hyperframes inspect --json          # agent-readable findings (schemaVersion, samples, issues, bboxes)
npx hyperframes inspect --samples 15    # denser timeline sweep (default 9)
npx hyperframes inspect --at 1.5,4,7.25 # explicit hero-frame timestamps
npx hyperframes inspect --tolerance 4   # allowed overflow in px before reporting (default 2)
npx hyperframes inspect --strict        # exit non-zero on warnings too (default: only errors)
```

在 `lint` 和 `validate` 之后使用，尤其适用于含 speech bubble、卡片、字幕或紧凑排版的 composition。报告：

- 文本超出最近视觉容器或 bubble
- 文本被自身固定宽/固定高盒子裁剪
- 文本超出 composition 画布
- 子元素逃出裁剪容器

render 前应修复 error。warning 供 agent 审阅；加 `--strict` 可在 warning 时也失败。重复的静态问题默认折叠，以保持 JSON 输出对 LLM 上下文窗口紧凑。

**逃生口：**

- `data-layout-allow-overflow`——入场/退场动画等有意溢出时，标记元素或祖先。
- `data-layout-ignore`——标记不应被审计的装饰元素。

`npx hyperframes layout` 仍可作为同一视觉检查 pass 的兼容别名。

### 动效验证（`*.motion.json` sidecar）

`inspect` 还会对照 renderer 使用的同一 seeked timeline 检查 **动效意图**——最接近「render MP4 并观看」的自动化代理。它能发现布局采样抓不到的 render≠preview 问题：seek 落在入场揭示之后、错乱的 stagger 顺序、 tween 中途元素漂出画幅、画面冻结。

将 `*.motion.json` sidecar 放在 composition 旁（同一目录多个 composition 时与 html  basename 匹配）。`inspect` 自动发现——无需 flag，无需改 authoring 框架。无 sidecar 时，`inspect` 行为与以前完全一致。

```json
{
  "duration": 6,
  "assertions": [
    { "kind": "appearsBy", "selector": "#headline", "bySec": 0.5 },
    { "kind": "before", "a": "#headline", "b": "#cta" },
    { "kind": "staysInFrame", "selector": ".card" },
    { "kind": "keepsMoving", "withinSelector": ".scene" }
  ]
}
```

| Assertion                      | 失败条件（code）                                                           |
| ------------------------------ | --------------------------------------------------------------------------- |
| `appearsBy(selector, bySec)`   | 在 `bySec` 前不可见（opacity ≥ 0.5）—— `motion_appears_late`              |
| `before(a, b)`                 | `a` 未严格早于 `b` 首次出现—— `motion_out_of_order`       |
| `staysInFrame(selector)`       | 一旦可见，其 box 离开画布—— `motion_off_frame`                |
| `keepsMoving(withinSelector?)` | 完全静止窗口超过 `maxStaticSec`（默认 2s）—— `motion_frozen` |

`duration`、`withinSelector`、`maxStaticSec` 可选。Findings **默认视为 error**（断言失败即失败运行，同布局 error——`--strict` 仍只 gate warning），出现在与布局 findings 相同的人类可读与 `--json` 输出中。selector 无匹配会报 `motion_selector_missing` 而非静默通过——拼错的 selector 会 loudly 失败。在反馈环中用此替代盯 render：断言动效应做什么，让 `inspect` 在 seek 与意图不一致时告诉你。

## snapshot

```bash
npx hyperframes snapshot                       # 5 key frames as PNG
npx hyperframes snapshot ./my-project          # specific project
npx hyperframes snapshot --frames 10           # evenly-spaced N frames
```

从 composition 截取静帧 PNG，用于视觉 diff、缩略图或附到 PR。只需少量 hero 帧时比 render 视频更快。输出写入项目的 snapshots 目录。
