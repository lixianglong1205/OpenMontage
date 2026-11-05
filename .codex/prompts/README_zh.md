# Codex 自定义提示词

Codex 仅从 **`~/.codex/prompts/`**（用户主目录）扫描自定义提示词 —— 它**不会**读取项目级的 `.codex/prompts/`。这些文件在此作为权威来源进行版本管理；若要在 Codex 中使用，请将其复制或符号链接到主目录：

```bash
mkdir -p ~/.codex/prompts
cp .codex/prompts/ink-art.md .codex/prompts/animated-drawing.md ~/.codex/prompts/
# or symlink so repo edits propagate:
# ln -s "$PWD/.codex/prompts/ink-art.md" ~/.codex/prompts/ink-art.md
```

然后重启 Codex；`/ink-art` 和 `/animated-drawing` 会出现在 `/` 菜单中。（OpenAI 正在弃用自定义提示词，转而采用 Codex「skills」——待该方案稳定后再迁移。）
