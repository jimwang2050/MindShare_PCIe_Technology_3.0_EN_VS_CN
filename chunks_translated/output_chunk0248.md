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
