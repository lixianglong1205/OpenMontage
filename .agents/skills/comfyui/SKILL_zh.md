---
name: comfyui
description: 在 OpenMontage 中使用 ComfyUI 工作流时使用，包括 comfyui_image/comfyui_video/comfyui_music、自定义 workflow_json/workflow_path 输入、output_node 选择、缺失模型设置、LoRA、低显存工作流选择以及社区工作流导入。
---

# OpenMontage 中的 ComfyUI 工作流

在调用 `comfyui_image`、`comfyui_video` 或 `comfyui_music` 之前使用本技能，并在将社区 ComfyUI 工作流转换为 OpenMontage 工具调用时使用。

## 服务端契约

- 生成前 ComfyUI 必须正在运行。默认服务器为 `http://localhost:8188`；可通过 `COMFYUI_SERVER_URL` 覆盖。
- 是否为不同能力运行独立的 ComfyUI 实例（不同 GPU、不同模型集）？`COMFYUI_IMAGE_SERVER_URL` / `COMFYUI_VIDEO_SERVER_URL` / `COMFYUI_MUSIC_SERVER_URL` 可分别仅对该工具覆盖 `COMFYUI_SERVER_URL`。可选 — 单服务器部署无需设置这些变量。
- 健康与硬件状态来自 `GET /system_stats`。
- 任务通过 `POST /prompt` 提交，完成后的输出从 `GET /history/{prompt_id}` 读取，产物字节通过 `GET /view` 下载。
- 长时间等待（视频、音乐）优先使用 ComfyUI 的 websocket 流以即时检测完成/错误；若未安装 `websocket-client` 则透明回退到 REST 轮询。无论哪种方式，超时均可恢复：将错误中的 `prompt_id` 作为 `resume_prompt_id` 传回，即可继续等待同一任务而无需重新提交。
- 使用 ComfyUI 的 API 格式 JSON 导出工作流，而非 UI 布局格式。若下载的工作流无法提交，请在 ComfyUI 中启用 API 格式后重新导出。

### Partner Nodes 为托管服务

- `comfyui_video` 中的 `gemini_omni_flash`、`seedance_2.5` 和 `minimax_h3_api` 为官方 ComfyUI Partner Nodes。它们调用托管 API，需要网络访问、已登录的 Comfy 账户以及预付费额度。
- 不要仅因图在本地 ComfyUI 进程中运行，就将 Partner Nodes 描述为本地、离线或免费。
- `minimax_h3_local` 是独立的开放权重路径。它需要以 API 格式导出的官方 MiniMax H3 工作流、其 `output_node`，以及工具报告所需的模型栈。

## 选择工作流

- 当请求的操作与 bundled 工作流匹配且本地机器具备所需模型与显存时，使用 bundled 工作流。
- 当用户需要社区配方、更低显存模型、不同风格族或自定义节点时，使用自定义 `workflow_json` 或 `workflow_path`。
- 对于 8GB–12GB GPU，优先选用更低占用工作流，例如 Wan 2.1 1.3B、LTXV FP8 或量化工作流，或 Wan 2.2 GGUF/量化社区工作流。bundled 的 Wan 2.2 14B FP8 视频工作流属于 16GB 级别路径，而非全 provider 的底线。
- 不要承诺任意自定义工作流一定能适配某台机器。工作流、量化、分辨率、帧数与 offload 设置共同决定真实的资源 envelope。

## 输出节点契约

- 自定义工作流必须传入 `output_node`。
- 选择写入产物的节点，通常为 `SaveImage`、`SaveVideo`、`VHS_VideoCombine` 或其他终端保存节点。
- 以字符串形式传入节点 ID，例如 `"108"`。不要传入 class 名称。
- 若工作流有多个保存节点，选择最终交付物节点，而非预览或中间结果。

## 模板节点 vs 固定节点

- 执行前识别模板节点：提示文本、seed、尺寸、帧数、源图、采样器设置以及输出文件名前缀。
- 固定节点包括模型加载器、VAE、文本编码器、LoRA 加载器、调度器与图连线。除非工作流作者有意允许该定制，否则不要修改它们。
- 对于社区工作流，检查每个加载器节点并记录运行前所需的全部模型或自定义节点。缺失模型应通过工具的结构化 `missing_models` 载荷处理（若可用）。

### 视频工作流需要时序 latent

