# 步骤 1：撰写 DESIGN.md（品牌真相速查表）

DESIGN.md 是一份**品牌真相速查表**——你在组合各 beat 时要**织入**其中的颜色与字体。它不是版式规格、不是情绪板、也不是 400 行的设计系统审计。

DESIGN.md 是子代理在构建每个 beat 时应用的品牌调性：哪种颜色是「主色」、标题用哪种字体、品牌承载何种调性——他们在构建过程中会拨动的承重旋钮。

**目标长度：250–350 行。** 步骤 5 的子代理会阅读 DESIGN.md 为每个 beat 打上品牌——此处编码的组件 CSS 值越精确，结果越贴近品牌。低于 200 行往往产出泛化的暗色电影感输出，因为子代理没有品牌组件 DNA 可用；超过 350 行则意味着在散文上投入过度。

**快节奏例外：** 对于 billboard-per-beat 视频（每条 beat 为全出血背景上的单一 hero 元素、偏短社交广告），50 行的 DESIGN.md 仅含颜色 + 字体 + 3–5 条 do's/don'ts 即可。步骤 5 的子代理提示会把品牌值内联粘贴，因此仅当 beat 渲染完整 UI 时 DESIGN.md 的深度才重要。

**用户偏好始终优先于品牌规则。** 若用户说「网站是暗色但请做亮一点」或「品牌是 sans 但请用 serif」——按用户来。DESIGN.md 描述的是捕获的网站；成片可能刻意打破它。

**现在就读这些**——它们是撰写 DESIGN.md 的输入。不要从截图猜颜色或尺寸：

- `capture/extracted/tokens.json` — 主要品牌色（HEX）及带字重范围的字体族。
- `capture/extracted/design-styles.json` — 来自 live DOM 的计算 CSS 值： typography 层级（各文本角色的 font-size、weight、line-height、letter-spacing）、按钮变体（background、padding、radius、shadow）、卡片/容器/导航样式、间距刻度、圆角刻度、带使用次数的 box-shadow 值。**第 3–6 节以下部分的主要数据源。**

**字体可用性检查——在写其他任何内容之前先做。** 读取 `capture/extracted/fonts-manifest.json`。捕获流水线会读取每个已下载字体文件内嵌的 OpenType `name` 表，因此即便 Next.js/Webpack 哈希重命名的字体也能按真实族名识别（Inter、JetBrains Mono、Geist Mono 等）。无需猜测。

manifest 提供两种视图：

- `families[]` — 每个 distinct 族一条，含已捕获字重、是否为 variable font、以及所属文件
- `files[]` — 每个已下载字体一条，含 family、subfamily、weight、style 及任意 variation 轴

**如何使用：**

- 在 DESIGN.md 中引用的每个族，按 `families[].family` 中的名称命名（例如「Inter」，而非「f266e704 哈希字体」）。哈希文件名是 `@font-face src` 路径——磁盘上保持原样；仅展示名来自 manifest。
- 若某族 `variable: true` 且 `variationAxes` 含 `"wght"`，即便捕获文件中只出现一个 static 字重，也可通过 `font-variation-settings: 'wght' <value>` 使用 100–900 任意字重。在 DESIGN.md 中注明，以便子代理知道可用完整字重范围。
- 若 manifest 的 `unidentified[]` 非空，这些文件未能从 name 表提取（少见——重度子集化并 strip 元数据的字体）。在 DESIGN.md 中标记为 `unknown` 并建议 fallback，不要猜。
- 托管在品牌 CDN 上的商业字体（GT Walsheim、Söhne、Graphik、Canela）不会出现在 manifest 中，因为未下载。通过对比站点实际使用（来自 `design-styles.json`）与 manifest 中内容来检测——使用但缺失的即为 CDN 托管字体。明确标注：「Söhne 不在捕获中；用 Inter 600 替代。」

子代理会尝试使用你列出的字体。manifest 准确告知可用内容——没有理由声称存在「Charlie Display 700」而实际没有该文件。

---

## 要写的 5 个章节

### `## 1. Visual Theme（一段）`

