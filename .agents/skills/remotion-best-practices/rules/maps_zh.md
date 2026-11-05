---
name: maps
description: 使用 Mapbox 制作地图动画
metadata:
  tags: map, map animation, mapbox
---

可以使用 Mapbox 将地图添加到 Remotion 视频中。  
[Mapbox 文档](https://docs.mapbox.com/mapbox-gl-js/api/) 提供 API 参考。

## 前提条件

需要安装 Mapbox 和 `@turf/turf`。

在项目中查找锁文件，并根据包管理器运行相应命令：

若找到 `package-lock.json`，使用以下命令：

```bash
npm i mapbox-gl @turf/turf @types/mapbox-gl
```

若找到 `bun.lock`，使用以下命令：

```bash
bun i mapbox-gl @turf/turf @types/mapbox-gl
```

若找到 `yarn.lock`，使用以下命令：

```bash
yarn add mapbox-gl @turf/turf @types/mapbox-gl
```

若找到 `pnpm-lock.yaml`，使用以下命令：

```bash
pnpm i mapbox-gl @turf/turf @types/mapbox-gl
```

用户需要注册免费的 Mapbox 账户，并访问 https://console.mapbox.com/account/access-tokens/ 创建访问令牌。

Mapbox 令牌需添加到 `.env` 文件中：

```txt title=".env"
REMOTION_MAPBOX_TOKEN==pk.your-mapbox-access-token
```

## 添加地图

以下是 Remotion 中地图的基础示例。

```tsx
import { useEffect, useMemo, useRef, useState } from "react";
import { AbsoluteFill, useDelayRender, useVideoConfig } from "remotion";
import mapboxgl, { Map } from "mapbox-gl";

export const lineCoordinates = [
  [6.56158447265625, 46.059891147620725],
  [6.5691375732421875, 46.05679376154153],
  [6.5842437744140625, 46.05059898938315],
  [6.594886779785156, 46.04702502069337],
  [6.601066589355469, 46.0460718554722],
  [6.6089630126953125, 46.0365370783104],
  [6.6185760498046875, 46.018420689207964],
];

mapboxgl.accessToken = process.env.REMOTION_MAPBOX_TOKEN as string;

export const MyComposition = () => {
  const ref = useRef<HTMLDivElement>(null);
  const { delayRender, continueRender } = useDelayRender();

  const { width, height } = useVideoConfig();
  const [handle] = useState(() => delayRender("Loading map..."));
  const [map, setMap] = useState<Map | null>(null);

  useEffect(() => {
    const _map = new Map({
      container: ref.current!,
      zoom: 11.53,
      center: [6.5615, 46.0598],
      pitch: 65,
      bearing: 0,
      style: "⁠mapbox://styles/mapbox/standard",
      interactive: false,
      fadeDuration: 0,
    });

    _map.on("style.load", () => {
      // Hide all features from the Mapbox Standard style
      const hideFeatures = [
        "showRoadsAndTransit",
        "showRoads",
        "showTransit",
        "showPedestrianRoads",
        "showRoadLabels",
        "showTransitLabels",
        "showPlaceLabels",
        "showPointOfInterestLabels",
        "showPointsOfInterest",
        "showAdminBoundaries",
        "showLandmarkIcons",
        "showLandmarkIconLabels",
        "show3dObjects",
        "show3dBuildings",
        "show3dTrees",
        "show3dLandmarks",
        "show3dFacades",
      ];
      for (const feature of hideFeatures) {
        _map.setConfigProperty("basemap", feature, false);
      }

      _map.setConfigProperty("basemap", "colorTrunks", "rgba(0, 0, 0, 0)");

      _map.addSource("trace", {
        type: "geojson",
        data: {
          type: "Feature",
          properties: {},
          geometry: {
            type: "LineString",
            coordinates: lineCoordinates,
          },
        },
      });
      _map.addLayer({
        type: "line",
        source: "trace",
        id: "line",
        paint: {
          "line-color": "black",
          "line-width": 5,
        },
        layout: {
          "line-cap": "round",
          "line-join": "round",
        },
      });
    });

    _map.on("load", () => {
      continueRender(handle);
      setMap(_map);
    });
  }, [handle, lineCoordinates]);

  const style: React.CSSProperties = useMemo(
    () => ({ width, height, position: "absolute" }),
    [width, height],
  );

  return <AbsoluteFill ref={ref} style={style} />;
};
```

在 Remotion 中需要注意以下几点：

- 动画必须由 `useCurrentFrame()` 驱动，应禁用 Mapbox 自带的动画。例如，`fadeDuration` 应设为 `0`，`interactive` 应设为 `false` 等。
- 加载地图时应使用 `useDelayRender()` 延迟渲染，在地图加载完成前应将 map 设为 `null`。
- 承载 ref 的元素必须具有明确的 width、height，以及 `position: "absolute"`。
- 不要添加 `_map.remove();` 清理函数。

## 绘制线条

除非我明确要求，否则不要为线条添加发光效果。  
除非我明确要求，否则不要在线条上添加额外的点。

## 地图样式

默认使用 `mapbox://styles/mapbox/standard` 样式。  
隐藏底图样式中的标签。

除非我另有要求，否则从 Mapbox Standard 样式中移除所有要素。

```tsx
// Hide all features from the Mapbox Standard style
const hideFeatures = [
  "showRoadsAndTransit",
  "showRoads",
  "showTransit",
  "showPedestrianRoads",
  "showRoadLabels",
  "showTransitLabels",
  "showPlaceLabels",
  "showPointOfInterestLabels",
  "showPointsOfInterest",
  "showAdminBoundaries",
  "showLandmarkIcons",
  "showLandmarkIconLabels",
  "show3dObjects",
  "show3dBuildings",
  "show3dTrees",
  "show3dLandmarks",
  "show3dFacades",
];
for (const feature of hideFeatures) {
  _map.setConfigProperty("basemap", feature, false);
}

_map.setConfigProperty("basemap", "colorMotorways", "transparent");
_map.setConfigProperty("basemap", "colorRoads", "transparent");
_map.setConfigProperty("basemap", "colorTrunks", "transparent");
```

## 相机动画

可以通过添加 `useEffect` 钩子，根据当前帧更新相机位置，使相机沿线条移动。

除非我明确要求，否则不要在相机角度之间跳跃切换。

```tsx
import * as turf from "@turf/turf";
import { interpolate } from "remotion";
import { Easing } from "remotion";
import { useCurrentFrame, useVideoConfig, useDelayRender } from "remotion";

const animationDuration = 20;
const cameraAltitude = 4000;
```

```tsx
const frame = useCurrentFrame();
const { fps } = useVideoConfig();
const { delayRender, continueRender } = useDelayRender();

useEffect(() => {
  if (!map) {
    return;
  }
  const handle = delayRender("Moving point...");

  const routeDistance = turf.length(turf.lineString(lineCoordinates));

  const progress = interpolate(
    frame / fps,
    [0.00001, animationDuration],
    [0, 1],
    {
      easing: Easing.inOut(Easing.sin),
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const camera = map.getFreeCameraOptions();

  const alongRoute = turf.along(
    turf.lineString(lineCoordinates),
    routeDistance * progress,
  ).geometry.coordinates;

  camera.lookAtPoint({
    lng: alongRoute[0],
    lat: alongRoute[1],
  });

  map.setFreeCameraOptions(camera);
  map.once("idle", () => continueRender(handle));
}, [lineCoordinates, fps, frame, handle, map]);
```

说明：

重要：默认保持相机朝北（北方向上）。
重要：多步动画时，在每个阶段都要设置全部属性（缩放、位置、线条进度），以避免跳跃。覆盖初始值。

- 进度会钳制到最小值，避免线条为空导致 turf 报错
- 更多时间控制选项见 [Timing](./timing.md)。
- 考虑合成尺寸，确保线条足够粗、标签字号足够大，以便合成缩放后仍清晰可读。

## 线条动画

### 直线（线性插值）

若要让线条在地图上看起来是直的，请在坐标之间使用线性插值。不要使用 turf 的 `lineSliceAlong` 或 `along`，它们基于大地线（大圆）计算，在墨卡托投影上会呈现为曲线。

```tsx
const frame = useCurrentFrame();
const { durationInFrames } = useVideoConfig();

useEffect(() => {
  if (!map) return;

  const animationHandle = delayRender("Animating line...");

  const progress = interpolate(frame, [0, durationInFrames - 1], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });

  // Linear interpolation for a straight line on the map
  const start = lineCoordinates[0];
  const end = lineCoordinates[1];
  const currentLng = start[0] + (end[0] - start[0]) * progress;
  const currentLat = start[1] + (end[1] - start[1]) * progress;

  const lineData: GeoJSON.Feature<GeoJSON.LineString> = {
    type: "Feature",
    properties: {},
    geometry: {
      type: "LineString",
      coordinates: [start, [currentLng, currentLat]],
    },
  };

  const source = map.getSource("trace") as mapboxgl.GeoJSONSource;
  if (source) {
    source.setData(lineData);
  }

  map.once("idle", () => continueRender(animationHandle));
}, [frame, map, durationInFrames]);
```

### 曲线（大地线/大圆）

若要让线条沿两点间的大地线（大圆）路径动画，请使用 turf 的 `lineSliceAlong`。适用于展示航线或地球表面实际最短距离。

```tsx
import * as turf from "@turf/turf";

const routeLine = turf.lineString(lineCoordinates);
const routeDistance = turf.length(routeLine);

const currentDistance = Math.max(0.001, routeDistance * progress);
const slicedLine = turf.lineSliceAlong(routeLine, 0, currentDistance);

const source = map.getSource("route") as mapboxgl.GeoJSONSource;
if (source) {
  source.setData(slicedLine);
}
```

## 标记

在合适的位置添加标签和标记。

```tsx
_map.addSource("markers", {
  type: "geojson",
  data: {
    type: "FeatureCollection",
    features: [
      {
        type: "Feature",
        properties: { name: "Point 1" },
        geometry: { type: "Point", coordinates: [-118.2437, 34.0522] },
      },
    ],
  },
});

_map.addLayer({
  id: "city-markers",
  type: "circle",
  source: "markers",
  paint: {
    "circle-radius": 40,
    "circle-color": "#FF4444",
    "circle-stroke-width": 4,
    "circle-stroke-color": "#FFFFFF",
  },
});

_map.addLayer({
  id: "labels",
  type: "symbol",
  source: "markers",
  layout: {
    "text-field": ["get", "name"],
    "text-font": ["DIN Pro Bold", "Arial Unicode MS Bold"],
    "text-size": 50,
    "text-offset": [0, 0.5],
    "text-anchor": "top",
  },
  paint: {
    "text-color": "#FFFFFF",
    "text-halo-color": "#000000",
    "text-halo-width": 2,
  },
});
```

确保标记足够大。根据合成尺寸相应缩放标签。  
对于 1920x1080 的合成尺寸，标签字号至少应为 40px。

重要：保持 `text-offset` 足够小，使文字靠近标记。需考虑标记圆半径。圆半径为 40 时，以下偏移较为合适：

```tsx
"text-offset": [0, 0.5],
```

## 3D 建筑

要启用 3D 建筑，使用以下代码：

```tsx
_map.setConfigProperty("basemap", "show3dObjects", true);
_map.setConfigProperty("basemap", "show3dLandmarks", true);
_map.setConfigProperty("basemap", "show3dBuildings", true);
```

## 渲染

渲染地图动画时，请使用以下标志进行渲染：

```
npx remotion render --gl=angle --concurrency=1
```
