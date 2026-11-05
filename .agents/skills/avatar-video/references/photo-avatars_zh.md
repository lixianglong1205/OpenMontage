---
name: photo-avatars
description: 使用 HeyGen 从照片创建数字人（会说话的照片）
---

# 照片数字人（Talking Photos）

照片数字人可以让静态照片动起来并开口说话。适用于用肖像、头像或任何合适图像制作个性化视频内容。

## 从上传图像创建照片数字人

工作流程：**上传图像 → 创建数字人组 → 用于视频**

### 步骤 1：上传图像

使用资源上传端点上传肖像照片。响应中包含 `image_key`，下一步会用到。

```bash
curl -X POST "https://upload.heygen.com/v1/asset" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: image/jpeg" \
  --data-binary '@./portrait.jpg'
```

响应：
```json
{
  "code": 100,
  "data": {
    "id": "741299e941764988b432ed3a6757878f",
    "name": "741299e941764988b432ed3a6757878f",
    "file_type": "image",
    "url": "https://resource2.heygen.ai/image/.../original.jpg",
    "image_key": "image/741299e941764988b432ed3a6757878f/original.jpg"
  }
}
```

> **重要：** 请保存 `image_key` 字段（不要用 `id`）。`image_key` 是用于创建照片数字人的 S3 路径。

完整上传说明见 [assets.md](assets.md)。

### 步骤 2：创建照片数字人组

使用上传响应中的 `image_key` 创建照片数字人组。系统会处理图像并生成可用的照片数字人。

**端点：** `POST https://api.heygen.com/v2/photo_avatar/avatar_group/create`

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/avatar_group/create" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_key": "image/741299e941764988b432ed3a6757878f/original.jpg",
    "name": "My Photo Avatar"
  }'
```

| 字段 | 类型 | 必填 | 说明 |
|-------|------|:---:|-------------|
| `image_key` | string | ✓ | 上传响应中的 S3 图像键 |
| `name` | string | ✓ | 数字人的显示名称 |
| `generation_id` | string | | 若使用 AI 生成的照片（见下文） |

响应：
```json
{
  "error": null,
  "data": {
    "id": "045c260bc0364727b2cbe50442c3a5bf",
    "image_url": "https://files2.heygen.ai/...",
    "created_at": 1771798135.777256,
    "name": "My Photo Avatar",
    "status": "pending",
    "group_id": "045c260bc0364727b2cbe50442c3a5bf",
    "is_motion": false,
    "business_type": "uploaded"
  }
}
```

`id`（与 `group_id` 相同）即视频生成时使用的 `talking_photo_id`。

### 步骤 3：等待处理

照片数字人初始 `status` 为 `"pending"`，数秒内会变为 `"completed"`。请轮询状态端点：

**端点：** `GET https://api.heygen.com/v2/photo_avatar/{id}`

```bash
curl "https://api.heygen.com/v2/photo_avatar/045c260bc0364727b2cbe50442c3a5bf" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

在用于视频生成前，请等待 `status` 为 `"completed"`。

### 步骤 4：用于视频生成

将照片数字人的 `id` 作为 `talking_photo_id` 使用：

```typescript
const videoConfig = {
  video_inputs: [
    {
      character: {
        type: "talking_photo",
        talking_photo_id: "045c260bc0364727b2cbe50442c3a5bf",
      },
      voice: {
        type: "text",
        input_text: "Hello! This is my photo avatar speaking.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
  dimension: { width: 1920, height: 1080 },
};
```

## TypeScript：完整工作流

```typescript
import fs from "fs";
import path from "path";

interface AssetUploadResponse {
  code: number;
  data: {
    id: string;
    image_key: string;
    url: string;
  };
}

interface PhotoAvatarResponse {
  error: string | null;
  data: {
    id: string;
    group_id: string;
    image_url: string;
    name: string;
    status: string;
    is_motion: boolean;
    business_type: string;
  };
}

async function createPhotoAvatar(
  imagePath: string,
  name: string
): Promise<string> {
  // 1. Upload image
  const resolvedPath = path.resolve(imagePath);
  const fileBuffer = fs.readFileSync(resolvedPath);
  const uploadResponse = await fetch("https://upload.heygen.com/v1/asset", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "image/jpeg",
    },
    body: fileBuffer,
  });

  const uploadJson: AssetUploadResponse = await uploadResponse.json();
  if (uploadJson.code !== 100) {
    throw new Error("Upload failed");
  }

  const imageKey = uploadJson.data.image_key;

  // 2. Create avatar group
  const createResponse = await fetch(
    "https://api.heygen.com/v2/photo_avatar/avatar_group/create",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image_key: imageKey, name }),
    }
  );

  const createJson: PhotoAvatarResponse = await createResponse.json();
  if (createJson.error) {
    throw new Error(createJson.error);
  }

  const photoAvatarId = createJson.data.id;

  // 3. Wait for processing
  await waitForPhotoAvatar(photoAvatarId);

  return photoAvatarId;
}

