# OpenMontage 图像生成用法

> 来源：OpenAI GPT Image 文档、FLUX/BFL API 文档，以及 `.agents/skills/flux-best-practices/` 与 `.agents/skills/bfl-api/` 中的现有 Layer 3 技能

## 速查卡

```
FLUX RESOLUTION:  1920x1088 (16:9) | 1088x1920 (9:16) — must be multiples of 16
MAX TOTAL:        4 megapixels (width x height)
CONSISTENCY:      Use hero image as input_image for subsequent frames
STYLE SYSTEM:     Derive from subject + audience + tone, then adapt per scene
BATCH STRATEGY:   Hero at max quality → iterate with klein → final pass with pro
```

## 视频帧分辨率

所有 FLUX 尺寸**必须是 16 的倍数**。总像素上限为 4MP。

| 目标 | FLUX 分辨率 | 成本（FLUX.2 pro） |
|--------|----------------|-------------------|
| YouTube 16:9 | `1920x1088` | $0.03/image |
| YouTube 4K | `3840x2160` | 需要 pro/max |
| TikTok/Reels 9:16 | `1088x1920` | $0.03/image |
| 方形 1:1 | `1024x1024` | $0.03/image |
| 缩略图 | `1280x720` | $0.03/image |

## 保持视觉一致性

最大难点：让 8–12 张生成图像看起来属于同一支视频。

### 策略 1 — 共享视觉系统（始终使用）

先为项目定义共享视觉系统，再按场景适配。
记录项目的：

- 主导情绪与质感，
- 色板方向，
- 光照倾向，
- 渲染媒介，
- 角色/环境一致性锚点。

playbook 中的 `image_prompt_prefix` 是素材来源，**不要**原样粘贴进每条 prompt。将其提炼为更短、适合该场景的锚点。

### 策略 2 — 主参考图（推荐）

1. 以最高质量生成一张「主图」（hero）（`FLUX.2 [max]`，$0.07）
2. 将其作为后续所有帧的 `input_image`：

```
Frame 1: T2I with detailed prompt → hero.png
Frame 2: I2I with hero.png + "Same style, camera pans right to show..."
Frame 3: I2I with hero.png + "Same style, zoomed in on..."
```

FLUX.2 最多支持 4 张参考（klein）或 8 张参考（pro/max/flex）。按编号引用：「The character from image 1 in the environment from image 2.」

### 策略 3 — 固定 Seed

在 prompt 相近的多轮生成中使用相同 `seed` 参数。构图会较相似，但对 prompt 变动很敏感——仅作补充，勿作主要策略。

## Prompt 构建 — 三段式上下文方法

**不要**把 playbook 的 `image_prompt_prefix` 原样复制进每条 prompt。那样会让所有场景看起来一样。应基于 3 层上下文构建每条 prompt：

### 第 1 部分：场景专属风格方向（来自 shot_language + texture_keywords）

用场景的 `shot_language` 字段设定机位与光照：
```
[SHOT SIZE from shot_language.shot_size, e.g., "medium close-up"].
[LIGHTING from shot_language.lighting_key, e.g., "golden hour warm light"].
[DEPTH from shot_language.depth_of_field, e.g., "shallow depth of field with bokeh"].
[TEXTURE from scene.texture_keywords, e.g., "film grain, warm tones"].
```

若场景没有 shot_language，则使用下方模板。

### 第 2 部分：Playbook 一致性锚点（改编，非逐字）

提取 playbook 视觉语言的**精髓**——不要复制前缀。例如：
- Playbook 写「Clean, minimal illustration with soft shadows, muted color palette」→ 改编为：「muted color palette, soft shadows」
- Playbook 写「Bold flat motion graphics, vibrant gradients」→ 改编为：「vibrant flat style」

锚点让场景视觉连贯，又不会让它们一模一样。

### 第 3 部分：场景描述

场景的实际内容。要具体——用可感知的细节替换空泛用词。

**差：**「A person using a computer in a modern office」
**好：**「Software developer in a dimly lit home office, blue monitor glow reflecting off glasses, desk cluttered with energy drinks and sticky notes」

