# charts — 分类模块

从数据生成动画化**数据可视化**。无需素材（「输入」即数据）。短时场景遵循「一图一信息」。

## 规划（Director）

`content`：`{ type: bar|line|pie|race|pct, data[], labels[], headline, axes: bool }`。`race` 类型时，数据须为累积/分阶段时间序列。

## 词汇 / 依赖

- 区块：**`data-chart`**（动画**柱状 + 折线**、错落揭示、数值标签 — 已验证：在原型 `charts-demo` 中借用、定制并渲染为 MP4）。
- 缺口（需手写）：**饼图 / 环形图、条形竞赛图、环形/百分比** — `data-chart` 未覆盖。数据→几何用 D3/visx，动效用 GSAP。
- 标志性动画：柱形错落生长 · 折线 `stroke-dashoffset` 描边绘制 · 饼图径向扫过 · 环形填充 · KPI 数字递增 · 竞赛重排。

## 构建（复用优先）

复用 `data-chart`：`npx hyperframes add data-chart` → 就地编辑数据数组、比例尺、标题/标签与配色（数据写在脚本内，无 `--variables` 参数）。坐标轴默认隐藏；仅当量级本身是信息时才以弱化样式显示。确定性：一切动画由 seek 时钟驱动，勿用墙钟时间。

## 仪表盘骨架变体

**产品仪表盘**场景：搭骨架布局 — 顶栏放**真实测试 Logo**（如 `samples/_assets/` 中的 hyperframes logo）+ 标题，下方网格 3–4 张 **KPI 卡片**（各为 `stat` 数字递增）+ 一块 `data-chart` 面板。揭示顺序：页眉/Logo 入 → 卡片错落入 → 图表动画。在仪表盘框架内组合 `stat` 与 `charts` 原语；Logo 为冻结的项目本地素材。
