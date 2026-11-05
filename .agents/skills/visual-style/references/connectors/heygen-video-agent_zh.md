# HeyGen Video Agent 连接器

将 `visual-style.md` 应用于 HeyGen Video Agent，用于 AI 生成视频。

## 概述

HeyGen Video Agent 接受文本提示，其中可包含视觉风格说明。`style_prompt_full` 字段可直接映射到该提示。

## 字段映射

| visual-style.md 字段 | HeyGen 用法 |
|-----------------------|--------------|
| `style_prompt_full` | 原样追加到生成提示末尾 |
| `motion.transitions` | 场景转场说明 |
| `motion.animation_style` | 动画行为 |
| `motion.pacing` | 节奏/时长指导 |
| `typography.caption` | 字幕样式（若启用字幕） |
| `layout.aspect_ratio` | 方向设置（16:9 = 横屏，9:16 = 竖屏） |
| `mood.avoid` | 负向提示 / 排除说明 |
| `assets.gsep_elements` | 叠加素材（若支持） |
| `x_heygen.orientation` | 显式方向覆盖 |
| `x_heygen.video_id` | 已有 HeyGen 视频的引用 |

## 提示模板

```
Create a video about [TOPIC].

Script:
[USER'S SCRIPT]

Visual style:
[PASTE style_prompt_full HERE]

Additional constraints:
- [ITEMS FROM mood.avoid]

Motion:
- Transitions: [motion.transitions]
- Pacing: [motion.pacing]
- Animation: [motion.animation_style]

Format: [layout.aspect_ratio OR x_heygen.orientation]
```

## 示例：无数字人动态图形

纯动态图形、不含数字人时：

```
Create a video about our Q4 results.

Script:
Revenue grew 40% year over year. We shipped 12 new features.
Customer satisfaction hit an all-time high of 94%.

Visual style:
Josef Müller-Brockmann Swiss International Style. Grid-locked layouts
with mathematical precision. Black and white base with ONE accent color
(electric blue #0066FF). Strong diagonal compositions. Helvetica
typography only. Data visualizations are the hero — animated charts,
counters, grids. Every frame snaps to a grid. Transitions are horizontal
grid wipes. No organic shapes. No gradients. No stock photography.
Everything is geometric, systematic, precise.

Additional constraints:
- No avatar
- No b-roll footage
- No stock photography
- Pure motion graphics only

Motion:
- Transitions: horizontal grid wipes, clean hard cuts
- Pacing: Measured, confident, unhurried
- Animation: Elements snap to grid positions, charts animate systematically

Format: landscape (16:9)
```

## 工作流

1. **加载风格** — 读取 `visual-style.md` 文件
2. **提取关键字段：**
   - `style_prompt_full`（必填）
   - `motion.*` 字段（推荐）
   - `mood.avoid`（推荐）
   - `layout.aspect_ratio` 或 `x_heygen.orientation`
3. **构建提示** — 使用上文模板
4. **调用 HeyGen Video Agent** — 使用 HeyGen MCP 工具或 API
5. **保存引用** — 如需可将视频 ID 写入 `x_heygen.video_id`

## 提示

- **明确写出你不想要的** — HeyGen 对负向约束响应良好
- **动态图形模式** — 抽象风格时可添加 “No avatar. No b-roll. Pure motion graphics.”
- **数据可视化** — 数字密集内容可提及 “animated charts, counters, data viz”
- **转场很重要** — 请显式指定转场风格；默认值可能与你的风格不符

## 支持的风格

以下图库风格与 HeyGen Video Agent 尤其契合：

- `mueller-brockmann-swiss.visual-style.md` — 数据驱动、网格锁定
- `neville-brody-industrial.visual-style.md` — 粗体 typography、工业风
- `saul-bass-cinematic.visual-style.md` — 电影感标题、大胆形状
- `game-boy-color.visual-style.md` — 像素艺术、复古游戏
- `heygen-ai-video.visual-style.md` — 现代 AI/SaaS 美学
