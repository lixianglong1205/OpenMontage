# BGM Montage Lite

BMTS-Lite 是 OpenMontage 的快速、本地、以音频为主导的蒙太奇路线。它接受一个音乐文件和一个或多个已提供的视频片段，分析完整音轨，规划节拍/乐句感知的切点，在需要时复用片段，将输出画面适配为所选或多数检测到的宽高比，并渲染 MP4。它不需要参考视频或 API 密钥。

## 选择合适的模式

| 模式 | 适用场景 | 所需媒体 | 选择与审阅 |
| --- | --- | --- | --- |
| **BMTS-Lite** (`bgm_montage_lite`) | 基于用户已选素材的快速、整曲节拍蒙太奇 | 一个音频文件和 1–100 个视频片段 | 随机、均衡复用；自动宽高比；无语义选择或工具专属的 agent 视觉审阅 |
| **BGM Montage**（在 [PR #751](https://github.com/calesthio/OpenMontage/pull/751) 中的独立集成） | 带风格分析与更严格源素材选择的专业参考引导剪辑 | 音频、参考视频与源素材库 | 参考风格分析、智能选择、渲染器 QA，以及完整集成的审阅关卡 |

Lite 工具刻意调用 BMTS-Lite 现有的 `worker.run()` 与 `engine/` 模块。它不会把该引擎复制进 OpenMontage，也不会走 BGM Montage 完整工作流。其现有的随机分配、12 镜头渲染批次、整轨音频混流、自动宽高比投票与模糊填充画幅均保持不变。

## 安装可选的本地运行时

集成将 BMTS-Lite 依赖放在 OpenMontage 主 Python 环境之外。请使用干净的 BMTS-Lite 检出与专用的 Python 3.11 环境：

```powershell
git clone https://github.com/sharbvane/BMTS-Lite.git
cd BMTS-Lite
py -3.11 -m venv .venv-openmontage
.\.venv-openmontage\Scripts\python.exe -m pip install -r requirements-runtime.txt
$env:BGM_MONTAGE_LITE_ROOT = (Get-Location).Path
$env:BGM_MONTAGE_LITE_PYTHON = (Resolve-Path .\.venv-openmontage\Scripts\python.exe).Path
```

在 `PATH` 上安装 FFmpeg（含 `ffprobe`）。在 macOS/Linux 上，用 `python3.11 -m venv .venv-openmontage` 创建虚拟环境，安装同一 requirements 文件，并将上述两个变量导出为检出目录与环境解释器路径。

蒙太奇运行期间不使用网络访问或 API 凭证。在源检出、运行时包、FFmpeg 与 ffprobe 齐备之前，工具会报告为不可用。

## 从 cinematic compose 阶段调用

该工具是 cinematic 流水线 compose 阶段的可选 `video_post` 能力。仅在不涉及参考匹配、旁白、标题或语义片段选择的简单整曲音乐蒙太奇时选用。已有视频 compose 路线仍用于 authored 合成、混合媒体以及专业参考引导工作流。

```python
from tools.tool_registry import registry

registry.discover()
result = registry.get("bgm_montage_lite").execute({
    "audio_path": "project/assets/music.mp3",
    "video_paths": [
        "project/assets/clip-01.mp4",
        "project/assets/clip-02.mp4",
        "project/assets/clip-03.mp4",
    ],
    "project_dir": "project",
    "aspect_ratio": "auto",
})
if not result.success:
    raise RuntimeError(result.error)
print(result.data["output_path"])
```

支持的显式宽高比为 `16:9`、`9:16`、`4:3`、`3:4`、`1:1` 与 `4:5`；`auto` 会选择与多数源片段最接近的支持比例。比例不一致的片段在现有模糊填充处理中仍保留完整画面。完整音频不会被静默截短：BMTS-Lite 接受 1 秒至 10 分钟的音乐轨，超出该范围会失败。

工具返回三个 OpenMontage 产物：MP4、`*.timeline.json` 与 `*.audiomap.json`。渲染报告包含探测到的编解码器、尺寸、帧率、时长、文件大小以及渲染器的全解码校验。输出不会被覆盖；若三者中任一文件已存在，请指定新的 `output_path`。

## 端到端验证

2026-10-09，OpenMontage 工具适配器使用本地 21.768 秒音乐轨与五个本地视频片段（无参考视频或 API 密钥）完成渲染。产出 33 镜头、1920×1080 H.264/AAC MP4；输出音频流覆盖完整 21.768 秒音轨。BMTS-Lite 检测到 45 个节拍：切点边界与最近检测节拍的平均距离 62.8 ms、最大 250.9 ms，78.1% 在 120 ms 内（其余含半拍/乐句切点）。五个片段各复用 6–7 次且源偏移各异，渲染器与独立 FFmpeg 全解码检查均成功。源媒体与渲染文件为本地测试输入/输出，有意未随本项目再分发。

## 许可与署名

当前 main 修订及之后版本的 BMTS-Lite 源码采用 AGPL-3.0-only 许可，版权 © 2026 Cui (sharbvane)。历史快照保留其随附许可。本 OpenMontage 贡献未 vendored BMTS-Lite 引擎源码或第三方媒体。单独安装的引擎与运行时依赖请参阅 [BMTS-Lite](https://github.com/sharbvane/BMTS-Lite) 及其 [`requirements-runtime.txt`](https://github.com/sharbvane/BMTS-Lite/blob/main/requirements-runtime.txt)。
