# Seedance 2.0 — 提示词指南

> Layer 3 权威文档：`.agents/skills/seedance-2-0/SKILL.md`
> 通用词汇表见：`skills/creative/video-gen-prompting.md`

## 何时选用 Seedance 2.0

Seedance 2.0（字节跳动 Seed 团队，2026 年 2 月发布）在已配置付费网关（通过 `seedance_video` 的 `FAL_KEY`，或 HeyGen Video Agent / Avatar Shots）时，是 OpenMontage 在**电影感预告片、 teaser、 hype 剪辑与动效主导短片**上的**首选高级默认模型**。它是当前模型阵容中唯一同时提供以下全部能力的：

- 单次生成原生同步音频（对白 + 音效 + 环境声一体，而非后期对齐），
- 在单条提示词内多镜头生成，
- 导演级镜头控制，
- 由引号对白驱动的口型同步，
- 参考条件生成（最多 9 张图 + 3 段视频 + 3 段音频），
- 跨镜头角色身份一致。

发布时在 Artificial Analysis 上 Elo 1269 — 领先 Veo 3、Sora 2、Runway Gen-4.5。

仅在确有理由时再换用其他模型：严格预算（用 `fast` 变体或 LTX）、用户明确偏好（VEO/Sora/Kling），或某风格更适合其他模型（VEO 偏写实风景，Kling 偏动漫）。

## Seedance 2.0 八要素提示结构

Seedance 对镜头语言、多镜头切分与引号对白极为「字面」执行。采用以下结构 — 按需包含，不必全写：

1. **镜头 / 景别** — 大全景建立、中景、特写、荷兰角等
2. **镜头运动** — 固定、慢推、航拍、手持、弧线、推拉变焦
3. **主体描述** — 必须在各镜头间保持的物理细节（身份锚点）
4. **动作节拍** — 一句一个节拍；多镜头用 `→` 或明确的 `Shot 1 / Shot 2`
5. **场景 / 环境** — 地点、时代、天气、时段
6. **光线 / 调色** — 一种光线思路，选定并贯彻
7. **风格 / 调色 / 时代** — 如「变形宽银幕镜头、青橙调色、35mm 胶片颗粒」
8. **音频** — 环境、画内声、音乐方向（仅质感描述）、用于口型同步的引号对白

## Seedance 特有优势

| 能力 | 如何调用 |
|---|---|
| **原生同步音频** | 在提示词中描述声场。保持 `generate_audio=true`。 |
| **单次生成多镜头** | 使用 `Shot 1 (...)`、`Shot 2 (...)` 等。各镜头主体描述保持一致。 |
| **导演级镜头** | 用无歧义术语：`slow dolly-in`、`arc shot`、`Dutch tilt`、`aerial push-in`、`handheld with micro-shake` |
| **引号对白口型同步** | `Character says: "台词。"` — 快切时每句约 ≤ 6 个词 |
| **参考生视频** | 使用 `reference-to-video` 端点；在提示词中命名各素材（`Reference 1: hero character — ...`） |
| **角色身份一致** | 每个镜头重复相同物理细节 — Seedance 将其作为身份锚点 |

## 多镜头模式

> **每个镜头逐字重复身份描述。**「同一角色」/ 代词 /「又是 Aang」无效。在每个镜头块中逐字重复 3–6 条可区分的视觉属性。Seedance 会把每个镜头当作你「从零说起」。

Seedance 支持明确的镜头列表：

```
Shot 1 (wide aerial establishing, slow push-in):
Snow-covered Air Temple at dawn, spires catching first orange light.
Wind lifting prayer flags.

Shot 2 (medium, low angle, handheld):
Aang — bald, blue arrow tattoo, orange robes — plants his staff on stone.
He squints into the rising sun.

Shot 3 (extreme close-up, rack focus):
Rack focus from the glowing arrow tattoo on his forehead to the distant peaks.
Aang says: "It's time."

Style: anamorphic lens, teal-orange cinematic grade, 35mm film grain.
Audio: rising orchestral swell with low taiko pulse, wind, distant wingbeats.
```

### 多镜头中的主体过渡原语

Seedance 能处理主体入画/出画的四种方式。显式命名原语有助于模型在镜头间构建正确过渡。

- **主体显现**（靠镜头运动或主体运动）— 主体在镜头中段才可见。
  示例：`Shot 2 (slow truck right): empty corridor at first; the camera trucks right to reveal Aang — bald, blue arrow tattoo, orange robes — pressed flat against the wall.`

- **主体消失** — 主体离开画面，通过运动或遮挡。
  示例：`Shot 4 (static wide): Aang — bald, blue arrow tattoo, orange robes — sprints into the temple doorway and is swallowed by shadow; camera holds on the empty threshold.`

