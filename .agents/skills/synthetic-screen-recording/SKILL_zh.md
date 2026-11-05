---
name: synthetic-screen-recording
description: 面向 Remotion `TerminalScene` 的合成式终端风格录屏指南。
license: MIT
---

# 合成式屏幕录制（Remotion TerminalScene）

**本技能要回答的决策：** 当用户想要一段看起来像屏幕录制的终端、CLI 工具或编码工作流演示时——应该 **录制真实桌面**（通过 `screen_recorder`、Windows-MCP、Cap 或 Playwright 进行 OS 级录屏），还是在 Remotion 里用 `TerminalScene` 组件 **合成**？

> **启发式规则：** 若智能体能够预先编写确切的命令/输出序列，则采用合成。仅在真实行为不可预测、需要真实应用 UI，或用户明确要求真实录屏时，才进行实况捕获。

## 为何存在本技能

OpenMontage 展示片 v3 曾尝试用 Windows-MCP + `screen_recorder` 驱动 Git-Bash 窗口完成安装 walkthrough，却在窗口定位、焦点竞态和任务栏隐私顾虑上卡住。我们转向 **纯 Remotion 渲染**——名为 `TerminalScene` 的 React 组件绘制假终端并逐字输入命令。成片在视觉上与真实录屏难以区分（同样的红绿灯窗口 chrome、闪烁光标、滚动输出），但具有确定性、隐私安全、1080p 像素级精确，且节奏可按帧控制。

该组件及模式即本技能所要暴露的能力。

## 何时使用合成（TerminalScene）

**适合合成，当：**
- 演示是 **终端 / CLI / 编码会话**，且命令与输出可预测
- 用户想要 polished 教程感（清晰排版、浮动 pill、光标闪烁）
- 安装 walkthrough、设置演示、API key 配置、`make` 目标、`git clone` 流程
- 需要与旁白 tight sync——每条命令必须落在特定节拍上
- 希望结果可复现（重渲染得到相同像素）
- 用户真实桌面有可见的私人应用/窗口，否则需要裁剪

**不适合合成，应录真实屏幕，当：**
- 演示是 **无法伪造的真实应用 UI**（Figma、Photoshop、带 live state 的 Web 应用、浏览器流程）
- 用户明确要求录制 *其* 真实屏幕
- 行为依赖无法脚本的时序（流式 LLM 输出、真实网络延迟）
- 存在仅 live 环境才出现的视觉细节（光标效果、插件弹窗等）

**浏览器演示** → 使用 `playwright-recording` 技能，而非本技能。
**真实桌面** → 使用 `screen_recorder` 工具或经 `cap_recorder` 的 Cap。

## 组件 — `TerminalScene`

位置：`remotion-composer/src/components/TerminalScene.tsx`
导出：`remotion-composer/src/components/index.ts`
分发接线：`remotion-composer/src/Explainer.tsx`（`if (cut.type === "terminal_scene")`）

**Props：**
```ts
interface TerminalSceneProps {
  title?: string;           // shown in the window title bar
  steps: TerminalStep[];    // the timeline
  prompt?: string;          // "$", ">", etc.
  accentColor?: string;     // pill + prompt glow
  backgroundColor?: string;
}
```

**步骤类型：**
```ts
{ kind: "cmd",   text: string, typeSpeed?: number, holdSeconds?: number }
{ kind: "out",   text: string, holdSeconds?: number }
{ kind: "pause", seconds: number }
{ kind: "pill",  text: string, color?: string, durationSeconds?: number }
```

- `cmd` — 打印 prompt，逐字输入文本（`typeSpeed` 为每字符秒数，默认 0.035），随后保持 `holdSeconds`（默认 0.3）
- `out` — 一行程序输出，即时出现并短 fade-in
- `pause` — 空档。终端保持上一可见状态。**用此与旁白同步。**
- `pill` — 非阻塞浮动徽章（右上）。spring 进入、保持、spring 退出。**不推进光标**——下一步并行执行。

## 编写模式

通过向 `build_composition.py`（或等价的 props 构建器）添加 cut 来编写新场景：

```python
install_steps = [
    {"kind": "pause", "seconds": 7.0},                 # wait for intro narration
    {"kind": "cmd", "text": "git clone https://github.com/calesthio/OpenMontage.git",
     "typeSpeed": 0.045, "holdSeconds": 0.3},
    {"kind": "out", "text": "Cloning into 'OpenMontage'..."},
    {"kind": "out", "text": "remote: Enumerating objects: 2847, done."},
    {"kind": "pill", "text": "repo cloned", "color": "#34D399", "durationSeconds": 2.6},
    {"kind": "pause", "seconds": 3.8},                 # bridge to next narration cue
    # ...
]

cuts.append({
    "id": "install-terminal",
    "type": "terminal_scene",
    "terminalTitle": "bash — OpenMontage setup",
    "prompt": "$",
    "accentColor": "#22D3EE",
    "steps": install_steps,
    "in_seconds": 50.0,
    "out_seconds": 110.0,
})
```

## 铁律：与旁白同速，绝不要超前