### 完整 Prompt 示例（含 shot_language）

```
Medium close-up, golden hour warm lighting, shallow depth of field.
Muted earth tones, soft shadows.
Beekeeper in white protective gear lifting a frame dripping with honey,
late afternoon sun catching golden droplets, lavender field blurred
in the background. Film grain, warm amber tones.
16:9 aspect ratio.
```

### 回退模板（无 shot_language 时）

```
[ADAPTED STYLE ANCHOR from playbook — 5-10 words, not the full prefix].
[SCENE DESCRIPTION: specific subject, action, environment].
[LIGHTING: golden hour / overcast / studio softbox / dramatic side-light].
[COMPOSITION: wide shot / medium shot / close-up / overhead / isometric].
[CAMERA: Shot on [camera] with [lens] at [aperture]] (for photorealistic only).
16:9 aspect ratio.
```

### 使用 lib/shot_prompt_builder.py

程序化构建 prompt 时，使用 shot prompt builder，自动实现三段式方法：

```python
from lib.shot_prompt_builder import build_shot_prompt
prompt = build_shot_prompt(scene, style_context=playbook_data)
```

该工具将结构化的 shot_language 字段转为面向图像/视频生成 provider 的自然语言 prompt。

### 按风格的 Prompt 模式

| 风格 | Prompt 模式 |
|-------|---------------|
| **Flat illustration** | "Flat vector illustration, bold colors, clean edges, no gradients, white background" |
| **Isometric** | "Isometric 3D illustration, 30-degree angle, clean geometric shapes, soft shadows" |
| **Photorealistic** | "Photorealistic, shot on Canon EOS R5 with 85mm f/1.4, shallow depth of field" |
| **Diagram-style** | "Technical diagram, labeled components, clean lines, minimal color, white background" |
| **Watercolor** | "Soft watercolor illustration, muted tones, visible brush strokes, paper texture" |

## 批量生成策略

| 阶段 | 模型 | 单张成本 | 用途 |
|-------|-------|-----------|---------|
| 1. 风格指南 | FLUX.2 [max] | $0.07 | 一张主图，最高质量 |
| 2. 分镜迭代 | FLUX.2 [klein] 9B | $0.015 | 规划阶段快速变体 |
| 3. 终稿帧 | FLUX.2 [pro] | $0.03 | 以主图为参考重新生成终稿 |

**速率限制：** 最多 24 个并发请求。请据此编排流水线。

**8 张图解说类视频预算：** $0.07（主图）+ $0.12（8× klein 迭代）+ $0.24（8× pro 终稿）≈ $0.43

## 常见陷阱

1. **图像内文字** — AI 生图对文字不可靠。prompt 中不要要求文字；在 compose 阶段以叠加层添加文字
2. **手与手指** — 图像模型仍易出错。避免需要精细手部姿势的 prompt
3. **角色不一致** — 无参考图时，同一角色每次外观不同。始终使用主图参考策略
4. **Prompt 过长** — 又长又复杂的 prompt 结果难控。控制在 2–3 句
5. **过度统一 prompt** — 每条 prompt 强行塞入完全相同的风格短语会让场景显得雷同。保持视觉系统一致，但让每个场景表达各自的主体、镜头与情绪节拍。

## 在 OpenMontage 中的应用

在 asset 阶段使用 `image_selector` 工具时：

1. **先设计视觉系统**：来自 proposal 或自定义 playbook——情绪、色板、质感、动效能量
2. **优先生成主图**（最高质量），并作为其余图像的参考
3. **16:9 视频帧使用 `1920x1088`**（满足 FLUX 16 倍数要求）
4. **不要在图像中请求文字** — 在 compose 阶段添加文字叠加
5. **预算检查** — 生成前估算图像总成本；超预算则改用本地 diffusers
6. **规划阶段用 klein 迭代，终稿用 pro**
7. **Prompt 保持 2–3 句** — 场景专属机位/光照 + 改编后的视觉锚点 + 具体主体
8. **对齐场景计划** — 每张图对应脚本中的具体场景
