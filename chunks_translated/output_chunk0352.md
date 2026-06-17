## **双主机系统模型**

2 通过使用额外的交换机将主机和线卡双端口接入冗余结构 (redundant fabric),可以将双主机 (dual-host) 系统模型扩展为完全冗余的双星型 (dual star) 系统,如第 957 页的图 C-0-7 所示。这对于使用基于机箱的系统的供应商特别有吸引力,因为其具有灵活性、可扩展性和可靠性。

3 系统中包含两块主机卡。主机 A 是结构 A 的主用主机,也是结构 B 的备用主机。同样,主机 B 是结构 B 的主用主机,也是结构 A 的备用主机。

4 每台主机通过一个透明桥/交换机端口连接到其主服务的结构,通过一个非透明桥/交换机端口连接到其仅提供备份的结构。这些非透明端口用于主机间的通信,并支持跨域的对等传输(当地址映射不允许更直接的连接时)。

**956**

## **Chapter: Appendix C: Implementing Intelligent Adapt-**

_Figure 0‐7: Dual‐Star Fabric_

## **摘要**

通过非透明桥接,PCI Express Base 为供应商提供了将智能适配器和多主机系统集成到其下一代设计中的能力。本附录演示了如何使用在 PCI 环境中采用的业界事实标准技术来部署这些功能,并展示了如何将其用于各种应用。因此,我们可以预期此方法将成为 PCI Express 范例中的行业标准。

**957**

**PCI Express 3.0 Technology**

## **地址转换 (Address Translation)**

本节提供使用非透明桥的系统如何使用地址转换进行通信的深入描述。我们提供有关系统如何确定不仅分配的内存大小,还提供有关如何使用内存指针的机制的详细信息。将讨论使用直接地址转换和基于查找表的地址转换的实现。通过将 PCI 范例中流行的非透明桥接的相同标准化架构实现引入 PCI Express 环境,互连供应商可以加快 PCI Express 在需要智能适配器、主机故障切换和多主机能力的市场中的应用。

透明桥在 I/O 空间、不可预取内存空间和可预取内存空间中使用基址和限制寄存器来映射下游方向跨桥的事务。所有下游设备都需要映射在连续的地址区域中,以至于每个空间中的单个孔径就足够了。上游映射是通过相对于相同寄存器的反向解码来完成的。透明桥不转换转发事务/分组的地址。

非透明桥在其 Type 0 CSR 头部中使用标准 BAR 集来定义到桥另一侧内存空间的孔径。BAR 有两组:一组在主侧 (Primary),另一组在次侧 (Secondary)。BAR 定义资源孔径,允许将事务转发到对侧(另一侧)接口。

对于每个 BAR 桥,存在一组关联的控制和设置寄存器,通常可从桥的另一侧写入。每个 BAR 都有一个 "设置" (setup) 寄存器,用于定义其孔径的大小和类型,以及一个地址转换寄存器 (address translation register)。某些 BAR 还具有限制寄存器 (limit register),可用于限制其孔径的大小。这些寄存器需要在允许从本地子系统外部访问之前进行编程。这通常由本地处理器上运行的软件或从 EEPROM 加载寄存器来完成。

在 PCI Express 中,通过这些孔径的分组的 Transaction ID 字段也被转换以支持 Device ID 路由。这些 Device ID 用于将完成路由到未发布请求和 ID 路由消息。

透明桥根据次级和从属总线号寄存器在下游方向转发 CSR 事务,根据需要将 Type 1 CSR 转换为 Type 0 CSR。非透明桥仅接受寻址到它的 CSR 事务,并对所有其他事务返回不支持请求响应。

**958**

**Chapter: Appendix C: Implementing Intelligent Adapt-**

## **直接地址转换 (Direct Address Translation)**

所有上游和下游事务的地址都被转换(访问 CSR 的 BAR 除外)。除了以下两节中的情况之外,从一个接口转发到另一接口的地址通过将基地址 (Base Address) 添加到它们落在的 BAR 内的偏移量来转换,如第 959 页的图 C-0-8 所示。BAR Base Translation Registers 用于为各个 BAR 设置这些基本转换。

_Figure 0‐8: Direct Address Translation_

## **基于查找表的地址转换 (Lookup Table Based Address Translation)**

按照 PCI 社区采用的事实标准,PCI Express 应提供几个 BAR 用于分配资源。所有 BAR 都包含内存分配;但是,根据 PCI 行业惯例,BAR 0 包含 CSR 信息,而 BAR 1 包含 I/O 信息,BAR 2 和 BAR 3 用于基于查找表的地址转换 (Lookup Table Based Translation)。BAR 4 和 BAR 5 用于直接地址转换 (Direct Address Translation)。

在次级侧,BAR 3 对落入其窗口内的事务使用特殊的基于查找表的地址转换,如第 960 页的图 C-0-9 所示。查找表在次级总线本地地址

**959**

**PCI Express 3.0 Technology**

到主总线地址方面提供更大的灵活性。索引字段在地址总线中的位置是可编程的,以调整孔径大小。

_Figure 0‐9: Lookup Table Based Translation_

## **下游 BAR 限制寄存器**

