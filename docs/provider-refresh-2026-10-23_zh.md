# 供应商刷新 — 2026 年 10 月 23 日

在 `codex/provider-refresh-oct23` 分支实现，基于 origin/main `c8066452`。
原始检出及其未提交工作均就地保留。

## 变更

- Google：Omni GA 模型，Google/fal/Replicate 上的 Nano Banana 2.1，仅 Vertex 直连 Veo/Imagen 路由，明确的 Vertex 凭据优先级。
- ElevenLabs：v4 Text to Dialogue 与 Turbo WebSocket 传输；视频转音乐及分轨导入。
- 旁白：xAI TTS、HeyGen 原生与目录音色、Voxtral 3、MAI Voice 2.1/Flash。
- 转换/转写：HeyGen 语音到语音、Voxtral 3 录制转写、MAI 流式转写。
- 图像：BFL/fal/Replicate 上的 FLUX 3，Bria/fal 上的 Fibo 2，MAI Image 2.6/Flash。
- 视频：fal 上的 FLUX 3 Max 与 Vidu Q4，Grok Imagine 1.5/Lite 直连。
- 实时：有界文件运行器及调用方管理的会话传输，用于 Grok Voice 3、Eleven Realtime Mini/Max 与 MAI 转写。无麦克风 UI 或自动工具执行。
- 各宿主 schema 夹具、凭据文档、Agent 指引及离线回归测试。

Kling 4 与实时翻译有意排除。未验证的 Atlas 路由及仅研究用途的模型候选未虚构。

## 审查

独立审查者收到范围、研究计划、实现位置与 API 证据。有效发现经复现或与实现对照后修正：

- 付费生成的完整缓存标识与随机分类。
- 提交前校验输出格式；保留 HeyGen 目录响应及其实际编解码后缀。
- 保留结构化 Grok 格式设置并规范化 MAI 选择器控件。
- 当 API 密钥凭据并存时强制 Vertex 用于 Imagen。
- 规范化 BFL 引用并校验成对尺寸；强制执行 MAI 尺寸限制。
- 生成前拒绝不兼容的 Bria 蒙版。
- 与输入发送并发接收实时事件，对文件使用 Eleven 突发 pacing，并在有限运行器中拒绝工具调用。

审查者确认所有已报告修复，并独立通过当时 26 项供应商测试套件。后续回归覆盖显式 Vertex ADC 路由与 Bria URL 编辑指令映射。

## 验证限制

测试中所有生成请求均为 mock，仓库网络防护仍启用。未执行付费生成、账户权益检查、音色归属检查或主观媒体质量评估。凭据存在仅表示已配置，不代表已验证服务访问。新价格需以当前账户专属报价为准。

精确模型 ID、宿主覆盖、API 参考与设置见[集成指南](../.agents/skills/provider-refresh-oct23/SKILL.md)。

## 最终检查

- 全仓库运行：2,102 通过，5 跳过，3 预期失败；五项失败为过时迁移预期或 mock 签名。
- 更新上述测试后，对所有受影响模块与供应商回归的最终重跑通过：**179 通过**（含此前五项失败用例及 28 项新供应商测试）。
- 必需编译检查通过；所有变更/新增 Python 文件已编译。`git diff --check` 通过。
- 测试夹具更新后未第二次跑完整套件；受影响模块已全量重跑。

## 与最新 main 集成

合并 origin/main `0f191f96`，四处重叠的 Gemini Omni 冲突以保留 main 的稳定适配器、更严请求校验、按用量定价、下载恢复、文档与扩展测试的方式解决。供应商刷新新增内容保持完整。

合并后验证：**218 通过**，覆盖 Gemini Omni、新供应商、Google/ElevenLabs 迁移、缓存标识与 phase-three 注册表契约。Python 编译与暂存 diff 检查亦通过。
