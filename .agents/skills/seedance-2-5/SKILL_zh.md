---
name: seedance-2-5
description: |
  通过 fal.ai、Volcengine Ark、Runway 或 ComfyUI Partner Nodes 使用字节跳动 Seedance 2.5 生成 4–30 秒电影感视频。适用于单次长生成、同步音频以及大规模多模态参考集（最多 30 张图片、10 段视频和 10 段音频）。并涵盖 2.5 提示词约定：章节顺序、多镜头「Hard cut」分解、跨切镜命名锁定（named locks）、资产与角色设定表方法、语音条件化以及迭代纪律。
---

# Seedance 2.5

Seedance 2.5 将 Seedance 2 系列扩展为 4–30 秒、480p/720p 的片段，并支持更大的多模态参考集。其为托管服务；OpenMontage 中无本地模型权重。

## 选择受支持的路由

| 路由 | 工具调用 | 说明 |
|-------|-----------|-------|
| fal.ai | `seedance_video`, `model_version: "2.5"` | T2V、I2V 及 reference-to-video |
| Volcengine Ark | `seedance_ark`, `model: "2.5"` | 官方模型 ID `doubao-seedance-2-5-260628`；成本估算需自定义 token 价格 |
| Runway | `runway_video`, `model: "seedance2_5"` | T2V、I2V、V2V；480p/720p |
| ComfyUI Partner Node | `comfyui_video`, `model_family: "seedance_2.5"` | 在 ComfyUI 图中运行，仍为托管且付费 |

当其当前公开 API schema 未列出 Seedance 2.5 时，不要臆造 Replicate、HeyGen 或 Higgsfield 的标识符。

> **分辨率说明。** 上述受支持路由仅提供 480p 与 720p。模型在厂商自有 Web 平台上可原生生成 1080p，该能力不属于 OpenMontage 路由。若厂商博客提到 1080p 或 4K，请先确认所指界面再写入流水线承诺。

## 参考上限

- 最多 30 张参考图片。
- 最多 10 段参考视频。
- 最多 10 段参考音频。
- 参考视频/音频的总时长须落在各提供商文档上限内；Runway 上限为 30 秒。
- Runway 视频转视频（V2V）时，源视频占用一个视频槽位。

参考输入因提供商而异。fal.ai 内部使用 `image_urls`、`video_urls` 与 `audio_urls`。Runway 使用 `references`、`referenceVideos` 与 `referenceAudio`。Ark 使用带角色的 typed content 条目。始终调用 OpenMontage 工具，勿手动拼装提供商 payload。

**50 个资产是刻意使用的上限，而非尽量堆满。** 面孔、道具与场景互相冲突的杂乱参考集，比更小、更精选的集合产出*更差*的一致性。规则：每个必须保持一致的元素只配一条参考——一张脸、一件产品、一处场景、一种风格。

---

## 提示词（Prompting）

先写镜头结构，再写主体、动作、机位、光线与音频。多镜头时，为每个节拍给出明确时间范围，对白用引号。在提示词中用稳定角色指名每条提供的资产。三十秒是上限而非目标：若场景只有一个有意义的动作，应使用更短的生成时长。

### 章节顺序

一段连续正文，拆成带标签的章节。跳过某一节通常不会整体劣化输出——它会在可预期的方式上破坏特定方面。

```
GLOBAL STYLE
  Genre, color grade, film stock or digital look, aspect ratio, shutter behavior,
  and anything that must not appear. Everything below must match this.

SCENE
  A one-line logline: what happens, where, in what mood.

CHARACTERS
  Face, hair, build, wardrobe. If a reference covers this, just name which
  reference is which character.

LOCATION
  The space and its props, separate from the people in it. A vague location is
  the single most common reason a multi-shot sequence drifts between cuts.

FIRST FRAME AND BLOCKING
  Exact starting positions: who is where, facing which direction, as the clip
  opens. Something fixed before any motion starts.

Shot 1: [shot type] [action in one or two sentences]. Hard cut.
Shot 2: [...]. Hard cut.
Shot 3: [...].
  Pacing is built here. State camera distance and framing per shot: vague
  transitions are the most common cause of a sequence collapsing.

OPTICS / CAMERA
  Focal length, camera height, handheld or dolly or crane, per shot.

PHYSICS
  Fabric, smoke, hair, liquid. Anything that would look wrong moving like a solid.

LIGHTING
  Where the light is motivated from, its direction, how it falls on faces.

AUDIO
  Ambience, specific effects, and what must not be heard. Default:
  "No music, no discernible dialogue", unless the scene needs otherwise.
```

有效提示词共有的形态：**顶部一条视觉规则，底部一条声音规则，中间按镜头拆开。** 有参考时可缩短 CHARACTERS；GLOBAL STYLE、镜头分解与 AUDIO 仍须保留。

### 类型、年代与光线比散文更有用

在厂商 Web 平台上这些多为 UI 选项；仅改类型就会在场景描述不变时改变节奏、对比与机位行为。**上述 API 路由不提供此类选择器**，因此在 OpenMontage 工具调用中须把意图写进 `GLOBAL STYLE` 与 `LIGHTING`——类型、年代、颗粒与色彩响应、光源及其角度、情绪基调。隐而不写，往往是镜头读成 noir 与 merely dark 的分野。

---

## 锁定（Locks）：跨切镜连续性

约束不应堆在末尾负向提示里。应放在**命名块**中，通常用肯定句说明什么保持不变。

