---
name: music-to-video
description: "当用户有一段音乐（音频文件，或可从视频中提取音频）并希望生成与节拍同步的 HyperFrames 视频（从舒缓到冲击感均可）时使用。音乐驱动一切：一次分析器只读一遍音轨，编排器布局各帧并填充逐帧计划，每个子代理构建一帧。字体与模板是底线——零素材也能做出完整视频——但用户提供的任意图片或视频会按同一节拍网格切入（节拍切 / Ken Burns）。流派（歌词视频、幻灯片、动感宣传片）由逐帧选择自然形成；流水线从不按流派分支。"
---

# music-to-video — 一条以音乐为基准、与节拍同步的视频工作流

使用本技能将**音乐曲目**转为与节拍同步的 HyperFrames 视频。你只需分析音轨一次、布局各帧、填充逐帧计划，并将每一帧构建为合成。输入为音乐曲目及可选的用户图片或视频——**无旁白、无网站抓取**。字体与模板是底线（零素材也能完成视频）；用户提供的任意媒体按同一节拍网格切入。

你是**编排器（orchestrator）**。在 `videos/<project>/` 下工作。按顺序执行各步骤，并在进入下一步前通过每一道 **Gate**。有两步需要用户参与：**Step 3**（计划审批）与 **Step 6**（渲染审批）。除 **Step 4** 外你亲自完成所有步骤；Step 4 中按帧派发**每个帧一个子代理**。设计与动效规则不在本文件中——它们在 `references/` 与 `frame-worker` 子代理里。

`SKILL_DIR` = 本技能目录。`PROJECT_DIR` = `videos/<project-name>/`。

工作流：Step 0 设置 → `hyperframes.json` + `assets/bgm.mp3`；Step 1 分析 → `audiomap.json`；Step 2 骨架 → `STORYBOARD.md`（帧、组为 `TBD`）；Step 3 计划 → 完整的 `STORYBOARD.md` + `frame.md`；Step 4 构建 → `compositions/frames/NN-*.html`；Step 5 组装 → `index.html`；Step 6 渲染 → `renders/video.mp4`。

## 塑造全局的两条原则

- **一个分析器，且你要信任它。** `analyze-beatgrid.py` 是唯一的节拍分析器——绝不用其他工具或凭耳重测节拍。其 energy / density / rolls / onsets / silences 始终可靠。`bpm` 与 `beats_sec` **仅在音乐确实具有节奏感时**可靠；在舒缓音乐上网格是追踪器强加的节拍器，因此应按乐句与能量定节奏，切勿硬切到网格。判断属于哪种情况由每帧的 `pacing`（Step 2）决定。
- **一帧一文件；组在帧内。** Step 2 将音轨切成**帧**，每帧对应一个合成文件 `compositions/frames/NN-<frame_id>.html`，由一个 frame-worker 构建。一帧可再细分为**组**（每组为模板或 motion-primitives 组合）。额外密度放在**组内**，因此**帧数跟踪的是不同处理手法，而非节拍数**——快歌不会爆炸式增加子代理数量。

---

## Step 0：设置、BGM 与输入

目标：确定音乐来源、创建 HyperFrames 项目，并记录用户提供的媒体。

**音乐是脊柱**——先确定一条音轨再做任何事。本技能针对**快节奏、高能量 BGM** 调优：强节拍网格驱动切镜（舒缓曲目也可，但按乐句而非节拍定节奏）。若用户给了音频——音乐文件或需从中提取音频的视频——则使用它。若没有，则生成一条：根据用户描述选情绪（如「 driving synthwave」「trap beat」「 upbeat corporate」），通过 `/hyperframes-media` 产出曲目（`references/bgm.md`——有凭证时用 HeyGen 检索，否则本地 Lyria / MusicGen；ElevenLabs 或其他生成器也可）。生成前运行 `npx hyperframes auth status`，并**原样转述其输出（不要意译或改写）**——它显示 BGM 来自 HeyGen 还是本地 MusicGen，以及未登录时如何登录。**若未登录，停止并等待用户选择——登录，或离线继续用本地 MusicGen——再生成音轨**；不要把密钥写进 per-repo 的 `.env`。（自主模式下，记录状态并离线继续。）详见 `/hyperframes-media` → Preflight 的权威说明。无论哪种方式，音轨最终落在 `assets/bgm.mp3`。暂存用户提供的图片或视频，以便各帧在节拍网格上织入；否则由字体承担整片视频。

