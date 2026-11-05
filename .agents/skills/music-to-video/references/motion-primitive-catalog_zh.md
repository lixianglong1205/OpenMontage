# 动效基元目录 — 自由组合菜单

原子层：一个锚点 → 一个微动效。当没有模板适合某组时，从此处命名基元进行自由组合。浏览 **anchor（锚点）** + **best span（最佳时长）** + **what it does（作用）**，再挑选能承载该组的最小集合。

## 时间与延迟（适用于每个基元）

- **硬击为 0ms。** 切镜、调色板翻转、内容互换、定格均为 `tl.set(...)`，无 duration — 打击感本身就是动效。给硬击加缓动会毁掉它。
- **提前于锚点。** 必须在节拍上 _落地_ 的动作（遮罩铺满画面、计数锁定、两块碰撞）需 **提前约 40–190ms** 启动，以便在锚点上完成。响应式入场（因硬击而 _出现_ 的元素）在 0–45ms 后触发。
- **缓动入场：300–500ms**（缩放冲击、滑入、镜头推进）。**宏观构建：800–2000ms**，横跨整段 roll / 静音。
- **每小节上限：** 每次硬击只累积一个元素（不要连发）；每个乐句最多一次镜头运动，绝不要每拍一次；密集的翻转/频闪系统运行 ≤2–3s。
- **张力构建须锁定。** 计数 / 顺序构建 / 形变必须在 downbeat 或 hard_stop 上 _收束_，不能在小节中途拖尾。
- **最佳时长指有效动效。** 目录中的 span 指引不是把单一基元拉满整帧的许可。若自由组合组超出所列 span，应加 hold / bed / 下一基元，或在下一音乐锚点把帧拆成另一组。

## 目录

