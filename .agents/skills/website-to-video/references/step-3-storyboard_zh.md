# 步骤 3：分镜 + 脚本

营销视频以概念为先。**顺序是：信息 → 叙事弧线 → 服务于弧线的节拍 → 用哪些素材与技法让每个节拍活起来。** 抓取的素材（SVG  logo、品牌插画、主视觉、渐变）与合成节拍一样，是一等公民的节拍内容——其中许多会自带独立节拍。唯一约束是：不要从素材清单出发（「我们有这些截图，做个幻灯片吧」）。从信息出发，再为每个节拍织入合适的抓取素材与合成元素。

**写节拍前先读 `capture/extracted/asset-descriptions.md`。** 了解抓取里有什么。品牌真实的视觉识别——真实 logo、真实插画、真实渐变、真实主视觉——才是让视频像「这一家」而不是通用暗色电影模板的关键。多数节拍会叠用一两个抓取素材与合成动效。

## 第一个决策：CONCEPT（概念）

在节奏、节拍或任何其他内容之前——在 `STORYBOARD.md` 顶部写好概念块。承接步骤 2 简报里已定的内容：

```markdown
**Message:** [本视频必须传达的唯一信息——一句话]
**Arc:** [Problem→Solution / Reveal / Demonstration / Vibe / Comparison — 以及一句话说明如何展开]
**Audience:** [谁在什么场景看——TikTok 划屏、LinkedIn、落地页嵌入]
**Brand voice:** [自信 /  playful / 临床 / 紧迫 / 高端 — 来自 DESIGN.md]
**Why this matters now:** [若相关则写 GTM 背景——发布、功能上线、品牌 reposition、持续 demo]
```

若任一行空白，分镜无法落地。回到简报——不要用「展示看板」代替信息。

**单句测试：** _「这段视频与任意 [行业] 品牌的通用 [视频类型] 有何不同？」_ 若无法从上面几行回答，概念不够锋利。写节奏或节拍前先 sharpen。

---

## 第二个决策：PACING（节奏）

概念锁定后，选服务于它的节奏。这决定节拍数量、时长与架构——下游选择都由此而来。

读概念块里的信息与弧线，以及步骤 2 简报的风格方向。映射到下列之一：

| 用户说法                                                   | 节奏       | 节拍数 | 节拍时长 | 架构                                               |
| ----------------------------------------------------------- | ------------ | ---------- | ------------- | ---------------------------------------------------------- |
| "fast", "punchy", "rapid cuts", "energetic", "social ad"    | **Fast**     | 8–15       | 0.7–1.8s      | 单文件堆叠节拍，硬切                       |
| "demo", "walkthrough", "product tour", "show features"      | **Moderate** | 4–6        | 3–5s          | 子合成，CSS 交叉淡入                          |
| "cinematic", "premium", "slow", "let it breathe", "elegant" | **Slow**     | 3–4        | 5–8s          | 子合成，长交叉淡入                          |
| "launch", "announcement", "story", "narrative"              | **Arc**      | 5–7        | varies        | 慢开场 → 中段递进 → 快峰值 → 收束结尾 |

**在 STORYBOARD.md 顶部写下节奏选择。** 示例：`**Pacing: Fast** — 12 beats, stacked divs, hard cuts.`

若用户说「dark cinematic feel」——那是 SLOW，不是 fast。若说「rapid cuts, bold typography」——那是 FAST。提示明确时不要默认 moderate。

---

## 技法选择清单（必填，写节拍文案之前完成）

对每个计划中的节拍，点名 **2–4 种技法**。只有一种技法的节拍等于幻灯片帧——若说不出两种，重设计该节拍。

从 [capabilities.md](capabilities.md) 的清单与 [techniques.md](../../hyperframes/references/techniques.md) 的实现模式里选。可组合节拍示例：

```
Beat 3: composed kanban (4 cards-as-divs per column) + counter chip on In-Progress + back.out entrance stagger
  techniques: layered panels (capabilities §1), counter via tl.set (techniques #15),
              GSAP stagger with back.out(1.7) (techniques #4)
  customize:  real project name "Atlas Q3", brand purple #5b3fff, realistic backlog items
```

**Customize 才是实际交付物**——让该节拍成为「这一品牌」的节拍。品牌色、真实内容、旁白同步时机。泛泛的「展示看板」、无具体技法、无 customize 计划、无品牌数据 = 偷懒。节拍须从本品牌身份发明，而非从通用 UI 形状拼装。

---

**写之前重读这些文件：**

- **DESIGN.md** — 色板、字体规则、组件、Do's/Don'ts。每个画面须 grounded 于该品牌身份。若写「白底紫强调」——规划亮场景，而非暗色情绪。
- **素材发现——仔细看联系表，每个格子。** 打开 `capture/assets/contact-sheet-*.jpg` 与 `capture/assets/svgs/contact-sheet-*.jpg`。两者都分页——看每一页（`contact-sheet-1.jpg`、`contact-sheet-2.jpg` 等）。**每页在继续前，列出你能看到的 5 个具体素材。** 过往 agent 扫一眼就说「看过联系表」，随后写的节拍引用不存在的素材或漏掉品牌 logo。别成为那个 agent。找到值得进节拍的素材时，记下标签上的文件名，引用为 `capture/assets/<filename>`。若缩略图太小无法判断分辨率/细节，打开单文件。另读 `capture/extracted/asset-descriptions.md` 一行摘要。**切勿在视频里直接用联系表或滚动截图**——联系表带网格标签；滚动截图是原始浏览器抓取。二者供 AI 浏览理解站点，不是放进合成。
- **[techniques.md](../../hyperframes/references/techniques.md)** — 13 种基础动画技法与代码模式。为节拍挑选，是改编起点，不是复制模板。
- **[text-effects.md](../../hyperframes/references/text-effects.md)** — 来自独立 `pixel-point/animate-text` 技能的 24 种命名文字动效。参考页说明如何加载上游技能；ID 内联列出。每个节拍里每个标题、标签、文案元素指定具体 effect ID——不要写泛泛的「淡入」。

