## **PCI Express 端点相关规则**

原生 PCI Express 端点不支持锁定。PCI Express 端点必须将 MRdLk 请求视为不支持的请求 (Unsupported Request)。

**972**

## _**术语表 (Glossary)**_

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|128b/130b Encoding|这与 8b/10b 意义上的编码不同。相反,发送端以块 (Block) 形式发送信息,每个块由一行的 16 个原始字节组成,前面有一个 2 位的同步 (Sync) 字段,用于指示该块应被视为数据块 (Data Block) 还是有序集块 (Ordered Set Block)。该方案从 Gen3 开始引入,主要是为了在不使时钟频率翻倍的情况下使链路带宽翻倍。它提供了更好的带宽利用率,但牺牲了 8b/10b 为接收器提供的一些优势。|
|8b/10b Encoding|多年前开发的编码方案,如今仍用于许多串行传输。它旨在帮助接收器从输入信号中恢复时钟和数据,但也会使接收器可用带宽减少 20%。该方案用于早期版本的 PCIe:Gen1 和 Gen2。|
|ACK/NAK Protocol|确认/否定确认 (Acknowledge/Negative Acknowledge) 机制,数据链路层通过该机制报告 TLP 在传输过程中是否发生任何错误。如果发生错误,则向发送方返回 NAK 以请求重传失败的 TLP。否则,返回 ACK 以表明一个或多个 TLP 已安全到达。|
|ACPI|高级配置与电源接口 (Advanced Configuration and Power Interface)。规定各种系统和设备电源状态。|
|ACS|访问控制服务 (Access Control Services)。|

**973**

## **PCI Express Technology**

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|ARI|替代路由 ID 解释 (Alternative Routing-ID Interpretation);可选功能,允许端点具有比通常允许的 8 个更多的功能 (Function)。|
|ASPM|活跃状态电源管理 (Active State Power Management):启用后,允许硬件将链路电源状态从 L0 更改为 L0s 或 L1,或两者兼有。|
|AtomicOps|原子操作 (Atomic Operations);在 2.1 规范修订版中添加的三个新请求。它们执行多个保证在目标设备内不间断进行的操作。|
|Bandwidth Management|硬件发起的链路速度或宽度更改,目的是节约电力或提高可靠性。|
|BAR|基地址寄存器 (Base Address Register)。由功能 (Function) 用于指示其本地内存和 IO 空间的类型和大小。|
|Beacon|低频带内信号,由主电源已关闭的设备使用,以表明已发生需要恢复电源的事件。当链路处于 L2 状态时,该信号可通过链路发送。|
|BER|误码率 (Bit Error Rate or Ratio);基于在一定时间内看到的传输误码数来衡量信号完整性。|
|Bit Lock|在接收器处获取发送器的精确时钟频率的过程。这在 CDR 逻辑中完成,是链路训练 (Link Training) 的第一步。|
|Block|由 Gen3 发送器发送的 130 位单元,由 2 位同步字段 (Sync Field) 后跟一组 16 个字节组成。|

**974**

## _**术语表 (Glossary)**_

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|Block Lock|在使用 128b/130b 编码时,在接收器处找到块 (Block) 边界以便识别传入的块。该过程涉及三个阶段。首先,在输入流中搜索 EIEOS (电气空闲退出有序集,Electrical Idle Exit Ordered Set) 并调整内部块边界以匹配它。接下来,搜索 SDS (开始数据流,Start Data Stream) 有序集。之后,接收器被锁定到块边界。|
|Bridge|充当两个总线之间接口的 Function (功能)。交换机 (Switch) 和根复合体 (Root Complex) 将在其端口上实现桥接器以实现数据包路由,也可以创建桥接器以连接不同协议,例如 PCIe 和 PCI 之间。|
|Byte Striping|将输出字节流分布到所有可用 Lane 上。每当发送字节时,都使用所有可用的 Lane。|
|CC|已消耗信用 (Credits Consumed):发送方在计算流控制时已使用的信用数。|
|CDR|时钟数据恢复 (Clock and Data Recovery) 逻辑,用于从输入比特流中恢复发送器时钟,然后对比特进行采样以识别模式。对于 8b/10b,在 COM、FTS 和 EIEOS 符号中找到的模式允许逻辑获取符号锁定 (Symbol Lock)。对于 128b/130b,EIEOS 序列用于通过三个锁定阶段来获取块锁定 (Block Lock)。|
|Character|用于描述要在链路邻居之间通信的 8 位值的术语。对于 Gen1 和 Gen2,这些是普通数据字节 (标记为 D 字符) 和特殊控制值 (标记为 K 字符) 的混合。对于 Gen3,因为不再使用 8b/10b 编码,没有控制字符。在这种情况下,字符都显示为数据字节。|

**975**

