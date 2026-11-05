# 旁白与脚本

如何为视频合成撰写旁白脚本。当合成包含画外音或 TTS 时阅读本文。

## 节奏

- **每秒 2.5 个词** 是自然的说话语速
- 15 秒 ≈ 37 词。30 秒 ≈ 75 词。60 秒 ≈ 150 词
- 留出停顿空间。句与句之间的沉默是特性，不是冷场
- 脚本应比视频**感觉更短**——画面留白很重要

## 语气

像人在说话，而不是宣传册：

- 使用缩略形式：`it's`、`you'll`、`that's`、`we've`
- 变化句长——短促有力的短语与较长流畅的句子交替
- 大声读一遍。若听起来像机器人在念，就重写
- 除非受众预期如此，否则避免行话

## 数字读音

写你希望配音实际说出的内容。TTS 会按字面朗读。

| 产品中的展示 | 脚本中应写成                |
| -------------- | --------------------------------- |
| 135+           | more than one hundred thirty five |
| $1.9T          | nearly two trillion dollars       |
| 99.999%        | ninety nine point nine percent    |
| 200M+          | over two hundred million          |
| 10x            | ten times                         |
| API            | A P I                             |
| stripe.com     | stripe dot com                    |

画面可以展示精确数字，而旁白可以四舍五入表述。

## 结构

产品类视频：

1. **Hook（钩子）** — 这个产品有什么令人惊讶或印象深刻之处？大胆断言、引发思考的问题、对比或震撼数字。这是开场第一句。**变化钩子类型**——不要每次都默认用数据开场。
2. **Story（故事）** — 产品做什么？谁在用？保持具体。
3. **Proof（证明）** — 数据、客户名称、社会证明。来自产品的真实数字。
4. **CTA（行动号召）** — 观众该做什么？例如：`Start building at stripe dot com.`

不是每条视频都需要四段齐全。15 秒社交广告可能是 Hook + Proof + CTA。60 秒产品导览会四段都用，且 Story 更充实。

## 开场第一句

整支视频里最重要的一句。前 3 秒必须制造张力、好奇或意外感。

有效的模式：

- **大胆断言**：「The financial infrastructure that powers the internet economy.」
- **引发思考的问题**：「What if your database could think?」
- **对比**：「Your AI agent already knows how to make videos. It just needs the right format.」
- **震撼数字**：「Nearly two trillion dollars.」（慎用——不是每条视频都该用数据开场。）

若开场很泛（「Welcome to Stripe」/「Introducing our product」），从头再来。

## 示例

来自一条 62 秒产品发布视频（团队参考）：

```
Your AI agent already knows how to make videos.
It just needs the right format.

This is Hyperframes. An open source framework. HTML in, video out.

A div is a keyframe. Data attributes are your timeline.
CSS is your look. G-Sap is your animation engine.

Anything a browser can render can be a frame in your video.

CSS animations. G-Sap. Lottie. Shaders. Three.js.

Drop in music, sound effects, footage — it all composes together.

No new framework for the agent to learn.
Just HTML.

The agent writes it. The renderer captures every frame as MP4.
It's deterministic. Identical outputs, every time.

Give your agent the CLI. Tell it what to make.
Watch it build.

Hyperframes. Go make something.
```

**注意：** 62 秒约 140 词——即 2.3 词/秒，为停顿与画面留白留出空间。
