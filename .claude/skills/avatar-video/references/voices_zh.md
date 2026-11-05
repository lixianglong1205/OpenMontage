---
name: voices
description: 列出 HeyGen 音色、语言区域及语速/音高配置
---

# HeyGen 音色

HeyGen 提供多种语言、口音与风格的 AI 音色。音色将文本脚本转换为自然流畅的语音。

## 列出可用音色

### curl

```bash
curl -X GET "https://api.heygen.com/v2/voices" \
  -H "X-Api-Key: $HEYGEN_API_KEY"
```

### TypeScript

```typescript
interface Voice {
  voice_id: string;
  name: string;
  language: string;
  gender: "male" | "female";
  preview_audio: string;
  support_pause: boolean;
  emotion_support: boolean;
}

interface VoicesResponse {
  error: null | string;
  data: {
    voices: Voice[];
  };
}

async function listVoices(): Promise<Voice[]> {
  const response = await fetch("https://api.heygen.com/v2/voices", {
    headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! },
  });

  const json: VoicesResponse = await response.json();

  if (json.error) {
    throw new Error(json.error);
  }

  return json.data.voices;
}
```

### Python

```python
import requests
import os

def list_voices() -> list:
    response = requests.get(
        "https://api.heygen.com/v2/voices",
        headers={"X-Api-Key": os.environ["HEYGEN_API_KEY"]}
    )

    data = response.json()
    if data.get("error"):
        raise Exception(data["error"])

    return data["data"]["voices"]
```

## 响应格式

```json
{
  "error": null,
  "data": {
    "voices": [
      {
        "voice_id": "1bd001e7e50f421d891986aad5158bc8",
        "name": "Sara",
        "language": "English",
        "gender": "female",
        "preview_audio": "https://files.heygen.ai/...",
        "support_pause": true,
        "emotion_support": true
      },
      {
        "voice_id": "de8b5d78f2e0485f88d1e9f5c8e7f9a6",
        "name": "Paul",
        "language": "English",
        "gender": "male",
        "preview_audio": "https://files.heygen.ai/...",
        "support_pause": true,
        "emotion_support": false
      }
    ]
  }
}
```

## 支持的语言

HeyGen 支持多种语言，包括：

| 语言 | 代码 | 说明 |
|----------|------|-------|
| 英语（美国） | en-US | 多种音色可选 |
| 英语（英国） | en-GB | 英式口音 |
| 西班牙语 | es-ES | 西班牙西班牙语 |
| 西班牙语（拉丁美洲） | es-MX | 墨西哥西班牙语 |
| 法语 | fr-FR | 法国法语 |
| 德语 | de-DE | 标准德语 |
| 葡萄牙语 | pt-BR | 巴西葡萄牙语 |
| 中文（普通话） | zh-CN | 简体中文 |
| 日语 | ja-JP | 标准日语 |
| 韩语 | ko-KR | 标准韩语 |
| 意大利语 | it-IT | 标准意大利语 |
| 荷兰语 | nl-NL | 标准荷兰语 |
| 波兰语 | pl-PL | 标准波兰语 |
| 阿拉伯语 | ar-SA | 沙特阿拉伯阿拉伯语 |

## 在视频生成中使用音色

### 基本用法

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
        input_text: "Hello! Welcome to our presentation.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### 调整语速

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
        input_text: "This is spoken at a faster pace.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
        speed: 1.2, // 1.0 is normal, range: 0.5 - 2.0
      },
    },
  ],
};
```

### 调整音高

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
        input_text: "This has a higher pitch.",
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
        pitch: 10, // Range: -20 to 20
      },
    },
  ],
};
```

## 使用 Break 标签添加停顿

HeyGen 支持 SSML 风格的 `<break>` 标签，在脚本中加入停顿。

### Break 标签格式

```
<break time="Xs"/>
```

其中 `X` 为秒数（例如 `1s`、`1.5s`、`0.5s`）。

### 要求

| 规则 | 示例 |
|------|---------|
| 使用带 "s" 后缀的秒数 | `<break time="1.5s"/>` ✓ |
| 标签前必须有空格 | `word <break time="1s"/>` ✓ |
| 标签后必须有空格 | `<break time="1s"/> word` ✓ |
| 自闭合标签 | `<break time="1s"/>` ✓ |

**错误：** `word<break time="1s"/>word`（无空格）
**正确：** `word <break time="1s"/> word`

### 示例

```typescript
// Single pause
const script1 = "Hello and welcome. <break time=\"1s\"/> Let me introduce our product.";

// Multiple pauses
const script2 = "First point. <break time=\"1.5s\"/> Second point. <break time=\"1s\"/> Third point.";

// Pause at start (dramatic opening)
const script3 = "<break time=\"0.5s\"/> Welcome to our presentation.";

// Longer pause for emphasis
const script4 = "And the winner is... <break time=\"2s\"/> You!";
```

### 完整示例

```typescript
const scriptWithPauses = `
Welcome to our product demo. <break time="1s"/>
Today I'll show you three key features. <break time="0.5s"/>
First, let's look at the dashboard. <break time="1.5s"/>
As you can see, it's incredibly intuitive.
`;

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
        input_text: scriptWithPauses,
        voice_id: "1bd001e7e50f421d891986aad5158bc8",
      },
    },
  ],
};
```

### 连续 Break

多个连续的 break 标签会自动合并：

```typescript
// These two breaks:
"Hello <break time=\"1s\"/> <break time=\"0.5s\"/> world"

// Are treated as a single 1.5s pause
```

