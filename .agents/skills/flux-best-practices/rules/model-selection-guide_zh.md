---
name: model-selection-guide
description: 如何为你的用例选择合适的 FLUX 模型
---

# FLUX 模型选择指南

根据你的需求选择最优 FLUX 模型的决策指南。

## 快速决策矩阵

| 优先级   | 推荐模型                        |
| -------- | ------------------------------- |
| 速度     | FLUX.2 [klein]                  |
| 质量     | FLUX.2 [max]                    |
| 平衡     | FLUX.2 [pro]                    |
| 排版     | FLUX.2 [flex]                   |
| 图像编辑 | FLUX.2 [klein]、[pro] 或 [max] |
| 本地/免费 | FLUX.2 [dev]                    |
| 局部重绘 | FLUX.1 Fill                     |

## 决策树

```
What's your primary need?

├─ Generate images (text-to-image OR image editing)
│   ├─ Need FASTEST possible generation?
│   │   └─ FLUX.2 [klein] (supports up to 4 reference images)
│   │
│   ├─ Need HIGHEST quality output?
│   │   └─ FLUX.2 [max] (supports up to 8-10 reference images)
│   │
│   ├─ Need TEXT/TYPOGRAPHY in image?
│   │   └─ FLUX.2 [flex] (supports up to 8 reference images)
│   │
│   ├─ Need BALANCED speed/quality?
│   │   └─ FLUX.2 [pro] (supports up to 8 reference images)
│   │
│   └─ Need LOCAL/FREE generation?
│       └─ FLUX.2 [dev]
│
├─ Need REAL-TIME web information?
│   └─ FLUX.2 [max] (grounding search)
│
└─ FLUX.1 family (only use when explicitly asked by user)
    ├─ FLUX.1 Kontext - context-aware editing
    └─ FLUX.1 Fill - inpainting/object removal
```

**注意：** 所有 FLUX.2 模型均原生支持通过参考图进行 image-to-image 编辑。只需提供源图作为参考，并描述期望的改动即可。

## 详细模型对比

### 按速度

| 模型              | 相对速度 | 最适合                  |
| ----------------- | -------- | ----------------------- |
| FLUX.2 [klein] 4B | 最快     | 快速原型验证            |
| FLUX.2 [klein] 9B | 很快     | 更高质量的预览          |
| FLUX.2 [pro]      | 中等     | 生产工作流              |
| FLUX.2 [flex]     | 中等     | 排版相关任务            |
| FLUX.2 [max]      | 较慢     | 最终主视觉图            |

### 按质量

| 模型              | 质量等级     | 权衡                       |
| ----------------- | ------------ | -------------------------- |
| FLUX.2 [max]      | 最高         | 最慢、成本最高             |
| FLUX.2 [pro]      | 高           | 良好平衡                   |
| FLUX.2 [flex]     | 高（文字）   | 专为排版优化               |
| FLUX.2 [klein] 9B | 良好         | 快，细节略少               |
| FLUX.2 [klein] 4B | 中等         | 最快，预览级质量           |

### 按成本

> **Credit 定价：** 1 credit = $0.01 USD。FLUX.2 采用按百万像素（megapixel）计价。

#### FLUX.2 模型

| 模型              | 首 MP | +MP  | 1MP T2I | 1MP I2I | 批量场景建议                |
| ----------------- | ----- | ---- | ------- | ------- | --------------------------- |
| FLUX.2 [klein] 4B | 1.4c  | 0.1c | $0.014  | $0.015  | 高批量、预览                |
| FLUX.2 [klein] 9B | 1.5c  | 0.2c | $0.015  | $0.017  | 高批量、更好质量            |
| FLUX.2 [pro]      | 3c    | 1.5c | $0.03   | $0.045  | 生产负载                    |
| FLUX.2 [max]      | 7c    | 3c   | $0.07   | $0.10   | 主视觉图、高端内容          |
| FLUX.2 [flex]     | 5c    | 5c   | $0.05   | $0.10   | 排版                        |
| FLUX.2 [dev]      | -     | -    | Free    | Free    | 本地开发（非商业）          |

> **定价公式：** `(firstMP + (outputMP-1) * mpPrice) + (inputMP * mpPrice)`（单位：美分）

#### FLUX.1 模型

