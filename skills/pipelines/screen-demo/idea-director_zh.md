# Idea Director - Screen Demo Pipeline

## 运行时选择（强制 — 列出所有可行运行时）

在创意阶段与制作模式一并锁定 `render_runtime`。可行运行时取决于模式：

| 制作模式 | 可行运行时 |
|-----------------|-----------------|
| `real_capture`（真实屏幕录制） | `remotion`（首选 — 将录制与叠加层混合），`ffmpeg`（纯拼接/裁剪） |
| `synthetic_terminal`（Remotion `TerminalScene`） | 仅 `remotion` |
| `synthetic_ui`（自定义 HTML UI 演示） | `remotion` 或 `hyperframes` — 真实二选一，两者都需呈现 |

按 AGENT_GUIDE.md →「Present Both Composition Runtimes (HARD RULE)」：当模式允许多种运行时且本机两者均可用（检查 `video_compose.get_info()["render_engines"]`）时，向用户呈现两者并附简要分析，推荐其一，等待批准。不得静默默认。当模式约束选择（例如 `synthetic_terminal` 仅 Remotion）时，明确告知用户该约束，而非静默锁定 remotion。在 `decision_log` 的 `render_runtime_selection` 中记录每项选择及所有曾考虑的选项。

## 何时使用

只要交付物是屏幕录制风格的演示，就使用本流水线。共有**两种制作模式** — 在 brief 中选一种：

| 模式 | 源素材 | 选用时机 |
|---|---|---|
| **`real_capture`** | 通过 `screen_recorder`、`cap_recorder` 或 `playwright-recording` 捕获的真实屏幕录制（MP4） | 真实应用 UI、实时行为、浏览器流程、IDE 插件、用户要求录自己的屏幕 |
| **`synthetic_terminal`** | 无 — 不捕获任何内容。你为 Remotion 编写 `terminal_scene` 片段 | CLI / 终端 / 安装流程 / make 目标 / git clone / API 密钥配置 — 一切可脚本化、每条命令及输出可预测的场景 |

**决策问题：** *「拍摄前能否预测每条命令及其输出？」* 能 → 合成。不能 → 真实捕获。

**在 `brief.metadata.production_mode` 中记录模式。** asset-director 读取该字段，在「捕获+叠加素材」与按旁白节奏的 `steps` 列表之间选择。

对于 `synthetic_terminal`，继续前还需阅读 `.agents/skills/synthetic-screen-recording/SKILL.md` — 其中包含避免早期 showcase 渲染问题的节奏规则（命令在约 40% 场景时间内播完，终端在剩余 60% 冻结）。

本阶段任务是将用户请求转化为清晰的流程化视频计划。主要交付物是符合 schema 的 `brief`，流水线特有细节存放在 `brief.metadata` 中。

## 操作原则

屏幕演示最佳实践一致强调：

- 流程优先于理论，
- 范围限定为单一工作流或单一结果，
- 旁白与可见动作对齐，
- 克制地规划注意力引导，
- 可读性优先于风格。

参考文档：
- `docs/screen-demo-best-practices.md`
- `skills/creative/screen-recording.md`

## 流程

### 1. 检查源素材

编写 brief 前使用可用分析工具：

- `frame_sampler` 获取代表性帧，并在可能的关键时刻附近密集采样
- `scene_detect` 检测窗口切换、页面变化与主要布局变化
- `transcriber` 判断录制是否含旁白、仅系统音或静音

识别：

- 展示的软件与界面，
- 正在教学的单一工作流，
- 关键交互：点击、输入、滚动、提交、结果，
- 明显需要缩放或高亮的时刻，
- 空档时间：安装、构建、加载、重复输入，
- `9:16` 是否在不过度损失含义的前提下可行。

### 2. 分类演示类型

选择一种主导原型：

- `tutorial`：分步完成任务
- `feature_showcase`：展示功能作用
- `troubleshooting`：复现并修复问题
- `walkthrough`：跨工具的多步流程讲解
- `comparison`：对比两种方法或结果

若素材混合多种原型，选应驱动节奏与包装的那一种。

### 3. 设定交付意图

屏幕演示应保持窄范围、以结果为导向：

- `30-60s`：快速技巧或功能揭示
- `60-120s`：聚焦的产品 walkthrough 或 bug 修复
- `120-300s`：分章教程

默认采用仍能清晰教会任务的最短时长。除非用户明确要求培训级素材且尽量少压缩，否则不要保留原始时长。

### 4. 选择可行的输出形态

按可读性规划平台，而非跟风：

- 密集桌面 UI 用 `youtube` 或 `linkedin`，
- 仅当活动区域能经受窄裁剪时用 `instagram` 或 `tiktok`，
- 界面有多面板或代码窗口时优先 `1:1` 或 `16:9`。

### 5. 构建 Brief

用 schema 字段写简洁创意契约，更丰富的制作细节存入 `metadata`。

推荐的 `metadata` 键：

- `source_path`
- `source_duration_seconds`
- `source_resolution`
- `has_voiceover`
- `software_shown`
- `demo_archetype`
- `critical_moments`
- `dead_time_segments`
- `recommended_aspect_ratios`
- `notes_for_scene_planner`

brief 应回答：

- 观众将学到什么，
- 面向谁，
- 视频应落在何种证明/结果上，
- 必须展示的动作有哪些，
- 哪些裁剪方向是安全的。

### 6. 质量门

checkpoint 前验证：

- 工作流对所选时长足够窄，
- 「顿悟」结果已明确识别，
- 目标平台与 UI 密度匹配，
- brief 点明实际软件而非模糊描述，
- metadata 为下游阶段提供足够的制作事实。

## 常见陷阱

- 默认把 7 分钟录制当作 7 分钟交付物。
- 用户要 Shorts 就为密集桌面捕获选 `9:16`。
- 用户实际需要任务完成却写概念型 brief。
- 未注明静音；若无旁白，下游阶段须立即知晓。

---

## 门控提醒（具有约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染 artifact），**结束本轮回复**。勿在同一回复中启动下一阶段。
批准按门控逐项进行 — 较早的「继续」不覆盖本门控。