| 锁定 | 解决的问题 |
|---|---|
| `FIRST FRAME AND SPATIAL BLOCKING` | 以画面 x/y 百分比表示站位，并写反打说明：机位横越后谁在哪一侧，避免左右互换 |
| `SCREEN DIRECTION` | 轴线。「海始终在画面右侧，沙丘线始终在左侧，永不反转」 |
| `LENS LOCK` | 每段一个焦距，以对角视场角表示：84° 广角、47° 标准、29° 人像、18° 长焦。并写「段内无镜头漂移」 |
| `SINGLE-LENS LOCK` | 全片单一焦距；景别变化来自摄影师移动。这才像纪录片 |
| `COUNT LOCK` | 「恰好四个，永不为五，无背景替身，镜中或反射不出现额外副本」 |
| `STILLNESS LOCK` | 不发生之事的清单：无人站起、无人拥抱、手不离开毯子 |
| `POSITIVE LOCKS` | 收尾块，用肯定句重申跨切镜仍成立的内容 |
| `IDENTITY / NO-IP LOCK` | 「完全原创、虚构的面孔。」无 logo、无可读文字、无可识别旋律 |

**状态单调性。** 最省成本的连续性技巧：状态只前进、不重置。湿意只增不减。饼干只变小——完整、被咬、两半、吃完——绝不复原。逐镜写出 progression，可避免模型在下一切把角色「洗干净」。

**每个动作一套语法。** 重复动作时，定义唯一执行方式并禁止其余，然后闭合列表：全片恰好五次挥剑，各带时间戳。慢动作同理——仅允许名单内时刻，别处禁止。

**事件轨道。** 把环境元素写成带时间戳的事件列表，而非笼统质感：每道浪的秒数与溅起高度（占画面百分比），间隔不规则。适用于海、风、雨、车流与人群。

**替换，而非仅禁止。** 若禁止某物，给出具体替代。「无 blood」弱；「切口发橙光、火星飞出、躯体化为灰烬」可执行。

---

## 资产（Assets）

成败在此，早于任何一次视频生成。

**角色设定表：三版底图，仅一版带脸。** 全身正面去掉面部、全身背面，以及带脸的 3/4 特写两版（微笑与中性）。全身底图去脸，是因为远景脸小且糊，模型会复制那种糊；若集中唯一的脸是清晰特写，模型会用那张。无微笑版则模型会臆造牙齿。

**一态一资产。** 变体拆成独立资产，勿只在提示里注明：干净夹克、湿透、沾血。拆分比争论便宜。

**十条规则。** 采纳资产前，在不同姿势与光线下生成十次。十次都必须可辨认。

**场景。** 不要生成正面静帧。生成空镜慢移视频，再从该素材推导房间其他侧面。静帧只得一面墙；慢移才得几何。

---

## 语音（Voice）

语音是**条件句，不是资产**。用口音、节奏与方式写一次，该角色每次开口都**一字不改**粘贴同一句。改写法会扩大采样范围并破坏声线稳定。

用音标式写法描述口型而非籍贯：`th going to f and v, dropped h, glottal t, -ing to -in'`。

音轨分开。切勿在同一参考片段里混人声与音乐。

---

## 模型做不到的事

| 失败点 | 变通 |
|---|---|
| **歌唱** | 预录音轨，切成 12 秒文件，每段标注 `THE TRACK THEY ARE PERFORMING`。标签说明音频在场景中的角色；`audio guide, for sync only` 技术上正确但几乎不可用 |
| **持续身体接触** | 打斗与两体持续接触。用手机拍参考作 motion reference；比二十次迭代便宜 |
| **多角色同镜** | 最难一类。单镜脸越多，每人越需参考材料，否则第三、四切后易漂成 generic face |

---

## 拼接与修正

超过 30 秒时，延长上一段或将其作为视频参考并描述后续——后一种方式还可在接缝处引入新角色或物体。避免厂商「长视频」选项：用一条短提示拼接多段生成，运行时可用细节不足。

单元素错误时，编辑而非整段重生成，说明改什么、什么不变：

```
Around the 2-second mark, change only [X] from [before] to [after].
Keep the characters, movement, camera, lighting, composition and timing unchanged.
```

修复帧也可作为起始图用于短替换段。注意张力：一部已公开的 110 分钟 Seedance 作品全程禁用起始帧，连续性靠资产而非上一镜末帧——末帧会带入自身漂移。把起始图修复当作点修，而非 continuity 方法。

---

## 成本与验证

所有受支持路由均付费。调用前确认确切提供商/模型，并检查结果的身份连续、切镜、口型同步、音频瑕疵与提示 adherence。ComfyUI Partner Nodes 使用预付 Comfy 积分，不是离线兜底。

控制成本的迭代纪律：

- **生成前先锁定资产。** 模型无记忆：每次都要重新描述一切。
- **每次迭代只改一处**，否则无法知道哪处改动有效。
- **10–15 次失败迭代后，简化或拆分场景，而非堆措辞。**
- 用该路由最低分辨率探索，只对有效结果重跑。
- 记录版本、改动与结论。
- **评判整段，勿评单帧。** 好静帧可能来自第 9 秒就崩的生成。
- 切镜落在运动上，勿落在静止 pose。

---

## 参考

[`reference/techniques.md`](reference/techniques.md) — 十种提示词原型、各自设置、组合为何有效、各引入何种技巧。从零写前先选最接近的原型。

## 出处（Provenance）

上文提示方法、锁定模式与资产规则提炼自 Higgsfield 团队 2026 年 8 月发布的内容——官方 Seedance 2.5 提示指南（十类、每类多代测试），以及一部 110 分钟 Seedance 长片的开源制作法。未逐字复现任一来源提示词；技巧以原创模板重述。底层工作归功于他们。

- <https://higgsfield.ai/blog/seedance-2-5-prompting-guide>
- <https://higgsfield.ai/original-series/cully-hill-boys/full-film>

本文件中的路由表、提供商字段名与成本说明为 OpenMontage 自有，优先于厂商博客关于 API 可用性的任何暗示。
