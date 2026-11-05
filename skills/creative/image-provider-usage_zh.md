# OpenMontage 图像 Provider 使用指南

> 如何在图像生成与图库 Provider 之间做选择，以及如何高效使用各自能力。
> 本文是对现有 `image-gen-usage.md` 的补充（后者深入讲解 FLUX 提示词）。

## Provider 全景

### 生成类 Provider（AI 生成图像）

| Tool | Provider | 成本 | 速度 | 最佳用途 |
|------|----------|------|-------|----------|
| `flux_image` | FLUX 2 Pro via fal.ai | ~$0.03-0.05 | ~5-10s | 照片级写实、通用场景、主力工具 |
| `grok_image` | Grok Imagine Image (xAI) | $0.02/output + $0.002/input edit image | ~5-15s | 图像编辑、风格迁移、多图合成 |
| `openai_image` | GPT Image 2 (OpenAI) | ~$0.01-0.21 | ~5-15s | 复杂指令、图中文字、多元素场景 |
| `recraft_image` | Recraft V4 via fal.ai | ~$0.04-0.25 | ~5-10s | Logo、SVG 矢量、品牌资产、文字渲染（见下文说明） |
| `local_diffusion` | Stable Diffusion (local) | Free | ~30s+ | 离线、隐私、零成本 |
| `image_gen` | Multi (legacy, deprecated) | Varies | Varies | **已弃用** — 请使用 `image_selector` 或各 Provider 专用工具 |

### 图库类 Provider（搜索并下载已有图像）

| Tool | Provider | 成本 | 速度 | 最佳用途 |
|------|----------|------|-------|----------|
| `pexels_image` | Pexels | Free | ~2-5s | 高质量摄影、按颜色筛选 |
| `pixabay_image` | Pixabay | Free | ~2-5s | 库容大、分类筛选、插画 |

### 选择器

| Tool | 用途 |
|------|---------|
| `image_selector` | 按偏好与可用性路由到最合适的 Provider |

## 按场景类型选择 Provider

| 场景类型 | 首选 Provider | 原因 | 备选 |
|-----------|-----------------|-----|----------|
| **真实世界照片**（城市、自然、人物） | `pexels_image` | 写实场景真实照片优于 AI | `pixabay_image` → `flux_image` |
| **技术示意图** | `diagram_gen` | 结构化、可编辑 | 配合示意图提示词的 `flux_image` |
| **抽象/概念插画** | `flux_image` | AI 擅长定制概念 | `openai_image` |
| **对已有图像做风格迁移/重绘** | `grok_image` | 原生编辑流程，提示词可控变换强 | `openai_image` |
| **多图合并/合成** | `grok_image` | 可将多张源图合成单一场景 | `openai_image` |
| **Logo 或品牌资产** | `recraft_image` | 支持 SVG、文字准确度较高 | `openai_image` |
| **带文字/标签的图像** | `openai_image` | 文字渲染最佳（GPT Image 2） | `recraft_image` |
| **复杂多元素构图** | `openai_image` | 指令遵循最佳 | `flux_image` |
| **主视觉（Hero image）** | `flux_image` | 视觉质量最高 | `openai_image` |
| **缩略图** | `flux_image` 或 `recraft_image` | 需要吸睛 | — |
| **预算/免费项目** | `pexels_image` 或 `pixabay_image` | 免费、即用 | `local_diffusion` |
| **离线/气隙环境** | `local_diffusion` | 无需网络 | — |

## 各 Provider 注意事项

### Recraft V4 via fal.ai
- **`style` 参数会导致 422 错误**（截至 2026-04）。`style` 枚举值（`digital_illustration`、`realistic_image` 等）会被 fal.ai 的 Recraft V4 端点拒绝。**变通：** 把风格方向写进提示词（例如用「牙齿横截面的数字插画」而不是 `style="digital_illustration"`）。`image_size` 与 `colors` 参数可正常使用。
- **精确商业名称的文字渲染不可靠。** Recraft（与所有 AI 图像模型一样）可能生成错误文字。凡要求逐字准确的场景（CTA 画面、商号、电话号码），应使用 Remotion 的 `text_card`，而非生成带文字的图像。

## 成本与质量权衡

```

PRODUCTION PATH: Premium
├── Hero images: flux_image ($0.05/img)
├── Supporting visuals: flux_image ($0.03/img)
├── Text overlays: openai_image ($0.05/img medium)
├── B-roll stills: pexels_image ($0.00)
└── Total for 10 images: ~$0.35

PRODUCTION PATH: Standard
├── All generated: flux_image ($0.03/img)
├── B-roll stills: pexels_image ($0.00)
└── Total for 10 images: ~$0.25

PRODUCTION PATH: Budget
├── All stock: pexels_image + pixabay_image ($0.00)
├── Diagrams: diagram_gen ($0.00)
└── Total: $0.00

PRODUCTION PATH: Offline
├── All generated: local_diffusion ($0.00)
├── Diagrams: diagram_gen ($0.00)
└── Total: $0.00 (but slower, lower quality)
```

当任务从已有图像出发且应仅路由到支持编辑的 Provider 时，使用 `generation_mode="edit"`。

## 使用 Image Selector

多数情况下使用 `image_selector` 让其自动路由：

```python
# The selector finds the best available provider
result = image_selector.execute({
    "prompt": "aerial view of a modern data center",
    "preferred_provider": "auto",  # or "flux", "pexels", etc.
    "output_path": "assets/images/scene-3.png"
})
```

若已明确场景类型对应的最佳 Provider，可用 `preferred_provider` 覆盖。
用 `allowed_providers` 限制为免费或本地选项：

```python
# Budget mode: only free providers
result = image_selector.execute({
    "prompt": "server room interior",
    "allowed_providers": ["pexels", "pixabay", "local_diffusion"],
    "output_path": "assets/images/scene-3.jpg"
})
```

## 混合来源下的一致性

同一视频中混用图库与生成图像时，视觉一致性是主要难点。

### 策略：统一调色
在合成阶段对图库与生成图像都应用 playbook 的调色 LUT，
以统一观感。`color_grade` 增强工具负责此步骤。

### 策略：对齐视觉身份，而非复制前缀
生成图像时，将 playbook 的情绪、色板、质感与媒介
提炼为简短的场景锚点。搜索图库时，按相同的
情绪与视觉特质筛选：色彩、光照、环境、构图、年代与
质感。把 playbook 当作一致性来源，而非整段粘贴的脚本。

### 策略：同一场景内避免混用风格
不要在同一场景里一部分用图库照片、另一部分用 AI 插画。
保持每个场景内部一致——要么全图库，要么全生成。
