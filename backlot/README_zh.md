# Backlot — 动态分镜板

只读本地看板，实时展示一次制作流程：pipeline 各阶段亮起、剧本文稿页、场景规划以胶片条形式呈现，并随资产生成逐步填充，同时展示决策、花费与活动——数据均来自 pipeline 已写入 `projects/<id>/` 的内容。

```bash
python -m backlot open <project-id>   # start server if needed + open browser
python -m backlot open                # library view (all projects)
python -m backlot serve --port 4750   # run the server in the foreground
```

Backlot 绑定 `127.0.0.1`，在所选端口上仅接受发往 `127.0.0.1` 或 `localhost` 的 HTTP 请求。其他 `Host` 请求头会收到 HTTP 400，以防 DNS 重绑定（DNS rebinding）泄露本地项目数据。

## 如何保持实时

无需 agent 参与。对 `projects/` 的 `watchfiles` 监听器通过 SSE 推送变更通知；浏览器重新拉取看板状态。状态来源：

| 看板元素 | 磁盘来源 |
|---|---|
| 标识 / 轨道顺序 | `project.json` + `pipeline_defs/<type>.yaml` |
| 阶段状态、门禁、版本 | `checkpoint_<stage>.json` + `history/` |
| 剧本卡片 / 弹窗 | `artifacts/script.json` |
| 胶片条卡片 | `scene_plan × script × asset_manifest` 关联 |
| 生成中 shimmer、活动 | `events.jsonl`（由 `BaseTool` 埋点写入） |
| 成本计量 | checkpoint `cost_snapshot` |
| 渲染产物 | `renders/*.mp4`（及根目录 mp4 启发式规则） |

没有 checkpoint 的项目会优雅降级为「监听器当前所见」视图——媒体、快照、渲染产物。

**回放**：已完成的运行可在看板上从头到尾回放（▶ REPLAY RUN）——由 checkpoint 历史与事件时间戳重建。

无需真实制作即可体验：

```bash
python scripts/backlot_simulate_run.py          # live demo run (~1 min)
python -m backlot open backlot-demo-run
```

设计文档：`internal/design/LIVING_STORYBOARD.md`。
