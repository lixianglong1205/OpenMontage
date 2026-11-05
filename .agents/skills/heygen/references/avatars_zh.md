---
name: avatars
description: 列出 HeyGen 数字人、数字人风格及 avatar_id 选择
---

# HeyGen 数字人（Avatars）

数字人是 HeyGen 视频中的 AI 生成主讲人。你可以使用 HeyGen 提供的公开数字人，也可以创建自定义数字人。

## 生成前预览数字人

在生成视频前务必预览数字人，确保符合用户偏好。每个数字人都有可在浏览器中直接打开的预览 URL，无需下载。

### 列出数字人并展示预览

```typescript
async function listAndPreviewAvatars(openInBrowser = true): Promise<void> {
  const response = await fetch("https://api.heygen.com/v2/avatars", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });
  const { data } = await response.json();

  for (const avatar of data.avatars.slice(0, 5)) {
    console.log(`\n${avatar.avatar_name} (${avatar.gender})`);
    console.log(`  ID: ${avatar.avatar_id}`);
    console.log(`  Preview: ${avatar.preview_image_url}`);
  }

  // Preview URLs can be opened directly in any browser
  for (const avatar of data.avatars.slice(0, 3)) {
    console.log(`Open in browser: ${avatar.preview_image_url}`);
  }
}
```

### 工作流：先预览再生成

1. **列出可用数字人** — 获取名称、性别和预览 URL
2. **向用户展示预览 URL** — 分享 `preview_image_url` 供视觉确认
3. **用户选择** 偏好的数字人（按名称或 ID）
4. **获取数字人详情** 以取得 `default_voice_id`
5. **使用所选数字人生成视频**

### API 响应中的预览字段

| 字段 | 说明 |
|-------|-------------|
| `preview_image_url` | 数字人静态图片（JPG）— 可公开访问的 URL |
| `preview_video_url` | 展示数字人动画的短视频片段 |

两个 URL 均可公开访问 — 查看时无需认证。

## 列出可用数字人

### curl

```bash
curl -X GET "https://api.heygen.com/v2/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface Avatar {
  avatar_id: string;
  avatar_name: string;
  gender: "male" | "female";
  preview_image_url: string;
  preview_video_url: string;
}

interface AvatarsResponse {
  error: null | string;
  data: {
    avatars: Avatar[];
    talking_photos: TalkingPhoto[];
  };
}

async function listAvatars(): Promise<Avatar[]> {
  const response = await fetch("https://api.heygen.com/v2/avatars", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: AvatarsResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.avatars;
}
```

### Python

```python
import requests
import os

def list_avatars() -> list:
    response = requests.get(
        "https://api.heygen.com/v2/avatars",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["avatars"]
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "avatars": [
      {
        "avatar_id": "josh_lite3_20230714",
        "avatar_name": "Josh",
        "gender": "male",
        "preview_image_url": "https://files.heygen.ai/...",
        "preview_video_url": "https://files.heygen.ai/..."
      },
      {
        "avatar_id": "angela_expressive_20231010",
        "avatar_name": "Angela",
        "gender": "female",
        "preview_image_url": "https://files.heygen.ai/...",
        "preview_video_url": "https://files.heygen.ai/..."
      }
    ],
    "talking_photos": []
  }
}
```

## 数字人类型

### 公开数字人

HeyGen 提供可供任何人使用的公开数字人库：

```typescript
// List only public avatars
const avatars = await listAvatars();
const publicAvatars = avatars.filter((a) => !a.avatar_id.startsWith("custom_"));
```

### 私有/自定义数字人

基于你自己的训练素材创建的自定义数字人：

```typescript
const customAvatars = avatars.filter((a) => a.avatar_id.startsWith("custom_"));
```

## 数字人风格

数字人支持不同的渲染风格：

| 风格 | 说明 |
|-------|-------------|
| `normal` | 全身镜头，标准构图 |
| `closeUp` | 面部特写，表现力更强 |
| `circle` | 圆形画框内的数字人（Talking Head） |
| `voice_only` | 仅音频，不渲染视频 |

### 各风格适用场景

| 使用场景 | 推荐风格 |
|----------|-------------------|
| 全屏主讲人视频 | `normal` |
| 个人化/亲密感内容 | `closeUp` |
| 画中画叠加 | `circle` |
| 角落小部件 | `circle` |
| 播客/纯音频内容 | `voice_only` |
| 带数字人叠加的动态图形 | `normal` 或 `closeUp` + 透明背景 |

