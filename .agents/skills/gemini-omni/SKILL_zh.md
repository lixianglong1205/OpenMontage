---
name: gemini-omni
description: |
  使用稳定的 Google Gemini Omni Flash（`gemini-omni-1.1-flash`）生成并以对话方式编辑短视频。适用场景：(1) 用自然语言迭代编辑片段而非重新生成（「让手机消失，其余保持不变」），(2) 生成 3–10 秒 720p 带合成音频、屏幕渲染文字或时间码节拍的片段，(3) 用 <FIRST_FRAME>/<IMAGE_REF_N> 提示标签将参考图绑定到角色，(4) 编辑已上传的现有视频。通过 `gemini_omni_video` 工具访问，使用项目的 GEMINI_API_KEY/GOOGLE_API_KEY — 与 Imagen 和 Google TTS 同一密钥。
allowed-tools: Bash, Read, Write
metadata:
  openclaw:
    requires:
      env_any:
        - GEMINI_API_KEY
        - GOOGLE_API_KEY
---

# Gemini Omni Flash (Google DeepMind)

Gemini Omni 是 Google DeepMind 的视频**生成与编辑**模型系列。OpenMontage 直接适配器通过 Gemini **Interactions API** 使用已全面提供的 **Gemini Omni 1.1 Flash** 模型（`gemini-omni-1.1-flash`）。其实现基线可生成 3–10 秒、720p/24fps 且带合成音频的片段。在 OpenMontage 能力矩阵中的差异化能力是**有状态对话式编辑**：每次存储的生成会返回 `interaction_id`，后续调用传入 `previous_interaction_id` 即可就地编辑该视频 — 其他封装提供商均无法在不全量重生成的情况下精修片段。

OpenMontage 将其封装为 `gemini_omni_video`（原生 Gemini API，无网关）。与 `google_imagen`、`google_tts` 共用 `GOOGLE_API_KEY`/`GEMINI_API_KEY` — 一把密钥，三种能力。仅付费档：约 $0.10/秒输出视频（精确为 5,792 输出 token/秒 × $17.50/1M，不含输入及任何文本/思考输出）。

当未选择直接 Google 密钥作为提供商时，还可使用其他已文档化路由：

| 路由 | OpenMontage 调用 | 重要限制 |
|-------|------------------|----------------------|
| fal.ai | `gemini_omni_fal` | T2V、I2V、参考视频与编辑端点；不返回 Google interaction ID |
| Runway | `runway_video`, `model: "gemini_omni_flash"` | T2V/I2V/V2V；视频编辑最多接受五张参考图 |
| ComfyUI Partner Node | 本适配器中非稳定的 1.1 回退 | 现有 `GeminiVideoOmni` 映射指向旧版预览节点；在宣称 Omni 1.1 支持前需单独迁移至 `GeminiVideoOmniV2` |

有状态对话式编辑请使用直接 `gemini_omni_video` 路由。网关路由返回普通提供商任务，无法保留 Google 的 `previous_interaction_id` 工作流。fal 编辑端点仍可通过将每次输出视频 URL 作为下一次编辑调用的输入来迭代。

## 何时选用（以及何时不选）

| 适合用于 | 更宜选用其他提供商 |
|---|---|
| 迭代精修 — 生成、审阅后分层编辑同一片段 | 一次性电影感主视觉片段（→ Seedance 2.0，见 `seedance-2-0`） |
| 编辑现有/已上传片段（改风格、增删物体、改文字） | 超过 10 秒或高于 720p 的片段 |
| 屏幕渲染文字与逐词文字节拍 | 可种子复现的生成（不支持 seed） |
| 通过提示标签绑定参考图的主体/风格 | 首尾帧插值（→ `veo_video`） |
| 单条提示内时间码编排的多节拍片段 | 非英语旁白（仅英语完全支持） |

生成类操作请经 `video_selector` 路由。**编辑（`edit_video`）为直接工具操作** — 从 registry 调用 `gemini_omni_video`，因多轮 interaction 状态在 selector 模型之外。

## 计费与时长提示

- `duration` 仅为调用方的规划/提示用途。适配器不会将其发给 Google；在提示或时间码中表达节奏，由模型决定实际长度。它不会封顶计费。
- 当响应含有效 `usage` 时，`ToolResult.cost_usd` 按：输入 token 各模态均为 $1.50/1M，输出文本 $9.00/1M，输出视频 $17.50/1M。未知/未分类输出及单独上报的思考 token 按较高 $17.50/1M 计，避免低估。
- 无有效 usage 时，回退假设最长 10 秒输出：`10 × 5,792 × $17.50/1M = $1.0136`，另加提示与可用媒体输入 token 的保守上限估计。较短的 `duration` 提示不会降低该回退值。

## 生成提示

描述 **场景 + 镜头 + 光照 + 运动 + 音频**。官方示例：

> Continuous, unbroken handheld shot of a fluffy tabby cat sitting on a sunny windowsill, looking out into a leafy garden. The cat's tail twitches slowly, and its ears rotate slightly toward ambient noises. Sunbeams illuminate dust motes in the air.

