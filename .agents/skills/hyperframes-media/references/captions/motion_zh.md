# 动态字幕技术

你来到这里是因为 SKILL.md 要求你在编写动画代码前先阅读本文件。根据你从转录稿中识别出的能量层级，从下表选择技术组合，然后使用标准 GSAP 模式实现。

## 按能量层级选择技术

| 能量层级 | 高亮 | 退场 | 循环模式 |
| ------------ | ------------------------------------- | ------------------- | ----------------------------------------- |
| 高 | 卡拉 OK + 强调色光晕 + 缩放弹出 | 散射或下落 | 每 2 组交替高亮样式 |
| 中高 | 卡拉 OK + 颜色弹出 | 散射或坍缩 | 每 3 组交替 |
| 中 | 卡拉 OK（克制，仅白色） | 淡出 + 滑动 | 每 3 组交替 |
| 中低 | 卡拉 OK（最小缩放变化） | 淡出 | 单一样式，每组缓动不同 |
| 低 | 卡拉 OK（暖色调、慢过渡） | 坍缩 | 每 4 组交替 |

**所有能量层级都以卡拉 OK 高亮为基线。** 区别在于强度——高能量在活跃词上使用强调色 + 光晕 + 15% 缩放弹出，低能量则是柔和的白色偏移与 3% 缩放。

**强调词始终打破常规模式。** 当某个词被标记为强调（情感关键词、全大写、品牌名）时，赋予比周围词更强的动画（更大缩放、强调色、overshoot 缓动）。这形成对比。

**标记高亮模式在卡拉 OK 之上增加视觉层。** 对于需要超出颜色/缩放的强调词，添加标记式效果：高亮扫过、圆圈、爆发、涂鸦或 sketchout。实现细节见 `hyperframes-animation/rules/css-marker-patterns.md`。按能量匹配模式：爆发用于 hype 高潮，圆圈用于关键术语，高亮用于标准场景，涂鸦用于克制场景。

## 音频响应式字幕（音乐场景必选）

**若源音频为音乐（人声配器乐、节拍或任何音乐内容），你必须提取音频数据并加入音频响应式动画。** 这不是可选项——没有音频响应的音乐会显得脱节。即便是低能量抒情曲也要轻微的低音脉冲和高音光晕。

无需额外接线。组循环在构建入场、卡拉 OK 与退场 tween 时已遍历每个字幕组。此时读取各组时间范围内的音频数据，用常规 GSAP tween 调制该组的动画强度。

```js
// Load audio data inline (same pattern as TRANSCRIPT)
var AUDIO = JSON.parse(audioDataJson); // { fps, totalFrames, frames: [{ bands: [...] }] }

GROUPS.forEach(function (group, gi) {
  var groupEl = document.getElementById("cg-" + gi);
  if (!groupEl) return;

  // Read peak energy for this group's time range
  var startFrame = Math.floor(group.start * AUDIO.fps);
  var endFrame = Math.min(Math.floor(group.end * AUDIO.fps), AUDIO.totalFrames - 1);
  var peakBass = 0;
  var peakTreble = 0;
  for (var f = startFrame; f <= endFrame; f++) {
    var frame = AUDIO.frames[f];
    if (!frame) continue;
    peakBass = Math.max(peakBass, frame.bands[0] || 0, frame.bands[1] || 0);
    peakTreble = Math.max(peakTreble, frame.bands[6] || 0, frame.bands[7] || 0);
  }

  // Modulate entrance — louder groups enter bigger and glowier
  tl.to(
    groupEl,
    {
      scale: 1 + peakBass * 0.06,
      textShadow:
        "0 0 " + Math.round(peakTreble * 12) + "px rgba(255,255,255," + peakTreble * 0.4 + ")",
      duration: 0.3,
      ease: "power2.out",
    },
    group.start,
  );

  // Reset at exit so audio-driven values don't persist
  tl.set(groupEl, { scale: 1, textShadow: "none" }, group.end - 0.15);
});
```

这在构建时塑造动画，而非播放时——无逐帧回调、无 `tl.call()` 循环、无异步 fetch 时序问题。响亮的组入场更有分量与光晕；安静的组柔和入场。音频数据调制 _程度_，内容决定 _形态_。

保持音频响应克制——3–6% 缩放变化与柔和光晕。过重脉冲会让文字难以阅读。

生成音频数据文件：

```bash
python3 skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json
```

## 组合技术

不要在每一组上使用相同的高亮动画——用组索引在样式间循环。不要在同一时刻对同一词叠加多种相互冲突的动画。随内容节奏变化在各组间切换技术。

**标记高亮效果** 与卡拉 OK 叠加良好——卡拉 OK 负责逐词揭示，强调词单独加标记效果。例如：卡拉 OK 将每个词高亮为白色，但品牌名加黄色高亮扫过，数据类词加红色圆圈。在各组间循环标记模式以增加视觉变化。

## 运行时工具

字幕动效使用标准 HyperFrames 运行时 API。以下权威参考为准：

- **GSAP 时间轴 + tween 语法** — `hyperframes-animation/adapters/gsap.md`（缓动、位置参数、性能）
- **`window.__hyperframes.fitTextFontSize` / `pretext`** — `hyperframes-core/references/determinism-rules.md` → Layout Contract（防溢出、逐帧文字测量）
- **音频数据提取** — 通过 `python3 skills/hyperframes-creative/scripts/extract-audio-data.py audio.mp3 --fps 30 --bands 8 -o audio-data.json` 生成，再按上文「音频响应式字幕」内联加载