仅在缺少 `hyperframes.json` 时初始化。根据简报用 kebab-case 命名 `<project>`，例如 `midnight-drive-loop`——不要用时间戳。`init` 会对照 GitHub 最新版检查已安装技能，若有过期则更新全局集合。

```bash
npx hyperframes init "videos/<project>" --non-interactive --example=blank
mkdir -p "$PROJECT_DIR/assets" "$PROJECT_DIR/renders"
cp "<user-music>" "$PROJECT_DIR/assets/bgm.mp3"   # extract from a video first if needed
# only if the user gave you images/videos:
node <SKILL_DIR>/scripts/stage-assets.mjs --from <dir> --hyperframes "$PROJECT_DIR" --into public
```

**品牌**（字体 + 调色板）在 Step 3 选定，不在此步。不要预先选流派或曲目类型——素材只是可选配料，流派由逐帧选择涌现。

**Gate：** 存在 `hyperframes.json` + `assets/bgm.mp3`；已记录宽高比 / 时长 / fps 及（若有）素材清单。

---

## Step 1：分析音乐

目标：产出整片视频所依赖的唯一权威 timing 分析。

`analyze-beatgrid.py` 是**唯一**节拍分析器——绝不用其他工具或凭耳重测。它读音轨一次并写入 `audiomap.json`：能量阶段（level / density / feel）、onsets + `onset_rate`、rolls、silences、`hard_stops`、`key_moments`、phrases、tempo / grid，以及 `audio.duration_sec`。它是确定性的——同一文件永远得到同一 map。多数字段对任何音乐都可靠；`bpm` 与 `beats_sec` 仅在音乐确实具有节奏感时可靠，该判断在 Step 2 做出。

**前提条件：** Python 3 可用，且已安装 `librosa`、`numpy`、`soundfile`。若 import 失败，在运行分析器前安装到当前 Python 环境：

```bash
python3 -m pip install librosa numpy soundfile
```

```bash
python3 <SKILL_DIR>/scripts/analyze-beatgrid.py "$PROJECT_DIR/assets/bgm.mp3" \
  -o "$PROJECT_DIR/audiomap.json" --print
```

**Gate：** 存在 `audiomap.json`；已知 `audio.duration_sec`。

---

## Step 2：帧骨架（仅结构）

目标：读懂音乐并布局帧——`STORYBOARD.md` 的骨架。

阅读 [`references/frame-skeleton.md`](references/frame-skeleton.md)。自行将 `audiomap.json` 转为 `STORYBOARD.md` 的**骨架**——没有中间 JSON。在真实音乐变化处（`hard_stops`、SURGE / DROP 的 `key_moments`、roll 边缘、无 onset 的段落、能量大跳）将音轨切成**帧**，每个边界对齐 audiomap 锚点。为每帧设置 `span_sec`、`pacing`（Step 1 信任判断的结论——网格真实时为 `beat_cut`，舒缓音乐上强加的节拍器时为 `phrase_flow`）、`mood`，以及一行 `feel`（Step 3 用来匹配模板的直白音乐情境）。此步只做分类与布局：每帧的 `### Groups` 留 `TBD (Step 3)`，frontmatter 的 `style` 留空——无模板、文案、颜色或字体。预期约 1–6 帧。

**Gate：** 帧铺满音轨（首帧 0，末帧 `duration_s`）；每帧含 `span_sec` + `pacing` + `mood` + `feel`；每个 `### Groups` 为 `TBD`；无任何内容填充。

---

## Step 3：填充计划（需用户门控）

目标：将骨架变为已审批、完整的 `STORYBOARD.md`。

