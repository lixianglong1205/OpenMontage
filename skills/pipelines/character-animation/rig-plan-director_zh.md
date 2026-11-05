# Rig 计划导演 - 角色动画流水线

## 目标

从 `character_design` 生成 `rig_plan` 和 `pose_library`。

## 流程

1. 将每个角色拆分为 rig 部件：
   - 身体（body），
   - 头部（head），
   - 眼睛/瞳孔（eyes/pupils），
   - 眉毛（brows），
   - 嘴型（mouth shapes），
   - 肢体/翅膀（limbs/wings），
   - 尾巴/配饰（tail/accessories），
   - 道具（props）。
2. 为每个可动部件定义枢轴点（pivot）。
3. 定义图层顺序。
4. 定义约束，避免肢体旋转到不可能的位置。
5. 为已通过审核的场景定义命名姿势（named poses）。
6. 仅在动作至少复用两次或对故事核心时才定义动作循环（action cycles）。

## 运行时模式

角色差异是数据。渲染器不应为老鼠与鸟类分别编写一次性代码。鸟类可能有 `wing_left`；老鼠可能有 `tail`，但二者都接入同一套姿势插值与时间轴编译器。

## 质量检查

- 每个可动部件都有枢轴点。
- 每个必需动作都有姿势或程序化策略。
- 每个姿势都标明发生变化的部件。
- 高风险动作应明确标注，不得隐藏。

## 工具使用

使用 `svg_rig_builder` 起草 rig 数据，使用 `pose_library_builder` 起草初始姿势库。代理可在检查点（checkpointing）之前修订其输出。
