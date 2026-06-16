1 在此示例中,锁定操作正常完成。操作期间发生的步骤将在以下两节中描述。 

2 ## **The Memory Read Lock Operation** 

3 图 E-1(第 967 页)说明了锁定事务系列中的第一步(即获取信号量的初始内存读): 

4 1. CPU 发起锁定序列(锁定的内存读),这是由于驱动程序执行了针对 PCI 目标的锁定 RMW 指令。 

5 2. 根端口(Root Port)从端口 2 发出 Memory Read Lock Request。根复合体 (Root Complex) 始终是锁定序列的发起方。 

6 3. 交换机在其上游端口(upstream port)接收到锁请求,并将该请求转发到目标出口端口(egress port)(3)。交换机在将该请求转发到出口端口后,必须阻塞来自除入口端口(ingress port)(1)之外的其他端口的请求从该出口端口发出。 

7 4. 从所示的 PCI Express 端点到 PCI 总线的后续对等传输(从交换机端口 2 到交换机端口 3)在锁定清除之前将被阻塞。注意,锁定尚未在另一个方向上建立。来自 PCI Express 端点的事务仍然可以发送到根复合体。 

8 **965** 

9 ## **PCI Express Technology** 

10 5. Memory Read Lock Request 从交换机的出口端口发送到 PCI Express 转 PCI 桥。该桥将实现 PCI 锁语义(有关 PCI 锁的详细信息,请参阅 MindShare 出版的《PCI System Architecture, Fourth Edition》一书)。 

11 6. 桥在 PCI 总线上执行 Memory Read 事务,并断言 PCI LOCK# 信号。目标内存设备将所请求的信号量数据返回给桥。 

12 7. 读数据返回到桥,然后通过 Memory Read Lock Completion with Data (CplDLk) 传递回交换机。 

13 8. 交换机使用 ID 路由将数据包向上游返回到主机处理器。当 CplDLk 数据包被转发到交换机的上游端口时,它会在上游方向上建立锁定,以防止来自其他端口的流量被路由到上游。PCI Express 端点通过锁定操作的路径被完全阻止向交换机端口发送任何事务。注意,交换机端口之间未参与锁定操作的传输将被允许(本例中未显示)。 

14 9. 在检测到 CplDLk 数据包后,根复合体知道在它和目标设备之间的路径上已经建立了锁定,完成数据被发送到 CPU。 

15 **966** 

16 **A endix D pp** 

17 _Figure D-1: Lock Sequence Begins with Memory Read Lock Request_ 

18 **==> picture [368 x 388] intentionally omitted <==** 

19 **----- Start of picture text -----**<br>
20 CPU 执行<br>发起锁的 PCI 目标 1 CPU<br>的设备驱动<br>根复合体<br>根复合体发出 根复合体接收<br>MRdLk Request 2 9 CplDLk 并返回数据<br>到 CPU<br>交换机将完成包转发到<br>交换机接收 MRdLk 并 1 上游端口(ID 路由)<br>转发到出口端口(3)。 3 8 并锁定上游端口(1)<br>交换机阻塞来自其他<br>交换机<br>端口到出口端口的事务。<br>2 3<br>桥使用 CplDLk 事务<br>PCIe 端点发出 MenRd 4 返回数据<br>Request 目标 PCI 设备,<br>但请求被阻塞 5<br>PCIe PCIe<br>Endpoint to<br>PCI Bridge<br>桥接器接收 MRdLk。<br>桥支持基于 PCI 的<br>要求的锁<br>6<br>目标 桥断言 LOCK 并<br>设备 执行 PCI Rd 事务<br>且目标返回读数据<br>MRdLk CplDLk<br>**----- End of picture text -----**<br>

21 ## **Read Data Modified and Written to Target and Lock Completes** 

22 设备驱动程序接收到信号量值,对其进行修改,然后发起内存写操作以更新遗留 PCI 设备内存中的信号量。图 E-2(第 969 页)说明了写序列,随后是 

