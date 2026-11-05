# 数学动画的视觉技巧

用于讲解数学概念的有效可视化模式。

## 核心原则

### 1. 渐进揭示（Progressive Disclosure）
不要一次展示全部内容。逐步增加复杂度。

**不好：** 立刻展示完整方程
**好：** 逐项构建方程，并解释每一部分

```
Scene flow:
1. Show simple case: f(x) = x²
2. Add complexity: f(x) = ax²
3. Full form: f(x) = ax² + bx + c
```

### 2. 变换而非替换
在可能的情况下，将对象变形为新形态，而不是淡出再淡入。

**不好：** FadeOut(equation1), FadeIn(equation2)
**好：** TransformMatchingTex(equation1, equation2)

这能保持视觉连贯性，并体现不同形式之间的关系。

### 3. 颜色承载含义
在整个视频中一致地用颜色编码含义。

**模式：**
- 输入/已知量：BLUE（蓝色）
- 输出/结果：GREEN（绿色）
- 正在讨论的关键项：YELLOW（黄色）高亮
- 错误/负向：RED（红色）
- 中性/辅助：WHITE/GREY（白/灰）

### 4. 空间关系
位置编码关系：
- 从左到右：变换、时间、因果
- 从上到下：层级、推导
- 中心：注意力焦点
- 边缘：上下文、参考

---

## 动画技巧

### 高亮与聚焦

**Indicate** — 短暂闪烁以吸引注意
```python
self.play(Indicate(term))
```

**Circumscribe** — 圈出重要元素
```python
self.play(Circumscribe(equation, color=YELLOW))
```

**FlashAround** — 在揭示时刻戏剧性地强调
```python
self.play(FlashAround(result))
```

### 方程操作

**Isolate terms** — 为特定部分上色或移动
```python
equation.set_color_by_tex("x", BLUE)
```

**Step-by-step derivation** — 展示每一步代数推导
```python
step1 = MathTex(r"2x + 4 = 10")
step2 = MathTex(r"2x = 6")
step3 = MathTex(r"x = 3")
# Transform between steps with alignment
```

**Substitution** — 展示数值代入变量
```python
# Animate the number moving into the variable's position
```

### 几何直觉

**Coordinate systems** — 始终标注坐标轴
```python
axes = Axes(x_range=[-3, 3], y_range=[-2, 2])
labels = axes.get_axis_labels(x_label="x", y_label="f(x)")
```

**Trace paths** — 展示点的运动轨迹
```python
trace = TracedPath(dot.get_center, stroke_color=YELLOW)
```

**Area visualization** — 用于积分、求和
```python
area = axes.get_area(graph, x_range=[a, b], color=BLUE, opacity=0.5)
```

### 3D 技巧

**Camera orbiting** — 展示三维结构
```python
self.play(frame.animate.reorient(60, 70), run_time=3)
```

**Projection** — 展示三维物体的二维投影
```python
# Helps connect 3D intuition to 2D formulas
```

**Slicing** — 切开三维物体
```python
# Show cross-sections to understand structure
```

---

## 常见视觉隐喻

### 向量即箭头
- 位置向量：从原点出发的箭头
- 加法：首尾相接
- 缩放：拉伸/收缩

### 函数即机器
- 输入从一侧进入
- 发生变换
- 输出从另一侧出来

### 矩阵即变换
- 展示网格被变换
- 跟踪基向量去向
- 强调行列式作为面积缩放因子

### 导数即斜率
- 切线接触曲线
- 放大以展示局部线性
- 随动点移动动画化斜率变化

### 积分即累积
- 用矩形的黎曼和
- 宽度 → 0 的动画
- 曲线下方面积填充

---

## 场景构图

### 黄金布局
```
┌─────────────────────────────────┐
│           TITLE/CONTEXT         │  (top edge)
├─────────────────────────────────┤
│                                 │
│      MAIN VISUALIZATION         │  (center, largest area)
│                                 │
├─────────────────────────────────┤
│    EQUATION / FORMULA           │  (bottom third)
└─────────────────────────────────┘
```

### 并排对比
```
┌───────────────┬───────────────┐
│   BEFORE /    │   AFTER /     │
│   CONCEPT A   │   CONCEPT B   │
└───────────────┴───────────────┘
```

### 放大细节
```
┌─────────────────────────────────┐
│  ┌─────┐                        │
│  │ZOOM │ ←── magnified detail   │
│  └─────┘                        │
│         Main context            │
└─────────────────────────────────┘
```

---

## 节奏与时间

| 动作 | 典型时长 |
|--------|------------------|
| 简单图形创建 | 0.5-1s |
| 文字/方程书写 | 1-2s |
| 变换 | 1-2s |
| 镜头运动 | 2-3s |
| 停顿供消化 | 0.5-1s |
| 复杂动画 | 2-4s |

### 节奏模式
快-快-慢-快-快-慢

铺垫用快速动画，关键洞察处放慢。

---

## 配色方案

### Classic 3b1b
- Background: #1C1C1C (dark grey)
- Primary: #58C4DD (blue)
- Secondary: #83C167 (green)
- Accent: #FFFF00 (yellow)
- Warning: #FF6666 (red)

### High Contrast
- Background: #000000
- Primary: #FFFFFF
- Accent: #FFD700

### Soft Academic
- Background: #2D2D2D
- Primary: #6ECFFF
- Secondary: #98E898
- Accent: #FFE66D
