---
name: seedance-2-0
description: |
  使用字节跳动 Seedance 2.0 生成电影感片段——在 OpenMontage 中配置付费网关时的首选高端视频模型。适用场景：(1) 制作预告片、 teaser、 hype 剪辑或高端电影感片段，(2) 需要单次生成原生同步音频（对白、音效、环境声），(3) 需要在一次生成内完成多镜头剪辑，(4) 需要导演级镜头控制，(5) 需要通过提示词中的引号对白实现口型同步，(6) 需要参考条件生成（最多 9 张图片 + 3 段视频 + 3 段音频），(7) 希望在多个镜头间保持角色身份一致。可通过 fal.ai（`seedance_video` 工具）、HeyGen（Video Agent / Avatar Shots）、Replicate、Runway（Enterprise，非美国）、Freepik、BytePlus ModelArk、Higgsfield、Pollo 及其他聚合平台访问。
allowed-tools: Bash, Read, Write
metadata:
  openclaw:
    requires:
      env_any:
        - FAL_KEY
        - HEYGEN_API_KEY
        - REPLICATE_API_TOKEN
---

# Seedance 2.0（ByteDance）

Seedance 2.0 是字节跳动 Seed 团队统一的多模态视频+音频模型（2026 年 2 月发布，2026 年 4 月起通过合作 API 全球可用）。在 OpenMontage 中，只要配置了任一支持的网关，它就是电影感、预告片、teaser 与动效导向工作的**首选高端默认模型**。OpenMontage 直接封装四个网关（`seedance_video` → fal.ai，`seedance_replicate` → Replicate，`runway_video` 且 `model="seedance_2.0"` → Runway，`higgsfield_video` 且 `model="seedance_2.0"` → Higgsfield）；BytePlus / Freepik / HeyGen-Video-Agent 封装在路线图中。评分引擎按 `provider="seedance"` 去重，用户配置 whichever 网关会自动胜出——代理应向 `video_selector` 传入 `preferred_provider="seedance"`（或让评分器选择），而不是按名称路由到特定网关。

## 为何是 OpenMontage 的高端默认

| 能力 | Seedance 2.0 | 说明 |
|---|---|---|
| 单次生成原生同步音频 | 是 | 对白 + 音效 + 环境声联合生成，非后期对齐 |
| 单次生成内多镜头 | 是 | 一个提示词内多个切镜/镜头 |
| 导演级镜头控制 | 是 | 识别镜头语言（dolly、tilt、arc、crane、handheld） |
| 引号对白口型同步 | 是 | `Character says: "..."` 匹配口型 |
| 参考条件 | 最多 9 图 + 3 视频 + 3 音频 | 12 资产多模态 |
| 角色身份一致性 | 是 | 跨镜头人脸/主体稳定 |
| 单镜头最长时长 | 15 s | auto / 4–15 s |
| 分辨率上限 | 部分端点 1080p（fal.ai 默认 720p） | 因提供商而异 |
| Elo（Artificial Analysis） | 1269（截至 2026 年 2 月 #1） | 优于 Veo 3、Sora 2、Runway Gen-4.5 |

仅在以下情况切换：预算严格（用 `fast` 变体或 LTX）、用户指定其他提供商（VEO/Sora/Kling），或风格更适合其他模型。

## 提供商接入面

| 接入面 | 环境变量 | OpenMontage 工具 | 状态 | 说明 |
|---|---|---|---|---|
| **fal.ai**（主） | `FAL_KEY` | `seedance_video` | ✅ 已封装 | 见下方模型 ID。支持 T2V、I2V、reference-to-video；`standard` 与 `fast` 变体。OpenMontage 默认。 |
| **Replicate** | `REPLICATE_API_TOKEN` | `seedance_replicate` | ✅ 已封装 | `bytedance/seedance-2.0` + `bytedance/seedance-2.0-fast`。标准 Replicate prediction API。 |
| **Runway** | `RUNWAY_API_KEY` | `runway_video`（model: `seedance_2.0`） | ✅ 已封装 | Runway 内第三方 Seedance 2.0 模型。**Unlimited/Enterprise 套餐，仅限非美国**。通过 `model` 参数选择。 |
| **Higgsfield** | `HIGGSFIELD_API_KEY` + `_SECRET` | `higgsfield_video`（model: `seedance_2.0`） | ✅ 已封装 | 该工具默认模型为 Seedance 2.0。强调角色身份与长片串联。 |
| **HeyGen** | `HEYGEN_API_KEY` | `heygen_video`（仅 1.x）+ TODO | ⚠️ 仅 1.x | HeyGen 上 `seedance_pro` / `seedance_lite` 工作流提供商字符串对应 Seedance 1.x。2.0 经 Video Agent / Avatar Shots 端点——独立 `seedance_heygen` 工具在路线图中。 |
| **BytePlus ModelArk / Volcengine** | BytePlus token | 未封装 | 🔜 路线图 | 字节直连。Pro 约 $0.15 / 5 s，Lite 约 $0.010/s。基于 token。 |
| **Freepik** | Freepik token | 未封装 | 🔜 路线图 | `POST /v1/ai/image-to-video/seedance-pro-1080p` 用于 1080p I2V |
| **Pollo / PiAPI / Atlas Cloud / AIMLAPI** | 各异 | 未封装 | 🔜 路线图 | 聚合商转售 fal.ai 或 ByteDance 端点 |

