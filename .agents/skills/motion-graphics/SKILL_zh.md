---
name: motion-graphics
description: >
  当用户需要一段简短、设计驱动的动态图形，且「动效即信息」时使用： kinetic typography（ kinetic 文字动画）、
  统计或数字 count-up（递增动画）、图表/数据可视化强调、logo sting（logo 片头）、
  brand lockup（品牌定版）、lower-third（下三分之一条）、callout（标注）、社交 overlay（叠加层）、
  动画标题/推文/新闻条目、motion poster（动态海报），或快速 captured-page（页面捕获）高亮。
  通常短于 10 秒、最长约 30 秒，无旁白叙事弧、无 voice-over（画外音）或实拍主体。
  可渲染为 MP4 或透明 overlay。不适用于更长、多场景、带旁白或品牌 reel 类作品（用 general-video）、
  带旁白的网站视频（website-to-video）、主题讲解（faceless-explainer）、
  产品 promo（product-launch-video）、PR 视频（pr-to-video），或在已有 footage 上加字幕（embedded-captions）。
  不确定是「快速动效优先」还是「更长/带旁白」处理时，请先参阅 /hyperframes。
metadata:
  {
    "tags": "orchestrator, motion-graphics, kinetic-type, data-viz, logo-reveal, lower-thirds, news, tweet, webpage, asset-fusion, short-form, overlay, no-narration",
  }
---

# motion-graphics — 调度入口

> **在 Step 0 之前确认路由。** 本技能产出**简短、设计驱动、无旁白的动态图形**（动效即信息；约 10 秒以内、无画外音）。**更长、多场景或带旁白**的处理 → `/general-video`；**带旁白的网站视频** → `/website-to-video`；**主题讲解** → `/faceless-explainer`；**产品 promo** → `/product-launch-video`；**在已有 footage 上加字幕** → `/embedded-captions`。**超出范围**：live / 渲染时实时数据，或无法捕获的 footage。不确定动效优先还是带旁白？**请先阅读 `/hyperframes`。**

一段简短、设计驱动的动态图形。**资产优先（Asset-first）**：在设计镜头之前先决定资产策略并获取真实素材，再围绕已有素材设计镜头，然后通过复用目录能力进行合成。所有产物写入 `PROJECT_DIR = videos/<project-name>/`（在 Step 0 创建）；下文路径均相对该目录。

| 阶段     | 执行                                                                  | 主要产物                                                         | 详细流程                      |
| -------- | --------------------------------------------------------------------- | ---------------------------------------------------------------- | ----------------------------- |
| init     | Bash                                                                  | `hyperframes.json`                                               | Step 0                        |
| plan     | subagent — **决定是否搜索？** + 分类 + 资产策略                       | `shot-plan.json`（草稿：category、`asset_needs` 查询、brief）    | `agents/director.md`（Part 1） |
| source ◇ | Bash — media-use resolve（**若 `asset_needs` 为空则跳过**）           | `assets/` + `assets/index.md`                                    | `phases/source/guide.md`      |
| design   | subagent — 围绕已解析资产设计镜头                                     | `shot-plan.json`（终稿：block(s) + layout + motion + positions） | `agents/director.md`（Part 2） |
| build    | subagent — 复用优先合成                                               | `compositions/index.html`                                        | `agents/builder.md`           |
| render   | Bash — `hyperframes render`（MP4，或 overlay 用 `--format webm/mov`） | `renders/video.mp4`                                              | Step 5                        |
| verify   | Bash — `lint` / `inspect` -> 失败时 repair subagent                   | （就地修复）                                                     | `agents/finalize.md`          |

`◇ source` 仅当所选 category 声明需要资产时运行。纯代码/文本类 category（如 `kinetic-type`、多数 `charts`/`stat`）的 `asset_needs: []`，从 plan 直接跳到 design。

## 分类 — 按「是否搜索」划分

`plan` 的**首要决策是：是否需要搜索？** 该分支将 category 分为两组；再选定具体 category — 对搜索驱动类，**按搜索返回的内容类型**选择。每个 category 对应一个 `categories/<id>/module.md`（其规划与构建规则）；共享动效词汇见 `references/motion-vocabulary.md`（→ `hyperframes-animation` rules/blueprints + registry blocks）。

**形态类 category — 不搜索；用户提供内容：**

