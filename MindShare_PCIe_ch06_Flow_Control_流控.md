# 📘 第 6 章　流控 (Chapter 6. Flow Control)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0244.md` ... `chunks/chunk0253.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Flow Control](#-本章目录-table-of-contents)

<a id="sec-6-1"></a>
## 6.1 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

This chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Trans‐ action Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like discon‐ nects, retries, and wait‐states. 

## **The Next Chapter** 

The next chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different pack‐ ets traversing the fabric. These mechanisms include application‐specific soft‐ ware that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **Flow Control Concept** 

Ports at each end of every PCIe Link must implement Flow Control. Before a packet can be transmitted, flow control checks must verify that the receiving port has sufficient buffer space to accept it. In parallel bus architectures like PCI, transactions are attempted without knowing whether the target is prepared to handle the data. If the request is rejected due to insufficient buffer space, the transaction is repeated (retried) until it completes. This is the “Delayed Transac‐ tion Model” of PCI and while it works the efficiency is poor. 

**215** 

## **PCI Ex ress Technolo p gy** 

Flow Control mechanisms can improve transmission efficiency if multiple Vir‐ tual Channels (VCs) are used. Each Virtual Channel carries transactions that are independent from the traffic flowing in other VCs because flow‐control buffers are maintained separately. Therefore, a full Flow Control buffer in one VC will not block access to other VC buffers. PCIe supports up to 8 Virtual Channels. 

The Flow Control mechanism uses a credit‐based mechanism that allows the transmitting port to be aware of buffer space available at the receiving port. As part of its initialization, each receiver reports the size of its buffers to the trans‐ mitter on the other end of the Link, and then during run‐time it regularly updates the number of credits available using Flow Control DLLPs. Technically, of course, DLLPs are overhead because they don’t convey any data payload, but they are kept small (always 8 symbols in size) to minimize their impact on per‐ formance. 

Flow control logic is actually a shared responsibility between two layers: the Transaction Layer contains the counters, but the Link Layer sends and receives the DLLPs that convey the information. Figure 6‐1 on page 217 illustrates that shared responsibility. In the process of making flow control work: 

- **Devices Report Available Buffer Space** — The receiver of each port reports the size of its Flow Control buffers in units called credits. The number of credits within a buffer is sent from the receive‐side transaction layer to the transmit‐side of the Link Layer. At the appropriate times, the Link Layer creates a Flow Control DLLP to forward this credit information to the receiver at the other end of the Link for each Flow Control Buffer. 

- **Receivers Register Credits** — The receiver gets Flow Control DLLPs and transfers the credit values to the transmit‐side of the transaction layer. The completes the transfer of credits from one link partner to the other. These actions are performed in both directions until all flow control information has been exchanged. 

- **Transmitters Check Credits** — Before it can send a TLP, a transmitter checks the Flow Control Counters to learn whether sufficient credits are available. If so, the TLP is forwarded to the Link Layer but, if not, the trans‐ action is blocked until more Flow Control credits are reported. 

**216** 

**Chapter 6: Flow Control** 

_Figure 6‐1: Location of Flow Control Logic_ 

**==> picture [371 x 310] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters FC Buffers FC Counters FC Buffers<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>Link<br>**----- End of picture text -----**<br>


## **Flow Control Buffers and Credits** 

Flow control buffers are implemented for each VC resource supported by a port. Recall that ports at each end of the Link may not support the same number of VCs, therefore the maximum number of VCs configured and enabled by soft‐ ware is the highest common number between the two ports. 

**217** 

**PCI Ex ress Technolo p gy** 

## **VC Flow Control Buffer Organization** 

Each VC Flow Control buffer at the receiver is managed for each category of transaction flowing through the virtual channel. These categories are: 

- Posted Transactions — Memory Writes and Messages 

- Non‐Posted Transactions — Memory Reads, Configuration Reads and Writes, and I/O Reads and Writes 

- Completions — Read and Write Completions 

In addition, each of these categories is separated into header and data portions for transactions that have both header and data. This yields six different buffers each of which implements its own flow control (see Figure 6‐2 on page 218). 

Some transactions, like read requests, consist of a header only while others, like write requests, have both a header and data. The transmitter must ensure that both header and data buffer space is available as needed for a transaction before it can be sent. Note that transaction ordering must be maintained within a VC Flow Control buffer when the transactions are forwarded to software or to an egress port in the case of a switch. Consequently, the receiver must also track the order of header and data components within the buffer. 

_Figure 6‐2: Flow Control Buffer Organization_ 

**==> picture [379 x 224] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Flow Control Buffers (Receiver)<br>Device Core Device Core<br>(PH) (PD) (NPH) (NPD) (CPLH) (CPLD)<br>PCIe-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters RCV Buffers P Posted Request<br>P NP CPL P NP CPL<br>NP Non-Posted Request<br>Data Link Layer Data Link Layer CPL Completion<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>Link<br>**----- End of picture text -----**<br>


**218** 

**Chapter 6: Flow Control** 

## **Flow Control Credits** 

Buffer space is reported by the receiver in units called Flow Control credits. The unit value of Flow Control Credits (FCCs) for header and data buffers are: 

- Header credits — maximum header size + digest 

   - 4 DWs for completions 

   - 5 DWs for requests 

- Data credits — 4 DWs (aligned 16 bytes) 

Flow Control DLLPs communicate this information, and do not require Flow Control credits themselves. That’s because they originate and terminate at the Link Layer and don’t use the Transaction Layer buffers. 

## **Initial Flow Control Advertisement** 

During Flow Control initialization, PCIe devices communicate their buffer sizes by “advertising” their buffer space via flow control credits. PCIe also defines an infinite Flow Control credit value that is required for some buffers. A receiver that advertises infinite buffer space is effectively guaranteeing that its buffer space will never overflow. 

## **Minimum and Maximum Flow Control Advertisement** 

The specification defines the minimum number of credits that can be reported for the different Flow Control buffer types as listed in Table 6‐1. However, devices normally advertise considerably more credits than the minimum. Table 6‐2 on page 220 lists the maximum advertisement allowed by the specifi‐ cation. 

_Table 6‐1: Required Minimum Flow Control Advertisements_ 

|Credit Type|**Minimum Advertisement**|
|---|---|
|Posted Request Header (PH)|1 unit. Credit Value = one 4DW HDR + Digest = 5DW.|
|Posted Request Data (PD)|Largest possible setting of the Max_Payload_Size in<br>credits. Example: If the largest Max_Payload_Size value<br>supported is 1024 bytes, the smallest permitted initial<br>credit value would be 040h.|



**219** 

## **PCI Ex ress Technolo p gy** 

_Table 6‐1: Required Minimum Flow Control Advertisements (Continued)_ 

|Credit Type|**Minimum Advertisement**|
|---|---|
|Non‐Posted Request HDR (NPH)|**1 unit**. Credit Value = one 4 DW HDR + Digest = 5DW.|
|Non‐Posted Request Data (NPD)|**1 unit**. Credit Value = 4DW.<br>**2 unit**. Receivers supporting AtomicOp routing or<br>AtomicOp Completer capability have credit value of 02h|
|Completion HDR (CPLH)|**1 unit**. Credit Value = one 3DW HDR + Digest = 4DW;<br>for Root Complex with peer‐to‐peer support and<br>Switches.<br>**Infinite units.**Initial Credit Value = all 0’s for Root Com‐<br>plex with no peer‐to‐peer support and Endpoints.|
|Completion Data (CPLD)|**n unit**. Value of largest possible setting of<br>Max_Payload_Size or size of largest Read Request<br>(which ever is smaller) divided by FC Unit Size (4DW);<br>for Root Complex with peer‐to‐peer support and<br>Switches.<br>**Infinite units**. Initial Credit Value = all 0’s; for Root<br>Complex with no peer‐to‐peer support and Endpoints.|



_Table 6‐2: Maximum Flow Control Advertisements_ 