### 最佳实践

1. **用于强调** - 在重要内容前添加停顿
2. **停顿时长合理** - 通常 0.5s 至 2s；过长会显得不自然
3. **贴近自然语流** - 在真人会换气或停顿的位置插入停顿
4. **试听验证** - 收听生成音频，确认节奏是否合适

## 使用自定义音频替代 TTS

除文本转语音外，也可提供自有音频：

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
        type: "audio",
        audio_url: "https://example.com/my-audio.mp3",
      },
    },
  ],
};
```

## 筛选音色

### 按语言

```typescript
function filterByLanguage(voices: Voice[], language: string): Voice[] {
  return voices.filter((v) =>
    v.language.toLowerCase().includes(language.toLowerCase())
  );
}

const englishVoices = filterByLanguage(voices, "english");
const spanishVoices = filterByLanguage(voices, "spanish");
```

### 按性别

```typescript
function filterByGender(voices: Voice[], gender: "male" | "female"): Voice[] {
  return voices.filter((v) => v.gender === gender);
}

const femaleVoices = filterByGender(voices, "female");
```

### 按功能

```typescript
function filterByFeatures(
  voices: Voice[],
  options: { supportPause?: boolean; emotionSupport?: boolean }
): Voice[] {
  return voices.filter((v) => {
    if (options.supportPause !== undefined && v.support_pause !== options.supportPause) {
      return false;
    }
    if (options.emotionSupport !== undefined && v.emotion_support !== options.emotionSupport) {
      return false;
    }
    return true;
  });
}

const expressiveVoices = filterByFeatures(voices, { emotionSupport: true });
```

## 音色选择辅助

```typescript
interface VoiceSelectionCriteria {
  language?: string;
  gender?: "male" | "female";
  supportPause?: boolean;
  emotionSupport?: boolean;
}

async function findVoice(criteria: VoiceSelectionCriteria): Promise<Voice | null> {
  const voices = await listVoices();

  const filtered = voices.filter((v) => {
    if (criteria.language && !v.language.toLowerCase().includes(criteria.language.toLowerCase())) {
      return false;
    }
    if (criteria.gender && v.gender !== criteria.gender) {
      return false;
    }
    if (criteria.supportPause !== undefined && v.support_pause !== criteria.supportPause) {
      return false;
    }
    if (criteria.emotionSupport !== undefined && v.emotion_support !== criteria.emotionSupport) {
      return false;
    }
    return true;
  });

  return filtered[0] || null;
}

// Usage
const voice = await findVoice({
  language: "english",
  gender: "female",
  emotionSupport: true,
});
```

## 多语言视频

可为每个场景使用不同语言：

```typescript
const multiLanguageConfig = {
  video_inputs: [
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hello! Welcome to our global product launch.",
        voice_id: "english_voice_id",
      },
    },
    {
      character: {
        type: "avatar",
        avatar_id: "josh_lite3_20230714",
        avatar_style: "normal",
      },
      voice: {
        type: "text",
        input_text: "Hola! Bienvenidos al lanzamiento global de nuestro producto.",
        voice_id: "spanish_voice_id",
      },
    },
  ],
};
```

## 音色与数字人匹配

### 推荐：使用数字人默认音色

许多数字人带有预匹配的 `default_voice_id`。**这是最佳做法。**

```typescript
// Using v2 API to get avatar with default voice
const response = await fetch(
  "https://api.heygen.com/v2/avatar_group.list?include_public=true",
  { headers: { "X-Api-Key": process.env.HEYGEN_API_KEY! } }
);
const { data } = await response.json();

// Find avatar with a default voice
const avatar = data.avatar_group_list.find((a: any) => a.default_voice_id);

if (avatar) {
  const videoConfig = {
    video_inputs: [{
      character: { type: "avatar", avatar_id: avatar.id },
      voice: {
        type: "text",
        input_text: script,
        voice_id: avatar.default_voice_id, // Pre-matched voice
      },
    }],
  };
}
```

完整示例见 [avatars.md](avatars.md)。

### 备选：手动按性别匹配

若数字人没有默认音色，可手动按性别匹配：

```typescript
interface AvatarVoicePair {
  avatarId: string;
  voiceId: string;
  gender: "male" | "female";
}

async function findMatchingAvatarAndVoice(
  preferredGender?: "male" | "female"
): Promise<AvatarVoicePair> {
  const [avatars, voices] = await Promise.all([
    listAvatars(),
    listVoices(),
  ]);

  // Default to male if no preference
  const gender = preferredGender || "male";

  // Find avatar with matching gender
  const avatar = avatars.find((a) => a.gender === gender);
  if (!avatar) {
    throw new Error(`No ${gender} avatar available`);
  }

  // Find voice with matching gender AND language
  const voice = voices.find(
    (v) => v.gender === gender && v.language.toLowerCase().includes("english")
  );
  if (!voice) {
    throw new Error(`No ${gender} English voice available`);
  }

  return {
    avatarId: avatar.avatar_id,
    voiceId: voice.voice_id,
    gender,
  };
}
```

## 最佳实践

1. **音色性别与数字人一致** - 男声配男性数字人，女声配女性数字人
2. **音色贴合内容** - 商务内容宜选用专业型音色
3. **试听预览** - 选定前先听 preview 音频
4. **考虑区域** - 口音与目标受众一致
5. **自然语速** - 为清晰起见调整语速，通常 0.9–1.1 倍
6. **添加停顿** - 用 SSML break 使语流更自然
7. **校验可用性** - 使用前确认 voice_id 存在
