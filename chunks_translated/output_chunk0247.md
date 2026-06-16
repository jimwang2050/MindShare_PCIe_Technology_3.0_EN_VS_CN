|when the table has been loaded into the Arbiter.||||||||||||
|Port VC Control Register<br>Port VC Status Register||||||||||||
|15<br>15                                            1 0||||4||3     1||0||||
|RsvdZ|RsvdP|||||||||||
|VC Arbitration Select (000b-111b)||||||||||||
|Load VC Arbitration<br>VC Arbitration Table Status||||Table||||||||
**260**
**Chapter 7: Quality of Service**
## **Port Arbitration**
## **General**
交换机端口和根端口通常会接收需要路由到另一个端口的传入包。由于来自多个端口的包都可以以同一传出端口中的同一 VC 为目标，因此需要仲裁来决定哪个传入端口的包获得对该 VC 的下一次访问。与 VC 仲裁一样，端口仲裁有多种可选方案可供配置软件选择。TC、VC 和仲裁支持的组合支持一系列服务级别，分为两大类：
**1. Asynchronous** — 包获得"尽力而为"的服务，可能根本不会得到任何优先考虑。许多设备和应用（如大容量存储设备）对带宽或延迟没有严格的要求，不需要特殊的计时机制。另一方面，通过为不同的包建立流量类层次结构，由更高要求的应用生成的包仍然可以优先处理，无需太多麻烦。区分服务被认为是异步的，直到服务级别需要保证。自然，异步服务始终可用，不需要任何特殊的软件或硬件选项。
**2. Isochronous** — 当需要延迟和带宽保证时，我们进入 isochronous 类别。当两个设备之间通常需要同步连接时，这将是有用的。例如，当耳机直接插入驱动器时，从音乐 CD 中获取数据的 CD‐ROM 使用同步连接。但是，当音频必须通过通用总线（如 PCIe）路由才能到达外部扬声器时，该连接不能是同步的，因为其他流量也可能需要使用相同的数据流。为了实现等效的结果，isochronous 服务必须保证对时间敏感的音频数据的正确传递，而不会阻止其他流量在同一时间使用该链路。毫不奇怪，需要专门的软件和硬件来支持此功能。
端口仲裁的概念如图 7‐14（第 262 页）所示。请注意，端口仲裁存在于系统中的多个位置：
- 交换机的 Egress ports
- 支持 peer‐to‐peer 事务时的根复合体端口
- 通往主内存等目标的根复合体 egress ports
**261**
**PCI Express Technology**
端口仲裁通常需要为交换机或根 egress port 支持的每个虚拟通道进行软件配置。在下面的示例中，根端口 2 支持来自根端口 1 和 2 的 peer‐to‐peer 传输，因此需要端口仲裁。但需要注意的是，根端口之间的 peer‐to‐peer 支持是可选的，因此可能并非每个根 egress port 都需要端口仲裁。
到系统内存的连接是一条有趣的路径。可能会有来自多个 ingress ports 的包同时尝试访问此端口，因此它需要支持端口仲裁。但是，它不使用 PCIe 端口，因此没有我们在此描述的支持仲裁的 PCIe 寄存器集。相反，根将需要提供一组称为根复合体寄存器块 (Root Complex Register Block, RCRB) 的供应商特定寄存器，以提供相同的功能。
由于端口仲裁为 egress port 的每个 VC 独立管理，因此需要为每个支持可编程端口仲裁的 VC 提供单独的表，如第 263 页的图 7‐15 所示。端口仲裁表仅由交换机和根端口支持，端点中不允许。
*Figure 7‐14: Port Arbitration Concept*
**==> picture [368 x 213] intentionally omitted <==**
**----- Start of picture text -----**<br>
CPU<br>Port Arbitration<br>(configured via RCRB)<br>Root Complex<br>Memory<br>1 2 3<br>VC0<br>Port Arbitration<br>Switch<br>(configured via PPB)<br>VC0 VC0<br>VC0 VC0<br>Endpoint Endpoint Endpoint Endpoint<br>A B C D<br>**----- End of picture text -----**<br>

**262**

**Chapter 7: Quality of Service**