## **PCI Express Technology**

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|CL|信用限制 (Credit Limit):从发送方角度看,流控制信用被视为可用。检查以验证是否有足够信用可用于发送 TLP。|
|Control Character|这些是在 8b/10b 编码中使用的特殊字符 (标记为 "K" 字符),有助于链路训练 (Link Training) 和有序集 (Ordered Sets)。它们不用于 Gen3,在 Gen3 中字符之间没有区别。|
|Correctable Errors|由硬件自动更正且不需要软件关注的错误。|
|CR|所需信用 (Credits Required) - 这是 CC 和 PTLP 的总和。|
|CRC|循环冗余校验 (Cyclic Redundancy Code);添加到 TLP 和 DLLP 中以允许验证无错传输。名称意味着这些模式本质上是循环的且是冗余的 (它们不添加任何额外信息)。这些代码不包含足够的信息以允许自动纠错,但提供强大的错误检测。|
|Cut-Through Mode|交换机 (Switch) 允许 TLP 通过的机制,从入口端口转发到出口端口,无需先存储以检查错误。这涉及风险,因为在部分内容已转发到出口端口后,TLP 可能被发现存在错误。在这种情况下,在数据链路层中修改数据包末尾,使其具有与应有的 LCRC 值相反的值,并在物理层中修改以在 8b/10b 编码中具有 End Bad (EDB) 帧符号,或在 128b/130b 编码中具有 EDB 令牌。该组合告诉接收器该数据包已作废 (nullified),应在不发送 ACK/NAK 响应的情况下丢弃。|
|Data Characters|表示普通数据的字符 (标记为 "D" 字符),在 8b/10b 中与控制字符区分开。对于 Gen3,字符之间没有区别。|

**976**

## _**术语表 (Glossary)**_

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|Data Stream|Gen3 操作的数据块流。该流由 SDS (数据流开始有序集) 进入,并以 EDS (数据流结束令牌) 退出。在数据流期间,只期望数据块或 SOS。当需要任何其他有序集时,必须退出数据流,仅在有更多数据块准备好发送时重新进入。启动数据流等同于进入 L0 链路状态,因为有序集仅在其他 LTSSM 状态 (如 Recovery) 中发送。|
|De-emphasis|降低流中重复比特的发送器电压的过程。这具有去加重信号中已知会在传输介质中引起问题的低频分量的效果,从而改善接收器处的信号完整性。|
|Digest|ECRC (端到端 CRC,End-to-End CRC) 值的另一个名称,可在 TLP 在事务层 (Transaction Layer) 中创建时附加到 TLP。|
|DLCMSM|数据链路控制和管理状态机 (Data Link Control and Management State Machine);管理链路层训练过程 (主要是流控制初始化)。|
|DLLP|数据链路层数据包 (Data Link Layer Packet)。这些在数据链路层中创建并转发到物理层,但事务层不可见。|
|DPA|动态功率分配 (Dynamic Power Allocation);2.1 规范修订版中引入的一组新配置寄存器,定义 D0 设备电源状态下的 32 个电源子状态,从而使软件更容易控制设备电源选项。|
|DSP (Downstream Port)|面向下游的端口,如根端口 (Root Port) 或交换机下游端口 (Switch Downstream Port)。这种区别在 LTSSM 中有意义,因为端口在某些状态下具有分配的角色。|

**977**

## **PCI Express Technology**

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|ECRC|端到端 CRC (End-to-End CRC) 值,可在 TLP 在事务层 (Transaction Layer) 中创建时附加到 TLP。这使接收器能够验证从源到目的地的可靠数据包传输,无论穿越了多少个链路 (Link)。|
|Egress Port|具有传出流量的端口。|
|Elastic Buffer|CDR 逻辑的一部分,该缓冲区使接收器能够补偿发送器和接收器时钟之间的差异。|
|EMI|电磁干扰 (Electro-Magnetic Interference):系统发射的电噪声。对于 PCIe,使用 SSC 和加扰 (scrambling) 来应对它。|
|Endpoint|位于 PCI 倒置树 (Inverted-Tree) 结构底部的 PCIe Function。|
|Enumeration|系统发现过程,其中软件读取所有预期的配置位置以了解哪些 PCI 可配置 Function 可见并因此存在于系统中。|
|Equalization|调整 Tx 和 Rx 值以补偿通过传输介质的实际或预期信号失真的过程。对于 Gen1 和 Gen2,这采用 Tx 去加重 (De-emphasis) 的形式。对于 Gen3,引入主动评估过程来测试信令环境并相应地调整 Tx 设置,并提及可选的 Rx 均衡。|
|Flow Control|发送器避免由于接收器缓冲区空间不足而导致数据包被拒绝的风险的机制。接收器定期发送有关可用缓冲区空间的更新,发送器在尝试发送数据包之前验证是否有足够空间可用。|
|FLR|功能级复位 (Function-Level Reset)|

**978**

## _**术语表 (Glossary)**_

|**术语 (Term)**|**定义 (Definition)**|
|---|---|
|Framing Symbols|在 8b/10b 编码中使用的 "开始" 和 "结束" 控制字符,指示 TLP 或 DLLP 的边界。|
|Gen1|第 1 代 (Generation 1),指设计为符合 PCIe 规范 1.x 版本的设计。|
|Gen1, Gen2, Gen3|PCIe 规范修订的缩写。Gen1 = 修订 1.x,Gen2 = 修订 2.x,Gen3 = 修订 3.0|
|Gen2|第 2 代 (Generation 2),指设计为符合 PCIe 规范 2.x 版本的设计。|
|Gen3|第 3 代 (Generation 3),指设计为符合 PCIe 规范 3.x 版本的设计。|
|IDO|基于 ID 的排序 (ID-based Ordering);启用后,允许来自不同请求者的 TLP 彼此失序转发。目标是改善延迟和性能。|
|Implicit Routing|TLP 的路由在不参考地址或 ID 的情况下即可理解。只有消息 (Message) 请求可以选择使用这种类型的路由。|
|Ingress Port|具有传入流量的端口。|
|ISI|符号间干扰 (Inter-Symbol Interference);由其前面的最近比特对比特时间造成的影响。|