- 视频工作流的空 latent 节点必须是**视频** latent — Wan 2.2 t2v 用 `EmptyHunyuanLatentVideo`，图像条件变体用 `Wan22ImageToVideoLatent` 或 `WanImageToVideo`。帧数写在 `length`；`batch_size` 表示生成多少条独立片段，保持为 `1`。
- 将 `batch_size` 设为帧数的 `EmptyLatentImage` 是陷阱：它会要求 N 张互不相关的图像，生成的 MP4 帧数、时长与编解码正确且 `ffprobe` 能通过 — 但画面会频闪。对任何不熟悉的视频工作流，运行前先检查 latent 节点。

## 模型与 LoRA 设置

- 在可用时使用 ComfyUI Manager 或工作流作者提供的模型链接，并遵守模型许可证。
- 将模型放在加载器节点期望的目录：扩散模型在 `ComfyUI/models/diffusion_models/`，文本编码器在 `ComfyUI/models/text_encoders/`，VAE 在 `ComfyUI/models/vae/`，LoRA 在 `ComfyUI/models/loras/`。
- 对于 LoRA 栈，在工作流中使用 `LoraLoader` 或 `LoraLoaderModelOnly` 链。记录每个 LoRA 名称以及适用的 `strength_model` 与 `strength_clip`。
- 当前 ComfyUI 工具不会向任意图注入 LoRA。要使用 LoRA，需提供已包含 LoRA 加载链的工作流，并传入模型栈溯源信息。

## 溯源（Provenance）

- 对于自定义工作流，在已知时提供 `workflow_name` 与 `workflow_model`。
- 当工作流非 bundled 时，为可复现性提供 `workflow_model_stack`：包括基础 checkpoint 或扩散模型、量化、文本编码器、VAE、LoRA 及强度、采样器或调度器、步数，以及工作流暴露的 guidance。
- 工具会记录最终工作流哈希。将该哈希与模型栈、seed、尺寸和 prompt 一并视为可复现性契约。

## 故障处理

- 若服务器不可用，展示结构化设置引导。首要修复是启动 ComfyUI 或设置 `COMFYUI_SERVER_URL`。
- 若模型缺失，读取 `data.missing_models[]`；每项应包含文件名、角色、目标路径提示，以及 OpenMontage 已知时的下载 URL。
- 若自定义节点缺失，请用户通过 ComfyUI Manager 或工作流作者文档中的安装路径安装，然后重启 ComfyUI。
- 若本地长时间渲染超时，在从头重试前先查 ComfyUI history；服务器可能已完成该 prompt — 或直接用超时错误中的 `prompt_id` 设置 `resume_prompt_id` 再次调用。

## 音乐（`comfyui_music`）

- bundled 默认为 ACE-Step v1（3.5B）文本转音频，基于 ComfyUI **原生** `TextEncodeAceStepAudio`/`EmptyAceStepLatentAudio` 节点（核心，非第三方包）构建 — 与 ACE-Step 1.5 或其他自定义节点包不同，v1 的接口足够标准化，可以安全 bundled。
- `prompt` 映射到 bundled 工作流的 `tags` 字段（风格/流派/情绪，例如 `"upbeat electronic pop, female vocals"`），与 `suno_music` 使用的「prompt = 音乐描述」约定一致。`lyrics` 为独立的可选字段 — 纯器乐留空，或使用 `[verse]`/`[chorus]`/`[bridge]` 结构标签以及 `[zh]`/`[ja]`/`[ko]` 等非英语行的语言代码前缀。
- `duration_seconds`、`steps`、`cfg`、`lyrics_strength` 与 `seed` 可在 bundled 工作流上 patch。缺失 `ace_step_v1_3.5b.safetensors` 会通过与图像/视频相同的 `data.missing_models[]` 契约暴露。
- 需要 ACE-Step 1.5、不同节点包或非 ACE-Step 音频模型？回退到 `workflow_json`/`workflow_path` + `output_node`，与自定义图像/视频工作流完全相同 — 该模式下 `prompt` 再次仅用于溯源/日志，且必须已 baked 进图中。
- `output_node`（bundled 或自定义）应为写入最终音频的节点 — bundled 工作流中为 `SaveAudioMP3`。客户端从该节点的 `"audio"` 输出键读取产物（与图像/视频保存器的 `"images"` 平行）。
- 对于自定义工作流，与自定义图像/视频工作流一样提供 `workflow_name`/`workflow_model`/`workflow_model_stack` 以作溯源。
