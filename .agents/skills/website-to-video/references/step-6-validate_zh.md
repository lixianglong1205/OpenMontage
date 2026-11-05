# 步骤 6：验证与交付

这是质量关卡。在用户看到任何内容之前，**你**必须确认视频与分镜、步骤 2 的创意方向以及 DESIGN.md 一致。交付你愿意署名的成品。

## 完成定义 — 在任意预览或总结之前必须满足

**在下方每一项都检查完成之前，不得说视频已就绪、看起来不错，或给出预览 URL。** 没有例外。不要总结你的印象 — 为每一项粘贴**实际证据**。

每项按 1–5 分打分。任一项低于 3 分，先修复再继续。**不要赶工。** 每个复选框都是单独过一遍产物 — 放慢速度，看每一帧，写出**实际观察**，而不是概括印象。

```
[ ] 逐 beat 自上而下阅读 HTML    → 见下文「逐 beat 文件阅读」；粘贴逐 beat 结论
[ ] Lint：零错误                     → 粘贴 lint 输出（不要写「lint 通过」）
[ ] 已拍快照，确认 N 帧              → 写明确切帧数
[ ] 完整阅读 descriptions.md          → 逐字引用 Gemini 描述的最差一帧
[ ] 逐格查看 contact sheet            → 每个 beat 一句：画面里有什么、什么在动、有哪些品牌素材
[ ] 视频中段无暗帧                    → 明确说明哪些帧（如有）偏暗及原因
[ ] 品牌素材确实可见                  → 每个 beat 点名屏幕上哪张 captured SVG / 插画 / 截图、对应时间戳。若某 beat 零 captured 素材，说明理由。
[ ] 音频时长与视频 ±0.5s 一致         → 粘贴两个数字
[ ] 已生成 animation-map.json          → 运行 `node <repo-root>/skills/hyperframes/scripts/animation-map.mjs <project-dir>`；确认每个 beat 都有事件列出且无 bbox/flag 警告
[ ] w2h-verify 报告                   → 运行 `node <repo-root>/skills/website-to-video/scripts/w2h-verify.mjs <project-dir>`；将**完整**输出（每一行、每一个百分比）逐字粘贴到面向用户的最终总结 — 见下文「w2h-verify — 事实来源」
[ ] 音频 + 动效验证已完成             → 见下文「音频 + 动效验证」；完整播放预览，确认 SFX 落在分镜时间戳
[ ] 已运行 Critic 子 agent            → 逐字粘贴其发现的**单一**最大质量缺口
```

### w2h-verify — 事实来源

该技能运行数月，agent 读到「REQUIRED」仍跳过。verify 脚本终结这一点 — 它计算 agent 无法粉饰的事实：

- **必需产物存在**（STORYBOARD.md、DESIGN.md、SCRIPT.md、index.html）
- **品牌视觉被使用** — 至少 1 个 beat 须引用 captured 的 `hero-*`、`image-*` 或 `svgs/*.svg` 素材（logo 不算）。捕获「9% 素材使用率 / 品牌视觉上不存在」类失败。
- **标题 font-size** — 逐 beat，最大 CSS `font-size` 须 ≥80px。捕获「标题太小读不清」、后续 inspect 出现 `clipped_text` 的失败。
- **时间轴覆盖** — 逐 beat，GSAP 事件位置须覆盖 beat 的 `data-duration` 的 ≥70%。捕获「网页未拍完」：beat 只有入场 tween 然后静止。
- **Shader 转场一致性** — STORYBOARD.md 中声明的 shader 须出现在 index.html（含 HyperShader 运行时，不能只是 SFX 文件引用）。
- **SFX 时间戳漂移** — 分镜 `t=X.Xs` 与 index.html `data-start=X.X`，多时间戳 SFX 按文件为每个 index 时间戳选最近者。
- **Beat 时长一致性** — 分镜 beat 区间（`B4 — Name | 16.600 – 21.000s |`）须与 index.html 的 `data-duration` 在 ±0.5s 内一致。捕获分镜陈旧。
- **已渲染 MP4 存在** — 仅 INFO；在未渲染却声称已验证动效时标记。

在 DoD 最后一关、修完其他项后运行：

```bash
node <repo-root>/skills/website-to-video/scripts/w2h-verify.mjs <project-dir>
```

