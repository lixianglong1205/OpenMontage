# 安装路径

## 默认路径

| 项目类型 | 默认安装路径                  | 配置项                       |
| --------- | ------------------------------------- | ----------------------------------- |
| Block     | `compositions/<name>.html`            | `hyperframes.json#paths.blocks`     |
| Component | `compositions/components/<name>.html` | `hyperframes.json#paths.components` |

## 路径重映射如何工作

每个条目的 `registry-item.json` 中的 `target` 字段指定默认安装路径。`add` 命令会根据 `hyperframes.json#paths` 重映射路径前缀：

- 以 `compositions/` 开头的 Block 目标会重映射到 `<paths.blocks>/`
- 以 `compositions/components/` 开头的 Component 目标会重映射到 `<paths.components>/`

## hyperframes.json

由 `hyperframes init` 自动创建。若在运行 `add` 时该文件不存在，CLI 会使用默认值创建它：

```json
{
  "$schema": "https://hyperframes.heygen.com/schema/hyperframes.json",
  "registry": "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
  "paths": {
    "blocks": "compositions",
    "components": "compositions/components",
    "assets": "assets"
  }
}
```

## 自定义布局

若要将 Block 安装到 `scenes/` 目录而非 `compositions/`：

```json
{
  "paths": {
    "blocks": "scenes"
  }
}
```

随后 `hyperframes add data-chart` 会写入 `scenes/data-chart.html`，而不是 `compositions/data-chart.html`。片段（snippet）输出会反映重映射后的路径。
