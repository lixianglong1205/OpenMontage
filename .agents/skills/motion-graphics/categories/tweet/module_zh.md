# tweet — 分类模块（搜索驱动）

**搜索一条推文 → 动效化推文卡片。** 基于真实帖子（RWA）。约 4–8 秒。

## 来源（步骤 2）

RWA `search_tweets`（具体查询，或给定的推文 URL/id）→ 推文：作者、handle、头像、正文、时间戳、指标（点赞/转发）。`asset_needs`：`{ kind: tweet, query|source, treatment: none }`。冻结头像及任何内嵌媒体。

## 词汇 / 依赖

- Block：registry **`x-post`**（带动效指标数据的 X/Twitter 帖子卡片叠加层）— 直接复用。
- Primitives：卡片滑入/缩放进入 · 文字逐字打出 / 逐行揭示 · 头像弹出 · 指标 **count-up** · 可选的关键词强调。

## 构建（复用优先）

`npx hyperframes add x-post` → 从解析后的推文填入 author / handle / avatar / text / metrics；让卡片入场，文字 type-on（或逐行揭示），指标 count-up。冻结为项目本地头像/媒体（绝不使用远程 URL）。若需叠在其他画面上方，使用 `export: alpha-overlay`。
