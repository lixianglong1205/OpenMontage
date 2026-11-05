# 编辑导演 - 角色动画流水线

## 目标

产出 `edit_decisions` 与 `action_timeline`。

## 流程

1. 从已批准的方案中延续 `render_runtime`。
2. 将场景节拍转换为带时序的角色动作。
3. 在合适处加入预备动作（anticipation）、保持（hold）、动作（action）与收尾跟进（follow-through）。
4. 将口型/手势节拍与对白或音乐对齐。
5. 保持动作密度可读。

## 时序模式

大多数表演节拍需要：

```text
anticipation -> action -> hold/reaction -> settle
```

不要让所有元素持续动画。停顿也是表演的一部分。

## 工具使用

先用 `action_timeline_compiler` 做初稿，若表演或节奏偏弱则修订时间轴。

## 质量标准

每个场景都有带时序的动作。每个动作都对应渲染器能理解的姿势、动作循环或程序化效果。