*Figure 7‐15: Port Arbitration Tables for Each VC*

**==> picture [320 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>

Extended Capability Header<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>PAT0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>PATn Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Port Arbitration Table 0 (PAT0)<br>Port Arbitration Table n (PATn)<br>**----- End of picture text -----**<br>


虽然规范中没有说明，但仲裁不同数据包流的过程还意味着使用额外的缓冲区来累积来自 egress port 中每个端口的流量，如图 7‐16（第 264 页）所示。本示例说明了两个 ingress ports（1 和 2），其事务被路由到 egress port (3)。交换机执行的操作包括以下内容：

1. 到达 ingress ports 的包根据 TC/VC 映射被定向到适当的流控缓冲区 (VC)。

2. 包从流控缓冲区转发到 routing logic，后者确定并将它们路由到适当的 egress port。

3. 路由到 egress port (3) 的包使用 TC/VC 映射确定它们应放入哪个 VC 缓冲区。

4. 一组缓冲区与每个 ingress port 相关联，允许 ingress port 编号被跟踪直到可以执行端口仲裁。

5. Port arbitration logic 确定从事务每组 ingress buffers 发送的顺序。

**263**

**PCI Express Technology**

*Figure 7‐16: Port Arbitration Buffering*

**==> picture [356 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>

Ingress Ports Egress Port<br>Port Arbiter<br>Port 2<br>Port 1<br>TC0:TC3 1 VC0 VC0<br>Port 2 VC0 VC Arbiter<br>Port 3 VC0<br>3<br>Port 1<br>VC0<br>TC0:TC1 2 Port 1<br>TC2:TC4 VC7<br>VC5<br>Port 3 Port 2 VC7<br>VC7<br>Port Arbiter<br>TC/VC Mapping Routing Logic<br>TC/VC Mapping<br>TC/VC Mapping Routing Logic<br>**----- End of picture text -----**<br>


## **Port Arbitration Mechanisms**

定义的实际端口仲裁机制类似于用于 VC 仲裁的模型。配置软件通过读取第 265 页的图 7‐17 中所示的寄存器来确定端口的能力，并为每个 VC 选择要使用的端口仲裁方案。

**264**

**Chapter 7: Quality of Service**

*Figure 7‐17: Software Selects Port Arbitration Scheme*

**==> picture [276 x 325] intentionally omitted <==**

**----- Start of picture text -----**<br>

VCn Resource Capability Register<br>31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>7      6    5    4   3     2     1     0<br>Rsvd<br>WRR with 256 Phases (101b)<br>Time-based WRR with 128 Phases (100b)<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>VCn Resource Control Register<br>31              26 24            19 17 16 15  8 7                     0<br>VC<br>RsvdP ID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


## **Hardware-Fixed Arbitration**

此机制不需要软件设置。一旦选择，它完全由硬件管理。实际的仲裁方案由硬件设计人员选择，可能基于设备的预期需求。这可能仅确保公平性或优化设计的某些方面，但它不支持区分或 isochronous 服务。

## **Weighted Round Robin Arbitration**

就像 VC 仲裁中的加权轮询机制一样，软件可以设置端口仲裁表，使某些端口比其他端口获得更多

**265**

**PCI Express Technology**

机会。此方法为来自不同端口的流量分配不同的权重。

在扫描表时，每个 phase 指定从其接收下一个包的端口号。一旦包被传递，仲裁逻辑立即进入下一个 phase。如果所选端口没有挂起的事务等待传输，则仲裁器立即进入下一个 phase。这些条目没有关联的时间值。

为 WRR 端口仲裁给出了四个表长度，由表使用的 phase 数决定。据推测，表中较多数量的条目允许仲裁选择的更有趣的比率。另一方面，较少的条目数将使用更少的存储空间并降低成本。

## **Time-Based, Weighted Round Robin Arbitration (TBWRR)**

此机制是 isochronous 支持所必需的。顾名思义，基于时间的加权轮询为每个仲裁 phase 添加了时间元素。与 WRR 一样，端口仲裁器从当前 phase 的 Port Number 指示的 ingress port VC 缓冲区传递一个事务。现在，与立即进入下一个 phase 不同的是，基于时间的仲裁器等待当前虚拟时隙结束后再前进。这确保了以规则的间隔从 ingress port 缓冲区接受事务。如果所选端口没有准备好发送的包，则在下一个时隙之前不会发送任何内容。请注意，时隙不管理传输的持续时间，而是管理传输之间的间隔。事务的最长持续时间是完成轮询并返回原始时隙所花费的时间。时隙的长度将来可能会更改，但目前的值为 100ns。

基于时间的 WRR 仲裁支持最大表长度为 128 phase，但给定 VC 的实际可用表条目数可能少于该值。该值由硬件初始化，并在每个支持 TBWRR 的虚拟通道的 _Maximum Time Slots_ 字段中报告，如图 7‐18（第 267 页）所示。

**266**

**Chapter 7: Quality of Service**

*Figure 7‐18: Maximum Time Slots Register*

**==> picture [331 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>

31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>**----- End of picture text -----**<br>


## **Loading the Port Arbitration Tables**

Port Arbitration Tables 的实际大小和格式是 phase 数量和支持 peer‐to‐peer 传输的 Switch、RCRB 或 Root Port 的 ingress ports 数量的函数。Port Arbitration Table 支持的最大 ingress ports 数为 256 个。每个表条目中的实际位数是设计相关的，由其事务可以传递到 egress port 的 ingress ports 数量控制。每个表条目的大小在 Port VC Capability Register 1 的 2 位 _Port Arbitration Table Entry Size_ 字段中报告。允许的值为：

- 00b — 1 位（在 2 个端口之间选择）

- 01b — 2 位（4 个端口）

**267**

**PCI Express Technology**

*Figure 7‐19: Format of Port Arbitration Tables*

**==> picture [339 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>

32-Phase Port Arbitration Table<br>with 4-bit entries<br>31       28 27      24 23      20 19 16 15       12 11         8 7          4 3           0<br>Phase[7] Phase[6] Phase[5] Phase[4] Phase[3] Phase[2] Phase[1] Phase[0] 00h<br>Phase[15] Phase[14] Phase[13] Phase[12] Phase[11] Phase[10] Phase[9] Phase[8] 04h<br>Phase[23] Phase[22] Phase[21] Phase[20] Phase[19] Phase[18] Phase[17] Phase[16] 08h<br>Phase[31] Phase[30] Phase[29] Phase[28] Phase[27] Phase[26] Phase[25] Phase[24] 0Bh<br>1. Configuration Software loads the Port Arbitration Table.<br>2. Changes to the table automatically set the Port Arbitration 00b PAT entry is 1 bit (2 ports)<br>Table Status bit.<br>01b PAT entry is 2 bits (4 ports)<br>3. Software sets the Load Port Arbitration Table bit to<br>10b PAT entry is 4 bits (16 ports)<br>     apply the table contents to the hardware.<br>4. Hardware loads table contents into the Port Arbiter, then  11b PAT entry is 8 bits (256 ports)<br>    automatically clears the Port Arbitration Table<br>    status bit when the table has been loaded.<br>VC Resource Status Register  Port VC Capability Register 1<br>15                                       2  1  0  31                                                          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP RsvdP<br>VC Negotiation Pending  Port Arbitration Table Entry Size<br> Port Arbitration Table Status  Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>VC Resource Capability Register<br>31              26 24            19 17 16 15 8 7                     0<br>RsvdP VCID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


**268**

**Chapter 7: Quality of Service**

## **Switch Arbitration Example**

让我们考虑一个三端口交换机的示例来说明 Port 和 VC 仲裁。该示例假定到达 ingress ports 0 和 1 的包正在向上游方向移动，端口 2 是面向上游的 egress port（朝向根复合体）。在以下讨论中请参考第 270 页的图 7‐20。

1. 到达 ingress port 0 的包根据端口 0 的 TC/VC 映射放入接收器 VC 中。如图所示，traffic class 为 TC0 或 TC1 的 TLP 被发送到 VC0 缓冲区。traffic class 为 TC3 或 TC5 的 TLP 被发送到 VC1 缓冲区。此链路上不允许使用其他 TC。顺便说一句，如果到达的包具有未映射到现有 VC 的 TC，它将被视为错误。

2. 到达 ingress port 1 的包也根据 TC/VC 映射放入 VC 中，但对于此端口它是不同的。如所示，traffic class 为 TC0 的 TLP 被发送到 VC0，而 traffic class 为 TC2‐TC4 的 TLP 被发送到 VC3。此链路上不允许使用其他 TC。

3. 在两个端口中，目标 egress port 由每个包中的 routing information 确定。例如，地址路由用于内存或 IO 请求 TLP。

4. 所有注定要到达 egress port 2 的包都将被提交给该端口的 TC/VC 映射逻辑。如图所示，traffic class 为 TC0‐TC2 的 TLP 被放入带有其 ingress port 编号标记的 VC0 缓冲区，而 traffic class 为 TC3‐TC7 的 TLP 被管理为 VC1。

5. Port Arbitration 独立应用于排队的包，以决定哪个端口的包将接下来被加载到真正的 VC 中。

6. 最后，VC arbitration 确定 VC 缓冲区中的事务将跨链路发送的顺序。

7. 请注意，VC 仲裁器仅在存在足够的流控信用时才选择要传输的包。

**269**

**PCI Express Technology**

*Figure 7‐20: Arbitration Examples in a Switch*

**==> picture [357 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>

Switch<br>(1)<br>TC0,1TC3,5  VC0VC1 0 Of IngressMappingTC/VCPort 0 TC0,1TC3,5 INRESS EGRESS (5)Port Arbitration: VC0Egress Port 2<br>FC Buffer VC0 FC Buffer VC1<br>TLP1 RoutingTLP2 Routing TCTC TLP4 RoutingTLP3 Routing TCTC (4) PacketsPort 0 VC0VC0 ARB (6)<br>Egress Port 2<br>To  Port 1 TC/VC VC Arbitration (7)<br>(2) Determine Egress Port(Using Routing Info) (3) To  Port 2To  Port 3 Of EgressMappingPort 2 VC0VC1 ARB 2 TC0-2TC3-7 VC0VC1<br>TC2-4TC0   VC0VC3 1 Of IngressMappingTC/VCPort 1 TC2-4TC0 TC0-2=>VC0TC3-7=>VC1 (5)Port Arbitration: VC1Egress Port 2<br>FC Buffers VC0 FC Buffers VC3 PacketsPort 1 VC1 ARB<br>TLP3 Routing TLP4 Routing VC1<br>TLP1 Routing TLP2 Routing<br>Determine Egress Port(Using Routing Info) (3) To  Port 0To  Port 2To  Port 3 This logic replicated for each egress port<br>**----- End of picture text -----**<br>


## **Arbitration in Multi-Function Endpoints**

为将在多 function 设备中实现 QoS 的端点的具体情况定义了一组称为 Multi‐Function Virtual Channel (MFVC) capability 的寄存器。毫不奇怪，这种情况在内部呈现了与交换机端口必须处理的相同的仲裁问题。

规范中为此仲裁描述了两种情况。在第一种情况下（如图 7‐21（第 271 页）所示），有两个 Function，但只有 Function 0 包括 VC Capability registers，在那里进行的分配对于所有 Function 隐式相同。对于此选项，Function 之间的仲裁将以某种供应商特定的方式处理。这是最简单的方法，但不包含用于定义来自不同 Function 的请求之间优先级的标准结构，因此不支持 QoS。

**270**

**Chapter 7: Quality of Service**

*Figure 7‐21: Simple Multi‐Function Arbitration*

**==> picture [252 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>

Function 0 Vendor-Specific<br>Arbitration<br>VC Internal Link<br>Capability<br>0002h<br>Egress Port<br>Function 1<br>Internal Link<br>**----- End of picture text -----**<br>


如果需要 QoS 支持，则在 VC0 中实现 MFVC，每个 function 都有自己唯一的 VC Capability registers 集。为了保持软件向后兼容性，规范规定 _不_ 使用 MFVC 的设备的 VC Capability ID 必须为 0002h，而 _实现_ MFVC 结构的设备的 VC Capability ID 必须为 0009h。

图 7‐22（第 272 页）显示了 MFVC 寄存器块以及端点中具有两个 function 的示例的框图，该端点的端口支持两个 VC。每个 function 都有一个 Transaction Layer 和自己的 VC Capability registers，但不实现较低的层。相反，它们连接到共享端口的 Transaction Layer，该端口确实具有所有层。共享硬件接口自然会导致较低的成本，而添加 MFVC 允许 function 处理 isochronous 流量。

如图所示，MFVC registers 仅驻留在 Function 0 中，并定义将用于此接口的 VC 和仲裁方法。MFVC registers 看起来与 VC capability registers 非常相似，并支持 VC 仲裁和 Function 仲裁。由于来自多个 function 的包可以同时尝试访问同一 VC，因此 Function Arbitration 决定它们之间的优先级。到现在为止，这应该看起来很熟悉，因为它与端口仲裁的概念相同，甚至使用相同的仲裁选项，包括 TBWRR。VC 仲裁选项也与单 function VC registers 中的相同。

**271**

**PCI Express Technology**

*Figure 7‐22: QoS Support in Multi‐Function Arbitration*

**==> picture [330 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>

Extended Capability Header Cnt<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>Func 0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>Func n Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Function Arbitration Table 0<br>Function Arbitration Table n<br>Function<br>Function 0 Arbiter<br>MFVC Port 1<br>Capability VC0<br>0008h Internal Link<br>Port 2 VC0 VC Arbiter<br>VC<br>Capability VC0<br>0009h<br>Egress<br>Port<br>Function 1<br>Port 1<br>VC7<br>Internal Link<br>VC Port 2 VC7<br>Capability VC7<br>0009h<br>TC/VC Mapping<br>**----- End of picture text -----**<br>


## **Isochronous Support**

如前所述，并非每台机器或应用程序都需要 isochronous 支持，但有些不能没有它。由于 PCIe 从一开始就设计为支持它，让我们考虑一下需要具备什么才能使其工作。

**272**

**Chapter 7: Quality of Service**

## **Timing is Everything**

考虑第 274 页图 7‐23 中所示的示例，在该示例中，同步连接是理想的但又是不可能的。相反，我们使用 isochronous 机制模拟同步路径。在此示例中，isochrony 定义将在每个 Service Interval 内传递的数据量以实现所需的服务。以下序列描述了该操作：

1. 同步源（视频摄像头和 PCI Express 接口）在第一个相等的 service interval（SI 1）期间在 Buffer A 中累积数据。

2. 摄像头在下一个 service interval (SI 2) 期间通过通用总线传递所有累积的数据，同时在 Buffer B 中累积下一个数据块。

   - 显然，系统必须能够保证在 service interval 期间传递 Buffer A 的全部内容，无论链路上是否还有其他流量。这是通过为时间敏感的包分配高优先级并对仲裁方案进行编程，以便在与其他流量竞争时它们将首先处理来实现的。还要注意，只要所有数据都在时间窗口内传递，就不必精确地知道它何时到达。它可能分散在间隔内或聚集在间隔内的一个位置。只要在 Service Interval 内全部传递，仍然可以满足保证。

3. 在 SI 2 期间，磁带接收器接收并缓冲传入的数据，然后可以在 SI 3 期间将数据传送到存储器进行记录。摄像头在 SI 3 期间将 Buffer B 卸载到链路上，同时将新数据累积到 Buffer A 中，循环重复。

**273**

**PCI Express Technology**

*Figure 7‐23: Example Application of Isochronous Transaction*

**==> picture [298 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>

Camera<br>SI 1 Data accumulated<br>in Buffer A<br>SI 2 Data from Buffer A<br>delivered while<br>next data accumulates<br>in Buffer B<br>SI 3 Data from Buffer B<br>delivered while next<br>data accumulates in<br>Buffer A<br>PCI Express<br>Interface<br>SI 1 SI 2 SI 3<br>Service Interval (SI)<br>SI 2 Data received into<br>Buffer A<br>SI 3 Data from Buffer A<br>delivered to Storage<br>while data received<br>into Buffer B<br>Storage (e.g.: tape)<br>Buffer A Buffer B<br>Buffer A Buffer B<br>**----- End of picture text -----**<br>


## **How Timing is Defined**