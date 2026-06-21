# 📘 第 3 章　配置概述 (Chapter 3. Configuration Overview)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0139.md` ... `chunks/chunk0169.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [3.1 Configuration Overview — 配置概述](#sec-3-1)
- [3.2 Configuration Overview — 配置概述](#sec-3-2)
- [3.3 Configuration Overview — 配置概述](#sec-3-3)
- [3.4 Configuration Overview — 配置概述](#sec-3-4)
- [3.5 Configuration Overview — 配置概述](#sec-3-5)
- [3.6 Configuration Overview — 配置概述](#sec-3-6)
- [3.7 Configuration Overview — 配置概述](#sec-3-7)
- [3.8 Configuration Overview — 配置概述](#sec-3-8)
- [3.9 Configuration Overview — 配置概述](#sec-3-9)
- [3.10 Configuration Overview — 配置概述](#sec-3-10)
- [3.11 Configuration Overview — 配置概述](#sec-3-11)
- [3.12 Configuration Overview — 配置概述](#sec-3-12)
- [3.13 Configuration Overview — 配置概述](#sec-3-13)
- [3.14 Configuration Overview — 配置概述](#sec-3-14)
- [3.15 Configuration Overview — 配置概述](#sec-3-15)
- [3.16 Configuration Overview — 配置概述](#sec-3-16)
- [3.17 Configuration Overview — 配置概述](#sec-3-17)
- [3.18 Configuration Overview — 配置概述](#sec-3-18)
- [3.19 Configuration Overview — 配置概述](#sec-3-19)
- [3.20 Configuration Overview — 配置概述](#sec-3-20)
- [3.21 Configuration Overview — 配置概述](#sec-3-21)
- [3.22 Configuration Overview — 配置概述](#sec-3-22)
- [3.23 Configuration Overview — 配置概述](#sec-3-23)
- [3.24 Configuration Overview — 配置概述](#sec-3-24)
- [3.25 Configuration Overview — 配置概述](#sec-3-25)
- [3.26 Configuration Overview — 配置概述](#sec-3-26)
- [3.27 Configuration Overview — 配置概述](#sec-3-27)
- [3.28 Configuration Overview — 配置概述](#sec-3-28)
- [3.29 Configuration Overview — 配置概述](#sec-3-29)
- [3.30 Configuration Overview — 配置概述](#sec-3-30)
- [3.31 Configuration Overview — 配置概述](#sec-3-31)

<a id="sec-3-1"></a>
## 3.1 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Introduction to PCI Express** 

PCI Express represents a major shift from the parallel bus model of its predeces‐ sors. As a serial bus, it has more in common with earlier
serial designs like InfiniBand or Fibre Channel, but it remains fully backward compatible with PCI in software.

</td>
<td width="50%">

## **PCI Express 简介**

PCI Express 代表了一次重大转变,摒弃了其前代产品所采用的并行总线模型。作为一种串行总线,它与早期的串行设计(如 InfiniBand 或 Fibre Channel)有更多相似之处,但在软件层面仍然与 PCI 完全向后兼容。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---


<img src="figures/embedded/page0177_img1_tight.png" alt="Figure from page 177" width="700">

<a id="sec-3-2"></a>
## 3.2 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

As is true of many high‐speed serial transports, PCIe uses a bidirectional con‐ nection and is capable of sending and receiving information
at the same time. The model used is referred to as a dual‐simplex connection because each inter‐ face has a simplex transmit path and a
simplex receive path, as shown in Figure 2‐1 on page 40. Since traffic is allowed in both directions at once, the communi‐ cation path
between two devices is technically full duplex, but the spec uses the term dual‐simplex because it’s a little more descriptive of the actual
communi‐ cation channels that exist.

_Figure 2‐1: Dual‐Simplex Link_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

The term for this path between the devices is a **Link** , and is made up of one or more transmit and receive pairs. One such pair is called
a **Lane** , and the spec allows a Link to be made up 1, 2, 4, 8, 12, 16, or 32 Lanes. The number of lanes is called the Link Width and is
represented as x1, x2, x4, x8, x16, and x32. The trade‐off regarding the number of lanes to be used in a given design is straight‐ forward:
more lanes increase the bandwidth of the Link but add to its cost, space requirement, and power consumption. For more on this, see “Links
and Lanes” on page 46.

_Figure 2‐2: One Lane_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>
</td>
<td width="50%">

## **PCI Express 技术** 

与许多高速串行传输协议一样,PCIe 使用双向连接,能够同时发送和接收信息。所采用的模型称为双单工 (dual-simplex) 连接,因为每个接口都具有一条单工发送路径和一条单工接收路径,如图 2-1 (第 40 页)
所示。由于两个方向同时允许流量传输,两个设备之间的通信路径在技术上是全双工的,但规范使用"双单工"这一术语,因为它更准确地描述了实际存在的通信通道。

_图 2-1:双单工链路_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

设备之间这条路径称为**链路 (Link)**,由一个或多个发送和接收对组成。每一对称为**通道 (Lane)**,规范允许一条链路包含 1、2、4、8、12、16 或 32 条通道。通道的数量称为链路宽度 (Link Width),用 x1、x2、x4、x8、x16 和 x32
表示。关于在特定设计中使用多少通道的权衡是直截了当的:更多的通道会增加链路的带宽,但同时也会增加其成本、空间占用和功耗。更多相关信息,请参阅第 46 页的"链路与通道"。

_图 2-2:一条通道_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

**第 2 章:PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-3"></a>
## 3.3 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Software Backward Compatibility** 

One of the most important design goals for PCIe was backward compatibility with PCI software. Encouraging migration away from a design that
is already installed and working in existing systems requires two things: First, a compel‐ ling improvement that motivates even considering
a change and, second, mini‐ mizing the cost, risk, and effort of changing. A common way to help this second factor in computers is to
maintain the viability of software written for the old model in the new one. To achieve this for PCIe, all the address spaces used for PCI
are carried forward either unchanged or simply extended. Memory, IO, and Configuration spaces are still visible to software and programmed
in exactly the same way they were before. Consequently, software written years ago for PCI (BIOS code, device drivers, etc.) will still work
with PCIe devices today. The configuration space has been extended dramatically to include many new regis‐ ters to support new
functionality, but the old registers are still there and still accessible in the regular way (see “Software Compatibility Characteristics”
on page 49).

</td>
<td width="50%">

## **软件向后兼容性** 

PCIe 最重要的设计目标之一是与 PCI
软件保持向后兼容。要推动用户从一种已经在现有系统中安装并正常运行的设计迁移,需要满足两个条件:第一,要有足够引人注目的改进,让人值得考虑更换;第二,要尽量降低更换所带来的成本、风险和投入。在计算机领域,帮助实现第二个因素的常见做法是让针对旧模型编写的软件在新模型中仍然可用。为了在
PCIe 上实现这一点,PCI 所使用的所有地址空间都被原封不动或仅仅加以扩展地继承了下来。内存空间 (Memory Space)、I/O 空间 (I/O Space) 和配置空间 (Configuration Space)
仍然对软件可见,并且其编程方式与之前完全相同。因此,多年前为 PCI 编写的软件(BIOS 代码、设备驱动程序等)如今仍然可以与 PCIe 设备配合工作。配置空间已经进行了大幅扩展,新增了许多寄存器以支持新功能,但原有的寄存器仍然存在,并且仍然可以以常规方式访问(参见第 49
页的"软件兼容性特性 (Software Compatibility Characteristics)")。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-4"></a>
## 3.4 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Serial Transport**

</td>
<td width="50%">

## **串行传输 (Serial Transport)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-5"></a>
## 3.5 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **The Need for Speed** 

Of course, a serial model must run much faster than a parallel design to accom‐ plish the same bandwidth because it may only send one bit at
a time. This has not proven difficult, though, and in the past PCIe has worked reliably at 2.5 GT/ s and 5.0 GT/s. The reason these and
still higher speeds (8 GT/s) are attainable is that the serial model overcomes the shortcomings of the parallel model.

**Overcoming Problems.** By way of review, there are a handful of problems that limit the performance of a parallel bus and three are
illustrated in Figure 2‐ 3 on page 42. To get started, recall that parallel buses use a common clock; out‐ puts are clocked out on one clock
edge and clocked into the receiver on the next edge. One issue with this model is the time it takes to send a signal from trans‐ mitter to
receiver, called the flight time. The flight time must be less than the clock period or the model won’t work, so going to smaller clock
periods is chal‐ lenging. To make this possible, traces must get shorter and loads reduced but eventually this becomes impractical. Another
factor is the difference in the arrival time of the clock at the sender and receiver, called clock skew. Board lay‐ out designers work hard
to minimize this value because it detracts from the tim‐ ing budget but it can never be eliminated. A third factor is signal skew, which is

the difference in arrival times for all the signals needed on a given clock. Clearly, the data can’t be latched until all the bits are ready
and stable, so we end up waiting for the slowest one.

_Figure 2‐3: Parallel Bus Limitations_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

How does a serial transport like PCIe get around these problems? First, flight time becomes a non‐issue because the clock that will latch
the data into the receiver is actually built into the data stream and no external reference clock is necessary. As a result, it doesn’t
matter how small the clock period is or how long it takes the signal to arrive at the receiver because the clock arrives with it at the same
time. For the same reason there’s no clock skew, again because the latching clock is recovered from the data stream. Finally, signal skew is
elimi‐ nated within a Lane because there’s only one data bit being sent. The signal skew problem returns if a multi‐lane design is used, but
the receiver corrects for this automatically and can fix a generous amount of skew. Although serial designs overcome many of the problems of
parallel models, they have their own set of complications. Still, as we’ll see later, the solutions are manageable and allow for high‐speed,
reliable communication.

**Bandwidth.** The combination of high speed and wide Links that PCIe sup‐ ports can result in some impressive bandwidth numbers, as shown
in Table 2‐1 on page 43. These numbers are derived from the bit rate and bus characteristics. One such characteristic is that, like many
other serial transports, the first two generations of PCIe use an encoding process called **8b/10b** that generates a 10‐ bit output based
on an 8‐bit input. In spite of the overhead this introduces, there are several good reasons for doing it as we’ll see later. For now it’s
enough to
know that sending one byte of data requires transmitting 10 bits. The first gen‐ eration (Gen1 or PCIe spec version 1.x) bit rate is 2.5
GT/s and dividing that by 10 means that one lane will be able to send 0.25 GB/s. Since the Link permits sending and receiving at the same
time, the aggregate bandwidth can be twice that amount, or 0.5 GB/s per Lane. Doubling the frequency for the second gener‐ ation (Gen2 or
PCIe 2.x) doubled the bandwidth. The third generation (Gen3 or PCIe 3.0) doubles the bandwidth yet again, but this time the spec writers
chose not to double the frequency. Instead, for reasons we’ll discuss later, they chose to increase the frequency only to 8 GT/s and remove
the 8b/10b encoding in favor of another encoding mechanism called **128b/130b** encoding (for more on this, see the chapter “Physical Layer
‐ Logical (Gen3)” on page 407). Table 2‐1 summarizes the bandwidth available for all the current possible combinations and shows the peak
throughput the Link could deliver in that configuration.

_Table 2‐1: PCIe Aggregate Gen1, Gen2 and Gen3 Bandwidth for Various Link Widths_ 

|**Link Width**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 Bandwidth**<br>**(GB /s)**|0.5|1|2|4|6|8|16|
|**Gen2 Bandwidth**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 Bandwidth**<br>**(GB/s)**|2|4|8|16|24|32|64|

</td>
<td width="50%">

## **对速度的需求** 

当然，串行模型必须比并行设计运行得快得多才能达到相同的带宽，因为它一次只能发送一个比特。不过这并不困难，过去 PCIe 已经在 2.5 GT/s 和 5.0 GT/s 速率下可靠地工作。之所以能达到这些乃至更高的速度（8 GT/s），是因为串行模型克服了并行模型的种种缺陷。 

**克服问题。** 回顾一下，限制并行总线性能的问题主要有几个，其中三个如图 2-3（第 42
页）所示。首先，回忆一下并行总线使用公共时钟；输出在一个时钟边沿被时钟输出，在下一个边沿被时钟锁存到接收器。这种模型的一个问题是信号从发送器传送到接收器所需的时间，称为飞行时间（flight
time）。飞行时间必须小于时钟周期，否则模型将无法工作，因此缩短时钟周期具有挑战性。要实现这一点，走线必须更短、负载必须更小，但最终会变得不切实际。另一个因素是发送端和接收端时钟到达时间的差异，称为时钟偏移（clock
skew）。板级布局设计人员努力将其最小化，因为它会消耗时序预算，但永远无法完全消除。第三个因素是信号偏移（signal skew），即

同一时钟下所有信号到达时间的差异。显然，在所有比特就位并稳定之前无法锁存数据，因此我们最终不得不等待最慢的那一位。 

_图 2-3：并行总线的局限性_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

像 PCIe
这样的串行传输是如何规避这些问题的呢？首先，飞行时间变得不再是问题，因为用于将数据锁存到接收器中的时钟实际上内置于数据流中，不需要外部参考时钟。因此，无论时钟周期多小，或者信号到达接收器需要多长时间，都无关紧要，因为时钟与数据同时到达。出于同样的原因，也不存在时钟偏移，原因同样是锁存时钟是从数据流中恢复的。最后，在单个通道（Lane）内消除了信号偏移，因为只发送一个数据比特。如果使用多通道设计，信号偏移问题会重新出现，但接收器会自动进行补偿，并可以校正相当大的偏移。虽然串行设计克服了并行模型的许多问题，但它们也有自己的一系列复杂性。尽管如此，正如我们稍后将看到的，这些解决方案是可管理的，并且能够实现高速、可靠的通信。

**带宽。** PCIe 所支持的高速与宽链路的组合可以产生令人印象深刻的带宽数字，如第 43 页的表 2-1 所示。这些数字是根据比特率和总线特性推导出来的。其中一个特性是，与许多其他串行传输一样，PCIe 的前两代使用一种称为 **8b/10b 编码**
的编码过程，该过程基于 8 位输入生成 10 位输出。尽管这会引入开销，但这样做有几个充分的理由，我们稍后会看到。现在，只需知道发送一个字节的数据需要传输 10 个比特即可。第一代（Gen1 或 PCIe 规范 1.x 版本）比特率为 2.5 GT/s，将其除以 10
意味着一个通道（Lane）将能够发送 0.25 GB/s。由于链路允许同时发送和接收，因此聚合带宽可以是该数值的两倍，即每通道 0.5 GB/s。第二代（Gen2 或 PCIe 2.x）将频率加倍，从而使带宽也加倍。第三代（Gen3 或 PCIe
3.0）再次将带宽加倍，但这一次规范的编写者选择不将频率加倍。相反，出于我们稍后将讨论的原因，他们选择仅将频率提高到 8 GT/s，并去除 8b/10b 编码，转而采用另一种称为 **128b/130b 编码** 的编码机制（有关更多内容，请参阅第 407 页“物理层 -
逻辑（Gen3）”章节）。表 2-1 总结了所有当前可能组合下可用的带宽，并显示了链路在该配置下可提供的峰值吞吐率。

_表 2-1：各种链路宽度下 PCIe Gen1、Gen2 和 Gen3 的聚合带宽_ 

|**链路宽度（Link Width）**|**x1**|**x2**|**x4**|**x8**|**x12**|**x16**|**x32**|
|---|---|---|---|---|---|---|---|
|**Gen1 带宽**<br>**(GB /s)**|0.5|1|2|4|6|8|16|
|**Gen2 带宽**<br>**(GB/s)**|1|2|4|8|12|16|32|
|**Gen3 带宽**<br>**(GB/s)**|2|4|8|16|24|32|64|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-6"></a>
## 3.6 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCIe Bandwidth Calculation** 

To calculate the bandwidth numbers included in the table above, see the calcu‐ lations outlined below. 

- Gen1 PCIe Bandwidth = (2.5 Gb/s x 2 directions) / 10 bits per symbol = 0.5 GB/s. 

- Gen2 PCIe Bandwidth = (5.0 Gb/s x 2 directions) / 10 bits per symbol = 1.0 GB/s. 

Note that in the above calculations, we divide by 10 bits per symbol not 8 bits per byte, because both Gen1 and Gen2 protocols require
packet bytes to be encoded using 8b/10b encoding schemes before packet transmission.

</td>
<td width="50%">

1 ## **PCIe 带宽计算** 

2 要计算上表中包含的带宽数字,请参阅下面概述的计算。 

3 - Gen1 PCIe 带宽 = (2.5 Gb/s × 2 个方向) / 每符号 10 位 = 0.5 GB/s。 

4 - Gen2 PCIe 带宽 = (5.0 Gb/s × 2 个方向) / 每符号 10 位 = 1.0 GB/s。 

5 请注意,在上述计算中,我们除以每符号 10 位而不是每字节 8 位,因为 Gen1 和 Gen2 协议都要求在数据包传输之前使用 8b/10b 编码方案对数据包字节进行编码。 

6 **43**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-7"></a>
## 3.7 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

• Gen3 PCIe Bandwidth = (8.0 Gb/s x 2 directions) / 8 bits per byte = 2.0 GB/s. 

Note that at Gen3 speed, we divide by 8 bits per byte not by 10 bits per symbol because at Gen3 speed, packets are NOT 8b/10b encoded,
rather they are 128b/ 130b encoded. There is an addition 2 bit overhead every 128 bits, but it is not large enough to account for in the
calculation.

These 3 calculated bandwidth numbers are multiplied by Link width to result in total Link bandwidth on multi‐Lane Links.

</td>
<td width="50%">

## **PCI Express 技术**

• Gen3 PCIe 带宽 = (8.0 Gb/s x 2 个方向) / 每字节 8 位 = 2.0 GB/s。

请注意，在 Gen3 速率下，我们除以每字节 8 位，而不是除以每符号 10 位，因为在 Gen3 速率下，数据包**并非**采用 8b/10b 编码，而是采用 128b/130b 编码。在每 128 位中增加了 2 位的开销，但其占比足够小，在带宽计算中可忽略不计。

这 3 个计算出的带宽数值需乘以链路宽度 (Link width)，才能得到多通道链路 (multi‐Lane Link) 上的总链路带宽 (Link bandwidth)。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-8"></a>
## 3.8 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Differential Signals** 

Each Lane uses differential signaling, sending both a positive and negative ver‐ sion (D+ and D‐) of the same signal as shown in Figure 2‐4
on page 44. This dou‐ bles the pin count, of course, but that’s offset by two clear advantages over single‐ended signaling that are
important for high speed signals: improved noise immunity and reduced signal voltage.

The differential receiver gets both signals and subtracts the negative voltage from the positive one to find the difference between them and
determine the value of the bit. Noise immunity is built in to the differential design because the paired signals are on adjacent pins of
each device and their traces must also be routed very near each other to maintain the proper transmission line imped‐ ance. Consequently,
anything that affects one signal will also affect the other by about the same amount and in the same direction. The receiver is looking at
the difference between them and the noise doesn’t really change that difference, so the result is that most noise affecting the signals
doesn’t affect the receiver’s ability to accurately distinguish the bits.

_Figure 2‐4: Differential Signaling_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>
</td>
<td width="50%">

## **差分信号**

每条通道 (Lane) 都采用差分信号传输方式,同时发送同一信号的同相和反相两个版本(D+ 和 D-),如图 2-4(第 44 页)所示。这样当然会使引脚数翻倍,但相对于单端信号,它带来了两个对高速信号至关重要的明显优势:更好的抗噪声能力以及更低的信号电压。

差分接收器接收两个信号,并将负电压从正电压中减去,得出两者之差,从而确定该比特的值。差分设计本身就具备抗噪声能力,因为成对的信号位于器件相邻引脚上,而且它们的走线也必须彼此紧邻布设,以保持合适的传输线阻抗。因此,任何影响其中一个信号的因素,通常也会以大致相当的幅度和相同的方向影响另一个信号。接收器观察的是两者之间的差值,而噪声实际上并不会改变这个差值,所以结果是,大多数影响信号的噪声并不会影响接收器准确区分比特的能力。

_图 2-4:差分信号_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

**第 2 章:PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-9"></a>
## 3.9 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **No Common Clock** 

As mentioned earlier, a common clock is not required for a PCIe Link because it uses a source‐synchronous model, meaning the transmitter
supplies the clock to the receiver to use in latching the incoming data. A PCIe Link does not include a forwarded clock. Instead, the
transmitter embeds the clock into the data stream using 8b/10b encoding. The receiver then recovers the clock from the data stream and uses
it to latch the incoming data. As mysterious as this might sound, the process by which this is done is actually fairly straightforward. In
the receiver, a PLL circuit (Phase‐Locked Loop, see Figure 2‐5 on page 45) takes the incoming bit stream as a reference clock and compares
its timing, or phase, to that of an output clock that it has created with a specified frequency. Based on the result of that comparison, the
output clock’s frequency is increased or decreased until a match is obtained. At that point the PLL is said to be locked, and the output
(recovered) clock frequency precisely matches the clock that was used to transmit the data. The PLL continually adjusts the recovered clock,
so changes in temperature or voltage that affect the transmitter clock frequency will always be quickly compensated.

One thing to note regarding clock recovery is that the PLL does need transitions on the input in order to make its phase comparison. If a
long time goes by with‐ out any transitions in the data, the PLL could begin to drift away from the cor‐ rect frequency. To prevent that
problem, one of the design goals of 8b/10b encoding is ensure no more than 5 consecutive ones or zeroes in a bit‐stream (to learn more on
this, refer to “8b/10b Encoding” on page 380).

_Figure 2‐5: Simple PLL Block Diagram_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

Once the clock has been recovered it’s used to latch the bits of the incoming data stream into the deserializer. Sometimes students wonder
whether this recov‐ ered clock can be used to clock all the logic in the receiver, but it turns out that the answer is no. One reason is
that a receiver can’t count on this reference always being present, because low power states on the Link involve stopping data transmission.
Consequently, the receiver must also have it’s own internal clock that can be locally generated.

</td>
<td width="50%">

## **无公共时钟 (No Common Clock)** 

如前所述，PCIe 链路 (Link) 并不需要公共时钟，因为它采用了源同步模型 (source-synchronous model)，即由发送器 (Transmitter) 向接收器 (Receiver) 提供时钟，用于锁存传入的数据。PCIe 链路中并不包含一个转发的时钟
(forwarded clock)。相反，发送器使用 8b/10b 编码将时钟嵌入到数据流中。接收器随后从数据流中恢复 (recover) 时钟，并使用该时钟来锁存传入的数据。尽管听起来很神秘，但这个过程的实现实际上相当简单。在接收器中，PLL 电路（锁相环，参见第 45 页的图
2-5）将传入的比特流作为参考时钟 (reference clock)，并将其时序或相位与其自身以指定频率产生的输出时钟进行比较。根据该比较结果，输出时钟的频率被增大或减小，直至两者匹配。此时，PLL 即被称为"已锁定"
(locked)，并且其输出（恢复）时钟的频率与发送数据时使用的时钟精确匹配。PLL 会持续地调整恢复时钟，因此由温度或电压变化所引起的发送器时钟频率的改变都将被迅速补偿。

关于时钟恢复有一点需要注意：PLL 需要输入信号中存在电平跳变 (transitions) 才能进行相位比较。如果数据长时间没有任何跳变，PLL 可能会逐渐偏离正确的频率。为了避免这个问题，8b/10b 编码 (8b/10b Encoding)
的设计目标之一就是确保比特流中不会出现超过 5 个连续的 1 或 0（欲了解更多信息，请参见第 380 页的"8b/10b 编码"）。

_图 2-5：简单的 PLL 框图_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

一旦时钟被恢复，它就被用于将传入数据流的比特锁存到解串器 (deserializer) 中。有时学生会有疑问：是否可以使用这个恢复的时钟来为接收器中的所有逻辑提供时钟？答案是不能。原因之一是接收器无法保证该参考时钟始终存在，因为链路 (Link) 上的低功耗状态 (low
power state) 会停止数据传输。因此，接收器还必须拥有自己可以在本地生成的内部时钟。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-10"></a>
## 3.10 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Packet-based Protocol** 

Moving from a parallel to a serial transport greatly reduces the pins needed to carry data. PCIe, like most other serial‐based protocols,
also reduces pin count by eliminating most side‐band control signals typically found in parallel buses. However, if there are no control
signals indicating the type of information being received, how can the receiver interpret the incoming bits? All transactions in PCIe are
sent in defined structures called packets. The receiver finds the packet boundaries and, knowing the pattern to expect, decodes the packet
structure to determine what it should do.

The details of the packet‐based protocol are covered in the chapter called “TLP Elements” on page 169, but an overview of the various packet
types and their uses can be found in this chapter; see “Data Link Layer” on page 72.

</td>
<td width="50%">

## **基于包（Packet）的协议** 

从并行传输转为串行传输大大减少了传输数据所需的引脚数。PCIe 与大多数其他基于串行的协议一样，也通过消除并行总线中常见的大多数边带控制信号来减少引脚数。然而，如果没有控制信号来指示所接收信息的类型，接收器如何解释传入的比特呢？PCIe
中的所有事务都以称为包（Packet）的已定义结构发送。接收器找到包的边界，并知道预期的模式后，对包结构进行解码以确定它应当执行的操作。

基于包的协议的详细信息将在第 169 页的“TLP 元素”章节中介绍，但本章也提供了各种包类型及其用途的概述；请参见第 72 页的“数据链路层”。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-11"></a>
## 3.11 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Links and Lanes** 

As mentioned earlier, a physical connection between two PCIe devices is called a Link and is made up of one or more Lanes. Each Lane
consists of a differential send and receive signal pair, as shown in Figure 2‐2 on page 40. One lane is suf‐ ficient for all communications
between devices and no other signals are required.

</td>
<td width="50%">

## **链路与通道** 

如前所述,两个 PCIe 设备之间的物理连接称为链路 (Link),由一条或多条通道 (Lane) 组成。每条通道由一组差分发送和接收信号对构成,如图 2-2(第 40 页)所示。一条通道足以满足设备之间的所有通信需求,且不需要其他信号。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-12"></a>
## 3.12 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Scalable Performance** 

However, using more Lanes will increase the performance of a Link, which depends on its speed and Link width. For example, using multiple
Lanes increases the number of bits that can be sent with each clock and thus improves the bandwidth. As noted earlier in Table 2‐1 on page
43, the number of Lanes supported by the spec includes powers of 2 up to 32 Lanes. A x12 Link is also supported, which may have been
intended to support the x12 Link width used by InfiniBand, an earlier serial design. Allowing a variety of Link widths per‐ mits a platform
designer to make the appropriate trade‐off between cost and performance, easily scaling up or down based on the number of Lanes.
</td>
<td width="50%">

## **可扩展的性能** 

然而，使用更多的通道（Lane）会提升链路（Link）的性能，这取决于其速度和链路宽度。例如，使用多个通道可以增加每个时钟周期可发送的比特数，从而提高带宽（Bandwidth）。如前文第 43 页表 2‐1 中所述，规范所支持的通道数包括 2 的幂次，最高可达 32
通道。此外还支持 x12 链路，这可能是为了兼容 InfiniBand 所采用的 x12 链路宽度，InfiniBand 是一种早期的串行设计。允许使用多种链路宽度使平台设计人员能够在成本与性能之间做出适当的权衡，可以根据通道数方便地进行扩展或缩减。

**第 2 章：PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-13"></a>
## 3.13 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Flexible Topology Options** 

A Link must be a point‐to‐point connection, rather than a shared bus like PCI, because of the very high speeds it uses. Since a Link can
therefore only connect two interfaces, a means for fanning out the connections is needed for building a non‐trivial system. This is
accomplished in PCIe with the use of Switches and Bridges, which allow flexibility in constructing the system topology ‐ the set of
connections between the elements in the system. Definitions of the elements in a system and some topology examples are given in the
following section.

</td>
<td width="50%">

## **灵活拓扑选项** 

由于链路 (Link) 使用了非常高的速率，因此它必须是点对点的连接，而不是像 PCI 那样的共享总线。由于一条链路 (Link) 一次只能连接两个接口，因此需要一种将连接进行扇出扩展的方法，以构建非平凡的系统。PCIe 通过使用交换机 (Switch) 和桥 (Bridge)
来实现这一点，它们允许在构建系统拓扑 (Topology)——即系统中各元素之间的连接集合——时具有灵活性。系统中的元素定义以及一些拓扑示例将在下一节中给出。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-14"></a>
## 3.14 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Some Definitions** 

A simple PCIe topology example is shown in Figure 2‐6 on page 47, and will help illustrate some definitions at this point. 

_Figure 2‐6: Example PCIe Topology_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
<td width="50%">

## **一些定义**

第 47 页的图 2-6 展示了一个简单的 PCIe 拓扑 (Topology) 示例,这将有助于说明此处的一些定义。

_图 2-6:PCIe 拓扑 (Topology) 示例_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-15"></a>
## 3.15 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Topology Characteristics** 

At the top of the diagram is a CPU. The point to make here is that the CPU is considered the top of the PCIe hierarchy. Just like PCI, only
simple tree struc‐ tures are permitted for PCIe, meaning no loops or other complex topologies are allowed. That’s done to maintain backward
compatibility with PCI software, which used a simple configuration scheme to track the topology and did not support complex environments.

To maintain that compatibility, software must be able to generate configuration cycles in the same way as before and the bus topology must
appear the same as it did before. Consequently, all the configurations registers software expects to find are still there and behave in the
same way they always have. We’ll come back to this discussion a little later, after we’ve had a chance to define some more terms.

</td>
<td width="50%">

## **拓扑特性** 

在图的顶部是一个 CPU。这里要说明的一点是，CPU 被认为是 PCIe 层级 (Hierarchy) 的顶端。与 PCI 一样，PCIe 只允许简单的树形结构 (Topology)，这意味着不允许环路或其他复杂的拓扑。这样做是为了保持与 PCI 软件的向后兼容性，因为 PCI
软件使用简单的配置方案来跟踪拓扑，并且不支持复杂的环境。

为了保持这种兼容性，软件必须能够以与以前相同的方式生成配置周期，并且总线拓扑 (Topology) 必须看起来与以前一样。因此，软件期望找到的所有配置寄存器仍然存在，并且其行为方式与以往完全相同。在我们有机会定义更多术语之后，我们稍后会回到这个讨论。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-16"></a>
## 3.16 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Root Complex** 

The interface between the CPU and the PCIe buses may contain several compo‐ nents (processor interface, DRAM interface, etc.) and possibly
even several chips. Collectively, this group is referred to as the Root Complex (RC or Root). The RC resides at the “root” of the PCI
inverted tree topology and acts on behalf of the CPU to communicate with the rest of the system. The spec does not care‐ fully define it,
though, giving instead a list of required and optional funtional‐ ity. In broad terms, the Root Complex can be understood as the interface
between the system CPU and the PCIe topology, with PCIe Ports labeled as “Root Ports” in configuration space.

</td>
<td width="50%">

## **根复合体 (Root Complex)**

CPU 与 PCIe 总线之间的接口可能包含多个组件（处理器接口、DRAM 接口等），甚至可能包含多个芯片。这些组件统称为根复合体 (Root Complex，简称 RC 或 Root)。RC 位于 PCI 倒置树状拓扑结构的"根"位置，代表 CPU
与系统其余部分进行通信。然而，规范并未对其进行精确定义，而是给出了一份必需功能和可选功能的清单。从广义上讲，根复合体可以理解为系统 CPU 与 PCIe 拓扑之间的接口，其中 PCIe 端口在配置空间中被标记为"根端口 (Root Port)"。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-17"></a>
## 3.17 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Switches and Bridges** 

Switches provide a fanout or aggregation capability and allow more devices to be attached to a single PCIe Port. They act as packet routers
and recognize which path a given packet will need to take based on its address or other rout‐ ing information.

Bridges provide an interface to other buses, such as PCI or PCI‐X, or even another PCIe bus. The bridge shown in the “Example PCIe Topology”
on page 47 is sometimes called a “forward bridge” and allows an older PCI or PCI‐ X card to be plugged into a new system. The opposite type
or “reverse bridge” allows a new PCIe card to be plugged into an old PCI system.
</td>
<td width="50%">

## **交换机与桥 (Switches and Bridges)**

交换机 (Switch) 提供扇出或聚合能力，允许将更多设备挂接到单个 PCIe 端口 (PCI Express Port)。它们充当分组路由器的角色，能够根据地址或其他路由信息识别给定分组需要经过的路径。

桥 (Bridge) 提供与其他总线（例如 PCI 或 PCI-X）的接口，甚至可以连接到另一条 PCIe 总线。第 47 页"PCIe 拓扑示例"中所示的桥有时被称为"前向桥 (forward bridge)"，它允许将较旧的 PCI 或 PCI-X
卡插入新系统中。相反的类型，或称为"反向桥 (reverse bridge)"，则允许将新的 PCIe 卡插入到旧的 PCI 系统中。

**第 2 章：PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-18"></a>
## 3.18 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Native PCIe Endpoints and Legacy PCIe Endpoints** 

Endpoints are devices in a PCIe topology that are not Switches or bridges and act as initiators and Completers of transactions on the bus.
They reside at the bottom of the branches of the tree topology and only implement a single Upstream Port (facing toward the Root). By
comparison, a Switch may have several Downstream Ports but can only have one Upstream Port. Devices that were designed for the operation of
an older bus like PCI‐X but now have a PCIe interface designate themselves as “Legacy PCIe Endpoints” in a configuration register and this
topology includes one. They make use of things that are pro‐ hibited in newer PCIe designs, such as IO space and support for IO transactions
or Locked requests. In contrast, “Native PCIe Endpoints” would be PCIe devices designed from scratch as opposed to adding a PCIe interface
to old PCI device designs. Native PCIe Endpoints device are memory mapped devices (MMIO devices).

</td>
<td width="50%">

## **原生 PCIe 端点与 Legacy PCIe 端点** 

端点是 PCIe 拓扑中既不是交换机 (Switch) 也不是桥 (Bridge) 的设备,在总线上作为事务的发起方 (Requester) 和完成方 (Completer)。它们位于树形拓扑分支的末端,并且只实现一个上游端口 (Upstream Port,朝向根复合体
(Root))。相比之下,一个交换机 (Switch) 可能有多个下游端口 (Downstream Port),但只能有一个上游端口 (Upstream Port)。那些原本为 PCI‐X 等老式总线设计、但现在增加了 PCIe
接口的设备,在配置寄存器中将自身标识为"Legacy PCIe 端点 (Legacy PCIe Endpoint)",这种拓扑中就包含此类设备。它们使用了一些在较新的 PCIe 设计中已被禁止的特性,例如 I/O 空间 (I/O Space) 及其 I/O 事务 (IO
Transaction) 支持,或者锁定请求 (Locked Request) 支持。相对而言,"原生 PCIe 端点 (Native PCIe Endpoint)"则是完全从零开始设计的 PCIe 设备,而不是为旧式 PCI 设备增加 PCIe 接口。原生 PCIe
端点设备是内存映射设备 (MMIO 设备)。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-19"></a>
## 3.19 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Software Compatibility Characteristics** 

One way compatibility with older software is maintained is that the configura‐ tion headers for Endpoints and bridges, shown in Figure 2‐7
on page 50, are unchanged from PCI. One difference now is that bridges are often aggregated into Switches and Roots, but legacy software is
unaware of that distinction and will still simply see them as bridges. At this point we just want to get familiar with the concepts, so we
won’t get into the details of the registers here. An intro‐ duction to the rather large topic of configuration can be found in “Configura‐
tion Overview” on page 85.

</td>
<td width="50%">

## **软件兼容性特性**

维持与旧版软件兼容的一种方式是：端点 (Endpoint) 与桥 (Bridge) 的配置包头（见第 50 页图 2-7）相比 PCI 保持不变。现在的一个不同之处在于，桥通常被聚合到交换机 (Switch) 和根复合体 (Root Complex)
中，但旧版软件并不知晓这种区分，仍会简单地将其视为桥。此时我们只是想先熟悉相关概念，因此此处不会深入介绍寄存器的细节。有关这个相当庞大的"配置"主题的介绍，请参见第 85 页的"配置概述"。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-20"></a>
## 3.20 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 2‐7: Configuration Headers_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

To illustrate the way the system appears to software, consider the example topology shown in Figure 2‐8 on page 51. As before, the Root
resides at the top of the hierarchy. The Root can be quite complex internally, but it will usually implement an internal bus structure and
several bridges to fan out the topology to several ports. That internal bus will appear to configuration software as PCI bus number zero and
the PCIe Ports will appear as PCI‐to‐PCI bridges. This internal structure is not likely to be an actual PCI bus, but it will appear that way
to software for this purpose. Since this bus is internal to the Root, its actual logical design doesn’t have to conform to any standard and
can be vendor spe‐ cific.
_Figure 2‐8: Topology Example_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

In a similar way, the internal organization of a Switch, shown in Figure 2‐9 on page 52, will appear to software as simply a collection of
bridges sharing a com‐ mon bus. A major advantage of this approach is that it allows transaction rout‐ ing to take place in the same way it
did for PCI. Enumeration, the process by which configuration software discovers the system topology and assigns bus numbers and system
resources, works the same way, too. We’ll see some exam‐ ples of how enumeration works later, but once it’s been completed the bus num‐ bers
in the system will have all been assigned in a manner like that shown in Figure 2‐9 on page 52.

_Figure 2‐9: Example Results of System Enumeration_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
<td width="50%">

## **PCI Express Technology** 

_图 2‐7：配置头 (Configuration Headers)_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

为了说明系统向软件呈现的方式，请参考图 2‐8（第 51 页）中所示的示例拓扑结构。与之前一样，根复合体 (Root) 位于层级结构的顶部。根复合体在内部可能相当复杂，但通常会实现一个内部总线结构以及多个桥 (Bridge) 以将拓扑扩展到多个端口。该内部总线对配置软件呈现为
PCI 总线编号 0，而 PCIe 端口则呈现为 PCI‐to‐PCI 桥 (PCI-PCI Bridge)。这种内部结构实际上可能并不是真正的 PCI 总线，但对软件而言它在此用途上呈现为 PCI
总线。由于该总线是根复合体内部的，其实际的逻辑设计不必遵循任何标准，可以是供应商专有的。

**第 2 章：PCIe 架构概述 (PCIe Architecture Overview)** 

_图 2‐8：拓扑示例 (Topology Example)_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

类似地，图 2‐9（第 52 页）中所示的交换机 (Switch) 的内部组织结构对软件而言也仅仅呈现为一组共享同一条总线的桥 (Bridge)。这种方法的一个主要优点是它允许事务路由以与 PCI 相同的方式进行。枚举
(Enumeration)，即配置软件发现系统拓扑并分配总线编号和系统资源的过程，其工作方式也是相同的。我们稍后会看到一些枚举工作方式的示例，但一旦完成枚举，系统中的总线编号将会以类似于图 2‐9（第 52 页）所示的方式进行分配。

_图 2‐9：系统枚举示例结果 (Example Results of System Enumeration)_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-21"></a>
## 3.21 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **System Examples** 

Figure 2‐10 on page 53 illustrates an example of a PCIe‐based system designed for a low‐cost application like a consumer desktop machine. A
few PCIe Ports are implemented, along with a few add‐in cards slots, but the basic architecture doesn’t differ much from the old‐style PCI
system.

By contrast, the high‐end server system shown in Figure 2‐11 on page 54 shows other networking interfaces built into the system. In the
early days of PCIe some thought was given to making it cable of operating as a network that could replace those older models. After all, if
PCIe is basically a simplified version of other networking protocols, couldn’t it fill all the needs? For a variety of rea‐ sons, this
concept never really achieved much momentum and PCIe‐based sys‐ tems still generally connect to external networks using other transports.
This also gives us an opportunity to revisit the question of what constitutes the Root Complex. In this example, the block labeled as “Intel
Processor” contains a number of components, as is true of most modern CPU architectures. This one includes a x16 PCIe Port for access to
graphics, and 2 DRAM channels, which means the memory controller and some routing logic has been integrated into the CPU package.
Collectively, these resources are often called the “Uncore” logic to distinguish them from the several CPU cores and their associated logic
in the package. Since we previously described the Root as being the interface between the CPU and the PCIe topology, that means that part of
the Root must be inside the CPU package. As shown by the dashed line in Figure 2‐11 on page 54, the Root here consists of part of several
packages. This will likely be the case for many future system designs.

_Figure 2‐10: Low‐Cost PCIe System_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

_Figure 2‐11: Server PCIe System_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
<td width="50%">

## **系统示例**

第 53 页的图 2-10 展示了一个基于 PCIe 系统的示例,该系统面向消费级台式机等低成本应用。系统实现了若干 PCIe 端口以及一些插卡插槽,但其基础架构与传统的 PCI 系统相比并无太大差异。

相比之下,第 54 页的图 2-11 所示的高端服务器系统则展示了内置的其他网络接口。在 PCIe 诞生之初,曾有人设想让它作为一种网络来替代那些较老的协议。毕竟,如果 PCIe
基本上是其他网络协议的简化版本,难道它不能胜任所有需求吗?由于种种原因,这一设想始终未能获得广泛认可,基于 PCIe 的系统在连接外部网络时通常仍采用其他传输方式。

**第 2 章:PCIe 架构概览**

这也让我们有机会重新审视"根复合体 (Root Complex) 由什么构成"这一问题。在本例中,标注为"Intel 处理器"的模块包含了众多组件,这在现代 CPU 架构中很常见。该模块包含一个 x16 PCIe 端口用于访问图形,以及 2 条 DRAM
通道,也就是说内存控制器和一些路由逻辑已被集成到 CPU 封装内部。这些资源通常被统称为"Uncore"(非核)逻辑,以区别于封装内的若干 CPU 核心及其相关逻辑。由于我们之前将根复合体 (Root) 描述为 CPU 与 PCIe 拓扑之间的接口,因此根复合体 (Root)
的一部分必然位于 CPU 封装内部。如第 54 页图 2-11 中的虚线所示,此处的根复合体 (Root) 由多个封装的部分共同组成。这种情况在未来的许多系统设计中很可能会成为常态。

_图 2-10:低成本 PCIe 系统_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">


_图 2-11:服务器 PCIe 系统_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-22"></a>
## 3.22 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Introduction to Device Layers** 

PCIe defines a layered architecture as illustrated in Figure 2‐12 on page 56. The layers can be considered as being logically split into two
parts that operate inde‐ pendently because they each have a transmit side for outbound traffic and a receive side for inbound traffic. The
layered approach has some advantages for hardware designers because, if the logic is partitioned carefully, it can be easier to migrate to
new versions of the spec by changing one layer of an existing design while leaving the others unaffected. Even so, it’s important to note
that the layers simply define interface responsibilities and a design is not required to be partitioned according to the layers to be
compliant with the spec. The goal in
this section is to describe the responsibilities of each layer and the flow of events involved in accomplishing a data transfer. 

The device layers as shown in Figure 2‐12 on page 56 consist of: 

- **Device core and interface to Transaction Layer.** The core implements the main functionality of the device. If the device is an
endpoint, it may consist of up to 8 functions, each function implementing its own configuration space. If the device is a switch, the switch
core consists of packet routing logic and an internal bus for accomplishing this goal. If the device is a root, the root core implements a
virtual PCI bus 0 on which resides all the chipset embedded endpoints and virtual bridges.

- **Transaction Layer.** This layer is responsible for Transaction Layer Packet (TLP) creation on the transmit side and TLP decoding on the
receive side. This layer is also responsible for Quality of Service functionality, Flow Con‐ trol functionality and Transaction Ordering
functionality. All these four Transaction Layer functions are described in book **Part two** .

- **Data Link Layer.** This layer is responsible for Data Link Layer Packet (DLLP) creation on the transmit side and decoding on the receive
side. This layer is also responsible for Link error detection and correction. This Data Link Layer function is referred to as the Ack/Nak
protocol. Both these Data Link Layer functions are described in book **Part Three** .

- **Physical Layer.** This layer is responsible for Ordered‐Set packet creation on the transmit side and Ordered‐Set packet decoding on the
receive side. This layer processes all three types of packets (TLPs, DLLPs and Ordered‐Sets) to be transmitted on the Link and processes all
types of packets received from the Link. Packets are processed on the transmit side by byte striping logic, scramblers, 8b/10b encoders
(associated with Gen1/Gen2 protocol) or 128b/130b encoders (associated with Gen3 protocol) and packet serializers. The packet is finally
differentially clocking out on all Lanes at the trained Link speed. On the receive Physical Layer, packet processing consists of serially
receiving differentially encoded bits and converting to digital for‐ mat and then deserializing the incoming bit‐stream. The is done at a
clock rate derived from a recovered clock from the CDR (Clock and Data Recov‐ ery) circuit. The received packets are processed by elastic
buffers, 8b/10b decoders (associated with Gen1/Gen2 protocol) or 128b/130b decoders (associated with Gen3 protocol), de‐scramblers and byte
un‐striping logic. Finally, the Link Training and Status State Machine (LTSSM) of the Physical Layer is responsible for Link Initialization
and Training. All these Physical Layer functions are described in book **Part Four** .

</td>
<td width="50%">

## **设备各层简介** 

PCIe 定义了一个分层架构,如图 2-12(第 56
页)所示。这些层在逻辑上可以被划分为相互独立的两部分,因为每一部分都有用于出向流量的发送侧和用于入向流量的接收侧。这种分层方式对硬件设计人员来说有一定优势:如果对逻辑进行仔细划分,在迁移到新版本规范时,只需修改现有设计的某一层而保持其它层不变,从而更容易完成过渡。尽管如此,仍需注意,这些层仅仅定义了接口职责,设计上并不要求严格按照层进行划分以满足规范要求。本节的目标是描述每一层的职责以及实现数据传输时所涉及的事件流程。

如图 2-12(第 56 页)所示,设备的各层包括: 

- **设备核心及与事务层的接口。** 核心实现设备的主要功能。如果设备是端点 (Endpoint),它最多可包含 8 个功能,每个功能实现自己的配置空间。如果设备是交换机 (Switch),交换机核心由报文路由逻辑和用于实现该目标的内部总线组成。如果设备是根复合体 (Root
Complex),根核心实现一个虚拟的 PCI 总线 0,芯片组的所有嵌入式端点和虚拟桥都驻留其上。

- **事务层 (Transaction Layer)。** 该层负责发送侧的 TLP(Transaction Layer Packet,事务层包)创建以及接收侧的 TLP 解码。该层还负责服务质量 (QoS)、流控 (Flow Control) 和事务排序
(Transaction Ordering) 功能。这四项事务层功能都将在本书的**第二部分**中介绍。

- **数据链路层 (Data Link Layer)。** 该层负责发送侧的 DLLP(Data Link Layer Packet,数据链路层包)创建以及接收侧的解码。该层还负责链路的错误检测与纠正。这一数据链路层功能称为 Ack/Nak
协议。这两项数据链路层功能都将在本书的**第三部分**中介绍。

- **物理层 (Physical Layer)。** 该层负责发送侧的有序集 (Ordered-Set) 包创建以及接收侧的有序集包解码。该层处理要在链路上发送的所有三种类型包(TLP、DLLP
和有序集),并处理从链路接收的所有类型包。在发送侧,这些包经由字节拆分逻辑、加扰器、8b/10b 编码器(对应 Gen1/Gen2 协议)或 128b/130b 编码器(对应 Gen3 协议)以及报文并串转换器进行处理。最终,报文以训练后的链路速度在所有通道 (Lane)
上以差分时钟方式输出。在接收物理层,报文处理包括:串行接收差分编码的比特,转换为数字格式,然后对输入比特流进行解串。这一过程以从 CDR(Clock and Data Recovery,时钟和数据恢复)电路恢复得到的时钟频率运行。接收到的报文经由弹性缓冲器、8b/10b
解码器(对应 Gen1/Gen2 协议)或 128b/130b 解码器(对应 Gen3 协议)、解扰器以及字节去拆分逻辑进行处理。最后,物理层的链路训练与状态机 (LTSSM,Link Training and Status State Machine)
负责链路的初始化与训练。这些物理层功能都将在本书的**第四部分**中介绍。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-23"></a>
## 3.23 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 2‐12: PCI Express Device Layers_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

Every PCIe interface supports the functionality of these layers, including Switch Ports, as shown in Figure 2‐13 on page 57. A question
often came up in earlier classes as to whether a Switch Port needs to implement all the layers, since it’s typically only forwarding
packets. The answer is yes, and the reason is that evaluating the contents of packets to determine their routing requires looking into the
internal details of a packet, and that takes place in the Transaction Layer logic.
_Figure 2‐13: Switch Port Layers_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

In principle, each layer communicates with the corresponding layer in the device on the other end of the Link. The upper two layers do so by
organizing a string of bits into a packet, creating a pattern that is recognizable by the corre‐ sponding layer in the receiver. The packets
are forwarded through the other lay‐ ers along the way to get to or from the Link. The Physical Layer also communicates directly with that
layer in the other device but it does differently.

Before we go deeper, let’s first walk through an overview to see how the layers interact. In broad terms, the contents of an outgoing
request or completion packet from the device are assembled in the Transaction Layer based on infor‐ mation presented by the device core
logic, which we also sometimes call the Software Layer (although the spec doesn’t use that term). That information would usually include the
type of command desired, the address of the target device, attributes of the request, and so on. The newly created packet is then stored in
a buffer called a Virtual Channel until it’s ready for passing to the next layer. When the packet is passed down to the Data Link Layer,
additional infor‐ mation is added to the packet for error checking at the neighboring receiver, and a copy is stored locally so we can send
it again if a transmission error occurs. When the packet arrives at the Physical Layer it’s encoded and transmit‐ ted differentially using
all the available Lanes of the Link.

</td>
<td width="50%">

## **PCI Express 技术**

_图 2‐12：PCI Express 设备分层_

**==> 图片 [232 x 201] 已省略 <==**

**----- 图片文字开始 -----**<br>
PCIe 设备 A　　　　　　　　　　PCIe 设备 B<br>
设备核心　　　　　　　　　　　　设备核心<br>
PCIe 核心　　　　　　　　　　　PCIe 核心<br>
硬件/软件　　　　　　　　　　　硬件/软件<br>
接口　　　　　　　　　　　　　　接口<br>
事务层　　　　　　　　　　　　事务层<br>
数据链路层　　　　　　　　　　数据链路层<br>
物理层　　　　　　　　　　　　物理层<br>
(RX)　　　　　　　　　(TX)　　(RX)　　(TX)<br>
　　　　　　　　　　　链路<br>
**----- 图片文字结束 -----**<br>

每一个 PCIe 接口都支持这些层的功能，包括交换机端口，如图 2‐13（第 57
页）所示。在早期的课程中经常有人会问：交换机端口是否需要实现所有层，因为它通常只是转发数据包？答案是肯定的，原因是评估数据包内容以确定其路由需要查看数据包的内部细节，而这些操作是在事务层逻辑中完成的。

**第 2 章：PCIe 架构概述**

_图 2‐13：交换机端口分层_

**==> 图片 [189 x 218] 已省略 <==**

**----- 图片文字开始 -----**<br>
事务层<br>
数据链路层<br>
物理层<br>
交换机<br>
核心<br>
**----- 图片文字结束 -----**<br>

原则上，每一层都与链路另一端设备中的对应层进行通信。上两层通过将一串比特组织成数据包来实现通信，创建一个能被接收方对应层识别的模式。数据包在传输过程中会经过其他各层，最终到达链路或从链路发出。物理层也会直接与另一设备的物理层通信，但其方式有所不同。

在深入之前，我们先总体浏览一下，看看各层是如何交互的。从广义上讲，从设备发出的请求或完成报文的内容是由事务层根据设备核心逻辑（我们有时也称为软件层，尽管规范中没有使用这个术语）提供的信息组装而成的。这些信息通常包括所需的命令类型、目标设备的地址、请求的属性等。新创建的数据包被存储在一个称为虚通道
(VC) 的缓冲区中，直到准备好传递给下一层。当数据包向下传递到数据链路层时，会向数据包添加额外的信息以供相邻接收方进行错误检查，同时在本地保存一个副本，以便在发生传输错误时能够重新发送。当数据包到达物理层时，它会被编码，并使用链路上所有可用的通道以差分方式发送出去。

**PCI Express 技术**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-24"></a>
## 3.24 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## _Figure 2‐14: Detailed Block Diagram of PCI Express Device’s Layers_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

The receiver decodes the incoming bits in the Physical Layer, checks for errors that can be seen at this level and, if there are none,
forwards the resulting packet up to the Data Link Layer. Here the packet is checked for different errors and, if there are no errors, is
forwarded up to the Transaction Layer. The packet is buff‐ ered, checked for errors, and disassembled into the original information (com‐
mand, attributes, etc.) so the contents can be delivered to the device core of the receiver. Next, let’s explore in greater depth what each
of the layers must do to make this process work, using Figure 2‐14 on page 58. We start at the top.
</td>
<td width="50%">

## _图 2‐14：PCI Express 设备各层的详细框图_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

接收器在物理层对传入的比特进行解码，检查该层级可发现的错误，若没有错误，则将得到的包向上转发到数据链路层。在数据链路层，包被检查是否存在不同的错误，若没有错误，则被向上转发到事务层。包被缓冲，进行错误检查，并被拆解为原始信息(命令、属性等)，以便将其内容传送到接收器的设备核心。接下来，让我们结合第
58 页的图 2‐14 更深入地探讨每一层为使此过程正常运作所必须完成的工作。我们从最顶层开始。

**第 2 章：PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-25"></a>
## 3.25 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Device Core / Software Layer** 

This is the core functionality of the device, such as a network interface or hard drive controller. This isn’t defined as a layer in the
PCIe spec, but can be thought of in that way since it resides above the Transaction Layer and will be either the source or destination of
all Requests. It provides the transmit side of the Trans‐ action Layer with requests that include information like the transaction type, the
address, amount of data to transfer, and so on. It’s also the destination for information forwarded up from the Transaction Layer when
incoming packets have been received.

</td>
<td width="50%">

## **设备核心 / 软件层**

这是设备的核心功能,例如网卡接口或硬盘控制器。虽然 PCIe 规范并未将其定义为一个层,但可以这样理解,因为它位于事务层之上,并且会成为所有请求 (Request)
的源或目的。它向事务层的发送端提供请求,其中包括事务类型、地址、要传输的数据量等信息。当接收到传入的数据包时,它也是从事务层向上转发信息的目的地。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-26"></a>
## 3.26 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Transaction Layer** 

In response to requests from the Software Layer, the Transaction Layer gener‐ ates outbound packets. It also examines inbound packets and
forwards the information contained in them up to the Software Layer. It supports the split transaction protocol for non‐posted transactions
and associates an inbound Completion with an outbound non‐posted Request that was transmitted earlier. The transactions handled by this
layer use TLPs (Transaction Layer Packets) and can be grouped into four request categories:

1. Memory 

2. IO 

3. Configuration 

4. Messages 

The first three of these were already supported in PCI and PCI‐X, but messages are a new type for PCIe. A **Transaction** is defined as the
combination of a **Request** packet that a delivers a command to a targeted device, together with any **Completion** packets the target
sends back in reply. A list of the request types is given in Table 2‐2 on page 59.

_Table 2‐2: PCI Express Request Types_ 

|**Request Type**|**Non‐Posted or Posted**|
|---|---|
|Memory Read|Non‐Posted|
|Memory Write|Posted|
|Memory Read Lock|Non‐Posted|

</td>
<td width="50%">

## **事务层 (Transaction Layer)** 

响应来自软件层的请求，事务层生成出站报文（outbound packets）。它还会检查入站报文（inbound packets），并将其所含信息向上传递给软件层。它支持用于 Non-Posted 事务的分离事务协议（split transaction
protocol），并将入站的完成报文（Completion）与先前发出的出站 Non-Posted 请求（Request）相关联。该层所处理的事务使用 TLP（事务层包，Transaction Layer Packets），可分为以下四种请求类别：

1. Memory（内存）

2. IO（输入/输出）

3. Configuration（配置）

4. Messages（消息）

前三种类型在 PCI 和 PCI‐X 中就已支持，但消息是 PCIe 新增的类型。一个**事务 (Transaction)** 被定义为：由一个将命令传送到目标设备的**请求 (Request)** 报文，加上目标设备作为响应发回的任何**完成报文 (Completion)**
所共同组成。请求类型的列表见表 2‐2（第 59 页）。

_表 2‐2：PCI Express 请求类型 (Request Types)_ 

|**请求类型**|**Non-Posted 或 Posted**|
|---|---|
|Memory Read（内存读）|Non-Posted|
|Memory Write（内存写）|Posted|
|Memory Read Lock（内存读锁定）|Non-Posted|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-27"></a>
## 3.27 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

_Table 2‐2: PCI Express Request Types (Continued)_ 

|**Request Type**|**Non‐Posted or Posted**|
|---|---|
|IO Read|Non‐Posted|
|IO Write|Non‐Posted|
|Configuration Read (Type 0 and Type 1)|Non‐Posted|
|Configuration Write (Type 0 and Type 1)|Non‐Posted|
|Message|Posted|

The requests also fall into one of two categories as shown in the right column of the table: **non‐posted** and **posted** . For non‐posted
requests, a Requester sends a packet for which a Completer should generate a response in the form of a Com‐ pletion packet. The reader may
recognize this as the split transaction protocol inherited from PCI‐X. For example, any read request will be non‐posted because the
requested data will need to be returned in a completion. Perhaps unexpectedly, IO writes and Configuration writes are also non‐posted. Even
though they are delivering the data for the command, these requests still expect to receive a completion from the target to confirm that the
write data has in fact made it to the destination without error.

In contrast, Memory Writes and Messages are posted, meaning the targeted device does not return a completion TLP to the Requester. Posted
transactions improve performance because the Requester doesn’t have to wait for a reply or incur the overhead of a completion. The trade‐off
is that they get no feedback about whether the write has finished or encountered an error. This behavior is inherited from PCI and is still
considered a good thing to do because the likeli‐ hood of a failure is small and the performance gain is significant. Note that, even though
they don’t require Completions, Posted Writes do still participate in the Ack/Nak protocol in the Data Link Layer that ensures reliable
packet delivery. For more on this, see Chapter 10, entitled ʺAck/Nak Protocol,ʺ on page 317.

</td>
<td width="50%">

## **PCI Express 技术**

_表 2‐2：PCI Express 请求类型（续）_

|**请求类型**|**Non‐Posted 或 Posted**|
|---|---|
|IO 读 (IO Read)|Non‐Posted|
|IO 写 (IO Write)|Non‐Posted|
|配置读 (Configuration Read)（Type 0 和 Type 1）|Non‐Posted|
|配置写 (Configuration Write)（Type 0 和 Type 1）|Non‐Posted|
|消息 (Message)|Posted|

如表中右列所示，这些请求还可以分为两类：**non‐posted**（非发布）和 **posted**（发布）。对于 non‐posted 请求，请求者 (Requester) 发送一个数据包，被请求端 (Completer) 应以完成报文 (Completion)
数据包的形式作出响应。读者可能会注意到，这是从 PCI‐X 继承而来的分离事务协议 (split transaction protocol)。例如，任何读请求都是 non‐posted 的，因为所请求的数据需要在完成报文中返回。出乎意料的是，IO 写和配置写也是
non‐posted 的。尽管它们正在为命令传送数据，这些请求仍然期望从目标设备接收一个完成报文，以确认写数据实际上已经无误地到达目的地。

相比之下，内存写 (Memory Write) 和消息 (Message) 是 posted 的，意味着目标设备不会向请求者返回完成报文 (Completion) TLP。Posted
事务提高了性能，因为请求者不必等待回复，也无需承担完成报文的开销。其代价是它们无法获得关于写操作是否已完成或是否遇到错误的反馈。这种行为是从 PCI 继承而来的，并且仍被认为是一种良好的做法，因为发生故障的可能性很小，而性能提升却很显著。需要注意的是，即使 posted
写不需要完成报文，它们仍然会参与数据链路层 (Data Link Layer) 中的 Ack/Nak 协议，以确保数据包可靠传输。有关这方面的更多内容，请参阅第 317 页第 10 章"ʺAck/Nak 协议ʺ"。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-28"></a>
## 3.28 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **TLP (Transaction Layer Packet) Basics** 

A list of all of the PCIe request and completion packet types is given in Table 2‐ 3 on page 61. 
_Table 2‐3: PCI Express TLP Types_ 

|**TLP Packet Types**|**Abbreviated Name**|
|---|---|
|Memory Read Request|MRd|
|Memory Read Request ‐ Locked access|MRdLk|
|Memory Write Request|MWr|
|IO Read|IORd|
|IO Write|IOWr|
|Configuration Read (Type 0 and Type 1)|CfgRd0,<br>CfgRd1|
|Configuration Write (Type 0 and Type 1)|CfgWr0,<br>CfgWr1|
|Message Request without Data|Msg|
|Message Request with Data|MsgD|
|Completion without Data|Cpl|
|Completion with Data|CplD|
|Completion without Data ‐ associated with Locked Memory Read<br>Requests|CplLk|
|Completion with Data ‐ associated with Locked Memory Read<br>Requests|CplDLk|

TLPs originate at the Transaction Layer of a transmitter and terminate at the Transaction Layer of a receiver, as shown in Figure 2‐15 on
page 62. The Data Link Layer and Physical Layer add parts to the packet as it moves through the layers of the transmitter, and then verify
at the receiver that those parts were transmitted correctly across the Link.

</td>
<td width="50%">

## **TLP（事务层包）基础**

所有 PCIe 请求和完成报文类型的列表见第 61 页的表 2-3。

**第 2 章：PCIe 架构概述**

_表 2-3：PCI Express TLP 类型_

|**TLP 报文类型**|**缩写 名称**|
|---|---|
|内存读请求|MRd|
|内存读请求 - 锁定访问|MRdLk|
|内存写请求|MWr|
|IO 读|IORd|
|IO 写|IOWr|
|配置读（Type 0 和 Type 1）|CfgRd0，<br>CfgRd1|
|配置写（Type 0 和 Type 1）|CfgWr0，<br>CfgWr1|
|不带数据的消息请求|Msg|
|带数据的消息请求|MsgD|
|不带数据的完成报文|Cpl|
|带数据的完成报文|CplD|
|不带数据的完成报文 - 与锁定内存读请求关联|CplLk|
|带数据的完成报文 - 与锁定内存读请求关联|CplDLk|

TLP 在发送端的**事务层**产生，并在接收端的**事务层**终止，如图 2-15（第 62 页）所示。**数据链路层**和**物理层**在报文通过发送端各层时为其添加相应的部分，然后在接收端验证这些部分是否已通过**链路**正确传输。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-29"></a>
## 3.29 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

_Figure 2‐15: TLP Origin and Destination_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

**TLP Packet Assembly.** An illustration of the parts of a finished TLP as it is sent over the Link is shown in Figure 2‐16 on page 63,
where it can be seen that different parts of the packet are added in each of the layers. To make it easier to recognize how the packet gets
constructed, the different parts of the TLP are color coded to indicate which layer is responsible for them: red for Transaction Layer, blue
for Data Link Layer, and green for the Physical Layer.

The device core sends the information required to assemble the core section of the TLP in the Transaction Layer. Every TLP will have a
header, although some, like a read request, won’t contain data. An optional End‐to‐End CRC (ECRC) field may be calculated and appended to
the packet. CRC stands for Cyclic Redundancy Check (or Code) and is employed by almost all serial architectures for the simple reason that
it’s simple to implement and provides very robust error detection capability. The CRC also detects “burst errors,” or string of repeated
mistaken bits, up to the length of the CRC value (32 bits for PCIe). Since this type of error is likely to be encountered when sending a
long string of bits, this characteristic is very useful for serial transports. The ECRC field is passed unchanged through any service points
(“service point” usually refers to a Switch or Root Port that has TLP routing options) between the sender and receiver of the packet, making
it useful for verifying at the destination that there were no errors anywhere along the way.
For transmission, the core section of the TLP is forwarded to the Data Link Layer, which is responsible to append a Sequence Number and
another CRC field called the Link CRC (LCRC). The LCRC is used by the neighboring receiver to check for errors and report the results of
that check back to the trans‐ mitter for every packet sent on that Link. The thoughtful reader may wonder why the ECRC would be helpful if
the mandatory LCRC check already verifies error‐free transmission across the Link. The reason is that there is still a place where
transmission errors aren’t checked, and that is within devices that route packets. A packet arrives and is checked for errors on one port,
the routing is checked, and when it’s sent out on another port a new LCRC value is calculated and added to it. The internal forwarding
between ports could encounter an error that isn’t checked as part of the normal PCIe protocol, and that’s why ECRC is helpful.

Finally, the resulting packet is forwarded to the Physical Layer where other characters are added to the packet to let the receiver know
what to expect. For the first two generations of PCIe, these were control characters added to the beginning and end of the packet. For the
third generation, control characters are no longer used but other bits are appended to the blocks that give the needed information about the
packets. The packet is then encoded and differentially transmitted on the Link using all of the available lanes.

_Figure 2‐16: TLP Assembly_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
<td width="50%">

## **PCI Express 技术**

_图 2-15：TLP 的源端与目的端_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

**TLP 数据包组装。** 关于已完成的 TLP 在链路上发送时各组成部分的示意图，请参见第 63 页的图 2-16，从中可以看出数据包的不同部分在每一层中添加。为了更容易识别数据包是如何构建的，TLP
的不同部分用颜色编码以指示负责该部分的层：事务层为红色，数据链路层为蓝色，物理层为绿色。

设备核心在事务层中发送组装 TLP 核心部分所需的信息。每个 TLP 都有一个包头（Header），尽管某些 TLP（如读请求）不包含数据。可以选择性地计算并附加一个端到端 CRC（ECRC）字段。CRC 代表循环冗余校验（Cyclic Redundancy Check 或
Code），几乎所有串行架构都采用它，原因很简单——它易于实现，并提供非常强大的错误检测能力。CRC 还能检测"突发错误"，即重复的误位串，其长度可达 CRC 值的长度（PCIe 中为 32 位）。由于在发送长串比特时很可能遇到此类错误，因此这一特性对串行传输非常有用。ECRC
字段在发送端和接收端之间的任何服务点（"服务点"通常指具有 TLP 路由选项的交换机或根端口）保持不变地传递，这使得它在目的地验证沿途没有发生错误时非常有用。

**第 2 章：PCIe 架构概述**

对于传输，TLP 的核心部分被转发到数据链路层，数据链路层负责附加一个序列号（Sequence Number）和另一个称为链路 CRC（LCRC）的 CRC 字段。LCRC
由相邻的接收器用于检查错误，并将该检查的结果针对该链路上发送的每个数据包报告回发送器。细心的读者可能会想，既然强制的 LCRC 检查已经验证了链路上无错误的传输，为什么 ECRC
仍然有用呢？原因是仍存在一处未检查传输错误的地方，那就是在路由数据包的设备内部。数据包在一个端口到达并被检查错误，检查路由，然后当从另一端口发出时，会计算并添加一个新的 LCRC 值。端口之间的内部转发可能会遇到未作为常规 PCIe 协议一部分被检查的错误，这就是 ECRC
之所以有用的原因。

最后，生成的数据包被转发到物理层，在那里会将其他字符添加到数据包中，以让接收器知道会发生什么。对于 PCIe
的前两代，这些是添加在数据包开头和结尾的控制字符。对于第三代，不再使用控制字符，但会在块上附加其他比特，以提供关于数据包所需的信息。然后，数据包使用所有可用的通道（Lane）进行编码并以差分方式在链路上传输。

_图 2-16：TLP 组装_

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-30"></a>
## 3.30 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **PCI Express Technology** 

**TLP Packet Disassembly.** When the neighboring receiver sees the incom‐ ing TLP bit stream, it needs to identify and remove the parts that
were added to recover the original information requested by the core logic of the transmitter. As shown in Figure 2‐17 on page 64, the
Physical Layer will verify that the proper Start and End or other characters are present and remove them, for‐ warding the remainder of the
TLP to the Data Link Layer. This layer first checks for LCRC and Sequence Number errors. If no errors are found, it removes those fields
from the TLP and forwards it to the Transaction Layer. If the receiver is a Switch, the packet is evaluated in the Transaction Layer to find
the routing information in the header of the TLP and determine to which port the packet should be forwarded. Even when it’s not the intended
destination, a Switch is allowed to check and report an ECRC error if it finds one. However, it’s not allowed to modify the ECRC, so the
targeted device will be able to detect the ECRC error as well.

The target device can check ECRC errors if it’s capable and was enabled. If this is the target device and there was no error, the ECRC field
is removed, leaving the header and data portion of the packet to be forwarded to the Software Layer.

_Figure 2‐17: TLP Disassembly_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>
</td>
<td width="50%">

## **PCI Express Technology** 

**TLP 包解封装。** 当相邻的接收器看到传入的 TLP 位流时,它需要识别并移除那些为恢复发送器核心逻辑所请求的原始信息而添加的部分。如第 64 页的图 2-17 所示,物理层 (Physical Layer) 将验证正确的 Start (起始) 和 End (结束)
或其他字符是否存在,并将它们移除,将其余的 TLP 转发到数据链路层 (Data Link Layer)。该层首先检查 LCRC (链路 CRC) 和序列号 (Sequence Number) 错误。如果未发现错误,则将这些字段从 TLP 中移除,并将其转发到事务层
(Transaction Layer)。如果接收器是交换机 (Switch),则会在事务层中评估该数据包,以查找 TLP 头 (Header) 中的路由信息,并确定应将该数据包转发到哪个端口。即使不是预期目的地,如果交换机发现 ECRC (端到端 CRC)
错误,也允许其检查并报告该错误。但是,不允许其修改 ECRC,因此目标设备也将能够检测到 ECRC 错误。

如果目标设备具备相应能力并且已使能,则可以检查 ECRC 错误。如果此设备就是目标设备且没有错误,则会移除 ECRC 字段,留下包头和数据部分,以便转发到软件层。 

_图 2-17:TLP 解封装_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>
</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-3-31"></a>
## 3.31 Configuration Overview | 配置概述

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

## **Non-Posted Transactions** 

**Ordinary Reads.** Figure 2‐18 on page 65 shows an example of a Memory Read Request sent from an Endpoint to system memory. A detailed
discussion of the TLP contents can be found in Chapter 5, entitled ʺTLP Elements,ʺ on page 169, but an important part of any memory read
request is the target address. The address for a memory Request can be 32 or 64 bits, and determines the packet routing. In this example,
the request gets routed through two Switches that forward it up to the target, which is the Root in this case. When the Root decodes the
request and recognizes that the address in the packet targets sys‐ tem memory, it fetches the requested data. To return that data to the
Requester, the Transaction Layer of the Root Port creates as many Completions as are needed to deliver all the requested data to the
Requester. The largest possible data payload for PCIe is 4 KB per packet, but devices are often designed to use smaller payloads than that,
so several completions may be needed to return a large amount of data.

_Figure 2‐18: Non‐Posted Read Example_ 

<img src="figures/page/page0177.png" alt="Figure 2‐1: Dual‐Simplex Link" width="700">

<br>

</td>
<td width="50%">

## **Non-Posted Transactions（非 Posted 事务）**

**Ordinary Reads（普通读）。** 第 65 页的图 2-18 展示了一个从端点 (Endpoint) 发往系统内存的 Memory Read Request（内存读请求）示例。关于 TLP 内容的详细讨论可参见第 169 页第 5 章 ʺTLP
Elements（TLP 元素）ʺ，但任何内存读请求的一个重要部分是目标地址。内存 Request（请求）的地址可以是 32 位或 64 位，并由此决定报文路由。在本例中，请求通过两个交换机 (Switch) 转发到目标（本例中即 Root）。当 Root
解码该请求并识别到报文中的地址指向系统内存时，它会取回所请求的数据。为了将这些数据返回给 Requester（请求者），Root Port（根端口）的 Transaction Layer（事务层）会按需生成尽可能多的 Completion（完成报文）以将所有请求数据传送到
Requester（请求者）。PCIe 单个报文最大数据载荷为 4 KB，但设备通常被设计为使用更小的载荷，因此可能需要多个 Completion（完成报文）才能返回大量数据。

</td>
</tr></tbody></table>

<p align="center"><b>Figure 2‐18: Non‐Posted Read Example（图 2-18：非 Posted 读示例）</b></p>
<p align="center"><img src="figures/page/page0177.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/page/page0177.png">Page 177</a></sub></p>

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