async function waitForPhotoAvatar(id: string): Promise<void> {
  for (let i = 0; i < 30; i++) {
    const response = await fetch(
      `https://api.heygen.com/v2/photo_avatar/${id}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json: PhotoAvatarResponse = await response.json();

    if (json.data.status === "completed") return;
    if (json.data.status === "failed") {
      throw new Error("Photo avatar processing failed");
    }

    await new Promise((r) => setTimeout(r, 2000));
  }

  throw new Error("Photo avatar processing timed out");
}

async function createVideoFromPhoto(
  photoPath: string,
  script: string,
  voiceId: string
): Promise<string> {
  // 1. Create photo avatar
  const talkingPhotoId = await createPhotoAvatar(photoPath, "Video Avatar");

  // 2. Generate video
  const response = await fetch("https://api.heygen.com/v2/video/generate", {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      video_inputs: [
        {
          character: {
            type: "talking_photo",
            talking_photo_id: talkingPhotoId,
          },
          voice: {
            type: "text",
            input_text: script,
            voice_id: voiceId,
          },
        },
      ],
      dimension: { width: 1920, height: 1080 },
    }),
  });

  const { data } = await response.json();
  return data.video_id;
}
```

## Python：完整工作流

```python
import requests
import os
import time

def create_photo_avatar(image_path: str, name: str) -> str:
    api_key = os.environ["HEYGEN_API_KEY"]

    # 1. Upload image
    with open(image_path, "rb") as f:
        upload_resp = requests.post(
            "https://upload.heygen.com/v1/asset",
            headers={
                "X-Api-Key": api_key,
                "Content-Type": "image/jpeg",
            },
            data=f,
        )

    upload_data = upload_resp.json()
    if upload_data.get("code") != 100:
        raise Exception("Upload failed")

    image_key = upload_data["data"]["image_key"]

    # 2. Create avatar group
    create_resp = requests.post(
        "https://api.heygen.com/v2/photo_avatar/avatar_group/create",
        headers={
            "X-Api-Key": api_key,
            "Content-Type": "application/json",
        },
        json={"image_key": image_key, "name": name},
    )

    create_data = create_resp.json()
    if create_data.get("error"):
        raise Exception(create_data["error"])

    photo_avatar_id = create_data["data"]["id"]

    # 3. Wait for processing
    for _ in range(30):
        status_resp = requests.get(
            f"https://api.heygen.com/v2/photo_avatar/{photo_avatar_id}",
            headers={"X-Api-Key": api_key},
        )
        status = status_resp.json()["data"]["status"]
        if status == "completed":
            return photo_avatar_id
        if status == "failed":
            raise Exception("Photo avatar processing failed")
        time.sleep(2)

    raise Exception("Photo avatar processing timed out")
```

## 列出现有 Talking Photos

获取账户中所有 talking photos：

**端点：** `GET https://api.heygen.com/v1/talking_photo.list`

```bash
curl "https://api.heygen.com/v1/talking_photo.list" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

响应：
```json
{
  "code": 100,
  "data": [
    {
      "id": "ef0ed70f72c6497793e5e36e434d2aea",
      "image_url": "https://files2.heygen.ai/talking_photo/.../image.WEBP",
      "circle_image": ""
    }
  ]
}
```

每个 `id` 均可作为视频生成中的 `talking_photo_id`。

## 向已有组添加照片

向已有数字人组添加更多照片造型：

**端点：** `POST https://api.heygen.com/v2/photo_avatar/avatar_group/add`

```typescript
async function addPhotosToGroup(
  groupId: string,
  imageKeys: string[],
  name: string
): Promise<void> {
  const response = await fetch(
    "https://api.heygen.com/v2/photo_avatar/avatar_group/add",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        group_id: groupId,
        image_keys: imageKeys,
        name,
      }),
    }
  );

  const json = await response.json();
  if (json.error) {
    throw new Error(json.error);
  }
}
```

## 训练照片数字人组

训练数字人组以提升动画质量：

**端点：** `POST https://api.heygen.com/v2/photo_avatar/train`

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/train" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"group_id": "045c260bc0364727b2cbe50442c3a5bf"}'
```

查询训练状态：

**端点：** `GET https://api.heygen.com/v2/photo_avatar/train/status/{group_id}`

## Avatar IV 视频生成

Avatar IV 是 HeyGen 最新的照片数字人技术，画质与动作更自然。可直接从上传图像生成视频，无需创建数字人组。

**端点：** `POST https://api.heygen.com/v2/video/av4/generate`

```bash
curl -X POST "https://api.heygen.com/v2/video/av4/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "image_key": "image/741299e941764988b432ed3a6757878f/original.jpg",
    "script": "Hello! This is Avatar IV with enhanced quality.",
    "voice_id": "1bd001e7e50f421d891986aad5158bc8",
    "video_orientation": "landscape",
    "video_title": "My Avatar IV Video"
  }'
```

| 字段 | 类型 | 必填 | 说明 |
|-------|------|:---:|-------------|
| `image_key` | string | ✓ | 资源上传返回的 S3 图像键 |
| `script` | string | ✓ | 数字人要说的文本 |
| `voice_id` | string | ✓ | 使用的音色 |
| `video_orientation` | string | | `"portrait"`、`"landscape"` 或 `"square"` |
| `video_title` | string | | 视频标题 |
| `fit` | string | | `"cover"` 或 `"contain"` |
| `custom_motion_prompt` | string | | 动作/表情描述 |
| `enhance_custom_motion_prompt` | boolean | | 用 AI 增强动作提示 |

### TypeScript

```typescript
interface AvatarIVRequest {
  image_key: string;
  script: string;
  voice_id: string;
  video_orientation?: "portrait" | "landscape" | "square";
  video_title?: string;
  fit?: "cover" | "contain";
  custom_motion_prompt?: string;
  enhance_custom_motion_prompt?: boolean;
}

interface AvatarIVResponse {
  error: null | string;
  data: {
    video_id: string;
  };
}

async function generateAvatarIVVideo(
  config: AvatarIVRequest
): Promise<string> {
  const response = await fetch(
    "https://api.heygen.com/v2/video/av4/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    }
  );

  const json: AvatarIVResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.video_id;
}
```

### Avatar IV 选项

| 方向 | 尺寸 | 适用场景 |
|-------------|------------|----------|
| `portrait` | 720x1280 | TikTok、Stories |
| `landscape` | 1280x720 | YouTube、网页 |
| `square` | 720x720 | Instagram 信息流 |

| 适配 | 说明 |
|-----|-------------|
| `cover` | 填满画面，可能裁切边缘 |
| `contain` | 完整显示图像，可能露出背景 |

### 自定义动作提示

```typescript
const videoId = await generateAvatarIVVideo({
  image_key: "image/.../original.jpg",
  script: "Let me tell you about our product.",
  voice_id: "1bd001e7e50f421d891986aad5158bc8",
  custom_motion_prompt: "nodding head and smiling",
  enhance_custom_motion_prompt: true,
});
```

## 生成 AI 照片数字人

通过文本描述生成合成照片数字人，而非上传照片。

**端点：** `POST https://api.heygen.com/v2/photo_avatar/photo/generate`

> **重要：8 个字段均为必填。** 缺少任一字段 API 将拒绝请求。
> 当用户要求「生成一位专业男性 AI 数字人」时，你需要询问或选定下面所有字段的值。

### 必填字段（必须全部提供）

| 字段 | 类型 | 允许的值 |
|-------|------|----------------|
| `name` | string | 生成数字人的名称 |
| `age` | enum | `"Young Adult"`, `"Early Middle Age"`, `"Late Middle Age"`, `"Senior"`, `"Unspecified"` |
| `gender` | enum | `"Woman"`, `"Man"`, `"Unspecified"` |
| `ethnicity` | enum | `"White"`, `"Black"`, `"Asian American"`, `"East Asian"`, `"South East Asian"`, `"South Asian"`, `"Middle Eastern"`, `"Pacific"`, `"Hispanic"`, `"Unspecified"` |
| `orientation` | enum | `"square"`, `"horizontal"`, `"vertical"` |
| `pose` | enum | `"half_body"`, `"close_up"`, `"full_body"` |
| `style` | enum | `"Realistic"`, `"Pixar"`, `"Cinematic"`, `"Vintage"`, `"Noir"`, `"Cyberpunk"`, `"Unspecified"` |
| `appearance` | string | 描述外观的文本提示（衣着、情绪、光线等），最多 1000 字符 |

### curl 示例

```bash
curl -X POST "https://api.heygen.com/v2/photo_avatar/photo/generate" \
  -H "X-Api-Key: $HEYGEN_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Sarah Product Demo",
    "age": "Young Adult",
    "gender": "Woman",
    "ethnicity": "White",
    "orientation": "horizontal",
    "pose": "half_body",
    "style": "Realistic",
    "appearance": "Professional woman with a friendly smile, wearing a navy blue blazer over a white blouse, soft studio lighting, clean neutral background"
  }'
```

响应：
```json
{
  "error": null,
  "data": {
    "generation_id": "6a7f7f2795de4599bec7cf1e06babe30"
  }
}
```

### 查询生成状态

**端点：** `GET https://api.heygen.com/v2/photo_avatar/generation/{generation_id}`

响应包含多张生成图像供选择：

```json
{
  "error": null,
  "data": {
    "id": "6a7f7f2795de4599bec7cf1e06babe30",
    "status": "success",
    "image_url_list": [
      "https://resource2.heygen.ai/photo_generation/.../image1.jpg",
      "https://resource2.heygen.ai/photo_generation/.../image2.jpg",
      "https://resource2.heygen.ai/photo_generation/.../image3.jpg",
      "https://resource2.heygen.ai/photo_generation/.../image4.jpg"
    ],
    "image_key_list": [
      "photo_generation/.../image1.jpg",
      "photo_generation/.../image2.jpg",
      "photo_generation/.../image3.jpg",
      "photo_generation/.../image4.jpg"
    ]
  }
}
```

### TypeScript

```typescript
interface GeneratePhotoAvatarRequest {
  name: string;
  age: "Young Adult" | "Early Middle Age" | "Late Middle Age" | "Senior" | "Unspecified";
  gender: "Woman" | "Man" | "Unspecified";
  ethnicity: "White" | "Black" | "Asian American" | "East Asian" | "South East Asian" | "South Asian" | "Middle Eastern" | "Pacific" | "Hispanic" | "Unspecified";
  orientation: "square" | "horizontal" | "vertical";
  pose: "half_body" | "close_up" | "full_body";
  style: "Realistic" | "Pixar" | "Cinematic" | "Vintage" | "Noir" | "Cyberpunk" | "Unspecified";
  appearance: string;
}

interface GeneratePhotoAvatarResponse {
  error: string | null;
  data: {
    generation_id: string;
  };
}

interface PhotoGenerationStatus {
  error: string | null;
  data: {
    id: string;
    status: "pending" | "processing" | "success" | "failed";
    msg: string | null;
    image_url_list?: string[];
    image_key_list?: string[];
  };
}

async function generatePhotoAvatar(
  config: GeneratePhotoAvatarRequest
): Promise<string> {
  const response = await fetch(
    "https://api.heygen.com/v2/photo_avatar/photo/generate",
    {
      method: "POST",
      headers: {
        "X-Api-Key": process.env.HEYGEN_API_KEY!,
        "Content-Type": "application/json",
      },
      body: JSON.stringify(config),
    }
  );

  const json: GeneratePhotoAvatarResponse = await response.json();

  if (json.error) {
    throw new Error(`Photo avatar generation failed: ${json.error}`);
  }

  return json.data.generation_id;
}

async function waitForPhotoGeneration(
  generationId: string
): Promise<string[]> {
  for (let i = 0; i < 60; i++) {
    const response = await fetch(
      `https://api.heygen.com/v2/photo_avatar/generation/${generationId}`,
      { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
    );

    const json: PhotoGenerationStatus = await response.json();

    if (json.error) throw new Error(json.error);

    if (json.data.status === "success") {
      return json.data.image_key_list!;
    }

    if (json.data.status === "failed") {
      throw new Error(json.data.msg ?? "Photo generation failed");
    }

    await new Promise((r) => setTimeout(r, 5000));
  }

  throw new Error("Photo generation timed out");
}
```

### AI 照片 → 数字人组 → 视频

使用 AI 生成的照片创建数字人组，再生成视频：

```typescript
// 1. Generate AI photo
const generationId = await generatePhotoAvatar({
  name: "Product Demo Host",
  age: "Young Adult",
  gender: "Woman",
  ethnicity: "Unspecified",
  orientation: "horizontal",
  pose: "half_body",
  style: "Realistic",
  appearance: "Professional woman, navy blazer, friendly smile, soft lighting",
});

// 2. Wait for generation and pick first result
const imageKeys = await waitForPhotoGeneration(generationId);
const selectedImageKey = imageKeys[0];

// 3. Create avatar group from the AI photo
const createResponse = await fetch(
  "https://api.heygen.com/v2/photo_avatar/avatar_group/create",
  {
    method: "POST",
    headers: {
      "X-Api-Key": process.env.HEYGEN_API_KEY!,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      image_key: selectedImageKey,
      name: "Product Demo Host",
      generation_id: generationId,
    }),
  }
);

