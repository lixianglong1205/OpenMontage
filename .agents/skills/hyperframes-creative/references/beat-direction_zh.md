# Beat 方向（Beat Direction）

如何在多场景合成中规划与执导单个场景（beat）。在编写任何多场景视频之前请先阅读本文。

## 目录

- 单 beat 方向
- 概念
- 情绪方向
- 动画编排
- 转场
- 景深层次
- SFX 提示
- 节奏规划
- 速度匹配转场

---

## 单 Beat 方向

每个 beat 是一个「世界」，而不是一种版式。在写 CSS 规格与 GSAP 指令之前，先描述观众会**体验到什么**。优秀分镜与平庸分镜的差别在于：

**平庸：**「深海军蓝背景。白色「$1.9T」，280px。Logo 左上。波形图右下。」
**优秀：**「镜头已在广阔深色画布上空飞行途中。渐变波形如极光般扫过画面——有生命、在流动。「$1.9T」以极大冲击力**砸**入画面，连波形都随之涟漪。这不是滑入——这是一个时刻。」

前者描述像素。后者描述体验。先写后者，再推导像素。

每个 beat 应包含：

### 概念

用 2–3 句话概括本 beat 的核心想法。我们处在怎样的视觉**世界**？什么隐喻在驱动画面？观众应**感受**什么？这是最重要的一块——其余皆由此流出。

### 情绪方向

文化与设计参照，而非 hex 色值：

- 「几何、有节奏、精确。可参考 Josef Albers 或包豪斯色彩研究。」
- 「温暖的工作区。好笔记本的质感，而非技术蓝图。」
- 「电影感片头。那种让你不自觉前倾的开场。」

### 动画编排

每个元素要有具体的运动动词——不是「它动画进入」，而是**如何**进入。动词来自 beat 的概念与内容，而非来自「能量档位」。 wellness（健康）品牌里偏「慢」的 beat，若内容关于「放手」，仍可能有东西**坠落**；数据类 beat 若品牌身份偏轻盈，也可能**漂浮**。

运动动词词汇（按物理气质组织，而非按能量高低）：

**冲击 / 重量：** SLAMS、CRASHES、PUNCHES、STAMPS、SHATTERS、DROPS（带力度）
**方向性 / 刻意：** SLIDES、PUSHES、PULLS、WIPES、CUTS
**揭示 / 构建：** DRAWS、FILLS、GROWS、EXPANDS、ASSEMBLES、COUNTS UP
**有机 / 环境：** FLOATS、DRIFTS、BREATHES、PULSES、ORBITS、MORPHS
**机械 / 精确：** TYPES ON、CLICKS、LOCKS IN、SNAPS、STEPS

每个元素都要有一个动词。若叫不出动词，说明该元素尚未设计完成。动词应服从 beat 的概念——而非查表「高能量」或「低能量」 beat 该用什么。

针对文字元素，可按 ID 指定确定性的命名效果（如 `typewriter`、`kinetic-center-build`、`soft-blur-in`），而不必从零发明时序——24 种效果词汇表及加载方式见 `skills/hyperframes-animation/adapters/animate-text.md`。

### 转场

本 beat 如何交给下一 beat。写明类型与参数。

**何时选哪种：**

| 选用 shader 转场 | 选用 CSS 转场 | 选用硬切 |
| ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------- |
| 揭示、大反应镜头、产品/Logo 揭幕、能量切换、「哇」时刻 | 连续运镜感 beat，整段像一次运动被切成多镜 | 快切列表、跟拍点的打击感剪辑、喜剧节奏 |
| 音乐/旁白在强拍（downbeat）或 SFX 重击处落点的任何时刻 | beat 之间用共享运动词汇平滑衔接 | 3 段及以上快速节拍匹配切换 |
| 转场本身即视觉的品牌时刻 | 极简/编辑型 pacing（节奏） | 0.3–0.8s 转场会显得太慢的任何情况 |

经验法则：若该 beat 是视频的**核心高光**，用 shader 转场切入。若 beat 是衔接段，CSS 交叉淡化即可。5–7 个 beat 的品牌片通常只需 1–2 次 shader 转场（英雄揭示 + CTA）——过多会冲淡冲击。

