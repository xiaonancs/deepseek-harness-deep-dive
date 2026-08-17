# DeepSeek Harness 源码深度解析

## 快速导航

- 📌 [总纲 · 技术主线分析](总纲-DeepSeek-Harness技术主线分析.md) —— 一句话主线、阅读路径、核心机制速览
- 🌐 [全网调研 · 社区认知地图](全网调研-社区认知地图.md) —— 外部基线、Cordis 血缘、公司理念、争议矩阵、盲区分析
- 📚 [Part I 理念与使用](#part-i-理念与使用)
- 🔧 [Part II 源码剖析](#part-ii-源码剖析)
- 🧭 [Part III 对比与元](#part-iii-对比与元)（含 Ch21 参考底座 Cordis 深度对比）
- 📄 [论文导读 · 时空可组合性范式](Appendix/论文导读-时空可组合性范式.md) · 📘 [官方文档对照](Appendix/官方文档对照.md)
- 📎 [Appendix 附录](Appendix/)

## 这份研究是什么

DeepSeek Harness 是 DeepSeek 开源的 agent 运行框架，核心理念是**一切皆插件**——连模型适配器、工具注册表、会话日志、agent loop 本身都是 [Cordis](https://github.com/cordiverse/cordis) 插件，全部可从配置替换。本研究以**一手源码为准**（结论尽量给 `文件:行号`），对"为什么这样设计"类动机保持证据边界（`[verified]`/`[inferred]`/`[claimed]` 三档标注），把承重判断以可审计的 ratify-note 呈现。

## 阅读方式

- **想快速判断值不值得用**：总纲 → Ch01 → Ch19 → Ch20。
- **架构评审者**：Ch02 → Ch05 → Ch11 → Ch06/07 → Ch13 → 各能力域。
- **插件作者**：Ch04 → Ch08/09 → Ch11 → 对应能力域章。
- **AI 工程/研究者**：Ch03 → Ch20 → Ch19。

## 目录

### Part I 理念与使用

| 章 | 标题 | 提要 |
|---|---|---|
| 01 | [项目定位与开发者预览](Part%20I%20Principles%20and%20Usage/01-定位与预览.md) | dsh 是什么、为何以预览姿态开源、运行形态与分层 |
| 02 | [一切皆插件与 Cordis 底座](Part%20I%20Principles%20and%20Usage/02-一切皆插件与Cordis.md) | Context/Service/Plugin/effect 模型与 vendoring |
| 03 | [时空可组合性范式](Part%20I%20Principles%20and%20Usage/03-时空可组合性范式.md) | 可逆 effect / 响应式 coeffect、Koishi 血缘 |
| 04 | [Profile 与 Bundle 组装](Part%20I%20Principles%20and%20Usage/04-Profile与Bundle组装.md) | boot 时分层覆盖组装插件树 |

### Part II 源码剖析

| 章 | 标题 | 提要 |
|---|---|---|
| 05 | [微内核与事件分类法](Part%20II%20Source%20Analysis/05-微内核与事件分类法.md) | waterfall/serial/parallel/emit 四模式 |
| 06 | [Agent Loop 与回合流](Part%20II%20Source%20Analysis/06-AgentLoop与回合流.md) | turn/step 生命周期与容错 |
| 07 | [事件溯源会话日志](Part%20II%20Source%20Analysis/07-事件溯源会话日志.md) | model-visible⟺logged 不变量 |
| 08 | [系统提示词与工具 Schema 组装](Part%20II%20Source%20Analysis/08-系统提示词与Schema组装.md) | prompt-section / tool-schema 组装 |
| 09 | [工具注册表与执行管线](Part%20II%20Source%20Analysis/09-工具注册表与执行管线.md) | 三段 waterfall + guard 卫生 |
| 10 | [LLM 适配器与流式词汇](Part%20II%20Source%20Analysis/10-LLM适配器与流式词汇.md) | StreamChunk + 双适配器孪生 |
| 11 | [能力接缝架构](Part%20II%20Source%20Analysis/11-能力接缝架构.md) | Definition/Provider/Consumer 三角色 |
| 12 | [执行世界 Shell/Subprocess/Terminal](Part%20II%20Source%20Analysis/12-执行世界.md) | 三层执行 + request/spec 显式 resolve |
| 13 | [沙箱与进程约束](Part%20II%20Source%20Analysis/13-沙箱与进程约束.md) | bwrap/Landlock/Seatbelt、steering 立场 |
| 14 | [文件系统、LSP 与代码运行时](Part%20II%20Source%20Analysis/14-文件系统-LSP-代码运行时.md) | fs 策略 / LSP / Code Mode |
| 15 | [编排与委派 Subagent/Workflow/Plan](Part%20II%20Source%20Analysis/15-编排与委派.md) | 委派 / worker 引擎 / plan 状态 |
| 16 | [上下文治理 压缩/注入/Skill](Part%20II%20Source%20Analysis/16-上下文治理.md) | compaction / context / skill / spill |
| 17 | [会话持久化、检索与远程接入](Part%20II%20Source%20Analysis/17-持久化检索与远程接入.md) | 持久化/检索/SDK/ACP/API/Web |
| 18 | [互操作与自我修改](Part%20II%20Source%20Analysis/18-互操作与自我修改.md) | MCP / Hooks / extensions 自指运行时 |

### Part III 对比与元

| 章 | 标题 | 提要 |
|---|---|---|
| 19 | [竞品对比与生态定位](Part%20III%20Comparative%20Analysis/19-竞品对比与生态定位.md) | vs Claude Code / Codex / Pi + 生态理念 |
| 20 | [AI 自举开发与理念映射](Part%20III%20Comparative%20Analysis/20-AI自举开发与理念映射.md) | 12293 commits 轨迹 + 工程纪律 + 公司理念 |
| 21 | [参考底座 Cordis 深度对比](Part%20III%20Comparative%20Analysis/21-参考底座Cordis深度对比.md) | vendored Cordis 源码剖析 + dsh↔Cordis 对比 + 血缘 |

### Appendix 附录

- 📄 [论文导读 · 时空可组合性范式](Appendix/论文导读-时空可组合性范式.md) —— 北大×DeepSeek 论文精读 + 论文↔dsh 逐条映射
- 📘 [官方文档对照](Appendix/官方文档对照.md) —— 官方开发者文档站与本研究的印证/补充/修正
- 📎 [Appendix/](Appendix/) —— 上游、证据等级约定、免责

## 免责

- 附录见 [Appendix/](Appendix/)。外部数据（star 数、HN 分数等）随时间变动，正文一律标 `[claimed]`；与源码冲突时以一手源码为准。
- 本研究为独立第三方技术分析，非 DeepSeek 官方文档。
