# 场景导演 — 纪录片蒙太奇流水线

## 何时使用

简报已就绪。接下来要把一个主题性问题转成检索层能填上的具体 **SLOT（槽位）** 列表。每个槽位包含一条意图（例如「黄昏门口的一个剪影」）以及能在真实素材库中找到它的查询（Pexels / Archive.org / NASA / Wikimedia / Unsplash）。

这是整条流水线里最具创造性的阶段。检索效果完全取决于你写的槽位描述。

## 前提条件

| 层级 | 资源 | 用途 |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | 产物校验 |
| 前置产物 | `state.artifacts["idea"]["brief"]` | 主题问题、基调、时长、结构形态 |
| 参考 | `skills/pipelines/documentary-montage/executive-producer.md` | 跨阶段规则 |
| 工具 | 此阶段尚无 — 纯规划 | — |

## 心智模型

场景导演的工作**不是**「挑片段」，而是「把片段需要长什么样描述得足够直白，让 CLIP 能找到它们」。

像**外景勘景**一样思考，而不是像**图库管理员**。

- 图库管理员会说：*「城市雨景蒙太奇，15 条片段」*。
- 外景勘景会说：*「蓝调时刻，雨丝横刮过公交车窗，乘客面孔柔焦，红绿交通灯透过玻璃晕开」*。

第二种才是 CLIP 真正能排序匹配的。第一种只是 CLIP 会弱匹配、且匹配很泛的分类标签。

## 流程

### 1. 把结构形态换算成节拍数量

阅读简报中的 `duration_seconds` 与 `shape`，推导槽位数量。除非基调另有要求，否则使用下列默认值：

| 基调 | 平均停留 | 每 60 秒槽位数 |
|------|--------------|---------------|
| elegiac（哀歌式） | 4.0s | ~15 |
| reverent（ reverent 式） | 3.5s | ~17 |
| dreamlike（梦幻） | 3.0s | ~20 |
| wry（冷幽默） | 2.0s | ~30 |
| urgent（紧迫） | 1.2s | ~50 |

再按 `shape` 规划弧线：

- **list**：N 个均匀槽位，无起伏拐点。
- **before/after**：N/2 个「之前」槽位 + 1 个 pivot 槽位 + N/2 个「之后」槽位。
- **three-act**：铺垫（30%）→ 转折（40%）→ 释放（30%）。
- **single-image expansion**：1 张锚点图 + 围绕它的 N 个变体。

在写任何槽位之前，先把节拍数量写下来。

### 2. 把主题问题拆成具体节拍

从简报里那**一个**主题问题出发，用**感官语言**回答它。不要写主题 — 写**质感**。

**示例 — 「雨让你看见城市的什么？」**

差的拆解（抽象、不可搜）：

- 「建立城市情绪」
- 「被天气困住的感觉」
- 「雨的普遍性」

好的拆解（具体、可搜）：

- a single raindrop hitting dry asphalt in slow motion
- an umbrella opening in a doorway, a hand visible
- neon signs reflected upside-down in a puddle
- rain streaking across a bus window, passengers soft
- a taxi roof light pushing through heavy rain, long lens
- a storm drain swallowing leaves and water, overhead
- a street vendor pulling plastic over a produce cart
- steam rising off wet cobblestones under tungsten streetlight
- a child's rubber boot stamping into a puddle
- a lit apartment window seen through sheets of rain

以上每一条都是**一个镜头**。每一条都 CLIP 可排序。每一条也是**同一想法的不同角度**，这才让 list 形蒙太奇有分量。

### 3. 撰写槽位描述

每个槽位都有 `description` 字段。这是 CLIP 会嵌入并用来排序的文本。写得像一条好的图库标签串 — **名词和形容词**，不要意图动词，不要情绪词。

**模板：**

```
<subject>, <action/pose>, <environment>, <lighting>, <era/texture hint>
```

**好的：**

- `"a single raindrop hitting dry asphalt, close up, slow motion,
  warm streetlamp glow"`
