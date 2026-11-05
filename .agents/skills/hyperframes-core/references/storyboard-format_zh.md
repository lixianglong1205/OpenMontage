# 分镜格式 — `STORYBOARD.md` 与解析后的 manifest

本文仅定义分镜的**基础数据格式**：`STORYBOARD.md` 的文件结构，以及解析得到的 `StoryboardManifest`。工作流**如何生成**分镜由该工作流自行规定；可选的旁白/TTS 文件（`SCRIPT.md`）是 TTS 步骤的独立关注点，不在本文范围内。

分镜是视频的**规划层**——单个 Markdown 文件中按顺序排列的一组**帧**（关键瞬间）。HyperFrames Studio 将其渲染为缩略图网格（Storyboard 视图，需开启 `VITE_STUDIO_ENABLE_STORYBOARD=1`）。解析器：`@hyperframes/core/storyboard` → `StoryboardManifest`；读取 API：`GET /api/projects/<id>/storyboard`。

## Frontmatter（全局方向）

文件顶部的 YAML 块。未知键保留在 `globals.extra` 下。

| Key        | 含义         | 示例                                   |
| ---------- | --------------- | ----------------------------------------- |
| `format`   | 画布尺寸     | `1920x1080`                               |
| `message`  | 一句话主旨 | `Ship a launch video in an afternoon`     |
| `arc`      | 叙事弧线   | `Hook → Problem → Solution → Proof → CTA` |
| `audience` | 目标受众    | `indie devs on X`                         |

## 逐帧章节

每一帧一个 `## Frame N — Title` 标题（H2/H3 接受 `Frame` / `Beat` / `Scene`）。元数据为 `- key: value` 列表项；其下至下一标题之前为自由格式的**叙事（narrative）**正文。

| Key             | 含义                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------- |
| `status`        | `outline` → `built` → `animated`（默认 `outline`）                                                         |
| `src`           | 指向该帧 HTML 子合成的项目相对路径（缩略图海报由此渲染）                   |
| `duration`      | 例如 `4s`                                                                                                     |
| `transition_in` | `crossfade` / `cut` / `wipe` …（别名 `transition`）                                                           |
| `scene`         | 缩略图网格一行说明（别名 `description` / `summary` / `caption`）                                |
| `voiceover`     | 该帧旁白**指引**（别名 `vo` / `voice_over` / `narration`）                                     |
| `poster`        | 缩略图海报 seek 秒数（跳过片头动画之后）                                                |
| _any other key_ | 原样保留在该帧的 `extra` 下 — 工作流可在此携带自有逐帧数据（特效、资源等） |

## 解析后的 manifest

解析器**宽松**：从不抛错，异常项记为 `warning`。

```
StoryboardManifest {
  globals: { format?, message?, arc?, audience?, extra: {…} }
  frames: Array<{
    index, number?, title?,
    status,                       // "outline" | "built" | "animated"
    src?, duration? / durationSeconds?, transitionIn?,
    scene?, voiceover?, poster?,
    narrative,                    // markdown below the metadata
    extra: {…}                    // unknown keys, preserved
  }>
  warnings: Array<{ message, line?, frameIndex? }>
}
```

读取 API 还会为每帧附加 `srcExists`，并在存在时挂载可选的 `SCRIPT.md` 载荷。

## `SCRIPT.md`（不在本文范围）

可选、自由格式、**不会解析进 manifest** — 驱动 TTS 的锁定旁白文件。其格式见 `references/script-format.md`；无旁白/TTS 的视频可没有该文件。上文逐帧 `voiceover` 是分镜自带的旁白指引。

## 示例

```markdown
---
format: 1920x1080
message: "Ship a launch video in an afternoon"
arc: Hook → Problem → Solution → Proof → CTA
audience: indie devs on X
---

## Frame 1 — Hook

- scene: Big type punches in on the beat
- duration: 3s
- poster: 2s
- transition_in: cut
- status: animated
- voiceover: "Ship a launch video in an afternoon."
- src: compositions/frames/01-hook.html

Open cold on the promise. This is the thesis — everything after pays it off.

## Frame 2 — The problem

- scene: A 20-minute timer spins on a stack of rejected takes
- duration: 4s
- transition_in: crossfade
- status: built
- voiceover: "The old way? Prompt, wait twenty minutes, get something that misses."
- src: compositions/frames/02-problem.html

The old way: prompt, wait, get something that misses. Establish the pain we remove.
```

## 说明

- `status: outline` 且尚无已构建 `src` 的帧会渲染为大纲占位。
- 多行 `voiceover` 值在保存时会折叠为单行。
