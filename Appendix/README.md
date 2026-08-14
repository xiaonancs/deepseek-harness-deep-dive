# Appendix · 附录

补充资料与研究元信息。

## 源码基线

本研究基于 DeepSeek Harness 源码快照（见仓库根目录 `repo/deepseek-harness/`）：

- 上游：https://github.com/deepseek-ai/deepseek-harness
- 版本：`0.1.0-rc.5`（developer preview）
- 提交区间：2026-06-10 → 2026-08-13（12,293 commits，5,610 merges）
- 规模：219 个 `@deepseek-ai/dsh-*` workspace 包（49 个功能组）、7,412 版本内文件
- 研究日：2026-08-14

## 研究方法与产物

- 工作流：`git-repo-deepresearch`（含内嵌的 **ratify-loop** 判断可信闸与 **review-loop** 分级收敛审校闸）。
- 章节配置：[../scripts/chapters.yaml](../scripts/chapters.yaml)
- 章节生成规范（七维 + ratify-note + mermaid 白底板）：[../scripts/prompt-template.md](../scripts/prompt-template.md)
- 审校记录：[../review/review-log.md](../review/review-log.md)

## 证据等级约定

- `[verified]` 源码可证（附 file:line）
- `[inferred]` 合理推断（有据但非直证）
- `[claimed]` 仅社区/二手口径（star 数、HN 分数、竞品对比等）

对源码无法证明的动机（"为什么这样设计""语言选型""团队意图"），一律用「可能/或许/不排除」，并以 ratify-note 呈现候选与残余风险。

## 免责

本研究为独立第三方技术分析，非 DeepSeek 官方文档。外部数据随时间变动；与源码冲突时以一手源码为准。
