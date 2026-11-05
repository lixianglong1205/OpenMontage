# 字体排版（Typography）

编译器**预打包固定的一组**字体（见下表）——在 `font-family` 中写其中任一家族即可**确定性地**离线渲染，无需额外配置、也不会出现警告。若使用的名称**不在**该集合内，**不会静默丢弃**：若是真实的 Google 字体，编译器会在**构建时**从 Google Fonts 拉取并嵌入，因此**仍能**渲染——但该隐式路径会 (a) 触发 `font_family_without_font_face` lint 警告，且 (b) 在**分布式/云端渲染**中为**失败即停（fail-closed）**——若无法访问 Google，渲染会**报错**，而不会悄悄替换为系统字体。此外，**本地渲染会自动捕获你实际拥有的字体**：机器上已安装的字体族、本地 `@font-face` 路径或外部 CDN 样式表都会在构建时压缩为 woff2 并内联。因此，既**不在**预打包列表**也不在** Google Fonts 上的名称，仅当**既**未本地安装**又**未在 `@font-face` 中声明时，才会真正回退到通用系统字体——即便如此也会记录编译器警告。**一处注意**：分布式/云端（Lambda）渲染会禁用系统字体捕获，因此不要依赖仅本地安装的字体。**不要**假设未打包的展示用字体名会「开箱即用」：凡需可预测渲染的内容，请从下表选预打包家族，**或自行嵌入 `@font-face`**（见「查找字体」）。

## 目录

- 可嵌入字体（自动解析）
- 禁用字体
- 护栏规则
- 未被明确要求时不要做的事
- 查找字体
- 选型思路
- 相似字体配对
- 深色背景
- 数据场景的 OpenType 特性

## 可嵌入字体（自动解析）

以下 **18 个家族**由渲染器**预打包**——以本地 data URI 嵌入，无需网络请求，可离线、确定性地渲染，零配置、无 lint 警告、无 fail-closed 拉取风险。在 `font-family` 中写任一家族即可渲染；**仅列出的字重存在**（请求某家族未提供的字重会得到合成/回退字重，而非真实字重）。（其他真实 Google 字体仍可通过引言中的隐式构建时拉取工作——但只有这些家族没有上述所有限制。）

| 家族              | 字重            | 角色              |
| ----------------- | --------------- | ----------------- |
| Inter             | 400 · 700 · 900 | sans（正文/UI）   |
| Roboto            | 400 · 700 · 900 | sans              |
| Open Sans         | 400 · 700       | sans              |
| Lato              | 400 · 700 · 900 | sans              |
| Nunito            | 400 · 700 · 900 | sans（圆角）      |
| Montserrat        | 400 · 700 · 900 | 几何 sans         |
| Poppins           | 400 · 700 · 900 | 几何 sans         |
| Outfit            | 400 · 700 · 900 | 几何 sans         |
| Oswald            | 400 · 700       | 紧凑 sans         |
| **League Gothic** | **仅 400**      | 紧凑展示体        |
| **Archivo Black** | **仅 400**      | 粗展示体          |
| Playfair Display  | 400 · 700 · 900 | serif（展示）     |
| EB Garamond       | 400 · 700       | serif（正文）     |
| Space Mono        | 400 · 700       | 等宽              |
| IBM Plex Mono     | 400 · 700       | 等宽              |
| JetBrains Mono    | 400 · 700       | 等宽              |
| Source Code Pro   | 400 · 700       | 等宽              |
| Noto Sans JP      | 400 · 700       | CJK（日文）       |

> ⚠ **League Gothic 与 Archivo Black 仅提供字重 400**——它们本身已是粗/紧凑展示面。不要对它们使用 `font-weight: 700/900`。

**别名**——以下常见名称会解析到已嵌入家族，可安全书写：`Helvetica Neue` / `Helvetica` / `Arial` → Inter · `Futura` / `DIN Alternate` / `Arial Black` → Montserrat · `Bebas Neue` → League Gothic · `Segoe UI` → Roboto · `Courier New` / `Courier` → JetBrains Mono · `Garamond` → EB Garamond。（因此「安全」的 `Helvetica Neue` 栈总能渲染——映射到已嵌入的 Inter。）