- `"empty city sidewalk at night after rain, reflected neon,
  handheld, 1970s grain"`
- `"an umbrella opening in a doorway, hand visible, diffused
  afternoon light, shallow focus"`

**差的：**

- `"the feeling of arriving home"` — 情绪词，无主体
- `"a warm welcoming moment"` — 形容词堆砌，无画面
- `"someone going through a door in a symbolic way"` — 意图，无镜头

经验法则：若你想象不出一张具体照片，CLIP 也想象不出。

### 4. 每个槽位写 2–3 条查询

槽位描述供 CLIP 排序。`queries` 供 `corpus_builder` 填充候选池。两件事不同，写法也要不同。

为每个槽位提供 `queries` 数组，含 2–3 条：

1. **字面查询（Literal query）** — 最直接的图库搜索短语。Pexels 用户会打的那种。`"raindrop on asphalt slow motion"`。
2. **横向查询（Lateral query）** — 同一想法换角度或尺度。`"wet pavement close up"`。
3. **联想查询（Association query）**（可选，用于 hero 槽位）— 相邻概念，可能捞到字面查询漏掉的质感片段。`"first rain city street"`。

图库搜索引擎里短查询优于长查询。每条 2–5 个词。不要 filler。

### 5. 按槽位指定目标来源（时代感知）

阅读 `brief.era_mix`。按素材所在位置，为每个槽位指定一个或多个 `preferred_sources`：

| 来源 | 优势 | 适用场景 |
|--------|-----------|----------|
| `pexels` | 现代 HD 素材、干净镜头、人物、城市、自然 | 现代/任意时代的默认 |
| `pixabay_video` | 大型社区库、自然、人物、科技、生活方式 | Pexels 缺货时的补位；通用广度 |
| `coverr` | 策展电影感 B-roll、自然、城市、抽象背景 | 高质量 establishing、定调镜头、现代生活 |
| `mixkit` | Envato 策展 HD/4K、自然、商业、科技 | 高质感 B-roll、干净自然、无需署名 |
| `archive_org` | Prelinger 家庭电影、 mid-century 教育片、1940s–1980s 质感 |  vintage、wry、dreamlike、怀旧 |
| `nara` | 美国国家档案馆 — WWII、冷战、阿波罗、民权、总统 | 美国历史纪录片、军事、政府、太空竞赛 |
| `loc` | 美国国会图书馆 — 早期电影、新闻片、文化录音 | 1928 年前公有领域、美国史、民俗 |
| `pond5_pd` | Pond5 公有领域 — 一战/二战、早期电影、历史演讲 | 档案/vintage、Méliès、Edison、新闻片 |
| `videvo` | 9 万+ 免费片段、自然、航拍、城市、抽象、延时 | 大库补 Pexels、不同贡献者 |
| `nasa` | 轨道看地球、天文、飞行、尺度 imagery | reverent、尺度/太空/行星/飞行 |
| `esa` | 欧空局任务、Hubble/Webb、地球观测 | 欧洲太空内容，补 NASA 非美任务 |
| `jaxa` | 日本任务、Hayabusa、ISS Kibo、H-IIA | 亚洲太空、独特探索角度 |
| `noaa` | 深海 ROV、海洋生物、珊瑚、天气、飓风 | 海洋/水下、深海、天气现象 |
| `dareful` | 精选 4K 自然 — 山、林、瀑布、延时 | 高质量自然 B-roll、统一视觉、航拍 |
| `wikimedia` | Commons 照片与 CC 视频、公民/纪录/公共事件 | 公共空间、地标、抗议、城市质感、教育 |
| `unsplash` | 精修 editorial 静帧、生活方式、产品向摄影 | 动态素材薄时的现代静帧支持 |

若 `era_mix = "vintage"`，槽位偏向 `archive_org`，查询用语要符合时代（「commuter」「housewife」「suburb」，而非「influencer」「wfh」「coworking」）。

