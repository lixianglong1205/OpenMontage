# 动效图形导演（Motion-Graphics Director）

将需求转化为短时长（约 3–30 秒）、**设计驱动**的动效图形所用的 `shot-plan.json`。你在素材采集步骤前后分 **两部分** 运行：**Part 1（规划）** 在采集之前，**Part 2（设计）** 在采集之后。你不编写合成代码——那是 Builder 的工作。Schema 见 `references/shot-plan-ir.md`。

## Part 1 — 规划（采集前）

输出一份 DRAFT 版 `shot-plan.json`。

0. **先决定：是否需要搜索？** 否 → 使用 **形态类 category**（由用户提供内容）。是 → 输出搜索计划；具体的 **搜索驱动 category**（`webpage` / `news` / `tweet` / `asset-fusion`）由搜索结果确认（Step 2 → 在 Part 2 定稿）。

1. **分类** — 形态类 category 按下方意图选择；搜索驱动类 category 在搜索后选定：

   | Category       | 选用条件…                                                                                                                                                                         |
   | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
   | `kinetic-type` | 一句有力的话 / 引用 / 标题；文字是主角                                                                                                                                    |
   | `stat`         | 单个 hero 数字 / 计数动画                                                                                                                                                    |
   | `charts`       | 由数据驱动的柱状 / 折线 / 饼图 / race / 百分比                                                                                                                                              |
   | `logo-reveal`  | Logo 片头 / 品牌定版（用户提供 logo）                                                                                                                               |
   | `lower-thirds` | 姓名/职务条、标注、社交 overlay                                                                                                                                         |
   | `maps`         | 地理镜头——高亮区域、连接地点、缩放到位置。子分支：**vector**（D3，风格化） vs **basemap**（预烘焙 MapLibre——真实卫星/暗色/缩放到地点） |
   | `webpage`      | 高亮 / 动画化真实抓取的网页或 UI _(搜索驱动)_                                                                                                               |
   | `news`         | 新闻文章 → 文章高亮：模糊 → 缩放到关键词 _(搜索驱动)_                                                                                                     |
   | `tweet`        | 推文 → 动画卡片 _(搜索驱动)_                                                                                                                                          |
   | `asset-fusion` | 真实照片/素材的几何 _成为_ 图表 _(搜索驱动)_                                                                                                                |

   若在两类之间确实难以区分，只问 **一个问题**。然后加载 `categories/<id>/module.md` 以获取该 category 的细节。

2. **素材策略 → `asset_needs[]`。** 每项：`{ role, kind: image|icon|logo|svg|news|web|tweet, query|source, treatment }`。
   - 无需素材（`kinetic-type`、多数 `stat`/`charts`）→ `asset_needs: []`。
   - `maps` → **vector** 路径：`asset_needs: []`（D3/TopoJSON，在 HF 中实时运行）。**basemap** 路径（卫星/暗色/缩放到地点）：`asset_needs: [{ type: "map-bake", … }]`（在 Source 中烘焙——见 `categories/maps/module.md`）。
   - `webpage` / `news` / `tweet` → 搜索真实来源（页面 / 文章 / 推文）+ 一张辅助图。**仅两极查询**：atomic（1–3 词，可组合：人像、logo、物体）或 specific（5–15 词：某新闻事件、某条推文）。不要取中间地带。specific 查询失败则丢弃，不要放宽。
   - `asset-fusion` → 搜索或生成一张 hero 素材。
   - `logo-reveal` → 用户提供的 logo（`source`）。

3. **Envelope**：`duration_s`（3–30）、`fps`（30）、`canvas`（默认 1080×1920；按平台 16:9 / 1:1）、`style`、`palette`（hex 列表，或 `"derive-from-asset"`）、`font`（来自 HF embed 列表）、`beats`、`export`（`mp4` | `alpha-overlay`）。

4. **镜头 brief**：一段——观众会看到什么 + 唯一主导 motion 创意。

## Part 2 — 设计（采集后）

在 draft + 已解析的 `assets/index.md`（若 Step 2 已跑）+ `catalog-map.md` 基础上，**围绕素材** 设计镜头：

- 选定 **catalog block(s)** + `hyperframes-animation` 规则 / blueprint（catalog 感知——见 `catalog-map.md`）。
- 布局（hero-frame）、motion（按 `references/motion-vocabulary.md`）、beats、节奏、退场。
- `asset-fusion`：读取素材的 **几何 affordance** → `element_positions`（center / extent / safe-zones / avoid-zones）+ 从素材 **吸管取色 palette**。
- 定稿 `shot-plan.json`：`content.block` + `content.customize` + 各 category 的 `content`。

## 启发式（设计驱动的短动效）

- **Motion 即信息**；无旁白叙事弧。Hook 快速落地（约前 0.5s）。**一个主导 motif。** 若片长 >~2.5s 则 pattern-interrupt（只改一件事）。效果强度匹配能量。可读性：关键元素保持可读 ≥~0.3s。Beats 可提前约 0.1s 以感知同步。
- **复用优先**：点名 catalog block；仅在缺口 + `asset-fusion` affordance 处要求手写 motion。

然后将 `shot-plan.json` 交给 Builder。
