# 素材总监 — 纪录片蒙太奇流水线

## 何时使用

镜头清单已经就绪。接下来你要为每个槽位实际找到能填满它的片段。有两条路径：

### 标准路径：语料库 + CLIP 检索

1. **构建语料库** — 将场景总监的查询分发到所有可用的素材源（Pexels、Pixabay Video、Coverr、Mixkit、Archive.org、NARA、Library of Congress、Pond5 PD、Videvo、NASA、ESA、JAXA、NOAA、Dareful、Wikimedia、Unsplash），下载并嵌入候选片段。
2. **按槽位挑选** — 针对语料库用每个槽位描述运行 CLIP 检索，并为每个槽位选定一个胜出片段。

最适合：50+ 槽位的大型制作、自动化多样化、依赖 CLIP 相似度排序的无人值守槽位填充。

### 快速路径：直接搜索（推荐用于按幕制作）

1. **搜索并下载** — 使用 `direct_clip_search` 向所有可用提供商分发查询，每个查询下载 2–3 个片段。无需 CLIP 嵌入、语料库索引或 `.npy` 文件。
2. **检查缩略图** — 浏览提取出的缩略图（或使用子代理）对照槽位描述核对视觉匹配。
3. **将片段映射到槽位** — 根据目视检查，手动为每个槽位指定最佳片段。

最适合：幕与幕之间需要用户审阅的按幕制作、快速迭代、每幕槽位少于约 30 个的制作。

**跨幕复用：** 按幕制作时，为较早幕次下载的片段可填充后续幕次的槽位。让代理指向先前下载的目录，复用与新槽位描述匹配的片段。生产中这可节省 40–50% 的下载时间。

**并行工作流：** 在后台运行 `direct_clip_search` 的同时，生成 TTS 旁白、混音、字幕并搜索配乐。可大幅缩短总制作时间。

**回退：** 若快速路径对特定槽位视觉匹配不佳，仅对这些槽位使用 `corpus_builder` + `clip_search`。两种方法并不互斥。

输出为 `asset_manifest`，将每个槽位精确映射到恰好一个带来完整溯源信息的片段。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | 制品校验 |
| 前置制品 | `state.artifacts["scene_plan"]["scene_plan"]` | 槽位描述 + 查询 + preferred_sources |
| 前置制品 | `state.artifacts["idea"]["brief"]` | `era_mix`、`sources_allowed`、`music_plan` |
| 工具（快速路径） | `direct_clip_search` | 轻量多提供商搜索 + 下载 |
| 工具（标准路径） | `corpus_builder` | 用 CLIP 嵌入填充检索索引 |
| 工具（标准路径） | `clip_search` | 按槽位描述对片段排序 |
| 工具（可选） | `music_gen`、用户的 `music_library/` | 配乐床 |

## 心智模型

语料库**不是**素材库。它是代理按需构建的**搜索索引**。你不会在里面滚动浏览——你会查询它。

由此得出三条规则：

1. **先建后选。** 切勿对不包含该槽位查询族候选的语料库调用 `clip_search.rank_for_slot`。排序会返回垃圾结果，槽位会被浪费。
2. **增长，不替换。** 语料库只追加。若某槽位检索偏弱，增加查询并重建——不要从头再来。
3. **按槽位选，不按片段选。** 最终剪辑中每个片段只属于一个槽位。使用 `exclude_ids` 防止重复使用。

## 儿童 / 童话内容 — 素材源覆盖

当场景计划的 `metadata.tone` 或 `metadata.target_audience` 表明儿童向内容（童话、睡前故事、儿童解说、动画故事）时，**覆盖常规素材路由**，**仅从 Pixabay Video 获取**。

### 为何只用 Pixabay Video

Pixabay 社区库中有大量 AI 生成的奇幻动画——发光森林、幻境景观、魔法生物——由使用 Midjourney/Stable Diffusion 视频工作流的创作者上传。对儿童吸引力远优于实拍。没有其他免费源在该风格上具备可比深度。

