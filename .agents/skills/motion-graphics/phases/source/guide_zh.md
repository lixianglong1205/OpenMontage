# source 阶段 — 资产采购（asset-first）

**仅当** `shot-plan.json.asset_needs` **非空时**运行（表单类别不会进入此阶段）。为每项所需资产采购 → 得到**冻结的项目本地路径** + 台账（`assets/index.md`）。使用 `/hyperframes-media`（采集 / 资产准备）；**若已安装外部资产搜索类技能（如 media-use）**，则使用其 `resolve` 步骤。若无此类搜索能力，则**降级为无资产模式**（见下文）。

## 每项 asset_need

- `image / icon / logo / svg` → media-use `resolve`：**搜索**（asset_scout：Google Images / SerpAPI + Noun Project）、**生成**（图像模型）或**用户提供**（logo）。可选 `treatment`：cutout（去背景）/ recolor / vectorize。
- `news / web / tweet` → **RWA 式搜索**（media-use 文档中的 lineage — `media-use/references/search-strategy.md` 将 `resolve` 追溯到 RWA 子代理）。两极查询：**原子型**（1–3 个词，可组合）或**具体型**（5–15 个词：某条新闻事件 / 推文）；避免介于两者之间的模糊查询。具体型查询失败则丢弃，不放宽。

## 步骤

1. 从 `shot-plan.json` 读取 `asset_needs`。
2. 对每一项：**分析 → 搜索 → 评审（采用 / 待定 / 拒绝 — 选型是难点；不要直接采用第一个或生成的结果）→ 冻结**保留资产到 `assets/`（重新托管远程 URL）。
3. 编写 `assets/index.md` — 供代理阅读的台账：`role → 冻结路径 + 来源`。
4. 对于 `asset-fusion`：还需采集资产的可度量几何（以便 Director Part 2 设置 `element_positions`）+ 吸管取色板。

## 优雅降级

若某 provider / 搜索不可用，在 `context.log` 中将该需求标为未满足；该类别在可能时回退为无资产模式（例如 `news` → 无采购图文的排版标题）。

> 示例：`(cd "$PROJECT_DIR" && node <SKILL_DIR>/phases/source/resolve.mjs --plan ./shot-plan.json --out ./assets)` — 或直接驱动 media-use 的 `resolve` 流程。