|**Credit Type**|**Maximum Advertisement**|
|---|---|
|Posted Request Header (PH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes.|
|Posted Request Data (PD)|2048 units. Value of the Max_Payload_Size (4096 bytes)<br>including all functions supported by device (8) divided<br>by the credit size (4 DWs) = 32,768 bytes<br>2048 credits @ 4 DWs = 32,768 bytes|
|Non‐Posted Request HDR (NPH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes.|
|Non‐Posted Request Data (NPD)|The author’s could not find a precise value for the maxi‐<br>mum number of credits for Non‐Posted Data. The maxi‐<br>mum number of credits listed for Data is 2048. However,<br>a more reasonable approach might use the Non‐Posted<br>header limit of 128 credits, because Non‐Posted Data is<br>always associated with Non‐Posted Headers.|



**220** 

**Chapter 6: Flow Control** 

_Table 6‐2: Maximum Flow Control Advertisements (Continued)_ 

|**Credit Type**|**Maximum Advertisement**|
|---|---|
|Completion HDR (CPLH)|**128 units**. 128 credits @ 5 DWs = 2,560 bytes. This in<br>the limit for ports that do not originate transactions (e.g.,<br>Root Complex with peer‐to‐peer support and Switches).<br>**Infinite units**. Initial Credit Value = all 0’s for ports that<br>originate transactions (e.g., Root Complex with no peer‐<br>to‐peer support and Endpoints).|
|Completion Data (CPLD)|**2048 units**. Value of the Max_Payload_Size (4096 bytes)<br>including all functions supported by a device (8)<br>divided by the credit size (4 DWs) = 32,768 bytes<br>2048 credits @ 4 DWs = 32,768 bytes<br>**Infinite units**. Initial Credit Value = all 0’s for ports that<br>originate transactions (e.g., Root Complex with no peer‐<br>to‐peer support and Endpoints).|



## **Infinite Credits** 

Note that a flow control value of 00h will be understood to mean infinite credits during initialization. Following Flow‐Control initialization no further advertise‐ ments are made. Devices that originate transactions must reserve buffer space for the data or status information that will return during split transactions. These transaction combinations include: 

- Non‐posted Read requests and return of Completion Data 

- Non‐posted Read requests and return of Completion Status 

- Non‐posted Write requests and return of Completion Status 

## **Special Use for Infinite Credit Advertisements.**

</td>
<td style="background-color:#e8e8e8">

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

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-2"></a>
## 6.2 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The specification points out a special consideration for devices that implement only VC0. For example, the only Non‐Posted writes are I/O Writes and Configu‐ ration Writes both of which are permitted only on VC0. Thus, Non‐Posted data buffers are not used for VC1 ‐ VC7 and an infinite value can be advertised for those values. However, the Non‐Posted Header must still operate and header credits must still need to be updated. 

**221** 

**PCI Ex ress Technolo p gy** 

## **Flow Control Initialization** 

## **General** 

Prior to sending any transactions, flow control initialization is needed. In fact, TLPs cannot be sent across the Link until Flow Control Initialization is per‐ formed successfully. Initialization occurs on every Link in the system and involves a handshake between the devices at each end of a link. This process begins as soon as the Physical Layer link training has completed. The Link Layer knows the Physical Layer is ready when it observes the LinkUp signal is active, as illustrated in Figure 6‐3. 

_Figure 6‐3: Physical Layer Reports That It’s Ready_ 

**==> picture [338 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core  Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer  Transaction Layer<br>DLL DLCMSM  DLL DLCMSM DLCMSM<br>LinkUp LinkUp<br>Phy Phy<br>LTSSM  LTSSM<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>


Once started, the Flow Control initialization process is fundamentally the same for all Virtual Channels and is controlled by hardware once a VC has been enabled. VC0 is always enabled by default, so its initialization is automatic. 

**222** 

**Chapter 6: Flow Control** 

That allows configuration transactions to traverse the topology and carry out the enumeration process. Other VCs only initialize when configuration soft‐ ware has set up and enabled them at both ends of the Link. 

## **The FC Initialization Sequence** 

The flow control initialization process involves the Link Layer’s DLCMSM (Data Link Control and Management State Machine). As shown in Figure 6‐4 on page 223, a reset puts the state machine into the DL_Inactive state. While in the DL_Inactive state, DL_Down is signaled to both the Link and Transaction Lay‐ ers. Meanwhile, it waits to see LinkUp from the Physical Layer to indicate that the LTSSM has finished its work and the Physical Layer is ready. That causes a transition to the DL_Init sub‐state, which contains two stages that handle flow control initialization: FC_INIT1 and FC_INIT2. 

_Figure 6‐4: The Data Link Control & Management State Machine_ 

**==> picture [251 x 287] intentionally omitted <==**

**----- Start of picture text -----**<br>
Reset<br>DL_Inactive Report DL_Down to Link<br>and Transaction Layers<br>Physical LinkUp=1<br>Physical LinkUp=0 &<br>Link Enabled andr<br>DL_Init<br>Report DL_Down<br>FC_Init1<br>(during FC_Init1)<br>Report DL_Up to remaining<br>FC_Init2<br>Link and Transaction Layers<br>(during FC_Init2)<br>FC_Init Complete<br>&<br>Physical LinkUp=1<br>DL_Active Report DL_Up<br>**----- End of picture text -----**<br>


**223** 

**PCI Ex ress Technolo p gy** 

## **FC_Init1 Details** 

During the FC_INIT1 state, devices continuously send a sequence of 3 InitFC1 Flow Control DLLPs advertising their receiver buffer sizes (see Figure 6‐5). According to the spec, the packets must be sent in this order: Posted, Non‐ posted, and Completions as illustrated in Figure 6‐6 on page 225. The specifica‐ tion strongly encourages that these be repeated frequently to make it easier for the receiving device to see them, especially if there are no TLPs or DLLPs to send. Each device should also receive this sequence from its neighbor so it can register the buffer sizes. Once a device has sent its own values and received the complete sequence enough times to be confident that the values were seen cor‐ rectly, it’s ready to exit FC_INIT1. To do that, it records the received values in its transmit counters, sets an internal flag (FL1), and changes to the FC_INIT2 state to begin the second initialization step. 

_Figure 6‐5: INIT1 Flow Control DLLP Format and Contents_ 

**==> picture [373 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataHdr FC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>0100  Init 1 Posted<br>0101  Init 1 Non Posted<br>0110  Init 1 Completion<br>1100  Init 2 Posted<br>1101  Init 2 Non Posted<br>1110  Init 2 Completion<br>**----- End of picture text -----**<br>


**224** 

**Chapter 6: Flow Control** 

_Figure 6‐6: Devices Send InitFC1 in the DL_Init State_ 

**==> picture [366 x 338] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIeX-Core PCIe-Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>FC Counters RCV Buffers FC Counters RCV Buffers<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(TX) (RX) (TX) (RX)<br>InitFC1-P InitFC1-NP InitFC1-Cpl<br>InitFC1-Cpl InitFC1-NP InitFC1-P<br>- Note required order of InitFC transmission<br>InitFC1 P<br>**----- End of picture text -----**<br>


## **FC_Init2 Details** 

In this state a device continuously sends InitFC2 DLLPs. These are sent in the same sequence as the InitFC1s and contain the same credit information, but they also confirm that FC initialization has succeeded at the sender. Since the device has already registered the values from the neighbor it doesn’t need any more credit information and will ignore any incoming InitFC1s while it waits to see InitFC2s. It can even send TLPs at this point, even though initialization hasn’t completed for the other side of the Link, and this is indicated to the Transaction Layer by the DL_Up signal (See Figure 6‐7). 

**225** 

## **PCI Ex ress Technolo p gy** 

Why is this second initialization step needed? The simple answer is that neigh‐ boring devices may finish FC initialization at different times and this method ensures that the late one will continue to receive the FC information it needs even if the neighbor finishes early. Once a device receives an FC_INIT2 packet for any buffer type, it sets an internal flag (Fl2). (It doesnʹt wait to receive an FC_Init2 for each type.) Note that FL2 is also set upon receipt of an UpdateFC packet or TLP. When both sides are done and have sent InitFC2s, the DLCMSM transitions to the DL_Active state and the Link Layer is ready for normal opera‐ tion. 

_Figure 6‐7: FC Values Registered ‐ Send InitFC2s, Report DL_Up_ 

**==> picture [346 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core  Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer  Transaction Layer<br>DL_Up<br>DLL DLCMSM  DLL DLCMSMDLCMSM<br>Phy Phy<br>LTSSM  LTSSM<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>InitFC2-Cpl InitFC2-NP InitFC2-P<br>**----- End of picture text -----**<br>


## **Rate of FC_INIT1 and FC_INIT2 Transmission** 

The specification defines the latency between sending FC_INIT DLLPs as fol‐ lows: 

**226** 

**Chapter 6: Flow Control** 

- **VC0** . Hardware‐initiated flow control of VC0 requires that FC_INIT1 and FC_INIT2 packets be transmitted “continuously at the maximum rate possi‐ ble.” That is, the resend timer is set to a value of zero. 

- **VC1‐VC7** . When software initiates flow control initialization for other VCs, the FC_INIT sequence is repeated “when no other TLPs or DLLPs are avail‐ able for transmission.” However, the latency between the beginning of one sequence to the next can be no greater than 17μs. 

## **Violations of the Flow Control Initialization Protocol** 

A violation of the flow control initialization protocol can be optionally checked by a device. An error detected can be reported as a Data Link Layer protocol error. 

## **Introduction to the Flow Control Mechanism** 

## **General** 

The specification defines the requirements of the Flow Control mechanism using registers, counters, and mechanisms for reporting, tracking, and calculat‐ ing whether a transaction can be sent. These elements are not required and the actual implementation is left to the device designer. This section introduces the specification model and serves to explain the concepts and to define the require‐ ments. 

## **The Flow Control Elements** 

Figure 6‐8 illustrates the elements used for managing flow control. The diagram shows transactions flowing in a single direction across a Link, and another set of these elements supports transfers in the opposite direction. The primary function of each element is listed below. While these Flow Control elements are duplicated for all six receive buffers, for simplicity this example only deals with non‐posted header flow control. 

One final element associated with managing flow control is the Flow Control Update DLLP. This is the only Flow Control packet that is used during normal transmission. The format of the FC Update packet is illustrated in Figure 6‐9 on page 229. 

**227** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐8: Flow Control Elements_ 

**==> picture [380 x 251] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>FC Gating Logic<br>PTLP<br>Transactions CC+PTLP =CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>Credits<br>Consumed Credit Limit VC0<br>Incr Check FC<br>Buffer<br>Link Packet optional incr<br>Control<br>incr Credits Rcv CredAlloc (NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC DLLPs<br>TLP Link<br>**----- End of picture text -----**<br>


## **Transmitter Elements** 

- **Transactions Pending Buffer** — holds transactions that are waiting to be sent in the same virtual channel. 

- **Credits Consumed counter** — contains the credit sum of all transactions sent for this buffer. This count is abbreviated “CC.” 

- **Credit Limit counter** — initialized by the receiver with the size of the corre‐ sponding Flow Control buffer. After initialization, Flow Control update packets are sent periodically to update the Flow Control credits as they become available at the receiver. This value is abbreviated “CL.” 

- **Flow Control Gating Logic** — performs the calculations to determine if the receiver has sufficient Flow Control credits to accept the pending TLP (PTLP). In essence, this logic checks that the CREDITS_CONSUMED (CC) plus the credits required for the next Pending TLP (PTLP) does not exceed the CREDIT_LIMIT (CL). This specification defines the following equation for performing the check, with all values represented in credits. 

**228** 

**Chapter 6: Flow Control** 

_CL_ –  _CC_ + _PTLP_  _mod_ 2  _[FieldSize]_   2  _[FieldSize]_   2 

For an example application of this equation, See “Stage 1 — Flow Control Fol‐ lowing Initialization” on page 230. 

## **Receiver Elements** 

- **Flow Control Buffer** — stores incoming headers or data. 

- **Credit Allocated** — tracks the total Flow Control credits that have been allocated (made available). It’s initialized by hardware to reflect the size of the associated Flow Control buffer. The buffer fills as transactions arrive but then they are eventually removed from the buffer by the core logic at the receiver. When they are removed, the number of Flow Control credits is added to the CREDIT_ALLOCATED counter. Thus the counter tracks the number of credits currently available.

</td>
<td style="background-color:#e8e8e8">

- **Credits Received counter (optional)** — 跟踪接收到 Flow Control 缓冲区的所有 TLP 的总信用数。当流控正常运行时，CREDITS_RECEIVED 计数应等于或小于 CREDIT_ALLOCATED 计数。如果此测试结果为 false，则表示发生了流控缓冲区溢出并检测到错误。规范建议实现此可选机制，并指出此处的失败将被视为致命错误。

*Figure 6‐9: Types and Format of Flow Control DLLPs*

**==> picture [374 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataFCHdrFC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>1000  Update Posted<br>1001  Update Non Posted<br>1010  Update Completion<br>**----- End of picture text -----**<br>


**229**

**PCI Express Technology**

## **Flow Control Example**

以下示例描述了 non‐posted header Flow Control 缓冲区，并试图在多种情况下捕获流控实现的细微差别。Flow Control 的讨论以一系列基本阶段描述如下：

**Stage One** — 初始化后立即发送一个事务并进行跟踪，以解释计数器和寄存器的基本操作。

**Stage Two** — 发送方比接收方处理事务的速度更快，缓冲区变满。

**Stage Three** — 当计数器回绕到零时，机制仍然有效，但有几个问题需要考虑。

**Stage Four** — 缓冲区溢出的可选接收方错误检查。

## **Stage 1 — Flow Control Following Initialization**

一旦流控初始化完成，设备就准备好进行正常操作。在我们的示例中，Flow Control 缓冲区为 2KB。我们正在描述 non‐posted header 缓冲区，每个信用为 5 dwords 或 20 字节。这意味着有 102d (66h) 个 Flow Control 单位可用。第 231 页的图 6‐10 说明了所涉及的元素，包括流控初始化后每个计数器和寄存器中的值。

当发送方准备好发送 TLP 时，它必须首先检查 Flow Control 信用。我们的示例很简单，因为 non‐posted header 是唯一正在发送的包，它始终只需要一个 Flow Control 信用，并且我们还假设事务中不包含数据。

使用无符号算术（2 的补码）进行 header 信用检查，并且必须满足以下公式：

**==> picture [193 x 13] intentionally omitted <==**

将图 6‐10 中的值代入：

66_h – (00_h + 01_h) _mod_ 2[8] ≤ 2[8] / 2  66_h – 01_h mod 256 ≤ 80_h

**230**

**Chapter 6: Flow Control**

*Figure 6‐10: Flow Control Elements Following Initialization*

**==> picture [376 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 00h CL = 66h<br>FC<br>Incr Check<br>Buffer<br>Link Packet optional incr<br>Control<br>incr CrRcv=00h CrAl=66h<br>(NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>CrAl = Credits Allocated<br>CC = Credits Consumed<br>CrRcv = Credits Received<br>CL = Credit Limit<br>PTLP = Pending TLP<br>**----- End of picture text -----**<br>


在这种情况下，将当前 CREDITS_CONSUMED 计数 (CC) 与 PTLP 所需信用相加，以确定 CREDITS_REQUIRED (CR)，即 00h + 01h = 01h。从 CREDIT_LIMIT 计数 (CL) 中减去 CREDITS_REQUIRED 计数以确定是否有足够的信用。

以下描述包含对 2 的补码减法的简要回顾。当使用 2 的补码执行减法时，要减去的数字被取反（1 的补码），然后加 1（2 的补码）。然后将此值添加到我们要从中减去的数字。由于加法而产生的任何进位都将被丢弃。

**231**

**PCI Express Technology**

信用检查：

```
CL 01100110b (66h) - CR 00000001b (01h) = n
```

CR 转换为 2 的补码：

`00000001b` (CR) `11111110b` (CR 取反) `11111110b + 1 11111111b` (2 的补码)

将 2 的补码加到 CL 上：

```
01100110 (CL)
11111111(2 的补码 of CR)
01100101 = 65h (carry bit is dropped)
```

结果是否 <= 80h？是的。如果减法结果等于或小于最大值的一半（用 modulo 256 计数器跟踪为 128），那么我们知道接收方缓冲区中有足够的空间，可以发送此包。仅使用一半的计数器值的决定避免了潜在的计数别名问题。请参见第 234 页 "Stage 3 — Counters Roll Over"。

*Figure 6‐11: Flow Control Elements After First TLP Sent*

**==> picture [370 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 01h CL = 66h FC<br>Incr Check Buffer<br>Link Packet optional incr<br>Control (NP Hdr)<br>incr CrRcv=01h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


**232**

**Chapter 6: Flow Control**

## **Stage 2 — Flow Control Buffer Fills Up**

假设现在接收方已经有一段时间无法从 Flow Control 缓冲区中移除事务。也许设备核心逻辑暂时忙碌，无法处理事务。最终，Flow Control 缓冲区变得完全填满，如第 234 页的图 6‐12 所示。如果发送方希望发送另一个 TLP 并检查 Flow Control 信用：

Credit Limit (CL)= 66h Credits Required (CR) = 67h

## `CL 01100110` (66)

`CR 10011001` (加 67h 的 2 的补码)

`11111111 = FFh <= 80h` (不正确；不发送包)

此通道被阻塞，直到收到具有 67h 或更大的新 CREDIT_LIMIT 值的 Update Flow Control DLLP。当新值被加载到 CL 寄存器中时，发送方信用检查将通过测试，并且可以发送 TLP。

- `CL 01100111` (67)

- `CR 10011001` 加 67 的 2 的补码

   - `00000000 = 00h <= 80h` (true, send transaction

**233**

**PCI Express Technology**

*Figure 6‐12: Flow Control Elements with Flow Control Buffer Filled*

**==> picture [376 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>CC = 66h CL = 66h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


## **Stage 3 — Counters Roll Over**

由于 Credit Limit (CL) 和 Credits Required (CR) 计数仅向上递增，它们最终会回绕到零。当 CL 回绕而 CR 没有回绕时，信用检查 (CL‐CR) 导致 CL 值较小而 CR 值较大。然而，使用无符号算术时看似的问题实际上并不存在。如前所述的示例所示，在执行 2 的补码减法时，结果会被正确处理。第 235 页的图 6‐13 显示了 CL 回绕前后以及 2 的补码结果的 CL 和 CR 计数。

**234**

**Chapter 6: Flow Control**

## *Figure 6‐13: Flow Control Rollover Problem*

**==> picture [368 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Before CL Rollover After CL Rollover<br>FFh<br>NTS = FF8h (4088d)CL = F8h AS = FE8h (4072d)CR = F8h<br>Available<br>Credit Available<br>NTS<br>Credit is the<br>AS = FE8h (4072d)CR = E8h Rollover<br>sum of these<br>two parts<br>NTS = FF8h (4088d)CL = 08h<br>00h<br>Using 2's complement: Using 2's complement:<br>  CL 11111000 (F8h)   CL 00001000 (08h)<br>+ CR 00011000 (E8h 2's complement) + CR 00001000 (F8h 2's complement)<br>  =  00010000 (0Fh)   =  00010000 (0Fh)<br>**----- End of picture text -----**<br>


## **Stage 4 — FC Buffer Overflow Error Check**

虽然可以选择性地执行此操作，但规范建议实现 FC 缓冲区溢出错误检查机制。第 236 页的图 6‐14 显示了与溢出错误检查相关联的元素，包括：

- Credits Received (CR) counter

- Credits Allocated (CA) counter

- Error Check Logic

这允许接收方以与发送方相同的方式跟踪 Flow Control 信用。如果流控工作正常，发送方的 Credits Consumed 计数永远不会超过其 Credit Limit，接收方的 Credits Received 计数永远不会超过其 Credits Allocated 计数。

**235**

**PCI Express Technology**

如果以下公式评估为 true，则检测到溢出情况。请注意，字段大小为 8（headers）或 12（data）：

**==> picture [161 x 12] intentionally omitted <==**

如果它确实评估为 true，则表示发送到 FC 缓冲区的信用超过了可用信用，因此发生了溢出。请注意，规范的 1.0a 版本将等式定义为 ≥ 而不是如上所示的 >。这似乎是一个错误，因为当 CA = CR 时不存在溢出情况。

*Figure 6‐14: Buffer Overflow Error Check*

**==> picture [350 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=67h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


**236**

**Chapter 6: Flow Control**

## **Flow Control Updates**

接收方必须定期使用在从事务中移除缓冲区时可用的 Flow Control 信用来更新其相邻设备。第 238 页的图 6‐15 说明了一个示例，其中发送方先前因为缓冲区已满而无法发送 header 事务。在图示中，接收方刚刚从 Flow Control 缓冲区中移除了三个 headers。现在有更多空间可用，但相邻设备不知道这一点。随着 headers 从缓冲区中移除，CREDITS_ALLOCATED 计数从 66h 增加到 69h。该新计数使用 Flow Control update 包报告给相邻设备的 CREDIT_LIMIT 寄存器。一旦更新了信用限制，就可以继续传输其他 TLP。

这里一个有趣的注意点是，update 报告了 Credits Allocated 寄存器的实际值。仅报告寄存器的变化也可以工作，例如"+3 credits on NP Headers"，但这代表了一个潜在问题。要了解此风险，请考虑如果包含增量信息的 DLLP 因某种原因丢失会发生什么情况。没有 DLLPs 的重传机制；如果发生错误，包将被简单丢弃。在这种情况下，增量信息将丢失而无法恢复。

另一方面，如果报告了寄存器的实际值并且 DLLP 失败，则下一个成功的 DLLP 将使计数器重新同步。在这种情况下，如果发送方正在等待 FC 信用才能发送下一个 TLP，则可能会浪费一些时间，但不会丢失任何信息。

**237**

**PCI Express Technology**

*Figure 6‐15: Flow Control Update Example*

**==> picture [368 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=69h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


## **FC_Update DLLP Format and Content**

回想一下，Flow Control update 包与 Flow Control 初始化包一样，包含两个信用字段，一个用于 header，一个用于 data，如第 239 页的图 6‐16 所示。接收方的 HdrFC 和 DataFC 字段中报告的信用值可能自上次发送 update 包以来已更新多次或根本没有更新。

**238**

**Chapter 6: Flow Control**

*Figure 6‐16: Update Flow Control Packet Format and Contents*

## **Flow Control Update Frequency**

规范定义了多种规则和建议的实现，用于管理何时以及多久发送一次 Flow Control Update DLLPs。这些规则的动机是：

- 尽可能早地通知发送设备有关新分配的信用，特别是如果任何事务先前被阻塞。

- 建立 FC Packets 之间的最坏情况延迟。

- 平衡与流控操作相关的要求，例如：— 需要足够频繁地报告信用以防止事务阻塞

- — 减少 FC_Update DLLPs 所需的链路带宽的愿望

- — 选择最佳缓冲区大小

   - 选择最大数据负载大小

- 检测 Flow Control 包之间最大延迟的违反。

仅当链路处于活动状态 (L0 或 L0s) 时才允许 Flow Control 更新。所有其他链路状态表示更积极的电源管理，具有更长的恢复延迟。

## **Immediate Notification of Credits Allocated**

当 Flow Control 缓冲区已满到无法发送最大大小的包时，规范要求在有更多空间可用时立即交付 FC_Update DLLP。存在两种情况：

**239**

**PCI Express Technology**

- **Maximum Packet Size = 1 Credit.** 当由于 non‐infinite NPH、NPD、PH 和 CPLH 缓冲区类型的缓冲区已满条件导致包传输被阻塞时，必须在为一个或多个该缓冲区类型分配信用时调度 UpdateFC 包进行传输。

- **Maximum Packet Size = Max_Payload_Size.** Flow Control 缓冲区空间可能减少到无法为 non‐infinite PD 和 CPLD 信用类型发送最大大小的包的程度。在这种情况下，当分配一个或多个额外信用时，必须调度 Update FCP 进行传输。

## **Maximum Latency Between Update Flow Control DLLPs**

每个 FC 信用类型（non‐infinite）的 Update FCP 的传输频率必须调度为至少每 30 μs (‐0%/+50%) 传输一次。如果 Control Link 寄存器中的 Extended Sync 位被设置，则更新必须调度为不超过每 120 μs (‐0%/+50%) 传输一次。请注意，Update FCPs 的调度传输频率可以比要求更频繁。

## **Calculating Update Frequency Based on Payload Size and Link Width**

规范提供了一个公式，用于根据最大数据负载大小和链路宽度计算需要发送 update 包的频率。该公式（如下所示）以 symbol time 定义 FC Update 传递间隔。作为参考，symbol time 定义为传递一个 symbol 所需的时间：Gen1 为 4ns，Gen2 为 2ns，Gen3 为 1ns。表 6‐3、表 6‐4 和表 6‐5 显示了每种速度的未调整 FC Update 值。

---------------------------------------------------------------------------------------------------------------------------------------（_MaxPayloadSize_ + _TLPOverhead_） × _UpdateFactor_ / **MaxPayloadSize** = Device Control 寄存器的 Max_Payload_Size 字段中的值

- **TLPOverhead** = 常量值（28 个 symbol），表示消耗链路带宽的附加 TLP 组件（TLP Prefix、Sequence Number、Packet Header、LCRC、Framing Symbols）

- **UpdateFactor** = 在两次收到的 UpdateFC 包之间发送的最大大小 TLP 的数量。此数字旨在平衡链路带宽效率和接收缓冲区大小 – 该值随 Max_Payload_Size 和 Link 宽度而变化

**240**

**Chapter 6: Flow Control**

- **LinkWidth** = 链路正在使用的 Lane 数

- **InternalDelay** = 19 个 symbol time 的常量值，表示已接收 TLP 和已发送 DLLP 的内部处理延迟

该公式定义的关系显示，update 包传递的频率随 Linkwidth 的增加而降低，并建议使用一个触发 update 包调度的计时器。请注意，此公式未考虑与接收方或发送方处于 L0s 电源管理状态相关的延迟。

*Table 6‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|237<br>UF=1.4|128<br>UF=1.4|73<br>UF=1.4|67<br>UF=2.5|58<br>UF=3.0|48<br>UF=3.0|33<br>UF=3.0|
|256 Bytes|416<br>FC=1.4|217<br>FC=1.4|118<br>UF=1.4|107<br>UF=2.5|90<br>UF=3.0|72<br>UF=3.0|45<br>UF=3.0|
|512 Bytes|559<br>UF=1.0|289<br>UF=1.0|154<br>UF=1.0|86<br>UF=1.0|109<br>UF=2.0|86<br>UF=2.0|52<br>UF=2.0|
|1024 Bytes|1071<br>UF=1.0|545<br>UF=1.0|282<br>UF=1.0|150<br>UF=1.0|194<br>UF=2.0|150<br>UF=2.0|84<br>UF=2.0|
|2048 Bytes|2095<br>UF=1.0|1057<br>UF=1.0|538<br>UF=1.0|278<br>UF=1.0|365<br>UF=2.0|278<br>UF=2.0|148<br>UF=2.0|
|4096 Bytes|4143<br>UF=1.0|2081<br>UF=1.0|1050<br>UF=1.0|534<br>UF=1.0|706<br>UF=2.0|534<br>UF=2.0|276<br>UF=2.0|

*Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|288<br>UF=1.4|179<br>UF=1.4|124<br>UF=1.4|118<br>UF=2.5|109<br>UF=3.0|99<br>UF=3.0|84<br>UF=3.0|
|256 Bytes|467<br>FC=1.4|268<br>FC=1.4|169<br>UF=1.4|158<br>UF=2.5|141<br>UF=3.0|123<br>UF=3.0|96<br>UF=3.0|

**241**

## **PCI Express Technology**

*Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|512 Bytes|610<br>UF=1.0|340<br>UF=1.0|205<br>UF=1.0|137<br>UF=1.0|160<br>UF=2.0|137<br>UF=2.0|103<br>UF=2.0|
|1024 Bytes|1122<br>UF=1.0|596<br>UF=1.0|333<br>UF=1.0|201<br>UF=1.0|245<br>UF=2.0|201<br>UF=2.0|135<br>UF=2.0|
|2048 Bytes|2146<br>UF=1.0|1108<br>UF=1.0|589<br>UF=1.0|329<br>UF=1.0|416<br>UF=2.0|329<br>UF=2.0|199<br>UF=2.0|
|4096 Bytes|4194<br>UF=1.0|2132<br>UF=1.0|1101<br>UF=1.0|585<br>UF=1.0|757<br>UF=2.0|585<br>UF=2.0|327<br>UF=2.0|

*Table 6‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|333<br>UF=1.4|224<br>UF=1.4|169<br>UF=1.4|163<br>UF=2.5|154<br>UF=3.0|144<br>UF=3.0|129<br>UF=3.0|
|256 Bytes|512<br>FC=1.4|313<br>FC=1.4|214<br>UF=1.4|203<br>UF=2.5|186<br>UF=3.0|168<br>UF=3.0|141<br>UF=3.0|
|512 Bytes|655<br>UF=1.0|385<br>UF=1.0|250<br>UF=1.0|182<br>UF=1.0|205<br>UF=2.0|182<br>UF=2.0|148<br>UF=2.0|
|1024 Bytes|1167<br>UF=1.0|641<br>UF=1.0|378<br>UF=1.0|246<br>UF=1.0|290<br>UF=2.0|246<br>UF=2.0|180<br>UF=2.0|
|2048 Bytes|2191<br>UF=1.0|1153<br>UF=1.0|643<br>UF=1.0|374<br>UF=1.0|461<br>UF=2.0|374<br>UF=2.0|244<br>UF=2.0|
|4096 Bytes|4239<br>UF=1.0|2177<br>UF=1.0|1146<br>UF=1.0|630<br>UF=1.0|802<br>UF=2.0|630<br>UF=2.0|372<br>UF=2.0|

规范认识到该公式对于许多应用（例如那些流式传输大数据块的应用）可能是不够的。这些应用可能需要比指定的最小值更大的缓冲区大小，以及更复杂的 update 策略，以优化性能并降低

**242**

**Chapter 6: Flow Control**

功耗。由于给定解决方案取决于应用程序的特定要求，因此没有为这些策略提供定义。

## **Error Detection Timer — A Pseudo Requirement**

规范为 Flow Control 包定义了一个可选的超时机制，该机制是强烈建议的，并且可能在规范的未来版本中成为要求。对于给定信用类型，FC 包之间的最大延迟为 120μs，并且此超时的最大限制为 200μs。为每个 FC 信用类型（P、NP、Cpl）实现一个单独的计时器，并在收到相应类型的 FC Update DLLP 时重置每个计时器。请注意，与 infinite FC 信用值关联的计时器不得报告错误。

除了 infinite 情况外，超时意味着链路存在严重问题。如果发生这种情况，物理层被发信号以进入 Recovery 状态并重新训练链路，以期清除错误情况。计时器特性包括：

- 仅当链路处于活动状态 (L0 或 L0s) 时才操作。

- 最长时间限制为 200 μs (‐0%/+50%)

- 收到任何 Init 或 Update FCP 时，计时器被重置，或可选地通过收到任何 DLLP 重置。

- 超时强制物理层进入 Link Training and Status State Machine (LTSSM) Recovery 状态。

**243**

**PCI Express Technology**

**244**

_**7**_

## _**Quality of Service**_

## **The Previous Chapter**

上一章讨论了 Flow Control 协议的目的和详细操作。流控旨在确保发送方永远不会发送接收方无法接受的 Transaction Layer Packets (TLPs)。这可以防止接收缓冲区溢出，并消除了 PCI 风格的低效（如 disconnect、retry 和 wait‐state）的需要。

## **This Chapter**

本章讨论支持 Quality of Service 的机制，并描述了控制穿越 fabric 的不同包的时序和带宽的方法。这些机制包括为每个包分配优先级值的应用特定软件，以及必须构建在每个设备中以管理事务优先级的可选硬件。

## **The Next Chapter**

下一章讨论了 PCI Express 拓扑中事务的排序要求。这些规则是从 PCI 继承的。Producer/Consumer 编程模型激励了其中许多规则，因此此处描述了其机制。原始规则还考虑了必须避免的潜在死锁条件。

## **Motivation**

如今的许多计算机系统不包括管理外围流量的带宽的机制，但有些应用程序需要它。一个例子是跨通用数据总线流式传输视频，需要按时交付数据。在嵌入式制导控制系统中，及时交付视频数据对于系统操作也是至关重要的。预见到这些需求，原始的 PCIe 规范包括可以优先考虑某些流量的 Quality of Service (QoS) 机制。这个更广泛的术语是

**245**

**PCI Express Technology**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-3"></a>
## 6.3 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- **Credits Received counter (optional)** — tracks the total credits of all TLPs received into the Flow Control buffer. When flow control is functioning properly, the CREDITS_RECEIVED count should be equal to or less than the CREDIT_ALLOCATED count. If this test ever becomes false, a flow con‐ trol buffer overflow has occurred and an error is detected. The spec recom‐ mends that this optional mechanism be implemented and notes that a failure here will be considered a fatal error. 

_Figure 6‐9: Types and Format of Flow Control DLLPs_ 

**==> picture [374 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataFCHdrFC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>1000  Update Posted<br>1001  Update Non Posted<br>1010  Update Completion<br>**----- End of picture text -----**<br>


**229** 

**PCI Ex ress Technolo p gy** 

## **Flow Control Example** 

The following example describes the non‐posted header Flow Control buffer, and attempts to capture the nuances of the flow control implementation in sev‐ eral situations. The discussion of Flow Control is described with a series of basic stages as follows: 

**Stage One** — Immediately following initialization a transaction is transmitted and tracked to explain the basic operation of the counters and registers. 

**Stage Two** — The transmitter sends transactions faster than the receiver can process them and the buffer becomes full. 

**Stage Three** — When counters roll over to zero, the mechanism still works but there are a couple of issues to consider. 

**Stage Four** — The optional receiver error check for a buffer overflow. 

## **Stage 1 — Flow Control Following Initialization** 

Once flow control initialization has completed, the devices are ready for normal operation. The Flow Control buffer in our example is 2KB in size. We’re describ‐ ing the non‐posted header buffer, and each credit is 5 dwords in size or 20 bytes. That means 102d (66h) Flow Control units are available. Figure 6‐10 on page 231 illustrates the elements involved, including the values that would be in each counter and register following flow control initialization. 

When the transmitter is ready to send a TLP, it must first check Flow Control credits. Our example is simple because a non‐posted header is the only packet being sent and it always requires just one Flow Control credit, and we are also assuming that no data is included in the transaction. 

The header credit check is made using unsigned arithmetic (2’s complement), and must satisfy the following formula: 

**==> picture [193 x 13] intentionally omitted <==**

Substituting values from Figure 6‐10 yields: 

66 _h_ –  00 _h_ + 01 _h_  _mod_ 2[8]  2[8]  2 66 _h_ –01 _h mod_ 256  80 _h_ 

**230** 

**Chapter 6: Flow Control** 

_Figure 6‐10: Flow Control Elements Following Initialization_ 

**==> picture [376 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 00h CL = 66h<br>FC<br>Incr Check<br>Buffer<br>Link Packet optional incr<br>Control<br>incr CrRcv=00h CrAl=66h<br>(NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>CrAl = Credits Allocated<br>CC = Credits Consumed<br>CrRcv = Credits Received<br>CL = Credit Limit<br>PTLP = Pending TLP<br>**----- End of picture text -----**<br>


In this case, the current CREDITS_CONSUMED count (CC) is added to the PTLP credits required, to determine the CREDITS_REQUIRED (CR), and that gives 00h + 01h = 01h. The CREDITS_REQUIRED count is subtracted from the CREDIT_LIMIT count (CL) to determine whether or not sufficient credits are available. 

The following description incorporates a brief review of 2’s complement sub‐ traction. When performing subtraction using 2’s complement the number to be subtracted is complemented (1’s complement) and 1 is added (2’s complement). This value is then added to the number from which we wish to subtract. Any carry due to the addition is dropped. 

**231** 

**PCI Ex ress Technolo p gy** 

Credit Check: 

```
CL 01100110b (66h) - CR 00000001b (01h) = n
```

CR is converted to 2’s complement: 

`00000001b` (CR) `11111110b` (CR inverted) `11111110b +1 11111111b` (2’s complement) 

2’s complement added to CL: 

```
01100110 (CL)
11111111(2’s complement of CR)
01100101 = 65h (carry bit is dropped)
```

Is result <= 80h? Yes. If the subtraction result is equal to or less than half the max value, which is tracked with a modulo 256 counter (128), then we know there is sufficient space in the receiver buffer and this packet can be sent. The decision to use only half the counter value avoids a potential count alias problem. See “Stage 3 — Counters Roll Over” on page 234. 

_Figure 6‐11: Flow Control Elements After First TLP Sent_ 

**==> picture [370 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 01h CL = 66h FC<br>Incr Check Buffer<br>Link Packet optional incr<br>Control (NP Hdr)<br>incr CrRcv=01h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


**232** 

**Chapter 6: Flow Control** 

## **Stage 2 — Flow Control Buffer Fills Up** 

Assume now that the receiver has been unable to remove transactions from the Flow Control buffer for some time. Perhaps the device core logic was tempo‐ rarily busy and unable to process transactions. Eventually, the Flow Control buffer becomes completely full, as shown in Figure 6‐12 on page 234. If the transmitter wishes to send another TLP and checks the Flow Control credits: 

Credit Limit (CL)= 66h Credits Required (CR) = 67h 

## `CL 01100110` (66) 

`CR 10011001` (add 2’s complement of 67h) 

`11111111 = FFh<=80h` (not true; don’t send packet) 

This channel is blocked until an Update Flow Control DLLP is received with a new CREDIT_LIMIT value of 67h or greater. When the new valued is loaded into the CL register the transmitter credit check will pass the test and a TLP can be sent. 

- `CL 01100111` (67) 

- `CR 10011001` add 2’s complement of 67 

   - `00000000 = 00h<=80h` (true, send transaction 

**233** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐12: Flow Control Elements with Flow Control Buffer Filled_ 

**==> picture [376 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>CC = 66h CL = 66h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


## **Stage 3 — Counters Roll Over** 

Since the Credit Limit (CL) and Credits Required (CR) counts only increment upward, they eventually roll over back to zero. When CL rolls over and CR has not, the credit check (CL‐CR) results in a small CL value and a large CR value. However, what might appear to be a problem is not when using unsigned arith‐ metic. As described in the previous examples the results are handled correctly when performing 2’s complement subtraction. Figure 6‐13 on page 235 shows the CL and CR counts before and after CL rollover along with the 2’s comple‐ ment results. 

**234** 

**Chapter 6: Flow Control** 

## _Figure 6‐13: Flow Control Rollover Problem_ 

**==> picture [368 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Before CL Rollover After CL Rollover<br>FFh<br>NTS = FF8h (4088d)CL = F8h AS = FE8h (4072d)CR = F8h<br>Available<br>Credit Available<br>NTS<br>Credit is the<br>AS = FE8h (4072d)CR = E8h Rollover<br>sum of these<br>two parts<br>NTS = FF8h (4088d)CL = 08h<br>00h<br>Using 2's complement: Using 2's complement:<br>  CL 11111000 (F8h)   CL 00001000 (08h)<br>+ CR 00011000 (E8h 2’s complement) + CR 00001000 (F8h 2’s complement)<br>  =  00010000 (0Fh)   =  00010000 (0Fh)<br>**----- End of picture text -----**<br>


## **Stage 4 — FC Buffer Overflow Error Check** 

Although it’s optional to do so, the specification recommends implementation of the FC buffer overflow error checking mechanism. Figure 6‐14 on page 236 shows the elements associated with the overflow error check that include: 

- Credits Received (CR) counter 

- Credits Allocated (CA) counter 

- Error Check Logic 

This permits the receiver to track Flow Control credits in the same manner as the transmitter. If flow control is working correctly, the transmitter’s Credits Consumed count will never exceed its Credit Limit, and the receiver’s Credits Received count will never exceed its Credits Allocated count. 

**235** 

**PCI Ex ress Technolo p gy** 

An overflow condition is detected if the following formula evaluates true. Note that the field size is either 8 (headers) or 12 (data): 

**==> picture [161 x 12] intentionally omitted <==**

If it does evaluate true, then more credits have been sent to the FC buffer than were available and an overflow has occurred. Note that the 1.0a version of the specification defines the equation as  rather than > as shown above. That appears to be an error, because when CA = CR no overflow condition exists. 

_Figure 6‐14: Buffer Overflow Error Check_ 

**==> picture [350 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=67h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


**236** 

**Chapter 6: Flow Control** 

## **Flow Control Updates** 

The receiver must regularly update its neighboring device with Flow Control credits that become available when transactions are removed from the buffer. Figure 6‐15 on page 238 illustrates an example where the transmitter was previ‐ ously blocked from sending header transactions because the buffer was full. In the illustration, the receiver has just removed three headers from the Flow Con‐ trol buffer. More space is now available, but the neighboring device is unaware of this. As headers are removed from the buffer, the CREDITS_ALLOCATED count increments from 66h to 69h. This new count is reported to the CREDIT_LIMIT register of the neighboring device using a Flow Control update packet. Once the credit limit has been updated, transmission of additional TLPs can proceed. 

An interesting note here is that the update reports the actual value of the Cred‐ its Allocated register. It would have worked to report just the change in the reg‐ ister, as perhaps “+3 credits on NP Headers” for example, but that represents a potential problem. To understand the risk, consider what would happen if the DLLP containing that increment information was lost for some reason. There is no replay mechanism for DLLPs; if an error occurs the packet is simply dropped. In this case, the increment information would be lost without a means of recovering it. 

If, on the other hand, the actual value of the register is reported instead and the DLLP fails, the next DLLP that succeeds will get the counters back in synchroni‐ zation. In that case some time might be wasted if the transmitter is waiting on the FC credits before it can send the next TLP, but no information is lost. 

**237** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐15: Flow Control Update Example_

</td>
<td style="background-color:#e8e8e8">

- **Credits Received counter (optional)** — 跟踪接收到 Flow Control 缓冲区的所有 TLP 的总信用数。当流控正常运行时，CREDITS_RECEIVED 计数应等于或小于 CREDIT_ALLOCATED 计数。如果此测试结果为 false，则表示发生了流控缓冲区溢出并检测到错误。规范建议实现此可选机制，并指出此处的失败将被视为致命错误。

*Figure 6‐9: Types and Format of Flow Control DLLPs*

**==> picture [374 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataFCHdrFC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>1000  Update Posted<br>1001  Update Non Posted<br>1010  Update Completion<br>**----- End of picture text -----**<br>


**229**

**PCI Express Technology**

## **Flow Control Example**

以下示例描述了 non‐posted header Flow Control 缓冲区，并试图在多种情况下捕获流控实现的细微差别。Flow Control 的讨论以一系列基本阶段描述如下：

**Stage One** — 初始化后立即发送一个事务并进行跟踪，以解释计数器和寄存器的基本操作。

**Stage Two** — 发送方比接收方处理事务的速度更快，缓冲区变满。

**Stage Three** — 当计数器回绕到零时，机制仍然有效，但有几个问题需要考虑。

**Stage Four** — 缓冲区溢出的可选接收方错误检查。

## **Stage 1 — Flow Control Following Initialization**

一旦流控初始化完成，设备就准备好进行正常操作。在我们的示例中，Flow Control 缓冲区为 2KB。我们正在描述 non‐posted header 缓冲区，每个信用为 5 dwords 或 20 字节。这意味着有 102d (66h) 个 Flow Control 单位可用。第 231 页的图 6‐10 说明了所涉及的元素，包括流控初始化后每个计数器和寄存器中的值。

当发送方准备好发送 TLP 时，它必须首先检查 Flow Control 信用。我们的示例很简单，因为 non‐posted header 是唯一正在发送的包，它始终只需要一个 Flow Control 信用，并且我们还假设事务中不包含数据。

使用无符号算术（2 的补码）进行 header 信用检查，并且必须满足以下公式：

**==> picture [193 x 13] intentionally omitted <==**

将图 6‐10 中的值代入：

66_h – (00_h + 01_h) _mod_ 2[8] ≤ 2[8] / 2  66_h – 01_h mod 256 ≤ 80_h

**230**

**Chapter 6: Flow Control**

*Figure 6‐10: Flow Control Elements Following Initialization*

**==> picture [376 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 00h CL = 66h<br>FC<br>Incr Check<br>Buffer<br>Link Packet optional incr<br>Control<br>incr CrRcv=00h CrAl=66h<br>(NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>CrAl = Credits Allocated<br>CC = Credits Consumed<br>CrRcv = Credits Received<br>CL = Credit Limit<br>PTLP = Pending TLP<br>**----- End of picture text -----**<br>


在这种情况下，将当前 CREDITS_CONSUMED 计数 (CC) 与 PTLP 所需信用相加，以确定 CREDITS_REQUIRED (CR)，即 00h + 01h = 01h。从 CREDIT_LIMIT 计数 (CL) 中减去 CREDITS_REQUIRED 计数以确定是否有足够的信用。

以下描述包含对 2 的补码减法的简要回顾。当使用 2 的补码执行减法时，要减去的数字被取反（1 的补码），然后加 1（2 的补码）。然后将此值添加到我们要从中减去的数字。由于加法而产生的任何进位都将被丢弃。

**231**

**PCI Express Technology**

信用检查：

```
CL 01100110b (66h) - CR 00000001b (01h) = n
```

CR 转换为 2 的补码：

`00000001b` (CR) `11111110b` (CR 取反) `11111110b + 1 11111111b` (2 的补码)

将 2 的补码加到 CL 上：

```
01100110 (CL)
11111111(2 的补码 of CR)
01100101 = 65h (carry bit is dropped)
```

结果是否 <= 80h？是的。如果减法结果等于或小于最大值的一半（用 modulo 256 计数器跟踪为 128），那么我们知道接收方缓冲区中有足够的空间，可以发送此包。仅使用一半的计数器值的决定避免了潜在的计数别名问题。请参见第 234 页 "Stage 3 — Counters Roll Over"。

*Figure 6‐11: Flow Control Elements After First TLP Sent*

**==> picture [370 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 01h CL = 66h FC<br>Incr Check Buffer<br>Link Packet optional incr<br>Control (NP Hdr)<br>incr CrRcv=01h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


**232**

**Chapter 6: Flow Control**

## **Stage 2 — Flow Control Buffer Fills Up**

假设现在接收方已经有一段时间无法从 Flow Control 缓冲区中移除事务。也许设备核心逻辑暂时忙碌，无法处理事务。最终，Flow Control 缓冲区变得完全填满，如第 234 页的图 6‐12 所示。如果发送方希望发送另一个 TLP 并检查 Flow Control 信用：

Credit Limit (CL)= 66h Credits Required (CR) = 67h

## `CL 01100110` (66)

`CR 10011001` (加 67h 的 2 的补码)

`11111111 = FFh <= 80h` (不正确；不发送包)

此通道被阻塞，直到收到具有 67h 或更大的新 CREDIT_LIMIT 值的 Update Flow Control DLLP。当新值被加载到 CL 寄存器中时，发送方信用检查将通过测试，并且可以发送 TLP。

- `CL 01100111` (67)

- `CR 10011001` 加 67 的 2 的补码

   - `00000000 = 00h <= 80h` (true, send transaction

**233**

**PCI Express Technology**

*Figure 6‐12: Flow Control Elements with Flow Control Buffer Filled*

**==> picture [376 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>CC = 66h CL = 66h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


## **Stage 3 — Counters Roll Over**

由于 Credit Limit (CL) 和 Credits Required (CR) 计数仅向上递增，它们最终会回绕到零。当 CL 回绕而 CR 没有回绕时，信用检查 (CL‐CR) 导致 CL 值较小而 CR 值较大。然而，使用无符号算术时看似的问题实际上并不存在。如前所述的示例所示，在执行 2 的补码减法时，结果会被正确处理。第 235 页的图 6‐13 显示了 CL 回绕前后以及 2 的补码结果的 CL 和 CR 计数。

**234**

**Chapter 6: Flow Control**

## *Figure 6‐13: Flow Control Rollover Problem*

**==> picture [368 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Before CL Rollover After CL Rollover<br>FFh<br>NTS = FF8h (4088d)CL = F8h AS = FE8h (4072d)CR = F8h<br>Available<br>Credit Available<br>NTS<br>Credit is the<br>AS = FE8h (4072d)CR = E8h Rollover<br>sum of these<br>two parts<br>NTS = FF8h (4088d)CL = 08h<br>00h<br>Using 2's complement: Using 2's complement:<br>  CL 11111000 (F8h)   CL 00001000 (08h)<br>+ CR 00011000 (E8h 2's complement) + CR 00001000 (F8h 2's complement)<br>  =  00010000 (0Fh)   =  00010000 (0Fh)<br>**----- End of picture text -----**<br>


## **Stage 4 — FC Buffer Overflow Error Check**

虽然可以选择性地执行此操作，但规范建议实现 FC 缓冲区溢出错误检查机制。第 236 页的图 6‐14 显示了与溢出错误检查相关联的元素，包括：

- Credits Received (CR) counter

- Credits Allocated (CA) counter

- Error Check Logic

这允许接收方以与发送方相同的方式跟踪 Flow Control 信用。如果流控工作正常，发送方的 Credits Consumed 计数永远不会超过其 Credit Limit，接收方的 Credits Received 计数永远不会超过其 Credits Allocated 计数。

**235**

**PCI Express Technology**

如果以下公式评估为 true，则检测到溢出情况。请注意，字段大小为 8（headers）或 12（data）：

**==> picture [161 x 12] intentionally omitted <==**

如果它确实评估为 true，则表示发送到 FC 缓冲区的信用超过了可用信用，因此发生了溢出。请注意，规范的 1.0a 版本将等式定义为 ≥ 而不是如上所示的 >。这似乎是一个错误，因为当 CA = CR 时不存在溢出情况。

*Figure 6‐14: Buffer Overflow Error Check*

**==> picture [350 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=67h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


**236**

**Chapter 6: Flow Control**

## **Flow Control Updates**

接收方必须定期使用在从事务中移除缓冲区时可用的 Flow Control 信用来更新其相邻设备。第 238 页的图 6‐15 说明了一个示例，其中发送方先前因为缓冲区已满而无法发送 header 事务。在图示中，接收方刚刚从 Flow Control 缓冲区中移除了三个 headers。现在有更多空间可用，但相邻设备不知道这一点。随着 headers 从缓冲区中移除，CREDITS_ALLOCATED 计数从 66h 增加到 69h。该新计数使用 Flow Control update 包报告给相邻设备的 CREDIT_LIMIT 寄存器。一旦更新了信用限制，就可以继续传输其他 TLP。

这里一个有趣的注意点是，update 报告了 Credits Allocated 寄存器的实际值。仅报告寄存器的变化也可以工作，例如"+3 credits on NP Headers"，但这代表了一个潜在问题。要了解此风险，请考虑如果包含增量信息的 DLLP 因某种原因丢失会发生什么情况。没有 DLLPs 的重传机制；如果发生错误，包将被简单丢弃。在这种情况下，增量信息将丢失而无法恢复。

另一方面，如果报告了寄存器的实际值并且 DLLP 失败，则下一个成功的 DLLP 将使计数器重新同步。在这种情况下，如果发送方正在等待 FC 信用才能发送下一个 TLP，则可能会浪费一些时间，但不会丢失任何信息。

**237**

**PCI Express Technology**

*Figure 6‐15: Flow Control Update Example*

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-4"></a>
## 6.4 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**==> picture [368 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=69h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


## **FC_Update DLLP Format and Content** 

Recall that Flow Control update packets, like the Flow Control initialization packets, contain two credit fields, one for header and one for data, as shown in Figure 6‐16 on page 239. The receiver’s credit values reported in the HdrFC and DataFC fields may have been updated many times or not at all since the last update packet was sent. 

**238** 

**Chapter 6: Flow Control** 

_Figure 6‐16: Update Flow Control Packet Format and Contents_ 

## **Flow Control Update Frequency** 

The specification defines a variety of rules and suggested implementations that govern when and how often Flow Control Update DLLPs should be sent. These are motivated by a desire to: 

- Notify the transmitting device as early as possible about new credits allo‐ cated, especially if any transactions were previously blocked. 

- Establish worst‐case latency between FC Packets. 

- Balance the requirements associated with flow control operation, such as: — the need to report credits often enough to prevent transaction blocking 

- — the desire to reduce the Link bandwidth needed for FC_Update DLLPs 

- — selecting the optimum buffer size 

   - selecting the maximum data payload size 

- Detect violations of the maximum latency between Flow Control packets. 

Flow Control updates are permitted only when the Link is in the active state (L0 or L0s). All other Link states represent more aggressive power management that have longer recovery latencies. 

## **Immediate Notification of Credits Allocated** 

When a Flow Control buffer is so full that maximum‐sized packets cannot be sent, the spec requires immediate delivery of a FC_Update DLLP when more space becomes available. Two cases exist: 

**239** 

## **PCI Ex ress Technolo p gy** 

- **Maximum Packet Size = 1 Credit.** When packet transmission is blocked due to a buffer full condition for non‐infinite NPH, NPD, PH, and CPLH buffer types, an UpdateFC packet must be scheduled for Transmission when one or more credits are made available (allocated) for that buffer type. 

- **Maximum Packet Size = Max_Payload_Size.** Flow Control buffer space may decrease to the extent that a maximum‐sized packet cannot be sent for non‐infinite PD and CPLD credit types. In this case, when one or more additional credits are allocated, an Update FCP must be scheduled for transmission. 

## **Maximum Latency Between Update Flow Control DLLPs** 

The transmission frequency of Update FCPs for each FC credit type (non‐infi‐ nite) must be scheduled for transmission at least once every 30 μs (‐0%/+50%). If the Extended Sync bit within the Control Link register is set, updates must be scheduled no later than every 120 μs (‐0%/+50%). Note that Update FCPs may be scheduled for transmission more frequently than is required. 

## **Calculating Update Frequency Based on Payload Size and Link Width** 

The specification offers a formula for calculating the frequency at which update packets need to be sent for maximum data payload sizes and Link widths. The formula, shown below, defines FC Update delivery intervals in symbol times. For reference, a symbol time is defined as the time it takes to deliver one sym‐ bol: 4ns for Gen1, 2ns for Gen2, 1ns for Gen3. Table 6‐3, Table 6‐4 and Table 6‐5 show the unadjusted FC Update values for each speed. 

--------------------------------------------------------------------------------------------------------------------------------------- _MaxPayloadSize_ + _TLPOverhead_   _UpdateFactor_ **-** + _InternalDelay LinkWidth_ • **MaxPayloadSize** = The value in the Max_Payload_Size field of the Device Control register 

- **TLPOverhead** = the constant value (28 symbols) representing the additional TLP components that consume Link bandwidth (TLP Prefix, Sequence Number, Packet Header, LCRC, Framing Symbols) 

- **UpdateFactor** = the number of maximum size TLPs sent during the interval between UpdateFC Packets received. This number is intended to balance Link bandwidth efficiency and receive buffer sizes – the value varies with Max_Payload_Size and Link width 

**240** 

**Chapter 6: Flow Control** 

- **LinkWidth** = The number of Lanes the Link is using 

- **InternalDelay** = a constant value of 19 symbol times that represents the internal processing delays for received TLPs and transmitted DLLPs 

The relationship defined by the formula shows that the frequency of update packet delivery decreases as the Linkwidth increases and suggests a timer that triggers scheduling of update packets. Note that this formula does not account for delays associated with the receiver or transmitter being in the L0s power management state. 

_Table 6‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|237<br>UF=1.4|128<br>UF=1.4|73<br>UF=1.4|67<br>UF=2.5|58<br>UF=3.0|48<br>UF=3.0|33<br>UF=3.0|
|256 Bytes|416<br>FC=1.4|217<br>FC=1.4|118<br>UF=1.4|107<br>UF=2.5|90<br>UF=3.0|72<br>UF=3.0|45<br>UF=3.0|
|512 Bytes|559<br>UF=1.0|289<br>UF=1.0|154<br>UF=1.0|86<br>UF=1.0|109<br>UF=2.0|86<br>UF=2.0|52<br>UF=2.0|
|1024 Bytes|1071<br>UF=1.0|545<br>UF=1.0|282<br>UF=1.0|150<br>UF=1.0|194<br>UF=2.0|150<br>UF=2.0|84<br>UF=2.0|
|2048 Bytes|2095<br>UF=1.0|1057<br>UF=1.0|538<br>UF=1.0|278<br>UF=1.0|365<br>UF=2.0|278<br>UF=2.0|148<br>UF=2.0|
|4096 Bytes|4143<br>UF=1.0|2081<br>UF=1.0|1050<br>UF=1.0|534<br>UF=1.0|706<br>UF=2.0|534<br>UF=2.0|276<br>UF=2.0|



_Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|288<br>UF=1.4|179<br>UF=1.4|124<br>UF=1.4|118<br>UF=2.5|109<br>UF=3.0|99<br>UF=3.0|84<br>UF=3.0|
|256 Bytes|467<br>FC=1.4|268<br>FC=1.4|169<br>UF=1.4|158<br>UF=2.5|141<br>UF=3.0|123<br>UF=3.0|96<br>UF=3.0|



**241** 

## **PCI Ex ress Technolo p gy** 

_Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|512 Bytes|610<br>UF=1.0|340<br>UF=1.0|205<br>UF=1.0|137<br>UF=1.0|160<br>UF=2.0|137<br>UF=2.0|103<br>UF=2.0|
|1024 Bytes|1122<br>UF=1.0|596<br>UF=1.0|333<br>UF=1.0|201<br>UF=1.0|245<br>UF=2.0|201<br>UF=2.0|135<br>UF=2.0|
|2048 Bytes|2146<br>UF=1.0|1108<br>UF=1.0|589<br>UF=1.0|329<br>UF=1.0|416<br>UF=2.0|329<br>UF=2.0|199<br>UF=2.0|
|4096 Bytes|4194<br>UF=1.0|2132<br>UF=1.0|1101<br>UF=1.0|585<br>UF=1.0|757<br>UF=2.0|585<br>UF=2.0|327<br>UF=2.0|



_Table 6‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|333<br>UF=1.4|224<br>UF=1.4|169<br>UF=1.4|163<br>UF=2.5|154<br>UF=3.0|144<br>UF=3.0|129<br>UF=3.0|
|256 Bytes|512<br>FC=1.4|313<br>FC=1.4|214<br>UF=1.4|203<br>UF=2.5|186<br>UF=3.0|168<br>UF=3.0|141<br>UF=3.0|
|512 Bytes|655<br>UF=1.0|385<br>UF=1.0|250<br>UF=1.0|182<br>UF=1.0|205<br>UF=2.0|182<br>UF=2.0|148<br>UF=2.0|
|1024 Bytes|1167<br>UF=1.0|641<br>UF=1.0|378<br>UF=1.0|246<br>UF=1.0|290<br>UF=2.0|246<br>UF=2.0|180<br>UF=2.0|
|2048 Bytes|2191<br>UF=1.0|1153<br>UF=1.0|643<br>UF=1.0|374<br>UF=1.0|461<br>UF=2.0|374<br>UF=2.0|244<br>UF=2.0|
|4096 Bytes|4239<br>UF=1.0|2177<br>UF=1.0|1146<br>UF=1.0|630<br>UF=1.0|802<br>UF=2.0|630<br>UF=2.0|372<br>UF=2.0|



The specification recognizes that the formula will be inadequate for many appli‐ cations such as those that stream large blocks of data. These applications may require buffer sizes larger than the minimum specified, as well as a more sophisticated update policy in order to optimize performance and reduce 

**242** 

**Chapter 6: Flow Control** 

power consumption. Because a given solution is dependent on the particular requirements of an application, no definition for such policies is provided. 

## **Error Detection Timer — A Pseudo Requirement** 

The specification defines an optional time‐out mechanism for Flow Control packets that is highly recommended and may become a requirement in future versions of the specification. The maximum latency between FC packets for a given credit type is 120μs, and this timeout has a maximum limit of 200μs. A separate timer is implemented for each FC credit type (P, NP, Cpl), and each timer is reset when a FC Update DLLP of the corresponding type is received. Note that a timer associated with infinite FC credit values must not report an error. 

Apart from the infinite case, a timeout implies a serious problem with the Link. If it occurs, the Physical Layer is signaled to go into the Recovery state and retrain the Link in hopes of clearing the error condition. Timer characteristics include: 

- Operates only when the Link is in an active state (L0 or L0s). 

- Max time limited to 200 μs (‐0%/+50%) 

- Timer is reset when any Init or Update FCP is received, or optionally by receipt of any DLLP. 

- Timeout forces the Physical Layer to enter Link Training and Status State Machine (LTSSM) Recovery state. 

**243** 

**PCI Ex ress Technolo p gy** 

**244** 

_**7**_ 

## _**Quality of Service**_ 

## **The Previous Chapter** 

The previous chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Transaction Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like disconnects, retries, and wait‐states. 

## **This Chapter** 

This chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different pack‐ ets traversing the fabric. These mechanisms include application‐specific soft‐ ware that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **The Next Chapter** 

The next chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock condi‐ tions that must be avoided. 

## **Motivation** 

Many computer systems today don’t include mechanisms to manage band‐ width for peripheral traffic, but there are some applications that need it. One example is streaming video across a general‐purpose data bus, that requires data be delivered at the right time. In embedded guidance control systems timely delivery of video data is also critical to system operation. Foreseeing those needs, the original PCIe spec included Quality of Service (QoS) mecha‐ nisms that can give preference to some traffic flows. The broader term for this is 

**245** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

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

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---



<img src="figures/embedded/page0241_img1_tight.png" alt="Figure from page 241" width="700">

<a id="sec-6-5"></a>
## 6.5 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Differentiated Service, since packets are treated differently based on an assigned priority and it allows for a wide range of service preferences. At the high end of that range, QoS can provide predictable and guaranteed perfor‐ mance for applications that need it. That level of support is called “isochro‐ nous” service, a term derived from the two Greek words “isos” (equal) and “chronos” (time) that together mean something that occurs at equal time inter‐ vals. To make that work in PCIe requires both hardware and software elements. 

## **Basic Elements** 

Supporting high levels of service places requirements on system performance. For example, the transmission rate must be high enough to deliver sufficient data within a time frame that meets the demands of the application while accommodating competition from other traffic flows. In addition, the latency must be low enough to ensure timely arrival of packets and avoid delay prob‐ lems. Finally, error handling must be managed so that it doesn’t interfere with timely packet delivery. Achieving these goals requires some specific hardware elements, one of which is a set of configuration registers called the Virtual Channel Capability Block as shown in Figure 7‐1. 

_Figure 7‐1: Virtual Channel Capability Registers_ 

**==> picture [368 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
0d<br>63d CapPtr Header<br>PCI Compatible<br>PCIeCapabilityBlock Space<br>PCIe Enhanced Capability Register<br>Port VC Cap Register 1 Ext VC Cnt 255d<br>VATOffset PortVCCapRegister2 VirtualChannel<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VCResourceCap(0) CapabilityStructure<br>VCResourceControlReg(0)<br>VCResourceStatus(0) Reserved PCIe Extended<br>PATnOffset VCResourceCap(n) CapabilitySpace<br>VCResourceControlReg(n)<br>VCResourceStatus(n) Reserved<br>VCArbitrationTable(VAT)<br>PortArbitrationTable0(PAT0) 4095d<br>PortArbitrationTablen(PATn)<br>**----- End of picture text -----**<br>


**246** 

**Chapter 7: Quality of Service** 

## **Traffic Class (TC)** 

The first thing we need is a way to differentiate traffic; something to distinguish which packets have high priority. This is accomplished by designating Traffic Classes (TCs) that define eight priorities specified by a 3‐bit TC field within each TLP header (with ascending priority; TC 0‐7). The 32‐bit memory request header in Figure 7‐2 reveals the location of the TC field. During initialization, the device driver communicates the level of services to the isochronous man‐ agement software, which returns the appropriate TC values to use for each type of packet. The driver then assigns the correct TC priority for the packet. The TC value defaults to zero so packets that don’t need priority service won’t acciden‐ tally interfere with those that do. 

_Figure 7‐2: Traffic Class Field in TLP Header_ 

**==> picture [372 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R R Attr AT Length<br>tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


Configuration software that’s unaware of PCIe won’t recognize the new regis‐ ters and will use the default TC0/VC0 combination for all transactions. In addi‐ tion, there are some packets that are always required to use TC0/VC0, including Configuration, I/O, and Message transactions. If these packets are thought of as maintenance‐level traffic, then it makes sense that they would need to be con‐ fined to VC0 and kept out of the path of high‐priority packets. 

## **Virtual Channels (VCs)** 

VCs are hardware buffers that act as queues for outgoing packets. Each port must include the default VC0, but may have as many as eight (from VC0 to VC7). Each channel represents a different path available for outgoing packets. 

**247** 

**PCI Ex ress Technolo p gy** 

The motivation for multiple paths is analogous to that of a toll road in which drivers purchase a radio tag that lets them take one of several high priority lanes at the toll booth. Those who don’t purchase a tag can still use the road but they’ll have to stop at the booth and pay cash each time they go through, and that takes longer. If there was only one path, everyone’s access time would be limited by the slowest driver, but having multiple paths available means that those who have priority are not delayed by those who don’t. 

## **Assigning TCs to each VC — TC/VC Mapping** 

The Traffic Class value assigned to each packet travels unchanged to the desti‐ nation and must be mapped to a VC at each service point as it traverses the path to the target. VC mapping is specific to a Link and can change from one Link to another. Configuration software establishes this association during initializa‐ tion using the _TC/VC Map_ field of the VC Resource Control Register. This 8‐bit field permits TC values to be mapped to a selected VC, where each bit position represents the corresponding TC value (bit 0 = TC0, bit 1 = TC1, etc.). Setting a bit assigns the corresponding TC value to the VC ID. Figure 7‐3 on page 249 shows a mapping example where TC0 and TC1 are mapped to VC0 and TC2:TC4 are mapped to VC3. 

Software has a great deal of flexibility in assigning VC IDs and mapping the TCs, but there are some rules regarding the TC/VC mapping: 

- TC/VC mapping must be identical for the two ports attached on either end of the same Link. 

- TC0 will automatically be mapped to VC0. 

- Other TCs may be mapped to any VC. 

- • A TC may **not** be mapped to more than one VC. 

The number of virtual channels used depends on the greatest capability shared by the two devices attached to a given link. Software assigns an ID for each VC and maps one or more TCs to the VCs. 

**248** 

**Chapter 7: Quality of Service** 

_Figure 7‐3: TC to VC Mapping Example_ 

**==> picture [348 x 407] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16 15                                      0<br>PCI Express Extended Capability Header<br>Port VC Capability Register 1<br>Port VC Capability Register 2<br>Port VC Status Register Port VC Control Register<br>PAT Offset VC0 Resource Capability Register<br>VC0 Resource Control Register<br>VC0 Resource Status Reg Reserved<br>PAT Offset VC3 Resource Capability Register<br>VC3 Resource Control Register<br>VC3 Resource Status Reg Reserved<br>31              26 24            19 17 16 15  8 7                     0<br>C0 VCID TC/VC Map<br>2      0 7                         0<br>0 0 0 0 0 0 0 0 0 1 1<br>31              26 24            19 17 16 15  8 7                     0<br>VC3 VCID TC/VC Map<br>2      0 7                         0<br>0 1 1 0 0 0 1 1 1 0 0<br>**----- End of picture text -----**<br>


## **Determining the Number of VCs to be Used** 

Software checks the number of VCs supported by the devices attached to a com‐ mon link and would usually assign the greatest number of VCs that both devices can support. Consider the example topology in Figure 7‐4 on page 250. 

**249** 

## **PCI Ex ress Technolo p gy** 

Here, the switch supports all 8 VCs on each of its ports, while Device A sup‐ ports only the default VC0, Device B supports 4 VC s, and Device C support 8 VCs. Note that even though switch port A supports all 8 VCs, Device A only supports VC0, so 7 VCs are left unused in switch port A. Similarly, only 4 VCs are used by switch port B. 

_Figure 7‐4: Multiple VCs Supported by a Device_ 

**==> picture [369 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>8 VCs supported<br>on each switch port<br>Switch<br>1 VC A C<br>B<br>8 VCs<br>4 VCs<br>Device<br>1 VC supported 8 VCs supported<br>B<br>4 VCs supported<br>A<br>Device<br>C<br>Device<br>**----- End of picture text -----**<br>


Configuration software determines the maximum number of VCs supported by each port interface by reading the _Extended VC Count_ field in the Virtual Chan‐ nel Capability registers, as shown in Figure 7‐5 on page 251. Software checks the Extended VC Count at both ends of the Link and selects the highest common count. Using all the available VCs is not mandatory, though. Software may choose to enable fewer VCs as well. 

**250** 

**Chapter 7: Quality of Service** 

_Figure 7‐5: Extended VCs Supported Field_ 

**==> picture [297 x 304] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header<br>Port VC Capability Register 1<br>Port VC Capability Register 2<br>Port VC Status Register  Port VC Control Register<br>PAT Offset VC0 Resource Capability Register<br>VC0 Resource Control Register<br>VC0 Resource Status Reg  Reserved<br>PAT Offset VCn Resource Capability Register<br>VCn Resource Control Register<br>VCn Resource Status Reg  Reserved<br>2                             0<br>Extended VC Count<br>0 = only VC0 supported<br>1-7 = number of additional<br>         VCs supported<br>**----- End of picture text -----**<br>


## **Assigning VC Numbers (IDs)** 

Configuration software assigns a number (ID) to each of the VCs, except VC0 which is always hardwired. As shown in Figure 7‐3 on page 249, the VC Capa‐ bilities registers include 12 bytes of configuration registers for each VC. The first set of registers always applies to VC0. The _Extended VC Count_ field defines the number of additional VCs implemented by this port, each of which will have a set of registers. The value “n” represents the number of additional VCs imple‐ mented. For example, if the _Extended VC Count_ contains a value of 3, then there are three VCs and register sets in addition to VC0. 

**251** 

**PCI Ex ress Technolo p gy** 

Software assigns a number for each of the additional VCs via the _VC ID_ field. (See Figure 7‐3 on page 249) The IDs don’t have to be contiguous but each num‐ ber can only be used once. 

## **VC Arbitration** 

## **General** 

If a device has more than one VC and they all have a packet ready to send, VC arbitration determines the order of packet transmission. Any of several schemes can be chosen by software from among the options implemented by hardware. The goals are to implement the desired service policy and ensure that all trans‐ actions are making forward progress to prevent inadvertent time‐outs. In addi‐ tion, VC Arbitration is affected by the requirements associated with flow control and transaction ordering. These topics are discussed in other chapters, but they affect arbitration, too, because: 

- Each supported VC provides its own buffers and flow control. 

- Transactions mapped to the same VC are normally passed along in strict order (although there are exceptions, such as when a packet has the “Relaxed Ordering” attribute bit set). 

- Transaction ordering only applies within a VC, so there’s no ordering rela‐ tionship among packets assigned to different VCs. 

The example in Figure 7‐6 on page 253 illustrates two VCs (VC0 and VC1) with a transmission priority based on a 3:1 ratio, meaning three VC1 packets are sent for every one VC0 packet. The device core sends requests (including a TC value) to the TC/VC Mapping logic. Based on the programmed mapping, the packet is placed into the appropriate VC buffer for transmission. Finally, the VC arbiter determines the VC priority for forwarding the packets. This example illustrates the flow in one direction, but the same logic exists for transmitting in the oppo‐ site direction at the same time. 

The VC capability registers provide three basic VC arbitration approaches: 

1. Strict Priority Arbitration — the highest numbered VC with a packet ready always wins.

</td>
<td style="background-color:#e8e8e8">

Isochronous timing 在 PCIe 中由 Time‐Based Weighted Round Robin 端口仲裁方案中使用的时隙定义。目前，每个时隙的时间为 100ns，并表示 TBWRR 表中 128 个条目之一的一个条目。设置后，仲裁器将每 12.8μs 重复循环此表一次，这表示整个 Service Interval。

使 isochronous path 按预期工作需要一些考虑。首先，必须以可预测的时序在规则的时间间隔传递数据包。其次，必须提前知道要传递的最大 isochronous 数据量，并且不允许包超过该限制。第三，链路带宽必须足以支持在给定时间片中传递的数据量。

**274**

**Chapter 7: Quality of Service**

考虑以下示例。以 2.5 Gbps 运行的单 Lane 链路每 4ns 传递一个 symbol。这允许它在 100ns 时隙内发送 25 个 symbol，但这是否足以使用？在许多情况下不是，因为 TLP 可能需要 28 字节的开销用于 header、sequence number、LCRC 等的组合。这意味着在 100ns 内甚至没有时间完成发送开销，更不用说任何数据负载了。如果我们需要发送 128 字节的数据，则带宽要求为 128+overhead = 156 字节。解决此问题的一种选择是将链路宽度增加到 8 个 Lanes，从而允许一次发送八倍的字节数。此更改将在 100ns 内传递 200 字节，并允许单个时隙传递所有 isochronous 数据。另一种解决方案是使用单 Lane 但为端口提供更多时隙，因为在较低链路宽度下 8 个时隙将传递相同数量的数据。解决方案的选择取决于成本和性能约束，但系统设计人员必须知道 isochronous path 的时序和带宽要求，才能正确设置它。

## **How Timing is Enforced**

当 timing 是设计正常操作不可或缺的一部分时（如上例所示），它是通过我们到目前为止讨论的内容的组合来强制执行的。首先，必须在软件中选择高优先级 TC，并在硬件中设置 VC，定义它们之间的映射，以便只有正确的包才会被放入高优先级 VC。然后，所需的时序是编程仲裁方案以在指定的时间内容纳所需带宽的问题。例如，VC 仲裁的选择可能是 Strict Priority 选项，因为它是唯一可以确保高优先级包不会被其他包延迟的选择。对于 Port 仲裁，选择必须是 TBWRR 以强制执行时序。

## **Software Support**

支持 isochronous 服务需要系统中软件元素之间的一些协调。在 PC 系统中，设备驱动程序将向 OS 报告 isochronous 要求和功能，然后 OS 将评估整个系统需求并适当地分配资源。嵌入式系统会有所不同，因为所有部件从一开始就是已知的，并且软件可以更简单。在下面的讨论中，我们将描述 PC 的情况，因为嵌入式系统应该是该情况的一个更简单的子集。

**275**

**PCI Express Technology**

## **Device Drivers**

设备驱动程序必须能够将其时序要求报告给监督 isochronous 操作的软件，并在尝试使用 isochronous 包之前获得许可。重要的是要注意，驱动程序级软件不应自行直接更改硬件分配或仲裁策略，即使它可以，因为结果将是混乱的。如果多个驱动程序各自独立地尝试执行此操作，则最后一个进行更改的驱动程序将覆盖以前的任何分配。为避免这种情况，称为 Isochronous Broker 的 OS 级程序接收来自系统设备的时序请求，并以适应它们所有的方式协调地分配系统资源。

## **Isochronous Broker**

该程序管理 isochronous 包的端到端流。它从设备驱动程序接收 isochronous 时序请求，并以一种通过目标路径适应请求的方式分配系统资源。在规范中，这被称为在 requester/completer 对和 PCIe fabric 之间建立 isochronous contract。这样做需要验证预期路径确实可以支持 isochronous 流量，然后对适当的仲裁方案进行编程以确保它在指定的时序要求内工作。

## **Bringing it all together**

到目前为止，应该相当清楚支持系统中的 isochronous 流量需要做什么，但让我们看一个最后的示例将所有部分放在一起。如果我们扩展前面的视频捕获示例以显示更复杂的系统（如图 7‐24（第 277 页）所示），我们将能够讨论如果视频摄像头能够将捕获的数据传送到系统内存中，所有必须就位的部分。这将是一个对 isochronous 服务来说困难的环境，因为路径中可以有这么多设备竞争带宽，但这也使得说明必须考虑的各种事情变得有用。

## **Endpoints**

从底部开始，视频端点设备本身的 PCIe 接口需要什么？在硬件中，如果我们要区分包，则需要多个 VC。为简单起见，我们假设单 function 设备。设备驱动程序将需要向 OS 级 Isochronous broker 报告设备功能和 isochronous 时序要求，后者将评估系统然后报告 isochronous contract 是否可行以及软件应使用哪些 TC。

**276**

**Chapter 7: Quality of Service**

*Figure 7‐24: Example Isochronous System*

**==> picture [308 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>

Processor<br>GFX Root Complex<br>System<br>Memory<br>Switch 2<br>Switch 1<br>Slot<br>Video SCSI<br>Camera<br>Lower<br>Time-<br>priority<br>sensitive<br>data<br>data<br>**----- End of picture text -----**<br>


然后，驱动程序将对 VC 编号进行编程并将适当的 TC 映射到每个 VC。它还很可能将 VC 仲裁编程为 Strict Priority 用于高优先级通道。这里的一个警告是仲裁仍然必须"公平"，这意味着低优先级通道不会因为访问而被饿死。这意味着高优先级 VC 不能持续有流量挂起，而必须在一段时间内分散包注入。

在我们完成关于端点的讨论之前，还需要对链路操作进行另一个观察，那就是关于流控。只要包根据 Isochronous Contract 均匀地注入，isochronous path 中设备的接收缓冲区必须足够大以处理预期的包流而不会引起任何背压。此外，必须足够快地返回 Flow Control Updates 以避免停顿。

**277**

**PCI Express Technology**

## **Switches**

接下来，考虑在端点和根复合体之间的每个交换机中需要存在什么。交换机通常没有设备驱动程序，因此将由 OS 级软件（如 Isochronous Broker）来读取它们的配置信息并确定它们支持的服务。首先，isochronous path 中的所有端口必须支持多个 VC，并且 TC/VC 映射必须在每个链路的两端匹配。请记住，一旦包进入交换机端口的 Transaction Layer，只有 TC 与包保持在一起，并且该 TC 的 VC 分配特定于每个端口。Switch 1 的下游端口的 TC/VC 映射必须与端点的映射匹配，但其他交换机端口的映射可能不同以匹配其链路的另一端。

**Arbitration Issues.** 仲裁的选择是直接的。在我们的示例中，isochronous path 显示为仅在一个方向上传输流量以简化。在存储器读的情况下，可能存在双向流动的 isochronous 流量，但我们的示例被选择为类似于视频流式传输的情况。

isochronous egress port 的 VC 仲裁很可能需要出于与端点相同的原因而使用 Strict Priority 方案。端口仲裁将需要使用 Time‐Based WRR 方案，这意味着软件必须理解适当的访问比率并对 Port Arbitration Tables 进行编程以实现它们。如果路径中有多个交换机，则这可能不像听起来那么简单，因为即使它们都将使用相同的 TBWRR 仲裁方案，但尚不清楚如何协调它们中每一个的 service intervals。如果 SI 未对齐，则意味着时序保证可能更困难，具体取决于链路的繁忙程度。规范中没有考虑协调 service intervals，因此它将再次涉及非标准方法。显然，如果我们在 isochronous path 中没有多个交换机，这个问题会简单得多。

**Timing Issues.** 图 7‐25（第 279 页）显示了我们的示例中两个端点传递的包的时序。来自视频设备的包具有已知的大小并以规则和可预测的间隔传递，显示为较粗的箭头。较小和较浅的箭头表示来自 SCSI 驱动器的包，这些包优先级较低且其时序不可预测。在端点中，包只需要为其分配适当的 TC，但交换机需要确保强制执行适当的 timing policy。这是通过使用 TBWRR 来完成的，它指定在给定时间哪个端口将具有访问权限以及持续多长时间。知道 isochronous 包的大小和频率

**278**

**Chapter 7: Quality of Service**

允许软件正确地安排时序，但需要什么样的时序？

*Figure 7‐25: Injection of Isochronous Packets*

**==> picture [269 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>

SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


首先，让我们通过考虑一个简单的示例来回顾涉及的参数。回想一下，PCIe 基于参考时钟周期的时间槽由 Port Capability Register 1 字段 Reference Clock 给出。目前该字段的唯一选项是 100ns，并且 TBWRR 表除了 128 个条目之外没有其他选项。Service Interval 的长度是这些的倍数，使其为 12.8μs。给定设备的带宽可以由下面的等式表示，其中 Y 是在一个时隙中传递的数据（规范规定必须将在配置期间编程的 Max Payload Size 用于此带宽计算），M 是时隙数，T 是整个 Service Interval。如果我们选择 128 字节作为有效负载，并且我们知道 SI 是 12.8μs，则对于分配的每个时隙 BW = 10 MB/s。

**==> picture [79 x 28] intentionally omitted <==**

现在让我们考虑一个更现实的示例。假设我们的链路以 Gen2 速度运行，视频设备需要具有 100MB/s 的保证带宽，并且它将发送 512 字节的包。填充等式显示需要 2.5 个 512 字节的实例。但实际可以在一个时隙中发送多少数据？答案当然取决于速度和链路宽度。在 5.0 Gb/s 时，发送每个 10 位 symbol 需要 2ns，因此每 100ns 每 Lane 可以传递 50 个 symbol。如果包大小为 512 字节的数据加上另外 28 字节左右的 header，则需要 11 个时隙来使用 x1 链路传递一个包的 550 个 symbol。如果需要，可以为一个端口分配多个连续的

**279**

**PCI Express Technology**

slots，因此这是一种解决方案。由于将发送的包大小始终相同，我们真的无法编程 2.5 个实例，因此我们必须使用 3 个实例。从我们的等式来看，3 个 512 字节的实例产生的实际带宽为 120MB/s。这高于我们需要，但解决了问题。使用的时隙数将为 11 x 3 = 33，在 Service Interval 中留下 95 个供其他使用。每组 11 个时隙需要是连续的，但这些组可以在 Service Interval 上间隔开。

另一种解决方案是增加链路宽度。虽然硬件成本会更高，但使用 11 个 Lanes 将允许在一个时隙内传递所有数据。CEM 规范目前不支持 x11 选项，但 x12 选项可用，并且适用于我们的示例。使用这样的宽链路意味着软件只需要为每个包编程一个时隙，并且在整个 Service Interval 中只需要三个来支持此设备的 isochronous 流量。与 x1 的情况不同，现在我们不需要连续的时隙。相反，它们可以以某种最佳方式在 Service Interval 上间隔开。

**Bandwidth Allocation Problems.** TBWRR 表必须编程以保证 isochronous 流量的足够及时带宽，并且不允许其他流量进行干扰。在第 279 页的图 7‐25 中，SCSI 控制器显示在 SI 1 中发送一个包，在 SI 3 中发送另一个包。如果时序是这样的，即每个 SI 允许该端点一个包，那么这就正常工作。

现在假设 SCSI 控制器尝试在 SI 1 中注入比它被允许的更多的包，如图 7‐26（第 280 页）所示。这是规范中提到的两个带宽分配问题中的第一个，称为"oversubscription"。这可能会干扰 isochronous 流量流，但编程 TBWRR 表可以轻松避免此问题，因为仲裁仅允许在该端口的特定时间从该端口传入一个包。如果来自该端口的更多包排队，它们只需等待下一个可用时间，这可能在此示例中所示的 SI 2 中。最终，这可能导致发送代理的流控背压

*Figure 7‐26: Over‐Subscribing the Bandwidth*

**==> picture [263 x 94] intentionally omitted <==**

**----- Start of picture text -----**<br>

SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**280**

**Chapter 7: Quality of Service**

第二个时序问题称为"congestion"（拥塞），发生在给定时间窗口内发送了太多 isochronous 请求时，如图 7‐27（第 281 页）所示。这是一个类似的问题，但现在没有简单的解决方案。与前一种情况不同，将高优先级包推迟到另一个时隙不是一种选择，因此系统必须努力处理它们全部。结果是某些请求可能会经历过多的服务延迟。为了纠正此问题，软件需要更改包的分布，以便它们可以由可用的硬件带宽支持。

*Figure 7‐27: Bandwidth Congestion*

**==> picture [263 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>

SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**Latency Issues.** 管理包传递的延迟是 isochrony 的重要组成部分，并且涉及 fabric 延迟和 Completer 延迟的组合。Fabric 延迟取决于系统中各个组件之间链路的所有特征，尤其是链路宽度和工作频率。最小化此值的一种简单方法是约束 isochronous paths 的 PCIe 拓扑的复杂性。Completer 延迟取决于目标端点的内部特征，例如内存速度和内部仲裁。

## **Root Complex**

RC 具有与交换机相同的仲裁和时序要求。它在多个下游端口上接收包，并以与之前描述的 isochrony 规则一致的方式将它们转发到目标。但是，其大部分完成方式将是供应商特定的，因为规范未定义 RC 或应如何对其进行编程。

**Problem: Snooping.** 我们尚未讨论的一个影响根中时序和延迟的有趣事情是 snooping 过程。通常，每当对系统内存进行访问时，它都将是一个位置，处理器认为该位置是可缓存的，这意味着它有权在其本地缓存中存储一个临时的

**281**

**PCI Express Technology**

副本。如果外部设备尝试访问该内存区域，则芯片组必须先检查处理器缓存，然后才允许访问，因为缓存的副本可能已被修改。如果是这样，则修改的数据将需要写回内存，然后才能用于设备访问。尽管有必要确保内存一致性，但问题在于 snooping 需要时间。所需的时间通常是有限的但不可预测的，因为它取决于 CPU 当时正在执行的其他操作。根据时序要求，这种不确定性可能会破坏 isochronous 数据流。

**Snooping Solutions.** 避免 snooping 的一种方法是让设备仅访问已指定为不可缓存的内存区域。另一种选择是软件在高优先级包头中设置 "No Snoop" 属性位。这会强制芯片组跳过 snoop 步骤而不管内存类型如何，并直接访问内存，因为软件已保证这样做不会引起问题。为了将此强制为 isochronous path 的要求，根端口中的高优先级 VC 可以由硬件初始化另一个位，称为 "Reject Snoop Transactions"（参见第 265 页图 7‐17 中的 VC Resource Capability Register）。其目的是仅允许具有 No Snoop 属性集的该 VC 的事务。任何传入未设置 No Snoop 属性的包都将被丢弃，以确保时序永远不会被等待 snoop 所破坏。

## **Power Management**

这是一个简单的观察，但如果时序对 PCIe 中的路径很重要，则该路径中设备的电源管理 (PM) 机制将需要仔细处理。配置软件可以读取与每个 PM 条件关联的延迟，并选择时序预算将允许的那些情况。不过，最简单的方法是禁用 isochronous path 中的所有 PM 选项。幸运的是，这可以使用现有的配置寄存器轻松完成。可以将设备置于设备状态 D0 并将其保留在那里，同时可以禁用硬件控制的链路 PM 机制（有关 PM 的更多信息，请参见第 16 章 "Power Management"，位于第 703 页）。

## **Error Handling**

最后，还有最后一个问题：当链路上发生错误时该怎么办。第 7 章中介绍的 ACK/NAK 协议提供了一种自动的、基于硬件的重试机制来纠正遇到传输问题的包。这种可取的特性给 isochrony 带来了一个问题，因为它需要时间。而解决错误所需的时间可能会有很大差异，这取决于问题是如何被检测到的。

**282**

**Chapter 7: Quality of Service**

为了决定这个问题，我们必须知道系统可以容忍多少时间不确定性，并且仍然可以提供 isochronous 数据。如果延迟预算太紧，那么根本不会有时间重试失败的包，并且必须禁用 ACK/NAK 协议。有趣的是，规范编写者显然没有考虑这种可能性，因为没有包括用于禁用它的配置位或决定如何处理将被重试但现在不会被重试的包。因此，禁用此操作将需要像供应商特定寄存器这样的非标准机制。

如果 _没有_ 足够的时间用于重试，则目标代理可以选择简单地丢弃任何错误的包。另一种选择是按原样使用错误的包，错误和所有这些。对于使用 isochronous 支持的某些应用程序而言，这并不像听起来那么违反直觉。例如，视频流中的错误可能会导致显示上偶尔出现故障，但可以认为这是可以接受的风险。

如果 Service Interval 中 _有_ 足够的时间允许重试，则可以通过添加计时器来跟踪距 Service Interval 结束的时间并使用它来决定是否可以尝试重试来限制它们可能增加的可能延迟。当然，错误不应经常发生，因此这可能足以纠正偶尔的传输错误，同时仍保持 isochronous 时序。

**283**

**PCI Express Technology**

**284**

## _**8**_

## _**Transaction Ordering**_

## **The Previous Chapter**

上一章讨论了支持 Quality of Service 的机制，并描述了控制穿越 fabric 的不同包的时序和带宽的方法。这些机制包括为每个包分配优先级值的应用特定软件，以及必须构建在每个设备中以管理事务优先级的可选硬件。

## **This Chapter**

本章讨论了 PCI Express 拓扑中事务的排序要求。这些规则是从 PCI 继承的。Producer/Consumer 编程模型激励了其中许多规则，因此此处描述了其机制。原始规则还考虑了必须避免的潜在死锁条件。

## **The Next Chapter**

下一章描述了 Data Link Layer Packets (DLLPs)。我们描述了 DLLP 包类型的使用、格式和定义以及其相关字段的详细信息。DLLPs 用于支持 Ack/Nak 协议、电源管理、流控机制，并且可以用于供应商定义的目的。

## **Introduction**

与其他协议一样，PCI Express 对同时通过 fabric 的相同 traffic class (TC) 的事务施加排序规则。具有不同 TC 的事务没有排序关系。这些针对相同 TC 的事务的排序规则的原因包括：

- 保持与遗留总线 (PCI、PCI‐X 和 AGP) 的兼容性。

- • 确保事务的完成是确定性的，并且按程序员预期的顺序进行。

**285**

**PCI Express 3.0 Technology**

- 避免死锁条件。

- 通过最小化读延迟和管理读写排序来最大化性能和吞吐量。

特定 PCI/PCIe 事务排序的实现基于以下特性：

1. Producer/Consumer 编程模型是基本排序规则的基础。

2. Relaxed Ordering 选项允许在 Requester 知道事务不依赖于先前事务时进行例外。

3. ID Ordering 选项允许交换机允许来自一个设备的请求超过来自另一个设备的请求，因为这两个设备正在执行不相关的执行线程。

4. 避免死锁条件和支持 PCI 遗留实现的手段。

## **Definitions**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---



<img src="figures/embedded/page0244_img1_tight.png" alt="Figure from page 244" width="700">

<a id="sec-6-6"></a>
## 6.6 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

2. Group Arbitration — VCs are divided by hardware into one low‐priority group and one high‐priority group. The low‐priority group uses an arbitra‐ tion method selected by software from the available choices, while the high‐ priority group always uses strict‐priority arbitration. 

3. Hardware Fixed arbitration — scheme built into the hardware. 

**252** 

**Chapter 7: Quality of Service** 

_Figure 7‐6: VC Arbitration Example_ 

**==> picture [246 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>VC1 VC0<br>Root Complex<br>Memory<br>TC/VC Mapping<br>VC arbitration in this<br>example yields a 3 to 1<br>ratio for transmitting<br>VC1 and VC0.<br>Arbiter<br>VC1 VC0<br>TC/VC Mapping<br>Device<br>Core<br>**----- End of picture text -----**<br>


## **Strict Priority VC Arbitration** 

The default priority scheme is based on the inherent priority of VC IDs (VC0=lowest priority and VC7=highest priority). The mechanism is automatic and requires no configuration. Figure 7‐7 on page 254 illustrates a strict priority arbitration example that includes all VCs. The VC ID governs the order in which transactions are sent. The maximum number of VCs that use strict prior‐ ity arbitration cannot be greater than the value in the _Extended VC Count_ field. 

**253** 

**PCI Ex ress Technolo p gy** 

(See Figure 7‐5 on page 251.) Furthermore, if the designer has chosen strict pri‐ ority arbitration for all VCs supported, the _Low Priority Extended VC Count_ field of Port VC Capability Register 1 is hardwired to zero. (See Figure 7‐8 on page 255. 

_Figure 7‐7: Strict Priority Arbitration_ 

|VC Resources|Priority Order|Priority Order|
|---|---|---|
|8th VC|VC7|Highest|
|7th VC|VC6||
|6th VC|VC5||
|5th VC|VC4||
|4th VC|VC3||
|3rd VC|VC2||
|2nd VC|VC1||
|1st VC|VC0|Lowest|
||||



Strict priority requires that higher‐numbered VCs always get precedence over lower‐priority VCs. For example, if all eight VCs are governed by strict priority, then packets in VC0 can only be sent when no other VCs have packets pending. This achieves the goal of giving the highest priority packets very high band‐ width with minimal latencies. However, strict priority has the potential to starve low‐priority channels for bandwidth, so care must be taken to ensure this doesn’t happen. The spec requires that high priority traffic be regulated to avoid starvation, and gives two possible methods of regulation: 

- The originating port can restrict the injection rate of high priority packets to allow more bandwidth for lower priority transactions. 

- Switches can regulate multiple traffic flows at the egress port. This method may limit the throughput from high bandwidth applications and devices that attempt to exceed the limitations of the available bandwidth. 

A device designer may also limit the number of VCs that participate in strict priority by splitting the VCs into a low‐priority group and a high‐priority group as discussed in the next section. 

**254** 

**Chapter 7: Quality of Service** 

## **Group Arbitration** 

Figure 7‐8 illustrates the _Low Priority Extended VC Count_ field within VC Capa‐ bility Register 1. This read‐only field specifies a VC ID that identifies the upper limit of the low‐priority arbitration group for this device. For example, if this value is 4, then VC0‐VC4 are members of the low‐priority group and VC5‐VC7 are in the high‐priority group. Note that a _Low Priority Extended VC Count_ of 7 means that no strict priority is used. 

_Figure 7‐8: Low‐Priority Extended VCs_ 

**==> picture [333 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header 00h<br>Port VC Capability Register 1  04h<br>Port VC Capability Register 2  08h<br>Port VC Status Register  Port VC Control Register  0Ch<br>PAT Offset VC0 Resource Capability Register  10h<br>VC0 Resource Control Register  14h<br>VC0 Resource Status Reg  Reserved 18h<br>PAT Offset VCn Resource Capability Register  10h+(n*0Ch)<br>VCn Resource Control Register  14h+(n*0Ch)<br>VCn Resource Status Reg  Reserved 18h+(n*0Ch)<br>n = one of the extended VCs<br>31          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP<br>Port Arbitration Table Entry Size<br>Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>**----- End of picture text -----**<br>


**255** 

**PCI Ex ress Technolo p gy** 

As depicted in Figure 7‐10 on page 257, the high‐priority VCs continue to use strict priority arbitration, while the low‐priority arbitration group uses one of the other arbitration methods supported by the device. VC Capability Register 2 reports which alternate methods are supported for this group, as shown in Fig‐ ure 7‐9, and the VC Control Register permits selection of the method to be used. The low‐priority arbitration schemes include: 

- Hardware Based Fixed Arbitration 

- Weighted Round Robin Arbitration (WRR) 

_Figure 7‐9: VC Arbitration Capabilities_ 

**==> picture [304 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                     24  23                            8 7                        0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>7                       4   3     2     1     0<br>RsvdP<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>**----- End of picture text -----**<br>


**==> picture [193 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Control Register<br>15                                 4  3     1 0<br>RsvdP<br>VC Arbitration Select (000b-111b)<br>Load VC Arbitration Table<br>**----- End of picture text -----**<br>


**256** 

**Chapter 7: Quality of Service** 

_Figure 7‐10: VC Arbitration Priorities_ 

|VC Resources|VC IDs|||Split Priority||
|---|---|---|---|---|---|
|||||Highest||
|8th VC|VC7|||||
|7th VC|VC6||High-Priority (Strict Priority Scheme)|||
|5th VC<br>6th VC|VC5<br>VC4|||Low-Priority VC ID = 4||
|4th VC|VC3|||||
|3rd VC|VC2||Low-Priority (Alternate Priority Scheme)<br>(Selected by Software)|||
|||||||
|2nd VC|VC1|||||
|1st VC|VC0|||Lowest||



## **Hardware Fixed Arbitration Scheme** 

This selection defines a hardware‐based method and requires no additional software setup. This method can be anything the hardware designer chooses to build in, and could be based on anticipated loading or band‐ width needs for the device. A simple example might be an ordinary round robin sequence, in which each VC gets an equal turn at sending packets during the rotation. 

## **Weighted Round Robin Arbitration Scheme** 

This is a scheme in which some VCs can be weighted more (given higher priority) than others by giving them more entries in the sequence than oth‐ ers. The spec defines three WRR options, each with a different number of entries (called phases). The table size is selected by writing the correspond‐ ing value in to the _VC Arbitration Select_ field of the Port VC Control Register (see Figure 7‐9 on page 256). Each entry in the table represents one phase that software loads with a low priority VC number. The VC arbiter will repeatedly scan all table entries in a sequential fashion and send packets from the VC specified in the table entries. Once a packet has been sent, the 

**257** 

**PCI Ex ress Technolo p gy** 

arbiter immediately proceeds to the next phase. Figure 7‐11 on page 258 shows an example of a WRR arbitration table with 64 entries. 

_Figure 7‐11: WRR VC Arbitration Table_ 

**==> picture [165 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Phase VC ID<br>0 VC 4<br>1 VC 3<br>2 255 (16KB)VC 2<br>3 VC 1<br>4 VC 4<br>5 VC 3<br>6 VC 0<br>7 64 (4KB)VC 4<br>8 VC 3<br>9 128 (8KB)VC 2<br>10 VC 1<br>1111 VC 4<br>621 VC 3<br>632 VC 0<br>Arbitration Logic Scans Table Entries<br>**----- End of picture text -----**<br>


## **Setting up the Virtual Channel Arbitration Table** 

The location of the VC Arbitration Table (VAT) in configuration space is given as an offset from the base address of the VC Capability Structure, as shown in Figure 7‐12 on page 259. 

As shown in Figure 7‐13 on page 260, each entry in the VAT is a 4‐bit field that identifies the VC number of the buffer that is scheduled to deliver data during that phase. The table length is selected by the arbitration option shown in Figure 7‐9 on page 256. 

**258** 

**Chapter 7: Quality of Service** 

_Figure 7‐12: VC Arbitration Table Offset and Load VC Arbitration Table Fields_ 

**==> picture [331 x 385] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Capability Register 2<br>31                     24  23                                             8 7                      0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>0d<br>Header<br>CapPtr<br>63d<br>PCICompatible<br>PCIe Cap Structure (CapID=10h) Space<br>255d<br>PCIEXEnhancedCapabilityRegister<br>PortVCCapRegister1 ExtVCCnt<br>VATOffset PortVCCapRegister2<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VC0 Resource Cap Reg<br>VC Resource Control Register PCIEXExtended<br>VC Resource Status Reg Reserved CapabilitySpace<br>PATnOffset VCn Resource Cap Reg<br>VC Resource Control Register<br>VC Resource Status Reg Reserved<br>VC Arbitration Table (VAT)<br>4095d<br>**----- End of picture text -----**<br>


The table is loaded by configuration software to achieve the desired priority order for the virtual channels. Hardware sets the _VC Arbitration Table Status_ bit whenever any changes are made to the table, giving software a way to verify whether changes have been made but not yet applied to the hard‐ ware. Once the table is loaded, software sets the _Load VC Arbitration Table_ bit 

**259** 

## **PCI Ex ress Technolo p gy** 

in the Port VC Control register. That causes hardware to load, or apply, the new values to the VC Arbiter. Hardware clears the _VC Arbitration Table Sta‐ tus_ bit when table loading is complete, signaling to software that loading has finished. This method is probably motivated by the desire to change the table contents during run time without disruption. The problem is that con‐ figuration writes are only able to update a dword at a time and are rela‐ tively slow transactions, which means it could take a long time to finish making changes, during which the table is only partially updated. That, in turn, could result in unexpected behavior by the device as it continues to operate during this time. To avoid that, this mechanism allows software to complete all the changes to the table and then apply them all at once to the hardware arbiter. 

_Figure 7‐13: Loading the VC Arbitration Table Entries_ 

|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|31       28 27      24 23      20 19<br>16 15       12 11|8||7|4|3|||0||||
|Phase[2]<br>Phase[3]<br>Phase[4]<br>Phase[5]<br>Phase[6]<br>Phase[7]|||Phase[1]||Phase[0]||||||00h|
|Phase[10]<br>Phase[11]<br>Phase[12]<br>Phase[13]<br>Phase[14]<br>Phase[15]|||Phase[9]||Phase[8]||||||04h|
|Phase[18]<br>Phase[19]<br>Phase[20]<br>Phase[21]<br>Phase[22]<br>Phase[23]|||Phase[17]||Phase[16]||||||08h|
|Phase[26]<br>Phase[27]<br>Phase[28]<br>Phase[29]<br>Phase[30]<br>Phase[31]|||Phase[25]||Phase[24]|||||0Ch||
|<br>1. Configuration Software loads the VC Arbitration Table.<br>2. The VC Arbitration Table Status bit is set when any|3||2|1||0||||||
|table  entry is updated.|RsvdP|||VC ID||||||||
|3. Software sets the Load VC Arbitration Table bit.||||||||||||
|4. Hardware applies table contents to VC Arbiter.||||||||||||
|5. Hardware clears the VC Arbitration Table status bit||||||||||||

</td>
<td style="background-color:#e8e8e8">

2. 组仲裁 (Group Arbitration) — VC 由硬件划分为一个低优先级组和一个高优先级组。低优先级组使用由软件从可用选项中选择的仲裁方法,而高优先级组则始终使用严格优先级仲裁 (Strict Priority)。

3. 硬件固定仲裁 (Hardware Fixed arbitration) — 内置于硬件中的方案。

**252**

**第 7 章:服务质量 (Quality of Service)**

_Figure 7‐6: VC 仲裁示例_

**==> picture [246 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>VC1 VC0<br>根复合体 (Root Complex)<br>内存<br>TC/VC 映射<br>本例中的 VC 仲裁<br>产生 3:1 的比例<br>用于传输 VC1 和 VC0<br>仲裁器 (Arbiter)<br>VC1 VC0<br>TC/VC 映射<br>设备<br>核心<br>**----- End of picture text -----**<br>


## **严格优先级 VC 仲裁 (Strict Priority VC Arbitration)**

默认的优先级方案基于 VC ID 的固有优先级 (VC0=最低优先级,VC7=最高优先级)。该机制是自动的,无需配置。图 7-7 (第 254 页) 展示了一个包含所有 VC 的严格优先级仲裁示例。VC ID 决定了事务发送的顺序。使用严格优先级仲裁的最大 VC 数量不能大于 _Extended VC Count_ 字段的值。

**253**

**PCI Ex ress Technolo p gy**

(参见第 251 页的图 7-5。)此外,如果设计者已对所有受支持的 VC 选择了严格优先级仲裁,则 Port VC Capability Register 1 的 _Low Priority Extended VC Count_ 字段被硬连线为零。(参见第 255 页的图 7-8。)

_Figure 7‐7: 严格优先级仲裁_

|VC 资源|优先级顺序|优先级顺序|
|---|---|---|
|第 8 个 VC|VC7|最高|
|第 7 个 VC|VC6||
|第 6 个 VC|VC5||
|第 5 个 VC|VC4||
|第 4 个 VC|VC3||
|第 3 个 VC|VC2||
|第 2 个 VC|VC1||
|第 1 个 VC|VC0|最低|
||||



严格优先级要求高编号的 VC 始终优先于低优先级 VC。例如,如果所有八个 VC 都由严格优先级管理,则只有当没有其他 VC 有待发数据包时,VC0 中的数据包才能被发送。这实现了以最小延迟为最高优先级数据包提供非常高带宽的目标。然而,严格优先级有可能使低优先级通道的带宽出现饥饿,因此必须谨慎处理以确保这种情况不会发生。规范要求调节高优先级流量以避免饥饿,并给出了两种可能的调节方法:

- 发起端口可以限制高优先级数据包的注入速率,以便为低优先级事务提供更多带宽。

- 交换机可以在出口端口调节多个流量流。该方法可能会限制来自高带宽应用和试图超出可用带宽限制的设备的吞吐量。

设备设计者还可以通过将 VC 拆分为低优先级组和高优先级组来限制参与严格优先级的 VC 数量,具体将在下一节中讨论。

**254**

**第 7 章:服务质量**

## **组仲裁 (Group Arbitration)**

图 7-8 展示了 VC Capability Register 1 中的 _Low Priority Extended VC Count_ 字段。该只读字段指定一个 VC ID,用于标识本设备低优先级仲裁组的上限。例如,如果该值为 4,则 VC0-VC4 是低优先级组的成员,VC5-VC7 属于高优先级组。注意 _Low Priority Extended VC Count_ 为 7 表示不使用严格优先级。

_Figure 7‐8: 低优先级扩展 VC_

**==> picture [333 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header 00h<br>Port VC Capability Register 1  04h<br>Port VC Capability Register 2  08h<br>Port VC Status Register  Port VC Control Register  0Ch<br>PAT Offset VC0 Resource Capability Register  10h<br>VC0 Resource Control Register  14h<br>VC0 Resource Status Reg  Reserved 18h<br>PAT Offset VCn Resource Capability Register  10h+(n*0Ch)<br>VCn Resource Control Register  14h+(n*0Ch)<br>VCn Resource Status Reg  Reserved 18h+(n*0Ch)<br>n = one of the extended VCs<br>31          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP<br>Port Arbitration Table Entry Size<br>Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>**----- End of picture text -----**<br>


**255**

**PCI Ex ress Technolo p gy**

如图 7-10 (第 257 页) 所示,高优先级 VC 继续使用严格优先级仲裁,而低优先级仲裁组使用该设备支持的其他仲裁方法之一。VC Capability Register 2 报告了该组支持哪些替代方法,如图 7-9 所示,VC Control Register 允许选择要使用的方法。低优先级仲裁方案包括:

- 基于硬件的固定仲裁 (Hardware Based Fixed Arbitration)

- 加权轮询仲裁 (Weighted Round Robin Arbitration, WRR)

_Figure 7‐9: VC 仲裁能力_

**==> picture [304 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                     24  23                            8 7                        0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>7                       4   3     2     1     0<br>RsvdP<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>**----- End of picture text -----**<br>


**==> picture [193 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Control Register<br>15                                 4  3     1 0<br>RsvdP<br>VC Arbitration Select (000b-111b)<br>Load VC Arbitration Table<br>**----- End of picture text -----**<br>


**256**

**第 7 章:服务质量**

_Figure 7‐10: VC 仲裁优先级_

|VC 资源|VC ID|||分割优先级||
|---|---|---|---|---|---|
|||||最高||
|第 8 个 VC|VC7|||||
|第 7 个 VC|VC6||高优先级(严格优先级方案)|||
|第 5 个 VC<br>第 6 个 VC|VC5<br>VC4|||低优先级 VC ID = 4||
|第 4 个 VC|VC3|||||
|第 3 个 VC|VC2||低优先级(替代优先级方案)<br>(由软件选择)|||
|第 2 个 VC|VC1|||||
|第 1 个 VC|VC0|||最低||


## **硬件固定仲裁方案 (Hardware Fixed Arbitration Scheme)**

此选择定义了一种基于硬件的方法,无需额外的软件设置。该方法可以是硬件设计者选择构建的任何方案,可以基于设备的预期负载或带宽需求。一个简单的例子可能是普通的轮询序列,其中每个 VC 在轮转过程中有平等的发送数据包机会。

## **加权轮询仲裁方案 (Weighted Round Robin Arbitration Scheme)**

在此方案中,某些 VC 可以被赋予比其他的更高的权重(给予更高的优先级),方法是在序列中给予它们比其他 VC 更多的条目。规范定义了三种 WRR 选项,每种具有不同数量的条目(称为阶段 phase)。表大小通过在 Port VC Control Register 的 _VC Arbitration Select_ 字段中写入相应的值来选择(参见第 256 页的图 7-9)。表中的每个条目表示一个阶段,软件用低优先级 VC 编号加载该阶段。VC 仲裁器将以顺序方式反复扫描所有表条目,并从表条目中指定的 VC 发送数据包。一旦数据包被发送,仲裁器立即继续到下一阶段。

**257**

**PCI Ex ress Technolo p gy**

图 7-11 (第 258 页) 展示了具有 64 个条目的 WRR 仲裁表示例。

_Figure 7‐11: WRR VC 仲裁表_

**==> picture [165 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Phase VC ID<br>0 VC 4<br>1 VC 3<br>2 255 (16KB)VC 2<br>3 VC 1<br>4 VC 4<br>5 VC 3<br>6 VC 0<br>7 64 (4KB)VC 4<br>8 VC 3<br>9 128 (8KB)VC 2<br>10 VC 1<br>1111 VC 4<br>621 VC 3<br>632 VC 0<br>Arbitration Logic Scans Table Entries<br>**----- End of picture text -----**<br>


## **设置虚拟通道仲裁表 (Setting up the Virtual Channel Arbitration Table)**

VC 仲裁表 (VAT) 在配置空间中的位置以 VC Capability Structure 的基地址作为偏移给出,如图 7-12 (第 259 页) 所示。

如图 7-13 (第 260 页) 所示,VAT 中的每个条目都是一个 4 位字段,标识在该阶段被调度传送数据的缓冲区的 VC 编号。表长度由图 7-9 (第 256 页) 所示的仲裁选项选择。

**258**

**第 7 章:服务质量**

_Figure 7‐12: VC 仲裁表偏移和加载 VC 仲裁表字段_

**==> picture [331 x 385] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Capability Register 2<br>31                     24  23                                             8 7                      0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>0d<br>Header<br>CapPtr<br>63d<br>PCICompatible<br>PCIe Cap Structure (CapID=10h) Space<br>255d<br>PCIEXEnhancedCapabilityRegister<br>PortVCCapRegister1 ExtVCCnt<br>VATOffset PortVCCapRegister2<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VC0 Resource Cap Reg<br>VC Resource Control Register PCIEXExtended<br>VC Resource Status Reg Reserved CapabilitySpace<br>PATnOffset VCn Resource Cap Reg<br>VC Resource Control Register<br>VC Resource Status Reg Reserved<br>VC Arbitration Table (VAT)<br>4095d<br>**----- End of picture text -----**<br>


表由配置软件加载,以实现虚拟通道所需的优先级顺序。每当对表进行任何更改时,硬件都会设置 _VC Arbitration Table Status_ 位,为软件提供一种方法来验证是否已进行更改但尚未应用于硬件。表加载完成后,软件设置 _Load VC Arbitration Table_ 位

**259**

## **PCI Ex ress Technolo p gy**

在 Port VC Control 寄存器中。这会导致硬件将新值加载(或应用)到 VC 仲裁器。表加载完成时,硬件清除 _VC Arbitration Table Status_ 位,向软件发出加载完成的信号。这种方法的动机可能是希望在运行时更改表内容而不会造成中断。问题在于配置写入一次只能更新一个 dword,并且是相对较慢的事务,这意味着完成更改可能需要很长时间,在此期间表仅部分更新。这反过来又可能导致设备在操作过程中出现意外行为。为避免这种情况,此机制允许软件完成对表的所有更改,然后一次性将所有更改应用到硬件仲裁器。

_Figure 7‐13: 加载 VC 仲裁表条目_

|32 阶段虚拟通道仲裁表|32 阶段虚拟通道仲裁表|32 阶段虚拟通道仲裁表|32 阶段虚拟通道仲裁表|||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|31       28 27      24 23      20 19<br>16 15       12 11|8||7|4|3|||0||||
|Phase[2]<br>Phase[3]<br>Phase[4]<br>Phase[5]<br>Phase[6]<br>Phase[7]|||Phase[1]||Phase[0]||||||00h|
|Phase[10]<br>Phase[11]<br>Phase[12]<br>Phase[13]<br>Phase[14]<br>Phase[15]|||Phase[9]||Phase[8]||||||04h|
|Phase[18]<br>Phase[19]<br>Phase[20]<br>Phase[21]<br>Phase[22]<br>Phase[23]|||Phase[17]||Phase[16]||||||08h|
|Phase[26]<br>Phase[27]<br>Phase[28]<br>Phase[29]<br>Phase[30]<br>Phase[31]|||Phase[25]||Phase[24]|||||0Ch||
|<br>1. 配置软件加载 VC 仲裁表。<br>2. 当任何|3||2|1||0||||||
|表条目被更新时设置 VC 仲裁表状态位。|RsvdP|||VC ID||||||||
|3. 软件设置 Load VC Arbitration Table 位。||||||||||||
|4. 硬件将表内容应用于 VC 仲裁器。||||||||||||
|5. 硬件清除 VC 仲裁表状态位。||||||||||||

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-7"></a>
## 6.7 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

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

Switch ports and root ports will often receive incoming packets that need to be routed to another port. Since packets arriving from multiple ports can all target the same VC in the same outgoing port, arbitration is needed to decide which incoming port’s packet gets next access to that VC. Like VC arbitration, port arbitration has several optional schemes available for selection by configuration software. The combination of TCs, VCs, and arbitration support a range of ser‐ vice levels that fall into two broad categories: 

**1. Asynchronous** — Packets get “best effort” service and may receive no prefer‐ ence at all. Many devices and applications, like mass storage devices, have no stringent requirements for bandwidth or latency and don’t need special timing mechanisms. On the other hand, packets generated by more demanding appli‐ cations can still be prioritized without much trouble by establishing a hierarchy of traffic classes for different packets. Differentiated service is still considered to be asynchronous until the level of service requires guarantees. Naturally, asyn‐ chronous service is always available and doesn’t need any special software or hardware options. 

**2. Isochronous** — When latency and bandwidth guarantees are needed, we move into the isochronous category. This would be useful when a synchronous connection would normally be required between two devices. For example, a CD‐ROM sourcing data from a music CD uses a synchronous connection when a headset is plugged directly into the drive. However, when the audio must be routed across a general‐purpose bus like PCIe to get to external speakers, the connection cannot be synchronous because other traffic may also need to use the same data stream. To achieve an equivalent result, isochronous service must guarantee proper delivery of the time‐sensitive audio data without preventing other traffic from using the Link during the same time. Not surprisingly, spe‐ cialized software and hardware are needed to support this. 

The concept of port arbitration is pictured in Figure 7‐14 on page 262. Note that port arbitration exists in several places in a system: 

- Egress ports of switches 

- Root Complex ports when peer‐to‐peer transactions are supported 

- Root Complex egress ports that lead to targets such as main memory 

**261** 

## **PCI Ex ress Technolo p gy** 

Port arbitration will usually need software configuration for each virtual chan‐ nel supported by a switch or root egress port. In the example below, root port 2 supports peer‐to‐peer transfers from root ports 1 and 2 and therefore needs port arbitration. It should be noted, though, that peer‐to‐peer support between root ports is optional, so it may be that not every root egress port would need port arbitration. 

The connection to system memory is an interesting path. There will likely be packets from multiple ingress ports trying to access this port at the same time, so it needs to support port arbitration. However, it doesn’t use a PCIe port, so it doesn’t have the set of PCIe registers to support arbitration that we’re describ‐ ing here. Instead, the root will need to supply a vendor‐specific set of registers called a Root Complex Register Block (RCRB) to provide the same functionality. 

Because port arbitration is managed independently for each VC of the egress port, a separate table is required for each VC that supports programmable port arbitration, as shown in Figure 7‐15 on page 263. Port arbitration tables are sup‐ ported only by switches and root ports and are not allowed in endpoints. 

_Figure 7‐14: Port Arbitration Concept_ 

**==> picture [368 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Port Arbitration<br>(configured via RCRB)<br>Root Complex<br>Memory<br>1 2 3<br>VC0<br>Port Arbitration<br>Switch<br>(configured via PPB)<br>VC0 VC0<br>VC0 VC0<br>Endpoint Endpoint Endpoint Endpoint<br>A B C D<br>**----- End of picture text -----**<br>


**262** 

**Chapter 7: Quality of Service** 

_Figure 7‐15: Port Arbitration Tables for Each VC_ 

**==> picture [320 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>PAT0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>PATn Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Port Arbitration Table 0 (PAT0)<br>Port Arbitration Table n (PATn)<br>**----- End of picture text -----**<br>


Although it isn’t stated in the spec, the process of arbitrating between different packet streams also implies the use of additional buffers to accumulate traffic from each port in the egress port as illustrated in Figure 7‐16 on page 264. This example illustrates two ingress ports (1 and 2) whose transactions are routed to an egress port (3). The actions taken by the switch include the following: 

1. Packets arriving at the ingress ports are directed to the appropriate flow control buffers (VC) based on the TC/VC mapping. 

2. Packets are forwarded from the flow control buffers to the routing logic, which determines and routes them to the proper egress port. 

3. Packets routed to the egress port (3) use TC/VC mapping to determine into which VC buffer they should be placed. 

4. A set of buffers is associated with each of the ingress ports, allowing the ingress port number to be tracked until port arbitration can be done. 

5. Port arbitration logic determines the order in which transactions are sent from each group of ingress buffers. 

**263** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐16: Port Arbitration Buffering_ 

**==> picture [356 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Ingress Ports Egress Port<br>Port Arbiter<br>Port 2<br>Port 1<br>TC0:TC3 1 VC0 VC0<br>Port 2 VC0 VC Arbiter<br>Port 3 VC0<br>3<br>Port 1<br>VC0<br>TC0:TC1 2 Port 1<br>TC2:TC4 VC7<br>VC5<br>Port 3 Port 2 VC7<br>VC7<br>Port Arbiter<br>TC/VC Mapping Routing Logic<br>TC/VC Mapping<br>TC/VC Mapping Routing Logic<br>**----- End of picture text -----**<br>


## **Port Arbitration Mechanisms** 

The actual port arbitration mechanisms defined are similar to the models used for VC arbitration. Configuration software determines the capability for a port by reading the registers shown in Figure 7‐17 on page 265 and selects the port arbitration scheme to use for each VC. 

**264** 

**Chapter 7: Quality of Service** 

_Figure 7‐17: Software Selects Port Arbitration Scheme_ 

**==> picture [276 x 325] intentionally omitted <==**

**----- Start of picture text -----**<br>
VCn Resource Capability Register<br>31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>7      6    5    4   3     2     1     0<br>Rsvd<br>WRR with 256 Phases (101b)<br>Time-based WRR with 128 Phases (100b)<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>VCn Resource Control Register<br>31              26 24            19 17 16 15  8 7                     0<br>VC<br>RsvdP ID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


## **Hardware-Fixed Arbitration** 

This mechanism doesn’t require software setup. Once selected, it’s managed solely by hardware. The actual arbitration scheme is chosen by the hard‐ ware designer, possibly based on the expected demands for the device. This may simply ensure fairness or it may optimize some aspect of the design, but it doesn’t support differentiated or isochronous services. 

## **Weighted Round Robin Arbitration** 

Just like the weighted round robin mechanism in VC arbitration, software can set up the port arbitration table so that some ports receive more oppor‐ 

**265** 

**PCI Ex ress Technolo p gy** 

tunities than others. This approach assigns different weights to traffic com‐ ing from different ports. 

As the table is scanned, each phase specifies the port number from which the next packet is received. Once the packet is delivered, the arbitration logic immediately proceeds to the next phase. If no transaction is pending transmission for the selected port, the arbiter advances immediately to the next phase. There is no time value associated with these entries. 

Four table lengths are given for WRR port arbitration, determined by the number of phases used by the table. Presumably, a larger number of entries in the table allows for more interesting ratios of arbitration selection. On the other hand, a smaller number of entries would use less storage and cost less. 

## **Time-Based, Weighted Round Robin Arbitration (TBWRR)** 

This mechanism is required for isochronous support. As the name implies, time‐based weighted round robin adds the element of time to each arbitra‐ tion phase. Just as in WRR the port arbiter delivers one transaction from the ingress port VC buffer indicated by the Port Number of the current phase. Now though, rather than immediately advancing to the next phase, the time‐based arbiter waits until the current virtual timeslot elapses before advancing. This ensures that transactions are accepted from the ingress port buffer at regular intervals. If the selected port does not have a packet ready to send then nothing will be sent until the next timeslot. Note that the timeslot does not govern the duration of the transfer, but rather the interval between transfers. The maximum duration of a transaction is the time it takes to complete the round robin and return to the original timeslot. The length of the timeslot may change in the future, but currently has the value of 100ns. 

Time‐based WRR arbitration supports a maximum table length of 128 phases, but the actual number of table entries available for a given VC may be less than that. The value is hardware initialized and reported in the _Max‐ imum Time Slots_ field of each virtual channel that supports TBWRR, as shown in Figure 7‐18 on page 267. 

**266** 

**Chapter 7: Quality of Service** 

_Figure 7‐18: Maximum Time Slots Register_ 

**==> picture [331 x 95] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                 24 23 22            16 15 14 13            8 7                     0<br>Port Arbitration Maximum Time Port Arbitration<br>RsvdP<br>Table Offset Slots Capability<br>RsvdP<br>Reject Snoop Transactions<br>Undefined<br>**----- End of picture text -----**<br>


## **Loading the Port Arbitration Tables** 

The actual size and format of the Port Arbitration Tables are a function of the number of phases and the number of ingress ports supported by the Switch, RCRB, or Root Port that supports peer‐to‐peer transfers. The maximum number of ingress ports supported by the Port Arbitration Table is 256 ports. The actual number of bits within each table entry is design dependent and governed by the number of ingress ports whose transactions can be delivered to the egress port. The size of each table entry is reported in the 2‐bit _Port Arbitration Table Entry Size_ field of Port VC Capability Register 1. The permissible values are: 

- 00b — 1 bit (selects between 2 ports) 

- 01b — 2 bits (4 ports)

</td>
<td style="background-color:#e8e8e8">

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

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-8"></a>
## 6.8 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- 10b — 4 bits (16 ports) 

- 11b — 8 bits (256 ports) 

Configuration software loads each table with port numbers to accomplish the desired port priority for each VC supported. As illustrated in Figure 7‐19 on page 268, the table format depends on the size of each entry and the number of phases supported by this design. 

**267** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐19: Format of Port Arbitration Tables_ 

**==> picture [339 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
32-Phase Port Arbitration Table<br>with 4-bit entries<br>31       28 27      24 23      20 19 16 15       12 11         8 7          4 3           0<br>Phase[7] Phase[6] Phase[5] Phase[4] Phase[3] Phase[2] Phase[1] Phase[0] 00h<br>Phase[15] Phase[14] Phase[13] Phase[12] Phase[11] Phase[10] Phase[9] Phase[8] 04h<br>Phase[23] Phase[22] Phase[21] Phase[20] Phase[19] Phase[18] Phase[17] Phase[16] 08h<br>Phase[31] Phase[30] Phase[29] Phase[28] Phase[27] Phase[26] Phase[25] Phase[24] 0Bh<br>1. Configuration Software loads the Port Arbitration Table.<br>2. Changes to the table automatically set the Port Arbitration 00b PAT entry is 1 bit (2 ports)<br>Table Status bit.<br>01b PAT entry is 2 bits (4 ports)<br>3. Software sets the Load Port Arbitration Table bit to<br>10b PAT entry is 4 bits (16 ports)<br>     apply the table contents to the hardware.<br>4. Hardware loads table contents into the Port Arbiter, then  11b PAT entry is 8 bits (256 ports)<br>    automatically clears the Port Arbitration Table<br>    status bit when the table has been loaded.<br>VC Resource Status Register  Port VC Capability Register 1<br>15                                       2  1  0  31                                                          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP RsvdP<br>VC Negotiation Pending  Port Arbitration Table Entry Size<br> Port Arbitration Table Status  Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>VC Resource Capability Register<br>31              26 24            19 17 16 15 8 7                     0<br>RsvdP VCID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


**268** 

**Chapter 7: Quality of Service** 

## **Switch Arbitration Example** 

Let’s consider an example of a three‐port switch to illustrate both Port and VC arbitration. The example presumes that packets arriving on ingress ports 0 and 1 are moving in the upstream direction and port 2 is the egress port facing upstream (toward the Root Complex). Refer to Figure 7‐20 on page 270 during the following discussion. 

1. Packets arriving at ingress port 0 are placed in a receiver VC based on the TC/VC mapping for port 0. As shown, TLPs with traffic class TC0 or TC1 are sent to the VC0 buffers. TLPs carrying traffic class TC3 or TC5 are sent to the VC1 buffers. No other TCs are permitted on this link. As an aside, if a packet does arrive with a TC that has not been mapped to an existing VC, it will be treated as an error. 

2. Packets arriving at ingress port 1 are placed in a VC based on TC/VC map‐ ping, too, but it’s not the same for this port. As indicated, TLPs carrying traffic class TC0 are sent to VC0, while TLPs carrying traffic class TC2‐TC4 are sent to VC3. No other TCs are permitted on this link. 

3. In both ports, the target egress port is determined from routing information in each packet. For example, address routing is used in memory or IO request TLPs. 

4. All packets destined for egress port 2 are submitted to the TC/VC mapping logic for that port. As shown, TLPs carrying traffic class TC0‐TC2 are placed into buffers for VC0 that are labeled with their ingress port number, while TLPs carrying traffic class TC3‐TC7 are managed for VC1. 

5. Port Arbitration is applied independently to queued up packets to decide which port’s packets will get loaded next into the real VC. 

6. Finally, VC arbitration determines the order in which transactions in the VC buffers will be sent across the link. 

7. Note that the VC arbiter selects packets for transmission only if sufficient flow control credits exist. 

**269** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐20: Arbitration Examples in a Switch_ 

**==> picture [357 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
Switch<br>(1)<br>TC0,1TC3,5  VC0VC1 0 Of IngressMappingTC/VCPort 0 TC0,1TC3,5 INRESS EGRESS (5)Port Arbitration: VC0Egress Port 2<br>FC Buffer VC0 FC Buffer VC1<br>TLP1 RoutingTLP2 Routing TCTC TLP4 RoutingTLP3 Routing TCTC (4) PacketsPort 0 VC0VC0 ARB (6)<br>Egress Port 2<br>To  Port 1 TC/VC VC Arbitration (7)<br>(2) Determine Egress Port(Using Routing Info) (3) To  Port 2To  Port 3 Of EgressMappingPort 2 VC0VC1 ARB 2 TC0-2TC3-7 VC0VC1<br>TC2-4TC0   VC0VC3 1 Of IngressMappingTC/VCPort 1 TC2-4TC0 TC0-2=>VC0TC3-7=>VC1 (5)Port Arbitration: VC1Egress Port 2<br>FC Buffers VC0 FC Buffers VC3 PacketsPort 1 VC1 ARB<br>TLP3 Routing TLP4 Routing VC1<br>TLP1 Routing TLP2 Routing<br>Determine Egress Port(Using Routing Info) (3) To  Port 0To  Port 2To  Port 3 This logic replicated for each egress port<br>**----- End of picture text -----**<br>


## **Arbitration in Multi-Function Endpoints** 

Another set of registers called Multi‐Function Virtual Channel (MFVC) capabil‐ ity is defined for the specific case of endpoints that will implement QoS in a device with multiple functions. Not surprisingly, this case presents the same arbitration issues internally that a switch port must handle. 

There are two cases described in the spec for this arbitration. In the first case, shown in Figure 7‐21 on page 271, there are two Functions but only Function 0 includes VC Capability registers and the assignments made there are implicitly the same for all functions. For this option, arbitration between the functions will be handled in some vendor‐specific manner. That’s the simplest approach, but doesn’t include a standard structure to define priority between requests from different functions and so it doesn’t support QoS. 

**270** 

**Chapter 7: Quality of Service** 

_Figure 7‐21: Simple Multi‐Function Arbitration_ 

**==> picture [252 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Function 0 Vendor-Specific<br>Arbitration<br>VC Internal Link<br>Capability<br>0002h<br>Egress Port<br>Function 1<br>Internal Link<br>**----- End of picture text -----**<br>


If QoS support is desired, then an MFVC is implemented in VC0 and each func‐ tion has its own unique set of VC Capability registers. To preserve software backward compatibility, the spec states that the VC Capability ID for a device that _does not_ use MFVC must be 0002h, while the VC Capability ID for a device that _does_ implement an MFVC structure must be 0009h. 

Figure 7‐22 on page 272 shows the MFVC register block and a block diagram of an example with two functions in an endpoint whose port supports two VCs. Each function has a Transaction Layer and its own VC Capability registers, but doesn’t implement the lower layers. Instead, they connect to the Transaction Layer of the shared port that does have all the layers. Sharing the hardware interface results in lower cost, of course, and the addition of MFVC allows the functions to handle isochronous traffic. 

As can be seen in the figure, the MFVC registers reside in Function 0 only and define the VCs and arbitration methods to be used for this interface. The MFVC registers look very much the same as VC capability registers and support VC arbitration and Function arbitration. Since packets from multiple functions can attempt to access the same VC at the same time, Function Arbitration decides the priorities among them. That should look familiar by now because it’s the same concept as port arbitration and even uses the same arbitration options, including TBWRR. VC arbitration options are also the same as they are in the single‐function VC registers. 

**271** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐22: QoS Support in Multi‐Function Arbitration_ 

**==> picture [330 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header Cnt<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>Func 0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>Func n Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Function Arbitration Table 0<br>Function Arbitration Table n<br>Function<br>Function 0 Arbiter<br>MFVC Port 1<br>Capability VC0<br>0008h Internal Link<br>Port 2 VC0 VC Arbiter<br>VC<br>Capability VC0<br>0009h<br>Egress<br>Port<br>Function 1<br>Port 1<br>VC7<br>Internal Link<br>VC Port 2 VC7<br>Capability VC7<br>0009h<br>TC/VC Mapping<br>**----- End of picture text -----**<br>


## **Isochronous Support** 

As mentioned earlier, not every machine or application needs isochronous sup‐ port, but there are some that can’t get by without it. Since PCIe was designed to support it from the beginning, let’s consider what would need to be in place to make this work. 

**272** 

**Chapter 7: Quality of Service** 

## **Timing is Everything** 

Consider the example shown in Figure 7‐23 on page 274, where a synchronous connection would be desirable but isn’t possible. Instead, we emulate a synchro‐ nous path with isochronous mechanisms. In this example, isochrony defines the amount of data that will be delivered within each Service Interval to achieve the required service. The following sequence describes the operation: 

1. The synchronous source (video camera and PCI Express interface) accumu‐ lates data in Buffer A during the first of the equal service intervals (SI 1). 

2. The camera delivers all of the accumulated data across the general‐purpose bus during the next service interval (SI 2) while it accumulates the next block of data in Buffer B. 

   - Clearly, the system must be able to guarantee that the entire contents of buffer A can be delivered during the service interval, regardless of whether other traffic is in flight on the Link. This is handled by assigning a high pri‐ ority to the time‐sensitive packets and programming arbitration schemes so they’ll be handled first any time there is competition with other traffic. Also note that, as long as all the data is delivered within the time window, it doesn’t matter exactly when it arrives. It might be spread out across the interval or bunched up in one place inside it. As long as it’s all delivered with the Service Interval the guarantees can still be met. 

3. During SI 2, the tape deck receives and buffers the incoming data, which can then be delivered to storage for recording during SI 3. The camera unloads Buffer B onto the Link during SI 3 while accumulating new data into Buffer A, and the cycle repeats. 

**273** 

**PCI Ex ress Technolo p gy** 

_Figure 7‐23: Example Application of Isochronous Transaction_ 

**==> picture [298 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
Camera<br>SI 1 Data accumulated<br>in Buffer A<br>SI 2 Data from Buffer A<br>delivered while<br>next data accumulates<br>in Buffer B<br>SI 3 Data from Buffer B<br>delivered while next<br>data accumulates in<br>Buffer A<br>PCI Express<br>Interface<br>SI 1 SI 2 SI 3<br>Service Interval (SI)<br>SI 2 Data received into<br>Buffer A<br>SI 3 Data from Buffer A<br>delivered to Storage<br>while data received<br>into Buffer B<br>Storage (e.g.: tape)<br>Buffer A Buffer B<br>Buffer A Buffer B<br>**----- End of picture text -----**<br>


## **How Timing is Defined**

</td>
<td style="background-color:#e8e8e8">

- 10b — 4 位(16 个端口)

- 11b — 8 位(256 个端口)

配置软件为每个表加载端口编号,以实现受支持的每个 VC 所需的端口优先级。如图 7-19 (第 268 页) 所示,表的格式取决于每个条目的大小和此设计支持的阶段数。

**267**

**PCI Ex ress Technolo p gy**

_Figure 7‐19: 端口仲裁表的格式_

**==> picture [339 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
32 阶段端口仲裁表<br>具有 4 位条目<br>31       28 27      24 23      20 19 16 15       12 11         8 7          4 3           0<br>Phase[7] Phase[6] Phase[5] Phase[4] Phase[3] Phase[2] Phase[1] Phase[0] 00h<br>Phase[15] Phase[14] Phase[13] Phase[12] Phase[11] Phase[10] Phase[9] Phase[8] 04h<br>Phase[23] Phase[22] Phase[21] Phase[20] Phase[19] Phase[18] Phase[17] Phase[16] 08h<br>Phase[31] Phase[30] Phase[29] Phase[28] Phase[27] Phase[26] Phase[25] Phase[24] 0Bh<br>1. 配置软件加载端口仲裁表。<br>2. 对表的更改自动设置端口仲裁 00b PAT 条目为 1 位(2 个端口)<br>表状态位。<br>01b PAT 条目为 2 位(4 个端口)<br>3. 软件设置 Load Port Arbitration Table 位以<br>10b PAT 条目为 4 位(16 个端口)<br>     将表内容应用于硬件。<br>4. 硬件将表内容加载到端口仲裁器,然后  11b PAT 条目为 8 位(256 个端口)<br>    在表加载完成时自动清除端口仲裁表<br>    状态位。<br>VC Resource Status Register  Port VC Capability Register 1<br>15                                       2  1  0  31                                                          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP RsvdP<br>VC Negotiation Pending  Port Arbitration Table Entry Size<br> Port Arbitration Table Status  Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>VC Resource Capability Register<br>31              26 24            19 17 16 15 8 7                     0<br>RsvdP VCID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


**268**

**第 7 章:服务质量**

## **交换机仲裁示例 (Switch Arbitration Example)**

让我们考虑一个三端口交换机的示例,以说明端口和 VC 仲裁。该示例假定入口端口 0 和 1 上的数据包向上游方向移动,端口 2 是面向上游(朝向根复合体)的出口端口。在下面的讨论中请参考图 7-20 (第 270 页)。

1. 到达入口端口 0 的数据包根据端口 0 的 TC/VC 映射被放置在接收器 VC 中。如图所示,流量类 TC0 或 TC1 的 TLP 被发送到 VC0 缓冲区。携带流量类 TC3 或 TC5 的 TLP 被发送到 VC1 缓冲区。此链路上不允许使用其他 TC。顺便说一句,如果收到的数据包具有未映射到现有 VC 的 TC,它将被视为错误。

2. 到达入口端口 1 的数据包也根据 TC/VC 映射放入 VC 中,但与此端口不同。如图所示,携带流量类 TC0 的 TLP 被发送到 VC0,而携带流量类 TC2-TC4 的 TLP 被发送到 VC3。此链路上不允许使用其他 TC。

3. 在两个端口中,目标出口端口由每个数据包中的路由信息决定。例如,内存或 IO 请求 TLP 使用地址路由。

4. 所有发往出口端口 2 的数据包都提交给该端口的 TC/VC 映射逻辑。如图所示,携带流量类 TC0-TC2 的 TLP 被放入标有其入口端口号的 VC0 缓冲区,而携带流量类 TC3-TC7 的 TLP 由 VC1 管理。

5. 端口仲裁独立地应用于排队的数据包,以决定哪个端口的数据包接下来将加载到实际 VC 中。

6. 最后,VC 仲裁确定 VC 缓冲区中的事务将按何种顺序通过链路发送。

7. 请注意,VC 仲裁器仅在存在足够流控信用时才选择要传输的数据包。

**269**

**PCI Ex ress Technolo p gy**

_Figure 7‐20: 交换机中的仲裁示例_

**==> picture [357 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
交换机 (Switch)<br>(1)<br>TC0,1TC3,5  VC0VC1 0 入口的 IngressMappingTC/VCPort 0 TC0,1TC3,5 INRESS EGRESS (5)端口仲裁:VC0出口端口 2<br>FC Buffer VC0 FC Buffer VC1<br>TLP1 RoutingTLP2 Routing TCTC TLP4 RoutingTLP3 Routing TCTC (4) 数据包Port 0 VC0VC0 ARB (6)<br>出口端口 2<br>到  端口 1 TC/VC VC 仲裁 (7)<br>(2) 确定出口端口(使用路由信息) (3) 到  端口 2到  端口 3 出口的 EgressMappingTC/VCPort 2 VC0VC1 ARB 2 TC0-2TC3-7 VC0VC1<br>TC2-4TC0   VC0VC3 1 入口的 IngressMappingTC/VCPort 1 TC2-4TC0 TC0-2=>VC0TC3-7=>VC1 (5)端口仲裁:VC1出口端口 2<br>FC Buffers VC0 FC Buffers VC3 数据包Port 1 VC1 ARB<br>TLP3 Routing TLP4 Routing VC1<br>TLP1 Routing TLP2 Routing<br>确定出口端口(使用路由信息) (3) 到  端口 0到  端口 2到  端口 3 此逻辑为每个出口端口复制<br>**----- End of picture text -----**<br>


## **多功能端点中的仲裁 (Arbitration in Multi-Function Endpoints)**

为将在具有多个功能的设备中实现 QoS 的端点这种特殊情况,定义了一组称为多功能虚拟通道 (MFVC, Multi-Function Virtual Channel) 功能的寄存器。毫不奇怪,这种情况在内部呈现出交换机端口必须处理的相同仲裁问题。

规范中描述了此仲裁的两种情况。在第一种情况中,如图 7-21 (第 271 页) 所示,有两个功能,但只有功能 0 包含 VC Capability 寄存器,此处所做的分配对所有功能隐式相同。对于此选项,功能之间的仲裁将以某种厂商特定的方式处理。这是最简单的方法,但不包括用于定义来自不同功能的请求之间优先级的标准结构,因此它不支持 QoS。

**270**

**第 7 章:服务质量**

_Figure 7‐21: 简单的多功能仲裁_

**==> picture [252 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Function 0 厂商特定 (Vendor-Specific)<br>仲裁<br>VC 内部链路<br>功能 (Capability)<br>0002h<br>出口端口<br>Function 1<br>内部链路<br>**----- End of picture text -----**<br>


如果需要 QoS 支持,则在 VC0 中实现 MFVC,并且每个功能都有其自己唯一的一组 VC Capability 寄存器。为保持软件向后兼容性,规范规定 _不使用_ MFVC 的设备的 VC Capability ID 必须为 0002h,而 _使用_ MFVC 结构的设备的 VC Capability ID 必须为 0009h。

图 7-22 (第 272 页) 展示了 MFVC 寄存器块以及端点中具有两个功能且其端口支持两个 VC 的示例框图。每个功能都有一个事务层 (Transaction Layer) 和自己的 VC Capability 寄存器,但未实现较低的层。相反,它们连接到共享端口的事务层(后者具有所有层)。共享硬件接口当然会导致成本降低,而添加 MFVC 允许这些功能处理等时流量。

从图中可以看出,MFVC 寄存器仅驻留在功能 0 中,并定义要用于此接口的 VC 和仲裁方法。MFVC 寄存器看起来与 VC capability 寄存器非常相似,并支持 VC 仲裁和功能仲裁。由于来自多个功能的数据包可以同时尝试访问同一 VC,因此功能仲裁决定它们之间的优先级。到现在为止,您应该对此很熟悉了,因为它与端口仲裁的概念相同,甚至使用相同的仲裁选项,包括 TBWRR。VC 仲裁选项也与单功能 VC 寄存器中的相同。

**271**

**PCI Ex ress Technolo p gy**

_Figure 7‐22: 多功能仲裁中的 QoS 支持_

**==> picture [330 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header Cnt<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>Func 0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>Func n Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Function Arbitration Table 0<br>Function Arbitration Table n<br>Function<br>Function 0 仲裁器<br>MFVC 端口 1<br>功能 VC0<br>0008h 内部链路<br>端口 2 VC0 VC 仲裁器<br>VC<br>功能 VC0<br>0009h<br>出口<br>端口<br>Function 1<br>端口 1<br>VC7<br>内部链路<br>VC 端口 2 VC7<br>功能 VC7<br>0009h<br>TC/VC 映射<br>**----- End of picture text -----**<br>


## **等时支持 (Isochronous Support)**

如前所述,并非每台机器或应用程序都需要等时支持,但有些机器或应用程序没有它就无法工作。由于 PCIe 从一开始就设计为支持它,让我们考虑一下要使其工作需要满足哪些条件。

**272**

**第 7 章:服务质量**

## **时序就是一切 (Timing is Everything)**

考虑图 7-23 (第 274 页) 所示的示例,此处需要同步连接但无法实现。相反,我们用等时机制模拟同步路径。在此示例中,等时性定义了在每个服务间隔 (Service Interval) 内将传送的数据量,以实现所需的服务。以下顺序描述了该操作:

1. 同步源(摄像机和 PCI Express 接口)在第一个相等的服务间隔 (SI 1) 期间将数据累积在缓冲区 A 中。

2. 摄像机在下一个服务间隔 (SI 2) 期间通过通用总线传送所有累积的数据,同时在缓冲区 B 中累积下一块数据。

   - 显然,系统必须能够保证缓冲区 A 的全部内容可以在服务间隔内传送,无论链路上是否有其他流量在传输。这是通过为时间敏感的数据包分配高优先级并编程仲裁方案来实现的,以便在与其他流量竞争时优先处理这些数据包。另请注意,只要所有数据都在时间窗口内传送,那么它确切何时到达并不重要。它可以分散在整个间隔内,也可以集中在一个位置内。只要它在服务间隔内全部传送,仍然可以满足保证。

3. 在 SI 2 期间,磁带录像机接收并缓冲传入数据,然后可以在 SI 3 期间将其传送到存储器进行记录。摄像机在 SI 3 期间将缓冲区 B 卸载到链路上,同时将新数据累积到缓冲区 A 中,如此循环往复。

**273**

**PCI Ex ress Technolo p gy**

_Figure 7‐23: 等时事务的示例应用_

**==> picture [298 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
摄像机 (Camera)<br>SI 1 数据累积<br>在缓冲区 A 中<br>SI 2 从缓冲区 A 传送数据<br>同时下一批数据<br>在缓冲区 B 中累积<br>SI 3 从缓冲区 B 传送数据<br>同时下一批数据<br>在缓冲区 A 中累积<br>PCI Express<br>接口<br>SI 1 SI 2 SI 3<br>服务间隔 (SI)<br>SI 2 数据接收到<br>缓冲区 A<br>SI 3 从缓冲区 A 传送数据<br>到存储器<br>同时数据接收到<br>缓冲区 B<br>存储器 (例如:磁带)<br>缓冲区 A 缓冲区 B<br>缓冲区 A 缓冲区 B<br>**----- End of picture text -----**<br>


## **时序如何定义 (How Timing is Defined)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-9"></a>
## 6.9 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Isochronous timing is defined in PCIe by the time slot used in the Time‐Based Weighted Round Robin port arbitration scheme. At present, the time for each slot is 100ns, and represents one entry of the 128 entries in the TBWRR table. Once set up, the arbiter will repeatedly cycle through this table once every 12.8  s, which represents the overall Service Interval. 

Making an isochronous path work as intended requires a few considerations. First, the data packets must be delivered with predictable timing at regular intervals. Second, the maximum amount of isochronous data to be delivered must be known ahead of time and packets must not be allowed to exceed that limit. Third, the Link bandwidth must be sufficient to support the amount of data that needs to be delivered in a given time slot. 

**274** 

**Chapter 7: Quality of Service** 

Consider the following example. A single‐Lane Link running at 2.5 Gbps deliv‐ ers one symbol every 4ns. That allows it to send 25 symbols within a 100ns time slot, but is that enough to be useful? In many cases it’s not, because a TLP may need 28 bytes of overhead for the combination of header, sequence number, LCRC, and so forth. That would mean there isn’t even time to finish sending the overhead, much less any data payload in 100ns. If we needed to send 128 bytes of data, then the bandwidth requirement would be 128+overhead = 156 bytes. One option for solving this problem would be to increase the Link width to 8 Lanes, allowing eight times as many bytes to be sent at once. That change would deliver 200 bytes in 100ns and allow a single time slot to deliver all the isochronous data. Another solution would be to use a single Lane but give the port more time slots, since 8 time slots at the lower Link width would deliver the same amount of data. The choice of solution depends on cost and perfor‐ mance constraints, but the system designer must know the timing and band‐ width requirements of the isochronous path to be able to set it up correctly. 

## **How Timing is Enforced** 

When timing is an integral part of the proper operation of a design, as in the previous example, it is enforced by the combination of things we’ve discussed so far. First, high‐priority TCs must be selected in software and VCs set up in hardware with the mappings between them defined so that only the correct packets will be placed into the high‐priority VCs. Then the desired timing is a matter of programming the arbitration schemes to accommodate the needed bandwidth in the specified time. For example, the choice for VC arbitration would probably be the Strict Priority option, since it’s the only choice that can ensure that a high‐priority packet won’t be delayed by other packets. For Port arbitration the choice must be TBWRR to enforce timing. 

## **Software Support** 

Supporting isochronous service requires some coordination between the soft‐ ware elements in the system. In a PC system, device drivers will report isochro‐ nous requirements and capabilities to the OS, which will then evaluate the overall system demands and allocate resources appropriately. Embedded sys‐ tems will be different, because the all the pieces are known at the outset and software can be simpler. In the following discussion we’ll describe the PC case since an embedded system should simply be a simpler subset of that. 

**275** 

**PCI Ex ress Technolo p gy** 

## **Device Drivers** 

A device driver must be able to report its timing requirements to the software that oversees isochronous operation and obtain permission before trying to use isochronous packets. It’s important to note that driver‐level software should not directly change hardware assignments or arbitration policies on its own, even though it could, because the result would be chaos. If multiple drivers were each independently trying to do this, the last one to make changes would over‐ write any previous assignments. To avoid that, an OS‐level program called an Isochronous Broker receives the timing requests from the system devices and assigns system resources in a coordinated way that accommodates them all. 

## **Isochronous Broker** 

This program manages the end‐to‐end flow of isochronous packets. It receives the isochronous timing requests from device drivers and allocates system resources in a way that accommodates the requests through the target path. In the spec this is referred to as establishing an isochronous contract between the requester/completer pair and the PCIe fabric. Doing so requires verifying that the intended path can indeed support isochronous traffic, and then program‐ ming the appropriate arbitration schemes to ensure it works within the speci‐ fied timing requirements. 

## **Bringing it all together** 

By now it should be reasonably clear what needs to be done to support isochro‐ nous traffic flow in a system, but let’s look at one last example to bring all the pieces together. If we expand on the previous video capture example to show a more complex system, like the one in Figure 7‐24 on page 277, we’ll be able to discuss all the parts that must be in place if the video camera is going to be able to deliver captured data into system memory. This would be a difficult environ‐ ment for isochronous service because there are so many devices that can com‐ pete for bandwidth in the path, but that also makes it useful to illustrate the various things that must be considered. 

## **Endpoints** 

Starting at the bottom, what will be needed in the PCIe interface for the video endpoint device itself? In hardware, more than one VC will be required if we’re going to differentiate packets. Let’s assume a single‐function device for simplic‐ ity. The device driver would need to report the device capabilities and isochro‐ nous timing requirements to the OS‐level Isochronous broker, which would evaluate the system and then report back whether an isochronous contract was possible and which TCs the software should use. 

**276** 

**Chapter 7: Quality of Service** 

_Figure 7‐24: Example Isochronous System_ 

**==> picture [308 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>GFX Root Complex<br>System<br>Memory<br>Switch 2<br>Switch 1<br>Slot<br>Video SCSI<br>Camera<br>Lower<br>Time-<br>priority<br>sensitive<br>data<br>data<br>**----- End of picture text -----**<br>


The driver would then program VC numbers and map the appropriate TCs to each VC. It would also most likely program the VC arbitration to be Strict Prior‐ ity for the high‐priority channels. The one caveat here is that the arbitration must still be “fair”, meaning the low‐priority channels won’t get starved for access. That means the high‐priority VCs can’t have traffic pending constantly but instead must spread out packet injection over time. 

One other observation regarding Link operation is necessary before we finish our discussion of endpoints, and that is regarding Flow Control. The receive buffers of devices in the isochronous path must be large enough to handle the expected packet flow without causing any back pressure as long as packets are injected uniformly according to the Isochronous Contract. In addition, Flow Control Updates must be returned quickly enough to avoid stalls. 

**277** 

**PCI Ex ress Technolo p gy** 

## **Switches** 

Next, consider what would need to be present in each of the switches that reside between the endpoint and the Root Complex. Switches don’t commonly have device drivers, so it would fall to OS‐level software like the Isochronous Broker to read their configuration information and determine what service they sup‐ port. First, all the ports in the isochronous path must support more than one VC, and the TC/VC mapping must match on both ends of each Link. Remember that once the packet gets into the Transaction Layer of the Switch port, only the TC remains with the packet, and the VC assignment for that TC is specific to each port. The TC/VC mapping of the downstream port of Switch 1 must match the mapping of the endpoint, but the other switch port mappings may be differ‐ ent to match the other end of their Links. 

**Arbitration Issues.** The choices for arbitration are straight‐forward. In our example, the isochronous path is shown as carrying traffic in only one direction for simplicity. It is possible to have isochronous traffic flowing in both directions in the case of a memory read, for example, but our example was chosen to resemble the video streaming case. 

VC arbitration for the isochronous egress port will most likely need to use the Strict Priority scheme for the same reasons the endpoint does. Port arbi‐ tration will need to use the Time‐Based WRR scheme, and that means soft‐ ware must understand the proper access ratios and program the Port Arbitration Tables to implement them. This might not be as simple as it sounds if multiple switches are in the path because even though they’ll all use the same TBWRR arbitration scheme, it’s not clear how the service inter‐ vals for each of them would be coordinated. If the SIs are not aligned, mean‐ ing timing guarantees could be more difficult depending on the how busy the Links are. Coordinating the service intervals wasn’t considered in the spec, though, so it would again involve a non‐standard method. Clearly, this problem would be much simpler if we didn’t have multiple switches in an isochronous path. 

**Timing Issues.** Figure 7‐25 on page 279 shows the timing of packets being delivered by the two endpoints for our example. Packets from the video device, with a known size and delivered in regular and predictable inter‐ vals, are shown as the heavier arrows. The smaller, lighter arrows represent packets from the SCSI drive that are lower priority and whose timing is not predictable. In the endpoint, the packets simply need to have the proper TC assigned to them, but a switch needs to ensure that the proper timing policy is enforced. This is done by using TBWRR, which specifies which port will have access at a given time and for how long. Knowing the size and fre‐ 

**278** 

**Chapter 7: Quality of Service** 

quency of the isochronous packets allows software to properly arrange the timing, but what kind of timing is needed? 

_Figure 7‐25: Injection of Isochronous Packets_ 

**==> picture [269 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


First, let’s review the parameters involved by considering a simple example. Recall that PCIe bases a time slot on the reference clock period is given by the Port Capability Register 1 field called Reference Clock. At present the only option for that field is 100ns, and the TBWRR table has no options besides 128 entries. The length of the Service Interval is the multiple of those, making it 12.8  s. The bandwidth for a given device can be expressed by the equation below, where Y is the data to be delivered in one time slot (the spec states that the Max Payload Size programmed during configuration must be used for this bandwidth calculation), M is the number of time slots, and T is the overall Ser‐ vice Interval. If we choose 128 bytes as the payload, and we know that SI is 12.8  s, then the BW = 10 MB/s for each time slot allocated. 

**==> picture [79 x 28] intentionally omitted <==**

Now let’s consider a more realistic example. Let’s say that our Links are running at the Gen2 speed, that the video device needs to have a guaranteed bandwidth of 100MB/s, and that it will send 512 byte packets. Filling in the equation shows M = 2.5 instances of 512 bytes are needed. But how much data can actually be 

**==> picture [324 x 41] intentionally omitted <==**

</td>
<td style="background-color:#e8e8e8">

等时时序在 PCIe 中由基于时间的加权轮询 (Time-Based Weighted Round Robin) 端口仲裁方案中使用的时间片定义。目前,每个时隙的时间为 100ns,代表 TBWRR 表中 128 个条目中的一个。一旦设置好,仲裁器将每 12.8μs 循环遍历一次该表,这表示整个服务间隔。

要使等时路径按预期工作,需要考虑一些事项。首先,数据包必须以可预测的时序在规律的间隔内传送。其次,必须提前知道要传送的最大等时数据量,并且必须不允许数据包超过该限制。第三,链路带宽必须足以支持在给定时间片内需要传送的数据量。

**274**

**第 7 章:服务质量**

考虑以下示例。单条 Lane 链路以 2.5 Gbps 运行,每 4ns 传送一个符号。这允许它在 100ns 的时间片内发送 25 个符号,但这足够用吗?在许多情况下是不够的,因为 TLP 可能需要 28 字节的开销用于头部、序列号、LCRC 等组合。这意味着在 100ns 内甚至没有时间完成开销的发送,更不用说任何数据有效负载了。如果我们需要发送 128 字节的数据,则带宽要求为 128+开销 = 156 字节。解决此问题的一种选择是将链路宽度增加到 8 个 Lane,从而允许一次发送八倍的字节数。此更改将在 100ns 内传送 200 字节,并允许单个时隙传送所有等时数据。另一种解决方案是使用单条 Lane 但给端口更多的时间片,因为在较低的链路宽度下 8 个时间片将传送相同数量的数据。解决方案的选择取决于成本和性能约束,但系统设计者必须知道等时路径的时序和带宽要求才能正确设置它。

## **时序如何强制执行 (How Timing is Enforced)**

当时序是设计正常运行不可分割的一部分时,如上例所示,它通过我们迄今为止讨论的内容的组合来强制执行。首先,必须在软件中选择高优先级 TC,并在硬件中设置 VC,定义它们之间的映射,以便只有正确的数据包才会被放入高优先级 VC。然后,所需的时序是对仲裁方案进行编程以适应指定时间内所需带宽的问题。例如,VC 仲裁的选择很可能是严格优先级选项,因为它是唯一可以确保高优先级数据包不会被其他数据包延迟的选择。对于端口仲裁,选择必须是 TBWRR 来强制执行时序。

## **软件支持 (Software Support)**

支持等时服务需要系统中软件元素之间的一些协调。在 PC 系统中,设备驱动程序将向操作系统报告等时要求和支持能力,然后操作系统将评估整个系统需求并适当地分配资源。嵌入式系统会有所不同,因为所有部件从一开始就是已知的,因此软件可以更简单。在下面的讨论中,我们将描述 PC 情况,因为嵌入式系统应该只是该情况的更简单子集。

**275**

**PCI Ex ress Technolo p gy**

## **设备驱动程序 (Device Drivers)**

设备驱动程序必须能够向监督等时操作的软件报告其时序要求,并在尝试使用等时数据包之前获得许可。重要的是要注意,即使驱动程序级软件可以直接更改硬件分配或仲裁策略,也不应自行执行此操作,因为这样会导致混乱。如果多个驱动程序各自独立地尝试执行此操作,那么最后进行更改的驱动程序将覆盖之前的所有分配。为避免这种情况,一个称为等时代理 (Isochronous Broker) 的操作系统级程序接收来自系统设备的时序请求,并以协调的方式分配系统资源以容纳所有这些请求。

## **等时代理 (Isochronous Broker)**

此程序管理等时数据包的端到端流。它从设备驱动程序接收等时时序请求,并以适应通过目标路径的请求的方式分配系统资源。在规范中,这称为在请求者/完成者对和 PCIe 架构之间建立等时合同。这样做需要验证预期路径是否确实可以支持等时流量,然后对适当的仲裁方案进行编程以确保它在指定的时序要求内工作。

## **将所有内容整合在一起 (Bringing it all together)**

到现在为止,应该相当清楚在系统中支持等时流量流需要做什么,但让我们看最后一个示例以将所有内容整合在一起。如果我们扩展之前的视频捕获示例以展示一个更复杂的系统,如图 7-24 (第 277 页) 所示,我们将能够讨论如果视频摄像机要能够将捕获的数据传送到系统内存中,必须准备好的所有部件。对于等时服务来说,这是一个困难的环境,因为路径中有很多设备可以竞争带宽,但这也使其可用于说明必须考虑的各种事情。

## **端点 (Endpoints)**

从底部开始,视频端点设备的 PCIe 接口中需要什么?在硬件中,如果我们要区分数据包,则需要多个 VC。为简单起见,我们假设一个单功能设备。设备驱动程序需要向操作系统级的等时代理报告设备支持能力和等时时序要求,该代理将评估系统然后报告等时合同是否可行以及软件应使用哪些 TC。

**276**

**第 7 章:服务质量**

_Figure 7‐24: 等时系统示例_

**==> picture [308 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
处理器 (Processor)<br>GFX 根复合体 (Root Complex)<br>系统<br>内存<br>交换机 2<br>交换机 1<br>插槽<br>视频 SCSI<br>摄像机<br>较低<br>时间<br>优先级<br>敏感<br>数据<br>数据<br>**----- End of picture text -----**<br>


然后驱动程序将编程 VC 编号并将适当的 TC 映射到每个 VC。它还很可能对高优先级通道的 VC 仲裁编程为严格优先级。这里的一个警告是仲裁仍必须"公平",这意味着低优先级通道不会因访问而被饿死。这意味着高优先级 VC 不能始终有挂起的流量,而是必须在一段时间内分散数据包的注入。

在完成端点讨论之前,关于链路操作还有另一个观察需要说明,即关于流控。只要数据包根据等时合同均匀注入,等时路径中设备的接收缓冲区必须足够大以处理预期的数据包流而不会造成任何背压。此外,流控更新必须足够快地返回以避免停顿。

**277**

**PCI Ex ress Technolo p gy**

## **交换机 (Switches)**

接下来,考虑位于端点和根复合体之间的每个交换机中需要存在的内容。交换机通常没有设备驱动程序,因此将由操作系统级软件(如等时代理)负责读取它们的配置信息并确定它们提供的服务。首先,等时路径中的所有端口必须支持多个 VC,并且 TC/VC 映射必须在每个链路的两端匹配。请记住,一旦数据包进入交换机端口的事务层,只有 TC 与数据包一起保留,并且该 TC 的 VC 分配特定于每个端口。交换机 1 的下游端口的 TC/VC 映射必须与端点的映射匹配,但其他交换机端口映射可能不同,以匹配其链路的另一端。

**仲裁问题 (Arbitration Issues)。** 仲裁的选择是直接的。在我们的示例中,为简单起见,等时路径仅显示为沿一个方向传输流量。例如在内存读取的情况下,等时流量可以双向流动,但我们的示例选择为类似于视频流传输的情况。

出于端点使用的相同原因,等时出口端口的 VC 仲裁很可能需要使用严格优先级方案。端口仲裁将需要使用基于时间的 WRR 方案,这意味着软件必须理解适当的访问比例并对端口仲裁表进行编程以实现这些比例。如果路径中有多个交换机,这可能不像听起来那么简单,因为即使它们都使用相同的 TBWRR 仲裁方案,目前也不清楚如何协调每个交换机的服务间隔。如果 SI 未对齐,则意味着时序保证可能更困难,这取决于链路的繁忙程度。协调服务间隔在规范中未被考虑,因此它将再次涉及非标准方法。显然,如果等时路径中没有多个交换机,这个问题会简单得多。

**时序问题 (Timing Issues)。** 图 7-25 (第 279 页) 展示了在我们的示例中由两个端点传送的数据包的时序。来自视频设备的数据包(具有已知大小并以规律可预测的间隔传送)显示为较粗的箭头。较小、较浅的箭头表示来自 SCSI 驱动器的较低优先级且时序不可预测的数据包。在端点中,数据包只需要为它们分配适当的 TC,但交换机需要确保强制执行适当的时序策略。这是通过使用 TBWRR 来完成的,它指定哪个端口将在给定时间访问以及访问多长时间。了解等时数据包的大小和频率允许软件正确安排时序,但需要什么类型的时序呢?

**278**

**第 7 章:服务质量**

_Figure 7‐25: 等时数据包的注入_

**==> picture [269 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = 服务间隔 (Service Interval)<br>SI 1 SI 2 SI 3<br>时间<br>**----- End of picture text -----**<br>


首先,让我们通过考虑一个简单的示例来回顾所涉及的参数。回想一下,PCIe 基于由 Port Capability Register 1 字段 Reference Clock 给出的参考时钟周期来计算时间片。目前该字段的唯一选项是 100ns,TBWRR 表除 128 个条目外没有其他选项。服务间隔的长度是这些的倍数,因此为 12.8μs。给定设备的带宽可以由下面的等式表示,其中 Y 是要在一个时间片中传送的数据(规范规定必须使用在配置期间编程的最大有效负载大小进行此带宽计算),M 是时间片数,T 是整个服务间隔。如果我们选择 128 字节作为有效负载,并且我们知道 SI 为 12.8μs,则对于分配的每个时间片,BW = 10 MB/s。

**==> picture [79 x 28] intentionally omitted <==**

现在让我们考虑一个更现实的示例。假设我们的链路以 Gen2 速度运行,视频设备需要保证 100MB/s 的带宽,并且它将发送 512 字节的数据包。代入等式显示 M = 2.5 个 512 字节的实例是必需的。但实际上在

**==> picture [324 x 41] intentionally omitted <==**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-6-10"></a>
## 6.10 Flow Control | 流控

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

sent in one time slot? The answer depends on speed and Link width, or course. At 5.0 Gb/s it takes 2ns to send each 10‐bit symbol, so 50 symbols can be deliv‐ ered per Lane in 100ns. If the packet size is 512 bytes of data plus another 28 or so for the header, then 11 time slots would be needed to deliver 550 symbols for one packet using a x1 Link. It is possible to give one port several contiguous 

**279** 

## **PCI Ex ress Technolo p gy** 

slots if needed, so that’s one solution. Since the packet size that will be sent is always the same, we can’t really program 2.5 instances of it, so we’d have to use 3 instead. From our equation, 3 instances of 512 bytes each results in an actual bandwidth of 120MB/s. That’s higher than we need, but it solves the problem. The number of time slots used would then be 11 x 3 = 33, leaving 95 for other use in the Service Interval. Each group of 11 time slots would need to be contig‐ uous but the groups could be spaced out over the service interval. 

Another solution would be increase the Link width. Although the hardware would cost more, using 11 Lanes would allow delivery of all the data in one time slot. The CEM spec doesn’t currently support a x11 option, but a x12 option is available and would work for our example. Using a wide Link like that means software would only need to program one time slot for each packet, and just three over the whole service interval to support isochronous traffic for this device. Unlike the x1 case, now we wouldn’t need contiguous time slots. Instead, they could be spaced over the service interval in some optimal fashion. 

**Bandwidth Allocation Problems.** The TBWRR table must be pro‐ grammed to guarantee sufficient timely bandwidth for isochronous traffic, and that other traffic won’t be allowed to interfere. In Figure 7‐25 on page 279, the SCSI controller is shown as sending one packet in SI 1 and another in SI 3. If the timing was such that one packet from that endpoint per SI was allowed then this works fine. 

Now let’s say the SCSI controller attempts to inject more packets than it has permission to do in SI 1, illustrated in Figure 7‐26 on page 280. This is the first of two bandwidth allocation problems mentioned in the spec and is called “oversubscription.” This could interfere with isochronous traffic flow, but programming the TBWRR table readily avoids that problem because the arbitration only allows a packet from that port at specific times. If more packets from that port are queued up, they simply have to wait until the next available time, which might be in SI 2, as shown in this exam‐ ple. Eventually, this can result in flow control back‐pressure at the sending agent 

_Figure 7‐26: Over‐Subscribing the Bandwidth_ 

**==> picture [263 x 94] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**280** 

**Chapter 7: Quality of Service** 

The second timing problem is called “congestion” and happens when too many isochronous requests are sent within a given time window, as shown in Figure 7‐27 on page 281. This is a similar problem but now there is no simple solution. Unlike the previous case, postponing high‐priority packets until another time slot is not an option, so the system must make an effort to handle them all. The result is that some requests may experience excessive service latencies. To correct this, software would need to change the distri‐ bution of packets so that they can be supported by the available hardware bandwidth. 

_Figure 7‐27: Bandwidth Congestion_ 

**==> picture [263 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = Service Interval<br>SI 1 SI 2 SI 3<br>time<br>**----- End of picture text -----**<br>


**Latency Issues .** Managing latency for packet delivery is an important part of isochrony, and involves the combination of the fabric latency and the Completer latency. Fabric latency depends on all the characteristics of the Link between the various components in the system, especially the Link width and frequency of operation. A simple way to minimize this value is to constrain the complexity of the PCIe topology for isochronous paths. Completer latency depends on the target endpoint internal characteristics, such as memory speed and internal arbitration. 

## **Root Complex** 

The RC has the same arbitration and timing requirements as a switch. It receives packets on several downstream ports and forwards them to the target in a way that’s consistent with the rules for isochrony described earlier. However, much of how this is done will be vendor specific because the spec doesn’t define the RC or how it should be programmed. 

**Problem: Snooping.** One interesting thing affecting timing and latency in the root that we haven’t yet discussed is the process of snooping. Normally, anytime an access to system memory takes place it will be to a location that the processor considers cacheable, meaning it has permission to store a tem‐ 

**281** 

**PCI Ex ress Technolo p gy** 

porary copy in its local caches. If an external device attempts to accesses that area of memory, the chipset must first check the processor caches before allowing the access because a cached copy may have been modified. If so, the modified data will need to be written back to memory before it will be available for the device access. Although it’s necessary to ensure memory coherency, the problem is that snooping takes time. How long it takes is typically bounded but not predictable because it depends on what else the CPUs are doing at that time. Depending on the timing require‐ ments, that kind of uncertainty could ruin an isochronous data flow. 

**Snooping Solutions.** One way to avoid snooping is for devices to only access areas of memory that have been designated as uncacheable. Another option is for software to set the “No Snoop” attribute bit in the high‐priority packet headers. That forces the chipset to skip the snoop step regardless of the memory type and go directly to memory because software has guaran‐ teed that doing so won’t cause a problem. To enforce this as a requirement for the isochronous path, another bit can be initialized by hardware in the root port for the high‐priority VC called “Reject Snoop Transactions” (see the VC Resource Capability Register in Figure 7‐17 on page 265). The pur‐ pose of this is to allow only transactions for that VC that have the No Snoop attribute set. Any incoming packets that don’t have it set are discarded to ensure that the timing will never be violated by waiting for a snoop. 

## **Power Management** 

It’s a simple observation, but if timing is important for a path in PCIe, then power management (PM) mechanisms for devices in that path will need to han‐ dled carefully. Configuration software can read the latencies associated with every PM condition and select those cases that the timing budget will permit. The simplest approach, though, would just be to disable all PM options in an isochronous path. Fortunately, this is easily done using existing configuration registers. Devices can be placed into the device state D0 and left there, while the hardware‐controlled Link PM mechanism can be disabled (for more on PM, see Chapter 16, entitled ʺPower Management,ʺ on page 703). 

## **Error Handling** 

Finally, there is one last issue: what to do when errors occur on the Link. The ACK/NAK protocol, covered in Chapter 7, provides an automatic, hardware‐ based retry mechanism to correct packets that encounter transmission prob‐ lems. This otherwise desirable feature presents a problem for isochrony because it takes time to do it. And how long it takes to resolve an error can vary widely depending on things like how the problem was detected. 

**282** 

**Chapter 7: Quality of Service** 

To decide this question we have to know how much time uncertainty the sys‐ tem can tolerate and still deliver isochronous data. If the latency budget is too tight, there simply won’t be time for retrying failed packets and the ACK/NAK protocol will have to be disabled. Interestingly, the spec writers evidently didn’t consider that possibility because no configuration bits are included for dis‐ abling it or deciding how to handle packets that would have been retried but now won’t be. Therefore disabling this will require non‐standard mechanisms like vendor‐specific registers. 

If there _isn’t_ enough time available for retries, the target agent may simply choose to discard any bad packets. Another option would be to use the bad packets as they are, errors and all. For some applications using isochronous support that isn’t as counter‐intuitive as it sounds. An error in video streaming, for example, might cause an occasional glitch on the display, but that could be considered an acceptable risk. 

If there _is_ enough time in the Service Interval to allow retries, a limit could be placed on the possible latency they might add by adding a timer to track the time until the end of the Service Interval and use that to decide whether a retry could be attempted. Errors shouldn’t happen very often, of course, so this might be sufficient to correct the occasional transmission fault while still maintaining isochronous timing. 

**283** 

**PCI Ex ress Technolo p gy** 

**284** 

## _**8**_ 

## _**Transaction Ordering**_ 

## **The Previous Chapter** 

The previous chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different packets traversing the fabric. These mechanisms include application‐specific software that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **This Chapter** 

This chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock condi‐ tions that must be avoided. 

## **The Next Chapter** 

The next chapter describes, Data Link Layer Packets (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power manage‐ ment, flow control mechanism and can be used for vender defined purposes. 

## **Introduction** 

As with other protocols, PCI Express imposes ordering rules on transactions of the same traffic class (TC) moving through the fabric at the same time. Transac‐ tions with different TCs do not have ordering relationships. The reasons for these ordering rules related to transactions of the same TC include: 

- Maintaining compatibility with legacy buses (PCI, PCI‐X, and AGP). 

- • Ensuring that the completion of transactions is deterministic and in the sequence intended by the programmer. 

**285** 

**PCI Ex ress 3.0 Technolo p gy** 

- Avoiding deadlock conditions. 

- Maximize performance and throughput by minimizing read latencies and managing read and write ordering. 

Implementation of the specific PCI/PCIe transaction ordering is based on the following features: 

1. Producer/Consumer programming model on which the fundamental order‐ ing rules are based. 

2. Relaxed Ordering option that allows an exception to this when the Requester knows that a transaction does not have any dependencies on pre‐ vious transactions. 

3. ID Ordering option that allows a switches to permit requests from one device to move ahead of requests from another device because unrelated threads of execution are being performed by these two devices. 

4. Means for avoiding deadlock conditions and supporting PCI legacy imple‐ mentations. 

## **Definitions**

</td>
<td style="background-color:#e8e8e8">

一个时间片内能发送多少数据?答案当然取决于速度和链路宽度。在 5.0 Gb/s 下,每 2ns 发送一个 10 位符号,因此在 100ns 内每个 Lane 可以传送 50 个符号。如果数据包大小是 512 字节的数据加上另外约 28 字节的头部,则使用 x1 链路需要 11 个时间片来传送一个数据包的 550 个符号。如有需要,可以让一个端口占用多个连续

**279**

## **PCI Ex ress Technolo p gy**

时隙,这就是一种解决方案。由于将发送的数据包大小始终相同,因此我们实际上无法对 2.5 个实例进行编程,因此我们必须使用 3 个。根据我们的等式,3 个 512 字节的实例产生的实际带宽为 120MB/s。这高于我们的需要,但它解决了问题。使用的时间片数将为 11 x 3 = 33,在服务间隔中剩下 95 个用于其他用途。每组 11 个时间片需要是连续的,但这些组可以在服务间隔内间隔开。

另一种解决方案是增加链路宽度。虽然硬件成本会更高,但使用 11 个 Lane 将允许在一个时间片中传送所有数据。CEM 规范目前不支持 x11 选项,但 x12 选项可用,并且适用于我们的示例。使用这样的宽链路意味着软件只需要为每个数据包编程一个时间片,而在整个服务间隔中只需要三个即可支持此设备的等时流量。与 x1 的情况不同,现在我们不需要连续的时间片。相反,它们可以以某种最佳方式在服务间隔内分布。

**带宽分配问题 (Bandwidth Allocation Problems)。** 必须对 TBWRR 表进行编程以保证等时流量的足够及时带宽,并且不允许其他流量进行干扰。在图 7-25 (第 279 页) 中,SCSI 控制器显示为在 SI 1 中发送一个数据包,在 SI 3 中发送另一个。如果时序允许每个 SI 来自该端点的一个数据包,那么这就可以正常工作。

现在假设 SCSI 控制器尝试在 SI 1 中注入超过其权限的数据包,如图 7-26 (第 280 页) 所示。这是规范中提到的两个带宽分配问题中的第一个,称为"过度订阅 (oversubscription)"。这可能会干扰等时流量流,但对 TBWRR 表进行编程可以轻松避免该问题,因为仲裁仅允许来自该端口的数据包在特定时间发送。如果来自该端口的更多数据包排队,则它们必须等待下一个可用时间,这可能在 SI 2 中,如此示例所示。最终,这可能导致发送代理处的流控背压

_Figure 7‐26: 过度订阅带宽_

**==> picture [263 x 94] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = 服务间隔 (Service Interval)<br>SI 1 SI 2 SI 3<br>时间<br>**----- End of picture text -----**<br>


**280**

**第 7 章:服务质量**

第二个时序问题称为"拥塞 (congestion)",发生在给定时间窗口内发送的等时请求过多时,如图 7-27 (第 281 页) 所示。这是一个类似的问题,但现在没有简单的解决方案。与前一种情况不同,将高优先级数据包推迟到另一个时间片不是一种选择,因此系统必须努力处理所有请求。结果是某些请求可能会经历过多的服务延迟。要纠正这一点,软件需要更改数据包的分发,以便它们可以由可用的硬件带宽支持。

_Figure 7‐27: 带宽拥塞_

**==> picture [263 x 102] intentionally omitted <==**

**----- Start of picture text -----**<br>
SI = 服务间隔 (Service Interval)<br>SI 1 SI 2 SI 3<br>时间<br>**----- End of picture text -----**<br>


**延迟问题 (Latency Issues)。** 管理数据包传送的延迟是等时性的重要组成部分,涉及架构延迟和完成者延迟的组合。架构延迟取决于系统中各个组件之间链路的所有特性,尤其是链路宽度和工作频率。最小化此值的一种简单方法是限制等时路径的 PCIe 拓扑的复杂性。完成者延迟取决于目标端点内部特性,例如内存速度和内部仲裁。

## **根复合体 (Root Complex)**

根复合体 (RC) 具有与交换机相同的仲裁和时序要求。它在多个下游端口上接收数据包,并以与前面描述的等时规则一致的方式将它们转发到目标。然而,如何执行此操作的许多细节将是厂商特定的,因为规范没有定义 RC 或应如何对其进行编程。

**问题:窥探 (Snooping)。** 有一个影响根复合体中的时序和延迟的有趣问题我们尚未讨论,即窥探过程。通常,每当对系统内存进行访问时,它将访问处理器认为可缓存的位置,这意味着它有权存储临时副本

**281**

**PCI Ex ress Technolo p gy**

在其本地缓存中。如果外部设备尝试访问该内存区域,则芯片组必须先检查处理器缓存,然后才允许访问,因为缓存的副本可能已被修改。如果是,则需要将修改后的数据写回内存,然后才可用于设备访问。尽管这对于确保内存一致性是必要的,但问题在于窥探需要时间。完成它所需的时间通常是有限的但不可预测的,因为它取决于 CPU 当时正在执行的其他操作。根据时序要求,这种不确定性可能会破坏等时数据流。

**窥探解决方案 (Snooping Solutions)。** 避免窥探的一种方法是让设备仅访问已指定为不可缓存的内存区域。另一种选择是让软件在高优先级数据包头部中设置"No Snoop"属性位。这将强制芯片组跳过窥探步骤,无论内存类型如何,直接访问内存,因为软件已保证这样做不会引起问题。为了将此强制为等时路径的要求,根端口中高优先级 VC 可以由硬件初始化另一位,称为"Reject Snoop Transactions"(请参见第 265 页图 7-17 中的 VC Resource Capability Register)。这样做的目的是仅允许具有 No Snoop 属性集的 VC 事务。任何未设置该位的传入数据包都将被丢弃,以确保时序永远不会因等待窥探而被违反。

## **电源管理 (Power Management)**

这是一个简单的观察,但如果时序对 PCIe 中的路径很重要,则该路径中设备的电源管理 (PM, Power Management) 机制需要谨慎处理。配置软件可以读取与每个 PM 条件关联的延迟,并选择时序预算允许的那些情况。然而,最简单的方法是仅在等时路径中禁用所有 PM 选项。幸运的是,这可以使用现有的配置寄存器轻松完成。设备可以置于设备状态 D0 并保持在那里,而可以禁用硬件控制的链路 PM 机制(有关 PM 的更多信息,请参见第 703 页第 16 章"电源管理")。

## **错误处理 (Error Handling)**

最后,还有一个问题:链路上发生错误时该怎么办。第 7 章中讨论的 ACK/NAK 协议提供了一种基于硬件的自动重试机制,以纠正遇到传输问题的数据包。这个本来很理想的功能对等时性来说带来了一个问题,因为它需要时间。而且解决错误所需的时间可能会有很大差异,这取决于诸如问题是如何被检测到的等因素。

**282**

**第 7 章:服务质量**

要决定这个问题,我们必须知道系统可以容忍多少时间不确定性,仍然能够传送等时数据。如果延迟预算太紧,则根本没有时间重试失败的数据包,必须禁用 ACK/NAK 协议。有趣的是,规范编写者显然没有考虑这种可能性,因为没有包含用于禁用它或决定如何处理将要重试但现在不会重试的数据包的配置位。因此,禁用此功能将需要非标准机制,如厂商特定寄存器。

如果 _没有_ 足够的时间用于重试,则目标代理可以简单地选择丢弃任何错误的数据包。另一种选择是按原样使用错误的数据包,包括错误。对于使用等时支持的某些应用程序来说,这并不像听起来那么违反直觉。例如,视频流中的错误可能导致显示器偶尔出现故障,但这可以被认为是可以接受的风险。

如果服务间隔中 _有_ 足够的时间允许重试,则可以通过添加一个计时器来跟踪距服务间隔结束的时间并使用它来决定是否可以尝试重试,从而限制它们可能增加的潜在延迟。错误当然不应该经常发生,因此这可能足以纠正偶尔的传输故障,同时仍保持等时时序。

**283**

**PCI Ex ress Technolo p gy**

**284**

## _**8**_

## _**事务排序 (Transaction Ordering)**_

## **上一章 (The Previous Chapter)**

上一章讨论了支持服务质量 (Quality of Service) 的机制,并描述了控制穿越架构的不同数据包的时序和带宽的方法。这些机制包括为每个数据包分配优先级值的应用程序特定软件,以及必须内置在每个设备中以实现事务优先级管理的可选硬件。

## **本章 (This Chapter)**

本章讨论 PCI Express 拓扑中事务的排序要求。这些规则继承自 PCI。生产者/消费者 (Producer/Consumer) 编程模型推动了其中的许多规则,因此其机制将在此处描述。原始规则还考虑了必须避免的可能死锁条件。

## **下一章 (The Next Chapter)**

下一章描述数据链路层数据包 (DLLP, Data Link Layer Packets)。我们描述 DLLP 数据包类型的使用、格式和定义,以及它们相关字段的详细信息。DLLP 用于支持 Ack/Nak 协议、电源管理、流控机制,并可用于厂商定义的目的。

## **引言 (Introduction)**

与其他协议一样,PCI Express 对同时通过架构的相同流量类 (TC) 的事务施加排序规则。具有不同 TC 的事务没有排序关系。对相同 TC 的事务使用这些排序规则的原因包括:

- 保持与传统总线 (PCI、PCI-X 和 AGP) 的兼容性。

- 确保事务的完成是确定性的,并按程序员预期的顺序进行。

**285**

**PCI Ex ress 3.0 Technolo p gy**

- 避免死锁条件。

- 通过最小化读延迟和管理读写排序来最大化性能和吞吐量。

特定的 PCI/PCIe 事务排序的实现基于以下特性:

1. 生产者/消费者 (Producer/Consumer) 编程模型,基本排序规则基于此模型。

2. 放宽排序 (Relaxed Ordering) 选项,允许在请求者知道事务不依赖于先前事务时出现例外。

3. ID 排序 (ID Ordering) 选项,允许交换机允许来自一个设备的请求超过来自另一设备的请求,因为这两个设备正在执行不相关的执行线程。

4. 避免死锁条件和支持 PCI 旧版实现的方法。

## **定义 (Definitions)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