分镜是创意北极星。告诉工程师每个节拍要建什么——情绪、镜头、动画、转场、素材、外观、声音。像在给从未见过该网站的动效设计师写 brief。

**纳入用户具体要求。** 若要「3D MacBook 揭示」——写进分镜。若说「惊喜我」——可以大胆，但保持在风格方向内。

保存为项目目录下的 `STORYBOARD.md`。

---

## 考虑：调研能否让视频更好？

深入节拍前暂停：**聚焦调研能否显著提升视频？**

并非总是需要。简单 SaaS 社交广告可能不需要市场研究。但有些视频受益于站点本身给不了的语境：

**需要调研时：**

- 视频面向竞争激烈市场——看竞品如何呈现产品、行业视觉语言、当下趋势
- 代表你不太了解的公司/产品——搜评测、报道、用户观点、公司史，理解受众在意什么
- 用户要领域内特定东西——金融科技发布视频受益于理解 Stripe、Ramp、Mercury 如何视觉定位
- 视频需引用站点没有的真实数据、趋势或语境

**跳过调研时：**

- 从清晰网站做直截了当的品牌片或社交广告
- 用户给了非常具体的创意方向（「就要 X、Y、Z」）
- 网站已含所需全部语境（功能、数据、证言）

**调研什么：** 领域内竞品视频、行业流行视觉风格、受众预期、有助于更好创意决策的公司背景。两分钟网页搜索可区分泛泛视频与像懂市场的人做的视频。

---

## 全局方向（Global Direction）

每个 STORYBOARD.md 以全局设置开头：

```markdown
**Format:** 1920×1080
**Audio:** [TTS provider] voiceover + underscore + SFX
**VO direction:** [voice character — e.g., "mid-age male, calm confident delivery,
Apple keynote register — economy of words, silence between sentences is a feature"]
**Style basis:** DESIGN.md (brand colors, fonts, components from the captured site)
```

**全局护栏** — 先读 [video-composition.md](../../hyperframes/references/video-composition.md)。它定义媒介规则：密度、色彩存在感、尺度、帧构图，以及 design.md 是品牌真理而非布局 spec。再应用下列抓取相关补充：

- 抓取素材是合成节拍上的点缀，不是节拍本身——见下文 Asset Audit，哪些素材值得出现（通常全片 2–4 处）。
- 使用 techniques.md 里不同技法——不是全片一种，而是**每个节拍**。不要默认基础 fade/scale/opacity——混用 SVG 路径绘制、HTML-in-canvas、shader、滚动或运动效果、CSS 3D 变换、打字效果、计数动画、canvas 程序化艺术。每个节拍应像独立视觉世界。按分镜需要多用。

**垫底音乐/音乐方向**（若适用）：

- 描述情绪、参考艺人、何时 swell 或 drop
- 示例："Minimal electronic. Warm sustained pad already playing when the video starts. Sits underneath everything, never competing with VO. Swells gently during the flex section, drops to near-nothing for the comparison, resolves on a final chord."

---

## 必填：能力发现（Required Capabilities Discovery）

写任何节拍前，须运行下列命令，将输出贴在 Global Direction 下方。这告诉你标准技法之外还有什么。

```bash
# 1. Check available shader transitions (installed in registry/blocks/)
ls registry/blocks/ 2>/dev/null | grep -E 'chromatic|cinematic|cross-warp|domain-warp|flash|glitch|gravitational|light-leak|ridged|ripple|sdf|swirl|thermal|whip' || echo "No shader transitions installed"

# 2. Check available VFX blocks
ls registry/blocks/ 2>/dev/null | grep vfx || echo "No VFX blocks installed"

# 3. Browse what's available to install
npx hyperframes catalog --type block 2>/dev/null | head -40
```

可能有 VFX 块（vfx-liquid-glass、vfx-iphone-device、vfx-shatter、vfx-portal 等），用于主视觉处理而非基础透视倾斜。需要的用 `npx hyperframes add <name>` 安装。Shader 不要过多——除非用户另有要求，每视频最多 2 个。

**Shader 转场——块名 ≠ shader 名。** 上面命令在 `registry/blocks/` 看到 `domain-warp-dissolve` 时，HyperShader 运行时名是 `domain-warp`（无 "-dissolve"）。安装块后打开其 showcase HTML（`compositions/<block-name>.html`），找 `HyperShader.init()` 里实际 shader 名。那才是写进分镜的名字。然后删 showcase 文件——仅为 demo，会污染 compositions/ 并产生 lint 警告。

## 素材审计（Asset Audit）——写节拍前必填（不可跳过）

本技能首要目的是**使用**品牌抓取素材——不是用 CSS 重建。多数节拍应至少含一个抓取素材：主插画、标志性 SVG、产品摄影、品牌 mark、 distinctive 图形。**若 STORYBOARD.md 结束时只用了 logo，本步骤失败。**