### 获取规则

1. **锁定来源。** 对所有查询设置 `sources: ["pixabay_video"]`。不要将实拍提供商（Pexels、Dareful 等）与奇幻片段混用——风格冲突会破坏儿童的沉浸感。

2. **查询改写。** 场景总监应已按奇幻风格改写槽位描述。若需编写回退查询，在开头加上奇幻关键词：
   - 魔法关键词：`fairy tale`、`fantasy`、`enchanted`、`magical`、`glowing`、`dreamy`、`mystical`、`fairy`、`enchanted forest`、`magical world`
   - 示例：槽位需要「叶上毛毛虫」→ 查询 `"fairy tale caterpillar magical forest glowing"`

3. **视觉一致性检查。** 下载后确认**所有**片段共享 AI 生成奇幻美学。拒绝任何看起来像实拍的片段——即使 CLIP 分数更高。奇幻蒙太奇中混入一条实拍会破坏氛围。

4. **回退。** 若 Pixabay 对某槽位无奇幻结果，在尝试更宽泛词之前用不同奇幻关键词改写查询。每槽位最多两次改写。若仍为空，向用户标记该槽位——**不要**静默用实拍替代。

## 流程 — 快速路径（直接搜索）

在按幕制作且幕间需要用户审阅时使用，或总槽位数低于约 30 时使用。

### F1. 在后台运行 `direct_clip_search`

在并行处理旁白/音频/字幕时启动搜索：

```python
direct_clip_search.execute({
    "output_dir": "projects/<name>/assets/video/raw_act2",
    "queries": [
        {"query": "cesium atomic clock laboratory", "slot_id": "slot_01"},
        {"query": "laser beam laboratory optics",   "slot_id": "slot_02"},
        {"query": "satellite dish night sky",        "slot_id": "slot_03"},
        # ... one per slot
    ],
    "sources": ["pexels", "pixabay_video", "coverr", "mixkit", "archive_org"],  # or omit for all available
    "clips_per_query": 3,
    "filters": {
        "min_duration": 3,
        "max_duration": 40,
        "orientation": "landscape",
        "min_width": 1280,
    },
})
```

**关键参数：**
- `clips_per_query=3` 是较优平衡点。选择足够，下载也快。
- 省略 `sources` 可自动搜索所有可用提供商。
- 设置 `skip_existing=true`（默认）以避免重试时重复下载。

### F2. 检查缩略图

浏览 `<output_dir>/thumbnails/` 核对每个片段。必要时用子代理读取缩略图图像做视觉确认。

对每个槽位，从已下载集合中挑选最匹配的片段。

### F3. 跨幕复用

制作第 2–5 幕时，在下载新片段前先检查较早幕次的片段。各幕之间存在许多主题重叠：

- 实验室画面（显微镜、激光、科学家）
- 科技镜头（服务器、卫星、电路）
- 自然/抽象画面（山脉、太空、延时）

让代理指向先前幕次目录，在运行新搜索前将已有片段映射到新槽位。

### F4. 用定向搜索填补缺口

若初始搜索后特定槽位仍无良好匹配：
1. 改写查询（更具体的名词、不同词汇）。
2. 仅对这些查询运行 `direct_clip_search`。
3. 若仍无匹配，**仅对这些槽位**回退到 `corpus_builder` + `clip_search`。

### F5. 记录素材清单

格式与标准路径相同（见下文第 9 步）。`source_tool` 字段应为 `"direct_clip_search"` 而非 `"corpus_builder"`。

---

## 流程 — 标准路径（语料库 + CLIP 检索）

用于大型制作（50+ 槽位）、需要基于 CLIP 的自动排序，或快速路径匹配不佳时使用。

### 1. 确定语料库目录

决定语料库存放位置。约定：

```
projects/<project-name>/corpus/
```

