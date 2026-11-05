---
name: kling-official
description: OpenMontage 提供商场景下的 Kling 官方直连 API 指南。在调用 `kling_official_video`、`kling_official_image`、`kling_tts`、`kling_avatar` 或 `kling_lip_sync` 之前请先阅读。
metadata:
  openclaw:
    requires:
      env_any:
        - KLING_API_KEY
---

# Kling 官方直连 API

在 OpenMontage 中使用 `provider="kling_official"` 的工具时，请遵循本技能。这不是 fal.ai 的 Kling 网关。官方 Kling 使用 `KLING_API_KEY`、可选的 `KLING_API_BASE_URL`，以及 `Authorization: Bearer <KLING_API_KEY>`。

## 提供商分流

- `kling_video` 使用 fal.ai、`FAL_KEY`、fal.ai 队列 URL，以及 `provider="kling"`。
- `kling_official_video` 使用 Kling 官方 API、`KLING_API_KEY`、官方任务协议，以及 `provider="kling_official"`。
- `kling_official_image` 对图像生成使用相同的官方鉴权与任务协议。
- `kling_tts` 使用官方音频 TTS 端点，仍归属现有 `tts` 能力。
- `kling_avatar` 与 `kling_lip_sync` 使用官方数字人/口型同步端点，仍归属现有 `avatar` 能力。它们不会替代本地 `talking_head` 或 `lip_sync`。

切勿在这些路径之间静默切换。若所选提供商不可用，应明确阻塞原因并在替换前询问用户。

## 鉴权与端点

默认 base URL：

```text
https://api-singapore.klingai.com
```

用户可通过 `KLING_API_BASE_URL` 覆盖，例如使用区域端点。所有请求发送 JSON，并携带：

```text
Authorization: Bearer <KLING_API_KEY>
```

## 任务协议

Classic API：

- 创建任务 ID 路径：`data.task_id`
- 状态：`submitted`、`processing`、`succeed`、`failed`
- 结果路径：`data.task_result.videos[]`、`data.task_result.images[]`、`data.task_result.audios[]`

Turbo API：

- 创建任务 ID 路径：`data.id`
- 轮询路径：`GET /tasks?task_ids=<id>`
- 状态：`submitted`、`processing`、`succeeded`、`failed`
- 结果路径：`data[0].outputs[]`

解析器须分开实现。不要编写在 `task_id` 与 `id` 之间、或在 `succeed` 与 `succeeded` 之间猜测的模糊解析器。

## Omni 引用

Video Omni 与 Image Omni 通过现有提供商工具内的 `api_family="omni"` 完成。
不要在 selector 层创建 Omni 操作。

Video Omni 接受官方引用结构：

- `image_list[]`，含 `image_url` 及可选 `type`（如 `first_frame` 或 `end_frame`）。
- `video_list[]`，含 `video_url`、官方 `refer_type` 值（如 `feature` 或 `base`），以及可选 `keep_original_sound`。
- `element_list[]`，含官方 `element_id` 值。
- 结构化 `multi_prompt[]`；勿将自然语言自动拆成镜头。

本地图像引用可通过 `tools/_kling/media.py` 规范化。本地视频路径不得通过 fal.ai 静默上传；应要求或提供可访问的 URL。

Image Omni 接受 `image_list[]`，使用官方 `image` 字段值。提示词占位符（如 `<<<image_1>>>`）须与所提供图像顺序稳定映射。若提示词已含占位符，须校验所引用图像存在且勿重复插入。

## 能力边界

TTS、数字人与口型同步是对现有 OpenMontage 能力的提供商扩展。音效与视频特效是官方 Kling 端点，但在流水线具备稳定能力槽位之前，不会注册为默认 OpenMontage 工具。

- 不要在提供商实现内部新增 `sound_effects` 或 `video_effects` 能力。
- 不要让视频特效进入普通 `video_generation` selector 路径。
- 除非流水线明确消费该形态且工具的 `best_for` / `not_good_for` 如此说明，否则勿将短音效伪装成长背景音乐。

## 视频参数

用 `operation` 表达 OpenMontage 语义：

- `text_to_video`
- `image_to_video`
- `reference_to_video`

用 `api_family` 选择官方协议：

- `classic`
- `turbo`
- `omni`

重要约束：

- 官方视频提供商输入 schema 不得暴露顶层 `image_url`；应使用 `reference_image_url` 或 `reference_image_path`。
- Classic 图生视频接受 `reference_image_url`，或本地路径转换为 raw base64 后写入官方字段 `image`。
- Turbo 图生视频要求 URL 首帧。勿通过 fal.ai 上传本地文件作为回退。
- 仅在当前 schema 支持处发送 `aspect_ratio`：Classic 文生视频、Turbo 文生视频、Video Omni。
- 默认付费路径应避免 `4k`、原生音效或批量行为，除非显式选择。

