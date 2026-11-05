# spatial-pan-stations — 空间平移 / 站点

**意图**：在一张超大画布上预先排布一串带标签的站点，再用单一虚拟摄影机依次穿越——重复的水平/对角平移，每次将下一站居中并揭示标注，最终在末站定格。

**适用角色**

- Hook（来自 hook-pan-timeline / #1 Hook_02）：沿细水平 `[timeline]` 等距排列的 `[markers]`，逐拍向左平移；每个标记弹出弹簧式 callout，末拍落在「当下」（「演进 / 里程碑一路走到我们」）。
- Problem（来自 problem-camera-pan-stations / #8 Problem_01）：由手绘引导线串联的痛点「站点」网状布局，对角平移一站接一站，终点是缠结的涂鸦结（「步骤太多且彼此脱节——一团乱麻」）。
- Product_Intro（来自 concept-demo-decode-pan）：两段镜头条带由**一次**横向平移衔接——镜头 1 定格静态短语，强调词 3D 翻页 DECODES（概念落地），摄影机带背景视差平移穿过条带进入镜头 2，光标驱动实时打字演示。该平移与 `cursor-ui-demo` 的焦点锁定跟踪打字配对使用。

**时长**：7–10s（Hook 8–10s、Problem ~7s、concept-demo ~7s 的并集）

**镜头结构**
单一超大平面画布，纯色 `[bg color]`；所有站点/标记预置在世界空间；`[accent color]` 文字 + 简单线型图标；一个虚拟 `.world` 摄影机在站点间 ease-in-out 平移。每站约停留 ~1.0s。

- 场景 1（0.0–~1.0s）：摄影机开场对准站点 1——`[label 1 / first step]` 居中。其上落下揭示（见变体）。随后摄影机开始 PAN 向站点 2，站点 1 滑出画外。
- 场景 2 → 场景 N-1（各 ~1.0s）：摄影机 PAN（ease-in-out）将下一站居中；到达时 `[label k]`（及可选 `[secondary label]`）按角色揭示规则 REVEAL。每站重复。
- 场景 N（末拍，~最后一拍）：最后一次平移落在终端站点；最终 `[callout / landing element]` 揭示并 **HOLD** 至结束。摄影机在 punchline 上静止。

- 变体 — Hook：站点为下三分之一细水平 `[timeline]` 上等距 `[markers]`；平移**仅向左**沿单轴（时间轴向左滚动）。每个 callout 为带边框 `[callout box]` + 向下三角（偏移投影），SPRING-POP 弹起（scale 0→100%，弹性过冲，transform-origin 在三角尖端），文案 `[label k]`；`[secondary label, e.g. year]` 淡入并 RISE 至其上方。部分中间标记仅靠平移揭示为纯静态文字（无框）。末场景落在 `[present-day label]`，弹簧弹出后 hold。
- 变体 — Problem：站点散布于 2D 网状布局；平移为**对角**，由 `[accent color]` 手绘线**引导**——每站有一条粗糙 write-on 线/箭头指向下站，摄影机沿其移动（场景 1 还会在标题关键词外画 loop/circle）。每站 = 白色 `[line-icon]` 在上、`[label]` 在下，仅靠平移 plain 揭示（无弹簧框）。末场景：accent 线螺旋成场中密集的 chaotic SCRIBBLE KNOT；摄影机 static hold 在缠结上（视觉 punchline）。

**运动词汇**
在同一大型静态画布上重复的 ease-in-out 摄影机平移（Hook 为水平向左，Problem 为对角引导）；预置站点随平移滑过画面；三角尖端为原点的弹簧过冲 callout 弹出（Hook）；secondary label 升起并淡出（Hook）；标签/图标仅靠平移到达；粗糙手绘 write-on 引导线/箭头 + 关键词 loop/circle 标记（Problem）；终端 chaotic scribble knot 绘制（Problem）；最终站点/punchline 上 static hold。

**规则映射**

- 画布上的摄影机平移 / 穿越（主）→ `viewport-change`（单一 `.world` 包装 transform；PAN 模式）
- 将重复平拍拍序列化为停靠 → `multi-phase-camera`
- 平移目标使每站居中 → `coordinate-target-zoom`（用作 pan-to-target，无 zoom）
- 弹簧过冲 callout 弹出、三角尖端原点（Hook）→ `spring-pop-entrance`
- secondary label 升起淡出 + 各站 plain 标签/图标随平移揭示 → `discrete-text-sequence`
- 手绘引导线 / 箭头 / loop-circle 关键词标记 / 终端 scribble knot（Problem）→ `svg-path-draw`
- 站点线型图标（Problem）→ `svg-icon-enrichment`
- 最终站点 / punchline static hold →（无运动；持续定格，无需规则）

**摄影机修饰**：平移即摄影机。单一 `.world` 虚拟摄影机 transform，PAN 模式 — `viewport-change` — 由 `multi-phase-camera` 在停靠间序列化，每站经 `coordinate-target-zoom`（pan-to-target）瞄准。无纵深 push-in（区别于 cluster-push-in / dataviz-pushthrough 蓝图）。
