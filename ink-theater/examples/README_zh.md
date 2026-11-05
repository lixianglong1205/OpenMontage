# Ink Theater 示例

## `mocap-figure/` — 标准可运行示例

一个自包含的 HyperFrames 合成：铅笔线条**自行绘制成
简笔画小人**，随后通过 `InkPuppet.choreograph(...)` 使用**真实 CMU 动作捕捉**（零手工调参）完成行走 / 奔跑 / 跳舞 / 踢腿 / 坐下 / 挥手等动作。

它自带所需全部文件（`ink-theater.js`、`ink-puppet.js`、`clips.js`、
`assets/patrickhand.ttf`），可直接 lint 与渲染：

```bash
npx hyperframes lint ink-theater/examples/mocap-figure
```

> 请将 linter 指向**合成目录**（内含 `index.html` 的目录），
> 而非 `examples/` 本身 — linter 会查找 `index.html`，
> 而 `examples/` 根目录下没有该文件。

若要在自己的项目中复用该引擎，将 `ink-theater.js`（角色需一并复制 `ink-puppet.js`
与 `mocap/clips.js`，手写体需 `assets/patrickhand.ttf`）
复制到项目根目录 — 详见 `../README.md`。
