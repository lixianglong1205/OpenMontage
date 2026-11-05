# locate — 在图像中查找「X」（不假定存在检测器 API）

所有消费者（asset-fusion 环、网页高亮、未来的 explainer/recut 叠加层等）共用的单一契约：

```
locate(image, target-description) → { box: [x0,y0,x1,y1], center: [cx,cy] }   # normalized 0..1
```

## 为何需要此协议

作者模型在**杂乱全图上回归像素坐标**时不可靠（实测：弱视觉模型中心误差约 16–24% → 环会偏离目标），但在**选择编号条带**上可靠（配合下方循环约 3–4%）。因此：永远不要凭感觉估坐标；通过离散选择来定位。（RSVP，ACL 2025。）

## 路由 — 选择实际可用且成本最低的路径

1. **有强检测器可用**（例如环境中配置了 `GEMINI_API_KEY`）→
   `node grounding/locate.mjs auto <img> "<target>"` — 一次调用即可。
   **切勿假定密钥存在。** 无密钥 → 走路径 2。
2. **无检测器（常见情况）** → 由**你**担任定位器；运行网格循环。

## 网格循环（各步之间由你读取图像）

```
node grounding/locate.mjs overlay <img> --out /tmp/g
  → READ /tmp/g/gv.png (vertical strips 1-9) and gh.png (horizontal 1-9);
    decide which strip numbers the target spans (list EVERY strip it touches).
node grounding/locate.mjs region <img> --vids 4,5 --hids 6,7 --out /tmp/g
  → READ /tmp/g/gc.png (the region cropped + upscaled, finer 6×6 grid);
    pick the finer strips. (Pick strips again — do NOT switch to estimating
    coordinates; discrete choice is the whole point, at BOTH stages.)
node grounding/locate.mjs final <img> --region <from step 2> --vids 3,4 --hids 3,4
  → the final {box, center}.
node grounding/locate.mjs mark <img> --box <final box> --out /tmp/g/check.png
  → VERIFY: READ check.png. Red box ON the target → done. Off → redo
    region/final with corrected strips (you now know which direction). Never
    skip this step; it converts silent misses into one cheap retry.
```

## 歧义 — 在定位之前先消解

若目标描述可能匹配多个实例（例如场景里有五个鼓时只说「a drum」），任何几何方法都救不了。先让指称唯一（「最右侧的鼓」「前船上的鼓」），必要时向用户确认 — 然后再运行循环。

## 降级路径（若 locate.mjs 本身不可用）

核心思路只有五行 — 用任意图像工具复现即可：
绘制编号 9×9 网格 → 选出目标所跨条带 → 裁剪该区域（条宽约 +0.4 的 padding）并放大 → 绘制更细的 6×6 网格 → 再选一次 → 映射回全局坐标
（`global = region_origin + local × region_size`）→ 画出框并**目视检查**。

## 说明

- 几何逻辑固化在 `locate.mjs` 中（node + ffmpeg，零 npm 依赖 — hyperframes 已要求二者）。不要临时重写；实测精度依赖**这一实现**。
- 消费者：`samples/asset-fusion/_ref-circle-highlight.html` 可直接使用 `final`/`auto` 输出的 `CFG.box`。
- 端到端实测（同一 agent、同一模板，仅定位步骤不同）：凭感觉估坐标平均中心误差 6.5% → 本协议 2.3%，且无更差个案。
