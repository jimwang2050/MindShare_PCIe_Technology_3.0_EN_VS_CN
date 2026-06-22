# 📘 第 20 章　Spec 2.1 修订更新 (Chapter 20. Updates for Spec Revision 2.1)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0347.md` ... `chunks/chunk0347.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [20.1 Updates for Spec Revision 2.1 — Spec 2.1 修订更新](#sec-20-1)

<a id="sec-20-1"></a>
## 20.1 Updates for Spec Revision 2.1 | Spec 2.1 修订更新

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

This change simplifies the Transaction Ordering Table by reducing the number of entries in the table. Essentially, it no longer
distinguishes between comple‐ tions for reads or completions for non‐posted writes. The motivation for this was to reduce the number of
cases that needed to be tested. For more on this, see the section called “The Simplified Ordering Rules Table” on page 288.

# Appendices

</td>
<td width="50%">

最近，业界已融合到 PCIe 作为企业存储和固态驱动器 (SSD) 应用程序的统一互连技术。NVM HCI（一个行业联盟）发布了一个名为 NVM Express (NVMe) 的规范，该规范使用 PCIe 提供 SSD 应用程序所需的带宽。此外，T10 委员会已开始定义 SCSI
over PCIe (SOP) 协议，以利用 PCIe 技术能力实现高性能存储应用程序。此外，SATA 联盟最近宣布将 PCIe 用作其下一代 SATA 规范（称为 SATA Express (SATAe)）的互连。

</td>
</tr>
<tr>
<td width="50%">

## _**Appendix A:**_

</td>
<td width="50%">

## **服务器 SSD 模块中的 PCIe**

传统上，企业 SSD 模块附带 SAS、SATA 和光纤通道接口，但由于上述发展，大多数 SSD 控制器、模块和系统供应商已推出具有 PCIe 接口的产品。由于管理闪存的繁重负载，大多数 SSD 控制器达到其性能和容量峰值。在高性能应用程序中，使用多个 SSD 控制器（或
ASIC）并通过 PCIe 交换机聚合。图 0-4（在第 941 页）显示了 PCIe 交换机在 SSD 附加卡中的基本用法，该用法适用于任何卡或模块形态因素。

**第 : 附录 B：PCI 的市场与应用**

_图 0-4：SSD 附加卡中的 PCIe 交换机应用程序_

对于大型数据中心应用程序，SSD 附加卡安装在服务器主板中，如图 0-5（在第 941 页）以及通过 PCIe 交换机聚合的 IO 扩展框（图 6）所示。在服务器主板设计中，PCIe 交换机用于创建更多端口/插槽，以适应其他 SSD 模块以支持应用程序的需求。

_图 0-5：服务器主板使用 PCIe 交换机_

除提供连接外，PCIe 交换机还可用于通过 NT 桥接和 MR 功能提供冗余和故障转移。MR 交换机支持 1+N 故障转移能力，其中一个服务器/主机与 N 个服务器通信以检查心跳并在其中一个发生故障时启动故障转移。图 0-6（在第 942 页）中所示的服务器之一可以在 1+N
故障转移方案中用作其他服务器的备份。

_图 0-6：1+N 故障转移方案中的服务器故障转移_

</td>
</tr>
<tr>
<td width="50%">

## _**Debugging PCIe Traffic with LeCroy Tools**_

</td>
<td width="50%">

## **结论**

PCIe 互连技术已成为超越芯片到芯片互连的许多高端应用程序的有力竞争者，并有望用于外部 I/O 共享、服务器集群、I/O 扩展和 TOR 交换。当前的 8 GT/s 和下一代 (Gen4) 16 GT/s
线路速率、在单个高带宽端口中聚合多个通道的能力、故障转移能力、用于数据传输的嵌入式 DMA 以及 IO 共享/虚拟化提供了至少等于（如果不优于）InfiniBand 和以太网等接口的能力。

</td>
</tr>
<tr>
<td width="50%">

## Christoper Webb, LeCroy Corporation

</td>
<td width="50%">

## _**附录 C：**_

_**使用 PCI Express 技术实现智能适配器和多主机系统**_