（从项目子目录定位仓库根： `find "$HOME" -path '*/skills/website-to-video/scripts/w2h-verify.mjs' -maxdepth 10 2>/dev/null | head -1`。）

**脚本输出即交付物。** 将整份报告 — 表格、百分比、FAIL 行 — 逐字粘贴到最终用户总结的「我验证了什么」/「我未验证什么」小节。用户会直接阅读。不得概括、简化或省略行。

**若任一行显示 FAIL：**

- 要么修复根因并重跑直到该行 PASS
- 要么在最终总结「我未验证什么」中逐字包含 FAIL 行，并用一句说明为何选择不修复

**禁止：**

- 手写与脚本输出不一致的验证总结
- 挑选要展示的行
- 用形容词替代百分比（「大部分素材已用」而非「8%」）
- 运行脚本看到 FAIL 却不提及

脚本退出码为 0（全过）或 1（一项及以上失败）。若以 exit=1 交付，用户从报告确切知道得到什么。

### 逐 beat 文件阅读

验证的含义现在是：打开每个 `compositions/beat-N.html`，对照 DESIGN.md 与 STORYBOARD.md 自上而下阅读。步骤 5 进入本步前已要求过一次 — 在此作为最终检查再重复，以防步骤 5 修复引入新问题。

每个 beat 按此格式写结论：

```
Beat N (Ns–Ns) — <name>
  CSS bg: <hex> (DESIGN.md 为 <hex>，匹配: yes/no)
  CSS accent: <hex> (DESIGN.md 为 <hex>，匹配: yes/no)
  Headline font-size: <px> (≥80: yes/no)
  Captured assets referenced: <来自 <img>、inline SVG、background-image 的路径列表> (分镜要求: <列表>)
  GSAP timeline coverage: 事件从 <first t> 到 <last t>，beat 时长 <N>s (完整覆盖: yes/no)
  Storyboard alignment: <一句 — 该 beat 是否交付 STORYBOARD.md 对应段落描述的内容>
  VERDICT: PASS / NEEDS FIX (<具体什么>)
```

修复前流程更慢正是因为能抓到这些问题。不要用匆匆打勾换仔细查看。

**为何重要：** 自然倾向是看 contact sheet、看到「有内容」就宣布完成。那不是验证 — 是在对完成信号做模式匹配。验证意味着打开子 agent 产出的每个文件、读每一行、报告原始结果。「14.2s 的第 7 帧显示 Raycast logo SVG 在 #07080A 上以 0.85 不透明度画完最后一笔，标题 'Crush your sprint' 以 96px Inter SemiBold 落在下方」是证据。「视频看起来很棒」不是。

---

## Lint + Validate + Snapshot

`hyperframes` 技能（步骤 5 已加载）已涵盖 lint、validate、snapshot 的机制。按该规则 — 运行 lint、validate，按视频长度缩放快照（公式：`max(beats × 3, ceil(duration_seconds / 2))`）。修复错误。本步在其上增加**流水线特有验证**。

**Errors：** 全部修复。这是真问题 — 缺少 timeline 注册、脚本损坏、素材缺失。

**Warnings：** 逐条阅读并判断。部分是必须修复的真实质量问题：

- **GSAP tween 重叠** — 多元素争同一属性 = 视觉 glitch
- **未限定作用域的选择器** — 打包后会作用于所有 composition，导致数据丢失
- **缺少 `class="clip"`** — 元素整段视频可见而非计划时段
- **根节点缺少 `data-start`** — 播放不会开始

部分是可安全忽略的风格建议：

- **文件过大** — composition 仍可用，只是难读
- **废弃属性**（data-layer、data-end）— 仍可用，只是非首选
- **轨道过密** — 信息性，非 bug

**WCAG 对比度警告 — 逐条验证，不可 blanket  dismiss。**

校验器在固定时间戳采样文字颜色。`opacity: 0`（入场前）或淡入淡出中的元素会被当作全不透明测量 — 确有误报。但这是**逐条警告**的判断，不是 blanket 借口。

**校验器发出的每条警告，在结论中粘贴此块：**

```
Warning N: <逐字引用校验器输出>
  Element: <selector>
  Sampled timestamp: t=<n>
  At t=<n>, is this element on-screen at full opacity? (yes/no — 在该时间戳快照上确认)
  Verdict: REAL ISSUE / SAMPLING ARTIFACT (一句理由)
  Action: <第 N 行 hex 修改>  OR  NONE because <原因>
```

