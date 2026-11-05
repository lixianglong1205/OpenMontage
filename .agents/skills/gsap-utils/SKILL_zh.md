---
name: gsap-utils
description: GSAP 官方技能：gsap.utils — clamp、mapRange、normalize、interpolate、random、snap、toArray、wrap、pipe。在用户询问 gsap.utils、clamp、mapRange、random、snap、toArray、wrap 或 GSAP 辅助工具时使用。
license: MIT
---

# gsap.utils

## 何时使用本技能

在编写或审查使用 **gsap.utils** 处理数学运算、数组/集合、单位解析或动画中的值映射的代码时应用（例如将滚动映射为数值、随机化、对齐网格或归一化输入）。

**相关技能：** 构建动画时与 **gsap-core**、**gsap-timeline**、**gsap-scrolltrigger** 配合使用；CustomEase 及其他缓动工具见 **gsap-plugins**。

## 概述

**gsap.utils** 提供纯函数辅助方法，无需注册。可用于补间变量（如基于函数的值）、ScrollTrigger 或 Observer 回调，或任何驱动 GSAP 的 JS 中。均挂载在 **gsap.utils** 上（例如 `gsap.utils.clamp()`）。

**省略 value：函数形式。** 许多 util 将被变换的值作为**最后一个**参数。若省略该参数，util 会返回一个**函数**，稍后再传入值。当需要用同一配置对大量值进行 clamp、map、normalize 或 snap 时（例如在 mousemove 处理器或补间回调中），使用函数形式。**例外：random()** — 将 **true** 作为最后一个参数以得到可复用函数（不要省略 value）；见 [random()](https://gsap.com/docs/v3/GSAP/UtilityMethods/random())。

```javascript
// With value: returns the result
gsap.utils.clamp(0, 100, 150); // 100

// Without value: returns a function you call with the value later
let c = gsap.utils.clamp(0, 100);
c(150);  // 100
c(-10);  // 0
```

## 钳制与范围

### clamp(min, max, value?)

将值限制在 min 与 max 之间。省略 **value** 可得到函数：`clamp(min, max)(value)`。

```javascript
gsap.utils.clamp(0, 100, 150); // 100
gsap.utils.clamp(0, 100, -10); // 0

let clampFn = gsap.utils.clamp(0, 100);
clampFn(150); // 100
```

### mapRange(inMin, inMax, outMin, outMax, value?)

将值从一个范围映射到另一个范围。在将滚动位置、进度（0–1）或输入范围转换为动画范围时使用。省略 **value** 可得到函数：`mapRange(inMin, inMax, outMin, outMax)(value)`。

```javascript
gsap.utils.mapRange(0, 100, 0, 500, 50);  // 250
gsap.utils.mapRange(0, 1, 0, 360, 0.5);   // 180 (progress to degrees)

let mapFn = gsap.utils.mapRange(0, 100, 0, 500);
mapFn(50);  // 250
```

### normalize(min, max, value?)

返回在给定范围内归一化到 0–1 的值。当目标范围为 0–1 时，与映射互为逆操作。省略 **value** 可得到函数：`normalize(min, max)(value)`。

```javascript
gsap.utils.normalize(0, 100, 50);   // 0.5
gsap.utils.normalize(100, 300, 200); // 0.5

let normFn = gsap.utils.normalize(0, 100);
normFn(50); // 0.5
```

### interpolate(start, end, progress?)

在给定进度（0–1）下在两个值之间插值。支持数字、颜色及键名匹配的对象。省略 **progress** 可得到函数：`interpolate(start, end)(progress)`。

```javascript
gsap.utils.interpolate(0, 100, 0.5);       // 50
gsap.utils.interpolate("#ff0000", "#0000ff", 0.5); // mid color
gsap.utils.interpolate({ x: 0, y: 0 }, { x: 100, y: 50 }, 0.5); // { x: 50, y: 25 }

let lerp = gsap.utils.interpolate(0, 100);
lerp(0.5); // 50
```

## 随机与对齐

### random(minimum, maximum[, snapIncrement, returnFunction]) / random(array[, returnFunction])

返回 **minimum**–**maximum** 范围内的随机数，或从 **array** 中随机取一个元素。可选 **snapIncrement** 将结果对齐到最近倍数（例如 `5` → 5 的倍数）。**要得到可复用函数**，将 **true** 作为最后一个参数（**returnFunction**）；返回的函数无参，每次调用得到新的随机值。这是唯一用 `true` 表示函数形式、而非省略 value 的 util。

```javascript
// immediate value: number in range
gsap.utils.random(-100, 100);        // e.g. 42.7
gsap.utils.random(0, 500, 5);        // 0–500, snapped to nearest 5

// reusable function: pass true as last argument
let randomFn = gsap.utils.random(-200, 500, 10, true);
randomFn();  // random value in range, snapped to 10
randomFn();  // another random value

// array: pick one value at random
gsap.utils.random(["red", "blue", "green"]);  // "red", "blue", or "green"
let randomFromArray = gsap.utils.random([0, 100, 200], true);
randomFromArray();  // 0, 100, or 200
```

**补间变量中的字符串形式：** 使用 `"random(-100, 100)"`、`"random(-100, 100, 5)"` 或 `"random([0, 100, 200])"`；GSAP 按目标分别求值。

```javascript
gsap.to(".box", { x: "random(-100, 100, 5)", duration: 1 });
gsap.to(".item", { backgroundColor: "random([red, blue, green])" });
```

### snap(snapTo, value?)

将值对齐到 **snapTo** 的最近倍数，或对齐到允许值数组中的最近值。省略 **value** 可得到函数：`snap(snapTo)(value)`（或 `snap(snapArray)(value)`）。

```javascript
gsap.utils.snap(10, 23);     // 20
gsap.utils.snap(0.25, 0.7);  // 0.75
gsap.utils.snap([0, 100, 200], 150); // 100 or 200 (nearest in array)

let snapFn = gsap.utils.snap(10);
snapFn(23); // 20
```

在补间中用于网格或步进式动画：

```javascript
gsap.to(".x", { x: 200, snap: { x: 20 } });
```

### shuffle(array)

返回元素相同但顺序随机的新数组。用于随机化顺序（例如配合副本使用 stagger 的 `"random"`）。

```javascript
gsap.utils.shuffle([1, 2, 3, 4]); // e.g. [3, 1, 4, 2]
```

### distribute(config)

**返回一个函数**，根据目标在数组（或网格）中的位置为其分配值。内部用于高级 stagger；当需要在多个元素间分布值（如 scale、opacity、x、delay）时使用。返回的函数接收 `(index, target, targets)` — 可手动调用，或将结果直接传入补间；GSAP 会按目标用 index、元素和数组调用它。

**配置（均可选）：**

| 属性 | 类型 | 说明 |
|----------|------|-------------|
| `base` | Number | 起始值。默认 `0`。 |
| `amount` | Number | 在所有目标间分配的总增量（加在 base 上）。例如 100 个目标 `amount: 1` → 相邻差 0.01。要用固定步长时用 **each**。 |
| `each` | Number | 相邻目标间的增量（加在 base 上）。例如 4 个目标 `each: 1` → 0, 1, 2, 3。要分配总量时用 **amount**。 |
| `from` | Number \| String \| Array | 分布起点：索引，或 `"start"`、`"center"`、`"edges"`、`"random"`、`"end"`，或比例如 `[0.25, 0.75]`。默认 `0`。 |
| `grid` | String \| Array | 用网格位置代替扁平索引：`[rows, columns]`（如 `[5, 10]`）或 `"auto"` 自动检测。扁平数组可省略。 |
| `axis` | String | 网格时限制单轴（`"x"` 或 `"y"`）。 |
| `ease` | Ease | 沿缓动曲线分布值（如 `"power1.inOut"`）。默认 `"none"`。 |

**在补间中：** 将 `distribute(config)` 的结果作为属性值；GSAP 对每个目标用 `(index, target, targets)` 调用该函数。

```javascript
// Scale: middle elements 0.5, outer edges 3 (amount 2.5 distributed from center)
gsap.to(".class", {
  scale: gsap.utils.distribute({
    base: 0.5,
    amount: 2.5,
    from: "center"
  })
});
```

**手动使用：** 用 `(index, target, targets)` 调用返回的函数，得到该索引对应的值。

```javascript
const distributor = gsap.utils.distribute({
  base: 50,
  amount: 100,
  from: "center",
  ease: "power1.inOut"
});
const targets = gsap.utils.toArray(".box");
const valueForIndex2 = distributor(2, targets[2], targets);
```

更多见 [distribute()](https://gsap.com/docs/v3/GSAP/UtilityMethods/distribute/)。

## 单位与解析

### getUnit(value)

返回值的单位字符串（如 `"px"`、`"%"`、`"deg"`）。在归一化或转换值时使用。

```javascript
gsap.utils.getUnit("100px");   // "px"
gsap.utils.getUnit("50%");     // "%"
gsap.utils.getUnit(42);        // "" (unitless)
```

### unitize(value, unit)

给数字附加单位；若已有单位则原样返回。在构建 CSS 值或补间结束值时使用。

```javascript
gsap.utils.unitize(100, "px");  // "100px"
gsap.utils.unitize("2rem", "px"); // "2rem" (unchanged)
```

### splitColor(color, returnHSL?)

将颜色字符串转为数组：**[red, green, blue]**（0–255），或存在/需要 alpha 时为 **[red, green, blue, alpha]**（4 元素 RGBA）。第二个参数 **returnHSL** 传 **true** 可得到 **[hue, saturation, lightness]** 或 **[hue, saturation, lightness, alpha]**（HSL/HSLA）。支持 `"rgb()"`、`"rgba()"`、`"hsl()"`、`"hsla()"`、十六进制及命名色（如 `"red"`）。在动画颜色分量或构建渐变时使用。见 [splitColor()](https://gsap.com/docs/v3/GSAP/UtilityMethods/splitColor/)。

```javascript
gsap.utils.splitColor("red");                    // [255, 0, 0]
gsap.utils.splitColor("#6fb936");                // [111, 185, 54]
gsap.utils.splitColor("rgba(204, 153, 51, 0.5)"); // [204, 153, 51, 0.5] (4 elements)
gsap.utils.splitColor("#6fb936", true);          // [94, 55, 47] (HSL: hue, saturation, lightness)
```

## 数组与集合

### selector(scope)

返回限定作用域的选择器函数，仅在给定元素（或 ref）内查找元素。在组件中使用，使 `".box"` 等选择器只匹配该组件后代，而非整页。接受 DOM 元素或 ref（如 React ref；会处理 `.current`）。

```javascript
const q = gsap.utils.selector(containerRef);
q(".box");        // array of .box elements inside container
gsap.to(q(".circle"), { x: 100 });
```

### toArray(value, scope?)

将值转为数组：选择器字符串（限定到元素）、NodeList、HTMLCollection、单个元素或数组。当向 GSAP（如 targets）传入混合输入且需要真实数组时使用。

```javascript
gsap.utils.toArray(".item");           // array of elements
gsap.utils.toArray(".item", container); // scoped to container
gsap.utils.toArray(nodeList);          // [ ... ] from NodeList
```

### pipe(...functions)

组合函数：**pipe(f1, f2, f3)(value)** 返回 f3(f2(f1(value)))。在补间或回调中应用变换链（如 normalize → mapRange → snap）时使用。

```javascript
const fn = gsap.utils.pipe(
  (v) => gsap.utils.normalize(0, 100, v),
  (v) => gsap.utils.snap(0.1, v)
);
fn(50); // normalized then snapped
```

### wrap(min, max, value?)

将值包裹进 min–max 范围（含 min、不含 max）。用于无限滚动或循环值。省略 **value** 可得到函数：`wrap(min, max)(value)`。

```javascript
gsap.utils.wrap(0, 360, 370);  // 10
gsap.utils.wrap(0, 360, -10);   // 350

let wrapFn = gsap.utils.wrap(0, 360);
wrapFn(370); // 10
```

### wrapYoyo(min, max, value?)

在范围内 yoyo 式包裹（在端点反弹）。用于范围内来回运动。省略 **value** 可得到函数：`wrapYoyo(min, max)(value)`。

```javascript
gsap.utils.wrapYoyo(0, 100, 150); // 50 (bounces back)

let wrapY = gsap.utils.wrapYoyo(0, 100);
wrapY(150); // 50
```

## 最佳实践

- ✅ 当同一范围/配置被多次使用时，省略 value 参数得到可复用函数（如滚动处理器、补间回调）：`let mapFn = gsap.utils.mapRange(0, 1, 0, 360); mapFn(progress)`。
- ✅ 网格对齐或步进值用 **snap**；当 GSAP 或你的代码需要由选择器或 NodeList 得到真实数组时用 **toArray**。
- ✅ 在组件中用 **gsap.utils.selector(scope)**，使选择器限定在容器或 ref 内。

## 请勿

- ❌ 假定 **mapRange** / **normalize** 处理单位；它们只处理数字。涉及单位时用 **getUnit** / **unitize**。
- ❌ 覆盖或依赖未文档化行为；请遵循已文档化的 API。

### 延伸阅读

https://gsap.com/docs/v3/HelperFunctions
