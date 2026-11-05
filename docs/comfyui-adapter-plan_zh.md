# OpenMontage 的 ComfyUI 提供商适配器

**RFC：用于图像与视频生成的原生 ComfyUI 后端**

---

## 动机

OpenMontage 的本地 GPU 工具（`wan_video`、`hunyuan_video`、`cogvideo_video`、
`local_diffusion`）直接使用 HuggingFace `diffusers`。这在 x86 +
消费级 GPU 上可行，但在 PyTorch 生态尚未跟上的新硬件上会出问题：

| 问题 | 详情 |
|-------|--------|
| **NVIDIA Blackwell (sm_121)** | 尚无稳定的 aarch64 + CUDA 13.0 PyTorch wheel。需 NGC 容器或 nightly 构建。 |
| **Flash Attention** | 不支持 sm_121。须改用 SageAttention v3 或原生 SDPA。 |
| **统一内存 (GB10/DGX Spark)** | `nvidia-smi` 无法报告 VRAM。Diffusers 的内存估算会失效。 |
| **模型格式不匹配** | Diffusers 期望 HF 仓库。生产部署使用 `.safetensors` 检查点及 diffusers 无法原生加载的量化变体（NVFP4、FP8）。 |

ComfyUI 已解决上述全部问题。NVIDIA 为 DGX Spark 提供官方 ComfyUI 容器。
社区针对 Blackwell 优化了工作流（SageAttention、
NVFP4 量化、LightX2V 4-step LoRA）。WAN 2.2、FLUX 2、
ACE-Step 等模型在 diffusers 无法运行的硬件上可通过 ComfyUI 稳定运行。

ComfyUI 适配器让 OpenMontage 能使用 ComfyUI 支持的任意模型、
在 ComfyUI 能运行的任意硬件上运行，而无需打包或维护 PyTorch 构建。

---

## 设计

### 架构

```
OpenMontage Agent
    |
    v
video_selector / image_selector
    |
    v
comfyui_video    comfyui_image    (new tools)
    |                |
    v                v
ComfyUI REST API  (POST /prompt, GET /history, GET /view)
    |
    v
GPU (any hardware ComfyUI supports)
```

### 集成模型

两个新的 `BaseTool` 子类，外加一个共享客户端库：

```
tools/
  _comfyui/
    __init__.py
    client.py              # Shared ComfyUI REST client
    workflows/             # Bundled workflow templates
      flux2-txt2img.json
      wan22-t2v-4step.json
      wan22-i2v-4step.json
  graphics/
    comfyui_image.py       # capability="image_generation", provider="comfyui"
  video/
    comfyui_video.py       # capability="video_generation", provider="comfyui"
```

### 注册表与选择器集成

工具通过类属性声明 `capability` 与 `provider`。
`tool_registry.discover()` 通过 `pkgutil.walk_packages` 自动发现它们。
`video_selector` 与 `image_selector` 通过 `registry.get_by_capability()` 找到它们。
选择器唯一需要的变更是 `video_selector` 中的按操作过滤，以便在仅安装
 bundled 文生视频模型时不会为 `image_to_video` 选中 ComfyUI，反之亦然。

---

## 共享客户端：`tools/_comfyui/client.py`

封装已在生产中验证的 ComfyUI REST API 模式（Bard 项目的 Airflow DAG
用于数千次生成）：

端点契约已对照当前 ComfyUI 服务端文档与 2026 年 4 月第三方开发者指南核对：

- 官方路由：`POST /prompt`、`GET /history/{prompt_id}`、`GET /view`、
  `POST /upload/image`、`GET /object_info/{node_class}`、`GET /models/{folder}`、
  `GET /system_stats`，以及 `WS /ws` 均为文档化服务端路由。
- `/prompt` 在 `prompt` 键下接受 API 格式工作流，
  校验失败时返回 `prompt_id`、`number` 与 `node_errors`。
- `/history/{prompt_id}` 返回已完成节点输出；产物记录包含
  `filename`、`subfolder` 与 `type`。客户端将三者一并传给
  `/view`，而非假定 `type=output`。
- 工作流须以 ComfyUI API 格式导出，而非常规可视化画布工作流格式。

参考：

- https://docs.comfy.org/development/comfyui-server/comms_routes
- https://www.runflow.io/blog/comfyui-api-developer-guide