**为何设此关卡：** 早期会话自写「Asset Audit」，65 个抓取里 60+ 标 SKIP，只用 logo，成片视觉上与通用暗色 SaaS 发布无法区分。抓取的 MetaBrain 插画、GitHub-sync 图、知识库主视觉——全闲置。让品牌可识别的 signature 视觉缺席。勿重复。

**分镜前必做流程：**

1. **查看 `capture/assets/contact-sheet-*.jpg` 每一页** 以及 **`capture/assets/svgs/contact-sheet-*.jpg` 每一页。** 这是 capture 为此生成的表。打开每页；逐格扫描。勿 skim——你在逐帧找品牌视觉身份。

2. **对每个联系表页，在 STORYBOARD.md 的「Asset Audit」下粘贴此块：**

```
Contact sheet: capture/assets/contact-sheet-1.jpg (page 1 of N)
  5 most visually distinctive assets I see (filename + one-sentence description of what the image shows):
  1. <filename>: <what's actually pictured — not the filename, the content>
  2. <filename>: <description>
  3. <filename>: <description>
  4. <filename>: <description>
  5. <filename>: <description>
```

对每个联系表页重复。页数 × 5 即候选素材池。

3. **对 STORYBOARD.md 中每个节拍**，对每个候选素材选 USE 或 SKIP：
   - **USE** 表示构建时该素材出现在节拍 HTML（`<img src=...>`、inline SVG、`background-image: url(...)`）。
   - **SKIP** 须一句话说明为何不服务该节拍。「不符合分镜」不是理由——点名哪个分镜时刻找不到用途。

4. **品牌默认下限：** 至少**一个**节拍须用品牌 signature 视觉（主插画、主摄影或 signature 图——不是 logo）。若步骤 2 列出 5+ 候选主插画却零个进任何节拍，即本关卡要抓的失败模式。

**禁止：**

- 除 logo 外每个素材写 SKIP 且无逐条理由
- 只读 `capture/extracted/asset-descriptions.md`（文本）凭文件名决策，不打开联系表
- 品牌 GitHub-sync 图 SVG 已在 `capture/assets/` 却结论「用 CSS 重建 GitHub-sync 图」。用真实素材。

若最终节拍表使用相关抓取素材不足约 30%（相关 = 除 favicon 与 tiny UI 图标外）， revisit。品牌视觉靠自有美术承载；用 div 重建会抹掉可识别性。

### HTML-in-Canvas — 在此规划，步骤 5 构建

`drawElementImage` Chrome API 以 60fps 将任意 live HTML/CSS 捕获为 GPU 加速纹理。这是 HyperFrames 最高影响能力——可让抓取的产品截图或 UI 经以下渲染：

- **3D 几何** — 旋转 iPhone 或笔记本模型、球体、曲面
- **WebGL shader** — liquid glass 折射、碎裂、portal 揭示、噪声扭曲
- **后期** — bloom、景深、胶片颗粒、调色

规划节拍时，决定哪些值得 HTML-in-Canvas 处理 vs 标准 GSAP。若要，在分镜里命名——步骤 5 读 [`../../hyperframes/references/html-in-canvas-patterns.md`](../../hyperframes/references/html-in-canvas-patterns.md) 实现。此处无需 API 细节。

### SFX 分配 — 在此完成，不在步骤 5

**写节拍前，** 读 SFX manifest。从当前目录定位：

```bash
find "$HOME" -path '*/website-to-video/assets/sfx/manifest.json' -maxdepth 10 2>/dev/null | head -1
```

若已复制 SFX 到项目（步骤 5 会做），读本地 `sfx/manifest.json`。每项有 filename、秒级 duration、description。在分镜里为**确切时刻**指定**具体 SFX 文件**。步骤 5 实现此处规定——不做 SFX 决策。

每节拍 SFX 示例：

- `sfx/impact-bass-1.mp3` at `0.2s`, volume `0.35` — 主图 snap 入画时
- `sfx/chime.mp3` at `3.8s`, volume `0.5` — logo 出现时

**少即是多。** 多数节拍零 SFX。典型每节拍一个；仅当节拍有真正 distinct 标点时刻才多个。勿直接在 shader 转场上放 SFX——shader 转场本身已是视听事件。

**各类声音如何放置**（行业惯例）：

- **Impact/hit**（`impact-bass-1`、`ping`、`pop`、`glitch-*`）：峰值在 clip 开头。恰好在视觉时刻触发。让 decay tail  bleed 进下一场景——正常，称 J-Cut，听起来专业。`data-duration` = manifest 完整 duration，勿裁切。
- **Riser/build-up**（`riser`、`whoosh-cinematic`）：峰值在 clip **末尾**。要让峰值落在 climax（转场、揭示），在 `climax_time - sfx_duration` 触发。`riser.mp3`（10.03s）在 t=20s 转场峰值：t=9.97s 触发。
- **短 accent**（`click`、`click-soft`、`chime`、`sparkle`、`ping`）：恰好在视觉标点时刻触发。时长短，无 tail 顾虑。

**SFX 与旁白重叠时的音量：** HyperFrames 无自动 ducking。若 SFX 在 spoken narration 下播放，volume 最高 0.2–0.3，非 0.5+。在分镜条目写明以便步骤 5 正确接线。

