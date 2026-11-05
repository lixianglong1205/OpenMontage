---
name: threejs-world-generation
description: 从文本或结构化简报构建可确定、可编辑、自由视点的 Three.js 世界。适用于电影级 3D 地形、语义区域、程序化生物群系、显式地标、环境散布、相机飞越、世界诊断，或需要真实 3D 环境而非生成 2D 影像的请求。与 OpenMontage 的 threejs_world 工具及 HyperFrames 集成；不适用于单个孤立 3D 物体或平面视差场景。
---

# Three.js 世界生成

若需生产级网格与 Blender 装配，另请阅读 `3d-asset-generation`。
Three.js 仍是语义化交互/体块渲染器；当简报要求密集、参考级场景时，Blender 为生产渲染器。

生产交接必须包含导入资产的目标尺寸、语义散布排除区、贴地水体/路径几何、地标可见性策略、相机净空，以及全局/区域/步行级审查帧。这些是 world-spec 契约，而非手工 Blender 清理说明。

创建持久场景图，而非一系列互不相关的 2D 镜头。保留用户显式约束，单独推断缺失的构造细节，先建立全局地形，再精炼选定区域且不破坏全世界空间契约。

## 显式选择保真度层级

- `blockout`：程序化基元、顶点色、语义/布局验证、快速迭代。切勿称其为生产质量、参考级或与 WorldClaw 视觉等价。
- `production`：经许可的本地 GLTF/GLB 目录，至少八个模型、覆盖四个语义类别，三层 PBR 地形，资产溯源，步行级重复审查，且地标不得回退为基元。

英雄视频或任何需展示已填充纹理环境的参考，使用 `production`。若无法满足其目录/材质/提供方要求，在预检或资产门处停止。勿将 blockout 作为最终交付物渲染。

## 先读这些

- 规划或解释由粗到细方法时，阅读 [references/worldclaw-principles.md](references/worldclaw-principles.md)。
- 编写 `world_spec` 或调用 `threejs_world` 前，阅读 [references/world-spec.md](references/world-spec.md)。
- 编辑生成的工作区前，阅读 `hyperframes-core`、`hyperframes-animation` 与 `hyperframes-animation/adapters/three.md`。
- 生产层级工作请阅读 `threejs-loaders`、`threejs-materials`、`threejs-textures`、`threejs-lighting` 与 `threejs-postprocessing`。

## 路由请求

- 设计主导、说明性、抽象或音乐驱动的世界影片，使用 `animation` 管线。
- 预告片式氛围、戏剧化揭示或源素材+世界编辑，使用 `cinematic` 管线。
- 交付物为代码原生 Three.js 世界时选 HyperFrames；参考级英雄渲染选 Blender，FFmpeg 仅用于打包 Blender 编号帧与已批准音频。在提案阶段记录该选择；批准后勿静默切换。
- 保持为现有管线内的能力。勿仅因场景为 3D 而新建管线。

## 工作流

### 1. 区分意图与补全

规划前先记录两份列表：

- `explicit_constraints`：仅用户提供的事实。
- `inferred_details`：为使世界可执行而补充的尺度、区域覆盖、地形算子、密度、调色精炼与相机细节。

切勿将推断的地标、生物群系或故事节拍混入显式列表。

### 2. 全局规划

编写一份共享 `world_spec`，包含：

- 世界尺度、地形分辨率、高程范围与 seed；
- 语义区域：归一化中心、半径、地貌算子、调色与散布配方；
- 跨所有区域共享的氛围与光照；
- 带稳定 ID 与世界空间放置的显式地标；
- 完整相机路径：时间、位置、目标与视场。

优先 3–7 个区域。每个区域须贡献独特的轮廓、表面可读性或功能角色。

### 3. 构建地形基础

生产模式下，先调用 `threejs_asset_catalog`，在 `projects/<id>/assets/3d/catalogs/<catalog-id>/` 下安装权利安全的目录。在资产清单中记录来源、许可证、归档哈希、模型清单及每个选中模型。再以 `quality_tier: "production"` 与已安装目录路径调用 `threejs_world`。

```python
from tools.graphics.threejs_world import ThreeJSWorld

result = ThreeJSWorld().execute({
    "operation": "build",
    "world_spec": world_spec,
    "output_path": "projects/<id>/hyperframes",
    "duration_seconds": 60,
    "render_mode": "cinematic",
    "quality_tier": "production",
    "asset_catalog_paths": ["projects/<id>/assets/3d/catalogs/kenney-nature-kit"],
})
```

将 `world.json`、`world-spec.js`、`world-runtime.js` 与 `world-report.json` 视为可编辑资产。在资产门批准前勿将其压平为视频。

### 4. 区域检视

当 cinematic 材质遍中空间问题难以看清时，以 `render_mode: "semantic"` 或 `"wireframe"` 做第二遍构建。从全局、区域与步行级视点检查快照。

维护带稳定主题的问题队列：

- 地形过渡或轮廓；
- 地标尺度、姿态或接触；
- 散布密度、坡度拒绝或重复；
- 材质对比与氛围；
- 相机净空、裁剪或弱构图。

尽可能只修复受影响区域或对象。保留 seed、区域 ID、相机时间与无关参数。

### 5. 有界循环精炼

最多运行三轮渲染引导精炼：

1. 构建工作区；
2. 运行统一 HyperFrames `check` 门并在代表性时间点快照；
3. 检查帧并更新问题队列；
4. 修改最窄的相关 spec 字段；
5. 以相同 seed 重建并对比。

当无实质问题剩余或达到迭代预算时停止。报告残余限制，勿用叠加层掩盖。

### 6. 合成且不覆盖

浏览器原生交付时，设 `render_runtime: "hyperframes"` 与 `composition_mode: "atelier"`；`video_compose` 须保留已编写的工作区。参考级视频用 `resume: true` 渲染 Blender PNG 序列，再设 `render_runtime: "ffmpeg"` 打包。保留 world spec 与 `.blend` 为可编辑真相源。

## 质量门

- 地形连续，区域边界融合且无明显接缝。
- 每个地标接触其支撑面且留在世界边界内。
- 散布遵守区域亲和、坡度限制与确定性 seed 行为。
- 全局、区域与步行级帧均读作同一连续世界。
- 相机路径保持在地形之上、避免裁剪，并至少有一次建立尺度的揭示镜头。
- 渲染后世界源仍可编辑：区域、地标、相机关键帧与调色有稳定 ID 或字段。
- 交付前 HyperFrames `check` 与渲染后审查通过。仅在支持旧 runtime 时使用 legacy `validate` 或 `inspect` 操作。
- 生产美观帧在前景、中景、背景深度均有纹理资产；无主导物体可读作无纹理的 box、cone、octahedron 或 dodecahedron。
- 生产要求至少四个语义资产类别、八个不同模型、三层 PBR 地形、每个相机关键区域一次区域构图审查，以及显式重复/接触结论。

## 边界

- 生产目录路径能显著改善几何与表面丰富度，但仍无法复现 WorldClaw 的 GPT-Image-2、SAM3、SAM3D、Hunyuan3D、BlenderMCP 或四 H20 实现。
- 除非其他工具显式添加，勿声称有关节资产、游戏物理、导航网格或交互逻辑。
- 勿使用无 seed 随机、墙钟时间动画、远程模型或渲染时资产拉取。
- 勿删除底层 `threejs-*` 技能。它们是扩展本 runtime 时的子系统参考。