const { data } = await createResponse.json();
const talkingPhotoId = data.id;

// 4. Generate video (after status is "completed")
const videoId = await generateVideo({
  video_inputs: [{
    character: {
      type: "talking_photo",
      talking_photo_id: talkingPhotoId,
    },
    voice: {
      type: "text",
      input_text: "Welcome to our product demo!",
      voice_id: "1bd001e7e50f421d891986aad5158bc8",
    },
  }],
  dimension: { width: 1920, height: 1080 },
});
```

### 生成前检查清单

调用 AI 生成 API 前，请确认所有字段均有值：

| # | 字段 | 需询问的问题 / 默认值 |
|---|-------|---------------------------|
| 1 | `name` | 该数字人叫什么？ |
| 2 | `age` | Young Adult / Early Middle Age / Late Middle Age / Senior？ |
| 3 | `gender` | Woman / Man？ |
| 4 | `ethnicity` | 族裔？（见上方枚举） |
| 5 | `orientation` | horizontal（横屏）/ vertical（竖屏）/ square？ |
| 6 | `pose` | half_body（推荐）/ close_up / full_body？ |
| 7 | `style` | Realistic（推荐）/ Cinematic / 其他？ |
| 8 | `appearance` | 描述衣着、表情、光线、背景 |

**若用户仅给出模糊需求**（如「做一个看起来很专业的男人」），请补充缺失字段，或采用合理默认（例如 `"Early Middle Age"`、`"Realistic"` 风格、`"half_body"` 姿势、`"horizontal"` 方向）。

### appearance 提示技巧

`appearance` 为文本提示，请尽量具体：

**好的提示：**
- "Professional woman with shoulder-length brown hair, wearing a light blue button-down shirt, warm friendly smile, soft studio lighting, clean white background"
- "Young man with short black hair, casual tech startup style, wearing a dark hoodie, confident expression, modern office background with plants"

**避免：**
- 模糊描述：如 "a nice person"
- 相互矛盾的属性
- 要求生成特定真实人物

## 管理照片数字人

### 获取照片数字人详情

**端点：** `GET https://api.heygen.com/v2/photo_avatar/{id}`