### 使用数字人风格

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal", // "normal" | "closeUp" | "circle" | "voice_only"
      },
      voice: {
        type: "text",
        input_text: "Hello, world!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### 圆形风格用于 Talking Head

圆形风格适合叠加合成：

```typescript
// Circle avatar for picture-in-picture
{
  character: {
    type: "avatar",
    avatar_id: "josh_lite3_20230714",
    avatar_style: "circle",
  },
  voice: { ... },
  background: {
    type: "color",
    value: "#00FF00", // Green for chroma key, or use webm endpoint
  },
}
```

## 搜索与筛选数字人

### 按性别

```typescript
function filterByGender(avatars: Avatar[], gender: "male" | "female"): Avatar[] {
  return avatars.filter((a) => a.gender === gender);
}

const maleAvatars = filterByGender(avatars, "male");
const femaleAvatars = filterByGender(avatars, "female");
```

### 按名称

```typescript
function searchByName(avatars: Avatar[], query: string): Avatar[] {
  const lowerQuery = query.toLowerCase();
  return avatars.filter((a) =>
    a.avatar_name.toLowerCase().includes(lowerQuery)
  );
}

const results = searchByName(avatars, "josh");
```

## 数字人分组

数字人按分组组织，便于管理。

### 列出数字人分组

```bash
curl -X GET "https://api.heygen.com/v2/avatar_group.list?include_public=true" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### 查询参数

| 参数 | 类型 | 默认值 | 说明 |
|-----------|------|---------|-------------|
| `include_public` | bool | false | 在结果中包含公开数字人 |

#### TypeScript

```typescript
interface AvatarGroupItem {
  id: string;
  name: string;
  created_at: number;
  num_looks: number;
  preview_image: string;
  group_type: string;
  train_status: string;
  default_voice_id: string | null;
}

interface AvatarGroupListResponse {
  error: null | string;
  data: {
    avatar_group_list: AvatarGroupItem[];
  };
}

async function listAvatarGroups(
  includePublic = true
): Promise<AvatarGroupListResponse["data"]> {
  const params = new URLSearchParams({
    include_public: includePublic.toString(),
  });

  const response = await fetch(
    `https://api.heygen.com/v2/avatar_group.list?${params}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json: AvatarGroupListResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}
```

### 获取分组内的数字人

```bash
curl -X GET "https://api.heygen.com/v2/avatar_group/{group_id}/avatars" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

## 在视频生成中使用数字人

### 基础用法

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Welcome to our product demo!",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
  dimension: { width: 1920, height: 1080 },
};
```

### 多场景使用不同数字人

```typescript
const multiSceneConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hi, I'm Josh. Let me introduce my colleague.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
    {
      character: {
        type: "avatar",
        avatar_id: "angela_expressive_20231010",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello! I'm Angela. Nice to meet you!",
        voice_id: "2d5b0e6a8c3f47d9a1b2c3d4e5f60718",
      },
    },
  ],
};
```

## 使用数字人的默认音色

许多数字人带有预匹配的 `default_voice_id`，效果更自然。**这是推荐做法**，优于手动挑选音色。

### 推荐流程

```
1. GET /v2/avatars           → Get list of avatar_ids
2. GET /v2/avatar/{id}/details → Get default_voice_id for chosen avatar
3. POST /v2/video/generate   → Use avatar_id + default_voice_id
```

### 获取数字人详情（v2 API）

给定 `avatar_id`，获取详情（含默认音色）：

```bash
curl -X GET "https://api.heygen.com/v2/avatar/{avatar_id}/details" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

#### 响应格式

```json
{
  "error": null,
  "data": {
    "type": "avatar",
    "id": "josh_lite3_20230714",
    "name": "Josh",
    "gender": "male",
    "preview_image_url": "https://files.heygen.ai/...",
    "preview_video_url": "https://files.heygen.ai/...",
    "premium": false,
    "is_public": true,
    "default_voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "tags": ["AVATAR_IV"]
  }
}
```

#### TypeScript

```typescript
interface AvatarDetails {
  type: "avatar";
  id: string;
  name: string;
  gender: "male" | "female";
  preview_image_url: string;
  preview_video_url: string;
  premium: boolean;
  is_public: boolean;
  default_voice_id: string | null;
  tags: string[];
}

async function getAvatarDetails(avatarId: string): Promise<AvatarDetails> {
  const response = await fetch(
    `https://api.heygen.com/v2/avatar/${avatarId}/details`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const json = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data;
}

// Usage: Get default voice for a known avatar
const details = await getAvatarDetails("josh_lite3_20230714");
if (details.default_voice_id) {
  console.log(`Using ${details.name} with default voice: ${details.default_voice_id}`);
} else {
  console.log(`${details.name} has no default voice, select manually`);
}
```

#### 完整示例：使用任意数字人的默认音色生成视频

```typescript
async function generateWithAvatarDefaultVoice(
  avatarId: string,
  script: string
): Promise<string> {
  // 1. Get avatar details to find default voice
  const avatar = await getAvatarDetails(avatarId);

  if (!avatar.default_voice_id) {
    throw new Error(`Avatar ${avatar.name} has no default voice`);
  }

  // 2. Generate video with the avatar's default voice
  const videoId = await generateVideo({
    video_inputs: [{
      character: {
        type: "avatar",
        avatar_id: avatar.id,
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: script,
        voice_id: avatar.default_voice_id,
      },
    }],
    dimension: { width: 1920, height: 1080 },
  });

  return videoId;
}
```

### 为何使用默认音色？

1. **性别一致有保障** — 数字人与音色已预配对
2. **口型更自然** — 默认音色针对该数字人优化
3. **代码更简单** — 无需单独拉取并匹配音色
4. **质量更好** — HeyGen 已验证该组合效果

## 选择合适的数字人

### 数字人分类

HeyGen 数字人分为不同类别，请按使用场景匹配：

| 类别 | 示例 | 最适合 |
|----------|----------|----------|
| **商务/专业** | Josh, Angela, Wayne | 企业视频、产品演示、培训 |
| **休闲/友好** | Lily、各类生活方式数字人 | 社交媒体、非正式内容 |
| **主题/季节** | 节日主题、装扮类数字人 | 特定营销活动、季节性内容 |
| **表现力型** | 名称含 "expressive" 的数字人 | 引人入胜的叙事、动态内容 |

### 选择指南

**商务/专业内容：**
- 选择着装中性的数字人（商务休闲或正装）
- 避免主题或季节类数字人（节日装扮、过于休闲的着装）
- 预览数字人以确认专业形象
- 根据受众 demographics 选择性别与外观

**休闲/社交内容：**
- 数字人选择更灵活
- 主题类数字人可用于特定活动
- 让数字人气质与内容调性一致

### 常见误区

1. **商务内容使用主题数字人** — 节日主题数字人在产品演示中显得不专业
2. **生成前不预览** — 务必通过预览 URL 确认外观
3. **忽略数字人风格** — `circle` 风格可能不适合全屏演示
4. **音色性别不匹配** — 始终使用 `default_voice_id`，或手动匹配性别

### 选择清单

生成视频前：
- [ ] 已在浏览器中预览数字人图片/视频
- [ ] 数字人外观与内容调性一致（专业 vs 休闲）
- [ ] 数字人风格（`normal`、`closeUp`、`circle`）适合视频格式
- [ ] 音色性别与数字人性别一致
- [ ] 在可用时使用 `default_voice_id`

## 辅助函数

### 按 ID 获取数字人

```typescript
async function getAvatarById(avatarId: string): Promise<Avatar | null> {
  const avatars = await listAvatars();
  return avatars.find((a) => a.avatar_id === avatarId) || null;
}
```

### 校验数字人 ID

```typescript
async function isValidAvatarId(avatarId: string): Promise<boolean> {
  const avatar = await getAvatarById(avatarId);
  return avatar !== null;
}
```

### 随机获取数字人

```typescript
async function getRandomAvatar(gender?: "male" | "female"): Promise<Avatar> {
  let avatars = await listAvatars();

  if (gender) {
    avatars = avatars.filter((a) => a.gender === gender);
  }

  const randomIndex = Math.floor(Math.random() * avatars.length);
  return avatars[randomIndex];
}
```

## 常用数字人 ID

部分常用公开数字人 ID（可用性可能变化）：

| Avatar ID | 名称 | 性别 |
|-----------|------|--------|
| `josh_lite3_20230714` | Josh | Male |
| `angela_expressive_20231010` | Angela | Female |
| `wayne_20240422` | Wayne | Male |
| `lily_20230614` | Lily | Female |

使用前请始终通过列表接口确认数字人是否仍可用。