**data-duration 规则**（步骤 5 实现）：始终等于 manifest duration 字段 exactly。勿为「 fit 剩余节拍时间」设更短——impact 中途截断正是 v2 视频 cut-off 声的根因。

### 架构约束：每个节拍是独立合成

每个节拍建为独立 HTML（`compositions/beat-N.html`）。独立加载——**不**与其他节拍共享 state、WebGL context、Three.js scene 或 DOM。因此：

- **节拍间无「持久」元素**——不能 MacBook 模型驻屏而仅 2、3、4 节拍换屏内容。每节拍从零加载自己的 MacBook。若要视觉连续，每节拍须独立把元素设到相同位置/旋转，**看起来**连续。
- **无共享 3D 场景**——用 Three.js 的节拍各自创建 renderer、scene、camera。若 2、3 都显示旋转笔记本，各自独立加载模型且须从匹配位置开始。
- **Shader 转场在节拍之间**（index.html），不在节拍内。勿规划节拍「内部」shader 转场。

在此约束内规划分镜。若描述「MacBook 原位 while 内容 swap」，须说明每节拍独立在同一位置重建 MacBook——不是持久存在。

### 设备 mockup：用 Registry 块

分镜要 MacBook 或 iPhone mockup 时，用预建 `vfx-iphone-device` registry 块——含 **iPhone 15 Pro Max 与 MacBook Pro** GLTF、live HTML-in-Canvas 屏、镜头编排、玻璃镜头 morph。`npx hyperframes add vfx-iphone-device` 安装。

**勿**从零手写 Three.js 设备场景。Registry 块正确处理 UV、屏纹理、光照、角度。手写版 consistently 坏屏纹理、错误 UV flip、路径解析 bug。用块。

---

## 逐节拍方向（Per-Beat Direction）

每个节拍是一个 **SHOT（镜头）**，不是布局。写**镜头做什么**、**画面揭示什么**——不是「页面上元素摆哪」。

### 节拍是镜头——写 CSS 前先定景别

每个节拍标题首行应声明 shot type。**景别：**

| Shot                  | 用于                                                                                  | 画面包含                                               |
| --------------------- | ---------------------------------------------------------------------------------------- | --------------------------------------------------------------------- |
| **Extreme close-up**  | 单卡/数字/字符/光标/按钮作为整帧主体               | 一元素占帧 60–90%，其余 blur 或 absent  |
| **Close-up**          | 小 UI 区域（单列、卡堆、图表、代码块）                 | 主体占帧 40–60%，后方 depth 分层语境   |
| **Medium**            | UI 一段——三列看板、三条消息聊天、两三 panel 仪表盘 | 主体占帧 60–80%，邻近 UI 边缘 bleed in        |
| **Wide**              | 完整 UI  assembly 可见——仅当**整体**才是重点                        | 完整 UI 70–90% scale， deliberate 负空间                |
| **Over-the-shoulder** | 观众在用户「身后」——光标/手/设备前景，UI 中景              | 前景占下 1/3，UI 填上 2/3，视差 depth |
| **Dutch angle**       | 张力、紧迫、「不对劲」                                                      | 帧倾斜 4–8°，内容构图不稳           |

**「Wide shot」陷阱：** _每个_ 节拍 wide 都像 CSS 截图。多数产品 demo 应是 60% close-up + close-up + 20% medium + 10% wide + 10% extreme close-up。Wide 是 rare  establishing，非默认。

### 镜头运动是主体，不是元素

网站思维：元素 animate in，然后静止供阅读。视频思维：**镜头穿过场景**。构图在变。

每个节拍至少一种 camera-style move。从中选：

- **Dolly in** — 构图 scale 1.0 → 1.08 跨节拍时长， slight x/y drift
- **Dolly out / pull-back** — scale 1.15 → 1.0，揭示更多语境
- **Push** — 关键瞬间快 scale-up（1.0 → 1.05，~0.5s power3.out）
- **Parallax pan** — 背景与前景反向不同速 drift
- **Orbit** — 主体 3D 旋转，或镜头环绕
- **Rack focus** — blur 从一元素移到另一（背景 blur 前景 sharpen）

若节拍**无** camera-style move 且元素仅在开头 animate in，会像带 entrance 动画的网页。那不是视频节拍。

### 禁止模式（视频当网页的失败）

子 agent  revert 网站思维时几乎每次迭代都会出现。拒绝写含下列内容的节拍：

- ❌ **macOS / 浏览器窗口 chrome** 框内容——traffic-light、URL bar、标签、面包屑——**除非**节拍概念就是 chrome 本身（如「macOS 窗口本身是镜头主体」）
- ❌ **侧栏、导航轨、页头、页脚**，除非节拍演示导航概念
- ❌ **「居中 card/panel/window，四边 60–120px margin」**——标准网页布局；视频用满帧与 meaningful 负空间
- ❌ **「Hold with breathing」微动画**——元素 y: ±1–2px 或 scale 1.01——视频分辨率不可见；子 agent 假装有 motion 实则没有
- ❌ **Settled hold 超过 1.5s** 且无持续镜头或构图变化——加 camera dolly、depth parallax 或 mid-beat 新 sub-element 进入
- ❌ **Hover 状态演示**——视频无 hover；若要传达 hover 效果，用 discrete 前后帧，非 hover 模拟
- ❌ **「提供语境」的 tooltip 与 modal**——视频用视觉语言，非 popup 提示

### 每个节拍必填（视频语法下限）

每个节拍视觉描述须指定：

