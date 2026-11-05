---
name: website-to-video
description: "抓取通用网站/URL 并转为 HyperFrames 视频（站点导览、展示，或基于站点自身视觉的社交短片）。使用无头 Chrome 截图与品牌素材。适用于通用意图——作品集/博客/落地页展示，或基于站点视觉的社交短片。不适用于：产品/SaaS 发布或推广（→ /product-launch-video，即使从 URL 出发）；无站点的主题讲解（→ /faceless-explainer）；GitHub PR（→ /pr-to-video）；为已有视频加字幕（→ /embedded-captions）；无旁白的短页高亮动态图形（→ /motion-graphics）。发布 vs 通用站点不清楚？先问一个问题，或从 /hyperframes 开始。"
---

> **media-use**：在获取音频/图像前，调用 `/media-use` 从 HeyGen 目录解析 BGM/SFX/图像。先运行 `--adopt` 以注册已有素材。见 `/media-use` 技能。

# 网站转 HyperFrames

抓取网站，并据此制作专业视频。

> **在 Step 0 之前确认路由。** 本技能针对**通用站点**制作/基于站点制作视频。若用户实际是**营销/发布/推广产品**（即使从该 URL，即使「为我们的站点做 promo」）→ `/product-launch-video`。**无站点的主题讲解** → `/faceless-explainer`；**GitHub PR** → `/pr-to-video`；**对已有视频文件重剪/调色/重排** → 超出范围。因模糊的「做个视频」路由到这里，或不确定发布 vs 通用站点？**先读 `/hyperframes`**（完整路由表 + § HyperFrames 不能做什么）。

用户可能这样说：

- "Turn this website into a 15-second social clip for Instagram"
- "Make a 30-second site tour / showcase from https://..."
- "Capture our homepage and build a video from its own visuals"

工作流共 7 步。每一步产出工件并 gate 下一步。默认协作式——标有 💬 的 gate 会停下并询问用户。若用户表示自主模式（「你决定」「随便来」），💬 用户偏好类 gate 可跳过；传播方式见 step-2-brief.md。

**自主模式不是「跳过所有 gate」。** 自动模式覆盖用户偏好问题（TTS 提供商、音色、色彩强调、节拍数、是否要音乐、是否要字幕——由 agent 代用户决定）。**不**覆盖质量验证 gate。以下在 auto 模式下仍不可跳过：

- 素材审计（Step 3）——查看 contact sheet 并为每项素材说明 USE/SKIP 理由
- 逐 beat HTML 阅读（Step 5）——每个 beat 的结构化证据块
- DoD 清单（Step 6）——含 animation-map、逐条 warning 的 WCAG 验证、音频/动效回放
- 诚实披露小节（Step 6）——最终摘要中必须出现「我未验证的内容」

若你推理「auto 模式偏向行动，所以跳过 X」——而 X 是验证 gate 而非偏好问题——该推理错误。偏向行动适用于决定**做什么**，不适用于决定**是否验证**。

---

## Step 0：抓取与理解品牌

**阅读：** [references/step-0-capture.md](references/step-0-capture.md)

抓取站点，然后阅读提取的数据以理解**品牌与产品**——做什么、面向谁、用什么语气、什么氛围。抓取的素材是后续品牌工具箱，不是视频的直接积木。

**在 brief 之前展示登录状态**——运行 `npx hyperframes auth status`，并**原样转述其输出（不要改写或 paraphrase）。** 它会报告旁白/BGM 用 HeyGen 还是本地引擎；未登录时如何登录。**若未登录，STOP 并等待用户选择——登录，或说「go」/「offline」用本地引擎继续——再问 brief 或其他任何事。** 当作真实决策点，不是顺带一提；不要把选择揉进 brief 问题，也不要把 key 写进 per-repo `.env`。（自主模式下，记录状态并 offline 继续。）见 `../hyperframes-media` → Preflight 的规范说明。

**Gate：** 已打印站点摘要——策略优先（产品做什么、面向谁、品牌语气），再是素材/颜色/字体清单；已展示登录状态（已登录，或 offline 继续）。

---

## Step 1：品牌识别

**阅读：** [references/step-1-design.md](references/step-1-design.md)

撰写 DESIGN.md——品牌速查表，涵盖视觉识别：颜色、字体、组件风格、布局原则。用 `design-styles.json` 获取精确计算值。

**加速选项：** 快节奏视频（billboard-per-beat）时，DESIGN.md 可以是 50 行的颜色+字体+do's/don'ts 摘要——不必 300 行。Step 5 的子 agent 提示会直接粘贴品牌值，故 DESIGN.md 深度仅对复杂合成重要。

**Gate：** 存在 `DESIGN.md`（任意长度），至少含：色板、字体选择、do's/don'ts。

---

## Step 2：策略与信息

**阅读：** [references/step-2-brief.md](references/step-2-brief.md)、[references/capabilities.md](references/capabilities.md)（扫目录——需要时再深读各节）

在谈视觉或素材前，与用户对齐**视频必须传达什么**。解析用户 prompt——他们多半已给出视频类型与风格。只问缺失项：视频必须说的**一件事**、叙事弧、受众。

**Gate：** 视频类型、时长、格式，以及——关键——信息与叙事弧已锁定。否则 Step 3 无法写 concept-first 分镜。

---

