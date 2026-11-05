# 转场注册表 — 机器可读的权威数据源

**PLV 场景间转场**的单一权威来源。确定性注入器（`product-launch-video/scripts/inject-transitions.mjs`）读取下方的 JSON 块，并将匹配的 `gsap_template` 写入主时间轴。规划器（`product-launch-video/agents/visual-design.md`）通过 `name` 指定转场；其余均由 harness 处理。

本文件**不是**全部转场的目录——那在 `catalog.md` 与 `css-*.md`（约 40 种 CSS + shader）中。本注册表是已精选、**Tier-B 就绪**的子集：仅对两个场景** clip 包装器**（`#el-<sid>`）做纯 transform / opacity / filter，不注入 overlay DOM，也不要求各场景配合。overlay 类（交错块、百叶窗、漏光、网格溶解、页面燃烧）与 shader 转场留待后续阶段。

## 注入器如何应用转场

在场景 _i_（`from`）与场景 _i+1_（`to`）之间的 `break` 边界，注入器会：

1. 将 `#el-<from>` 包装器的 `data-duration` 延长 `duration_s`（保持其最后一帧——已验证：`core/src/runtime/init.ts:1393-1410` 的 external-slot 分支）。
2. 将 `#el-<to>` 包装器的 `data-start` 提前 `duration_s`（形成重叠窗口）。
3. 将所有 clip 的 `data-track-index` 按 0/1 乒乓重分配，使两个重叠包装器永不共轨（同轨重叠非法——见 `core/src/lint/rules/composition.ts`）。较高轨道叠在上方。
4. 在 `T = overlap-start` 处，将 `gsap_template` 写入 `window.__timelines["main"]`。

原型渲染已验证（2026-05-31）：主时间轴包装器 tween 会被 seek 并渲染（不与子 comp 自身 paused 时间轴二次 seek——运行时独立驱动），延长后的包装器保持场景 _i_ 的最后一帧，较高轨道的入场景包装器叠在上层并与出场景混合。

## 模板占位符

注入器会在每条 `gsap_template` 行中替换以下 token：

| Token                              | 含义                                                                  |
| ---------------------------------- | ------------------------------------------------------------------------ |
| `__OLD__`                          | `"#el-<from>"` — 出场景 clip 包装器选择器（带引号）                 |
| `__NEW__`                          | `"#el-<to>"` — 入场景 clip 包装器选择器（带引号）                   |
| `__T__`                            | 重叠起始时刻（秒，主时钟）                             |
| `__DUR__`                          | 该边界的 `duration_s`                                           |
| `__DX__`                           | 方向性类型的水平位移：`-1920`（LEFT）/ `1920`（RIGHT） |
| `__DY__`                           | 垂直位移：`-1080`（UP）/ `1080`（DOWN）                            |
| `__ORIGIN_OUT__` / `__ORIGIN_IN__` | `squeeze` 的 transformOrigin 配对                                       |

`filter` / `scaleX` / `transformOrigin` 在主时间轴上通过 lint（已验证：`core/src/lint/rules/gsap.ts` 无逐属性白名单，且检查范围限定在 `data-composition-id` 区间；x/y/scale/rotation/opacity 白名单仅是*场景 worker* 提示规则——不约束 index.html）。

## 注册表

