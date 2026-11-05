# 设计规格 — `frame.md` / `design.md`

关于**设计规格是什么、如何找到它、如何阅读它**的单一事实来源。其他参考文档在解析与格式方面以本文为准；**消费**契约（「品牌，而非版式」）见 `video-composition.md`。

## `frame.md` 是什么

`frame.md` 是视频 / hyperframes 项目的**帧级设计系统**——面向视频的首选用法，与 `design.md`（面向 Web / 静态页面）并列。与 `design.md` 使用相同文件格式；它以「帧」为单元重新表述品牌。

规格由 **YAML frontmatter + Markdown 正文** 组成，两层并不等同：

- **Frontmatter 是规范层** — `colors`、`typography`、`spacing`、`components` 等是真实、可机器读取的取值。须逐字引用（精确 hex、字体族、字重）；不得臆造或四舍五入。
- **正文是语境层** — `##` 各节（Overview、The Frame、Composition Rules 等）承载意图、使用场景以及 token 无法表达的约束。阅读它们以获取判断，而非取值。

## 解析应读哪份规格

优先级 — 读取**第一个存在的**，忽略其余：

```
frame.md  →  design.md  →  DESIGN.md
```

```bash
SPEC=$(ls frame.md design.md DESIGN.md 2>/dev/null | head -1)
```

- 对视频 / hyperframes 项目，`frame.md` 是首选规格；若多份同时存在，以它为准。
- `frame.md` **始终为小写** — 不存在 `FRAME.md` 变体。（`design.md` 与 `DESIGN.md` 在 Linux 上确实是不同文件；帧预设会提供大写 `FRAME.md` _模板_，采用时复制为小写 `frame.md` — 见下文「从预设起步」。）

在 **Step 1** **加载一次**规格；后续各步（扩展、编写、遵循）都消费已加载的规格，而非重新解析。

## 从预设起步（可选）

可选地从 `[../frame-presets/](../frame-presets/)` 中的现成 **frame-preset** 种子化 `frame.md` — 固定集合，每项附带 `FRAME.md` 模板，由工作流的设计步骤复制并叠加品牌 token。引用预设**并非必需**；定制或 [picker](design-picker.md) 生成的规格同样有效。

