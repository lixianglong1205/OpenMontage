---
name: api-key-setup
description: 如何获取并配置 BFL API 密钥
---

# API 密钥设置

> **重要：** 在尝试生成图像之前，请务必验证你的 API 密钥。缺失或无效的密钥会导致「Not authenticated」错误。

## 快速验证

先运行以下命令，检查密钥是否已配置且有效：

```bash
# Check if key is set
[ -z "$BFL_API_KEY" ] && echo "Error: BFL_API_KEY not set" || echo "OK: Key configured"
```

若未设置，请按下方步骤操作。

## 获取密钥

1. 打开 **https://dashboard.bfl.ai/get-started**
2. 点击 **「Create Key」**
3. 选择组织（若有多个选项，请询问用户）
4. 复制密钥（以 `bfl_` 开头）

## 面向直接调用 API 的 Agent

当当前会话中未设置 `BFL_API_KEY` 时：

1. **检查是否已有 `.env` 文件**：
   ```bash
   grep BFL_API_KEY .env 2>/dev/null
   ```

2. **若已找到，则导出**：
   ```bash
   export BFL_API_KEY=$(grep BFL_API_KEY .env | cut -d '=' -f2)
   ```

3. **若未找到，向用户索取密钥**：
   > 「我需要 BFL API 密钥才能生成图像。请：
   > 1. 打开 https://dashboard.bfl.ai/get-started
   > 2. 点击「Create Key」并复制密钥
   > 3. 将密钥粘贴到这里」

4. **保存并导出**：
   ```bash
   echo 'BFL_API_KEY=bfl_provided_key' >> .env
   echo '.env' >> .gitignore
   export BFL_API_KEY=bfl_provided_key
   ```

此后，在当前会话中即可使用 `$BFL_API_KEY` 进行直接的 curl/API 调用。
