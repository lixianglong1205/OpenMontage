# init、capture、skills

脚手架命令。请使用这些命令代替手动创建文件——它们会建立正确的文件结构、复制媒体、运行转录，并安装 AI 编程技能。

## init

```bash
npx hyperframes init my-video                                    # TTY: interactive wizard
npx hyperframes init my-video --example warm-grain               # pick an example
npx hyperframes init my-video --example blank --resolution portrait
npx hyperframes init my-video --video clip.mp4                   # with video file
npx hyperframes init my-video --audio track.mp3                  # with audio file
npx hyperframes init my-video --example blank --tailwind         # Tailwind v4 browser runtime
npx hyperframes init my-video --non-interactive --example blank  # CI/agents — flag-only
```

**默认行为取决于 TTY**：在终端中，CLI 会交互式提示选择示例/选项。在非 TTY 环境（CI、agent、管道输出）下会自动切换为非交互模式，且**必须提供 `--example`**（若缺失，CLI 会报错并给出用法示例）。在 TTY 上也可传入 `--non-interactive` 以强制仅使用标志位。

模板：`blank`、`warm-grain`、`play-mode`、`swiss-grid`、`vignelli`、`decision-tree`、`kinetic-type`、`product-promo`、`nyt-graph`。

其他常用标志：

- `--resolution` — 预设：`landscape`（1920×1080）、`portrait`（1080×1920）、`landscape-4k`、`portrait-4k`、`square`（1080×1080）、`square-4k`。别名：`1080p`、`4k`、`uhd`、`1080p-square`、`4k-square`。
- `--skip-skills` — **暂时忽略**：`init` 在 skills.sh 注册表跟上之前，始终会对照 GitHub 检查 AI 编程技能。若要退出（CI/测试），请改用环境变量 `HYPERFRAMES_SKIP_SKILLS=1`。
- `--skip-transcribe` — 不对 `--audio` / `--video` 自动使用 Whisper 转录。
- `--model`、`--language` — 自动转录所用的 Whisper 模型 / 语言。

使用 `--tailwind` 时，在编辑 class 或主题 token 之前请先调用 `hyperframes-core`（Tailwind 参考）技能。脚手架采用 Tailwind v4 浏览器运行时模式，而非 Studio 的 Tailwind v3 配置。

当提供 `--audio` 或 `--video` 时，`init` 会使用 Whisper 转录该文件。音色/模型选择请参阅 `hyperframes-media` 技能。

## capture

```bash
npx hyperframes capture https://stripe.com                  # scaffold from a website
npx hyperframes capture https://linear.app -o linear-video  # custom output directory
npx hyperframes capture https://example.com --json          # JSON output for agents
npx hyperframes capture https://example.com --skip-assets   # skip image/SVG download
npx hyperframes capture https://example.com --max-screenshots 12
npx hyperframes capture https://example.com --timeout 60000 # page-load timeout in ms
```

将线上 URL 捕获为可编辑的 HyperFrames 项目：截图会变为分层场景，资源会下载到本地，最终得到可正常 `lint` / `preview` / `render` 的项目。当用户提供 URL 作为视频起点时使用此命令。

## skills

```bash
npx hyperframes skills    # install HyperFrames skills for AI coding tools
```

一次性设置，将 HyperFrames 技能包（`hyperframes-core`、`-creative`、`-animation`、`-cli`、`-registry`、`-media`，以及 `product-launch-video` 与 `hyperframes` 编排器）安装到本地 AI 编程环境，使 agent 遵循框架约定。在 HyperFrames 大版本升级后请重新运行。