阅读 [`references/planning.md`](references/planning.md)、[`storyboard-format.md`](references/storyboard-format.md)、[`template-catalog.md`](references/template-catalog.md)、[`motion-primitive-catalog.md`](references/motion-primitive-catalog.md)，以及（仅当用户提供素材时）[`montage.md`](references/montage.md)。在同一文件上就地编辑，做两件事：

1. **选定品牌。** 从 `../hyperframes-creative/frame-presets/` 选一个预设，对照 `../hyperframes-creative/references/design-spec.md` 中的表（匹配曲目情绪；**只有字体与颜色重要**——模板负责构图）。**原样**复制到 `frame.md`，并从其中填充 frontmatter 的 `style`（字体 + ≤4–6 个色板 swatch）。
2. **填满每一帧。** 决定其组并为每组定处理：目录中匹配的模板（绑定参数与真实 audiomap 锚点）、primitive 目录的自由 compose，或**遵守 `pacing`** 的素材处理。撰写文案。你负责 WHAT（模板 / primitives + 内容 + 锚点）；frame-worker 负责 HOW——**切勿在 storyboard 里写毫秒级 tween**。

```bash
node <SKILL_DIR>/scripts/validate-plan.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --audiomap "$PROJECT_DIR/audiomap.json" --templates <SKILL_DIR>/references/templates
```

修复每个 `✗`（硬错误：时长不匹配、帧未铺满音轨、缺少 `src`）；警告尽力而为。然后向用户展示逐帧摘要并迭代直至批准。

**Gate：** `frame.md` 为预设 verbatim 复制；`validate-plan.mjs` 退出码 0；用户已批准计划。

---

## Step 4：按计划构建帧

目标：将每一帧构建为自包含的合成文件。

创建 `compositions/frames/`。阅读 [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md) 与 `../hyperframes-core/references/subagent-dispatch.md`。**每帧派发一个 frame-worker**，尽可能并行（否则分波次）。每个 worker 只拿一帧及如下上下文：

```text
PROJECT_DIR: <abs path>
frame_id: <NN-frame_id>              # = the frame file stem, e.g. 02-f2; the composition id
Your block: the `## Frame N — <frame_id>` block in PROJECT_DIR/STORYBOARD.md
audiomap: PROJECT_DIR/audiomap.json
frame.md: PROJECT_DIR/frame.md
Materials: for each group, <SKILL_DIR>/references/templates/<id>/index.html (templates) and
           <SKILL_DIR>/references/motion-primitives/<id>/ (free); staged assets/ (asset groups)
Contracts: ../hyperframes-core/references/sub-compositions.md + determinism-rules.md
Canvas: <w>×<h>   Pacing: <beat_cut|phrase_flow>
Write to: PROJECT_DIR/compositions/frames/<frame_id>.html
```

worker  fork 所引用的材料，将所有锚点转为帧内本地秒（`local_t = track_t − span_sec[0]`），用 0ms 切对其组，并写入一个可 seek 的帧文件。**worker 从不运行 `hyperframes` CLI**——那些命令针对已组装项目，此时尚不存在，会检查错误文件。worker 只按契约写入并停止；你在组装后验证（Step 6）。每个 worker 返回后，可确认其文件已落盘。

**Gate：** 每帧在磁盘上有对应的 `compositions/frames/NN-*.html`。

---

## Step 5：组装

目标：将已构建的帧 + BGM 接入可播放的 `index.html`。

`assemble-index.mjs` 是确定性的——无子代理、无主观判断。它在各帧累计 `data-start` 处引用帧文件，在 track 11 挂载 `assets/bgm.mp3`，帧与帧之间硬切（帧铺满音轨无间隙，因此**无 transition injector**）。

```bash
node <SKILL_DIR>/scripts/assemble-index.mjs --storyboard "$PROJECT_DIR/STORYBOARD.md" \
  --hyperframes "$PROJECT_DIR" --audiomap "$PROJECT_DIR/audiomap.json"