### fal.ai 模型 ID（`seedance_video` 使用）

```
bytedance/seedance-2.0/text-to-video
bytedance/seedance-2.0/image-to-video
bytedance/seedance-2.0/reference-to-video        # 9 img + 3 vid + 3 audio
bytedance/seedance-2.0/fast/text-to-video
bytedance/seedance-2.0/fast/image-to-video
bytedance/seedance-2.0/fast/reference-to-video
```

定价（fal.ai，720p）：standard T2V $0.3034 / s，I2V $0.3024 / s。Fast 各端点 $0.2419 / s。
`fast` 变体以牺牲部分镜头/运动保真换取延迟与成本——**不要**在首次尝试时将慢动作、多镜头或 dolly 密集的提示词路由到 `fast`。

## 在 OpenMontage 内调用 Seedance 2.0

始终通过 `video_selector` 并设置 `preferred_provider="seedance"`（或让评分引擎选择）：

```python
from tools.tool_registry import registry
registry.ensure_discovered()
selector = registry.get("video_selector")
result = selector.execute({
    "prompt": PROMPT,
    "preferred_provider": "seedance",
    "operation": "text_to_video",       # or image_to_video / reference_to_video
    "aspect_ratio": "21:9",             # 21:9 / 16:9 / 9:16 / 4:3 / 1:1 / 3:4
    "duration": "10",                   # auto / 4..15
    "resolution": "720p",               # 480p / 720p
    "output_path": "projects/<proj>/assets/video/clip_01.mp4",
})
```

直接调用提供商工具（仅当必须绕过 selector 时）：

```python
seedance = registry.get("seedance_video")
seedance.execute({
    "prompt": PROMPT,
    "model_variant": "standard",   # "standard" or "fast"
    "operation": "text_to_video",
    "aspect_ratio": "21:9",
    "duration": "10",
    "resolution": "720p",
    "generate_audio": True,
    "seed": 12345,                 # optional, for reproducible variations
    "output_path": "...",
})
```

## 提示词结构 — Higgsfield 方法论（2026 年 canonical）

**关键：每个提示词必须以镜头结构声明开头。** Seedance 奖励在任意创意描述之前先声明格式的提示词。这是单一最大的质量杠杆。

### 开头模板（逐字复制其一，再扩展）

**动作/格斗/多镜头（表现最佳格式）：**
```
Montage, multi-shot Hollywood action, don't use one camera angle or single cut, cinematic lighting, photorealistic, 35mm film quality, ARRI ALEXA aesthetic, heavy film grain, sharp but imperfect focus, motion blur on fast actions, halation on highlights, soft highlight rolloff, wide-angle lens with strong distortion, subtle chromatic aberration near frame edges, no 3D, no cartoon, no VFX aesthetic.
```

**单 POV 连续镜头（orb、walkthrough）：**
```
Single continuous shot, first-person POV perspective, the camera IS [his/her] eyes, hyper-chaotic handheld motion, completely unstabilized, violent raw human movement, constant micro-jitters, aggressive head swings, abrupt jerks, frequent over-rotation, no smoothness at all, no cuts, no zoom, 35mm film, photorealistic.
```

**锁定 POV 反应场景：**
```
One continuous shot, POV [setting] perspective, no cuts, no zoom, natural head movement, photorealistic, 35mm film grain.
```

### 正文结构（开头之后）

1. **环境/地点** — 感官细节（湿沥青、钠灯、霓虹溢光、雨粒、体积雾）
2. **角色块** — 含参考标签与 identity-lock 语言（见下方 Reference-to-video）
3. **敌人/次要角色块** — 同等细节层级
4. **逐拍编排** 带时间标记：`0–3s: …  3–6s: …  6–10s: …`
5. **括号内联 VFX：** `[VFX: branching white-blue electric arcs pulsing along forearms, sparks jumping between fingers]`
6. **慢动作标记：** 在冲击拍前写 `RAMPS TO SLOW MOTION`，恢复时写 `SNAPS BACK TO REAL TIME`
7. **声音设计块：** 要么 `no music, only raw SFX`，要么明确 SFX 序列。音乐描述保持质感化。

