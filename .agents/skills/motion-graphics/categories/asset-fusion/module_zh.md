# asset-fusion — 分类模块（搜索驱动 · 全新 IP）

**真实资产的 geometry _成为_ 图表** — RWA 叙事内融合（吸管变成仪表；玻璃杯中的液体变成饼图）。不在任何目录中；真正全新的能力。约 5–8 秒。

## 来源（Step 2）

搜索或生成一个具有强几何 affordance 的 **hero asset**。`asset_needs`：`{ kind: image, query|generate, treatment: cutout|none }`。将其冻结在项目本地。

## 规划（Director Part 2）— 融合逻辑

1. 分类 **数据类型**（temporal / quantitative / proportion / spatial）。
2. 读取资产的 **几何 affordance** — 线性 → 时间线/仪表 · 体积/纹理 → 饼图 · 高度 → 柱状 · 容器 → 爆炸视图。
3. `element_positions`：**用定位协议做 GROUND — 绝不凭肉眼估像素坐标。** 阅读 **`grounding/PROTOCOL.md`**，并用 `node grounding/locate.mjs` 运行循环（`overlay` → 读条带 → `region` → 读裁剪 → `final` → **`mark` + 验证**）。零密钥/零依赖假设（仅 node + ffmpeg）；可选 `auto` 快速路径仅在碰巧设置了 `GEMINI_API_KEY` 时存在。原因：凭肉眼会把环画偏主体（弱视觉模型上约 16–24% 中心误差）；网格循环可拉到约 2–4%（端到端实测：肉眼 6.5% → 协议平均中心误差 2.3%，无更差案例）。
4. 从资产 **吸管取色板**（绝不用通用 #FFF/#000）。

## 高亮 + 圆环配方（常见情况）

「在真实图像中为对象 X 加环/聚光灯」→ 使用即插即用模板 **`samples/asset-fusion/_ref-circle-highlight.html`**：设置 `CFG.box`（来自定位协议）、`CFG.label`、`CFG.asset`、偶数 `CFG.W/H`、`CFG.mode`（`full` = 环+连接线+标签+角括号+扫描线，`circle` = 仅环）。它根据 box 计算径向 wash、琥珀色双线描边环、连接线、标注与角括号准星。完整流水线：locate（PROTOCOL.md）→ 填模板 → 渲染。

## 渲染注意事项（已编码 — 跳过这些会破坏渲染）

- **偶数宽高** — 宽或高为奇数（如 1400×933）→ `ffmpeg` 编码失败/失真。将资产/舞台 resize 为偶数尺寸（1400×932）。
- **`data-width`/`data-height` 必须是舞台上的静态 HTML 属性** — 渲染器的 StaticGuard 在编译时、JS 运行前读取它们。通过 `setAttribute` 设置太晚 → 渲染回退到竖屏 1080×1920 并失真。（圆环高亮模板现已硬编码；保持与 `CFG.W/H` 相等。）
- **描边动画（`stroke-dashoffset`）必须用 `autoAlpha:0` 门控** — layout 前 `getTotalLength()` 可能读到 0 → dash 禁用 → t=0 出现实线。每个 draw-on 元素用 `autoAlpha:0` 门控直到开始绘制，并回退 `getTotalLength() || <const>`。
- **CSS 变量 tween 作用域** — `gsap.to(":root", {"--x":..})` 无法到达自身 inline 设置了 `--x` 的元素；应在该元素上 tween 变量。
- **固定 overlay 下不要做 camera push** — 缩放图像而环/wash 固定会把目标移出环。要么跳过 push，要么整场景一起缩放。
- 无损交付：`--format mov`（ProRes）；`mp4` 为有损。

## 词汇 / 依赖

- 从 registry **`north-korea-locked-down`** 借用标注套件（手绘 scribble 圆环 draw-on、弹出标签 + 指针、编辑 wash、camera push）。
- 原语：沿 affordance 的 gauge fill / marker-rise · 连接线（数据 → 资产点）· 与资产 geometry 融合的叙事内图表。
- 按每个资产的 affordance 适配叙事内图表（读 geometry，把数据融合进去）。

## 构建（复用优先 + 手写 affordance）

**两层**：资产（z0，全出血）+ 与其 geometry 融合的数据图形（z1+），由 `element_positions` 锚定；连接线/scribble 在物理上把数据绑到资产；资产保持可见。参考实现：原型 `fusion-demo/index-annotated.html`（吸管 → 仪表 + 借用的标注套件）。
