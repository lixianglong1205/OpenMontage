# HunyuanVideo 1.5 — 提示词指南

> 来源：[Tencent Prompt Handbook](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md)
> 通用词汇表见：`skills/creative/video-gen-prompting.md`

**字数：** Hunyuan 1.5 在 80–200 词时表现最佳；写 400 词长文并不会带来额外收益。

## HunyuanVideo 提示词公式

### 文生视频（Text-to-Video）
```
Subject + Motion + Scene + [Shot Type] + [Camera Movement] + [Lighting] + [Style] + [Atmosphere]
```

### 图生视频（Image-to-Video）
```
Subject Motion Dynamics + Scene Motion Dynamics + [Camera Movement]
```

I2V 场景下应着重描述**运动**，而非外观（外观由输入图像提供）。

## HunyuanVideo 特有优势

### 以光照营造氛围
腾讯强调：**「光是氛围的灵魂。」**

从多个维度描述光照：
- **风格**：柔和、硬光、霓虹、环境光
- **方向**：侧光、逆光、顶光、底光
- **质感**：强烈聚光、漫射辉光
- **阴影**：拉长且戏剧性的阴影、柔和阴影边缘
- **色温**：黄金时段暖色、冷色日光蓝
- **反射**：湿面反射、金属高光

### 镜头运动词库

| 运动 | 类型 | HunyuanVideo 提示词 |
|----------|------|-------------------|
| Crane / Pedestal | 平移（垂直） | "camera rises vertically" |
| Truck / Tracking | 平移（水平） | "camera tracks left alongside subject" |
| Dolly In | 平移（推） | "camera pushes forward toward subject" |
| Dolly Out | 平移（拉） | "camera pulls back from subject" |
| Pan | 旋转（偏航） | "camera pans right across the scene" |
| Tilt | 旋转（俯仰） | "camera tilts upward to follow the rocket" |
| Roll | 旋转（Z 轴 / 荷兰角） | "camera rolls clockwise into a Dutch tilt" |
| Orbit | 环绕 | "camera orbits around subject" |
| Follow | 锁定跟随 | "camera follows subject from behind" |
| Zoom | 纯镜头（焦距） | "camera slowly zooms in on the figure" |
| Rack focus | 纯镜头（焦平面，快切） | "rack focus from the foreground bottle to the figure in the background" |
| Pull focus | 纯镜头（焦平面，渐变） | "camera shifts focus from foreground X to background Y" |
| Static | 固定 | "static camera, no movement" |

### 动态景深镜头：起止焦平面都要写清

Hunyuan 在焦点变化的镜头里，明确写出起点与终点焦平面时效果更好。说明焦点**从哪里开始**、**最终落在何处**——不要只写一半。

示例："shallow DoF; focus on the foreground bottle at start; focus pulls to the figure in the background by end."

若缺少任一端点，Hunyuan 常会默认深景深，或停留在错误的焦平面上。

### 风格关键词

**写实 / 电影感**：
- Film noir、硬科幻、电影摄影
- 年代剧、战争纪录片、自然纪录片

**动画 / 插画**：
- 2D 动画、日式动漫
- 水彩、中国水墨
- 低多边形 3D、像素风

## I2V 最佳实践

图生视频时，输入图像已定义外观。提示词**只应**描述：
1. 主体如何运动
2. 环境如何变化
3. 镜头运动

**好的 I2V 提示词**："The woman's hair blows in the wind as she turns to face the camera. Leaves scatter across the path. Camera slowly dollies in."

**差的 I2V 提示词**："A beautiful woman in a red dress standing in a forest" —— 这是在重复图像里已有的内容。

### 按时间顺序描述运动

按时间先后写运动；若有多段动作，分开写（例如「先向右摇镜，再向上仰拍」）。Hunyuan 会按提示词中的出现顺序执行运动——把两个动作挤在同一句里，容易导致其中一个被省略或混在一起。

## 示例（T2V）

```
A young woman in a flowing white dress walks barefoot along
a deserted beach at golden hour. She trails her hand through
the shallow surf, leaving ripples. Her hair catches the warm
side-light from the setting sun. Medium tracking shot, camera
follows alongside at knee height. Soft golden lighting with
long shadows stretching toward the camera. Cinematic
photography style, shallow depth of field. Peaceful,
contemplative atmosphere.
```

## 示例（I2V）

```
The cat stretches lazily, then leaps from the windowsill
to the floor. Dust motes scatter in the shaft of light.
Camera remains static, slight rack focus from window to
landing spot.
```
