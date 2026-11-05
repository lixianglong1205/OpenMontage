---
name: quota
description: HeyGen 的积分体系、使用限额及剩余配额查询
---

# HeyGen 配额与积分

HeyGen 采用基于积分的视频生成计费方式。了解配额管理有助于避免视频生成请求失败。

## 查询剩余配额

### curl

```bash
curl -X GET "https://api.heygen.com/v2/user/remaining_quota" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface QuotaResponse {
  error: null | string;
  data: {
    remaining_quota: number;
    used_quota: number;
  };
}

const response = await fetch("https://api.heygen.com/v2/user/remaining_quota", {
  headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
});

const { data }: QuotaResponse = await response.json();
console.log(`Remaining credits: ${data.remaining_quota}`);
```

### Python

```python
import requests
import os

response = requests.get(
    "https://api.heygen.com/v2/user/remaining_quota",
    headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
)

data = response.json()["data"]
print(f"Remaining credits: {data['remaining_quota']}")
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "remaining_quota": 450,
    "used_quota": 50
  }
}
```

## 积分消耗

不同操作消耗的积分数量不同：

| 操作 | 积分成本 | 说明 |
|-----------|-------------|-------|
| 标准视频（1 分钟） | 约每分钟 1 积分 | 因分辨率而异 |
| 720p 视频 | 基础费率 | 标准画质 |
| 1080p 视频 | 约为基础费率的 1.5 倍 | 更高画质 |
| 视频翻译 | 不定 | 取决于视频时长 |
| 流式数字人 | 按会话计费 | 实时使用 |

## 生成前配额检查

生成视频前务必确认配额充足：

```typescript
async function generateVideoWithQuotaCheck(videoConfig: VideoConfig) {
  // Check quota first
  const quotaResponse = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data: quota } = await quotaResponse.json();

  // Estimate required credits (rough estimate: 1 credit per minute)
  const estimatedMinutes = videoConfig.estimatedDuration / 60;
  const requiredCredits = Math.ceil(estimatedMinutes);

  if (quota.remaining_quota < requiredCredits) {
    throw new Error(
      `Insufficient credits. Need ${requiredCredits}, have ${quota.remaining_quota}`
    );
  }

  // Proceed with video generation
  return generateVideo(videoConfig);
}
```

## 配额管理最佳实践

### 1. 定期监控用量

```typescript
async function logQuotaUsage() {
  const response = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data } = await response.json();

  console.log({
    remaining: data.remaining_quota,
    used: data.used_quota,
    percentUsed: (
      (data.used_quota / (data.remaining_quota + data.used_quota)) *
      100
    ).toFixed(1),
  });
}
```

### 2. 设置告警

```typescript
const QUOTA_WARNING_THRESHOLD = 50;

async function checkQuotaWithAlert() {
  const response = await fetch(
    "https://api.heygen.com/v2/user/remaining_quota",
    { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
  );

  const { data } = await response.json();

  if (data.remaining_quota < QUOTA_WARNING_THRESHOLD) {
    // Send alert (email, Slack, etc.)
    await sendAlert(`Low HeyGen quota: ${data.remaining_quota} credits remaining`);
  }

  return data;
}
```

### 3. 开发时使用测试模式

若可用，开发阶段请使用测试模式，以免消耗积分：

```typescript
const videoConfig = {
  test: true, // Use test mode during development
  video_inputs: [...],
};

// Test videos may have watermarks but don't consume credits
```

## 订阅档位

不同订阅档位对应的配额额度和功能不同：

| 档位 | 功能 |
|------|----------|
| Free | 积分有限，基础功能 |
| Creator | 更多积分，标准数字人 |
| Team | 更高限额，团队协作 |
| Enterprise | 自定义限额、API 访问、优先支持 |

API 访问通常需要 Enterprise 档位或更高。

## 配额相关错误处理

```typescript
async function handleQuotaError(error: any) {
  if (error.message.includes("quota") || error.message.includes("credit")) {
    console.error("Quota exceeded. Consider:");
    console.error("1. Upgrading your subscription");
    console.error("2. Waiting for quota reset");
    console.error("3. Purchasing additional credits");

    // Check current quota
    const quota = await getQuota();
    console.error(`Current remaining: ${quota.remaining_quota}`);
  }

  throw error;
}
```