</td>
</tr>
<tr>
<td width="50%">

## **Overview** 

The transition of IO bus architecture from PCI to PCI Express had a large impact on developers with respect to types of tools required for
validation and debug.

With parallel buses such as PCI, a waveform view of the signals shows enough information for the developer to interpret the state of the
bus. A user could visually examine a waveform and mentally decode the type of transactions, how much data is transferred, and even the
content of that transfer.

Since PCI Express packet traffic is both encoded and scrambled, examining a waveform view of the traffic provides very little information
about the state of the link. The speed of the link can be inferred from the width of the bit times, and the width of the link can be
inferred by the number of active lanes. How‐ ever, the user cannot visually interpret the symbol alignment, let alone the packets
themselves.

A new class of tools evolved to help developers visualize the state of their now serial links. These tools perform the de‐serialization,
decoding, and de‐scram‐ bling for the users. At first glance this would seem to be enough for the devel‐ oper. But for PCI Express
specifically, other complications such as flow control credits, lane‐to‐lane skew, polarity inversion, and lane reversal must also be
comprehended by these tools as part of understanding PCIe protocol.

Both pre‐ and post‐silicon debug share a common need for tools. In this appen‐ dix chapter, we describe some of the product offerings
available for debugging PCI Express interconnects, both from a pre and post silicon perspective.

</td>
<td width="50%">

## **Jack Regula、Danny Chi、Tim Canepa（PLX Technology, Inc.）**

</td>
</tr>
<tr>
<td width="50%">

## **Pre-silicon Debugging**

</td>
<td width="50%">

## **简介**

智能适配器、主机故障转移机制和多处理器系统是当今常见的三种使用模型，并有望随着下一代系统的市场需求变得更加普遍。尽管每个模型都是为了响应完全不同的市场需求而开发的，但它们都有一个共同的要求，即利用它们的系统需要在系统内共存多个处理器。本附录概述了 PCI Express
如何通过非透明桥接 (non-transparent bridging) 来满足这些需求。

由于使用智能适配器、主机故障转移和多主机技术的系统的广泛普及，PCI Express 硅供应商必须提供一种支持它们的手段。这实际上是一项相对低风险的努力；鉴于 PCI Express 与 PCI 软件兼容，而 PCI 系统早已实现了分布式处理。最明显的方法，也是 PLX
所倡导的方法，是为 PCI Express 模拟 PCI 空间中使用最广泛的实现。此策略允许系统设计人员不仅使用熟悉的实现，而且使用经过验证的方法，

并在他们从 PCI 迁移到 PCI Express 时可以提供重要的软件重用。本白皮书概述了多处理器 PCI Express 系统将如何使用 PCI 范例中建立的行业标准实践来实现。但是，首先，我们将定义不同的使用模型，并回顾 PCI
社区为满足这些需求而开发机制的成功努力。最后，我们将介绍 PCI Express 系统如何利用非透明桥接来为这些类型的系统提供所需的功能。

</td>
</tr>
<tr>
<td width="50%">

## **RTL Simulation Perspective** 

In RTL simulation, looking at a waveform view of an FPGA or an ASIC signal is the most common way to debug. By showing internal state
machine states, monitoring IO as it moves through the device, or seeing the state of control sig‐ nals; a waveform view is quite powerful.
But, as we discussed above, a PCI express link is not understandable when shown as a waveform. Additional pro‐ cessing or decoding must be
done to make sense of this new link. To augment the simulation tools, a PCI Express Bus Monitor is typically added to address this need.

</td>
<td width="50%">

## **使用模型**

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express RTL Bus Monitor** 

A PCI Express Bus monitor is a piece of code which users insert in their RTL simulation to help monitor the state of their PCIe link. At
minimum, this moni‐ tor will output text based log files with information about link state changes and types of packet activity. More
complex monitors will perform real time compliance checking. A number of vendors provide purchasable IP which per‐ form this exact function.
The emphasis however is typically on compliance. Less functionality is provided with respect to visualization of things such as flow control
credits, link utilization, or link training debug.

</td>
<td width="50%">

