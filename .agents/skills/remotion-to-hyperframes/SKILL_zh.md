---
name: remotion-to-hyperframes
description: '将现有 Remotion（React）合成迁移为 HyperFrames HTML。仅在用户明确要求移植/转换/迁移/翻译 Remotion 源码时使用。勿用于：(a) 从零编写新的 HyperFrames 合成；(b) 顺带提到 Remotion；(c) 仅把 Remotion 代码当作参考；(d) 只说「和我的 Remotion 视频一样」但未明确要求迁移——应视为全新构建。有疑虑 → `/general-video`。单向、仅 Remotion：不支持反向导出（HyperFrames→Remotion 或任意框架），非 Remotion 来源（After Effects、Framer Motion、纯 React/CSS）超出范围，请通过 `/general-video` 重新创建。会标记不支持的写法（useState、useEffect、async calculateMetadata、第三方 React 库、`@remotion/lambda`），并推荐运行时互操作而非有损翻译。不确定该移植还是新建，或只是顺带提到 Remotion？→ 先读 `/hyperframes`。'
---

# Remotion 转 HyperFrames

> **动手前先确认路线。** 本技能**仅**用于将现有 **Remotion**（React）合成的源码移植到 HyperFrames。编写**全新**合成（即便灵感来自某段 Remotion 视频）→ 使用创作工作流 / `/general-video`。**超出范围**（单向、仅 Remotion）：不支持反向导出（HyperFrames → Remotion 或任意框架）；**非 Remotion** 来源（After Effects、Framer Motion、纯 React / CSS 动画等）没有可翻译的 Remotion 源码 → 请通过 `/general-video` 原生重建。不确定，或只是顺带提到 Remotion？**请先阅读 `/hyperframes`。**

## 概述

将 Remotion（基于 React）的视频合成翻译为 HyperFrames（HTML + GSAP）合成。多数 Remotion 惯用法在 HyperFrames 中有直接对应——对约 80% 的典型合成，翻译过程是机械性的。本技能编码了映射关系，并通过拒绝翻译与 HF 的 seek 驱动模型不兼容的模式，并推荐 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 中的运行时互操作模式，来防范其余约 20% 的有损情况。

本技能附带**分级测试语料**（T1–T4，共 4 个 fixture），按测得的 SSIM 阈值对翻译结果评分。未跑 eval 就不要声称翻译完成——看起来正确但 SSIM 比已验证基线低 0.05 的翻译，属于静默错误。

## 何时使用

**仅在用户明确要求从 Remotion 迁移时使用本技能。** 示例触发语：

- "port my Remotion project to HyperFrames"
- "convert this Remotion code to HyperFrames"
- "migrate from Remotion"
- "translate this Remotion comp"
- "rewrite this as HyperFrames HTML"

**勿使用本技能的情况：**

- (a) 用户正在编写**新的** HyperFrames 合成，即便其拥有或正在 A/B 测试类似的 Remotion 视频。
- (b) 用户顺带提到 Remotion，但未要求迁移。
- (c) 用户分享 Remotion 代码仅作参考，而非要求翻译。
- (d) 用户要求「和我的 Remotion 视频一样」，但未明确要求迁移源码——应视为全新的 HyperFrames 构建。

**不支持（请拒绝——非本技能职责）：**

- **反向。** 将 HyperFrames 合成导出回 Remotion（或任意其他框架）不是本工作流——翻译方向仅为 Remotion → HyperFrames。请明确说明。
- **非 Remotion 来源。** After Effects 工程（`.aep`）、Framer Motion / 纯 React / CSS 动画，或任何其他工具的源码都不是 Remotion 合成——没有 Remotion 源码可译。请通过 `/general-video` 原生重建，若 HyperFrames 无法表达则拒绝。

有疑虑时，默认使用 `/general-video`（通用 HyperFrames 创作流程）编写原生 HyperFrames 合成。

## 工作流

### 步骤 1：对源码做 Lint

对 Remotion 源码目录运行 [`scripts/lint_source.py`](scripts/lint_source.py)。Lint 会检测无法干净翻译的模式：

- **阻断项**（拒绝 + 推荐互操作）：`useState`、`useReducer`、deps 非空的 `useEffect`/`useLayoutEffect`、async `calculateMetadata`、第三方 React UI 库（MUI、Chakra、Mantine、antd、shadcn、Radix、NextUI）。
- **警告**（丢弃该构造后继续翻译）：`@remotion/lambda` 配置、`delayRender`、`useCallback`、`useMemo`、自定义 hooks。
- **信息**（翻译并附注）：`staticFile`、`interpolateColors`。

若出现任一阻断项，**停止**。阅读 [`references/escape-hatch.md`](references/escape-hatch.md) 并给出推荐说明。警告不阻止翻译——在步骤 3 中丢弃违规构造，并在 `TRANSLATION_NOTES.md` 中记录缺口。`@remotion/lambda` 配置是典型警告：技能会丢弃 import 与 `renderMediaOnLambda(...)` 调用，但翻译合成的其余部分。

### 步骤 2：规划翻译

阅读 [`references/api-map.md`](references/api-map.md)——所有 Remotion API 及其 HF 等价物或分主题参考的索引。根据源码实际用法，确定需要加载哪些主题参考：

