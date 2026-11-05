---
name: hyperframes-registry
description: 在 HyperFrames 合成中安装并接入 registry 块与组件。适用于执行 hyperframes add、安装块或组件、将已安装项接入 index.html，或处理 hyperframes.json 的场景。涵盖 add 命令、安装路径、块子合成接入、组件片段合并、registry 发现，以及向上游贡献新块或组件的完整流程（构思 → 脚手架 → 校验 → PR）。
---

# HyperFrames Registry

registry 提供可通过 `hyperframes add <name>` 安装的可复用块与组件。

- **Blocks（块）** — 独立子合成（自带尺寸、时长与时间轴）。在宿主合成中通过 `data-composition-src` 引入。
- **Components（组件）** — 效果片段（无独立尺寸）。直接粘贴进宿主合成的 HTML。

## 快速参考

```bash
hyperframes add data-chart              # install a block
hyperframes add grain-overlay           # install a component
hyperframes add shimmer-sweep --dir .   # target a specific project
hyperframes add data-chart --json       # machine-readable output
hyperframes add data-chart --no-clipboard  # skip clipboard (CI/headless)
```

安装完成后，CLI 会打印写入的文件列表，以及可粘贴到宿主合成中的片段。该片段仅为起点 — 接入块时，你还需要添加 `data-composition-id`（必须与块内部的 composition ID 一致）、`data-start` 和 `data-track-index` 属性。

注意：`hyperframes add` 仅适用于块与组件。示例请改用 `hyperframes init <dir> --example <name>`。

## 安装路径

块默认安装到 `compositions/<name>.html`。
组件默认安装到 `compositions/components/<name>.html`。

这些路径可在 `hyperframes.json` 中配置：

```json
{
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

完整说明见 [install-locations.md](./references/install-locations.md)。

## 接入块

块是独立合成 — 在宿主 `index.html` 中通过 `data-composition-src` 引入：

```html
<div
  data-composition-id="data-chart"
  data-composition-src="compositions/data-chart.html"
  data-start="2"
  data-duration="15"
  data-track-index="1"
  data-width="1920"
  data-height="1080"
></div>
```

关键属性：

- `data-composition-src` — 块 HTML 文件路径
- `data-composition-id` — 必须与块内部 ID 一致
- `data-start` — 块在宿主时间轴上出现的时间（秒）
- `data-duration` — 块播放时长
- `data-width` / `data-height` — 块画布尺寸
- `data-track-index` — 图层顺序（数值越大越靠前）

完整说明见 [wiring-blocks.md](./references/wiring-blocks.md)。

## 接入组件

组件是片段 — 将其 HTML 粘贴进合成的 markup，CSS 粘贴进样式块，JS（如有）粘贴进脚本：

1. 阅读已安装文件（例如 `compositions/components/grain-overlay.html`）
2. 将 HTML 元素复制到合成的 `<div data-composition-id="...">` 内
3. 将 `<style>` 块复制到合成的样式中
4. 将任意 `<script>` 内容复制到合成脚本中（位于你的时间轴代码之前）
5. 若组件提供 GSAP 时间轴集成（见片段中的注释块），在时间轴中加入相应调用

完整说明见 [wiring-components.md](./references/wiring-components.md)。

## 发现

浏览可用项：

```bash
# Read the registry manifest
curl -s https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry/registry.json
```

每项的 `registry-item.json` 包含：name、type、title、description、tags、dimensions（仅块）、duration（仅块）以及文件列表。

按 type 与 tags 筛选的说明见 [discovery.md](./references/discovery.md)。

## 贡献新块或组件

若要**新建** registry 项（字幕样式、VFX 块、转场、下三分之一或可复用组件）并以 upstream PR 形式交付 — 而非安装已有项 — 请按 [contributing.md](./references/contributing.md) 中的完整流程：构思 → 脚手架 → 构建 → 校验 → 预览 → 发布。可复制粘贴的起始模板（caption / VFX / component / `registry-item.json`）见 [templates.md](./references/templates.md)。