```typescript
async function getPhotoAvatar(id: string): Promise<PhotoAvatarResponse> {
  const response = await fetch(
    `https://api.heygen.com/v2/photo_avatar/${id}`,
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );
  return response.json();
}
```

### 删除照片数字人

**端点：** `DELETE https://api.heygen.com/v2/photo_avatar/{id}`

```typescript
async function deletePhotoAvatar(id: string): Promise<void> {
  const response = await fetch(
    `https://api.heygen.com/v2/photo_avatar/${id}`,
    {
      method: "DELETE",
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to delete photo avatar");
  }
}
```

### 删除照片数字人组

**端点：** `DELETE https://api.heygen.com/v2/photo_avatar_group/{group_id}`

```typescript
async function deletePhotoAvatarGroup(groupId: string): Promise<void> {
  const response = await fetch(
    `https://api.heygen.com/v2/photo_avatar_group/${groupId}`,
    {
      method: "DELETE",
      headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
    }
  );

  if (!response.ok) {
    throw new Error("Failed to delete photo avatar group");
  }
}
```

## API 参考

| 端点 | 方法 | 说明 |
|----------|--------|-------------|
| `upload.heygen.com/v1/asset` | POST | 上传图像（返回 `image_key`） |
| `/v2/photo_avatar/avatar_group/create` | POST | 从 `image_key` 创建照片数字人 |
| `/v2/photo_avatar/avatar_group/add` | POST | 向已有组添加照片 |
| `/v2/photo_avatar/train` | POST | 训练数字人组 |
| `/v2/photo_avatar/train/status/{group_id}` | GET | 查询训练状态 |
| `/v2/photo_avatar/{id}` | GET | 获取照片数字人详情/状态 |
| `/v2/photo_avatar/{id}` | DELETE | 删除照片数字人 |
| `/v2/photo_avatar_group/{id}` | DELETE | 删除数字人组 |
| `/v2/photo_avatar/photo/generate` | POST | 从文本生成 AI 照片 |
| `/v2/photo_avatar/generation/{id}` | GET | 查询 AI 生成状态 |
| `/v2/video/av4/generate` | POST | 从 `image_key` 生成 Avatar IV 视频 |
| `/v1/talking_photo.list` | GET | 列出所有现有 talking photos |
| `/v2/video/generate` | POST | 使用 `talking_photo_id` 生成视频 |

## 照片要求

### 技术要求

| 方面 | 要求 |
|--------|-------------|
| 格式 | JPEG、PNG |
| 分辨率 | 至少 512x512px |
| 文件大小 | 小于 10MB |
| 面部可见性 | 清晰、正面 |

### 质量指南

1. **光线** - 面部光线均匀、自然
2. **表情** - 中性或轻微微笑
3. **背景** - 简洁、不杂乱
4. **面部位置** - 居中、完整入镜
5. **清晰度** - 锐利、对焦准确
6. **角度** - 正面或轻微侧角

## 最佳实践

1. **使用高质量照片** - 输入越好，输出越好
2. **正面肖像** - 最适合动画
3. **中性表情** - 动画更自然
4. **优先使用 Avatar IV** - 最新一代技术
5. **训练数字人组** - 提升动画质量
6. **复用照片数字人 ID** - 创建后可在多个视频中使用同一 `talking_photo_id`

## 限制

- 照片质量显著影响输出效果
- 侧脸照片支持有限
- 全身照可能无法正确动画
- 部分表情可能不自然
- 处理时间因复杂度而异