```python
class ComfyUIClient:
    """Thin client for the ComfyUI REST API."""

    def __init__(self, server_url: str | None = None):
        self.server_url = server_url or os.environ.get(
            "COMFYUI_SERVER_URL", "http://localhost:8188"
        )

    def is_available(self) -> bool:
        """Health check -- can we reach the server?"""

    def submit(self, workflow: dict) -> str:
        """POST /prompt. Returns prompt_id. Raises on node_errors."""

    def poll(self, prompt_id: str, timeout: int = 600, interval: int = 5) -> dict:
        """GET /history/{prompt_id} until complete. Returns outputs dict."""

    def download(self, filename: str, subfolder: str, dest: Path) -> Path:
        """GET /view?filename=...&type=output. Writes bytes to dest."""

    def upload_image(self, local_path: Path, name: str) -> str:
        """POST /upload/image. Returns server-side filename for LoadImage nodes."""

    def generate(self, workflow: dict, output_node: str, dest: Path,
                 timeout: int = 600) -> Path:
        """Full cycle: submit -> poll -> download. Returns artifact path."""
```

**为何需要共享客户端？** 图像与视频生成的 submit/poll/download 循环相同。
差异仅在于：使用哪个工作流模板、
定制哪些节点、从哪个输出节点读取。

---

## 工具规格

### `comfyui_image` -- 图像生成

| 字段 | 值 |
|-------|-------|
| capability | `image_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_image`, `image_to_image` |
| dependencies | (runtime: ComfyUI server reachable) |
| fallback_tools | `flux_image`, `local_diffusion`, `openai_image` |
| cost | `$0.00` (local compute) |

**Bundled workflow:** `flux2-txt2img.json`

加载 FLUX 2 Dev (NVFP4) 与 Mistral 文本编码器。可模板化节点：

| Node | Class | Templated field |
|------|-------|-----------------|
| 4 | CLIPTextEncode | `text` (prompt) |
| 6 | EmptyFlux2LatentImage | `width`, `height` |
| 7 | RandomNoise | `noise_seed` |
| 10 | Flux2Scheduler | `steps` |
| 13 | SaveImage | `filename_prefix` |

**Input schema:**

```yaml
prompt:        string    # required
width:         integer   # default 1024
height:        integer   # default 1024
steps:         integer   # default 20
seed:          integer   # optional (random if omitted)
guidance:      number    # default 3.5
output_path:   string    # where to save the image
workflow_json: string    # optional custom workflow; requires output_node
workflow_path: string    # optional path to workflow JSON; requires output_node
output_node:   string    # required for custom workflows
workflow_name: string    # optional custom workflow provenance label
workflow_model: string   # optional custom model/provenance label
workflow_model_stack: [] # optional custom dependency provenance
```

**get_status():**  ping ComfyUI 服务端并通过 `/object_info` 检查 bundled FLUX 模型名。
当服务端与 bundled 模型集就绪时返回 `AVAILABLE`，
服务端可达但 bundled 模型缺失时返回 `DEGRADED`，
无法连接服务端时返回 `UNAVAILABLE`。

**execute() flow:**
1. Deep-copy workflow template
2. Inject prompt, seed, dimensions, steps into templated nodes
3. `client.generate(workflow, output_node="13", dest=output_path)`
4. Return `ToolResult` with artifact path, seed, model info

对于自定义工作流，调用方须提供 `workflow_json` 或 `workflow_path`
以及 `output_node`。工具不对自定义工作流假定 bundled 节点 ID，除非调用方提供
`workflow_model`，否则溯源报告为用户 supplied。结果还包含最终工作流 SHA-256 哈希，
对 bundled 工作流则包含已知模型栈。

---

### `comfyui_video` -- 视频生成

| 字段 | 值 |
|-------|-------|
| capability | `video_generation` |
| provider | `comfyui` |
| runtime | `LOCAL_GPU` |
| tier | `GENERATE` |
| stability | `EXPERIMENTAL` |
| capabilities | `text_to_video`, `image_to_video` |
| dependencies | (runtime: ComfyUI server reachable) |
| fallback_tools | `wan_video`, `hunyuan_video`, `ltx_video_local` |
| cost | `$0.00` (local compute) |

**Bundled workflows:**

1. **`wan22-i2v-4step.json`** -- 图生视频 (WAN 2.2 14B, fp8, 4-step LightX2V LoRA)
2. **`wan22-t2v-4step.json`** -- 文生视频 (WAN 2.2 14B, fp8, 4-step LightX2V LoRA)

