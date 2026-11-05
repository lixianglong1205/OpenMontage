# D3.js 比例尺参考

涵盖所有 d3 比例尺类型的综合指南，含示例与用例。

## 连续比例尺

### 线性比例尺（Linear scale）

将连续输入域映射到连续输出范围，采用线性插值。

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

scale(50);  // Returns 250
scale(0);   // Returns 0
scale(100); // Returns 500

// Invert scale (get input from output)
scale.invert(250); // Returns 50
```

**用例：**
- 定量数据最常用的比例尺
- 坐标轴、柱长、位置编码
- 温度、价格、计数、测量值

**方法：**
- `.domain([min, max])` - 设置输入域
- `.range([min, max])` - 设置输出范围
- `.invert(value)` - 由范围值反查域值
- `.clamp(true)` - 将输出限制在范围边界内
- `.nice()` - 将域扩展到整齐的整数值

### 幂比例尺（Power scale）

将连续输入映射到连续输出，并施加指数变换。

```javascript
const sqrtScale = d3.scalePow()
  .exponent(0.5)  // Square root
  .domain([0, 100])
  .range([0, 500]);

const squareScale = d3.scalePow()
  .exponent(2)  // Square
  .domain([0, 100])
  .range([0, 500]);

// Shorthand for square root
const sqrtScale2 = d3.scaleSqrt()
  .domain([0, 100])
  .range([0, 500]);
```

**用例：**
- 感知缩放（人类感知是非线性的）
- 面积编码（用平方根将数值映射到圆半径）
- 强调小值或大值区间的差异

### 对数比例尺（Logarithmic scale）

将连续输入映射到连续输出，并施加对数变换。

```javascript
const logScale = d3.scaleLog()
  .domain([1, 1000])  // Must be positive
  .range([0, 500]);

logScale(1);    // Returns 0
logScale(10);   // Returns ~167
logScale(100);  // Returns ~333
logScale(1000); // Returns 500
```

**用例：**
- 跨多个数量级的数据
- 人口、GDP、财富分布
- 对数坐标轴
- 指数增长类可视化

**重要：** 域值必须严格为正（>0）。

### 时间比例尺（Time scale）

面向时间数据的专用线性比例尺。

```javascript
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)])
  .range([0, 800]);

timeScale(new Date(2022, 0, 1)); // Returns 400

// Invert to get date
timeScale.invert(400); // Returns Date object for mid-2022
```

**用例：**
- 时间序列可视化
- 时间线坐标轴
- 时间动画
- 基于日期的交互

**方法：**
- `.nice()` - 将域扩展到合适的时间间隔
- `.ticks(count)` - 生成间距合理的刻度值
- 适用所有线性比例尺方法

### 量化比例尺（Quantize scale）

将连续输入映射到离散的输出桶。

```javascript
const quantizeScale = d3.scaleQuantize()
  .domain([0, 100])
  .range(['low', 'medium', 'high']);

quantizeScale(25);  // Returns 'low'
quantizeScale(50);  // Returns 'medium'
quantizeScale(75);  // Returns 'high'

// Get the threshold values
quantizeScale.thresholds(); // Returns [33.33, 66.67]
```

**用例：**
- 连续数据分箱
- 热力图颜色
- 风险等级（低/中/高）
- 年龄组、收入档

### 分位数比例尺（Quantile scale）

根据分位数将连续输入映射到离散输出。

```javascript
const quantileScale = d3.scaleQuantile()
  .domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20, 24]) // Sample data
  .range(['low', 'medium', 'high']);

quantileScale(8);  // Returns based on quantile position
quantileScale.quantiles(); // Returns quantile thresholds
```

**用例：**
- 与分布无关的等规模分组
- 基于百分位的分类
- 处理偏态分布

### 阈值比例尺（Threshold scale）

按自定义阈值将连续输入映射到离散输出。

```javascript
const thresholdScale = d3.scaleThreshold()
  .domain([0, 10, 20])
  .range(['freezing', 'cold', 'warm', 'hot']);

thresholdScale(-5);  // Returns 'freezing'
thresholdScale(5);   // Returns 'cold'
thresholdScale(15);  // Returns 'warm'
thresholdScale(25);  // Returns 'hot'
```

**用例：**
- 自定义断点
- 等级边界（A、B、C、D、F）
- 温度类别
- 空气质量指数

## 顺序比例尺

### 顺序色标（Sequential colour scale）

将连续输入映射到连续颜色渐变。

```javascript
const colourScale = d3.scaleSequential(d3.interpolateBlues)
  .domain([0, 100]);

