# 评估：如何端到端验证一次翻译

每次翻译都应被度量。本技能提供三个脚本以及分层测试语料库，共同作为翻译质量的门禁。

## 三个脚本

| 脚本                     | 输入                        | 输出                                                                |
| ------------------------ | --------------------------- | ------------------------------------------------------------------- |
| `scripts/lint_source.py` | Remotion 源目录或文件       | JSON 发现项 + 退出码（0 表示干净，1 表示存在阻塞项）                 |
| `scripts/render_diff.sh` | 两个 MP4 路径               | 逐帧 SSIM + JSON 摘要（`mean`、`min`、`p05`、`p95`、`pass`）         |
| `scripts/frame_strip.sh` | 两个 MP4 路径               | 并排对比条带 PNG，用于视觉调试                                       |

按此顺序运行：**lint → render → diff →（若失败）strip**。

## 每个 fixture 的流程

```bash
# 1. Lint the source — blockers mean stop
python3 ../../scripts/lint_source.py ./remotion-src/src/

# 2. Generate any binary assets (T2+T3 only)
[ -f setup.sh ] && ./setup.sh

# 3. Render Remotion baseline
cd remotion-src && npm install && npm run render
# -> remotion-src/out/baseline.mp4

# 4. Render HF translation
cd .. && node ../../../packages/cli/dist/cli.js render hf-src/ --output hf.mp4
# -> hf.mp4

# 5. SSIM diff
../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
# -> diff/summary.json

# 6. If diff fails, generate frame strip for visual inspection
../../scripts/frame_strip.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./strip 8
# -> strip/strip.png
```

## 解读 `diff/summary.json`

```json
{
  "frame_count": 90,
  "mean": 0.974,
  "min": 0.972,
  "max": 0.999,
  "p05": 0.972,
  "p95": 0.983,
  "threshold": 0.95,
  "pass": true
}
```

| 字段          | 含义                                                                        |
| ------------- | --------------------------------------------------------------------------- |
| `mean`        | 所有帧的平均 SSIM；主要汇总指标                                             |
| `min`         | 最差帧；低于阈值表示至少有一帧在结构上错误                                   |
| `p05` / `p95` | 第 5 / 第 95 百分位 — 多数帧落在此区间                                       |
| `threshold`   | 来自 `R2HF_SSIM_THRESHOLD` 环境变量（默认 0.85）                             |
| `pass`        | 是否满足 `mean >= threshold`                                                |

## 已验证的分层阈值

针对实际 Remotion + HF 渲染结果校准：

| 层级 | 合成形态                                    | Mean  | Threshold | Margin |
| ---- | ------------------------------------------- | ----- | --------- | ------ |
| T1   | 单元素淡入                                  | 0.974 | 0.95      | +0.022 |
| T2   | 多场景 + spring + 音频 + 图像               | 0.985 | 0.95      | +0.016 |
| T3   | 数据驱动、自定义子组件、数字递增            | 0.953 | 0.90      | +0.038 |

每个 fixture 的 `expected.json` 包含：

- `ssim_threshold` — `pass` 的门禁阈值
- `validation` — 校准运行中实际测得的数值
- `translation_notes` — 哪些部分有损以及原因

## 关键：编码器配置

Remotion 与 HF 必须输出相同的像素格式，SSIM 才有意义。Remotion 默认 JPEG 输出为 `yuvj420p`（全范围）；HF 输出 `yuv420p`（有限范围）。该不一致约损失 ~0.05 SSIM。

每个 fixture 的 `remotion.config.ts` 应设置：

```ts
Config.setVideoImageFormat("png");
Config.setColorSpace("bt709");
```

若用户源码中没有这些配置，应在翻译步骤中补上 — 否则 diff 度量的是编码器差异，而非翻译保真度。

## 噪声底长什么样

占主导的非翻译噪声是 **系统字体回退差异**。Remotion 内置 Chromium 与 HF 的 `chrome-headless-shell` 在未安装真实字体时对 `font-weight: 800` 的解释不同：

- Remotion 160px 的 HELLO：中等粗细笔画
- HF 160px 的 HELLO：较粗笔画

这约损失 ~0.025 平均 SSIM。在 T1 的 frame strip 中可见。[fonts.md](fonts.md) 说明如何缓解（使用 Inter、显式加载 Google Fonts）。

## 阈值经验法则

将阈值设在实测 `p05` 下方约 0.02：

- 真实的翻译回归会使 mean 下降 0.05 以上 — 会被捕获。
- CI 运行间编码器/字体漂移约在 ~0.01 以内 — 不会被误报。

若某次校准运行的实测 mean 远高于你最初的阈值猜测，**不要**为凑数而收紧阈值。保留余量 — 在不同硬件上重渲染 fixture 会漂移。

## 当 diff 失败时

1. **先看 `frame_strip.sh` 输出。** 在 6–10 个均匀时间点的并排条带可区分失败是结构性的（场景时长错误、元素缺失）还是外观层面（字重不同、轻微时序偏移）。
2. **查看 `diff/ssim.log`。** 逐帧 SSIM 指出**哪些**帧失败。场景中段成簇的差帧 = 动画问题；场景边界处的差帧 = 场景编排问题。
3. **重读相关参考文档。** spring/easing 见 [timing.md](timing.md)，场景边界见 [sequencing.md](sequencing.md)，资源加载见 [media.md](media.md)。

## CI 集成

fixture 尚未接入 CI（`packages/producer/tests/` 在 Docker 内运行；技能语料库需要同等环境）。该栈的 PR 7 将添加编排器，运行全部四个 tier 并输出聚合 pass 报告。目前请按 fixture 手动评估。
