# Sora 2 — 提示词指南

> 来源：[OpenAI Sora 2 Cookbook](https://developers.openai.com/cookbook/examples/sora/sora2_prompting_guide)
> 通用词汇表见：`skills/creative/video-gen-prompting.md`

**字数：** Sora 2 在约 100–250 词处趋于饱和。超过 250 词后，额外细节很少再改善输出。

## Sora 专用提示词模板

Sora 对「散文式场景描述 + 摄影区块 + 动作节拍」的结构化格式响应最佳：

```
[Prose scene description — characters, costumes, scenery, weather, details.
 Be as descriptive as possible to match your vision.]

Cinematography:
Camera shot: [framing and angle]
Lens: [focal length, type]
Lighting: [key, fill, rim, practical sources with color temp]
Mood: [overall tone]

Actions:
- [Beat 1: specific gesture or movement]
- [Beat 2: another distinct beat]
- [Beat 3: reaction or dialogue]

Dialogue:
[Short natural lines, kept brief for clip length]
```

## 高级可选字段

Sora 对以下多数模型会忽略的制作级细节有响应：

| 字段 | 示例 |
|-------|---------|
| **镜头规格** | "40mm spherical", "85mm", "Anamorphic 2.0x" |
| **滤镜** | "Black Pro-Mist 1/4", "slight CPL rotation" |
| **调色 / 色板** | "Warm Kodak-inspired grade", "teal-and-orange LUT" |
| **胶片模拟** | "16mm black-and-white", "35mm photochemical contrast" |
| **画内音效（diegetic sound）** | "faint rail screech, rain patters window, clock ticks" |
| **服装** | "navy coat, sleeves rolled, suspenders loose" |
| **成片处理** | "fine-grain overlay, mild halation, gate weave, soft vignette" |
| **快门** | "180° shutter angle" |
| **播放速度** | "speed ramp from 1x to 0.25x mid-shot", "stop-motion staccato", "time-reversed exhale" |
| **镜头畸变** | "fisheye barrel distortion at the edges", "subtle barrel curvature on straight lines" |
| **对焦模式** | "rack focus from foreground bottle to background figure", "deep focus, FG to BG sharp" |

## Sora 的独特之处

- **散文优先**：先写一段丰富的段落，再补充技术区块。不要以相机参数开头。
- **角色引用**：可通过 API 锁定最多 2 个已上传的角色 ID。
- **对白同步**：短句有效；复杂的多角色对白则不行。
- **编辑指令**：如「Same shot, switch to 85mm」或「Same lighting, new palette: teal, sand, rust」——Sora 支持在已有生成结果上迭代精修。
- **创作自由度**：提示词越短 → 创作空间越大；越长 → 控制越细。

## 色板技巧

用 3–5 个锚定色名替代模糊的「暖色调」：
- "Amber, cream, walnut brown"（复古暖调）
- "Teal, sand, rust"（海岸沙漠）
- "Cool blues with warm tungsten accents"（黑色电影风）

## Sora API 参数（无法在提示词中设置）

- `model`: `sora-2` 或 `sora-2-pro`
- `size`: 720x1280, 1280x720, 1080x1920, 1920x1080, 1024x1792, 1792x1024
- `seconds`: 4, 8, 12, 16, 20

## 示例

```
Style: Hand-painted 2D/3D hybrid animation with soft brush textures,
warm tungsten lighting, tactile stop-motion feel. Subtle watercolor wash;
warm-cool balance; filmic motion blur.

Inside a cluttered workshop, shelves overflow with gears and yellowing
blueprints. Small round robot sits on wooden bench, dented body patched
with mismatched plates. Large glowing blue eyes flicker as it fiddles
with a humming light bulb.

Cinematography:
Camera: medium close-up, slow push-in with gentle parallax from hanging tools
Lens: 35mm virtual; shallow depth of field
Lighting: warm key from overhead practical; cool spill from window
Mood: gentle, whimsical, touch of suspense

Actions:
- Robot taps bulb; sparks crackle
- Flinches, dropping bulb, eyes widening
- Bulb tumbles in slow motion; catches it just in time
- Puff of steam escapes chest — relief and pride

Background Sound:
Rain, ticking clock, soft mechanical hum, faint bulb sizzle
```