```

修复其报告的任意 `✗`——缺失或空白帧文件表示该 worker 写了部分文件；重新派发（Step 4）并重新组装。

**Gate：** 存在 `index.html`；总时长 == `audiomap.audio.duration_sec`。

---

## Step 6：验证与渲染

目标：验证已组装视频、取得用户批准并渲染最终 MP4。

在**已组装项目**上运行 CLI——这才是正确单元（逐帧 worker 无法运行它）。`lint` 检查结构，`validate` 用无头 Chrome（捕获 JS 错误与缺失素材），`inspect` 对帧快照。

```bash
( cd "$PROJECT_DIR" && npx hyperframes lint . && npx hyperframes validate . && npx hyperframes inspect . )
```

在 `t=0`、每帧起点、最强 DROP / SURGE、每个 `hard_stops[].t` 以及最后一帧处 inspect。失败时自行做**最便宜的安全修复**：编辑有问题的 `compositions/frames/NN-*.html`。切勿改时长或音频 timing 来掩盖同步问题。门控通过后暂停供用户审阅，仅在批准后渲染：

```bash
( cd "$PROJECT_DIR" && npx hyperframes render . --skill=music-to-video -q draft -o renders/video.mp4 --fps 30 )
```

**Gate：** `lint` / `validate` / `inspect` 已通过；用户已批准；存在 `renders/video.mp4`，含音频，时长 == `audiomap.audio.duration_sec`。最终回复须给出 MP4 路径与时长。

---

## 续作对照表

| 已有                       | 从哪步继续 |
| -------------------------- | ---------- |
| 仅 `assets/bgm.mp3`        | Step 1     |
| `audiomap.json`            | Step 2     |
| `STORYBOARD.md`（骨架）    | Step 3     |
| `STORYBOARD.md`（完整）    | Step 4     |
| 全部帧文件                 | Step 5     |
| `index.html`               | Step 6     |

## 快速参考

**格式：** 默认横屏 `1920x1080`；竖屏 `1080x1920`；方 `1080x1080`。在 storyboard frontmatter 中一次性设置画布（`canvas: { w, h, fps }`）。

**脚本** 位于 `scripts/`：`analyze-beatgrid.py`（唯一分析器）、`validate-plan.mjs`（计划检查）、`assemble-index.mjs`（index 组装）、`stage-assets.mjs`（暂存用户媒体）、`lib/storyboard.mjs`（ vendored 解析器）。其余为 `hyperframes` CLI。

| 阅读                                                                                                           | 何时                                                    |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------- |
| [`references/frame-skeleton.md`](references/frame-skeleton.md)                                                 | Step 2：读音乐、布局帧、设 pacing                       |
| [`references/planning.md`](references/planning.md) · [`storyboard-format.md`](references/storyboard-format.md) | Step 3：选品牌、填满每帧、写计划                        |
| [`references/template-catalog.md`](references/template-catalog.md)                                             | Step 3：每组选模板                                      |
| [`references/motion-primitive-catalog.md`](references/motion-primitive-catalog.md)                             | Step 3/4：自由 compose 的 L0 配方                       |
| [`references/montage.md`](references/montage.md)                                                               | Step 3/4：素材处理（beat-cut / ken-burns）              |
| [`sub-agents/frame-worker.md`](sub-agents/frame-worker.md)                                                     | Step 4：派发 + 构建一帧                                 |
| `../hyperframes-core/references/subagent-dispatch.md`                                                          | Step 4：安全派发子代理                                  |
| `../hyperframes-creative/references/design-spec.md`                                                            | Step 3：选预设（品牌）                                  |

## 目录结构

```
music-to-video/
  SKILL.md
  references/   frame-skeleton.md · planning.md · storyboard-format.md
                template-catalog.md · motion-primitive-catalog.md · montage.md
                templates/<id>/          { index.html (+ assets/ · program.json) }  ← L1 catalog impls
                motion-primitives/<id>/  { index.html } (+ ../assets/gsap.min.js shared by recipes) ← L0 catalog impls
  scripts/      analyze-beatgrid.py · assemble-index.mjs · validate-plan.mjs · stage-assets.mjs · lib/storyboard.mjs
  sub-agents/   frame-worker.md   ← the one subagent (one per frame)
```