若 `era_mix = "any"`，按槽位混用来源 — 场景导演根据节拍含义决定每条用哪个源。

#### 儿童 / 童话内容

当简报的 `tone` 或 `target_audience` 表明儿童向（童话、睡前故事、儿童科普、动画故事）时，**视觉策略从实拍切换到 Pixabay 上的 AI 生成幻想片段**。

Pixabay 社区库有大量 AI 幻想动画（发光森林、 enchanted landscape、魔法生物），对儿童参与度远胜实拍。

**儿童内容的查询改写规则：**

| 槽位意图 | 实拍查询 | 幻想改写 |
|-------------|-------------------|-----------------|
| 花园 / 自然 | `garden flowers morning` | `enchanted fairy tale garden glowing magical` |
| 昆虫 / 生物 | `caterpillar leaf close up` | `fairy tale caterpillar magical forest glowing` |
| 变形 / 茧 | `chrysalis butterfly cocoon` | `magical chrysalis enchanted tree glowing` |
| 蝴蝶 / 飞行 | `butterfly flying sky` | `fantasy butterfly glowing magical wings` |
| 日落 /  landscape | `sunset landscape golden` | `enchanted fantasy landscape magical sunset` |
| 雨 / 天气 | `rain leaves gentle` | `fairy tale rain magical forest enchanted` |
| 夜空 / 星星 | `milky way timelapse` | `fantasy night sky magical stars enchanted` |
| 海洋 / 水 | `river water golden` | `magical underwater world fairy tale` |
| 山 / 航拍 | `mountain peaks golden` | `fantasy mountain castle fairy tale magical` |
| 森林 / 树 | `forest path morning` | `fairy tale mushroom forest glowing enchanted` |

**来源路由：** 所有槽位设 `preferred_sources: ["pixabay_video"]`。Pixabay 是唯一免费且 AI 幻想库够深的来源。不要混实拍与幻想 — 风格冲突会破坏儿童沉浸。

**用于检索 AI 幻想类内容的关键词：** `fairy tale`, `fantasy`, `enchanted`, `magical`, `glowing`, `dreamy`, `mystical`, `fairy`, `enchanted forest`, `magical world`。

### 6. 标记 Hero 槽位

每条蒙太奇有 2–3 个整片依赖的槽位：开场、转折、结尾。在槽位元数据里设 `hero: true`。

Hero 槽位获得：

- 更长停留（2–4s，而非基调默认），
- 资产阶段更大候选池（k=30 而非 k=10），
- 更多查询（3 条而非 2 条）。

### 7. 给资产阶段留余地

不要过度指定。资产导演的工作是用你的描述给候选排序。若描述和具体片段都钉死，你就抢了资产导演的活，也扼杀了它的创意空间。

规则：描述槽位要像电话里跟研究助理说 — 具体到会认出来，松到会给你惊喜。

### 8. 记录镜头列表

用 `scene_plan.schema.json` 产物，每个槽位一条 `scene`。本流水线把 documentary-montage 专用字段放在每条 scene 的 `metadata` 里。规范形态：

```json
{
  "version": "1.0",
  "scenes": [
    {
      "id": "slot_01",
      "type": "broll",
      "description": "a single raindrop hitting dry asphalt, close up, slow motion, warm streetlamp glow",
      "start_seconds": 0.0,
      "end_seconds": 3.5,
      "narrative_role": "establish_context",
      "hero_moment": true,
      "texture_keywords": ["wet", "slow motion", "streetlamp"],
      "required_assets": [
        { "type": "video", "description": "raindrop on asphalt", "source": "source" }
      ]
    }
  ],
  "metadata": {
    "pipeline": "documentary-montage",
    "shape": "list",
    "tone": "elegiac",
    "thematic_question": "What does rain show you about a city?",
    "slots": [
      {
        "id": "slot_01",
        "description": "a single raindrop hitting dry asphalt, close up, slow motion, warm streetlamp glow",
        "hero": true,
        "preferred_sources": ["pexels", "archive_org"],
        "queries": [
          "raindrop on asphalt slow motion",
          "wet pavement close up",
          "first rain city street"
        ],
        "min_duration": 3.0,
        "target_hold_seconds": 3.5,
        "era_hint": "any"
      }
    ]
  }
}
```

