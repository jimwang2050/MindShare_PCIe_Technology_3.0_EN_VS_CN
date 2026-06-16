事务排序在虚通道缓冲区中进行管理。这些缓冲区被分组为 Posted、Non-Posted 和 Completion 事务，并且每个组独立管理流控。这使得弱排序更有用，因为与我们的示例一样，即使一个缓冲区已满，其他缓冲区仍可能有可用空间。

## **基于 ID 的排序 (IDO)**

另一个优化排序和提升性能的机会与流量流的性质相关。不同 Requester 的报文很可能没有依赖关系；毕竟，一个设备几乎不可能知道另一个设备何时完成了某些步骤（基于排序），因为它们到达其共享资源可能有不同的路径。考虑到这一点，PCIe 规范的 2.1 版本引入了所谓的基于 ID 的排序 (ID-based Ordering) 以提升性能。

## **解决方案**

如果不考虑事务排序的报文源，则性能可能会受到影响，如第 302 页的图 8-7 所示。在该图中，事务 1 设法到达交换机的上游端口，但由于根端口中该报文类型的缓冲区已满（这将由流控信用不足指示）而无法进一步进展。使用规范术语，来自同一 Requester 的报文称为 TLP 流 (TLP stream)。在此示例中，事务 1 所示的路径可能包括作为 TLP 流一部分的几个 TLP。然后事务 2 到达同一出口端口，也被阻止向前移动，因为它必须与事务 1 保持顺序。由于报文来自不同的源（不同的 TLP 流），这种延迟几乎肯定是不必要的；它们之间很可能没有依赖关系，但普通的排序模型没有考虑到这一点。为了获得更好的性能，我们需要另一个选项。

解决方案很简单：如果报文不使用相同的 Requester ID（或完成报文的 Completer ID），则允许重排序报文。此可选功能允许软件启用设备以使用 IDO，并且交换机端口可以识别报文属于不同的 TLP 流。这是通过在 Device Control 2 Register 中设置启用位来完成的。

**301**

**PCI Exress 3.0 Technology**

_图 8-7：不同来源不太可能有依赖关系_

**==> 图片 [151 x 145] 已省略 <==**