## **智能适配器**

智能适配器通常是使用本地处理器来减轻主机任务的外围设备。智能适配器的示例包括 RAID 控制器、调制解调器卡以及执行安全和流处理等任务的内容处理刀片。通常，这些任务要么计算繁重，要么如果由主机执行则需要大量 I/O
带宽。通过向端点添加本地处理器，系统设计人员可以享受显著的增量性能。在 RAID 市场中，大量产品利用本地智能进行 I/O 处理。

智能适配器的另一个示例是电子商务刀片。由于通用主机处理器未针对 SSL 所需的对数数学进行优化，因此利用主机处理器执行 SSL 握手通常会将系统性能降低 90% 以上。此外，SSL 握手操作的要求之一是真正的随机数生成器。许多通用处理器没有此功能，因此实际上没有专用硬件就很难执行
SSL 握手。类似的示例在整个智能适配器市场中比比皆是；事实上，这种使用模型非常普遍，以至于对于许多应用程序来说，它已成为事实上的标准实现。

</td>
</tr>
<tr>
<td width="50%">

## **RTL vector export to PETracer Application** 

LeCroy has partnered with a number of the leading PCIe verification IP vendors to create tools to further enhance the visualization and
analysis of pre‐silicon PCIe traffic. This involves using the vendors Bus Monitor to export raw symbol traffic into the same PETracer
application used by the dedicated PCIe Analyzer hardware. SimPASS PE is LeCroy’s solution to supporting this export.

More information about LeCroy’s PETracer application and its features are described in the section “As a last resort, a flying lead probe
shown in Figure 5 on page 924 may be used to attach the protocol analyzer to the system under test. This involves soldering a resistive tap
circuit and connector pins to the PCIe traces. This circuitry is typically soldered to the AC coupling caps of the PCIe link as they are
often the only place to access the traces. Once the probe cir‐

**A endix A pp** 

cuitry is soldered to the PCB, the analyzer probe can be connected and removed as needed. This approach can be used on virtually any PCIe
link, however the robustness of the connection is limited by the skill of the technician adding the probe.” on page 924.

</td>
<td width="50%">

## **主机故障转移**

主机故障转移能力被设计到需要高可用性的系统中。高可用性已成为越来越重要的要求，尤其是在存储和通信平台中。确保整个系统保持运行状态的实际方法是提供冗余

**第 : 附录 C：实现智能适配**

对于所有组件。主机故障转移系统通常包括一个基于主机的系统，该系统连接到多个端点。此外，备份主机连接到系统并被配置为监视系统状态。当主主机发生故障时，备份主机处理器不仅必须识别故障，然后采取措施承担主要控制，移除失败的主机以防止进一步的破坏，重建系统状态，并在不丢失任何数据的情况下继续系统的运行。

</td>
</tr>
<tr>
<td width="50%">

## **Post-Silicon Debug**

</td>
<td width="50%">

## **多处理器系统**

多处理器系统通过允许多个计算引擎同时处理复杂问题的各个部分来提供更大的处理带宽。与利用主机故障转移的系统不同，其中备份处理器基本上是空闲的，多处理器系统利用所有引擎来提高计算吞吐量。这使得系统能够实现仅使用单个主机处理器无法实现的性能水平。多处理器系统通常由两个或多个完整的子系统组成，这些子系统可以通过特殊互连彼此传递数据。多主机系统的一个很好的示例是刀片服务器机箱。每个刀片都是一个完整的子系统，通常配备有自己的
CPU、直连存储和 I/O。

</td>
</tr>
<tr>
<td width="50%">

## **Oscilloscope** 

Use of an oscilloscope for debugging a PCIe link is typically focused on the elec‐ trical validation of the link. The most common usage is
examining an eye pat‐ tern with a mask overlay for determining electrical compliance. A lesser known compliance check is to examine the
entry and exit of electrical idle state to see if the link goes to the common mode voltage within the required time periods after an
electrical idle ordered set is transmitted. These are 2 examples of PCIe compliance checking which are best performed using an oscilloscope
such as shown in Figure 1 on page 920.

