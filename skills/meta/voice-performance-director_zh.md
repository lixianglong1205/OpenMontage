# 语音表演指导（Voice Performance Director）

当流水线将使用 TTS 生成旁白时，请使用本元技能（meta skill）。

目标是让生成的旁白听起来像被「导演过」，而不只是被朗读。不要在提示里把表现力留成「自然朗读」。从脚本到资产生成，全程携带一份具体的语音表演计划，并用样片验证。

## 必备约定

每条以旁白为主的脚本都应包含顶层 `voice_performance` 对象，并在模式允许时为各段落提供 `delivery_cues`。

顶层语音表演：

```json
{
  "performance_intent": "Warm, decisive product narrator with human pauses.",
  "pacing_profile": "conversational",
  "energy_curve": "measured hook, warmer middle, more deliberate close",
  "pause_policy": "Use short pauses after setup lines and longer pauses before reversals or important claims.",
  "provider_notes": {
    "openai": "Use instructions for emotional arc and emphasis.",
    "google_tts": "Use SSML input with break tags when the selected voice supports it.",
    "elevenlabs": "Use lower stability and moderate style for expressive narration."
  }
}
```

段落级 delivery cues：

```json
{
  "pace": "measured",
  "energy": "curious",
  "emphasis_words": ["not", "process"],
  "pause_before_seconds": 0.2,
  "pause_after_seconds": 0.7,
  "delivery_note": "Set up the contrast, then slow down on the final phrase.",
  "provider_text": "This is not just another tool. <break time=\"0.6s\"/> It is a process."
}
```

## 写作规则

- 写口语，不写论文体。优先短句、适度缩写和清晰标点。
- 用停顿当结构。在转折前、惊人论断后、以及最终要点前加入停顿。
- 停顿标记要有目的。过多 break 会显得舞台腔且拖沓。
- 避免空泛指令，如「natural」「engaging」「expressive」，除非同时给出具体的 pace、emphasis、pause 或 energy 提示。
- 每段只承载一种 delivery 意图。若一段需要三次情绪转折，请拆段。

## 供应商映射

- OpenAI TTS：发送 `instructions` 时使用 `model: "gpt-4o-mini-tts"`。把情绪弧线、节奏、重音和角色写进 `instructions`；输入文本保持干净但标点完整。不要向 `tts-1` 或 `tts-1-hd` 发送 `instructions`。
- Google TTS：仅在添加 break 标签或其他 SSML 时使用 `input_type: "ssml"`。工具会映射到 Google 的 `input.ssml`，并在需要时用 `<speak>...</speak>` 包裹整句。`speaking_rate` 保持在 Google 支持的 `0.25..2.0`，pitch 在 `-20..20`。
- ElevenLabs：较低 `stability` 以增加变化，适中 `style` 以提升表现力，`speed` 落在供应商的 `0.7..1.2`，`similarity_boost` 足够高以保留音色。
- 离线/基础音色：依赖标点、更短句子和显式分段，因为可能没有供应商级情绪控制。

## 样片门禁

批量生成旁白之前：

1. 从对表演最敏感的一段生成样片，不必默认第一段。
2. 验证音色、节奏、停顿、重音和情绪弧线。
3. 若样片平淡，在生成其余内容前调整 `voice_performance` 计划或供应商参数。
4. 在资产清单中记录已批准的样片路径与供应商设置。

## 失败条件

以下视为质量失败：

- 以旁白为主的脚本没有 `voice_performance` 计划。
- 段落方向仅写「自然朗读」或「有表现力」，没有具体的 pause、emphasis、pace 或 energy 提示。
- 样片批准后更换 TTS 供应商、音色、语速或模型，却未重新做样片。
- 存在结构化 `provider_text` 或 `delivery_cues` 时，最终旁白仍从原始脚本文本生成。
