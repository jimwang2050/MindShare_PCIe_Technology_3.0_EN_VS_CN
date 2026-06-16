本章讨论了 Flow Control 协议的目的和详细操作。流控旨在确保发送方永远不会发送接收方无法接受的 Transaction Layer Packets (TLPs)。这可以防止接收缓冲区溢出，并消除了 PCI 风格的低效（如 disconnect、retry 和 wait‐state）的需要。

## **The Next Chapter**

下一章讨论支持 Quality of Service 的机制，并描述了控制穿越 fabric 的不同包的时序和带宽的方法。这些机制包括为每个包分配优先级值的应用特定软件，以及必须构建在每个设备中以管理事务优先级的可选硬件。

## **Flow Control Concept**

每个 PCIe Link 两端的端口必须实现 Flow Control。在传输包之前，流控检查必须验证接收端口是否具有足够的缓冲区空间来接受它。在诸如 PCI 这样的并行总线架构中，事务在没有知道目标是否准备好处理数据的情况下被尝试。如果请求由于缓冲区空间不足而被拒绝，则该事务将重复（重试）直到完成。这就是 PCI 的 "Delayed Transaction Model"，虽然它工作但效率很差。

**215**

## **PCI Express Technology**

如果使用多个 Virtual Channels (VCs)，流控机制可以提高传输效率。每个 Virtual Channel 承载独立于其他 VC 中流动的流量的事务，因为流控缓冲区是单独维护的。因此，一个 VC 中满的 Flow Control 缓冲区不会阻塞对其他 VC 缓冲区的访问。PCIe 最多支持 8 个 Virtual Channels。

Flow Control 机制使用基于信用的机制，允许发送端口知道接收端口可用的缓冲区空间。作为初始化的一部分，每个接收方将其缓冲区大小报告给链路另一端的发送方，然后在运行期间使用 Flow Control DLLPs 定期更新可用信用数。从技术上讲，DLLPs 当然是开销，因为它们不传达任何数据负载，但它们保持小（始终为 8 个 symbol 大小）以最小化它们对性能的影响。

流控逻辑实际上是两个层之间的共同责任：Transaction Layer 包含计数器，但 Link Layer 发送和接收传达信息的 DLLPs。第 217 页的图 6‐1 说明了这种共同责任。在使流控工作的过程中：

- **设备报告可用缓冲区空间** — 每个端口的接收方以称为 credits 的单位报告其 Flow Control 缓冲区的大小。缓冲区内的信用数从接收侧事务层发送到链路层的发送侧。在适当的时候，链路层创建一个 Flow Control DLLP，以将此信用信息转发给链路上另一端的接收方，用于每个 Flow Control Buffer。

- **接收方注册信用** — 接收方获得 Flow Control DLLPs 并将信用值传输到事务层的发送侧。完成从一个链路伙伴到另一个链路伙伴的信用传输。这些动作在两个方向上执行，直到所有流控信息已被交换。

- **发送方检查信用** — 在发送 TLP 之前，发送方检查 Flow Control Counters 以了解是否有足够的信用可用。如果是，则 TLP 被转发到 Link Layer，但如果不是，则事务被阻塞，直到报告更多的 Flow Control 信用。

**216**

**Chapter 6: Flow Control**

*Figure 6‐1: Location of Flow Control Logic*