同一 `corpus_dir` 传给每次 `corpus_builder` 与 `clip_search` 调用。语料库可在重跑间复用——若场景总监后续增加槽位，可在同一语料库上扩展而非从零重建。

### 2. 将查询分发到 `corpus_builder`

读取 `scene_plan.metadata.slots[]`。收集每个槽位的全部 `queries[]` 数组。去重。按 `preferred_sources` 分组。

对每个来源集合调用一次 `corpus_builder.execute(...)`：

```python
# Example shape. The agent constructs this from the shot list.
corpus_builder.execute({
    "corpus_dir": "projects/<name>/corpus",
    "queries": [
        {"query": "raindrop on asphalt slow motion", "kind": "video", "per_source": 8},
        {"query": "wet city street night neon",       "kind": "video", "per_source": 8},
        {"query": "taxi heavy rain yellow",           "kind": "video", "per_source": 6},
        # ... one entry per unique slot query
    ],
    "sources": ["pexels", "archive_org", "wikimedia"],   # from preferred_sources union
    "filters": {
        "min_duration": 3,
        "max_duration": 40,
        "orientation": "landscape",
        "min_width": 1280,
    },
    "max_new_clips": 150,          # enlarge the search space
    "thumbs_per_video": 5,
})
```

**分发规则：**

- 若 brief 固定某来源且 `corpus_builder.source_provider_menu` 显示该源不可用，**停止**并上报。不要静默降级到剩余来源。
- 语料库预算约为槽位数的 8–12 倍。15 槽位蒙太奇约需 ~150 个候选，检索才有真实选择。
- 每查询 `per_source` 4–8 通常足够。推到 20+ 多半只是增加噪声。
- 若 `era_mix = "vintage"`，单独跑一批限制为 `["archive_org"]` 且查询符合年代的 fan-out。Prelinger 搜索慢——不要与现代 Pexels 批次交错。
- 若任槽位 `preferred_sources` 含 `nasa`，跑**一次**小型仅 `nasa` 批次。NASA 慢且结果偏 niche。
- `unsplash` 仅图片。作辅助源，不要作为以动效为主的纪录片剪辑的主干。

### 3. 检索前检查语料库

在槽位挑选上消耗 token 之前，用 `operation=stats` 调用 `clip_search`：

```python
clip_search.execute({
    "operation": "stats",
    "corpus_dir": "projects/<name>/corpus",
})
```

查看 `rows`、`per_source`、`per_kind`、`mean_motion_score`。检查三种失败模式：

- `rows < 50` — 语料库过小。扩展它。
- `per_source` 严重倾斜（如 98% pexels、2% archive_org）且 brief 为 vintage — 跑定向 archive_org fan-out。
- `mean_motion_score < 1.0` — 语料库充满静态片段，成片会像幻灯片。用不同查询重跑，或在 rank 时应用 `motion_min`。

### 4. 按槽位对候选排序

对 `scene_plan.metadata.slots[]` 中每个槽位，用 `operation=rank_for_slot` 调用 `clip_search`：

```python
clip_search.execute({
    "operation": "rank_for_slot",
    "corpus_dir": "projects/<name>/corpus",
    "query_text": slot["description"],      # NOT slot["queries"] — the description is richer
    "k": 30 if slot.get("hero") else 12,
    "tag_weight": 0.3,
    "motion_min": 1.5,
    "kind": "video",
    "exclude_ids": already_picked_ids,      # global accumulator
})
```

要点：

- 使用槽位 **description**，不是 queries。description 是场景总监写的丰富名词+形容词串。CLIP 对其排序优于短搜索短语。
- `tag_weight=0.3` 混合视觉嵌入（70%）与来源标签嵌入（30%）。Pexels URL 标签强且视觉通道噪声大时提到 0.5。Prelinger 标签为长 prose 时降到 0.15。
- 始终传入已锁定到槽位的每个片段的 `exclude_ids`，避免同一把钥匙开门片段赢得两个槽位。