| id                    | 锚点                             | 最佳时长          | 作用                                                                      |
| --------------------- | -------------------------------- | ----------------- | ------------------------------------------------------------------------- |
| `hypercut-whip`       | beat / hard_stop                 | 0.18-0.45s        | 帧间快速甩镜硬切                                                          |
| `kinetic-letter-in`   | downbeat / phrase                | 0.4-1.2s          | 逐字 kinetic 入场                                                         |
| `braam-punch`         | drop / surge                     | 0.2-0.9s active   | 大冲击：缩放 + 重量感 slam                                                |
| `chromatic-split`     | snare / glitch / surge           | 0.1-0.6s          | 文字上的 RGB 通道分离 / 故障                                              |
| `mask-reveal`         | section_start / downbeat         | 0.5-1.2s          | clip-path 遮罩擦除揭示                                                    |
| `screen-shake`        | drop / crash / kick              | 0.1-0.5s          | 镜头 / 画面抖动                                                           |
| `binary-decrypt`      | roll / build                     | 0.8-2.5s          | scramble→decode 文本（二进制 → 词）                                         |
| `dolly-zoom`          | phrase / build                   | 1.2-2.5s          | 眩晕感 dolly-zoom（缩放 vs 透视）                                         |
| `iris-open`           | section_start / reveal           | 0.6-1.2s          | 圆形 iris 开屏揭示                                                        |
| `electric-arc`        | accent / glitch                  | 0.1-0.6s          | 电弧 / 闪电点缀                                                           |
| `neon-flicker`        | hold / texture                   | 0.5-2.5s          | 霓虹灯闪烁                                                                |
| `chrome-sweep`        | downbeat / reveal                | 0.6-1.4s          | 文字上的金属高光扫过                                                      |
| `slot-machine-reveal` | roll → downbeat                  | 0.8-2.0s          | 老虎机旋转落定字符揭示                                                    |
| `liquid-morph`        | phrase / transition              | 1.0-2.5s          | 液体 / blob 形变                                                          |
| `gooey-metaball`      | build / drop                     | 1.5-3.0s          | 黏糊 metaball 融合场                                                      |
| `3d-card-flip`        | downbeat / swap                  | 0.8-1.6s          | 3D 卡片翻转（rotateY）                                                    |
| `crash-zoom-in`       | drop / surge                     | 0.2-0.8s          | 猛烈 crash 推近                                                           |
| `spotlight-sweep`     | reveal / hold                    | 0.8-2.0s          | 聚光 / 渐变扫过文字                                                       |
| `outline-to-fill`     | downbeat / reveal                | 0.8-1.8s          | 描边轮廓 → 实心填充                                                       |
| `counting-punch`      | roll → downbeat                  | 1.0-2.5s          | 数字计数上冲并锁定                                                        |
| `particle-burst`      | drop / crash                     | 0.2-1.2s          | 粒子爆炸 burst                                                            |
| `radial-burst-lines`  | drop / surge                     | 0.2-0.8s          | 径向速度线 burst                                                          |
| `pixel-dissolve`      | transition / hard_stop           | 0.5-1.5s          | 像素化溶解                                                                |
| `datamosh-smear`      | glitch / transition              | 0.4-1.2s          | datamosh / 运动拖影                                                       |
| `text-wave-distort`   | hold / texture                   | 1.0-2.5s          | 文字波浪扭曲                                                              |
| `bg-flow-field`       | energy / whole span (bed)        | 4-12s bed         | 生成式 curl-noise 背景 bed；可在其上组合任意前景动效                      |
| `blur-resolve`        | stop / final hold                | 0.7-2.0s          | 由虚到清晰对焦，切镜时再虚出                                              |
| `chromatic-pressure`  | snare / glitch                   | 0.1-0.5s          | 瞬态上的 RGB 分离 / 数字张力                                              |
| `color-grid-shuffle`  | onset                            | 0ms hits; ≤2s run | 按每次 onset 的确定性索引重着色网格单元                                   |
| `content-swap`        | beat                             | 0ms hits; ≤3s run | 堆叠节点 0ms 互换：主力打击型动效                                         |
| `directional-fill`    | beat / reveal                    | 0.3-1.0s each     | 方向性擦除填充（scaleX）扫过条块                                          |
| `flash-cut`           | drop / crash                     | 0-0.6s            | 全帧闪白掩盖文字 / 色态变化                                               |
| `freeze-hold`         | hard_stop                        | 0ms in; 0.5-2s    | 冻结运动系统并保持                                                        |
| `hard-cut`            | beat / hard_stop                 | 0ms in; 0.3-2s    | 采样精度的色块 + 文字切镜                                                 |
| `mosaic-pack`         | beat / build                     | 1.5-3.5s          | 散落 tile 飞入并拼成网格                                                  |
| `negative-space-hold` | silence / hard_stop / final hold | 1-6s hold         | 去掉繁忙层，在留白中保持一个可读标记                                      |
| `overlay-pop`         | accent                           | 0.2-0.6s in       | 角标 / 下三分之一 overlay 在底图上弹出                                    |
| `palette-flip`        | section change                   | 0ms flip; 0.5-4s  | 同一布局经 0ms 调色板变量翻转换肤                                         |
| `staggered-exit`      | phrase / transition              | 0.4-1.2s          | 有序级联退出清空画面                                                      |
| `staggered-reveal`    | build                            | 0.8-2.5s          | 堆叠 / 列表有序级联进入                                                   |
| `system-replace`      | drop / regime change             | 0ms cut           | 硬切整个视觉系统，再启动新系统                                            |
| `text-spectral-rays`  | phrase / sweep (hero text)       | 2.5-5s            | 字标向扫光光标投射体积光射线                                              |
| `tile-mosaic`         | build / reveal                   | 1.5-3.5s          | 对角扫过揭示 tile 网格，拼成海报                                          |
| `typewriter-reveal`   | roll / build                     | 1.0-3.0s          | 逐字 / 逐词打字显现与 caret                                               |
| `value-counter`       | roll → downbeat                  | 1.0-2.5s          | 计数在 downbeat / hard_stop 上锁定                                        |
| `word-grid-burst`     | onsets → downbeat                | 1.8-3.2s          | 每次 onset 揭示词格，downbeat 上聚焦一词                                  |

## 如何组合

- 每组一个主导系统；最多在一个结构基元上叠一层纹理基元。
- 强拍上放结构（切镜、镜头、`system-replace` → downbeat / phrase / section_start）；弱拍 / 切分音上放纹理（`content-swap`、打字机逐字、chromatic 点缀）。
- roll 是累积容器 — 在 roll 期间构建，在其结束的 downbeat 硬切到干净布局。
- `drop` ≠ `downbeat`：downbeat 是同一 regime 内的切点；drop 是 regime 切换（`system-replace`、总清空、元素数量跃迁）。
- 用静音减密度（`negative-space-hold`）。
- 背景 bed 是层，不是动效：同一时间一个 bed，位于前景基元之下。
- `text-spectral-rays` 是 hero 字标处理；不要在上面再叠同一词的可见副本。