```json
{
  "transitions": [
    {
      "name": "crossfade",
      "tier": "b",
      "overlay": false,
      "energy": "any",
      "default_duration_s": 0.5,
      "directions": [],
      "source": "css-dissolve.md",
      "gsap_template": [
        "tl.to(__OLD__, { opacity: 0, duration: __DUR__, ease: \"power2.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { opacity: 0 }, { opacity: 1, duration: __DUR__, ease: \"power2.inOut\" }, __T__);"
      ]
    },
    {
      "name": "blur-crossfade",
      "tier": "b",
      "overlay": false,
      "energy": "calm",
      "default_duration_s": 0.6,
      "directions": [],
      "source": "css-dissolve.md",
      "note": "Default when the two scenes' #root backgrounds differ a lot — the blur masks the background-color clash a plain crossfade would expose.",
      "gsap_template": [
        "tl.to(__OLD__, { filter: \"blur(10px)\", scale: 1.03, opacity: 0, duration: __DUR__, ease: \"power2.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { filter: \"blur(10px)\", scale: 0.97, opacity: 0 }, { filter: \"blur(0px)\", scale: 1, opacity: 1, duration: __DUR__, ease: \"power2.inOut\" }, __T__);"
      ]
    },
    {
      "name": "push-slide",
      "tier": "b",
      "overlay": false,
      "energy": "medium",
      "default_duration_s": 0.5,
      "directions": ["LEFT", "RIGHT", "UP", "DOWN"],
      "default_direction": "LEFT",
      "source": "css-push.md",
      "note": "Directional. The injector picks __DX__/__DY__ from the direction and emits the horizontal OR vertical pair (not both).",
      "gsap_template_horizontal": [
        "tl.to(__OLD__, { x: __DX__, duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { x: __DXIN__, opacity: 1 }, { x: 0, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ],
      "gsap_template_vertical": [
        "tl.to(__OLD__, { y: __DY__, duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { y: __DYIN__, opacity: 1 }, { y: 0, duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ]
    },
    {
      "name": "zoom-through",
      "tier": "b",
      "overlay": false,
      "energy": "high",
      "default_duration_s": 0.4,
      "directions": [],
      "source": "css-scale.md",
      "gsap_template": [
        "tl.to(__OLD__, { scale: 2.5, opacity: 0, filter: \"blur(8px)\", duration: __DUR__, ease: \"power3.in\" }, __T__);",
        "tl.fromTo(__NEW__, { scale: 0.5, opacity: 0, filter: \"blur(8px)\" }, { scale: 1, opacity: 1, filter: \"blur(0px)\", duration: __DUR__, ease: \"power3.out\" }, __T__);"
      ]
    },
    {
      "name": "squeeze",
      "tier": "b",
      "overlay": false,
      "energy": "medium",
      "default_duration_s": 0.4,
      "directions": [],
      "source": "css-push.md",
      "note": "Old compresses to a vertical line on the left edge; new expands from the right edge. Incoming starts off (scaleX 0) so its higher-track stacking is harmless.",
      "gsap_template": [
        "tl.to(__OLD__, { scaleX: 0, transformOrigin: \"left center\", duration: __DUR__, ease: \"power3.inOut\" }, __T__);",
        "tl.fromTo(__NEW__, { scaleX: 0, transformOrigin: \"right center\", opacity: 1 }, { scaleX: 1, transformOrigin: \"right center\", duration: __DUR__, ease: \"power3.inOut\" }, __T__);"
      ]
    }
  ],
  "tier_a_types": ["morph", "shared-element"],
  "default_high_energy": "zoom-through",
  "default_calm": "blur-crossfade",
  "max_duration_s": 2.0
}
```

## 默认推导（规划器省略 `**Transition:**` 时由 prep.mjs 使用）

未命名转场的 `break` 边界会采用默认：

1. 若入场景创意简报为 HIGH 能量（explosive / kinetic / frenetic 等关键词），使用 `default_high_energy`（`zoom-through`）。
2. 否则使用 `default_calm`（`blur-crossfade`）——通用默认。模糊可掩盖背景变化，观感 intentional，整片约 2 种转场（「重复 2–3 种」原则）。

## 作为规划器如何选择（唯一的 agent 触点）

整片选 **2–3 种类型并重复使用**——重复才显得专业（见 `overview.md`）。该预算仅计**场景间 Tier-B 类型**（上表注册 5 种）；Tier-A 的 `shared-element` morph 由叙事 `intent: morph` 驱动的 worker 编写桥接——**豁免，不计入** 2–3。在每个场景上命名入转场：

```
**Transition:** blur-crossfade
**Transition:** push-slide LEFT
**Transition:** zoom-through 0.3s
```

省略该锚点则接受上文默认。不要写 GSAP、不要动 timing、不要改 index.html——harness 会写入代码、计算重叠并分配轨道。
