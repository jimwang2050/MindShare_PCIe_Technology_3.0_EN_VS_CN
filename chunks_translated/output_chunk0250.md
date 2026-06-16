|当表已加载到仲裁器时。||||||||||||
|Port VC Control Register<br>Port VC Status Register||||||||||||
|15<br>15                                            1 0||||4||3     1||0||||
|RsvdZ|RsvdP|||||||||||
|VC Arbitration Select (000b-111b)||||||||||||
|Load VC Arbitration<br>VC Arbitration Table Status||||Table||||||||


**260**

**第 7 章:服务质量**

## **端口仲裁 (Port Arbitration)**

## **概述 (General)**

交换机端口和根端口经常会收到需要路由到另一端口的传入数据包。由于来自多个端口的数据包都可以以同一传出端口的同一 VC 为目标,因此需要进行仲裁以确定哪个传入端口的数据包获得对该 VC 的下一次访问权。与 VC 仲裁一样,端口仲裁有几种可选方案可供配置软件选择。TC、VC 和仲裁的组合支持一系列服务级别,大致分为两大类:

**1. 异步 (Asynchronous)** — 数据包获得"尽力而为"的服务,可能根本得不到任何偏好。许多设备和应用程序(如大容量存储设备)对带宽或延迟没有严格的要求,不需要特殊的时序机制。另一方面,通过为不同的数据包建立流量类层次结构,由要求更高的应用程序生成的数据包仍然可以优先处理而不会带来太多麻烦。在服务级别需要保证之前,差异化服务仍被视为异步的。自然而然,异步服务始终可用,不需要任何特殊的软件或硬件选项。

**2. 等时 (Isochronous)** — 当需要延迟和带宽保证时,我们进入等时类别。当两个设备之间通常需要同步连接时,这将很有用。例如,当耳机直接插入驱动器时,从音乐 CD 读取数据的 CD-ROM 使用同步连接。但是,当音频必须通过 PCIe 等通用总线路由到外部扬声器时,连接不能是同步的,因为其他流量也可能需要使用同一数据流。为了实现等效的结果,等时服务必须保证时间敏感的音频数据能够正确传送,同时防止其他流量在同一时间使用链路。不出所料,这需要专门的软件和硬件支持。

图 7-14 (第 262 页) 描绘了端口仲裁的概念。注意端口仲裁存在于系统中的多个位置:

- 交换机的出口端口

- 支持对等事务时的根复合体端口

- 通往主内存等目标的根复合体出口端口

**261**

## **PCI Ex ress Technolo p gy**

端口仲裁通常需要为交换机或根出口端口支持的每个虚拟通道进行软件配置。在下面的示例中,根端口 2 支持来自根端口 1 和 2 的对等传输,因此需要端口仲裁。但需要注意的是,根端口之间的对等支持是可选的,因此并非每个根出口端口都需要端口仲裁。

到系统内存的连接是一条有趣的路径。可能有来自多个入口端口的数据包试图同时访问此端口,因此它需要支持端口仲裁。但是,它不使用 PCIe 端口,因此没有我们在此描述的用于支持仲裁的 PCIe 寄存器集。相反,根需要提供一组称为根复合体寄存器块 (RCRB, Root Complex Register Block) 的厂商特定寄存器来提供相同的功能。

由于端口仲裁是为出口端口的每个 VC 独立管理的,因此每个支持可编程端口仲裁的 VC 都需要一个单独的表,如图 7-15 (第 263 页) 所示。端口仲裁表仅由交换机和根端口支持,不允许在端点中使用。

_Figure 7‐14: 端口仲裁概念_

