# VEO 3.1 / VEO 3 — 提示词指南

> 来源：[Vertex AI Video Gen Prompt Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide)
> 通用词汇表见：`skills/creative/video-gen-prompting.md`

**字数：** VEO 3.1 的最佳区间约为 100–250 词；更长的提示词通常不再带来收益。

## VEO 专属的 14 要素结构

VEO 对提示词结构的响应最为全面：

1. **主体（Subject）** — 动作围绕谁/什么展开
2. **动作（Action）** — 动作、互动、表情
3. **场景 / 情境（Scene / Context）** — 地点、时间、天气、时代
4. **机位角度（Camera Angles）** — 景别与视角
5. **镜头运动（Camera Movements）** — 动态运镜
6. **镜头 / 光学效果（Lens / Optical Effects）** — 相机如何「看」
7. **光线（Lighting）** — 光源、方向、质感
8. **基调 / 情绪（Tone / Mood）** — 情感色彩
9. **艺术风格（Artistic Style）** — 写实、电影感、动画、艺术流派
10. **氛围（Ambiance）** — 配色、大气效果、材质
11. **时间要素（Temporal Elements）** — 节奏、时间流逝、韵律
12. **音频（Audio）** — 音效、环境声、对白（VEO 3 可生成对白）
13. **电影术语（Cinematic Terms）** — 剪辑手法（match cut、蒙太奇、split diopter 等）
14. **负向提示（Negative Prompt）** — 需要排除的内容

## VEO 专属优势

- **对白生成**：VEO 3 原生生成角色语音。对白请用自然写法。
- **音频一体化**：环境声、音乐与人声与画面一并生成。
- **负向提示**：明确支持 — 例如「no text overlays, no watermarks, no lens flare」
- **剪辑词汇**：能理解「match cut」「jump cut」「montage」「split diopter」等提示词术语。

### VEO 会字面执行的镜头词汇

VEO 3.1 区分三类镜头运动，并将各自 token 视为独立原语。混用（例如想要 dolly 却写 zoom）会得到错误运动。

- **平移（机位物理移动）：** `dolly`（沿光轴前后）、`truck`（左右横移）、`pedestal`（上下垂直）
- **旋转（机位不动，相机旋转）：** `pan`（偏航，左右）、`tilt`（俯仰，上下）、`roll`（荷兰角 / Z 轴）
- **仅镜头（机位与机身不动）：** `zoom`（焦距变化）、`rack focus` / `pull focus` / `focus tracking`（焦平面变化）

dolly ≠ zoom；pan ≠ truck。VEO 以提示中领先的 token 为准。

## VEO 镜头效果（独有）

VEO 对多数模型忽略的光学效果响应明确：

| 效果 | 提示词用语 |
|--------|----------------|
| **Rack focus** | "rack focus from foreground flower to background figure"（快速切换） |
| **Pull focus** | "slow pull focus from the candle in the foreground to the doorway behind"（渐进，比 rack 更慢） |
| **Focus tracking** | "focus tracks the runner as she crosses frame; background stays soft"（焦点跟随运动主体） |
| **Dolly zoom (vertigo)** | "vertigo effect as character realizes the truth" |
| **Fisheye** | "fisheye lens distortion, skatepark POV" |
| **Anamorphic lens flare** | "anamorphic lens flare streaking horizontally from setting sun" |

三种对焦模式（rack、pull、tracking）含义不同 — VEO 3.1 会按论文区分执行。

## VEO 艺术流派参考

VEO 适合用具体艺术流派作风格锚点：
- "Van Gogh-inspired swirling sky"
- "Surrealist Dalí-esque melting landscape"
- "Art Deco geometric patterns in the architecture"
- "Bauhaus clean lines and primary colors"
- "Gritty graphic novel illustration style"
- "Chinese ink wash painting animation"

## 避免自动生成字幕

VEO 在对白场景下可能默认加字幕。若要避免：
- 在负向提示中加入："no subtitles, no captions, no text overlays"

## 示例

```
Subject: A lone astronaut in a weathered white spacesuit
Action: Slowly turns to face the camera, visor reflecting a dying star
Scene: Surface of a barren moon, cracked grey terrain, massive ringed
       planet filling the horizon
Camera: Low-angle medium shot, slow arc around subject
Lens: Wide-angle, deep focus keeping both astronaut and planet sharp
Lighting: Harsh rim light from the star behind, cool blue fill from
          planet reflection, no atmosphere diffusion
Mood: Awe, isolation, quiet grandeur
Style: Photorealistic sci-fi cinematography, IMAX-scale
Audio: Breathing inside helmet, faint radio static, low rumble
Negative: No text, no HUD overlay, no lens flare
```
