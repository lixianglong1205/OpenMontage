# HyperFrames Skills — 来源说明

`.agents/skills/` 下的 12 个 HyperFrames 系列技能均从上游 HyperFrames 单体仓库 vendored 引入：

- **Source**: https://github.com/heygen-com/hyperframes
- **Vendored commit**: `3351fb1a` (`chore: release v0.7.17`, 2026-06-27)
- **Vendored tag**: `v0.7.17`
- **Vendor date**: 2026-06-27
- **Vendored by**: re-vendor on branch `chore/version-bumps-and-hf-resync`

## 已 vendored 的内容

**自先前 0.4.2 时代副本重新 vendored（上游重命名/重构）：**

| 技能 | 说明 |
|---|---|
| `hyperframes` | 0.7 中为精简入口；深度内容已拆至下方各专项技能。 |
| `hyperframes-cli` | 0.7 中大幅扩展（由 1 个文件增至 7 个）。现原生覆盖 `validate`、`inspect`、`snapshot`、`benchmark`、`lambda` 等——原先 OM 本地补丁中关于 `validate` 的说明已过时并已移除。 |
| `hyperframes-registry` | Block/组件注册表工作流。 |
| `website-to-video` | 上游由 `website-to-hyperframes` 重命名。 |

**新 vendored（0.5–0.7 中的战略新增）：**

| 技能 | 在 OpenMontage 中的价值 |
|---|---|
| `hyperframes-core` | 合成契约——`data-*` 时序、轨道、子合成。相当于 0.4 版 `hyperframes` 中拆出的核心部分。 |
| `hyperframes-creative` | 非动画向创意指导——调色、字体、旁白、节拍规划。 |
| `hyperframes-media` | 音频与媒体资产——TTS、BGM、SFX、转写、字幕、背景移除。 |
| `hyperframes-animation` | 全部动画知识（规则、蓝图、转场、技法、7 种运行时适配器）。取代原先散落在 `hyperframes` 中的临时动效指引。 |
| `media-use` | Agent Media OS——单一 `resolve` 动词通过项目/全局缓存与 HeyGen 目录，将 BGM/SFX/图片/图标需求解析为本地文件。对 OpenMontage 资产阶段具有战略价值。 |
| `motion-graphics` | 短设计向动效模式（kinetic typography、数据揭示、Logo 片头、下三分之一条）。 |
| `remotion-to-hyperframes` | 迁移指南——OpenMontage 同时运行两种运行时，直接相关。 |
| `music-to-video` | 使用 `hyperframes beats` 的节拍同步、音乐驱动视频工作流。 |

## 有意未 vendored

以下上游技能与 HyperFrames 工作流强绑定，会与 OpenMontage 自有流水线路由竞争或重复。按流水线需求再评估：

`embedded-captions`, `faceless-explainer`, `general-video`, `pr-to-video`, `product-launch-video`, `slideshow`, `talking-head-recut`.

## 重新同步说明

从较新的上游重新 vendored：

```bash
cd C:/Users/ishan/Documents/hyperframes
git pull --ff-only origin main
# Then in OpenMontage:
cd /c/Users/ishan/Documents/OpenMontage
HF=C:/Users/ishan/Documents/hyperframes
for d in hyperframes hyperframes-cli hyperframes-registry hyperframes-core \
         hyperframes-creative hyperframes-media hyperframes-animation \
         media-use motion-graphics remotion-to-hyperframes \
         music-to-video website-to-video; do
  rm -rf ".agents/skills/$d"
  cp -r "$HF/skills/$d" ".agents/skills/$d"
done
# Then update vendor commit/tag/date at the top of this file.
```

## 未来自动化

上游 0.7 新增 `hyperframes skills`——带 freshness manifest 与版本检查的 CLI，用于安装/更新 HF 技能。可考虑将其作为机械层面的唯一事实来源，替代手工 vendored（亦可在多 Agent 环境中自动标记陈旧）。参见 HF 历史中的 `feat(cli): skills freshness — version check, manifest, global install + multi-agent mirror (#1753)`。
