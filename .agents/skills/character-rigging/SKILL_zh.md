---
name: character-rigging
description: 为本地动画构建数据驱动的 2D 角色绑定：部件、枢轴、图层、约束、视图及可复用绑定包。
license: MIT
---

# 角色绑定

在构建 OpenMontage 的 `rig_plan` 产物或为本地 2D 角色动画准备渲染器输入时使用本技能。

## 成熟模式

- 保持运行时代码通用；将每个角色做成数据包。
- 将角色拆分为可独立变换的部件。
- 在与美术资源相同的坐标空间中定义枢轴。
- 在可动部件上存储约束，以避免不可能的旋转。
- 显式维护图层顺序；生成后不要依赖 SVG 源顺序。
- 先从单一视图开始，仅在镜头表需要时再增加视图。

## 绑定包

```json
{
  "character_id": "mouse",
  "rig_type": "svg_rig",
  "parts": [
    { "id": "body", "kind": "torso", "layer": 10 },
    { "id": "head", "kind": "head", "layer": 30, "parent": "body" },
    { "id": "arm_right", "kind": "limb", "layer": 40, "parent": "body" }
  ],
  "joints": {
    "head": { "pivot": [320, 180], "rotation": [-20, 20] },
    "arm_right": { "pivot": [390, 310], "rotation": [-70, 95] }
  }
}
```

## 质量检查清单

- 每个可动部件都有枢轴。
- 在层级关系重要时，每个子部件都有父部件。
- 口型形状使用独立资源或独立路径组。
- 需要改变视线时，眼睛与瞳孔分开。
- 若角色会接触或携带道具，道具应单独拆分。

## 参考来源

- SVG 的 transform-origin 行为由浏览器定义，可能对坐标空间敏感；使用 GSAP 的
  `svgOrigin` 时优先使用显式的 SVG 坐标枢轴：https://gsap.com/docs/v3/GSAP/CorePlugins/CSS/
- Remotion 动画必须通过当前帧（current frame）实现帧驱动且确定性：
  https://www.remotion.dev/docs/use-current-frame