**同一合成中混用 shader 与 CSS 交叉淡化转场是支持的。** 任意转场条目省略 `shader` 即得平滑 opacity 交叉淡化——HyperShader 统一管理所有场景可见性。让 HyperShader 创建时间轴（不要传入预构建的 `timeline:` 选项），在 `init()` 之后把所有合成 tween 加到返回的 `tl` 上。配置片段见 `skills/hyperframes-animation/transitions/overview.md` → 「CSS vs Shader」。

**CSS 转场** — 13 大类 30+ 模式。完整代码在 `skills/hyperframes-animation/transitions/`（经 `catalog.md` 路由）。按能量与手感选取：

| 类别 | 模式 | 运动气质 |
| ------------------ | ------------------------------------------------------------------------ | -------------------------------------------------------------------------- |
| **Push / slide** | Push slide、vertical push、elastic push、squeeze | 内容像在连续表面上穿过画面 |
| **Scale / zoom** | Zoom through、zoom out | 透视变化——靠近或远离内容 |
| **Radial / clip** | Circle iris、diamond iris、diagonal split | 几何揭示——内容由形状露出或盖住 |
| **3D** | 3D card flip | 物理感——内容像实体翻面 |
| **Dissolve** | Crossfade、blur crossfade、focus pull、color dip | 重叠混合——转场期间两场景同时存在 |
| **Cover / blinds** | Staggered color blocks、horizontal blinds（6/12 条）、vertical blinds | 结构感——内容被切条、叠层或覆盖 |
| **Light** | Light leak overlays、overexposure burn、film burn | 有机胶片——光晕扫过画面 |
| **Distortion** | Glitch（CSS RGB jitter）、chromatic aberration、ripple、VHS tape | 不稳定——图像本身像故障 |
| **Blur** | Blur through、directional blur | 柔焦——内容模糊进出 |
| **Mechanical** | Shutter（两半）、clock wipe（9 点楔形） | 精确——带可见机械逻辑的转场 |
| **Grid** | Grid dissolve（12/120 格） | 碎片化——画面拆成块 |
| **Destruction** | Page burn（SVG clip-path + canvas 边缘） | 戏剧性 decay——上一场景被「烧掉」 |
| **Other** | Gravity drop、morph circle | 物理或形变运动，不适配其他类 |

常用快选：

- **速度匹配向上**：exit `y:-150, blur:30px, 0.33s power2.in` → entry `y:150→0, blur:30px→0, 1.0s power2.out`
- **Whip pan**：exit `x:-400, blur:24px, 0.3s power3.in` → entry `x:400→0, blur:24px→0, 0.3s power3.out`
- **Blur through**：exit `blur:20px, 0.3s` → entry `blur:20px→0, 0.25s power3.out`
- **Zoom through**：exit `scale:1→1.2, blur:20px, 0.2s power3.in` → entry `scale:0.75→1, blur:20px→0, 0.5s expo.out`
- **Hard cut / smash cut**：即时，用于快切序列

时序预设：snappy（0.2s）、smooth（0.4s）、gentle（0.6s）、dramatic（0.5s）、instant（0.15s）、luxe（0.7s）。

**Shader 转场** — 14 种内置 WebGL GPU 效果。安装：`npx hyperframes add <name>`（block 名 ≠ shader 名——见 `skills/hyperframes-registry/references/discovery.md`）；完整 API 见 `packages/shader-transitions/README.md`。