3–5 句描述品牌视觉个性。涵盖：dark-first 或 light-first、对比策略、主导视觉元素（渐变、插画、摄影、UI mockup）、整体情绪、与泛化设计相比有何 distinctive。

这是唯一的散文章节。要针对**这一**品牌具体——不是填模板。一句能描述任何设计良好网站的话没有用。

**示例：**

> Stripe 的视觉语言以 light-first、干净为基调，深海军蓝（`#061B31`）与纯白构成基础。强调色栈——Stripe Purple（`#533AFD`）用于 CTA、Vibrant Orange（`#FF6118`）用于 energetic 强调——使交互元素 unmistakable。字体为 display 用 sohne-var Light（300）、正文 weight 400；品牌通过尺寸与字重建立层级，从不靠颜色变化。情绪是自信的金融科技——高级而无 theatrical drama。Distinctive：135° 紫橙渐变叠加作为白底上的 subtle wash，从不作为 bold 焦点。

---

### `## 2. Quick Reference`

子代理在组合 beat 时抓取值的扁平查找表。两个子节——保持紧凑。

#### Colors

列出 8–12 种颜色，带品牌特定名称 + HEX + 角色。不要泛化（「Accent 1」），要 evocative（「Stripe Purple」「Deep Navy」「Slate Border」）。名称承载含义；「blue 4」不行。

**对品牌使用的每种文字-表面组合，计算 WCAG AA 对比度并明确标注不合格配对。** 以往运行的真实失败模式：品牌 secondary 文字色（`#68686A`）在其 dark panel 色（`#18191B`）上 = 3.16:1，低于 AA 4.5:1 最低要求。子代理忠实复现品牌色选择，结果不可读。在此编码安全/不安全配对，使子代理按表面上下文选文字色，而非「这是品牌的 secondary 文字色」。`/hyperframes-contrast` 技能会审计比率——定稿 DESIGN.md 前运行它。

**示例：**

```markdown
#### Colors

- **Stripe Purple** (`#533AFD`): Primary CTA, interactive elements, focus rings — the brand's action signal
  - On Pure White: 6.2:1 ✅ — On Deep Navy: 3.8:1 ⚠ AA-only-Large
- **Deep Navy** (`#061B31`): Primary text on light surfaces, also a dark surface tier
  - As text on Pure White: 17.4:1 ✅ — As surface: see Slate-on-Navy pairings below
- **Pure White** (`#FFFFFF`): Page background, card surfaces
- **Light Gray** (`#F5F7FA`): Surface tier 2 (cards on white pages, alternating sections)
- **Slate Blue** (`#273951`): Secondary text on LIGHT surfaces
  - On Pure White: 12.6:1 ✅ — On Light Gray: 11.8:1 ✅ — On Deep Navy: 1.4:1 ❌ DO NOT USE
- **Light Slate** (`#64748D`): Metadata, captions on light surfaces only
  - On Pure White: 4.8:1 ✅ — On Light Gray: 4.5:1 ✅ — On Deep Navy: 3.0:1 ❌ — On Dark Panel: 2.9:1 ❌
  - **For dark-surface metadata, use `#9A9A9E` instead: 6.4:1 on Deep Navy ✅, 6.1:1 on Dark Panel ✅**
