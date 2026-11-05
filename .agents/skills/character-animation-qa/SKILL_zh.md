---
name: character-animation-qa
description: 使用 schema 校验、Playwright 浏览器预览、帧采样以及 FFmpeg/ffprobe 最终输出检查来审查本地角色动画。
license: MIT
---

# 角色动画 QA

在展示角色动画预览或最终渲染结果之前使用本技能。

## 审查层级

1. Schema 校验：角色设计、绑定方案、姿势库、动作时间线。
2. 静态资源检查：引用的部件与背景均存在。
3. 浏览器预览：加载预览、截屏并收集控制台错误。
4. 运动检查：对比采样帧是否存在显著差异。
5. 最终 MP4 检查：ffprobe 元数据、时长、分辨率、音频与帧采样。
6. Agent 视觉审查：检查采样帧中的肢体分离、错误图层、出画角色、难以辨认的表情以及错乱文本。

## Playwright 模式

```ts
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1280, height: 720 } });
await page.goto(previewUrl, { waitUntil: "networkidle" });
await page.screenshot({ path: "preview.png" });
```

## 通过/修订/失败

- `pass`：技术检查通过，表演可读。
- `revise`：可修复的绑定/时间线问题。
- `fail`：资源缺失、空白渲染、运行时失败或错误运行时。

## 参考来源

- Playwright 截图：
  https://playwright.dev/docs/screenshots
- Playwright 页面导航：
  https://playwright.dev/docs/api/class-page#page-goto
- 最终媒体探测应使用 FFmpeg/ffprobe：
  https://ffmpeg.org/ffprobe.html