| Shader | 视觉描述 | 时长范围 |
| ----------------------- | ---------------------------------------------------------------------------------------------- | -------------- |
| **domain-warp** | 有机 FBM 溶解——两场景向彼此扭曲，中点 accent 闪 | 0.5–0.8s |
| **ridged-burn** | 多重分形遮罩沿 burn ramp 揭示入画场景，边缘火花 | 0.5–0.8s |
| **whip-pan** | 10 采样水平运动模糊 + 横向交叉淡化——像镜头在镜头间 pan | 0.3–0.5s |
| **sdf-iris** | 圆 SDF 自中心扩展，扩展边缘 accent 色光晕环 | 0.5–0.7s |
| **ripple-waves** | 径向驻波 UV 位移——内容随场景交叉向外涟漪 | 0.6–1.0s |
| **gravitational-lens** | 向中心 pinch + R/B 色散——内容内弯再释放 | 0.6–1.0s |
| **cinematic-zoom** | 12 采样 RGB 偏移径向 zoom 模糊——自中心辐射运动条痕 | 0.4–0.6s |
| **chromatic-split** | R/B 径向通道外移、G 固定——通道分离再汇合 | 0.3–0.5s |
| **swirl-vortex** | 逆时针 swirl + FBM 噪声——内容旋出、新场景旋入 | 0.5–0.8s |
| **thermal-distortion** | 垂直 sine + FBM 水平位移——热霾 shimmer 扫过画面 | 0.5–0.8s |
| **flash-through-white** | 经白色中点淡入淡出——0.01s 几乎不可见，0.3s 可察觉 | 0.01s–0.3s |
| **cross-warp-morph** | FBM 向量场位移两场景；第三 FBM 偏置 wipe 方向 | 0.5–0.8s |
| **light-leak** | 固定画外光源、指数衰减、暖色与 ridge flare | 0.5–0.8s |
| **glitch** | 行位移 + RGB 横向分离 + 扫描调制 + posterization + flicker | 0.3–0.5s |

**你并不限于此处所列。** 这些是内置选项，但你应当且可以：

- **从零编写自定义 GLSL shader** 以实现独特转场
- **在线搜索** shader 代码（ShaderToy、GLSL Sandbox、GitHub）并适配
- **构建不在任何类别中的自定义 CSS 转场**——以新方式组合 clip-path、transform、filter
- **向用户索取或一起寻找** 特定效果，若你需要专门素材

若分镜需要尚不存在的效果——就去做。框架能渲染浏览器能跑的任何东西。

### 景深层次

前景、中景、背景各有什么。每个 beat 至少应有 2 层：

- 「BG：深海军蓝填充 + 轻微径向光晕。MG：带投影的数据卡片。FG：品牌 Logo 右下。」

### SFX 提示

何时出现什么声音：

- 「在 capture pulse（捕捉脉冲）时——轻柔、温暖的模拟快门咔哒。」
- 「左侧 faint 低频 drone（嗡鸣）。fold 时：drone 切断。静默。然后一声干净 chime（钟音）。」

---

## 节奏规划

在写 HTML 之前，声明场景节奏：哪些镜是快击、哪些是 hold、shader 落在哪、能量峰值在哪。先命名模式——如 fast-fast-SLOW-fast-SHADER-hold——再实现。

**节奏来自分镜与品牌，而非查表。** 15 秒建筑事务所社交广告与 15 秒游戏品牌社交广告节奏不同——同为 15 秒，一个是 slow-reveal-hold-CTA，另一个是 rapid-fire-SLAM-hook。视频类型设定约束（时长、大致 beat 数）；品牌与内容决定那些 beat 是慢是快、疏是密、戏剧还是克制。

驱动节奏决策的问题：

- 观众应经历怎样的情绪旅程？峰值时刻在哪？
- 旁白最重 emphasis（强调）落在哪？那通常是能量应峰值处。
- 品牌自身视觉 pacing（节奏）暗示什么——从容还是紧迫？
- 在该时长内能支撑多少 beat 而不显仓促或注水？

15 秒内既要 2s hook、又要展示 3 个功能、还要 CTA 的社交广告会像噪声。有时「hook-hold-CTA」加一个强功能，才是 15 秒的正确节奏。实现前先写下你规划的节奏。

---

## 速度匹配转场

出画 beat 用加速 ease（`power2.in` 或 `power3.in`）退出，并渐增 blur。入画 beat 用减速 ease（`power2.out` 或 `power3.out`）进入，并渐清 blur。两条 ease 曲线最快点在切点相遇——观众感知连续运镜，而非两段离散动画。出画速度与入画速度匹配，容差约 ±5%。
