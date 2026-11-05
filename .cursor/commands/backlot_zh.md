# /backlot — 打开实时故事板

为指定项目打开 Backlot 看板（浏览器界面，实时展示流水线阶段、剧本、场景规划与已生成素材）：

```bash
python -m backlot open <project-id>
```

- 未指定项目 id → 打开库视图：`python -m backlot open`
- 幂等（Idempotent）：如需要会先启动 Backlot 服务器，然后在浏览器中打开该项目的看板。
- 若失败，报告并继续——看板是观察者，从不会阻塞流程。
- 看板从磁盘上的 `projects/<id>/` 推导全部状态；切勿手动更新 UI。请按 `skills/meta/checkpoint-protocol.md` 保持检查点与产物一致。
