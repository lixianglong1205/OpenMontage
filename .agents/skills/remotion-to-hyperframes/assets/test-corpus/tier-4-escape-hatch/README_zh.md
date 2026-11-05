# Tier 4 — escape-hatch

## 测试内容

T4 是**仅 lint** 层级。没有可 diff 的渲染输出——技能是否合格，取决于它能否正确*拒绝*翻译各用例（并推荐 PR #214 中的运行时互操作模式），或在合适情况下于去掉 warning 级装饰后再翻译。

每个 `cases/*.tsx` 文件都是展示某一特定模式的最小 Remotion composition。技能应：

1. 对源码运行 `scripts/lint_source.py`。
2. 将该用例的 JSON 输出与 `expected.json` 比对。
3. 执行文档中的 `skill_action`：
   - `refuse_translation_recommend_interop` — 输出理由 + PR #214 互操作指南链接；不要生成 HF 输出。
   - `drop_lambda_code_translate_remainder_if_clean` — 去掉 `@remotion/lambda` 相关代码并附说明；仅当没有其他 blocker 时再翻译其余部分。
   - `translate_after_dropping_wrappers` — 正常翻译；去掉 `useCallback` / `useMemo` / `delayRender` 包装。
   - `inline_hook_body_if_pure` — 若自定义 hook 仅为 `useCurrentFrame` 的纯派生，则内联其函数体；否则退出。

## 用例

| #   | File                       | 预期发现                            | 说明                                           |
| --- | -------------------------- | ----------------------------------- | ----------------------------------------------- |
| 01  | `01-use-state.tsx`         | blocker `r2hf/use-state`            | useState 驱动动画                      |
| 02  | `02-use-effect-deps.tsx`   | blocker `r2hf/use-effect-deps`      | 带非空 deps 的 useEffect/useLayoutEffect   |
| 03  | `03-async-metadata.tsx`    | blocker `r2hf/async-metadata`       | calculateMetadata 返回 Promise             |
| 04  | `04-third-party-react.tsx` | blocker `r2hf/third-party-react-ui` | 导入 `@mui/material`                         |
| 05  | `05-lambda-config.tsx`     | warning `r2hf/lambda-import`        | 导入 `@remotion/lambda` — 去掉后翻译  |
| 06  | `06-warnings-only.tsx`     | 仅 warnings                       | delayRender / useCallback / useMemo             |
| 07  | `07-custom-hook.tsx`       | warning `r2hf/custom-hook`          | 本地定义的 `useFadeIn`（export const 形式） |
| 08  | `08-mixed.tsx`             | 3 个 blocker + 1 个 warning              | 聚合发现结果测试                         |

## 验证

```bash
./validate.sh
```

该脚本对每个用例运行 `lint_source.py` 并断言：

- 每个预期 blocker 规则以 `blocker` 严重级别触发。
- 每个预期 warning 规则以 `warning`（或更高）严重级别触发。
- 当预期存在 blocker 时，`lint_source.py` 的退出码为 1，否则为 0。

当每个用例与其预期输出一致时，T4 通过。不涉及渲染。