| 模型                 | 单张价格 | 用例                    |
| -------------------- | -------- | ----------------------- |
| FLUX.1 Kontext [pro] | $0.04    | 上下文感知编辑          |
| FLUX.1 Kontext [max] | $0.08    | 最高质量编辑            |
| FLUX1.1 [pro]        | $0.04    | 标准 T2I                |
| FLUX1.1 [pro] Ultra  | $0.06    | 超高分辨率              |
| FLUX1.1 [pro] Raw    | $0.06    | 纪实摄影风格            |
| FLUX.1 Fill [pro]    | $0.05    | 局部重绘（Inpainting）  |
| FLUX.1 [pro]         | $0.05    | 原版 pro 模型           |

> 不同分辨率下的精确费用请使用 [bfl.ai/pricing](https://bfl.ai/pricing) 计算器。

## 用例推荐

### 创意探索 / 构思

**推荐：FLUX.2 [klein]**

- 快速迭代
- 概念快速验证
- 情绪板生成
- 探索 prompt 变体

### 生产级营销素材

**推荐：FLUX.2 [pro]**

- 质量稳定
- 速度合理
- 规模化成本可控
- 适合自动化流水线

### 主视觉图 / 高端内容

**推荐：FLUX.2 [max]**

- 细节最多
- 一致性最佳
- 支持 grounding search
- 关键视觉值得溢价

### 排版 / 标识 / 海报

**推荐：FLUX.2 [flex]**

- 文字渲染更优
- 质量参数可调
- 最适合可读文字
- UI mockup 与信息图

### 角色一致性

**推荐：FLUX.2 [max] 或 [pro]**

- 多参考图支持（最多 8–10 张）
- 编辑一致性最佳
- 跨场景保持身份
- 质量优于 FLUX.1 Kontext

### 照片编辑 / 修图

**推荐：FLUX.2 [klein]、[pro] 或 [max]**

- 通过参考图原生支持 image-to-image
- 风格迁移
- 物体修改
- 属性变更
- 效果优于 FLUX.1 Kontext

### 实时信息

**推荐：FLUX.2 [max]**

- grounding search 功能
- 时事
- 近期新闻可视化
- 天气/位置数据

### 本地开发 / 测试

**推荐：FLUX.2 [dev]**

- 无 API 费用
- 完全可控
- 微调实验
- 可离线使用

### 带排版的编辑内容

```
1. FLUX.2 [max] - Generate base image (highest quality)
2. FLUX.2 [flex] - Add text overlay pass
```

### 角色一致系列

```
1. FLUX.2 [max] - Create character reference
2. FLUX.2 [max]/[pro] - Generate consistent variations using reference images
3. FLUX.2 [klein] - Quick iteration on variations if needed
```

### 电商产品流水线

```
1. FLUX.2 [pro] - Bulk product generations
2. FLUX.2 [pro]/[klein] - Product variations (colors, angles) using references
3. FLUX.2 [flex] - Add promotional text/pricing
```

## 基于约束的选择

### 预算有限

- **高批量**：FLUX.2 [klein] 4B
- **需要质量**：FLUX.2 [pro]（性价比最佳）

### 时间紧

- **任意任务**：FLUX.2 [klein]
- **质量重要**：FLUX.2 [pro]

### 必须最高质量

- **始终**：FLUX.2 [max]

### 文字必须可读

- **始终**：FLUX.2 [flex]

### 编辑现有图像

- **快速编辑**：FLUX.2 [klein] + 参考图
- **质量编辑**：FLUX.2 [max] 或 [pro] + 参考图
- **备选**：FLUX.1 Kontext（更推荐 FLUX.2）

### 速率限制敏感

- **优先**：FLUX.2 模型（24 路并发上限）
- **避免**：FLUX.1 Kontext Max（6 路并发上限）

## 摘要速查

```
Speed?      → FLUX.2 [klein]
Quality?    → FLUX.2 [max]
Balance?    → FLUX.2 [pro]
Text?       → FLUX.2 [flex]
Edit?       → FLUX.2 [klein/pro/max] with reference images
Free?       → FLUX.2 [dev]
```

**要点：** 所有 FLUX.2 模型均通过参考图原生支持图像编辑。编辑任务推荐 FLUX.2，而非 FLUX.1 Kontext。