**==> picture [371 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters FC Buffers FC Counters FC Buffers<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>Link<br>**----- End of picture text -----**<br>


## **Flow Control Buffers and Credits**

为端口支持的每个 VC 资源实现流控缓冲区。回想一下，链路两端的端口可能不支持相同数量的 VC，因此由软件配置和启用的最大 VC 数量是两个端口之间最高的共同数量。

**217**

**PCI Express Technology**

## **VC Flow Control Buffer Organization**

接收方处的每个 VC Flow Control 缓冲区针对流经虚拟通道的每类事务进行管理。这些类别为：

- Posted Transactions — Memory Writes and Messages

- Non‐Posted Transactions — Memory Reads, Configuration Reads and Writes, and I/O Reads and Writes

- Completions — Read and Write Completions

此外，对于同时具有 header 和 data 的事务，这些类别中的每一个都分为 header 和 data 部分。这产生了六个不同的缓冲区，每个缓冲区都实现其自己的流控（参见第 218 页的图 6‐2）。

某些事务（如读请求）仅由 header 组成，而其他事务（如写请求）同时具有 header 和 data。发送方必须确保在事务发送之前，根据需要为 header 和 data 缓冲区空间都可用。请注意，在事务被转发到软件或交换机的情况下，事务排序必须在 VC Flow Control 缓冲区中维护。因此，接收方还必须跟踪缓冲区中 header 和 data 组件的顺序。

*Figure 6‐2: Flow Control Buffer Organization*

**==> picture [379 x 224] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Flow Control Buffers (Receiver)<br>Device Core Device Core<br>(PH) (PD) (NPH) (NPD) (CPLH) (CPLD)<br>PCIe-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters RCV Buffers P Posted Request<br>P NP CPL P NP CPL<br>NP Non-Posted Request<br>Data Link Layer Data Link Layer CPL Completion<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>Link<br>**----- End of picture text -----**<br>


**218**

**Chapter 6: Flow Control**

## **Flow Control Credits**

缓冲区空间由接收方以称为 Flow Control credits 的单位报告。Flow Control Credits (FCCs) 对于 header 和 data 缓冲区的单位值为：

- Header credits — maximum header size + digest

   - 完成请求为 4 DWs

   - 请求为 5 DWs

- Data credits — 4 DWs (aligned 16 bytes)

Flow Control DLLPs 传达此信息，并且本身不需要 Flow Control credits。这是因为它们源自并终止于 Link Layer，并且不使用 Transaction Layer 缓冲区。

## **Initial Flow Control Advertisement**

在 Flow Control 初始化期间，PCIe 设备通过"广告"其缓冲区空间（通过流控信用）来传达其缓冲区大小。PCIe 还定义了一些缓冲区所需的 infinite Flow Control credit 值。广告无限缓冲区空间的接收方实际上保证了其缓冲区空间永远不会溢出。

## **Minimum and Maximum Flow Control Advertisement**

规范定义了可以为不同 Flow Control 缓冲区类型报告的最小信用数，如表 6‐1 所列。然而，设备通常广告比最小值大得多的信用。第 220 页的表 6‐2 列出了规范允许的最大广告。

*Table 6‐1: Required Minimum Flow Control Advertisements*

|Credit Type|**Minimum Advertisement**|
|---|---|
|Posted Request Header (PH)|1 unit. Credit Value = one 4DW HDR + Digest = 5DW.|
|Posted Request Data (PD)|Largest possible setting of the Max_Payload_Size in<br>credits. Example: If the largest Max_Payload_Size value<br>supported is 1024 bytes, the smallest permitted initial<br>credit value would be 040h.|

**219**

## **PCI Express Technology**

*Table 6‐1: Required Minimum Flow Control Advertisements (Continued)*

|Credit Type|**Minimum Advertisement**|
|---|---|
|Non‐Posted Request HDR (NPH)|**1 unit**. Credit Value = one 4 DW HDR + Digest = 5DW.|
|Non‐Posted Request Data (NPD)|**1 unit**. Credit Value = 4DW.<br>**2 unit**. Receivers supporting AtomicOp routing or<br>AtomicOp Completer capability have credit value of 02h|
|Completion HDR (CPLH)|**1 unit**. Credit Value = one 3DW HDR + Digest = 4DW;<br>for Root Complex with peer‐to‐peer support and<br>Switches.<br>**Infinite units.**Initial Credit Value = all 0's for Root Com‐<br>plex with no peer‐to‐peer support and Endpoints.|
|Completion Data (CPLD)|**n unit**. Value of largest possible setting of<br>Max_Payload_Size or size of largest Read Request<br>(which ever is smaller) divided by FC Unit Size (4DW);<br>for Root Complex with peer‐to‐peer support and<br>Switches.<br>**Infinite units**. Initial Credit Value = all 0's; for Root<br>Complex with no peer‐to‐peer support and Endpoints.|

*Table 6‐2: Maximum Flow Control Advertisements*

|**Credit Type**|**Maximum Advertisement**|
|---|---|
|Posted Request Header (PH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes.|
|Posted Request Data (PD)|2048 units. Value of the Max_Payload_Size (4096 bytes)<br>including all functions supported by device (8) divided<br>by the credit size (4 DWs) = 32,768 bytes<br>2048 credits @ 4 DWs = 32,768 bytes|
|Non‐Posted Request HDR (NPH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes.|
|Non‐Posted Request Data (NPD)|The author's could not find a precise value for the maxi‐<br>mum number of credits for Non‐Posted Data. The maxi‐<br>mum number of credits listed for Data is 2048. However,<br>a more reasonable approach might use the Non‐Posted<br>header limit of 128 credits, because Non‐Posted Data is<br>always associated with Non‐Posted Headers.|

**220**

**Chapter 6: Flow Control**

*Table 6‐2: Maximum Flow Control Advertisements (Continued)*

|**Credit Type**|**Maximum Advertisement**|
|---|---|
|Completion HDR (CPLH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes. This in<br>the limit for ports that do not originate transactions (e.g.,<br>Root Complex with peer‐to‐peer support and Switches).<br>**Infinite units**. Initial Credit Value = all 0's for ports that<br>originate transactions (e.g., Root Complex with no peer‐<br>to‐peer support and Endpoints).|
|Completion Data (CPLD)|**2048 units**. Value of the Max_Payload_Size (4096 bytes)<br>including all functions supported by a device (8)<br>divided by the credit size (4 DWs) = 32,768 bytes<br>2048 credits @ 4 DWs = 32,768 bytes<br>**Infinite units**. Initial Credit Value = all 0's for ports that<br>originate transactions (e.g., Root Complex with no peer‐<br>to‐peer support and Endpoints).|

## **Infinite Credits**

请注意，在初始化期间，值为 00h 的流控值将被理解为无限信用。在 Flow‐Control 初始化之后，不进行进一步的广告。发起事务的设备必须为在 split transactions 期间返回的数据或状态信息预留缓冲区空间。这些事务组合包括：

- Non‐posted Read requests and return of Completion Data

- Non‐posted Read requests and return of Completion Status

- Non‐posted Write requests and return of Completion Status

## **Special Use for Infinite Credit Advertisements.**

规范指出了仅实现 VC0 的设备的特殊注意事项。例如，唯一的 Non‐Posted 写入是 I/O Writes 和 Configuration Writes，它们都只允许在 VC0 上。因此，Non‐Posted data 缓冲区不用于 VC1 ‐ VC7，并且可以为这些值广告无限值。但是，Non‐Posted Header 必须仍然操作，并且 header 信用必须仍然需要更新。

**221**

**PCI Express Technology**

## **Flow Control Initialization**

## **General**

在发送任何事务之前，需要进行流控初始化。事实上，TLPs 在成功完成 Flow Control Initialization 之前无法跨链路发送。初始化发生在系统中的每个 Link 上，并涉及链路两端设备之间的握手。此过程在 Physical Layer 链路训练完成后立即开始。如图 6‐3 所示，Link Layer 在观察到 LinkUp 信号处于活动状态时知道 Physical Layer 已准备就绪。

*Figure 6‐3: Physical Layer Reports That It's Ready*

**==> picture [338 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core  Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer  Transaction Layer<br>DLL DLCMSM  DLL DLCMSM DLCMSM<br>LinkUp LinkUp<br>Phy Phy<br>LTSSM  LTSSM<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>


一旦启动，Flow Control 初始化过程对于所有 Virtual Channels 基本上是相同的，并且一旦 VC 启用就由硬件控制。VC0 始终默认启用，因此其初始化是自动的。

**222**

**Chapter 6: Flow Control**

这允许配置事务穿越拓扑并执行枚举过程。其他 VC 仅在配置软件在链路两端设置和启用它们时才初始化。

## **The FC Initialization Sequence**

流控初始化过程涉及 Link Layer 的 DLCMSM (Data Link Control and Management State Machine)。如第 223 页的图 6‐4 所示，复位将状态机置于 DL_Inactive 状态。在 DL_Inactive 状态期间，DL_Down 被发信号到 Link 和 Transaction Layers。同时，它等待从 Physical Layer 看到 LinkUp 以指示 LTSSM 已完成其工作且 Physical Layer 已准备就绪。这导致转换到 DL_Init 子状态，该子状态包含处理流控初始化的两个阶段：FC_INIT1 和 FC_INIT2。

*Figure 6‐4: The Data Link Control & Management State Machine*

**==> picture [251 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
Reset<br>DL_Inactive Report DL_Down to Link<br>and Transaction Layers<br>Physical LinkUp=1<br>Physical LinkUp=0 &<br>Link Enabled andr<br>DL_Init<br>Report DL_Down<br>FC_Init1<br>(during FC_Init1)<br>Report DL_Up to remaining<br>FC_Init2<br>Link and Transaction Layers<br>(during FC_Init2)<br>FC_Init Complete<br>&<br>Physical LinkUp=1<br>DL_Active Report DL_Up<br>**----- End of picture text -----**<br>


**223**

**PCI Express Technology**

## **FC_Init1 Details**

在 FC_INIT1 状态期间，设备连续发送 3 个 InitFC1 Flow Control DLLPs 序列，宣传其接收方缓冲区大小（参见图 6‐5）。根据规范，必须按以下顺序发送包：Posted、Non‐posted 和 Completions，如第 225 页的图 6‐6 所示。规范强烈建议这些应该频繁重复，以便接收设备更容易看到它们，特别是如果没有 TLP 或 DLLP 可发送时。每个设备还应从其邻居接收此序列，以便它可以注册缓冲区大小。一旦设备已发送其自己的值并已接收完整的序列足够多次以确信这些值被正确看到，它就准备好退出 FC_INIT1。为此，它将接收到的值记录在其发送计数器中，设置内部标志（FL1），并更改为 FC_INIT2 状态以开始第二个初始化步骤。

*Figure 6‐5: INIT1 Flow Control DLLP Format and Contents*

**==> picture [373 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataHdr FC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>0100  Init 1 Posted<br>0101  Init 1 Non Posted<br>0110  Init 1 Completion<br>1100  Init 2 Posted<br>1101  Init 2 Non Posted<br>1110  Init 2 Completion<br>**----- End of picture text -----**<br>


**224**

**Chapter 6: Flow Control**

*Figure 6‐6: Devices Send InitFC1 in the DL_Init State*

**==> picture [366 x 338] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIeX-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters RCV Buffers FC Counters RCV Buffers<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>InitFC1-P InitFC1-NP InitFC1-Cpl<br>InitFC1-Cpl InitFC1-NP InitFC1-P<br>- Note required order of InitFC transmission<br>InitFC1 P<br>**----- End of picture text -----**<br>


## **FC_Init2 Details**

在此状态下，设备连续发送 InitFC2 DLLPs。这些 DLLP 以与 InitFC1s 相同的顺序发送，并包含相同的信用信息，但它们还确认发送方已成功完成 FC 初始化。由于设备已从邻居注册了值，它不需要任何更多的信用信息，并将忽略任何传入的 InitFC1，同时等待看到 InitFC2s。它甚至可以在此时发送 TLP，即使初始化未在链路的另一侧完成，这由 DL_Up 信号指示给 Transaction Layer（参见图 6‐7）。

**225**

**PCI Express Technology**

为什么需要这个第二个初始化步骤？简单的答案是，相邻设备可能在不同时间完成 FC 初始化，此方法确保晚完成的设备将继续接收其所需的 FC 信息，即使邻居提前完成。一旦设备收到任何缓冲区类型的 FC_INIT2 包，它会设置内部标志（Fl2）。（它不等待收到每个类型的 FC_Init2。）请注意，FL2 也会在收到 UpdateFC 包或 TLP 时设置。当两侧都完成并已发送 InitFC2s 时，DLCMSM 转换到 DL_Active 状态，Link Layer 已准备好进行正常操作。

*Figure 6‐7: FC Values Registered ‐ Send InitFC2s, Report DL_Up_*

**==> picture [346 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core  Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer  Transaction Layer<br>DL_Up<br>DLL DLCMSM  DLL DLCMSMDLCMSM<br>Phy Phy<br>LTSSM  LTSSM<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>InitFC2-Cpl InitFC2-NP InitFC2-P<br>**----- End of picture text -----**<br>


## **Rate of FC_INIT1 and FC_INIT2 Transmission**

规范定义 FC_INIT DLLPs 之间的延迟如下：

**226**

**Chapter 6: Flow Control**

- **VC0**。VC0 的硬件启动流控要求 FC_INIT1 和 FC_INIT2 包"以最大可能速率连续"传输。即，重传计时器设置为零值。

- **VC1‐VC7**。当软件启动其他 VC 的流控初始化时，FC_INIT 序列在"没有其他 TLP 或 DLLP 可用于传输"时重复。然而，一个序列的开始到下一个序列的开始之间的延迟不能大于 17μs。

## **Violations of the Flow Control Initialization Protocol**

设备可以选择性地检查流控初始化协议的违反情况。检测到的错误可以报告为 Data Link Layer 协议错误。

## **Introduction to the Flow Control Mechanism**

## **General**

规范使用寄存器、计数器以及用于报告、跟踪和计算是否可以发送事务的机制来定义 Flow Control 机制的要求。不需要这些元素，实际实现留给设备设计者。本节介绍规范模型，并用于解释概念和定义要求。

## **The Flow Control Elements**

图 6‐8 说明了用于管理流控的元素。该图显示了事务在单个方向上跨链路流动，而另一组这些元素支持在相反方向上的传输。每个元素的主要功能列在下面。虽然这些 Flow Control 元素为所有六个接收缓冲区复制，但为简单起见，本示例仅处理 non‐posted header 流控。

与流控管理相关联的最后一个元素是 Flow Control Update DLLP。这是正常传输期间使用的唯一 Flow Control 包。FC Update 包的格式在第 229 页的图 6‐9 中说明。

**227**

**PCI Express Technology**

*Figure 6‐8: Flow Control Elements*

**==> picture [380 x 251] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>FC Gating Logic<br>PTLP<br>Transactions CC+PTLP =CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>Credits<br>Consumed Credit Limit VC0<br>Incr Check FC<br>Buffer<br>Link Packet optional incr<br>Control<br>incr Credits Rcv CredAlloc (NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC DLLPs<br>TLP Link<br>**----- End of picture text -----**<br>


## **Transmitter Elements**

- **Transactions Pending Buffer** — 保存正在同一虚拟通道中等待发送的事务。

- **Credits Consumed counter** — 包含此缓冲区发送的所有事务的信用总和。此计数缩写为 "CC"。

- **Credit Limit counter** — 由接收方使用相应 Flow Control 缓冲区的大小初始化。初始化后，Flow Control update 包被定期发送以更新 Flow Control 信用，因为它们在接收方变得可用。此值缩写为 "CL"。

- **Flow Control Gating Logic** — 执行计算以确定接收方是否具有足够的 Flow Control 信用来接受挂起的 TLP (PTLP)。本质上，此逻辑检查 CREDITS_CONSUMED (CC) 加上下一个挂起的 TLP (PTLP) 所需的信用不超过 CREDIT_LIMIT (CL)。本规范定义了用于执行检查的以下等式，所有值均以信用表示。

**228**

**Chapter 6: Flow Control**

_CL_ – (_CC_ + _PTLP_) _mod_ 2^[_FieldSize_] ≤ 2^[_FieldSize_] / 2

有关此等式的应用示例，请参见第 230 页 "Stage 1 — Flow Control Following Initialization"。

## **Receiver Elements**

- **Flow Control Buffer** — 存储传入的 headers 或 data。

- **Credit Allocated** — 跟踪已分配（可用）的总 Flow Control 信用。它由硬件初始化以反映关联的 Flow Control 缓冲区的大小。缓冲区随着事务到达而填充，但最终它们由接收方的核心逻辑从缓冲区中移除。当它们被移除时，Flow Control 信用数被添加到 CREDIT_ALLOCATED 计数器中。因此，计数器跟踪当前可用的信用数。
