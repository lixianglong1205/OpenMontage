# Lyria 3 API 与提示词参考

最后验证日期：2026-07-18。

## 提供商系列

### Lyria 3 Clip

- 模型：`lyria-3-clip-preview`
- 最适合：提示词迭代、预览、循环、短片段
- 输入：文本或图像
- 输出：MP3 音频，以及包含歌词或歌曲结构的文本
- 时长：固定 30 秒
- Gemini Developer API 价格：每次请求 $0.04；无免费层

### Lyria 3 Pro

- 模型：`lyria-3-pro-preview`
- 最适合：完整歌曲、人声、主歌、副歌、桥段、较长配乐
- 输入：文本，或通过底层 API 最多 10 张图像
- 输出：默认 MP3；底层 Pro API 可请求 audio/WAV 响应格式
- 时长：受提示词影响，最长约三分钟；并非精确的媒体契约
- Gemini Developer API 价格：每次请求 $0.08；无免费层

### Lyria RealTime

- 模型：`lyria-realtime-exp`
- 实验性、纯器乐、持久 WebSocket 会话
- 支持持续调节 BPM、音阶、密度、亮度与 guidance
- 非 Interactions API，也不是 OpenMontage `google_music` 所使用的模型

## Interactions API 结构

Python：

```python
from google import genai

client = genai.Client()
interaction = client.interactions.create(
    model="lyria-3-pro-preview",
    input="A structured instrumental score ...",
)

audio = interaction.output_audio
text = interaction.output_text
```

对于普通响应，优先使用上述便捷属性。对于交错响应，遍历 `interaction.steps`；检查 `model_output` 内容块，并将 `audio` 与 `text` 块分开处理。

OpenMontage 适配器当前：

- 发送包含一个文本块、以及可选的一个图像块的列表；
- 在文本末尾追加 `[Target Duration: N seconds]`；
- 使用 `lyria-3-pro-preview` 调用 `client.interactions.create()`；
- 依次通过 `output_audio`、旧版 outputs、步骤遍历提取音频；
- 写入 MP3，并报告请求的时长，而不探测实际结果。

## 提示词模板：视频配乐

```text
Create an original instrumental background score for [purpose], target [N] seconds.

Style: [genre/blend/era], [mood], [foreground or background role].
Tempo and harmony: [BPM], [meter], [key/scale or tonal behavior].
Instrumentation: [lead], [rhythm], [bass], [texture].

[0:00-0:06] [one musical state and entrance rule].
[0:06-0:12] [one development].
[0:12-0:15] [build or reduction that prepares the sync point].
[0:15-0:18] [exact synchronization event and required hold].
[0:18-0:30] [release and ending behavior].

Mix: [density, space, transient character, dynamic range].
Ending: [tail, final resonance, no abrupt cutoff].
Instrumental only. No vocals, speech, choir, humming, vocal chops,
spoken samples, lyrical fragments, or recognizable quotations.
Avoid: [unwanted instruments, clichés, oversized hits, abrupt fade].
```

将时间戳用作结构说明，而非 Pro 会返回精确长度文件的保证。

## 提示词模板：带自定义歌词的歌曲

```text
Create a [duration] [genre] song in [key] at [BPM].
Vocal profile: [range, tone, delivery, language].
Instrumentation and production: [details].
Structure: [Intro], [Verse], [Chorus], [Bridge], [Outro].

Lyrics:
[Verse 1]
...

[Chorus]
...
```

将歌词与制作方向分开。仅当需要背景和声回声时使用圆括号。

## 人声与自定义歌词

除非提示词明确要求纯器乐，否则 Lyria 会生成人声与歌词。Google 建议提供详细的歌手画像，涵盖声部类型或性别呈现、音色与音域。模型以提示词所用语言生成歌词，明确的语言指令可覆盖该默认行为。

对于带人声的歌曲，请指定：

- **角色：** 独唱主唱、二重唱、呼应式对唱、背景和声组，或无词纹理。
- **画像：** 音域、音色、演绎方式、咬字、强度、装饰音与换区变化。
- **语言：** 演唱语言、预期语域，以及是否允许语码转换。
- **段落映射：** 人声从何开始、和声从何进入、哪段为器乐、人声如何结束。
- **背景策略：** 仅对有意设计的回声或背景和声使用括号。
- **排除项：** 不需要的合唱、口语短语、即兴 ad-lib、哼唱、人声切片，或模仿具名艺人。

