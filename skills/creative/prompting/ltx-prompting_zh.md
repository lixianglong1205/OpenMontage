# LTX-2 — 提示词指南

> 来源：[LTX 官方提示词指南](https://docs.ltx.video/api-documentation/prompting-guide)
> 通用词汇见：`skills/creative/video-gen-prompting.md`

## LTX 专用六要素结构

LTX-2 采用简洁、聚焦的提示词结构：

1. **确立镜头** — 使用与题材匹配的摄影/镜头术语
2. **设定场景** — 光照、色板、质感、氛围
3. **描述动作** — 按时间顺序自然展开，从始至终
4. **定义角色** — 用可见特征（年龄、发型、衣着），避免抽象标签
5. **镜头运动** — 说明方式与时机；描述运动**之后**画面中出现的内容。（LTX 区分平移/旋转/镜头：`dolly` ≠ `zoom`，`pan` ≠ `truck`。选对类别 — 平移移动机位，旋转绕轴转动，纯镜头变化只改焦距或焦平面而不移动相机。）
6. **描述音频** — 环境声、音乐、对白或演唱

### 严格固定镜头规则

若写明「固定镜头（static camera）」，则整段**不得**有任何运动、对焦变化或变焦。LTX 会把 static 按字面理解 — 若在后续再写任何运动类动词，要么被忽略，要么出现镜头自相矛盾的 glitch。二选一：固定镜头，或**单一**具名运动。

## LTX 专用技巧

### 运动后描述
LTX 在你描述运动**结果**时更准确：
- 不要写：「镜头向左摇（Camera pans left）」
- 应写：「镜头向左摇，露出繁忙的市集广场（Camera pans left to reveal a bustling market square）」

### 音频提示（LTX-2 独有）
LTX-2 生成同步音频。使用具体描述：

| 类别 | 示例 |
|----------|---------|
| **环境声** | 「咖啡店嘈杂声」「风雨声」「森林鸟鸣」 |
| **嗓音风格** | 「活力播音腔」「浑厚有分量的嗓音」「孩童般好奇」 |
| **音量** | 「低语」「嘟囔」「喊叫」「尖叫」 |
| **音乐** | 「轻柔原声吉他」「逐渐增强的电子节拍」 |

对白用引号：`The narrator says: "Welcome to the future."`
指定语言/口音：`speaks in British English with a warm tone`

### 风格类别
LTX 将风格分为三大类：

**动画**：定格动画、2D 动画、3D 动画、黏土动画、手绘
**风格化**：漫画、赛博朋克、8-bit 像素、超现实、极简、绘画感
**电影感**：年代剧、黑色电影、奇幻、惊悚、纪录片、艺术电影

## 应避免的内容（LTX 专用）

| 避免 | 原因 |
|-------|--------|
| 内心情绪（「悲伤」「困惑」） | 改用视觉线索：泪水、佝偻姿态、紧皱眉头 |
| 可读文字与 Logo | 无法稳定渲染 |
| 复杂物理（爆炸、飞溅） | 易产生瑕疵；简单运动更稳妥 |
| 场景过载 | 角色/动作过多会降低一致性 |
| 矛盾的光照描述 | 选定一种布光并贯彻 |
| 一上来就写复杂提示 | 先简单，再逐层叠加 |
| 提示词超过约 80 词 | 超过后 LTX-2 质量下降。只保留最重要的 5–6 个要素。 |

## LTX 技术说明

- **时长**：单次生成约 5–8 秒
- **音频**：自动生成；在提示中描述希望听到的内容
- **约 30% 输出含瑕疵** — 换 seed 重跑
- **无法渲染可读文字** — 不要写招牌或标题
- **帧数须满足** `(n-1) % 8 == 0`：有效帧数为 25、49、73、97、121、161、193

## 示例

```
A wide establishing shot captures a misty morning harbor.
Weathered fishing boats bob gently, their paint peeling in
patches of red and blue. A grey-haired fisherman in a dark
wool peacoat steps onto the dock, carrying a heavy net over
one shoulder. He pauses, looks out at the fog bank, then
walks toward the nearest boat with steady, deliberate steps.
The camera tracks alongside him at waist height, slowly
pushing in as he reaches the boat and tosses the net aboard.
Soft overcast light with a warm break in the clouds near
the horizon. Ambient sound of water lapping, rope creaking,
and distant foghorn.
```