### 5. 凭判断挑选，不单看分数

第一名不总是正确选择。看前 3–5 名并逐项判断：

- **年代契合。** 关于「家」的 elegiac 列表蒙太奇里，2022 年 4K Pexels 镜头合适吗？也许。也许不。
- **动效契合。** 场景总监的 tone 表告诉你 hold 多长。若 clip 目标 hold 4.0s 而片段仅 2s 且快摇，撑不住。
- **构图延续。** 该片段能否与相邻槽位已选片段并置？尚不确定——但若 slot_02 是雨中宽景屋顶，slot_03 第一名也是宽景雨中屋顶，选 #2。
- **情绪基调。** CLIP 会把「夜间空城人行道」轻易匹配到明亮霓虹 Vegas 切镜。对 elegiac brief，霓虹镜头是**错的**。0.42 分不能盖过 tone。

**可接受分数经验法则（CLIP ViT-B/32 cosine）：**

- `>= 0.30` — 强匹配，通常可用。
- `0.22-0.30` — 尚可，需人工判断。
- `< 0.22` — 语料库没有你需要的。扩展它，不要硬选。

### 6. 检索偏弱时扩展语料库

若某槽位 top 分低于 0.22，**不要**在差集中选最好的。应：

1. 改写槽位 queries——可能太抽象，或词汇不符合年代。
2. 仅对该槽位用新 queries 再跑 `corpus_builder.execute(...)`。builder 跳过索引中已有片段，成本低。
3. 重新 rank。

每槽位两次扩展足够。若三次仍找不到 >0.22，告诉 idea director 该槽位无法从开放语料库拍摄，建议删槽或让用户提供素材。

### 7. 多样化相邻选择

每个槽位有一个候选后，你得到按时间线顺序的 clip_id 列表。视觉上冗余的相邻镜头会毁掉剪辑。对列表运行 `clip_search.diversify`：

```python
clip_search.execute({
    "operation": "diversify",
    "corpus_dir": "projects/<name>/corpus",
    "candidate_ids": picked_ids_in_timeline_order,
    "n": len(picked_ids_in_timeline_order),
    "diversity": 0.5,
})
```

若 `diversify` 丢弃某片段，说明两个选择视觉上相同。对被丢弃槽位用 `exclude_ids` 包含幸存 twin 重新 rank。

### 8. 处理音乐计划

读取 `brief.music_plan`。严格执行 idea director 记录的计划——**不要**在此发明新来源：

- **`source=library`**：确认 `music_plan.path` 文件存在。在素材清单中记为 `type=music`、`subtype=library`。
- **`source=user`**：同上，`subtype=provided`。
- **`source=generated`**：用 brief 中的 seed prompt 调用指定音乐工具。先 sample，确认 mood 后再 batch。记录 provider 与成本。
- **`source=none`**：不要生成静音。不要因为剪辑感觉薄就换轨。用户批准「无音乐」就无音乐运行。

**切勿在此阶段切换音乐来源。** 违反 Decision Communication Contract——改音乐模式是重大制作变更，需在提案阶段获用户批准。

### 9. 记录素材清单

按 canonical schema 为每个槽位输出一条 asset。纪录片蒙太奇专用字段在 `metadata`：

