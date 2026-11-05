# stat — 分类模块

单个**主数字**揭晓动效。无需素材（「输入」即为数字本身）。时长约 4–6 秒。

## 方案（Director）

`content`：`{ value, prefix ($), suffix (% / x / K-M-B), label, ring: bool }`。整体气质：粗体展示字体，克制配色 + 一处强调色。

## 词汇 / 依赖

- 区块：**`apple-money-count`**（金融向：$ 计数 + 绿色闪动 + 钱币 burst + 音效），适用时优先复用；否则手写实现。
- 规则：`hyperframes-animation/rules/{counting-dynamic-scale, stat-bars-and-fills}`。
- 原语：`count_up`（里程表式计数）· `scale_pop` · `ring_fill`（弧环）· `label_stagger`（数值落定后）· `hold`。

## 构建（复用优先）

复用 `apple-money-count` 并设置 target / prefix / suffix / label / palette；**或**按已验证原型 `v0-stat-motion-demo` 手写：

- **计数由时间轴驱动** — 对代理对象 `{v:0}→target` 做 tween，在 `onUpdate` 中写入格式化数字（可 seek；勿用 setInterval/墙钟时间）。
- `font-variant-numeric: tabular-nums`；减速缓动；约 1.2–1.6 秒后 **hold** 最终数值。
- 环/弧通过 `stroke-dashoffset` 实现，与 count-up 同步结束；标签在数字落定**之后**淡入（数值 → 含义）。