这些 bundled WAN 2.2 14B FP8 工作流属于高质量配置，
建议约 16GB VRAM。这并非 ComfyUI 全局要求。`comfyui_video` 工具顶层的
`resource_profile` 是 8GB 提供商下限，以免 preflight 暗示 ComfyUI 本身需要 16GB。
低 VRAM 用户应使用自定义工作流，例如 Wan 2.1 1.3B、LTX-Video/LTXV FP8 或量化图、
或 Wan 2.2 GGUF/量化社区工作流，并酌情缩短帧数、降低分辨率。

**I2V workflow -- templated nodes:**

| Node | Class | Templated field |
|------|-------|-----------------|
| 93 | CLIPTextEncode | `text` (positive prompt) |
| 97 | LoadImage | `image` (server filename from upload) |
| 98 | WanImageToVideo | `width`, `height`, `length` |
| 86 | KSamplerAdvanced | `noise_seed` |
| 108 | SaveVideo | `filename_prefix` |

**Input schema:**

```yaml
prompt:               string    # required
operation:            string    # "text_to_video" | "image_to_video" (default: t2v)
reference_image_path: string    # local path (for i2v)
reference_image_url:  string    # URL (for i2v, downloaded first)
width:                integer   # default 640
height:               integer   # default 640
num_frames:           integer   # default 81 (5s at 16fps)
seed:                 integer   # optional
output_path:          string    # where to save the video
workflow_json:        string    # optional custom workflow; requires output_node
workflow_path:        string    # optional path to workflow JSON; requires output_node
output_node:          string    # required for custom workflows
workflow_name:        string    # optional custom workflow provenance label
workflow_model:       string    # optional custom model/provenance label
workflow_model_stack: []        # optional custom dependency provenance
timeout_seconds:      integer   # optional, default 3600 (see below)
resume_prompt_id:     string    # optional, resume a timed-out job without resubmitting
```

**execute() flow (i2v):**
1. Upload reference image via `client.upload_image()`
2. Deep-copy i2v workflow template
3. Inject prompt, uploaded image name, seed, dimensions
4. `client.generate(workflow, output_node="108", dest=output_path, timeout=inputs.get("timeout_seconds", 3600), resume_prompt_id=inputs.get("resume_prompt_id"))`
5. Return `ToolResult`

**execute() flow (t2v):**
1. Deep-copy t2v workflow template
2. Inject prompt, seed, dimensions
3. `client.generate(workflow, output_node="16", dest=output_path, timeout=inputs.get("timeout_seconds", 3600), resume_prompt_id=inputs.get("resume_prompt_id"))`
4. Return `ToolResult`

**超时与恢复（真实本地 GPU 测试后新增）：** 默认客户端等待从 900s 提高到 3600s ——
在 modest 本地 GPU 上未加速的自定义 Wan 1.3B 工作流在
832x480/81-97 帧下观测到约 1360–1630s，旧 900s 默认会误报失败，
尽管 ComfyUI 仍在服务端渲染。`ComfyUIError` 现在在执行错误与超时上均携带
`prompt_id`（`ComfyUIError.prompt_id`），
`ComfyUIVideo` 的 `ToolResult.error`/`.data` 在超时时暴露它，以免调用方猜测任务是否已死。
调用方可通过再次调用 `execute()` 并设置 `resume_prompt_id` 为该 `prompt_id`
（必要时加长 `timeout_seconds`）恢复超时但仍在运行的任务 ——
`client.generate()` 则完全跳过 `submit()`，仅继续轮询/下载现有任务，而非重复入队。

`comfyui_video` 在 `get_info()` 中发布 `operation_statuses` 并实现
`is_operation_available(operation)` 供选择器路由。这使部分安装的 ComfyUI
对已安装模式仍有用，而不会把未就绪的操作模式标为可用。`video_selector` 在
`operation="rank"` 时也通过 `target_operation` 应用此就绪检查，以免 preflight 排名
在 bundled 模型缺失的操作上提升 ComfyUI。

---

### `comfyui_music` -- 音乐生成（已交付，含原生节点 bundled 工作流）

`tools/audio/comfyui_music.py`。`capability="music_generation"`, `provider="comfyui"`。