## Step 3：分镜 + 脚本 💬

**阅读：** [references/step-3-storyboard.md](references/step-3-storyboard.md)

concept-first 写分镜：信息 → 叙事弧 → 服务弧线的 beats → 每 beat 技法 → 最后品牌点缀 pass。再写匹配的旁白脚本。向用户呈现两者及逐 beat 摘要。迭代直至批准。

**Gate：** 存在 `STORYBOARD.md` + `SCRIPT.md`，且用户已批准计划。

---

## Step 4：VO、时间与字幕 💬

**阅读：** [references/step-4-vo.md](references/step-4-vo.md)

若 Step 2 说不要旁白——询问背景音乐，然后跳到 Step 5。否则：问用户 TTS 提供商（HeyGen TTS、ElevenLabs 或 Kokoro），生成音频、转写、将时间戳映射到 beats。再问字幕。

**Gate：** 要么 (a) 未要求旁白且分镜有手动 beat 时长，要么 (b) 存在 `narration.wav` + `transcript.json` 且 beat 时长已按真实时长更新。

---

## Step 5：构建 Composition

**阅读：** `hyperframes` 技能（加载——每条规则都重要）
**阅读：** [references/step-5-build.md](references/step-5-build.md)

按 Step 3 分镜选的架构与节奏构建 index.html 与 compositions。子 agent 在每个 beat 回报前运行 `hyperframes lint` 与 `hyperframes snapshot`。

**Gate：** 主 agent 已对照 DESIGN.md 与 STORYBOARD.md 通读每个 `compositions/beat-N.html`。逐 beat 清单见 [step-5-build.md](references/step-5-build.md)。

---

## Step 6：验证与交付

**阅读：** [references/step-6-validate.md](references/step-6-validate.md)

Lint、validate，按视频长度缩放截图（公式：`max(beats × 3, ceil(duration_seconds / 2))`），并审阅每一张。交付前修复问题。交付 localhost Studio 项目 URL——仅在用户明确要求时渲染 MP4。Studio URL **仅在 handoff 时** surfaced——它是最终稳定预览；构建阶段截图为 headless，构建中途不要弹出预览。

**交付你引以为豪的作品。** handoff 前自问：我会愿意署名发到社交媒体吗？若否，修掉问题。

**Gate：** `npx hyperframes lint` 与 `npx hyperframes validate` 零错误通过，且最终回复含活跃 Studio 项目 URL。

---

## 快速参考

### 视频类型

按类型的典型约束——作起点，非公式。beat 数应由内容与旁白决定，而非目标区间。

| 类型                  | 典型时长 | 时长驱动因素       | 旁白             |
| --------------------- | -------- | ------------------ | ---------------- |
| 社交广告（IG/TikTok） | 10–15s   | 平台限制           | 可选             |
| 产品演示              | 30–60s   | 脚本长度           | 完整旁白         |
| 功能发布              | 15–30s   | 功能复杂度         | 完整旁白         |
| 品牌 reel             | 20–45s   | 音乐轨             | 可选，以音乐为主 |
| 发布 teaser           | 10–20s   | Hook 能量          | 极简             |

beat 数 intentionally 不在此表——应来自分镜，而非「社交广告 = 3–4 beats」。复杂产品的社交广告可能需要 5 个节奏好的 beats。视觉论点强的品牌 reel 可能只需 3 个。

### 画幅

- **Landscape**：1920x1080（默认）
- **Portrait**：1080x1920（Instagram Stories、TikTok）
- **Square**：1080x1080（Instagram feed）

### 参考文件

| 文件                                                                               | 何时阅读                                                                                                                                       |
| ---------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------- |
| [step-0-capture.md](references/step-0-capture.md)                                  | Step 0 — 抓取、理解品牌与产品、写策略优先的站点摘要                                                                                            |
| [step-1-design.md](references/step-1-design.md)                                    | Step 1 — 写 DESIGN.md 品牌速查（5 节，250–350 行；billboard 式社交广告 50 行快路径）                                                           |
| [step-2-brief.md](references/step-2-brief.md)                                      | Step 2 — 与用户对齐信息、叙事弧、受众                                                                                                            |
| [capabilities.md](references/capabilities.md)                                      | Step 2 与 5 — HyperFrames 能力全表（24 节）。brief 时扫 TOC，构建时深读具体节                                                                   |
| [step-3-storyboard.md](references/step-3-storyboard.md)                            | Step 3 — 分镜 + 脚本（合并）及用户审阅 gate                                                                                                      |
| [step-4-vo.md](references/step-4-vo.md)                                            | Step 4 — TTS 提供商选择、生成、时间对齐                                                                                                          |
| [step-5-build.md](references/step-5-build.md)                                      | Step 5 — 构建 index.html + compositions                                                                                                        |
| [step-6-validate.md](references/step-6-validate.md)                                | Step 6 — lint、validate、截图（按视频长度缩放）、预览                                                                                            |
| [techniques.md](../hyperframes/references/techniques.md)                           | Step 3 与 5 — 13 种基础动画技法及代码模式（适配，勿 copy-paste）                                                                                 |
| [html-in-canvas-patterns.md](../hyperframes/references/html-in-canvas-patterns.md) | Step 5 — HTML-in-Canvas 效果完整代码模式（位于 hyperframes 技能）                                                                              |
