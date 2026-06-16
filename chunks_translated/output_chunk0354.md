1 ## **Rules Related To PCI Express Endpoints** 

2 原生 PCI Express 端点不支持锁定。PCI Express 端点必须将 MRdLk Request 视为 Unsupported Request。 

3 **972** 

4 ## _**Glossary**_ 

5 |**Term**|**Definition**|
6 |---|---|
7 |128b/130b Encoding|这并不是与 8b/10b 相同意义上的编码。相反,发送方以块(Blocks)的形式发送信息,每个块由一排 16 个原始字节组成,前面是一个 2 位的同步(Sync)字段,指示该块应被视为数据块(Data Block)还是有序集块(Ordered Set Block)。该方案随 Gen3 引入,主要为了允许链路带宽在不提高时钟速率的情况下翻倍。它提供了更好的带宽利用率,但牺牲了 8b/10b 为接收器提供的一些优势。|
8 |8b/10b Encoding|多年前开发的编码方案,目前用于许多串行传输中。它旨在帮助接收器从输入信号中恢复时钟和数据,但它也将接收器处的可用带宽减少了 20%。此方案用于早期版本的 PCIe:Gen1 和 Gen2。|
9 |ACK/NAK Protocol|数据链路层 (Data Link Layer) 用于报告 TLP 在传输过程中是否发生错误的确认/否定确认(Acknowledge/Negative Acknowledge)机制。如果是,则向发送方返回 NAK 以请求重放失败的 TLP。如果不是,则返回 ACK 以指示一个或多个 TLP 已安全到达。|
10 |ACPI|高级配置和电源接口 (Advanced Configuration and Power Interface)。指定各种系统和设备电源状态。|
11 |ACS|访问控制服务 (Access Control Services)。|

12 **973** 

13 ## **PCI Ex ress Technolo p gy** 

14 |**Term**|**Definition**|
15 |---|---|
16 |ARI|替代路由 ID 解释 (Alternative Routing-ID Interpretation);一种可选特性,允许端点具有超过通常允许的 8 个功能(functions)。|
17 |ASPM|活动状态电源管理 (Active State Power Management):启用后,允许硬件将链路电源状态从 L0 更改为 L0s 或 L1,或两者都更改。|
18 |AtomicOps|原子操作 (Atomic Operations);随 2.1 规范修订版添加的三个新请求。这些请求执行多个操作,并保证在目标设备内不中断地进行。|
19 |Bandwidth Management|为节能或可靠性目的,硬件发起的链路速度或宽度的更改。|
20 |BAR|基址寄存器 (Base Address Register)。功能(Function)使用它来指示其本地内存和 IO 空间的类型和大小。|
21 |Beacon|低频带内信号,由主电源已关闭的设备使用,以发出已发生需要恢复电源的事件的信号。当链路处于 L2 状态时,可以通过链路发送该信号。|
22 |BER|误码率或误码比 (Bit Error Rate or Ratio);基于一段时间内看到的传输位错误数量的信号完整性度量。|
23 |Bit Lock|在接收器处获取发送器精确时钟频率的过程。这在 CDR 逻辑中完成,是链路训练 (Link Training) 中的第一步。|
24 |Block|由 Gen3 发送器发送的 130 位单位,由 2 位同步字段后跟 16 字节数据组成。|

25 **974** 

26 **Glossar y** 