## 图像参数

`api_family="generation"` 对应 `/v1/images/generations`；`api_family="omni"` 对应 `/v1/images/omni-image`。

生成/编辑路径：

- `prompt` 必填，且应低于官方 2500 字符限制。
- `image_url` 原样透传为官方 `image`。
- `image_path` 转为 raw base64 后作为官方 `image` 发送。
- `image_reference` 可为 `subject` 或 `face`。

Omni 路径：

- 在 `image_list[]` 中放置引用，使用官方 `image` 值。
- 仅当提示词需绑定特定引用图时使用 `<<<image_1>>>` 等占位符。

## TTS 参数

`kling_tts` 使用：

- `text`
- `voice_id`
- `voice_language`，当前为 `zh` 或 `en`
- `voice_speed`

除非已验证某账户专属默认音色，否则必须显式提供 `voice_id`。勿硬编码虚构音色。下载每条返回的音频，将 `data.output_path` 设为第一个本地文件，并包含 `voice_id`、`voice_language`、`voice_speed`、`task_id` 及非零 `cost_usd`。

## 数字人参数

`kling_avatar` 使用 `/v1/videos/avatar/image2video`，接受：

- 数字人图像：URL 或本地路径转 raw base64
- `audio_id` 或 `sound_file`
- 可选 `prompt`
- `mode`，如 `std` 或 `pro`

与本地 `talking_head` 保持分离。需要 Kling 数字人输出的流水线须显式列出并选择。

## 口型同步参数

`kling_lip_sync` 分两步：

1. `POST /v1/videos/identify-face`，传入 `video_id` 或 `video_url`；从 `data.face_data[]` 读取人脸
2. `POST /v1/videos/advanced-lip-sync`，传入 `session_id` 及一条 `face_choose[]` 项，含 `face_id`、`audio_id` 或 `sound_file`，以及音频起止/插入时间

本地视频路径不得通过 fal.ai 或其他提供商静默上传。若返回多张人脸且用户未传 `face_id` 或 `face_choose`，应停止并返回人脸列表供确认，除非显式设置了 `auto_select_face=True`。若自动选择，须在结果/制品中记录选择理由与所选人脸。

## 音效与视频特效

官方 Kling 音效（`/v1/audio/text-to-audio`、`/v1/audio/video-to-audio`）与视频特效（`/v1/videos/effects`）有意不作为默认 OpenMontage selector 工具。在文档/测试中记录未映射原因，而非注册当前流水线可能误用的工具。

## Elements 辅助

Elements 是 Kling Official 内部辅助能力，不是新的 OpenMontage 工具能力。
使用 `tools/_kling/elements.py` 规范化 `element_list[].element_id`、可选查询只读 element 端点，并在查询时记录 element 元数据。勿在默认提供商路径中创建或删除 element。

## 账户用量辅助

Account Usage 仅用于诊断。使用 `tools/_kling/account.py` 低频调用 `/account/costs`，配合本地缓存与节流保护。勿在每次生成前调用，勿放入 selector 或生产流水线阶段。

对于 `1101` 或 `1102`，应说明账户或资源包已耗尽，并附带 account-usage 诊断提示。

## 回调说明

提供商可接受 `callback_url`，但轮询仍是默认执行模式。

- Classic 与 Omni 路径在顶层传递 `callback_url`。
- Turbo 路径在 `options.callback_url` 中传递。
- 成功结果应记录 `callback_requested=true`、`polling_used=true`、`callback_url` 与 `task_id`。
- 发送前校验 callback URL；仅绝对 `http` 或 `https` URL 应通过。

## 错误处理

尽可能暴露官方 `code`、`message` 与 `request_id`。

勿重试：

- 鉴权失败：`1000`-`1004`
- 余额/资源包耗尽：`1101`、`1102`
- 权限/模型访问：`1103`
- 参数错误：`1200`、`1201`
- 安全策略：`1301`

以下情况可有限重试：

- `1302` 请求过快
- `1303` 并发/资源包槽位限制
- `5000`、`5001`、`5002` 服务器/维护/积压错误

对于 `1303`，应说明账户触发了并发或资源包槽位限制。

## 成本治理

官方 Kling 是付费远程 API。提供商工具须从 `estimate_cost()` 返回非零保守估计，并在成功付费结果中包含 `cost_usd`。在实现账户用量对账之前，将估计视为低置信度。
高成本 Omni 输入（多引用、element ID、`result_type="series"`、`mode="4k"`、`sound="on"`）须提高或标记成本估计。

## 提示词说明

视频方面，从 OpenMontage 通用视频提示词骨架出发：主体、主体运动、场景、空间构图与镜头。Kling 对清晰的时间动作顺序、镜头运动动词以及简洁负向提示响应较好。引用工作流中，应说明引用中须保持一致的内容与须变更的内容。