- **主体切换**（ rack focus / 镜头运动）— 焦点或构图从一方转移到另一方。
  示例：`Shot 5 (close-up, rack focus): rack focus from Aang's glowing arrow tattoo in foreground to Sokka — dark hair, blue tunic, boomerang on back — emerging from the mist behind.`

- **复杂交替焦点** — 单镜头内焦点在两主体间来回。
  示例：`Shot 7 (medium two-shot, alternating rack focus): focus on Aang — bald, blue arrow tattoo, orange robes — as he speaks, then pulls to Katara — long brown hair, blue water-tribe parka — as she answers, then back to Aang on the final beat.`

## 口型同步模式

```
Aang says: "I won't run anymore."
Sokka, half a step behind, replies: "Then we fight."
```

- 严格使用 `Character says: "..."` / `Character replies: "..."` — 口型由引号内字符串驱动。
- 快切镜头台词宜短（≤ 6 词），避免漂移。
- 单人独白时，该镜头宜近景且镜头相对固定。

## 参数速查

| 参数 | 建议 |
|---|---|
| `duration` | `5`–`8` s 主镜头，`10`–`12` s 多镜头场景，`4` s 插入镜头。不确定时用 `auto`。 |
| `aspect_ratio` | `21:9` 预告片，`16:9` 播送，`9:16` Reels/Shorts/TikTok |
| `resolution` | 默认 `720p`。仅成本受限预览用 `480p`。 |
| `generate_audio` | 保持 `true` — 同步音频是核心优势。未用可在 compose 阶段剥离。 |
| `model_variant` | 主镜头、多镜头、重镜头用 `standard`。B-roll、预览、延迟敏感用 `fast`。 |
| `seed` | 构图满意后锁定；同 seed 迭代变体。 |
| `prompt length` | 主镜头 200–400 词；插入 80–150 词。Seedance 是少数奖励长而结构化五要素提示的模型之一。 |

## 迭代策略

1. **搭形状** — `duration=5`、`fast`、单镜头。确认构图。
2. **锁定 seed** — 记入该片段 README。
3. **升级到 `standard`** — 同 seed，收紧镜头与光线表述。
4. **延长或多镜头** — 仅在单镜头版本干净之后。
5. **定稿** — 将提示词、seed、变体、时长写入素材清单，便于 compose 一致重渲。

## 应避免

| 不要 | 原因 |
|---|---|
| 单镜头四个以上同时动作 | 运动连贯性崩溃。拆成多镜头。 |
| 画面内可读文字 / Logo | 文字渲染不可靠。文字用 Remotion 叠加。 |
| 冲突光线（`bright noon` + `neon night`） | 模型只选一种，忽略另一种。 |
| 快切上的长对白 | 口型漂移。 |
| 慢动作、多镜头或复杂镜头用 `fast` | 常一次不过。改 `standard`。 |
| 向 Seedance 要完整多乐器配乐 | 音频方向保持质感；真实配乐走 `music` / `pixabay_music` / `elevenlabs`，在 compose 混音。 |
| 无理由绕过 `video_selector` | 失去评分、回退与成本处理。 |

## 集成说明

- **电影管线：** Seedance 2.0 为默认。21:9，蒙太奇用多镜头，brief 有视觉圣经时用 reference-to-video。
- **动画解说：** 仅建立镜头 / 情绪 / 冷开场用 Seedance 2.0 — 核心动效仍在 Remotion。
- **屏幕演示 / 播客 / 切片工厂：** 非默认。仅风格化冷开场。
- **成本：** fal.ai 上 `standard` 10 s ≈ $3.03/条。`fast` 5 s ≈ $1.21。在提案阶段做预算。

## 示例 — 降世神通预告主节拍（总预告 60 s，此为 7 镜中的第 3 组）

```
Shot 1 (wide aerial, slow push-in, 3s):
Snow-covered Air Temple at dawn, spires catching orange light,
prayer flags lifting in wind.

Shot 2 (low angle medium, handheld, 3s):
Aang — bald, blue arrow tattoo on forehead, orange and yellow robes —
plants his staff on weathered stone, squints into the rising sun.

Shot 3 (extreme close-up, rack focus, 3s):
Rack focus from the glowing arrow on his forehead to distant peaks.
Aang says: "It's time."

Lighting: cold blue ambient with warm break on the horizon,
rim light from rising sun.
Style: anamorphic 2.39:1, teal-orange cinematic grade, 35mm film grain,
halation on speculars.
Audio: low taiko drums rising to orchestral swell on Shot 3,
wind through temple, distant wingbeats, leather staff-grip creak.
```

参数：`duration=10`，`aspect_ratio=21:9`，`resolution=720p`，`model_variant=standard`，`generate_audio=true`，第 2 镜后锁定 seed。