27 |**Term**|**Definition**|
28 |---|---|
29 |Block Lock|在使用 128b/130b 编码时,在接收器处查找块边界以识别传入块。该过程涉及三个阶段。首先,在输入流中搜索 EIEOS(电气空闲退出有序集,Electrical Idle Exit Ordered Set),并将内部块边界调整以匹配它。接下来,搜索 SDS(数据流开始,Start Data Stream)有序集。之后,接收器锁定到块边界。|
30 |Bridge|充当两个总线之间接口的功能(Function)。交换机和根复合体 (Root Complex) 将在其端口上实现桥以启用数据包路由,桥也可以制作用于连接不同协议,例如 PCIe 和 PCI 之间。|
31 |Byte Striping|将输出字节流分布在所有可用的 Lane(Lane)上。发送字节时使用所有可用的 Lane。|
32 |CC|已消耗信用 (Credits Consumed):发射器在计算流控 (Flow Control) 时已使用的信用数。|
33 |CDR|时钟和数据恢复 (Clock and Data Recovery) 逻辑,用于从输入比特流中恢复发射器时钟,然后对比特进行采样以识别模式。对于 8b/10b,该模式在 COM、FTS 和 EIEOS 符号中找到,允许逻辑获取 Symbol Lock。对于 128b/130b,EIEOS 序列用于通过三个锁定阶段获取 Block Lock。|
34 |Character|用于描述要在链路邻居之间通信的 8 位值的术语。对于 Gen1 和 Gen2,这些是普通数据字节(标记为 D 字符)和特殊控制值(标记为 K 字符)的混合。对于 Gen3,没有控制字符,因为不再使用 8b/10b 编码。在这种情况下,字符都显示为数据字节。|

35 **975** 

36 ## **PCI Ex ress Technolo p gy** 

37 |**Term**|**Definition**|
38 |---|---|
39 |CL|信用限制 (Credit Limit):从发射器角度看的可用流控信用。检查以验证在发送 TLP 之前是否有足够的信用可用。|
40 |Control Character|这些是在 8b/10b 编码中使用的特殊字符(标记为"K"字符),便于链路训练 (Link training) 和有序集 (Ordered Sets)。它们不在 Gen3 中使用,Gen3 中字符之间没有区别。|
41 |Correctable Errors|由硬件自动纠正且不需要软件关注的错误。|
42 |CR|所需信用 (Credits Required) — 这是 CC 和 PTLP 的总和。|
43 |CRC|循环冗余校验 (Cyclic Redundancy Code);添加到 TLP 和 DLLP 中以允许验证无错传输。该名称意味着模式本质上是循环的并且是冗余的(它们不添加任何额外信息)。这些代码不包含足够的信息以允许自动纠错,但提供强大的错误检测。|
44 |Cut-Through Mode|交换机允许 TLP 通过而无需先存储它即可从入口端口转发到出口端口的机制。这涉及风险,因为 TLP 可能在一部分已转发到出口端口后才被发现有错误。在这种情况下,在数据链路层 (Data Link Layer) 修改数据包的末尾以具有与应有的值相反的 LCRC 值,并在物理层 (Physical Layer) 修改为具有 End Bad (EDB) 帧符号(对于 8b/10b 编码)或 EDB 令牌(对于 128b/130b 编码)。这种组合告诉接收器该数据包已被作废,应在不发送 ACK/NAK 响应的情况下丢弃。|
45 |Data Characters|表示普通数据的字符(标记为"D"字符),在 8b/10b 中与控制字符区分开。对于 Gen3,字符之间没有区别。|

46 **976** 

47 **Glossar y** 

48 |**Term**|**Definition**|
49 |---|---|
50 |Data Stream|用于 Gen3 操作的数据块流。该流由 SDS(数据流开始有序集)进入,以 EDS(数据流结束令牌)退出。在数据流期间,只期望数据块或 SOS。当需要任何其他有序集时,必须退出数据流,并且仅在有更多数据块准备发送时重新进入。启动数据流等同于进入 L0 链路状态,因为有序集仅在其他 LTSSM 状态(如 Recovery)期间发送。|
51 |De-emphasis|降低流中重复比特的发射器电压的过程。这具有去加重(de-emphasizing)已知会在传输介质中引起问题的信号低频分量的效果,从而改善接收器处的信号完整性。|
52 |Digest|ECRC(端到端 CRC,End-to-End CRC)值的另一个名称,可在事务层 (Transaction Layer) 中创建 TLP 时可选地附加。|
53 |DLCMSM|数据链路控制和管理状态机 (Data Link Control and Management State Machine);管理链路层训练过程(主要是流控 (Flow Control) 初始化)。|
54 |DLLP|数据链路层包 (Data Link Layer Packet)。这些在数据链路层 (Data Link Layer) 中创建并转发到物理层 (Physical Layer),但事务层 (Transaction Layer) 看不到它们。|
55 |DPA|动态功率分配 (Dynamic Power Allocation);随 2.1 规范修订版添加的一组新配置寄存器,定义 D0 设备电源状态下的 32 个功率子状态,使软件更容易控制设备电源选项。|
56 |DSP (Downstream Port)|面向下游的端口,例如根端口 (Root Port) 或交换机下游端口 (Switch Downstream Port)。这种区别在 LTSSM 中是有意义的,因为端口在某些状态期间具有分配的角色。|

