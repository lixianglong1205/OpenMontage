# 视频生成提示词 — 通用指南

## 何时使用

在为视频生成工具族（`video_selector`、`seedance_video`、
`heygen_video`、`wan_video`、`hunyuan_video`、`ltx_video_local`、`ltx_video_modal`、
`cogvideo_video`）撰写提示词时使用。本技能涵盖适用于各类视频生成模型的通用提示词词汇。
**首选高端默认**见下表 Seedance 2.0 一行。

模型专属技巧见下方链接指南。

## 模型专属指南

| 模型 | 指南 | 关键要点 |
|-------|-------|-------------|
| **Seedance 2.0（标准 / 快速）** | `creative/prompting/seedance-prompting.md` + Layer 3 `.agents/skills/seedance-2-0/` | 配置 `FAL_KEY` 或 HeyGen 时的**首选高端默认**。单次生成同步音频、多镜头、导演级运镜、引号对白唇形同步、参考图生视频（9 图 + 3 视频 + 3 音频）。Elo 1269（Artificial Analysis 榜首）。 |
| **Sora 2 / Sora 2 Pro** | [OpenAI Sora 2 Cookbook](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide) | 结构最丰富的模板。高级字段：镜头、滤光、调色、画内音、服装、成片风格。 |
| **VEO 3.1 / VEO 3** | [Vertex AI Prompt Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide) | 最佳词汇参考表。14 组件提示结构。 |
| **Grok Imagine Video** | `creative/prompting/grok-prompting.md` | 提示需参考图占位符如 `<IMAGE_1>` 及身份/产品延续时首选。 |
| **LTX-2** | [LTX Prompting Guide](https://docs.ltx.video/api-documentation/prompting-guide) | 六要素结构。音频/人声提示。强「应避免」章节。 |
| **HunyuanVideo 1.5** | [Tencent Prompt Handbook](https://github.com/Tencent-Hunyuan/HunyuanVideo-1.5/blob/main/assets/HunyuanVideo_1_5_Prompt_Handbook_EN.md) | 公式：主体 + 运动 + 场景 + [镜头] + [摄影机] + [光照] + [风格] + [氛围]。 |
| **Runway Gen-4** | [Runway Prompting Guide](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide) | 「聚焦运动，而非外观。」每段一个场景。简洁取胜。 |
| **Kling 2.6** | [Kling Prompt Guide](https://fal.ai/learn/devs/kling-2-6-pro-prompt-guide) | 四段结构。支持 `++emphasis++` 语法强调关键元素。 |
| **Kling Official** | Layer 3 `.agents/skills/kling-official/` | 官方 API 直连。用 `provider="kling_official"` 与 fal.ai Kling 区分。`api_family` 选 Classic、Turbo 或 Omni；Turbo 图生视频需 URL 参考图。 |
| **Wan 2.1 / CogVideoX** | 使用本通用指南 | 无官方提示指南。标准电影摄影词汇效果良好。 |

## 顺序很重要

列举多个主体或事件时：

- **时间顺序**：事件随时间展开时（「先 X 进入，再 Y 反应」）。
- **突出度顺序**：与时间无关时 — 人先于物，最大/最居中主体优先，再写次要主体。

## 自包含提示词

> 提示词应让从未看过目标成片的人，仅凭文字就能想象主体、场景、运动与运镜。若读者无法想象，生成模型也无法正确渲染。

## 通用提示词公式

既有研究（CMU/Harvard，《Building a Precise Video Language with Human-AI Oversight》）表明，视觉语言模型可靠描述主体与场景，但在运动、空间与摄影机方面易失败。**强制提示填满五个槽位是杠杆最高的改动。**

OpenMontage 规范五要素骨架：

```
[Subject]        type + key visual attributes + how to disambiguate when multiple
[Subject Motion] actions in temporal order; subject↔object and subject↔subject interactions; group action
[Scene]          overlays (separately!) + POV + setting + time of day + scene dynamics
[Spatial]        shot size + position-in-frame + depth (FG/MG/BG) + camera-height-relative
                 — and how those CHANGE during the clip
[Camera]         playback speed → lens distortion → height → angle → focus/DoF → steadiness → movement
```

**更短提示 = 更大创作自由度。更长提示 = 更强控制。**

### 各模型提示长度

论文第 6 节经验最优区间 — 不同模型对提示密度回报不同：

| 模型 | 最优区间 | 说明 |
|---|---|---|
| Seedance 2.0 | 主镜头 200–400 词，插入镜头 80–150 | 适合长而结构化的五要素提示 |
| Wan 2.2 | 200–400 词 | 针对长 caption 微调 |
| Sora 2 / VEO 3.1 | 100–250 词 | 约 250 词后收益趋平 |
| LTX-2 | ≤ 80 词 | 更长会劣化，保持紧凑 |
| Runway Gen-4 | ≤ 60 词 | 「聚焦运动，而非外观」 |

### 叠加层不是场景景深

> 叠加层（标题、HUD、字幕、水印、画框图形）不属于场景前景/中景/背景景深轴。单独列出内容与位置。勿写「叠加层在前景」。

---

## 摄影机景别

| 景别 | 适用场景 |
|------|-------------|
| **Wide / establishing shot** | 开场、交代地点 |
| **Full / long shot** | 主体全身入画并带环境 |
| **Medium shot** | 腰上，细节与语境平衡 |
| **Medium close-up** | 胸上，对话亲密感 |
| **Close-up** | 面部或关键物体，强调情绪 |
| **Extreme close-up** | 孤立细节（眼、水滴、纹理） |
| **Over-the-shoulder** | 对话构图、关联感 |
| **Point-of-view (POV)** | 观众代入角色 |
| **Bird's-eye / top-down** | 地图式俯瞰、全知感 |
| **Worm's-eye view** | 仰视，强调高度 |
| **Dutch / canted angle** | 倾斜地平线，不安或张力 |
| **Low-angle** | 主体显强大、主导 |
| **High-angle** | 主体显渺小、脆弱 |

## 摄影机运动

论文指出当前模型易混淆平移、旋转与纯镜头变化 — 提示中分组以免混为一谈：

| 组别 | 基本动作 | 规则 |
|---|---|---|
| **Translation**（摄影机物理移动） | dolly in/out, truck left/right, pedestal up/down | 「dolly forward toward subject」 |
| **Rotation**（原地 pivot） | pan left/right, tilt up/down, roll CW/CCW | 「pan right across the room」 |
| **Lens-only**（无摄影机位移） | zoom in/out, rack focus, pull focus, focus tracking | 「zoom in」≠「dolly in」 |
| **Hybrid / signature** | dolly zoom (vertigo), arc/orbit, crane, whip pan, tracking/follow, handheld | 「vertigo」仅用于揭示时刻 |
| **Stillness states** | static（完全无运动 — 严格）, micro-shake, locked-off | 「static」要求零运动、零焦点变化、零变焦 |

> **dolly ≠ zoom。** dolly 是摄影机平移；zoom 是焦距变化。模型跟随占主导的 token。**pan ≠ truck。** pan 是旋转，truck 是横向平移。

> **固定镜头很严格。** 固定镜头零运动、零焦点变化、零变焦。若任一项发生，勿写「static camera」— 选用正确的运动基本动作。

## 摄影机高度（相对地面）

| 基本动作 | 示例 |
|---|---|
| Aerial-level | 「drone-altitude wide of the city」 |
| Overhead-level | 「rooftop height looking across the street」 |
| Eye-level | 「framed at eye level」 |
| Hip-level | 「hip-height tracking shot」 |
| Ground-level | 「low to the ground, ankle height」 |
| Water-level | 「skimming the water surface」 |
| Underwater | 「submerged below the surface」 |

## 摄影机角度（相对主体）

| 基本动作 | 定义 |
|---|---|
| **Bird's-eye** | 严格正俯视。不同于 aerial。 |
| High angle | 俯视主体 |
| Level angle | 摄影机与主体同高 |
| Low angle | 仰视主体 |
| Worm's-eye | 直线向上看 |
| **Dutch angle (fixed)** | 倾斜地平线保持不动 |
| **Dutch angle (rolling)** | 拍摄中地平线倾角变化 |

> **bird's-eye = 严格正俯视。aerial = 高度。** 无人机 45° 俯视是高角度 + 空中高度，不是 bird's-eye。

## 视点 (POV)

| POV | 示例 |
|---|---|
| First-person | 「the camera follows the character's viewpoint as they walk」 |
| Drone | 「aerial drone footage of city skyline」 |
| Over-the-shoulder | 「OTS framing of the laptop screen」 |
| Top-down oblique | 「top-down view of the chess board, tilted slightly」 |
| Dashcam | 「vehicle dashcam framing of the road」 |
| Objective / Neutral | （默认 — 无特定 POV 时使用） |

## 光照词汇

| 术语 | 效果 |
|------|--------|
| **Natural light** | 柔和、写实（晨光、阴天、月光） |
| **Golden hour** | 暖阳光、长影、浪漫 |
| **High-key** | 明亮均匀、轻快 — 喜剧、生活方式 |
| **Low-key** | 暗部、高对比 — 惊悚、剧情 |
| **Rembrandt** | 颊部三角光，经典肖像 |
| **Film noir** | 深影、强高光 |
| **Volumetric** | 大气中可见光路（雾、尘） |
| **Backlighting** | 主体背后光，剪影感 |
| **Side lighting** | 强方向光，戏剧性阴影 |
| **Practical lights** | 画内光源（灯、蜡烛、霓虹） |
| **Rim / edge light** | 勾轮廓，与背景分离 |

**光照方向修饰**：key light、fill light、bounce、rim、spill、negative fill。

**色温**：暖（钨丝、琥珀）、冷（日光、蓝）、混合。

## 镜头与光学效果

| 效果 | 结果 |
|--------|--------|
| **Wide-angle lens** (24-35mm) | 更广视野、透视 exaggeration |
| **Telephoto** (85mm+) | 压缩透视、主体隔离 |
| **Anamorphic** | 拉伸画幅、标志性镜头光晕 |
| **Lens flare** | 强光入镜产生的条纹 |

### 镜头畸变

论文区分两种模型会分别响应的基本动作 — 不可互换：

| 基本动作 | 效果 |
|---|---|
| **Fisheye** | 极端弯曲，边缘强烈外凸 |
| **Barrel** | 轻度畸变，直线略向外弯 |

### 焦点 / 景深

| 基本动作 | 定义 |
|---|---|
| Deep focus | 全清晰，前景至背景 |
| Shallow DoF | 主体 sharp，背景 bokeh |
| Extremely shallow DoF | 极薄焦平面 |
| Rack focus | 拍摄中焦点在两主体间切换 |
| Pull focus | 渐变焦点（比 rack 慢） |
| Focus tracking | 焦点跟随移动主体 |

景深在镜头内变化时，标注起点与终点焦平面（FG/MG/BG/out-of-focus）。

## 主体过渡

主体入画、出画或交接焦点时，明确命名过渡类型：

| 基本动作 | 时机 |
|---|---|
| **Subject revealing** | 新主体入画（主体运动或摄影机运动） |
| **Subject disappearing** | 主体出画 |
| **Subject switching** | 焦点从一主体切到另一（常经 rack focus 或运镜） |
| **Complex alternating** | 多主体多次交替焦点 |

始终写明原因：「by subject movement」或「by camera movement」。多镜头提示中可解锁 reveal 式运镜。

## 多镜头提示中的身份锚定

> 模型在切镜间会丢失角色身份，除非反复重述。多镜头提示的每一镜中，对每个命名主体 verbatim 重复相同的 3–6 条消歧视觉属性。代词与「同一角色」无效。
>
> 示例：「Aang — bald, blue arrow tattoo on forehead, orange-and-yellow robes — plants his staff. … Aang — bald, blue arrow tattoo on forehead, orange-and-yellow robes — turns to camera.」

## 风格与美学参考

### 电影风格
- Film noir、时代剧、惊悚、现代爱情
- 纪录片、艺术片、实验电影
- 史诗太空歌剧、奇幻、恐怖片
- 1970 年代爱情剧、90 年代纪录片风

### 动画风格
- 吉卜力 / 日式 anime
- 经典 Disney、Pixar 式 3D
- 定格、黏土动画
- 手绘 2D/3D 混合
- Cel-shaded、low-poly 3D

### 艺术流派
- 印象派、超现实、Art Deco、包豪斯
- 水彩、炭笔素描、水墨
- 图像小说、蓝图 schematic

### 胶片 / 调色
- Kodak 暖调、Fuji 冷调
- 16mm 黑白、35mm  photochemical 对比
- 复古颗粒叠加、高光 halation
- Teal-and-orange 调色

## 时间效果

### 播放速度

论文定义六种显式播放速度基本动作。选对词 — 非同义：

| 基本动作 | 定义 |
|---|---|
| Time-lapse | 明显快于实时（云疾走） |
| Fast-motion | 略快于实时（1x–3x） |
| Slow-motion | 慢于实时 |
| Stop-motion | 逐帧离散运动 |
| Speed-ramp | 同镜头内快慢混合 |
| Time-reversed | 倒放 |

### 其他时间手法

| 效果 | 用途 |
|--------|-----|
| **Freeze-frame** | 戏剧性停顿 |
| **Rapid cuts** | 能量、紧迫 |
| **Continuous / long take** | 沉浸、张力 |
| **Fade in / fade out** | 场景过渡 |
| **Match cut** | 场景间视觉连续 |

## 音频描述

支持音频生成的模型（LTX-2、Sora 2、VEO 3）可响应：

**Ambient**：风、雨、交通、人群 murmur、林间鸟、机械 hum
**Diegetic sound**：脚步、门吱呀、碰杯、键盘
**Voice style**：低语、平静旁白、活力 announcer、 gravitas
**Music mood**：「soft piano in background」、「upbeat electronic」

对白用引号：`Character says: "Hello world."`

## 应避免

> **用情绪的视觉成因替代情绪形容词。**
> - 「sad character」→「tears on cheek, shoulders slumped, staring at empty chair」
> - 「cinematic mood」→「low-key Rembrandt key + 35mm anamorphic + crushed shadows, lifted-by-2-stops shadow detail」
> - 「epic」→「low-angle, 24mm wide, sun directly behind subject, lens flare on the rim」
>
> 「Inspiring」「powerful」「moody」「epic」无法约束像素。

> **固定镜头很严格。** 固定镜头零运动、零焦点变化、零变焦。若任一项发生，勿写「static camera」— 选用正确的运动基本动作。

| 不要 | 原因 | 改为 |
|-------|-----|-----------|
| 「Beautiful scene」 | 过 vague，无视觉信息 | 「Wet cobblestone street, warm streetlamp glow reflecting in puddles」 |
| 「Person moves quickly」 | 无可见动作 | 「Woman sprints three steps and vaults over the railing」 |
| 「Cinematic look」 | 各模型已在尝试 | 写明：「anamorphic lens, shallow DOF, golden hour lighting」 |
| 「Sad character」 | 内心状态不可见 | 「Tears on cheek, shoulders slumped, staring at empty chair」 |
| 可读文字 / logo | 模型渲染文字不可靠 | 避免带字招牌，或接受 imperfect 渲染 |
| 复杂物理 | 混沌运动易 artifact | 物理从简；跳舞/走路 OK，爆炸 risky |
| 多人同时说话 | 多人对白 sync 易崩 | 每段一个说话者，或用反应镜头 |
| 提示过载 | 元素过多 = 不 coherent | 从简开始，每次加一层 |
| 光照冲突 | 「Bright noon」+「dark shadows」 | 选定一套光照并贯彻 |

## 提示迭代策略

1. **从简开始** — 主体 + 动作 + 场景。看模型给出什么。
2. **每次加一个元素** — 摄影机，再光照，再风格。
3. **镜头失败时** — 做减法。固定摄影机、简化动作、重试。
4. **多段一致性** — 重复相同风格/光照/调色描述。
5. **使用 seed** — 好结果时保存 seed 做变体。
6. **Grok 参考图视频** — 在提示中用 `<IMAGE_1>`、`<IMAGE_2>` 等为每张源图指定清晰角色。

## 示例：通用提示模板

```
[Shot]: Medium close-up, slight low angle
[Camera]: Slow dolly-in
[Subject]: A weathered fisherman in his 60s, salt-and-pepper beard,
           dark wool sweater, calloused hands gripping a rope
[Action]: He pulls the rope hand-over-hand, muscles straining,
          then pauses and looks out to sea
[Setting]: Wooden dock at dawn, calm grey ocean, distant fog bank,
           seagulls wheeling overhead
[Lighting]: Soft overcast with warm break in clouds on the horizon,
            gentle rim light from the rising sun
[Style]: Documentary cinematography, 35mm film grain,
         muted earth tones with a cold blue-grey palette
[Audio]: Rope creaking, water lapping, distant gull cries, wind
```