将制作方向保留在歌词块之外：

```text
Create a [duration] [genre] song in [key] at [BPM].
Vocal role: [solo, duet, call-and-response, or ensemble].
Singer profile: [range], [timbre], [delivery], and [diction].
Sing in [language and intended register]. Use backing vocals only for words
shown in parentheses. No [unwanted vocal gestures or effects], and do not
imitate a named singer.

Lyrics:
[Verse 1]
[custom lyrics in the selected language and script]

[Chorus]
[lead line] ([intentional backing-vocal echo])
```

### 多语言工作

- 即使自定义歌词已表明语言，仍应明确写出演唱语言。
- 审慎选择书写系统或转写方式；未经用户同意不要转换文字系统。
- 在同一歌词版本中保持单一文字系统，避免模型推断意外的语言切换。
- 描述预期语域、方言、正式程度及任何有意的语码转换。
- 将已批准的歌词文本与生成提示词分开保存。Lyria 可能改动、省略或重复词句，因此须将返回文本与可听表现同该源文本对照。
- 将发音与语言覆盖视为输出级 QA。API 文档称 Lyria 遵循提示词语言，但并不保证每种语言或地区语域的发音都完美。

### 人声 QA

试听并记录：

1. 请求的主唱、二重唱或组和声角色是否出现。
2. 每条已批准歌词行是否被演唱、省略、改动或重复。
3. 语言、由文字系统推导的发音与预期语域是否一致。
4. 请求的音域、音色、动态、装饰音与段落进入是否被遵循。
5. 背景和声是否仅出现在请求处。
6. 主唱在编曲中是否清晰可辨，且无削波或掩蔽。
7. 结尾是否包含完整的最后乐句与音乐上有用的衰减。

不要将咬字或歌词 adherence 失败归类为文件格式问题。这是随机的提示词/ adherence 失败；任何重试都是新的付费生成，须遵循已批准的重试策略。

## 图像转音乐

底层 API 接受最多 10 张带 MIME 类型的 base64 编码图像。在提示词中明确音乐诠释：情绪、色板到音色的映射、运动到节奏的映射，以及期望结构。当前 OpenMontage 适配器接受一个 `image_path` 或一个 `image_url`。

## 限制与安全

- 生成为随机过程；相同提示词可能产生不同结果。
- Lyria 3 为单轮；当前无法通过多轮编辑链对已生成音轨进行精修。
- 安全过滤器可能拒绝模仿艺人声线、受版权歌词或其他受限内容。
- 所有生成音频均包含不可察觉的 SynthID 水印。
- 预览模型与速率限制在稳定版发布前可能变更。
- 官方页面对 44.1 kHz 与 48 kHz 的描述目前不一致。请探测每个返回文件并记录观测值。

## 故障分类

| 症状 | 类别 | 操作 |
|---|---|---|
| `401` 或无效密钥 | 认证 | 验证所选凭证，勿打印其内容 |
| `403`、`API_KEY_SERVICE_BLOCKED` | 认证/项目策略 | 停止重试；修复 Google 密钥、项目、API 启用或服务限制 |
| `429` | 速率限制 | 仅在已批准的重试/预算策略内重试 |
| 超时 | 瞬时/提供商 | 使用工具超时策略；勿并行发起重复的付费调用 |
| 无 `output_audio` | 响应解析 | 遍历 `model_output` 步骤内容查找 `audio` 块 |
| 输出长于/短于请求 | 模型行为 | 保留源文件、探测，并单独制作精确时长的母版 |
| 意外人声 | 提示词/adherence | 加强完整纯器乐排除列表；试听下一次付费结果 |
| 安全拒绝 | 策略/提示词 | 移除艺人模仿或受版权材料；勿伪装请求 |

## 官方来源

- Gemini API 音乐生成：https://ai.google.dev/gemini-api/docs/music-generation
- Gemini Interactions API：https://ai.google.dev/gemini-api/docs/interactions-overview
- Gemini Developer API 定价：https://ai.google.dev/gemini-api/docs/pricing
- Google DeepMind Lyria 提示词指南：https://deepmind.google/models/lyria/prompt-guide/
- Lyria RealTime：https://ai.google.dev/gemini-api/docs/realtime-music-generation
- Lyria 3 Pro 的 Google 公告：https://blog.google/innovation-and-ai/technology/ai/lyria-3-pro/
