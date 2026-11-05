# kinetic-type — 分类模块

文字是主角；字体排版与动效承载信息。通常无需资产（`asset_needs: []`）。

## 规划（Director）

- **风格优先。** 若项目有 **`design.md` / `frame.md`**（优先级：`frame.md` → `design.md` → `DESIGN.md`），请阅读并采用其 **精确的色板 / 字体 / 约束** — 不要自行编造。无规范时 → 选定一种命名风格，或询问：情绪 + 明/暗 + 任何品牌色/字体。（风格是案例必须覆盖的输入；同一镜头在不同 `design.md` 下应呈现不同观感。）
- 按语义 / 呼吸切分文案为场景（英文约 3–7 词；中文约 4–12 字）。为每个场景标注 **Hook → Build → Punch → Resolve**。
- 每场景 1–2 个 `emphasis_words`。每场景：`emotion` + `motion`（自由描述）+ `beats`。

## 词汇表

动效原语与注册表块：**`references/motion-vocabulary.md`**（slide / scale / fade / blur / typewriter / word_reveal / wave / bounce / slam / scale_pulse / shake / glow / color_shift，以及 18 个 `caption-*` 块）。

## 构建（复用优先）

- 若有合适的 **`caption-*` 块**（`caption-kinetic-slam` / `caption-editorial-emphasis` / …），优先使用：`npx hyperframes add`，并设置 words / `emphasis_words` / palette / font。
- 否则手写：一个全时长 `.clip`；每场景一个 `.group`（flex 居中）；词以 span 呈现；按场景 `motion` 用 `gsap.from()` 做入场；强调词在 beat 上 → `glow` / `scale_pulse`；**seek 安全显隐**（`autoAlpha`）。遵守 `references/builder-contract.md`。
- 参考实现：原型 `v0-text-motion-demo` + `pipeline-demo`。
