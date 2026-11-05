# /backlot — 打开实时故事板

为指定项目打开 Backlot 看板（浏览器 UI，实时展示 pipeline 阶段、剧本、场景规划与生成素材）：

```bash
python -m backlot open <project-id>
```

- 未指定项目 id → 打开库视图：`python -m backlot open`
- 幂等：如需要会先启动 Backlot 服务，再在浏览器中打开该项目看板。
- 若失败则报告并继续 — 看板是观察者，从不会阻塞流程。
- 看板从磁盘上的 `projects/<id>/` 推导全部状态；切勿手动更新 UI。按 `skills/meta/checkpoint-protocol.md` 保持 checkpoint 与产物一致。