23 **967** 

24 **PCI Express Technology** 

25 根复合体 (Root Complex) 发出释放锁定的 Unlock 消息: 

26 10. 根复合体 (Root Complex) 通过锁定路径向目标设备发出 Memory Write Request。 

27 11. 交换机将事务转发到目标出口端口(3)。Memory Write 的内存地址必须与初始 Memory Read 请求相同。 

28 12. 桥将事务转发到 PCI 总线。 

29 13. 目标设备接收内存写数据。 

30 14. 一旦 Memory Write 事务从根复合体 (Root Complex) 发出,它会发送一个 Unlock 消息,指示锁定路径中的交换机和任何 PCI/PCI-X 桥释放锁定。注意,根复合体假定操作已正常完成(因为内存写是 Posted 的,并且没有返回 Completion 来验证成功)。 

31 15. 交换机接收到 Unlock 消息,解锁其端口,并将该消息转发到已锁定的出口端口,以通知锁定路径中的任何其他交换机和/或桥必须清除锁定。 

32 16. 在检测到 Unlock 消息后,桥还必须释放 PCI 总线上的锁定。 

33 **968** 

34 **A endix D pp** 

35 _Figure D-2: Lock Completes with Memory Write Followed by Unlock Message_ 

36 **==> picture [369 x 414] intentionally omitted <==** 

37 **----- Start of picture text -----**<br>
38 CPU 执行<br>发起锁的 PCI 目标 CPU<br>的设备驱动<br>根复合体<br>根复合体发出 根复合体发送<br>Mem Write Request 10 14 Unlock 消息<br>1<br>交换机接收 MemWt 并  交换机接收 Unlock<br>转发到出口端口(3) 11 15 消息并解锁<br>锁定路径中的交换机端口<br>2 3<br>桥由于 Unlock 消息<br>而释放锁<br>16<br>PCIe PCIe<br>12<br>Endpoint to<br>PCI Bridge<br>桥接器接收 MemWt<br>执行等效的 PCI<br>事务<br>13<br>目标 目标设备接收 PCI<br>设备 写数据,从而<br>完成操作<br>MemWt Unlock message<br>**----- End of picture text -----**<br>

38 **969** 

39 **PCI Express Technology** 

40 ## **Notification of an Unsuccessful Lock** 

41 当初始的 Memory Read Lock Request 收到一个没有数据的完成包(CplLk)时,锁定事务系列被中止。这意味着锁定序列必须终止,因为没有返回数据。这可能是由与内存读事务相关联的错误引起的,或者目标设备正忙而无法在此刻响应。 

42 ## **Summary of Locking Rules** 

43 以下是适用于根复合体 (Root Complex)、交换机(Switches)和桥(Bridges)的排序规则列表。 

44 ## **Rules Related To the Initiation and Propagation of Locked Transactions** 

45 - 以非"成功完成"(Successful Completion)状态完成的锁定请求不会建立锁定。 

46 - 无论与锁定序列相关联的任何完成状态如何,所有锁定序列和尝试的锁定序列都必须通过发送 Unlock Message 来终止。 

47 - MRdLk、CplDLk 和 Unlock 语义仅允许用于默认流量类(TC0)。 

48 - 在单个层次域内的给定时刻,只允许一个锁定事务序列尝试处于进行中状态。 

49 - 任何不参与锁定序列的设备必须忽略 Unlock Message。 

50 锁定事务序列通过 PCI Express 结构的发起和传播按以下方式执行: 

51 - 锁定事务序列以 MRdLk Request 开始: 

52   - 与锁定事务序列相关联的任何后续读操作也必须使用 MRdLk Requests。 

53   - 任何成功的 MRdLk Request 的完成使用 CplDLK 完成类型,或对不成功请求使用 CplLk 完成类型。 

54 **970** 

55 **A endix D pp** 

