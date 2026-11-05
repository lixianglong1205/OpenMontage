# OpenMontage 背景移除用法

> 来源：rembg 库文档、U2Net 论文（Qin 等，2020）、IS-Net 论文（Qin 等，2022）、OpenMontage `tools/bg_remove.py` 实现

## 速查卡

```
DEFAULT MODEL:    u2net (general purpose, fast)
FOR PEOPLE:       u2net_human_seg (optimized for human silhouettes)
FINE EDGES:       Enable alpha_matting (hair, fur, leaves)
OUTPUT:           Transparent PNG by default; set bg_color for solid replacement
RUNTIME:          ~1-3s per image (CPU), <0.5s (GPU with onnxruntime-gpu)
INSTALL:          pip install rembg (CPU) | pip install rembg[gpu] (CUDA)
```

## 何时使用 bg_remove

背景移除是 **资产预处理（asset-prep）** 步骤，应在合成（compose）阶段之前使用。

- **产品演示 / 电商视频** — 将产品隔离在干净背景上
- **合成** — 将讲者叠放在生成背景或图表之上
- **缩略图生成** — 为 YouTube 缩略图制作干净抠图
- **绿幕替换** — 无需真实绿幕即可实现绿幕效果
- **B-roll 准备** — 清理原始照片以供叠加使用

## 模型选择指南

| 模型 | 适用场景 | 速度 | 说明 |
|-------|----------|-------|-------|
| `u2net` | 通用物体、产品、场景 | 快 | 默认；综合表现好 |
| `u2net_human_seg` | 人物、肖像、讲者 | 快 | 人体轮廓遮罩更准确 |
| `isnet-general-use` | 复杂边缘、头发、毛发 | 较慢 | 精细边界细节更高 |

**决策规则：** 若主体是人，使用 `u2net_human_seg`。若主体有复杂边缘（头发、毛发、 foliage）且需要最高质量，使用 `isnet-general-use`。否则使用默认 `u2net`。

## Alpha 抠图（Alpha Matting）

Alpha 抠图通过在边界处计算柔和透明度来精修边缘遮罩，边缘更自然，但处理时间大约增加 2 倍。

| 主体类型 | Alpha 抠图 | 原因 |
|-------------|---------------|--------|
| 头发、毛发、羽毛 | 启用 | 半透明细缕需要柔和边缘 |
| 树叶、树木、草 | 启用 | 不规则有机边界受益于抠图 |
| 产品、设备 | 禁用 | 几何边缘清晰；抠图无额外收益 |
| 文字、Logo、形状 | 禁用 | 硬边对这些主体是正确的 |

## 常见工作流

### 1. 合成用讲者抠图

从背景中提取讲者，叠放在图表或幻灯片上。

```
bg_remove(input_path="speaker.png", model="u2net_human_seg")
  --> speaker_nobg.png (transparent)
  --> compose over diagram/slide in compose stage
```

### 2. 产品隔离

隔离产品，并可选择放在品牌色背景上。

```
bg_remove(input_path="product.jpg", model="u2net")
  --> product_nobg.png (transparent)

# Or with brand background:
bg_remove(input_path="product.jpg", model="u2net", bg_color="#FFFFFF")
  --> product_nobg.png (white background)
```

### 3. 缩略图准备

移除背景、放大，再在合成阶段叠加文字。

```
bg_remove(input_path="subject.png", model="u2net_human_seg", alpha_matting=True)
  --> subject_nobg.png
  --> upscale --> compose with text overlays in compose stage
```

### 4. 批量帧处理

为合成序列准备多帧时，在进入 compose 阶段前处理所有源帧。

```
for each source frame:
    bg_remove(input_path=frame, model="u2net_human_seg")
    --> frame_nobg.png
then: compose all transparent frames over background sequence
```

## 质量检查清单

进入 compose 阶段前，请逐项核对每次 `bg_remove` 输出：

- [ ] **边缘质量干净** — 主体周围无光晕伪影
- [ ] **细节保留** — 头发、手指等细部完整
- [ ] **透明完整** — 透明区域无残留背景渗色
- [ ] **主体完整** — 未误删主体部分
- [ ] **合成测试** — 叠在目标背景上时主体融合自然

## 在 OpenMontage 中的应用

在资产准备阶段使用 `bg_remove` 工具时：

1. **含人物的帧一律用 `u2net_human_seg`** — 比通用模型在人体轮廓上遮罩更紧
2. **仅对复杂边缘主体启用 `alpha_matting`**（如头发、毛发、 foliage）— 清晰边缘主体可跳过以节省时间
3. **合成工作流输出透明 PNG**（省略 `bg_color`），在 compose 阶段叠加 — 保留最大灵活性
4. **纯色背景替换时设置 `bg_color`**，与 playbook 背景色 token 一致 — 输出与项目风格统一
5. **在 compose 阶段之前处理源帧** — bg_remove 是资产预处理，不是 compose 时操作
6. **合成前以全分辨率检查输出边缘** — 光晕与边缘渗色在成片中可见，需尽早发现
