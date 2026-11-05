# preview、play、render、publish

提供服务、渲染与分享相关命令。

## preview

```bash
npx hyperframes preview                   # serve current directory
npx hyperframes preview --port 4567       # custom port (default 3002)
```

文件变更时会热重载。会自动在浏览器中打开 Studio —— 完整的时间线编辑器，用户可在渲染前播放视频并手动编辑任意内容。这是审阅界面，而不仅是查看器。

将项目交还给用户时，应使用 Studio 项目 URL，而不是源 `index.html` 路径：

```text
http://localhost:<port>/#project/<project-name>
```

请使用实际端口与项目目录名；将 `index.html` 视为源代码上下文，而非预览界面。例如，在 `codex-openai-video` 中执行 `npx hyperframes preview --port 3017` 后，应报告 `http://localhost:3017/#project/codex-openai-video`。

## play（轻量播放器）

```bash
npx hyperframes play                  # current project, port 3003
npx hyperframes play ./my-video       # specific project
npx hyperframes play --port 8080      # custom port
```

`play` 通过可嵌入的 `<hyperframes-player>` Web 组件提供合成内容，而非完整 Studio UI。适合分享预览链接，或在不需要编辑器与面板、Studio 过重时使用。`play` 报告的是纯 `http://localhost:<port>` URL —— 不含 `#project/<name>` 片段（该片段仅为 Studio 路由约定，仅 `preview` 使用）。

播放器的 `playback-rate` 属性（预览速度控制，驱动时间线的 `timeScale`）被限制在 `[0.1, 5]`；值 `≤ 0` 或非有限数会回退为 `1`。这是预览/播放旋钮，不是合成 `data-*` 属性 —— 创作的运动仍以 `1×` 渲染。

### 使用外部浏览器启动（preview + play）

`preview` 与 `play` 均可在显式指定的 Chromium 兼容浏览器中打开，而非系统默认浏览器。两种场景：隔离的 Chromium 配置文件，或外部 CDP 附加（DevTools / Playwright / Puppeteer / browser-MCP）。**HyperFrames 本身不拥有 CDP 自动化** —— 此处仅暴露端点；如何连接由你自行负责。勿与 `--browser-gpu`（控制捕获时 Chrome GPU 访问的 `render` 标志）混淆。

| 标志                      | 类型            | 说明                                                                                                                                                                                           |
| ------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--browser-path`          | path            | Chromium 兼容可执行文件的绝对路径（`/usr/bin/chromium`、`/Applications/Brave Browser.app/...`）。                                                                                 |
| `--user-data-dir`         | path            | Chromium 兼容配置文件目录。需要 `--browser-path`。使用临时目录以免状态写入主配置文件。                                                             |
| `--remote-debugging-port` | integer 1-65535 | 在指定端口打开 Chromium CDP 端点。**需要同时**提供 `--browser-path` 与 `--user-data-dir` —— 否则拒绝，以免 CDP 端点意外泄漏到主配置文件。 |

```bash
# Open preview in an isolated Chromium profile
npx hyperframes preview --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile

