# 论文导读：时空可组合性范式

> 读完能回答：一篇北大 × DeepSeek 的论文，怎么把编程语言理论里的 effect / coeffect「搬到运行时」，用来解释"插件热插拔为什么这么难做对"？它和本仓库解析的 DeepSeek Harness（下称 dsh）又是什么关系？

如果你写过 VSCode 插件，或维护过任何"能装能卸"的插件系统，大概踩过这样的坑：装一个扩展改了一堆全局状态，卸载时却收不干净，最后只能重启进程了事；想让插件 A 依赖插件 B 提供的能力，却发现依赖关系要么写不出来、要么没有类型。这两件看似不相干的麻烦事，被这篇论文归纳成同一个理论问题的两个面。本篇导读带你快速吃透它，并把它和 dsh 的源码机制逐一对上。

---

## 一、论文核心与元信息

**标题**：《A Programming Paradigm for Spatiotemporal Composability》（一种面向时空可组合性的编程范式）

**作者与单位**：Yifan Shi¹²、Wei Zhang¹、Tianyi Cui²。其中 ¹ 为 **Peking University（北京大学）**，² 为 **DeepSeek-AI**。这是一篇学术界与工业界合著的论文——理论骨架来自北大，工程验证来自 DeepSeek 一侧的实践者。

**TL;DR（一句话）**：现代软件（从插件系统到 self-evolving agent harness）越来越需要"动态组合"——组件在运行时来了又走——但它的形式基础一直没打牢。论文把编程语言理论里两个经典概念**提升为运行时机制**：把描述"计算如何修改环境"的 **effect** 提升成**可逆的**（revertible），把描述"计算如何依赖环境"的 **coeffect** 提升成**响应式的**（reactive），从而得到一套语言无关、可落地的动态组合范式，并在名为 **Cordis** 的元框架里实现、在拥有 4000+ 社区插件的 **Koishi** 平台上验证。

**为什么值得读**：它给"热插拔为什么难"提供了一套精确的词汇。以前我们只能含糊地说"卸载没收干净""依赖没管好"；这篇论文把前者定义为 **temporal composability**（时间维：卸载时能否完全回滚副作用），把后者定义为 **spatial composability**（空间维：能否声明式地、响应式地管理组件间依赖）。两个维度正交，各自对应 effect 与 coeffect。

**开篇动机（§1）**：论文用 VSCode 插件生态做实证切入。

- **时间维的局限**：扩展一旦加载，其可执行代码无法在运行时卸载——作者统计 top100 扩展中有 **87 个**包含可执行代码、需要重启才能真正卸下。
- **空间维的局限**：扩展间依赖几乎无法表达——top100 中仅 **7 个**声明了 `extensionDependencies`，而拿到别的扩展导出的 API（`getExports`）时**没有类型**。
- 现实里大家的"粗粒度绕过"（coarse-grained workaround）就是重启进程 / 容器：一个模块行为异常就重启整个进程，一个服务依赖就交给编排器管。代价很大——重启会丢掉进程内所有累积状态（缓存、连接、部分计算），重建要数秒到数分钟；为了维持可用性还得堆冗余副本。论文点名 **self-evolving agent harness**（会自我改写、替换自身组件的智能体运行时）是这一需求最尖锐的新场景。

**四条贡献（§1.3，与 PDF 第 6 页逐条核对一致）**：

1. **形式化 revertible effects（§3.1）**：每个 context 变换都配一个显式的逆函数，使得 effect tracking 与 recovery 成为**保持组合运算**的操作，从而保证组件移除时**完全的状态恢复**。这是动态时间可组合性的代数基础。
2. **形式化 reactive coeffects（§3.2）**：组件把自己的需求声明为一个 typed dependency set，一套基于"满足性"的通知机制自动把状态变迁分类为 **activating / deactivating / neutral**（激活 / 去激活 / 中性）。这是动态空间可组合性的代数基础。
3. **建立 component lifecycle 模型（§3.3）**并把 effect context 与 coeffect context 整合为**统一的 context type（§3.4）**，构成一套可动态组合的编程范式。
4. **在 Cordis 中实现（§4）**：一个"时空可组合性元框架"，含 core library（effect tracking + coeffect resolution）与 declarative component loader（config reconciliation + hot module replacement / 热模块替换）；并以 **Koishi** 聊天机器人平台（4000+ 生产环境社区插件）做案例研究验证。

---

