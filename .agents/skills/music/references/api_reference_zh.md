# Music API 参考

## 目录

- [compose](#compose)
- [composition_plan.create](#composition_plancreate)
- [compose_detailed](#compose_detailed)
- [upload](#upload)
- [Error Handling](#error-handling)

## compose

根据文本提示生成音乐。返回音频流。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| `prompt` | string | 是* | 期望音乐的描述 |
| `composition_plan` | object | 是* | 预定义的创作计划（与 `prompt` 二选一） |
| `music_length_ms` | integer | 否 | 使用 `prompt` 时的时长（毫秒，3,000–600,000）；省略时由模型自行决定 |
| `model_id` | string | 否 | 默认为 `music_v1` |
| `force_instrumental` | boolean | 否 | 保证输出为纯器乐（仅 prompt 模式） |
| `respect_sections_durations` | boolean | 否 | 严格按创作计划中各段的 `duration_ms` 执行 |

*须提供 `prompt` 或 `composition_plan` 之一，不可同时提供。

### Python

```python
audio = client.music.compose(
    prompt="An upbeat electronic track with synth leads",
    music_length_ms=30000
)

with open("output.mp3", "wb") as f:
    for chunk in audio:
        f.write(chunk)
```

### JavaScript

```javascript
const audio = await client.music.compose({
  prompt: "An upbeat electronic track with synth leads",
  musicLengthMs: 30000,
});

const writeStream = createWriteStream("output.mp3");
audio.pipe(writeStream);
```

### 使用创作计划

```python
plan = client.music.composition_plan.create(
    prompt="A jazz ballad with piano and saxophone",
    music_length_ms=60000
)

# Modify the plan as needed
audio = client.music.compose(
    composition_plan=plan,
    music_length_ms=60000
)
```

## composition_plan.create

根据提示生成结构化创作计划，以便在生成音频前进行细粒度控制。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| `prompt` | string | 是 | 音乐描述 |
| `music_length_ms` | integer | 是 | 时长（毫秒） |

### 响应结构

```json
{
  "positiveGlobalStyles": ["jazz", "smooth", "warm"],
  "negativeGlobalStyles": ["aggressive", "distorted"],
  "sections": [
    {
      "name": "Intro",
      "localStyles": ["soft", "building"],
      "duration_ms": 15000,
      "lines": [
        { "text": "Instrumental intro", "type": "instrumental" }
      ]
    }
  ]
}
```

### Python

```python
plan = client.music.composition_plan.create(
    prompt="A peaceful ambient track with nature sounds",
    music_length_ms=60000
)

# Inspect and modify the plan
print(plan.positiveGlobalStyles)
for section in plan.sections:
    print(f"{section.name}: {section.duration_ms}ms")
```

## compose_detailed

生成音乐，并同时返回创作计划、元数据与音频。

### 返回值

| 字段 | 说明 |
|-------|-------------|
| `json` | 创作计划 + 歌曲元数据（如适用则含歌词） |
| `filename` | 输出文件标识 |
| `audio` | 音频字节 |

### Python

```python
result = client.music.compose_detailed(
    prompt="A pop song about summer adventures",
    music_length_ms=120000
)

# Access the composition plan and metadata
print(result.json)

# Save the audio
with open(result.filename, "wb") as f:
    f.write(result.audio)
```

## upload

上传音乐文件，供后续 inpainting 工作流使用。该端点面向具备 inpainting 功能的企业客户。

### 参数

| 参数 | 类型 | 必填 | 说明 |
|-----------|------|----------|-------------|
| `file` | file | 是 | 待上传的音频文件 |
| `extract_composition_plan` | boolean | 否 | 为 `true` 时，响应包含提取的创作计划，返回可能更慢 |

### 返回值

| 字段 | 说明 |
|-------|-------------|
| `song_id` | 已上传歌曲的唯一标识 |
| `composition_plan` | 提取的创作计划；未启用 `extract_composition_plan` 时为 `null` |

### Python

```python
client.music.upload(
    file="example_file",
)
```

### cURL

```bash
curl -X POST "https://api.elevenlabs.io/v1/music/upload" \
  -H "xi-api-key: $ELEVENLABS_API_KEY" \
  -F "file=@<file1>"
```

## Error Handling

### bad_prompt

当提示涉及受版权保护的内容（特定艺人、乐队或受版权保护的歌词）时触发。错误响应包含 `prompt_suggestion`，提供替代表述建议。

```python
try:
    audio = client.music.compose(
        prompt="A song like Beatles",
        music_length_ms=30000
    )
except Exception as e:
    print(f"Request failed: {e}")
```

### bad_composition_plan

当创作计划包含受版权保护的风格时返回。错误中包含带修正风格的 `composition_plan_suggestion`。对有害内容不提供建议。

### 常见 HTTP 错误

| 代码 | 含义 |
|------|---------|
| 401 | API 密钥无效 |
| 422 | 参数无效 |
| 429 | 超出速率限制 |
