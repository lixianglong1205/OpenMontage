# D3.js 配色方案与调色板推荐

在 d3.js 数据可视化中选用颜色的全面指南。

## 内置分类配色方案

### Category10（默认）

```javascript
d3.schemeCategory10
// ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',
//  '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
```

**特点：**
- 10 种可区分的颜色
- 对色觉障碍者较友好
- 多数分类数据的默认选择
- 饱和度与亮度均衡

**适用场景：** 通用分类编码、图例项、多条数据系列

### Tableau10

```javascript
d3.schemeTableau10
```

**特点：**
- 10 种为数据可视化优化的颜色
- 专业外观
- 区分度出色

**适用场景：** 商业仪表盘、专业报告、演示文稿

### Accent

```javascript
d3.schemeAccent
// 8 colours with high saturation
```

**特点：**
- 明亮、鲜艳的颜色
- 高对比度
- 现代审美

**适用场景：** 突出重要类别、现代 Web 应用

### Dark2

```javascript
d3.schemeDark2
// 8 darker, muted colours
```

**特点：**
- 低调柔和的调色板
- 专业外观
- 适合深色背景

**适用场景：** 深色模式可视化、专业场景

### Paired

```javascript
d3.schemePaired
// 12 colours in pairs of similar hues
```

**特点：**
- 相近色相的明暗成对颜色
- 适用于嵌套类别
- 12 种可区分颜色

**适用场景：** 分组条形图、层次类别、前后对比

### Pastel1 与 Pastel2

```javascript
d3.schemePastel1 // 9 colours
d3.schemePastel2 // 8 colours
```

**特点：**
- 柔和、低饱和度颜色
- 观感温和
- 适合大面积填充

**适用场景：** 背景色、低调分类、舒缓型可视化

### Set1、Set2、Set3

```javascript
d3.schemeSet1 // 9 colours - vivid
d3.schemeSet2 // 8 colours - muted
d3.schemeSet3 // 12 colours - pastel
```

**特点：**
- Set1：高饱和度，区分度最大
- Set2：专业、均衡
- Set3：柔和低调，适合较多类别

**适用场景：** 根据视觉层次需求而定

## 顺序配色方案

顺序方案用单一色相或渐变将连续数据从低值映射到高值。

### 单色相顺序

**Blues：**
```javascript
d3.interpolateBlues
d3.schemeBlues[9] // 9-step discrete version
```

**其他单色相选项：**
- `d3.interpolateGreens` / `d3.schemeGreens`
- `d3.interpolateOranges` / `d3.schemeOranges`
- `d3.interpolatePurples` / `d3.schemePurples`
- `d3.interpolateReds` / `d3.schemeReds`
- `d3.interpolateGreys` / `d3.schemeGreys`

**适用场景：**
- 简单热力图
- 等值区域图（choropleth）
- 密度图
- 单一指标可视化

### 多色相顺序

**Viridis（推荐）：**
```javascript
d3.interpolateViridis
```

**特点：**
- 感知均匀（perceptually uniform）
- 色觉障碍友好
- 适合印刷
- 无视觉“死区”
- 感知亮度单调递增

**其他感知均匀选项：**
- `d3.interpolatePlasma` - 紫到黄
- `d3.interpolateInferno` - 经红/橙由黑到白
- `d3.interpolateMagma` - 经紫由黑到白
- `d3.interpolateCividis` - 针对色觉障碍优化

**色觉障碍友好：**
```javascript
d3.interpolateTurbo // Rainbow-like but perceptually uniform
d3.interpolateCool  // Cyan to magenta
d3.interpolateWarm  // Orange to yellow
```

**适用场景：**
- 科学可视化
- 医学成像
- 任意高精度数据可视化
- 无障碍可视化

### 传统顺序方案

**黄-橙-红：**
```javascript
d3.interpolateYlOrRd
d3.schemeYlOrRd[9]
```

**黄-绿-蓝：**
```javascript
d3.interpolateYlGnBu
d3.schemeYlGnBu[9]
```

**其他多色相：**
- `d3.interpolateBuGn` - 蓝到绿
- `d3.interpolateBuPu` - 蓝到紫
- `d3.interpolateGnBu` - 绿到蓝
- `d3.interpolateOrRd` - 橙到红
- `d3.interpolatePuBu` - 紫到蓝
- `d3.interpolatePuBuGn` - 紫到蓝绿
- `d3.interpolatePuRd` - 紫到红
- `d3.interpolateRdPu` - 红到紫
- `d3.interpolateYlGn` - 黄到绿
- `d3.interpolateYlOrBr` - 黄到橙褐

**适用场景：** 传统数据可视化、熟悉的颜色联想（温度、植被、水）