1. **Shot type**（上述六种之一）
2. **Camera move**（哪一种、何时开始、持续多久）
3. **Depth strategy**（前景/中景/背景各有什么、如何 parallax）
4. **视频尺度可读的 motion 幅度**（y/x 移动 30px+，scale 变化 ≥0.05，opacity 过渡 ≥0.5）
5. **镜头目的**——这 3–5 秒观众应**感受或注意到**什么？

---

### 既有节拍级字段（在下）叠在 shot grammar 之上

每个节拍是一个 **WORLD**，不是布局。写观众**体验**再写 CSS spec。

**Motion 动词**——每个动画元素一个。从节拍概念选，非 energy bucket：

- **Impact:** SLAMS, CRASHES, PUNCHES, DROPS, SHATTERS
- **Directional:** SLIDES, PUSHES, WIPES, CUTS
- **Reveals:** DRAWS, FILLS, GROWS, ASSEMBLES, COUNTS UP
- **Organic:** FLOATS, DRIFTS, BREATHES, PULSES, ORBITS
- **Mechanical:** TYPES ON, CLICKS, LOCKS IN, SNAPS, STEPS

**转场决策矩阵** — shader vs CSS vs hard cut：
| Shader transition for | CSS crossfade for | Hard cut for |
|---|---|---|
| Hero 揭示、logo  unveil、「wow」时刻 | 节拍间连续 motion、编辑节奏 | 快切列表、 percussive 剪辑、喜剧 timing |

每视频 1–2 个 shader 转场（hero + CTA）。过多 flatten  impact。同一 HyperShader 合成可混 shader 与 CSS crossfade——任意 transition entry 省略 `shader`。

**Rhythm** — 实现前声明场景 rhythm：fast-fast-SLOW-fast-SHADER-hold。Rhythm 来自品牌与内容，非模板。

用本步骤顶部定的 pacing。节拍数、时长、架构已设定。

**剪片匹配旁白长度**——若脚本产生 22 秒音频，视频应 24 秒含 2 秒 CTA hold，非 30 秒末尾 8 秒 dead silence。末尾空转丢观众。

**满帧规则：** 逐节拍描述视觉时用**占帧百分比**，非像素。「产品截图占帧 80%」非「600px 宽 card」。

**用节拍需要的任意 primitive——可单独或组合。** 一层可叠 HTML/CSS、SVG（抓取或手绘）、WebGL/Canvas shader、Three.js、抓取插画与摄影、kinetic typography、抓取 Lottie——场景需要可全开。它们是单一输出（视频帧）的输入；无意图→primitive 硬映射。视频应**每一帧都 alive**——连续、可触的 motion，**像物存在于物理世界**。窄 no-go：勿把产品 UI 截图当 load-bearing 内容（slideshow 模式）。其余开放。

**开场默认：快 intro 停住划屏者。** 即使 cinematic 也应 punch 开场——flash、shader bloom、logo strike、kinetic word build、particle burst——anything 在首 1.0–1.5 秒内落地。慢 intro 适合 prestige trailer；社交/ feed 视频需 beat 1.5 秒 scroll 阈值的 hook。把 opener 规划为分镜最 ambitious 节拍，非最 gentleness。

**CTA / 收尾节拍** consistently 最弱。Agent 当「logo + tagline + done」。好 CTA：logo 入场是事件（SVG path draw、scale overshoot 或任何 awesome）、背景持续 motion、最后 spoken word 后仅 hold 2–3 秒——**非** 8–10 秒 silence。

**VO 起始时机——在此决定，非步骤 5。** 旁白相对第一视觉何时真正开始？选项：(a) VO 在 visual intro 上开始（内容 settle 前听到——紧迫），(b) visual intro settle 后开始（先看开场再听——戏剧），(c) 几秒纯音乐 visual 再进 VO。无默认——按品牌与 opening beat 概念选。在分镜 Global Direction  Explicit 写 intended narration start，如 `**Narration start:** 0.8s (after hero intro settles)`。步骤 5 用 audio 元素 `data-start` 接线。

**Concept-first 节拍。** 每节拍从 **CONCEPT** 开始——非「用什么技法」而是「这场景应展示什么，上一场景展示了什么、下一场将展示什么…？」传达什么 idea？疯狂有趣的 concept 驱动每个技术决策。

在 capture pipeline 中，每节拍含：

### Concept

相对前序（若有）与后续场景，这场景**代表**什么？非「展示功能」而是具体 idea 与 logic。

### VO cue

哪句旁白盖在此节拍（同时牢记全片 narration flow）。

### Visual description

观众所见——电影化描述，非 CSS spec。用镜头语言与 production motion designer 词汇（pan、zoom、drift、settle 等）。分层思考——前景、中景、背景同时发生什么？

**当抓取素材是主视觉**（logo 开/收、带 parallax 主插画、带 motion 处理主摄影、全 bleed 渐变背景等）：指定哪一素材、占帧多少（%）、文字/标签相对其 safe zone 位置。勿盲 center 文字于 busy 产品 UI。窄 no-go：勿把产品 UI 截图全 bleed 当节拍内容——即本 workflow 要打破的 slideshow。抓取 logo、插画、主视觉、摄影在 concept 需要时可作主视觉。

### Composition + Accents

两件事，均必填：

**Composed（load-bearing——承载节拍）：**

