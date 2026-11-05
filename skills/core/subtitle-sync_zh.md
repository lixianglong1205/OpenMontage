# 字幕同步技能

## 使用场景

使用 `subtitle_gen` 工具将转录数据（来自 `transcriber`）
转换为时间轴正确的字幕文件。本技能涵盖竖屏与横屏视频的
时间策略、格式与可读性。

## 工具

| 工具 | 能力 |
|------|------|
| `subtitle_gen` | 根据词级时间戳生成 SRT、VTT 或 caption JSON |

## 输出格式

| 格式 | 扩展名 | 使用场景 |
|--------|-----------|----------|
| SRT | `.srt` | 通用 — 适用于 FFmpeg、播放器、YouTube 上传 |
| VTT | `.vtt` | Web 原生 — HTML5 视频、浏览器播放 |
| Caption JSON | `.caption.json` | 程序化 — 供自定义渲染器使用的词级数据 |

## 各格式的字幕条长度

### 竖屏短视频（TikTok、Reels、Shorts）

- **每条字幕最多 3–4 个词** — 屏幕窄，文字需足够大才易读
- **每行最多 20 个字符** — 避免在窄屏上换行
- 字幕 **必不可少**（多数观众静音观看）

### 横屏标准（YouTube、Web）

- **每条字幕最多 6–8 个词** — 宽屏可容纳更多文字
- **每行最多 42 个字符** — 标准广播上限

### 通用规则

- 观众平均阅读速度约 15 字符/秒
- 最短显示时间：每条字幕 0.5 秒
- 最长显示时间：每条字幕 5 秒

## 烧录样式（ASS force_style）

通过 `video_compose` 烧录字幕时，以下参数作为 ASS
`force_style` 传入。请使用正确的 ASS 颜色格式：`&HAABBGGRR`（非 hex RGB）。

### 竖屏视频（1080x1920）

```
font: Arial
font_size: 18
bold: true
primary_color: &H00FFFFFF      # white (ASS format: alpha=00, BGR=FFFFFF)
outline_color: &H00000000      # black
outline_width: 3               # thick outline for readability on varied backgrounds
shadow: 2
margin_v: 50                   # pixels from bottom edge
alignment: 2                   # bottom center
```

### 横屏视频（1920x1080）

```
font: Arial
font_size: 22
bold: true
primary_color: &H00FFFFFF
outline_color: &H00000000
outline_width: 2
shadow: 1
margin_v: 40
alignment: 2
```

### 常见错误

- **颜色格式错误：** `&HFFFFFF` 会破坏定位。始终使用完整的 8 位 `&H00FFFFFF`。
- **竖屏字号过大：** `font_size: 28` 会占满 9:16 画面中部。最大使用 18。
- **竖屏每条词数过多：** 5 个词以上会形成多行块，遮挡人脸。
- **MarginV 过大：** 超过 200 会把文字推出屏幕外。多数情况保持在 100 以下。

## 时间轴最佳实践

### 与语音对齐

- 字幕开始须与词语起始时刻一致（不能早于说话人开口）
- 字幕结束应在最后一个词之后约延长 200ms，便于阅读
- 不要让一条字幕延续到下一位说话人开口

### 按词边界分组

`subtitle_gen` 工具在 `max_words_per_cue` 与
`max_chars_per_line` 约束下对词进行分组。若无词级时间戳，则回退
到片段级时间轴并均匀分配。

## 质量检查清单

- [ ] 每个说出的词都出现在某条字幕中
- [ ] 没有字幕超出目标格式的字符上限
- [ ] 字幕位于画面下方 20% 区域 — 不遮挡人脸
- [ ] 在原生分辨率下移动端可读
- [ ] 时间轴与语音一致 — 无过早或过晚的字幕
- [ ] 各条字幕互不重叠
- [ ] 描边/阴影在各种背景下对比度足够
