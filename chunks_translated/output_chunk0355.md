1 |Lane|允许两个端口之间一位的发送和接收路径的两对差分线。链路可以仅由一条 Lane 组成,也可以包含多达 32 条 Lane。|
2 |Lane-to-Lane Skew|不同 Lane 上比特到达时间的差异。要求接收器检测到这种差异并在内部进行纠正。|
3 |Legacy Endpoint|携带以下三种遗留项目之一的端点:支持 IO 事务、支持本地仅 32 位可预取内存空间,或支持锁定事务 (locked transactions)。|

4 **979** 

5 ## **PCI Ex ress Technolo p gy** 

6 |**Term**|**Definition**|
7 |---|---|
8 |LFSR|线性反馈移位寄存器 (Linear-Feedback Shift Register);创建用于加扰的伪随机模式。|
9 |Link|两个端口之间的接口,由一条或多条 Lane 组成。|
10 |LTR|延迟容忍报告 (Latency-Tolerance Reporting);允许设备在发送请求时向系统报告其需要多快地获得服务的机制。较长的延迟为系统提供更多电源管理选项。|
11 |LTSSM|链路训练和状态状态机 (Link Training and Status State Machine);管理物理层 (Physical Layer) 的训练过程。|
12 |Non-posted Request|期望接收完成包作为响应的请求。例如,任何读请求都是非发布 (non-posted) 的。|
13 |Non-prefetchable Memory|读取时具有副作用的内存。例如,读取时自动自清的状态寄存器。这种数据不能安全地预取,因为如果请求者从未请求该数据并且该数据被丢弃,它将对系统丢失。这对于 PCI 桥很重要,它们必须猜测读取的数据大小。如果它们知道可以推测性地预先读取内存空间,它们可以猜测一个较大的数字并实现更好的效率。这种区别对于 PCIe 来说不那么重要,因为传输的确切字节数包含在 TLP 中,但保持它允许向后兼容性。|
14 |Nullified Packet|当发射器识别出数据包有错误并且不应被发送时,该数据包可以被"作废"(nullified),这意味着应丢弃它并且接收器应表现得好像它从未被发送过一样。在交换机上使用"直通"(cut-through)操作时可能会出现此问题。|

15 **980** 

16 **Glossar y** 

17 |**Term**|**Definition**|
18 |---|---|
19 |OBFF|优化缓冲区刷新和填充 (Optimized Buffer Flush and Fill);允许系统告诉设备启动流量的最佳时间的机制。如果设备在最佳时间发送请求而不是在其他时间发送请求,系统电源管理将得到改善。|
20 |Ordered Sets|作为物理层 (Physical Layer) 通信发送的符号组,用于 Lane 管理。对于 8b/10b 编码,这些通常仅由控制字符组成。它们在发送方的物理层 (Physical Layer) 中创建,并在接收方的物理层 (Physical Layer) 中使用,其他层完全看不到它们。|
21 |PCI|外设组件互连 (Peripheral Component Interface)。旨在取代 PC 中早期使用的总线设计,如 ISA。|
22 |PCI-X|PCI 扩展 (PCI eXtended)。旨在纠正 PCI 的缺点并实现更高的速度。|
23 |PME|电源管理事件 (Power Management Event);来自设备的指示需要电源相关服务的消息。|
24 |Poisoned TLP|数据负载在创建时已知为坏的数据包。在数据包中发送错误数据可能有助于诊断问题并确定解决方案。|
25 |Polarity Inversion|允许接收器的信号极性反向连接,以支持简化板布局的情况。要求接收器在链路训练 (Link Training) 期间检测此情况并在内部反转信号以进行纠正。|
26 |Port|PCIe 链路的输入/输出接口。|
27 |Posted Request|不期望完成包的数据包请求。规范中只定义了两种这样的请求:内存写 (Memory Writes) 和消息 (Messages)。|

28 **981** 

29 ## **PCI Ex ress Technolo p gy** 

30 |**Term**|**Definition**|
31 |---|---|
32 |Prefetchable Memory|读取时没有副作用的内存。该属性使其可以安全地预取,因为如果它被中间缓冲区丢弃,以后需要时始终可以再次读取。这对于 PCI 桥很重要,它们必须猜测读取的数据大小。可预取空间允许推测性地读取更多数据并提供更好效率的机会。对于 PCIe 来说,这种区别不那么重要,因为传输的确切字节数包含在 TLP 中,但保持它允许向后兼容性。|
33 |PTLP|挂起的 TLP (Pending TLP) — 发送当前 TLP 所需的流控信用。|
34 |QoS|服务质量 (Quality of Service);PCIe 拓扑为不同数据包分配不同优先级的能力。这可能仅意味着在仲裁点优先处理数据包,但在更复杂的系统中,它允许为数据包提供带宽和延迟保证。|
35 |Requester ID|事务的请求者的配置地址,意思是与请求者对应的 BDF(总线、设备和功能号)。完成者将使用它作为结果完成包的返回地址。|
36 |Root Complex|充当系统中 CPU 内核和 PCIe 拓扑之间接口的组件。这可以由一个或多个芯片组成,可以是简单的或复杂的。从 PCIe 的角度来看,它充当反向树结构的根,与 PCI 的向后兼容性要求该结构。|
37 |Run Length|连续 1 或 0 的数量。对于 8b/10b 编码,游程长度限制为 5 位。对于 128b/130b,没有定义限制,但它使用的修改加扰方案旨在补偿这一点。|

38 **982** 

39 **Glossar y** 

