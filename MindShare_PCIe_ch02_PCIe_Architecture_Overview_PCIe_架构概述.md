# 📘 第 2 章　PCIe 架构概述 (Chapter 2. PCIe Architecture Overview)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0113.md` ... `chunks/chunk0138.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [2.1 PCIe Architecture Overview — PCIe 架构概述](#sec-2-1)
- [2.2 PCIe Architecture Overview — PCIe 架构概述](#sec-2-2)
- [2.3 PCIe Architecture Overview — PCIe 架构概述](#sec-2-3)
- [2.4 PCIe Architecture Overview — PCIe 架构概述](#sec-2-4)
- [2.5 PCIe Architecture Overview — PCIe 架构概述](#sec-2-5)
- [2.6 PCIe Architecture Overview — PCIe 架构概述](#sec-2-6)
- [2.7 PCIe Architecture Overview — PCIe 架构概述](#sec-2-7)
- [2.8 PCIe Architecture Overview — PCIe 架构概述](#sec-2-8)
- [2.9 PCIe Architecture Overview — PCIe 架构概述](#sec-2-9)
- [2.10 PCIe Architecture Overview — PCIe 架构概述](#sec-2-10)
- [2.11 PCIe Architecture Overview — PCIe 架构概述](#sec-2-11)
- [2.12 PCIe Architecture Overview — PCIe 架构概述](#sec-2-12)
- [2.13 PCIe Architecture Overview — PCIe 架构概述](#sec-2-13)
- [2.14 PCIe Architecture Overview — PCIe 架构概述](#sec-2-14)
- [2.15 PCIe Architecture Overview — PCIe 架构概述](#sec-2-15)
- [2.16 PCIe Architecture Overview — PCIe 架构概述](#sec-2-16)
- [2.17 PCIe Architecture Overview — PCIe 架构概述](#sec-2-17)
- [2.18 PCIe Architecture Overview — PCIe 架构概述](#sec-2-18)
- [2.19 PCIe Architecture Overview — PCIe 架构概述](#sec-2-19)
- [2.20 PCIe Architecture Overview — PCIe 架构概述](#sec-2-20)
- [2.21 PCIe Architecture Overview — PCIe 架构概述](#sec-2-21)
- [2.22 PCIe Architecture Overview — PCIe 架构概述](#sec-2-22)
- [2.23 PCIe Architecture Overview — PCIe 架构概述](#sec-2-23)
- [2.24 PCIe Architecture Overview — PCIe 架构概述](#sec-2-24)
- [2.25 PCIe Architecture Overview — PCIe 架构概述](#sec-2-25)
- [2.26 PCIe Architecture Overview — PCIe 架构概述](#sec-2-26)

<a id="sec-2-1"></a>
## 2.1 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Interrupt Handling** 

PCI devices use one of four sideband interrupt signals (INTA#, INTB#, INTC#, or INTD#) to send an interrupt request to the system. When one
of the pins is asserted, the interrupt controller in a single‐CPU system responded by asserting the INTR (interrupt request) pin to the CPU.
Later multi‐CPU designs needed to improve on the single wire input for interrupts and changed to an APIC (Advanced Programmable Interrupt
Controller) model, in which the controller sends a message to the multiple CPUs instead of asserting the INTR pin to one of them. Regardless
of the delivery model, an interrupted CPU must determine the source of the interrupt and then service the interrupt. The legacy model
required several bus cycles for this and wasn’t very efficient. The APIC model is better but also leaves room for improvement.

</td>
<td width="50%">

## **PCI 中断处理** 

PCI 设备使用四个边带中断信号（INTA#、INTB#、INTC# 或 INTD#）之一向系统发送中断请求。当其中某个引脚被置位时，单 CPU 系统中的中断控制器通过置位 CPU 的 INTR（中断请求）引脚来响应。之后的多 CPU 设计需要对单线中断输入进行改进，于是改为
APIC（高级可编程中断控制器）模型，在该模型中，控制器向多个 CPU 发送消息，而不是将 INTR 引脚置位给其中某一个 CPU。无论采用哪种传递模型，被中断的 CPU 都必须确定中断源，然后服务该中断。传统模型需要多个总线周期来完成这一过程，效率较低。APIC
模型更好一些，但仍有改进空间。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-2"></a>
## 2.2 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Error Handling** 

PCI devices can optionally detect and report address and data phase parity errors during transactions. PCI generates ʺeven parityʺ across
most of the sig‐ nals during a transaction by using the PAR signal. This means that if the num‐ ber of set bits during an address or data
phase is odd, the master device will set the PAR signal to make the parity ʺeven.ʺ The target device receives the address or data and checks
for errors. Parity errors are detectable only as long as an odd number of signals are affected causing the received number of ones to be
odd. If a device detects a data phase parity error, it asserts PERR# (parity error). This is potentially a recoverable error since, for
cases like a memory read, just repeat‐ ing the transaction may resolve the problem. PCI does not include any auto‐ matic or hardware‐based
recovery mechanisms, though, so any attempts to resolve the error would be handled by software.

_Figure 1‐9: PCI Error Handling_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0100.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

However, it’s a different matter if a parity error is detected during the address phase. In this case the address was corrupted and the
wrong target may have recognized the address. There’s no way to tell what the corrupted address became or what devices on the bus did in
response to it, so there’s also no sim‐
ple recovery. As a result, errors of this type result in the assertion of the SERR# (system error) pin, which typically results in a call to
the system error handler. In older machines, this would often halt the system as a precaution, resulting in the “blue screen of death.”

In older machines, both PERR# and SERR# were connected to the error logic in the South Bridge. For reasons of simplicity and cost, this
typically resulted in the assertion of an NMI signal (non‐maskable interrupt signal) to the CPU, which would often simply halt the system.

</td>
<td width="50%">

## **PCI 错误处理** 

PCI 设备可以在事务过程中可选地检测并报告地址与数据阶段的奇偶校验错误。PCI 在事务期间使用 PAR 信号在大多数信号上生成"偶校验"。这意味着如果在地址或数据阶段被置位的比特数为奇数,主设备会设置 PAR
信号以使校验变为"偶校验"。目标设备接收地址或数据并检查错误。奇偶校验错误仅在受影响的信号数为奇数(导致接收到的 1 的个数为奇数)时才能被检测出来。如果设备检测到数据阶段奇偶校验错误,它会断言
PERR#(奇偶校验错误)。这通常是一个可恢复的错误,因为对于内存读等情况,只需简单地重试该事务即可解决该问题。不过 PCI 不包含任何自动或基于硬件的恢复机制,因此任何尝试解决错误的操作都将由软件处理。

_图 1‐9: PCI 错误处理_ 

**==> 图片 [376 x 229] 已刻意省略 <==**

**----- 图片文字开始 -----**<br>
NMI<br>
处理器<br>
FSB<br>
图形<br>
北桥北桥<br>
(Intel 440)(Intel 440) S DRAM<br>
地址端口 数据端口<br>
PCI 33 MHz<br>
插槽<br>
CD HDD IDE PERR#<br>
错误<br>
南桥逻辑<br>
USB SERR#<br>
ISA<br>
以太网 SCSI<br>
启动 调制解调器 音频 超级<br>
ROM 芯片 芯片 I/O<br>
COM1<br>
COM2<br>
**----- 图片文字结束 -----**<br>

然而,如果在地址阶段检测到奇偶校验错误,情况就不同了。在这种情况下,地址已经被损坏,错误的设备可能已经识别了该地址。我们无法知道被损坏的地址变成了什么,也无法知道总线上的设备对此做了什么响应,因此也无法简单地恢复。因此,此类错误会导致
SERR#(系统错误)引脚被断言,这通常会导致调用系统错误处理程序。在较老的机器中,出于预防考虑,这通常会停止系统,从而导致"蓝屏死机"的出现。

在较老的机器中,PERR# 和 SERR# 都连接到南桥中的错误逻辑。出于简洁性和成本的考虑,这通常会导致向 CPU 断言 NMI 信号(不可屏蔽中断信号),从而通常简单地停止系统。 

**第 1 章:背景**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-3"></a>
## 2.3 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Address Space Map** 

PCI architecture supports 3 address spaces as shown in Figure 1‐10 on page 26: memory, I/O and configuration address space. x86 processors
can access mem‐ ory and IO space directly. A PCI device maps into the processors memory address space and can either support 32 or 64 bit
memory addressing. In I/O address space, PCI supports 32 bit addresses but, since x86 CPUs only used 16 bits for I/O space, many platforms
limit the I/O space to 64 KB (16 bits worth).

PCI also introduced a third address space called configuration space that the CPU could only indirectly access. Each function contains
internal registers for configuration space that allow software visibility and control of its addresses and resources in a standardized way,
providing a true “plug and play” environ‐ ment in the PC. Each PCI function may have up to 256 Bytes of configuration address space. Given
that PCI supports up to 8 functions/device, 32 devices/bus and up to 256 buses/system, then the total amount of configuration space asso‐
ciated with a system is 256 Bytes/function x 8 functions/device x 32 devices/bus x 256 buses/system = 16MB of configuration space.

Since an x86 CPU cannot access configuration space directly, it must do so indi‐ rectly by indexing through IO registers (although with PCI
Express a new method to access configuration space was introduced by mapping it into the memory address space). The legacy model, shown in
Figure 1‐10 on page 26, uses an IO Port called Configuration Address Port located at address CF8h‐ CFBh and a Configuration Data Port mapped
to address CFCh‐CFFh. Details regarding this method and the memory mapped method of accessing configu‐ ration space are explained in the
next section.

_Figure 1‐10: Address Space Mapping_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0101.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
<td width="50%">

1 ## **PCI 地址空间映射** 

2 PCI 架构支持 3 个地址空间,如图 1-10(第 26 页)所示:内存、I/O 和配置地址空间。x86 处理器可以直接访问内存和 IO 空间。PCI 设备映射到处理器的内存地址空间,可以支持 32 位或 64 位内存寻址。在 I/O 地址空间中,PCI 支持 32
位地址,但由于 x86 CPU 仅对 I/O 空间使用 16 位,许多平台将 I/O 空间限制为 64 KB(16 位)。

3 PCI 还引入了第三个地址空间,称为配置空间,CPU 只能间接访问它。每个功能(Function)都包含用于配置空间的内部寄存器,这些寄存器以标准化方式提供对其地址和资源的软件可见性和控制,从而在 PC 中提供真正的"即插即用"环境。每个 PCI 功能最多可以有 256
字节的配置地址空间。鉴于 PCI 支持每个设备最多 8 个功能、每条总线 32 个设备和每个系统最多 256 条总线,则与系统关联的配置空间总量为 256 字节/功能 × 8 功能/设备 × 32 设备/总线 × 256 总线/系统 = 16MB 配置空间。

4 由于 x86 CPU 不能直接访问配置空间,因此必须通过 IO 寄存器进行索引来间接访问(尽管在 PCI Express 中,通过将配置空间映射到内存地址空间引入了一种新的访问配置空间的方法)。图 1-10(第 26 页)中显示的遗留模型使用位于地址 CF8h-CFBh 的
IO 端口(称为配置地址端口)以及映射到地址 CFCh-CFFh 的配置数据端口。有关此方法以及访问配置空间的内存映射方法的详细信息将在下一节中说明。

5 **25** 

6 **PCI Express Technology** 

7 _Figure 1-10: Address Space Mapping_ 

8 <img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0102.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-4"></a>
## 2.4 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Configuration Cycle Generation** 

Since IO address space is limited, the legacy model was designed to be very conservative with addresses. The common way of doing that in IO
space was to have one register for pointing to an internal location, and a second one for read‐ ing or writing the data. In PCI
configuration that involves two steps.

Step 1: The CPU generates an IO write to the Address Port at IO address CF8h in the North Bridge to give the address of the configuration
register to be accessed. This address, shown in Figure 1‐11 on page 27, consists primarily of the three things that locate a PCI function
within the topology: which bus we want to access out of the 256 possible, which device on that bus out of the 32 possible, and which
function within that device out of the 8 possible. The only other information needed is to identify which of the 64 dwords (256 bytes) in
that function’s configuration space is to be accessed.
Step 2: The CPU generates either an IO read or IO write to the Data Port at loca‐ tion CFCh in the North Bridge. Based on that, the North
Bridge then generates a configuration read or configuration write transaction to the PCI bus specified in the Address Port.

_Figure 1‐11: Configuration Address Register_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0103.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
<td width="50%">

## **PCI 配置周期的生成** 

由于 IO 地址空间有限，传统模型在地址使用上被设计得非常保守。在 IO 空间中的常见做法是使用一个寄存器来指向内部位置，再用另一个寄存器来读取或写入数据。在 PCI 配置中，这需要两个步骤。 

步骤 1：CPU 在北桥（North Bridge）的 IO 地址 CF8h 处生成一次 IO 写操作，以给出待访问配置寄存器的地址。如第 27 页图 1-11 所示，该地址主要由三个用于在拓扑中定位 PCI 功能（Function）的字段组成：256
条可能总线中要访问的总线号、该总线上 32 个可能的设备号、以及该设备上 8 个可能的功能号。唯一还需要的信息是标识该功能配置空间中 64 个双字（256 字节）中的哪一个要被访问。

**第 1 章：背景** 

步骤 2：CPU 在北桥的 CFCh 位置处对数据端口（Data Port）执行一次 IO 读或 IO 写操作。基于此，北桥随后向地址端口所指定的 PCI 总线生成一个配置读或配置写事务。 

_图 1-11：配置地址寄存器_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0104.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-5"></a>
## 2.5 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Function Configuration Register Space** 

Each PCI function contains up to 256 bytes of configuration space. The first 64 bytes of each functionʹs configuration space contains a
structure called the Header, while the remaining 192 Bytes support optional functionality. System configuration is first performed by Boot
ROM firmware. After the OS loads, it may reconfigure the system and rearrange resource assignments, with the result that the process of
system configuration may be done twice.

There are two basic classes of PCI functions as defined by their header types. A Type 1 header identifies a function that is a bridge (as
shown in Figure 1‐12 on page 28) and creates another bus in the topology, while a Type 0 header indi‐ cates a function that is NOT a bridge
(as shown in Figure 1‐13 on page 29). This header type information is contained in a field by the same name in dword 3, byte 2, and should
be one of the first things software checks when discovering which functions exist in the system (a process called “enumeration”).

</td>
<td width="50%">

## **PCI 功能配置寄存器空间** 

每个 PCI 功能最多包含 256 字节的配置空间。每个功能配置空间的前 64 字节包含一个称为"头部 (Header)"的结构，其余 192 字节用于支持可选功能。系统配置首先由 Boot ROM
固件执行。操作系统加载后，可能会重新配置系统并重新分配资源，因此系统配置的过程可能会被执行两次。

根据头部类型，PCI 功能分为两个基本类别。Type 1 头部标识该功能是一个桥 (Bridge)（如第 28 页的图 1-12 所示），它会在拓扑 (Topology) 中创建另一条总线；而 Type 0 头部标识该功能不是桥 (Bridge)（如第 29 页的图 1-13
所示）。该头部类型信息位于 dword 3、byte 2 中一个同名字段里，应当是软件在发现系统中存在哪些功能（这个过程称为"枚举 (Enumeration)"）时首先检查的内容之一。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-6"></a>
## 2.6 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 1‐12: PCI Configuration Header Type 1 (Bridge)_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0105.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>
_Figure 1‐13: PCI Configuration Header Type 0 (not a Bridge)_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0106.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

Details of the configuration register space and the enumeration process are described later. For now we simply want you to become familiar
with the big picture of how all the parts fit together.

</td>
<td width="50%">

## **PCI Express 技术**

_图 1‐12：PCI 配置头类型 1（桥）_

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0107.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

**第 1 章：背景**

_图 1‐13：PCI 配置头类型 0（非桥）_

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0108.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

配置寄存器空间的详细内容和枚举过程将在后面描述。现在，我们只是想让你熟悉所有这些部分如何组合在一起的全局概览。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-7"></a>
## 2.7 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Higher-bandwidth PCI** 

To support higher bandwidth, the PCI specification was updated to support both wider (64‐bit) and faster (66 MHz) versions, achieving 533
MB/s. Figure 1‐ 14 shows an example of a 66 MHz, 64‐bit PCI system.

</td>
<td width="50%">

## **更高带宽的 PCI** 

为了支持更高的带宽，PCI 规范进行了更新，同时支持更宽的（64 位）和更快的（66 MHz）版本，从而达到 533 MB/s 的带宽。图 1‐14 展示了一个 66 MHz、64 位 PCI 系统的示例。 

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-8"></a>
## 2.8 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 1‐14: 66 MHz PCI Bus Based Platform_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0109.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
<td width="50%">

## **PCI Express 技术** 

_图 1-14：基于 66 MHz PCI 总线的平台_ 

**==> 图片 [384 x 260] 已刻意省略 <==**

**----- 图片文字开始 -----**<br>
处理器 处理器<br>FSB（前端总线）<br>AGP<br>4x<br>GFX（图形显示）<br>RDRAM<br>内存控制器集线器<br>P64H (Intel 860 MCH)<br>插槽 PCI-66MHz 集线器接口 RDRAM<br>P64H<br>集线器接口
插槽<br>IDE<br>PCI-33MHz<br>CD HDD<br>USB 2.0 IO 控制器集线器<br>(ICH2) IEEE SCSI<br>LPC 1394<br>Super AC'97<br>IO 接口<br>COM1 Modem Audio
Boot<br>COM2 Codec Codec Ethernet ROM（启动 ROM）<br>**----- 图片文字结束 -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-9"></a>
## 2.9 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Limitations of 66 MHz PCI bus** 

While the throughput of the bus was doubled at this speed relative to the 33 MHz bus, the diagram illustrates one of its major shortcomings:
using the same reflected‐wave switching model with only half the timing budget meant that the loading on the bus had to be greatly reduced.
The result was that only one add‐in card could be supported on each bus. Adding more device meant add‐ ing more PCI bridges and buses would
increases both cost and board real estate requirements. The 64‐bit PCI bus increases pin count, increasing system cost and lowered system
reliability. In combination, it’s easy to see why these factors limited the popularity of 64‐bit or 66 MHz version of PCI bus.
</td>
<td width="50%">

## **66 MHz PCI 总线的局限性** 

虽然在此速率下总线的吞吐量相对于 33 MHz 总线翻了一番，但该图说明了其主要缺点之一：仍然采用反射波开关模型，而时序预算却减半，这意味着总线上的负载必须大幅减少。其结果是每条总线上只能支持一块扩展卡。若要增加更多设备，就需要增加更多的 PCI
桥和总线，这会同时增加成本和板卡空间需求。64 位 PCI 总线增加了引脚数，提高了系统成本并降低了系统可靠性。综合来看，很容易理解为何这些因素限制了 64 位或 66 MHz 版本 PCI 总线的普及。

**第 1 章：背景**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-10"></a>
## 2.10 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Signal Timing Problems with the Parallel PCI Bus Model beyond 66 MHz** 

PCI bus clock frequency cannot be increased beyond 66MHz given the realistic loads that exist on a PCI bus and signal flight times. With a
66 MHz clock, the clock period is 15 ns. Setup time allocated at the receiver is 3 ns. With the PCI “non‐registered input” signal bus model,
reducing signal setup time below this 3 ns value is not realistic. The rest of the 12 ns timing budget is allocated towards output delays at
the transmitter and signal flight time. Clocking PCI bus any faster than 66 MHz implies reducing clock period. A transmitted signal will not
be received in time enough to be sampled at the receiver.

The PCI‐X bus introduced in the next section takes the approach of registering all input signals with a Flip‐Flop before using them. Doing
so reduced signal setup time to below 1 ns. The setup time savings of PCI setup time allows PCI‐X bus to be run at higher frequencies of 100
MHz or even 133 Mhz. In the next sec‐ tion, we describe PCI‐X bus architecture briefly.

</td>
<td width="50%">

## **并行 PCI 总线模型在 66 MHz 以上的信号时序问题**

考虑到 PCI 总线上实际存在的负载以及信号飞行时间，PCI 总线的时钟频率无法提高到 66 MHz 以上。当时钟频率为 66 MHz 时，时钟周期为 15 ns。接收端分配的建立时间为 3 ns。在 PCI"非寄存器输入"信号总线模型下，将信号建立时间压缩到低于 3 ns
的值是不现实的。剩余的 12 ns 时序预算则分配给发送端的输出延迟以及信号飞行时间。如果将 PCI 总线的时钟频率提高到 66 MHz 以上，就意味着要缩短时钟周期，而发送的信号将无法及时到达接收端以供其采样。

下一节将要介绍的 PCI-X 总线采用了在使用所有输入信号之前，先用触发器（Flip-Flop）将其寄存的方法。这样做将信号建立时间减少到了 1 ns 以下。PCI 建立时间的节省使得 PCI-X 总线能够运行在 100 MHz 甚至 133 MHz
的更高频率下。下一节我们将简要介绍 PCI-X 总线架构。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-11"></a>
## 2.11 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Introducing PCI-X** 

PCI‐X is backward compatible with PCI in both hardware and software, but provides better performance and higher efficiency. It uses the same
connector format, so PCI‐X devices can be plugged into PCI slots and vice‐versa. And it uses the same configuration model, so device
drivers, operating systems, and applications that run on a PCI system also run on a PCI‐X system.

To achieve higher speeds without changing the PCI signaling model, PCI‐X added a few tricks to improve the bus timing. First, they implement
PLL (phase‐locked loop) clock generators that provide phase‐shifted clocks inter‐ nally. That allows the outputs to be driven a little
earlier and the inputs to be sampled a little later, improving the timing on the bus. Likewise, PCI‐X inputs are registered (latched) at the
input pin of the target device, resulting in shorter setup times. The time gained by these means increased the time available for signal
propagation on the bus and allowed higher clock frequencies.

</td>
<td width="50%">

1 ## **介绍 PCI-X** 

2 PCI-X 在硬件和软件上与 PCI 向后兼容,但提供更好的性能和更高的效率。它使用相同的连接器格式,因此 PCI-X 设备可以插入 PCI 插槽,反之亦然。它使用相同的配置模型,因此在 PCI 系统上运行的设备驱动程序、操作系统和应用程序也可以在 PCI-X 系统上运行。 

3 为了在不更改 PCI 信令模型的情况下实现更高的速度,PCI-X 添加了一些技巧来改进总线时序。首先,他们实现了 PLL(锁相环)时钟发生器,在内部提供相移时钟。这允许输出稍早驱动,输入稍晚采样,从而改善总线上的时序。同样,PCI-X
输入在目标设备的输入引脚处被寄存(锁存),从而导致更短的建立时间。通过这些方式获得的时间增加了总线上信号传播的可用时间,并允许更高的时钟频率。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-12"></a>
## 2.12 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI-X System Example** 

An example of an Intel 7500 server chipset‐based system is shown in Figure 1‐15 on page 32. The MCH chip includes three additional
high‐performance Hub Link 2.0 ports that are connected to three PCI‐X Hub 2 bridges (P64H2). Each

bridge supports two PCI‐X buses that can run at frequencies up to 133MHz. The Hub Link 2.0 can sustain the higher bandwidth requirements for
PCI‐X traffic. Note that we have the same loading problem that we did for 66‐MHz PCI, resulting in a large number of buses needed to support
more devices and a rela‐ tively expensive solution. The bandwidth is much higher now, though.

_Figure 1‐15: 66 MHz/133 MHz PCI‐X Bus Based Platform_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0110.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
<td width="50%">

## **PCI-X 系统示例**

基于 Intel 7500 服务器芯片组的一个系统示例如第 32 页的图 1-15 所示。MCH 芯片包含三个额外的高性能 Hub Link 2.0 端口，这三个端口分别连接到三个 PCI-X Hub 2 桥 (P64H2)。每个

桥支持两条 PCI-X 总线，这些总线可以运行在最高 133MHz 的频率下。Hub Link 2.0 能够维持 PCI-X 流量所需的更高带宽需求。需要注意的是，我们遇到了与 66 MHz PCI
相同的负载问题，导致需要大量的总线来支持更多的设备，并且解决方案相对昂贵。不过现在的带宽要高得多了。

_图 1-15：基于 66 MHz/133 MHz PCI-X 总线的平台_

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0111.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-13"></a>
## 2.13 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI-X Transactions** 

Figure 1‐16 on page 33 shows an example of a PCI‐X burst memory read trans‐ action. Note that PCI‐X does not allow Wait States after the
first data phase. This is possible because the transfer size is now provided to the target device in the Attribute phase of the transaction,
so the target devices knows exactly what is going to be required of him. In addition, most PCI‐X bus cycles are bursts and data is generally
transferred in blocks of 128 Bytes. These features allow for more efficient bus utilization and device buffer management.
_Figure 1‐16: Example PCI‐X Burst Memory Read Bus Cycle_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0112.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
<td width="50%">

## **PCI-X 事务**

第 33 页的图 1‐16 显示了一个 PCI‐X 突发内存读事务的示例。请注意，PCI‐X 不允许在第一个数据相位之后插入等待状态。这是可行的，因为传输大小现在已在事务的 Attribute（属性）相位中提供给目标设备，所以目标设备确切地知道对其有什么要求。此外，大多数
PCI‐X 总线周期都是突发传输，并且数据通常以 128 字节块的形式传输。这些特性可以更高效地利用总线，并更好地管理设备缓冲。

**第 1 章：背景**

_图 1‐16：PCI‐X 突发内存读总线周期示例_

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0113.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-14"></a>
## 2.14 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI-X Features**

</td>
<td width="50%">

## **PCI-X 特性 (PCI-X Features)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-15"></a>
## 2.15 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Split-Transaction Model** 

In a conventional PCI read transaction, the Bus Master initiates a read to a target device on the bus. As described earlier, if the target
is unprepared to finish the transaction it can either hold the bus with Wait States while fetching the data, or issue a Retry in the process
of a Delayed Transaction.

PCI‐X bus uses a Split Transaction to handle these cases, as illustrated in Figure 1‐17 on page 34. To help keep track of what each device
is doing, the device ini‐ tiating the read is now called the Requester, and the device fulfilling the read request is called the Completer.
If the completer is unable to service the request immediately, it memorizes the transaction (address, transaction type, byte count,
requester ID) and signals a split response. This tells the requester to put this transaction aside in a queue, end the current bus cycle,
and release the bus to the idle state. That makes the bus available for other transactions while the completer is awaiting the requested
data. The requester is free to do whatever it

</td>
<td width="50%">

## **分割事务模型** 

在传统的 PCI 读事务中,总线主设备 (Bus Master) 向总线上的目标设备发起一次读操作。如前所述,如果目标设备尚未准备好完成该事务,它既可以在取数据的过程中通过等待状态 (Wait States) 占用总线,也可以在"延迟事务" (Delayed
Transaction) 的过程中发出 Retry (重试)。

PCI‐X 总线使用分割事务 (Split Transaction) 来处理这些情况,如图 1‐17 (第 34 页) 所示。为了便于跟踪每个设备正在执行的操作,发起读操作的设备现在称为"请求者" (Requester),而满足该读请求的设备则称为"完成者"
(Completer)。如果完成者无法立即响应该请求,它会记忆该事务(地址、事务类型、字节数、请求者 ID),并发出一个分割响应 (Split
Response)。这告诉请求者将该事务放到一边排入队列,结束当前的总线周期,并将总线释放到空闲状态。这样,当完成者正在等待所请求的数据时,总线就可用于其他事务。请求者可以自由地做任何

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-16"></a>
## 2.16 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

likes while it waits for the completer, such as initiating other requests, even to the same completer. Once the completer has gathered the
requested data, it then arbitrates for ownership of the bus and initiates a split completion during which it returns the requested data. The
requester claims the split completion bus cycle and accepts the data from the completer. The split completion looks very much like a write
transaction to the system. This Split Transaction Model is pos‐ sible because not only does the request indicate how much data they are
requesting in the Attribute phase, but they also indicate who they are (their Bus:Device:Function number) which allows the completer to
target the correct device with the completion.

Two bus transactions are needed to complete the entire data transfer, but between the read request and the split completion the bus is
available for other work. The requester does not need to poll the device with retries to learn when the data is ready. The completer simply
arbitrates for the bus and drives the requested data back when it is ready. This makes for a much more efficient transaction model in terms
of bus utilization.

These protocol enhancements made to the PCI‐X bus architecture described so far contribute towards an increased transfer efficiency of
around 85% for PCI‐X as compared to 50%‐60% with the standard PCI protocol.

_Figure 1‐17: PCI‐X Split Transaction Protocol_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0114.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

</td>
<td width="50%">

## **PCI Express Technology** 

likes while it waits for the completer, such as initiating other requests, even to the same completer. Once the completer has gathered the
requested data, it then arbitrates for ownership of the bus and initiates a split completion during which it returns the requested data. The
requester claims the split completion bus cycle and accepts the data from the completer. The split completion looks very much like a write
transaction to the system. This Split Transaction Model is pos‐ sible because not only does the request indicate how much data they are
requesting in the Attribute phase, but they also indicate who they are (their Bus:Device:Function number) which allows the completer to
target the correct device with the completion.

Two bus transactions are needed to complete the entire data transfer, but between the read request and the split completion the bus is
available for other work. The requester does not need to poll the device with retries to learn when the data is ready. The completer simply
arbitrates for the bus and drives the requested data back when it is ready. This makes for a much more efficient transaction model in terms
of bus utilization.

These protocol enhancements made to the PCI‐X bus architecture described so far contribute towards an increased transfer efficiency of
around 85% for PCI‐X as compared to 50%‐60% with the standard PCI protocol.

</td>
</tr></tbody></table>

<p align="center"><b>Figure 1‐17: PCI‐X Split Transaction Protocol</b></p>
<p align="center"><img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0115.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_02_PCIe_Architecture_Overview/page/page0115.png">Page 115</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-17"></a>
## 2.17 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Message Signaled Interrupts** 

PCI‐X devices require MSI (Message Signaled Interrupt) capability, which was developed as a way to reduce or eliminate the need to share
interrupts across multiple devices as was typically required in the legacy interrupt architecture.
To generate an interrupt request using MSI, a device initiates a memory write transaction using a pre‐defined address range that is
understood to be an inter‐ rupt which should be delivered to one of more CPUs, and the data is a unique interrupt vector associated with
that device. The CPU, armed with the interrupt number, is able to immediately jump to the interrupt service routine for the device and
avoids the overhead associated with finding which device generated the interrupt. In addition, no sideband pins are needed.

</td>
<td width="50%">

## **消息信号中断**

PCI‐X 设备要求具备 MSI（消息信号中断，Message Signaled Interrupt）能力，该机制的提出是为了减少或消除在传统中断架构中通常所需的多设备共享中断的需求。

**第 1 章：背景**

要使用 MSI 产生中断请求，设备会使用一个预定义的地址范围发起存储器写事务，该地址范围被理解为应被递送至一个或多个 CPU 的中断，而数据则是与该设备关联的唯一中断向量。CPU
获取中断号后，便能立即跳转到该设备的中断服务例程，从而避免了为确定是哪个设备产生中断而带来的开销。此外，无需额外的边带引脚。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-18"></a>
## 2.18 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Transaction Attributes** 

Finally, PCI‐X also added another phase to the beginning of each transaction called the Attribute Phase (see Figure 1‐16 on page 33). In
this time slot the requester delivers information that can be used to help improve the efficiency of transactions on the bus, such as the
byte count for this request and who the requester is (Bus:Device:Function number). In addition to those items, two new bits were added to
help characterize this transaction: the ʺNo Snoopʺ bit and the ʺRelaxed Orderingʺ bit.

**No Snoop (NS):** Normally, when a transaction moves data into or out of memory, the CPU’s internal caches need to be checked to see if
that memory location has been copied into one or more CPU caches. If so, the cache contents may need to be written back to memory or
invalidated before the requested transaction is allowed to access memory. Naturally, this snoop process takes time and adds latency to a
request. Sometimes the software is aware that a requested location will never be found in the CPU caches (perhaps because the location was
defined by the system as uncacheable), so snooping is unnecessary and that step could be skipped. The No Snoop bit was added with precisely
that case in mind.

**Relaxed Ordering (RO):** Normally, transactions are required to remain in the same order that they were issued on the bus while they go
through buffers in bridges. This is referred to as the Strongly Ordered model, and PCI and PCI‐ X generally follow that rule with a few
exceptions. That’s because it helps resolve dependencies among transactions that are related to each other, such as writing and then reading
the same location. However, not all transactions actu‐ ally have dependencies. If they don’t, then forcing them to stay in order can result
in loss of performance, and that’s what this bit was designed to alleviate. If the requester knows that a particular transaction is
unrelated to the other transactions that have gone before, it can set this bit to tell bridges that this transaction is allowed to jump
ahead in the queue to give better performance.

</td>
<td width="50%">

## **事务属性 (Transaction Attributes)**

最后，PCI-X 还在每个事务的开始处增加了一个新的相位，称为属性相位 (Attribute Phase)（参见第 33 页的图 1-16）。在这个时间槽内，请求者提供一些信息，可用于帮助提高总线上事务的效率，例如本次请求的字节数以及请求者是谁（总线:设备:功能号，即
Bus:Device:Function）。除这些信息外，还新增了两个比特来进一步刻画该事务的特性：即 "No Snoop"（无监听）位和 "Relaxed Ordering"（宽松排序）位。

**No Snoop (NS, 无监听)：** 通常，当某个事务将数据搬入或搬出内存时，需要检查 CPU 的内部缓存，以确定该内存位置是否已被复制到某一个或多个 CPU 缓存中。如果是的话，可能需要先将缓存内容写回内存 (write back) 或使其失效
(invalidate)，然后才允许所请求的事务访问内存。显然，这个监听 (snoop) 过程会消耗时间，并给请求带来额外的延迟。有时软件知道所请求的位置永远不会被缓存到 CPU 缓存中（例如该位置已被系统定义为不可缓存），此时监听过程是不必要的，可以跳过。No Snoop
位的引入正是针对这种情形。

**Relaxed Ordering (RO, 宽松排序)：** 通常情况下，事务在穿过桥 (Bridge) 中的缓冲区时，必须保持其在总线上发出时的相同顺序。这被称为强排序 (Strongly Ordered) 模型，PCI 和 PCI-X
在一些例外之外大体遵循这一规则。这是因为强排序有助于解决相互关联的事务之间的依赖关系，例如先写后读同一位置。然而，并非所有事务之间都真正存在依赖关系。如果事务之间没有依赖，强制其保持顺序则会导致性能损失，这正是 RO
位设计用来缓解的问题。如果请求者知道某个特定事务与此前的其他事务没有关联，便可以置起该位以告知桥：本事务允许在队列中跳到前面，从而获得更好的性能。

**PCI Express 技术**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-19"></a>
## 2.19 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Higher Bandwidth PCI-X**

</td>
<td width="50%">

## **更高带宽的 PCI-X (Higher Bandwidth PCI-X)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-20"></a>
## 2.20 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Problems with the Common Clock Approach of PCI and PCI-X 1.0 Parallel Bus Model** 

An issue that becomes clear when trying to migrate a bus like PCI to higher speeds is that parallel bus designs have some inherent
limitations. Figure 1‐18 on page 36 helps illustrate these. These designs use a common or distributed clock, in which data is driven out on
one clock edge and latched in on the next clock edge so that the total timing budget is the time for one clock period. Natu‐ rally, the
higher the frequency, the smaller the clock period and thus the smaller the timing budget.

_Figure 1‐18: Inherent Problems in a Parallel Design_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0116.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

The first issue to note is signal skew. When multiple data bits are sent at once, they experience slightly different delays and arrive at
slightly different times at the receiver. If that difference is too large, incorrect signal sampling with clock may occur at the receiver as
shown in the diagram. A second issue is clock skew between multiple devices. The arrival time of the common clock at one device is not
precisely the same as the arrival time at the other which further reduces the timing budget. Finally, a third issue relates to the time it
takes for the signal to
propagate from a transmitter to a receiver, called the flight time. The clock period or timing budget must be greater than the signal flight
time. To ensure this, the board design is required to implement signal traces that are short enough such that signal propagation delays are
smaller than the clock period. In many board designs, this short signal traces may not be realistic enough to design for.

To further improve performance in spite of these limitations, a couple of tech‐ niques can be used. First, the existing protocol can be
streamlined and made more efficient. And second, the bus model can be changed to a source synchro‐ nous clocking model where the bus signal
and clock (strobe) are driven at the same time on signals that experience equal propagation delay. This is the approach taken by PCI‐X 2.0
protocol.

</td>
<td width="50%">

## **PCI 与 PCI-X 1.0 并行总线模型共同时钟方式存在的问题**

在试图将 PCI 之类的总线迁移到更高速度时,一个明显的问题在于并行总线设计存在一些固有的局限性。第 36 页的图 1-18
有助于说明这些问题。这些设计采用共同时钟或分布式时钟,数据在一个时钟边沿驱动输出,在下一个时钟边沿被锁存采样,因此总的时间预算为一个时钟周期的时间。自然而然,频率越高,时钟周期越小,从而时间预算也越小。

_图 1-18:并行设计中的固有问题_

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0117.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

首先需要注意的问题是信号偏斜(Signal
Skew)。当多个数据位同时发送时,它们经历的延迟略有不同,到达接收器的时间也略有差异。如果这种差异过大,如图所示,接收器处可能发生错误的时钟采样。第二个问题是多个设备之间的时钟偏斜。共同时钟到达一个设备的时刻与到达另一个设备的时刻并不精确相同,这进一步减少了时间预算。第三个问题涉及信号从发送器传播到接收器所需的时间,称为飞行时间(Flight
Time)。时钟周期或时间预算必须大于信号飞行时间。为确保这一点,板级设计需要实现足够短的信号走线,使信号传播延迟小于时钟周期。在许多板级设计中,这种短信号走线在设计时可能并不现实。

**Chapter 1: Background**(第 1 章:背景)

为了在存在这些限制的情况下进一步提高性能,可以采用若干技术。首先,可以对现有协议进行精简和优化以提高效率。其次,可以将总线模型改为源同步时钟模型,即总线信号与时钟(选通信号)在经历相同传播延迟的信号线上同时驱动。PCI-X 2.0 协议即采用了这一方法。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-21"></a>
## 2.21 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI-X 2.0 Source-Synchronous Model** 

PCI‐X 2.0 further increased the bandwidth of PCI‐X. As before, the devices and connectors remained hardware and software backward compatible
with PCI devices and connectors. To achieve the higher speeds, the bus uses a source‐ synchronous delivery model to support either Dual Data
Rate (DDR) or Quad Data Rate (QDR).

The term “source synchronous” means that the device transmitting the data also provides another signal that travels the same basic path as
the data. As illustrated in Figure 1‐19 on page 38, that signal in PCI‐X 2.0 is called a “strobe” and is used by the receiver for latching
the incoming data bits. The transmitter assigns the timing relationship between the data and strobe and as long as their paths are similar
in length and other characteristics that can affect transmission latency, that relationship will be about the same when they arrive at the
receiver and the receiver can simply use the Strobe as the signal to latch the data in with. This allows higher speeds because clock skew
with respect to the common clock is removed as a separate budget item and because the issue of flight time goes away. It no longer matters
how long it takes for the data to travel from point A to point B because the strobe that latches it in takes about the same time and so
their relationship will be unaffected.

It’s important to note again that the very high‐speed signal timing eliminates the possibility of using a shared‐bus model and forces a
point‐to‐point design instead. As a result, increasing the number of devices means more bridges will be needed to create more buses. A
device could be designed to support this with three interfaces and an internal bridge structure to allow them all to com‐ municate with each
other. Such a device would have a very high pin count, though, and a higher cost, relegating PCI‐X 2.0 to the very high‐end market.

</td>
<td width="50%">

## **PCI-X 2.0 源同步模型** 

PCI‐X 2.0 进一步提升了 PCI‐X 的带宽。与以往一样，设备和连接器在硬件和软件上仍然向后兼容 PCI 设备和连接器。为了实现更高的速度，总线采用源同步传输模型来支持双倍数据速率（DDR）或四倍数据速率（QDR）。

"源同步"一词意味着发送数据的设备还会提供另一个信号，该信号沿与数据基本相同的路径传输。如第 38 页的图 1‐19 所示，PCI‐X 2.0
中的这个信号被称为"选通信号（strobe）"，由接收器用于锁存传入的数据位。发送器负责确定数据与选通信号之间的时序关系，只要它们的路径在长度以及其他可能影响传输延迟的特性方面大致相同，那么这种关系在到达接收器时也将基本保持一致，接收器只需使用选通信号作为锁存数据的信号即可。这之所以能够支持更高的速度，是因为相对于公共时钟的时钟偏斜不再作为单独的预算项，同时飞行时间的问题也得以消除。数据从
A 点传输到 B 点需要多长时间已经不再重要，因为锁存数据的选通信号几乎需要相同的时间，因此它们之间的关系不会受到影响。

需要再次强调的是，这种非常高速的信号时序排除了使用共享总线模型的可能性，迫使设计采用点对点架构。因此，增加设备数量意味着需要更多的桥 (Bridge) 来构建更多的总线。一个设备可以通过设计三个接口和内部桥接结构来支持这一点，从而允许它们彼此通信。然而，这样的设备引脚 (Pin)
数量会非常多，成本也更高，这使得 PCI‐X 2.0 仅适用于高端市场。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-22"></a>
## 2.22 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

Since it was recognized that this would be an expensive solution that would appeal more to high‐end designers, PCI‐X 2.0 also supports ECC
generation and checking. ECC is much more robust and sophisticated than parity detec‐ tion, allowing automatic correction of single‐bit
errors on the fly, and robust detection of multi‐bit errors. This improved error handling adds cost, but high‐ end platforms need the
improved reliability it provides, hence a logical choice.

_Figure 1‐19: Source‐Synchronous Clocking Model_ 

<img src="figures/chapter_02_PCIe_Architecture_Overview/page/page0118.png" alt="Figure 1‐9: PCI Error Handling" width="700">

<br>

Despite the improvements in bandwidth, efficiency and reliability that came with PCI‐X (2.0), the parallel bus model was approaching its end
of life and a new model was needed to address the relentless demand for higher bandwidth and lower cost. The new model chosen was a serial
interface which is a drasti‐ cally different bus from a physical perspective, but was still made to be software backwards compatible. We
know this new model as PCI Express.

</td>
<td width="50%">

## **PCI Express 技术**

由于人们认识到这将是一个昂贵的解决方案,更受高端设计人员的青睐,PCI‐X 2.0 还支持 ECC 生成和校验。ECC
比奇偶校验检测更加强大和复杂,可以自动即时纠正单位错误,并能可靠地检测多位错误。这种改进的错误处理增加了成本,但高端平台需要其所提供的更高可靠性,因此这是一个合乎逻辑的选择。

_图 1‐19:源同步时钟模型_

**==> 图片 [374 x 172] 故意省略 <==**

**----- 图片文字开始 -----**<br>
数据<br>D Q<br>数据<br>D Q<br>数据<br>D Q<br>选通<br>源设备 接收设备<br>
**----- 图片文字结束 -----**<br>

尽管 PCI‐X (2.0) 在带宽、效率和可靠性方面都有了改进,但并行总线模型已接近其生命周期的尽头,需要一种新的模型来满足对更高带宽和更低成本的无止境需求。所选择的新模型是一种串行接口,从物理角度看它与之前的总线截然不同,但在软件上仍保持向后兼容。我们将这个新模型称为 PCI
Express。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-23"></a>
## 2.23 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## _**2 PCIe Architecture Overview**_

</td>
<td width="50%">

## _**2 PCIe 架构概述 (PCIe Architecture Overview)**_

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-24"></a>
## 2.24 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Previous Chapter** 

The previous chapter provided historical background to establish a foundation for understanding PCI Express. This included reviewing the
basics of PCI and PCI‐X 1.0/2.0. The goal was to provide a context for the overview of PCI Express that follows.

</td>
<td width="50%">

## **上一章** 

上一章提供了历史背景，以便为理解 PCI Express 奠定基础。这其中包括回顾 PCI 和 PCI‐X 1.0/2.0 的基础知识。其目标是为接下来对 PCI Express 的概述提供相应的上下文。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-25"></a>
## 2.25 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **This Chapter** 

This chapter provides a thorough introduction to the PCI Express architecture and is intended to serve as an “executive level” overview,
covering all the basics of the architecture at a high level. It introduces the layered approach given in the spec and describes the
responsibilities of each layer. The various packet types are introduced along with the protocol used to communicate them and facilitate
reliable transmission.

</td>
<td width="50%">

## **本章内容** 

本章对 PCI Express 架构进行了全面的介绍,旨在作为一份"高管级"的概览文档,从较高层次覆盖架构的所有基础知识。文中将介绍规范所定义的分层方法,并描述每一层所承担的职责。文中还将介绍各种类型的包,以及用于传输这些包并实现可靠传输的协议。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-2-26"></a>
## 2.26 PCIe Architecture Overview | PCIe 架构概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **The Next Chapter** 

The next chapter provides an introduction to configuration in the PCI Express environment. This includes the space in which a Function’s
configuration regis‐ ters are implemented, how a Function is discovered, how configuration transac‐ tions are generated and routed, the
difference between PCI‐compatible space and PCIe extended space, and how software differentiates between an Endpoint and a Bridge.

</td>
<td width="50%">

## **下一章**

下一章将介绍 PCI Express 环境中的配置 (Configuration)。内容包括：实现 Function 配置寄存器的地址空间、Function 的发现 (Discovery) 方式、配置事务 (Configuration Transaction)
的生成与路由、PCI 兼容空间 (PCI-Compatible Space) 与 PCIe 扩展空间 (Extended Configuration Space) 之间的差异，以及软件如何区分端点 (Endpoint) 与桥 (Bridge)。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
