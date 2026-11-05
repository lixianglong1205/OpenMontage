# 资产总监 — 角色动画流水线

## 目标

产出包含角色部件、背景、道具、音频、音乐及预览制品的 `asset_manifest`。

## 第三层技能门控

在编写或生成动画资产之前，请阅读相关的第三层（Layer 3）技能：

- `character-rigging`
- `svg-character-animation`
- `pose-library-design`
- 使用 p5/canvas 特效时阅读 `canvas-procedural-animation`
- 审查前阅读 `character-animation-qa`
- 进行 GSAP/Remotion 工作时阅读 `gsap-core`、`gsap-timeline` 和 `gsap-react`
- 进行 Remotion 渲染工作时阅读 `remotion` 和 `remotion-best-practices`
- 进行 HyperFrames 工作时阅读 `hyperframes` 和 `hyperframes-cli`

在进行图像/TTS/音乐生成之前，请从注册表中阅读该工具的 `agent_skills`。

## 资产组织

将角色资产写入以下路径：

```text
projects/<project-name>/assets/characters/<character-id>/
```

使用以下子文件夹：

```text
parts/
poses/
previews/
```

生成的背景存放于：

```text
projects/<project-name>/assets/backgrounds/
```

## 流程

1. 仅制作或获取 `rig_plan` 所需的部件。
2. 每个可动部件保持独立。
3. 部件保留透明背景。
4. 记录提示词、随机种子、提供商及模型名称。
5. 在全面扩展资产前先构建小型预览。

## 质量门槛

在合成（compose）之前，`rig_plan` 引用的所有部件必须已存在。缺失部件属于阻塞项，除非动作时间线已移除需要该部件的动作。

---

## 门控提醒（具约束力）

本阶段以人工批准为门控（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` 创建检查点，展示摘要（Backlot 看板会渲染该制品），并 **结束本轮**。不要在同一回复中启动下一阶段。
批准按门控逐项生效 — 先前说的「继续」不涵盖本门控。
