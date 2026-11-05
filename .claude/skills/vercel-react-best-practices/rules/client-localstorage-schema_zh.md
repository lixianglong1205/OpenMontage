---
title: 为 localStorage 数据做版本化并最小化存储
impact: MEDIUM
impactDescription: 避免 schema 冲突，减小存储体积
tags: client, localStorage, storage, versioning, data-minimization
---

## 为 localStorage 数据做版本化并最小化存储

为键名添加版本前缀，且只保存所需字段。可避免 schema 冲突，并防止误存敏感数据。

**错误示例：**

```typescript
// No version, stores everything, no error handling
localStorage.setItem('userConfig', JSON.stringify(fullUserObject))
const data = localStorage.getItem('userConfig')
```

**正确示例：**

```typescript
const VERSION = 'v2'

function saveConfig(config: { theme: string; language: string }) {
  try {
    localStorage.setItem(`userConfig:${VERSION}`, JSON.stringify(config))
  } catch {
    // Throws in incognito/private browsing, quota exceeded, or disabled
  }
}

function loadConfig() {
  try {
    const data = localStorage.getItem(`userConfig:${VERSION}`)
    return data ? JSON.parse(data) : null
  } catch {
    return null
  }
}

// Migration from v1 to v2
function migrate() {
  try {
    const v1 = localStorage.getItem('userConfig:v1')
    if (v1) {
      const old = JSON.parse(v1)
      saveConfig({ theme: old.darkMode ? 'dark' : 'light', language: old.lang })
      localStorage.removeItem('userConfig:v1')
    }
  } catch {}
}
```

**仅保存服务端响应中的必要字段：**

```typescript
// User object has 20+ fields, only store what UI needs
function cachePrefs(user: FullUser) {
  try {
    localStorage.setItem('prefs:v1', JSON.stringify({
      theme: user.preferences.theme,
      notifications: user.preferences.notifications
    }))
  } catch {}
}
```

**始终用 try-catch 包裹：** 在无痕/隐私浏览（Safari、Firefox）、配额超限或 storage 被禁用时，`getItem()` 与 `setItem()` 会抛出异常。

**收益：** 通过版本化实现 schema 演进、减小存储体积，并避免保存 token、PII（个人可识别信息）或内部标志位。