| 源码包含                                                                  | 加载参考                                      |
| ------------------------------------------------------------------------- | --------------------------------------------- |
| `Composition`、`defaultProps`、`schema`、`calculateMetadata`              | [`parameters.md`](references/parameters.md)   |
| `Sequence`、`Series`、`Loop`、`AbsoluteFill`、`Freeze`                    | [`sequencing.md`](references/sequencing.md)   |
| `useCurrentFrame`、`interpolate`、`spring`、`Easing`、`interpolateColors` | [`timing.md`](references/timing.md)           |
| `Audio`、`Video`、`Img`、`IFrame`、`staticFile`、`delayRender`            | [`media.md`](references/media.md)             |
| `TransitionSeries`、`@remotion/transitions`                               | [`transitions.md`](references/transitions.md) |
| `@remotion/lottie`                                                        | [`lottie.md`](references/lottie.md)           |
| `@remotion/google-fonts/<Family>`、`Font.loadFont`、`@font-face`          | [`fonts.md`](references/fonts.md)             |

不要全部加载——只加载当前源码需要的部分。

### 步骤 3：生成 HF 合成

输出 `index.html`，包含：

- 根节点 `<div id="stage">` 携带合成的 `data-composition-id`、`data-start="0"`、`data-duration`（秒）、`data-fps`、`data-width`、`data-height`，以及每个标量 prop 对应的一个 `data-*`。
- 扁平的场景 div 列表，带 `data-start` / `data-duration` / `data-track-index`。
- 内联 `<style>` 负责布局；CSS 设定每个动画属性的 `from` 状态。
- 底部单个 `<script>`，内含一条 paused 的 `gsap.timeline({paused: true})`。每个 Remotion `useCurrentFrame()` 推导在 timeline 上对应偏移处变为 tween。
- `window.__timelines["<composition-id>"] = tl;` 向 HF 运行时注册 timeline。

自定义 React 子组件内联为重复 HTML，以 prop 接口为模板（每实例 `data-*` 模式见 [`parameters.md`](references/parameters.md)）。

### 步骤 4：验证

运行 eval  harness——完整指南见 [`references/eval.md`](references/eval.md)。快捷路径：

```bash
# Render Remotion baseline (after npm install in the fixture)
cd remotion-src && npx remotion render <CompositionId> out/baseline.mp4

# Render HF translation
cd ../hf-src && npx hyperframes render --skill=remotion-to-hyperframes --output ../hf.mp4

# SSIM diff
../../scripts/render_diff.sh ./remotion-src/out/baseline.mp4 ./hf.mp4 ./diff
```

阈值：约比该源码复杂度 tier 的 `p05` 低 0.02（见 `eval.md` 中的已验证阈值表）。若 diff 失败，运行 [`scripts/frame_strip.sh`](scripts/frame_strip.sh) 查看**哪些**帧不一致，再重读相关 timing/sequencing/media 参考。

**关键**：两次渲染须使用一致的像素格式。在 Remotion 源码的 `remotion.config.ts` 中设置 `Config.setVideoImageFormat("png")` + `Config.setColorSpace("bt709")`——否则 diff 衡量的是编码器差异（约 0.05 SSIM 损失），而非翻译保真度。

### 步骤 5：记录缺口

凡未干净翻译的部分（丢弃的音量渐变、近似自定义 presentation、字体替换等），在 HF 输出旁写入 `TRANSLATION_NOTES.md`。格式见 [`references/limitations.md`](references/limitations.md)。

## 本技能明确不做的事

- **翻译 React 状态机。** 通过 `useState` + `useEffect` 驱动动画的合成，在 HyperFrames 的 seek 驱动模型下不是确定性逐帧捕获目标。请推荐运行时互操作模式。
- **与 HyperFrames 并行运行 Remotion 渲染管线。** 那是 [PR #214](https://github.com/heygen-com/hyperframes/pull/214) 的运行时互操作模式——针对无法通过本技能 lint 的合成的独立方案。

（`@remotion/lambda` **不是**阻断项——Lambda 配置属于部署，非动画。技能以警告形式丢弃，并翻译其余部分。见 [`references/escape-hatch.md`](references/escape-hatch.md)。）

## 如何自评翻译质量

运行测试语料编排器：

```bash
./assets/test-corpus/run.sh
```

它对 T1、T2、T3（render + diff）和 T4（lint 验证）执行，打印按 tier 的通过/失败表，并输出聚合 JSON 报告。用于在干净 checkout 上端到端验证技能是否正常——以及在编辑任意 reference 后做回归检查。

已验证基线（截至 2026-04-27）：

| Tier | 合成形态                                   | Mean SSIM | Threshold |
| ---- | ------------------------------------------- | --------- | --------- |
| T1   | 单元素淡入                                  | 0.974     | 0.95      |
| T2   | 多场景 + spring + 音频 + 图片               | 0.985     | 0.95      |
| T3   | 数据驱动、自定义子组件、数字递增            | 0.953     | 0.90      |
| T4   | 逃生舱（8 个 lint 用例）                    | 8/8 pass  | n/a       |