**Bundled default:** ACE-Step v1 (3.5B) 文生音频，经由 `tools/_comfyui/workflows/ace-step-1-t2a.json`。
最初阻碍该工具的节点包碎片化（`AceStepModelLoader`
与原生 `TextEncodeAceStepAudio` 等）对 ACE-Step v1 而言无关紧要：
ComfyUI 将 `TextEncodeAceStepAudio`/`EmptyAceStepLatentAudio` 作为**原生核心
节点**（`comfy_extras/nodes_ace.py`）而非第三方包，Comfy-Org 自己的
[`workflow_templates`](https://github.com/Comfy-Org/workflow_templates) 仓库 bundled
官方 ACE-Step-v1 模板，完全由这些原生节点加上
长期稳定的核心节点（`CheckpointLoaderSimple`、`KSampler`、`ModelSamplingSD3`、
`VAEDecodeAudio`、`SaveAudioMP3`）构成。`ace-step-1-t2a.json` 中每个节点的 `class_type` 与输入名
均对照 ComfyUI 自身源码
（`comfy_extras/nodes_ace.py`、`nodes_audio.py`、`nodes_latent.py`、`nodes.py`）交叉核对 ——
而非从 UI 导出猜测 —— 因为 Comfy-Org 提供的 UI 格式模板无法直接作为本客户端提交的 API 格式 JSON。

`prompt` 映射到 ACE-Step 的 `tags` 字段（风格/流派/情绪描述，与 `suno_music` 已用的
「prompt = 期望音乐描述」约定一致）。
`lyrics` 为独立可选字段（纯音乐时为空）。`duration_seconds`、
`steps`、`cfg`、`lyrics_strength` 与 `seed` 均可 patch；`shift` 与
tonemap `multiplier` 保持官方模板默认值。

较新/不同配置不受限：`workflow_json`/`workflow_path` +
`output_node` 与图像/视频工具的 override 路径完全相同 ——
适用于 ACE-Step 1.5、不同节点包或非 ACE-Step 音频模型。

**选择器集成：** OpenMontage 中尚无专用 `music_selector`
（不同于 `tts_selector`/`image_selector`/`video_selector`）—— 音乐工具已通过
`registry.get_by_capability("music_generation")` 直接路由，
`comfyui_music` 与 `suno_music`/`music_gen` 参与方式相同。`fallback_tools = ["suno_music", "music_gen"]`。

**音频产物 schema：** `ToolResult.data` 与图像/视频工具同形（`provider`、`model`、`output`、`format`、`workflow_provenance`），
另加 `lyrics` 与 `duration_seconds` —— 后者为对已下载文件的最佳努力 `ffprobe` 探测
（PATH 上无 `ffprobe` 时为 `None`），因 bundled 工作流也不会通过 `/history` 回传实际渲染时长。

**工作流/输出节点契约：** 与图像/视频相同 —— `output_node`
必须是写入最终产物的节点 ID（bundled 工作流为 `SaveAudioMP3`，ComfyUI 原生音频保存器）。`ComfyUIClient.generate()` 的产物提取现在也会检查 `"audio"` 输出键（此前仅
`"images"`/`"gifs"`），即 `SaveAudioMP3`/`SaveAudio` 在 ComfyUI `/history` 响应中写入的键。

---

## 工作流覆盖机制

图像与视频工具接受 `workflow_json` 或 `workflow_path`。
提供时，自定义工作流完全替换 bundled 模板，
调用方还必须提供 `output_node`。此更严格契约是必需的，
因为社区工作流使用任意节点 ID。

- 在不改代码的情况下使用较新模型检查点
- 自定义采样策略（不同调度器、步数、LoRA）
- 原样放入社区工作流
- A/B 测试不同生成方式

Agent 也可从 `tools/_comfyui/workflows/` 读取工作流文件，
在传给 `execute()` 前以程序方式修改。

自定义工作流结果元数据将 `workflow_provenance.source` 报告为
`user_supplied`，并在提供时使用 `workflow_model`、`model` 或 `workflow_name` 作为
模型标签。未提供自定义标签时，模型报告为 `custom-comfyui-workflow` 而非 bundled 模型名之一。
溯源 payload 还记录 `workflow_hash_sha256`。对用户 supplied 工作流，调用方应在已知时提供
`workflow_model_stack`（基模型、文本编码器、VAE、LoRA 及强度、调度器、步数、guidance）。

---

## Agent Skill 与设置契约

两个 ComfyUI 工具均宣传 Layer 3 `comfyui` skill。Agent 在调用任一工具前须阅读
`.agents/skills/comfyui/SKILL.md`，以了解如何加载社区工作流、识别输出节点、处理 LoRA 加载链、
以及记录自定义工作流溯源。

不可用的 ComfyUI 工具在 `get_info()`、
`provider_menu()` 与 `provider_menu_summary().setup_offers[]` 中暴露结构化 `setup_offer`：

```yaml
kind: local_server
env_var: COMFYUI_SERVER_URL
default_url: http://localhost:8188
health_check: GET /system_stats
```

当 bundled 模型缺失时，工具返回机器可读的
`data.missing_models[]` 列表，含文件名、角色、目标路径提示，以及 OpenMontage 知晓规范来源时的下载
URL。Agent 应展示该 payload，而非解析散文式错误文本。

---

## 配置

**环境变量：**

```bash
# .env
COMFYUI_SERVER_URL=http://localhost:8188    # ComfyUI API endpoint
COMFYUI_POLL_INTERVAL=5                     # seconds between status checks
COMFYUI_POLL_TIMEOUT=600                    # max wait for image gen
COMFYUI_VIDEO_TIMEOUT=900                   # max wait for video gen
```

**多服务器（可选）：** 将 `comfyui_image`、`comfyui_video` 与
`comfyui_music` 指向不同 ComfyUI 实例 —— 例如一 GPU 跑 FLUX 2、
另一跑 WAN 2.2、再一跑 ACE-Step —— 通过按能力覆盖设置。各覆盖仅对其自身工具优先于 `COMFYUI_SERVER_URL`；
三者均不设置则全部对话单一共享服务器。

```bash
COMFYUI_IMAGE_SERVER_URL=http://gpu-a:8188
COMFYUI_VIDEO_SERVER_URL=http://gpu-b:8188
COMFYUI_MUSIC_SERVER_URL=http://gpu-c:8188
```

**Docker Compose 场景**（ComfyUI 在容器内）：

```bash
COMFYUI_SERVER_URL=http://host.docker.internal:8188
# or
COMFYUI_SERVER_URL=http://comfyui:8188      # if on same docker network
```

---

## 提供商选择行为

适配器可用时，选择器将与其他提供商一起按 OpenMontage 七维评分排名：

| 维度 | ComfyUI 得分 | 理由 |
|-----------|---------------|-----------|
| Task fit | 高 | 支持 t2i、i2v、t2v |
| Quality | 高 | 最新模型 (FLUX 2, WAN 2.2 14B) |
| Control | 最高 | 完整工作流定制 |
| Reliability | 高 | 生产验证 |
| Cost | $0 | 本地算力 |
| Latency | 中 | GPU  bound，无网络往返 |
| Continuity | 高 | 种子可复现 |

ComfyUI 不可用（服务端宕机）时，选择器回退到其他可用提供商。仅配置一种视频操作时，`video_selector`
使用工具的操作级就绪状态，避免为缺失模式选中 ComfyUI。

---

## 此方案解锁的能力

### 即时（现有模型）

- **FLUX 2 Dev NVFP4** 图像生成 —— Blackwell 优化，约 60s/张
- **WAN 2.2 14B FP8 高质量配置** i2v 与 4-step 加速 —— 约 3.5 分钟/5s 片段，建议约 16GB VRAM
- **WAN 2.2 14B FP8 高质量配置** t2v（模型已下载，含工作流），建议约 16GB VRAM

### 低 VRAM 配置

用户在提供合适 `workflow_json` 或 `workflow_path` 时，ComfyUI 在 8GB–12GB GPU 上仍有用。合适候选包括：

- Wan 2.1 1.3B 工作流用于低内存文生视频。
- LTX-Video/LTXV FP8 或量化工作流用于快速短视频。
- 较低分辨率与帧数的 Wan 2.2 GGUF/量化社区工作流。

OpenMontage 应将这些视为自定义工作流配置，直至 bundled 低 VRAM 工作流。对自定义工作流，资源需求由工作流提供，而非从 bundled WAN 2.2 14B 配置推断。

### 未来（向 ComfyUI 添加模型，OpenMontage 无需改代码）

- 较新检查点 (WAN 3.x, FLUX 3 等) —— 仅更新工作流 JSON
- ControlNet、IP-Adapter、AnimateDiff —— 通过 ComfyUI 自定义节点支持
- 放大、inpainting、outpainting —— ComfyUI 节点已存在
- ComfyUI 生态支持的任意模型

### 硬件可移植性

同一适配器适用于：
- NVIDIA DGX Spark (GB10, aarch64, CUDA 13.0)
- 消费级 GPU (RTX 3090/4090, x86)
- 云实例 (A100, H100)
- 多 GPU 配置 (ComfyUI 处理设备放置)

无需 PyTorch 版本锁定、架构专用 wheel 或 CUDA
兼容矩阵。ComfyUI 即抽象层。

---

## 实现范围

| 组件 | 文件 | 估计规模 |
|-----------|-------|----------------|
| Shared client | `tools/_comfyui/client.py` | ~180 lines |
| Shared metadata | `tools/_comfyui/metadata.py` | setup, model stack, provenance helpers |
| Image tool | `tools/graphics/comfyui_image.py` | ~140 lines |
| Video tool | `tools/video/comfyui_video.py` | ~190 lines |
| Layer 3 skill | `.agents/skills/comfyui/SKILL.md` | usage contract |
| Registry summary | `tools/tool_registry.py` | setup offer surfacing |
| Selector readiness filter | `tools/video/video_selector.py` | small operation-readiness check |
| Workflow templates | `tools/_comfyui/workflows/*.json` | 3 files |
| Tests | `tests/contracts/test_comfyui_tools.py` | ~200 lines |
| Docs | `docs/comfyui-adapter-plan.md` | This file |

**合计：** 约 500 行 Python + 3 个工作流 JSON。

不改动：`base_tool.py`、现有非 ComfyUI 生成提供商、
任何 pipeline 定义或任何 schema。

---

## 开放问题

1. **工作流版本：** 工作流 JSON 应放在仓库还是用户通过配置目录提供？Bundling 保证可复现；
   外部路径更灵活。

2. ~~**异步生成：**~~ **已解决。** `ComfyUIClient.generate()` 现在默认通过 ComfyUI websocket 订阅（`wait_ws()`）等待，即时响应
   `executing`/`execution_error` 事件，而非在 REST 轮询间 sleep —— 完成与错误无
   `interval` 秒延迟即可捕获，可选 `on_progress` 回调接收实时
   `progress` 事件（`comfyui_video` 用于长渲染时打印步进进度）。无新硬依赖：`websocket-client` 为可选
   import，未安装或连接失败时 `_wait()` 透明回退原
   `poll()` REST 循环 ——
   `resume_prompt_id` 恢复两种方式行为一致。

3. ~~**多服务器：**~~ **已解决。** `ComfyUIClient(capability="image"|"video"|"music")`
   优先从按能力环境变量解析服务端 URL
   （`COMFYUI_IMAGE_SERVER_URL` / `COMFYUI_VIDEO_SERVER_URL` / `COMFYUI_MUSIC_SERVER_URL`），
   其次共享 `COMFYUI_SERVER_URL`，最后默认 `http://localhost:8188`。
   三个工具在构造时传入其 capability，图像、视频与
   音乐生成可各指向不同 ComfyUI 实例（不同 GPU、
   不同模型集）且零代码变更 —— 单服务器设置无需额外
   配置，因三个环境变量均为可选。`client.capability`/
   `client.is_default_url`/`client.unavailable_reason()` 均考虑
   覆盖，`COMFYUI_SETUP_OFFER.per_capability_env_var_overrides` 在 `provider_menu()` 的设置 offer 展示中记录
   该行为。

4. ~~**音乐生成：**~~ **已解决 —— 已交付 bundled ACE-Step v1 工作流。**
   `comfyui_music` 现为真实工具（非隐藏的图像/视频 override），通过现有
   `registry.get_by_capability("music_generation")` 路径路由，
   与 `suno_music`/`music_gen` 相同。最初阻碍的节点包碎片化对 ACE-Step v1 不适用：其 ComfyUI 节点为
   原生核心节点而非第三方包，故 `ace-step-1-t2a.json` 作为默认 bundled，逐节点对照 ComfyUI 源码验证。自定义
   `workflow_json`/`workflow_path` + `output_node` 仍可用于其他
   版本/包。完整契约见上文 `comfyui_music` 节。