**----- 图片文字开始 -----**<br>
Write Buffer Root<br>Full<br>ey<br>Switch<br>ty a ONO<br>®<br>Posted Write<br>| [7] [le ma"<br>sd Cle fl PCle ff Legacy<br>**----- 图片文字结束 -----**<br>


## **何时使用 IDO**

规范强烈建议只要安全可行，就同时使用 IDO 和 RO。例如，当端点仅与一个其他实体（例如根复合体）直接通信时，对所有 TLP 使用 IDO 应该是安全的。另一方面，如果端点正在与多个代理通信，则使用它就不安全了。规范中此失败情况的一个示例开始于一个设备执行对内存的 DMA 写，然后执行对另一设备中标志 (flag) 的对等 (peer-to-peer) 写。当第二个设备收到标志时，它也会启动对同一内存区域的 DMA 写。通常，两个 DMA 操作会保持顺序，但使用 IDO 时，由于上游设备将它们视为来自不同的设备 ID，因此无法保证该排序。类似地，将 RO 用于涉及控制流量的报文也是不安全的。

对于 Completer，如果启用了 IDO，则建议将其用于所有 Completions，除非有特定原因不这样做。

**302**

**第 8 章：事务排序**

## **软件控制**

软件可以通过在端口的 Device Control 2 Register 中设置适当的位来启用 IDO 用于来自给定端口的请求或完成。与 RO 一样，没有能力位 (capability bits) 让软件查明设备支持什么，只有启用位，因此软件需要通过其他方式知道设备能够执行此操作。这些位启用了该报文类型对 IDO 的使用，但软件仍必须决定每个单独的报文是否会设置其 IDO 位。头部中的新属性位指示 TLP 是否正在使用 IDO，如第 303 页的图 8-8 所示。这引出了另一个相关的点：Completions 通常会继承生成它们的 Request 的所有属性位，但对于 IDO 来说情况可能并非如此，因为这可以由 Completer 独立启用。换句话说，Completions 可能会使用 IDO，即使发起它们的 Request 没有使用。

_图 8-8：64 位头部中的 IDO 属性_

**==> 图片 [313 x 127] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- 图片文字结束 -----**<br>


## **死锁避免**

由于 PCI 总线使用延迟事务，或者由于 PCI Express 内存读请求可能因流控信用不足而被阻塞，可能会出现多种死锁场景。这些死锁避免规则包含在 PCI Express 排序中，以确保无论拓扑如何都不会发生死锁。遵守排序规则可以防止由于意外拓扑（例如跨 PCI Express 交换网络连接的两个 PCI Express 到 PCI 桥）而出现的边界条件问题。请参考 MindShare 出版的标题为《_PCI System Architecture, Fourth Edition_》（由 Addison-Wesley 出版）的书，获取构成 PCI Express 死锁避免相关排序规则基础的场景的详细说明

**303**

## **PCI Exress 3.0 Technology**

排序规则。表 8-1（第 289 页）列出了死锁避免排序规则，这些规则被标识为 A3、A4、D3、D4 和 A5b 条目。请注意，避免死锁涉及这 5 种情况中的每一种的"Yes"条目。如果由于与第 3 列或第 4 列中标识的 Non-Posted 请求缓冲区相关的流控信用不足而发生阻塞，则与行 A 关联的 Posted 请求或与行 D 关联的 Completions 必须移到第 3 列或第 4 列中指定存在"Yes"条目的 Non-Posted 请求之前。另请注意，A5b 中的"Yes"条目仅适用于 PCI Express 到 PCI 或 PCI-X 桥。

基本上，此死锁避免规则可以总结为"必须允许后到达的内存写请求或完成通过先前被阻塞的 Non-Posted 请求，否则可能导致死锁"。

**304**

## 第三部分：

数据链路层

## _**9**_

## _**DLLP 元素**_

## **上一章**

上一章讨论了 PCI Express 拓扑中事务的排序要求。这些规则是从 PCI 继承而来的，生产者/消费者编程模型激发了其中的许多规则，因此此处描述了其机制。原始规则还考虑了必须避免的可能死锁条件，但不包括避免可能导致的性能问题的任何手段。

## **本章**

在本章中，我们描述另一类主要的数据包——数据链路层包 (Data Link Layer Packets, DLLP)。我们描述 DLLP 报文类型的使用、格式和定义以及其相关字段的详细信息。DLLP 用于支持 Ack/Nak 协议、电源管理、流控机制，甚至可以用于供应商自定义目的。

## **下一章**

下一章描述数据链路层的一个关键特性：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。Ack DLLP 确认 TLP 的良好接收，而 Nak DLLP 指示传输错误。我们将描述在未检测到 TLP 或 DLLP 错误时的正常操作规则，以及与 TLP 和 DLLP 错误相关联的错误恢复机制。

## **概述**

数据链路层可以被认为管理着较低级别的链路协议。它的主要职责是确保在设备之间移动的 TLP 的完整性，但它也参与 TLP 流控、链路初始化和电源管理，并在其上方的传输层和下方的物理层之间传递信息。

**307**

**PCI Exress Technology**

在执行这些工作时，数据链路层与被称为数据链路层包 (Data Link Layer Packets, DLLP) 的邻居交换包。DLLP 在每个设备的数据链路层之间进行通信。第 308 页的图 9-1 说明了设备之间交换的 DLLP。

_图 9-1：数据链路层发送 DLLP_

**==> 图片 [342 x 298] 已省略 <==**

**----- 图片文字开始 -----**<br>
PCIe Device A PCIe Device B<br>
Device Core Device Core<br>
PCIe Core  PCIe Core<br>
Hardware/Software Hardware/Software<br>
Interface Interface<br>
Transaction Layer Transaction Layer<br>
Data Link Layer Data Link Layer<br>
Physical Layer Physical Layer<br>
(RX) (TX) (RX) (TX)<br>
Framing C Framing<br>
DLLP R<br>
(SDP) C (END)<br>
**----- 图片文字结束 -----**<br>


## **DLLP 是本地流量**

DLLP 具有简单的报文格式，固定大小为 8 字节，包括成帧字节。与 TLP 不同，它们不携带目标或路由信息，因为它们仅用于最近邻通信，根本不被路由。事务层也看不到它们，因为它们不属于在该层交换的信息。

**308**

**第 9 章：DLLP 元素**

## **DLLP 的接收方处理**

收到 DLLP 时，有几条规则适用：

1. 它们在接收方立即被处理。换句话说，它们的流不能像 TLP 那样被控制（DLLP 不受流控影响）。

2. 检查它们是否有错误；首先在物理层，然后是数据链路层。通过计算 CRC 应该是什么并将其与接收到的值进行比较来检查随包附带的 16 位 CRC。未能通过此检查的 DLLP 将被丢弃。链路将如何从此错误中恢复？DLLP 仍会定期到达，该类型的下一个成功的 DLLP 将更新丢失的信息。

3. 与 TLP 不同，DLLP 没有确认协议。相反，规范定义了超时机制以促进从失败的 DLLP 中恢复。

4. 如果没有错误，则确定 DLLP 类型并传递给适当的内部逻辑进行管理：

   - Ack/Nak 通知 TLP 状态

   - 流控通知可用缓冲区空间

   - 电源管理设置

   - 供应商特定信息

## **发送 DLLP**

## **概述**

这些报文源自数据链路层，并传递给物理层。如果使用 8b/10b 编码（Gen1 和 Gen2 模式），将在 DLLP 的两端添加成帧符号，然后再发送包。在 Gen3 模式下，两个字节的 SDP 标记被添加到 DLLP 的前端，但不添加 END 添加到 DLLP 的末尾。第 310 页的图 9-2 显示了一个传输中的通用（Gen1/Gen2）DLLP，显示了成帧符号和包的常规内容。

**309**

**PCI Exress Technology**

_图 9-2：通用数据链路层包格式_

**==> 图片 [360 x 313] 已省略 <==**

**----- 图片文字开始 -----**<br>
Device A Device B<br>
Device Core Device Core<br>
PCI-XP Core  PCI-XP Core<br>
Hardware/Software Hardware/Software<br>
Interface Interface<br>
Transaction Layer Transaction Layer<br>
Data Link Layer Data Link Layer<br>
Physical Layer Physical Layer<br>
(RX) (TX) (RX) (TX)<br>
Framing C Framing<br>
DLLP R<br>
(SDP) C (END)<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
Byte 0 DLLP Type (Fields Vary With DLLP Type)<br>
Byte 4 16 Bit CRC<br>
**----- 图片文字结束 -----**<br>