- 描述从零构建的 UI/元素/场景：markup 结构、驱动它的技法（cite [capabilities.md](capabilities.md) 节 + [techniques.md](../../hyperframes/references/techniques.md) 条目）、关键 animation 事件。如「Composed kanban: 3 column divs, 4 cards each, drag-and-drop with `back.out(1.7)` entrance stagger, counter chip on In-Progress incrementing via `tl.set()`.」
- **Brand-inflect：** DESIGN.md 品牌色、真实产品数据（项目名、真实指标、真实 copy——非 placeholder），narration-sync 时刻。让节拍成为**这一品牌**的节拍，非 generic UI demo。

**Accents（仅装饰——brand-inflect 节拍）：**

- 可选。多数节拍 0–1 accent。格式：`capture/assets/<filename>` — 如何出现：位置、opacity、treatment、motion（如 `capture/assets/logo.svg` — top-left, 60×60, fades in at 0.4s, breathes during hold）。
- 常见 accent（主视觉是别物时）：UI 节拍 stamp 品牌 logo、 kinetic type 后 depth 层主插画、ambient 背景 wash 渐变图。当抓取素材**即**主视觉（opener logo 自绘、parallax 主插画 hero beat），不是 accent——是节拍内容；写在 Composition，非此处。
- 若无 obvious accent 需求，留空。主视觉足够。

为本项目**真实**品牌与上文审计素材写本节——非凭记忆。

### Text Animations

本节拍每个文字元素须 catalog 中具体 effect。参考 [`../../hyperframes/references/text-effects.md`](../../hyperframes/references/text-effects.md)（或 `find "$HOME" -path '*/hyperframes/references/text-effects.md' -maxdepth 10 2>/dev/null | head -1`）。列 24 个 effect ID（来自独立 `pixel-point/animate-text` 技能）；按品牌与本节拍 mood 选——勿每节拍同一 effect。

格式（结构**示例**，非处方——按品牌/mood/context 选）：

- `[element — e.g. "main headline"]`: `[effect-id]`
- `[element — e.g. "eyebrow label"]`: `[effect-id]`

构建时 sub-agent 加载 `/animate-text`（上游技能）并从 `.agents/skills/animate-text/assets/effects/<id>.json` 读各 effect spec。构建时无创意决策——仅 spec 检索与实现。

### Beat Timing

步骤 5 正确接线 `data-start` 与 `data-duration` 的两个数：

- **HyperShader transition in at:** `[time]s`（transitions array 中**进入**本 beat 的 transition 的 `time:`——beat 1 为 0）
- **GSAP timeline duration:** `[duration]s`（本 beat 内部动画跑多久——最后一个 tween 何时结束？）

示例：`Transition in at: 4.2s · GSAP duration: 5.5s` → 步骤 5 设 `data-start="4.2" data-duration="5.5"`。

### Animation Sequence — 须覆盖**整个**节拍

节拍是内部有生命的 **SCENE**，非单次 entrance 后 static hold。全程应有事发生——新元素出现、既有 transform、camera drift、细节 reveal、sub-moment 展开。

若 animation sequence 仅前 2 秒有事件而节拍更长，其余是 dead air。规划跨完整 duration 的时刻。无元素应 unchanged 超过 ~2 秒——若在屏，给 continuous motion（drift、breathe、pulse、parallax）。

精确描述 feel：「snappy overshoot bounce settling into place」→ back.out；「slow heavy drift」→ power1.inOut。模糊形容词无用。

---

## 品牌点缀 pass（最后创意决策——节拍写完后）

节拍现已概念定义。每个有承载它的主视觉（composed UI、抓取素材、kinetic typography、WebGL 等）。**现在**单次 pass 决定哪些抓取素材——若有——在另一 primitive 承载视觉的节拍上值得 accent 角色。

这是 file-tree 前**最后**创意 pass。故意放此：素材服务 concept 定义的节拍——作主视觉或 accent，取决于节拍需要——但不 seed 节拍。若因素材「会 cool」想加节拍，是素材在做分镜——回去从 message 重写该节拍。

### 品牌默认（多数品牌视频 nice-to-have）

两个默认适合多数品牌向视频。concept 需要时可 skip；非硬要求。

1. **开场 + 收尾的品牌 mark。** 多数品牌视频，logo/wordmark SVG 在 opener（entry tag）与 closer（sign-off）。观众在观看两端得到品牌。concept 需要时可 skip——如 teaser 故意 delay 品牌 reveal 到 beat 3 造 narrative tension，或品牌 mark 对抓取主视觉 redundant。

2. **视频中某处站点 signature 视觉。** 每个抓取站点有一个：gradient wave、主插画、 distinctive 产品 UI mark、wordmark 动画、色组合、主摄影。懂品牌的人会指认说「那就是他们」。步骤 0 找到；concept 能用处放置。非必须——但若品牌视频不含，问是否仍像**这一**品牌。

这些是默认，非要求。除此之外，全片 aim 2–4 个品牌 accent 总计，非每 beat。多数 0–1。超出 floor 须 justify：_「这素材让节拍**更**这一品牌，还是 filler？」_

节拍写完后打印此表一次：

