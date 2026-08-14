# Review Log · DeepSeek Harness 深度解析

> 阶段5 review-loop 审校记录。停止条件：机械门禁全绿 + 高危确认数清零并保持。证据基准：`repo/deepseek-harness/` 源码优先。

## Round 1 · 机械门禁（自动）

| 门禁 | 结果 | 处置 |
|---|---|---|
| Mermaid 白底板（暗色可读性底线） | **20/20 章达标**，每章 mermaid 块数 = 白底 div 数 | 通过 |
| 过强措辞（最精妙/必然选择/极致/完美…） | 0 命中 | 通过 |
| 承重错误传播（"56 个包"） | **2 处高危**：Ch03、Ch11 | ✅ 已修为 219 |
| 源码引用真实性（190 条唯一路径逐一验证） | **0 造假**；7 条"缺失"均为正则误伤（`...` 省略、`docs/ADR` 泛指、路径缩写、`06-…`/`subagent-…` 截断），逐一核实为真实存在或语境正确 | 通过 |
| 证据等级标注 [verified]/[inferred]/[claimed] | 20/20 章均含，且每章 ≥2 条 ratify-note | 通过 |

**Round 1 确认高危：2（均已修）。**

### 记录在案的可接受偏差（deferred，不再重复 flag）
- **9 章 mermaid 图为 3 张**（02/06/09/10/11/12/17/19/20），低于模板"≥4"软目标。判定：白底板可读性底线 100% 达标，图均有效且配图注；补图边际价值低、成本高。按 review-loop right-sizing 记为可接受偏差，不强行补齐。

## Round 2 · 分级内容审（3 个对抗式 subagent 对照源码，按 Part 切片）

三个 reviewer 各审 Ch01–07 / Ch08–14 / Ch15–20，只报不改；对每条经我**对抗式复核**（打开源码核对）后才进修复 plan。总体：机制描述、git 事实、Agent Note 主计数、竞品对比边界（均挂 [claimed]/[inferred]）经复核**高度准确**；问题集中在少量承重数字与引用行号。

### 确认并已修复

| # | 章 | 级别 | 问题 | 修复 |
|---|---|---|---|---|
| H1 | 11 | 高 | 把 `dsh-shell`（Definition）说成"仅测试用 devDependency"，**反转了"Consumer 依赖 Definition"论点** | 改为：Definition 挂 `peerDependencies`（契约依赖），仅 Provider `dsh-bash-local` 在 devDeps |
| M1 | 20 | 中 | 双语门禁误引 `quality-gates.md:20-22`（该处是覆盖率/knip/lefthook） | 改引真正的翻译配对门禁 `scripts/merge-translation-pairing*.ts` + doc-sync |
| M2 | 20 | 中 | `feature 229 / architecture 153` 被"其中"歧义框定为"活跃之中" | 标明为**跨全状态含归档合计**，并补 implemented 层 170/129 |
| M3 | 19 | 中 | "monorepo（56+ 包）" | 改 219 包 / 49 组 |
| M4 | 07 | 中 | 事件类型"43 种" | 实为 **44**（`known-event-types.ts` 逐条计数），已改 |
| M5 | 05 | 中 | 文末残留工具产物标签 `</content></invoke>` | 已删（Ch20 同样残留，一并删） |
| M6 | 05 | 中 | `:181` 属 `AgentFactory` 接口非"Agent 接口"；`setFactory` 声明在 `:372` 非 `:248` | 已订正表述与行号 |
| M7 | 01 | 中 | acp server 引 `AGENTS.md:42`（实为 interaction 行） | 改 `:41`（正文 + 源码索引） |
| M8 | 10 | 中 | 错误码 `'UNSUPPORTED'` | 实为 `'UNSUPPORTED_OPTION'`（`adapter.ts:278`），已改 |
| M9 | 13 | 中 | "功能性探测会 fail-closed"（单候选链**不探测**，自相矛盾） | 改为：fail-closed 来自执行期 spawn 失败归因，非功能性探测 |
| M10 | 14 | 中 | 首个 flowchart 用 `\n` 换行（mermaid 不解析） | 全部改 `<br/>` |
| M11 | 19 | 中 | "very small team" 引 `CONTRIBUTING.md:11` | 实为 `:12`，已改 |
| — | 11 | 中 | shell provider"三" | 实为 4（bash/pwsh × local/sandbox），已改 |

### 记录在案的低危（deferred，不逐一修）
- 若干二级引用行号"漂移一两行但机制方向正确"（Ch06 `:116`→`:117`、Ch08 `:44-49`→`:24-26`、Ch09 `:490`→`:507`、Ch10 `:98`→`:97`、Ch12 `:35`→`:22-23`、Ch13 `roots.ts:1-70` 文件仅 55 行）。均不影响论断，成本高价值低，记录后不再重复 flag。
- Ch01 "约 47 个组"（按 README 表行计）与实测 49 目录的口径差，已 hedged 且注明方法，保留。

## Round 3 · 复核更新后状态（收敛判定）

机械复核：残留工具标签**清零**；"56 包"仅剩 Ch01 的**有意订正说明**（非错误）；Ch14 mermaid 无裸 `\n`；关键修复（`UNSUPPORTED_OPTION`/`peerDependencies`/`44 种`）全部生效；过强措辞 0。**无回退、无新增确认高/中危。**

**收敛：** Round1 高危 2 → Round2 高危 1 → Round3 高危 **0 并保持**。达成默认停止条件（≥3 轮且高危清零）。

## Round 4 · 收尾补强（应用户要求继续 TODO）

- **图表补齐**：原 9 章仅 3 图的可接受偏差已消除——派 9 个 subagent 各补 1 张不重复的白底 mermaid，现 **20/20 章 ≥4 图，全库 80 张**，白底板 100% 匹配、无裸 `\n`。
- **外链核实**（补 blind-spot #1 的一部分）：WebFetch 核实 HN 主帖存在（"DeepSeek Harness developer preview"，实时 608 分/261 评，作者 tianyicui 参与）；Cordis 论文页无 DeepSeek 署名。HN 分数为移动值，正文按 `[claimed]` 快照对待。
- **论文归属定性**（回答"有没有 DeepSeek 论文"）：`[verified]` 该 harness 引用的唯一论文是 **Cordis 的**《A Programming Paradigm for Spatiotemporal Composability》（cordiverse/Shigma，非 DeepSeek）；commit `0ae8f27b93`（Shigma 本人提交）加了外链并删除内置 `docs/cordis-paper.pdf`。**未发现 DeepSeek 自己关于 harness 的论文**。已写入《全网调研》B 节。

## Blind-spot（诚实残留，交给人）
1. **外部 `[claimed]` 口径未独立核实**：19/20 章及《全网调研》A/D/E/F 节的 HN 反响、体积数字、竞品内部机制、暗涌/ChinaTalk 理念引文，其一手链接不在本地源码内，本轮只核实了"章内标注为 [claimed]/[inferred] 且措辞谨慎"，未核实转述是否失真/过时。建议单独审计《全网调研》的外链。
2. **二级文档（docs/subsystems/*.md、ADR 内文）行号未逐行比对**：抽检约 20 处承重 file:line 全中，但未穷尽；残余"行号漂移"风险集中于未抽中的引用。
3. **Mermaid 仅做语法/白底/比例审，未在渲染器实跑全部 ~80 张图**：白底板 100%、未见语法错，但未逐图渲染。