## 二、逐节精读（含关键公式与四图重绘）

论文共 7 节：1 Introduction、2 Preliminaries、3 核心形式化、4 实现与案例、5 Discussion、6 Related Work、7 Conclusion。这里聚焦第 2、3 节的形式化骨架——这是全文最硬也最值钱的部分。

### 2.1 Preliminaries：effect 与 coeffect 的经典分工（§2）

一句话对齐术语：**effect 描述"计算怎样改变环境"，coeffect 描述"计算怎样依赖环境"**。前者的判断形如 $\Gamma\vdash t:T_{\text{effect}}$（可用 monadic 方式，或 algebraic effects + handlers 建模）；后者形如 $\Gamma_{\text{coeffect}}\vdash t:T$。经典理论里这两者都是**编译期、静态、作用于词法固定作用域**的分析——恰恰不覆盖"组件运行时来去"的动态场景。论文接下来做的，就是把这两者各自"提升"到运行时。

### 2.2 Revertible effects：给每个副作用配一个"撤销键"（§3.1）

**核心直觉**：普通的副作用是"泼出去的水"；可逆 effect 要求你在泼水的同时，把"怎么把水收回来"也一并记下来。

论文把 effect context 定义为原状态空间与一族"恢复变换"的乘积：

$$\partial\Gamma := \Gamma \times \mathfrak{F}_\Gamma$$

它的元素是一个 pair $(\gamma,\varphi)$，其中 $\gamma$ 是**当前状态**，$\varphi$ 是**能把状态恢复到初始态的变换**。配套两个操作：`track`（累积新的副作用及其逆）与 `recover`（把 $\varphi$ 应用到 $\gamma$ 上、并将 $\varphi$ 重置为恒等 $\text{id}$）。

一个"effect 函数"被定义为**同时返回新状态和自身的逆**：

$$\mathfrak{E}_\Gamma := \Gamma \to \Gamma \times (\Gamma \to \Gamma)$$

多个 effect 用组合算子 $\diamond$ 串起来时，论文证明 effect tracking 保持这个组合运算——**这正是"完全可恢复"的代数保证**：无论中间叠加了多少层副作用，逆的组合总能精确地退回原点。

打个比方：可逆 effect 像给每一步操作都留了一张"回执"，撤销时按回执逆序作废即可，不必猜"当初到底改了什么"。对使用者来说，这就是"卸载一个组件 = 它从没来过"的底气。

### 2.3 Reactive coeffects：把"我需要什么"变成会被自动通知的声明（§3.2）

coeffect context 被建模为一个**依赖偏函数**（partial function，只对已提供的 key 有定义）：

$$\Sigma := (k:K) \rightharpoonup \mathcal{V}_k$$

配 `get` / `set` 两个操作。**关键洞见**：`set(k,v)` 本身就是 $\Sigma$ 上的一个 effect 函数——也就是说"coeffect 操作即 effect，而 effect 可逆"。这一句把空间维和时间维缝到了一起：管理依赖所引发的状态变化，天然享有可逆性。

组件声明的依赖集 $d$ 是否被满足，由一个满足谓词判定：

$$\sigma \vDash d := \forall k \in d.\; k \in \mathrm{dom}(\sigma)$$

当 context 从 $\sigma$ 变到 $\sigma'$，通知机制 $\mathrm{notify}_d(\sigma,\sigma')$ 会把这次变迁分成三类：

- **activating**：之前不满足、现在满足 → 该激活组件；
- **deactivating**：之前满足、现在不满足 → 该卸载组件；
- **neutral**：满足性没变 → 无需动作。

**一个漂亮的涌现结果**：正确的**空间依赖序**——依赖者必须"在被依赖者之后激活、在被依赖者之前卸载"——不需要专门写调度逻辑，它从 notify 的定义里**自然涌现**。

论文还给了两个进阶结构，dsh 里都能找到对应：

- **isolation realm $\Sigma^{iso}$**：同一个 key 在不同 realm 里解析出不同的值 → 相当于**运行时的 ad-hoc 多态**，用于多租户、测试、沙箱。
- **interception $\Sigma^{inter}$**：对依赖访问附加横切元数据（例如给文件系统访问加"哪些路径可读可写"的策略）；采用**右偏合并**，让外层 context 能"约束"组件而**不必改动组件本身**。类比：像给插座加一个限流保护套，灯泡不用换。

### 2.4 组件生命周期与四张图（§3.3）

