---
name: grok-media
description: xAI Grok 图像与视频生成指南，涵盖认证、端点、提示词结构、图像编辑、参考图视频及异步轮询。
metadata:
  author: OpenMontage
  version: "1.0.0"
  tags: xai, grok, image-generation, video-generation, media
---

# Grok Media

在 OpenMontage 中使用 xAI 媒体模型时，请使用本技能。

## 模型

- `grok-imagine-image`：图像生成与图像编辑
- `grok-imagine-video`：文生视频、图生视频与参考图视频

## 认证

- 环境变量：`XAI_API_KEY`
- Base URL：`https://api.x.ai/v1`
- Header：`Authorization: Bearer $XAI_API_KEY`

## 图像 API

### 文生图

- 端点：`POST /images/generations`
- 核心字段：
  - `model`
  - `prompt`
  - `n`
  - `aspect_ratio`
  - `resolution`

### 图像编辑

- 端点：`POST /images/edits`
- 单张源图使用 `image`
- 多图合成使用 `images`
- 每张源图可以是：
  - 公开 HTTPS URL
  - base64 data URI

### 图像提示词

- Grok 对直接的自然语言描述响应良好
- 编辑时只描述预期变更，其余部分通过省略隐含保留
- 多图合并时，明确说明每张源图的贡献方式
- 优先使用一条清晰的场景描述，而非堆叠冗长风格词

## 视频 API

### 生成

- 端点：`POST /videos/generations`
- 轮询端点：`GET /videos/{request_id}`
- 成功状态：`status == "done"`
- 需显式处理的失败状态：`failed`、`expired`

### 模式

- 文生视频：
  - 仅使用 prompt 生成
- 图生视频：
  - 使用 `image: {"url": ...}`
  - 用于锚定起始帧
- 参考图生视频：
  - 使用 `reference_images: [{"url": ...}, ...]`
  - 影响视频中出现的对象/人物，但不锁定首帧
  - 提示词可用占位符引用输入，如 `<IMAGE_1>`、`<IMAGE_2>`

### 视频约束

- Grok 视频宜按短视频生成对待
- 当前输出分辨率为 `480p` 与 `720p`
- 参考图视频支持多张图片，适用于产品植入、服装迁移与身份一致性
- 请及时下载输出；提供商 URL 可能为临时链接

## 定价

- `grok-imagine-image`：每张生成图像 `$0.02`
- `grok-imagine-image` 编辑/合成：每张输入图像另加 `$0.002`
- `grok-imagine-video`：
  - `480p`：每秒 `$0.05`
  - `720p`：每秒 `$0.07`
- `grok-imagine-video` 带图像条件的请求：每张输入图像另加 `$0.002`

## Grok 专用提示词指南

### 图像

- 从主体、动作、场景入手
- 只加一个风格锚点，不要堆五个
- 编辑时：
  - 描述期望的修改
  - 通过省略保持图像其余部分稳定，而非写冗长的保留清单

### 视频

- 提示词保持场景局部：一个镜头、一个主要运动想法、一个情绪节拍
- 参考图条件视频时，明确将源图映射到角色：
  - 人物来自 `<IMAGE_1>`
  - 夹克来自 `<IMAGE_2>`
  - 产品来自 `<IMAGE_3>`
- 镜头与节奏语言有帮助：
  - slow push-in
  - handheld follow
  - locked-off medium shot
  - high-energy whip pan transition

## 适用场景

- 图像风格迁移
- 多源图像合成
- 参考图条件的短视频
- 以产品为主的动态片段
- 无需硬性锁定首帧的角色一致场景

## 不适用场景

- 长片段生成
- 重度依赖确定性 seed
- 含多次场景切换的过载提示词

## 失败处理

- 若提交生成成功但轮询过期，应作为提供商/运行时问题上报
- 若请求失败，在错误中保留端点、模式与提示词摘要
- 用户已选择 xAI 后，未经用户同意不得静默替换为其他提供商