# Same plus a CDP endpoint on :9222 (attach DevTools / Playwright / etc.)
npx hyperframes play --browser-path /usr/bin/chromium --user-data-dir /tmp/hf-profile --remote-debugging-port 9222
```

校验在任意服务启动前执行，无效值会干净退出，不会留下监听中的套接字。

## render

> 仅在用户已在 `preview` 中审阅并批准后渲染。检查通过时不要自动渲染。

```bash
npx hyperframes render                                # standard MP4 from cwd
npx hyperframes render ./my-video --output ./out.mp4  # render from outside the project dir
npx hyperframes render --output final.mp4             # named output (no timestamp)
npx hyperframes render -c compositions/intro.html -o intro.mp4  # render a specific sub-composition file
npx hyperframes render --quality draft                # fast iteration
npx hyperframes render --fps 60 --quality high        # final delivery
npx hyperframes render --format webm                  # transparent WebM
npx hyperframes render --docker                       # byte-identical
```

> 默认 `--output` 为 `renders/<project-name>_<YYYY-MM-DD>_<HH-MM-SS>.<ext>` —— 每次渲染带时间戳，连续运行不会互相覆盖。传入 `--output` 可获得稳定文件名。

| 标志                                 | 选项                                                                                            | 默认值                        | 说明                                                                                                                                                                                                                                                                                    |
| ------------------------------------ | -------------------------------------------------------------------------------------------------- | ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `dir`（位置参数）                   | path                                                                                               | cwd                            | 项目目录。省略则使用当前工作目录。                                                                                                                                                                                                                                |
| `--composition`, `-c`                | path to composition file                                                                           | `index.html`                   | 渲染指定合成文件（如 `compositions/intro.html`），而非项目的 `index.html`。                                                                                                                                                                               |
| `--output`, `-o`                     | path                                                                                               | `renders/<project>_<ts>.<ext>` | 输出路径。默认为带时间戳（`<project-name>_YYYY-MM-DD_HH-MM-SS.<ext>`）。                                                                                                                                                                                                        |
| `--fps`                              | 24, 30, 60                                                                                         | 30                             | 60fps 渲染时间约翻倍                                                                                                                                                                                                                                                                |
| `--quality`                          | draft, standard, high                                                                              | standard                       | draft 用于迭代                                                                                                                                                                                                                                                                      |
| `--format`                           | mp4, webm, mov, gif, png-sequence                                                                  | mp4                            | WebM/MOV 可带透明渲染；gif 用于 GitHub PR/README/文档内联自动播放（两遍调色板编码，fps 上限 30 —— 建议 `--fps 15` —— 无音频，仅 1-bit 透明，HDR 回退 SDR）；png-sequence 将 RGBA 帧写入目录（供 AE/Nuke/Fusion 导入） |
| `--gif-loop`                         | 0-65535                                                                                            | 0                              | GIF 循环次数；`0` 为无限循环。仅与 `--format gif` 同用。                                                                                                                                                                                                                             |
| `--resolution`                       | landscape, portrait, landscape-4k, portrait-4k, square, square-4k（及别名 `1080p`、`4k`、`uhd`） | —                              | 通过 Chrome `deviceScaleFactor` 超采样。宽高比须与合成一致；缩放须为整数。不可与 `--hdr` 同用。                                                                                                                                                             |
| `--crf`                              | 0-51                                                                                               | —                              | 编码器 CRF（越低质量越高）。与 `--video-bitrate` 互斥。                                                                                                                                                                                                         |
| `--video-bitrate`                    | e.g. `10M`, `5000k`                                                                                | —                              | 目标码率。与 `--crf` 互斥。                                                                                                                                                                                                                                         |
| `--hdr`                              | flag                                                                                               | off                            | 即使源为 SDR 也强制 HDR 输出。仅 MP4。                                                                                                                                                                                                                                        |
| `--sdr`                              | flag                                                                                               | off                            | 即使源为 HDR 也强制 SDR。                                                                                                                                                                                                                                                         |
| `--workers`                          | number or `auto`                                                                                   | auto                           | 每个 worker 会启动 Chrome（约 256 MB）                                                                                                                                                                                                                                                      |
| `--docker`                           | flag                                                                                               | off                            | 跨主机可复现输出                                                                                                                                                                                                                                                         |
| `--gpu`                              | flag                                                                                               | off                            | GPU 加速 FFmpeg 编码（NVENC / VideoToolbox / VAAPI / QSV）                                                                                                                                                                                                                     |
| `--browser-gpu` / `--no-browser-gpu` | flag                                                                                               | auto（本地）, off（docker）     | 主机 GPU 用于 Chrome/WebGL 捕获                                                                                                                                                                                                                                                        |
| `--browser-timeout`                  | seconds (0.001–86400)                                                                              | 60                             | Puppeteer 加载入口 HTML 的页面导航超时。重型合成（大量视频/字体/远程资源）无法在默认 60s 内达到 `domcontentloaded` 时可调高。                                                                                                         |
| `--quiet`                            | flag                                                                                               | off                            | 抑制详细输出                                                                                                                                                                                                                                                                  |
| `--strict`                           | flag                                                                                               | off                            | lint 报错时失败                                                                                                                                                                                                                                                                      |
| `--strict-all`                       | flag                                                                                               | off                            | lint 报错与警告均失败                                                                                                                                                                                                                                                         |
| `--variables`                        | JSON object                                                                                        | —                              | 覆盖 `data-composition-variables` 中声明的值                                                                                                                                                                                                                                 |
| `--variables-file`                   | path                                                                                               | —                              | 含变量值的 JSON 文件（`--variables` 的替代）                                                                                                                                                                                                                            |
| `--strict-variables`                 | flag                                                                                               | off                            | `--variables` 中存在未声明键或类型不匹配时渲染失败                                                                                                                                                                                                                       |

**质量建议：** 迭代用 `draft`，审阅用 `standard`，最终交付用 `high`。

**参数化渲染：** 合成在 `<html>` 根节点通过 **`data-composition-variables`** 声明变量 —— JSON **声明数组**（每项 `{id, type, label, default}`）定义 schema（结构）。内部脚本通过 `window.__hyperframes.getVariables()` 读取解析后的值。CLI `--variables '{"title":"Q4 Report"}'` 是按 id 键的 JSON **对象**，用于单次渲染覆盖上述默认；未提供的键沿用默认，因此同一合成在开发预览与生产环境行为一致。子合成宿主还可用 `data-variable-values` 按实例覆盖。完整模式见 `hyperframes-core` skill。

## publish

```bash
npx hyperframes publish              # upload current project, return public URL
npx hyperframes publish ./my-video   # specific project
npx hyperframes publish --yes        # skip the confirmation prompt (scripts/CI)
```

上传项目源码（HTML + 资源）并返回可在浏览器中渲染的稳定公开 URL。可用于渲染 MP4 前分享草稿审阅，或在外部嵌入合成。上传前会展示 lint 结果，但不阻塞上传。
