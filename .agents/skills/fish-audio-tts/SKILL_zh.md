---
name: fish-audio-tts
description: 使用 fish.audio（S1 / S2 代模型）生成富有表现力、多语言旁白，并通过 reference_id 复用克隆音色。适用于用户偏好 fish.audio/Fish Audio TTS、需要指定 playground 语音模型，或需要高情感语音克隆旁白的场景。
---

# fish.audio TTS

需在 `.env` 中配置 `FISH_AUDIO_API_KEY`（在 https://fish.audio/go-api/api-keys/ 创建）。
在 fish.audio playground 中创建语音模型，将其 id 作为 `reference_id` 传入即可复用克隆音色。

## 当前 API

单次同步调用，返回原始音频字节：

```text
POST https://api.fish.audio/v1/tts
Authorization: Bearer ${FISH_AUDIO_API_KEY}
Content-Type: application/json
model: <backend model>     # HTTP header selects the backend, e.g. s1
```

后端模型通过 `model` **HTTP 头**选择，而非请求体字段。在 OpenMontage 中对应工具的 `model` 输入。

## 后端模型

`model` **必填——无默认值**。传入以下之一：

- `s2.1-pro` — 最新一代。质量最佳：内联情感标签、80+ 语言、多说话人。适合主旁白。
- `s2.1-pro-free` — **促销**免费使用 s2.1-pro。仅在促销期内以 $0 做草稿、样片与验证运行。据 [fish.audio 公告](https://fish.audio/ko/blog/s2-1-pro-free-api/?articleLocale=en)：免费至 2026 年 8 月 31 日，受 Fair Use 约束、无 SLA/延迟保证、请求可能被保留，且商业使用受限。切勿将生产或客户旁白路由到此模型。
- `s2-pro` — S2 第一代。稳定高质量，支持情感标签。
- `s1` — 上一代旗舰。保留以兼容现有集成。

计费按**输入文本的 UTF-8 字节数**（非字符数）。CJK 文本与 emoji 的可见长度相同时，成本约为 ASCII 字符的 3–4 倍。当前标价：`s1` / `s2-pro` / `s2.1-pro` = 每 100 万字节 $15；`s2.1-pro-free` 仅在促销期内 $0（2026 年 8 月 31 日后工具的 `estimate_cost()` 会切换为付费 `s2.1-pro` 费率）。大批量前请在 https://docs.fish.audio/developer-guide/models-pricing/pricing-and-rate-limits 核对最新价格。

## 内联情感标签（仅 S2 模型）

`s2-pro` / `s2.1-pro` / `s2.1-pro-free` 会解析文本中嵌入的内联情感标签：

- 如 `[laugh]`、`[whispers]` 等标签可在句中改变表达方式。
- 示例：`"That's hilarious [laugh] but let me explain seriously."`
- `s1` 不解析情感标签——可能被当作普通文本读出，面向 s1 时应剥离这些标签。

## 音色选择（reference_id）

- 在 fish.audio playground 中创建或选择音色，复制其模型 id。
- 作为 `reference_id` 传入。当未提供 `reference_id` 时，选择器的通用 `voice_id` 可作为别名接受。
- 无 `reference_id` 时，fish.audio 使用所选模型的默认音色。

本工具**不支持**请求内即时克隆（每次上传参考音频 + 文本）——请先在 playground 创建语音模型。

## OpenMontage 用法

通过 TTS 选择器生成：

```python
from tools.audio.tts_selector import TTSSelector

result = TTSSelector().execute({
    "preferred_provider": "fish_audio",
    "text": "Here's why compound interest quietly beats every get-rich-quick scheme.",
    "model": "s1",
    "reference_id": "<playground voice model id>",
    "output_path": "projects/my-video/assets/audio/narration.mp3",
})
```

或直接调用 provider：

```python
from tools.audio.fish_audio_tts import FishAudioTTS

result = FishAudioTTS().execute({
    "text": "Short sample line for approval.",
    "model": "s1",
    "reference_id": "<playground voice model id>",
    "output_path": "projects/my-video/assets/audio/fish_sample.mp3",
})
```

provider 将音频写入 `output_path`，并返回 `data.output` 以及解析后的 `model` 与 `reference_id`。

## 质量与延迟调优

- `latency`：`normal`（默认，质量最佳）、`balanced`（略快）或 `low`（最快，质量略降）。
- `normalize`：默认 `true`；保持开启以便数字、日期、货币自然朗读。
- `prosody`：可选 `{ "speed": 1.0, "volume": 0 }` 微调语速/响度。
- `mp3_bitrate`：`128` 为常用默认；混有较多音乐 bed 时可提高到 `192`。
- `temperature`：默认 `0.7`。向 `0.9` 提高可获得更富表现力的朗读（配合情感标签时推荐）；降低则更稳定、可预测。
- `top_p` / `repetition_penalty`：通常保持默认（`0.7` / `1.2`）。

## 推荐工作流

1. 在完整付费旁白前，用选定的 `model` + `reference_id` 生成 10–15 秒样片。
2. 请用户确认音色自然度、情感与语速。
3. 确认后再生成完整旁白。
4. 批量/本地化且成本敏感时，可在 `s2.1-pro-free` 上原型（促销期 $0；仅非商业草稿），定稿升级到 `s2.1-pro`。

## 故障排查

- `401 Unauthorized`：`FISH_AUDIO_API_KEY` 错误或缺失。
- `402` / 支付错误：账户额度用尽。
- `404` / 音色错误：`reference_id` 错误或不在本账户下。
- 音频为空/过短：检查 `text` 非空，且 `normalize` 未把整个输入剥空。

## 安全

切勿将 API key 打印或写入日志、元数据、补丁或项目产物。`.env.example` 中应只保留空变量名。
