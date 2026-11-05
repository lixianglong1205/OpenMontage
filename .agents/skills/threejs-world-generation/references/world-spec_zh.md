# `threejs_world` 规范

使用归一化区域坐标 `[-1, 1]`；工具会将其转换为世界空间。地标与相机的位置为世界空间 `[x, y, z]` 值。

## 最小结构

```json
{
  "version": "1.0",
  "title": "The Luminous Divide",
  "seed": 2048,
  "explicit_constraints": ["a volcanic rift divides a living valley"],
  "inferred_details": ["three semantic regions", "dawn atmosphere"],
  "world": {
    "size": 120,
    "resolution": 160,
    "elevation_scale": 18,
    "water_level": -1.5
  },
  "atmosphere": {
    "sky_color": "#07111f",
    "fog_color": "#13263a",
    "fog_density": 0.009,
    "sun_color": "#ffd7a3",
    "sun_intensity": 3.2,
    "sun_position": [45, 70, 20]
  },
  "terrain_materials": [
    {
      "id": "mossy-ground",
      "regions": ["ember-rift"],
      "base_color": "assets/materials/mossy-ground/diffuse.jpg",
      "normal": "assets/materials/mossy-ground/normal.jpg",
      "roughness": "assets/materials/mossy-ground/roughness.jpg",
      "meters_per_repeat": 7
    }
  ],
  "asset_palette": [
    {
      "id": "rift-tree-a",
      "catalog_id": "kenney-nature-kit",
      "model_id": "tree-pine-a",
      "category": "tree",
      "region_id": "ember-rift",
      "count": 80,
      "scale_range": [0.8, 1.5]
    }
  ],
  "regions": [
    {
      "id": "ember-rift",
      "label": "Ember Rift",
      "center": [-0.35, 0.12],
      "radius": 0.58,
      "base_elevation": 0.3,
      "amplitude": 1.0,
      "frequency": 1.4,
      "landform": "ridge",
      "blend_width": 0.2,
      "color": "#5b271f",
      "accent_color": "#ff6b2c",
      "scatter": {"rock": 90, "crystal": 22, "tree": 0}
    }
  ],
  "landmarks": [
    {
      "id": "rift-gate",
      "type": "arch",
      "region_id": "ember-rift",
      "position": [-24, 0, 8],
      "scale": 5.5,
      "color": "#2a2020",
      "accent_color": "#ff7a35"
    }
  ],
  "camera_path": [
    {"time": 0, "position": [72, 42, 72], "target": [0, 3, 0], "fov": 46},
    {"time": 60, "position": [-54, 13, -32], "target": [-12, 4, 5], "fov": 40}
  ]
}
```

## 区域（Regions）

必填：`id`、`center`、`radius`、`color`。

常用字段：

- `label`：面向人类的诊断用标签。
- `base_elevation`：在应用 `elevation_scale` 之前的归一化垂直偏移。
- `amplitude`：起伏/ relief 贡献度。
- `frequency`：宏观噪声频率。
- `landform`：`plain`、`peak`、`ridge`、`dune`、`terrace`、`basin` 或 `canyon`。
- `blend_width`：语义边界的柔和程度。
- `accent_color`：用于语义与环境细节。
- `scatter`：`tree`、`rock`、`crystal` 原型的数量。
- `slope_limit`：散布实例可接受的最大坡度代理值。

每个地形采样点都会对区域权重做归一化。兜底区域仍须覆盖整个域，因此避免没有宽泛邻接的小块孤立区域。

## 地标（Landmarks）

支持的程序化类型：`monolith`、`arch`、`tower`、`ruin`、`crystal`、`settlement` 和 `ring`。

每个地标放置在采样地形高度上。`position[1]` 是额外的垂直偏移，而非绝对 Y 坐标。在迭代 refine 时保持 ID 稳定，以便评审备注仍可对应到具体对象。

## 相机路径（Camera path）

- 至少提供两个关键帧。
- 首个关键帧的 `time` 必须为 `0`；最后一个关键帧应对齐所请求的时长。
- 关键帧按时间有序，且落在时长范围内。
- 运行时对 position、target 和 FOV 使用 smoothstep 缓动插值。
- 为区域级与步行级镜头增加更多关键帧；不要用相邻关键帧瞬移来模拟剪辑。
- 除非经过评审的刻意贴地镜头，相机应至少高于采样地形 `2` 个世界单位。

## 渲染模式

- `cinematic`：PBR 顶点色、雾、水面、阴影与叠加层。
- `semantic`：饱和区域色与标签，用于布局诊断。
- `wireframe`：地形拓扑与显式场景节点，用于几何诊断。

## 工具输出

`operation: "build"` 会写入：

- `index.html`：HyperFrames 合成根节点。
- `world.json`：归一化、可编辑的规范。
- `world-spec.js`：可在浏览器中加载的规范。
- `world-runtime.js`：确定性的 Three.js 场景构建。
- `world.css`：全画布与生产用叠加层样式。
- `world-report.json`：校验、性能估算与警告。
- `hyperframes.json`：本地 registry 配置。

生产构建还会额外写入 `asset-catalog-index.json` 与 `asset-catalog.js`，并将所选 catalog 复制到 `assets/models/`，使渲染不依赖远程模型拉取。

`operation: "validate"` 仅执行规范检查，不写入工作区。
