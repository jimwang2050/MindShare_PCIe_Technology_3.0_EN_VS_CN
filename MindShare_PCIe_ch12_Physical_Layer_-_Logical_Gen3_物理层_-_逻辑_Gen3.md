# 📘 第 12 章　物理层 - 逻辑 (Gen3) (Chapter 12. Physical Layer - Logical (Gen3))

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0285.md` ... `chunks/chunk0292.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [12.1 Link Power Management States — 物理层 - 逻辑 (Gen3)](#sec-12-1)
- [12.2 Ordered Sets in Link Training — 物理层 - 逻辑 (Gen3)](#sec-12-2)
- [12.3 _Exit to “Polling State”_ — 物理层 - 逻辑 (Gen3)](#sec-12-3)
- [12.4 _Entering Polling.Compliance:_ — 物理层 - 逻辑 (Gen3)](#sec-12-4)
- [12.5 Confirming Link and Lane Numbers. — 物理层 - 逻辑 (Gen3)](#sec-12-5)

<a id="sec-12-1"></a>
## 12.1 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|VRX‐DIFF‐<br>PP‐CC|175<br>(min)<br>1200<br>(max)|120 (min)<br>1200<br>(max)|Indirectly<br>specified|mV|Peak‐to‐peak differential
voltage<br>sensitivity of common‐clocked<br>Receiver.|
|VRX‐DIFF‐<br>PP‐DC|175<br>(min)<br>1200<br>(max)|100 (min)<br>1200<br>(max)|Indirectly<br>specified|mV|Peak‐to‐peak differential
voltage<br>sensitivity of data‐clocked<br>Receiver.|
|VRX‐IDLE‐<br>DET‐DIFFp‐<br>p|65 (min) 175 (max)|||mV|Electrical Idle detect threshold<br>at the Receiver pins.|
|ZRX‐DIFF‐<br>DC|80<br>(min)<br>120<br>(max)|Covered by<br>RLRX‐DIFF|||At higher frequencies imped‐<br>ance can no longer be
repre‐<br>sented by a lumped‐sum value<br>and must be described in more<br>detail.|
|ZRX‐‐DC|40<br>(min)<br>60<br>(max)|40 (min)<br>60 (max)|Bounded<br>by<br>RLRX‐CM||DC impedance needed for<br>Receiver Detect.|


_Table 13‐5: Common Receiver Characteristics (Continued)_ 

|**Item**|**2.5 GT/**<br>**s.**|**5.0 GT/s.**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|LRX‐SKEW|20|8|6|ns|Max Lane‐to‐Lane skew that a<br>Receiver must be able to correct.|
|RLRX‐‐DIFF|10<br>(min)|10 (min)<br>for 0.05 ‐<br>1.25 GHz,<br>8 (min)<br>for >1.25 ‐<br>2.5 GHz|10 (min)<br>for 0.05 ‐<br>1.25 GHz,<br>8
(min)<br>for >1.25 ‐<br>2.5 GHz,<br>5 (min)<br>for >2.5 ‐<br>4.0 GHz|dB|Rx package + Si differential<br>return loss|
|RLRX‐‐CM|6 (min)|6 (min)|6 (min)<br>for 0.05 ‐<br>2.5 GHz,<br>5 (min)<br>for >2.5 ‐ 4<br>GHz|dB|Common mode Rx return loss|


_Figure 13‐34: 2.5 GT/s Receiver Eye Diagram_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0468.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Link Power Management States** 

Figure 13‐35 on page 500 through Figure 13‐39 on page 504 illustrate the electri‐ cal state of the Physical Layer while the link is in
various power management states and describe several characteristics. One of these is the Tx and Rx termi‐ nations, which are sometimes
implemented as active logic

_Figure 13‐35: L0 Full‐On Link State_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0469.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>

## _Figure 13‐36: L0s Low Power Link State_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0470.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


- Recommended Power Budget <= 20 mW per Lane 

- Recommended exit latency < 50 ns, however designers indicate that a more realistic number appears to be 1 us-2 us 

- One direction of the Link can be in L0s while the other is in L0 

- Transmitter and Receiver clock PLL are ON but Rx Clock loses sync 

- Transmitter is On, Receiver is ON  High or Low impedance termination at transmitter 

## **PCI Express Technology** 

## _Figure 13‐37: L1 Low Power Link State_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0471.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>

_Figure 13‐38: L2 Low Power Link State_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0472.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **PCI Express Technology** 

## _Figure 13‐39: L3 Link Off State_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0473.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## _**14 Link Initialization & Training**_ 

## **The Previous Chapter** 

The previous chapter describes the Physical Layer electrical interface to the Link, including some low‐level characteristics of the
differential Transmitters and Receivers. The need for signal equalization and the methods used to accom‐ plish it are also discussed here.
This chapter combines electrical transmitter and receiver characteristics for both Gen1, Gen2 and Gen3 speeds.

## **This Chapter** 

This chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process
of the Link is described from Power‐On or Reset until the Link reaches fully‐operational L0 state during which normal packet traffic occurs.
In addition, the Link power management states L0s, L1, L2, and L3 are discussed along with the state transi‐ tions. The Recovery state,
during which bit lock, symbol lock or block lock are re‐established is described. Link speed and width change for Link bandwidth management
is also discussed.

## **The Next Chapter** 

The next chapter discusses error types that occur in a PCIe Port or Link, how they are detected, reported, and options for handling them.
Since PCIe is designed to be backward compatible with PCI error reporting, a review of the PCI approach to error handling is included as
background information. Then we focus on PCIe error handling of correctable, non‐fatal and fatal errors.

## **Overview** 

Link initialization and training is a hardware‐based (not software) process con‐ trolled by the Physical Layer. The process configures and
initializes a device’s link and port so that normal packet traffic proceeds on the link.

_Figure 14‐1: Link Training and Status State Machine Location_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0474.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>

The full training process is automatically initiated by hardware after a reset and is managed by the LTSSM (Link Training and Status State
Machine), shown in Figure 14‐1 on page 506.

Several things are configured during the Link initialization and training pro‐ cess. Let’s consider what they are and define some terms up
front.

- **Bit Lock** : When Link training begins the Receiver’s clock is not yet synchronized with the transmit clock of the incoming signal, and
is unable to reliably sample incoming bits. During Link training, the Receiver CDR (Clock and Data Recovery) logic recreates the
Transmitter’s clock by using the incoming bit stream as a clock reference. Once the clock has been recovered from the stream, the Receiver
is said to have acquired Bit Lock and is then able to sam‐ ple the incoming bits. For more on the Bit Lock mechanism, see “Achieving Bit
Lock” on page 395.

- **Symbol Lock** : For 8b/10b encoding (used in Gen1 and Gen2), the next step is to acquire Symbol Lock. This is a similar problem in that
the receiver can now see individual bits but doesn’t know where the boundaries of the 10‐bit Symbols are found. As TS1s and TS2s are
exchanged, Receivers search for a recognizable pattern in the bit stream. A simple one to use for this is the COM Symbol. Its unique
encoding makes it easy to recognize and its arrival shows the boundary of both the Symbol and the Ordered Set since a TS1 or TS2 must be in
progress. For more on this, see “Achieving Symbol Lock” on page 396.

</td>
<td style="background-color:#e8e8e8">

|VRX‐DIFF‐PP‐CC|175<br>（最小）<br>1200<br>（最大）|120（最小）<br>1200（最大）|间接指定|mV|公共时钟接收器的峰峰值差分电压灵敏度。|
|VRX‐DIFF‐PP‐DC|175<br>（最小）<br>1200<br>（最大）|100（最小）<br>1200（最大）|间接指定|mV|数据时钟接收器的峰峰值差分电压灵敏度。|
|VRX‐IDLE‐DET‐DIFFp‐p|65（最小）175（最大）|||mV|接收器引脚处的电气空闲检测阈值。|
|ZRX‐DIFF‐DC|80<br>（最小）<br>120<br>（最大）|由 RLRX‐DIFF 覆盖||Ω|在较高频率下，阻抗不能再用集总值表示，必须更详细地描述。|
|ZRX‐‐DC|40<br>（最小）<br>60<br>（最大）|40（最小）<br>60（最大）|由 RLRX‐CM 限定|Ω|接收器检测所需的直流阻抗。|


**第 13 章：物理层 - 电气**

_表 13‐5：通用接收器特性（续）_

|**项目**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|**单位**|**备注**|
|---|---|---|---|---|---|
|LRX‐SKEW|20|8|6|ns|接收器必须能够纠正的最大 Lane 到 Lane 偏移。|
|RLRX‐‐DIFF|10<br>（最小）|10（最小）<br>，频率 0.05 ‐<br>1.25 GHz，<br>8（最小）<br>，频率 >1.25 ‐<br>2.5 GHz|10（最小）<br>，频率 0.05 ‐<br>1.25
GHz，<br>8（最小）<br>，频率 >1.25 ‐<br>2.5 GHz，<br>5（最小）<br>，频率 >2.5 ‐<br>4.0 GHz|dB|Rx 封装 + Si 差分回波损耗|
|RLRX‐‐CM|6（最小）|6（最小）|6（最小）<br>，频率 0.05 ‐<br>2.5 GHz，<br>5（最小）<br>，频率 >2.5 ‐ 4<br>GHz|dB|共模 Rx 回波损耗|


_图 13‐34：2.5 GT/s 接收器眼图_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0475.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **链路电源管理状态**

第 500 页的图 13‐35 至第 504 页的图 13‐39 说明了物理层在各种电源管理状态下的电气状态，并描述了几个特性。其中之一是 Tx 和 Rx 终端，有时实现为有源逻辑

_图 13‐35：L0 全开链路状态_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0476.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


**第 13 章：物理层 - 电气**

## _图 13‐36：L0s 低功耗链路状态_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0477.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


- 推荐功耗预算 ≤ 每 Lane 20 mW

- 推荐退出延迟 < 50 ns，但设计人员表示更现实的数字似乎是 1 us-2 us

- 链路的一个方向可以处于 L0s，而另一个处于 L0

- 发送器和接收器时钟 PLL 开启，但 Rx 时钟失去同步

- 发送器开启，接收器开启 → 发送器处为高或低阻抗终端

## **PCI Express Technology**

## _图 13‐37：L1 低功耗链路状态_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0478.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


**第 13 章：物理层 - 电气**

_图 13‐38：L2 低功耗链路状态_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0479.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **PCI Express Technology**

## _图 13‐39：L3 链路关闭状态_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0480.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## _**14 链路初始化与训练**_

## **上一章**

上一章描述了物理层到链路的电气接口，包括差分发送器和接收器的一些低级特性。本章还讨论了对信号均衡的需求以及用于实现它的方法。本章结合了 Gen1、Gen2 和 Gen3 速度的电气发送器和接收器特性。

## **本章**

本章描述了物理层链路训练和状态状态机 (LTSSM) 的操作。链路的初始化过程从上电或复位开始描述，直到链路在正常数据包传输发生期间达到完全可操作的 L0 状态。此外，还讨论了链路电源管理状态 L0s、L1、L2 和 L3
以及状态转换。描述了在链路训练期间重新建立位锁定、符号锁定或块锁定的恢复状态。还讨论了用于链路带宽管理的链路速度和宽度变化。

## **下一章**

下一章讨论 PCIe 端口或链路中发生的错误类型、如何检测、报告以及处理它们的选项。由于 PCIe 被设计为向后兼容 PCI 错误报告，因此包括对 PCI 错误处理方法的回顾作为背景信息。然后我们将重点关注可纠正、非致命和致命错误的 PCIe 错误处理。

## **概述**

链路初始化和训练是由物理层控制的基于硬件（非软件）的过程。该过程配置和初始化设备的链路和端口，以便正常的分组流量在链路上进行。

_图 14‐1：链路训练和状态状态机位置_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0481.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


**第 14 章：链路初始化与训练**

完整的训练过程在复位后由硬件自动启动，并由 LTSSM（链路训练和状态状态机）管理，如第 506 页图 14‐1 所示。

在链路初始化和训练过程中配置了几件事。让我们考虑一下它们是什么并预先定义一些术语。

- **位锁定 (Bit Lock)**：当链路训练开始时，接收器的时钟尚未与输入信号的发送时钟同步，无法可靠地采样输入位。在链路训练期间，接收器 CDR（时钟数据恢复）逻辑使用输入位流作为时钟参考来重新创建发送器的时钟。一旦从流中恢复时钟，就可以说接收器已获得位锁定 (Bit
Lock)，然后能够对输入位进行采样。有关位锁定机制的更多信息，请参见第 395 页 "Achieving Bit Lock"。

- **符号锁定 (Symbol Lock)**：对于 8b/10b 编码（用于 Gen1 和 Gen2），下一步是获取符号锁定。这是一个类似的问题，因为接收器现在可以看到各个位，但不知道 10 位符号的边界在哪里。随着 TS1 和 TS2
的交换，接收器在位流中搜索可识别的模式。一个用于此目的的简单模式是 COM 符号。其独特的编码使其易于识别，其到达显示了符号和有序集的边界，因为 TS1 或 TS2 必须正在进行中。有关详细信息，请参见第 396 页 "Achieving Symbol Lock"。

## **PCI Express Technology**

- **块锁定 (Block Lock)**：对于 8.0 GT/s（Gen3），该过程与符号锁定略有不同，因为不使用 8b/10b 编码，所以没有 COM 字符。但是，接收器仍然需要在输入位流中找到可识别的分组边界。解决方案是在训练序列中包含更多
EIEOS（电气空闲退出有序集）的实例，并使用它来定位边界。EIEOS 可识别为 00h 和 FFh 字节交替的模式，并且它定义了块边界，因为根据定义，当该模式结束时，下一个块必须开始。

- **链路宽度**：具有多个 Lane 的设备可能能够使用不同的链路宽度。例如，具有 x2 端口的设备可以连接到具有 x4 端口的设备。在链路训练期间，两个设备的物理层测试链路并将宽度设置为最高公共值。

- **Lane 反转**：多 Lane 设备端口上的 Lane 从 Lane 0 开始按顺序编号。通常，一个设备端口的 Lane 0 连接到相邻设备端口的 Lane 0，Lane 1 连接到 Lane 1，依此类推。然而，有时希望能够逻辑上反转 Lane 编号以简化布线并允许
Lane 直接连接而不必交叉（参见第 508 页的图 14‐2）。只要一台设备支持可选的 Lane 反转功能，这就可以工作。该情况在链路训练期间被检测到，并且一台设备必须在内部反转其 Lane 编号。由于规范不要求支持此功能，因此板设计人员将需要在以相反顺序连接 Lane
之前验证至少一台连接的设备支持此功能。

_图 14‐2：Lane 反转示例（支持可选）_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0482.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>

- **极性反转**：两台设备的 D+ 和 D‐ 差分对端子也可以根据需要进行反转，以使板布局和布线更容易。每个接收器 Lane 必须独立检查此情况并在训练期间根据需要进行自动纠正，如第 509 页的图 14‐3 所示。为此，接收器查看传入 TS1 或 TS2 的符号 6 到
15。如果在 TS1 中收到 D21.5 而不是 D10.2，或在 TS2 中收到 D26.5 而不是预期的 D5.2，则该 Lane 的极性反转，必须进行纠正。与 Lane 反转不同，此功能的支持是强制性的。

**第 14 章：链路初始化与训练**

_图 14‐3：极性反转示例（支持必需）_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0483.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


- **链路数据速率**：复位后，链路初始化和训练将始终使用默认的 2.5Gbit/s 数据速率以实现向后兼容性。如果有更高的数据速率可用，它们会在此过程中通告，训练完成后，设备将自动通过快速重新训练更改为最高共同支持的速率。

- **Lane 到 Lane 去偏移**：走线长度变化和其他因素会导致多 Lane 链路的并行位流在不同时间到达接收器，这个问题称为信号偏移 (signal skew)。接收器需要通过根据需要延迟早期到达的位来补偿此偏移以对齐位流（参见第 442 页 "Lane‐to‐Lane
Skew"）。他们必须自动纠正较大的偏移（在 2.5GT/s 时允许 20ns 的到达时间差），这使板设计人员免于创建等长走线的困难约束。结合极性反转和 Lane 反转，这大大简化了板设计人员创建可靠的高速链路的任务。

## **链路训练中的有序集**

## **概述**

所有不同类型的物理层有序集在第 388 页 "Ordered sets" 一节中描述。训练序列 TS1 和 TS2 在训练过程中值得关注。它们在 Gen1 或 Gen2 模式下的格式如图 14‐4（第 510 页）所示，而在 Gen3 操作模式下，它们如图 14‐5（第 511
页）所示。以下是其内容的详细描述。

## **PCI Express Technology**

_图 14‐4：Gen1 或 Gen2 模式下的 TS1 和 TS2 有序集_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0484.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **TS1 和 TS2 有序集**

如图所示，TS1 和 TS2 由 16 个符号组成。它们在 LTSSM 的 Polling、Configuration 和 Recovery 状态期间交换，在第 518 页 "Link Training and Status State Machine (LTSSM)"
中描述。这些符号的描述如下，并在第 514 页的表 14‐1（TS1）和第 516 页的表 14‐2（TS2）中进行了总结。

为了使描述更短更易读，术语 "Gen1" 将用于指示 2.5 GT/s 的数据速率，"Gen2" 用于指示 5.0 GT/s 的数据速率，"Gen3" 用于指示 8.0 GT/s 的数据速率。另请注意，链路和 Lane 编号中使用的 PAD 字符在较低数据速率下由 K23.7
字符表示，但在 Gen3 下表示为数据字节 F7h。在我们的讨论中，PAD 类型之间的区别并不重要，将仅隐含表示。

**第 14 章：链路初始化与训练**

_图 14‐5：Gen3 操作模式下的 TS1 和 TS2 有序集块_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0485.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


第 514 页的表 14‐1 和第 516 页的表 14‐2 是 TS1 和 TS2 内容的摘要。16 个 TS1/TS2 符号的更详细描述如下：

- **符号 0**：

- 对于 **Gen1 或 Gen2**，任何有序集的第一个符号是 K28.5（COM）字符。接收器使用此字符获取符号锁定。由于它必须同时出现在所有 Lane 上，因此它对于 Lane 的去偏移也很有用。

- 对于 **Gen3**，有序集由必须在块之前出现的 2 位同步头标识（图中未显示），之后的第一个符号指示将跟随哪个有序集。对于 TS1，第一个符号是 1Eh，对于 TS2，是 2Dh。

- **符号 1（Link #）**：在 Polling 状态中，此字段包含 PAD 符号，但在其他状态中分配了链路编号。

- **符号 2（Lane #）**：在 Polling 状态中，此字段包含 PAD 符号，但在其他状态中分配了 Lane 编号。

- **符号 3（N_FTS）**：表示接收器在以当前速度退出 L0s 电源状态以达到 L0 状态时所需的快速训练序列的数量。发送器将发送至少那么多

## **PCI Express Technology**

FTS 以退出 L0s。所需的时间量取决于需要的数量和正在使用的数据速率。例如，在 2.5 GT/s 时，每个符号需要 4ns，因此，如果需要 200 个 FTS，则所需时间为 200 FTS * 每个 FTS 4 个符号 * 4ns/符号 = 3200
ns。如果发送器设备中设置了 Extended Synch 位，则必须发送总共 4096 个 FTS。这个大数字旨在为外部链路监控工具提供足够的时间来获取位和符号锁定，因为其中一些工具在这方面可能很慢。

- **符号 4（Rate ID）**：设备报告它们支持的数据速率，以及一些用于硬件发起的带宽更改的更多信息。2.5 GT/s 速率必须始终受支持，链路在复位后将始终自动训练到该速度，以便较新的组件保持与较旧组件的向后兼容性。如果支持 8.0 GT/s，还要求 5.0 GT/s
必须可用。此符号中的其他信息包括以下内容：

- **自动更改**：如果设置，则任何请求的带宽更改都是为了电源管理原因而发起的。如果请求了更改但未设置此位，则在更高速度或更宽链路上检测到不可靠的操作，并且请求更改以解决该问题。

- **可选去加重**

 - **上游端口**设置此位以指示它们在 5.0 GT/s 时所需去加重的级别。它们如何做出此选择是特定于实现的。在 Recovery.RcvrCfg 状态中，它们在内部注册接收到的此位的值（规范将其描述为存储在 select_deemphasis 变量中）。

 - **下游端口和根端口**：在 Polling.Compliance 状态中，select_deemphasis 变量必须设置为与该位的接收值匹配。在 Recovery.RcvrCfg 状态中，发送器将其 TS2 中的此位设置为与 Link Control 2 寄存器中的
Selectable De‐emphasis 字段匹配。由于该寄存器位是硬件初始化的，预期它在启动时由固件或绑定选项分配给最佳值。

 - 在 5.0 GT/s 的环回模式下，从设备的去加重值由主设备发送的 TS1 中的该位分配。

- **链路向上配置能力**：报告宽度减小后的宽链路是否能够恢复到宽状态。如果链路的两端在 Configuration.Complete 期间都报告了此情况，则此事实被内部记录（例如，upconfigure_capable 位被设置）。

- **符号 5（Training Control）**：传达特殊条件，例如热复位、启用环回模式、禁用链路、禁用加扰。

**第 14 章：链路初始化与训练**

- **符号 6‐9（均衡控制）**：

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-12-2"></a>
## 12.2 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- **Block Lock** : For 8.0 GT/s (Gen3), the process is a little different from Symbol Lock because since 8b/10b encoding is not used, there
are no COM charac‐ ters. However, Receivers still need to find a recognizable packet boundary in the incoming bit stream. The solution is to
include more instances of the EIEOS (Electrical Idle Exit Ordered Set) in the training sequence and use that to locate the boundaries. An
EIEOS is recognizable as a pattern of alternating 00h and FFh bytes, and it defines the Block boundary because, by definition, when that
pattern ends the next Block must begin.

- **Link Width** : Devices with multiple Lanes may be able to use different Link widths. For example, a device with a x2 port may be
connected to one with a x4 port. During Link training, the Physical Layer of both devices tests the Link and sets the width to the highest
common value.

- **Lane Reversal:** The Lanes on a multi‐Lane device’s port are numbered sequentially beginning with Lane 0. Normally, Lane 0 of one
device’s port connects to Lane 0 of the neighbor’s port, Lane 1 to Lane 1, and so on. How‐ ever, sometimes it’s desirable to be able to
logically reverse the Lane numbers to simplify routing and allow the Lanes to be wired directly without having to crisscross (see Figure
14‐2 on page 508). As long as one device supports the optional Lane Reversal feature, this will work. The situation is detected dur‐

ing Link training and one device must internally reverse its Lane numbering. Since the spec doesn’t require support for this, board
designers will need to verify that at least one of the connected devices supports this feature before wiring the Lanes in reverse order.

_Figure 14‐2: Lane Reversal Example (Support Optional)_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0486.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


- **Polarity Inversion** : The D+ and D‐ differential pair terminals for two devices may also be reversed as needed to make board layout and
routing easier. Every Receiver Lane must independently check for this and automatically correct it as needed during training, as illustrated
in Figure 14‐3 on page 509. To do this, the Receiver looks at Symbols 6 to 15 of the incoming TS1s or TS2s. If a D21.5 is received instead
of a D10.2 in a TS1, or a D26.5 instead of the D5.2 expected for a TS2, then the polarity of that lane is inverted and must be corrected.
Unlike Lane reversal, support for this feature is manda‐ tory.
_Figure 14‐3: Polarity Inversion Example (Support Required)_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0487.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


- **Link Data Rate** : After a reset, Link initialization and training will always use the default 2.5Gbit/s data rate for backward
compatibility. If higher data rates are available, they are advertised during this process and, when the training is completed, devices will
automatically go through a quick re‐training to change to the highest commonly supported rate.

- **Lane‐to‐Lane De‐skew** : Trace length variations and other factors cause the parallel bit streams of a multi‐Lane Link to arrive at the
Receivers at different times, a problem referred to as signal skew. Receivers are required to com‐ pensate for this skew by delaying the
early arrivals as needed to align the bit streams (see “Lane‐to‐Lane Skew” on page 442). They must correct a rela‐ tively big skew
automatically (20ns difference in arrival time is permitted at 2.5GT/s), and that frees board designers from the sometimes difficult con‐
straint of creating equal‐length traces. Together with Polarity Inversion and Lane Reversal, this greatly simplifies the board designer’s
task of creating a reliable high‐speed Link.

## **Ordered Sets in Link Training** 

## **General** 

All of the different types of Physical Layer Ordered Sets were described in the section called “Ordered sets” on page 388. Training
Sequences TS1 and TS2 are of interest during the training process. The format for these when in Gen1 or Gen2 mode is shown in Figure 14‐4 on
page 510, while for Gen3 mode of opera‐ tion, they are as shown in Figure 14‐5 on page 511. A detailed description of their contents
follows.

## **PCI Express Technology** 

_Figure 14‐4: TS1 and TS2 Ordered Sets When In Gen1 or Gen2 Mode_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0488.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **TS1 and TS2 Ordered Sets** 

As seen in the illustrations, TS1s and TS2s consist of 16 Symbols. They are exchanged during the Polling, Configuration, and Recovery states
of the LTSSM described in “Link Training and Status State Machine (LTSSM)” on page 518. The Symbols are described below and summarized in
Table 14‐1 on page 514 for TS1s and Table 14‐2 on page 516 for TS2s.

To make the descriptions a little shorter and easier to read, the term “Gen1” will be used to indicated data rate of 2.5 GT/s, “Gen2” to
indicated data rate of 5.0 GT/s and “Gen3” to indicate data rates of 8.0 GT/s. Also, note that the PAD char‐ acter used in the Link and Lane
numbers is represented by the K23.7 character for the lower data rates, but as the data byte F7h for Gen3. In our discussion the distinction
between the types of PAD is not interesting and will simply be implied.
_Figure 14‐5: TS1 and TS2 Ordered Set Block When In Gen3 Mode of Operation_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0489.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


Table 14‐1 on page 514 and Table 14‐2 on page 516 is a summary of TS1 and TS2 contents. A more detailed description of the 16 TS1/TS2
Symbols follows:

- **Symbol 0** : 

- For **Gen1 or Gen2** , the first Symbol of any Ordered Set is the K28.5 (COM) character. Receivers use this character to acquire Symbol
Lock. Since it must appear on all Lanes at the same time it’s also useful for de‐skewing the Lanes.

- For **Gen3** , an Ordered Set is identified by the 2‐bit Sync Header that must precede the Block (not shown in the illustration), and the
first Symbol after that indicates which Ordered Set will follow. For a TS1, the first Symbol is 1Eh, and for a TS2, it’s 2Dh.

- **Symbol 1 (Link #)** : In the Polling state this field contains the PAD Symbol, but in the other states a Link Number is assigned. 

- **Symbol 2 (Lane #)** : In the Polling state this field contains the PAD Symbol, but in the other states a Lane Number is assigned. 

- **Symbol 3 (N_FTS)** : Indicates the number of Fast Training Sequences the Receiver will need in order to achieve the L0 state when
exiting from the L0s power state at the current speed. Transmitters will send at least that many

## **PCI Express Technology** 

FTSs to exit L0s. The amount of time needed for this depends on how many are needed and the data rate in use. For example, at 2.5 GT/s each
Symbol takes 4ns so, if 200 FTSs were needed the required time would be 200 FTS * 4 Symbols per FTS * 4ns/Symbol = 3200 ns. If the Extended
Synch bit is set in the transmitter device, a total of 4096 FTSs must be sent. This large number is intended to provide enough time for
external Link monitoring tools to acquire Bit and Symbol Lock, since some of them may be slow in this regard.

- **Symbol 4 (Rate ID** ): Devices report which data rates they support, along with a little more information used for hardware‐initiated
bandwidth changes. The 2.5 GT/s rate must always be supported and the Link will always train to that speed automatically after reset so that
newer components will remain backward compatible with older ones. If 8.0 GT/s is supported, it’s also required that 5.0 GT/s must be
available. Other information in this Symbol includes the following:

- **Autonomous Change** : If set, any requested bandwidth change was initi‐ ated for power‐management reasons. If a change is requested and
this bit is not set, then unreliable operation has been detected at the higher speed or wider Link and the change is requested to fix that
problem.

- **Selectable De‐emphasis** 

 - **Upstream Ports** set this to indicate their desired de‐emphasis level at 5.0 GT/s. How they make this choice is implementation
specific. In the Recovery.RcvrCfg state, they register the value they receive for this bit internally (the spec describes it as being stored
in a select_deemphasis variable).

 - **Downstream Ports and Root Ports** : In the Polling.Compliance state the select_deemphasis variable must be set to match the received
value of this bit. In the Recovery.RcvrCfg state, the Transmitter sets this bit in its TS2s to match the Selectable De‐emphasis field in the
Link Control 2 register. Since this register bit is hardware‐initialized, the expectation is that it’s assigned to an optimal value at
power‐up by firmware or a strapping option.

 - In Loopback mode at 5.0 GT/s, the Slave de‐emphasis value is assigned by this bit in the TS1s sent by the Master. 

- **Link Upconfigure Capability** : Reports whether a wide Link whose width is reduced will be capable of going back to the wide case or
not. If both sides of a Link report this during Configuration.Complete, this fact is recorded internally (e.g. an upconfigure_capable bit is
set).

- **Symbol 5 (Training Control)** : Communicates special conditions such as a Hot Reset, Enable Loopback mode, Disable Link, Disable
Scrambling.
- **Symbols 6‐9 (Equalization Control** ):

</td>
<td style="background-color:#e8e8e8">

- 对于 **Gen1 或 Gen2**，符号 7‐9 只是 TS1 或 TS2 标识符，符号 6 通常也是如此。但是，如果符号 6 的位 7 设置为 1 而不是 TS1 或 TS2 标识符的 0，则表示这是从下游端口 (DSP - 面向下游的端口，如根端口) 发送的 EQ
TS1 或 EQ TS2。"EQ" 标签代表均衡，意味着链路将要更改为 8.0 GT/s，因此上游端口 (USP - 面向上游的端口，如端点端口) 需要知道要使用什么均衡器值。对于 EQ TS1 或 TS2，符号 6 以发送器预设和接收器预设提示的形式将该信息提供给 USP。支持
8.0 GT/s 的端口必须接受任一 TS 类型（常规或 EQ），但不支持它的端口不需要接受 EQ 类型。这些预设的可能值列在第 579 页的表 14‐8 和第 580 页的表 14‐9 中。

- 对于 **Gen3**，符号 6‐9 提供均衡过程的预设值和系数。TS2 中符号 6 的位 7 现在可以由 USP 用于请求重新进行均衡。如果这样做，位 6 也可以设置以指示重复均衡过程所需的时间不会引起问题，例如完成超时，只要它在返回 L0 后快速完成（在 1ms
内）。例如，如果检测到均衡结果有问题，则可能需要这样做。DSP 还可以使用位 6 和 7 要求 USP 提出此类请求并保证没有副作用，尽管 USP 不需要响应此请求。有关均衡过程的更多信息，请参见第 577 页 "Link Equalization Overview"。

- **符号 10‐13**：TS1 或 TS2 标识符。

- **符号 14‐15**：（DC 平衡）

- 对于 **Gen1 和 Gen2**，由于 DC 平衡由 8b/10b 编码维持，这些只是 TS1 或 TS2 标识符。

- 对于 **Gen3**，这两个符号的内容取决于 Lane 的 DC 平衡。发送器的每个 Lane 必须独立跟踪为 TS1 和 TS2 发送的所有加扰位的运行 DC 平衡。"运行 DC 平衡"是指发送的 1 数与发送的 0 数之间的差，Lane 必须能够跟踪任一方向上最多
511 的差。这些计数器在其最大值处饱和但继续跟踪减少量。例如，如果计数器指示已发送比 0 多 511 个 1，那么无论再发送多少个 1，该值都将保持为 511。但是，如果发送了 2 个 0，计数器将递减到 509。当发送 TS1 或 TS2 时，使用以下算法确定符号 14 和
15：

 - 如果在符号 11 结束时运行 DC 平衡值 > 31 且发送了更多的 1，则符号 14 = 20h，符号 15 = 08h。如果发送了更多的 0，则符号 14 = DFh，符号 15 = F7h。

## **PCI Express Technology**

- 如果运行 DC 平衡值 > 15，则符号 14 = 正常的加扰 TS1 或 TS2 标识符，而符号 15 = 08h 以减少 1 的数量，或 F7h 以减少 DC 平衡计数中的 0 的数量。

- 否则，将发送正常的 TS1 或 TS2 标识符符号。

- 关于 Gen3 DC 平衡的其他注意事项：

 - 运行 DC 平衡由电气空闲退出或数据块之后的 EIEOS 复位。

 - DC 平衡符号绕过加扰以确保发送预期的位模式。

_表 14‐1：TS1 有序集内容摘要_

|**符号**<br>**编号**|**描述**|
|---|---|
|0|• 对于 Gen1 或 Gen2，COM (K28.5) 符号<br>• 对于 Gen3，1Eh 表示 TS1。|
|1|链路号<br>• 不支持 Gen3 的端口：0‐255，PAD<br>• 支持 Gen3 的下游端口：0‐31，PAD<br>• 支持 Gen3 的上游端口：0‐255，PAD|
|2|Lane 号<br>• 0‐31，PAD|
|3|N_FTS<br>• 退出 L0s 时接收器达到 L0 所需的 FTS 有序集数：0 ‐ 255|
|4|数据速率标识符：<br>• 位 0 — 保留。<br>• 位 1 — 支持 2.5 GT/s（必须设置为 1b）<br>• 位 2 — 支持 5.0 GT/s（如果设置了位 3，则必须设置）<br>• 位 3 — 支持 8.0 GT/s<br>• 位 5:4 —
保留<br>• 位 6 — 自动更改/可选去加重<br>–<br>下游端口：在 Polling.Active、Configuration.Linkwidth.Start 和 Loopback.Entry LTSSM 状态中使用，在所有其他状态中保留。<br>–<br>上游端口：在
Polling.Active、Configuration、Recovery 和 Loopback.Entry LTSSM 状态中使用，在所有其他状态中保留。<br>• 位 7 — 速率更改。此位只能在 Recovery.RcvrLock LTSSM 状态中设置为
1，在所有其他状态中保留。|

**第 14 章：链路初始化与训练**

_表 14‐1：TS1 有序集内容摘要（续）_

|**符号**<br>**编号**|**描述**|
|---|---|
|5|训练控制（0=取消断言，1 = 断言）<br>• 位 0 — 热复位<br>• 位 1 — 禁用链路<br>• 位 2 — 环回<br>• 位 3 — 禁用加扰（对于 2.5 或 5.0 GT/s；为 Gen3 保留）<br>• 位 4 — 合规接收（对于 2.5 GT/s
是可选的，对于所有其他速率是必需的）<br>• 位 7:5 — 保留，设置为 0|
|6|对于 Gen1 或 Gen2：<br>• TS1 标识符 (4Ah) 编码为 D10.2<br>• EQ TS1 将其编码为<br>位 2:0 — 接收器预设提示<br>位 6:3 — 发送器预设<br>位 7 — 设置为 1b<br>对于 Gen3：<br>• 位 1:0
— 均衡控制 (EC)。仅在 Recovery.Equalization 和 Loopback LTSSM 状态中使用；在所有其他状态中必须为 00b。<br>• 位 2 — 复位 EIEOS 间隔计数。仅在 Recovery.Equalization LTSSM
状态中使用；在所有其他状态中保留。<br>• 位 6:3 — 发送器预设<br>• 位 7 — 使用预设。（如果为 1，则使用预设值而不是系数值。如果为 0，则使用系数而不是预设。）仅在 Recovery.Equalization 和 Loopback LTSSM
状态中使用；在所有其他状态中保留。|
|7|对于 Gen1 或 Gen2 GT/s，TS1 标识符 (4Ah) 编码为 D10.2<br>对于 Gen3：<br>• 位 5:0 — 当符号 6 的 EC 字段为 01b 时的 FS（满摆幅值），否则为预冲系数。<br>• 位 7:6 — 保留。|
|8|对于 Gen1 或 Gen2，TS1 标识符 (4Ah) 编码为 D10.2<br>对于 Gen3：<br>• 位 5:0 — 当符号 6 的 EC 字段为 01b 时的 LF（低频值），否则为游标系数。<br>• 位 7:6 — 保留。|

## **PCI Express Technology**

_表 14‐1：TS1 有序集内容摘要（续）_

|**符号**<br>**编号**|**描述**|
|---|---|
|9|对于 Gen1 或 Gen2，TS1 标识符 (4Ah) 编码为 D10.2<br>对于 Gen3：<br>• 位 5:0 — 后游标系数。<br>• 位 6 — 拒绝系数值。仅在 Recovery.Equalization LTSSM 状态的特定阶段中设置；否则必须为
0b。<br>• 位 7 — 奇偶校验 (P)。这是符号 6、7、8 的所有位和符号 9 的位 6:0 的偶校验。接收器必须计算此值并将其与接收到的奇偶校验位进行比较。仅当奇偶校验位匹配时，接收到的 TS1 才有效。|
|10‐13|对于 Gen1 或 Gen2，TS1 标识符 (4Ah) 编码为 D10.2<br>• 对于 Gen3，TS1 标识符 (4Ah)|
|14‐15|对于 Gen1 或 Gen2，TS1 标识符 (4Ah) 编码为 D10.2<br>• 对于 Gen3，TS1 标识符 (4Ah)，或 DC 平衡符号。|

细心的读者可能想知道为什么 EQ TS1 在较低数据速率下显示在符号 6 中，因为只有 8.0 GT/s 数据速率使用均衡。那是因为它们用于为支持 Gen3 但当前以较低速率运行并希望更改为 8.0 GT/s 的 Lane 传递 EQ 值。有关此以及 Gen3
均衡过程的更多详细信息，请参见第 577 页 "Link Equalization Overview"。

_表 14‐2：TS2 有序集内容摘要_

|**符号**<br>**编号**|**描述**|
|---|---|
|0|• 对于 Gen1 或 Gen2，COM (K28.5) 符号<br>• 对于 Gen3，2Dh 表示 TS2。|
|1|链路号<br>• 不支持 Gen3 的端口：0‐255，PAD<br>• 支持 Gen3 的下游端口：0‐31，PAD<br>• 支持 Gen3 的上游端口：0‐255，PAD|
|2|Lane 号<br>• 0‐31，PAD|

**第 14 章：链路初始化与训练**

_表 14‐2：TS2 有序集内容摘要（续）_

|**符号**<br>**编号**|**描述**|
|---|---|
|3|N_FTS<br>• 退出 L0s 时接收器达到 L0 所需的 FTS 有序集数：0 ‐ 255|
|4|数据速率标识符：<br>• 位 0 — 保留。<br>• 位 1 — 支持 2.5 GT/s（必须设置为 1b）<br>• 位 2 — 支持 5.0 GT/s（如果设置了位 3，则必须设置）<br>• 位 3 — 支持 8.0 GT/s<br>• 位 5:4 —
保留<br>• 位 6 — 自动更改/可选去加重/链路向上配置能力。在 Polling.Configuration、Configuration.Complete 和 Recovery LTSSM 状态中使用；在所有其他状态中保留。<br>• 位 7 — 速率更改。此位只能在
Recovery.RcvrLock LTSSM 状态中设置为 1，在所有其他状态中保留。|
|5|训练控制（0 = 取消断言，1 = 断言）<br>• 位 0 — 热复位，<br>• 位 1 — 禁用链路<br>• 位 2 — 环回<br>• 位 3 — 禁用加扰（对于 2.5 或 5.0 GT/s；为 Gen3 保留）<br>• 位 7:4 — 保留，设置为 0|
|6|对于 Gen1 或 Gen2：<br>• TS2 标识符 (4Ah) 编码为 D10.2<br>• EQ TS2 将其编码为<br>位 2:0 — 接收器预设提示<br>位 6:3 — 发送器预设<br>位 7 — 均衡命令<br>对于 Gen3：<br>• 位 5:0 —
保留。<br>• 位 6 — 静止保证。定义为仅在 Recovery.RcvrCfg 中使用；在所有其他状态中保留。<br>• 位 7 — 请求均衡。定义为仅在 Recovery.RcvrCfg 中使用；在所有其他状态中保留。|
|7‐13|• 对于 Gen1 或 Gen2，TS2 标识符 (45h) 编码为 D5.2<br>• 对于 Gen3，TS2 标识符 (45h)|
|14‐15|• 对于 Gen1 或 Gen2，TS2 标识符 (45h) 编码为 D5.2<br>• 对于 Gen3，TS2 标识符 (45h)，或 DC 平衡符号|

## **PCI Express Technology**

## **链路训练和状态状态机 (LTSSM)**

## **概述**

第 519 页的图 14‐6 说明了链路训练和状态状态机 (LTSSM) 的顶层状态。每个状态由子状态组成。退出基本复位（冷或热复位）或热复位后进入的第一个 LTSSM 状态是 Detect 状态。

LTSSM 由 11 个顶层状态组成：Detect、Polling、Configuration、Recovery、L0、L0s、L1、L2、Hot Reset、Loopback 和 Disable。这些可以分为五类：

1. 链路训练状态

2. 重新训练（Recovery）状态

3. 软件驱动的电源管理状态

4. 活动状态电源管理 (ASPM) 状态

5. 其他状态

退出任何类型的复位时，LTSSM 的流程遵循**链路训练状态**：Detect => Polling => Configuration => L0。在 L0 状态下，正常的分组传输/接收正在进行。

**链路重新训练（也称为 Recovery）**状态进入的原因有很多，例如从低功耗链路状态（如 L1）返回，更改链路带宽（通过速度或宽度更改）。在此状态下，链路根据需要重复尽可能多的训练过程来处理该问题，然后返回 L0（正常操作）。

电源管理软件还可以将设备置于低功耗设备状态（D1、D2、D3Hot 或 D3Cold），这将强制链路进入较低的**电源管理链路状态**（L1 或 L2）。

如果一段时间没有要发送的分组，则可以允许 ASPM 硬件自动将链路转换为低功耗 **ASPM 状态**（L0s 或 ASPM L1）。

此外，软件可以指导链路进入一些**其他特殊状态**：Disabled、Loopback 或 Hot Reset。在这里，这些统称为其他状态组。

**第 14 章：链路初始化与训练**

_图 14‐6：链路训练和状态状态机 (LTSSM)_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0490.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>

## **Overview of LTSSM States** 

Below is a brief description of the 11 high‐level LTSSM states. 

- **Detect** : The initial state after reset. In this state, a device electrically detects a Receiver is present at the far end of the Link.
That’s an unusual thing in the world of serial transports, but it’s done to facilitate testing, as we’ll see in the next state. Detect may
also be entered from a number of other LTSSM states as described later.

- **Polling** : In this state, Transmitters begin to send TS1s and TS2s (at 2.5 GT/s for backward compatibility) so that Receivers can use
them to accomplish the following:

 - Achieve Bit Lock 

 - Acquire Symbol Lock or Block Lock 

 - Correct Lane polarity inversion, if needed 

 - Learn available Lane data rates 

 - If directed, Initiate the Compliance test sequence: The way this works is that if a receiver was detected in the Detect state but no
incoming signal is seen, it’s understood to mean that the device has been connected to a test load. In that case, it should send the
specified Compliance test pat‐ tern to facilitate testing. This allows test equipment to quickly verify that voltage, BER, timing, and other
parameters are within tolerance.

- **Configuration** : Upstream and Downstream components now play specific roles as they continue to exchange TS1s and TS2s at 2.5 GT/s to
accomplish the following:

 - Determine Link width 

 - Assign Lane numbers 

 - Optionally check for Lane reversal and correct it 

 - Deskew Lane‐to‐Lane timing differences 

 - From this state, scrambling can be disabled, the Disable and Loopback states can be entered, and the number of FTS Ordered Sets required
to transition from the L0s state to the L0 state is recorded from the TS1s and TS2s.

- **L0** : This is the normal, fully‐active state of a Link during which TLPs, DLLPs and Ordered Sets can be exchanged. In this state, the
Link could be running at higher speeds than 2.5 GT/s, but only after re‐training (Recovery) the Link and going through a speed change
procedure.

- **Recovery** : This state is entered when the Link needs re‐training. This could be caused by errors in L0, or recovery from L1 back to
L0, or recovery from L0s if the Link does not train properly using the FTS sequence. In Recovery, Bit Lock and Symbol/Block Lock are
re‐established in a manner similar to that used in the Polling state but it typically takes much less time.

- **L0s** : This ASPM state is designed to provide some power savings while affording a quick recovery time back to L0. It’s entered when
one Transmitter sends the EIOS while in the L0 state. Exit from L0s involves sending FTSs to quickly re‐acquire Bit and Symbol/Block Lock.

- **L1** : This state provides greater power savings by trading off a longer recovery time than L0s does (see “Active State Power Management
(ASPM)” on page 735). Entry into L1 involves a negotiation between both Link partners to enter it together and can occur in one of two ways:

 - The first is autonomous with ASPM: hardware in an Upstream Port with no scheduled TLPs or DLLPs to transmit can automatically negotiate
to put its Link into the L1 state. If the Downstream Port agrees, the Link enters L1. If not, the Upstream Port will enter L0s instead (if
enabled).

 - The second is the result of power management software issuing a com‐ manding a device to a low‐power state (D1, D2, or D3Hot). As a
result, the Upstream Port notifies the Downstream Port that they must enter L1, the Downstream Port acknowledges that, and they enter L1.
- **L2** : In this state the main power to the devices is turned off to achieve a greater power savings. Almost all of the logic is off, but
a small amount of power is still available from the Vaux source to allow the device to indicate a wakeup event. An Upstream Port that
supports this wakeup capability can send a very low frequency signal called the Beacon and a Downstream Port can forward it to the Root
Complex to get system attention (see “Beacon Sig‐ naling” on page 483). Using the Beacon, or a side‐band WAKE# signal, a device can trigger
a system wakeup event to get main power restored. [An L3 Link power state is also defined, but it doesn’t relate to the LTSSM states. The L3
state is the full‐off condition in which Vaux power is not available and a wakeup event can’t be signaled.]

- **Loopback** : This state is used for testing but exactly what a Receiver does in this mode (for example: how much of the logic
participates) is left unspeci‐ fied. The basic operation is simple enough: the device that will be the Loop‐ back Master sends TS1 Ordered
Sets that have the Loopback bit set in the Training Control field to the device that will be the Loopback Slave. When a device sees two
consecutive TS1s with the Loopback bit set, it enters the Loopback state as the Loopback Slave and echoes back everything that comes in. The
Master, recognizing that what it is sending is now being echoed, sends any pattern of Symbols that follow the 8b/10b encoding rules, and the
Slave echoes them back exactly as they were sent, providing a round‐trip ver‐ ification of Link integrity.

- **Disable** : This state allows a configured Link to be disabled. In this state, the Transmitter is in the Electrical Idle state while the
Receiver is in the low impedance state. This might be necessary because the Link has become unre‐ liable or due to a surprise removal of the
device. Software commands a device to do this by setting the Disable bit in the Link Control register. The device then sends 16 TS1s with
the Disable Link bit set in the TS1 Training Control field. Receivers are disabled when they receive those TS1s.

- **Hot Reset:** Software can reset a Link by setting the Secondary Bus Reset bit in the Bridge Control register. That causes the bridge’s
Downstream Port to send TS1s with the Hot Reset bit set in the TS1 Training Control field (see “Hot Reset (In‐band Reset)” on page 837) When
a Receiver sees two consecutive TS1s with the Hot Reset bit set, it must reset its device.

## **Introductions, Examples and State/Substates** 

The balance of this chapter covers each of the LTSSM states. Depending on the complexity of a given state, the discussion may include an
introduction, general background, and/or examples that accompanies the detailed discussion of the State/Substate. In some cases, the reader
may choose to skip the detailed cover‐

## **PCI Express Technology** 

age and jump to introductory material. Each section is organized to facilitate these options. 

Every device must perform initial link training at the base rate of 2.5 GT/s. Fig‐ ure 14‐7 highlights the states involved in the initial
training sequence. Devices capable of operating at 5.0 or 8.0 GT/s must transition to the Recovery state to change the speed to the higher
rate chosen.

## **Detect State** 

## **Introduction** 

Figure 14‐8 represents the two substates and transitions associated with the Detect state. The actions associated with the Detect state are
performed by each
transmitter in the process of detecting the presence of a receiver at the opposite end of the link. Because there are only two substates and
because they are fairly simple, we will move directly to the substate discussions.

## **Detailed Detect Substate** 

## **Detect.Quiet** 

This substate is the initial state after any reset (except Function Level Reset) or power‐up event and must be entered within 20 ms after
Reset. This substate is also entered from other states if unable to move forward (See the states that may enter Detect.Quiet in Figure 14‐8
on page 523). The properties of this substate are listed below:

- The Transmitter starts in Electrical Idle (but the DC common mode voltage doesn’t have to be within the normally‐specified range). 

- The intended data rate is set to 2.5 GT/s (Gen1). If it set to a different rate when this substate was entered, the LTSSM must stay in
this substate for 1ms before changing the rate to Gen1.

- The Physical Layer’s status bit (LinkUp = 0) informs the Data Link Layer that the Link is not operational. The LinkUp status bit is an
internal state bit

## **PCI Express Technology** 

- (not found in standard config space) and also indicates when the Physical Layer has completed Link Training (LinkUp=1), thereby informing
the Data Link Layer and Flow Control initialization to begin its part of Link initial‐ ization (for more on this, see “The FC Initialization
Sequence” on page 223).

- • Any previous equalization (Eq.) status is cleared by setting the four Link Status 2 register bits to zero: Eq. Phase 1 Successful, Eq.
Phase 2 Successful, Eq. Phase 3 Successful, Eq. Complete.

- Variables: 

 - Several variables are cleared to zero: (directed_speed_change=0b, upconfigure_capable=0b, equalization_done_8GT_data_rate=0b,
idle_to_rlock_transitioned=00h). The select_deemphasis variable setting depends on the port type: for an Upstream Port it’s selected by
hardware, while for a Downstream Port it takes the value in the Link Control 2 regis‐ ter of the Selectable Preset/De‐emphasis field.

 - Since these variables were defined beginning with the 2.0 spec version, devices designed to earlier spec versions won’t have them and
will behave as if directed_speed_change and upconfigure_capable were set to 0b and idle_to_rlock_transitioned was set to FFh.

## _Exit to “Detect.Active”_ 

The next substate is Detect.Active after a 12 ms timeout or when any Lane exits Electrical Idle. 

## **Detect.Active** 

This substate is entered from Detect.Quiet. At this time the Transmitter tests whether a Receiver is connected on each Lane by setting a DC
common mode voltage of any value in the legal range and then changing it. The detection logic observes the rate of change as the time it
takes the line voltage to charge up and compares it to an expected time, such as how long it would take without a Receiver termination. If a
Receiver is attached, the charge time will be much longer, making it easy to recognize. For more details on this process, see “Receiver
Detection” on page 460. To simplify the discussions that follow, Lanes that detect a Receiver during this substate are referred to as
“Detected Lanes.”

## _Exit to “Detect.Quiet”_

</td>
</tr></tbody></table>

<p align="center"><b>Figure 14‐7: States Involved in Initial Link Training at 2.5 Gb/s</b></p>
<p align="center"><img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0494.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0494.png">Page 494</a></sub></p>


<p align="center"><b>Figure 14‐8: Detect State Machine</b></p>
<p align="center"><img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0495.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0495.png">Page 495</a></sub></p>

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

<td style="background-color:#e8e8e8">

- 如果没有 Lane 检测到接收器，则返回 Detect.Quiet。只要未检测到接收器，它们之间的循环每 12ms 重复一次。

## _退出到 "Polling 状态"_

- 如果在所有 Lane 上都检测到接收器，则下一个状态将是 Polling。Lane 现在必须在 0 ‐ 3.6 V VTX‐CM‐DC 规格范围内驱动直流共模电压。

## _特殊情况：_

如果设备的部分（但不是全部）Lane 连接到接收器（如 x4

**第 14 章：链路初始化与训练**

设备连接到 x2 设备），则等待 12 ms 并重试。如果相同的 Lane 在第二次检测到接收器，则退出到 Polling 状态，否则返回 Detect.Quiet。如果转到 Polling，则对于未看到接收器的 Lane 有两种可能性：

1. 如果 Lane 可以作为单独的链路运行（参见第 541 页 "Designing Devices with Links that can be Merged"），使用另一个 LTSSM 并让那些 Lane 重复检测序列。

2. 如果没有其他 LTSSM 可用，则未检测到接收器的 Lane 将不是链路的一部分，必须转换到电气空闲。

## **Polling 状态**

## **介绍**

到目前为止，链路一直处于电气空闲状态，但是在 Polling 期间，LTSSM TS1 和 TS2
在两个连接的设备之间交换。此状态的主要目的是让两个设备理解彼此在说什么。换句话说，他们需要在彼此传输的位流上建立位和符号锁定，并解决任何极性反转问题。一旦完成，每个设备都成功地接收来自其链路伙伴的 TS1 和 TS2 有序集。第 525 页的图 14‐9 显示了 Polling
状态机的子状态。

_图 14‐9：Polling 状态机_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0496.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Polling 子状态详解**

## **Polling.Active**

## _在 Polling.Active 期间_

一旦其共模电压稳定在 Transmit Margin 字段指定的电平，发送器在所有检测到的 Lane 上发送至少 1024 个连续的 TS1。两个链路伙伴可以在不同时间退出 Detect 状态，因此 TS1 交换未同步。以 Gen1 速度（2.5 GT/s）发送 1024 个
TS1 所需的时间为 64μs。

关于此子状态的一些注意事项：

- TS1 的 Lane 和 Link Number 字段中必须使用 PAD 符号。

- 必须通告设备支持的所有数据速率，即使它不打算使用所有速率。

- 接收器使用传入的 TS1 获取位锁定（参见第 395 页 "Achieving Bit Lock"），然后对于较低速率获取符号锁定（参见第 396 页 "Achieving Symbol Lock"），或者对于 8.0 GT/s 获取块对齐（参见第 438 页
"Achieving Block Alignment"）。

## _退出到 "Polling.Configuration"_

- 下一个状态是 Polling.Configuration，如果在发送至少 1024 个 TS1 之后，**所有**检测到的 Lane 接收到 8 个连续的训练序列（或其补码，由于极性反转），满足以下条件之一：

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，Compliance Receive 位清零为 0b（符号 5 的位 4）。

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，符号 5 的 Loopback 位设置为 1b。

-

- 接收到的 TS2 的 Link 和 Lane 设置为 PAD。

如果上述条件未满足，则在 24ms 超时后，如果在接收到 TS1 后发送了至少 1024 个 TS1，并且**任意**检测到的 Lane 接收到八个连续的 TS1 或 TS2 有序集（或其补码），其 Lane 和 Link 编号设置为 PAD，并且以下条件之一为真：

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，Compliance Receive（符号 5 的位 4）清零为 0b。

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，Loopback（符号 5 的位 2）设置为 1b。

- 接收到的 TS2 的 Link 和 Lane 设置为 PAD。

**第 14 章：链路初始化与训练**

如果仍然不满足上述条件，则如果至少预定数量的检测到的 Lane 也自进入 Polling.Active 以来至少检测到一次电气空闲退出（这可防止一个或多个不良发送器或接收器阻碍链路配置）。准确的预定 Lane 集是特定于实现的，这是相对于 1.1
规范的变化，该规范需要在所有检测到的 Lane 上看到电气空闲退出。

## _退出到 "Polling.Compliance"_

如果 Link Control 2 寄存器中的 Enter Compliance 位设置为 1b，或者如果在进入 Polling.Active 之前设置了此位，则更改到 Polling.Compliance 必须是立即的，并且在 Polling.Active 中不发送 TS1。

否则，在 24ms 超时后，如果：

- 自进入 Polling.Active 以来，预定集中的所有 Lane 都未看到电气空闲退出（表示被动测试负载，例如至少一个 Lane 上的电阻器，迫使所有 Lane 进入 Polling.Compliance）。

- 任何检测到的 Lane 接收到 8 个连续的 TS1（或其补码），其 Link 和 Lane 编号设置为 PAD，符号 5 的 Compliance Receive 位设置为 1b 且 Loopback 位清零为 0b。

## _退出到 "Detect 状态"_

- 如果 24ms 后，转到 Polling.Configuration 或 Polling.Compliance 的条件未满足，则返回 Detect 状态。

## **Polling.Configuration**

在此子状态中，发送器将停止发送 TS1 并开始发送 TS2，Link 和 Lane 编号仍设置为 PAD。更改为发送 TS2 而不是 TS1 的目的是向链路伙伴通告此设备已准备好继续状态机中的下一个状态。这是一种握手机制，以确保链路上的两个设备一起通过
LTSSM。在两个设备都准备好之前，任何一个设备都不能继续到下一个状态。他们通过发送 TS2 有序集来通告他们已准备好。因此，一旦设备既发送又接收 TS2，它就知道它可以继续到下一个状态，因为它已准备好，其链路伙伴也已准备好。

## _在 Polling.Configuration 期间_

- 发送器在所有检测到的 Lane 上发送 Link 和 Lane 编号设置为 PAD 的 TS2，并且必须通告它们支持的所有数据速率，即使它们不打算使用。此外，每个 Lane 的接收器必须在必要时独立反转其差分输入对的极性。有关如何执行此操作的说明，请参见第 506 页
"Overview"。Transmit Margin 字段必须重置为 000b。

## **PCI Express Technology**

## _退出到 "Configuration 状态"_

在任何检测到的 Lane 上接收到八个连续的 Link 和 Lane 设置为 PAD 的 TS2，并且自接收到一个 TS2 起已发送至少 16 个 TS2 之后，退出到 Configuration。

## _退出到 "Detect 状态"_

否则，在 48ms 超时后退出到 Detect。

## _退出到 Polling.Speed（不存在的子状态）_

作为历史回顾，Polling 的子状态自规范的 1.0 版本发布以来已发生变化。当时认为当其他速度可用时，尽快在此状态下更改为最高可用速率是有意义的。然而，更高速度的出现恰好与意识到能够出于电源管理原因在运行时向上和向下更改速度将是有利的认识相吻合。通过 Polling
状态涉及清除许多链路值，这使其成为运行时使用的一条没有吸引力的路径，因此速率更改阶段从该状态移出到 Recovery 状态。参见第 528 页的图 14‐10。

_图 14‐10：具有传统速度更改的 Polling 状态机_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0497.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


如今，复位后链路始终训练到 2.5 GT/s，即使其他速度可用。如果 LTSSM 达到 L0 后有更高的速度可用，则它转换到 Recovery 并尝试更改为最高共同支持或通告的速率。支持的速度在交换的 TS1 中报告

**第 14 章：链路初始化与训练**

和 TS2，以便任一设备随后可以决定通过转换到 Recovery 状态来启动速度更改。规范仍然列出此子状态但声明它是不可达的。

## **Polling.Compliance**

此子状态仅用于测试，并使发送器发送旨在创建接近最坏情况的符号间干扰 (ISI) 和串扰条件的特定模式以便于链路分析。在此子状态中可以发送两种不同的模式，即合规模式和修改的合规模式。

**8b/10b 的合规模式。** 此模式由按顺序重复的 4 个符号组成：K28.5‐、D21.5+、K28.5+ 和 D10.2‐，其中（‐）表示负电流差或 CRD，（+）表示正 CRD（由于 CRD 是强制的，因此允许在模式开头存在差异错误）。如果链路具有多个
Lane，则四个延迟符号（在表中显示为 D，但实际上只是额外的 K28.5 符号）被注入到 Lane 0 上，两个在下一个合规模式之前，两个在之后。一旦 Lane 0 上发送了最后一个延迟符号，则四个延迟符号也在 Lane 1
上发送（同样，两个在下一个合规模式之前，两个在之后）。此过程继续进行，直到延迟符号传播通过 Lane 7。然后它们回到 Lane 0 重新开始，如第 529 页表 14‐3 所示（合规模式以灰色阴影显示）。每八个 Lane 的组都是这样的行为。移动延迟符号将确保相邻 Lane
之间的干扰并提供更好的测试条件。

_表 14‐3：8b/10b 合规模式的符号序列_

|**符号**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|


## **PCI Express Technology**

_表 14‐3：8b/10b 合规模式的符号序列（续）_

|**符号**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|6|D|K28.5+|K28.5+||D|
|7|D|D10.2|D10.2||D|
|8|K28.5‐|D|K28.5‐||K28.5‐|
|9|K21.5|D|K21.5||K21.5|
|10|K28.5+|K28.5‐|K28.5+||K28.5+|
|...|...|...|...||...|
|16|K28.5‐|K28.5‐|D||K28.5‐|
|17|K21.5|K21.5|D||K21.5|
|18|K28.5+|K28.5+|K28.5‐||K28.5+|


**128b/130b 的合规模式。** 此模式由以下 36 个块的重复序列组成：

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-12-3"></a>
## 12.3 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- If no Lanes detect a Receiver, go back to Detect.Quiet. The loop between them is repeated every 12ms, as long as no Receiver is detected. 

## _Exit to “Polling State”_ 

- If a receiver is detected on all Lanes, the next state will be Polling. The Lanes must now drive a DC common voltage within the 0 ‐ 3.6 V
VTX‐CM‐DC spec.

## _Special Case:_ 

If some but not all Lanes of a device are connected to a Receiver (like a x4 
device connected to a x2 device), then wait 12 ms and try it again. If the same Lanes detect a Receiver the second time, exit to the Polling
state, oth‐ erwise go back to Detect.Quiet. If going to Polling, there are two possibili‐ ties for the Lanes that didn’t see a Receiver:

1. If the Lanes can operate as a separate Link (see “Designing Devices with Links that can be Merged” on page 541), use another LTSSM and
have those Lanes repeat the detect sequence.

2. If another LTSSM is not available, then the Lanes that don’t detect a Receiver will not be part of a Link and must transition to
Electrical Idle.

## **Polling State** 

## **Introduction** 

To this point the link has been in the electrical idle state, however during Polling the LTSSM TS1s and TS2s are exchanged between the two
connected devices. The primary purpose of this state is for the two devices to understand what the each other is saying. In other words,
they need to establish bit and symbol lock on each other’s transmitted bit stream and resolve any polarity inversion issues. Once this has
been accomplished, each device is successfully receiving the TS1 and TS2 ordered‐sets from their link partner. Figure 14‐9 on page 525 shows
the substates of the Polling state machine.

_Figure 14‐9: Polling State Machine_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0498.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Detailed Polling Substates** 

## **Polling.Active** 

## _During Polling.Active_ 

Transmitters send a minimum of 1024 consecutive TS1s on all detected Lanes once their common‐mode voltage has settled at the level specified
in the Transmit Margin field. The two Link partners may exit the Detect state at different times, so the TS1 exchange is not synchronized.
The time needed to send 1024 TS1s at Gen1 speed (2.5 GT/s) is 64μs.

Some notes regarding this substate are: 

- The PAD Symbol must be used in the Lane and Link Number fields of the TS1s. 

- All data rates a device supports must be advertised, even if it doesn’t intend to use them all. 

- Receivers use the incoming TS1s to acquire Bit Lock (see “Achieving Bit Lock” on page 395) and then either Symbol Lock (see “Achieving
Symbol Lock” on page 396) for the lower rates, or Block Alignment for 8.0 GT/s (see “Achieving Block Alignment” on page 438).

## _Exit to “Polling.Configuration”_ 

- The next state is Polling.Configuration if, after sending at least 1024 TS1s **ALL** detected Lanes receive 8 consecutive training
sequences (or their com‐ plement, due to polarity inversion) that satisfy one of the following condi‐ tions:

- TS1s with Link and Lane set to PAD were received with the Compli‐ ance Receive bit cleared to 0b (bit 4 of Symbol 5). 

- TS1s with Link and Lane set to PAD were received with the Loopback bit of Symbol 5 set to 1b. 

- 

- TS2s were received with Link and Lane set to PAD. 

If the conditions above are not met, then after a 24ms timeout, if at least 1024 TS1s were sent after receiving a TS1, and **ANY** detected
Lane received eight consecutive TS1 or TS2 Ordered Sets (or their complement) with the Lane and Link numbers set to PAD, and one of the
following is true:

- TS1s with Link and Lane set to PAD were received with the Compli‐ ance Receive (bit 4 of Symbol 5) cleared to 0b. 

- TS1s with Link and Lane set to PAD were received with the Loopback (bit 2 of Symbol 5) set to 1b. 

- TS2s were received with Link and Lane set to PAD. 
If still none of the conditions above are met, if at least a predetermined number of detected Lanes also detected an exit from Electrical
Idle at least once since entering Polling.Active (this prevents one or more bad Transmit‐ ters or Receivers from holding up Link
configuration). The exact set of pre‐ determined Lanes is implementation specific now, which is a change from the 1.1 spec that needed to
see an Electrical Idle exit on all detected Lanes.

## _Exit to “Polling.Compliance”_ 

If the Enter Compliance bit in the Link Control 2 register is set to 1b, or if this bit was set before entering Polling.Active, the change
to Polling.Com‐ pliance must be immediate and no TS1s are sent in Polling.Active.

Otherwise, after a 24ms timeout, if: 

- All Lanes from the predetermined set have not seen an exit from Elec‐ trical Idle since entering Polling.Active (indicates a passive test
load such as a resistor on at least one Lane forces all Lanes into Poll‐ ing.Compliance).

- Any detected Lane received 8 consecutive TS1s (or their complement) with Link and Lane numbers set to PAD, the Compliance Receive bit of
Symbol 5 set to 1b and the Loopback bit cleared to 0b.

## _Exit to “Detect State”_ 

- If, after 24ms, the conditions for going to Polling.Configuration or Poll‐ ing.Compliane are not met, return to the Detect state. 

## **Polling.Configuration** 

In this substate, a transmitter will stop sending TS1s and start sending TS2s, still with PAD set for the Link and Lane numbers. The purpose
of the change to sending TS2s instead of TS1s is to advertise to the link partner that this device is ready to proceed to the next state in
the state machine. It is a handshake mecha‐ nism to ensure that both devices on the link proceed through the LTSSM together. Neither device
can proceed to the next state until both devices are ready. The way they advertise they are ready is by sending TS2 ordered‐sets. So once a
device is both sending AND receiving TS2s, it knows it can proceed to the next state because it is ready and its link partner is ready too.

## _During Polling.Configuration_ 

- Transmitters send TS2s with Link and Lane numbers set to PAD on all detected Lanes, and they must advertise all the data rates they
support, even those they don’t intend to use. Also, each Lane’s receiver must inde‐ pendently invert the polarity of its differential input
pair if necessary. For an explanation of how this is done, see “Overview” on page 506. The Trans‐ mit Margin field must be reset to 000b.

## **PCI Express Technology** 

## _Exit to “Configuration State”_ 

After eight consecutive TS2s with Link and Lane set to PAD are received on any detected Lanes, and at least 16 TS2s have been sent since
receiving one TS2, exit to Configuration.

## _Exit to “Detect State”_ 

Otherwise, exit to Detect after a 48ms timeout. 

## _Exit to Polling.Speed (Non‐existent substate)_ 

As a historical aside, the substates of Polling have changed since the 1.0 version of the spec was released. At that time it was thought
that when other speeds became available it would make sense to change to the highest available rate as soon as possible in this state.
However, the advent of higher rates coincided with the realization that it would be advantageous to be able to change speeds both higher and
lower during runtime for power management reasons. Going through the Polling state involves clearing a number of Link values and that makes
it an unattractive path for runtime use, so the rate change stage was moved out of this state into the Recovery state. See Figure 14‐10 on
page 528.

_Figure 14‐10: Polling State Machine with Legacy Speed Change_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0499.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


Today, the Link always trains to 2.5 GT/s after a reset, even if other speeds are available. If higher speeds are available once the LTSSM
has reached L0, then it transitions to Recovery and attempts to change to the highest commonly‐sup‐ ported or advertised rate. Supported
speeds are reported in the exchanged TS1s
and TS2s, so that either device can subsequently decide to initiate a speed change by transitioning to the Recovery state. The spec still
lists this substate but declares that it is now unreachable.

## **Polling.Compliance** 

This substate is only used for testing and causes a Transmitter to send specific patterns intended to create near‐worst‐case Inter‐Symbol
Interference (ISI) and cross‐talk conditions to facilitate analysis of the Link. Two different patterns can be sent while in this substate,
the Compliance Pattern and the Modified Compli‐ ance Pattern.

**Compliance Pattern for 8b/10b.** This pattern consists of 4 Symbols that are repeated sequentially: K28.5‐, D21.5+, K28.5+ and D10.2‐,
where (‐) means negative current running disparity or CRD and (+) means positive CRD (since the CRD is forced, it’s permissible to have a
disparity error at the beginning of the pattern). If the Link has multiple Lanes, then four Delay Symbols (shown as D, but are really just
additional K28.5 symbols) are injected on Lane 0, two before the next compliance pattern and two after the compliance pattern. Once the last
Delay symbol has been sent on Lane 0, the four delay symbols are also sent on Lane 1 (again, two before the next compliance pattern and two
after). This process continues until after the Delay symbols have propagated through Lane 7. Then they go back to start‐ ing on Lane 0 again
as can be seen in Table 14‐3 on page 529 (the compli‐ ance pattern is shaded in grey). Every group of eight lanes behaves this way. Shifting
the Delay Symbols will ensure interference between adjacent Lanes and provide better test conditions.

_Table 14‐3: Symbol Sequence 8b/10b Compliance Pattern_ 

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|


## **PCI Express Technology** 

_Table 14‐3: Symbol Sequence 8b/10b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|6|D|K28.5+|K28.5+||D|
|7|D|D10.2|D10.2||D|
|8|K28.5‐|D|K28.5‐||K28.5‐|
|9|K21.5|D|K21.5||K21.5|
|10|K28.5+|K28.5‐|K28.5+||K28.5+|
|...|...|...|...||...|
|16|K28.5‐|K28.5‐|D||K28.5‐|
|17|K21.5|K21.5|D||K21.5|
|18|K28.5+|K28.5+|K28.5‐||K28.5+|


**Compliance Pattern for 128b/130b.** This pattern consists of the follow‐ ing repeating sequence of 36 Blocks:

</td>
<td style="background-color:#e8e8e8">

- 如果没有 Lane 检测到接收器，则返回到 Detect.Quiet。它们之间的循环每 12ms 重复一次，只要没有检测到接收器。

## _退出至"Polling 状态"_

- 如果在所有 Lane 上都检测到接收器，则下一个状态将是 Polling。Lane 现在必须在 0 至 3.6 V VTX‐CM‐DC 规范内驱动直流共模电压。

## _特殊情况：_

如果设备的一些但不是所有 Lane 连接到接收器（例如 x4

**第 14 章：链路初始化与训练**

设备连接到 x2 设备），则等待 12 ms 并重试。如果相同的 Lane 在第二次时检测到接收器，则退出到 Polling 状态，否则返回到 Detect.Quiet。如果转到 Polling，对于未看到接收器的 Lane 有两种可能性：

1. 如果 Lane 可以作为单独的链路运行（请参阅第 541 页的"设计具有可合并链路的设备"），请使用另一个 LTSSM 并让这些 Lane 重复检测序列。

2. 如果另一个 LTSSM 不可用，则未检测到接收器的 Lane 将不属于该链路的一部分，并且必须转换为电气空闲 (Electrical Idle)。

## **Polling 状态**

## **简介**

到此为止，链路一直处于电气空闲状态，然而在 Polling 期间，LTSSM TS1 和 TS2 在两个连接的设备之间交换。此状态的主要目的是让两个设备理解彼此的通信内容。换句话说，它们需要在彼此传输的比特流上建立位和符号锁定 (bit and symbol
lock)，并解决任何极性反转问题。一旦完成此操作，每个设备都成功地接收来自其链路伙伴的 TS1 和 TS2 有序集。第 525 页图 14-9 显示了 Polling 状态机的子状态。

_图 14-9：Polling 状态机_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0500.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">


**PCI Express 技术**

## **详细的 Polling 子状态**

## **Polling.Active**

## _在 Polling.Active 期间_

一旦其共模电压稳定在 Transmit Margin 字段指定的水平上，发送器将在所有检测到的 Lane 上发送最少 1024 个连续的 TS1。两个链路伙伴可以在不同时间退出 Detect 状态，因此 TS1 交换未同步。在 Gen1 速度 (2.5 GT/s) 下发送
1024 个 TS1 所需的时间为 64μs。

关于此子状态的一些注意事项：

- PAD 符号必须用于 TS1 的 Lane 和 Link Number 字段中。

- 必须通告设备支持的所有数据速率，即使它不打算使用全部。

- 接收器使用传入的 TS1 获得位锁定 (Bit Lock)（请参阅第 395 页的"实现位锁定"），然后对于较低速率为符号锁定 (Symbol Lock)（请参阅第 396 页的"实现符号锁定"），或者对于 8.0 GT/s 为块对齐 (Block
Alignment)（请参阅第 438 页的"实现块对齐"）。

## _退出至"Polling.Configuration"_

- 如果在发送至少 1024 个 TS1 之后，**所有**检测到的 Lane 收到 8 个连续的训练序列（或其补码，由于极性反转），满足以下条件之一，则下一个状态为 Polling.Configuration：

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Compliance Receive 位清零为 0b (Symbol 5 的位 4)。

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Symbol 5 的 Loopback 位置为 1b。

- 

- 接收到 Link 和 Lane 设置为 PAD 的 TS2。

如果以上条件均不满足，则在 24ms 超时后，如果在收到 TS1 后已发送至少 1024 个 TS1，并且**任何**检测到的 Lane 收到 8 个连续的 TS1 或 TS2 有序集（或其补码），其 Lane 和 Link 号设置为 PAD，并且以下之一为真：

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Compliance Receive (Symbol 5 的位 4) 清零为 0b。

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Loopback (Symbol 5 的位 2) 置为 1b。

- 接收到 Link 和 Lane 设置为 PAD 的 TS2。

**第 14 章：链路初始化与训练**

如果以上条件仍然不满足，则如果至少预定数量的检测 Lane 也检测到自进入 Polling.Active 以来至少一次退出电气空闲（这可以防止一个或多个有问题的发送器或接收器阻碍链路配置）。预定 Lane 的确切集合现在是特定于实现的，这是相对于 1.1
规范的更改，后者需要查看所有检测到的 Lane 上的电气空闲退出。

## _退出至"Polling.Compliance"_

如果 Link Control 2 寄存器中的 Enter Compliance 位置为 1b，或者如果该位在进入 Polling.Active 之前已置位，则转换到 Polling.Compliance 必须是即时的，并且在 Polling.Active 中不发送 TS1。

否则，在 24ms 超时后，如果：

- 预定集合中的所有 Lane 自进入 Polling.Active 以来未观察到退出电气空闲（表明存在被动测试负载，例如至少一个 Lane 上的电阻迫使所有 Lane 进入 Poll‐ ing.Compliance）。

- 任何检测到的 Lane 收到 8 个连续的 TS1（或其补码），其 Link 和 Lane 号设置为 PAD，Symbol 5 的 Compliance Receive 位置为 1b 且 Loopback 位清零为 0b。

## _退出至"Detect 状态"_

- 如果在 24ms 后，未满足转到 Polling.Configuration 或 Poll‐ ing.Compliance 的条件，则返回到 Detect 状态。

## **Polling.Configuration**

在此子状态下，发送器将停止发送 TS1 并开始发送 TS2，Link 和 Lane 号仍设置为 PAD。更改为发送 TS2 而不是 TS1 的目的是向链路伙伴通告此设备已准备好进入状态机中的下一状态。这是一种握手机制，以确保链路上的两个设备一起通过 LTSSM
前进。在两个设备都准备好之前，任何设备都不能进入下一状态。它们通过发送 TS2 有序集来通告它们已准备好。因此，一旦设备同时发送并接收 TS2，它就知道可以进入下一状态，因为它已准备好且其链路伙伴也已准备好。

## _在 Polling.Configuration 期间_

- 发送器在所有检测到的 Lane 上发送 Link 和 Lane 号设置为 PAD 的 TS2，并且必须通告其支持的所有数据速率，即使它不打算使用。此外，每个 Lane 的接收器必须根据需要独立反转其差分输入对的极性。有关如何完成此操作的说明，请参阅第 506
页的"概述"。Transmit Margin 字段必须重置为 000b。

## **PCI Express 技术**

## _退出至"Configuration 状态"_

在任何检测到的 Lane 上收到 8 个连续的 Link 和 Lane 设置为 PAD 的 TS2，并且自收到一个 TS2 以来已发送至少 16 个 TS2 之后，退出到 Configuration。

## _退出至"Detect 状态"_

否则，在 48ms 超时后退出到 Detect。

## _退出至 Polling.Speed（不存在的子状态）_

作为历史回顾，自规范 1.0 版本发布以来，Polling 的子状态已发生变化。当时认为，当其他速度可用时，应尽快在此状态下更改为最高可用速率。然而，更高速度的出现恰好伴随着这样的认识：在运行时出于电源管理原因同时更改更高和更低速度将是有利的。通过 Polling
状态涉及清除许多链路值，这使其成为运行时使用的不具吸引力的路径，因此速率更改阶段已从该状态移出到 Recovery 状态。请参阅第 528 页图 14-10。

_图 14-10：具有旧式速度更改的 Polling 状态机_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0501.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">


如今，链路在复位后始终训练到 2.5 GT/s，即使其他速度可用。如果在 LTSSM 达到 L0 后有更高速率可用，则它转换到 Recovery 并尝试更改为最高共同支持或通告的速率。支持的速度在交换的 TS1 中报告。

**第 14 章：链路初始化与训练**

和 TS2，以便任一设备随后都可以通过转换到 Recovery 状态来决定发起速度更改。规范仍列出此子状态，但声明它现在不可达。

## **Polling.Compliance**

此子状态仅用于测试，并导致发送器发送旨在产生接近最坏情况的符号间干扰 (Inter‐Symbol Interference, ISI) 和串扰条件的特定模式，以促进对链路的分析。在此子状态下可以发送两种不同的模式：Compliance Pattern 和 Modified
Compliance Pattern。

**8b/10b 的合规模式。** 此模式由按顺序重复的 4 个符号组成：K28.5‐、D21.5+、K28.5+ 和 D10.2‐，其中 (‐) 表示负电流运行差异 (CRD)，(+) 表示正 CRD（由于强制 CRD，模式开头可以存在差异错误）。如果链路有多个
Lane，则四个延迟符号（显示为 D，但实际上只是其他 K28.5 符号）被注入到 Lane 0 上，在下一个合规模式之前两个，在合规模式之后两个。最后一个延迟符号在 Lane 0 上发送后，四个延迟符号也在 Lane 1
上发送（同样，在下一个合规模式之前两个，在之后两个）。此过程继续进行，直到延迟符号传播通过 Lane 7。然后它们返回到从 Lane 0 重新开始，如第 529 页表 14-3 所示（合规模式以灰色阴影显示）。每组八个 Lane 都以这种方式表现。移动延迟符号将确保相邻 Lane
之间的干扰，并提供更好的测试条件。

_表 14-3：8b/10b 合规模式的符号序列_

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|


## **PCI Express 技术**

_表 14-3：8b/10b 合规模式的符号序列（续）_

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|6|D|K28.5+|K28.5+||D|
|7|D|D10.2|D10.2||D|
|8|K28.5‐|D|K28.5‐||K28.5‐|
|9|K21.5|D|K21.5||K21.5|
|10|K28.5+|K28.5‐|K28.5+||K28.5+|
|...|...|...|...||...|
|16|K28.5‐|K28.5‐|D||K28.5‐|
|17|K21.5|K21.5|D||K21.5|
|18|K28.5+|K28.5+|K28.5‐||K28.5+|


**128b/130b 的合规模式。** 此模式由以下 36 个块的重复序列组成：

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-12-4"></a>
## 12.4 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

1. The first Block consists of the Sync Header 01b and contains the unscrambled payload of 64 ones followed by 64 zeros. 

2. The second Block has Sync Header 01b and contains the unscrambled payload shown in Table 14‐4 on page 530 (note that the pattern repeats
after 8 Lanes, and that P means the 4‐bit Tx preset being used, while ~P is the bit‐wise inverse of that).

3. The third Block has Sync Header 01b and contains the unscrambled payload shown in Table 14‐5 on page 531 (same notes as the second
Block).

4. The fourth Block is an EIEOS Block 

5. 32 more Data Blocks, each containing 16 scrambled IDL Symbols (00h). 

_Table 14‐4: Second Block of 128b/130b Compliance Pattern_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|0|55h|FFh|FFh|FFh|55h|FFh|FFh|FFh|
|1|55h|FFh|FFh|FFh|55h|FFh|FFh|FFh|


_Table 14‐4: Second Block of 128b/130b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|2|55h|00h|FFh|FFh|55h|FFh|FFh|FFh|
|3|55h|00h|FFh|C0h|55h|FFh|F0h|F0h|
|4|55h|00h|FFh|00h|55h|FFh|00h|00h|
|5|55h|00h|C0h|00h|55h|E0h|00h|00h|
|6|55h|00h|00h|00h|55h|00h|00h|00h|
|7|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|
|8|00h|1Eh|2Dh|3Ch|4Bh|5Ah|69h|78h|
|9|00h|55h|00h|00h|00h|55h|00h|F0h|
|10|00h|55h|00h|00h|00h|55h|00h|00h|
|11|00h|55h|00h|00h|00h|55h|00h|00h|
|12|00h|55h|0Fh|0Fh|00h|55h|07h|00h|
|13|00h|55h|FFh|FFh|00h|55h|FFh|00h|
|14|00h|55h|FFh|FFh|7Fh|55h|FFh|00h|
|15|00h|55h|FFh|FFh|FFh|55h|FFh|00h|


_Table 14‐5: Third Block of 128b/130b Compliance Pattern_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|0|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|1|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|2|FFh|FFh|55h|FFh|FFh|FFh|55h|FFh|
|3|F0h|F0h|55h|F0h|F0h|F0h|55h|F0h|
|4|00h|00h|55h|00h|00h|00h|55h|00h|


## **PCI Express Technology** 

_Table 14‐5: Third Block of 128b/130b Compliance Pattern (Continued)_ 

|**Symbol**|**Lane**<br>**0**|**Lane**<br>**1**|**Lane**<br>**2**|**Lane**<br>**3**|**Lane**<br>**4**|**Lane**<br>**5**|**Lane**<br>**6**|**Lane**<br>**7**|
|---|---|---|---|---|---|---|---|---|
|5|00h|00h|55h|00h|00h|00h|55h|00h|
|6|00h|00h|55h|00h|00h|00h|55h|00h|
|7|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|{P,~P}|
|8|00h|1Eh|2Dh|3Ch|4Bh|5Ah|69h|78h|
|9|00h|00h|00h|55h|00h|00h|00h|55h|
|10|00h|00h|00h|55h|00h|00h|00h|55h|
|11|00h|00h|00h|55h|00h|00h|00h|55h|
|12|FFh|0Fh|0Fh|55h|0Fh|0Fh|0Fh|55h|
|13|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|
|14|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|
|15|FFh|FFh|FFh|55h|FFh|FFh|FFh|55h|


**Modified Compliance Pattern for 8b/10b.** The second compliance pat‐ tern adds an error status field that reports how many Receiver errors
have been detected while in Polling.Compliance.

In 8b/10b mode, the original pattern is still used, but 2 Symbols are added to report the error status (2 are used instead of one to avoid
interfering with the required disparity of the sequence) and 2 more K28.5 Symbols are added at the end, making the pattern 8 Symbols long
altogether.

_Table 14‐6: Symbol Sequence of 8b/10b Modified Compliance Pattern_ 

|Symbol|Lane 0|Lane 1|Lane 2|...|Lane 8|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|D|K28.5+|K28.5+||D|
|3|D|D10.2|D10.2||D|


_Table 14‐6: Symbol Sequence of 8b/10b Modified Compliance Pattern (Continued)_ 

|Symbol|Lane 0|Lane 1|Lane 2|...|Lane 8|
|---|---|---|---|---|---|
|4|K28.5‐|ERR|ERR||K28.5‐|
|5|K21.5|ERR|ERR||K21.5|
|6|K28.5+|K28.5‐|K28.5‐||K28.5+|
|7|D10.2|K28.5+|K28.5+||D10.2|
|8|ERR|K28.5‐|K28.5‐||ERR|
|9|ERR|K21.5|K21.5||ERR|
|10|K28.5‐|K28.5+|K28.5+||K28.5‐|
|11|K28.5+|D10.2|D10.2||K28.5+|
|12|K28.7‐|ERR|ERR||K28.7‐|
|13|K28.7‐|ERR|ERR||K28.7‐|
|14|K28.7‐|K28.5‐|K28.5‐||K28.7‐|
|15|K28.7‐|K28.5+|K28.5+||K28.7‐|
|16|K28.5‐|D|K28.5‐||K28.5‐|


The encoded error status byte contains a Receiver Error Count in ERR [6:0] that reports the number of errors seen since Pattern Lock was
asserted. The “Pattern Lock” indicator is ERR bit [7], and shows when the Receiver has locked to the incoming Modified Compliance Pattern.
The delay sequence is also different for this pattern, and now adds four K28.5 Symbols (shown as “D” in the table) in a row at the beginning
of the sequence and four K28.7 Symbols at the end of the 8‐Symbol pattern, making a total of 16 Symbols that are sent before the Delay
pattern shifts to the next Lane. This pattern is illustrated in Table 14‐6 on page 532. It can be seen that the delay pattern shifts to Lane
1 after 16 Symbols. As before, the basic pattern (8‐Symbols now) is highlighted in grey.

**Modified Compliance Pattern for 128b/130b.** This pattern consists of a repeating sequence of 65792 Blocks as listed here: 

1. One EIEOS Block 

2. 256 Data Blocks of 16 scrambled IDL Symbols (00h) each. 

3. 255 sets of the following sequence: 

 - One SOS 

 - 256 Data Blocks of 16 scrambled IDL Symbols each. 

Since the payload in the Data Blocks is all zeros, the output ends up being simply the output of the scrambler for that Lane. Recall that
the scrambler doesn’t advance with the Sync Header bits and is initialized by the EIEOS. Since the scrambler seed value depends on the Lane
number, it’s important that they be understood correctly. If Link training completed earlier but then software sent the LTSSM to this
substate by setting the Enter Compli‐ ance bit in the Link Control 2 register, then the Lane numbers and polarity inversions that were
assigned during training are used. If a Lane wasn’t active during training, or if this substate was entered in any other way, then the Lane
numbers will be the default numbers assigned by the Port. Finally, note that the Data Blocks in this pattern don’t form a Data Stream and
don’t have to follow the requirements for that (such as sending any SDS Ordered Sets or EDS Tokens).

The thoughtful reader may be wondering about the absence of error status Symbols in this sequence that are prominent in the 8b/10b sequence.
As it turns out, for 128b/130b they’re included inside the SOSs now. Recall that the last 2 bytes of the SOS are used to report the Receiver
error count during Polling.Compliance (see “Ordered Set Example ‐ SOS” on page 426 for more on this).

## _Entering Polling.Compliance:_ 

As was the case when entering Polling.Active, the Transmit Margin field of the Link Control 2 register is used to set the Transmitter
voltage range that will be in effect while in this substate.

The data rate and de‐emphasis level are determined as described below. Since many of the choices about these settings depend on the Link
Control 2 register fields, that register is shown in Figure 14‐11 on page 536 for refer‐ ence.

- If a Port only supports 2.5 GT/s, then that will be the data rate and the de‐ emphasis level will be ‐3.5dB. 

- Otherwise, if this substate was entered because 8 consecutive TS1s were received with the Compliance Receive bit set to 1b and the
Loopback bit cleared to 0b (bits 4 and 2 of TS1 Symbol 5), then the rate will be the high‐ est common value for any Lane. The
select_deemphasis variable must be set to match the Selectable De‐emphasis bit in TS1 Symbol 4. If the chosen rate is 8.0 GT/s, the
select_preset variable on each Lane is taken from
Symbol 6 of the consecutive TS1s. For this Gen3 rate, Lanes that didn’t receive 8 consecutive TS1s with Transmitter Preset information can
choose any value they support.

- Otherwise, if the Enter Compliance bit is set in the Link Control 2 regis‐ ter, the compliance pattern is transmitted at the data rate
given by the Target Link Speed field. If the rate will be 5.0 GT/s, the select_deemphasis variable is set if the Compliance
Preset/De‐emphasis field equals 0001b. If the rate will be 8.0 GT/s, the select_preset variable of each Lane is cleared to 0b and the
Transmitter must use the Compliance Preset/De‐emphasis value, as long as it isn’t a Reserved encoding.

- Finally, if none of the other cases are true, then the data rate, preset, and de‐emphasis settings will cycle through a sequence based on
the compo‐ nent’s maximum supported speed and the number of times Polling.Com‐ pliance is entered this way. The sequence is given in Table
14‐7 on page 535 and begins with Setting Number 1 the first time Polling.Compli‐ ance is entered, it increments through the list each time
it’s re‐entered, and eventually repeats the pattern if it’s re‐entered more than 14 times. This provides a handy way to test all of a
component’s supported set‐ tings: transition to Polling.Compliance, test that setting, transition back to Polling.Active, then back to
Polling.Compliance again to test the next set‐ ting. A method for a load board to cause these transitions is described in the spec, and
consists of sending a 100MHz, 350mVp‐p signal for about 1ms on one leg of a receiver’s differential pair.

_Table 14‐7: Sequence of Compliance Tx Settings_ 

|Setting<br>Number|Data<br>Rate|De‐<br>emphasis|Tx Preset<br>Encoding|
|---|---|---|---|
|1|2.5|‐3.5|n/a|
|2|5.0|‐3.5|n/a|
|3|5.0|‐6.0|n/a|
|4|8.0|n/a|0000b|
|5|8.0|n/a|0001b|
|6|8.0|n/a|0010b|
|7|8.0|n/a|0011b|
|8|8.0|n/a|0100b|


## **PCI Express Technology** 

_Table 14‐7: Sequence of Compliance Tx Settings (Continued)_ 

|Setting<br>Number|Data<br>Rate|De‐<br>emphasis|Tx Preset<br>Encoding|
|---|---|---|---|
|9|8.0|n/a|0101b|
|10|8.0|n/a|0110b|
|11|8.0|n/a|0111b|
|12|8.0|n/a|1000b|
|13|8.0|n/a|1001b|
|14|8.0|n/a|1010b|


_Figure 14‐11: Link Control 2 Register_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0502.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


If the data rate won’t be 2.5 GT/s, then: 

- If any TS1s were sent during Polling.Active, the Transmitter must send either one or two consecutive EIOSs before going into Electrical
Idle.

- If no TS1s were sent in Polling.Active, the transmitter enters Electrical Idle without sending any EIOSs. 

- The Electrical Idle period must be >1ms and <2ms. During this time, the data rate is changed to the new speed and stabilized. If the rate
will be 5.0 GT/s, the de‐emphasis level is given by the select_deemphasis variable
(0b = ‐3.5dB, 1b = ‐6.0 dB). If the rate will be 8.0 GT/s, then the select_preset variable gives the transmitter presets to use. 

## _During Polling.Compliance:_ 

Once the data rate and de‐emphasis or preset values have been determined, the following rules will apply: 

**Compliance Pattern.** If entry was not due to the Compliance Receive bit set and Loopback bit cleared in the TS Ordered Sets and was not
due to both the Enter Compliance and Enter Modified Compliance bits being set in the Link Control 2 register, then Transmitters send the
compliance pattern on all detected Lanes.

## _Exit to “Polling.Active”_ 

If any of these conditions are true: 

- a) Electrical Idle exit is detected at the Receiver of any detected Lane and the Enter Compliance bit is cleared (0b).

</td>
<td style="background-color:#e8e8e8">

- 规范指出"任何 Lane"这一规定支持前面描述的负载板使用模型，以允许设备循环遍历所有支持的测试用例。

- b) Enter Compliance 位自进入 Polling.Compliance 以来已清零 (0b)。

- c) 对于上游端口，Enter Compliance 位设置为 (1b) 并且在任何 Lane 上检测到 EIOS。此条件清零 Enter Compliance 位 (0b)。

如果数据速率不是 2.5 GT/s 或在进入 Polling.Compliance 期间设置了 Enter Compliance 位，则发送器发送 8 个连续的 EIOS 并在转换到 Polling.Active 之前进入电气空闲。在电气空闲期间，端口更改为 2.5 GT/s
并稳定 1ms 到 2ms 之间的时间。

发送多个 EIOS 有助于确保链路伙伴将检测到至少一个并在用于 Enter Compliance 寄存器位进入时退出 Polling.Compliance

**修改合规模式。** 如果 Polling.Compliance 是因为 TS1 指示而进入的，并且要么设置了 Compliance Receive 位并清除了 Loopback 位，要么 Link Control 2 寄存器中的 Enter Compliance 和
Enter Modified Compliance 位都被设置，则在所有检测到的 Lane 上发送错误状态符号清零为全零的修改合规模式。

如果速率为 2.5 或 5.0 GT/s，则每个 Lane 通过查找修改合规模式的一个实例来指示对传入模式的成功锁定，然后在其发送回的修改合规模式中设置 Pattern Lock 位（8 位错误状态符号的位 7）。

- 错误状态符号不能用于锁定过程中，因为如果链路伙伴尚未锁定，它们没有意义，因此它们的含义可能是未定义的。

- 模式的一个实例定义如下所述的 4 个符号序列：K28.5、D21.5、K28.5 和 D10.2 或这些符号的补码（意味着极性反转）。

- 被测设备必须在从链路伙伴接收到修改合规模式后的 1ms 内设置其发送的修改合规模式中的 Pattern Lock 位。

- 一个 Lane 上的任何接收器错误都会将该 Lane 的错误计数递增 1，并在计数达到 127 时饱和（不会更高或回绕）。

如果速率是 8.0 GT/s

- 进入此子状态时，Error_Status 字段设置为 00h。

- 被测设备必须在从链路伙伴接收到修改合规模式后的 4ms 内设置其发送的修改合规模式中的 Pattern Lock 位。

- 每个 Lane 在实现块对齐时独立设置 Pattern Lock。之后，数据块中的符号应为 IDL (00h)，任何不匹配的符号都会将计数递增 1。接收器错误计数在 127 处饱和，并在包含在此模式中的 SOS 的最后 2 个符号中发送。

- 加扰要求照常应用于修改合规模式：种子值按 Lane 设置，EIEOS 启动 LFSR，SOS 不推进 LFSR。

- 规范指出，设备应在获取块对齐之前等待足够长的时间以确保其接收器已稳定且不会看到任何位滑动。它甚至提到设备可能希望重新验证其块对齐，然后再设置 Pattern Lock 位。

## _退出到 "Polling.Active"_

如果在进入 Polling.Compliance 时设置了 Enter Compliance 位 (1b)，并且要么 Enter Compliance 位已清零 (0b)，要么它是上游端口并在任何 Lane 上接收到 EIOS。这也会导致其 Enter Compliance
位清零 (0b)。

**第 14 章：链路初始化与训练**

如果数据速率不是 2.5 GT/s 或在进入 Polling.Compliance 期间设置了 Enter Compliance 位，则发送器发送 8 个连续的 EIOS 并在转换到 Polling.Active 之前进入电气空闲。在电气空闲期间，端口更改为 2.5 GT/s 和
‐3.5dB 去加重，并且此时间必须介于 1ms 和 2ms 之间。

发送多个 EIOS 有助于确保链路伙伴将检测到至少一个并在用于 Enter Compliance 寄存器位进入时退出 Polling.Compliance。

## _退出到 "Detect 状态"_

如果 Link Control 2 寄存器中的 Enter Compliance 位清零 (0b) 并且设备被指示退出此子状态。

_图 14‐12：Link Control 2 寄存器的 "Enter Compliance" 位_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0503.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Configuration 状态**

最初，Configuration 状态以 2.5 GT/s 速率执行链路和 Lane 编号；但是，存在允许 5 GT/s 和 8 GT/s 设备也从 Recovery 状态进入 Configuration 状态的规定。从 Recovery 到 Configuration
的转换主要是为了对多 Lane 设备的链路宽度进行动态更改。动态更改仅支持 5 GT/s 和 8 GT/s 设备。因此，这些设备的详细状态转换出现在从第 552 页开始的详细 Configuration 子状态描述中。

## **Configuration 状态 — 概述**

此状态的主要目标是发现端口是如何连接的并为其分配 Lane 编号。例如，8 个 Lane 可能可用但只有 2 个处于活动状态，或者 Lane 可以拆分为多个链路，例如两个 x4 链路。与其他状态不同，端口具有取决于它们是面向上游还是下游的已定义角色。因此，这些子状态的描述分为下游
Lane 和上游 Lane 的行为。下游端口（向下游发送的端口）在此链路上扮演"领导者"角色，以完成链路初始化过程中的其余状态。上游端口（向上游发送的端口）扮演"追随者"角色。领导者或下游端口将向上游端口指定链路和 Lane
编号，上游端口将简单地以其被告知的相同值进行回复，除非存在冲突，我们将在本节中看到这一点。链路和 Lane 编号在此期间交换的 TS1 的字段中报告，如第 540 页的图 14‐13 中再次所示。这些字段包含 PAD 符号作为占位符，直到分配实际值。

_图 14‐13：TS1/TS2 中的链路和 Lane 编号编码_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0504.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


**第 14 章：链路初始化与训练**

## **设计具有可合并链路的设备**

设计人员根据性能和成本要求选择在给定链路上实现多少 Lane。窄链路可以选择性地组合成更宽的链路，宽链路可以选择性地拆分为多个较窄的链路。第 541 页的图 14‐14 显示了具有一个上游端口和四个 x2 下游端口的交换机。在此示例中，它们还可以分组为两个 x4
链路。作为提醒，规范要求每个端口还必须支持作为 x1 链路运行。

如图的左侧所示，交换机内部由一个上游逻辑桥和四个下游逻辑桥组成。每个端口需要一个桥，因此支持 4 个下游端口需要 4 个下游桥。但是，如果端口按图的右侧所示组合，则某些桥只是未使用。在链路训练期间，每个下游端口的 LTSSM 确定实际实现的连接选项。

_图 14‐14：组合 Lane 以形成更宽的链路（链路合并）_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0505.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Configuration 状态 — 训练示例**

## **介绍**

在 Configuration 状态中，链路和 Lane 编号过程由下游端口"领导者"（例如，根端口或交换机下游端口）启动。端点和交换机上游端口不启动，但响应。它们是"追随者"。现在让我们考虑一些示例以使概念更容易理解。

## **链路配置示例 1**

第 543 页图 14‐15 中所示的设备都支持实现 x4、x2 或 x1 Lane 大小的单个链路。Lane 编号分配由设备内部固定，必须从零开始按顺序排列。物理 Lane 编号显示在设备框内，报告的或逻辑的 Lane 编号由 TS
有序集报告。通常，这些将是相同的，但并非在每种情况下都如此。

## **链路号协商。**

1. 由于此示例中只有一个链路可能，下游端口（向下游发送的端口）对所有 Lane 发送使用相同链路号 _N_ 的 TS1，Lane 号为 PAD。

2. 在此 Configuration 状态中，上游端口开始发送 Link 和 Lane 号字段中带有 PAD 的 TS1，但在接收到来自下游端口的带有非 PAD 链路号的 TS1 后，上游端口在所有连接的 Lane 上以反映相同链路号 _N_ 和 Lane 号字段的 PAD
进行响应。基于此响应，下游 LTSSM 识别出四个 Lane 已响应并使用与正在发送的相同的链路号，因此所有 4 个 Lane 将被配置为一个链路。链路号本身是特定于实现的值，不存储在任何定义的配置寄存器中，也与端口号或任何其他值无关。

**第 14 章：链路初始化与训练**

_图 14‐15：示例 1 — 步骤 1 和 2_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0506.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Lane 号协商。**

3. 下游端口现在开始发送具有相同链路号的 TS1，但为连接的 Lane 分配 Lane 号 0、1、2 和 3，如图 14‐16（第 544 页）所示。

4. 响应于传入的非 PAD Lane 号，上游端口将验证传入的 Lane 号是否与接收它们的 Lane 号匹配。在此示例中，下游和上游端口的 Lane 连接正确。因为所有 Lane 号都匹配，上游端口也在其发送的 TS1 中通告其 Lane 号。当下游端口看到响应中的非 PAD
Lane 号时，它将传入的编号与其正在发送的值进行比较。如果它们匹配，一切都很好，但如果不匹配，则需要采取其他步骤。如果一些（但不是全部）Lane 号匹配，则可以相应地调整链路宽度。如果 Lane 反转，则将需要可选的 Lane 反转功能。因为它是可选的，所以 Lane
可能已反转但任一设备都无法纠正它。这将是一个严重的板设计错误，因为在这种情况下可能无法配置链路以进行操作。

## **PCI Express Technology**

_图 14‐16：示例 1 — 步骤 3 和 4_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0507.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **确认链路和 Lane 号。**

5. 由于所有 Lane 上的发送和接收链路和 Lane 号匹配，下游端口通过发送具有相同链路和 Lane 号的 TS2 有序集来表示它已准备好结束此协商并继续到下一个状态 L0。

6. 在接收到具有相同链路和 Lane 号的 TS2 后，上游端口也通过发送回 TS2 来表示其准备好离开 Configuration 状态并继续到 L0。这在第 545 页的图 14‐17 中示出。

7. 一旦端口接收到至少 8 个 TS2 并发送至少 16 个，它将发送一些逻辑空闲数据，然后转换到 L0。

**第 14 章：链路初始化与训练**

_图 14‐17：示例 1 — 步骤 5 和 6_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0468.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


选项：一个链路 x4、x2 或 x1

## **链路配置示例 2**

应涵盖的另一个示例是具有 4 个下游 Lane 的设备，该设备能够配置为单个 x4 链路或两个 x2 链路或四个 x1 链路的组合。因此，即使一个 x2 链路和两个 x1 链路的配置也可以。此类设备的示例如第 546 页的图 14‐18 所示。

如果所有四个 Lane 都检测到接收器并达到 Configuration 状态，则有许多连接可能性：

- 一个 x4 链路

- 两个 x2 链路

- 一个 x2 链路和两个 x1 链路

- 四个 x1 链路

规范中定义的一种示例方法，用于确定实现哪些配置，如下所述。

## **链路号协商。**

1. 在此示例方法中，下游端口开始通过在每个 Lane 上通告唯一的链路号。Lane 0 通告链路号 N，Lane 1 通告链路号 N+1，依此类推，如第 546 页的图 14‐18
所示。这些链路号只是示例，它们不必是连续的。同样重要的是要记住下游端口不知道它连接到的是什么，并且在此过程中端口正在尝试确定每个 Lane 的连接。

_图 14‐18：示例 2 — 步骤 1_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0469.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


2. 在接收到返回的 TS1 时，下游端口识别出两件事：所有四个 Lane 都正常工作并且它们连接到两个不同的上游端口。这意味着实际上将有_两个_下游端口。每个下游端口将有自己的 Lane 0 和 Lane 1，如图 14‐20（第 548 页）所示。

**第 14 章：链路初始化与训练**

_图 14‐19：示例 2 — 步骤 2_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0470.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Lane 号协商。**

3. 该过程现在为每个链路独立继续，但它们将采用与之前相同的步骤来确定 Lane 号：下游端口将在 TS1 中通告其 Lane 号。还需要注意的是，下游端口开始为链路的 Lane 通告单个返回的链路号。左侧的链路正在为两个 Lane 通告链路号 N，右侧的链路正在通告 N+2。

4. 在此示例中，链路上左侧的下游和上游端口的 Lane 号匹配。但是，对于右侧的链路，下游端口的 Lane 号与连接的上游端口的 Lane 号相反。上游端口意识到这一点，如果它支持 Lane 反转，它将在内部实现并回复与下游端口通告的相同的 Lane 号，如图 14‐20
所示。如果上游端口不支持 Lane 反转，它将在中通告其自己的 Lane 号

## **PCI Express Technology**

- 返回的 TS1，然后下游端口将意识到该问题并有机会实现 Lane 反转。

5. Lane 反转可以由任一端口可选地处理。如果上游端口检测到此情况并支持 Lane 反转，它只需在内部进行 Lane 分配更改，并使用正确的 Lane 号返回 TS1。因此，下游端口不知道曾经存在问题。如果上游端口无法处理 Lane 反转，那么下游端口将看到按相反顺序的传入
Lane 号。如果它支持 Lane 反转，那么它将纠正编号并开始使用新的 Lane 号发送 TS2。

_图 14‐20：示例 2 — 步骤 3、4 和 5_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0471.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **确认链路和 Lane 号。**

6. 下游端口接收具有通告的链路和 Lane 号的 TS1，因此每个端口独立地开始发送 TS2，作为通知它已准备好以协商的设置继续到 L0 状态。

**第 14 章：链路初始化与训练**

7. 上游端口接收没有链路和 Lane 号更改的 TS2，并开始以相同值发送回 TS2。

8. 一旦每个端口接收到至少 8 个 TS2 并发送至少 16 个 TS2，它将发送一些逻辑空闲数据，然后转换到 L0。右侧链路的上游端口正在内部实现 Lane 反转。

## **链路配置示例 3：失败的 Lane**

最后，让我们考虑一下其中一个 Lane 无法正常工作的情况。考虑上游端口的 Lane 2 无法正常工作的示例，如图 14‐21（第 550 页）所示。需要注意的是，Lane 并没有物理损坏，因为如果物理损坏，它将无法检测到接收器，也不会被考虑包含在链路中。但是，即使 Lane
已连接，上游端口的 Lane 2 的发送器或接收器（或两者）也无法完成工作。

在这种情况下，链路训练过程很可能需要更长的时间，因为大多数状态转换在所有 Lane 都准备好下一个状态之前等待继续到下一个状态，或者如果一部分 Lane 已准备好并且已发生超时条件。

以下步骤指示了在通过 Configuration 状态机的子状态转换时可以处理这种情况的方法。

## **链路号协商。**

9. 即使上游端口上的 Lane 2 接收器出现问题，下游端口也将在进入 Configuration 状态时采用相同的过程。下游端口在所有 Lane 上发送 TS1，链路号为 N，Lane 号设置为 PAD。

10. Lane 0、1 和 3 都接收了具有非 PAD 链路号的 TS1，因此这些 Lane 将 TS1 发送回下游端口。但是，上游端口的 Lane 2 未成功接收具有非 PAD 链路号的 TS1，因此其发送器继续发送 Link 和 Lane 号字段中带有 PAD 的
TS1，如图 14‐21（第 550 页）所示。

## **PCI Express Technology**

_图 14‐21：示例 3 — 步骤 1 和 2_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0472.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Lane 号协商。**

11. 一旦下游端口在 Lane 0、1 和 3 上接收到具有相同链路号的 TS1，它将等待所需的超时期望 Lane 2 开始工作。当这种情况没有发生时，下游端口意识到它只能训练为 x2 链路。在接受此事实后，下游端口将通告 Lane 0 和 1 的 Lane 号，但 Lane
2 和 3 返回以在 Link 和 Lane 号字段中发送 PAD。

12. 当上游端口在 Lane 0 和 1 上接收到具有通告的 Lane 号的 TS1，并且它看到 Lane 3 已返回到接收 PAD TS1 时，它通告 Lane 0 和 1 的 Lane 号，但所有其他 Lane 开始（或继续）在 Lane 和 Link 号字段中发送设置为
PAD 的 TS1，如图 14‐22（第 551 页）所示。

**第 14 章：链路初始化与训练**

_图 14‐22：示例 3 — 步骤 3 和 4_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0473.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **确认链路和 Lane 号。**

13. 由于 Lane 0 和 1 上的发送和接收链路和 Lane 号匹配，下游端口通过在这些 Lane 上发送具有相同链路和 Lane 号的 TS2 有序集来表示它已准备好结束此协商并继续到下一个状态 L0。其他 Lane 继续发送 Link 和 Lane 号都为 PAD 的
TS1。

14. 在 Lane 0 和 1 上接收到具有相同链路和 Lane 号的 TS2 后，上游端口也通过在这些 Lane 上发送回 TS2 来表示其准备好离开 Configuration 状态并继续到 L0。其他 Lane 继续发送 Link 和 Lane 号都为 PAD 的
TS1。这在第 552 页的图 14‐23 中示出。

_图 14‐23：示例 3 — 步骤 5 和 6_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0478.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


一旦端口接收到至少 8 个 TS2 并发送至少 16 个，它将发送一些逻辑空闲数据，然后这些 Lane 转换到 L0。其他 Lane（在此示例中为 Lane 2 和 3）转换到电气空闲，直到下一次启动链路训练过程，此时这些 Lane 将像正常一样尝试训练过程。

## **Configuration 子状态详解**

此处提供了每个子状态的详细解释，以涵盖 Configuration 的所有子状态，如第 553 页的图 14‐24 所示。鉴于前面讨论的链路训练示例，Configuration 子状态应该更容易理解。

**第 14 章：链路初始化与训练**

_图 14‐24：Configuration 状态机_

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0479.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Configuration.Linkwidth.Start**

此子状态在 Polling 状态的正常完成之后（如第 527 页 "Polling.Configuration" 中所述）进入，或者如果 Recovery 状态发现自上次分配以来链路或 Lane 号已更改，因此恢复过程无法正常完成（如第 571 页 "Recovery
State" 中所述）。

## **下游 Lane。**

## _在 Configuration.Linkwidth.Start 期间_

下游端口现在成为此链路上的领导者，并在所有活动 Lane 上发送具有非 PAD 链路号的 TS1（只要 LinkUp 未设置且链路宽度的向上配置未正在进行）。在 TS1 中，链路号字段从 PAD 更改为数字，而 Lane 号保持
PAD。规范中对链路号值的唯一约束是，如果支持多个链路，则它们对于每个可能的链路必须是唯一的。例如，x8 链路将在所有 8 个 Lane 上具有相同的链路号，但如果它也可以配置为两个 x4 链路，则两组 4 个 Lane 将被分配不同的链路号，例如一组为 5，另一组为
6。这些值对链路伙伴是本地的，不需要软件跟踪它们或尝试使它们在整个系统中唯一。如果 upconfigure_capable 位设置为 1b，则这些 TS1 也将在接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1 的任何非活动 Lane 上发送。

- 从 Polling 进入此子状态时，任何检测到接收器的 Lane 被视为活动。

- 从 Recovery 进入时，通过 Configuration.Complete 后成为链路一部分的任何 Lane 被视为活动 Lane。

- 必须在 TS1 中通告所有支持的数据速率，即使端口不打算使用它们。

**交叉链路。** 对于 LinkUp = 0b 且支持可选交叉链路功能的情况，所有检测到接收器的 Lane 必须发送最少 16 到 32 个具有非 PAD 链路号和 PAD Lane 号的 TS1。之后，端口将评估其接收的内容以查看是否存在交叉链路。

**向上配置链路宽度。** 如果 LinkUp = 1b 且 LTSSM 想要向上配置链路，则在当前活动 Lane、它打算激活的非活动 Lane 以及已看到传入 TS1 的 Lane 上发送 Link 和 Lane 号设置为 PAD 的 TS1。当 Lane
接收到返回的两个连续的 TS1 时，或在 1ms 后，链路号在正在发送的 TS1 中分配一个值。

- 如果激活非活动 Lane，则发送器必须等待 Tx 共模电压稳定后再退出电气空闲并发送 TS1。

- 对于将分组到链路中的 Lane，链路号必须相同。只有对于能够充当唯一链路的 Lane 组，数字才不同。

- _退出到 "如果其他条件都不成立，则 24ms 超时后。"_ 任何之前接收到至少一个具有 PAD 的 Link 和 Lane 号的 TS1 的 Lane 现在接收到两个具有匹配发送链路号的非 PAD 链路号且 Lane 号仍为 PAD 的连续 TS1 将退出到
Configuration.Linkwidth.Accept 子状态。

**第 14 章：链路初始化与训练**

## _退出到 "Configuration.Linkwidth.Start"_

- 如果此子状态接收的第一组 TS1 具有非 PAD 链路号，则可以理解存在交叉链路，并且链路邻居也表现为下游端口。为了处理这种情况，下游 Lane 更改为上游 Lane 并选择随机的交叉链路超时。下一个子状态将是相同的
Configuration.Linkwidth.Start，但 Lane 现在表现为上游 Lane。

这支持两个链路伙伴都表现为下游端口时的可选行为。这种情况的解决方案是将两者都更改为上游端口并为每个分配一个随机超时，当它到期时将其更改为下游端口。由于超时不会相同，最终一个端口被视为下游，而另一个被视为上游，然后训练可以继续进行。超时必须是随机的，以便即使连接了两个相同的设备，任何可能的死锁最终也会被打破。

如果支持交叉链路，则接收到的 TS1 序列首先具有 PAD 的链路号，后来具有匹配发送链路号的非 PAD 链路号，仅在该序列未被 TS2 中断时才有效。

## _退出到 "Disable 状态"_

如果端口被更高层指示在所有检测到的 Lane 上发送 Disable Link 位被断言的 TS1 或 TS2。通常，下游端口将启动此操作，但对于可选的交叉链路情况，它可以改为变为上游端口，然后如果在两个连续的 TS1 中设置了 Loopback 位，则 Disable
将是下一个状态。

## _退出到 "Loopback 状态"_

如果支持环回的发送器被更高层指示发送 Loopback 位被断言的 TS 有序集，或者如果正在发送 TS1 的 Lane 接收到 2 个连续的设置了 Loopback 位的 TS1。发送设置了该位的 TS1 的端口将成为环回主设备，而接收它们的端口将成为环回从设备。

## _退出到 "Detect 状态"_

如果其他条件都不成立，则在 24ms 超时后。

## **上游 Lane。**

## _在 Configuration.Linkwidth.Start 期间_

上游端口现在成为此链路上的追随者，并返回发送 Link 和 Lane 号字段设置为 PAD 的 TS1 有序集。它将继续这样做，直到它开始从下游端口（领导者）接收具有非 PAD 链路号的 TS1。

上游端口在以下 Lane 上发送 Link 和 Lane 值设置为 PAD 的 TS1：a) 所有活动 Lane，b) 它想要向上配置的 Lane，以及 c) 如果 upconfigure_capable 设置为 1b，则在该子状态中已接收到两个连续的 Link 和 Lane
号设置为 PAD 的 TS1 的每个非活动 Lane 上。

- 从 Polling 进入此子状态时，任何检测到接收器的 Lane 被视为活动。

- 从 Recovery 进入时，通过 Configuration.Complete 后成为链路一部分的任何 Lane 被视为活动 Lane。如果转换不是由 LTSSM 超时引起的，则如果发送器确实计划因自动原因更改链路宽度，则发送器必须将 TS1 符号 4 位 6 的
Autonomous Change 位设置为 1b。

- 必须在 TS1 中通告所有支持的数据速率，即使端口不打算使用它们。

**交叉链路。** 对于 LinkUp = 0b 且支持可选交叉链路功能的情况，所有检测到接收器的 Lane 必须发送最少 16 到 32 个 Link 和 Lane 值设置为 PAD 的 TS1。之后，端口将评估其接收的内容以查看是否存在交叉链路。

_退出到 "如果其他条件都不成立，则 24ms 超时后。"_

- 如果_任何_ Lane 接收到两个具有非 PAD 链路号和 PAD Lane 号的连续 TS1，则此端口转换到 Configuration.Linkwidth.Accept 子状态，其中为这些 Lane 选择一个接收到的链路号，并在_所有_接收到具有非 PAD 链路号的
TS1 的 Lane 上使用该链路号和 PAD Lane 号发送 TS1。任何剩余的检测到接收器但没有链路号的 Lane 必须发送 Link 和 Lane 号设置为 PAD 的 TS1。

- 如果正在向上配置链路，LTSSM 等待直到它在以下情况下接收到两个具有非 PAD 链路号和 PAD Lane 号的连续 TS1：a) 它想要激活的所有非活动 Lane，或 b) 在进入此子状态后 1ms 内的任何

**第 14 章：链路初始化与训练**

Lane，以较早者为准。之后，它使用所选链路号以及 PAD Lane 号发送 TS1。

- 为了避免配置比必要的更小的链路，建议在某些 Lane 上看到错误或丢失块对齐的多 Lane 链路延迟此接收器评估。对于 8b/10b 编码，它应至少再等待两个 TS1，而对于 128b/130b 编码，它应至少等待 34 个 TS1，但任何情况下都不能超过 1ms。

- 激活非活动 Lane 后，发送器必须等待 Tx 共模电压稳定后再退出电气空闲并发送 TS1。

## _退出到 "Configuration.Linkwidth.Start"_

- 交叉链路超时后，发送 16 到 32 个 Link 和 Lane 值设置为 PAD 的 TS2。上游 Lane 更改为下游 Lane，下一个子状态将是相同的 Configuration.Linkwidth.Start，但这次 Lane 表现为下游
Lane。对于连接在一起的两个上游端口的情况，此可选行为允许其中一个最终作为下游端口担任领导角色。

## _退出到 "Disable 状态"_

如果满足以下任一条件：

- 任何正在发送 TS1 的 Lane 也接收到 Disable Link 位被断言的 TS1。

- 支持可选交叉链路，并且所有正在发送和接收 TS1 的 Lane 在两个连续的 TS1 中接收 Disable Link 位，或者交叉链路端口被更高层指示在所有检测到接收器的 Lane 上的 TS1 和 TS2 中断言 Disable 位。

## _退出到 "Loopback 状态"_

- 如果支持环回的发送器被更高层指示发送 Loopback 位被断言的 TS 有序集，或者所有正在发送和接收 TS1 的 Lane 接收到 2 个连续的设置了 Loopback 位的 TS1。发送设置了该位的 TS1 的端口将成为环回主设备，而接收它们的端口将成为环回从设备。

## **PCI Express Technology**

## _退出到 "Detect 状态"_

- 如果其他条件都不成立，则在 24ms 超时后。

## **Configuration.Linkwidth.Accept**

此时，上游端口现在在其所有 Lane 上发送回具有相同链路号的 TS1 有序集。链路号源自下游端口，上游端口只是将该值反映回其所有 Lane。现在下游端口知道链路宽度（接收相同链路号的 Lane 数）并且必须开始通告 Lane 号。因此领导者（下游端口）继续发送
TS1，但现在使用指定的实际 Lane 号而不是 PAD。此外，所有这些 TS1 将具有相同的链路号。下游和上游 Lane 的详细行为概述如下：

## **下游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 下游端口现在将启动 Lane 号。如果可以从至少一组 Lane 形成链路，并且所有 Lane 都接收两个连续的 TS1 并且都看到相同的链路号，则发送保持相同链路号的 TS1 但现在也分配唯一的非 PAD Lane 号。

## _退出到 "Configuration.Lanenum.Wait"_

- 下游端口不会在 Configuration.Linkwidth.Accept 子状态中停留很长时间。一旦它从上游端口接收到指示链路宽度的必要 TS1，它就会更新所需的任何内部状态信息，开始发送如上所述的具有非 PAD Lane 号的 TS1，并立即转换到
Configuration.Lanenum.Wait 以等待来自上游端口的 Lane 号确认。

## **上游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 上游端口发送 TS1，其中在_所有_接收到具有非 PAD 链路号的 TS1 的 Lane 上的 TS1 中选择并发送一个接收到的链路号。任何剩余的检测到接收器但没有链路号的 Lane 必须发送 Link 和 Lane 号设置为 PAD 的 TS1。

## _退出到 "Configuration.Lanenum.Wait"_

- 上游端口必须响应链路邻居向其提议的 Lane 号。如果可以使用在其 TS1 上发送非 PAD 链路号并接收到两个具有相同链路号和任何非 PAD Lane 号的连续 TS1 的 Lane 形成链路，那么它应发送与相同 Lane 号分配匹配的
TS1（如果可能），或者如果需要则不同（例如使用可选的 Lane 反转）。

**第 14 章：链路初始化与训练**

## **Configuration.Lanenum.Wait**

在讨论 Configuration.Lanenum.Wait 状态之前，一些背景信息可能会有所帮助。Lane 号从零开始按顺序分配到链路可能的最大数量。例如，x8 链路将被分配 Lane 号 0 ‐ 7。端口需要支持与其具有的 Lane 数一样宽的链路和一个小至一个 Lane
的链路。Lane 将始终从 Lane 0 开始，并且必须既是顺序的又是连续的。例如，如果 x8 端口上的某些 Lane 无法工作，则可以选择将其设计为配置 x4 链路，如果是这样，它将需要使用 Lane 0‐3。作为另一个示例，如果 x8 端口的 Lane 2
无法工作，则不可能使用 Lane 0、1、3 和 4 形成 x4 链路，因为 Lane 不是连续的。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

规范中针对 Configuration 子状态重复了许多次的常见时序注意事项。这里不是在每种情况下重复它，只需注意它通常适用于上游和下游端口：

为了避免配置比必要的更小的链路，建议在某些 Lane 上看到错误或丢失块对齐的多 Lane 端口延迟最终链路宽度评估。对于 8b/10b，它应至少再等待两个 TS1，而对于 128b/130b 模式，它应至少等待 34 个 TS1，但任何情况下都不能超过 1ms。其想法是
Lane 在上电或复位后可能需要稳定时间。

## _退出到 "Detect 状态"_

在 2ms 超时后，如果无法配置链路（例如：Lane 0 不工作且 Lane 反转不可用），或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号中都带有 PAD 的 TS1，则链路必须退出到 Detect 状态。

## **下游 Lane**

## _在 Configuration.Lanenum.Wait 期间_

下游端口将继续传输具有非 PAD 链路和 Lane 号的 TS1，直到满足退出条件之一。

## _退出到 "Configuration.Lanenum.Accept"_

如果满足下列任一情况：

- 如果在所有 Lane 上接收到两个连续的 TS1，其链路和 Lane 号与在这些 Lane 上发送的内容匹配。

## **PCI Express Technology**

- 如果任何检测到接收器的 Lane 接收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD 链路号。规范指出，这允许两个端口就相互可接受的链路宽度达成一致。

## _退出到 "Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

上游 Lane

## _在 Configuration.Lanenum.Wait 期间_

上游端口将继续传输具有非 PAD 链路和 Lane 号的 TS1，直到满足退出条件之一。

## _退出到 "Configuration.Lanenum.Accept"_

如果满足下列任一情况：

- 如果任何 Lane 接收到两个连续的 TS2。

- 如果任何 Lane 接收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD 链路号。

请注意，允许上游 Lane 在更改为该子状态之前等待最多 1ms，以防止接收错误或 Lane 之间的偏移影响最终链路配置。

## _退出到 "Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

## **Configuration.Lanenum.Accept**

下游 Lane

## _在 Configuration.Lanenum.Accept 期间_

下游端口现在已接收到具有非 PAD 链路和 Lane 号的 TS1。在这一点上，下游端口必须决定是否可以使用上游端口返回的 Lane 号建立链路。三个可能的状态转换在下面列出。

## _退出到 "Configuration.Complete"_

如果接收到两个连续的 TS1 具有相同的非 PAD 链路和 Lane 号，并且它们与所有 Lane 的 TS1 中传输的链路和 Lane 号匹配，则上游端口已同意下游端口通告的链路和

**第 14 章：链路初始化与训练**

Lane 号，下一个子状态是 Configuration.Complete。或者如果接收到的 TS1 中的 Lane 号与下游端口通告的相反，如果下游端口支持 Lane 反转，它仍然可以使用反转的 Lane 号继续到 Configuration.Complete。

规范指出，反转 Lane 条件严格定义为 Lane 0 接收具有最高 Lane 号（Lane 总数 ‐ 1）的 TS1，并且最高 Lane 号接收 Lane 号为零的 TS1。可以从中理解的是，课堂上偶尔出现的问题的答案：Lane
号是否可以混合而不是顺序的？答案是不可以的，它们必须是从 0 到 n‐1 或从 n‐1 到 0；不支持其他选项。

如果 Configuration 状态是从 Recovery 状态进入的，则可能已请求带宽更改。如果是这样，状态位将更新以报告发生的情况的性质。基本上，系统需要报告此更改是由于链路工作不可靠而启动，还是因为硬件只是在管理链路功率。位更新如下：

- 如果带宽更改是由下游端口因可靠性问题而启动的，则链路带宽管理状态位设置为 1b。

- 如果带宽更改不是由下游端口启动，但两个连续接收的 TS1 中的 Autonomous Change 位清零为 0b，则链路带宽管理状态位设置为 1b。

- 否则，链路自动带宽状态位设置为 1b。

## _退出到 "Configuration.Lanenum.Wait"_

- 如果可以使用部分（但不是全部）接收两个连续的具有相同非 PAD 链路和 Lane 号的 TS1 的 Lane 形成配置的链路，则这些 Lane 使用相同的链路号和新的 Lane 号发送 TS1。目标是使用较小的 Lane 组来实现工作的链路。

新的 Lane 号必须从零开始并按顺序递增以覆盖将使用的 Lane。任何不接收 TS1 的 Lane 不能成为组的一部分，并将破坏 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。例如，如果 8 个 Lane 可用，但 Lane
2 看不到传入的 TS1，则链路不能由需要 Lane 2 的组组成。因此，x8 和 x4 选项将不可用，只有 x1 或 x2 链路是可能的。

## **PCI Express Technology**

## _退出到 "Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 接收到两个连续的具有 PAD 的链路和 Lane 号的 TS1。

## **上游 Lane**

## _在 Configuration.Lanenum.Accept 期间_

- 上游端口现在已接收到具有非 PAD 链路和 Lane 号的 TS2 或 TS1。在这一点上，上游端口必须决定是否可以使用下游端口发送的 Lane 号建立链路。三个可能的状态转换在下面列出。

## _退出到 "Configuration.Complete"_

- 如果接收到两个连续的 TS2 具有相同的非 PAD 链路和 Lane 号，并且它们与这些 Lane 的 TS1 中传输的链路和 Lane 号匹配，则一切正常，下一个子状态将是 Configuration.Complete。

## _退出到 "Configuration.Lanenum.Wait"_

- 如果可以使用接收两个连续的具有相同非 PAD 链路和 Lane 号的 TS1 的 Lane 的子集形成配置的链路，则这些 Lane 使用相同的链路号和新的 Lane 号发送 TS1。目标是使用较小的 Lane 组来实现工作的链路。在这种情况下，下一个子状态将是
Configuration.Lanenum.Wait。

与下游 Lane 的情况一样，新的 Lane 号必须从零开始并按顺序递增以覆盖将使用的 Lane。任何不接收 TS1 的 Lane 不能成为组的一部分，并将破坏 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

## _退出到 "Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 接收到两个连续的具有 PAD 的链路和 Lane 号的 TS1，则下一个状态将是 Detect。

## **Configuration.Complete**

这是 Configuration 状态中交换 TS2 的唯一子状态。如前所述，TS2 的目的是一种握手或确认，即链路上的两个设备已准备好继续到下一个状态。因此这是 TS1 中交换的链路和 Lane 号的最终确认

**第 14 章：链路初始化与训练**

应注意的是，允许设备在进入此子状态时更改其支持的数据速率和向上配置能力，但不能在其中更改。这是因为设备从这些 TS2 中通告的内容记录其链路伙伴的能力，如本节所述。

## **下游 Lane**

## _在 Configuration.Complete 期间_

使用与接收到的 TS1 匹配的链路和 Lane 号发送 TS2。如果端口支持使用 Lane 0 的 x1 链路并能够向上配置链路，则 TS2 可以设置 Upconfigure Capability 位。

对于 8b/10b 编码，离开此子状态时必须完成 Lane 去偏移。此外，如果所有配置的 Lane 看到两个连续的设置了 Disable Scrambling 位的 TS2，则将禁用加扰。发送这些的端口还必须禁用加扰。请注意，由于加扰对信号完整性有必要贡献，因此在
128b/130b 模式下不能禁用加扰。

下游端口正在发送 TS2 并监视返回的 TS2。供将来参考，记录从传入 TS2 的 N_FTS 字段中退出 L0s 状态时必须发送的 FTS 数。

## _退出到 "Configuration.Idle"_

当所有发送 TS2 的 Lane 接收 8 个 TS2，具有匹配的链路和 Lane 号（非 PAD）、匹配的速率标识符以及所有链路中匹配的 Link Upconfigure Capability 位时，下一个状态将是 Configuration.Idle。在接收到一个 TS2
之后，还必须发送至少 16 个 TS2。

如果设备支持大于 2.5 GT/s 的速率，则它必须记录在任何已配置 Lane 上接收到的速率标识符，并且这将覆盖任何先前记录的值。用于跟踪 Recovery 中速度更改的变量 "changed_speed_recovery" 被清零。

变量 "upconfigure_capable" 在以下情况下设置为 1b：如果设备发送 Link Upconfigure Capability 设置为 1b 的 TS2 并接收 8 个连续的设置了相同位的 TS2。否则，它被清零。

未配置为链路一部分的任何 Lane 不再与正在进行的 LTSSM 关联，并且必须是以下之一：

- 与新的 LTSSM 关联，或

- 转换到电气空闲

 - a) 如果那些 Lane 之前已通过 L0 配置为链路的一部分，并且 LinkUp 仍设置为 1b，则出现特殊情况

从那以后。如果链路具有向上配置能力，它们必须保持与同一 LTSSM 关联。对于这种情况，还建议那些 Lane 保持其接收器终端开启，因为如果链路被向上配置，它们将再次成为链路的一部分。如果终端未保持开启，则它们必须在 LTSSM 进入 Recovery.RcvrCfg
状态时一直通过 Configuration.Complete 打开。但是，通过此过程，之前不是链路一部分的 Lane 不能成为其一部分。

- b) 对于可选交叉链路，接收器终端必须介于 ZRX‐HIGH‐IMP‐DC‐POS 和 ZRX‐HIGH‐IMP‐DC‐NEG 之间。

- c) 如果 LTSSM 返回 Detect，这些 Lane 将再次与其关联。

- d) 在 Lane 进入电气空闲之前不需要 EIOS，并且转换不必在符号或有序集边界上发生。

## 在 2ms 超时后：

_退出到 "Configuration.Idle"_

如果 idle_to_rlock_transitioned 变量小于 FFh **且**当前数据速率为 8.0 GT/s，则下一个状态是 Configuration.Idle。

在此转换中，变量 "changed_speed_recovery" 被清零。此外，如果至少一个 Lane 看到八个具有匹配链路和 Lane 号（非 PAD）的连续 TS2，则变量 "upconfigure_capable" 可以更新，尽管不需要这样做。如果发送和接收的 Link
Upconfigure Capability 位为 1b，则将其设置为 1b，否则清零。

未配置链路一部分的 Lane 不与正在进行的 LTSSM 关联，并具有与上面列出的非超时情况相同的要求。

_退出到 "Detect 状态"_

否则，下一个状态是 Detect。

## **上游 Lane**

_在 Configuration.Complete 期间_

使用与接收到的 TS2 匹配的链路和 Lane 号发送 TS2。如果端口支持使用 Lane 0 的 x1 链路并能够向上配置链路，则 TS2 可以设置 Upconfigure Capability 位。

**第 14 章：链路初始化与训练**

对于 8b/10b 编码，离开此子状态时必须完成 Lane 去偏移。此外，如果所有配置的 Lane 看到两个连续的设置了 Disable Scrambling 位的 TS2，则将禁用加扰。发送这些的端口还必须禁用加扰。请注意，由于加扰对信号完整性有必要贡献，因此在
128b/130b 模式下不能禁用加扰。

在此子状态中，上游端口正在从下游端口接收 TS2，供将来参考，应记录从传入 TS2 中的 N_FTS 字段值退出 L0s 状态时必须发送的 FTS 数。

## _退出到 "Configuration.Idle"_

当所有发送 TS2 的 Lane 接收 8 个 TS2，具有匹配的链路和 Lane 号（非 PAD）、匹配的速率标识符以及所有链路中匹配的 Link Upconfigure Capability 位时，下一个状态将是 Configuration.Idle。在接收到一个 TS2
之后，还必须发送至少 16 个 TS2。

如果设备支持大于 2.5 GT/s 的速率，则它必须记录在任何已配置 Lane 上接收到的速率标识符，并且这将覆盖任何先前记录的值。用于跟踪 Recovery 中速度更改的变量 "changed_speed_recovery" 被清零。

变量 "upconfigure_capable" 在以下情况下设置为 1b：如果设备发送 Link Upconfigure Capability 设置为 1b 的 TS2 并接收 8 个连续的设置了相同位的 TS2。否则，它被清零。

未配置为链路一部分的任何 Lane 不再与正在进行的 LTSSM 关联，并且必须是以下之一：

- 可选择与新的交叉链路 LTSSM 关联（如果支持此功能），或

- 转换到电气空闲

 - a) 如果那些 Lane 之前已通过 L0 配置为链路的一部分，并且 LinkUp 自那时起仍设置为 1b，则出现特殊情况。如果链路具有向上配置能力，它们必须保持与同一 LTSSM 关联。对于这种情况，还建议那些 Lane
保持其接收器终端开启，因为如果链路被向上配置，它们将再次成为链路的一部分。如果它们未保持开启，则它们必须在 LTSSM 进入 Recovery.RcvrCfg 状态时一直通过 Configuration.Complete 打开。但是，通过此过程，之前不是链路一部分的 Lane
不能成为其一部分。

## **PCI Express Technology**

- b) 接收器终端必须介于 ZRX‐HIGH‐IMP‐DC‐POS 和 ZRX‐

 - HIGH‐IMP‐DC‐NEG 之间。

- c) 如果 LTSSM 返回 Detect，这些 Lane 将再次与其关联。

- d) 在 Lane 进入电气空闲之前不需要 EIOS，并且转换不必在符号或有序集边界上发生。

## 在 2ms 超时后：

## _退出到 "Configuration.Idle"_

如果 idle_to_rlock_transitioned 变量小于 FFh **且**当前数据速率为 8.0 GT/s，则下一个状态是 Configuration.Idle。

在此转换中，变量 "changed_speed_recovery" 被清零。此外，如果至少一个 Lane 看到八个具有匹配链路和 Lane 号（非 PAD）的连续 TS2，则变量 "upconfigure_capable" 可以更新，尽管不需要这样做。如果发送和接收的 Link
Upconfigure Capability 位为 1b，则将其设置为 1b，否则清零。

未配置链路一部分的 Lane 不与正在进行的 LTSSM 关联，并具有与上面列出的非超时情况相同的要求。

## _退出到 "Detect 状态"_

否则，下一个状态是 Detect。

## **Configuration.Idle**

## _在 Configuration.Idle 期间_

在此子状态中，发送器正在发送空闲数据并等待接收空闲数据的最小数量，以便此链路可以转换到 L0。在此期间，物理层向上层报告链路处于运行状态（Linkup = 1b）。

对于 8b/10b 编码，发送器在所有已配置 Lane 上发送空闲数据。空闲数据只是被加扰和编码的数据零。

对于 128b/130b 编码，发送器在所有已配置 Lane 上发送一个 SDS 有序集，后跟空闲数据符号。Lane 0 上的第一个空闲符号是数据流的第一个符号。

**第 14 章：链路初始化与训练**

## _退出到 "L0 状态"_

如果使用 8b/10b 编码，则下一个状态是 L0，如果在所有已配置 Lane 上接收到 8 个连续的空闲数据符号时间，并且在接收到一个空闲符号之后发送了 16 个符号时间的空闲数据。

如果使用 128b/130b，则下一个状态是 L0，如果在所有已配置 Lane 上接收到 8 个连续的空闲数据，在接收到一个空闲符号之后发送了 16 个空闲，并且此状态不是通过 Configuration.Complete 的超时进入的。

- 数据流处理开始之前必须完成 Lane 到 Lane 去偏移。

- 必须在数据块中接收空闲符号。

- 如果软件自上次从 Recovery 或 Configuration 转换到 L0 以来在 Link Control 寄存器中设置了 Retrain Link 位，则下游端口必须将 Link Status 寄存器中的 Link Bandwidth Management 位设置为
1b，以指示此更改不是硬件发起的（自动）。

- 转换到 L0 时，变量 "idle_to_rlock_transitioned" 清零为 00h。

## 在 2ms 超时后：

## _退出到 "Recovery 子状态详解"_

如果 idle_to_rlock_transitioned 变量小于 FFh，则下一个状态是 Recovery (Recovery.RcvrLock)。然后：

- a) 对于 8.0 GT/s，idle_to_rlock_transitioned 递增 1。

- b) 对于 2.5 或 5.0 GT/s，将 idle_to_rlock_transitioned 设置为 FFh。

- c) 注意：此变量计算 LTSSM 因序列未工作而从此状态转换到 Recovery 状态的次数。问题可能是均衡尚未正确调整或所选速度根本不起作用，Recovery 状态将采取措施解决这些问题。此变量限制这些尝试的次数以避免无限循环。如果在进行此操作 256 次（当计数达到
FFh 时）后链路仍不工作，则返回 Detect 并重新开始，希望获得更好的结果。

_退出到 "Detect 状态"_

否则（即 idle_to_rlock = FFh），下一个状态是 Detect。

## **L0 状态**

这是正常的、完全运行的链路状态，在此期间逻辑空闲、TLP 和 DLLP 在链路邻居之间交换。L0 在链路训练过程结束后立即实现。物理层还通过设置 LinkUp 变量来通知上层链路已准备好运行。此外，变量 idle_to_rlock_transitioned 清零为 00h。

## _退出到 "Recovery 状态"_

如果指示链路速度或链路宽度的变化，或者如果链路伙伴通过转到 Recovery 或电气空闲来启动此操作，则下一个状态将是 Recovery。让我们在下面的讨论中更详细地考虑这三种情况中的每一种。

## **速度更改**

规范中描述了将导致自动速度更改的两种条件。

第一种是当两个伙伴都支持高于 2.5 GT/s 的速率并且链路处于活动状态（数据链路层报告 DL_Active），或者当一个伙伴在其 TS 有序集中请求速度更改时。例如，如果注意到更高速率并且软件写入 Retrain Link 位并在将 Target Link Speed
字段（参见第 569 页的图 14‐26）设置为与当前速率不同的速率之后，下游端口将启动速度更改。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-12-5"></a>
## 12.5 Physical Layer - Logical (Gen3) | 物理层 - 逻辑 (Gen3)

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

4. In response to seeing non‐PAD Lane numbers coming in, the Upstream Port will verify that the incoming Lane numbers match the Lane num‐
bers they are received on. In this example, the Lanes of the Downstream and Upstream Ports are connected correctly. Because all the Lane
num‐ bers match, the Upstream Port advertises its Lane numbers in the TS1s it is sending as well. When the Downstream Port sees non‐PAD Lane
numbers in response, it compares the incoming numbers to the values it’s sending. If they match, all is well but, if not, then other steps
will need to be taken. If some but not all Lane numbers match, then the Link width may be adjusted accordingly. If the Lanes are reversed,
then the optional Lane Reversal feature will be needed. Because it’s optional, it’s possible that the Lanes have been reversed but neither
device is capable of correcting it. This would be a dramatic board design error because it is possible the Link cannot be configured for
operation in this case.

## **PCI Express Technology** 

_Figure 14‐16: Example 1 ‐ Steps 3 and 4_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0480.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Confirming Link and Lane Numbers.** 

5. Since the transmitted and received Link and Lane numbers matched on all the Lanes, the Downstream Port indicates it is ready to conclude
this negotiation and proceed to the next state, L0, by sending TS2 Ordered Sets with the same Link and Lane numbers.

6. Upon receiving TS2s with the same Link and Lane numbers, the Upstream Port also indicates its readiness to leave the Configuration state
and proceed to L0 by sending TS2s back. This is shown in Figure 14‐17 on page 545.

7. Once a Port receives at least 8 TS2s and transmits at least 16, it sends some logical idle data and then transitions to L0. 
_Figure 14‐17: Example 1 ‐ Steps 5 and 6_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0481.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


Options: One Link x4, x2 or x1 

## **Link Configuration Example 2** 

Another example that should be covered is of a Device with 4 Downstream Lanes that is capable of being configured as a single x4 Link or a
combination of two x2 Links or four x1 Links. So even a configuration of one x2 Link and two x1 Links would be just fine. An example of this
type of Device can be seen in Fig‐ ure 14‐18 on page 546.

If all four Lanes have detected a receiver and made it to the Configuration state, there are a number of connection possibilities: 

- One x4 Link 

- Two x2 Links 

- One x2 Link and two x1 Links 

- Four x1 Links 

One example method defined in the spec to determine which of the configura‐ tions are implemented is described below. 

## **Link Number Negotiation.** 

1. In this example method, the Downstream Port begins by advertising a unique Link number on each Lane. Lane 0 advertises a Link number of
N, Lane 1 advertises a Link number of N+1, etc. as shown in Figure 14‐ 18 on page 546. These Link numbers are just examples, and they do not
have to be sequential. Also, it is important to remember that the Down‐ stream Port does not know what it is connected to and it is this
process where the Port is trying to determine the connections for each Lane.

_Figure 14‐18: Example 2 ‐ Step 1_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0482.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


2. Upon receiving the returned TS1s, the Downstream Port recognizes two things: all four Lanes are working and they are connected to two
differ‐ ent Upstream Ports. This means there will actually be _two_ Downstream Ports. Each Downstream Port will have its own Lane 0 and Lane
1 as shown in Figure 14‐20 on page 548.
_Figure 14‐19: Example 2 ‐ Step 2_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0483.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Lane Number Negotiation.** 

3. The process continues now for each Link independently but they’ll take the same steps as before to determine the Lane numbers: the Down‐
stream Ports will advertise their Lane numbers in the TS1s. It is also important to note that the Downstream Ports begin advertising the
sin‐ gle returned Link number for all Lanes of the Link. The Link on the left is advertising a Link number of N for both Lanes and the Link
on the right is advertising N+2.

4. In this example, the Lane numbers of the Link on the left match between the Downstream and Upstream Port. However, for the Link on the
right, the Lane numbers of the Downstream Port are reversed from the connected Upstream Port. The Upstream Port realizes this and if it
supports Lane Reversal, it will implement that internally and reply back with the same Lane numbers that were advertised by the Down‐ stream
Port, as shown in Figure 14‐20. If the Upstream Port did not sup‐ port Lane Reversal, it would have advertised its own Lane numbers in

## **PCI Express Technology** 

 - the returned TS1s and then the Downstream Port would have realized the issue and had a chance to implement Lane Reversal. 

5. Lane Reversal can optionally be handled by either Port. If the Upstream Port detects this case and supports Lane Reversal, it simply
makes the Lane assignment change internally and returns TS1s with the proper Lane numbers. As a result, the Downstream Port is unaware that
there was ever an issue. If the Upstream Port is unable to handle Lane Rever‐ sal though, then the Downstream Port will see the incoming
Lane num‐ bers in reverse order. If it supports Lane Reversal, it will then correct the numbering and begin sending TS2s with the new Lane
numbers.

_Figure 14‐20: Example 2 ‐ Steps 3, 4 and 5_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0484.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Confirming Link and Lane Numbers.** 

6. The Downstream Ports receive the TS1s with the Link and Lane num‐ bers that match what was advertised so each Port, independently, starts
sending TS2s as a notification that it is ready to proceed to the L0 state with the negotiated settings.
7. The Upstream Ports receive the TS2s with no Link and Lane number changes and start transmitting TS2s in return with the same values. 

8. Once each Port receives at least 8 TS2s and transmits at least 16 TS2s, it sends some logical idle data and then transitions to L0. The
Upstream Port of the Link on the right is implementing Lane Reversal internally.

## **Link Configuration Example 3: Failed Lane** 

Finally, let’s consider what happens if one of the Lanes isn’t working properly. Consider an example in which Lane 2 of the Upstream Port is
not functioning well as shown in Figure 14‐21 on page 550. It’s important to note that the Lane isn’t physically broken because if it were
it wouldn’t have detected a Receiver and wouldn’t be considered for inclusion in the Link. However, even though the Lane is attached, either
the Transmitter or Receiver (or both) of Lane 2 on the Upstream Port is not getting the job done.

In cases like this, it is likely that the link training process will take considerably longer because most of the state transitions wait to
proceed to the next state until ALL Lanes are ready for the next state, OR if a subset of Lanes are ready and a timeout condition has
occurred.

The steps below indicate a way this situation could be handled when transition‐ ing through the substates of the Configuration state
machine.

## **Link Number Negotiation.** 

9. Even though the Lane 2 Receiver on the Upstream Port is having issues, the Downstream Port is going to take the same process upon
entering the Configuration state. The Downstream Port sends TS1s on all Lanes with the Link number N and with the Lane number set to PAD.

10. Lanes 0, 1 and 3 all received the TS1s with the non‐PAD Link number, so those Lanes send TS1s back to the Downstream Port. However, Lane
2 of the Upstream Port did not successfully receive the TS1s with the non‐PAD Link number, so its Transmitter continues sending TS1s with
PAD in the Link and Lane number fields as shown in Figure 14‐21 on page 550.

## **PCI Express Technology** 

_Figure 14‐21: Example 3 ‐ Steps 1 and 2_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0485.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Lane Number Negotiation.** 

11. Once the Downstream Port has received the TS1s with the same Link number on Lanes 0, 1 and 3, it waits until the required timeout period
hoping that Lane 2 will start working. When that doesn’t happen, the Downstream Port realizes that it will only be able to train as a x2
Link. After accepting this fact, the Downstream Port will advertise its Lane numbers for Lanes 0 and 1, but Lanes 2 and 3 go back to send
PADs in the Link and Lane number fields.

12. When the Upstream Port receives the TS1s on Lanes 0 and 1 with the advertised Lane numbers and it sees that Lane 3 has gone back to
receiving PAD TS1s, it advertises its Lane number for Lanes 0 and 1 but all the other Lanes start (or continue) sending TS1s with PAD set in
both the Lane and Link number fields as shown in Figure 14‐22 on page 551.
_Figure 14‐22: Example 3 ‐ Steps 3 and 4_ 

<img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0486.png" alt="Figure 13‐34: 2.5 GT/s Receiver Eye Diagram" width="700">

<br>


## **Confirming Link and Lane Numbers.**

</td>
<td style="background-color:#e8e8e8">

**13. Since the transmitted and received Link and Lane numbers matched on Lanes 0 and 1, the Downstream Port indicates it is ready to
conclude this negotiation and proceed to the next state, L0, by sending TS2 Ordered Sets with the same Link and Lane numbers on these Lanes.
The other Lanes continue sending TS1s with PAD for both the Link and Lane numbers.**

**14. Upon receiving TS2s with the same Link and Lane numbers on Lanes 0 and 1, the Upstream Port also indicates its readiness to leave the
Configuration state and proceed to L0 by sending TS2s back on these Lanes. The other Lanes continue sending TS1s with PAD for both the Link
and Lane numbers. This is shown in Figure 14‐23 on page 552.**

Once a Port receives at least 8 TS2s and transmits at least 16, it sends some logical idle data and those Lanes transitions to L0. The other
Lanes, Lanes 2 and 3 in this example, transition to Electrical Idle until the next time the link training process is initiated at which
point those Lanes will attempt the training process like normal.

## **Detailed Configuration Substates**

A detailed explanation of each substate is presented here to cover all the substates of Configuration, as shown in Figure 14‐24 on page 553.
The Configuration Substates should be easier to follow, given the Link Training examples discussed previously.
## **Configuration.Linkwidth.Start**

This substate is entered after either the normal completion of the Polling state (as described in "Polling.Configuration" on page 527), or
if the Recovery state finds that Link or Lane numbers have changed since the last time they were assigned and thus the recovery process
can't finish normally (as described in the "Recovery State" on page 571).

## **Downstream Lanes.**

## _During Configuration.Linkwidth.Start_

The Downstream Port is now the leader on this Link and sends TS1s with a non‐PAD link number on all active Lanes (as long as LinkUp is

not set and upconfiguration of the Link width is not taking place). In the TS1s, the Link number field is changed from PAD to a number while
the Lane number remains PAD. The only constraint on the value of the Link numbers in the spec is that they must be unique for each possible
Link if multiple Links are supported. For example, a x8 Link would have the same Link number on all 8 Lanes, but if it could also be
configured as two x4 Links, both groups of 4 Lanes would be assigned different Link numbers, such as 5 for one group and 6 for the other.
The values are local to the Link partners and there's no need for software to track them or try to make them unique throughout the system.
If the upconfigure_capable bit is set to 1b, these TS1s will also be sent on any inactive Lanes that received two consecutive TS1s with Link
and Lane numbers set to PAD.

- When entering this substate from Polling, any Lane that detected a Receiver is considered active.

- When entering from Recovery, any Lane that was part of the Link after going through Configuration.Complete is considered an active Lane.

- All supported data rates must be advertised in the TS1s, even if the Port doesn't intend to use them.

**Crosslinks.** For cases where LinkUp = 0b and the optional crosslink capability is supported, all Lanes that detected a Receiver must send
a minimum of 16 to 32 TS1s with a non‐PAD Link number and PAD Lane number. After that, the port will evaluate what it is receiving to see if
a crosslink is present.

**Upconfiguring the Link Width.** If LinkUp = 1b and the LTSSM wants to upconfigure the Link, TS1s with Link and Lane numbers set to PAD are
sent on the currently active Lanes, the inactive Lanes it intends to activate, and the Lanes that have seen incoming TS1s. When the Lanes
have received two consecutive TS1s coming back, or after 1ms, the Link number is assigned a value in the TS1s being sent.

- If activating an inactive Lane, the Transmitter must wait for the Tx common mode voltage to settle before exiting Electrical Idle and
sending TS1s.

- Link numbers must be the same for Lanes that will be grouped into a Link. The numbers can only be different for groups of Lanes that are
capable of acting as a unique Link.

- _Exit to "After a 24ms timeout if none of the other conditions are true."_ Any Lanes that previously received at least one TS1 with Link
and Lane
number of PAD now receive two consecutive TS1s with a non‐PAD Link number that matches a transmitted Link number and Lane numbers are still
PAD will exit to the Configuration.Linkwidth.Accept substate.

## _Exit to "Configuration.Linkwidth.Start"_

- If the first set of received TS1s for this substate have a non‐PAD Link number then it's understood that a crosslink is present and the
Link neighbor is also behaving as a Downstream Port. To handle this situation, the Downstream Lanes are changed to Upstream Lanes and a
random crosslink timeout is chosen. The next substate will be the same Confiuration.Linkwidth.Start again but the Lanes will now behave as
Upstream Lanes.

This supports the optional behavior when both Link partners behave as Downstream Ports. The solution for this situation is to change both to
Upstream Ports and assign each a random timeout that, when it expires, changes it to a Downstream Port. Since the timeouts won't be the
same, eventually one Port is seen as Downstream while the other is seen as Upstream and then the training can go forward. The timeout must
be random so that even if two of the same devices are connected any possible deadlock will eventually be broken.

If crosslinks are supported, receiving a sequence of TS1s that first have a Link number of PAD and later have a non‐PAD Link number that
matches the transmitted Link number is valid only if the sequence wasn't interrupted by a TS2.

## _Exit to "Disable State"_

If the Port is instructed by a higher layer to send TS1s or TS2s with the Disable Link bit asserted on all detected Lanes. Normally, the
Downstream Port will initiate this but, for the optional crosslink case, it could become an Upstream Port instead and then Disabled will be
the next state if 2 consecutive TS1s are received with the Loopback bit set.

## _Exit to "Loopback State"_

If the loopback‐capable Transmitter is instructed by a higher layer to send TS Ordered Sets with the Loopback bit asserted, or if Lanes that
are sending TS1s receive 2 consecutive TS1s with the Loopback bit set. Whichever Port sends the TS1s with the bit set will become the
Loopback master, while the Port that receives them will become the Loopback slave.

## _Exit to "Detect State"_

After a 24ms timeout if none of the other conditions are true.

## **Upstream Lanes.**

## _During Configuration.Linkwidth.Start_

The Upstream Port is now the follower on this Link and goes back to sending TS1 ordered‐sets with PAD set for the Link and Lane number
fields. It will continue to do this until it begins receiving TS1s with a non‐PAD Link number from the Downstream Port (leader).

The Upstream Port sends TS1s with Link and Lane values of PAD on a) all active Lanes, b) the Lanes it wants to upconfigure and, c) if
upconfigure_capable is set to 1b, on each of the inactive Lanes that have received two consecutive TS1s with Link and Lane numbers set to
PAD while in this substate.

- When entering this substate from Polling, any Lane that detected a Receiver is considered active.

- When entering from Recovery, any Lane that was part of the Link after going through Configuration.Complete is considered an active Lane.
If the transition wasn't caused by an LTSSM timeout, the Transmitter must set the Autonomous Change bit (Symbol 4, bit 6) to 1b in the TS1s
being sent in the Configuration state if it does, in fact, plan to change the Link width for autonomous reasons.

- All supported data rates must be advertised in the TS1s, even if the Port doesn't intend to use them.

**Crosslinks.** For cases where LinkUp = 0b and the optional crosslink capability is supported, all Lanes that detected a Receiver must send
a minimum of 16 to 32 TS1s with Link and Lane values of PAD. After that, the port will evaluate what it is receiving to see if a crosslink
is present.

_Exit to "After a 24ms timeout if none of the other conditions are true."_

- If _any_ Lanes receive two consecutive TS1s with non‐PAD Link number and PAD Lane number, this port transitions to the
Configuration.Linkwidth.Accept substate where one of the received Link numbers is selected for those Lanes and TS1s are sent back with that
Link number and a PAD Lane number, on _all_ the Lanes that received TS1s with a non‐ PAD Link number. Any left‐over Lanes that detected a
Receiver but no Link number must send TS1s with Link and Lane numbers set to PAD.

- If upconfiguring the Link, the LTSSM waits until it receives two consecutive TS1s with a non‐PAD Link number and PAD Lane number on either
a) all the inactive Lanes it wants to activate, or b) on any
Lane 1ms after entering this substate, whichever is earlier. After that, it sends TS1s with the selected Link number along with PAD Lane
numbers.

- To avoid configuring a Link smaller than necessary, it's recommended that a multi‐Lane Link that sees an error or loses Block Alignment on
some Lanes delay this Receiver evaluation. For 8b/10b encoding, it should wait at least two more TS1s, while for 128b/130b encoding it
should wait for at least 34 TS1s, but never more than 1ms in any case.

- After activating an inactive Lane, the Transmitter must wait for the Tx common mode voltage to settle before exiting Electrical Idle and
sending TS1s.

## _Exit to "Configuration.Linkwidth.Start"_

- After a crosslink timeout, send 16 to 32 TS2s with Link and Lane values of PAD. The Upstream Lanes change to Downstream Lanes and the next
substate will be the same Confiuration.Linkwidth.Start again but this time the Lanes behave as Downstream Lanes. For the case of two
Upstream Ports connected together, this optional behavior allows one of them to eventually take the lead as a Downstream Port.

## _Exit to "Disable State"_

If either of the following is true:

- Any Lanes that are sending TS1s also receive TS1s with the Disable Link bit asserted.

- The optional crosslink is supported and either all Lanes that are sending and receiving TS1s receive the Disable Link bit in two
consecutive TS1s, or else a crosslink Port is directed by a higher Layer to assert the Disable bit in its TS1s and TS2s on all Lanes that
detected a Receiver.

## _Exit to "Loopback State"_

</td>
</tr></tbody></table>

<p align="center"><b>Figure 14‐23: Example 3 ‐ Steps 5 and 6</b></p>
<p align="center"><img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0487.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0487.png">Page 487</a></sub></p>


<p align="center"><b>Figure 14‐24: Configuration State Machine</b></p>
<p align="center"><img src="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0488.png" width="700"></p>
<p align="center"><sub>📄 <a href="figures/chapter_12_Physical_Layer_Logical_Gen3/page/page0488.png">Page 488</a></sub></p>

<table style="width:100%;table-layout:fixed">
<colgroup><col style="width:50%"><col style="width:50%"></colgroup>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>

</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`