With the addition of dynamic link training for 8.0 GT/s operation, devices must now train the transmitter emphasis during the Recovery.EQ
LTSSM sub‐state. The goal is to set the transmitter EQ to provide the best signal eye to the receiver. Monitoring this dynamic equalization
process is another example where the use of an oscilloscope is quite powerful. With a real time oscilloscope, the user can capture this
process and see the impact on the waveform as trans‐ mitter settings are changed. This allows the user to verify that the transmitter is
indeed acting on the coefficient change requests, but it also allows the user to determine if the receiver has properly chosen the correct
setting.

For logical debug of the link, the oscilloscope is most useful when the link is x1 or x2 as you are limited by the number channels the scope
can acquire. The first method of examining PCIe traffic is a waveform view. As with the RTL wave‐ form viewer, there is little to understand
about the state of the link without SW help to perform 8b/10b decoding and de‐scrambling. Fortunately, more advanced oscilloscopes have SW
packages that perform these duties. For this to work properly, the scope must have deep capture buffers and must see the SKIP ordered sets
so that they can decipher the byte alignment and synchronize the de‐scrambler LFSR.

The LeCroy Oscilloscope can overlay PCIe symbols right onto the waveform for enhanced visibility of the traffic. An additional text based
listing of the packet symbols can be displayed on the screen as an additional method of examining the waveform.

</td>
<td width="50%">

## **使用 PCI 的多处理器实现的历史**

为了更好地理解为 PCI Express 提出的实现，首先需要了解 PCI 实现。

PCI 最初于 1992 年为个人计算机定义。由于当时 PC 的性质，协议架构师没有预料到对多处理器的需求。因此，他们设计系统时假设主机处理器将枚举整个内存空间。显然，如果添加另一个处理器，系统操作将失败，因为两个处理器都将尝试为系统请求提供服务。

随后发明了几种方法以适应使用 PCI 的多处理器功能要求。最流行的实现，也是本文针对 PCI Express 讨论的实现，是使用处理子系统之间的非透明桥接来隔离它们的内存空间。[1]

由于主机在首次上电或复位时不知道系统拓扑，因此它必须执行发现以了解存在的设备，然后将它们映射到内存空间中。为了支持标准发现和配置软件，PCI 规范定义了合规设备的控制和状态寄存器 (CSR) 的标准格式。标准 PCI-to-PCI 桥 CSR 头，称为 Type 1
头，包括主桥、次桥和从属总线号寄存器，当主机写入这些寄存器时，它们定义了桥另一侧设备的 CSR 地址。采用 Type 1 CSR 头的桥称为透明桥。

Type 0 头用于端点。Type 0 CSR 头包括用于从主机请求内存或 I/O 孔径的基地址寄存器 (BAR)。Type 1 和 Type 0 头都包括类代码寄存器，用于指示表示哪种桥或端点，并可在子类字段以及设备 ID 和供应商 ID 寄存器中获得更多信息。CSR
头格式和寻址规则允许处理器搜索 PCI 层次结构的所有分支，从主机桥向下到每个叶节点，读取它找到的每个设备的类代码寄存器，并在发现 PCI-to-PCI 桥时相应地分配总线号。发现完成后，主机知道哪些设备存在以及每个设备运行所需的内存和 I/O 空间。这些概念如图 C-0-1
所示。

1. 除非另有明确说明，使用 PCI 和 PCI Express 的多处理器系统的架构是相似的，可以互换使用。

**第 : 附录 C：实现智能适配**

_图 0-1：使用透明桥的枚举_

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

LeCroy recently announced a SW package called ProtoSync for their oscillo‐ scope line which allows the user to export the captured waveform
into the PETracer application. This is the same SW package that the protocol analyzer uses which includes a wide range of post processing
capabilities described below. The PETracer software can run independently on the scope hardware, often on a second monitor. This allows time
correlated comparison of the physi‐ cal layer data presented by the scope waveform alongside the logic layer pre‐ sentation of data
presented by the PETracer software.

