---
name: media-use
description: Agent Media OS — 将任意媒体需求（BGM、SFX、图片、图标）解析为冻结的本地文件与台账记录。单一动词（`resolve`）完成完整级联：项目缓存、全局缓存、HeyGen 目录搜索、冻结、注册。搜索过程留在磁盘，向 agent 返回路径。当合成需要背景音乐、音效、图片或图标时使用。
---

# media-use

将媒体需求解析为冻结的本地文件。一个动词、四种类型、零上下文噪音。

## 何时使用

每当合成需要媒体——背景音乐、音效、图片或图标——时调用 `resolve`。media-use 搜索 HeyGen 目录、下载最佳匹配、在本地冻结并登记到 manifest。agent 只收到一行结果；所有搜索噪音留在磁盘上。

## Resolve

```bash
node <SKILL_DIR>/scripts/resolve.mjs --type <type> --intent "<description>" --project <dir>
```

返回一行：`resolved <id> → <path> (<type>, <metadata>)`

### 类型

| 类型    | 查找内容       | 提供方                                 |
| ------- | ------------------- | ---------------------------------------- |
| `bgm`   | 背景音乐    | HeyGen 音频目录（1 万+ 曲目）       |
| `sfx`   | 音效       | 内置 19 文件库 + HeyGen 目录 |
| `image` | 照片、背景 | HeyGen 资源搜索（7.5 万+ 矢量）       |
| `icon`  | 图标、Logo        | HeyGen 资源搜索（type=icon）          |

### 示例

```bash
# Background music
node <SKILL_DIR>/scripts/resolve.mjs --type bgm --intent "upbeat tech launch" --project .
# → resolved bgm_001 → .media/audio/bgm/bgm_001.mp3 (bgm, 25s)

# Sound effect
node <SKILL_DIR>/scripts/resolve.mjs --type sfx --intent "whoosh" --project .
# → resolved sfx_001 → .media/audio/sfx/sfx_001.mp3 (sfx, 0.57s)

# Image
node <SKILL_DIR>/scripts/resolve.mjs --type image --intent "gradient tech background" --project .
# → resolved image_001 → .media/images/image_001.jpg (image)

# Icon
node <SKILL_DIR>/scripts/resolve.mjs --type icon --intent "rocket" --project .
# → resolved icon_001 → .media/images/icon_001.png (icon, transparent)
```

### 标志

| 标志            | 说明                                |
| --------------- | ------------------------------------------ |
| `--type, -t`    | 媒体类型：bgm、sfx、image、icon          |
| `--intent, -i`  | 需求描述（自然语言）           |
| `--entity, -e`  | 用于缓存匹配的实体名（可选）  |
| `--project, -p` | 项目目录（默认：`.`）             |
| `--adopt`       | 批量将现有 assets/ 导入 manifest |
| `--json`        | 输出 JSON 而非单行结果     |

## 工作原理

1. 检查项目 `.media/manifest.jsonl` 是否存在与 prompt 完全匹配的记录
2. 扫描现有 `assets/` 目录，查找未注册且符合需求的文件
3. 检查全局缓存 `~/.media/` 是否有可复用资源
4. 通过提供方搜索（HeyGen 音频目录、HeyGen 资源搜索）
5. 将文件冻结到 `.media/<type>/`，登记到 manifest，并重新生成 `index.md`

agent 只收到**一行**结果。候选、评分、来源信息留在磁盘上。

## 接入现有项目

多数 HyperFrames 项目的 `assets/` 中已有资源。media-use 可接入它们：

```bash
node <SKILL_DIR>/scripts/resolve.mjs --adopt --project .
# → adopted 9 assets from assets/
#   bgm_001 → assets/bgm/mango-fizz.mp3 (bgm, 146.6s)
#   image_001 → assets/images/avatar.jpg (image, 400×400)
```

`ffprobe` 会提取真实的时长与尺寸。在 resolve 过程中，`assets/` 内未注册且与 intent 匹配的文件会被即时接入。

## 阅读清单

resolve 或 adopt 之后，阅读 `.media/index.md` 查看完整清单：

```
# .media · 4 assets

id         type   dur   dims       path                          description
bgm_001    bgm    25s   —          .media/audio/bgm/bgm_001.mp3  upbeat tech launch
sfx_001    sfx    0.6s  —          .media/audio/sfx/sfx_001.mp3  whoosh
image_001  image  —     1920×1080  .media/images/image_001.jpg   gradient tech background
icon_001   icon   —     200×200    .media/images/icon_001.png    rocket
```

## 跨项目复用

resolve 时会自动缓存资源。对相同 prompt 的后续 resolve 会命中 `~/.media/` 的全局缓存——无需重新下载、无需调用提供方。使用 `organize --promote <id>` 可显式提升某资源，使其可在所有项目中复用。

## 文件

- `.media/manifest.jsonl` — 机器侧单一事实来源（SSOT），每行一条 JSON 记录
- `.media/index.md` — 供 agent 阅读的表格（id、type、dur、dims、path、description）
- `~/.media/` — 全局跨项目复用缓存（按内容寻址，SHA-256）

## 使用的 CLI 工具

| 工具      | 用途                                    | 是否必需     |
| --------- | ------------------------------------------ | ------------- |
| `ffprobe` | 在 adopt 时探测时长、尺寸、编解码器 | 是           |
| `heygen`  | 音频目录、资源搜索                | 使用提供方时需要 |

安装 `heygen` CLI（单一静态二进制，无运行时）并完成认证：

```bash
curl -fsSL https://static.heygen.ai/cli/install.sh | bash   # installs latest to ~/.local/bin
heygen update                                               # if already installed: needs >= v0.1.6
export HEYGEN_API_KEY=<your-key>                            # or: heygen auth login --key <key>
```

需要 **heygen >= v0.1.6** — 提供方标签会使用白名单中的 `--headers 'X-HeyGen-Client-Source: media-use'` 标志，该标志自 v0.1.6 起加入。`asset search` 是预发布命令，不会出现在 `heygen --help` 中，但可以运行。若 PATH 上没有 `heygen`（或没有有效密钥），提供方会向 stderr 打印一行诊断信息，resolve 会继续尝试直至「无提供方可解析」。
