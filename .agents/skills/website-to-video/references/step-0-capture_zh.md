# 步骤 0：捕获

捕获流水线会下载站点并提取结构化数据，供后续工作流读取。步骤 0 只需执行一条命令并做一次健全性检查。**所有分析（读文件、查看联系表、推导品牌调性、挑选素材）都在步骤 1–3 中进行，而不是在本步。**

## 运行捕获

基础捕获不需要 API 密钥。但在运行之前，请询问用户：

> 「为获得最佳效果，建议设置 Gemini API 密钥——这样我可以为每张捕获的图片生成 AI 描述，便于为每个场景选对素材。每张图片大约 $0.001。你也可以跳过；但有了密钥，视频质量会更好。设置方式：在项目根目录的 `.env` 文件中添加 `GEMINI_API_KEY=your-key`。可在 ai.google.dev 获取免费密钥。」

若用户提供密钥或已配置，则继续。若用户跳过，同样继续——没有密钥也能完成捕获，但 `asset-descriptions.md` 将只有 DOM 上下文描述（位置、尺寸、alt 文本），而没有 AI 视觉描述。

若尚未创建视频项目目录，请先创建，再将网站捕获到其下的 `capture/` 子文件夹：

```bash
npx hyperframes capture <URL> -o <project-dir>/capture
```

示例：`npx hyperframes capture https://stripe.com -o videos/stripe-launch/capture`

将捕获产物（`screenshots/`、`assets/`、`extracted/`、`AGENTS.md`、`CLAUDE.md`）放在独立的 `capture/` 子文件夹中，可与后续构建文件（`SCRIPT.md`、`STORYBOARD.md`、`DESIGN.md`、`compositions/`、`index.html`、`narration.wav`、`transcript.json`、`renders/`、`snapshots/`）隔离，后者均位于 `<project-dir>/` 根目录。

若只是探索性捕获、尚未用于制作视频，默认 `./capture/`（或任意你指定的 `-o <name>`）即可——只有在捕获之上继续搭建视频时，才需要遵守上述隔离约定。

## 确认成功

等待捕获完成。打印一行摘要说明捕获结果：

> 「已捕获 N 张截图、M 个素材、K 个 SVG、F 种字体。可进入步骤 1。」

若命令非零退出、各项计数均为零，或缺少必需目录（`extracted/`、`assets/`、`screenshots/`），则展示错误并停止——不要用损坏的捕获进入步骤 1。

## `capture/` 中的内容（参考表——**不要在本步读取**）

各下游步骤只读取所需内容。不要在步骤 0 预取全部文件；那样会膨胀上下文，且到真正使用时摘要已过时。

| 路径                                      | 首次读取于                                 |
| ----------------------------------------- | --------------------------------------------- |
| `capture/extracted/tokens.json`           | 步骤 1（DESIGN.md — 颜色 / 字体）           |
| `capture/extracted/design-styles.json`    | 步骤 1（DESIGN.md — 版式 / 组件）  |
| `capture/extracted/fonts-manifest.json`   | 步骤 1（字体识别）                  |
| `capture/extracted/asset-descriptions.md` | 步骤 2（简报 grounding）与步骤 3（素材）  |
| `capture/extracted/visible-text.txt`      | 步骤 2（brief）与步骤 3（脚本）            |
| `capture/assets/contact-sheet-*.jpg`      | 步骤 3（素材挑选）                        |
| `capture/assets/svgs/contact-sheet-*.jpg` | 步骤 3（SVG / logo 挑选）                   |
| `capture/screenshots/contact-sheet-*.jpg` | 步骤 3（视觉氛围参考）                |
| `capture/extracted/animations.json`       | 步骤 3 / 步骤 5（仅当站点有动画时） |
| `capture/extracted/lottie-manifest.json`  | 步骤 3（仅当站点使用 Lottie 时）             |
| `capture/extracted/video-manifest.json`   | 步骤 3（仅当站点嵌入视频时）            |
| `capture/extracted/shaders.json`          | 步骤 3 / 步骤 5（仅当站点有 WebGL 时）      |
| `capture/assets/<individual files>`       | 步骤 5（仅当放置特定素材时）   |

## 门禁

捕获以退出码 0 结束。素材 / 截图 / 字体计数非零。进入步骤 1。