**==> picture [368 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Port Arbitration<br>(通过 RCRB 配置)<br>根复合体 (Root Complex)<br>内存<br>1 2 3<br>VC0<br>Port Arbitration<br>交换机 (Switch)<br>(通过 PPB 配置)<br>VC0 VC0<br>VC0 VC0<br>端点 端点 端点 端点<br>A B C D<br>**----- End of picture text -----**<br>


**262**

**第 7 章:服务质量**

_Figure 7‐15: 每个 VC 的端口仲裁表_

**==> picture [320 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>PAT0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>PATn Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Port Arbitration Table 0 (PAT0)<br>Port Arbitration Table n (PATn)<br>**----- End of picture text -----**<br>


尽管规范中没有说明,但在不同数据包流之间进行仲裁的过程也意味着使用额外的缓冲区来在出口端口累积来自每个端口的流量,如图 7-16 (第 264 页) 所示。本示例说明了两个入口端口(1 和 2),它们的事务被路由到出口端口(3)。交换机所采取的操作包括:

1. 到达入口端口的数据包根据 TC/VC 映射被引导到适当的流控缓冲区 (VC)。

2. 数据包从流控缓冲区转发到路由逻辑,由路由逻辑确定并将其路由到正确的出口端口。

3. 路由到出口端口(3)的数据包使用 TC/VC 映射来确定它们应放入哪个 VC 缓冲区。

4. 一组缓冲区与每个入口端口相关联,允许在完成端口仲裁之前跟踪入口端口号。

5. 端口仲裁逻辑确定从每组入口缓冲区发送事务的顺序。

**263**

**PCI Ex ress Technolo p gy**

_Figure 7‐16: 端口仲裁缓冲_

**==> picture [356 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Ingress Ports Egress Port<br>Port Arbiter<br>Port 2<br>Port 1<br>TC0:TC3 1 VC0 VC0<br>Port 2 VC0 VC Arbiter<br>Port 3 VC0<br>3<br>Port 1<br>VC0<br>TC0:TC1 2 Port 1<br>TC2:TC4 VC7<br>VC5<br>Port 3 Port 2 VC7<br>VC7<br>Port Arbiter<br>TC/VC Mapping Routing Logic<br>TC/VC Mapping<br>TC/VC Mapping Routing Logic<br>**----- End of picture text -----**<br>


## **端口仲裁机制 (Port Arbitration Mechanisms)**

所定义的实际端口仲裁机制类似于用于 VC 仲裁的模型。配置软件通过读取图 7-17 (第 265 页) 所示的寄存器来确定端口的能力,并为每个 VC 选择要使用的端口仲裁方案。

**264**

**第 7 章:服务质量**

_Figure 7‐17: 软件选择端口仲裁方案_

**==> picture [276 x 325] intentionally omitted <==**

**----- Start of picture text -----**<br>
VCn Resource Capability Register<br>31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>7      6    5    4   3     2     1     0<br>Rsvd<br>WRR with 256 Phases (101b)<br>Time-based WRR with 128 Phases (100b)<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>VCn Resource Control Register<br>31              26 24            19 17 16 15  8 7                     0<br>VC<br>RsvdP ID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


## **硬件固定仲裁 (Hardware-Fixed Arbitration)**

此机制不需要软件设置。一旦选定,它就完全由硬件管理。实际的仲裁方案由硬件设计者选择,可能基于设备的预期需求。这可能仅仅是为了确保公平,或者可能优化设计的某些方面,但它不支持差异化或等时服务。

## **加权轮询仲裁 (Weighted Round Robin Arbitration)**

就像 VC 仲裁中的加权轮询机制一样,软件可以设置端口仲裁表,以便某些端口比其他端口获得更多机会。这种方法为来自不同端口的流量分配不同的权重。

在扫描表时,每个阶段指定从哪个端口号接收下一个数据包。一旦数据包被传送,仲裁逻辑立即进入下一阶段。如果所选端口没有挂起的事务等待发送,仲裁器立即进入下一阶段。这些条目不关联时间值。

WRR 端口仲裁给出了四种表长度,由表使用的阶段数决定。可以推测,表中的条目数越多,可以实现越有趣的仲裁选择比例。另一方面,较少的条目数将使用更少的存储空间并且成本更低。

## **基于时间的加权轮询仲裁 (Time-Based, Weighted Round Robin Arbitration, TBWRR)**

此机制是等时支持所必需的。顾名思义,基于时间的加权轮询为每个仲裁阶段增加了时间元素。与 WRR 中一样,端口仲裁器从当前阶段的端口号所指示的入口端口 VC 缓冲区传送一个事务。但是现在,基于时间的仲裁器不是立即进入下一阶段,而是等待当前虚拟时间片结束后再前进。这确保了事务以规律的间隔从入口端口缓冲区被接受。如果所选端口没有准备发送的数据包,则在下一个时间片之前不会发送任何内容。请注意,时间片不控制传输的持续时间,而是控制传输之间的时间间隔。事务的最长持续时间是完成轮询并返回到原始时间片所需的时间。时间片的长度将来可能会更改,但目前值为 100ns。

基于时间的 WRR 仲裁支持最大 128 阶段的表长度,但给定 VC 的实际表条目数可能少于该值。该值由硬件初始化,并在支持 TBWRR 的每个虚拟通道的 _Maximum Time Slots_ 字段中报告,如图 7-18 (第 267 页) 所示。

**266**

**第 7 章:服务质量**

_Figure 7‐18: 最大时间片寄存器_

**==> picture [331 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>**----- End of picture text -----**<br>


## **加载端口仲裁表 (Loading the Port Arbitration Tables)**

端口仲裁表的实际大小和格式是阶段数和支持对等传输的交换机、RCRB 或根端口所支持的入口端口数的函数。端口仲裁表支持的入口端口最大数量为 256 个。每个表条目内的实际位数是与设计相关的,受其事务可以传送到出口端口的入口端口数量的控制。每个表条目的大小在 Port VC Capability Register 1 的 2 位 _Port Arbitration Table Entry Size_ 字段中报告。允许的值为:

- 00b — 1 位(2 个端口之间选择)

- 01b — 2 位(4 个端口)
