---
description: 打开 Backlot 实时分镜板——在浏览器中展示流水线阶段、脚本、场景规划以及生成资产的实时看板，并在制作进行时同步更新。
argument-hint: [project-id (optional — defaults to the current/most recent project)]
---

为所选项目打开 Backlot 看板：

```bash
python -m backlot open $ARGUMENTS
```

- 无参数 → 打开库视图（全部项目）：`python -m backlot open`
- 该命令是幂等的：若 Backlot 服务未运行会先启动，然后在浏览器中打开该项目的看板。
- 若命令失败，报告失败并继续处理用户的其他请求——看板只是观察者，永不应成为阻塞项。
- 看板上的所有内容均来自磁盘（`projects/<id>/` 下的 checkpoints、artifacts、assets、events）。切勿手动更新 UI；只要按 `skills/meta/checkpoint-protocol.md` 保持 checkpoints 与 artifacts 准确，看板也会保持准确。
