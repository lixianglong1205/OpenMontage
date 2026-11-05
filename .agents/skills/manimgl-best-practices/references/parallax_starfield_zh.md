# 视差星场 - 参考指南

**示例文件**：`examples/parallax_starfield.py`

## 用户查询场景

本示例适用于如下类型的需求：
- “用星星演示视差是如何工作的”
- “创建一个展示深度知觉的 3D 场景”
- “动画演示观察者穿过星场”
- “用可视化方式解释恒星视差”
- “说明为什么移动时近处物体比远处移动得更多”

## 场景构思过程（3b1b 风格）

### 1. 明确核心概念
**视差（Parallax）**：当观察者移动时，近处物体相对背景产生的视位移比远处物体更明显。天文学家正是用这一原理测量附近恒星的距离。

### 2. 视觉设计决策

**为什么用星星/点而不是复杂物体？**
- 星星天然分布在不同距离上
- 点状元素计算高效（`GlowDots` 可轻松处理 200+ 个点）
- 效果清晰，不会被物体形状分散注意力

**为什么放一个参考立方体？**
- 在 3D 中提供空间语境
- 帮助观众理解星星所在的体积范围
- 线框不会遮挡星星

**为什么用 Pi 角色作为观察者？**
- 让场景更易共情——你在看某人如何观察
- 其移动方式直观易懂
- 可用 `observer.change("pondering")` 表现反应

### 3. 技术实现

#### 用 GlowDots 高效渲染星星
```python
# Random 3D positions
star_positions = np.random.uniform(-1, 1, (n_stars, 3))
stars = GlowDots(star_positions)
stars.set_glow_factor(2)  # Soft bloom effect
stars.set_radii(np.random.uniform(0, 0.075, n_stars))  # Varying sizes
```

**要点**：`GlowDots` 远比逐个创建 `Dot` 对象高效。对于 200+ 个点，这是必选项。

#### 3D 相机控制
```python
frame = self.frame
self.set_floor_plane("xz")  # Z is now vertical

# Smooth camera reorientation
self.play(frame.animate.reorient(-40, -26, 0), run_time=2)
```

**为何使用 `set_floor_plane("xz")`？** 在天文类可视化中，常希望 Z 轴为竖直方向。该调用会重新配置坐标系。

#### 观察者移动模式
```python
for dy in [1.5, -3, 3, -3, 1.5]:
    self.play(observer.animate.shift(dy * IN), run_time=3)
```

**为何采用这一具体模式？**
- `[1.5, -3, 3, -3, 1.5]` 形成：上 → 下 → 上 → 下 → 回中
- 观众能看到视差位移的完整范围
- 回到起始位置，便于需要时做干净循环

### 4. 场景变体

示例包含三个变体，展示逐步增加的复杂度：

| 场景 | 用途 | 适用时机 |
|-------|---------|-------------|
| `ParallaxStarfield` | 基础效果，第三人称视角 | 一般性讲解 |
| `ParallaxFromObserverPOV` | 第一人称视角 | “你会看到什么？” |
| `LayeredParallax` | 显式距离分层 | 清晰讲授概念 |

## 展示的关键模式

### 模式：相机跟随物体
```python
frame.always.match_z(observer)
```
相机的 Z 坐标持续与观察者对齐，形成第一人称视角。

### 模式：分层深度以增强清晰度
```python
colors = [RED, YELLOW, BLUE]
distances = [2, 5, 10]
```
在特定距离上使用不同颜色，使视差效果在教学上一目了然。

### 模式：平滑横向移动
```python
self.play(
    observer.animate.shift(dx * RIGHT),
    run_time=3,
    rate_func=smooth
)
```
缓慢、平滑的移动让观众能追踪单颗星星并观察效果。

## 常见修改

### 增加星星数量
```python
n_stars = 500  # Increase count
stars.set_radii(np.random.uniform(0, 0.05, n_stars))  # Smaller radii for density
```

### 不同的星星颜色
```python
# Temperature-based star colors
colors = [RED, ORANGE, YELLOW, WHITE, BLUE_A]
for i, star in enumerate(stars):
    star.set_color(random.choice(colors))
```

### 添加背景星系
```python
background = ImageMobject("milky_way.png")
background.set_height(20)
background.shift(50 * OUT)  # Far behind stars
self.add(background)
```

## 输出

渲染后将得到：
- 蓝色线框立方体内的 3D 星场
- 上下移动的观察者（Randolph）
- 星星随距离不同而呈现不同的视位移
- 对视差原理的清晰演示

## 运行命令

```bash
# Full render
manimgl parallax_starfield.py ParallaxStarfield -w

# Preview (no file output)
manimgl parallax_starfield.py ParallaxStarfield -p

# All three scenes
manimgl parallax_starfield.py ParallaxStarfield ParallaxFromObserverPOV LayeredParallax -w
```