**与下文禁用列表的对照：** 多个已嵌入家族（Inter、Roboto、Open Sans、Lato、Nunito、Poppins、Outfit、Playfair Display、EB Garamond）**同时**出现在禁用「千篇一律」列表中——能正常渲染但观感偏泛用。既**已嵌入又未禁用**、相对安全且易出辨识度的选择：**Montserrat、Oswald、League Gothic、Archivo Black、Space Mono、IBM Plex Mono、JetBrains Mono、Source Code Pro、Noto Sans JP**。优先选用这些（或通过「查找字体」步骤确认过的非打包字体）。非打包名称并非一定失败——真实 Google 字体会自动拉取并嵌入——但会带 lint 警告，且在云端渲染中 fail-closed；凡需可预测渲染，请**通过 `@font-face` 自行嵌入**（见「查找字体」），勿依赖隐式拉取。

## 禁用字体

训练数据中的默认选择，各类 LLM 都爱用。会让作品之间显得千篇一律。

Inter, Roboto, Open Sans, Noto Sans, Arimo, Lato, Source Sans, PT Sans, Nunito, Poppins, Outfit, Sora, Playfair Display, Cormorant Garamond, Bodoni Moda, EB Garamond, Cinzel, Prata, Syne

**Syne 尤其**是最滥用的「有辨识度」展示字体，一眼即 AI 设计痕迹。

## 护栏规则

你懂这些规则却常违反。请停止。

- **不要配对两种 sans-serif。** 你常这样做——标题一种、正文一种。应跨边界：serif + sans，或 sans + mono。
- **每个场景一种表现型字体。** 你常选两种「有趣」字体想更好——一种表演，一种退后。
- **字重对比必须极端。** 你默认 400 对 700。视频需要 300 对 900。动态画面中一眼要能看出差别。
- **用视频尺寸，不是网页尺寸。** 正文：至少 20px。标题：60px+。数据标签：16px。你会想用 14px。不要。

## 未被明确要求时不要做的事

- **张力应有含义。** 不要模式化配对。问清这两种字体**为何**冲突。配对应体现内容的矛盾——机械 vs 人性、公开 vs 私密、机构 vs 个人。若说不清张力，就是随意搭配。
- **语域切换。** 为不同交际模式指定不同字体——陈述一种、数据一种、署名一种。不是页面层级，而是对话中的不同声音。
- **张力可存在于单一字体内。** 看起来熟悉却暗中怪异的字体，与观者预期形成张力，而非与另一字体。
- **只改一个变量 = 强烈对比。** 同一字形，等宽 vs 比例。同一家族不同光学尺寸。仅改节奏而其余不变。
- **双重人格可行。** 两种表现型字体可共存，若态度一致（都戏谑或都精确），即使形态完全不同。
- **时间是层级。** 最先出现的元素最重要。在视频中，顺序取代位置。
- **动效即排版。** 词如何入场与字体本身同样传达含义。0.1s 猛击 vs 2s 渐显——同一字体，完全不同的信息。
- **固定阅读时间。** 屏上 3 秒 = 2 秒内必须可读。更少字、更大号。
- **字距比网页更紧。** 展示字号用 -0.03em 至 -0.05em。视频编码会压缩笔画细节。

## 查找字体

不要默认只用熟悉的。若内容是奢华，grotesque sans 可能比预期的 Didone serif 更有张力。先定语域，再搜索。

将下列脚本保存为 `/tmp/fontquery.py`，并运行 `curl -s 'https://fonts.google.com/metadata/fonts' > /tmp/gfonts.json && python3 /tmp/fontquery.py /tmp/gfonts.json`：