| 预设                                                             | 外观                                                                                                                                                                                                                                                                                                                     | 适用场景                                                                                                                        |
| ------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| `[biennale-yellow](../frame-presets/biennale-yellow/FRAME.md)`     | 文学编辑型图录 — 暖羊皮纸底、单一深靛蓝墨色、太阳黄作径向 bloom / 面板 / 瓷砖底纹，Instrument Serif 400 展示（紧、负字距）+ Archivo 正文 + JetBrains Mono 数据，严格矩形（0 圆角），1px 发丝线作为唯一边框，无阴影  | 自信 / 有氛围 / 克制；希望博物馆图录式优雅与编辑权威的产品 |
| `[blockframe](../frame-presets/blockframe/FRAME.md)`               | 极繁新粗野主义 — 4px 黑边、8px 硬偏移阴影、五种糖果 pastel、Inter 800–900 大写、方角、倾斜装饰 | 大胆 / 冲击感 /  playful 高响度；希望自信、偏图形化的产品 |
| `[blue-professional](../frame-presets/blue-professional/FRAME.md)` | 咨询级克制 — 暖奶油画布、单一饱和钴蓝 (#1e2bfa) 点缀、Space Grotesk + Inter 字体、柔和着色卡片（4% 填充 / 20% 边框 / 10–14px 圆角）且无阴影、药丸形 chrome (100px)、三级灰文字阶梯、钴蓝进度条 | 稳健 / 高管可读 /  premium 信号；希望投研严谨与 refined 克制的产品 |
| `[bold-poster](../frame-presets/bold-poster/FRAME.md)`             | 民粹编辑海报 — Shrikhand 展示倾斜 −6°..+2°、Libre Baskerville 衬线正文、Space Grotesk mono chrome、四色限定（白 / 棕黑墨 / 番茄红 / off-white）、双边框网格（3px+1.5px）、红色 leftbar 卡片、红色 em-dash 项目符号、红色展示 stacked text-shadow、方角 | 有力 / 印刷感 / 克制；希望编辑权威与 vintage gravitas 的产品 |
| `[broadside](../frame-presets/broadside/FRAME.md)`                 | 抗议海报体系 — 两档平面（墨黑 / 火橙）、超大写 Barlow 900 作图形基元、IBM Plex Mono chrome（大写、0.14em）、火橙为唯一点缀、1px 发丝线、锐角、无阴影 | 大胆 / 字体主导 / 宣言式；希望存在感与权威的产品 |
| `[capsule](../frame-presets/capsule/FRAME.md)`                     | 活泼编辑风 — 每个容器为药丸（2px 墨线轮廓）、奶油画布、九种糖果点缀、Bodoni Moda + Space Grotesk、柔和偏移阴影、floating-pill 壁纸 |  friendly / 柔和 / 编辑感；希望温暖与亲和力的产品 |
| `[cartesian](../frame-presets/cartesian/FRAME.md)`                 | 博物馆图录编辑 — 1px 灰褐发丝网格、五暖石色板 (#EDE8E0 / #E2DBD1 / #1A1A1A / #5A5A5A / #8A8178)、Playfair Display 400 + Inter、锐角、compass-drafted 几何环、零阴影 / 零填充 |  sparse / 文学 / 克制；希望 quiet 权威与编辑严谨的产品 |
| `[claude](../frame-presets/claude/FRAME.md)`                       | 暖编辑品牌书 — 暖奶油纸（绝不用纯白）、terracotta coral (#CC785C)  scarce voltage、发丝线墨 elevation（无重阴影）、EB Garamond 衬线展示 + Inter 正文 + JetBrains Mono 索引 / 暖海军代码面 code、sentence-case 展示、✱ coral spike |  considered / 文学 / 面向开发者；代码变更、发布或文档，希望编辑 calm 与一流 code surface |
| `[cobalt-grid](../frame-presets/cobalt-grid/FRAME.md)`             | 现代主义双色 risograph — 奶油纸、电钴墨、permanent 方格纸网格（10% 钴）、顶/底钴发丝线、Newsreader 400 衬线 + Hanken Grotesk + DM Mono、0° 角、pixel-glitch 列 + QR-block 补丁 |  restrained /  systemic / 编辑；希望 clarity 与 measured 权威的产品 |
| `[coral](../frame-presets/coral/FRAME.md)`                         |  bold 编辑杂志 — 三实色面（coral fire / ink black / warm cream）硬边相接、45° coral 斜线 hatch、Bebas Neue + Inter tracked caps、零阴影/半径（圆 50%）、oversized 壁纸数字与 giant marks |  bold / 结构主义 / 编辑；希望图形 confidence 与 hard-edged confidence 的产品 |
| `[creative-mode](../frame-presets/creative-mode/FRAME.md)`         | neo-brutalist 编辑 — 奶油画布、4px 墨边、硬偏移阴影（无 blur）、四 accent rationed two-to-three、Archivo Black 大写 0.92 行高、JetBrains Mono taxonomy、Space Grotesk 正文、方角 save one pill chip |  sparse / 图形 / punchy-restrained；希望编辑 presence 与 geometric confidence 的产品 |
| `[daisy-days](../frame-presets/daisy-days/FRAME.md)`               |  cheerful 绘本 — 3px charcoal 轮廓、6/4px 硬偏移阴影（无 blur）、九 sunny-garden pastel（cream + turquoise/soft-pink/butter/mint/lavender/peach/sky + coral accent）、Fredoka One + Quicksand、generous 圆角（20–50px）、hand-drawn SVG ornament（daisies/stars/suns/clouds/rainbows） |  playful / childlike / sticker-sheet kawaii；希望 warmth 与 whimsy 的产品 |
| `[editorial-forest](../frame-presets/editorial-forest/FRAME.md)`   | 衬线主导文学编辑 — green / pink / cream 编辑 triad、Source Serif 4 weight 500 (opsz) 展示 + JetBrains Mono 500 大写 chrome、flat paper depth（无阴影）、2px 发丝线、6/8px 卡片圆角、monogram 圆 stamp |  spacious / restrained / 编辑；希望 quiet confidence 与 literary tone 的产品 |

每个预设文件夹还附带 `frame-showcase.html` — 其帧处理的预览样张；打开以 _看_ 外观，切勿将其纳入项目。

## 消费规格

如何将规格应用到帧 — 品牌严格（hex、字体、字重关系、Do's / Don'ts），版式自由 — 的消费契约在 `[video-composition.md](video-composition.md)`（「The Design Spec Is Brand, Not Layout」）。选色或写 HTML 前先读该文；本文仅涵盖查找与解析规格。