| Category       | 意图                                           | 主要依赖                                                                    |
| -------------- | ---------------------------------------------- | --------------------------------------------------------------------------- |
| `kinetic-type` | 有力的一行/引用/标题，动效优先文字             | `caption-*` blocks + animation rules                                        |
| `stat`         | 单个 hero 数字 / count-up + 环形               | `apple-money-count` / `rules/{counting-dynamic-scale, stat-bars-and-fills}` |
| `charts`       | 来自数据的 bar / line / pie / race / %         | `data-chart` block                                                          |
| `logo-reveal`  | logo sting / brand lockup（用户 logo）         | `logo-outro` / `rules/svg-path-draw`                                        |
| `lower-thirds` | 姓名/标题条、callout、社交 overlay             | `caption-*` + registry overlay blocks                                       |

**搜索驱动 category — 先搜索，再按内容类型动效化**（RWA 路径）：

| 返回内容         | Category       | 动效                                                           |
| ---------------- | -------------- | -------------------------------------------------------------- |
| webpage / link   | `webpage`      | webpage / UI 动效（滚动、揭示、光标、callout）                 |
| news article     | `news`         | 标题揭示 + 来源卡片 + 关键事实 callout                         |
| tweet            | `tweet`        | 动画推文卡片                                                   |
| image / entity   | `asset-fusion` | 资产几何**成为**图表（RWA diegetic fusion）                    |

构建顺序：一次一个，覆盖优先（粗略即可）。`kinetic-type` 已从原型移植；其余按序跟进。

## 前提条件

macOS Apple Silicon 或 Linux x64。系统工具：`brew install node ffmpeg`。运行一次 `npx hyperframes doctor`。macOS GPU 渲染：`export PRODUCER_BROWSER_GPU_MODE=hardware`。

可选密钥（未设置时使用本地回退）— 仅被通过 media-use  sourcing/生成资产的 category 需要：

| Key                                 | 用途                                                        | 回退                            |
| ----------------------------------- | ----------------------------------------------------------- | ------------------------------- |
| `GEMINI_API_KEY` / `GOOGLE_API_KEY` | 图像生成（media-use resolve）                               | 跳过 generate / 仅 search       |
| (asset_scout / search providers)    | `webpage`/`news`/`tweet` + `asset-fusion` 真实资产搜索      | category 降级为无资产           |

## 流程

### Step 0 — 初始化

cwd 为 agent 工作区根目录；所有产物写在 `PROJECT_DIR = videos/<project-name>/` 下。`<project-name>`：用用户给出的目录，否则从意图生成短 kebab-case 名（`<subject>-motion`）。不要用工作区 basename 或时间戳。

仅当 `$PROJECT_DIR/hyperframes.json` 不存在时：

```bash
PROJECT_DIR="${MOTION_GRAPHICS_DIR:-videos/<project-name>}"
mkdir -p "$(dirname "$PROJECT_DIR")"
npx hyperframes init "$PROJECT_DIR" --non-interactive --example=blank
```

`init` 会对照 GitHub 最新版检查已安装 skills，若有过期则更新全局集合。

**约束：** 切勿在工作区根目录执行 `hyperframes init`；切勿在 `PROJECT_DIR` 内再嵌套 `hyperframes/`；每条 Bash 命令（主 agent + subagent）必须是 `(cd "$PROJECT_DIR" && ...)` 子 shell — 禁止裸 `cd`。

### Step 1 — Plan（subagent：Director Part 1）

派发一个 subagent。prompt = 完整 `agents/director.md` + `## Dispatch context`（`SKILL_DIR` / `PROJECT_DIR` / 用户请求 / `Schema: <SKILL_DIR>/references/shot-plan-ir.md`）。它必须：

1. **决策：是否需要搜索？**（第一分支）
   - **否** → 选**形态 category**（kinetic-type / stat / charts / logo-reveal / lower-thirds）；内容由用户提供；`asset_needs: []`。
   - **是** → 将**搜索计划**写入 `asset_needs[]`（news / web / tweet / image；两极查询）。具体**搜索驱动 category**（webpage / news / tweet / asset-fusion）在 Step 2 按返回内容类型确认，在 Step 3 定稿。
2. 写入草稿 `shot-plan.json`（envelope + 所选形态 category _或_ 搜索意图 + `asset_needs` + 一段 shot brief）。Schema：`references/shot-plan-ir.md`。

Validation: `[ -s "$PROJECT_DIR/shot-plan.json" ] && echo ok || echo missing`。

### Step 2 — Source ◇（Bash：media-use，条件执行）

若 `shot-plan.json.asset_needs` 非空，解析资产（search / generate / fetch → 冻结的项目本地路径 + ledger）。见 `phases/source/guide.md`（封装 `media-use resolve`；搜索驱动 category 使用 news/web/tweet/image 搜索）。若 `asset_needs` 为空，**跳到 Step 3**。