| Asset                          | Type     | Where (beat #)  | Role                                                                            |
| ------------------------------ | -------- | --------------- | ------------------------------------------------------------------------------- |
| stripe-logo.svg                | SVG      | Beat 1 + Beat N | Brand mark (opener stroke-draw, closer hold)                                    |
| wave-fallback-desktop.png      | Gradient | Beat 3 bg layer | Ambient depth wash behind composed dashboard                                    |
| datavizstatic3x.png            | Data viz | SKIP            | Compose the stats from divs + counter animations instead                        |
| enterprise-accordion-hertz.png | Photo    | SKIP            | Compose the customer-story UI from divs with the brand's testimonial card style |
| icon-3.svg                     | Icon     | SKIP            | Decorative, too small to matter                                                 |

当 composed 等价物（dashboard、kanban、chat、terminal、file tree、calendar、pricing cards 等）更好——产品 UI 的强默认——标 SKIP。composed 节拍用品牌**真实**数据（项目名、真实指标、真实产品 copy）——永非截图 placeholder。

**按本 pass 结果更新各节拍 Composition + Accents。** 多数节拍仍无 accent。少数值得的在「Accents」下单行：文件、位置、opacity、motion。

**标准：** 每节拍视觉用场景需要的 primitive 组合。Accent 是可选品牌 inflection 叠在上；上文品牌默认（opener+closer logo、signature 视觉一次）覆盖多数品牌视频但非硬要求。

---

## 生产架构（Production Architecture）

分镜底部含此文件树：

```
project/
├── index.html                    root — VO + underscore + beat orchestration
├── DESIGN.md                     brand reference (from Step 1)
├── SCRIPT.md                     narration text (from Step 3)
├── STORYBOARD.md                 THIS FILE — creative north star
├── transcript.json               word-level timestamps (from Step 4)
├── narration.wav                 TTS audio (from Step 4)
├── capture/                      captured website data (from Step 0)
│   ├── screenshots/
│   ├── assets/
│   │   ├── svgs/
│   │   ├── fonts/
│   │   ├── lottie/
│   │   └── videos/
│   ├── extracted/
│   │   ├── tokens.json
│   │   ├── design-styles.json
│   │   ├── visible-text.txt
│   │   ├── asset-descriptions.md
│   │   ├── animations.json
│   │   ├── assets-catalog.json
│   │   └── detected-libraries.json
│   ├── AGENTS.md
│   └── CLAUDE.md
└── compositions/
    ├── beat-1-hook.html
    ├── beat-2-features.html
    ├── ...
    └── captions.html
```

---

## 示例：逐节拍格式

下面两节拍来自真实 Claude Design × HyperFrames 生产视频。展示预期 specificity——精确 timing、GSAP 值、animation sequence。

**为何只示 2 节拍：** 本参考旧版示全部 10 节拍，agent 不论抓取品牌都 pattern-match。Moodboard 布局、capabilities grid、orbital letter closer 开始出现在每个视频。那些 beat 的 concept 专属于 HyperFrames 产品——不应出现在 fintech 或 wellness app 视频。此处仅两节拍演示格式深度，非建议这些具体技法。

### BEAT 1 — LIGHT BALL OPENER (0:00–0:03)

**Concept:** No title card, no fade from black. A single point of warm light appears in total darkness. It blooms into a horizon-spanning glow. The viewer leans in before a single word is spoken.

**Visual:** Deep black canvas (#050507) with grain overlay (mix-blend-mode: overlay, 0.12 opacity) and extended vignette (inset: -200px for long falloff). The `.ball-core` is a 40px radial-gradient orb (white center → accent → transparent). Animation sequence:

- 0.0s: Orb appears tiny (scale: 0.15, opacity: 0→1, 0.18s, expo.out)
- 0.18s: Orb grows continuously (scale: 0.4→1.4, 0.7s, power1.in). Simultaneously the `.ball-halo` (140% width, 70% height ellipse, accent-tinted radial-gradient, blur: 60px) blooms in (scale: 0.4→1, opacity: 0→1, 0.55s, sine.out)
- 0.65s: Orb keeps growing as it fades (scale: 1.4→8, opacity: 1→0, 0.4s, power2.in) — the point of light dissolves into pure glow. Halo expands further (scale: 1→1.25, opacity: 0.85)
- 0.85s: Horizontal beam line emerges from center (scaleX: 0→1, 0.4s, expo.out) with warm box-shadow glow (0 0 24px 1px rgba(255,240,220,0.4))
- 1.0s: Title "Claude Design × HyperFrames" fades up above the line (opacity: 0→1, y: 14→0, 0.7s, power3.out). Ampersand in italic accent color.
- 1.3s: Date subtitle appears below the line (0.6s, power2.out). Monospace font, 0.32em letter-spacing, uppercase.
- 2.2s: Bottom credit line fades in ("This entire video was made with HyperFrames in Claude Design")
- 3.0–4.4s: Hold — halo breathes (opacity drifts to 0.55, scale to 1.4, sine.inOut), headline drifts slightly (y: -3px)
- 4.4s: Everything fades to black together (0.6s, power2.in)

Corner marks (monospace, 11px, 0.45 opacity) at top-left and bottom-right for editorial feel.

**SFX:** Deep ambient bass pad already playing from frame 1.

---

_(Beats 2–9 intentionally omitted. See above for why.)_

### BEAT 10 — ORBITAL LETTERS / CLOSE (example of a closing beat spec)

**VO:** (resolving — the brand name assembles)

**Concept:** Individual letterforms of "HYPER FRAMES" burst in from alternating sides, each with rotation and offset. They bounce into place with back.out(2.0) overshoot. An accent line draws itself across the width. An orbit ring expands with a glowing dot tracing a full 360° rotation. A tagline types itself out: "HTML in. Video out." with deliberate pauses after each word. Everything breathes after assembly — letters float gently, glow pulses, connector lines shimmer.

**Visual:** Deep black. Center glow: 900px radial-gradient orb (accent #e8a769 at 0.35 → 0.12 → 0.025 → transparent), blur(100px).

**Animation sequence:**

- 0.1s: 12 character elements ("H Y P E R [space] F R A M E S") enter staggered 0.06s apart, each from y: 80 with alternating x offset (odd: -30, even: +30) and rotation: -15. Landing: back.out(2.0), 0.7s — gives each letter a satisfying overshoot bounce.
- 1.0s: Accent SVG line draws across the full 1920px width (strokeDashoffset: 1920→0, 0.6s, power3.out). #e8a769 stroke, 2px.
- 1.0s: Glow breathes in (opacity: 0→0.2, sine.inOut, 0.4s), then back to 0.1.
- 1.4s: Orbit ring (600px circle, 1px border rgba(accent, 0.3)) expands from scale: 0.5 to 1.0 (expo.out, 0.5s). A glowing orbit dot (8px, accent color, box-shadow glow) on the ring traces a full 360° rotation over 2.5s (linear easing — constant speed).
- 1.25s onward: Letters begin a subtle float — alternating directions (y: ±2px, sine.inOut, 1.4s, yoyo, repeat 1), staggered 0.04s. Keeps the assembled word feeling alive.
- 1.8s: Tagline types itself in monospace (24px, accent color, 0.15em letter-spacing): "HTML" (pause 0.2s), " in." (pause 0.25s), " Video" (pause 0.1s), " out." — each segment at 0.03s per character using steps(N) easing for discrete character appearance.
- 1.8s onward: Glow continues gentle breathing (opacity: 0.1→0.14, sine.inOut, 1.2s, yoyo, repeat 1).

**SFX:** Soft chime on letter assembly completion. Silence under the tagline typing — let it land.

---

## 撰写旁白脚本（同一步——与分镜并行写）

脚本与分镜是一步。每节拍已有 VO cue——脚本即所有 VO cue 汇编成单文档。写每节拍时写其 narration line。然后汇编为 `SCRIPT.md`。

脚本服务分镜——写 fit 视觉计划的词，非反过来。引用 `capture/extracted/visible-text.txt` 的真实产品功能、真实 stats、真实组件。用精确数字。

**脚本长度取决于创意方向，非公式。** cinematic 视频 dramatic pause 与纯 visual 时刻可能 30 秒 40 词。rapid feature showcase 可能 30 秒 100 词。分镜 pacing 与风格（步骤 2 brief）决定 narration vs silence 比例。有些节拍有 narration；有些纯 visual。让创意计划驱动词数，非反过来。

关键约束：勿在无事发生时 pad dead silence。若节拍无 narration，须有 visual 承载观众注意力。空帧 = 丢观众。

保存为项目目录 `SCRIPT.md`。

**脚本写作规则：**

- ~2.5 words/sec 自然 pace。15s ≈ ~37 词，30s ≈ ~75 词。
- 用缩写（"it's", "you'll"）。大声读——若 robotic，重写。
- 数字按口语写：`$1.9T` → "nearly two trillion dollars", `API` → "A P I", `10x` → "ten times"
- **Hook 优先**—— bold claim、 provocative 问题、 contrast 或 shocking 数字。永非 "Welcome to..." 或 "Introducing..."
- 结构：Hook → Story → Proof → CTA。15s 广告可 skip Story。

---

## 用户审阅关卡（User Review Gate）

写完分镜**与**脚本后，将**两者**一并呈现用户审阅。分镜与脚本耦合——用户需一起看才能判断视频是否 work。

### 如何呈现

清晰 summarize 计划。勿 dump 完整 STORYBOARD.md——给 30 秒可扫的逐 beat 概览：

> **Here's what I've planned for your [duration] [type]:**
>
> **Beat 1 (0:00–0:04):** [one sentence — what happens visually + what the narration says]
> **Beat 2 (0:04–0:10):** [one sentence]
> **Beat 3 (0:10–0:18):** [one sentence] _(hero beat — 3D MacBook reveal with bloom effect)_
> ...
> **Beat N (closing):** [one sentence — CTA/logo]
>
> **Style:** [dimension summary — e.g., "Cinematic pacing, dark mood, dramatic transitions for hero, clean for the rest"]
> **Narration:** [first and last line of the script]
> **Total duration:** [X]s with [N] beats
>
> **Does this match what you envisioned?** I can adjust: beats, pacing, specific effects, the script tone, or anything else. Or if this looks good, I'll proceed to voice generation.

### 如何处理反馈

- **「Looks good」/ 批准** → 进入步骤 4（VO）
- **具体反馈**（「beat 3 加长」、「opening 更快」、「不要 typing effect」）→ 更新 STORYBOARD.md 与 SCRIPT.md，再呈现
- **大方向变更**（「其实要更 playful 不要 cinematic」）→  revisit 步骤 2 brief dimensions，重写分镜
- **迭代至用户满意。** 此处改分镜最便宜——改一 beat 约 30 秒。改已建 composition 约 5 分钟。

### 关卡

STORYBOARD.md 与 SCRIPT.md 均存在**且**用户**明确**批准计划。

**自主模式例外：** 若用户在步骤 2  signaled 自主模式（「surprise me」/「decide for me」/「just build it」），跳过批准等待。inline 呈现分镜 summary 作 heads-up，直接进入步骤 4。
