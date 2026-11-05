---
name: atlas-cloud
description: 通过 Atlas Cloud 网关生成或编辑图像与视频。适用于 Atlas 托管的 Seedance 2.5/2.0、Gemini Omni Flash、MiniMax H3、Seedream 5.0、GPT Image 2、Nano Banana 2，或当一把 ATLASCLOUD_API_KEY 需访问多种媒体模型家族时。
---

# Atlas Cloud

将完整制作流程路由至 `image_selector` 或 `video_selector`。当用户明确指定 Atlas Cloud 或某一精确 Atlas 模型时，直接调用 `atlas_image` 或 `atlas_video`。切勿用直连厂商端点替代 Atlas 请求。

设置 `ATLASCLOUD_API_KEY`。为兼容起见，也接受别名 `ATLAS_CLOUD_API_KEY` 与 `ATLAS_API_KEY`。

## 每次付费调用前的前置检查

1. 读取 `tool.get_info()["model_catalog"]`；勿从搜索集合推断可用性，也不要臆造任务后缀。
2. 从该目录中选择精确模型 id 及该模型支持的操作。
3. 提交前声明 Atlas 工具、提供商、精确模型、请求次数与预估费用。
4. 方便时使用本地路径输入；工具会通过 Atlas 上传。
5. 将输出保存于当前 `projects/<project-id>/` 目录树内并检查。

## 视频路由

| 家族 | 操作 | 精确路由说明 |
|---|---|---|
| Seedance 2.5 | text, image, reference | `bytedance/seedance-2.5/{text,image,reference}-to-video`；图像模式使用 `image` 及可选 `last_image`；参考模式最多 30 张图、10 段视频、10 段音频（含纯音频）；4–30 秒；$0.134/s |
| Seedance 2.0 | text, image, reference | `bytedance/seedance-2.0/{text,image,reference}-to-video`；4–15 秒；$0.112/s |
| Gemini Omni Flash | text, image, reference, video edit | 标准路由为 `google/gemini-omni-flash/...`；开发者路由仅支持 text/image/reference。标准图像模式使用单张 `image`；标准参考模式使用 `images`；开发者参考模式需一个 `video_clips` 对象。 |
| MiniMax H3 | text, image, reference | `minimax/h3/{text,image,reference}-to-video`；图像模式支持可选 `end_image`；参考模式需要 `refers` 对象；4–15 秒；768P/2K；$0.10/s |

使用规范的 OpenMontage 字段：

```python
tool.execute({
    "prompt": "...",
    "model": "minimax/h3/reference-to-video",
    "operation": "reference_to_video",
    "duration": 10,
    "resolution": "2K",
    "reference_images": ["projects/demo/character.png"],
    "reference_audios": ["projects/demo/performance.wav"],
    "output_path": "projects/demo/h3.mp4",
})
```

Gemini 开发者参考视频需传入带 `url`、`start` 与 `ends` 的 `video_clips` 对象。H3 调用方可传入规范化后的 `reference_images`、`reference_videos` 与 `reference_audios`；工具会将其转换为 `refers`。

勿静默截断时长、分辨率或宽高比。无效值必须在计费前失败，并在错误中列出支持的选项。

## 图像路由

| 家族 | 操作 | 精确路由说明 |
|---|---|---|
| Seedream 5.0 Pro | generate, edit, decompose | `bytedance/seedream-v5.0-pro/text-to-image`、`/edit`、`/layer-decomposition`；编辑最多 10 张图；尺寸使用 `WIDTH*HEIGHT` |
| Seedream 5.0 Lite | edit | `bytedance/seedream-v5.0-lite/edit`；不假定存在可用的 Lite 文生图兄弟模型；最多 14 张图 |
| GPT Image 2 | generate, edit | `openai/gpt-image-2/text-to-image`、`/edit`；尺寸使用 `WIDTHxHEIGHT`；编辑最多 10 张图 |
| Nano Banana 2 | generate, edit | `google/nano-banana-2/text-to-image`、`/edit`；使用宽高比加 1k/2k/4k 分辨率；编辑最多 14 张图 |

将 `generation_mode` 设为 `generate`、`edit` 或 `decompose`。源图可通过 `image_path`、`image_paths`、`image_url` 或 `image_urls` 提供。

```python
tool.execute({
    "prompt": "Replace the packaging with matte cobalt glass; preserve the logo",
    "model": "google/nano-banana-2/edit",
    "generation_mode": "edit",
    "image_paths": ["projects/campaign/source.png"],
    "resolution": "2k",
    "output_path": "projects/campaign/revised.png",
})
```

## 结果与失败约定

两个工具均提交至 Atlas，轮询返回的 prediction id，下载全部输出，并返回包含提供商、精确模型、prediction id、提交参数、源 URL、产物路径与预估费用的 `ToolResult` 溯源信息。缺少密钥、不支持的路由、无效枚举、缺少媒体输入、预测失败、超时或下载失败时，必须返回失败结果且不得切换提供商。

在报价或批量消费前，请从机器可读的模型页面（`Accept: text/markdown`）确认当前定价与 schema。