### 格斗词汇（实测有效）

- `snaps forward`, `lunges`, `sprints`, `weaves`, `chambers`, `drives`, `pivots`, `redirects`, `ducks`, `slips`
- `explodes outward`, `devastating`, `raw force`, `kinetic`, `overload`, `compresses`, `erupts`, `fractures`, `ripples`
- 避免软动词：`attacks`, `hits`, `fights` — 这些显得泛化，Seedance 表现不足

### 镜头行为 — 说明镜头在做什么、不在做什么

Seedance 在镜头意图模糊时容易失误。始终明确否定你不想要的：
- `no cuts`（连续 POV）
- `no zoom`（避免不自然透视推进）
- `no stabilization`（需要 chaotic handheld 时）
- `no smoothness at all`
- `no 3D, no cartoon, no VFX aesthetic` — 反直觉但可强制 photoreal 皮肤/纹理/光照，即使场景有重 VFX

### 写实强化短语

当 brief 有 VFX 但你要 photoreal 皮肤/纹理（非塑料 Marvel 卡通感）时，加入：
```
no 3D, no cartoon, no VFX aesthetic — photorealistic textures, real skin pores, authentic fabric detail, grounded in reality
```

### 格式优先级（Higgsfield 经验排序）

| 格式 | 最适合 | 模式 |
|---|---|---|
| **Transformation** | 平静 → 威胁 → 变身 → 余波 | 6 编号镜头 × 各 2.5s @ 共 15s |
| **Orbs** | 单连续 POV | 1 镜头 × 15s，hyper-chaotic handheld |
| **Fights** | 格斗编排 | 逐拍、力量对比清晰、RAMPS/SNAPS |
| **POV** | 锁定反应 | 连续、「no cuts no zoom」 mantra |
| **Animation** | 风格化 3D | `@image` 关键帧 + 分段计时 |

多镜头生成中 **每镜头 2.5 秒节奏** 似乎最优。

## 遗留 8 段模板（仅用于简单单镜头，非动作）

Seedance 2.0 对镜头语言、多镜头切镜与引号对白异常字面。使用此 8 段模板：

```
[Shot / framing] + [Camera movement] +
[Subject description — physical detail that must persist across shots] +
[Action beat 1] → [optional cut] → [Action beat 2] +
[Setting / environment] + [Lighting / palette] +
[Style / grade / era] + [Audio — ambient, diegetic, music, dialogue]
```

### 单次生成内多镜头

Seedance 识别提示词内 explicit 镜头列表。每镜格式：

```
Shot 1 (wide establishing, slow aerial push-in): ...
Shot 2 (medium close-up, handheld): ...
Shot 3 (extreme close-up, rack focus): ...
```

跨镜头保持主体描述一致以稳定身份。

### 引号对白口型同步

```
Aang stands on the cliff edge, staff raised, wind in his cloak.
Aang says: "I won't run anymore."
Sokka, half a step behind, replies: "Then we fight."
```

精确使用 `Character says: "..."` / `Character replies: "..."` — 口型绑定引号字符串。每行控制在约 6 词内；更长在快切片段上易漂移。

### 有效的音频提示

环境：`distant thunder rolling over mountains`, `wind through reeds`, `crackling campfire`
画内：`boots crunching snow`, `staff planting on stone`, `wingbeats overhead`
音乐方向（轻触）：`low orchestral swell building`, `taiko drums entering on Shot 3`
**不要**请求复杂多乐器配乐 — 音乐语言保持质感化。

### Reference-to-video

有角色/产品/服装参考时，使用 reference-to-video 端点。Seedance 2.0 识别 explicit 括号标签语法：

```
[reference_image: hero_portrait.png]
[identity_lock]
The same character — bald, blue arrow tattoo, orange robes — consistent across all shots, no drift or deformation. Do not alter clothing category or primary color.

Shot 1 (wide, slow push-in): hero walks across the snowy Air Temple courtyard, wind lifting robes.
Shot 2 (medium close-up): hero turns toward camera, staff in hand.
Shot 3 (extreme close-up, rack focus): hero's eyes open, wind whipping.
```

**可 measurably 减少人脸漂移的身份锚短语**（叠加使用 — 冗余有帮助）：
- `the same character`
- `consistent across different scenes / all shots`
- `maintain exact appearance from reference image`
- `no deformation, no drift, no face morph`
- `Do not alter clothing category or primary color`

**单参考工作流（实践中常见）：** 仅有一张照片时：
- 使用清晰、正面、中性光、运动模糊最小的肖像；避免遮挡面部（手机、墨镜、重阴影）。
- 所有镜头复用**同一**参考图 — 不要每镜生成新 ref。
- 在单一 `[identity_lock]` 块下将所有镜头放入**一个**提示词，使模型视为连贯序列。
- 若按设计换装（如便装 → 戏服），在出现该戏服的每镜 verbatim 描述，并加 `Do not alter clothing category or primary color` 以锁定生成结果。

