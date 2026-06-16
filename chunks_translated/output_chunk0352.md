2 通过使用额外的交换机将主机和线卡双端口接入冗余结构,如图 C-0-7(第 957 页)所示,双主机系统模型可以扩展为完全冗余的双星型系统。这对于采用基于机箱的系统的厂商尤其具有吸引力,因为这类系统具有灵活性、可扩展性和可靠性。 

3 系统中包含两块主机卡。主机 A 是 Fabric A 的主用主机,也是 Fabric B 的备用主机。同样,主机 B 是 Fabric B 的主用主机,也是 Fabric A 的备用主机。 

4 每台主机通过一个透明桥/交换机端口连接到其主服务的结构,通过一个非透明桥/交换机端口连接到其仅提供备份的结构。这些非透明端口用于主机间的通信,并支持跨域的对等传输(当地址映射不允许更直接的连接时)。 

5 **956** 

6 ## **Chapter : Appendix C:  Implementing Intelligent Adapt-** 

7 _Figure 0-7: Dual-Star Fabric_ 

8 ## **Summary** 

9 通过非透明桥接(Non-Transparent Bridging),PCI Express Base 为厂商提供了将智能适配器和多主机系统集成到其下一代设计中的能力。本附录演示了这些特性如何使用 PCI 环境中采用的事实标准技术进行部署,并展示了它们将如何被用于各种应用。因此,我们可以预期该方法将成为 PCI Express 领域中的业界标准。 

10 **957** 

11 **PCI Ex ress 3.0 Technolo p gy** 

12 ## **Address Translation** 

13 本节深入描述了使用非透明桥的系统如何通过地址转换进行通信。我们提供了关于系统如何确定所分配内存大小的机制细节,以及内存指针的使用方式。同时讨论了直接地址转换(Direct Address Translation)和基于查找表的地址转换(Lookup Table Based Address Translation)的实现方式。通过在 PCI Express 环境中沿用 PCI 范式中流行的同一标准化非透明桥接架构实现方式,互连厂商可以加速 PCI Express 在需要智能适配器、主机故障切换和多主机能力的市场中的推广。 

14 透明桥使用 I/O 空间、不可预取内存空间和可预取内存空间中的基址(Base)和限值(Limit)寄存器来映射跨桥的下行方向事务。所有下游设备都需要被映射到连续的地址区域,以便每个空间中单个窗口就足够了。上行映射通过对相同寄存器的反向解码完成。透明桥不会转换被转发事务/数据包的地址。 

15 非透明桥在其 Type 0 CSR 头部中使用标准的一组 BAR 来定义桥另一侧内存空间的窗口。BAR 共有两组:一组在主端(Primary side),另一组在次端(Secondary)。BAR 定义了资源窗口,允许将事务转发到对端(另一侧)接口。 

16 对于每个 BAR 桥,都存在一组相关的控制和设置寄存器,通常可从桥的另一侧进行写入。每个 BAR 都有一个"设置"寄存器,用于定义其窗口的大小和类型,以及一个地址转换寄存器。某些 BAR 还具有限值寄存器,可用于限制其窗口的大小。在允许从本地子系统外部访问之前,需要对这些寄存器进行编程。这通常由本地处理器上运行的软件完成,或从 EEPROM 中加载寄存器值。 

17 在 PCI Express 中,穿过这些窗口的数据包的 Transaction ID 字段也会被转换,以支持 Device ID 路由。这些 Device ID 用于将完成包路由到 Non-Posted 请求和 ID 路由的消息。 

18 透明桥根据次级和上级总线号寄存器在下游方向转发 CSR 事务,并根据需要将 Type 1 CSR 转换为 Type 0 CSR。非透明桥只接受寻址到它自己的 CSR 事务,并对所有其他事务返回不支持请求(Unsupported Request)响应。 

19 **958** 

20 **Chapter : Appendix C:  Implementing Intelligent Adapt-** 

21 ## **Direct Address Translation** 

22 所有上游和下游事务的地址都会被转换(BAR 访问 CSR 的情况除外)。除了以下两节中描述的情况外,从一个接口转发到另一个接口的地址会通过在 BAR 内的偏移量上加上基址(Base Address)来转换,如图 C-0-8(第 959 页)所示。BAR 基址转换寄存器(BAR Base Translation Registers)用于为各个 BAR 设置这些基址转换。 

23 _Figure 0-8: Direct Address Translation_ 

24 ## **Lookup Table Based Address Translation** 

25 按照 PCI 社区采用的事实标准,PCI Express 应提供多个 BAR 用于分配资源。所有 BAR 都包含内存分配;然而,根据 PCI 行业惯例,BAR 0 包含 CSR 信息,BAR 1 包含 I/O 信息,BAR 2 和 BAR 3 用于基于查找表的转换(Lookup Table Based Translation)。BAR 4 和 BAR 5 用于直接地址转换(Direct Address Translation)。 

26 在次端,BAR 3 对落在其窗口内的事务使用一种特殊的基于查找表的地址转换,如图 C-0-9(第 960 页)所示。该查找表在将次级总线本地地址转换到主总线地址时提供了更大的灵活性。索引字段在地址总线中的位置是可编程的,以调整窗口大小。 

27 **959** 

28 **PCI Ex ress 3.0 Technolo p gy** 

29 查找到主总线地址。索引字段在地址总线中的位置是可编程的,以调整窗口大小。 

30 _Figure 0-9: Lookup Table Based Translation_ 

31 ## **Downstream BAR Limit Registers** 

