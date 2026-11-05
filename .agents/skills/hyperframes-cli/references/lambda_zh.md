# lambda — 在 AWS Lambda 上云端渲染

将 HyperFrames 分布式渲染部署到 AWS Lambda，并从本地笔记本或 CI 驱动渲染。封装 `@hyperframes/aws-lambda` SDK 与 AWS SAM。端到端只需三条命令：

```bash
npx hyperframes lambda deploy
npx hyperframes lambda render ./my-project --width 1920 --height 1080 --wait
npx hyperframes lambda destroy
```

## 何时使用 Lambda 与本地 render

- **本地 `render`** — 开发循环迭代、单机、1080p 下几分钟以内的任务。
- **`lambda render`** — 长视频、4K、大批量并行，或本地 Chrome 会超时 / 耗尽内存的场景。按调用计费，无空闲成本。

一次性短渲染不值得承担部署开销。

## 前提条件

- 已配置 AWS 凭证（环境变量、`~/.aws/credentials`、SSO 或 IMDS）。
- AWS SAM CLI 在 `PATH` 中。
- `bun` 在 `PATH` 中（用于构建 Lambda handler ZIP）。

## 子命令

### deploy

```bash
npx hyperframes lambda deploy \
  --stack-name=hyperframes-prod \
  --region=us-east-1 \
  --concurrency=8 \
  --memory=10240
```

构建 `packages/aws-lambda/dist/handler.zip` 并通过 SAM 部署栈（Lambda + Step Functions + S3 + IAM）。幂等 — 在同一 `--stack-name` 上重复运行且无任何变更时为 no-op。写入 `<cwd>/.hyperframes/lambda-stack-<name>.json`，后续子命令无需再调用 `describe-stacks`。

| Flag            | Default                         | Description                   |
| --------------- | ------------------------------- | ----------------------------- |
| `--stack-name`  | `hyperframes-default`           | CloudFormation 栈名称         |
| `--region`      | `AWS_REGION` env or `us-east-1` | AWS 区域                      |
| `--profile`     | `AWS_PROFILE` env               | 具名 AWS 凭证配置文件         |
| `--concurrency` | `8`                             | Lambda 预留并发               |
| `--memory`      | `10240`                         | Lambda 内存（MB）             |
| `--skip-build`  | off                             | 复用已有 `handler.zip`        |

### sites create

```bash
npx hyperframes lambda sites create ./my-project
# → siteId: abc1234deadbeef0  (同一目录树重复运行保持稳定)

npx hyperframes lambda render ./my-project --site-id=abc1234deadbeef0 ...
```

将 `<projectDir>` 打包并上传到 S3，使用内容寻址键。返回可复用的稳定 `siteId` — 同一目录树再次渲染可跳过上传。

### render

```bash
npx hyperframes lambda render ./my-project \
  --width 1920 --height 1080 --fps 30 --format mp4 \
  --chunk-size 240 --max-parallel-chunks 16 \
  --wait
```

启动 Step Functions 执行。除非设置 `--wait`，否则立即返回 `renderId`；设置 `--wait` 时 CLI 会阻塞至完成并流式输出每个 chunk 的进度行。添加 `--json` 可得到机器可解析的输出。

