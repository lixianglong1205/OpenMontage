# `SCRIPT.md` — 锁定旁白（可选）

项目的**锁定旁白**：最终口播文案 + 音色 + 演绎方式。它是规划层中的*可选*文件——无旁白（仅 BGM、静默叠加）的视频不需要该文件。分镜板每帧的 `voiceover` 是更轻、可编辑的*指南*；`SCRIPT.md` 是*定稿*。（分镜格式 → `references/storyboard-format.md`。）

本文件仅定义 SCRIPT.md 的**结构**。将口播文案合成为音频的能力由 `hyperframes-media` 负责 → `references/tts.md`。

自由格式 Markdown — 无严格解析器；Studio 在分镜板旁只读展示，TTS 步骤提取缩进后的口播行。

## 结构

一个头部块，随后每句口播一个章节。

| 部分                            | 包含                                                                                                                                   |
| ------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- |
| 头部                            | `**Voice:**`（供应商 + 音色）、`**Voice settings:**`（如 stability / similarity / style）、`**Voice direction:**`（整体演绎） |
| `## Line N — <label> (Frame N)` | 一句口播，对应其分镜帧                                                                                           |
| `**Time:**`                     | 分镜板上的大致时间窗 — *指南*，非权威（真实时间来自 TTS 词级时间戳）                                    |
| `**Delivery:**`                 | 单行演绎说明                                                                                                                  |
| 缩进块                  | **口播正文** — 唯一送入 TTS 的部分                                                                                          |

## 示例

```markdown
# SCRIPT — acme-launch

**Voice:** Rachel (ElevenLabs)
**Voice settings:** stability 0.35 · similarity 0.75 · style 0.20
**Voice direction:** Confident, warm, a little playful.

---

## Line 1 — Hook (Frame 1)

**Time:** 0.0 – 3.0s
**Delivery:** Land the promise on the beat.

    Ship a launch video in an afternoon.

## Line 2 — The problem (Frame 2)

**Time:** 3.0 – 7.0s
**Delivery:** Wry, a touch tired.

    The old way? Prompt, wait twenty minutes, get something that misses.
```

## 接入 TTS

将每行的口播正文送入 `npx hyperframes tts`（按头部固定 `--voice` / `--provider`；捕获词级时间戳用于字幕）。真实逐词时间将取代 `**Time:**` 指南。CLI 约定 → `hyperframes-media/references/tts.md`。
