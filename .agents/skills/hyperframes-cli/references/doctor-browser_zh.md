# doctor、browser

环境诊断与捆绑 Chrome 管理。当渲染或预览失败时，请先运行这些命令。

## doctor

```bash
npx hyperframes doctor
npx hyperframes doctor --json     # CI / agent output (always exit 0; gate on payload `ok`)
```

运行独立检查，并将每一项报告为 ok/warn/fail：

- **Version** — 已安装的 CLI 与 npm 上的最新版本（过旧时会提示升级）
- **Node.js** — 需要 ≥ 22
- **CPU**、**Memory**、**Disk** — 主机资源
- **Environment** — 影响渲染器的环境变量
- **FFmpeg** / **FFprobe** — 是否找到、版本、编解码器
- **Chrome** — 捆绑或系统 Chrome、版本、路径
- **Docker** / **Docker running** — 仅在 `render --docker` 时需要
- **/dev/shm** — 仅容器内

在以下情况请先运行 `doctor`：

- `render` 因 Chrome 或 FFmpeg 报错失败。
- `preview` 能打开但 composition 无法加载。
- 全新机器从未运行过 HyperFrames。

常见问题：

- **缺少 FFmpeg** — 通过 `brew install ffmpeg`（macOS）或系统包管理器安装。
- **缺少捆绑 Chrome** — 运行 `npx hyperframes browser ensure`。
- **内存不足** — 关闭其他 Chrome 实例、降低 `--workers`，或使用 `--quality draft`。

## browser

```bash
npx hyperframes browser ensure    # find or download the pinned Chrome
npx hyperframes browser path      # print the browser executable path (for scripting)
npx hyperframes browser clear     # remove the cached Chrome download
```

管理 HyperFrames 用于渲染的 Chrome 构建。锁定版本是因为不同 Chrome 版本的像素输出会漂移——使用捆绑构建可在各机器间保持渲染输出可复现。

在脚本中嵌入二进制路径请使用 `path`：`$(npx hyperframes browser path)`。