57 **977** 

58 ## **PCI Ex ress Technolo p gy** 

59 |**Term**|**Definition**|
60 |---|---|
61 |ECRC|端到端 CRC (End-to-End CRC) 值,在事务层 (Transaction Layer) 中创建 TLP 时可选地附加。这使接收器能够验证从源到目的地的可靠数据包传输,无论跨越了多少条链路 (Links)。|
62 |Egress Port|具有传出流量的端口。|
63 |Elastic Buffer|CDR 逻辑的一部分,此缓冲区使接收器能够补偿发射器和接收器时钟之间的差异。|
64 |EMI|电磁干扰 (Electro-Magnetic Interference):系统发射的电噪声。对于 PCIe,使用 SSC 和加扰 (scrambling) 来对抗它。|
65 |Endpoint|PCIe 功能(Function),位于 PCI 反向树 (Inverted-Tree) 结构的底部。|
66 |Enumeration|系统发现过程,其中软件读取所有预期的配置位置以了解哪些 PCI 可配置功能(functions)在系统中可见并因此存在。|
67 |Equalization|调整 Tx 和 Rx 值以补偿通过传输介质的实际或预期信号失真的过程。对于 Gen1 和 Gen2,这采用 Tx 去加重 (De-emphasis) 的形式。对于 Gen3,引入主动评估过程以测试信令环境并相应地调整 Tx 设置,并提到可选的 Rx 均衡 (equalization)。|
68 |Flow Control|发射器避免由于缓冲区空间不足而导致数据包在接收器处被拒绝的风险的机制。接收器定期发送有关可用缓冲区空间的更新,发射器在尝试发送数据包之前验证是否有足够的空间。|
69 |FLR|功能级复位 (Function-Level Reset)|

70 **978** 

71 **Glossar y** 

72 |**Term**|**Definition**|
73 |---|---|
74 |Framing Symbols|在 8b/10b 编码中用于指示 TLP 或 DLLP 边界的"开始"和"结束"控制字符。|
75 |Gen1|第一代 (Generation 1),意味着设计为符合 1.x 版本 PCIe 规范。|
76 |Gen1, Gen2, Gen3|PCIe 规范版本的缩写。Gen1 = 1.x 版,Gen2 = 2.x 版,Gen3 = 3.0 版。|
77 |Gen2|第二代 (Generation 2),意味着设计为符合 2.x 版本 PCIe 规范。|
78 |Gen3|第三代 (Generation 3),意味着设计为符合 3.x 版本 PCIe 规范。|
79 |IDO|基于 ID 的排序 (ID-based Ordering);启用后,这允许来自不同请求者的 TLP 相对于彼此乱序转发。目标是改善延迟和性能。|
80 |Implicit Routing|TLP 的路由无需参考地址或 ID 即可理解。只有消息请求可以选择使用这种类型的路由。|
81 |Ingress Port|具有传入流量的端口。|
82 |ISI|符号间干扰 (Inter-Symbol Interference);由之前的比特引起的对比特时间的影响。|
83 
84 
85 
86 **979** 
