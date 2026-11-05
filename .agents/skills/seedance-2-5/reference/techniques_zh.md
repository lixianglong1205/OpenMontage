# Seedance 2.5 — 十种官方提示词类别

Higgsfield 于 2026 年 8 月发布了一个包含十个类别的提示词库，每个类别都经过多轮生成测试，以观察哪些结构在第二次运行时仍然成立。本文件记录每个类别使用的设置、该组合为何有效，以及**它引入的技法**。

在从零撰写提示词之前，可先选用最接近的原型。

完整提示词见 <https://higgsfield.ai/blog/seedance-2-5-prompting-guide>，页面带复制按钮。此处不逐字复现——下文是可提炼的方法。

---

## 1. 戏剧性外景 · 人物主体，现有光

**设置：** 类型 drama · 黄金时刻，单一动机光源 · 情绪控制：克制之下的悲恸 · 变形宽银幕大画幅，广角与特写混合覆盖。

**为何有效：** drama 比多数类型更久地留住镜头，双人戏才有空间展开。黄金时刻让各段光线一致，无需在每段里重复描述太阳位置。

**引入：**
- **Event track（事件轨）。** 大海被声明为「事件轨，而非纹理」，每一道浪、每一阵风都给出时间戳，以及溅起高度占画幅的百分比。间隔不规则，没有两次完全相同。
- **STILLNESS LOCK（静止锁定）。** 列出不发生之事：无人站起、无人拥抱、没有手离开毯子。恰好一滴泪落下，是她的，在 13.2s。
- **Blocking in percentages（百分比走位）。** 她在 x 42%，头在 y 44%。他在 x 58%，y 42%。
- **Reverse-angle note（反打角度说明）。** 当镜头切到面向大海一侧时，她在画面右侧、他在画面左侧。两人永不互换左右。
- **LENS LOCK per segment（每段镜头锁定）** 以度数计：广角 47°，特写 29°。
- **Invented face（虚构面孔）。** 「完全原创、虚构的面孔」，避免克隆任何真实相貌。

## 2. 动作序列 · 多镜头编排

**设置：** 类型 action · 物理真实、高冲击、真实纸张质量与惯性 · 变形宽银幕，手持与陀螺稳定混合 · 硬冷主光加单一暖色点缀。

**为何有效：** action 收紧节奏并让摄影机贴近运动，九镜打斗读起来像一条连续序列，而非拼接镜头。

**引入：**
- **Physics per material, named and marked critical（按材质写物理，命名并标为 critical）。** 整段专写钞票是独立纸张——可见纤维、磨损折痕，每张钞票在各自气流中翻滚——避免数百张钞票被读成一块刚性整体。
- **Marking sections "(critical)"（将段落标为「(critical)"）。** 标出不可被忽略的块。
- **Palette in percentages（百分比调色）。** 60% 冷钢、30% 哑光黑、10% 暖色焦点 pop。「她和现金是冷世界里唯一的暖色。」
- **Author references "in spirit, fully original execution"（作者引用「精神致敬，执行完全原创」）。** 点名导演与摄影指导，但不复制具体作品。
- **Explicit anti-plastic block（显式反塑料块）** 枚举真实光学瑕疵：胶片颗粒、片门抖动、光晕、色差、跟焦时的镜头呼吸。
- **Cuts land on the hits（切在打击点上）**，绝不在静止 pose 上切。

## 3. 商业产品 · 多参考场景

**设置：** 类型 general · 真实手持、轻微抖动 · 物理：在诚实规则下的「真实魔法」。

**为何有效：** 锁定三个 reference（人物、场景、产品）让三者稳定，噱头在周围发生。

**引入：** 把效果定义为带规则的 **mechanic（机制）**，而非形容词。色波从每一步 footfall 以恒定径向速度辐射，重绘所过之处并保留。同一机制让模型逐镜重复，而非每镜即兴。若你的片子里有视觉花招，应这样写。

## 4. 史诗 landscape · 环境即主角

**设置：** 类型 epic · 三镜皆慢速稳定 push-in · 明亮漫射日光、冷调 grade。

**十类中最短。** 三镜、三句，镜间 `Hard cut`，结尾 consistent-look 块写排除项（无人、无动物、无鸟、无 shake）。

**要点：** 画面上无人时，几乎不需要各类 lock。提示词复杂度应跟踪**实际可能漂移的内容**，而非野心大小。

## 5. 黑色电影 · 阴影与氛围

**设置：** 带 noir 底的 drama · 硬主光、高对比、单色 · 变形宽银幕，每段镜头锁定。

**引入：**
- **LOCATION MAP（场景地图）。** 空间写清：整段序列摄影机从南人行道朝北工作，背景、中景、前景均指定。
- **SCREEN DIRECTION LOCK（银幕方向锁定）。** 轿车始终从画面右侧入画，女子始终右向左行，摄影机永不穿过到街对面。
- **Lens ladder per segment（每段镜头阶梯）：** 84° 广角、29° 中景、47° 标准、18° 长焦双人、84° 低机位收尾，并写「段内无镜头 drift」。
- **State monotonicity（状态单调性）** 用于湿度：只增不减，从不重置。
- **Controlled legible text（可控可读文字）：** 全场唯一可读文字是霓虹招牌上的词。

## 6. 多角色 · 跨帧面孔一致

**设置：** Action，performance piece · 平均镜头低于 1.5 s · Dual-quality system。

