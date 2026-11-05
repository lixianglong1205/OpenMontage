# OpenMontage 的 B-Roll 规划

> 如何根据脚本规划 B-roll 需求、在素材库与生成素材之间做选择、
> 构建有效的搜索查询，以及评估素材质量。

## 何时使用

你在为视频规划视觉资产，需要补充镜头（B-roll）配合旁白、建立情境或增加画面变化时。
本技能说明何时选用素材库镜头与 AI 生成，以及如何从各自渠道获得好结果。

## 决策矩阵：素材库 vs. 生成

| 场景需求 | 优先素材库 | 优先生成 |
|------------|-------------|-----------------|
| 真实世界建立镜头（城市、办公室、自然） | **是** — 素材库擅长此类 | 仅当找不到合适素材时 |
| 真实情境中的人物 | **是** — 生成人物常显不自然 | 仅在使用高质量模型时 |
| 抽象概念可视化 | 否 | **是** — AI 可创造不存在的事物 |
| 自定义图表/信息图 | 否 | **是** — 使用 `diagram_gen` 或 `image_selector` |
| 品牌/风格化画面 | 否 | **是** — AI 可匹配你的 playbook 风格 |
| 历史/档案镜头 | **是** — 素材库有档案内容 | 否 |
| 特定技术设备 | **是** — 真实照片更可信 | 仅当设备不存在时 |
| 运动/动作片段（海浪、车流、云） | **是** — 素材视频非常适合 | AI 视频在追赶 |
| 隐喻性画面（成长、连接） | 两者皆可 | **是** — 创意控制更强 |

**经验法则：** 若场景需要看起来 _真实_，用素材库。若需要看起来 _贴合你的概念_，则生成。

## 从脚本提取 B-Roll 需求

逐段阅读脚本。对每一段问：

1. **旁白在讲什么？** — 主题即画面线索。
2. **是否有增强提示？** — 编剧可能已嵌入 `[B-ROLL: ...]` 提示。
3. **本节是否提到具体事物？** — 「数据中心里的服务器」→ 服务器素材。
4. **本节是否在讲抽象概念？** — 「算法权衡各因素」→ 生成图表。
5. **本节多长？** — 决定所需片段时长。

### 输出：B-Roll 简报

对每个识别出的需求，创建一条记录：

```
Scene: s3 (15s-22s)
Need: Establishing shot of a modern data center
Source: stock
Keywords: ["data center", "server room", "rack servers blue light"]
Duration: 4-6 seconds
Orientation: landscape
Mood: cool, technological, clean
Fallback: AI-generated image of server racks
```

## 构建有效的素材库搜索查询

### 查询构建规则

1. **具体但勿过细。** 「aerial city skyline sunset」有效。「aerial shot of downtown San Francisco financial district at 6:47pm golden hour」往往无结果。

2. **使用 2–4 个关键词。** 素材搜索基于关键词，非语义。词越多，结果越少。

3. **主体词放前面。** 用「ocean waves」，而非「beautiful calm serene ocean waves at dawn」。

4. **加入所需画面特质：**
   - 俯拍加「aerial」或「drone」
   - 细节加「close-up」或「macro」
   - 延时加「timelapse」
   - 慢动作加「slow motion」

5. **失败时试同义词。** 若「programmer coding」结果差，试「developer laptop」或「software engineer workspace」。

### 按场景类型的查询模板

每条查询都加上 **POV 关键词**。素材库（Pexels、Pixabay、Storyblocks、Artgrid）会明确索引 POV 术语 — drone、aerial、OTS（over-the-shoulder）、macro、top-down、dashcam、FPV、handheld、locked-off — 加上 POV 往往比细化主体更能找到合适匹配。CMU/Harvard CHAI 分类法将 POV 视为 Scene 的一等维度，原因相同：它决定你在搜哪一类库架。

| 场景类型 | 查询模板 | 含 POV 示例 |
|-----------|---------------|---------|
| 建立镜头 | `[place] [time of day] [POV]` | "tokyo skyline night drone" |
| 活动 | `[person] [action] [POV]` | "scientist microscope OTS" |
| 物体 | `[object] [style] [POV]` | "circuit board macro top-down" |
| 自然 | `[element] [quality] [POV]` | "ocean waves aerial drone" |
| 抽象运动 | `[movement] [style] [POV]` | "light trails timelapse locked-off" |
| 工作场所 | `[setting] [activity] [POV]` | "modern office meeting handheld" |

若场景描述未隐含 POV，向脚本/场景导演确认 — 不要默认「无 POV」。POV 错误（场景要 drone 却拿到 handheld）比调色错误更难补救。

## 评估素材库镜头质量

素材工具返回结果后，使用前评估：

### 图像标准
- **分辨率：** 满足目标（视频帧至少 1080p）
- **相关性：** 确实呈现场景所需（非仅关键词命中）
- **风格兼容：** 不与 playbook 视觉风格冲突
- **无水印：** Pexels/Pixabay 免授权，但仍需核实
- **构图：** 主体构图良好，无生硬裁切
- **POV 匹配：** 素材实际 POV（drone、OTS、macro、handheld、locked-off 等）是否符合场景？POV 错误 — 例如场景要 drone 却是 handheld — **比调色错误代价更高**。应拒绝并重新查询，而非靠裁切硬改。

### 视频标准（含全部图像标准，另加）
- **时长：** 至少满足场景需求（可裁短，不可延长）
- **运动：** 平滑，无突兀运镜（除非刻意如此）
- **帧率：** 匹配目标输出（标准 24/30fps）
- **音频：** 素材视频音频通常丢弃 — 不必纳入考量

### 评分启发式

每条结果打 1–5 分：
- **5：** 完美匹配，可直接使用
- **4：** 良好匹配，需轻微裁切或修剪
- **3：** 可接受，可通过调色匹配 playbook
- **2：** 勉强 — 先换关键词
- **1：** 错误 — 与场景完全不符

**阈值：** 使用 3 分及以上。低于 3 分则优化查询或改用生成。

## 失败升级

素材搜索失败（无结果或全部低于 3 分）时：

1. **换关键词重试** — 同义词、更宽术语或不同角度
2. **换另一家素材提供商** — Pexels 与 Pixabay 库不同
3. **改用 AI 生成** — 用 `flux_image` 或 `openai_image` 配合场景描述
4. **升级给用户** — 「我无法为 [场景] 找到合适素材。最佳选项：[展示结果]。或我可以生成图像。你更倾向哪种？」

仅当素材搜索与生成回退都可能产出次优结果时，才应询问用户。多数情况下，回退链可静默处理。

## 归属追踪

Pexels 与 Pixabay 均可商用且无需强制署名。
但最佳实践是在资产清单中记录来源：

```json
{
  "id": "broll-scene-3",
  "type": "image",
  "source_tool": "pexels_image",
  "provider": "pexels",
  "attribution": {
    "photographer": "Joey Farina",
    "source_url": "https://www.pexels.com/photo/...",
    "license": "Pexels License"
  }
}
```

工具响应中提供此类数据（`photographer`、`pexels_url` / `page_url`）。为透明起见，请写入资产清单。