| Flag                    | Description                                                                                                                                                                                                                                                                                                                                                   |
| ----------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--width` / `--height`  | 输出像素尺寸                                                                                                                                                                                                                                                                                                                                                  |
| `--output-resolution`   | 超采样预设（启用 Chrome `deviceScaleFactor`）— `landscape` / `landscape-4k` / `portrait` / `portrait-4k` / `square` / `square-4k`，以及别名（`1080p`、`4k`、`uhd`、`hd`、`1080p-portrait`、`4k-portrait`、`1080p-square`、`4k-square`）。用于在按 1080p 创作的作品上输出 4K 而无需重新排版 — 见下方 footgun。                                              |
| `--fps`                 | `24` / `30` / `60`                                                                                                                                                                                                                                                                                                                                            |
| `--format`              | `mp4` / `mov` / `png-sequence`（默认 `mp4`）                                                                                                                                                                                                                                                                                                                  |
| `--codec`               | `h264` / `h265`（仅 mp4）                                                                                                                                                                                                                                                                                                                                     |
| `--quality`             | `draft` / `standard` / `high`                                                                                                                                                                                                                                                                                                                                 |
| `--chunk-size`          | 每个 chunk 的帧数（默认 `240`）                                                                                                                                                                                                                                                                                                                               |
| `--max-parallel-chunks` | 最大并发 chunk 数（默认 `16`）                                                                                                                                                                                                                                                                                                                                |
| `--site-id`             | 复用已有 site（跳过上传）                                                                                                                                                                                                                                                                                                                                     |
| `--wait`                | 阻塞至完成并流式输出进度                                                                                                                                                                                                                                                                                                                                      |
| `--json`                | 机器可解析的进度快照                                                                                                                                                                                                                                                                                                                                          |

**`--width` / `--height` footgun。** 对 `data-width="1920"` 的作品设置 `--width 3840 --height 2160` 会静默得到 1080p — 运行时按作品创作尺寸排版页面，CLI 标志对布局无效。要真正输出 4K，请使用 `--output-resolution 4k`（通过 `deviceScaleFactor` 超采样）。当 CLI 尺寸与作品的 `data-width` / `data-height` 不一致且未设置 `--output-resolution` 时，CLI 会打印警告；使用 `--json` 或磁盘上无 `index.html`（`--site-id` 流程）时抑制该警告。

### progress

```bash
npx hyperframes lambda progress hf-render-abcd1234
npx hyperframes lambda progress arn:aws:states:us-east-1:...:execution:...
```

打印一次快照 — 总进度百分比、已渲染帧数、Lambda 调用次数、累计费用及任何错误。接受裸 `renderId`（相对栈的状态机 ARN 解析）或完整 SFN 执行 ARN。

### destroy

```bash
npx hyperframes lambda destroy
```

调用 `sam delete --no-prompts` 并删除本地状态文件。**渲染用 S3 桶配置为 `Retain`**，栈销毁后仍保留 — 若需回收存储，请在 AWS 控制台 / CLI 中清空并删除。

### 不可重试的错误

部分失败会被 Step Functions 状态机短路，不会走完 4×15 分钟的重试预算。`progress` 会立即展示这些错误及错误类名；看到此类错误时不要盲目再次执行 `lambda render`。

- **`ChromeBinaryUnavailableError`** — `@sparticuz/chromium` 返回空或缺失的可执行路径。先前某个 chunk 在解压过程中遇到 `Sandbox.Timedout`，温实例会卡住直至执行环境回收。补救：修改 Lambda 环境变量（强制新执行环境）或再次 `lambda deploy`。非瞬时渲染失败；重试会在同一卡住的实例上消耗预算。
- **`FFMPEG_VERSION_MISMATCH`** / **`PLAN_HASH_MISMATCH`** — 规划器与执行器版本漂移。请重新部署。

### policies

打印或校验 CLI 所需的最小 IAM 权限。

```bash
npx hyperframes lambda policies user                                  # IAM 用户的内联策略
npx hyperframes lambda policies role --principal=cloudformation       # { TrustRelationship, InlinePolicy }
npx hyperframes lambda policies validate ./infra/iam/hf-deploy.json   # CI 门禁
```

`validate` 读取 JSON 策略文档，将其 `Effect: Allow` 动作并集（展开 `s3:*` / `s3:Get*` / `*` 通配符）与 CLI 所需动作集比对。缺失动作输出到 stderr；命令以非零退出。接入 CI 可在下次部署失败前捕获策略漂移。

默认动作集故意较宽（`Resource: "*"`），因为 CloudFormation 在每位采用者首次部署时会创建新 ARN。若安全策略要求，可在首次运行后收紧 `Resource`。

## 状态文件

`hyperframes lambda` 在 `<cwd>/.hyperframes/lambda-stack-<name>.json` 下存储每栈元数据（桶名、状态机 ARN、区域）。非机密，但可识别 AWS 账户。按工作流提交到仓库或加入 `.gitignore`。

## 费用与清理

- `lambda destroy` 移除 SAM 栈但**保留 S3 桶**（`Retain`）。若需回收存储请手动删除。
- Lambda 按调用次数 + 时长计费。`progress` 报告累计费用。
- `--concurrency` 限制并行 Lambda 调用 — 与账户配额对齐。
- `--chunk-size` 与 `--max-parallel-chunks` 在单 chunk 开销与并行度之间权衡；较大 chunk 降低协调开销，较小 chunk 并行更激进。
