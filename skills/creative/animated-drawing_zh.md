# 动画手绘 — 用真实动作捕捉驱动你提供的绘画/照片

> 命令：`/animated-drawing` · **路径 A（栅格）。** 姊妹命令：`/ink-art`（矢量，从零创建）。
> 工具：Meta 开源 **AnimatedDrawings**（github.com/facebookresearch/AnimatedDrawings — 代码 MIT，仓库于 2025 年归档）。

**何时使用：** 用户*已有*一张**人形**角色的绘画或照片，并希望**该图像**动起来（跳舞 / 行走 / 跳跃 / 挥手）。输出 = 原图被变形以匹配动作的栅格 **GIF（透明）或 MP4**。若要**从零**创建会自行绘制并移动的矢量涂鸦 → 请改用 **`/ink-art`**。

**它做什么：** 自动绑定骨骼（预测 16 关节骨架），然后通过 As-Rigid-As-Possible（尽可能刚体）网格变形对平面纹理进行变形，将 BVH 动作捕捉片段重定向到该角色上。它*只会移动已经画完整的图* — **没有逐笔绘制 / 自描揭示**（那是 `/ink-art` 的事）。

## 选择角色来源 — 先询问（切勿静默复用捆绑角色）

该工具会动画化*你交给它的任意图像*，且需要一张**绘制的人形**（头、双臂、双腿、肢体分开、浅色纯色背景）。在搭建前，**向用户展示以下选项**并择一（若用户没有素材则默认*生成*）— 这也是避免每个视频都像同一个吉祥物的原因：

1. **用户上传绘画** — 他们自己的人形涂鸦。效果最好；是他们的角色。
2. **用户上传照片 / 任意图像** — 先**涂鸦化**（`image_selector` img2img，FLUX/Recraft：「把这张图变成简单的儿童蜡笔人形涂鸦，全身，纯白背景」）→ 再绑定。「手绘感」来自这一步；原始照片直接变形效果很差。
3. **生成全新角色** ⭐（推荐默认）— `image_selector`（FLUX/Imagen）：*「儿童蜡笔绘制的角色，全身，正面，A-pose 且手臂与腿分开，纯白背景，无阴影，无文字。」* 每个视频都独一无二。
4. **抓取库存角色** — `pixabay_image` / `pexels_image`，筛选为*纯色背景上的绘制人形*。成败参半（多数库存是照片）— 优先选 #3。

捆绑示例角色**仅供演示** — 不要当作用户的角色交付。选项 1–4 都需要下面的 **auto-rig Docker 服务**；若未启动，请明确告知。

## 两种运行模式

**A · 捆绑角色 + 预设动作 — 开箱即用，无需 Docker（已在 Windows 上验证）：**
```bash
git clone --depth 1 https://github.com/facebookresearch/AnimatedDrawings.git && cd AnimatedDrawings
# the repo pins Python 3.8 + old wheels; get 3.8 via uv:
uv python install 3.8 && uv venv --python 3.8 .venv
uv pip install --python .venv -e .
uv pip install --python .venv "setuptools<81"      # repo imports pkg_resources but doesn't declare it
.venv/Scripts/python -c "from animated_drawings import render; render.start('./examples/config/mvc/export_gif_example.yaml')"
```
每段约 10–12 秒（CPU），无需 GPU/Docker/模型下载。

**B · 为新绘画自动绑定 — 重量级（Docker + 约 670 MB 模型，约 16 GB RAM）：**
```bash
python image_to_animation.py drawing.png out_dir    # detect → segment → rig → retarget → render
```
需要仓库的 TorchServe 容器（`docker/`），会下载 `drawn_humanoid_detector.mar`（311 MB）+ `drawn_humanoid_pose_estimator.mar`（357 MB）。Windows：仅通过该容器运行 rig 栈（OpenMMLab 实际仅支持 Linux）。

## 输入要求（自动绑定）
一张清晰绘制的**人形**，大致 T/A-pose（肢体分开、不重叠），**浅色纯色背景**（分割为阈值 + 泛洪填充），且恰好一个主体。