论文用一个**统一的 context 类型**把上述一切收口。组件被定义为依赖与 effect 的乘积再加一份可变生命周期态：

$$\mathfrak{C}_\Gamma := \mathfrak{D}_\Gamma \times \mathfrak{E}_\Gamma$$

而全局统一 context 是一个自相似的递归类型：

$$\Gamma_\infty := \mu\Gamma.\; \Gamma \times (\Gamma \to \Gamma) \times \Sigma$$

它自我嵌套（$\Sigma$ 里又装着 context），且 $\Sigma$ **subsumes 一切共享可变态**——一个类型统吃状态、逆、依赖。论文还区分了两种实现风格：**in-place**（原地修改、逆函数非平凡）与 **derived**（返回新 context、逆就是丢弃该 id 对应的派生物，恢复即"扔掉"）。

下面用白底 mermaid 重绘论文的四张图。

#### 图 1：base lifecycle（组件基础生命周期，对应论文 Fig.1）

<div style="background: #ffffff !important; background-color: #ffffff !important; padding: 16px; border-radius: 8px; margin: 16px 0;" bgcolor="#ffffff">

```mermaid
%%{init: {'theme':'neutral'}}%%
stateDiagram-v2
    [*] --> INACTIVE
    INACTIVE --> ACTIVE: RELOAD (依赖满足)
    ACTIVE --> INACTIVE: UNLOAD (依赖失效 / 主动卸载)
    ACTIVE --> ACTIVE: 运行中
    INACTIVE --> [*]: 销毁
```

</div>

<p>图注：组件的基础生命周期只有两个稳定态——INACTIVE 与 ACTIVE；两条迁移动作 RELOAD 与 UNLOAD 分别对应 coeffect 通知里的 activating 与 deactivating。UNLOAD 触发时执行可逆 effect 的逆，把副作用完全回滚。</p>

#### 图 2：iterative transition（可中断的多步迁移，对应论文 Fig.2）

<div style="background: #ffffff !important; background-color: #ffffff !important; padding: 16px; border-radius: 8px; margin: 16px 0;" bgcolor="#ffffff">

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart LR
    S0([开始迁移]) --> A[step 1]
    A -.->|step 边界: 天然中断点| B[step 2]
    B -.->|step 边界| C[step 3]
    C --> E([迁移完成])
    A -.->|收到中断| X([挂起 / 撤回])
    B -.->|收到中断| X
```

</div>

<p>图注：一次组件迁移被拆成若干 step，step 之间的边界是天然的可中断点。论文把这套多步执行刻画为 reified delimited continuation（被具体化的定界续延），它正对应主流语言里的 yield——迁移可以在 step 边界暂停、撤回或重来。</p>

#### 图 3：epoch 版本化目标态（星形拓扑，对应论文 Fig.3）

<div style="background: #ffffff !important; background-color: #ffffff !important; padding: 16px; border-radius: 8px; margin: 16px 0;" bgcolor="#ffffff">

```mermaid
%%{init: {'theme':'neutral'}}%%
flowchart TD
    E["epoch 目标态<br/>ε_d(σ) = 依赖当前取值快照"]
    E --> D1[依赖 k1]
    E --> D2[依赖 k2]
    E --> D3[依赖 k3]
    D1 --> I1[INACTIVE 分支]
    D2 --> I2[INACTIVE 分支]
    D3 --> I3[INACTIVE 分支]
```

</div>

<p>图注：epoch 定义为 ε_d(σ) := ⟨σ(k) | k ∈ d⟩——把依赖集当前取值打包成一个"版本号"。组件持有的 epoch 与最新 epoch 不一致，即说明目标态已陈旧、需要 reload。星形结构里每条依赖各配一条分支通向 INACTIVE，任一依赖失效都能独立触发去激活。</p>

#### 图 4：inertial state machine（惯性态处理异步，对应论文 Fig.4）

<div style="background: #ffffff !important; background-color: #ffffff !important; padding: 16px; border-radius: 8px; margin: 16px 0;" bgcolor="#ffffff">

```mermaid
%%{init: {'theme':'neutral'}}%%
stateDiagram-v2
    [*] --> INACTIVE
    INACTIVE --> RELOAD: 目标=激活
    RELOAD --> ACTIVE: 跑完再响应新目标
    ACTIVE --> UNLOAD: 目标=卸载
    UNLOAD --> INACTIVE: 跑完再响应新目标
    RELOAD --> RELOAD: 惯性态: 新目标先记账
    UNLOAD --> UNLOAD: 惯性态: 新目标先记账
