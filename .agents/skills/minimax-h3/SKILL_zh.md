---
name: minimax-h3
description: |
  通过 MiniMax 官方 v2 API、fal.ai、Runway、ComfyUI 合作伙伴节点，或在 ComfyUI 中使用本地开源权重，生成 MiniMax H3（海螺 3.0）视频。适用于 4–15 秒 2K 片段、首尾帧动画，以及基于图像/视频/音频参考的条件化视频生成。
---

# MiniMax H3

MiniMax H3 属于海螺 3.0 系列。官方 API 标识为
`MiniMax-H3`；fal.ai 将该系列暴露为 `hailuo-03`，Runway 使用
`hailuo3`。请勿将某一提供商的标识符用于另一家的 API。

## 选择接入路径

| 路径 | 工具调用 | 执行方式 |
|-------|-----------|-----------|
| MiniMax 直连 | `minimax_video`, `model: "MiniMax-H3"` | 托管官方 v2 API；全球或中国大陆区域 |
| fal.ai | `minimax_fal_video` | 托管网关；T2V、I2V、参考图生视频 |
| Runway | `runway_video`, `model: "hailuo3"` | 托管；768P 或 2K，5–15 秒 |
| ComfyUI 合作伙伴节点 | `comfyui_video`, `model_family: "minimax_h3_api"` | 托管，按 Comfy 积分计费 |
| ComfyUI 开源权重 | `comfyui_video`, `model_family: "minimax_h3_local"` | 本地 GPU，使用官方工作流与模型栈 |

本地 ComfyUI 时，以 API 格式导出官方工作流，并传入
`workflow_json` 或 `workflow_path` 以及 `output_node`。OpenMontage 会说明所需的
扩散模型、Qwen3-VL 文本编码器、视频 VAE 与音频 VAE；不会静默下载大型权重。

## 操作与提示词

- 文生视频：使用具体宽高比；无视觉输入时不要使用 `adaptive`。
- 图生视频：提供首帧图像。
- 首尾帧：同时提供两张图像，并描述二者之间的运动。
- 参考生视频：可组合图像、视频与音频。使用音频时至少需要一项视觉参考。

提示词建议写为主体 + 动作 + 镜头运动 + 环境 + 光照 +
音频意图。MiniMax 对明确的镜头方向响应较好。请确保所描述的运动在 4–15 秒内可实现，并对原生音频与画面一样仔细审查。

## 各提供商差异

MiniMax v2 直连路径当前输出 2K，支持 4–15 秒。
Runway 的海螺 3.0 路径支持 768P/2K，文档记载为 5–15 秒。合作伙伴
节点需要网络访问与积分。仅在 ComfyUI 开源权重路径下，所有模型安装完成后可本地/离线运行。