**禁止：** 写「N 条警告大多是转场窗口误报」而无逐条证据。仅该表述即不过关。校验器不是把 158 条警告当一组报告 — 逐条报告，你逐条验证。

不要盲目忽略。不要盲目修复。逐条核实。

## 视觉验证（snapshot）

lint 与 validate 通过后，拍快照帧以**看见**自己的输出。**尽量多拍 — 在你能真正读完、看完且未遇收益递减的前提下**。这是用户看到项目前唯一的视觉反馈。你要对交给用户的东西感到自豪。

按视频缩放快照数量 — 非固定数。公式：`max(beats × 3, ceil(duration_seconds / 2))`。3 beat 10s 视频：max(9, 5) = 9 帧。8 beat 60s 视频：max(24, 30) = 30 帧。至少每 beat 3 帧：入场、hold、近出场。

```bash
# The CLI auto-loads .env from the current working directory, so a
# .env file in <project-dir> with GEMINI_API_KEY=... is enough — no
# explicit `export` needed. If you've set GEMINI_API_KEY in your shell
# environment, that works too.
npx hyperframes snapshot <project-dir> --frames <N>

# Pass a custom question to Gemini instead of the default prompt:
npx hyperframes snapshot <project-dir> --frames <N> \
  --describe "Is the brand logo visible in every beat? Is any beat showing a black or blank frame?"
```

输出在 `<project-dir>/snapshots/`。Gemini 自动写入 `snapshots/descriptions.md`。

**若 snapshot 后 `descriptions.md` 缺失或为空：** 未设置 `GEMINI_API_KEY` — 确认在 `<project-dir>/.env`（CLI 从 CWD 加载 .env）或 shell 环境。修复后重跑。

**Gemini 确实不可用时的后备**（无 key、key 无效或配额耗尽）：用你自己的读图能力直接检查 `snapshots/` 中每帧。每帧写一句屏幕内容 — 聚焦 Gemini 会抓的维度（空白/暗帧、缺品牌素材、文字可读性、布局问题）。自行保存为 `snapshots/descriptions.md`，以便清单仍有单一事实来源。在结论中明确说明描述由 agent 撰写而非 Gemini，便于用户 spot-check。

**Gemini 描述会把两帧标为「空白/黑」— 这两帧预期如此，非 bug：**

- `frame-00-at-0.0s.png` — 始终偏暗，动画尚未开始
- 视频最后一帧 — 始终偏暗，s-end dummy scene 故意不可见

视频**中间**其他被描述为「black」「blank」「no visible content」「loading screen」的帧**是 bug**。调查并修复。

**两次必读 — 都要，不能只做其一。然后写逐 beat 结论。**

1. **阅读 `snapshots/descriptions.md`** — Gemini 对每帧的客观文字分析。读每一行。不要 skim。

2. **逐格查看 `snapshots/contact-sheet.jpg`。** 不是扫一眼。看每一格，说出里面有什么。过往 agent 扫一眼就说「contact sheet 看起来不错」，却漏掉：某 beat 80% 时长视觉上全黑、logo 在屏外、标题在画布边缘被裁、字幕跑出底部。contact sheet 是这些失败集中可见的唯一地方。**每格写一句：画面内容、什么在动、哪些品牌素材、任何异常。** 若想整页概括 contact sheet，停下回到逐格。

读完两者后，为每个 beat 写结论：

```
Beat 1 (0.0s–4.5s): [Gemini 描述] | [contact sheet 显示] | PASS / NEEDS FIX
Beat 2 (4.0s–9.5s): ...
Beat 3 ...
CTA beat: ...
```

beat 仅当以下全部满足才 PASS：

- Gemini 描述与 STORYBOARD.md 计划一致
- contact sheet 显示可见内容（非黑、非空、非 loading）
- 品牌色/字体可见
- 无元素被裁或错位

「有点内容」不自动 PASS。对照**计划**，而非仅「有东西」。

**任一 beat 失败：修复、重拍 snapshot、重读 descriptions.md、从零重写逐 beat 结论。** 修复后不要沿用旧结论 — 重新评估全部，因修复可能破坏相邻 beat。

**迭代直到每个 beat 都 PASS。** 无时间上限。CTA beat 全黑不算完成。

## Critic 子 Agent — 不可跳过

