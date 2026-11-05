---
name: setup-api-key
description: 引导用户为 ElevenLabs MCP 工具配置 ElevenLabs API 密钥。当用户需要配置 ElevenLabs API 密钥、ElevenLabs 工具因缺少 API 密钥而失败，或用户提到需要访问 ElevenLabs 时使用。会先检查 ELEVENLABS_API_KEY 是否已配置且有效，仅在需要时执行完整设置流程。
license: MIT
compatibility: 需要可访问 elevenlabs.io 与 api.elevenlabs.io 的网络。
---

# ElevenLabs API 密钥设置

引导用户获取并配置 ElevenLabs API 密钥。

## 工作流程

### 步骤 0：先检查是否已有 API 密钥

在向用户索取密钥之前，先检查是否已有 `ELEVENLABS_API_KEY`：

1. 检查当前环境中是否存在 `ELEVENLABS_API_KEY`。
2. 若环境中没有，则在 `.env` 中查找 `ELEVENLABS_API_KEY=<value>`。
3. 若找到已有密钥，**验证该密钥**：
   ```
   GET https://api.elevenlabs.io/v1/user
   Header: xi-api-key: <existing-api-key>
   ```
4. **若已有密钥验证成功：**
   - 告知用户 ElevenLabs 已配置且可用
   - 跳过设置流程
   - 询问是否要更换/轮换密钥；若不需要，则结束
5. **若已有密钥验证失败：**
   - 告知用户现有密钥似乎无效或已过期
   - 继续执行步骤 1

### 步骤 1：请求 API 密钥

告知用户：

> 要设置 ElevenLabs，请打开 API 密钥页面：https://elevenlabs.io/app/settings/api-keys
>
> （还没有账号？请先在 https://elevenlabs.io/app/sign-up 注册）
>
> 若你还没有 API 密钥：
> 1. 点击「Create key」
> 2. 为密钥命名（或使用默认名称）
> 3. 设置密钥权限。若你提供的密钥将「User」权限设为「Read」，本技能会自动验证密钥是否可用
> 4. 点击「Create key」确认
> 5. **请立即复制密钥**——密钥只会显示一次！
>
> 准备好后，请在此粘贴你的 API 密钥。

然后等待用户的下一条消息，其中应包含 API 密钥。

### 步骤 2：验证并配置

用户提供了 API 密钥后：

1. **验证密钥**，发起请求：
   ```
   GET https://api.elevenlabs.io/v1/user
   Header: xi-api-key: <the-api-key>
   ```

2. **若验证失败：**
   - 告知用户该 API 密钥似乎无效
   - 请用户重试
   - 提醒密钥页面 URL：https://elevenlabs.io/app/settings/api-keys
   - 若第二次仍失败，显示错误并退出

3. **若验证成功**，将 API 密钥写入 `.env` 文件：
   ```
   ELEVENLABS_API_KEY=<the-api-key>
   ```
   - 若 `.env` 中已有 `ELEVENLABS_API_KEY=...`，则替换该行
   - 否则新增一行 `ELEVENLABS_API_KEY`

4. **确认成功：**
   > 完成！你的密钥已作为环境变量保存在 .env 中
   > 请妥善保管密钥，不要与任何人分享！