## 发散配色方案

发散方案用两种不同色相突出相对中心值的偏离。

### 红-蓝（温度）

```javascript
d3.interpolateRdBu
d3.schemeRdBu[11]
```

**特点：**
- 直观的温度隐喻
- 强对比
- 正负区分清晰

**适用场景：** 温度、盈亏、高于/低于平均、相关性

### 红-黄-蓝

```javascript
d3.interpolateRdYlBu
d3.schemeRdYlBu[11]
```

**特点：**
- 三色渐变
- 经黄色过渡更柔和
- 更多视觉层级

**适用场景：** 需强调极值且中间值也需可见时

### 其他发散方案

**交通灯：**
```javascript
d3.interpolateRdYlGn // Red (bad) to green (good)
```

**Spectral（彩虹）：**
```javascript
d3.interpolateSpectral // Full spectrum
```

**其他选项：**
- `d3.interpolateBrBG` - 褐到蓝绿
- `d3.interpolatePiYG` - 粉到黄绿
- `d3.interpolatePRGn` - 紫到绿
- `d3.interpolatePuOr` - 紫到橙
- `d3.interpolateRdGy` - 红到灰

**适用场景：** 按语义含义与无障碍需求选择

## 色觉障碍友好调色板

### 通用准则

1. **避免红绿组合**（最常见的色觉障碍类型）
2. **发散图用蓝-橙** 代替红-绿
3. **增加纹理或图案** 作为冗余编码
4. **用模拟工具测试**

### 推荐的色觉安全方案

**分类：**
```javascript
// Okabe-Ito palette (colour-blind safe)
const okabePalette = [
  '#E69F00', // Orange
  '#56B4E9', // Sky blue
  '#009E73', // Bluish green
  '#F0E442', // Yellow
  '#0072B2', // Blue
  '#D55E00', // Vermillion
  '#CC79A7', // Reddish purple
  '#000000'  // Black
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(okabePalette);
```

**顺序：**
```javascript
// Use Viridis, Cividis, or Blues
d3.interpolateViridis  // Best overall
d3.interpolateCividis  // Optimised for CVD
d3.interpolateBlues    // Simple, safe
```

**发散：**
```javascript
// Use blue-orange instead of red-green
d3.interpolateBrBG
d3.interpolatePuOr
```

## 自定义调色板

### 创建自定义顺序比例尺

```javascript
const customSequential = d3.scaleLinear()
  .domain([0, 100])
  .range(['#e8f4f8', '#006d9c']) // Light to dark blue
  .interpolate(d3.interpolateLab); // Perceptually uniform
```

### 创建自定义发散比例尺

```javascript
const customDiverging = d3.scaleLinear()
  .domain([0, 50, 100])
  .range(['#ca0020', '#f7f7f7', '#0571b0']) // Red, grey, blue
  .interpolate(d3.interpolateLab);
```

### 创建自定义分类比例尺

```javascript
// Brand colours
const brandPalette = [
  '#FF6B6B', // Primary red
  '#4ECDC4', // Secondary teal
  '#45B7D1', // Tertiary blue
  '#FFA07A', // Accent coral
  '#98D8C8'  // Accent mint
];

const colourScale = d3.scaleOrdinal()
  .domain(categories)
  .range(brandPalette);
```

## 语义颜色联想

### 普遍颜色含义

**Red：**
- 危险、错误、负面
- 高温
- 债务、亏损

**Green：**
- 成功、正面
- 增长、植被
- 盈利、收益

**Blue：**
- 信任、平静
- 水、冷
- 信息、中性

**Yellow/Orange：**
- 警告、谨慎
- 能量、温暖
- 注意力

**Grey：**
- 中性、非活跃
- 缺失数据
- 背景

### 场景专用调色板

**金融：**
```javascript
const financialColours = {
  profit: '#27ae60',
  loss: '#e74c3c',
  neutral: '#95a5a6',
  highlight: '#3498db'
};
```

**Temperature：**
```javascript
const temperatureScale = d3.scaleSequential(d3.interpolateRdYlBu)
  .domain([40, -10]); // Hot to cold (reversed)
```

**Traffic/Status：**
```javascript
const statusColours = {
  success: '#27ae60',
  warning: '#f39c12',
  error: '#e74c3c',
  info: '#3498db',
  neutral: '#95a5a6'
};
```

## 无障碍最佳实践

### 对比度

确保颜色与背景之间有足够对比：

```javascript
// Good contrast example
const highContrast = {
  background: '#ffffff',
  text: '#2c3e50',
  primary: '#3498db',
  secondary: '#e74c3c'
};
```

