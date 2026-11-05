# 定稿 / 修复（子 agent）

快照视觉 QA + 一次就地修复 + 渲染。仅在 Step 6 的 `lint`/`inspect` 报告问题时调度，或用于执行最终渲染。

## 调度上下文

`SKILL_DIR` / `PROJECT_DIR` / `Render quality: draft|standard|high` / 快照时间点 / lint+inspect 输出尾部（如有）。

## 流程

1. **快照** — `npx hyperframes inspect . --at <beat times>`；目视检查：溢出 / 画外、文字碰撞、空帧、错误内容、动效难以辨认。
2. **一次就地修复** — 用 `Edit` 修改 `compositions/index.html` 以修复可见问题。**切勿修改固定的 `data-duration`**（时序在上游已设定；修改会破坏装配）。重新运行 `lint`/`inspect`。
3. **渲染** — `(cd "$PROJECT_DIR" && npx hyperframes render . --skill=motion-graphics -q <quality> -o ./renders/video.mp4)`（需要 alpha 叠加导出时加上 `--format webm`）。确认 mp4 存在且时长一致。

## 停止 / 升级

仅当镜头**根本性错误**（整段内容偏离、需要重新构图）时 — 回到 Step 3/4（重新设计 + 重新构建），不要靠编辑硬改。小问题永不升级。
