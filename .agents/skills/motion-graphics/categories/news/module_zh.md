# news — 分类模块（搜索驱动）

搜索一篇真实新闻文章 → 将其动画化为 **article-highlight** — 对居中强调（centered-emphasis）技法的忠实 HF 移植。标志性动效：文章正文以 **可读字号（非放大）** 排版，上滑并淡入，随后 **关键词在原位高亮** — 标记色带自左向右在其背后生长。无放大变焦。约 5–7 秒。

两种版式共享同一高亮核心 — 按画幅比例以及是否需要展示 logo / 人物来选择：

| 版式                    | 画幅     | 适用场景                                                        | 包含                                                                        |
| ------------------------- | ---------- | --------------------------------------------------------------- | -------------------------------------------------------------------------- |
| **A · centered-emphasis** | 9:16 / 1:1 | 纯文字、社交竖屏                                      | kicker + 一句居中句子 + 关键词高亮                         |
| **B · full article**      | 16:9       | 故事中有真实 **媒体 logo** 和/或 **人物** | logo + 日期 + 多行标题关键词高亮 + dek + 媒体名 + 人物抠图 |

## 素材来源（Step 2）

RWA / 网页搜索（或 `hyperframes capture`）→ 一篇真实文章。Director 提取 **关键词**（1–2 个词 / 数字 / 人名 — 钩子），Layout B 还需 **品牌 logo**、**日期** 与 **人物照片**。`asset_needs: { kind: news|web|image, query }` — 将 logo（Wikimedia / simple-icons）与人物照片（Wikimedia）作为独立素材查询请求。人物照片经 `hyperframes remove-background <in> -o <out>.png` 得到透明抠图。

## 高亮核心（两种版式共用）— 标记色带技法

关键词高亮为经 `background-size` 自左向右生长的标记色带（**不是** `transform:scaleX` 条）：

```css
.hl {
  --hlw: 0%;
  background-image: linear-gradient(var(--hl), var(--hl)); /* --hl: rgba(250,222,99,.6) */
  background-repeat: no-repeat;
  background-position: 0 72%;
  background-size: var(--hlw) 64%;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
```

`box-decoration-break:clone` 使色带在 **换行处无缝延续** — 跨 2–3 行的多词关键词仍可连续高亮（旧式 `scaleX` 条做不到）。GSAP 补间 CSS 变量 `--hlw` 从 0%→100%，**在文字落定后再扫入 — 切勿预先应用**。可选按关键词长度缩放时长，约 0.5–1.5s。

## Layout A — centered-emphasis（9:16，纯文字）— Builder

1. **以可读字号排版关键句 — 不要放大。** 纸感浅色舞台；顶部 outlet `#kicker`（如 "BBC NEWS · TECHNOLOGY"，品牌强调色）；关键句居中、衬线体，**约 70–76px / 700 / 行高约 1.4**，`max-width ≈ 900`。整句保持易读；关键词在其 **内部** 强调。
2. 行内包裹关键词：`… raised <span class="hl" id="kw">$750M</span> at …`。
3. **时间轴**（可 seek、暂停）：kicker 淡入+滑入 → **句子滑入+淡入**（`set{autoAlpha:0,y:52}`→`to{autoAlpha:1,y:0,duration:0.8,ease:"power3.out"}`，无 zoom）→ **关键词高亮生长**（`--hlw 0→100%`，句子落定后）→ 轻微 hold（`scale 1.012`）。

**参考：** `samples/news/_ref-centered-emphasis.html`（+ `news/v2-*`）。

## Layout B — full article（16:9，logo + 人物）— Builder

编辑式文章卡片版式（左上 logo + 日期 + 大号衬线标题含多行关键词高亮 + dek + 左下媒体名 + 右下背景移除的 **人物抠图**）。1920×1080，纸感浅色渐变舞台，Georgia 衬线体。

1. **Logo** 左上（`#logo`，约 64px）— 内联 outlet/品牌 SVG，`fill:currentColor`，`color` 设为标识自身色相（或单色标识用近黑）。其下 **日期**（`#date`，约 30px，弱化色）。
2. **标题**（`#headline`，Georgia **96px / 700**，`width≈1080`，`line-height 1.16`），关键词包在 `<span class="hl" id="kw">` 内 — 高亮色带扫过短语 **所有换行**。
3. **Dek**（`#dek`，Helvetica 约 38px 灰）在标题下；**媒体名**（`#outlet`，Georgia bold 约 50px）左下。
4. **人物抠图**（`#subject`，去背 PNG，`height≈860`，`right:40; bottom:0`，`drop-shadow`）— 作为 hero beat **自右下方向上滑入**。
5. **时间轴**（可 seek、暂停）：logo `back.out` @0.15 → date @0.4 → **人物上滑**（`set{autoAlpha:0,x:90,y:60}`→`to{autoAlpha:1,x:0,y:0,duration:0.85,ease:"power3.out"}`）@0.45 → headline @0.7 → dek @1.5 → outlet @1.9 → **关键词高亮**（`--hlw 0→100%`，`duration:0.8`）@2.2。时长约 6.5s。

**参考：** `samples/news/_ref-article-layout.html`（真实文章 + 真实媒体 logo + 去背人物 + 真实故事）。

## 关键要点

高亮 **在原位生长，文字出现后再扫入 — 切勿预先应用**。文字 **保持可读 — 不要将关键词放大填满画面**（团队反馈 2026-06-09：放大丢失语境、观感错误；本技法从不 zoom — 呈现全文并高亮词语）。Layout B 的人物 **必须** 为 `remove-background` 抠图（禁止矩形照片框）。确定性实现；遵守 `references/builder-contract.md`。
