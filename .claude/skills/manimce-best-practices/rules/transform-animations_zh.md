---
name: transform-animations
description: Transform、ReplacementTransform 与形变动画
metadata:
  tags: transform, replacementtransform, morph, transformfromcopy
---

# 形变动画（Transform Animations）

将一种 mobject 形变为另一种的动画。

## Transform

将源 mobject 形变为目标的形状。源 mobject 会被修改。

```python
class TransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()

        self.play(Create(square))
        self.play(Transform(square, circle))
        # Note: 'square' now looks like 'circle' but is still 'square'
```

**重要：** Transform 之后，原变量仍指向该 mobject，尽管外观上已与目标一致。

## ReplacementTransform

将源形变为目标，并替换引用。对大多数用法更直观。

```python
class ReplacementTransformExample(Scene):
    def construct(self):
        square = Square()
        circle = Circle()
        triangle = Triangle()

        self.play(Create(square))
        self.play(ReplacementTransform(square, circle))
        # 'square' is removed, 'circle' is now in the scene
        self.play(ReplacementTransform(circle, triangle))
        # 'circle' is removed, 'triangle' is now in the scene
```

## Transform 与 ReplacementTransform 对比

```python
# Transform - source variable changes appearance
self.play(Transform(A, B))
# A is still in scene (but looks like B)
# B is NOT in scene

# ReplacementTransform - source is replaced by target
self.play(ReplacementTransform(A, B))
# A is removed from scene
# B is now in scene
```

## TransformFromCopy

复制源对象并将其形变为目标。原对象保持不变。

```python
class TransformFromCopyExample(Scene):
    def construct(self):
        square = Square().shift(LEFT * 2)
        circle = Circle().shift(RIGHT * 2)

        self.add(square)
        self.play(TransformFromCopy(square, circle))
        # Both square and circle are now visible
```

## TransformMatchingShapes

智能匹配对应部分并进行形变。

```python
class MatchingShapesExample(Scene):
    def construct(self):
        source = Text("ABC")
        target = Text("ABCD")

        self.play(Write(source))
        self.play(TransformMatchingShapes(source, target))
```

## TransformMatchingTex

按 TeX 字符串匹配 LaTeX 各部分。

```python
class MatchingTexExample(Scene):
    def construct(self):
        eq1 = MathTex("a", "^2", "+", "b", "^2")
        eq2 = MathTex("a", "^2", "+", "2ab", "+", "b", "^2")

        self.play(Write(eq1))
        self.play(TransformMatchingTex(eq1, eq2))
```

## MoveToTarget

预先设定目标状态并动画过渡到该状态。

```python
class MoveToTargetExample(Scene):
    def construct(self):
        square = Square()
        self.add(square)

        # Generate and modify target
        square.generate_target()
        square.target.shift(RIGHT * 2)
        square.target.set_color(RED)
        square.target.scale(2)

        self.play(MoveToTarget(square))
```

## 路径弧形形变（Path Arc Transforms）

使用 `path_arc` 控制形变路径。

```python
class PathArcExample(Scene):
    def construct(self):
        dot1 = Dot(LEFT * 2)
        dot2 = Dot(RIGHT * 2)

        self.add(dot1)
        # Transform along an arc
        self.play(Transform(dot1, dot2, path_arc=PI/2))
```

## 链式形变（Chained Transformations）

```python
class ChainedExample(Scene):
    def construct(self):
        shape = Square()
        self.play(Create(shape))

        # Chain of transformations
        for target in [Circle(), Triangle(), Star()]:
            self.play(Transform(shape, target))
            self.wait(0.5)
```

## 最佳实践

1. **为清晰起见使用 ReplacementTransform** — 变量行为更直观
2. **需要保留原对象时使用 TransformFromCopy** — 当两者都需可见时
3. **公式使用 TransformMatchingTex** — 更好对齐匹配部分
4. **设置 path_arc 增强视觉效果** — 曲线路径更有动感