**反漂移回退：** 若首渲跨帧人脸 morph，缩短时长（5–6s 而非 10s）、收紧 identity-lock 语言；若有多张参考图，精简为最一致的 3 张而非堆满 9 张。

## 参数指引

| 参数 | 指引 |
|---|---|
| `duration` | 英雄镜头 `5`–`8`，含多镜头切镜的完整场景 `10`–`12`，快插 `4`。不确定用 `auto`。 |
| `aspect_ratio` | 电影预告 `21:9`，广播/YouTube `16:9`，Reels/Shorts/TikTok `9:16` |
| `resolution` | 默认 `720p`。成本受限批量预览降至 `480p`，非成片 |
| `generate_audio` | 除非有明确理由静音否则**保持开启** — Seedance 护城河是同步音频。合成阶段可下游剥离音频。 |
| `model_variant` | 英雄/电影感用 `standard`；`fast` 仅用于 B-roll、预览或延迟为硬约束 |
| `seed` | 在选定镜头的变体迭代前固定 seed — 其余参数保持不变 |

## 应避免

| 不要 | 原因 |
|---|---|
| 一镜内塞四个以上同时角色动作 | 运动连贯性崩；拆成多镜头 |
| 在片段内请求可读文字/Logo | 文字渲染不可靠 — 在 Remotion 叠加层处理 |
| 混用冲突光照（「正午明亮」+「霓虹夜」） | 模型择一忽略另一 |
| 快切镜头写超过约 6 词对白 | 口型同步漂移 |
| 慢动作、多镜头或复杂运镜用 `fast` 变体 | 首次尝试常失败 — 路由到 `standard` |
| 通过 Seedance 音频生成完整配乐 | 质感可以；真实配乐用 `music` / `pixabay_music` / `elevenlabs` 在 compose 混音 |
| 无理由绕过 `video_selector` | 失去成本/可用性/回退与评分上下文 |

## 迭代策略

1. **勾勒形态**：用目标构图下单次 `duration=5` `fast` T2V。确认构图成立。
2. **锁定 seed**：构图可读后。
3. **升级到 `standard`**：同 seed，收紧镜头与光照语言。
4. **延长与加镜** — 单镜版本干净后再上多镜头或更长时长。
5. **每镜保留 README**：记录 prompt + seed + variant，便于 compose 阶段一致重渲。

## OpenMontance 流水线集成说明

- **电影感流水线：** Seedance 2.0 为默认视频模型。英雄用 21:9，蒙太奇节拍用多镜头，brief 有视觉 bible 时用 reference-to-video。
- **动画解说：** Seedance 2.0 仅用于 establishing / 情绪镜头；多数镜头应留在 Remotion。不要用 Seedance 替换 Remotion 动效 — 不同工具、不同职责。
- **屏幕演示 / 播客 / 片段工厂：** Seedance 非合适默认 — 这些是 footage 导向。仅用于风格化 cold-open。
- **成本纪律：** `standard` 10 s ≈ 每片段 $3.03。提案阶段 accordingly 预算。预览 `fast` 5 s ≈ $1.21。

## 每个 Seedance 镜头的验证清单

- [ ] 所选时长内运动连贯可读
- [ ] 音频确实同步（检查对白 + 脚步/冲击）
- [ ] 角色身份与参考/前镜一致
- [ ] 镜头方向符合提示（要求 static 时不要 auto-dolly）
- [ ] 无模型尝试渲染的可读文字
- [ ] 调色匹配已批准风格 playbook
- [ ] 输出时长与请求一致（部分端点会四舍五入）

## 来源

- fal.ai Seedance 2.0: https://fal.ai/seedance-2.0
- fal.ai how-to-use: https://fal.ai/learn/tools/how-to-use-seedance-2-0
- Replicate bytedance collection: https://replicate.com/bytedance
- HeyGen Seedance 2.0: https://www.heygen.com/blog/introducing-seedance-2-and-heygen
- Runway Seedance: https://runwayml.com/product/seedance
- BytePlus Dreamina Seedance 2.0: https://www.byteplus.com/en/product/seedance
- Freepik Seedance 2.0: https://www.freepik.com/seedance-2
- Higgsfield Seedance 2.0: https://higgsfield.ai/seedance/2.0
- Pollo Seedance 2.0: https://pollo.ai/m/seedance/seedance-2-0
- ByteDance Seed official: https://seed.bytedance.com/en/seedance2_0
- Seedance 2.0 Wikipedia: https://en.wikipedia.org/wiki/Seedance_2.0