```python
import json, sys, random
from collections import OrderedDict

random.seed()  # true random each run

with open(sys.argv[1]) as f:
    data = json.load(f)
fonts = data.get("familyMetadataList", [])

ban = {"Inter","Roboto","Open Sans","Noto Sans","Lato","Poppins","Source Sans 3",
       "PT Sans","Nunito","Outfit","Sora","Playfair Display","Cormorant Garamond",
       "Bodoni Moda","EB Garamond","Cinzel","Prata","Arimo","Source Sans Pro","Syne"}
skip_pfx = ("Roboto","Noto ","Google Sans","Bpmf","Playwrite","Anek","BIZ ",
            "Nanum","Shippori","Sawarabi","Zen ","Kaisei","Kiwi ","Yuji ","Radio ")

def ok(f):
    if f["family"] in ban: return False
    if any(f["family"].startswith(b) for b in skip_pfx): return False
    if "latin" not in (f.get("subsets") or []): return False
    return True

seen = set()
R = OrderedDict()

# Trending Sans — recent (2022+), popular (<300)
R["Trending Sans"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") in ("Sans Serif","Display") and f.get("dateAdded","") >= "2022-01-01" and f.get("popularity",9999) < 300:
        R["Trending Sans"].append(f); seen.add(f["family"])

# Trending Serif — recent (2018+), popular (<600)
R["Trending Serif"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Serif" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Trending Serif"].append(f); seen.add(f["family"])

# Monospace — recent (2018+), popular (<600)
R["Monospace"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Monospace" and f.get("dateAdded","") >= "2018-01-01" and f.get("popularity",9999) < 600:
        R["Monospace"].append(f); seen.add(f["family"])

# Impact & Condensed — heavy display fonts with 800+ weight
R["Impact & Condensed"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    has_heavy = any(k in list(f.get("fonts",{}).keys()) for k in ("800","900"))
    is_display = f.get("category") in ("Sans Serif","Display")
    if has_heavy and is_display and f.get("popularity",9999) < 400:
        R["Impact & Condensed"].append(f); seen.add(f["family"])

# Script & Handwriting — popular (<300)
R["Script & Handwriting"] = []
for f in fonts:
    if not ok(f) or f["family"] in seen: continue
    if f.get("category") == "Handwriting" and f.get("popularity",9999) < 300:
        R["Script & Handwriting"].append(f); seen.add(f["family"])


# Randomize the top 5 in each category so the LLM doesn't always pick the same first result
for cat in R:
    R[cat].sort(key=lambda x: x.get("popularity",9999))
    top5 = R[cat][:5]
    rest = R[cat][5:]
    random.shuffle(top5)
    R[cat] = top5 + rest
limits = {"Trending Sans":15,"Trending Serif":12,"Monospace":8,
          "Impact & Condensed":12,"Script & Handwriting":10}
for cat in R:
    items = R[cat][:limits.get(cat,10)]
    if not items: continue
    print(f"--- {cat} ({len(items)}) ---")
    for ff in items:
        var = "VAR" if ff.get("axes") else "   "
        print(f'  {ff.get("popularity"):4d} | {var} | {ff["family"]}')
    print()
```

五类：流行 sans、流行 serif、等宽、冲击/紧凑、手写/Script。均从 Google Fonts 元数据动态筛选——无硬编码字体名。配对时可跨分类边界。

## 选型思路

不要按类别反射选（ editorial → serif、tech → mono、modern → 几何 sans）。那是模式匹配，不是设计。

1. **命名语域。** 内容以何种声音在说话？机构权威？个人倾诉？技术精确？随意戏谑？语域比类别更能收窄范围。
2. **物理化想象。** 把字体想象成品牌能实体出货的对象——博物馆说明牌、手绘店招、1970 年代大型机终端手册、大衣内衬织标、廉价新闻纸童书、税表。与语域最契合的物理对象指向合适的**类型**。
3. **拒绝第一直觉。** 第一个「感觉对」的字体往往是该语域的训练数据默认。若上次也选了它，换别的。
4. **交叉检验假设。** 编辑类 brief **不必** serif。技术 brief **不必** sans。儿童产品 **不必** 圆角展示体。最有辨识度的选择常违背类别预期。

## 相似字体配对

切勿配对相似但不相同的两种字体——两种几何 sans、两种过渡 serif、两种 humanist sans。会产生视觉摩擦却缺乏清晰层级。观者觉得「不对」却说不清。要么一种字体两种字重，要么在多轴上对比：serif + sans、紧凑 + 宽体、几何 + humanist。

## 深色背景

浅色字 on 深色底会产生两种光学错觉，需补偿：

- **表观字重增加。** 同 `font-weight` 下，浅 on 深比深 on 浅看起来更粗。正文用 350 而非 400。标题受影响较小，因字号补偿。
- **表观间距更紧。** 字母周围光晕缩小 perceived 间隙。`line-height` 比浅色背景值高 0.05–0.1。展示字号可加 0.01em `letter-spacing` 抵消。

## 数据场景的 OpenType 特性

多数字体自带默认关闭的 OpenType 特性。数据类构图请开启：

```css
/* Tabular numbers — digits align vertically in columns */
.stat-value,
.timer,
.data-column {
  font-variant-numeric: tabular-nums;
}

/* Diagonal fractions — renders 1/2 as ½ */
.recipe-amount,
.ratio {
  font-variant-numeric: diagonal-fractions;
}

/* Small caps for abbreviations — less visual shouting */
.abbreviation,
.unit {
  font-variant-caps: all-small-caps;
}

/* Disable ligatures in code — fi, fl, ffi should stay separate */
code,
.code {
  font-variant-ligatures: none;
}
```

只要数字纵向堆叠——统计高亮、计时器、记分牌、数据表——`tabular-nums` 都必不可少。否则数字为比例宽度，列无法对齐。
