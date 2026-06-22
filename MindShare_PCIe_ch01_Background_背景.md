# 📘 第 1 章　背景 (Chapter 1. Background)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0091.md` ... `chunks/chunk0112.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [1.1 Background — 背景](#sec-1-1)
- [1.2 Background — 背景](#sec-1-2)
- [1.3 Background — 背景](#sec-1-3)
- [1.4 Background — 背景](#sec-1-4)
- [1.5 Background — 背景](#sec-1-5)
- [1.6 Background — 背景](#sec-1-6)
- [1.7 Background — 背景](#sec-1-7)
- [1.8 Background — 背景](#sec-1-8)
- [1.9 Background — 背景](#sec-1-9)
- [1.10 Background — 背景](#sec-1-10)
- [1.11 Background — 背景](#sec-1-11)
- [1.12 Background — 背景](#sec-1-12)
- [1.13 Background — 背景](#sec-1-13)
- [1.14 Background — 背景](#sec-1-14)
- [1.15 Background — 背景](#sec-1-15)
- [1.16 Background — 背景](#sec-1-16)
- [1.17 Background — 背景](#sec-1-17)
- [1.18 Background — 背景](#sec-1-18)
- [1.19 Background — 背景](#sec-1-19)
- [1.20 Background — 背景](#sec-1-20)
- [1.21 Background — 背景](#sec-1-21)
- [1.22 Background — 背景](#sec-1-22)

<a id="sec-1-1"></a>
## 1.1 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## Part One: 

The Big Picture 

_**1 Background**_

</td>
<td width="50%">

## 第一部分：

总体概览

_**1 背景**_

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<a id="sec-1-2"></a>
## 1.2 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **This Chapter** 

This chapter reviews the PCI (Peripheral Component Interface) bus models that preceded PCI Express (PCIe) as a way of building a foundation
for understand‐ ing PCI Express architecture. PCI and PCI‐X (PCI‐eXtended) are introduced and their basic features and characteristics are
described, followed by a discussion of the motivation for migrating from those earlier parallel bus models to the serial bus model used by
PCIe.

</td>
<td width="50%">

## **本章** 

本章回顾了 PCI Express（PCIe）之前作为前代总线模型的 PCI（外围组件接口）总线模型，以此为理解 PCI Express 架构奠定基础。本章将介绍 PCI 和
PCI-X（PCI-eXtended），并描述它们的基本特性和特点，随后讨论从这些早期的并行总线模型迁移到 PCIe 所采用的串行总线模型的动机。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/page/page0082.png" alt="Figure from page 82" width="700">

<a id="sec-1-3"></a>
## 1.3 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **The Next Chapter** 

The next chapter provides an introduction to the PCI Express architecture and is intended to serve as an “executive level” overview,
covering all the basics of the architecture at a high level. It introduces the layered approach to PCIe port design given in the spec and
describes the responsibilities of each layer.

</td>
<td width="50%">

## **下一章**

下一章将介绍 PCI Express 架构，旨在作为一份“管理层”级别的概览，从高层次覆盖该架构的所有基础知识。它将介绍规范中给出的 PCIe 端口设计的分层方法，并描述每一层的职责。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-4"></a>
## 1.4 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Introduction** 

Establishing a solid foundation in the technologies on which PCIe is built is a helpful first step to understanding it, and an overview of
those architectures is presented here. Readers already familiar with PCI may prefer to skip to the next chapter. This background is only
intended as a brief overview. For more depth and detail on PCI and PCI‐X, please refer to MindShare’s books: PCI System Architecture, and
PCI‐X System Architecture.

As an example of how this background can be helpful, the software used for PCIe remains much the same as it was for PCI. Maintaining this
backward com‐ patibility encourages migration from the older designs to the new by making the software changes as simple and inexpensive as
possible. As a result, older PCI software works unchanged in a PCIe system and new software will con‐ tinue to use the same models of
operation. For this reason and others, under‐ standing PCI and its models of operation will facilitate an understanding of PCIe.

**9**

</td>
<td width="50%">

## **简介** 

在 PCIe 所基于的各项技术之上建立扎实的基础,是理解 PCIe 的一个有益的第一步,本节将对这些架构进行概述。已经熟悉 PCI 的读者可以跳过本章直接进入下一章。本背景内容仅作为简要概述。如果希望深入了解 PCI 和 PCI‐X 的更多细节,请参阅 MindShare
的书籍: 《PCI System Architecture》和《PCI‐X System Architecture》。

举一个能够体现这些背景知识作用的例子:PCIe 所使用的软件与 PCI 时代基本相同。保持这种向后兼容性,可以通过使软件变更尽可能简单和廉价,从而鼓励从旧设计向新设计的迁移。因此,旧版 PCI 软件可以在 PCIe
系统中无需修改地运行,而新软件也将继续沿用相同的操作模型。出于这一原因及其他原因,理解 PCI 及其操作模型将有助于理解 PCIe。

**9**

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-5"></a>
## 1.5 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI and PCI-X** 

The PCI (Peripheral Component Interface) bus was developed in the early 1990’s to address the shortcomings of the peripheral buses that were
used in PCs (personal computers) at the time. The standard at the time was IBM’s AT (Advanced Technology) bus, referred to by other vendors
as the ISA (Industry Standard Architecture) bus. ISA had been sufficient for the 286 16‐bit machines for which it was designed, but
additional bandwidth and improved capabilities, such plug‐and‐play, were needed for the newer 32‐bit machines and their peripherals. Besides
that, ISA used big connectors that had a high pin count. PC vendors recognized the need for a change and several alternate bus designs were
proposed, such as IBM’s MCA (Micro‐Channel Architecture), the EISA bus (Extended ISA, proposed as an open standard by IBM competitors), and
the VESA bus (Video Electronics Standards Association, proposed by video card vendors for video devices). However, all of these designs had
drawbacks that prevented wide acceptance. Eventually, PCI was developed as an open standard by a consortium of major players in the PC
market who formed a group called the PCISIG (PCI Special Interest Group). The performance of the newly‐devel‐ oped bus architecture was much
higher than ISA, and it also defined a new set of registers within each device referred to as configuration space. These regis‐ ters allowed
software to see the memory and IO resources a device needed and assign each device addresses that wouldn’t conflict with other addresses in
the system. These features: open design, high speed, and software visibility and control, helped PCI overcome the obstacles that had limited
ISA and other buses PCI quickly became the standard peripheral bus in PCs.

A few years later, PCI‐X (PCI‐eXtended) was developed as a logical extension of the PCI architecture and improved the performance of the bus
quite a bit. We’ll discuss the changes a little later, but a major design goal for PCI‐X was main‐ taining compatibility with PCI devices,
both in hardware and software, to make migration from PCI as simple as possible. Later, the PCI‐X 2.0 revision added even higher speeds,
achieving a raw data rate of up to 4 GB/s. Since PCI‐X main‐ tained hardware backward compatibility with PCI, it remained a parallel bus and
inherited the problems associated with that model. That’s interesting for us because parallel buses eventually reach a practical ceiling on
effective band‐ width and can’t readily be made to go faster. Going to a higher data rate with PCI‐X was explored by the PCISIG, but the
effort was eventually abandoned. That speed ceiling, along with a high pin count, motivated the transition away from the parallel bus model
to the new serial bus model.

These earlier bus definitions are listed in Table 1‐1 on page 11, which shows the development over time of higher frequencies and
bandwidths. One of the inter‐

esting things to note in this table is the correlation of clock frequency and the number of add‐in card slots on the bus. This was due to
PCI’s low‐power signal‐ ing model, which meant that higher frequencies required shorter traces and fewer loads on the bus (see
“Reflected‐Wave Signaling” on page 16). Another point of interest is that, as the clock frequency increases, the number of devices permitted
on the shared bus decreases. When PCI‐X 2.0 was introduced, its high speed mandated that the bus become a point‐to‐point interconnect.

_Table 1‐1: Comparison of Bus Frequency, Bandwidth and Number of Slots_ 

|**Bus Type**|**Clock Frequency**|**Peak Bandwidth** **32‐bit ‐ 64‐bit ...|**Number of Card** **Slots per Bus**|
|---|---|---|---|
|PCI|33 MHz|133 ‐ 266 MB/s|4‐5|
|PCI|66 MHz|266 ‐ 533 MB/s|1‐2|
|PCI‐X 1.0|66 MHz|266 ‐ 533 MB/s|4|
|PCI‐X 1.0|133 MHz|533 ‐ 1066 MB/s|1‐2|
|PCI‐X 2.0 (DDR)|133 MHz|1066 ‐ 2132 MB/s|1 (point‐to‐point bus)|
|PCI‐X 2.0 (QDR)|133 MHz|2132 ‐ 4262 MB/s|1 (point‐to‐point bus)|

</td>
<td width="50%">

## **PCI 与 PCI-X**

PCI（Peripheral Component Interface，外围组件互连）总线于 1990 年代初期开发，旨在弥补当时 PC（个人计算机）所使用外围总线的不足。当时的标准是 IBM 的 AT（Advanced Technology，高级技术）总线，其他厂商称之为
ISA（Industry Standard Architecture，工业标准架构）总线。ISA 对于其最初设计的 286 16 位机器而言已经够用，但对于较新的 32 位机器及其外围设备，需要更大的带宽和增强的功能，例如即插即用。此外，ISA 使用的大型连接器引脚数量较多。PC
厂商认识到变革的必要性，于是提出了若干备选总线设计方案，例如 IBM 的 MCA（Micro-Channel Architecture，微通道架构）、由 IBM 竞争对手以开放标准名义提出的 EISA 总线（Extended ISA，扩展 ISA），以及由显卡厂商为视频设备提出的
VESA 总线（Video Electronics Standards Association，视频电子标准协会）。然而，这些设计都存在一些缺陷，难以被广泛接受。最终，PCI 由 PC 市场的主要厂商组成的联盟开发为开放标准，该联盟成立了一个名为 PCISIG（PCI
Special Interest Group，PCI 特殊兴趣小组）的组织。全新开发的总线架构性能远高于 ISA，并且它还在每个设备内部定义了一组新的寄存器，称为配置空间（Configuration Space）。这些寄存器使软件能够查看设备所需的内存和 I/O
资源，并为每个设备分配不会与系统中其他地址冲突的地址。这些特性：开放的设计、高速度以及软件可见性与可控性，帮助 PCI 克服了曾经限制 ISA 及其他总线发展的障碍。PCI 迅速成为 PC 中的标准外围总线。

几年后，PCI-X（PCI-eXtended，PCI 扩展）作为 PCI 架构的逻辑扩展被开发出来，显著提升了总线性能。我们稍后将讨论这些变化，但 PCI-X 的一个主要设计目标是在硬件和软件上保持与 PCI 设备的兼容性，以尽可能简化从 PCI 的迁移过程。后来，PCI-X
2.0 版本进一步提升了速度，原始数据速率高达 4 GB/s。由于 PCI-X 在硬件上保持了与 PCI 的向后兼容性，它仍然是一种并行总线，并继承了并行模型相关的问题。这对我们而言很有意义，因为并行总线最终会达到实际的有效带宽上限，难以进一步提速。PCISIG
曾探索通过提升数据速率来加速 PCI-X，但最终放弃了这一努力。这一速度上限，加上较高的引脚数，推动了从并行总线模型向新串行总线模型的过渡。

这些早期总线定义列于第 11 页的表 1-1 中，该表展示了随时间推移总线频率和带宽的演进。该表中值得注意的一点是总线时钟频率与总线上扩展卡插槽数量之间的关联性。这源于 PCI 的低功耗信号模型，意味着更高的频率需要更短的走线和更少的总线负载（参见第 16
页的"反射波信号"）。另一个值得关注的现象是，随着时钟频率的增加，共享总线上允许的设备数量也在减少。PCI-X 2.0 引入时，其高速率要求总线必须采用点对点互连。

**表 1-1：总线频率、带宽与插槽数量对比**

|**总线类型**|**时钟频率**|**峰值带宽**<br>**32 位 ‐ 64 位总线**|**每条总线的卡 插槽数量**|
|---|---|---|---|
|PCI|33 MHz|133 ‐ 266 MB/s|4‐5|
|PCI|66 MHz|266 ‐ 533 MB/s|1‐2|
|PCI‐X 1.0|66 MHz|266 ‐ 533 MB/s|4|
|PCI‐X 1.0|133 MHz|533 ‐ 1066 MB/s|1‐2|
|PCI‐X 2.0 (DDR)|133 MHz|1066 ‐ 2132 MB/s|1（点对点总线）|
|PCI‐X 2.0 (QDR)|133 MHz|2132 ‐ 4262 MB/s|1（点对点总线）|

**第 1 章：背景**

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-6"></a>
## 1.6 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Basics**

</td>
<td width="50%">

## **PCI 基础知识**

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-7"></a>
## 1.7 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Basics of a PCI-Based System** 

Figure 1‐1 on page 12 shows an older system based on a PCI bus. The system includes a North Bridge (called “north” because if the diagram is
viewed as a map, it appears geographically north of the central PCI bus) that interfaces between the processor and the PCI bus. Associated
with the North Bridge is the processor bus, system memory bus, AGP graphics bus, and PCI. Several devices share the PCI bus and are either
connected directly to the bus or plugged into an add‐in card connector. A South Bridge connects PCI to system peripherals, such as the ISA
bus where legacy peripherals were carried forward for a few years. The South Bridge was typically also the central resource for PCI that
pro‐ vided system signals like reset, reference clock, and error reporting.

</td>
<td width="50%">

## **基于 PCI 的系统基础** 

第 12 页的图 1‐1 展示了一个基于 PCI 总线的较老式系统。该系统包含一个北桥（之所以称为"北桥"，是因为如果将该图视为一张地图，它在地理位置上位于中央 PCI 总线的北侧），用于在处理器和 PCI 总线之间进行接口对接。与北桥相关联的有处理器总线、系统内存总线、AGP
图形总线以及 PCI 总线。多个设备共享 PCI 总线，它们要么直接连接到总线上，要么插入到扩展卡连接器中。南桥将 PCI 与系统外设（例如 ISA 总线，用于在早期几年中继续承载传统外设）连接起来。南桥通常也是 PCI 的中央资源，提供复位、参考时钟以及错误报告等系统信号。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-8"></a>
## 1.8 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 1‐1: Legacy PCI Bus‐Based Platform_ 

<img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<br>

</td>
<td width="50%">

## **PCI Express 技术** 

_图 1‐1：传统 PCI 总线架构平台_ 

**==> 图片 [384 x 227] 已有意省略 <==**

**----- 图片文字开始 -----**<br>
处理器<br>前端总线 (FSB)<br>图形<br>北桥<br>(Intel 440) SDRAM<br>地址端口 数据端口<br>PCI 33 MHz<br>插槽<br>IDE<br>CD HDD<br>USB 南桥 逻辑错误 以太网 SCSI<br>ISA<br>启动
调制解调器 音频 超级<br>ROM 芯片 芯片 I/O<br>COM1<br>COM2<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-9"></a>
## 1.9 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Bus Initiator and Target** 

In a PCI hierarchy each device on the bus may contain up to eight functions that all share the bus interface for that device, numbered 0‐7
(a single‐function device is always assigned function number 0). Every function is capable of act‐ ing as a target for transactions on the
bus, and most will also be able to initiate transactions. Such an initiator (called a Bus Master) has a pair of pins (REQ# and GNT#)
dedicated to arbitrating for use of the shared PCI bus. As shown in Fig‐ ure 1‐2 on page 13, a Request (REQ#) pin indicates that the master
needs to use the bus and is sent to the bus arbiter for evaluation against all the other requests at that moment. The arbiter is often
located in the bridge that is hierarchically above the bus and receives arbitration requests from all the devices that can act as initiators
(Bus Masters) on that bus. The arbiter decides which requester should be the next owner of the bus and asserts the Grant (GNT#) pin for that
device. According to the protocol, whenever the previous transaction finishes and the bus goes idle, whichever device sees its GNT# asserted
at that time is designated as the next Bus Master and can begin its transaction.

_Figure 1‐2: PCI Bus Arbitration_ 

<img src="figures/page/page0082.png" alt="Figure from page 82" width="700">

<br>

</td>
<td width="50%">

## **PCI 总线发起方与目标方**

在 PCI 层级结构中,总线上的每个设备最多可包含八个功能,这些功能共享该设备的总线接口,编号为 0~7(单功能设备始终被分配功能编号 0)。每个功能都能够作为总线上事务的目标方,其中大多数还能够发起事务。这样的发起方(称为总线主设备)具有一对专用于仲裁共享 PCI
总线使用权的引脚(REQ# 和 GNT#)。如图 1-2(第 13
页)所示,请求(REQ#)引脚表示主设备需要使用总线,该信号被发送到总线仲裁器,以便与此时所有其他请求一起进行评估。仲裁器通常位于层级结构中该总线上方的桥接器中,接收来自该总线上所有可作为发起方(总线主设备)的设备的仲裁请求。仲裁器决定哪个请求者应成为总线的下一个所有者,并为该设备断言授权(GNT#)引脚。根据协议,无论何时,只要前一个事务完成且总线进入空闲状态,在此期间观察到其
GNT# 被断言的设备就被指定为下一个总线主设备,并可以开始其事务。

**第 1 章:背景**

_图 1-2:PCI 总线仲裁_

<img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<br>

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-10"></a>
## 1.10 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Typical PCI Bus Cycle** 

Figure 1‐3 on page 15 represents a typical PCI bus cycle. PCI is synchronous, meaning events happen on clock edges, so the clock is shown at
the top of the diagram and it’s rising edges are marked with dotted lines because those are the times when signals are driven out or
sampled. A brief description of what hap‐ pens on the bus is as follows:

1. On clock edge 1, FRAME# (used to indicate when a bus access is in progress) and IRDY# (Initiator Ready for data) are both inactive,
showing that the bus is idle. At the same time, GNT# is active, meaning the bus arbi‐ ter has selected this device to be the next initiator.

2. On clock edge 2, FRAME# is asserted by the initiator, indicating that a new transaction has started. At the same time, it drives the
address and com‐ mand for this transaction. All of the other devices on the bus will latch this information and begin the process of
decoding the address to see whether it’s a match for them.

</td>
<td width="50%">

## **典型 PCI 总线周期**

第 15 页的图 1‐3 展示了一个典型的 PCI 总线周期。PCI 是同步的，意味着事件发生在时钟边沿上,因此时钟显示在图表的顶部,其上升沿用虚线标出,因为这些是信号被驱动输出或采样的时刻。总线上发生的情况简要描述如下:

1. 在时钟边沿 1 上,FRAME#(用于指示总线访问正在进行)和 IRDY#(发起方数据就绪)均处于无效状态,表明总线处于空闲状态。与此同时,GNT# 有效,意味着总线仲裁器已选择该设备作为下一个发起方。

2. 在时钟边沿 2 上,由发起方断言 FRAME#,表示新事务已开始。同时,它驱动该事务的地址和命令。总线上的所有其他设备将锁存此信息并开始对地址进行解码,以查看该事务是否与它们匹配。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-11"></a>
## 1.11 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Express Technology** 

3. On clock edge 3, the initiator indicates its readiness for data transfer by asserting IRDY#. The round arrow symbol shown on the AD bus
indicates that the tri‐stated bus is undergoing a “turn‐around cycle” as ownership of the signals changes (needed here because this is a
read transaction; the initi‐ ator drives the address but receives data on the same pins). The target’s buffer is not turned on using the
same clock edge that turns the initiator’s buffer off because we want to avoid the possibility of both buffers trying to drive a signal
simultaneously, even for a brief time. That contention on the bus could damage the devices so, instead, the previous buffer is turned off
one clock before the new one is turned on. Every shared signal is handled this way before changing direction.

4. On clock edge 4, a device on the bus has recognized the requested address and responded by asserting DEVSEL# (device select) to claim
this transac‐ tion and participate in it. At the same time, it asserts TRDY# (target ready) to show that it is delivering the first part of
the read data and drives that data onto the AD bus (this could have been delayed ‐ the target is allowed 16 clocks from the assertion of
FRAME# until TRDY#). Since both IRDY# and TRDY# are active at the same time here, data will be transferred on that clock edge, completing
the first data phase. The initiator knows how many bytes will eventually be transferred, but the target does not. The command does not
provide a byte count, so the target must look at the status of FRAME# whenever a data phase completes to learn when the initiator is
satisfied with the amount of data transferred. If FRAME# is still asserted, this was not the last data phase and the transaction will
continue with the next contiguous set of bytes, as is the case here.

5. On clock edge 5, the target is not prepared to deliver the next set of data, so it deasserts TRDY#. This is called inserting a “Wait
State” and the transac‐ tion is delayed for a clock. Both initiator and target are allowed to do this, and each can delay the next data
transfer by up to 8 consecutive clocks.

6. On clock edge 6, the second data item is transferred, and since FRAME# is still asserted, the target knows that the initiator still wants
more data.

7. On clock edge 7, the initiator forces a Wait State. Wait States allow devices to pause a transaction to quickly fill or empty a buffer
and can be helpful because they allow the transaction to resume without having to stop and restart. On the other hand, they are often very
inefficient because they not only stall the current transaction, they also prevent other devices from gain‐ ing access to the bus while it’s
stalled.

8. On clock edge 8, the third data set is transferred and now FRAME# has been deasserted so the target can tell that this was the last data
item. Conse‐ quently, after this clock, all the control lines are turned off and the bus once again goes to the idle state.

In keeping with the low cost design goal for PCI, several signals have more than one meaning on the bus to reduce the pin count. The 32
address and data sig‐ nals are multiplexed and the C/BE# (Command/Byte Enable) signals share their four pins for the same reason. Although
reducing the pin count is desirable, it’s also the reason that PCI uses “turn‐around cycles”, which add more delay. It also precludes the
option to pipeline transactions (sending the address for the next cycle while data for the previous one is delivered). Handshake signals
like FRAME#, DEVSEL#, TRDY#, IRDY#, and STOP# control the timing of events during the transaction.

_Figure 1‐3: Simple PCI Bus Transfer_ 

<img src="figures/page/page0082.png" alt="Figure from page 82" width="700">

<br>

</td>
<td width="50%">

## **PCI Express Technology**

3. 在时钟边沿 3,发起端通过置位 IRDY# 来表明其已准备好进行数据传输。AD 总线上显示的圆形箭头符号表示三态总线正在进行"转向周期 (turn-around
cycle)",因为信号的所有权正在发生改变(此处需要该周期,因为这是一次读事务;发起端驱动地址,但在相同的引脚上接收数据)。目标设备的缓冲区并不是在使用与关闭发起端缓冲区相同的时钟边沿上打开,因为我们希望避免两个缓冲区在同一时刻(哪怕是短暂的时间)同时驱动信号的可能性。总线上的这种争用可能会损坏器件,因此,前一个缓冲区要在新缓冲区打开的前一个时钟被关闭。每条共享信号在改变方向之前都会以这种方式处理。

4. 在时钟边沿 4,总线上的某个设备识别到了所请求的地址,并通过置位 DEVSEL# (Device Select) 来响应该事务,从而认领该事务并参与其中。同时,它置位 TRDY# (Target Ready) 以表明它正在提供读数据的第一个部分,并将该数据驱动到 AD
总线上(这可能会被延迟——目标端从置位 FRAME# 起最多有 16 个时钟的窗口来置位 TRDY#)。由于此处 IRDY# 和 TRDY#
同时有效,因此将在该时钟边沿上传输数据,从而完成第一个数据相位。发起端知道最终将传输多少字节,但目标端并不知道。该命令并不提供字节计数,因此目标端必须在每个数据相位完成时查看 FRAME# 的状态,以了解发起端是否对已传输的数据量感到满意。如果 FRAME#
仍然处于置位状态,则表示这并非最后一个数据相位,事务将继续传输下一组连续的字节,正如本例中的情况。

5. 在时钟边沿 5,目标端尚未准备好提供下一组数据,因此它撤销 TRDY#。这称为插入一个"等待状态 (Wait State)",事务将因此延迟一个时钟。发起端和目标端均允许这样做,并且各自可以将下一次数据传输延迟最多连续 8 个时钟。

6. 在时钟边沿 6,传输第二个数据项,并且由于 FRAME# 仍然处于置位状态,目标端知道发起端仍然希望获取更多的数据。

7. 在时钟边沿 7,发起端强制插入一个等待状态。等待状态允许设备暂停一个事务以快速填充或清空缓冲区,这是非常有用的,因为它允许事务在不停止并重新启动的情况下继续进行。另一方面,它们通常效率很低,因为它们不仅会停滞当前事务,还会阻止其他设备在该停滞期间访问总线。

8. 在时钟边沿 8,传输第三组数据,此时 FRAME# 已被撤销,因此目标端可以判断这是最后一个数据项。因此,在该时钟之后,所有控制线均关闭,总线再次进入空闲状态。

**第 1 章:背景**

为了保持 PCI 的低成本设计目标,总线上有多个信号具有多重含义,以减少引脚数。32 个地址和数据信号进行了多路复用,C/BE# (Command/Byte Enable,命令/字节使能) 信号也在其 4 个引脚上进行了复用,出于同样的原因。尽管减少引脚数是可取的,但这也是
PCI 使用"转向周期"的原因,这会引入更多的延迟。同时,这一设计也排除了流水线事务的可能性(在前一个周期的数据交付期间发送下一个周期的地址)。诸如 FRAME#、DEVSEL#、TRDY#、IRDY# 和 STOP# 之类的握手信号用于控制事务过程中事件的时间安排。

_**图 1‐3:简单的 PCI 总线传输**_

<img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<br>

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-12"></a>
## 1.12 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Reflected-Wave Signaling** 

PCI architecturally supports up to 32 devices on each bus, but the practical elec‐ trical limit is considerably less, on the order of 10 to
12 electrical loads at the base frequency of 33MHz. The reason for this is that the bus uses a technique called “reflected‐wave signaling”
to reduce the power consumption on the bus (see Figure 1‐4 on page 17). In this model, devices save cost and power by implementing weak
transmit buffers that can only drive the signal to about half the voltage needed to switch the signal. The incident wave of the signal
propa‐ gates down the transmission line until it reaches the end. By design, there is no termination at the end of the line so the wavefront
encounters an infinite imped‐ ance and reflects back. This reflection is additive in nature and increases the sig‐ nal to the full voltage
level as it makes its way back to the transmitter. When the signal reaches the originating buffer, the low output impedance of the driver
terminates the signal and prevents further reflections. The total elapsed time from the buffer asserting a signal until the receiver detects
a valid signal is thus the propagation time down the wire plus the reflection delay coming back and the setup time. All of that must be less
than the clock period.

As the length of the trace and the number of electrical loads on a bus increase, the time required for the signal to make this round trip
increases. A 33 MHz PCI bus can only meet the signal timing with about 10‐12 electrical loads. An electri‐ cal load is one device installed
on the system board, but a populated connector slot actually counts as two loads. Therefore, as indicated in Table 1‐1 on page 11, a 33 MHz
PCI bus can only be designed for reliable operation with a maximum of 4 or 5 add‐in card connectors.

_Figure 1‐4: PCI Reflected‐Wave Signaling_ 

<img src="figures/page/page0082.png" alt="Figure from page 82" width="700">

<br>

To connect more loads in a system, a PCI‐to‐PCI bridge is needed, as shown in Figure 1‐5. By the time more modern chipsets were available,
peripherals had grown so fast that their competition for access to the shared PCI bus was limit‐ ing their performance. PCI speeds didn’t
keep up, and it became a system bot‐ tleneck even though it was still very popular for peripherals. The solution to this problem was to move
PCI out of the main path between system peripherals and memory, replacing the chipset interconnect with a proprietary solution (in this
example, Intel’s Hub Link interface).

A PCI Bridge is an extension to the topology. Each Bridge creates a new PCI bus that is electrically isolated from the bus above it,
allowing another 10‐12 loads. Some of these devices could also be bridges, allowing a large number of devices to be connected in a system.
The PCI architecture allows up to 256 buses in a single system and each of those buses can have up to 32 devices.

_Figure 1‐5: 33 MHz PCI System, Including a PCI‐to‐PCI Bridge_ 

<img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<br>

</td>
<td width="50%">

## **反射波信号（Reflected-Wave Signaling）** 

PCI 在架构上每条总线最多支持 32 个设备,但实际可承受的电气负载远低于该数值,在 33MHz 基频下大约只有 10 到 12 个电气负载。其原因是 PCI 总线采用了一种称为"反射波信号"的技术以降低总线功耗（参见第 17 页的图
1-4）。在该模型中,设备通过实现较弱的发送缓冲器来节省成本和功耗,这种缓冲器只能将信号驱动到切换信号所需电压的一半左右。信号的入射波沿传输线传播,直到到达末端。按设计,线路末端没有端接器,因此波前会遭遇无穷大阻抗并被反射回来。该反射在性质上是叠加的,会在其返回发送器的过程中将信号电压叠加至完整电平。当信号到达原始缓冲器时,驱动器较低的输出阻抗会终结该信号并阻止进一步的反射。因此,从缓冲器发出信号到接收器检测到有效信号所经历的总耗时,等于信号沿导线传播的传播时间加上反射回来的延迟再加上建立时间。所有这些时长都必须小于时钟周期。

随着走线长度和总线上电气负载数量的增加,信号完成该往返所需的时间也随之增加。33 MHz 的 PCI 总线在仅约 10-12 个电气负载时才能满足信号时序要求。一个电气负载可以是安装在系统板上的一台设备,但一个已插接的连接器插槽实际上计为两个负载。因此,正如第 11 页的表
1-1 所示,33 MHz PCI 总线在设计上最多只能稳定支持 4 到 5 个扩展卡连接器插槽。

**第 1 章：背景** 

_图 1-4：PCI 反射波信号_ 

**==> 图片 [223 x 194] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
PCI CLK 周期<br>
30ns（33MHz 时）<br>
C<br>
Tprop Tsu<br>
最大 10ns 最小 7ns<br>
Tval A B<br>
最大 11ns<br>
**----- 图片文字结束 -----**<br>

要在系统中连接更多负载,就需要 PCI-to-PCI 桥（PCI-to-PCI Bridge）,如图 1-5 所示。等到更现代的芯片组出现时,各类外设增长迅速,它们对共享 PCI 总线访问权的竞争已开始限制其性能表现。PCI
的速度未能跟上,即便它在当时仍非常流行,却已成为系统瓶颈。该问题的解决方案是将 PCI 从系统外设与内存之间的主路径中移除,并用一种专有方案（本例中为 Intel 的 Hub Link 接口）来替代芯片组互连。

PCI 桥是拓扑的扩展。每个桥都会创建一条新的 PCI 总线,该总线在电气上与其上游总线相隔离,从而允许再增加 10-12 个负载。这些设备中的一部分也可以是桥,从而使系统中可以连接大量设备。PCI 架构在单个系统中最多允许 256 条总线,每条总线上又可挂载多达 32 个设备。

**PCI Express 技术** 

_图 1-5：33 MHz PCI 系统,包含 PCI-to-PCI 桥_ 

**==> 图片 [353 x 219] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
处理器（Processor）<br>
FSB<br>
AGP<br>
4x 内存控制器 Hub（Memory Controller Hub）<br>
GFX<br>
(Intel 8XX GMCH) DDR<br>
O n TT SDRAM<br>
Hub Link 插槽（Slots）<br>
IDE<br>
CD HDD PCI-33MHz<br>
USB IO Controller Hub 主 PCI 总线（Primary PCI Bus）<br>
(ICH4) PCI<br>
LPC<br>
桥（Bridge）<br>
Super AC'97<br>
IO Link 次 PCI 总线（Secondary PCI Bus）<br>
以太网（Ethernet）<br>
COM1 COM1 调制解调器（Modem）音频（Audio） (a 启动<br>
COM2 编解码器（CODEC）编解码器（CODEC）以太网（Ethernet） ROM<br>
**----- 图片文字结束 -----**<br>

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-13"></a>
## 1.13 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Bus Architecture Perspective**

</td>
<td width="50%">

## **PCI 总线架构视角 (PCI Bus Architecture Perspective)**

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-14"></a>
## 1.14 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Transaction Models** 

PCI uses three models for data transfer just as previous bus models did: Pro‐ grammed I/O (PIO), Peer‐to‐peer, and DMA. These models are
illustrated in Figure 1‐6 on page 19 and described in the following sections.

</td>
<td width="50%">

## **PCI 事务模型** 

与之前的总线模型一样,PCI 使用三种模型进行数据传输:编程 I/O (PIO)、对等 (Peer-to-Peer) 和 DMA。这些模型如图 1-6(第 19 页)所示,并将在以下各节中进行描述。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-15"></a>
## 1.15 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Programmed I/O** 

PIO was commonly used in the early days of the PC because designers were reluctant to add the expense or complexity to their devices of
transaction man‐ agement logic. The processor could do the job faster than any other device any‐ way so, in this model, it handles all the
work. For example, if a PCI device

interrupts the CPU to indicate that it needs to put data in memory, the CPU will end up reading data from the PCI device into an internal
register and then copying that register to memory. Going the other way, if data is to be moved from memory to the PCI device, software
instructs the CPU to read from mem‐ ory into its internal register and then write that register to the PCI device.

The process works but is inefficient for two reasons. First, there are two bus cycles generated by the CPU for every data transfer, and
second, the CPU is busy with data transfer housekeeping rather than more interesting work. In the early days this was the fastest transfer
method and the single‐tasking processor didn’t have much else to do. These types of inefficiencies are typically not acceptable in modern
systems, so this method is no longer very common for data transfers, and instead the DMA method described in the next section is the
preferred approach. However, programmed IO is still a necessary transaction model in order for software to interact with a device.

_Figure 1‐6: PCI Transaction Models_ 

<img src="figures/page/page0082.png" alt="Figure from page 82" width="700">

<br>

</td>
<td width="50%">

## **程序化 I/O** 

PIO 在个人电脑 (PC) 早期被广泛使用,这是因为设计者不愿意在其设备中增加事务管理逻辑所需的成本或复杂性。处理器反正比任何其他设备完成这项工作都要快,因此在这种模式下,处理器承担了所有的工作。例如,如果一个 PCI 设备

**第 1 章:背景** 

向 CPU 发出中断以表明它需要将数据放入内存,那么 CPU 最终会从 PCI 设备读取数据到其内部寄存器,然后再将该寄存器中的数据复制到内存。反过来,如果需要将数据从内存移动到 PCI 设备,软件则指示 CPU 从内存读取数据到其内部寄存器,然后再将该寄存器中的数据写入 PCI
设备。

这个过程虽然可行,但出于两个原因效率低下。首先,CPU 每传输一次数据就会产生两个总线周期;其次,CPU
一直忙于数据传输的杂事,而无法做更有意义的工作。在早期,这是最快的传输方式,而且单任务处理器也没有太多其他事情可做。这种低效率在现代系统中通常是不可接受的,因此这种方法在数据传输中已不再常见,取而代之的是下一节中介绍的 DMA 方法,这才是首选方案。然而,程序化 I/O
仍然是一种必要的事务模型,因为软件需要通过它与设备进行交互。

_图 1‐6:PCI 事务模型_ 

**==> 图片 [380 x 226] 故意省略 <==**

**----- 图片文字开始 -----**<br>
处理器<br>前端总线 (FSB) 程序化 I/O<br>图形<br>北桥 (Intel 440北桥 (Intel 440)) SDRAM<br>地址端口 数据端口<br>DMA<br>PCI 33 MHz<br>对等<br>到<br>对等 插槽<br>IDE<br>CD
HDD<br>USB 南桥 逻辑错误 以太网 SCSI<br>ISA<br>启动 调制解调器 音频 超级<br>ROM 芯片 芯片 I/O<br>COM1<br>COM2<br>**----- 图片文字结束 -----**<br>

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-16"></a>
## 1.16 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Direct Memory Access (DMA)** 

A more efficient method of transferring data is called DMA (direct memory access). In this model another device, called a DMA engine,
handles the details of memory transfers to a peripheral on behalf of the processor, off‐loading this

tedious task. Once the CPU has programmed the starting address and byte count into it, the DMA engine handled the bus protocol and address
sequencing on its own. This didn’t involve any change to the PCI peripherals and allowed them to keep their low‐cost designs. Later,
improved integration allowed peripherals to integrate this DMA functionality locally, so they didn’t need an external DMA engine. These
devices were capable of handling their own bus transfers and were called Bus Master devices.

Figure 1‐3 on page 15 is an example of a Bus Master transaction on PCI. The North Bridge might decode the address and recognize that it will
be the target for the transaction. In the data phase of the bus cycle, data is transferred between the Bus Master and the North Bridge
acting as the target. The North Bridge in turn will generate DRAM bus cycles to communicate with system memory. After the transfer is
completed, the PCI peripheral might generate an interrupt to inform the system. The DMA method of data transfer is more effi‐ cient because
the CPU is not involved in the data movement, and a single bus cycle may be sufficient to move a block of data.

</td>
<td width="50%">

## **直接内存访问 (DMA)**

一种更高效的数据传输方法被称为 DMA（直接内存访问）。在该模式下，另一种称为 DMA 引擎的设备代表处理器处理与外设之间的内存传输细节，从而

将这一繁琐的任务卸载。一旦 CPU 将起始地址和字节计数编程到 DMA 引擎中，DMA 引擎便自行处理总线协议和地址排序。这并不需要对 PCI 外设进行任何改动，并允许它们保持低成本的设计。后来，随着集成度的提高，外设可以在本地集成该 DMA 功能，因此不再需要外部的 DMA
引擎。这些设备能够自行处理总线传输，被称为总线主控（Bus Master）设备。

第 15 页的图 1-3 是 PCI 上总线主控事务的一个示例。北桥（North Bridge）可能对地址进行译码，并识别出它将成为该事务的目标。在总线周期的数据阶段，数据在总线主控与作为目标的北桥之间传输。北桥随后将生成 DRAM 总线周期以与系统内存通信。传输完成后，PCI
外设可能会产生一个中断以通知系统。DMA 数据传输方法更为高效，因为 CPU 不参与数据的搬移，并且单个总线周期便足以搬移一整块数据。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-17"></a>
## 1.17 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **Peer-to-Peer** 

If a device is capable of acting as a Bus Master, then another interesting option presents itself. One PCI Bus Master could initiate a
transfer to another PCI device, with the result that the entire transaction remains local to the PCI bus and doesn’t involve any other
system resources. Since this transaction takes place between devices that are considered peers in the system, it’s referred to as a
peer‐to‐peer transaction. This has some obvious efficiencies because the rest of the system remains free to do other work. Nevertheless,
it’s rarely used in prac‐ tice because the initiator and target don’t often use the same format for the data unless both are made by the
same vendor. Consequently, the data usually must first be sent to memory where the CPU can reformat it before it is then trans‐ ferred to
the target, defeating the goal of a peer‐to‐peer transfer.

</td>
<td width="50%">

## **对等传输 (Peer-to-Peer)**

如果一个设备能够充当总线主设备 (Bus Master)，那么另一个有趣的选择就出现了。一个 PCI 总线主设备可以向另一个 PCI 设备发起传输，其结果是整个事务保持在 PCI
总线本地进行，而不涉及任何其他系统资源。由于这种事务发生在系统中被视为对等体的设备之间，因此被称为对等 (peer-to-peer)
事务。这具有明显的效率优势，因为系统的其余部分可以保持空闲以执行其他工作。然而，在实践中它很少被使用，因为发起方和目标方通常不会使用相同的数据格式，除非两者由同一家供应商制造。因此，数据通常必须首先被发送到内存，由 CPU
对其进行重新格式化，然后再传输到目标设备，这就违背了对等传输的目标。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-18"></a>
## 1.18 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Bus Arbitration** 

Consider Figure 1‐2 on page 13. Since PCI devices today are almost all capable of being bus‐master, they are able to do both DMA and
peer‐to‐peer transfers. In a shared bus architecture like PCI, they have to take turns on the bus, so a device that wants to initiate
transactions must first request ownership of the bus from the bus arbiter. The arbiter sees all the current requests and uses an imple‐
mentation‐specific algorithm to decide which Bus Master gets ownership of the bus next. The PCI spec doesn’t describe this algorithm, but
does state that it must be “fair” and not starve any device for access.

The arbiter can grant bus ownership to the next requesting device while the pre‐ vious Bus Master is still executing its transfer, so that
no clocks are used on the bus to sort out the next owner. As a result, the arbitration appears to happen behind the scenes and is referred
to as “hidden” bus arbitration, which was a design improvement over earlier bus protocols.

</td>
<td width="50%">

## **PCI 总线仲裁**

请参考第 13 页的图 1-2。由于如今的 PCI 设备几乎都具备总线主控（Bus‐Master）能力，它们既能执行 DMA 传输，也能进行点对点（peer‐to‐peer）传输。在像 PCI
这样的共享总线架构中，它们必须轮流使用总线，因此希望发起事务的设备必须首先向总线仲裁器请求总线所有权。仲裁器会看到所有当前的请求，并使用一种与具体实现相关的算法来决定下一个获得总线所有权的是哪个总线主控设备。PCI
规范并未规定该算法，但确实要求它必须是"公平的"，不能让任何设备因长期得不到访问机会而被饿死。

**第 1 章：背景**

仲裁器可以在上一个总线主控设备仍在执行其传输的过程中，就将总线所有权授予下一个请求的设备，因此在总线上不会消耗额外的时钟周期来决定下一个所有者。因此，仲裁过程看起来好像在后台完成，被称为"隐藏式"总线仲裁，这是相对于早期总线协议的一项设计改进。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-19"></a>
## 1.19 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Inefficiencies**

</td>
<td width="50%">

## **PCI 的不足之处 (PCI Inefficiencies)**

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-20"></a>
## 1.20 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Retry Protocol** 

When a PCI master initiates a transaction to access a target device and the target device is not ready, the target signals a transaction
retry. This scenario is shown in Figure 1‐7.

_Figure 1-7: PCI Transaction Retry Mechanism_ 

<img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<br>

Consider the following example in which the North bridge initiates a memory read transaction to read data from the Ethernet device. The
Ethernet target claims the bus cycle. However, the Ethernet target does not immediately have the data to return to the North bridge master.
The Ethernet device has two choices by which to delay the data transfer. The first is to insert wait‐states in

</td>
<td width="50%">

## **PCI 重试协议** 

当 PCI 主设备发起一次访问目标设备的交易，而目标设备尚未就绪时，目标设备会发出交易重试 (Retry) 信号。该场景如图 1-7 所示。 

_图 1-7:PCI 交易重试机制_ 

**==> 图片 [372 x 226] 已省略 <==**

**----- 图片文字开始 -----**<br>
处理器<br>FSB<br>显卡<br>北桥北桥桥桥<br>(Intel 440(Intel 440 ) S DRAM<br>地址端口 数据端口<br>1. 发起<br>PCI 33 MHz 3. 重试<br>插槽<br>IDE<br>CD HDD<br>USB 南桥 逻辑错误
以太网 SCSI<br>ISA<br>启动 调制解调器 音频 超级 2. 目标设备<br>ROM 芯片 芯片 I/O 未就绪<br>COM1<br>COM2<br>**----- 图片文字结束 -----**<br>

考虑下面这个示例:北桥发起一次内存读交易,以读取以太网设备中的数据。以太网目标设备声明占用该总线周期。然而,以太网目标设备并不能立即将数据返回给北桥主设备。以太网设备有两种选择来延迟数据传输。第一种是在

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-21"></a>
## 1.21 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Express Technology** 

the data phase. If only a few wait‐states are needed, then the data is still trans‐ ferred efficiently. If however the target device
requires more time (more than 16 clocks from the beginning of the transaction), then the second option the target has is to signal a retry
with a signal called STOP#. A retry tells the master to end the bus cycle prematurely without transferring data. Doing so prevents the bus
from being held for a long time in wait‐states, which compromises the bus effi‐ ciency. The Bus Master that is retried by the target waits a
minimum of 2 clocks and must once again arbitrate for use of the bus to re‐initiate the identical bus cycle. During the time that the Bus
Master is retried, the arbiter can grant the bus to other requesting masters so that the PCI bus is more efficiently utilized. By the time
the retried master is granted the bus and it re‐initiates the bus cycle, hopefully the target will claim the cycle and will be ready to
transfer data. The bus cycle goes to completion with data transfer. Otherwise, if the target is still not ready, it retries the master’s bus
cycle again and the process is repeated until the master successfully transfers data.

</td>
<td width="50%">

## **PCI Express Technology**

数据阶段。如果只需要几个等待状态（wait-state），那么数据仍能被高效传输。然而，如果目标设备需要更多时间（从事务开始算起超过 16 个时钟），那么目标设备的第二个选项就是通过一个称为 STOP#
的信号来发出重试（retry）。重试通知主设备提前结束该总线周期，而不传输数据。这样做可以防止总线长时间停留在等待状态，从而避免总线效率受损。被目标设备重试的总线主设备至少需要等待 2
个时钟周期，并且必须再次仲裁总线使用权以重新发起相同的总线周期。在该总线主设备被重试的这段时间里，仲裁器可以将总线授予其他请求总线的主设备，从而更高效地利用 PCI
总线。等到被重试的主设备获得总线授权并重新发起总线周期时，希望目标设备此时能接受该周期并准备好传输数据。该总线周期将携带数据传输完成。否则，如果目标设备仍未准备好，它会再次重试主设备的总线周期，并重复该过程，直到主设备成功完成数据传输。

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-1-22"></a>
## 1.22 Background | 背景

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%">🇨🇳 中文</th></tr></thead>
<tbody>
<tr>
<td width="50%">

## **PCI Disconnect Protocol** 

When a PCI master initiates a transaction to access a target device and if the tar‐ get device is able to transfer at least one doubleword
of data but cannot com‐ plete the entire data transfer, it disconnects the transaction at the point at which it cannot continue. This
scenario is illustrated in Figure 1‐8 on page 23.

Consider the following example in which the North bridge initiates a burst memory read transaction to read data from the Ethernet device.
The Ethernet target device claims the bus cycle and transfers some data, but then runs out of data to transfer. The Ethernet device has two
choices to delay the data transfer. The first option is to insert wait‐states during the current data phase while wait‐ ing for additional
data to arrive. If the target needs to insert only a few wait‐ states, then the data is still transferred efficiently. If however the target
device requires more time (the PCI specification allows maximum of 8 clocks in the data phase), then the target device must signal a
disconnect. To do this the tar‐ get asserts STOP# in the middle of the bus cycle to tell the master to end the bus cycle prematurely. A
disconnect results in some data transferred, while a retry does not. Disconnect frees the bus from long periods of wait states. The discon‐
nected master waits a minimum of 2 clocks before once again arbitrating for use of the bus and continuing the bus cycle at the disconnected
address. During the time that the Bus Master is disconnected, the arbiter may grant the bus to other requesting masters so that the PCI bus
is utilized more efficiently. By the time the disconnected master is granted the bus and continues the bus cycle, hope‐ fully the target is
ready to continue the data transfer until it is completed. Oth‐ erwise, the target once again retries or disconnects the master’s bus cycle
and the process is repeated until the master successfully transfers all its data.

_Figure 1-8: PCI Transaction Disconnect Mechanism_ 

<img src="figures/page/page0082.png" alt="Figure from page 82" width="700">

<br>

</td>
<td width="50%">

1 ## **PCI 断开连接协议** 

2 当 PCI 主设备发起事务以访问目标设备时,如果目标设备能够传输至少一个双字的数据但不能完成整个数据传输,它会在无法继续的位置断开事务。图 1-8(第 23 页)说明了这种情况。 

3 考虑以下示例,其中北桥(North
bridge)发起突发内存读事务以从以太网设备读取数据。以太网目标设备声明总线周期并传输一些数据,但随后就没有数据可传输了。以太网设备有两种选择来延迟数据传输。第一个选项是在当前数据阶段插入等待状态,同时等待更多数据到达。如果目标只需要插入少量等待状态,则数据仍然可以有效地传输。但是,如果目标设备需要更多时间(PCI
规范允许在数据阶段最多 8 个时钟),则目标设备必须发出断开连接信号。为此,目标在总线周期中间断言 STOP#,以告诉主设备提前结束总线周期。断开连接会导致部分数据传输,而重试则不会。断开连接将总线从长时间的等待状态中解放出来。断开连接的主设备至少等待 2
个时钟,然后再次仲裁使用总线并在断开连接的地址处继续总线周期。在总线主设备断开连接期间,仲裁器可以将总线授予其他请求的主设备,以便更有效地利用 PCI
总线。当断开连接的主设备被授予总线并继续总线周期时,希望目标已准备好继续数据传输,直到完成为止。否则,目标将再次重试或断开主设备的总线周期,并重复该过程,直到主设备成功传输所有数据。

4 **22** 

5 **Chapter 1: Background** 

6 _Figure 1-8: PCI Transaction Disconnect Mechanism_ 

7 <img src="figures/page/page0080.png" alt="Figure from page 80" width="700">

<br>

</td>
</tr>
</tbody>
</table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