40 |**Term**|**Definition**|
41 |---|---|
42 |Scrambling|随机化输出比特流以避免链路上重复模式从而减少 EMI 的过程。对于 Gen1 和 Gen2 可以关闭加扰以允许在链路上指定模式,但 Gen3 不能关闭,因为它在该速度下执行其他工作,并且链路预期无法在没有它的情况下可靠工作。|
43 |SOS|跳过有序集 (Skip Ordered Set) — 用于补偿 Tx 和 Rx 之间的轻微频率差异。|
44 |SSC|扩频时钟 (Spread-Spectrum Clocking)。这是一种通过允许时钟频率在允许范围内来回变化来减少系统中的 EMI 的方法。这将发射能量扩展到更宽的频率范围,因此避免了在一个特定频率集中太多 EMI 能量的问题。|
45 |Sticky Bits|其值在复位后仍然保留的状态位。当错误由链路下游的功能(Function)检测到时,该特性对于维护状态信息很有用,这些功能不再正常工作。必须复位失败的链路才能访问下游功能(Function),并且其寄存器中的错误状态信息必须在该复位后保留以供软件使用。|
46 |Switch|包含多个下游端口 (Downstream Ports) 和一个上游端口 (Upstream Port) 的设备,能够在端口之间路由流量。|
47 |Symbol|跨链路发送的编码单位。对于 8b/10b,这些是编码产生的 10 位值,对于 128b/130b,它们是 8 位值。|
48 |Symbol Lock|在使用 8b/10b 编码时,在接收器处查找符号边界以识别传入符号,从而识别数据包的内容。|
49 |Symbol time|在链路上发送一个符号所花的时间 — Gen1 为 4ns,Gen2 为 2ns,Gen3 为 1ns。|

50 **983** 

51 ## **PCI Ex ress Technolo p gy** 

52 |**Term**|**Definition**|
53 |---|---|
54 |TLP|事务层包 (Transaction Layer Packet)。这些在事务层 (Transaction Layer) 中创建并通过其他层传递。|
55 |Token|在 Gen3 速度下运行时,数据流期间传递的信息类型的标识符。|
56 |TPH|TLP 处理提示 (TLP Processing Hints);这些帮助系统路由代理做出选择以改善延迟和流量拥塞。|
57 |UI|单位间隔 (Unit Interval);在链路上发送一位所花的时间 — Gen1 为 0.4ns,Gen2 为 0.2ns,Gen3 为 0.125ns。|
58 |Uncorrectable Errors|无法由硬件纠正的错误,因此通常需要软件关注才能解决。这些分为致命错误 — 使进一步链路操作不可靠的错误,以及非致命错误 — 尽管检测到问题但不影响链路操作的错误。|
59 |USP|上游端口 (Upstream Port),即面向上游的端口,例如端点 (Endpoint) 或交换机上游端口 (Switch Upstream Port)。这种区别在 LTSSM 中是有意义的,因为端口在配置 (Configuration) 和恢复 (Recovery) 期间具有分配的角色。|

60 **984** 

61 **Glossar y** 

62 |**Term**|**Definition**|
63 |---|---|
64 |Variables|使用多个标志在硬件层之间传递事件和状态。这些特定于硬件中的状态转换,通常对软件不可见。一些例子:<br>—<br>LinkUp — 从物理层 (Physical Layer) 到数据链路层 (Data Link Layer) 的指示,表示训练已完成,物理层 (Physical Layer) 现在处于运行状态。<br>—<br>idle_to_rlock_transitioned — 此计数器跟踪 LTSSM 从 Configuration.Idle 转换到 Recovery.RcvrLock 状态的次数。每当识别 TS2 以离开 Configuration 的过程无法工作时,LTSSM 转换到 Recovery 以采取适当的步骤。如果在 256 次通过 Recovery 后仍无法工作(计数器达到 FFh),则返回 Detect 重新开始。可能是某些 Lane 不工作。|
65 |WAKE#|带外引脚,用于向系统发出应恢复电源的信号。在需要重要节能的系统中,它代替 Beacon 使用。|

66 **985** 

67 **PCI Ex ress Technolo p gy** 

68 **986** 

69 ## _**Numerics**_ 

70 128b/130b 43 128b/130b Encoding 973 1x Packet Format 374, 375 3DW Header 152 3-Tap Transmitter Equalization 585 4DW Headers 152 4x Packet Format 374 8.0 GT/s 410 8b/10b 42 8b/10b Decoder 367 8b/10b Encoder 366 8b/10b Encoding 973 

71 ## _**A**_ 

72 AC Coupling 468 ACK 318 Ack 311 ACK DLLP 75, 312 ACK/NAK DLLP 312 ACK/NAK Latency 328 ACK/NAK Protocol 318, 320, 329, 973 Ack/Nak Protocol 74 ACKD_SEQ Count 323 ACKNAK_Latency_Timer 328, 343 ACPI 711, 973 ACPI Driver 706 ACPI Machine Language 712 ACPI Source Language 712 ACPI spec 705 ACPI tables 712 ACS 973 Active State Power Management 405, 735 Address Routing 158 Address Space 121 Address Translation 958, 959 Advanced Correctable Error Reporting 690 Advanced Correctable Error Status 689 Advanced Correctable Errors 688 Advanced Error Reporting 685 Advanced Source ID Register 697 Advanced Uncorrectable Error Handling 691 Advanced Uncorrectable Error Status 691 Aggregate Bandwidth 408 Alternative Routing-ID Interpretation 909 AML 712 AML token interpreter 712 Arbitration 20, 270 Arbor 117 Architecture Overview 39 ARI 909, 974 ASL 712 ASPM 735, 742, 910, 974 ASPM Exit Latency 756, 757 Assert_INTx messages 806 Async Notice of Slot Status Change 876 

73 AtomicOp 150 AtomicOps 897, 974 Attention Button 854, 862 Attention Indicator 854, 859 Aux_Current field 726 

74 ## _**B**_ 