colourScale(0);   // Returns lightest blue
colourScale(50);  // Returns mid blue
colourScale(100); // Returns darkest blue
```

**可用插值器：**

**单色相：**
- `d3.interpolateBlues`, `d3.interpolateGreens`, `d3.interpolateReds`
- `d3.interpolateOranges`, `d3.interpolatePurples`, `d3.interpolateGreys`

**多色相：**
- `d3.interpolateViridis`, `d3.interpolateInferno`, `d3.interpolateMagma`
- `d3.interpolatePlasma`, `d3.interpolateWarm`, `d3.interpolateCool`
- `d3.interpolateCubehelixDefault`, `d3.interpolateTurbo`

**用例：**
- 热力图、等值区域图（choropleth）
- 连续数据可视化
- 温度、高程、密度

### 发散色标（Diverging colour scale）

将连续输入映射到以中点为界的发散颜色渐变。

```javascript
const divergingScale = d3.scaleDiverging(d3.interpolateRdBu)
  .domain([-10, 0, 10]);

divergingScale(-10); // Returns red
divergingScale(0);   // Returns white/neutral
divergingScale(10);  // Returns blue
```

**可用插值器：**
- `d3.interpolateRdBu` - 红到蓝
- `d3.interpolateRdYlBu` - 红、黄、蓝
- `d3.interpolateRdYlGn` - 红、黄、绿
- `d3.interpolatePiYG` - 粉、黄、绿
- `d3.interpolateBrBG` - 棕、蓝绿
- `d3.interpolatePRGn` - 紫、绿
- `d3.interpolatePuOr` - 紫、橙
- `d3.interpolateRdGy` - 红、灰
- `d3.interpolateSpectral` - 光谱彩虹

**用例：**
- 具有有意义中点（零、均值、中性）的数据
- 正负值
- 高于/低于对比
- 相关矩阵

### 顺序分位数比例尺（Sequential quantile scale）

将顺序颜色与分位数映射结合。

```javascript
const sequentialQuantileScale = d3.scaleSequentialQuantile(d3.interpolateBlues)
  .domain([3, 6, 7, 8, 8, 10, 13, 15, 16, 20, 24]);

// Maps based on quantile position
```

**用例：**
- 感知上均匀的分箱
- 处理离群值
- 偏态分布

## 序数比例尺

### 带状比例尺（Band scale）

将离散输入映射到连续带状区域（矩形），可选内边距。

```javascript
const bandScale = d3.scaleBand()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.1);

bandScale('A');           // Returns start position (e.g., 0)
bandScale('B');           // Returns start position (e.g., 110)
bandScale.bandwidth();    // Returns width of each band (e.g., 95)
bandScale.step();         // Returns total step including padding
bandScale.paddingInner(); // Returns inner padding (between bands)
bandScale.paddingOuter(); // Returns outer padding (at edges)
```

**用例：**
- 柱状图（最常见）
- 分组元素
- 分类坐标轴
- 热力图单元格

**内边距选项：**
- `.padding(value)` - 同时设置内外边距（0-1）
- `.paddingInner(value)` - 带与带之间的内边距（0-1）
- `.paddingOuter(value)` - 边缘外边距（0-1）
- `.align(value)` - 带的对齐方式（0-1，默认 0.5）

### 点比例尺（Point scale）

将离散输入映射到连续点位置（无宽度）。

```javascript
const pointScale = d3.scalePoint()
  .domain(['A', 'B', 'C', 'D'])
  .range([0, 400])
  .padding(0.5);

pointScale('A'); // Returns position (e.g., 50)
pointScale('B'); // Returns position (e.g., 150)
pointScale('C'); // Returns position (e.g., 250)
pointScale('D'); // Returns position (e.g., 350)
pointScale.step(); // Returns distance between points
```

**用例：**
- 折线图分类 x 轴
- 带分类轴的散点图
- 网络图中的节点位置
- 各类别的点位置布局

### 序数颜色比例尺（Ordinal colour scale）

将离散输入映射到离散输出（颜色、形状等）。

```javascript
const colourScale = d3.scaleOrdinal(d3.schemeCategory10);