- **Subtle Border** (`#D4DEE9`): Card borders, dividers (not text — borders don't need AA)
- **Vibrant Orange** (`#FF6118`): Energy accent — gradient endpoints, highlight bursts (never primary text)
- **Error Red** (`#FF0022`): Validation errors. On Pure White: 4.5:1 ✅
- **Success Green** (`#4CD963`): Confirmation states. On Pure White: 1.7:1 ❌ — must be paired with a darker outline or use as accent on dark surfaces
```

**当品牌自有调色板不满足 WCAG 时**，记录替代色（如上 `#9A9A9E` override）。子代理按表面选安全色——若偏离对品牌身份重要，用户可在步骤 6 再议。

#### Fonts

列出字体族及其角色，以及来自 `fonts-manifest.json` 的**每个族 + 字重的确切文件路径**。子代理会原样复制 `@font-face` 块——若只写族名不写路径，子代理需猜哪个 `.woff2` 属于哪个族，一半时间会错（以往真实失败：代理把「ES Build Neutral」的 `@font-face` 指到 Inter 的 `.woff2`，wordmark 用 Inter 渲染）。

**示例：**

````markdown
#### Fonts

- **Display:** `"ES Build Neutral"` — wordmarks, headlines
  - 600: `capture/assets/fonts/14d7ce3e41dcbb66-s.p.woff2`
  - 700: `capture/assets/fonts/e8b276476c0ac6fa-s.p.woff2`
- **Body:** `"Inter"` (variable 100–900, captured ✓) — body, labels, UI
  - 400: `capture/assets/fonts/9a8d3f06c4e89f2b-s.p.woff2`
  - 600: `capture/assets/fonts/1b0b3615811be75b-s.p.woff2`
- **Mono:** `"JetBrains Mono"` — code, metadata
  - 400: `capture/assets/fonts/c7d2e9f5a1b3c8d4-s.p.woff2`
- **Fallback stack:** `-apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif`

**`@font-face` block to paste in every composition** (sub-agents copy this verbatim — do not invent file paths):

```css
@font-face {
  font-family: "ES Build Neutral";
  src: url("capture/assets/fonts/14d7ce3e41dcbb66-s.p.woff2") format("woff2");
  font-weight: 600;
  font-display: block;
}
@font-face {
  font-family: "Inter";
  src: url("capture/assets/fonts/9a8d3f06c4e89f2b-s.p.woff2") format("woff2");
  font-weight: 400;
  font-display: block;
}
/* + any other family/weight combinations the storyboard's beats need */
```
````

品牌用**尺寸建层级、字重建强调**。Display 1：48px/600，Display 2：32px/600，Body：14px/400。（按实际品牌层级调整。）

````

确切的 `@font-face` 块让子代理原样复制而非推断构造。若 beat 需要 manifest 中没有的字重，在此明确标注：例如「ES Build Neutral 900 未捕获；用 ES Build Neutral 700 替代，或 fallback 到 Inter 700。」

 typography 整节即此。若子代理需要精确 line-height 或 letter-spacing，他们直接读 `design-styles.json`。

---

### `## 3. Component Stylings`（构建步骤的规格表）

这是子代理在步骤 5 构建 beat 时查阅最多的章节。**没有精确的 per-component CSS，子代理会退回泛化「暗底 + 发光 + 居中文字」模式，与品牌无关**——因此每个视频看起来都一样。在此编码品牌真实的组件 DNA。

目标 **6–12 个 distinct 组件**。记录站点实际使用的；品牌没有的类别跳过。每个组件用描述性命名（「Stripe Primary Button」而非「Button 1」），并提供精确 CSS 级属性：background、text color、padding、border-radius、border、font size/weight、height、box-shadow，以及 hover/active/disabled 等状态。

#### Buttons（始终需要）

覆盖站点使用的每个变体——通常 Primary、Secondary/Ghost、Icon。**示例：**

```markdown
#### Primary Button (Stripe Purple)

- **Background:** `#533AFD`
- **Text color:** `#FFFFFF`
- **Font:** sohne-var 16px / 400
- **Padding:** `15.5px 24px 16.5px 24px`
- **Border radius:** `4px`
- **Border:** none
- **Height:** `48px` (with padding)
- **Box shadow:** none
- **Hover:** background `#4329E8`, opacity `0.95`
- **Active:** background `#3720D4`, scale `0.98`
- **Disabled:** background `#C9C3F0`, cursor `not-allowed`

#### Secondary Button (outline)

- **Background:** `#FFFFFF`
- **Text color:** `#533AFD`
- **Border:** `1px solid #533AFD`
- **Padding / radius / font:** same as Primary
- **Hover:** background `#F3F0FF`, border `#4329E8`

#### Ghost Button (text-only link)

- **Background:** transparent
- **Text color:** `#533AFD`
- **Font:** sohne-var 14px / 400
- **Padding:** `12px 0`
- **Hover:** background `rgba(83, 58, 253, 0.08)`, optional underline
````

#### Cards & Containers（若站点使用则始终需要）

记录每种 distinct 卡片类型——Standard、Feature Highlight、Glass、Pricing、Testimonial——该品牌实际使用的 whatever。**示例：**

```markdown
#### Standard Card

- **Background:** `#FFFFFF`
- **Border:** `1px solid #D4DEE9`
- **Border radius:** `5px`
- **Padding:** `32px`
- **Box shadow:** `0 1px 2px rgba(0, 0, 0, 0.04)` (default), `0 4px 12px rgba(0, 0, 0, 0.08)` (hover)
- **Hover:** border `#B8CCDB`

#### Feature Highlight Card (gradient backdrop)

- **Background:** linear-gradient(180deg, rgba(83, 58, 253, 0.05) 0%, rgba(255, 97, 24, 0.03) 100%)
- **Border:** `1px solid #E5EDF5`
- **Padding:** `36px`
- **Box shadow:** none
```

#### Distinctive components（品牌实际展示的其他任何内容）

Logo marquee、testimonial carousel、pricing table、gradient overlay、glassmorphism panel、bento grid、code block、terminal UI、dashboard mockup——命名并记录任何视觉上 distinctive 的内容。storyboard 需要展示 X 的 beat 时，子代理会取用这些规格。

```markdown
#### Glass Container (frosted overlay)

- **Background:** `rgba(255, 255, 255, 0.9)`
- **Border:** `1px solid rgba(255, 255, 255, 0.2)`
- **Backdrop filter:** `blur(8px)`
- **Use:** floating chat widgets, modal overlays, hero callouts only — the only place transparent fills appear in the system
```

**规则：** 若步骤 5 的子代理必须为该品牌实际使用的组件发明 CSS 值，说明本节文档不足。值应可查找，不可猜测。

---

### `## 4. Spacing & Layout`

品牌的节奏。三个子节，保持紧凑。

#### Spacing scale

识别**基础单位**（通常 `4px` 或 `8px`）及带使用语境的完整刻度。**示例：**

```markdown
**Base unit:** `4px`

| Token | Value   | Used for                                                  |
| ----- | ------- | --------------------------------------------------------- |
| xs    | `4px`   | Inline icon gaps, tight badge padding                     |
| sm    | `8px`   | Button-group gaps, small component padding                |
| md    | `16px`  | Card padding, form-field gaps, standard component spacing |
| lg    | `32px`  | Section vertical spacing, large card padding              |
| xl    | `60px`  | Major section separation                                  |
| 2xl   | `100px` | Page-level rhythm, hero section padding                   |

Never use odd values (`13px`, `17px`) — the system only uses multiples of 4.
```

#### Border-radius scale

站点使用的每个 radius，及用途。

```markdown
- `0px`: Form labels, technical UI markers
- `4px`: Primary buttons, inputs, small badges
- `8px`: Standard cards, dropdowns
- `12px`: Feature cards, larger callouts
- `40px`: Icon buttons (square pill)
- `9999px`: Pill-shaped CTAs, status chips
```

#### Whitespace philosophy（一段）

品牌如何使用留白——generous 且 architectural？紧凑且信息密集？区块间距 60–100px 还是 20–40px？记录品牌实际节奏。

```markdown
Generous whitespace as confidence. Section gaps are always `60–100px`. Content never touches viewport edges — minimum `40px` horizontal padding on mobile, `80–160px` on desktop. The brand uses negative space as active design, not emptiness.
```

---

### `## 5. Iteration Guide`（承重章节）

5–10 条编号规则，编码最重要的品牌决策。每条规则是**一句可执行的话，说明做什么，并带上本站点具体值。** 这些是子代理在组合 beat 时查阅的「有疑则如此」规则。

**最常见的失败模式是写泛化规则，适用于任何设计良好的网站。** 不点名具体值、具体颜色或本品牌实际使用的具体组件的规则，等于没用。

**对你写的每条规则做测试：** 能否换成另一个品牌而规则仍成立？若能，太泛化。若不能，保留。

#### ❌ 泛化 vs ✅ 站点特定

| 泛化（删除）                                  | 站点特定（保留）                                                                                                                                                            |
| ------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 主品牌色用于 CTA。             | 所有 primary CTA 使用 Stripe Purple（`#533AFD`）。Secondary 动作为白底 + `#533AFD` 边框与文字。**系统中不存在第三种按钮色。** |
| 通过颜色对比维持视觉层级。 | 正文在白色上为 `#000000`，在深色上为 `#FFFFFF`。Metadata 仅在白色上用 `#64748D`——从不在深色上。品牌没有在深色背景上使用 mid-gray 文字。                  |
| 使用清晰的 typography 层级。                  | 全部字体为 sohne-var。H1 `48px`/300，H2 `32px`/300，body `14px`/400。**Never use weights above 400** — this brand has no bold variant.                                         |
| 使用一致的 spacing。                           | Spacing 来自固定刻度：`4, 8, 12, 16, 20, 24, 32, 40, 60` px。Section gaps 始终 `60–100px`。Card padding 始终 `32px`。无例外。                         |
| 按钮应有圆角。              | 按钮最小高度 `40px`，radius `4px`，padding `15.5px 24px`。Pill 形 `9999px` radius 仅保留给 floating chat trigger。                                |

#### 一个完整示例（Framer — 5 条规则）

```markdown
### Iteration Guide

1. **All interactive elements use Framer Blue (`#0000EE`)** — links, primary buttons, active states, focus indicators. Secondary uses `#0099FF` for hover. **No other interactive color exists in the system.**

2. **Typography: GT Walsheim Medium for headings, Inter for body.** Hierarchy enforced through size only, never color. H2 `62px`, H5 `85px`, body `14px`, labels `12px`/500. Text defaults to `#000000` on white, `#FFFFFF` on dark.

3. **Spacing is base-4** — every margin / padding / gap is a multiple of `4px`. Section gaps `60–100px`. **Never use odd values like `13px` or `17px`** — the system has no place for them.

4. **Cards: white (`#FFFFFF`), `1px` border `#EFEFEF`, `8px` radius, `16–20px` padding, no shadow by default.** Dark-mode cards swap to `#1A1A1A` background with `#242424` border. Shadow only appears on hover.

5. **Glass containers** use `rgba(255,255,255,0.9)` background, `1px` border `rgba(255,255,255,0.2)`, optional `backdrop-filter: blur(8px)`. **These are the only place transparent fills appear** — everywhere else uses solid color.
```

若草稿中有类似「所有交互元素需可见 focus 状态以满足无障碍」的规则——删掉。并非错误，只是对**这一**品牌不是承重项。

---

## 规则

- 使用来自 `capture/extracted/tokens.json` 的**精确值**。需要时与截图交叉核对。
- 颜色与组件用描述性命名——「Stripe Purple」而非「Accent 1」。
- 无法提取精确值时，从视觉检查估算并注明。
- 不要「Assets」节——`capture/extracted/asset-descriptions.md` 是资产索引。
- 不要「Motion」节——storyboard 按 beat 指定动效。
- 不要单独的「Components」节——Quick Reference 是组件所在。
- 不要「Depth & Elevation」表——阴影语言由品牌情绪隐含（premium 用重阴影，flat/clean 无阴影）；子代理无需表格即可选合适值。

---

## 快速用户核对（进入步骤 2 前）

进入步骤 2 前 30 秒 sanity check：

> 「以下是我提取的 [品牌名] 视觉识别：
>
> - **Colors：** [primary]、[accent]、[另外 2–3 个及角色]
> - **Fonts：** [标题字体]、[正文字体]
> - **Tone：** [品牌感受一句话]
>
> 这与您希望视频呈现的感觉一致吗？在开始 storyboard 前有任何修正或 override？」

若用户有修正（「用蓝色，不是灰色」/「忽略 dark mode」/「刚 rebrand，改用 [这些值]」）——现在更新 DESIGN.md。此处花一分钟可省下三十分钟重建。

---

## 怎样的 DESIGN.md 才有用

只读 Quick Reference + Iteration Guide 的子代理应能：

1. 为任意 primary action、secondary action、正文、错误状态选对颜色
2. 为任意标题、正文、metadata 选对 font/weight/size
3. 知道哪 2–3 条规则一旦打破就会失去品牌

这就是测试。若他们能从 60–120 行文档回答这三问，你就做对了。若需要读 400 行情绪板散文才能找到一种颜色，你就把信号埋没了。