```json
{
  "version": "1.0",
  "assets": [
    {
      "id": "asset_slot_01",
      "type": "video",
      "path": "projects/<name>/corpus/clips/pexels_12345/video.mp4",
      "source_tool": "corpus_builder",
      "scene_id": "slot_01",
      "duration_seconds": 7.2,
      "resolution": "1920x1080",
      "format": "mp4",
      "provider": "pexels",
      "license": "Pexels License (free, no attribution required)",
      "original_url": "https://www.pexels.com/video/12345",
      "subtype": "stock",
      "generation_summary": "Retrieved via CLIP rank for slot 'raindrop on asphalt slow motion...'. Score 0.38."
    },
    {
      "id": "asset_music_bed",
      "type": "music",
      "path": "music_library/dawn_04.mp3",
      "source_tool": "music_library",
      "scene_id": "global",
      "subtype": "library",
      "license": "user-provided"
    }
  ],
  "metadata": {
    "pipeline": "documentary-montage",
    "corpus_dir": "projects/<name>/corpus",
    "corpus_stats": { "rows": 157, "per_source": {"pexels": 98, "archive_org": 52, "nasa": 7} },
    "rejected_picks": [
      {
        "slot_id": "slot_03",
        "clip_id": "pexels_99921",
        "score": 0.41,
        "reason": "wrong era — 2022 4K kitchen, brief is vintage"
      }
    ]
  }
}
```

`rejected_picks` 日志很重要。edit director 在挑选感觉不对时需要 #2 选项时会读它。

### 10. 质量门

- 场景计划中每个槽位恰好映射一条 asset。
- 每个选中片段在 rejected-picks 日志中 `score >= 0.22`（或记录「user-approved override」说明）。
- 无 clip_id 作为两个槽位的主选。
- `diversify` 对最终列表干净通过（无丢弃，或所有丢弃已重填）。
- `corpus_stats` 显示 rows 至少为槽位数的 8 倍。
- 存在音乐 asset **或** `music_plan.source = "none"` 且有明确确认。
- vintage brief 下，至少 60% 挑选来自 `archive_org`。
- 所有文件路径可解析。

## 常见陷阱

- **对空语料库运行 `clip_search.rank_for_slot`。** 会得到空 `results` 或晦涩 shape 错误。构建后、排序前务必先 `stats`。
- **只看分数挑选。** 分数是判断的输入，不是判断本身。充满 top 分 Pexels HD 阳光的 elegiac 作品无论分数多高都会感觉不对。
- **忘记 `exclude_ids`。** 没有它，同一段精彩片段赢得每个槽位，蒙太奇变成一张图的幻灯片。
- **静默替换音乐。** 用户说「none」，代理因「剪辑感觉薄」仍生成。这是重大变更，需批准——见 `skills/pipelines/documentary-montage/executive-producer.md` 跨阶段规则。
- **无界扩展语料库。** 弱槽位最多两次扩展。再往后，开放语料库里可能没有该素材，槽位需要改。
- **用槽位 queries 作 rank 文本。** queries 是给 stock API 的搜索短语；descriptions 是给 CLIP 的语义文本。不同。用 descriptions rank。
- **丢失溯源。** 每个片段在 manifest 中必须带 `provider`、`original_url`、`license`。这是任何下游发布步骤的非协商项。

## 检索配方

几种常见检索动作：

### 「找 N 个与我爱的这条片段相似的变体」

```python
clip_search.execute({
    "operation": "find_similar_set",
    "corpus_dir": "projects/<name>/corpus",
    "seed_clip_id": "pexels_12345",
    "n": 5,
    "diversity": 0.4,
    "candidate_pool": 40,
})
```

用于槽位想要「再来五条同 register 镜头」——例如同一调性下门口目录。

### 「我有 20 个候选，裁成 8 个不冗余的挑选」

```python
clip_search.execute({
    "operation": "diversify",
    "corpus_dir": "projects/<name>/corpus",
    "candidate_ids": [...],
    "n": 8,
    "diversity": 0.5,
})
```

### 「查一条片段的完整元数据」

```python
clip_search.execute({
    "operation": "get",
    "corpus_dir": "projects/<name>/corpus",
    "clip_id": "archive_org_Prelinger_HomeMovies_0042",
})
```

edit director 在锁定剪辑前想确认 provider/URL 时使用。

---

## 关卡提醒（绑定）

本阶段以人工批准为门（`human_approval_default: true`）。审阅通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染制品），并**结束本轮**。不要在同一回复中启动下一阶段。
批准按门进行——较早的「继续」不覆盖本门。