```

</div>

<p>图注：异步是热插拔的头号敌人——组件还在加载途中，目标态又变了怎么办？论文把 RELOAD / UNLOAD 提升为"惯性态"（inertial states）：正在进行的迁移必须跑完，才去响应最新目标态，避免半途切换导致状态错乱。这是把图 1 的两态机在异步世界里做的加固。</p>

### 2.5 与既有范式的对照（§3.4.2）

论文明确把自己和两类主流做法做了对比：

- **vs 函数式 State monad**：monad 需要显式地把状态"穿线"（threading）过每一步，人体工学差；可逆 effect 把逆藏在 context 里，调用方无感。
- **vs 命令式 / OOP 的隐式变更**：React 的 `useEffect` 靠"调用顺序"隐式建立依赖与清理，脆弱；Spring 的 `getBean` 靠运行时反射拿依赖，无类型、无生命周期协调。可逆 effect + 响应式 coeffect 把这些都显式化、可追踪化。

### 2.6 实现与案例（§4）、讨论（§5）要点

**Cordis / Koishi（§4.3）**：Koishi 建立在 Cordis 之上（Koishi 用 v3，本文形式化对应 v4）；论文直言"**Koishi 的 plugin 就是本文说的 component**"。Koishi 有两个独立运行时——服务端 bot 与浏览器里的 web console——都跑在 Cordis 上。作者诚实标注了 threats to validity：这是**单生态、单语言**的验证，性质上是 "existence-and-adoption"（存在性与被采用度）而非定量基准。

**Discussion（§5）**几个值得记住的点：

- **§5.1 service multiplexing**：从 exclusive binding（独占绑定）走向 service broker（服务代理），后者能支撑负载均衡、滚动更新、跨进程调用。
- **§5.2 access control**：`inject` 是"能力请求"，context proxy 是"能力中介"，因而**静态可审批**；interception 做细粒度策略（如 fs 元数据）。但论文态度很诚实：**沙箱化不可信组件，需要语言之外的执行边界**（SFI、隔离运行时、沙箱进程、虚拟容器），经由 bridge 接入。
- **§5.3 语言无关性**：时间维需要 closures + 运行时可引入 / 撤回模块（managed 语言用模块注册表、native 用 `dlopen`/`dlclose`、wasm 看 embedder）；空间维需要依赖注入（类型层用 typeclass / trait / TS module augmentation，运行时用 Proxy / `__get__` / 反射）。
- **§5.4 相互依赖**：出现环 → 静态可预测的"永久 INACTIVE"，而**非死锁**；可分解为单向绑定，代价是组件数增多，用 bundling / 约定接线 / 脚手架缓解。
- **§5.5 依赖类型与版本**：key 靠名义链接会有 interface drift、key collision；三条出路——key namespacing / peer dependencies（Cordis 现用）/ structural compatibility。

---

## 三、论文 ↔ dsh 深度映射（本导读重点）

这一节是本导读的核心：把论文的每个形式化概念，对上 dsh 源码里的具体机制。dsh 侧均标注章号 / 文件与**证据等级**（[verified] 源码可查实、[inferred] 有据推断）。

### 3.1 revertible effects ↔ dsh 的 effect / disposer 体系

论文的"每个 effect 配显式逆、组件移除时完全回滚"，在 dsh 里是**一等机制**：`ctx.effect()` 返回一个 disposer；fiber 在卸载时按 `_disposables` **反序**逐个调用 disposer，精确回退。dsh 的 AGENTS.md 甚至把它立成铁律——**"Registrations are effects"（一切注册皆副作用，故必须可撤销）**。见 Ch02 / Ch03 [verified]。

这与论文 $\mathfrak{E}_\Gamma$ 返回"新态 + 自身逆"、组合算子 $\diamond$ 保持可逆的代数结构，是**同一个东西的两种表述**——论文给形式，dsh 给运行时实现。

### 3.2 reactive coeffects ↔ dsh 的 inject + fiber epoch

论文的 typed dependency context 与满足性通知，对应 dsh 的 `inject`（声明依赖）+ fiber 的 epoch 机制（`_setEpoch` / `_refresh`），以及 PENDING ↔ ACTIVE 的状态切换。见 Ch03 / Ch05 / Ch11。

- **notify 的 activating / deactivating** ↔ epoch 变化触发 dsh 的 `_reload` / `_unload`。依赖刚满足 → `_reload` 激活；依赖失效 → `_unload` 卸载并回滚。
- 论文的 **epoch $\varepsilon_d(\sigma)$**（图 3）直接对应 dsh fiber 里同名的 epoch 概念——用版本号检测"目标态是否陈旧"。

### 3.3 idempotent guard 与 effect iterator

- **idempotent guard `idem`** ↔ dsh 的幂等 disposer（Ch03 §4.1 [verified]）：返回的 partial disposer 只生效一次，重复调用无害；generative 版本每次给新 handle。
- **effect iterator** ↔ dsh 的 turn / step 边界（Ch06）。论文把多步迁移刻画为可中断的 delimited continuation，dsh 的一个 turn / step 边界正是这种天然中断点。此处为**类比 [inferred]**——dsh 未必显式实现 continuation，但结构同构。

### 3.4 isolation realm 与 interception

- **isolation realm $\Sigma^{iso}$** ↔ Cordis 的 `isolate` realm / dsh 的 per-session preset（Ch04 / Ch11）：同一 key 在不同 realm 解析不同值，用于多会话隔离。
- **interception $\Sigma^{inter}$**（右偏合并、外层约束组件）↔ dsh 的多处横切策略：fs-observation-policy（Ch14）、sandbox policy（Ch13）、以及 waterfall（Ch05 / Ch09）。这些都是"外层 context 给组件加约束、而不改组件代码"的实例。

### 3.5 统一 context 与 service multiplexing

- **统一 $\Gamma_\infty$** ↔ Cordis 的 `ctx` / dsh 的 fiber：一个自相似类型承载状态、逆与依赖。
- **service multiplexing（§5.1）** ↔ dsh 的多个"注册表 / 提供者"场景：LLM 适配器注册表（Ch10）、subagent providers（Ch15）、SDK-ACP 桥接（Ch17）。这些正是"从独占绑定走向服务代理"的工程化身。

### 3.6 一个诚实立场的共振：沙箱需要语言之外的边界

论文 §5.2 明说：**要真正隔离不可信组件，光靠语言机制不够，必须有语言之外的执行边界**。dsh 采取了完全一致的立场——"steering not containment"（引导而非围栏），真正需要强隔离时接入 E2B 等外部沙箱（Ch13）。两者在这一点上是同一种工程诚实：可逆 effect 管得住"善意组件的副作用回滚"，管不住"恶意组件的越权"，后者交给进程 / 容器边界。

### 3.7 作者链与"工程验证体"推断

- **Tianyi Cui** 既是本论文的共同作者（² DeepSeek-AI），又是 dsh 的**头号提交者**——git 已核实其 5235 commits [verified]。
- README 里的 paper 链接由 Shigma 提交；**Yifan Shi 可能即 Shigma** [inferred]（音 / 名相合，但未在论文正文取得直接证据，措辞保守）。
- 论文 §7 Conclusion 把 **self-evolving agent harness** 明确列为该范式的未来验证方向（AI agent 持续生成 / 替换自身 harness 组件，用以验证"快速替换下的完全恢复"与"频繁拓扑变化下的依赖协调"）。

把这几条串起来：**dsh 很可能正是这篇论文所构想范式的一个工程验证体**——一个真实的 self-evolving agent harness，其可逆 effect / 响应式 coeffect 机制与论文形式化高度同构，且作者与代码提交者存在交集。这是**有据推断 [inferred]**，本导读在措辞上保持谨慎：论文正文并未点名 dsh，此结论建立在机制同构 + 作者链 + Conclusion 明示方向三条证据之上，而非论文的直接声明。

---

## 四、与相关工作的定位（据 §6）

论文的 Related Work 用一连串"vs"精准划出自己的坐标。理解这些对比，能帮你把这篇工作放进整个学术谱系：

- **vs Effekt**（effects as capabilities）：Effekt 把 effect 当能力，但它是**静态、解释式**的；本文是运行时、可逆的。
- **vs Heunen 的可逆 effect**：Heunen 走 denotational（指称语义）、**全局可逆**；本文是运行时、局部可组合的可逆。
- **vs Orchard 的 graded types**：graded coeffect 也刻画依赖，但**静态**；本文是响应式、运行时的。
- **vs COP（Context-Oriented Programming）**：COP 把 context 当一等公民，但它**不追踪也不回滚 activation**；本文两者都做。
- **vs AOP（面向切面编程）**：AOP 的 pointcut 是 "oblivious & quantified"（组件对被切浑然不觉、且靠模式量化匹配）；Cordis 的 coeffect 是 "declared & traceable"（显式声明、可追踪），且切面**绑定组件生命周期**。
- **vs DSU / Erlang 热更 / HMR**：这些走 **forward migration**（向前迁移状态）；Cordis 走**回滚重放**（revert-and-replay）。
- **vs React useEffect**：受限于 top-level 调用、且**逆不能组合**；本文的逆可组合。
- **vs OSGi / iPOJO**：它们也做 availability-reactive（按可用性响应），但 cleanup 要**手写**、且**同步**；本文自动且可异步。
- **vs FRP / signals**：FRP 在 **value 层**（值随时间变化）；本文在 **component 层**（组件随依赖满足性激活 / 卸载）。

一句话总结坐标：**别人要么静态、要么只在值层、要么向前迁移不回滚、要么清理靠手写；这篇把"运行时 + 组件层 + 可逆回滚 + 自动响应"四个特性同时占齐了。**

---

## 五、事实核验

按证据来源分列，并标注证据等级。

### 【论文事实】（据 PDF 及已核实 source-truth）

- 标题、作者（Yifan Shi¹²、Wei Zhang¹、Tianyi Cui²）、单位（¹北京大学、²DeepSeek-AI）：已用 Read 打开 PDF **第 1 页**核对一致 [verified]。
- 四条贡献（revertible effects / reactive coeffects / component lifecycle + unified context / Cordis 实现 + Koishi 4000+ 插件验证）：已用 Read 打开 PDF **第 6 页**逐条核对一致 [verified]。
- 7 节结构、VSCode 统计（top100 中 87 个含可执行码、7 个声明 extensionDependencies）、各公式定义（$\partial\Gamma$、$\mathfrak{E}_\Gamma$、$\Sigma$、满足谓词、epoch、$\Gamma_\infty$ 等）、四张图语义、§4–§6 论点：来自已核实的 source-truth [claimed by source-truth]。**边界说明**：本导读**未逐页复核**这些公式的排版细节与 §2–§6 全文，公式与图的转述以 source-truth 为准；如需引用到论文原文的精确记号，请回到 PDF 对应小节复核。

### 【报告推断】（dsh 侧映射与关系判断）

- dsh 的 `ctx.effect()` / disposer 反序卸载 / "Registrations are effects" 铁律 ↔ 可逆 effect：Ch02 / Ch03 [verified]。
- `inject` + fiber epoch（`_setEpoch` / `_refresh`）/ PENDING↔ACTIVE ↔ 响应式 coeffect：Ch03 / Ch05 / Ch11 [verified]。
- 幂等 disposer ↔ idempotent guard：Ch03 §4.1 [verified]。
- turn / step 边界 ↔ effect iterator（delimited continuation）：Ch06，结构同构 [inferred]。
- isolate realm / per-session preset ↔ isolation realm（Ch04 / Ch11）；fs-policy / sandbox-policy / waterfall ↔ interception（Ch14 / Ch13 / Ch05 / Ch09）[verified]。
- LLM 适配器注册表 / subagent providers / SDK-ACP ↔ service multiplexing：Ch10 / Ch15 / Ch17 [verified]。
- "steering not containment" + E2B ↔ §5.2 沙箱需外部执行边界：Ch13 [verified]，立场一致性判断 [inferred]。
- Tianyi Cui 为 dsh 头号提交者（5235 commits）且论文共同作者：git 已核实 [verified]。
- Yifan Shi 可能即 Shigma：[inferred]，未取得论文正文直接证据。
- "dsh 是这篇论文构想的工程验证体"：**有据推断 [inferred]**，建立在机制同构 + 作者链 + §7 明示 self-evolving harness 为验证方向三条证据上；论文正文并未点名 dsh。

---

**收尾**：这篇论文最动人的地方，在于它把一个工程界习以为常的"重启大法"，还原成一个有精确形式基础的理论缺口，并给出了"可逆 effect × 响应式 coeffect"这一对优雅的答案。而 §7 那句把 self-evolving agent harness 列为未来验证方向的话，几乎就是为 dsh 这类系统写的注脚——理论与工程，在这里对上了暗号。