```bash
# illustrative — see phases/source/guide.md
(cd "$PROJECT_DIR" && node <SKILL_DIR>/phases/source/resolve.mjs --plan ./shot-plan.json --out ./assets)
```

优雅降级：若搜索/ provider 不可用，category 回退为无资产（在 `context.log` 中注明）。

### Step 3 — Design（subagent：Director Part 2）

派发 subagent（prompt = `agents/director.md` Part 2 + dispatch context，含 Step 2 若运行则 `assets/index.md` + `catalog-map.md`）。它**围绕可用资产**设计镜头：选 catalog block(s) + `hyperframes-animation` rules/blueprints、layout、motion、beats，以及（对 `asset-fusion`）`element_positions` + eyedropper palette。定稿 `shot-plan.json`（`content.block` + `content.customize` + 各 category 内容）。

### Step 4 — Build（subagent：Builder，复用优先）

派发 subagent。prompt = 完整 `agents/builder.md` + dispatch context（`shot-plan.json`、`catalog-map.md`、该 category 的 `module.md`、`references/motion-vocabulary.md`、`references/builder-contract.md`）。**复用优先**：`npx hyperframes add <block>` + 就地 customize；仅手写缺口 + asset-fusion affordance。输出 `compositions/index.html`，遵守 HF contract（paused GSAP timeline 在 `window.__timelines`、`class="clip"` + 稳定 id、`tl.seek(0)`、确定性）。

### Step 5 — Render（Bash）

```bash
(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q draft -o ./renders/video.mp4)
# transparent overlay variant: --format webm  (or mov)
```

### Step 6 — Verify（Bash → 失败时 repair subagent）

```bash
(cd "$PROJECT_DIR" && npx hyperframes lint . && npx hyperframes inspect .)
```

exit 0 → 完成。lint/inspect 报错时，派发 repair subagent（`agents/finalize.md`：snapshot QA + 一次就地修复 + 重渲染）。repair 中切勿修改已固定的 duration。

### 报告 + 可选预览

报告最终输出（`renders/video.mp4`，或 `.webm` / `.mov` overlay 变体）+ duration。**运行过程中不要打开预览。** 仅在用户请求时、在**渲染完成后**再启动，以提供最终文件：

```bash
(cd "$PROJECT_DIR" && npx hyperframes preview)   # Studio UI; or `npx hyperframes play` for a shareable link
```

标志位见 `hyperframes-cli` skill（`references/preview-render.md`）。

## 恢复表

| 状态                                                     | 从何处继续               |
| -------------------------------------------------------- | ------------------------ |
| 无 `shot-plan.json`                                      | Step 1（plan）           |
| `shot-plan.json` 含 `asset_needs`，无 `assets/`        | Step 2（source）         |
| `shot-plan.json` 已定稿，无 `compositions/index.html`  | Step 3/4（design+build） |
| 已有 `compositions/index.html`，无 `renders/video.mp4` | Step 5（render）+ Step 6 |
| 已有 `renders/video.mp4`                                 | 报告并停止               |

## 设计说明（维护者 — 执行流程不读本节）

- **资产优先理由：** sourcing 前置并 inform 镜头设计（RWA 流：analyze → search → review → compose）。搜索驱动 category（`webpage`/`news`/`tweet`）与 `asset-fusion` 均依赖 media-use 搜索（news/web/tweet/image），即 media-use 文档中的 RWA  lineage。
- **复用优先：** 生态内类比 LLM 生成模板的是「组合 catalog blocks + `hyperframes-animation` rules」。HF 的 paused GSAP timeline ≙ Remotion 的 `useCurrentFrame`。
- **Category 模块契约：** 一个 `categories/<id>/module.md`（plan + build），共享 `references/motion-vocabulary.md`（+ 可选 eval）。新增 category = 放入文件夹 + 在 `agents/director.md` 注册 classifier 行 + 在 `catalog-map.md` 增加一行；阶段 pipeline 不变。
- **目录结构：**
  ```
  videos/<project-name>/
    hyperframes.json  context.log
    shot-plan.json            # the IR (Director output)
    assets/  assets/index.md  # media-use output (if sourced)
    compositions/index.html   # Builder output
    renders/video.mp4
  ```
- **注册：** 在 `hyperframes` router 中 — 添加「设计驱动短动态图形」意图 + Workflow 描述；从 `/general-video`  carve 出 motion-graphics 触发；添加反向 Do-NOT-use 边。见 `motion-graphics-genre.md` §5-7。