**WCAG 指南：**
- 正文：至少 4.5:1
- 大号文字：至少 3:1
- UI 组件：至少 3:1

### 冗余编码

不要仅依赖颜色传递信息：

```javascript
// Add patterns or shapes
const symbols = ['circle', 'square', 'triangle', 'diamond'];

// Add text labels
// Use line styles (solid, dashed, dotted)
// Use size encoding
```

### 测试

针对色觉障碍测试可视化：
- Chrome DevTools（Rendering > Emulate vision deficiencies）
- Colour Oracle（免费桌面应用）
- Coblis（在线模拟器）

## 专业配色推荐

### 数据新闻

```javascript
// Guardian style
const guardianPalette = [
  '#005689', // Guardian blue
  '#c70000', // Guardian red
  '#7d0068', // Guardian pink
  '#951c75', // Guardian purple
];

// FT style
const ftPalette = [
  '#0f5499', // FT blue
  '#990f3d', // FT red
  '#593380', // FT purple
  '#262a33', // FT black
];
```

### 学术/科学

```javascript
// Nature journal style
const naturePalette = [
  '#0071b2', // Blue
  '#d55e00', // Vermillion
  '#009e73', // Green
  '#f0e442', // Yellow
];

// Use Viridis for continuous data
const scientificScale = d3.scaleSequential(d3.interpolateViridis);
```

### 企业/商业

```javascript
// Professional, conservative
const corporatePalette = [
  '#003f5c', // Dark blue
  '#58508d', // Purple
  '#bc5090', // Magenta
  '#ff6361', // Coral
  '#ffa600'  // Orange
];
```

## 动态颜色选择

### 基于数据范围

```javascript
function selectColourScheme(data) {
  const extent = d3.extent(data);
  const hasNegative = extent[0] < 0;
  const hasPositive = extent[1] > 0;
  
  if (hasNegative && hasPositive) {
    // Diverging: data crosses zero
    return d3.scaleSequentialSymlog(d3.interpolateRdBu)
      .domain([extent[0], 0, extent[1]]);
  } else {
    // Sequential: all positive or all negative
    return d3.scaleSequential(d3.interpolateViridis)
      .domain(extent);
  }
}
```

### 基于类别数量

```javascript
function selectCategoricalScheme(categories) {
  const n = categories.length;
  
  if (n <= 10) {
    return d3.scaleOrdinal(d3.schemeTableau10);
  } else if (n <= 12) {
    return d3.scaleOrdinal(d3.schemePaired);
  } else {
    // For many categories, use sequential with quantize
    return d3.scaleQuantize()
      .domain([0, n - 1])
      .range(d3.quantize(d3.interpolateRainbow, n));
  }
}
```

## 常见配色错误

1. **顺序数据用彩虹渐变**
   - 问题：感知不均匀，难以阅读
   - 解决：使用 Viridis、Blues 或其他均匀方案

2. **发散图用红-绿（色觉障碍）**
   - 问题：约 8% 男性无法区分
   - 解决：使用蓝-橙或紫-绿

3. **分类颜色过多**
   - 问题：难以区分和记忆
   - 解决：限制在 5–8 类，采用分组

4. **对比度不足**
   - 问题：可读性差
   - 解决：测试对比度，浅色背景上用更深颜色

5. **文化语义不一致**
   - 问题：语义含义混淆
   - 解决：研究目标受众的颜色联想

6. **温度比例尺颠倒**
   - 问题：违反直觉（红 = 冷）
   - 解决：红/橙 = 热，蓝 = 冷

## 快速参考

**需要展示…**

- **类别（≤10）：** `d3.schemeCategory10` 或 `d3.schemeTableau10`
- **类别（>10）：** `d3.schemePaired` 或对类别分组
- **顺序（通用）：** `d3.interpolateViridis`
- **顺序（科学）：** `d3.interpolateViridis` 或 `d3.interpolatePlasma`
- **顺序（温度）：** `d3.interpolateRdYlBu`（反转）
- **发散（以零为中心）：** `d3.interpolateRdBu` 或 `d3.interpolateBrBG`
- **发散（好/坏）：** `d3.interpolateRdYlGn`（反转）
- **色觉安全（分类）：** Okabe-Ito 调色板（见上文）
- **色觉安全（顺序）：** `d3.interpolateCividis` 或 `d3.interpolateBlues`
- **色觉安全（发散）：** `d3.interpolatePuOr` 或 `d3.interpolateBrBG`

**务必记住：**
1. 做色觉障碍测试
2. 保证足够对比度
3. 恰当使用语义颜色
4. 增加冗余编码（图案、标签）
5. 保持简洁（颜色越少，可视化越清晰）
