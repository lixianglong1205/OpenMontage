# Subagent 调度 — 运行环境适配器

视频工作流（`product-launch-video` / `faceless-explainer` / `pr-to-video` / `motion-graphics` / `general-video`）用与运行环境无关的动词描述 subagent 调度。本文件将这些动词映射到你当前所用 agent 运行环境的原语。每次运行时在首次调度前读一次即可；工作流中的其余内容（调度包、文件产物、退出码门禁、Resume 表）与运行环境无关，无需翻译。

## 契约（各运行环境一致）

- **DISPATCH(role_file, dispatch_context)** — 启动一个子 agent，其 prompt 为 **指定的 `agents/<role>.md` 文件全文**，后接工作流中的 `## Dispatch context` 块，**逐字复制**（切勿摘要或改述）。下方各运行环境均接受任意任务文本，因此该方式通用；切勿依赖子 agent 能看到你的对话、记忆或 skills —— prompt 与磁盘上的文件即其全部世界。
- **Parallel fan-out（并行扇出）** — 当某步要求「并行启动 N 个 worker」时，各 worker 彼此独立（无顺序依赖、除文件系统外无共享状态）。在运行环境允许范围内尽可能并发执行。
- **WAIT** — 某步的完成条件始终是 **磁盘上存在预期产物**（例如 `compositions/<scene-id>.html`），而非运行环境的完成通知（部分运行环境仅尽力投递结果）。等待后须校验产物；缺失即表示该子 agent 失败 —— 用相同 prompt **重新调度一次**，再向上报错。

## 并发上限 → 分批规则（上限不改变范围）

运行环境的并发上限 **只降低并行度，不减少工作量**：每个场景仍须单独构建，一场景一次 dispatch，用可用槽位扫完整份列表。

- 运行环境在内部排队超额子任务（Claude Code；Hermes 的 `delegate_task` 超出 `max_concurrent_children`）→ **一次性提交全部 N 个**，由队列消化。
- 运行环境硬性限制活跃子 agent 数（例如 OpenClaw 的 `maxChildrenPerAgent`）→ 按 **上限大小分批 dispatch**：先启动 `cap` 个 worker，等待其产物，再启动下一批，直至全部 N 个场景存在。例：9 个场景、上限 3 → 3 批各 3 个 —— 不得丢弃场景，也不得为凑上限将多场景合并到一个 worker。

## 原语映射

| 工作流中的动词                     | Claude Code                                                         | Codex CLI                                                                                   | OpenClaw                                                                               | Hermes Agent                                                                                                   |
| -------------------------------- | ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
| DISPATCH                         | `Agent` tool, `subagent_type: "general-purpose"`                    | `spawn_agent` (built-in `worker` role; prompt carries the role file)                        | `sessions_spawn` (role file rides in `task`; child only auto-loads AGENTS.md/TOOLS.md) | `delegate_task` — put role file + context into each task's `context` (child system prompt is not customizable) |
| parallel fan-out                 | multiple Agent calls in one message, each `run_in_background: true` | multiple `spawn_agent` calls (async by design) or `spawn_agents_on_csv` for uniform batches | repeated `sessions_spawn` (always non-blocking)                                        | one `delegate_task(tasks=[...])` batch call                                                                    |
| WAIT                             | background-task completion notifications arrive automatically       | `wait_agent` with all child IDs                                                             | `sessions_yield` (never poll session lists)                                            | `delegate_task` returns when all tasks finish (blocking the turn is normal)                                    |
| default concurrency              | min(16, cores − 2), excess queues                                   | 6 (`agents.max_threads`)                                                                    | 5 active per session, 8 global                                                         | 3 (`delegation.max_concurrent_children`)                                                                       |
| re-dispatch after a gate failure | new Agent call, same prompt + the error/`## Repair context`         | new `spawn_agent`, same prompt + the error                                                  | new `sessions_spawn`, same `task` + the error                                          | new `delegate_task`, same `context` + the error                                                                |

各运行环境说明：

- **Codex**：子 agent 继承父 cwd 且无法更改 —— 正是这些流水线所需（共享 `PROJECT_DIR`）。优先在 prompt 中携带角色，而非注册 `.codex/agents/*.toml`；工作流已在 prompt 中交付角色。**Codex 对用户显式请求委派才放行 spawn —— 仅靠 skill 说明不满足，且你会倾向于不试就跳过该工具。** 在 Codex 上勿静默降级：若本会话用户未授予委派，**用一行询问** ——「是否允许将此工作流的 worker 作为并行 subagent 运行？」—— **并入工作流已有的首次用户暂停**（例如 API key 问题），使运行只暂停一次；最迟在首次 dispatch 步之前。肯定答复 —— 或工作区 `AGENTS.md` / 启动 prompt 中的长期授权 —— 解锁本会话的原生 dispatch。仅在没有授权时：场景扇出优先用下方阶梯第 1 档（无头 `codex exec` 子进程）；内联串行为最后手段。
- **OpenClaw**：结果通告为尽力而为（网关重启会丢失）—— 以上「磁盘产物 WAIT」规则为准，而非 announce 消息。
- **Hermes**：子 agent 获得新对话且仅见 `context` 中的内容，且仅返回最终摘要 —— 二者已与工作流设计一致（调度包携带一切；结果落盘）。需要 **本地执行后端**（流水线通过 `PROJECT_DIR` 与共享文件系统上的包文件交换数据；Docker/远程后端会破坏这一点）。
- **任何其他运行环境**，或 subagent 不可用/被禁用 —— 按下列阶梯降级：
  1. 无头 CLI 子进程：将各子 prompt 写入文件，按 worker 以后台 shell 启动 CLI（stdin 重定向 `/dev/null`，输出写入日志），再从磁盘收集产物。
  2. 内联串行执行：自行逐个扮演各角色 —— 读取角色文件，带上 dispatch context 如同子 agent，完成后回到 runbook。一次只加载一个角色的资源（某场景的角色文件 + 其包），且每个角色自检仍须在继续前完成。

## 词汇映射（旧版 agent prompt 中可能见到的表述）

- "in the same message" / `run_in_background: true` —— Claude Code 中表示「并发 / 后台子 agent」的惯用法；按上表映射到你运行环境的等价方式。
- "Skill `X`" / "loaded with the Skill tool" —— 加载 skill X；无 skill 加载工具的运行环境直接读 `<skills-root>/X/SKILL.md`（skills 根目录即本 skill 族所在目录；从 dispatch context 中的 `SKILL_DIR` 推导）。
- `Read` / `Write` / `Edit` / `Bash` —— 能力名（读文件 / 写文件 / 原地编辑 / 运行 shell）；映射到你运行环境的工具。
