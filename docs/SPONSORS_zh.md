# 赞助商

本文档说明如何将赞助商 Logo 添加到 OpenMontage 的 README 中。

## 赞助商资源规范

- 将赞助商 Logo 存放在 `assets/sponsors/`。
- 文件名使用基于赞助商名称的小写 kebab-case，例如 `acme-video.svg`。
- 优先使用 SVG。仅当赞助商无法提供矢量图时使用 PNG。
- Logo 应保持透明背景、紧凑裁剪，并在 `44px` 高度下清晰可读。
- 链接目标使用赞助商官网或产品页。
- 使用描述性 alt 文本：例如 `Acme Video logo`，不要只写 `logo`。

## README 片段

在 `README.md` 顶部附近的「Sponsors」小节中，为每位赞助商添加一行表格：

```html
<tr>
<td width="180" align="center"><a href="https://example.com"><img src="assets/sponsors/example-sponsor.svg" alt="Example Sponsor" width="150"></a></td>
<td><strong>Example Sponsor</strong> helps OpenMontage users do something concrete. Mention the useful product outcome, then close with a short <a href="https://example.com">CTA link</a>.</td>
</tr>
```

若赞助商分别提供浅色与深色 Logo，使用 `picture` 元素：

```html
<tr>
<td width="180" align="center">
  <a href="https://example.com">
    <picture>
      <source media="(prefers-color-scheme: dark)" srcset="assets/sponsors/example-sponsor-dark.svg">
      <img src="assets/sponsors/example-sponsor-light.svg" alt="Example Sponsor" width="150">
    </picture>
  </a>
</td>
<td><strong>Example Sponsor</strong> helps OpenMontage users do something concrete. Mention the useful product outcome, then close with a short <a href="https://example.com">CTA link</a>.</td>
</tr>
```

## 接入清单

添加赞助商前，请收集：

- 赞助商展示名称
- 赞助商 URL
- Logo 文件，优先 SVG
- 确认 OpenMontage 有权在 README 中展示该 Logo
- 赞助商要求的商标表述（如有）

除非项目维护者明确批准，请勿添加追踪 URL、联盟跳转链接，或关于背书的表述。
