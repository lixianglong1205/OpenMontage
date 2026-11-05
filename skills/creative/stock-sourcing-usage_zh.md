# OpenMontage 素材库检索用法

> 如何高效使用素材图片与视频工具——查询构建、提供商选择、许可意识，以及与素材流水线的集成。

## 可用素材工具

| 工具 | 提供商 | 内容 | 费用 | 速率限制 | 适用场景 |
|------|----------|---------|------|-----------|----------|
| `pexels_image` | Pexels | 照片 | 免费 | 200/小时 | 高质量摄影、丰富图库 |
| `pixabay_image` | Pixabay | 照片、插画、矢量 | 免费 | 100/分钟 | 分类筛选、大型图库（500 万+） |
| `pexels_video` | Pexels | 视频片段 | 免费 | 200/小时 | HD/4K 真实场景实拍 |
| `pixabay_video` | Pixabay | 视频片段 | 免费 | 100/分钟 | 分类筛选视频、动画片段 |

## 提供商选择指南

### 何时使用 Pexels
- 需要**高质量摄影**（精选、专业）
- 需要**视频**（视频库比 Pixabay 更大）
- 需要**方向筛选**（横屏/竖屏/方形）
- 需要**颜色筛选**（匹配 playbook 调色板）
- 需要**多语言**结果（28 种 locale）

### 何时使用 Pixabay
- 需要**按分类筛选**（自然、商业、科学等）
- 除照片外还需要**插画或矢量**
- 需要**编辑精选**（editor's choice）结果
- 需要**更高速率限制**（100/分钟 vs 200/小时）
- 需要**视频类型筛选**（实拍 vs 动画）

### 决策流程
```
Need stock image?
├── Need specific category (science, business, etc.)? → pixabay_image
├── Need illustration/vector? → pixabay_image
├── Need color matching? → pexels_image
└── General photo? → pexels_image (higher quality curation)

Need stock video?
├── Need 4K? → pexels_video (supports 4K via size="large")
├── Need animation clips? → pixabay_video (video_type="animation")
├── Need category filter? → pixabay_video
└── General footage? → pexels_video (better HD quality)
```

## 输入参数指南

### pexels_image / pexels_video
```python
{
    "query": "city skyline sunset",      # Required: search term
    "orientation": "landscape",           # Optional: landscape/portrait/square
    "size": "large",                      # Optional: large/medium/small
    "color": "FF6B35",                    # Optional: hex without # or color name
    "per_page": 5,                        # Results per page (1-80)
    "download_size": "large2x",           # Image: original/large2x/large/medium
    "preferred_quality": "hd",            # Video: hd/sd
    "output_path": "assets/images/s3.jpg" # Where to save
}
```

### pixabay_image / pixabay_video
```python
{
    "query": "server room",              # Required: search term (max 100 chars)
    "image_type": "photo",               # Image: all/photo/illustration/vector
    "video_type": "film",                # Video: all/film/animation
    "orientation": "horizontal",          # all/horizontal/vertical
    "category": "computer",              # One of 20 categories
    "colors": "blue,gray",              # Comma-separated color names
    "editors_choice": true,              # Curated high-quality only
    "safesearch": true,                  # Always true for production
    "output_path": "assets/video/s5.mp4" # Where to save
}
```

## 注意事项与最佳实践

### 1. Pixabay URL 会过期
Pixabay 下载 URL 内含会过期的 token。**搜索后请立即下载**。工具会自动处理，但切勿缓存 Pixabay URL 供后续使用。

### 2. Pixabay 分辨率限制
标准 Pixabay API 用户最高获得 1280px 宽图像（`largeImageURL`）。完整分辨率需获批的 API 访问权限。对多数视频制作叠加层而言，1280px 已足够。

### 3. Pexels 认证头
Pexels 在 `Authorization` 头中使用裸 API key（**不是** `Bearer`）。工具已处理，调试时需知晓。

### 4. 搜索结果因 locale 而异
Pexels 支持 28 种 locale。若搜索文化特定内容，请设置 locale 参数。

### 5. 素材图片结果是确定性的
与 AI 生成不同，两次搜索「ocean waves」会返回相同结果。若第一条结果不够好，请换关键词——不要重复同一查询。

### 6. 视频时长筛选
两种素材视频工具均支持 `min_duration` 与 `max_duration`。仅需 4 秒时可用其避免下载 30 秒片段——节省带宽与时间。

## 与素材流水线集成

素材工具与生成工具集成方式完全相同。在 asset manifest 中：

```json
{
    "id": "broll-s3",
    "type": "image",
    "subtype": "broll",
    "path": "assets/images/broll-s3.jpg",
    "source_tool": "pexels_image",
    "scene_id": "scene-3",
    "cost_usd": 0.00,
    "metadata": {
        "photographer": "Joey Farina",
        "source_url": "https://www.pexels.com/photo/2014422/",
        "license": "Pexels License (free, no attribution required)"
    }
}
```

Edit Director 与 Compose Director 将素材资源与生成资源同等对待——只需从 manifest 引用文件路径。

## 许可摘要

| 提供商 | 商业使用 | 署名 | 限制 |
|----------|---------------|-------------|-------------|
| Pexels | 是，免费 | 非必须（建议注明） | 不得原样出售；不得暗示背书 |
| Pixabay | 是，免费 | 非必须 | 不得原样出售；不得创建竞争性素材服务 |

二者均适用于 OpenMontage 全部用例。无许可费、无按次版税、无署名义务。