## Agent 生成的配置（均为 YAML）
`char_cfg.yaml`（+ `texture.png`、`mask.png`；由 `image_to_annotations.py` 自动生成）· 一份 **motion** 配置（bvh + frames + groundplane）· 一份 **retarget** 配置（BVH 关节 → rig 关节；骨架无差异时复用捆绑的 `fair1_ppf` / `cmu1_pfp`）· 一份 **MVC** 配置（`controller.MODE: video_render`、`OUTPUT_VIDEO_PATH`，可选 `WINDOW_DIMENSIONS` / `CLEAR_COLOR` / `BACKGROUND_IMAGE` / `CAMERA_POS`）。

## 预设动作 → retarget 配置（必须与 BVH 骨架一致）
每个捆绑 BVH 属于不同骨架族；用错 retarget 配置会**崩溃**（`ValueError: 'RightArm' is not in list`）。请配对：

| 动作 | BVH 文件夹 | retarget 配置 |
|---|---|---|
| `dab`, `wave_hello`, `jumping`, `zombie` | `bvh/fair1/` | `fair1_ppf` |
| `jumping_jacks` | `bvh/cmu1/` | `cmu1_pfp` |
| `jesse_dance` | `bvh/rokoko/` | `mixamo_fff` |

其他 BVH → 匹配其骨架（或编写 retarget 配置）。**截断长片段**用 `end_frame_idx`（`wave_hello` 有 839 帧），否则渲染会跑数分钟；触地类片段（`dab`、`wave_hello`）渲染约慢 8 倍。

## 角色多样性 — 动画化用户的绘画（解决「总是同一个角色」）
捆绑角色**仅供演示**。实际使用中角色是用户**提供**的任意素材 — 每个视频独一无二。对「直接帮我做个视频」且没有绘画的请求，**生成全新角色**（图像生成：「儿童蜡笔绘制的 …」→ 纯色浅色背景 PNG）并 **auto-rig**（Docker 路径）→ 每次不同角色。**切勿在多个视频中复用捆绑角色**，否则每个输出都像同一个吉祥物。

## 合成进 HyperFrames（后半段 — 做成真正视频所必需）
AnimatedDrawings 只输出移动的角色。要做*视频*（背景、气球、音乐），在 HyperFrames 中合成：
- **透明输出：** MVC 配置中 `view.CLEAR_COLOR: [0,0,0,0]` → 透明帧。
- **GIF 在确定性 HyperFrames 渲染中会冻结。** 转为 **带 alpha 的 VP9 WebM**：`ffmpeg -i char.gif -c:v libvpx-vp9 -pix_fmt yuva420p char.webm`。（`ffprobe` 会误报 `yuv420p` — alpha 实际完好。）
- **视频契约（linter 会强制 — 运行 `npm run check`）：** `<video>` 必须是**带独立 `id` 的舞台直接子元素**，不要嵌套在带计时的 `<div>` 里（嵌套会**冻结**）；每段 clip 需要自己的 `data-track-index`；淡入淡出需要在末尾硬切 `tl.set(el,{opacity:0})`。
- 文字/**气球** = HTML overlay div，使用完整的 `ink-theater/assets/patrickhand.ttf`（见 ink-theater 字体注意事项）。
- **流水线豁免：** `/animated-drawing` + `/ink-art` 是创意入口，不是 Rule-Zero 流水线 — 无需 `.yaml` manifest。

## 输出与如实限制
GIF（透明）/ MP4（H.264，`avc1`），分辨率来自 `WINDOW_DIMENSIONS`（示例 500×500）。**仅栅格**（变形绘画像素 — 放大可见拉伸纹理），**仅人形**，**无逐笔揭示**，**背景较粗糙**。是「你的涂鸦活过来」的趣味玩法；auto-rig 路径依赖 Docker 服务。不是通用矢量引擎 — 若要会自行绘制的白墨矢量涂鸦，请用 `/ink-art`。

会话评估中的示例渲染：`.tmp/animated-drawings/out/`（`char3_dab.gif`、`char1_zombie.mp4`）。