**最难类别：** 四个具名角色、二十四快切，镜间无暇重新交代谁是谁。

**引入：**
- **COUNT LOCK（数量锁定）。** 恰好四人，永不为五，无背景替身、无克隆成员，无 mirror、玻璃或反射多出一副本。
- **DUAL-QUALITY SYSTEM（双画质系统）。** 每个 beat 标 `[FILM]` 或 `[REPORTER CAM]`， degradation 写全，并明确规则：**永不泄漏**到另一体系。
- **Match-cut motif（匹配切 motif）。** 圆形与眼睛在场景间押韵：CRT 屏、舷窗、牙科灯、行星盘、瞳孔。
- **Wardrobe by act（按幕服装）**，在 locks 块中声明。
- 「每只手恰好五根手指。」

## 7. 奇幻动作 · 人物与生物尺度

**设置：** Epic，action · 夸张物理，全程无 blood · 情绪控制： calm、专注、不恐惧。

**引入：**
- **One grammar per action（每个动作一套语法）。** 她只 cut、从不 stab，四阶段 cut 写清，外加片中**封闭列表**的五次挥剑动作及时间戳。
- **Slow-motion allow-list（慢动作白名单）。** 仅两处，精确时间戳，别处禁止。
- **Substitute rather than only forbid（替代而非仅禁止）。** 无 blood：恶魔为冷却熔岩、内藏火，cut 缘发橙光、火星吹出、躯体化为 ash。
- **Numeric heights（数值高度）。** ledge 地面为 0，horde 2.5 m，archdemon 5 m、眼在 4.5 m；她平视 4 m、降至 3 m 使他俯视她。
- **A geometric weak point（几何弱点）** 带尺寸与暴露条件。
- **Progressive dirt（渐进脏污）** 只增不洗。

## 8. UGC 风格广告 · 自然运动、无制作感

**设置：** 类型 general，不施加类型专属视觉逻辑 · 全程固定 handheld 自拍 framing · 客舱内柔和均匀光 · 情绪控制： understated、不表演。

**引入：**
- **Performance by imperfection（以不完美表演）。** 自然 blink 频率、反应慢半拍、微笑由小变大、句中瞥离镜头再回看、飞机上自拍时压低声音的 self-conscious 感。
- **Live background people, not NPCs（活背景人，非 NPC）。** 各自独立活动；无人看镜头、无人同步反应。
- **Fixed seating geometry（固定座位几何）** 贯穿八镜。
- **State monotonicity** 用于 cookie：整、咬过、两半、吃完，从不再生。
- **Turbulence 仅存在于两镜且不再出现。**
- **Dialogue per shot in complete sentences（每镜完整句对白）**，全部 speech 在 25s 前结束。

## 9. 恐怖 · 错误的光、错误的角度

**设置：** 类型 horror · 深一点透视、4:3 · 真实重量与惯性 · 情绪控制：疲惫、泪涌、张力 holding 无 release。

**引入：** 肩后 negative space 先声明为空，再被填满—— dread 来自缺席而非 reveal。

十类中最精炼的规则之一： antagonist **直至最后一秒才清晰对焦**。始终是 blur、silhouette、货架后的 fragment。「autofocus 拒绝在她身上 lock。」对焦作为叙事装置来 directing。

## 10. 纪录片 · 观察式摄影机

**设置：** General，第三人称观察 · 整段单一 47° 镜头 · 同一连续时段内五种 distinct 自然光状态。

**引入：**
- **SINGLE-LENS LOCK（单镜头锁定）。** 三十秒单一焦距；所有 framing 变化靠操作者 physically 行走，每段声明 camera-to-subject 距离：5 m、2 m、3 m、2.5 m、7 m。
- **Crowd size as the clock（人群规模作时钟）。** 起始四十人、六十、峰值一百、深夜十五或二十、黎明五六——读起来像连续一夜而非五场独立戏。
- **FRAMING RESPECT LOCK（ framing 尊重锁定）。** 摄影机把她当派对上的人而非 body：无 slow pan 上下扫身、无孤立 torso 或 leg 镜头、无 low angle。
- **BEAUTY WITHOUT RETOUCHING LOCK（无修图之美锁定）。** 可见毛孔、晒红加深、盐渍干成 faint bloom、前臂 sand、黎明 tired eyes。
- **CLEAN-AIR LOCK（洁净空气锁定）。** 无人吸烟；唯一 smoke 来自火且始终向海飘。
- **Wardrobe layered progressively** 随气温下降逐层增加。

---

## 测试得出的六点结论

1. **Reference 比文字描述更可靠地跨切保持 identity。** 面孔或产品一旦锁为 reference，能在 hard cut、光变、运镜下存活，否则易 drift。
2. **类型与 lighting 设置比大部分提示词正文更有效。**
3. **多角色场景是最难保持一致的类别。** 单镜面孔越多，每个需要的 reference 素材越多。
4. **逐镜 breakdown 优于单一连续场景描述**，只要不止一个机位。模糊 transition 是序列散架最常见原因。
5. **50 个 reference 是上限，宜 deliberate 使用，而非默认拉满。** 杂乱 reference 集比小而精的集更不 coherent。
6. **GLOBAL STYLE 与 AUDIO 更像 guardrail 而非指令。** 显式排除不应出现的内容，比堆正面描述更能防失败。