**这不是可选项。逐 beat 结论全 PASS 后运行 — 在你开始 preview 之前。**

用以下**确切** prompt  spawn 子 agent：

```
You are a senior motion designer and creative director reviewing a brand video before it ships. You have high standards and have seen hundreds of these.

Read these files:
- STORYBOARD.md (what was planned)
- DESIGN.md (brand rules)
- snapshots/descriptions.md (what Gemini sees in each frame)
- snapshots/contact-sheet.jpg (view it)

Score each dimension 1–5. Be specific — name the beat and timestamp for every problem you identify.

1. **Beat execution** (1–5): Does every beat deliver what STORYBOARD.md planned? Name any beat that underdelivers and what exactly is wrong.
2. **Brand accuracy** (1–5): Does this feel made for THIS brand specifically, or could it be for any company? Name one element that is distinctly on-brand and one that is generic.
3. **Captured asset utilization** (1–5): The user captured the brand's actual SVG logos, hero illustrations, and screenshots into `capture/assets/`. Are they on screen in this video, or did the agents recreate everything from divs and CSS? List which captured assets appear in which beats. If beats are missing them, flag it — a video that recreates everything in CSS is generic, not branded.
4. **Visual quality** (1–5): Any blank frames, clipped text, centering failures, invisible elements? Cite exact frame timestamps.
5. **Motion design** (1–5): Do animations feel intentional and polished, or default and mechanical? Name the weakest transition and why.
6. **CTA beat** (1–5): Is the final beat clear, centered, readable, and does it hold long enough? Describe exactly what is visible on the CTA frame.

End with: What is the single most important fix before this ships? Name the beat, the element, and the specific change.

If you cannot find any problems and want to score everything 4–5, you are not looking hard enough. Look again.
```

读每个分数。展示给用户前，低于 3 的都要修。CTA 低于 3 就修 CTA。不要把低分 rationalize 成「用户自己决定」。

## 音频 + 动效验证 — 三条路径，选一条

快照是无声静帧。30s 30fps 视频只拍 18 张 PNG = 18/900 = 2% 帧。其余 98% — 含全部动效、转场、音频 — 快照 alone 未验证。「已通过 snapshot 确认」不算覆盖。

宣布完成前**必须**完成以下三者之一：

### 路径 1（首选）：播放 preview

通过 Playwright（或你有的其他浏览器工具）在浏览器打开 Studio URL。以 1.0× 从头到尾播放（**不要** scrub）。确认：

```
[ ] 以 1.0× 完整播放 — 真正播放，非 scrub
[ ] STORYBOARD.md 中每个 SFX：声音落在视觉时刻 ±0.1s 内
    (Beat N SFX `<file>`: 分镜 t=<x>s → 听到 t=<y>s → 漂移 <z>s)
[ ] 旁白每 beat 对应正确台词（无 off-by-one 或缺句）
[ ] 无「有音频但画面非故意处于转场中间」的时刻
[ ] 音频可听且未 clip/peak
```

### 路径 2：渲染低分辨率 MP4 并逐帧阅读

Playwright 不可用时，540p 渲染（快 — 30s 视频约 30s）并读 MP4：

```bash
node /<repo-root>/packages/cli/dist/cli.js render <project-dir> \
  --width 960 --height 540 --quality medium
```

然后至少 5fps 采样 MP4（需要时用 `ffmpeg -i <mp4> -r 5 frames/frame-%04d.png`）。顺序读这些帧。对 STORYBOARD.md 中每个 SFX 时刻，找对应帧并确认视觉匹配。

### 路径 3（最后手段）：明确延迟披露并量化缺口

本会话既无法路径 1 也无法路径 2，最终总结**必须**包含以下逐字内容：

```
**Audio + motion verification: NOT POSSIBLE in this session.**
- Snapshots cover: <N> frames out of <video_duration × fps> total (<percentage>% coverage)
- NOT verified: motion between snapshots, SFX/visual timing alignment, shader transition smoothness, audio mix levels, narration sync to beats
- Recommended user action: open the preview URL above and play start-to-end; flag anything that feels off
```

**处处禁止：**

- 用「Confirmed via snapshot」或「snapshots look right」作为音频/动效证据
- 「Preview 在跑，看起来不错」却未实际播放
- 路径 3 披露省略量化覆盖缺口（百分比 mandatory）

## Preview（始终执行）