- **明确强制单镜头**：「In a single continuous shot,」/「No scene cuts.」否则模型可能在场景间切镜。
- **否定意图写在散文里** — 无 `negative_prompt` 参数：「No dialogue,」「No extra sound effects.」
- **无采样器控制**：系统指令、temperature、top_p、seed 均不支持。提示是唯一杠杆。
- **质量元提示**：「Consider micro-detail, expression and timing to create a very rich, detailed but entirely natural scene.」

### 时间码语法

用方括号区间或自然语言编排节拍 — 可直接映射到 OpenMontage 场景规划时间：

```
[0-3s] A person is walking [3-6s] They stop and turn around
```

> "After 3 seconds, a woman enters the scene." / "At 5s the chorus starts in the background audio."

### 音频与屏幕文字

音频自动合成；在提示中指挥：「Include calm background music,」「The audio is a low tinny radio broadcast in the background.」渲染文字可用且可定时：

> One word on the screen at a time: 'did, you, know, that, Omni, can, do, awesome, text?' Each word appears for 1s.

## 参考图（`<FIRST_FRAME>` / `<IMAGE_REF_N>` 标签）

经 `reference_image_paths` 传入本地图片（按顺序发送），再在**提示内**用标签绑定角色。`<IMAGE_REF_N>` 从 0 起按所供顺序编号：

```
in the style of <IMAGE_REF_0> a woman <IMAGE_REF_1> is walking
```

```
[0-3s] A studio fashion sequence. Starting with woman <IMAGE_REF_0>, she is
holding <IMAGE_REF_1> [3-6s] Then we see the man <IMAGE_REF_2> holding <IMAGE_REF_3>
```

- `<FIRST_FRAME>` 将某图作为开场帧：`<FIRST_FRAME> a woman is walking`。
- 使用高分辨率图片；具体描述 intended 运动，而非「make it move」。
- 说明每张图*是什么*（产品/角色/风格/背景参考）— 模型根据上下文决定用法。

## 对话式编辑（差异化能力）

**编辑提示与生成提示相反：短而精准。** 过于冗长的编辑提示会导致非预期改动。

1. 生成基础片段（主体 + 场景 + 运动）。工具在结果数据中返回 `interaction_id`。
2. 将其作为 `previous_interaction_id` 传回，并设 `operation="edit_video"`，**仅描述增量**。
3. 追加 **「Keep everything else the same.」** 以固定未提及元素。
4. 分层精修 — 一轮改光照、一轮改镜头、一轮改动作、一轮改音频。

官方好/坏示例：

| 避免 | 改为 |
|---|---|
| "In the video of the man sitting on the sofa, please add a small black cat..." | "Add a cat that jumps onto his lap, he begins to pet it. Keep everything else the same." |
| "Please remove the cell phone... and fill in the background so it looks like..." | "Make the phone invisible. Keep everything else the same." |

其他可用编辑提示：「Make this video anime」/「Put a fashionable hat on this person」/「Change the lighting to be more dramatic」/「Change the text on the sign to say 'Omni Flash'」。

**注意 — `store`：** 经 `previous_interaction_id` 编辑仅当*上一次*调用在服务端保留 interaction 时有效（`gemini_omni_video` 中 `store` 默认为 true）。仅对永不再编辑的一次性生成设 `store=false`。

**下载恢复：** 已接受的付费生成之后，Files API 轮询或下载仍可能失败。此时工具返回 `output_uri`、在返回有效 usage 时基于 usage 的计费（否则为保守回退），以及 `resume_download` 载荷。将该载荷传回 `gemini_omni_video` 以仅重试现有文件的 GET/轮询流程；不得再次提交付费生成。

**编辑已上传视频：** 传 `input_video_path` 而非 `previous_interaction_id`；工具经 Files API 上传。在 EEA、瑞士与英国不可用（*生成*视频的编辑全球可用）。

## 当前适配器限制（稳定模型）

- 输出：3–10s、720p、24fps、带音频 MP4；宽高比 `16:9` 或 `9:16`。所有输出含不可见 SynthID 水印。
- 无 seed、negative prompt、temperature、top_p 或系统指令。
- 稳定 Google 模型支持视频延长、首尾帧插值及更高分辨率，但本 OpenMontage 适配器尚未实现这些控制。勿将其宣传为可用的直接工具能力。不支持语音编辑。
- 不支持音频参考输入。≤3s 的视频参考虽被 schema 接受但**未正确处理** — 勿依赖。
- 不支持多视频提示；可能降低输出质量。
- 英语完全支持；其他语言未充分测试。
- 未成年人图像（EEA/CH/UK）及某些可识别人物在上传/编辑时被拦截。

## 来源

- 生成与编辑指南：https://ai.google.dev/gemini-api/docs/omni
- 模型卡片：https://ai.google.dev/gemini-api/docs/models/gemini-omni-flash
- 定价：https://ai.google.dev/gemini-api/docs/pricing
- 公告：https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-omni/