主侧的两个下游 BAR(BAR2/3 和 BAR4/5)也具有限制寄存器 (Limit register),可从本地侧编程,以进一步限制它们暴露的窗口大小,如第 961 页的图 C-0-10 所示。BAR 只能以 "2 的幂" 粒度分配内存资源。限制寄存器提供了一种通过在 "2 的幂" 粒度内 "上限" BAR 大小来获得更好粒度的方法。只有低于限制寄存器的交易才会转发到次级总线。超过限制的交易将被丢弃,或在读取时返回 0xFFFFFFFF,或主中止 (master abort) 等效分组。

**960**

**Chapter: Appendix C: Implementing Intelligent Adapt-**

_Figure 0‐10: Use of Limit Register_

## **转发 64 位地址内存事务**

某些 BAR 可以配置为成对工作,以提供包含 64 位地址的事务的基地址和转换。命中这些 64 位 BAR 内的事务使用直接地址转换转发。与 32 位事务的情况一样,当内存事务从主总线转发到次级总线时,主地址可以映射到次级总线域中的另一个地址。该映射通过用新基地址替换原始地址的基地址来执行。

桥系统侧的 64 位 BAR 对用于将在桥系统侧发起且包含 64 位地址的分组窗口转换到本地空间中低于 2³² 的地址。

**961**

**PCI Express 3.0 Technology**

**962**

## _**Appendix D:**_

## _**Locked Transactions**_

## **引言**

本机 PCI Express 实现不支持旧的锁定协议 (lock protocol)。对锁定事务序列 (Locked transaction sequences) 的支持仅用于支持在主机处理器上执行的旧版设备软件,该软件对旧版 PCI 设备中的内存位置执行锁定的 RMW(读-修改-写)操作。本章定义了 PCI Express 为旧版设备锁定访问序列的此旧版支持定义的协议。不支持锁定可能导致死锁。

## **背景**

PCI Express 仅支持旧版设备的原子或非中断事务序列(通常称为原子读-修改-写序列)。本机 PCIe 设备根本不支持此操作,如果它们收到锁定请求 (locked Request),将返回具有 UR (Unsupported Request) 状态的完成。

锁定操作由基本的 RMW 序列组成,即:

1. 从目标位置进行一次或多次内存读取以获取值。
2. 在处理器寄存器中修改数据。

3. 一次或多次写入以将修改后的值写回目标内存位置。

此事务序列必须以在锁定序列期间不允许对目标位置(或设备)进行其他访问的方式执行。这需要在操作期间阻塞其他事务。这可能导致死锁和性能下降。

**963**

**PCI Express Technology**

需要支持锁定序列的设备包括:

- 根复合体 (Root Complex)。

- 通往旧版设备的路径中的任何交换机,这些设备可能是锁定事务系列的目标。

- PCIe-PCI 桥或 PCIe-PCI-X 桥。

- 任何驱动程序对驻留在旧版设备中的内存发出锁定事务的旧版设备。

PCI 环境中的锁定是通过使用 LOCK# 信号实现的。PCIe 中的等效功能通过使用模拟 LOCK# 信号功能的特定请求来完成。

## **PCI Express 锁定协议**

PCI Express 支持的唯一锁定源是通过根复合体 (Root Complex) 操作的系统处理器。锁定操作在根端口 (Root Port) 和旧版端点 (Legacy Endpoint) 之间执行。在大多数系统中,旧版设备通常是 PCI Express-PCI 或 PCI Express-PCI-X 桥。对于给定的层次结构路径,一次仅支持一个锁定序列。

锁定事务仅限于使用流量类别 0 (Traffic Class 0) 和虚拟通道 0 (Virtual Channel 0)。映射到非零 VC 的具有其他 TC 值的事务可以穿越结构而不考虑锁定操作,但映射到 VC0 的事务受此处描述的锁定规则影响。

## **锁定消息 — 虚拟锁定信号**

PCI Express 定义以下事务,它们共同充当虚拟连线并替代 LOCK# 信号。

- **Memory Read Lock Request** (MRdLk) — 发起锁定序列。第一个 MRdLk 事务阻止 VC0 中的其他请求到达目标设备。在此序列期间可以发出一个或多个这些锁定读请求。

- **Memory Read Lock Completion with Data** (CplDLk) — 返回数据并确认到目标的路径已锁定。为第一个 Memory Read Lock 请求返回数据的成功读完成会导致根复合体和目标设备之间的路径被锁定。也就是说,来自其他端口的穿越相同路径的事务被阻止到达根端口或目标端口。在 VC1-VC7 的缓冲区中路由的事务不受锁定影响。

**964**

**Appendix D**

- **Memory Read Lock Completion without Data** (CplLK) — 没有数据有效负载的完成表明锁定序列当前无法完成,并且路径保持解锁状态。

- **Unlock Message** — 解锁消息由根复合体从锁定的根端口发出。此消息解锁根端口和目标端口之间的路径。

## **锁定协议序列 — 示例**

本节通过示例解释 PCI Express 锁定协议。该示例包括以下设备:

- 代表主机处理器发起锁定事务系列的根复合体。

- 根端口和目标旧版端点之间的路径中的交换机。

- 到目标路径中的 PCI Express-PCI 桥。

- 其设备驱动程序发起锁定 RMW 的目标 PCI 设备。