Capture of the 8.0 GT/s dynamic link equalization on the oscilloscope and exporting this traffic to the PETracer application is a prime
example where this solution is most powerful. The user can navigate PETracer to the link training packet where the TX coefficient change
request has been sent, then identify where this coefficient change was applied in the scope SW. The user can then measure the time it takes
for the coefficient change to be applied and compare this to the timing required in the PCIe spec.

_Figure A‐1: LeCroy Oscilloscope with ProtoSync Software Option_

</td>
<td width="50%">

## **在 PCI Express 基础系统中实现多主机/智能适配器**

到目前为止，我们的讨论仅限于一个具有一个内存空间的处理器。随着技术的发展，系统设计人员开始开发具有内置本地处理器的端点。这导致的问题是，主机处理器和智能适配器在上电或复位时都会尝试枚举整个系统，从而导致系统冲突，最终导致系统无法运行。[1]

1. 虽然我们使用智能端点作为示例，但我们应注意多主机系统也存在类似的问题。

</td>
</tr>
<tr>
<td width="50%">

## **Protocol Analyzer** 

A growing trend in debugging PCIe links is to use a dedicated protocol analysis tool. What separates a protocol analyzer from a logic
analyzer is that it is built to support a specific protocol such as PCIe. From a hardware perspective, a PCIe protocol analyzer is optimized
for acquiring and storing PCIe traffic. This starts from the dedicated PCIe interposer probes, continues to the cabling choice, and caries
through into the internal hardware components. For recover‐ ing PCIe traffic, specialized clock and data recovery circuits are used which
can handle the electrical idle transitions, spread spectrum modulation, as well as

**A endix A pp** 

handle the run lengths found in 128b/130b encoding. Sophisticated equalization circuits are used to recover the signal eye prior to
deserialization. Without com‐ prehending the complexities of PCIe recovery, the Analyzer hardware would not be optimized for recovering
complex traffic such as speed switching, dynamic link widths, and low power states such as L0s.

In addition to choosing appropriate hardware components for recovering PCIe traffic, a protocol analyzer includes logic circuitry which is
PCIe specific. This logic must infer the state of the PCIe link and follow it during various LTSSM state changes. Once the link state is
being properly followed, dedicated packet inspection circuits perform data matching against incoming packets to look for events programmed
by the user. These matchers are used for filtering of traffic as well as performing the trigger functionality needed for stopping the
traffic capture. A mixture of these traffic filters as well as deep trace buffers (often 4GB to 8GB in size) allow the user to capture
significantly longer traffic scenarios than would be possible without a protocol analyzer.

Finally, the most important piece of a protocol analyzer is the software GUI. By optimizing the traffic views, post processing reports, and
hardware controls with a dedicated PCI Express software tool; a very comprehensive set of PCI express specific analysis can be performed.

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **Logic Analyzer** 

Some logic analyzers offer PCIe specific software packages. This software will read the PCI express capture from the logic analyzer hardware
and perform some amount of post processing of this data. This analysis includes the basics such as decoding, de‐scrambling, and decoding of
the traffic. These SW tools do not perform many of the rich post processing features offered by dedicated pro‐ tocol analyzer software,
however.

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **Using a Protocol Analyzer Probing Option** 

To record your PCIe traffic you must first find the best method for probing it. PCIe started as an add‐in card form factor for desktop PC’s
and servers, but has since proliferated into a dizzying array of standard and non‐standard form fac‐ tors. For the standard form factors,
the best probe option is a dedicated inter‐ poser.

An Interposer is a dedicated piece of hardware which includes probe circuitry required for passing a copy of the PCIe traffic to the
Analyzer hardware for cap‐ ture and analysis. These interposers are designed specifically for the mechanical

</td>
<td width="50%">

</td>
</tr>
<tr>
<td width="50%">

## **PCI Express Technology** 

and electrical environments for which they are placed. The most common inter‐ poser is a “Slot Interposer” such as shown in Figure 2 on page
922. This inter‐ poser is used for probing standard CEM compliant PCIe add‐in cards.

</td>
<td width="50%">

</td>
</tr>

</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`


<img src="figures/embedded/page0960_img1_tight.png" alt="Figure from page 960" width="700">