始终启动 preview，使用户能查看并 scrub 项目：

```bash
npx hyperframes preview
```

Studio URL 是交付物。最终回复中始终包含：

```text
http://localhost:<port>/#project/<project-name>
```

使用 preview 命令输出中的实际 port 与 project name。不要把 `index.html` 当作项目链接 — 那是源文件。面向用户的项目是运行中的 Studio preview。

### 诚实披露 — 最终总结中必填

给用户的最终消息**必须**以以下两节结尾，即使全部通过。两节都在 preview URL **之后**、你结束发言**之前**。

```
**What I verified:**
- <每个通过的 DoD 项一条 bullet，内联引用实际证据>
  (e.g. "Lint: zero errors — output pasted above")
  (e.g. "Per-beat read: 7/7 beats PASS, evidence blocks above")
  (e.g. "WCAG: 3 warnings flagged, all 3 verified as sampling artifacts — see verdicts above")

**What I did NOT verify (spot-check these):**
- <每项跳过、延迟或无法完成 — 及原因>
  (e.g. "Audio + motion verification deferred — no Playwright in this session. SFX timing is computed but unconfirmed in playback.")
  (e.g. "animation-map.json skipped — script not found at expected path; manually confirmed timeline coverage in per-beat reads instead.")
  (e.g. "Beat 5 has a 0.4s window where the doc card is visible but contents are still opacity 0 — sub-agent flagged it, I chose not to fix because it was below my threshold; worth your eye.")
```

用户读此节以知道该 spot-check 什么。

**不可接受的最终总结：**

- 「Looks great, ready to ship」（无披露）
- 「All checks pass」（实际跳过某项）
- 「Sub-agents confirmed everything」（委托信任而未自证）
- 因碰巧全验证了而省略「What I did NOT verify」（仍须出现该节 — 若真无则写 "None"，但节标题必须存在）。

此处撒谎或省略比诚实跳过更糟。用户短 spot-check 胜过隐藏的坏视频。

## Render（仅按需）

**不要自动 render。** Preview 即交付 — 用户 scrub、发现微调、你再迭代。render 每轮数分钟，若用户要改则浪费。

仅当用户**明确要求** — 「render it」「make the final」「export the MP4」「I'm happy, produce the file.」

render 时**始终显式指定 quality 与 resolution。** 不要静默用默认 — 按场景选对设置并告诉用户你在 render 什么：

```bash
# Standard quality, 1080p landscape (default for most videos)
npx hyperframes render --skill=website-to-video --output renders/<name>.mp4 --quality standard --fps 30

# High quality for final delivery
npx hyperframes render --skill=website-to-video --output renders/<name>.mp4 --quality high --fps 30

# Portrait for Instagram Stories / TikTok
npx hyperframes render --skill=website-to-video --output renders/<name>.mp4 --quality standard --fps 30 --resolution portrait

# 4K for premium output
npx hyperframes render --skill=website-to-video --output renders/<name>.mp4 --quality high --fps 30 --resolution 4k
```

**可用选项：**

| Flag              | Values                                                                                     | Notes                                                                              |
| ----------------- | ------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| `--quality`       | `draft`, `standard`, `high`                                                                | draft = 快/低，standard = 平衡，high = 慢/最佳                            |
| `--fps`           | `24`, `30`, `60`                                                                           | 30 为标准，24 电影感，60 更顺滑                        |
| `--resolution`    | `landscape` (1920×1080), `portrait` (1080×1920), `landscape-4k` (3840×2160), `portrait-4k` | 别名：`1080p`、`4k`、`uhd`                                                      |
| `--format`        | `mp4`, `webm`, `mov`, `png-sequence`                                                       | 默认 mp4。mov/webm 支持透明。png-sequence 供 AE/Nuke                   |
| `--output`        | path                                                                                       | 始终设为 `renders/<project-name>.mp4` 便于识别                      |
| `--gpu`           | flag                                                                                       | 可用时用 GPU 编码（更快）                                             |
| `--crf`           | integer                                                                                    | 覆盖编码质量（越低越好，与 --video-bitrate 互斥） |
| `--video-bitrate` | e.g. `10M`                                                                                 | 目标码率（与 --crf 互斥）                                     |

告诉用户你在 render 什么及原因：「以 standard quality、1080p landscape、30fps 渲染 — 质量与耗时平衡。需要 high quality 或 4K 吗？」