56 - 如果与锁定序列相关联的任何读操作未成功完成,则请求者必须假定锁定的原子性不再得到保证,并且请求者和完成者之间的路径不再被锁定。 

57 - 与锁定序列相关联的所有写操作必须使用 MWr Requests。 

58 - Unlock Message 用于指示锁定序列的结束。交换机通过锁定的 Egress Port 传播 Unlock Messages。 

59 - 接收到 Unlock Message 后,遗留端点 (Legacy Endpoint) 或桥必须在其处于锁定状态时解锁自身。如果它未锁定,或者接收方是不支持锁定的 PCI Express 端点或桥,则忽略并丢弃 Unlock Message。 

60 ## **Rules Related to Switches** 

61 交换机必须将锁定序列相关联的事务与其他事务区分开来,以防止其他事务干扰锁定并可能导致死锁。以下规则涵盖了如何实现此操作。注意,锁定访问仅限于 TC0,TC0 始终映射到 VC0。 

62 - 当交换机将 MRdLk Request 从 Ingress Port 传播到 Egress Port 时,它必须阻止所有映射到默认虚拟通道 (VC0) 的请求被传播到 Egress Port。如果在此 Ingress Port 收到寻址不同 Egress Port 的后续 MRdLk Request,则交换机的行为未定义。注意,这种 split-lock 访问不被 PCI Express 支持,软件不得导致此类锁定访问。可能由此类访问导致系统死锁。 

63 - 当返回第一个 MRdLk Request 的 CplDLk 时,如果 Completion 指示 Successful Completion 状态,则交换机必须阻止来自所有其他端口的请求被传播到参与锁定访问的两个端口中的任一个,映射到 Egress Port 上 VC0 以外通道的请求除外。 

64 - 参与锁定序列的两个端口必须保持阻塞,直到交换机接收到 Unlock Message(在接收到初始 MRdLk Request 的 Ingress Port) 

65   - Unlock Message 必须转发到锁定的 Egress Port。 

66   - Unlock Message 可以广播到所有其他端口。 

67   - Ingress Port 在 Unlock Message 到达后解除阻塞,而被阻塞的 Egress Port 在 Unlock Message 从 Egress Port 发送后解除阻塞。未参与锁定访问的端口不受 Unlock Message 影响 

68 **971** 

69 **PCI Express Technology** 

70 ## **Rules Related To PCI Express/PCI Bridges** 

71 PCI Express/PCI 桥的要求与对交换机的要求类似,只是由于这些桥仅使用 TC0 和 VC0,因此在锁定访问期间所有其他流量都被阻塞。PCI 总线侧的要求在 MindShare 出版的《PCI System Architecture, Fourth Edition》一书中描述。 

72 ## **Rules Related To the Root Complex** 

73 允许根复合体 (Root Complex) 作为请求者支持锁定事务。如果支持锁定事务,根复合体 (Root Complex) 必须遵循已描述的规则以执行锁定访问。根复合体 (Root Complex) 用来连接主机处理器 FSB(前端总线,Front-Side Bus)的机制不在规范的讨论范围之内。 

74 ## **Rules Related To Legacy Endpoints** 

75 允许遗留端点 (Legacy Endpoints) 支持锁定访问,尽管不鼓励使用。如果支持锁定访问,遗留端点 (Legacy Endpoints) 必须按以下方式处理它们: 

76 - 当遗留端点为锁定事务系列访问的第一个读请求的第一个完成发送 Successful Completion 状态时,遗留端点变为锁定: 

77   - 如果完成状态不是 Successful Completion,则遗留端点不会变为锁定状态。 

78   - 一旦锁定,遗留端点必须保持锁定,直到它接收到 Unlock Message。 
79 
80 - 处于锁定状态时,遗留端点不得使用映射到默认虚拟通道 (VC0) 的流量类发出任何 Request。注意,此要求适用于端点内所有可能的 Request 来源,在有多个可能的 Request 来源的情况下。可以使用映射到 VC0 以外的 VC 的 TC 发出 Request。