**头号失败模式：** 步骤连续播放，在前 40% 场景时长内烧完所有内容，剩余 60% 终端冻结。v3 首轮即因此翻车——能力菜单在 t=80s 渲染，旁白直到 t=92s 才念到。

**应这样做：**

1. **掌握旁白 cue**——对每个场景，写下各旁白片段开始的精确视频时间。
2. **以 pause 开场**，在任意命令开始输入前，先等到第一个旁白 cue。
3. **让每条命令与其旁白句同时落地**——旁白念到该行时 `cmd` 才开始打字，不能更早。
4. **在命令组之间插入 pause**，桥接到下一个旁白 cue。
5. **结尾留足 hold**——pause 要足够长，旁白结束后最终状态仍可读。

**渲染前先 sanity-check 步骤**——Remotion 每一分钟渲染都很宝贵。汇总步骤时长并验证等于场景时长：

```python
import math
def trace(steps, scene_start, fps=30):
    t = 0.0
    for s in steps:
        k = s["kind"]
        if k == "cmd":
            tf = math.ceil(len(s["text"]) * s.get("typeSpeed", 0.035) * fps)
            t += tf / fps + s.get("holdSeconds", 0.3)
        elif k == "out":
            t += max(2, math.ceil(0.08 * fps)) / fps + s.get("holdSeconds", 0.15)
        elif k == "pause":
            t += s["seconds"]
        # "pill" is non-blocking — does NOT advance cursor
        print(f"  {t + scene_start:6.2f}s  {k}: {s.get('text', '')[:40]}")
trace(install_steps, 50)
```

看输出列。每个旁白 cue 的视频时间应紧挨其宣告的命令/输出。若命令比 cue 早或晚 10s，调整 pause。

可复用脚本见 `lib/verify_scene_pacing.py`。

## 设计规则（继承自 v3 retune）

- **开场 pause**——每个终端场景在任意输入前，至少 2s 空终端 + 闪烁光标，让观众识别窗口。
- **Pill 时机**——pill 应在屏幕上对应事件完成的瞬间触发（例如最后一条 `Receiving objects` 行后立即 `repo cloned`）。Pill 替代真实世界的 UI 通知。
- **输入完成后的命令 hold**——每个 `cmd` 的 `holdSeconds` ≥ 0.3，让观众在首行输出滚动前看清完整命令。
- **输出节奏**——输出行 `holdSeconds` 介于 0.4 与 1.0。过快像 bug，过慢显无聊。
- **自动滚动可用**——终端保留最近 18 行。不必担心屏外内容。
- **光标仅在最新命令行输入时闪烁，输入完成后约 0.2s tail。**

## `ProviderChip`（配套组件）

`.agents/skills/synthetic-screen-recording` 模式还包含 `ProviderChip`——按固定节奏轮播 provider 名称列表的旋转徽章 overlay。v3 展示片在「generated motion」段落中轮播全部 11 个 AI 视频生成 provider。

```python
overlays.append({
    "type": "provider_chip",
    "providers": ["Veo 3.1", "Seedance 2.0", "Kling 2.5", ...],
    "cycleSeconds": 2.5,
    "position": "bottom-right",
    "accentColor": "#22D3EE",
    "label": "generated with",
    "in_seconds": 195.0,
    "out_seconds": 222.5,
})
```

分发接线：`remotion-composer/src/Explainer.tsx` overlay 渲染器（`overlay.type === "provider_chip"`）。

## 添加新的合成 UI 组件

模式可泛化。当需要伪造其他 UI 表面（Claude Code 聊天气泡、Jira 工单视图、GitHub PR diff、Slack 消息、VS Code 状态栏）时：

1. 以 `TerminalScene.tsx` 为模板复制。
2. 为相关时间线原语定义 `steps` 接口。
3. 将 `frame` 对累积起止时间插值以渲染各步。
4. 在 `Explainer.tsx` 的 `SceneRenderer` 分发中接入新 `cut.type`。
5. 在 `Explainer.tsx` 的 `Cut` 接口及 `components/index.ts` 中加入该类型。
6. 在本技能中新增文档章节。
7. 在 `remotion-composer/SCENE_TYPES.md` 中更新新 cut 类型。

## 相关技能

- `.agents/skills/remotion` — 通用 Remotion 编写（hooks、springs、sequences）
- `.agents/skills/playwright-recording` — Web 应用的真实浏览器流程捕获
- `tools/capture/screen_recorder` — 基于 ffmpeg 的桌面捕获
- `tools/capture/cap_recorder` — Cap.so polished 桌面捕获
- `skills/pipelines/screen-demo/asset-director.md` — 为 screen-demo 项目选择合成或真实

## 来源

引入：OpenMontage showcase v3 渲染（2026-04-16）。原始动机：v3 设置 walkthrough 需要约 60 秒安装演示，每条命令对齐 Chirp 3 HD 旁白 cue，而 Windows-MCP 驱动的真实捕获在实践中过于不稳定。参考实现见 `projects/openmontage-showcase/build_composition.py`。
