---
name: pose-library-design
description: 设计可复用的 2D 角色姿势库、动作循环与表情状态，用于数据驱动动画。
license: MIT
---

# 姿势库设计

在产出 `pose_library` 产物时使用本技能。

## 姿势类别

- 中性：idle、breathe、listening。
- 注意力：look_up、look_down、look_left、look_right。
- 情绪：happy、sad、surprised、worried、determined。
- 动作：reach、point、hold、jump、flap、walk_contact、walk_passing。
- 口型：closed、small_o、wide_open、smile、frown、phoneme-ish shapes。

## 表演模式

使用带时序的姿势序列：

```text
anticipation -> action -> hold -> settle
```

不要让每个部位持续运动。停顿（hold）让表演更易读。

## 姿势数据模式

```json
{
  "pose": "surprised",
  "parts": {
    "head": { "rotation": -6, "y": -4 },
    "pupil_left": { "x": 4, "y": -6 },
    "mouth": "small_o"
  },
  "hold_frames": 18,
  "transition": "back.out"
}
```

## 质量检查清单

- 所需情绪均有对应姿势。
- 所需动作均有姿势或循环。
- 复用的循环包含 contact 与 passing 姿势。
- 姿势仅命名变更的部位；默认值来自 rig。

## 参考来源

- 使用 GSAP 时间轴序列实现可读的多步姿势：
  https://gsap.com/docs/v3/GSAP/Timeline/
- Remotion 插值用于基于帧的过渡：
  https://www.remotion.dev/docs/interpolate
- Remotion spring 实现自然运动：
  https://www.remotion.dev/docs/spring
