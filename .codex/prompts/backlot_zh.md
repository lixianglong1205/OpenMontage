# /backlot — 打开实时故事板

为指定项目打开 Backlot 看板（浏览器界面，实时展示流水线阶段、脚本、场景规划与已生成素材）：

```bash
python -m backlot open <project-id>
```

- 未指定项目 id → 打开库视图：`python -m backlot open`
- 幂等：如需要会先启动 Backlot 服务，再在浏览器中打开该项目的看板。
- 若失败，报告后继续 — 看板是观察者，从不会阻塞主流程。
- 看板上的全部状态均来自磁盘上的 `projects/<id>/`；切勿手动改 UI。检查点与产物须按 `skills/meta/checkpoint-protocol.md` 保持真实一致。