colourScale('apples');  // Returns first colour
colourScale('oranges'); // Returns second colour
colourScale('apples');  // Returns same first colour (consistent)

// Custom range
const customScale = d3.scaleOrdinal()
  .domain(['cat1', 'cat2', 'cat3'])
  .range(['#FF6B6B', '#4ECDC4', '#45B7D1']);
```

**内置配色方案：**

**分类：**
- `d3.schemeCategory10` - 10 色
- `d3.schemeAccent` - 8 色
- `d3.schemeDark2` - 8 色
- `d3.schemePaired` - 12 色
- `d3.schemePastel1` - 9 色
- `d3.schemePastel2` - 8 色
- `d3.schemeSet1` - 9 色
- `d3.schemeSet2` - 8 色
- `d3.schemeSet3` - 12 色
- `d3.schemeTableau10` - 10 色

**用例：**
- 类别颜色
- 图例项
- 多系列图表
- 网络节点类型

## 比例尺工具

### 整齐域（Nice domain）

将域扩展到整齐的整数值。

```javascript
const scale = d3.scaleLinear()
  .domain([0.201, 0.996])
  .nice();

scale.domain(); // Returns [0.2, 1.0]

// With count (approximate tick count)
const scale2 = d3.scaleLinear()
  .domain([0.201, 0.996])
  .nice(5);
```

### 钳制（Clamping）

将输出限制在范围边界内。

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500])
  .clamp(true);

scale(-10); // Returns 0 (clamped)
scale(150); // Returns 500 (clamped)
```

### 复制比例尺（Copy scales）

创建相互独立的副本。

```javascript
const scale1 = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

const scale2 = scale1.copy();
// scale2 is independent of scale1
```

### 刻度生成（Tick generation）

为坐标轴生成合适的刻度值。

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range([0, 500]);

scale.ticks(10);        // Generate ~10 ticks
scale.tickFormat(10);   // Get format function for ticks
scale.tickFormat(10, ".2f"); // Custom format (2 decimal places)

// Time scale ticks
const timeScale = d3.scaleTime()
  .domain([new Date(2020, 0, 1), new Date(2024, 0, 1)]);

timeScale.ticks(d3.timeYear);      // Yearly ticks
timeScale.ticks(d3.timeMonth, 3);  // Every 3 months
timeScale.tickFormat(5, "%Y-%m");  // Format as year-month
```

## 色彩空间与插值

### RGB 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"]);
// Default: RGB interpolation
```

### HSL 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateHsl);
// Smoother colour transitions
```

### Lab 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateLab);
// Perceptually uniform
```

### HCL 插值

```javascript
const scale = d3.scaleLinear()
  .domain([0, 100])
  .range(["blue", "red"])
  .interpolate(d3.interpolateHcl);
// Perceptually uniform with hue
```

## 常见模式

### 自定义中点的发散比例尺

```javascript
const scale = d3.scaleLinear()
  .domain([min, midpoint, max])
  .range(["red", "white", "blue"])
  .interpolate(d3.interpolateHcl);
```

### 多停靠点渐变比例尺

```javascript
const scale = d3.scaleLinear()
  .domain([0, 25, 50, 75, 100])
  .range(["#d53e4f", "#fc8d59", "#fee08b", "#e6f598", "#66c2a5"]);
```

### 圆的半径比例尺（感知一致）

```javascript
const radiusScale = d3.scaleSqrt()
  .domain([0, d3.max(data, d => d.value)])
  .range([0, 50]);

// Use with circles
circle.attr("r", d => radiusScale(d.value));
```

### 按数据范围自适应的比例尺

```javascript
function createAdaptiveScale(data) {
  const extent = d3.extent(data);
  const range = extent[1] - extent[0];
  
  // Use log scale if data spans >2 orders of magnitude
  if (extent[1] / extent[0] > 100) {
    return d3.scaleLog()
      .domain(extent)
      .range([0, width]);
  }
  
  // Otherwise use linear
  return d3.scaleLinear()
    .domain(extent)
    .range([0, width]);
}
```

### 显式类别的颜色比例尺

```javascript
const colourScale = d3.scaleOrdinal()
  .domain(['Low Risk', 'Medium Risk', 'High Risk'])
  .range(['#2ecc71', '#f39c12', '#e74c3c'])
  .unknown('#95a5a6'); // Fallback for unknown values
```