`scenes[]` 满足 schema。`metadata.slots[]` 才是资产导演实际读的 — 带检索字段（`queries`、`preferred_sources`、`hero`、`era_hint`），`scene_plan.schema.json` 本身不包含这些。

### 9. 质量门

- 槽位数量与步骤 1 的节拍数学一致。
- 每个槽位 `description` 符合名词+形容词模板 — 无情绪词、无意图动词。
- 每个槽位 2–3 条短查询（每条 ≤5 词）。
- 至少 2 个槽位标 `hero`。
- `target_hold_seconds` 之和落在 `brief.duration_seconds` 的 ±10% 内。
- 若 `era_mix = "vintage"`，至少 60% 槽位的 `preferred_sources` 含 `archive_org`。
- `metadata.thematic_question` 与简报逐字一致（防漂移自检）。

## 常见陷阱

- **把槽位描述写成意图而非画面。** 「进门前的犹豫瞬间」是剧本方向，不是 CLIP 查询。「女人静立在门廊，手靠近门把」才是。
- **分类式查询。** `"home"`、`"family"` 什么都匹配也什么都匹配不好。推到具体名词：door, mat, key, hall, shoe。
- **单查询槽位。** 第二条查询是廉价保险 — 第一条若返回垃圾，语料库仍有可用项。
- **忘记时长数学。** 90 秒 elegiac ≈ 15 个 ~6s 停留。若写了 40 槽，等于误做成 urgent。
- **vintage 简报却跳过 `era_hint`。** Pexels 会用 2020s HD 淹没语料，埋掉 Prelinger。
- **主题问题漂移。** 简报说「回家」，槽位列表却三条飞机，成片会变成旅行而非回家。起草后重读简报。

## 完整示例 — 「雨中一分钟」

- 时长：90s，elegiac → ~15 槽，各 ~6s。
- 形态：list（天气+城市目录）。
- 主题问题：「What does rain show you about a city?」

槽位草图（ abbreviated）：

1. **hero** single raindrop hitting dry asphalt, slow motion
2. umbrella opening in a doorway, diffused afternoon light
3. neon sign reflected upside-down in a puddle, handheld
4. rain streaking across a bus window, passengers soft focus
5. a taxi roof light pushing through heavy rain, long lens
6. storm drain swallowing leaves and water, overhead
7. a street vendor pulling plastic over a produce cart
8. wet cobblestone alley, steam rising, tungsten streetlamp
9. rooftop antennae against a grey sky, wide shot
10. a child's rubber boot stamping a puddle, low angle
11. **hero** a lit apartment window seen through sheets of rain
12. windshield wipers at night, colored city lights beyond
13. rain beading on a parked bicycle seat, macro
14. footprints filling with water on a tiled station floor
15. **hero** first patch of blue sky breaking through grey clouds

每个槽位具备：

- 名词+形容词模板的 `description`，
- 2–3 条短查询（例：槽位 5：`"taxi heavy rain", "yellow cab
  wet street night", "city traffic downpour"`），
- `preferred_sources`（槽 1–6 → pexels+archive_org，槽 8 → archive_org 时代质感，槽 11 → pexels），
- 槽 1、11、15 设 `hero: true`，
- `target_hold_seconds` 合计 ~90。

这是资产导演将对其跑检索的产物。

---

## 关卡提醒（具有约束力）

本阶段需人工批准（`human_approval_default: true`）。审查通过后：
以 `status="awaiting_human"` checkpoint，呈现摘要（Backlot 看板渲染产物），**结束本轮**。勿在同一回复里启动下一阶段。
批准按关卡计 — 更早的「继续」不覆盖本关。