32 主端的两个下游 BAR(BAR2/3 和 BAR4/5)也具有限值寄存器(Limit registers),可从本地端进行编程,以进一步限制其暴露的窗口大小,如图 C-0-10(第 961 页)所示。BAR 只能以"2 的幂"粒度分配内存资源。限值寄存器提供了一种通过在"2 的幂"粒度内"封顶"(capping)BAR 大小来获得更好粒度的方法。低于限值寄存器的事务才会被转发到次级总线。高于限值的事务会被丢弃,或在读操作时返回 0xFFFFFFFF,或返回等同于主设备中止(master abort)的数据包。 

33 **960** 

34 **Chapter : Appendix C:  Implementing Intelligent Adapt-** 

35 _Figure 0-10: Use of Limit Register_ 

36 ## **Forwarding 64bit Address Memory Transactions** 

37 某些 BAR 可以配置成对工作,以提供 64 位地址事务的基址和转换。命中这些 64 位 BAR 范围内的事务会使用直接地址转换(Direct Address Translation)进行转发。与 32 位事务的情况一样,当内存事务从主总线转发到次级总线时,主总线地址可以映射到次级总线域中的另一个地址。该映射通过将原始地址的基址替换为新的基址来执行。 

38 桥系统侧的 64 位 BAR 对用于将在桥系统侧发起的数据包中的 64 位地址窗口转换到本地空间的 232 以下。 

39 **961** 

40 **PCI Ex ress 3.0 Technolo p gy** 

41 **962** 

42 ## _**Appendix D:**_ 

43 ## _**Locked Transactions**_ 

44 ## **Introduction** 

45 原生 PCI Express 实现不支持旧的锁协议。对锁事务序列(Locked transaction sequences)的支持仅用于支持在主机处理器上执行的遗留设备软件,该软件对遗留 PCI 设备中的内存位置执行锁定的 RMW(读-修改-写)操作。本章定义了 PCI Express 规范中针对遗留设备的锁定访问序列的遗留支持协议。如果不支持锁,可能会导致死锁。 

46 ## **Background** 

47 PCI Express 仅对遗留设备支持原子或不被中断的事务序列(通常被描述为原子读-修改-写序列)。原生 PCIe 设备完全不支持此功能,如果它们接收到锁定请求,会返回具有 UR(Unsupported Request)状态的完成包。 

48 锁定操作由基本 RMW 序列组成,即: 

49 1. 从目标位置进行一个或多个内存读操作以获得值。 
50 2. 在处理器寄存器中修改数据。 

51 3. 一个或多个写操作,将修改后的值写回目标内存位置。 

52 该事务序列必须以在锁定序列期间不允许对目标位置(或设备)进行其他访问的方式执行。这需要在操作期间阻塞其他事务。这可能导致死锁和较差的性能。 

53 **963** 

54 **PCI Express Technology** 

55 需要支持锁定序列的设备包括: 

56 - 根复合体 (Root Complex)。 

57 - 路径中可能成为锁定事务系列目标的任何交换机(Switches)。 

58 - PCIe 转 PCI 桥(PCIe-to-PCI Bridge)或 PCIe 转 PCI-X 桥(PCIe-to-PCI-X Bridge)。 

59 - 任何发出对驻留在遗留设备内内存的锁定事务的遗留设备(Legacy Device)。 

60 在 PCI 环境中,锁定通过使用 LOCK# 信号实现。PCIe 中的等效功能通过使用模拟 LOCK# 信号功能的特定请求来完成。 

61 ## **The PCI Express Lock Protocol** 

62 PCI Express 支持的唯一锁源是通过根复合体 (Root Complex) 工作的系统处理器。锁定操作在根端口(Root Port)和遗留端点(Legacy Endpoint)之间执行。在大多数系统中,遗留设备通常是 PCI Express 转 PCI 或 PCI Express 转 PCI-X 桥。对于给定的层次路径,一次只支持一个锁定序列。 

63 锁定事务被限制为仅使用流量类 0 (Traffic Class 0) 和虚拟通道 0 (Virtual Channel 0)。映射到非零 VC 的其他 TC 值的事务可以穿越结构而不受锁定操作影响,但映射到 VC0 的事务受此处描述的锁规则影响。 

64 ## **Lock Messages — The Virtual Lock Signal** 

65 PCI Express 定义了以下事务,它们共同充当虚拟连线(virtual wire),取代 LOCK# 信号。 

66 - **Memory Read Lock Request** (MRdLk) — 发起一个锁定序列。第一个 MRdLk 事务会阻塞 VC0 中到达目标设备的其他请求。在该序列期间可以发出一个或多个这样的锁定读请求。 

67 - **Memory Read Lock Completion with Data** (CplDLk) — 返回数据并确认到目标的路径已被锁定。对第一个 Memory Read Lock 请求的返回数据的成功读完成会导致根复合体和目标设备之间的路径被锁定。也就是说,从其他端口穿越相同路径的事务将被阻塞,无法到达根端口或目标端口。在 VC1-VC7 缓冲中路由的事务不受锁影响。 

68 **964** 

69 **A endix D pp** 

70 - **Memory Read Lock Completion without Data** (CplLK) — 没有数据负载的完成包表示锁定序列当前无法完成,路径保持未锁定状态。 

71 - **Unlock Message** — 解锁消息由根复合体从锁定的根端口发出。该消息解锁根端口和目标端口之间的路径。 

72 ## **The Lock Protocol Sequence — an Example** 

73 本节通过示例解释 PCI Express 锁协议。示例包含以下设备: 

74 - 代表主机处理器发起锁定事务系列的根复合体 (Root Complex)。 

75 - 根端口和目标遗留端点之间路径中的一个交换机 (Switch)。 

76 - 目标路径上的一个 PCI Express 转 PCI 桥。 

77 - 发起锁定 RMW 的目标 PCI 设备的设备驱动程序。 
78 
79 - 包含一个 PCI Express 端点以描述锁定期间交换机的行为。
