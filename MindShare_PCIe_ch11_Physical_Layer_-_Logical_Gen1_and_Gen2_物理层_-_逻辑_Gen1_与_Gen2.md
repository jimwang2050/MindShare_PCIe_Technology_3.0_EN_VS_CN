# 📘 第 11 章　物理层 - 逻辑 (Gen1 与 Gen2) (Chapter 11. Physical Layer - Logical (Gen1 and Gen2))

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0278.md` ... `chunks/chunk0284.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [11.1 Component Interfaces — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-1)
- [11.2 8.0 GT/s — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-2)
- [11.3 Reduced-Swing Differential Voltage — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-3)
- [11.4 Solution for 2.5 GT/s — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-4)
- [11.5 Presets and Ratios — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-5)
- [11.6 Beacon Signaling — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-6)
- [11.7 Receiver Characteristics — 物理层 - 逻辑 (Gen1 与 Gen2)](#sec-11-7)

<a id="sec-11-1"></a>
## 11.1 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>
## **Component Interfaces** 

Components from different vendors must work reliably together, so a set of parameters are specified that must be met for the interface. For 2.5 GT/s it was implied, and for 5.0 GT/s it was explicitly stated, that the characteristics of this interface are defined at the device pins. That allows a component to be charac‐ terized independently, without requiring the use of any other PCIe components. Other interfaces may be specified at a connector or other location, but those are not covered in the base spec and would be described in other form‐factor specs like the _PCI Express Card Electromechanical Spec_ . 

## **Physical Layer Electrical Overview** 

The electrical sub‐block associated with each lane, as shown in Figure 13‐1 on page 450, provides the physical interface to the Link and contains differential Transmitters and Receivers. The Transmitter delivers outbound Symbols on each Lane by converting the bit stream into two single‐ended electrical signals with opposite polarity. Receivers compare the two signals and, when the differ‐ ence is sufficiently positive or negative, generate a one or zero internally to rep‐ resent the intended serial bit stream to the rest of the Physical Layer. 

## **PCI Express Technology** 

_Figure 13‐1: Electrical Sub‐Block of the Physical Layer_ 

**==> picture [367 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Physical Layer Physical Layer<br>Tx Rx Tx Rx<br>Logical Logical<br>Tx Rx Tx Rx<br>Electrical Electrical<br>Link<br>Tx+ Tx- Rx+ Rx- CTX Tx- Tx+ Rx- Rx+<br>CTX<br>**----- End of picture text -----**<br>


When the Link is in the L0 full‐on state, the drivers apply the differential volt‐ age associated with a logical 1 and logical 0 while maintaining the correct DC common mode voltage. Receivers sense this voltage as the input stream, but if it drops below a threshold value, it’s understood to represent the Electrical Idle Link condition. Electrical Idle is entered when the Link is disabled, or when ASPM logic puts the Link into low‐power Link states such as L0s or L1 (see “Electrical Idle” on page 736 for more on this topic). 

Devices must support the Transmitter equalization methods required for each supported data rate so they can achieve adequate signal integrity. De‐emphasis is applied for 2.5 and 5.0 GT/s, and a more complex equalization process is applied for 8.0 GT/s. These are described in more detail in “Signal Compensa‐ tion” on page 468, and “Recovery.Equalization” on page 587. 

The drivers and Receivers are short‐circuit tolerant, making PCIe add‐in cards suited for hot (powered‐on) insertion and removal events in a hot‐plug environ‐ ment. The Link connecting two components is AC‐coupled by adding a capaci‐ tor in‐line, typically near the Transmitter side of the Link. This serves to de‐ 
couple the DC part of the signal between the Link partners and means they don’t have to share a common power supply or ground return path, as when the devices are connected over a cable. Figure 13‐1 on page 450 illustrates the place‐ ment of this capacitor (CTX) on the Link. 

## **High Speed Signaling** 

The high‐speed signaling environment of PCIe is characterized by the drawing in Figure 13‐2 on page 451. This low‐voltage differential signaling environment is a common method used in many serial transports and one reason is for the noise rejection it provides. Electrical noise that affects one signal will also affect the other because they are on adjacent pins and their traces are very close to each other. Since both signals are influenced, as shown in Figure 13‐3 on page 452, the difference between them doesn’t change much and is therefore not seen at the receiver. 

A design goal for the 3.0 spec revision was that the 8.0 GT/s rate should still work with existing standard FR4 circuit boards and connectors, and that was achieved by changing the encoding scheme from the old 8b/10b to the new 128b/130b model to keep the frequency low. This goal will probably change with the next speed step (Gen4). 

_Figure 13‐2: Differential Transmitter/Receiver_ 

**==> picture [384 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Logic<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>VTX-CM = 0 - 3.6 V<br>ZTX = ZRX = 50 Ohms +/- 20%<br>CTX = 75 - 265 nF (Gen1 & Gen2)<br>= 176 - 265 nF (Gen3)<br>No Spec<br>**----- End of picture text -----**<br>


## **PCI Express Technology** 

_Figure 13‐3: Differential Common‐Mode Noise Rejection_ 

**==> picture [374 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
D+<br>D-<br>Reference voltage shift<br>Differential<br>voltage remains<br>+ Differential the same<br>voltage<br>Tx Rx<br>- +<br>0 V 0 V<br>-<br>Single-<br>ended<br>voltage Single-ended<br>voltage changes<br>Transient Noise<br>Tx Rx<br>+ +<br>Vcm Vcm<br>- -<br>Differential<br>voltage<br>remains same<br>**----- End of picture text -----**<br>


## **Clock Requirements** 

## **General** 

For all data rates, both Transmitter and Receiver clocks must be accurate to within +/‐ 300 ppm (parts per million) of the center frequency. In the worst case, the Transmitter and Receiver could both be off by 300 ppm in opposite direc‐ tions, resulting in a maximum difference of 600 ppm. That worst‐case model translates to a gain or loss of 1 clock every 1666 clocks and that’s the difference that a Receiver’s clock compensation logic must take into account. 

Devices are allowed to derive their clocks from an external source, and the 100 MHz Refclk is still optionally available for this purpose in the 3.0 spec. Using the Refclk permits both Link partners to readily maintain the 600 ppm accuracy even when Spread Spectrum Clocking is applied. 
## **SSC (Spread Spectrum Clocking)** 

SSC is an optional technique used to modulate the clock frequency slowly over a prescribed range to spread the signal’s EMI (Electro‐Magnetic Interference) across a range of frequencies rather than allowing it all to be concentrated at the center frequency. Spreading the radiated energy helps a device or system to pass government emissions standards by staying under a threshold value, as illustrated in Figure 13‐4 on page 454. Note that the frequency of interest for the signal is only half the clock rate because two rising clock edges are needed to create one cycle on the data, as illustrated in Figure 13‐5 on page 454. For exam‐ ple, a 2.5 GT/s rate uses a bit clock of 2.5 GHz, resulting in a frequency of inter‐ est on the traces of 1.25 GHz. 

The use of SCC is not required by the spec but, if will be supported, the follow‐ ing rules apply: 

- The clock can be modulated by +0% to ‐0.5% from nominal (5000 ppm), referred to as “down spreading.” A frequency modulation envelope is not specified, but a sawtooth‐wave pattern like the one shown in Figure 13‐6 on page 455 yields good results. Note that there is a trade‐off with down spreading, because the average clock frequency will now be 0.25% lower than it would have been without SSC, resulting in a slight performance reduction. 

- The modulation rate must be between 30KHz and 33KHz. 

- The +/‐ 300 ppm requirement for clock frequency accuracy still holds and therefore so does the maximum 600 ppm variation between Link partners. The spec states that most implementations will require both Link partners to use the same clock source, although it’s not required. One way to do that would be for them to both use a modulated version of the Refclk to derive their own clocks (see “Common Refclk” on page 456). 

## **PCI Express Technology** 

_Figure 13‐4: SSC Motivation_ 

**==> picture [324 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
EMI Power Threshold<br> Ordinary Signal<br>Spread-Spectrum<br>Signal<br>range = 0.5%<br>Signal<br>Frequency<br>Frequency (GHz)<br>Emitted Power (dB)<br>**----- End of picture text -----**<br>


_Figure 13‐5: Signal Rate Less Than Half the Clock Rate_ 

**==> picture [384 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
Signal on<br>the wire<br>Tx Clock<br>**----- End of picture text -----**<br>

_Figure 13‐6: SSC Modulation Example_ 

**==> picture [274 x 147] intentionally omitted <==**

**----- Start of picture text -----**<br>
nominal<br>nominal - 0.5%<br>Time<br>modulation modulation<br>period/2 period<br>Frequency<br>**----- End of picture text -----**<br>


## **Refclk Overview** 

Receivers must generate their own clocks to operate their internal logic, but there are some options for generating the recovered clock for the incoming bit stream. The details for them have developed with each succeeding version of the spec and are based on the data rate. 

## **2.5 GT/s** 

In the early spec versions using the 2.5 GT/s rate, information regarding the optional Refclk was not included in the base spec but instead in the separate CEM (Card Electro‐Mechanical) spec for PCIe. A number of parameters were specified there and several general terms have been carried forward to the newer versions of the spec. The Refclk was described as a 100 MHz differential clock driving a 100  differential load (+/‐ 10%) with a trace length limited to 4 inches. SSC is allowed, as described in “SSC (Spread Spectrum Clocking)” on page 453. 

## **5.0 GT/s** 

When the 5.0 GT/s rate was developed, the spec writers chose to include the Refclk information in the electrical section of the base spec and listed three options for the clock architecture: 

**Common Refclk.** The first architecture described is one in which both Link partners make use of the same Refclk, as shown in Figure 13‐7 on page 456. There are three straightforward advantages for this implementation: 

- First, the jitter associated with the reference clock is the same for both Tx and Rx and is thus tracked and accounted for intrinsically. 

- – Second, the use of SSC will be simplest with this model because maintaining the 600 ppm separation between the Tx and Rx clocks is easy if both follow the same modulated reference. 

- Third, the Refclk remains available during low‐power Link states L0s and L1 and that allows the Receiver’s CDR to maintain a sem‐ blance of the recovered clock even in the absence of a bit stream to supply the edges in the data. That, in turn, keeps the local PLLs from drifting as much as they otherwise would, resulting in a reduced recovery time back to L0 compared to the other clocking options. 

_Figure 13‐7: Shared Refclk Architecture_ 

**==> picture [374 x 138] intentionally omitted <==**

**----- Start of picture text -----**<br>
+<br>Tx Lane in Rx<br>Register Tx directionone Rx Register<br>-<br>CDR<br>PLL<br>PLL<br>Refclk<br>**----- End of picture text -----**<br>


**Data Clocked Rx Architecture.** In this clock architecture, the Receiver doesn’t use a reference clock at all, but simply recovers the Transmitter clock from the data stream, as shown in Figure 13‐9 on page 457. This implementation is clearly the simplest of the three and would therefore ordinarily be preferred. The spec doesn’t prohibit the use of SSC in this model, but doing so would bring up two issues. First, the Receiver CDR must remain locked onto the input frequency as it modulates through a much wider range (5600 ppm instead of the usual 600 ppm), and that could require more complex logic. And second, the maximum clock frequency separation of 600ppm must still be maintained and it’s less clear how that would be done without a common reference. 

</td>
<td style="background-color:#e8e8e8">

**第 13 章：物理层 - 电气**

_图 13-8：数据时钟 Rx 架构_

**==> 图片 [374 x 92] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+<br>
Tx 通道方向 接收器<br>
寄存器 Tx 一个 Rx 寄存器<br>
-<br>
CDR<br>
PLL<br>
Refclk<br>
**----- 图片文字结束 -----**<br>


**单独的 Refclks (Separate Refclks)。** 最后，链路伙伴也可以使用不同的参考时钟，如图 13-9（第 457 页）所示。但是，此实现对 Refclks 提出了明显更严格的要求，因为在接收器处看到的抖动将是它们的 RSS（Root Sum of Squares，均方根和）组合，从而使时序预算变得困难。在此模型中管理 SSC 也变得异常困难，这就是规范声明在这种情况下必须关闭 SSC 的原因。总体而言，规范给人的印象是这是最不理想的选择，并声明它没有明确定义此架构的要求。

_图 13-9：单独的 Refclk 架构_

**==> 图片 [374 x 109] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+<br>
Tx 通道方向 接收器<br>
寄存器 Tx 一个 Rx 寄存器<br>
-<br>
CDR<br>
PLL<br>
Refclk 1 PLL<br>
Refclk 2<br>
**----- 图片文字结束 -----**<br>


## **8.0 GT/s**

规范中也为该数据速率描述了相同的三个时钟架构。一个区别是现在定义了两种类型的 CDR：用于共享 Refclk 架构的一阶 CDR，以及用于数据时钟架构的二阶 CDR。这反映了这样一个事实，即对于较低的数据速率也是如此，数据时钟架构的 CDR 将需要更复杂，以便在参考在 SSC 的宽范围内变化时保持锁定。

## **发送器 (Tx) 规范 (Transmitter (Tx) Specs)**

## **测量 Tx 信号 (Measuring Tx Signals)**

规范指出，在更高频率下测量 Tx 输出的方法有限。在 2.5 GT/s 时，可以将测试探头放在 DUT（Device Under Test，被测设备）的引脚附近，但对于更高的速率，有必要使用带有 SMA（SubMiniature version A）微波型同轴连接器的"分离通道"，如第 458 页图 13-10 中 TP1（Test Point 1）、TP2 和 TP3 所示。请注意，必须为被测设备提供低抖动时钟源，以便在输出处看到的抖动仅由设备本身引入。规范还提到，在测试期间，重要的是让设备同时使用尽可能多的通道和其他输出，以便最好地模拟真实系统。

由于分离通道会对信号引入一些影响，因此对于 8.0 GT/s，有必要能够测量这些影响并将其从被测信号中移除（去嵌入）。实现此目的的一种方法是让测试板提供与用于设备引脚的路径非常相似的另一个信号路径。用已知信号表征此"复制通道"会提供有关通道的必要信息，从而可以将其影响从 DUT 信号中去嵌入，以便恢复组件引脚处的信号。

_图 13-10：测试电路测量通道_

**==> 图片 [294 x 159] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
DUT<br>
TP1<br>
分离通道<br>
低抖动<br>
时钟源<br>
复制通道<br>
TP2 TP3<br>
**----- 图片文字结束 -----**<br>


**第 13 章：物理层 - 电气**

## **Tx 阻抗要求 (Tx Impedance Requirements)**

为了获得最佳精度，分离通道的特性差分阻抗应在 10% 内为 100 Ω 差分，单端阻抗为 50 Ω。为了匹配此环境，发送器在 2.5 GT/s 期间信号传输期间具有 80 至 120 Ω 的差分低阻抗值，在 5.0 和 8.0 GT/s 时不超过 120 Ω。对于接收器，单端阻抗在 2.5 或 5.0 GT/s 时为 40 - 60 Ω，但对于 8.0 GT/s，未给出特定值。相反，只是注意到单端接收器阻抗必须在进入 Detect LTSSM 状态时在 20% 内为 50 Ω，以便检测电路将正确感应接收器。

发送器还必须在任何时候发送差分信号时满足回波损耗参数 RLTX-DIFF 和 RLTX-CM。作为该术语的非常简要介绍，"回波损耗"是衡量通过传输路径传输或从传输路径反射回的能量。回波损耗是用于分析高频信号环境的多个"散射 (Scattering)"参数（S 参数）之一。当频率较低时，集总元件描述就足够了，但当频率变得足够高以至于波长接近电路的大小时，需要分布式模型，这就是 S 参数用于表示的内容。规范描述了许多这些参数来表征传输路径，但此高频分析的详细信息确实超出了本书的范围。

当信号未被驱动时，如在低功耗链路状态中，发送器可能会进入高阻抗状态以减少功耗。在这种情况下，它只需要满足 ITX-SHORT 值，并且差分阻抗未定义。

## **ESD 和短路要求 (ESD and Short Circuit Requirements)**

所有信号和电源引脚必须使用人体模型承受 2000V ESD（静电放电），使用充电设备模型承受 500V。有关这些模型或 ESD 的更多详细信息，请参阅 JEDEC JESE22-A114-A 规范。

ESD 要求不仅防止静电损坏，而且有助于支持意外热插拔事件（在通电时添加或移除附加卡）。该目标还促使要求发送器和接收器能够承受 ITX-SHORT 的持续短路电流（参见第 498 页的表 13-5）。

## **接收器检测 (Receiver Detection)**

## **概述 (General)**

第 461 页图 13-11 中发送器中显示的 Detect 块用于检查在退出复位后链路另一端是否存在接收器。在串行传输世界中，此步骤有点不寻常，因为向链路伙伴发送数据包并通过它是否响应来测试其存在是足够简单的。然而，PCIe 中此方法的原因是提供测试环境中的自动硬件辅助。如果检测到正确的负载，但链路伙伴拒绝发送 TS1 并参与链路训练，则组件将假定它必须处于测试环境中，并将开始发送合规模式以促进测试。由于链路在复位或上电事件后将始终以 2.5 GT/s 开始操作，因此 Detect 仅用于 2.5 GT/s 速率。这就是为什么接收器的单端 DC 阻抗为该速率指定（ZRX-DC = 40 到 60 Ω），以及为什么无论其预期运行速度如何，Detect 逻辑都必须包含在每个设计中。

通过将发送器的 DC 共模电压设置为一个值然后更改为另一个值来完成检测。知道接收器存在时的预期充电时间，逻辑将测量的时间与该时间进行比较。如果连接了接收器，则由于接收器的端接，充电时间（RC 时间常数）相对较长。否则，充电时间要短得多

## **检测接收器存在 (Detecting Receiver Presence)**

1. 复位或上电后，发送器在 D+ 和 D- 端子上驱动稳定电压。

2. 然后发送器将共模电压沿正方向更改不超过所有三个数据速率规定的 VTX-RCV-DETECT 量 600mV。

3. Detect 逻辑测量充电时间：

 - 如果充电时间短，则接收器不存在。

 - 如果充电时间长（由串联电容器和接收器端接主导），则接收器存在。

规范在这里提到了一个可能的问题：正确的负载可能出现在一个差分信号上但不出现在另一个上，如果检测不检查两者，它可能会误解情况。避免这种情况的简单方法是对 D+ 和 D- 都执行 Detect 操作。3.0 规范不要求这样做，

**第 13 章：物理层 - 电气**

但提到未来的规范版本可能会要求。因此，明智的做法是在新设计中包含此功能。

_图 13-11：接收器检测机制_

**==> 图片 [370 x 380] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Detect<br>
逻辑 接收器存在<br>
D+ CTX ZTX => 长充电时间 D+<br>
+<br>
通道方向 发送器一个 接收器<br>
CTX ZTX<br>
-<br>
D- D-<br>
ZTX ZTX ZRX ZRX<br>
VRX-CM = 0 V<br>
VCM<br>
Detect<br>
逻辑<br>
接收器不存在<br>
D+ CTX => 短充电时间<br>
发送器<br>
CTX<br>
D-<br>
ZTX ZTX<br>
VCM<br>
无规范<br>
**----- 图片文字结束 -----**<br>


## **发送器电压 (Transmitter Voltages)**

差分信号传输（与 PCI 和 PCI-X 中采用的单端信号传输相反）非常适合高频信号传输。差分信号传输的一些优点是：

- 接收器查看信号之间的差异，因此每个单独的电压摆幅可以更小，从而允许更高频率而不超过功率预算。

- 由于通过并排使用相反极性的电压而产生的两个信号的噪声抵消，EMI 减少了。

- 抗噪性非常好，因为影响一个信号的噪声也会以相同方式影响另一个信号，结果接收器不会注意到这种变化（参见第 452 页图 13-3）。

## **DC 共模电压 (DC Common Mode Voltage)**

在链路训练的 Detect 状态之后，发送器 DC 共模电压 VTX-DC-CM（参见第 489 页表 13-3）必须保持在相同电压。共模电压仅在 L2 或 L3 低功耗链路状态中关闭，在这些状态下设备的主电源被移除。设计人员可以选择 0 至 3.6V 范围内的任何共模电压。

## **全摆幅差分电压 (Full-Swing Differential Voltage)**

发送器输出由两个信号 D+ 和 D- 组成，它们是相同的但使用相反的极性。当 D+ 信号为高且 D- 信号为低时，表示逻辑 1，而通过将 D+ 信号驱动为低并将 D- 信号驱动为高来表示逻辑 0，如图 13-13（第 464 页）所示。

由发送器驱动的差分峰峰值电压 VTX-DIFFp-p（参见第 489 页表 13-3）在 800 mV 和 1200 mV 之间（对于 8.0 GT/s 为 1300 mV）。

- 逻辑 1 用正差分电压表示。

- 逻辑 0 用负差分电压表示。

在电气空闲期间，发送器将差分峰值电压 VTX-IDLE-DIFFp[(参见第 489 页表 13-3) 保持在非常接近零（0-20 mV）的位置。在此]期间，发送器可能处于低阻抗或高阻抗状态。

接收器通过评估链路上的电压来感应逻辑 1 或 0 以及电气空闲。高频下预期的信号损耗意味着

**第 13 章：物理层 - 电气**

接收器必须能够感应信号的衰减版本，定义为 VRX-DIFFp-p（参见第 498 页表 13-5）。

_图 13-12：差分信号传输_

**==> 图片 [301 x 145] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
V+<br>
D+<br>
V<br>
cm<br>
接收器减去<br>
D- 从 D+ 值<br>
得到差分<br>
D- 电压。<br>
V<br>
cm<br>
V-<br>
**----- 图片文字结束 -----**<br>


## **差分表示法 (Differential Notation)**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-11-2"></a>
## 11.2 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>
_Figure 13‐8: Data Clocked Rx Architecture_ 

**==> picture [374 x 92] intentionally omitted <==**

**----- Start of picture text -----**<br>
+<br>Tx Lane in Rx<br>Register Tx directionone Rx Register<br>-<br>CDR<br>PLL<br>Refclk<br>**----- End of picture text -----**<br>


**Separate Refclks.** Finally, it’s also possible for the Link partners to use dif‐ ferent reference clocks, as shown in Figure 13‐9 on page 457. However, this implementation makes substantially tighter demands on the Refclks because the jitter seen at the Receiver will be the RSS (Root Sum of Squares) combination of them both, making the timing budget difficult. It also becomes enormously more difficult to manage SSC in this model and that’s why the spec states that SSC must be turned off in this case. Overall, the spec gives the impression that this is the least desirable alternative, and states that it doesn’t explicitly define the requirements for this architecture. 

_Figure 13‐9: Separate Refclk Architecture_ 

**==> picture [374 x 109] intentionally omitted <==**

**----- Start of picture text -----**<br>
+<br>Tx Lane in Rx<br>Register Tx directionone Rx Register<br>-<br>CDR<br>PLL<br>Refclk 1 PLL<br>Refclk 2<br>**----- End of picture text -----**<br>


## **8.0 GT/s** 

The same three clock architectures are described in the spec for this data rate, too. One difference is that two types of CDR are defined now: a 1[st] order CDR for the shared Refclk architecture, and a 2[nd] order CDR for the data clocked architecture. This just reflects the fact that, as it was for the lower data rates, the CDR for the data‐clocked architecture will need to be more sophisticated to be able to stay locked when the reference varies over a wide range for SSC. 

## **Transmitter (Tx) Specs** 

## **Measuring Tx Signals** 

The spec notes that the methods for measuring the Tx output are limited at the higher frequencies. At 2.5 GT/s it’s possible to put a test probe very near the pins of the DUT (Device Under Test), but for the higher rates it’s necessary to use a “breakout channel” with SMA (SubMiniature version A) microwave‐type coax‐ ial connectors, as illustrated at TP1 (Test Point 1), TP2, and TP3 in Figure 13‐10 on page 458. Note that it’s necessary to have a low‐jitter clock source to the device under test, so that jitter seen at the output is only introduced by the device itself. The spec also mentions that it’s important during testing for the device to have as many of its Lanes and other outputs in use at the same time as possible, so as to best simulate a real system. 

Since the breakout channel introduces some effects to the signal, for 8.0 GT/s it’s necessary to be able to measure those effects and remove (de‐embed) them from the signal being tested. One way to accomplish this is for the test board to sup‐ ply another signal path that is very similar to the one used for the device pins. Characterizing this “replica channel” with a known signal gives the needed information about the channel, allowing its effects to be de‐embedded from the DUT signals so the signal at the component pins can be recovered. 

_Figure 13‐10: Test Circuit Measurement Channels_ 

**==> picture [294 x 159] intentionally omitted <==**

**----- Start of picture text -----**<br>
DUT<br>TP1<br>Breakout Channel<br>Low-Jitter<br>Clock Source<br>Replica Channel<br>TP2 TP3<br>**----- End of picture text -----**<br>

## **Tx Impedance Requirements** 

For best accuracy, the characteristic differential impedance of the Breakout Channel should be 100  differential within 10%, with a single‐ended imped‐ ance of 50  . To match this environment, Transmitters have a differential low‐ impedance value during signaling between 80 and 120  at 2.5 GT/s, and no more than 120  at 5.0 and 8.0 GT/s. For receivers, the single‐ended impedance is 40 ‐ 60  at 2.5 or 5.0 GT/s, but for 8.0 GT/s no specific value is given. Instead, it’s simply noted that the single‐ended receiver impedance must be 50  within 20% by the time the Detect LTSSM state is entered so that the detect circuit will sense the Receiver correctly. 

Transmitters must also meet the return loss parameters RLTX‐DIFF and RLTX‐CM anytime differential signals are sent. As a very brief introduction to this termi‐ nology, “return loss” is a measure of energy transmitted through or reflected back from a transmission path. Return loss is one of several “Scattering” param‐ eters (S‐parameters) that are used to analyze high‐frequency signal environ‐ ments. When frequencies are low, a lumped‐element description is sufficient, but when they become high enough that the wavelength approaches the size of the circuit, a distributed model is needed and that’s what S‐parameters are used to represent. The spec describes a number of these to characterize a transmis‐ sion path but the details of this high‐frequency analysis are really beyond the scope of this book. 

When a signal is not being driven, as would be the case in the low‐power Link states, the Transmitter may go into a high‐impedance condition to reduce the power drain. For that case, it only has to meet the ITX‐SHORT value and the dif‐ ferential impedance is not defined. 

## **ESD and Short Circuit Requirements** 

All signals and power pins must withstand a 2000V ESD (Electro‐Static Dis‐ charge) using the Human Body Model and 500V using the Charged Device Model. For more details on these models or ESD, see the JEDEC JESE22‐A114‐A spec. 

The ESD requirement not only protects against electro‐static damage, but facili‐ tates support of surprise hot insertion and removal events (adding or removing an add‐in card while the power is on). That goal also motivates the requirement that Transmitters and Receivers be able to withstand sustained short‐circuit cur‐ rents of ITX‐SHORT (see Table 13‐5 on page 498). 

## **Receiver Detection** 

## **General** 

The Detect block in the Transmitter shown in Figure 13‐11 on page 461 is used to check whether a Receiver is present at the other end of the Link after coming out of reset. This step is a little unusual in the serial transport world because it’s easy enough to send packets to the Link partner and test its presence by whether or not it responds. The motivation for this approach in PCIe, however, is to provide an automatic hardware assist in a test environment. If the proper load is detected, but the Link partner refuses to send TS1s and participate in Link Training, the component will assume that it must be in a test environment and will begin sending the Compliance Pattern to facilitate testing. Since a Link will always start operation at 2.5 GT/s after a reset or power‐up event, Detect is only used for the 2.5 GT/s rate. That’s why the Receiver’s single‐ended DC impedance is specified for that rate (ZRX‐DC = 40 to 60  ), and why the Detect logic must be included in every design regardless of its intended operating speed. 

Detection is accomplished by setting the Transmitter’s DC common mode volt‐ age to one value and then changing it to another. Knowing the expected charge time when a Receiver is present, the logic compares the measured time against that. If a Receiver is attached, the charge time (RC time constant) is relatively long due to the Receiver’s termination. Otherwise, the charge time is much shorter 

## **Detecting Receiver Presence** 

1. After reset or power‐up, Transmitters drive a stable voltage on the D+ and D‐ terminal. 

2. Transmitters then change the common mode voltage in a positive direction by no more than the VTX‐RCV‐DETECT amount of 600mV specified for all three data rates. 

3. Detect logic measures the charge time: 

 - Receiver is absent if the charge time is short. 

 - Receiver is present if the charge time is long (dominated by the series capacitor and Receiver termination). 

The spec mentions a possible problem here: the proper load may appear on one of the differential signals but not the other, and if detection doesn’t check both it could misinterpret the situation. The simple way to avoid that would be to per‐ form the Detect operation on both D+ and D‐. The 3.0 spec does not require this, 
but mentions that future spec revisions may. Therefore, it would be wise to include this functionality in new designs. 

_Figure 13‐11: Receiver Detection Mechanism_ 

**==> picture [370 x 380] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Logic Receiver Present<br>D+ CTX ZTX => Long Charge time D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>Detect<br>Logic<br>Receiver Absent<br>D+ CTX => Short Charge time<br>Transmitter<br>CTX<br>D-<br>ZTX ZTX<br>VCM<br>No Spec<br>**----- End of picture text -----**<br>


## **Transmitter Voltages** 

Differential signaling (as opposed to the single‐ended signaling employed in PCI and PCI‐X) is ideal for high frequency signaling. Some advantages of differ‐ ential signaling are: 

- Receivers look at the difference between the signals, so the voltage swing for each one individually can be smaller, allowing higher frequencies with‐ out exceeding the power budget. 

- EMI is reduced because of the noise cancellation that results from having the two signals by side by side, using opposite‐polarity voltages. 

- Noise immunity is very good, because noise that affects one signal will also affect the other in the same way, with the result that the Receiver doesn’t notice the change (refer to Figure 13‐3 on page 452). 

## **DC Common Mode Voltage** 

After the Detect state of Link training, the Transmitter DC common mode volt‐ age VTX‐DC‐CM (see Table 13‐3 on page 489) must remain at the same voltage. The common mode voltage is turned off only in the L2 or L3 low‐power Link states, in which main power to the device is removed. A designer can choose any common mode voltage in the range from 0 to 3.6V. 

## **Full-Swing Differential Voltage** 

The Transmitter output consists of two signals, D+ and D‐, that are identical but use opposite polarities. A logical one is indicated when the D+ signal is high and the D‐ signal low, while a logical zero is represented by driving the D+ sig‐ nal low and the D‐ signal high, as shown in Figure 13‐13 on page 464. 

The differential peak‐to‐peak voltage driven by the Transmitter VTX‐DIFFp‐p (see Table 13‐3 on page 489) is between 800 mV and 1200 mV (1300 mV for 8.0 GT/s). 

- Logical 1 is signaled with a positive differential voltage. 

- Logical 0 is signaled with a negative differential voltage. 

During Electrical Idle the Transmitter holds the differential peak voltage VTX‐ IDLE‐DIFFp[(see Table 13‐3 on page 489) very near zero (0‐20 mV). During this] time the Transmitter may be in either a low‐ or high‐impedance state. 

The Receiver senses a logical one or zero, as well as Electrical Idle, by evaluating the voltage on the Link. The signal loss expected at high frequency means the 
Receiver must be able to sense an attenuated version of the signal, defined as VRX‐DIFFp‐p (see Table 13‐5 on page 498). 

_Figure 13‐12: Differential Signaling_ 

**==> picture [301 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
V+<br>D+<br>V<br>cm<br>Receiver subtracts<br>D- from D+ value to<br>arrive at differential<br>D- voltage.<br>V<br>cm<br>V-<br>**----- End of picture text -----**<br>


## **Differential Notation**

</td>
<td style="background-color:#e8e8e8">

差分信号电压是通过取两个导体 D+ 和 D- 上的电压差来定义的。每个导体上相对于地的电压为 VD+ 和 VD-。差分电压由 VDIFF = VD+ ‐ VD- 给出。共模电压 VCM 定义为信号开关周围的电压，即 VCM = (VD+ + VD-) / 2 给出的平均值。

规范在讨论差分电压时使用两个术语，有时会导致混淆。如第 464 页图 13-13 所示，峰值是信号之间的最大电压差，而峰峰值是加上相反方向的最大值。对于对称信号，峰峰值就是峰值的两倍。

1. 差分峰值电压 => VDIFFp = (max |VD+ ‐ VD‐ |)

2. 差分峰峰值电压 => VDIFFp‐p = 2 *(max |VD+ ‐ VD‐ |)

作为示例，假设 VCM = 0 V，则如果 D+ 值为 300mV 且 D- 值为 ‐300mV，则对于逻辑 1，VDIFFp 将是 300 ‐ (‐300) = 600 mV。类似地，对于逻辑 0，它将是 (‐300) ‐ (+300) = ‐600 mV。此对称情况的 VDIFFp‐p 将是 1200 mV。在应用均衡之前，2.5 GT/s 和 5.0 GT/s 的允许 VDIFFp‐p 范围为 800 到 1200 mV，而对于 8.0 GT/s 则为 800 到 1300 mV。

_图 13-13：差分峰峰值 (_ VDIFFp‐p _) 和峰值 (_ VDIFFp _) 电压_

**==> 图片 [327 x 127] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
D+<br>
V VDIFFp VDIFFp<br>
CMp（逻辑 1）（逻辑 0）<br>
D-<br>
0 V<br>
VDIFFp-p = 2 * max | VD+ - VD- | = VDIFFp（逻辑 1）+ VDIFFp（逻辑 0）<br>
**----- 图片文字结束 -----**<br>


## **减摆幅差分电压 (Reduced-Swing Differential Voltage)**

长或损耗大的通道需要全摆幅电压，并且发送器需要支持它。但是，当信号环境短且低损耗时，不需要高电压，可以通过降低电压来实现节能。考虑到这一点，2.5 GT/s 和 5.0 GT/s 的规范定义了另一种用于功率敏感系统的减摆幅电压，其中使用短通道。在这种模式下，电压降低到其全摆幅范围的一半左右。支持此操作是可选的，并且选择它的方法未定义，将是实现特定的。

对于 8.0 GT/s 信号传输也是如此，只不过在这种情况下它是通过使用有限范围的系数来实现的。例如，减摆幅情况的最大增益限制为 3.5 dB。与较低的数据速率一样，对此电压模型的支持是可选的，但现在实现它的方法很简单：只需设置 Tx 系数值即可实现。

应该注意的是，接收器电压电平与发送器无关，这是我们直观预期的：接收到的信号始终需要满足正常要求，因此发送器和通道必须设计为保证它。

## **均衡电压 (Equalized Voltage)**

为了在本节中保持良好的流程，这个大主题在第 468 页的"信号补偿 (Signal Compensation)"部分单独介绍。

**第 13 章：物理层 - 电气**

## **电压裕量 (Voltage Margining)**

裕量的概念是发送器特性（如输出电压）可以在测试期间在很宽的值范围内调整，以确定它能多好地处理信号环境。2.5 GT/s 速率不包括此功能，但电压裕量是随着 5.0 GT/s 速率添加的，并且必须由使用该速率或更高速率的发送器实现。其他参数（如去加重或抖动）也可以选择性地进行裕量。裕量调整的粒度必须在链路基础上可控，并且可以在通道基础上可控。此控制通过 PCIe Capability 寄存器块中的 Link Control 2 寄存器完成。传输裕量字段（如图 13-14（第 465 页）所示）包含 3 位，因此可以表示 8 个级别。未定义其值，并且不需要实现所有值。默认值是全零，表示正常工作范围。

重要的是要注意，此字段仅用于调试和合规测试目的，在此期间软件仅允许在这些时间修改它。在所有其他时间，要求将该值设置为默认值全零。

_图 13-14：Link Control 2 寄存器中的 Transmit Margin 字段_

**==> 图片 [355 x 211] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Link Control 2 寄存器<br>
15 12 11 10 9 7 6 5 4 3 0<br>
合规预设/<br>
去加重<br>
合规 SOS<br>
进入修改合规<br>
传输裕量<br>
可选去加重<br>
硬件自主<br>
速度禁用<br>
进入合规<br>
目标链路速度<br>
**----- 图片文字结束 -----**<br>


对于 8.0 GT/s，发送器需要实现电压裕量并使用 Link Control 2 寄存器中的相同字段，但均衡增加了一些对选项的约束，因为它不能要求比正常操作定义的 1/24 分辨率更精细的系数或预设分辨率。

在 Tx 裕量期间，2.5 GT/s 和 5.0 GT/s 的均衡容差从 +/‐ 0.5 dB 放宽到 +/‐ 1.0 dB。对于 8.0 GT/s 速率，容差由系数粒度和为发送器指定的正常均衡器容差定义。

## **接收器 (Rx) 规范 (Receiver (Rx) Specs)**

## **接收器阻抗 (Receiver Impedance)**

除非设备断电（如在 L2 和 L3 电源状态期间或基本复位期间），否则接收器需要满足 RLRX-DIFF 和 RLRX-CM（参见第 498 页表 13-5）参数。在这些情况下，接收器进入高阻抗状态，必须满足 ZRX-HIGH-IMP-DC-NEG 和 ZRX-HIGH-IMP-DC-NEG 参数。

（参见第 498 页表 13-5。）

## **接收器 DC 共模电压 (Receiver DC Common Mode Voltage)**

接收器的 DC 共模电压被指定为 0V 以适应所有数据速率，这在第 467 页图 13-15 中通过显示信号端接连接到地来表示。CTX 在线电容器允许发送器处的此电压不同，指定范围为 0 - 3.6V。当发送器和接收器在同一机箱中并具有相同电源时，这不那么有趣，但如果它们通过电缆连接并驻留在具有不同电源的不同机器中，则变得更加重要。在这种情况下，很难避免机器之间的参考电压差异，并且由于信号电压已经很小，这种差异可能使接收器难以识别信号。当将使用某种连接器时，此电容器的位置必须靠近发送器引脚，但如果没有连接器，它可以位于传输线上的任何方便的位置。尽管它可以集成到设备中，但预计 CTX 将是外部的，因为它太大了而无法集成。

**第 13 章：物理层 - 电气**

第 467 页图 13-15 中的图还显示了接收器处的一组可选电阻，标记为"无规范 (No Spec)"，因为规范中没有提到它们。这里的故事是接收器设计人员不喜欢使用零共模电压，原因很简单，这通常需要他们实现两个参考电压，一个高于零，一个低于它。首选的实现将信号完全偏移到零的上方或下方，以便只需要一个参考电压。虚线内显示的电路通过添加一个小值的在线电容器将线上信号的 DC 分量与接收器本身的 DC 分量解耦来实现此目的。然后，电阻梯形用于将接收器的共模电压偏移到一个方向或另一个方向以实现目标。

_图 13-15：接收器 DC 共模电压调整_

**==> 图片 [384 x 273] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
小 大<br>
电阻比率<br>
大 设置 DC 共模电压<br>
小 大<br>
检测 大<br>
逻辑<br>
D+ CTX ZTX D+<br>
+<br>
通道方向 发送器一个 接收器<br>
CTX ZTX<br>
-<br>
D- D-<br>
ZTX ZTX ZRX ZRX<br>
VRX-CM = 0 V<br>
VCM<br>
无规范<br>
**----- 图片文字结束 -----**<br>


## **传输损耗 (Transmission Loss)**

发送器驱动最小差分峰峰值电压 VTX-DIFFp-p 为 800 mV。接收器灵敏度设计为最小差分峰峰值电压 (VRX-DIFFp-p) 为 175 mV。这转化为链路设计为 13.2dB 的损耗预算。尽管电路板设计人员可以确定针对各种频率绘制的链路的衰减损耗预算，但发送器和接收器眼图测量是链路损耗预算的最终决定因素。眼图在第 485 页的"眼图 (Eye Diagram)"中描述。驱动高达最大允许差分峰峰值电压 1200 mV 的发送器可以补偿具有最坏情况衰减特性的有损链路。

## **AC 耦合 (AC Coupling)**

PCI Express 要求在线 AC 耦合电容器放置在每个通道上，通常靠近发送器。电容器可以集成到系统板上，或集成到设备本身中，尽管它们所需的大尺寸使其不太可能。具有 PCI Express 设备的附加卡必须将电容器放置在卡的发送器附近或将电容器集成到 PCIe 硅片中。这些电容器在链路两端提供两个设备之间的 DC 隔离，从而通过允许设备使用独立的电源和接地平面来简化设备设计。

## **信号补偿 (Signal Compensation)**

## **与 Gen1 和 Gen2 PCIe 关联的去加重 (De-emphasis Associated with Gen1 and Gen2 PCIe)**

对于 2.5 GT/s 和 5.0 GT/s 传输，PCIe 强制使用一种相当简单的发送器均衡形式，称为**去加重 (de-emphasis)**，以减少链路传输线上信号失真的影响。这种失真问题始终存在，但随着频率增加和有损传输线而变得更糟。

## **问题 (The Problem)**

随着数据速率变高，单位间隔 (UI - 位时间) 变得更小，结果是越来越难以避免一个位时间的值影响另一位时间的值。通道始终抵抗电压电平的变化，我们尝试切换电压的速度越快，

**第 13 章：物理层 - 电气**

这种影响就越明显。然而，当信号已在相同电压下保持了几个位时间时（如在发送几个相同极性的连续位时），通道有更多时间接近目标电压。产生的较高电压使得在极性确实改变时难以在所需时间内更改为相反的值。这种前一位影响后续位的问题称为**ISI（码间干扰，inter-symbol interference）**。

## **去加重有何帮助？ (How Does De-Emphasis Help?)**

去加重降低了位流中重复位的电压。虽然起初听起来违反直觉，因为这降低了信号摆幅，因此降低了到达接收器的能量，但对这些情况降低发送器电压可以显著改善信号质量。第 469 页图 13-16 通过显示发送器输出"1000010000"来说明这一点，其中相同极性的重复位已被去加重。去加重可以被认为是一个二抽头 Tx 均衡器，与其相关的一些规则是：

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-11-3"></a>
## 11.3 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

A differential signal voltage is defined by taking the difference in the voltage on the two conductors, D+ and D‐. The voltage with respect to ground on each con‐ ductor is VD+ and VD‐. The differential voltage is given by VDIFF = VD+ ‐ VD‐. The Common Mode voltage, VCM, is defined as the voltage around which the signal is switching, which is the mean value given by VCM = (VD++ VD‐) / 2. 

The spec uses two terms when discussing differential voltages and confusion sometimes arises as a result. As illustrated in Figure 13‐13 on page 464, the Peak value is the maximum voltage difference between the signals, while the Peak‐to‐ Peak voltage is that value plus the maximum in the opposite direction. For a symmetric signal, the Peak‐to‐Peak value is simply twice the Peak value. 

1. Differential Peak Voltage => VDIFFp = (max |VD+ ‐ VD‐ |) 

2. Differential Peak‐to‐Peak Voltage => VDIFFp‐p = 2 *(max |VD+ ‐ VD‐ |) 

As an example, assume VCM = 0 V, then if the D+ value is 300mV and the D‐ value is ‐300mV, then VDIFFp would be 300 ‐ (‐300) = 600 mV for a logical one. Similarly, it would be (‐300) ‐ (+300) = ‐600 mV for a logical zero. The VDIFFp‐p for this symmetric case would be 1200 mV. The allowed VDIFFp‐p range for 2.5 GT/s and 5.0 GT/s is 800 to 1200 mV, while for 8.0 GT/s it is 800 to 1300 mV before equalization is applied. 

_Figure 13‐13: Differential Peak‐to‐Peak (_ VDIFFp‐p _) and Peak (_ VDIFFp _) Voltages_ 

**==> picture [327 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
D+<br>V VDIFFp VDIFFp<br>CMp (Logical 1) (Logical 0)<br>D-<br>0 V<br>VDIFFp-p = 2 * max | VD+ - VD- | = VDIFFp (Logical 1) + VDIFFp (Logical 0)<br>**----- End of picture text -----**<br>


## **Reduced-Swing Differential Voltage** 

The full‐swing voltage is needed for channels that are long or otherwise lossy, and Transmitters are required to support it. But when the signal environment is short and low loss, a high voltage is unnecessary and a power savings can be realized by reducing it. With this in mind, the spec for 2.5 GT/s and 5.0 GT/s defines another, reduced‐swing voltage for power‐sensitive systems where a short channel is being used. In this mode the voltage is reduced to about half of its full‐swing range. Support for this operation is optional, and the means for selecting it is not defined and will be implementation specific. 

The same is true for 8.0 GT/s signaling, except that in this case it’s achieved by using a limited range of coefficients. For example, the maximum boost for the reduced‐swing case is limited to 3.5 dB. As with the lower data rates, support for this voltage model is optional, but now the means of achieving it is straight‐ forward: just set the Tx coefficient values to make it happen. 

It should be noted that the Receiver voltage levels are independent of the trans‐ mitter, which is intuitively what we’d expect: the received signal always needs to meet the normal requirements and so the Transmitter and channel must be designed to guarantee that it will. 

## **Equalized Voltage** 

In the interest of maintaining a good flow in this section, this large topic is cov‐ ered separately in the section called “Signal Compensation” on page 468. 
## **Voltage Margining** 

The concept of margining is that Transmitter characteristics like output voltage can be adjusted across a wide range of values during testing to determine how well it can handle a signaling environment. The 2.5 GT/s rate didn’t include this capability, but voltage margining was added with the 5.0 GT/s rate and must be implemented by Transmitters that use that rate or higher. Other parameters, like de‐emphasis or jitter can optionally be margined as well. The granularity for the margining adjustments must be controllable on a Link basis and may be controllable on a Lane basis. This control is accomplished by means of the Link Control 2 register in the PCIe Capability register block. The transmit margin field, shown in Figure 13‐14 on page 465, contains 3 bits and can thus represent 8 levels. Their values are not defined, and not all of them need to be imple‐ mented. The default value is all zeros, which represents the normal operating range. 

It’s important to note that this field is only intended for debug and compliance testing purposes during which software is only allowed to modify it during those times. At all other times, the value is required to be set to the default of all zeros. 

_Figure 13‐14: Transmit Margin Field in Link Control 2 Register_ 

**==> picture [355 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 Register<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


For 8.0 GT/s, transmitters are required to implement voltage margining and use the same field in the Link Control 2 register, but equalization adds some con‐ straints to the options because it can’t require finer coefficient or preset resolu‐ tion than the 1/24 resolution defined for normal operation. 

During Tx margining the equalization tolerance for 2.5 GT/s and 5.0 GT/s is relaxed from +/‐ 0.5 dB to +/‐ 1.0 dB. For the 8.0 GT/s rate, the tolerance is defined by the coefficient granularity and the normal equalizer tolerances spec‐ ified for the transmitter. 

## **Receiver (Rx) Specs** 

## **Receiver Impedance** 

Receivers are required to meet the RLRX‐DIFF and RLRX‐CM (see Table 13‐5 on page 498) parameters unless the device is powered down, as it would be, for example, in the L2 and L3 power states or during a Fundamental Reset. In those cases, a Receiver goes to the high impedance state and must meet the ZRX‐HIGH‐IMP‐DC‐NEG and ZRX‐HIGH‐IMP‐DC‐NEG parameters. 

(See Table 13‐5 on page 498.) 

## **Receiver DC Common Mode Voltage** 

The Receiver’s DC common mode voltage is specified to be 0V for all data rates, and that’s represented in Figure 13‐15 on page 467 by showing the signal termi‐ nations connected to ground. The CTX in‐line capacitor permits this voltage to be something different at the Transmitter, which is specified to be in the range from 0 ‐ 3.6V. That’s not as interesting when the Transmitter and Receiver are in the same enclosure and have the same power supply, but if they’re connected over a cable and reside in different machines with different power supplies it becomes more important. In that case it’s difficult to avoid reference voltage dif‐ ferences between the machines and, since the signal voltages are already small, such a difference could make the signal difficult to recognize at the Receiver. The location of this capacitor must be near the Transmitter pins when a connec‐ tor of some kind will be used but, if there’s no connector, it can be located at any convenient place on the transmission line. Although it could be integrated into a device, it’s expected that CTX will be external because it would be too big to inte‐ grate. 
The drawing in Figure 13‐15 on page 467 also shows an optional set of resistors at the Receiver, labeled as “No Spec” because they are not mentioned in the spec. The story here is that Receiver designers dislike using a common‐mode voltage of zero for the simple reason that it usually requires them to implement two reference voltages, one above zero and one below it. A preferred imple‐ mentation offsets the signal entirely above or below zero, so that only one refer‐ ence voltage is needed.The circuit shown within the dotted line accomplishes this by adding a small‐value in‐line capacitor to de‐couple the DC component of the signal on the wire from that of the Receiver itself. Then, a resistor ladder serves to offset the Receiver’s common‐mode voltage in one direction or the other to accomplish the goal. 

_Figure 13‐15: Receiver DC Common‐Mode Voltage Adjustment_ 

**==> picture [384 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
Small Big<br>Ratio of resistors<br>Big sets DC common<br>mode voltage<br>Small Big<br>Detect Big<br>Logic<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>No Spec<br>**----- End of picture text -----**<br>


## **Transmission Loss** 

The Transmitter drives a minimum differential peak‐to‐peak voltage VTX‐DIFFp‐p of 800 mV. The Receiver sensitivity is designed for a minimum dif‐ ferential peak‐to‐peak voltage (VRX‐DIFFp‐p) of 175 mV. This translates to a 13.2dB loss budget that a Link is designed for. Although a board designer can determine the attenuation loss budget of a Link plotted against various frequen‐ cies, the Transmitter and Receiver eye diagram measurement are the ultimate determinant of loss budget for a Link. Eye diagrams are described in “Eye Dia‐ gram” on page 485. A Transmitter that drives up to the maximum allowed dif‐ ferential peak‐to‐peak voltage of 1200 mV can compensate for a lossy Link that has worst‐case attenuation characteristics. 

## **AC Coupling** 

PCI Express requires in‐line AC‐coupling capacitors be placed on each Lane, usually near the Transmitter. The capacitors can be integrated onto the system board, or integrated into the device itself, although the large size they would need makes that unlikely. An add‐in card with a PCI Express device on it must place the capacitors on the card close to the Transmitter or integrate the capaci‐ tors into the PCIe silicon. These capacitors provide DC isolation between two devices on both ends of a Link thus simplifying device design by allowing devices to use independent power and ground planes. 

## **Signal Compensation** 

## **De-emphasis Associated with Gen1 and Gen2 PCIe** 

For 2.5 GT/s and 5.0 GT/s transmission, PCIe mandates the use of a fairly simply form of Transmitter equalization called **de‐emphasis** to reduce the effects of signal distortion along the Link transmission line. This distortion problem is always present but gets worse with increased frequency and lossy transmission lines. 

## **The Problem** 

As data rates get higher, the Unit Interval (UI ‐ bit time) becomes smaller, with the result that it’s increasingly difficult to avoid having the value in one bit time affect the value in another bit time. The channel always resists changes to the voltage level, The faster we attempt to switch voltage, the more pronounced 
that effect becomes. However, when a signal has been held at the same voltage for several bit times, as when sending several bits in a row of the same polarity, the channel has more time to approach the target voltage. The resulting higher voltage makes it difficult to change to the opposite value within the required time when the polarity does change. This problem of previous bits affecting subsequent bits is referred to as **ISI** ( **inter‐symbol interference** ). 

## **How Does De-Emphasis Help?** 

De‐emphasis reduces the voltage for repeated bits in a bit stream. Although it sounds counter‐intuitive at first because this reduces the signal swing and thus the energy that reaches the Receiver, reducing the Transmitter voltage for these cases can substantially improve signal quality. Figure 13‐16 on page 469 illus‐ trates how this works by showing a Transmitter output of ‘1000010000’, where the repeated bits of the same polarity have been de‐emphasized. De‐emphasis can be thought of as a two‐tap Tx equalizer, and some rules related to it are:

</td>
<td style="background-color:#e8e8e8">

差分信号电压是通过取两条导线 D+ 和 D- 上的电压差来定义的。每条导线相对于地的电压为 VD+ 和 VD-。差分电压由 VDIFF = VD+ ‐ VD- 给出。共模电压 (Common Mode voltage, VCM) 定义为信号切换的电压范围，即由 VCM = (VD+ + VD-) / 2 给出的平均值。

规范在讨论差分电压时使用了两个术语，有时会引起混淆。如第 464 页图 13-13 所示，峰值 (Peak) 是信号之间的最大电压差，而峰峰值 (Peak‐to‐ Peak) 电压是该值加上相反方向上的最大值。对于对称信号，峰峰值仅为峰值的两倍。

1. 差分峰值电压 => VDIFFp = (max |VD+ ‐ VD-|)

2. 差分峰峰值电压 => VDIFFp‐p = 2 *(max |VD+ ‐ VD-|)

作为一个示例，假设 VCM = 0 V，则如果 D+ 值为 300mV 且 D- 值为 ‐300mV，则对于逻辑 1，VDIFFp 将为 300 ‐ (‐300) = 600 mV。类似地，对于逻辑 0，它将是 (‐300) ‐ (+300) = ‐600 mV。这种对称情况的 VDIFFp‐p 将为 1200 mV。在应用均衡之前，2.5 GT/s 和 5.0 GT/s 的允许 VDIFFp‐p 范围为 800 至 1200 mV，而 8.0 GT/s 的范围为 800 至 1300 mV。

**PCI Express 技术**

_图 13-13：差分峰峰值 ( VDIFFp‐p ) 和峰值 ( VDIFFp ) 电压_

**==> picture [327 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
D+<br>V VDIFFp VDIFFp<br>CMp (Logical 1) (Logical 0)<br>D-<br>0 V<br>VDIFFp-p = 2 * max | VD+ - VD- | = VDIFFp (Logical 1) + VDIFFp (Logical 0)<br>**----- End of picture text -----**


## **低摆幅差分电压**

对于长距离或其他有损的信道，需要满摆幅电压，并且要求发送器支持它。但是当信号环境短且低损耗时，不需要高压，并且可以通过降低电压来实现节能。考虑到这一点，2.5 GT/s 和 5.0 GT/s 的规范定义了另一种低摆幅电压，用于使用短信道且对功率敏感的系统。在这种模式下，电压降低到其满摆幅范围的大约一半。对该操作的支持是可选的，并且选择它的方式未定义，将特定于实现 (implementation specific)。

8.0 GT/s 信号传输也是如此，只是在这种情况下它是通过使用有限范围的系数来实现的。例如，低摆幅情况的最大提升限制为 3.5 dB。与较低数据速率一样，对该电压模型的支持是可选的，但现在实现它的方法很简单：只需设置 Tx 系数值即可实现。

值得注意的是，接收器电压电平与发送器无关，这符合我们的直觉：接收到的信号始终需要满足正常要求，因此发送器和信道必须设计为保证它能实现。

## **均衡电压**

为了在本节中保持良好的流程，此大主题在第 468 页的"信号补偿"部分单独介绍。

**第 13 章：物理层 - 电气**

## **电压裕量**

裕量 (margining) 的概念是可以在测试期间调整发送器特性（例如输出电压）跨越广泛的值范围，以确定它处理信号环境的能力。2.5 GT/s 速率不包括此功能，但电压裕量是在 5.0 GT/s 速率中添加的，并且必须由使用该速率或更高速率的发送器实现。其他参数（例如去加重 (de‐emphasis) 或抖动）也可以选择性地进行裕量测试。裕量调整的粒度必须在链路 (Link) 基础上可控，并且可以在 Lane 基础上可控。此控制通过 PCIe 能力 (Capability) 寄存器块中的链路控制 2 (Link Control 2) 寄存器来完成。发送裕量 (Transmit Margin) 字段如第 465 页图 13-14 所示，包含 3 位，因此可以表示 8 个级别。它们的值未定义，并且不需要全部实现。默认值为全零，表示正常工作范围。

重要的是要注意，此字段仅用于调试和合规测试，在这些期间软件才被允许修改它。在所有其他时间，值需要设置为全零的默认值。

_图 13-14：链路控制 2 寄存器中的发送裕量字段_

**==> picture [355 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 Register<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**


**PCI Express 技术**

对于 8.0 GT/s，发送器需要实现电压裕量并使用链路控制 2 (Link Control 2) 寄存器中的相同字段，但均衡 (equalization) 会对选项施加一些约束，因为它不能要求比正常操作定义的 1/24 分辨率更精细的系数或预设 (preset) 分辨率。

在 Tx 裕量测试期间，2.5 GT/s 和 5.0 GT/s 的均衡容差从 +/‐ 0.5 dB 放宽至 +/‐ 1.0 dB。对于 8.0 GT/s 速率，容差由系数粒度和为发送器指定的正常均衡器容差定义。

## **接收器 (Rx) 规范**

## **接收器阻抗**

除非设备断电（例如在 L2 和 L3 电源状态或基本复位 (Fundamental Reset) 期间），否则接收器需要满足 RLRX‐DIFF 和 RLRX‐CM（参见第 498 页表 13-5）参数。在这些情况下，接收器进入高阻抗状态，必须满足 ZRX‐HIGH‐IMP‐DC‐NEG 和 ZRX‐HIGH‐IMP‐DC‐NEG 参数。

（参见第 498 页表 13-5。）

## **接收器直流共模电压**

接收器的直流共模电压对于所有数据速率都规定为 0V，这在第 467 页图 13-15 中通过将信号端接连接到地来表示。CTX 内联电容器允许发送器处的该电压不同，规定范围为 0 至 3.6V。当发送器和接收器位于同一机箱内并具有相同电源时，这就不那么重要了，但如果它们通过电缆连接并位于具有不同电源的不同机器中，则变得更加重要。在这种情况下，很难避免机器之间的参考电压差异，并且由于信号电压已经很小，这样的差异可能会使信号难以在接收器处识别。当使用某种连接器时，此电容器的位置必须靠近发送器引脚，但是如果没有连接器，则可以将其放置在传输线上的任何方便位置。尽管它可以集成到设备中，但预期 CTX 将是外部的，因为将其集成会太大。

**第 13 章：物理层 - 电气**

第 467 页图 13-15 中的图还显示了接收器处的一组可选电阻器，标记为"No Spec"，因为规范中没有提到它们。这里的故事是，接收器设计人员不喜欢使用零共模电压，原因很简单，因为这通常要求他们实现两个参考电压，一个在零之上，一个在零之下。首选的实现方式是将信号完全偏移到零之上或之下，这样只需要一个参考电压。虚线内显示的电路通过添加一个小值内联电容器将线上信号的直流分量与接收器本身的直流分量解耦来实现这一点。然后，电阻梯形网络用于将接收器的共模电压偏移到一个方向或另一个方向以实现目标。

_图 13-15：接收器直流共模电压调整_

**==> picture [384 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
Small Big<br>Ratio of resistors<br>Big sets DC common<br>mode voltage<br>Small Big<br>Detect Big<br>Logic<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>No Spec<br>**----- End of picture text -----**


**PCI Express 技术**

## **传输损耗**

发送器驱动最小差分峰峰值电压 VTX‐DIFFp‐p 为 800 mV。接收器灵敏度设计为最小差分峰峰值电压 (VRX‐DIFFp‐p) 为 175 mV。这相当于链路设计为 13.2dB 的损耗预算。尽管板设计器可以确定针对各种频率绘制的链路的衰减损耗预算，但发送器和接收器眼图测量 (eye diagram measurement) 是链路损耗预算的最终决定因素。眼图在第 485 页的"眼图"中描述。驱动高达最大允许差分峰峰值电压 1200 mV 的发送器可以补偿具有最坏情况衰减特性的有损链路。

## **交流耦合**

PCI Express 要求在每个 Lane 上放置内联交流耦合电容器 (in‐line AC‐coupling capacitors)，通常靠近发送器。这些电容器可以集成在系统板上，或者集成到设备本身中，尽管它们需要的大尺寸使得这种情况不太可能发生。具有 PCI Express 设备的插卡必须在靠近发送器的卡上放置电容器，或将电容器集成到 PCIe 硅片中。这些电容器在链路两端的两个设备之间提供直流隔离，从而通过允许设备使用独立的电源和接地层来简化设备设计。

## **信号补偿**

## **与 Gen1 和 Gen2 PCIe 关联的去加重**

对于 2.5 GT/s 和 5.0 GT/s 传输，PCI 强制要求使用一种相当简单的发送器均衡形式，称为 **去加重 (de‐emphasis)**，以减少链路传输线上信号失真的影响。这种失真问题始终存在，但随着频率增加和传输线有损耗而变得更糟。

## **问题所在**

随着数据速率的提高，单位间隔 (Unit Interval, UI ‐ 比特时间) 变小，结果是越来越难以避免一个比特时间中的值影响另一个比特时间中的值。信道始终抵抗电压电平的变化，我们尝试切换电压的速度越快，

**第 13 章：物理层 - 电气**

这种效果就越明显。但是，当信号在多个比特时间内保持在相同电压时（例如在发送多个相同极性的连续位时），信道有更多时间接近目标电压。由此产生的较高电压使得在极性变化时难以在所需时间内改变为相反值。前面的位影响后续位的问题称为 **ISI** (**符号间干扰, inter‐symbol interference**)。

## **去加重如何提供帮助？**

去加重 (De‐emphasis) 降低了比特流中重复位的电压。乍一听这似乎违反直觉，因为这降低了信号摆幅，从而降低了到达接收器的能量，但降低这些情况下发送器电压可以显着提高信号质量。第 469 页图 13-16 通过显示发送器输出"1000010000"来说明此工作原理，其中相同极性的重复位已被去加重。去加重可以被认为是一个两抽头 (two‐tap) Tx 均衡器，并且与之相关的一些规则是：

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-11-4"></a>
## 11.4 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- When the signal changes to the opposite polarity of the preceding bit it’s not de‐emphasized, but uses the peak‐to‐peak differential voltage as specified by VTX‐DIFFp‐p (see Table 13‐3 on page 489). 

- The first bit of a series of same polarity bits is not de‐emphasized. 

- Only subsequent bits of the same polarity after the first bit are de‐empha‐ sized. 

- The de‐emphasized voltage is reduced by 3.5 dB from normal for 2.5 GT/s, which translates to about a one‐third reduction in voltage. 

- The Beacon signal is de‐emphasized, too, but uses slightly different rules. (see “Beacon Signaling” on page 483). 

_Figure 13‐16: Transmission with De‐emphasis_ 

**==> picture [377 x 159] intentionally omitted <==**

**----- Start of picture text -----**<br>
De-emphasized Voltage Level<br>1 0 0 0 0 1 0 0 0 0<br>1.3V<br>3.5 dB<br>1.225 D-<br>De-emphasized<br>VTX-DIFFp VTX-DIFFp VTX-CMp<br>=600mV =450mV =1 V<br>0.775 D+<br>3.5 dB<br>0.7 V<br>1 UI = 400 ps<br>**----- End of picture text -----**<br>


## **Solution for 2.5 GT/s** 

For 2.5 GT/s, each subsequent bit transmitted after the first bit of the same polarity must be de‐emphasized by 3.5dB to accommodate this worst‐case loss budget. Of course, for low‐loss environments this is less important and for a very short path it can even make the received signal look worse. After all, de‐ emphasis is essentially distorting the transmitted signal in the opposite way of the distortion that is expected during transmission so as to cancel it out. If there turns out to be little or no distortion, then de‐emphasis will make the signal look worse. The spec doesn’t describe any way to test the signal environment or adjust the de‐emphasis level, but doesn’t prohibit a designer from developing an implementation‐specific method of doing so. 

An example of the benefit of de‐emphasis is shown in Figure 13‐17 on page 471, which is a scope capture converted into a drawing for clarity. The captures were taken from a device driving a long path and using a bit stream with several repeated bits to show the signal distortion. The trace at the top shows that the bit pattern for one side of the differential pair (also called a single‐ended signal) has 2 bits of one polarity followed by 5 bits of the opposite polarity. Five consec‐ utive bits is the worst case for 8b/10b, and this particular pattern only appears in a few characters like the COM character. The channel resists high‐speed changes but will continue to charge up if the driver keeps trying to reach a higher voltage and that can be seen in this example. When the bits aren’t repeated there isn’t time for the voltage to go as far, but repeated bits give more time for the change. The problem this creates is seen in the bit following the 5[th] in a row (highlighted in the oval), which fails to reach a good signal value dur‐ ing its UI because the voltage difference was too large to overcome in that short time. The difference between the value it reaches and the value it should have reached is shown by the line marking the level reached by other bits that aren’t experiencing as much ISI. 

In the lower half of the illustration, a de‐emphasized version of the signal is cap‐ tured and compared to the original. Here we can see that reducing the voltage for repeated bits prevents the voltage from charging up as much and results in a cleaner signal because the bits that follow are not influenced as much by the previous bits. For both the 2 consecutive bits and then the 5 consecutive bits, the over‐charging problem is reduced, which improves the timing jitter as well as the voltage levels. Consequently, the troublesome bit looks much better with de‐ emphasis turned on and the received signal approaches the normal voltage swing in that bit time. 
_Figure 13‐17: Benefit of De‐emphasis at the Receiver_ 

**==> picture [358 x 283] intentionally omitted <==**

**----- Start of picture text -----**<br>
5 bits in a row<br>Without De [-] Emphasis<br>With De-Emphasis<br>**----- End of picture text -----**<br>


In Figure 13‐18 on page 472 both positive and negative versions of the differen‐ tial signal are shown so as to illustrate the resulting eye opening. The improved signal quality from de‐emphasis is clear because the eye opening at the trouble‐ some time in the lower trace is so much larger than the one without de‐empha‐ sis in the upper trace. 

_Figure 13‐18: Benefit of De‐emphasis at Receiver Shown With Differential Signals_ 

**==> picture [357 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Without De [-] Emphasis<br>With De-Emphasis<br>**----- End of picture text -----**<br>


## **Solution for 5.0 GT/s** 

As one might expect, increasing data rates exacerbates the problem of ISI because the bit times get progressively smaller, and more aggressive equaliza‐ tion techniques are needed. The change for 5.0 GT/s is incremental, and consists of providing three choices regarding the amount of de‐emphasis to be applied. 

1. When running at 2.5 GT/s speed, ‐3.5 dB de‐emphasis is required. 

2. When running at 5.0 GT/s speed, ‐6.0 dB de‐emphasis is recommended, while the use of ‐3.5 dB is optional. ‐6.0 dB de‐emphasis level is intended to compensate for the greater signal attenuation at higher frequency. As Fig‐ ure 13‐19 on page 473 suggests, a 3.5 dB reduction represents a 33% reduc‐ tion in voltage, while a 6 dB reduction represents a 50% reduction. To avoid a possible confusion, note that the dB measure of power and voltage are dif‐ ferent by a factor of two. A 3 dB reduction represents a 50% change in power but only a 25% change in voltage. 
_Figure 13‐19: De‐emphasis Options for 5.0 GT/s_ 

**==> picture [288 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
2.5 GT/s 3.5 dB<br>de-emphasis<br>5.0 GT/s 6.0 dB<br>de-emphasis<br>**----- End of picture text -----**<br>


3. Normally, a Transmitter operates in the full‐swing mode and can use the entire available voltage range to help overcome signal attenuation. The volt‐ age needs to start out at a higher value to compensate for the loss, as shown in the top half of Figure 13‐20 on page 474. However, for 5.0 GT/s another option is provided called reduced‐swing mode. This is intended to support short, low‐loss signaling environments, as shown in the lower half of Figure 13‐20 on page 474, and reduces the voltage swing by about half to save power. This mode also provides the third de‐emphasis option by turning off de‐emphasis entirely, which makes sense because, as mentioned earlier, the signal distortion it creates would not be reduced by loss in the path and the resulting signal at the Receiver would look worse. 

_Figure 13‐20: Reduced‐Swing Option for 5.0 GT/s with No De‐emphasis_ 

**==> picture [376 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Full Swing (high transmission amplitude)<br>Tx<br>Transmitter Receiver<br>Long path<br>Rx<br>+ +<br>_<br>_<br>Reduced Swing (low transmission amplitude)<br>Short path<br>Transmitter Receiver Tx<br>Rx<br>+ +<br>_<br>_<br>**----- End of picture text -----**<br>


## **Solution for 8.0 GT/s - Transmitter Equalization** 

When going to the 8.0 GT/s data rate, the signal conditioning model changes significantly. Transmitter equalization becomes more complex and a handshake training procedure is used to adapt to the actual signaling environment rather than making assumptions about what will be needed. To learn more about the process of evaluating the Link, refer to the section called “Recovery.Equaliza‐ tion” on page 587. Basically, that process allows a Receiver to request that the Link partner’s Transmitter use a certain combination of coefficients and then the receiver tests how well the received signal looks and possibly proposes others if the result isn’t good enough. 

Sometimes students ask whether this model is really sufficient to achieve good error rates, since evaluating a signal across all the possible situations requires days of testing in the lab to achieve a BER of 10[‐15] or better. The answer to this has two parts. First, even with the handshake process, the coefficients will be an approximation that worked well when the training was done but may or may not work as well under other conditions. Extrapolation from a small sample size 
is a necessary part of arriving at working values quickly and it works reason‐ ably well. Second, associated with 8 GT/s transfer rate, it’s only necessary to achieve a minimum BER of 10[‐12] , and that doesn’t take as long to verify as it would BER of 10[‐15] . 

## **Three-Tap Tx Equalizer Required** 

To accomplish better wave shaping at the Transmitter, the spec requires the use of a 3‐tap FIR (Finite Impulse Response) filter, meaning a filter with 3 bit‐time‐ spaced inputs. A conceptual drawing of this is shown in Figure 13‐21 on page 475, where it can be seen that the output voltage is the sum of three versions of the input: the original input, a version delayed by one bit time and a third delayed by another bit time. This type of FIR filter is often used in other SER‐ DES applications above 6.0 Gb/s, and it’s helpful for PCIe because it compen‐ sates for the fact that the channel spreads the signal across a longer time. Another way of thinking about it is that a given bit is affected by both the bit value that preceded it and the bit that comes after it. 

_Figure 13‐21: 3‐Tap Tx Equalizer_ 

**==> picture [371 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
� Output<br>Tap (-1) Tap (0) Tap (+1)<br>C C C<br>-1 0 +1<br>Input<br>1 UI delay 1 UI delay<br>**----- End of picture text -----**<br>


With this in mind, the three inputs can be described by their timing position as “pre‐cursor” for C‐1, “cursor” for C0, and “post‐cursor” for C+1, which combine to create an output based on the upcoming input, the current value, and the pre‐ vious value. Adjusting the coefficients for the taps allows the output wave to be optimally shaped. This effect is illustrated by the pulse‐response waveform shown in Figure 13‐22 on page 476. Looking at a single pulse allows the adjust‐ ment to the signal to be more easily recognized. 

The filter shapes the output according to the coefficient values (or tap weights) assigned to each tap. The sum of the absolute value of the three coefficient mag‐ nitudes together is defined to be unity so that only two of them need to be given for the third one to be calculated. Consequently, only C‐1 and C+1 are given in the spec and C0 is always implied and is always positive. 

_Figure 13‐22: Tx 3‐Tap Equalizer Shaping of an Output Pulse_ 

**==> picture [294 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
V<br>Unmodified Signal<br>t<br>UI UI UI UI<br>Cursor<br>V<br>Pre-cursor<br>Post-cursor<br>reduction<br>reduction<br>Equalized Signal<br>t<br>UI UI UI UI<br>Cursor<br>**----- End of picture text -----**<br>


## **Pre-shoot, De-emphasis, and Boost** 

The effect of the coefficient values is to adjust the output voltage to create up to four different voltage levels to accommodate different signaling environments, as shown in Figure 13‐23 on page 477. This waveform was taken from a test device and shows a representative example, but the voltage levels depend on whether a Transmitter implements preshoot or de‐emphasis or both. 

The waveform shows the four general voltages to be transmitted, which are: maximum‐height (Vd), normal (Va), de‐emphasized (Vb), and pre‐shoot (Vc). 
</td>
<td style="background-color:#e8e8e8">

## **发送器 (Tx) 规格**

## **低阻抗与高阻抗**

发送器提供低阻抗驱动或高阻抗驱动能力的选择。低阻抗选项通常提供更好的信号完整性，而高阻抗选项在低功耗状态下更有用。这两个选项之间的选择是实现特定的，规范允许这样做。

## **发送器预设**

对于 8.0 GT/s，引入了发送器预设的概念以简化均衡协商。预设是发送器系数的预定义集合，允许链路伙伴在训练期间请求特定的信号整形。规范定义了一组 11 个预设（P0 到 P10），每个都有不同的系数值，旨在应对各种通道条件。

预设的选择由接收器在链路训练和均衡协商期间请求。接收器测试信号质量并可以请求不同的预设，直到找到产生可接受信号的预设。

## **去加重水平**

对于 2.5 GT/s 和 5.0 GT/s，去加重水平是固定的（分别为 -3.5 dB 和 -6.0 dB）。对于 8.0 GT/s，去加重水平是发送器系数的一部分，可以通过均衡协商进行调整。

## **接收器 (Rx) 规格**

## **接收器灵敏度**

接收器灵敏度是指接收器可以正确检测的最小信号幅度。对于 PCIe，VRX-DIFFp-p 最小值为 175 mV，这意味着接收器必须能够正确检测低至 175 mV 的差分信号。

## **接收器阻抗**

接收器必须在通电时满足 RLRX-DIFF 和 RLRX-CM 参数，并在断电时满足 ZRX-HIGH-IMP-DC-NEG 和 ZRX-HIGH-IMP-DC-POS 参数。

## **抖动容差**

抖动容差是指接收器在存在抖动的情况下正确检测信号的能力。规范定义了多种抖动测量，包括确定性抖动、随机抖动和总体抖动。接收器必须能够在存在这些抖动类型的情况下正确解码信号。

## **回波损耗**

回波损耗衡量的是反射回信号源的能量量。接收器必须在指定频率范围内满足 RLRX-DIFF 和 RLRX-CM 参数。

## **通道**

## **概述**

通道是连接两个 PCIe 设备的物理介质。它可以包括印刷电路板走线、连接器、电缆和任何其他组件。通道的特性显著影响信号完整性，因此规范定义了各种通道参数以确保互操作性。

## **插入损耗**

插入损耗衡量的是信号通过通道时损失的信号能量量。规范定义了最大插入损耗预算，发送器和接收器必须在该预算内运行。

## **串扰**

串扰是指一个通道中的信号干扰另一个通道中的信号。规范定义了串扰要求以确保多个通道可以同时运行而不会显著降低信号质量。

## **传播延迟**

传播延迟是信号通过通道传播所需的时间。规范定义了最大传播延迟，链路训练必须考虑该延迟。

## **通道合规性**

为了确保互操作性，通道必须经过测试以验证其满足规范要求。通道合规性测试是 PCIe 合规性计划的一部分。

## **合规性和调试**

## **合规模式**

合规模式是一种特殊操作模式，允许测试设备验证 PCIe 设备的合规性。在合规模式下，设备发送合规模式信号，测试设备可以验证信号是否符合规范要求。

## **进入合规模式**

设备可以通过多种方式进入合规模式：

- 在链路训练期间通过设置 TS1 或 TS2 中的合规位

- 通过设置链路控制寄存器中的合规位

- 通过发送合规模式信号

## **合规模式信号**

合规模式信号是一组预定义的位模式，允许测试设备验证设备的合规性。规范定义了多种合规模式信号，每种都有特定的用途。

## **调试**

PCIe 提供多种调试功能，包括：

- 错误报告寄存器

- 链路训练状态机状态可见性

- 信号完整性测量

- 协议分析功能

## **总结**

本章介绍了 PCIe 物理层的电气特性，包括发送器和接收器规格、信号补偿和通道要求。理解这些电气特性对于设计可靠且合规的 PCIe 系统至关重要。

## **信标信号 (Beacon Signaling)**

## **概述**

信标信号是一种特殊的低频信号，用于在链路处于 L2 或 L3 低功耗状态时发出唤醒请求。信标使用与正常 PCIe 信号不同的信号模式，以便在主电源被移除时仍可以检测到。

## **信标信号要求**

信标信号必须满足以下要求：

- 使用差分信令，但具有不同的电压电平

- 以低频发送（30 kHz 到 500 MHz）

- 在 L2 和 L3 状态下发送

- 不需要参考时钟

## **信标信号检测**

接收器必须能够检测信标信号，即使在主电源被移除时也是如此。这通常使用辅助电源实现，该辅助电源为信标检测电路提供电源。

## **信标和唤醒**

当设备想要唤醒链路时，它会发送信标信号。接收到信标信号后，链路伙伴可以启动唤醒过程，将链路从 L2 或 L3 状态转换回 L0 状态。

## **唤醒过程**

唤醒过程涉及以下步骤：

1. 发送信标信号以请求唤醒

2. 接收器检测信标信号

3. 链路伙伴协商返回 L0 状态

4. 链路重新训练到所需的数据速率

5. 恢复正常操作

## **辅助电源**

辅助电源是为信标检测电路供电的电源，即使在主电源被移除时也是如此。辅助电源必须能够在主电源被移除时为信标检测电路提供足够的电源。

## **信标和合规性**

信标信号必须满足合规性要求，以确保不同供应商的设备可以互操作。规范定义了信标信号的合规性测试要求。

## **热插拔支持**

热插拔允许在系统通电时添加或移除 PCIe 设备。规范定义了支持热插拔所需的电气和逻辑要求。

## **热插拔要求**

热插拔支持需要以下功能：

- 存在检测

- 电源控制

- 链路训练协商

- 错误恢复

## **存在检测**

存在检测用于检测何时添加或移除卡。这通常通过在卡插槽中使用存在检测引脚来实现。

## **电源控制**

电源控制用于在添加或移除卡时控制卡的电源。这通常通过使用电源开关实现。

## **链路训练协商**

链路训练协商用于在添加或移除卡时协商链路参数。这确保了新添加的卡可以与系统正常通信。

## **错误恢复**

错误恢复用于处理热插拔事件期间的错误。这包括检测错误并采取适当的恢复操作。

## **总结**

本章介绍了 PCIe 物理层的各种电气特性，包括发送器、接收器、信号补偿、合规性和热插拔支持。理解这些特性对于设计可靠且合规的 PCIe 系统至关重要。

## **附录 A：术语表**

**AC 耦合 (AC Coupling)**：使用电容器阻断信号的 DC 分量，允许两个设备具有不同的 DC 共模电压。

**通道 (Lane)**：两个 PCIe 设备之间的单条单向差分信号路径。链路可以由多个通道组成（x1、x2、x4、x8、x16 等）。

**链路 (Link)**：两个 PCIe 设备之间的双向连接，由一个或多个通道组成。

**LTSSM (Link Training and Status State Machine)**：用于管理 PCIe 链路状态的状态机，包括 Detect、Polling、Configuration、L0、L0s、L1、L2、L3 和 Recovery 状态。

**均衡 (Equalization)**：用于补偿通道引入的信号失真的技术。PCIe 支持去加重（Gen1 和 Gen2）和三抽头 FIR 滤波（Gen3）。

**信标 (Beacon)**：在低功耗状态下使用的低频信号，用于发出唤醒请求。

**热插拔 (Hot Plug)**：在系统通电时添加或移除 PCIe 设备的能力。

**合规性 (Compliance)**：验证设备是否符合 PCIe 规范要求的过程。

**附录 B：参考规范**

- PCI Express Base Specification Revision 3.0

- PCI Express Card Electromechanical Specification Revision 3.0

- PCI Express Architecture PHY Test Specification Revision 3.0

**附录 C：缩略语**

- **BER**：Bit Error Rate（误码率）

- **CDR**：Clock and Data Recovery（时钟和数据恢复）

- **CRD**：Current Running Disparity（当前运行不一致性）

- **DPC**：Downstream Port Containment（下游端口遏制）

- **EIEOS**：Electrical Idle Exit Ordered Set（电气空闲退出有序集合）

- **EIOS**：Electrical Idle Ordered Set（电气空闲有序集合）

- **EMI**：Electro-Magnetic Interference（电磁干扰）

- **ESD**：Electro-Static Discharge（静电放电）

- **FTS**：Fast Training Sequence（快速训练序列）

- **ISI**：Inter-Symbol Interference（码间干扰）

- **LFSR**：Linear Feedback Shift Register（线性反馈移位寄存器）

- **LTSSM**：Link Training and Status State Machine（链路训练和状态状态机）

- **PLL**：Phase-Locked Loop（锁相环）

- **SOS**：Skip Ordered Set（Skip 有序集合）

- **SSC**：Spread Spectrum Clocking（扩频时钟）

- **TS1/TS2**：Training Sequence 1/2（训练序列 1/2）

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-11-5"></a>
## 11.5 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

This scheme is backward‐compatible with the 2.5 and 5.0 GT/s model that only uses de‐emphasis, because pre‐shoot and de‐emphasis can be defined indepen‐ dently. The voltages both with and without de‐emphasis are the same as they have been for the lower data rates, except that now there are more options for the de‐emphasis value, ranging from 0 to ‐6 dB. Preshoot is a new feature designed to improve the signal in the following bit time by boosting the voltage in the current bit time. Finally, the maximum value is simply what the signal would be if both C‐1 and C+1 were zero (and C0 was 1.0). As illustrated by the bit stream shown at the top of the diagram, we may summarize the strategy for these voltages as follows: 

- When the bits on both sides of the cursor have the opposite polarity, the voltage will be Vd, the maximum voltage. 

- When a repeated string of bits is to be sent: 

 - The first bit will use Va, the next lower voltage to the maximum voltage Vd. 

 - 

 - Bits between the first and last bits use Vb, the lowest voltage. 

- The last repeated bit before a polarity change uses Vc, the next higher voltage to the lowest voltage Vb. 

_Figure 13‐23: 8.0 GT/s Tx Voltage Levels_ 

**==> picture [366 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
 1 0 1 0 0 1 1 1 1 1 0 1 0 1 0 1<br>Va Vb Vc Vd<br>**----- End of picture text -----**<br>


## **Presets and Ratios** 

As described in “Recovery.Equalization” on page 587, when the Link is prepar‐ ing to change from a lower data rate to 8.0 GT/s, the Downstream Port sends EQ TS2s that give the Upstream Port a set of preset values to use for its coefficients as a starting point from which to begin testing the Link signal quality. The list of 11 possible presets along with their corresponding coefficient values and volt‐ age ratios is given in Table 13‐1 on page 478. Note that the voltages are given as a ratio with respect to the max value. These values were selected to match the earlier spec versions. As an example of how that is used, the first entry, P4, uses no de‐emphasis or preshoot, so all the voltage values are equal to the max value and the ratios are all 1.000. 

_Table 13‐1: Tx Preset Encodings with Coefficients and Voltage Ratios_ 

|**Preset**<br>**Number**|**Preshoot**<br>**(dB)**|**De-emphasis**<br>**(dB)**|**C-1**|**C+1**|**Va/Vd**|**Vb/Vd**|**Vc/Vd**|
|---|---|---|---|---|---|---|---|
|P4|0.0.|0.0|0.000|0.000|1.000|1.000|1.000|
|P1|0.0.|-3.5 +/- 1 dB|0.000|-0.167|1.000|0.668|0.668|
|P0|0.0.|-6.0 +/- 1.5 dB|0.000|-0.250|1.000|0.500|0.500|
|P9|3.5 +/- 1 dB|0.0|-0.166|0.000|0.668|0.668|1.000|
|P8|3.5 +/- 1 dB|-3.5 +/- 1 dB|-0.125|-0.125|0.750|0.500|0.750|
|P7|3.5 +/- 1 dB|-6.0 +/- 1.5 dB|-0.100|-0.200|0.800|0.400|0.600|
|P5|1.9 +/- 1 dB|0.0|-0.100|0.000|0.800|0.800|1.000|
|P6|2.5 +/- 1 dB|0.0|-0.125|0.000|0.750|0.750|1.000|
|P3|0.0|-2.5 +/- 1 dB|0.000|-0.125|1.000|0.750|0.750|
|P2|0.0|-4.4 +/- 1.5 dB|0.000|-0.200|1.000|0.600|0.600|
|P10|0.0|Defined by LF|0.000|(FS-LF) /2|1.000|Not<br>fixed|Not<br>fixed|


## **Equalizer Coefficients** 

Presets allow a device to use one of 11 possible starting values to be used for the partner’s Transmitter coefficients when first training to the 8.0 GT/s data rate. This is accomplished by sending EQ TS1s and EQ TS2s during training which gives a coarse adjustment of Tx equalization as a starting point. If the signal using the preset delivers the desired 10[‐12] error rate, no further training is needed. But if the measured error rate is too high, the equalization sequence is used to fine‐tune the coefficient settings by trying different C‐1 and C+1 values and evaluating the result, repeating the sequence until the desired signal qual‐ ity or error rate is achieved. 

An 8.0 GT/s transmitter is required to report its range of supported coefficient values to its neighboring Receiver. There are some constraints on this: 

- Device must support all 11 presets as listed in Table 13‐1 on page 478. 

- Transmitters must meet the full‐swing VTX‐EIEOS‐FS signaling limits 

- Transmitters may optionally support the reduced‐swing, and if they do they must meet the VTX‐EIEOS‐RS limits 

- Coefficients must meet the boost limits (VTX‐BOOST‐FS = 8.0 dB min, VTX‐ BOOST‐RS[ = 2.5 dB min) and resolution limits (EQ] TX‐DOEFF‐RESS[= 1/24 max to] 1/63 min). 

Applying these constraints and using the maximum granularity of 1/24 creates a list of pre‐shoot, de‐emphasis, and boost values for each setting. This is pre‐ sented in a table in the spec that is partially reproduced from the spec here in Table 13‐2 on page 480. The table contains blank entries because the boost value can’t exceed 8.0 +/‐ 1.5 dB = 9.5 dB. That results in a diagonal boundary where the boost has reached 9.5 for the full‐swing case. For reduced swing, the bound‐ ary is at 3.5 dB. The 6 shaded entries along the left and top edges of the table that go as far as 4/24 are presets supported by full‐ or reduced‐swing signaling. The other 4 shaded entries are presets supported for full‐swing signaling only. 

## **PCI Express Technology** 

_Table 13‐2: Tx Coefficient Table_ 

|**PS DE**<br>**Boost**|**PS DE**<br>**Boost**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|
|---|---|---|---|---|---|---|---|---|
|||0/24|1/24|2/24|3/24|4/24|5/24|6/24|
|**C-1**|0/24|0.0 0.0<br>0.0|0.0 -0.8<br>0.8|0.0 -1.8<br>1.6|0.0 -2.5<br>2.5|0.0 -3.5<br>3.5|0.0 -4.7<br>4.7|0.0 -6.0-<br>6.0|
||1/24|0.8 0.0<br>0.8|0.8 -0.8<br>1.6|0.9 -1.7<br>2.5|1.0 -2.8<br>3.5|1.2 -3.9<br>4.7|1.3 -5.3<br>6.0|1.6 -6.8<br>7.6|
||2/24|1.6 0.0<br>1.6|1.7 -0.9<br>2.5|1.9 -1.9<br>3.5|2.2 -3.1<br>4.7|2.5 -4.4<br>6.0|2.9 -6.0<br>7.6|3.5 -8.0<br>9.5|
||3/24|2.5 0.0<br>2.5|2.8 -1.0<br>3.5|3.1 -2.2<br>4.7|3.5 -3.5<br>6.0|4.1 -5.1<br>7.6|4.9 -7.0<br>9.5|-|
||4/24|3.5 0.0<br>3.5|3.9 -1.2<br>4.7|4.4 -2.5<br>6.0|5.1 -4.1<br>7.6|6.0 -6.0<br>9.5|-|-|
||5/24|4.7 0.0<br>4.7|5.3 -1.3<br>6.0|6.0 -2.9<br>7.6|7.0 -4.9<br>9.5|-|-|-|
||6/24|6.0 0.0<br>6.0|6.8 -1.6<br>7.6|8.0 -3.5<br>9.5|-|-|-|-|


**Coefficient Example.** Let’s drill a little deeper on the coefficients by using preset number P7 from Table 13‐1 on page 478 as an example. In this entry, C‐1 = ‐0.100, and C+1 = ‐0.200, and since C0 must be positive and the sum of their absolute values must be one, it’s implied that C0 = 0.700. 

Matching these values to the table of coefficient space given in the spec is not straightforward because the coefficients are given as fractions rather than decimal values, but converting the fractions to their decimal values matches them pretty closely. The C‐1 value of 0.100 is closest to 2/24 (0.083), while C+1 at 0.200 is a little less than 5/24 (0.208). The coefficient table entry for those fractions is highlighted as one of the preset values, giving us some confidence that this is on the right track. In the preset table, P7 lists a pre‐ shoot value of 3.5 +/‐ 1 dB, and the value in the coefficient table is shown as 2.9 dB. If we correct for the difference in coefficient values, ((0.083/.1) * 3.5 = 2.9) we arrive at the same preshoot value. The difference in coefficient val‐ ues for de‐emphasis was much smaller (0.200 vs. 0.208) and so, as we might expect, both tables show this as ‐6.0 dB. 
What voltages do the P7 coefficients create? Assuming a full‐swing voltage of Vd as a starting point then, according to the ratios in the preset table, the other voltages would be Va = 0.8Vd, Vb = 0.4Vd, and Vc = 0.6Vd. How well do those correspond to the values that would result from using the pre‐ shoot and de‐emphasis numbers? De‐emphasis was given as ‐6.0 dB, and we already know that represents a 50% voltage reduction, so we’d expect that Vb should be half of Va, which it is. Pre‐shoot was given as 3.5 dB meaning the ratio of Vc/Vb is 0.668, and 0.4/0.668 = 0.598Vd for Vc; very close to the 0.6Vd we expected. Last of all, the Boost value, which is the ratio of Vd/Vb, is not given in the preset table but, using the formula 20*log(Vd/ Vb), the boost from the preset values turns out to be 7.9 dB. That’s reason‐ ably close to the 7.6 dB value given in the coefficient table and gives us some confidence that the tables are consistent among themselves. 

So how are the four voltages obtained? There are essentially three program‐ mable drivers whose output is summed to derive the final signal value to be launched. If the cursor setting remains unchanged, and the pre‐ and post‐ cursor taps are negative, then the answer can be found by simply adding the taps as (C0 + C‐1 + C+1). 

- Vd = (C0 + C‐1 + C+1) = (0.700 + 0.100 + 0.200) = 1.0 * max voltage. This is the “boosted” value that results when a bit is both preceded and fol‐ lowed by bits of the opposite polarity. In all four voltages listed here, if the polarity of the bits is inverted then the values would all be negative. 

- — Va = (0.700 + (‐0.100) + 0.200) = 0.8 * max voltage. This is the value that results when a bit is preceded by the opposite polarity but followed by the same polarity, meaning it is the first in a repeated string of bits. 

- Vb = (0.700 + (‐0.100) + (‐0.200)) = 0.4 * max voltage. This is the de‐ emphasized value that results when a bit is both preceded and followed by bits of the same polarity, meaning it’s in the middle of a repeated string of bits. 

- Vc = (0.700 + 0.100 + (‐0.200)) = 0.6 * max voltage. This is the pre‐shoot value that results when a bit is preceded by the same polarity but fol‐ lowed by the opposite polarity, meaning it’s the last bit in a repeated string of bits. 

What determines when the coefficients are added or subtracted to arrive at these numbers? This turns out to be fairly simple, since it’s just a matter of the polarity of the time‐shifted pre‐ and post‐cursor inputs. This is illus‐ trated in Figure 13‐24 on page 482. The single‐ended waveform labeled “Weighted Cursor (C0)” shows the positive half of the differential bit stream currently being transmitted. If the waveforms are understood as shifting to the right with time, then the next lower trace (C+1) is the post‐cursor signal. 

## **PCI Express Technology** 

This version arrives one clock later and is weighted negatively by its coeffi‐ cient, causing it to be inverted. The top trace (C‐1) arrives a clock earlier than the cursor and is the pre‐cursor value that is also weighted negatively according to its own coefficient. 

Finally, the bottom trace shows the result of summing all three inputs to arrive at the final signal that is actually launched onto the wire. In the illus‐ tration, this is overlaid with the single‐ended output waveform from Figure 13‐23 on page 477 to show that it approximates a real capture fairly well. Some voltage calculations are shown from our previous example to demon‐ strate how the resulting voltages are obtained. 

_Figure 13‐24: Tx 3‐Tap Equalizer Output_ 

**==> picture [383 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
Weighted<br>Pre-Cursor<br>(C-1)<br>Weighted 1 0 1 0 0 1 1 1 1 1 0<br>Cursor (C0)<br>Weighted<br>Post-Cursor<br>(C+1)<br>Vd (0.7 + (-0.1) + (-0.2))<br>= 0.4<br>Vc<br>Va<br>Vb<br>Output<br>(C0 + C-1 + C+1) Vc<br>Va<br>Vd (-0.7 + (-0.1) + (0.2)) Vd<br>= - 0.6<br>(-0.7 + (0.1) + (-0.2))<br>(-0.7 + (-0.1) + (-0.2)) = - 0.8<br>= -1.0<br>**----- End of picture text -----**<br>

The coefficient presets are exchanged before the Link changes to 8.0 GT/s, and then they may be updated during the Link equalization process (see “Recovery.Equalization” on page 587 for more details).

</td>
<td style="background-color:#e8e8e8">

该方案向后兼容仅使用去加重 (de‐emphasis) 的 2.5 和 5.0 GT/s 模型，因为预冲 (pre‐shoot) 和去加重可以独立定义。无论是否使用去加重，电压都与较低数据速率下的电压相同，只是现在去加重值的选项更多，范围从 0 到 ‐6 dB。预冲是一项新特性，旨在通过在当前位时间内提升电压来改善下一位时间的信号。最后，最大值简单地表示当 C‐1 和 C+1 都为零（且 C0 为 1.0）时的信号。如图顶部所示的位流所示，我们可以将这些电压的策略总结如下：

- 当游标两侧的位具有相反极性时，电压将是 Vd，即最大电压。

- 当要发送重复的位串时：

 - 第一位使用 Va，即低于最大电压 Vd 的次低电压。

 -

 - 第一位与最后一位之间的位使用 Vb，即最低电压。

- 极性变化之前的最后一个重复位使用 Vc，即高于最低电压 Vb 的次高电压。

_图 13‐23：8.0 GT/s 发送器电压电平_

**==> picture [366 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
 1 0 1 0 0 1 1 1 1 1 0 1 0 1 0 1<br>Va Vb Vc Vd<br>**----- End of picture text -----**<br>


## **预设和比率**

如第 587 页 “Recovery.Equalization” 中所述，当链路准备从较低的数据速率更改为 8.0 GT/s 时，下游端口发送 EQ TS2，向上游端口提供一组预设值用作其系数的起点，并从此开始测试链路信号质量。11 个可能预设的列表及其对应的系数值和电压比率见表 13‐1（第 478 页）。请注意，电压以相对于最大值的比率给出。这些值的选择是为了与早期规范版本匹配。作为示例，第一个条目 P4 不使用去加重或预冲，因此所有电压值都等于最大值，比率均为 1.000。

_表 13‐1：发送器预设编码与系数及电压比率_

|**预设**<br>**编号**|**预冲**<br>**(dB)**|**去加重**<br>**(dB)**|**C-1**|**C+1**|**Va/Vd**|**Vb/Vd**|**Vc/Vd**|
|---|---|---|---|---|---|---|---|
|P4|0.0.|0.0|0.000|0.000|1.000|1.000|1.000|
|P1|0.0.|-3.5 +/- 1 dB|0.000|-0.167|1.000|0.668|0.668|
|P0|0.0.|-6.0 +/- 1.5 dB|0.000|-0.250|1.000|0.500|0.500|
|P9|3.5 +/- 1 dB|0.0|-0.166|0.000|0.668|0.668|1.000|
|P8|3.5 +/- 1 dB|-3.5 +/- 1 dB|-0.125|-0.125|0.750|0.500|0.750|
|P7|3.5 +/- 1 dB|-6.0 +/- 1.5 dB|-0.100|-0.200|0.800|0.400|0.600|
|P5|1.9 +/- 1 dB|0.0|-0.100|0.000|0.800|0.800|1.000|
|P6|2.5 +/- 1 dB|0.0|-0.125|0.000|0.750|0.750|1.000|
|P3|0.0|-2.5 +/- 1 dB|0.000|-0.125|1.000|0.750|0.750|
|P2|0.0|-4.4 +/- 1.5 dB|0.000|-0.200|1.000|0.600|0.600|
|P10|0.0|由 LF 定义|0.000|(FS-LF) /2|1.000|不固定|不固定|


**第 13 章：物理层 - 电气**

## **均衡器系数**

预设允许设备在首次训练到 8.0 GT/s 数据速率时使用 11 个可能的起始值之一作为合作伙伴发送器系数的初始值。这是通过在训练期间发送 EQ TS1 和 EQ TS2 来实现的，为发送器均衡提供一个粗略调整的起点。如果使用预设的信号能够达到所需的 10[‐12] 误码率，则无需进一步训练。但如果测得的误码率过高，则使用均衡序列通过尝试不同的 C‐1 和 C+1 值并评估结果来微调系数设置，重复该序列直到达到所需的信号质量或误码率。

8.0 GT/s 发送器需要向其相邻的接收器报告其支持的系数值范围。对此有一些约束：

- 设备必须支持表 13‐1（第 478 页）中列出的所有 11 个预设。

- 发送器必须满足满摆幅 VTX‐EIEOS‐FS 信号限制

- 发送器可以选择支持缩减摆幅，如果支持，则必须满足 VTX‐EIEOS‐RS 限制

- 系数必须满足提升限制 (VTX‐BOOST‐FS = 最小 8.0 dB, VTX‐BOOST‐RS = 最小 2.5 dB) 和分辨率限制 (EQ_TX‐DOEFF‐RES 最大为 1/24，最小为 1/63)。

应用这些约束并使用最大粒度 1/24，可为每个设置生成预冲、去加重和提升值的列表。该列表在规范的表格中给出，此处从规范中部分转载到表 13‐2（第 480 页）。表中包含空白条目，因为提升值不能超过 8.0 +/‐ 1.5 dB = 9.5 dB。结果在满摆幅情况下形成一条对角边界，提升已达到 9.5 dB。对于缩减摆幅，边界在 3.5 dB 处。表中左侧和顶部边缘的 6 个阴影条目，最远可达 4/24，是由满摆幅或缩减摆幅信号支持的预设。其他 4 个阴影条目仅为满摆幅信号支持的预设。

## **PCI Express Technology**

_表 13‐2：发送器系数表_

|**PS DE**<br>**Boost**|**PS DE**<br>**Boost**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|
|---|---|---|---|---|---|---|---|---|
|||0/24|1/24|2/24|3/24|4/24|5/24|6/24|
|**C-1**|0/24|0.0 0.0<br>0.0|0.0 -0.8<br>0.8|0.0 -1.8<br>1.6|0.0 -2.5<br>2.5|0.0 -3.5<br>3.5|0.0 -4.7<br>4.7|0.0 -6.0-<br>6.0|
||1/24|0.8 0.0<br>0.8|0.8 -0.8<br>1.6|0.9 -1.7<br>2.5|1.0 -2.8<br>3.5|1.2 -3.9<br>4.7|1.3 -5.3<br>6.0|1.6 -6.8<br>7.6|
||2/24|1.6 0.0<br>1.6|1.7 -0.9<br>2.5|1.9 -1.9<br>3.5|2.2 -3.1<br>4.7|2.5 -4.4<br>6.0|2.9 -6.0<br>7.6|3.5 -8.0<br>9.5|
||3/24|2.5 0.0<br>2.5|2.8 -1.0<br>3.5|3.1 -2.2<br>4.7|3.5 -3.5<br>6.0|4.1 -5.1<br>7.6|4.9 -7.0<br>9.5|-|
||4/24|3.5 0.0<br>3.5|3.9 -1.2<br>4.7|4.4 -2.5<br>6.0|5.1 -4.1<br>7.6|6.0 -6.0<br>9.5|-|-|
||5/24|4.7 0.0<br>4.7|5.3 -1.3<br>6.0|6.0 -2.9<br>7.6|7.0 -4.9<br>9.5|-|-|-|
||6/24|6.0 0.0<br>6.0|6.8 -1.6<br>7.6|8.0 -3.5<br>9.5|-|-|-|-|


**系数示例。** 让我们使用第 478 页表 13‐1 中的预设 P7 作为示例，深入了解这些系数。在此条目中，C‐1 = ‐0.100，C+1 = ‐0.200，由于 C0 必须为正且它们绝对值之和必须为 1，因此 C0 = 0.700。

将这些值与规范中给出的系数空间表进行匹配并不直观，因为系数以分数形式而非十进制值给出，但将分数转换为十进制值后可以非常接近地匹配。C‐1 值 0.100 最接近 2/24（0.083），而 C+1 值 0.200 略小于 5/24（0.208）。这些分数对应的系数表条目作为预设值之一被突出显示，让我们对此充满信心。在预设表中，P7 列出的预冲值为 3.5 +/‐ 1 dB，系数表中显示的值为 2.9 dB。如果我们根据系数值的差异进行修正，((0.083/.1) * 3.5 = 2.9)，即可得到相同的预冲值。去加重的系数值差异较小（0.200 vs. 0.208），所以正如预期，两个表都将其显示为 ‐6.0 dB。

**第 13 章：物理层 - 电气**

P7 系数会产生什么电压？假设以满摆幅电压 Vd 作为起点，根据预设表中的比率，其他电压将为 Va = 0.8Vd、Vb = 0.4Vd 和 Vc = 0.6Vd。这些值与使用预冲和去加重数值得到的结果对应得有多好？去加重被指定为 ‐6.0 dB，我们已知这表示电压降低 50%，因此我们期望 Vb 应为 Va 的一半，确实如此。预冲被指定为 3.5 dB，意味着 Vc/Vb 的比率为 0.668，0.4/0.668 = 0.598Vd，即 Vc；非常接近我们预期的 0.6Vd。最后，提升值即 Vd/Vb 的比率，未在预设表中给出，但使用公式 20*log(Vd/Vb)，从预设值得出的提升值为 7.9 dB。这与系数表中给出的 7.6 dB 值相当接近，让我们确信这些表之间是一致的。

那么这四个电压是如何获得的呢？基本上有三个可编程驱动器，其输出被求和以推导出最终要发送的信号值。如果游标设置保持不变，且预游标和后游标抽头为负，则答案可通过简单地将抽头相加 (C0 + C‐1 + C+1) 来获得。

- Vd = (C0 + C‐1 + C+1) = (0.700 + 0.100 + 0.200) = 1.0 * 最大电压。这是一个"提升"值，当一个位前后的位均为相反极性时产生。在此处列出的所有四个电压中，如果位的极性反转，则所有值都为负。

- Va = (0.700 + (‐0.100) + 0.200) = 0.8 * 最大电压。这是当一个位前面是相反极性、后面是相同极性时的值，表示它是重复位串中的第一位。

- Vb = (0.700 + (‐0.100) + (‐0.200)) = 0.4 * 最大电压。这是去加重值，当一个位前后均为相同极性时产生，表示它位于重复位串的中间。

- Vc = (0.700 + 0.100 + (‐0.200)) = 0.6 * 最大电压。这是预冲值，当一个位前面是相同极性、后面是相反极性时产生，表示它是重复位串中的最后一位。

什么决定了系数何时相加或相减以得出这些数值？结果相当简单，因为这仅仅是时移预游标和后游标输入的极性问题。这在第 482 页的图 13‐24 中说明。标记为"Weighted Cursor (C0)"的单端波形显示了当前正在发送的差分位流的正半部分。如果将波形理解为随时间向右移动，则下一条较低的波形（C+1）是后游标信号。

## **PCI Express Technology**

该版本晚一个时钟到达，并通过其系数进行负加权，导致其反相。顶部波形（C‐1）比游标早一个时钟到达，是预游标值，也根据其自身的系数进行负加权。

最后，底部波形显示了对所有三个输入求和的结果，以得出实际发送到线路上的最终信号。在该图中，此波形与第 477 页图 13‐23 中的单端输出波形叠加显示，以表明它与实际捕获非常接近。图中显示了之前示例的一些电压计算，以演示如何得出所得电压。

_图 13‐24：发送器 3 抽头均衡器输出_

**==> picture [383 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
Weighted<br>Pre-Cursor<br>(C-1)<br>Weighted 1 0 1 0 0 1 1 1 1 1 0<br>Cursor (C0)<br>Weighted<br>Post-Cursor<br>(C+1)<br>Vd (0.7 + (-0.1) + (-0.2))<br>= 0.4<br>Vc<br>Va<br>Vb<br>Output<br>(C0 + C-1 + C+1) Vc<br>Va<br>Vd (-0.7 + (-0.1) + (0.2)) Vd<br>= - 0.6<br>(-0.7 + (0.1) + (-0.2))<br>(-0.7 + (-0.1) + (-0.2)) = - 0.8<br>= -1.0<br>**----- End of picture text -----**<br>


**第 13 章：物理层 - 电气**

系数预设在链路更改为 8.0 GT/s 之前交换，然后在链路均衡过程中可能会更新（有关更多详细信息，请参阅第 587 页 "Recovery.Equalization"）。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-11-6"></a>
## 11.6 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**EIEOS Pattern.** At 8.0 GT/s, some voltages are measured when the signal has a low frequency because the high‐frequency changes won’t reach the levels we want to measure. The EIEOS sequence contains 8 consecutive ones followed by 8 consecutive zeros in a pattern that repeats for 128 bit times. Its purpose is primarily to serve as an unambiguous indication that a Transmitter is exiting from Electrical Idle, which scrambled data can’t guar‐ antee. Its launch voltage is defined as VTX‐EIEOS‐FS for full swing and VTX‐ EIEOS‐RS[for reduced swing signals.] 

**Reduced Swing.** Transmitters may support a reduced swing signal much as they did for 5.0 GT/s: to achieve both power savings and a better signal over short, low‐loss transmission paths. The output voltage has the same 1300 mV max value as the full‐swing case, but allows a lower minimum voltage of 232 mV as defined for VTX‐EIEOS‐RS. Operating at reduced swing limits the number of presets because the maximum boost supported is 3.5 dB. 

## **Beacon Signaling** 

## **General** 

De‐emphasis is also applied to the Beacon signal, so a discussion about the Bea‐ con is included in this section. A device whose Link is in the L2 state can gener‐ ate a wake‐up event to request that power be restored so it can communicate with the system. The Beacon is one of two methods available for this purpose. The other method is to assert the optional sideband WAKE# signal. An example of what the Beacon might look like is shown in Figure 13‐25 on page 484. This version shows the differential signals pulsing and then decaying in opposite directions and is reminiscent of a flashing beacon light. Other options are avail‐ able for the Beacon, but this one illustrates the concept well. 

_Figure 13‐25: Example Beacon Signal_ 

**==> picture [262 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
V<br>t<br>**----- End of picture text -----**<br>


While a Link is in L2 power state, its main power source and clock are turned off but an auxiliary voltage source (Vaux) keeps a small part of the device work‐ ing, including the wake‐up logic. To signal a wake‐up event, a downstream device can drive the Beacon upstream to start the L2 exit sequence. A switch or bridge receiving a Beacon on its Downstream Port must forward notification upstream by sending the Beacon on its Upstream Port or by asserting the WAKE# pin. See “WAKE#” on page 773. 

The motivation for creating two wake‐up mechanisms is to provide choices regarding power consumption. To use the Beacon, all the bridges and switches between an Endpoint and the Root Complex will need to use Vaux so they can detect and generate the signal. If a system is always plugged in and uncon‐ cerned about the amount of standby power, the Beacon in‐band signal may be preferred over having to route an extra side‐band signal. But in a mobile system with limited battery life where conserving power is a high priority, the WAKE# pin is preferred because that approach uses as little Vaux as possible. The pin could be connected directly from the Endpoint to the Root Complex and then no other devices would need to be involved or use Vaux. 

## **Properties of the Beacon Signal** 

- A low‐frequency, DC‐balanced differential signal consisting of a periodic pulse of between 2ns and 16  s. 

- The maximum time between pulses can be no more than 16  s. 

- The transmitted Beacon signal must meet the electrical voltage specs docu‐ mented in Table 13‐3 on page 489. 
- The signal must be DC balanced within a maximum time of 32  s. 

- Beacon signaling, like normal differential signaling, must be done with the Transmitter in the low impedance mode (50  single‐ended, 100  differen‐ tial impedance). 

- When signaled, the Beacon signal must be transmitted on Lane 0, but does not have to be transmitted on other Lanes. 

- With one exception, the transmitted Beacon signal must be de‐emphasized according to the rules defined in the previous section. For Beacon pulses greater than 500ns, the Beacon signal voltage must be 6db de‐emphasized from the VTX‐DIFFp‐p spec. The Beacon signal voltage may be de‐empha‐ sized by up to 3.5dB for Beacon pulses smaller than 500ns. 

## **Eye Diagram** 

## **Jitter, Noise, and Signal Attenuation** 

As the bit stream travels from the Transmitter on one end of a link to the Receiver on the other end, it is subject to the following disruptive influences: 

- Deterministic (i.e., predictable) jitter induced by the Link transmission line. 

- Data‐dependent jitter induced by the dynamic data patterns on the Link. 

- Noise induced into the signal pair. 

- Signal attentuation due to the impedance effect of the transmission line. 

## **The Eye Test** 

To verify that a Receiver sees an signal that is within the allowed variation, an eye test may be performed. The following description of this measurement was provided by James Edwards from an article he authored for _OE Magazine_ . 

_“The most common time‐domain measurement for a transmission system is the eye diagram. The eye diagram is a plot of data points repetitively sampled from a pseudo‐random bit sequence and displayed by an oscilloscope. The time window of observation is two data periods wide. For a [PCI Express link running at 2.5 GT/s], the period is 400ps, and the time window is set to 800ps. The oscilloscope sweep is triggered by every data clock pulse. An eye diagram allows the user to observe sys‐ tem performance on a single plot._ 

_To observe every possible data combination, the oscilloscope must operate like a multiple‐exposure camera. The digital oscilloscopeʹs display persistence is set to infinite. With each clock trigger, a new waveform is measured and overlaid upon all_ 

_previous measured waveforms. To enhance the interpretation of the composite image, digital oscilloscopes can assign different colors to convey information on the number of occurrences of the waveforms that occupy the same pixel on the display, a process known as color‐grading. Modern digital sampling oscilloscopes include the ability to make a large number of automated measurements to fully characterize the various eye parameters.“_ 

## **Normal Eye Diagram** 

An ideal trace capture would paint an eye pattern that matched the outline shown in the center of Figure 13‐26 on page 486 labeled “Normal”. As long as the pattern resides entirely within that region, the Transmitter and Link are within tolerance. Note that the differential voltage parameters and values shown are peak voltages instead of the peak‐to‐peak voltages used in the spec, because only peak voltages can be represented in an eye diagram. Figure 13‐27 on page 488 shows a screen capture of a good eye diagram. 

_Figure 13‐26: Transmitter Eye Diagram_ 

**==> picture [354 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Overshoot<br>Normal<br>Minimum Eye<br>De-emphasized Eye<br>Eye Opening<br>Normal<br>Undershoot<br>Jitter Jitter<br>TTX-EYE<br>UI = Unit Interval<br>TX-DIFF-p-MAX TX-DIFFp-MIN<br>V V<br>**----- End of picture text -----**<br>

## **Effects of Jitter** 

Jitter (timing uncertainty) is what happens when an edge arrives either before or after its ideal time, and acts to reduce signal integrity and close the eye open‐ ing. It’s caused by a variety of factors, from environmental effects to the data pattern in flight, to noise or signal attenuation that causes the signal’s voltage level to overshoot or undershoot the normal zone. At 2.5 GT/s this could be treated as a simple lumped effect, but at higher data rates it becomes a more sig‐ nificant issue and must be considered in several different parts. Aiming at this goal, the 8.0 GT/s data rate defines 5 different jitter values. The details of jitter analysis and minimization are beyond the scope of this book, but let’s at least define the terms the spec uses. Jitter is described as being in one of several cate‐ gories: 

1. Un‐correlated ‐ jitter that is not dependent on, or “correlated” to, the data pattern being transmitted. 

2. Rj ‐ Random jitter from unpredictable sources that are unbounded and usu‐ ally assumed to fit a Gaussian distribution. Often caused by electrical or thermal noise in the system. 

3. Dj ‐ Deterministic jitter that’s predictable and bounded in its peak‐to‐peak value. Often caused by EMI, crosstalk, power supply noise or grounding problems. 

4. PWJ ‐ Pulse Width Jitter ‐ uncorrelated, edge‐to‐edge, high‐frequency jitter. 5. DjDD ‐ Deterministic Jitter, using the Dual‐Dirac approximation. This model is a method of quickly estimating total jitter for a low BER without requiring the large sample size that would normally be needed. It uses a representative sample taken over a relatively short period (an hour or so) and extrapolates the curves to arrive at acceptable approximate values. 

6. DDj ‐ Data‐dependent jitter is a function of the data pattern being sent, and the spec states that this is mostly due to package loss and reflection. ISI is an example of DDj. 

Figure 13‐28 on page 488 shows a screen capture of a bad Eye Diagram at 2.5 GT/s. Since this is captured without de‐emphasis, the traces should all stay out‐ side the Minimum Eye area, shown on the screen by the trapezoid shape in the middle. This example illustrates that jitter can affect both edge arrival times and voltage levels, causing some trace instances to encroach on the keep‐out area of the diagram. 

## **PCI Express Technology** 

_Figure 13‐27: Rx Normal Eye (No De‐emphasis)_ 

_Figure 13‐28: Rx Bad Eye (No De‐emphasis)_ 
## **Transmitter Driver Characteristics** 

Table 13‐3 on this page lists some Transmitter driver characteristics. This is not intended to replicate the tables from the spec, but to give some basic parameters to illustrate some differences between the data rates, such as UI, and to show that some things have remained unchanged, such as the Tx common‐mode volt‐ age. 

_Table 13‐3: Transmitter Specs_ 

|**Item**|**2.5 GT/s.**|**5.0 GT/s**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|UI|399.88<br>(min)<br>400.12<br>(max)|199.94<br>(min)<br>200.06<br>(max)|124.9625<br>(min)<br>125.0375<br>(max)|ps|Unit Interval (bit time)|
|TTX‐EYE|0.75<br>(min)|0.75 (min)|See notes|UI|Transmitter Eye, includ‐<br>ing all jitter sources.<br>For 8.0 GT/s, five jitter<br>sources are specified sep‐<br>arately.|
|TTX‐RF‐MIS‐<br>MATCH|Not<br>Specified|0.1 (max)|Not<br>Specified|UI|Rise and Fall time differ‐<br>ence measured from 20%<br>to 80% differentially.|
|VTX‐DIFFp‐p|0.8 (min)<br>1.2 (max)|0.8 (min)<br>1.2 (max)|See Table<br>13‐4|mV|Peak‐to‐peak differential<br>voltage.|
|VTX‐DIFFp‐p<br>LOW|0.4 (min)<br>1.2 (max)|0.4 (min)<br>1.2 (max)|See Table<br>13‐4|mV|Low‐power voltage.|
|VTX‐DC‐CM|0 to 3.6|0 to 3.6|0 to 3.6|V|DC common mode volt‐<br>age at Tx pins.|
|VTX‐DE‐<br>RATIO‐3.5dB|3 (min)<br>4 (max)|3 (min)<br>4 (max)|See Table<br>13‐4|mV|Ratio for 3.5 dB de‐<br>emphasized bits.|
|VTX‐DE‐<br>RATIO‐6dB|n/a|5.5 (min)<br>6.5 (max)|See Table<br>13‐4|mV|Ratio for 6 dB de‐empha‐<br>sized bits.|


## **PCI Express Technology** 

_Table 13‐3: Transmitter Specs (Continued)_ 

|**Item**|**2.5 GT/s.**|**5.0 GT/s**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|ITX‐SHORT|90|90|90|mA|Total single‐ended cur‐<br>rent Tx can supply when<br>shorted to ground.|
|VTX‐IDLE‐<br>DIFF‐AC‐P|0 (min)<br>20 (max)|0 (min)<br>20 (max)|0 (min)<br>20 (max)|mV|Peak differential voltage<br>under Electrical Idle state<br>of Link. Must include a<br>bandpass filter passing<br>frequencies from 10 KHz<br>to 1.25 GHz.|

</td>
<td style="background-color:#e8e8e8">

**EIEOS 模式。** 在 8.0 GT/s 时，由于高频变化无法达到我们想要测量的电平，因此在信号为低频时测量一些电压。EIEOS 序列包含 8 个连续的 1 后跟 8 个连续的 0，以在 128 位时间内重复的模式。其主要目的是用作发送器退出电气空闲 (Electrical Idle) 的明确指示，而加扰数据无法保证这一点。其启动电压对满摆幅定义为 VTX‐EIEOS‐FS，对缩减摆幅信号定义为 VTX‐EIEOS‐RS。

**缩减摆幅。** 发送器可以像 5.0 GT/s 时那样支持缩减摆幅信号：以实现节能并获得短距离、低损耗传输路径上的更好信号。输出电压具有与满摆幅情况相同的最大 1300 mV 值，但允许较低的最小电压 232 mV，如 VTX‐EIEOS‐RS 所定义。在缩减摆幅下运行时，由于支持的最大提升为 3.5 dB，因此会限制预设的数量。

## **信标信号**

## **概述**

去加重也应用于信标 (Beacon) 信号，因此本节包含了关于信标的讨论。链路处于 L2 状态的设备可以生成唤醒事件，以请求恢复电源以便与系统通信。信标是用于此目的的两种方法之一。另一种方法是断言可选的边带 WAKE# 信号。图 13‐25（第 484 页）显示了信标可能外观的示例。该版本显示差分信号脉冲然后以相反方向衰减，让人联想到闪烁的信标灯。信标还有其他可用选项，但这个示例很好地说明了概念。

_图 13‐25：信标信号示例_

**==> picture [262 x 151] intentionally omitted <==**

**----- Start of picture text -----**<br>
V<br>t<br>**----- End of picture text -----**<br>


当链路处于 L2 电源状态时，其主电源和时钟被关闭，但辅助电压源 (Vaux) 保持设备的一小部分继续工作，包括唤醒逻辑。为了发出唤醒事件，下游设备可以向上游驱动信标以启动 L2 退出序列。在下游端口上接收到信标的交换机或桥必须通过在上游端口上发送信标或断言 WAKE# 引脚来将通知向上游转发。参见第 773 页 "WAKE#"。

创建两种唤醒机制的动机是为了在功耗方面提供选择。要使用信标，端点和根复合体之间的所有桥和交换机将需要使用 Vaux，以便它们能够检测和生成该信号。如果系统始终插入电源且不关心待机功耗的大小，则信标带内信号可能优于不得不路由额外的边带信号。但在电池寿命有限的移动系统中，节能是首要任务，则首选 WAKE# 引脚，因为该方法使用尽可能少的 Vaux。该引脚可以直接从端点连接到根复合体，那么不需要涉及其他设备或使用 Vaux。

## **信标信号属性**

- 一个低频、直流平衡的差分信号，由 2ns 到 16μs 之间的周期性脉冲组成。

- 脉冲之间的最大时间不能超过 16μs。

- 发送的信标信号必须满足第 489 页表 13‐3 中记录的电气电压规格。

**第 13 章：物理层 - 电气**

- 信号必须在最长 32μs 时间内直流平衡。

- 与普通差分信令一样，信标信令必须使用发送器处于低阻抗模式（单端 50Ω，差分 100Ω 阻抗）完成。

- 信标信号必须在 Lane 0 上发送，但不必在其他 Lane 上发送。

- 除一个例外外，发送的信标信号必须根据上一节中定义的规则进行去加重。对于大于 500ns 的信标脉冲，信标信号电压必须从 VTX‐DIFFp‐p 规格去加重 6dB。对于小于 500ns 的信标脉冲，信标信号电压可以去加重最多 3.5dB。

## **眼图**

## **抖动、噪声和信号衰减**

当位流从链路一端的发送器传输到另一端的接收器时，它会受到以下破坏性影响：

- 由链路传输线路引起的确定性（即可预测的）抖动。

- 由链路上动态数据模式引起的数据相关抖动。

- 感应到信号对中的噪声。

- 由于传输线路的阻抗效应导致的信号衰减。

## **眼图测试**

为了验证接收器看到的信号是否在允许的变化范围内，可以执行眼图测试。以下描述由 James Edwards 在他为 _OE Magazine_ 撰写的文章中提供。

_“传输系统最常见的时域测量是眼图。眼图是从伪随机位序列重复采样的数据点的曲线图，由示波器显示。观察的时间窗口宽度为两个数据周期。对于以 2.5 GT/s 运行的 [PCI Express 链路]，周期为 400ps，时间窗口设置为 800ps。示波器扫描由每个数据时钟脉冲触发。眼图允许用户在单个图上观察系统性能。_

_为了观察每个可能的数据组合，示波器必须像多次曝光相机一样工作。数字示波器的显示持续时间设置为无限。每次时钟触发时，都会测量一个新的波形并叠加在所有_ 

_先前测量的波形之上。为了增强合成图像的解释，数字示波器可以分配不同的颜色来传达占据显示器上同一像素的波形出现次数的信息，这一过程称为颜色分级。现代数字采样示波器包括进行大量自动测量的能力，以充分表征各种眼图参数。"_

## **正常眼图**

理想的迹线捕获将绘制出与图 13‐26（第 486 页）中心标记为"正常"的轮廓相匹配的眼图模式。只要模式完全位于该区域内，发送器和链路就在容差范围内。请注意，显示的差分电压参数和值是峰值电压，而不是规范中使用的峰峰值电压，因为眼图中只能表示峰值电压。第 488 页的图 13‐27 显示了一个良好眼图的屏幕截图。

_图 13‐26：发送器眼图_

**==> picture [354 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Overshoot<br>Normal<br>Minimum Eye<br>De-emphasized Eye<br>Eye Opening<br>Normal<br>Undershoot<br>Jitter Jitter<br>TTX-EYE<br>UI = Unit Interval<br>TX-DIFF-p-MAX TX-DIFFp-MIN<br>V V<br>**----- End of picture text -----**<br>


**第 13 章：物理层 - 电气**

## **抖动的影响**

抖动（时序不确定性）是当边缘早于或晚于其理想时间到达时发生的，它会降低信号完整性并缩小眼图张开度。它由多种因素引起，从环境影响到正在传输的数据模式，再到导致信号电压电平过冲或欠冲正常区域的噪声或信号衰减。在 2.5 GT/s 时，这可以视为一个简单的集总效应，但在更高的数据速率下，它成为一个更显著的问题，必须在多个不同部分中加以考虑。为此，8.0 GT/s 数据速率定义了 5 个不同的抖动值。抖动分析和最小化的细节超出了本书的范围，但让我们至少定义规范使用的术语。抖动被描述为属于以下几个类别之一：

1. 不相关抖动 - 不依赖于或与正在传输的数据模式"相关"的抖动。

2. Rj - 随机抖动，来自不可预测的来源，无界，通常假定符合高斯分布。通常由系统中的电气或热噪声引起。

3. Dj - 确定性抖动，可预测且其峰峰值有界。通常由 EMI、串扰、电源噪声或接地问题引起。

4. PWJ - 脉冲宽度抖动 - 不相关的、边到边、高频抖动。 5. DjDD - 确定性抖动，使用双狄拉克近似。该模型是一种在不需要通常所需的大量样本的情况下快速估算低 BER 总抖动的方法。它使用在相对较短的时间段（约一小时）内采集的代表性样本，并外推曲线以得出可接受的近似值。

6. DDj - 数据相关抖动，是正在发送的数据模式的函数，规范指出这主要是由于封装损耗和反射引起的。ISI 是 DDj 的一个例子。

第 488 页的图 13‐28 显示了在 2.5 GT/s 下捕获的糟糕眼图的屏幕截图。由于这是在没有去加重的情况下捕获的，因此迹线应保持在最小眼图区域之外，该区域在屏幕上由中间的梯形形状显示。此示例说明抖动可以影响边缘到达时间和电压电平，导致一些迹线实例侵入眼图的禁区。

## **PCI Express Technology**

_图 13‐27：接收器正常眼图（无去加重）_

_图 13‐28：接收器不良眼图（无去加重）_

**第 13 章：物理层 - 电气**

## **发送器驱动器特性**

第 489 页的表 13‐3 列出了一些发送器驱动器特性。这并不打算复制规范中的表格，而是给出一些基本参数来说明数据速率之间的一些差异，例如 UI，并显示某些内容保持不变，例如 Tx 共模电压。

_表 13‐3：发送器规格_

|**项目**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|**单位**|**备注**|
|---|---|---|---|---|---|
|UI|399.88<br>（最小）<br>400.12<br>（最大）|199.94<br>（最小）<br>200.06<br>（最大）|124.9625<br>（最小）<br>125.0375<br>（最大）|ps|单位间隔（位时间）|
|TTX‐EYE|0.75<br>（最小）|0.75（最小）|见备注|UI|发送器眼图，包括所有抖动源。对于 8.0 GT/s，五个抖动源单独指定。|
|TTX‐RF‐MISMATCH|未指定|0.1（最大）|未指定|UI|从 20% 到 80% 测得的上升和下降时间差异（差分）。|
|VTX‐DIFFp‐p|0.8（最小）<br>1.2（最大）|0.8（最小）<br>1.2（最大）|见表 13‐4|mV|峰峰值差分电压。|
|VTX‐DIFFp‐p<br>LOW|0.4（最小）<br>1.2（最大）|0.4（最小）<br>1.2（最大）|见表 13‐4|mV|低功率电压。|
|VTX‐DC‐CM|0 到 3.6|0 到 3.6|0 到 3.6|V|Tx 引脚处的直流共模电压。|
|VTX‐DE‐RATIO‐3.5dB|3（最小）<br>4（最大）|3（最小）<br>4（最大）|见表 13‐4|mV|3.5 dB 去加重位的比率。|
|VTX‐DE‐RATIO‐6dB|n/a|5.5（最小）<br>6.5（最大）|见表 13‐4|mV|6 dB 去加重位的比率。|


## **PCI Express Technology**

_表 13‐3：发送器规格（续）_

|**项目**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|**单位**|**备注**|
|---|---|---|---|---|---|
|ITX‐SHORT|90|90|90|mA|当接地短路时发送器可提供的总单端电流。|
|VTX‐IDLE‐DIFF‐AC‐P|0（最小）<br>20（最大）|0（最小）<br>20（最大）|0（最小）<br>20（最大）|mV|链路处于电气空闲状态下的峰值差分电压。必须包括通过 10 KHz 到 1.25 GHz 频率的带通滤波器。|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-11-7"></a>
## 11.7 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|TTX‐IDLE‐MIN|20 (min)|20 (min)|20 (min)|ns|Minimum time a Trans‐<br>mitter must be in Electri‐<br>cal Idle.|
|TTX‐IDLE‐SET‐<br>TO‐IDLE|8 (max)|8 (max)|8 (max)|ns|Time allowed for Tx to<br>meet Electrical Idle spec<br>after last bit of required<br>EIOSs.|
|TTX‐IDLE‐TO‐<br>DIFF‐DATA|8|8|8|ns|Max time for Tx to meet<br>differential transmission<br>spec after Electrical Idle<br>exit.|
|ZTX‐DIFF‐DC|80 (min)<br>120 (max)|120 (max)|120 (max)||DC differential Tx imped‐<br>ance. Typical value is 100<br>. Min value for 5.0 and<br>8.0 GT/s is bounded by<br>RLTX‐DIFF|


_Table 13‐3: Transmitter Specs (Continued)_ 

|**Item**|**2.5 GT/s.**|**5.0 GT/s**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|RLTX‐DIFF|10 (min)|10 (min)<br>for 0.5‐1.25<br>GHz<br>8 (min) for<br>>1.25‐2.5<br>GHz|10 (min)<br>for 0.5‐1.25<br>GHz<br>8 (min) for<br>>1.25 ‐ 2.5<br>GHz<br>4 (min) for<br>>2.5 to 4<br>GHz|dB|Tx package return loss.<br>Note that the frequency is<br>the signal on the wire.<br>Note that at higher rates<br>it becomes necessary to<br>specify different parame‐<br>ters for different frequen‐<br>cies.|
|CTX|75 (min)<br>265 (max)|75 (min)<br>265 (max)|176 (min)<br>265 (max)|nF|Required AC coupling<br>cap on each Lane placed<br>in the media or in the<br>component itself.|
|LTX‐SKEW|500 ps +<br>2 UI<br>(max)|500 ps +<br>4 UI<br>(max)|500 ps +<br>6 UI|ps|Skew between any two<br>Lanes in the same Trans‐<br>mitter.|


_Table 13‐4: Parameters Specific to 8.0 GT/s_ 

|**Symbol**<br>VTX‐FS‐NO‐EQ|**Value**|**Units**|**Notes**|
|---|---|---|---|
||1300 (max)<br>800 (min)|mvPP|No EQ is applied; measured using 64<br>zeros followed by 64 ones.|
|VTX‐RS‐NO‐EQ|1300 (max)|mvPP|No EQ is applied; measured using 64<br>zeros followed by 64 ones.|
|VTX‐BOOST‐FS|8.0 (min)|dB|Tx boost ratio for full swing.<br>(Assumes +/‐ 1.5 dB tolerance)|
|VTX‐BOOST‐RS|2.5 (min)|dB|Tx boost ratio for reduced swing.<br>(Assumes +/‐ 1.0 dB tolerance)|
|EQTX‐COEFF‐<br>RES|1/24 (max)<br>1/63 (min)|n/a|Tx coefficient resolution|


## **Receiver Characteristics** 

## **Stressed-Eye Testing** 

Receivers are tested using a stressed eye technique, in which a signal with spe‐ cific problems is presented to the input pins and the BER is monitored. The spec presents these for 2.5 and 5.0 GT/s separately from 8.0 GT/s because of the dif‐ ference in the methods used, and then gives a third section that defines parame‐ ters common to all the speeds. 

## **2.5 and 5.0 GT/s** 

At 2.5 GT/s, the parameters are measured at the Receiver pins and there is an implied correlation between the margins observed and the BER. At 5.0 GT/s, receiver tolerancing is applied. This is a two‐step method in which a test board is calibrated to show the worst‐case signal margins as defined in the spec. Then, once the calibration is done, the test load is replaced by the device to be tested and its BER is observed. There are actually two sets of worst‐case numbers based on the clocking scheme: one is defined for the common‐clock architecture and another for the data‐clocked architecture. At higher speeds every element of the signal path must be carefully considered, and that’s true for the device package, too. The effects added to the signal by the package must be compre‐ hended in the testing process. 

The calibration channel itself must be designed with specific characteristics in mind, but the spec observes that a trace length of 28 inches on an FR4 PCB should suffice to create the necessary ISI. A signal generator is used to inject the Compliance Pattern with the appropriate jitter elements included. 

## **8.0 GT/s** 

The method for testing the stressed eye at 8.0 GT/s is similar, but there are some differences. One difference is that the signal can’t be evaluated at the device pin and so a replica channel is used to allow measuring the signal as it would appear at the pin if the device were an ideal termination. 

In order to evaluate the Receiver’s ability to perform equalization properly, it’s recommended that multiple calibration channels with different insertion loss characteristics be used so the receiver can be tested in more than one environ‐ ment. As with the transmitter at 8.0 GT/s, the calibration channel for the receiver consists of differential traces terminated at both ends with coaxial con‐ nectors. 
To establish the correct correlation between the channel and the receiver it’s nec‐ essary to model what the receiver see internally after equalization has been applied. That means post processing is must be applied that will model what happens in the Receiver, including the following items, the details of which are described in the spec: 

- Package insertion loss 

- CDR ‐ Clock and Data Recovery logic 

- Equalization that accounts for the longest calibration channel, including 

 - First‐order CTLE (Continuous Time Linear Equalizer) 

 - One‐tap DFE (Decision Feedback Equalizer) 

## **Receiver (Rx) Equalization** 

Transmitter equalization is mandatory, but the signal may still suffer enough degradation going through the longest permissible channel that the eye is closed and the signal is unrecognizable at the Receiver. To accommodate this the spec describes receiver equalization logic, but says is not intended to serve as an implementation guideline. What it does say is that a version will be required for calibrating the stressed eye when using the longest allowed calibra‐ tion channel. As described earlier, that requirement is described as a first‐order CTLE and a one‐tap DFE. 

## **Continuous-Time Linear Equalization (CTLE)** 

A linear equalizer removes the undesirable frequency components from the received signal. For PCIe this could be as simple as a passive high‐pass filter that reduces the voltage of the low frequency component from the received sig‐ nal which attenuates by a lower amount on the transmission line. It could also be done with amplification to open up the received eye, however that would amplify the high‐frequency noise along with the signal and create other prob‐ lems. 

One form of receiver equalization would be a circuit like the one shown in Fig‐ ure 13‐29 on page 494, which is a Discrete Time Linear Equalizer (DLE). This is simply an FIR filter, similar to the one used by the transmitter, to provide wave shaping as a means of compensating for channel distortion. One difference is that it uses a Sample and Hold (S & H) circuit on the front end to hold the ana‐ log input voltage at a sampled value for a time period, rather than allowing it to constantly change. The spec doesn’t mention DLE, and the reasons may include its higher cost and power compared to CTLE. As with the transmitter FIR, more taps provide better wave shaping but add cost, so only a small number are prac‐ tical. 

## **PCI Express Technology** 

_Figure 13‐29: Rx Discrete‐Time Linear Equalizer (DLE)_ 

**==> picture [297 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
Input<br>�<br>Received<br>S & H<br>Signal<br>C C<br>0 +1<br>1 UI delay 1 UI delay<br>**----- End of picture text -----**<br>


In contrast, CTLE is not limited to discrete time intervals and improves the sig‐ nal over a longer time interval. A simple RC network can serve as an example of a CTLE high‐pass filter, as shown in Figure 13‐30 on page 494. This serves to reduce the low‐frequency distortion caused by the channel without boosting the noise in the high‐frequency range of interest and cleans the signal for use at the next stage. Figure 13‐31 on page 495 illustrates the attenuation effect of CTLE high‐pass filter on the received low frequency component of a signal e.g. continuous 1s or continuous 0s. 

_Figure 13‐30: Rx Continuous‐Time Linear Equalizer (CTLE)_ 

**==> picture [239 x 96] intentionally omitted <==**

**----- Start of picture text -----**<br>
R<br>Channel Input<br>C<br>**----- End of picture text -----**<br>

_Figure 13‐31: Effect of Rx Continuous‐Time Linear Equalizer (CTLE) on Received Signal_ 

## **Decision Feedback Equalization (DFE)** 

An example one‐tap DFE circuit like the one described in the spec is shown in Figure 13‐32 on page 495, where it can be seen that the received signal is summed with the feedback value and then fed into a data “slicer.” A slicer is an A/D circuit that takes the analog‐looking input and converts it into a clean, full‐ swing digital signal for internal use. It makes its best guess and decides whether the input is a positive or negative value and outputs either +1 or ‐1. This deci‐ sion is sent into an FIR filter with only one tap, which is just a delayed version weighted according to a coefficient setting. The output of this filter is then fed back and summed with the received signal for use as the new input to the data slicer. 

_Figure 13‐32: Rx 1‐Tap DFE_ 

**==> picture [223 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
Output<br>Received<br>Signal<br>Slicer<br>- d1 Coefficient<br>1 UI<br>**----- End of picture text -----**<br>


## **PCI Express Technology** 

The spec only describes a single‐tap filter, but a two‐tap version is shown in Fig‐ ure 13‐33 on page 497 to illustrate another option. The motivation for including more taps is to create a cleaner output, since each tap reduces the noise for one more UI. Thus, two taps further reduce the undesirable components of the sig‐ nal, as shown in the pulse response waveform at the bottom of the drawing. This version is also shown as adaptive, meaning it’s able to modify the coeffi‐ cient values on the fly based on design‐specific criteria. 

The coefficients of the filter could be fixed, but if they’re adjustable the receiver is allowed to change them at any time as long as doing so doesn’t interfere with the current operation. In the section called “Recovery.Equalization” on page 587, Receiver Preset Hints are described as being delivered by the Down‐ stream Port to the Upstream Port on a Link, using EQ TS1s. The preset gives a hint, in terms of dB reduction, at a starting point for choosing these coefficients. 

Since the spec doesn’t require it, what the Receiver chooses to do regarding sig‐ nal compensation will be implementation specific. Industry literature states that DFE is more effective when working with an open eye, and that’s why it’s usu‐ ally employed after a linear equalizer that serves to clean up the input enough for DFE to work well. 
_Figure 13‐33: Rx 2‐Tap DFE_ 

**==> picture [303 x 364] intentionally omitted <==**

**----- Start of picture text -----**<br>
Output<br>Received Slicer<br>Signal<br>�<br>Adaptive<br>Coefficient<br>� Adjustment<br>- d2 - d1<br>1 UI 1 UI<br>V<br>1st tap reduction<br>2nd tap<br>reduction<br>t<br>UI UI UI UI Rx Original<br>Cursor Rx after DFE<br>**----- End of picture text -----**<br>


## **Receiver Characteristics** 

Some selected Receiver characteristics are listed in Table 13‐5 on page 498. The Receiver Eye Diagram in Figure 13‐34 on page 499 also illustrates some of the parameters listed in the table. 

## **PCI Express Technology** 

_Table 13‐5: Common Receiver Characteristics_ 

|**Item**|**2.5 GT/**<br>**s.**|**5.0 GT/s.**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|UI|399.88<br>(min)<br>400.12<br>(max)|199.94<br>(min)<br>200.06<br>(max)|124.9625<br>(min)<br>125.0375<br>(max)|ps|Unit Interval = bit time.|
|TRX‐EYE|0.4<br>(min)|Indirectly<br>specified||UI|Minimum eye width for a BER<br>or 10‐12. At higher rates and long<br>channels the eye is effectively<br>closed, making external mea‐<br>surement impractical.|
|VRX‐EYE|300|120 (CC)<br>100 (DC)|Not<br>specified|mVpp<br>diff|CC = common clocked, DC =<br>data clocked|

</td>
<td style="background-color:#e8e8e8">

|TTX‐IDLE‐MIN|20（最小）|20（最小）|20（最小）|ns|发送器必须处于电气空闲的最短时间。|
|TTX‐IDLE‐SET‐TO‐IDLE|8（最大）|8（最大）|8（最大）|ns|在所需 EIOS 的最后一位之后允许 Tx 满足电气空闲规格的时间。|
|TTX‐IDLE‐TO‐DIFF‐DATA|8|8|8|ns|Tx 在电气空闲退出后满足差分传输规格的最长时间。|
|ZTX‐DIFF‐DC|80（最小）<br>120（最大）|120（最大）|120（最大）|Ω|直流差分 Tx 阻抗。典型值为 100Ω。5.0 和 8.0 GT/s 的最小值由 RLTX‐DIFF 限定。|


**第 13 章：物理层 - 电气**

_表 13‐3：发送器规格（续）_

|**项目**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|**单位**|**备注**|
|---|---|---|---|---|---|
|RLTX‐DIFF|10（最小）|10（最小）<br>，频率 0.5‐1.25<br>GHz<br>8（最小），频率<br>>1.25‐2.5<br>GHz|10（最小）<br>，频率 0.5‐1.25<br>GHz<br>8（最小），频率<br>>1.25 ‐ 2.5<br>GHz<br>4（最小），频率<br>>2.5 至 4<br>GHz|dB|Tx 封装回波损耗。请注意，频率是线路上的信号。请注意，在较高速率下，有必要为不同频率指定不同参数。|
|CTX|75（最小）<br>265（最大）|75（最小）<br>265（最大）|176（最小）<br>265（最大）|nF|每个 Lane 所需的 AC 耦合电容，放置在介质或组件本身中。|
|LTX‐SKEW|500 ps +<br>2 UI<br>（最大）|500 ps +<br>4 UI<br>（最大）|500 ps +<br>6 UI|ps|同一发送器中任意两个 Lane 之间的偏移。|


_表 13‐4：8.0 GT/s 特定参数_

|**符号**<br>VTX‐FS‐NO‐EQ|**值**|**单位**|**备注**|
|---|---|---|---|
||1300（最大）<br>800（最小）|mvPP|不应用 EQ；使用 64 个零后跟 64 个一进行测量。|
|VTX‐RS‐NO‐EQ|1300（最大）|mvPP|不应用 EQ；使用 64 个零后跟 64 个一进行测量。|
|VTX‐BOOST‐FS|8.0（最小）|dB|满摆幅的 Tx 提升比率。（假设 +/‐ 1.5 dB 容差）|
|VTX‐BOOST‐RS|2.5（最小）|dB|缩减摆幅的 Tx 提升比率。（假设 +/‐ 1.0 dB 容差）|
|EQTX‐COEFF‐RES|1/24（最大）<br>1/63（最小）|n/a|Tx 系数分辨率|


## **接收器特性**

## **应力眼图测试**

接收器使用应力眼图技术进行测试，其中将具有特定问题的信号呈现给输入引脚并监控 BER。规范针对 2.5 和 5.0 GT/s 与 8.0 GT/s 分别给出了这些参数，因为所使用的方法不同，然后给出了定义所有速度通用参数的第三部分。

## **2.5 和 5.0 GT/s**

在 2.5 GT/s 时，参数在接收器引脚处测量，观察到的裕量与 BER 之间存在隐含的相关性。在 5.0 GT/s 时，应用接收器容差。这是一种两步方法，其中校准测试板以显示规范中定义的最坏情况信号裕量。然后，一旦校准完成，测试负载被替换为要测试的设备并观察其 BER。实际上根据时钟方案有两组最坏情况数字：一组为公共时钟架构定义，另一组为数据时钟架构定义。在更高的速度下，信号路径的每个元素都必须仔细考虑，设备封装也是如此。封装添加到信号的影响必须在测试过程中加以理解。

校准通道本身必须以特定的特性进行设计，但规范观察到 FR4 PCB 上 28 英寸的走线长度应足以产生必要的 ISI。使用信号发生器注入包含适当抖动元素的合规模式。

## **8.0 GT/s**

8.0 GT/s 应力眼图测试方法类似，但存在一些差异。一个差异是信号无法在设备引脚处评估，因此使用复制通道以允许在设备是理想终端的情况下测量引脚处的信号。

为了评估接收器正确执行均衡的能力，建议使用具有不同插入损耗特性的多个校准通道，以便可以在多个环境中测试接收器。与 8.0 GT/s 的发送器一样，接收器的校准通道由两端均端接同轴连接器的差分走线组成。

**第 13 章：物理层 - 电气**

为了建立通道和接收器之间的正确相关性，有必要对接收器在应用均衡后在内部看到的内容进行建模。这意味着必须应用后处理来模拟接收器中发生的情况，包括以下项目，其详细信息在规范中描述：

- 封装插入损耗

- CDR - 时钟数据恢复逻辑

- 考虑最长校准通道的均衡，包括：

 - 一阶 CTLE（连续时间线性均衡器）

 - 单抽头 DFE（判决反馈均衡器）

## **接收器 (Rx) 均衡**

发送器均衡是强制性的，但信号在通过最长允许通道时仍可能遭受足够的退化，导致眼图关闭且信号在接收器处无法识别。为了适应这种情况，规范描述了接收器均衡逻辑，但表示不打算将其作为实现指南。它确实说的是，当使用最长允许的校准通道时，校准应力眼图将需要一个版本。如前所述，该需求被描述为一阶 CTLE 和单抽头 DFE。

## **连续时间线性均衡 (CTLE)**

线性均衡器去除接收信号中不良的频率分量。对于 PCIe，这可以像无源高通滤波器一样简单，它降低从传输线路上衰减较少的接收信号的低频分量的电压。它也可以通过放大来实现以打开接收到的眼图，但这会放大高频噪声以及信号并产生其他问题。

接收器均衡的一种形式是如图 13‐29（第 494 页）所示的电路，这是一个离散时间线性均衡器 (DLE)。它只是一个 FIR 滤波器，类似于发送器使用的滤波器，用作波形整形以补偿通道失真。一个区别是它使用采样保持 (S & H) 电路在前端将模拟输入电压保持在一个采样值上一段时间，而不是允许其不断变化。规范没有提到 DFE，原因可能包括其相对于 CTLE 较高的成本和功耗。与发送器 FIR 一样，更多的抽头提供更好的波形整形但增加了成本，因此实际只能使用少量抽头。

## **PCI Express Technology**

_图 13‐29：接收器离散时间线性均衡器 (DLE)_

**==> picture [297 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
Input<br>�<br>Received<br>S & H<br>Signal<br>C C<br>0 +1<br>1 UI delay 1 UI delay<br>**----- End of picture text -----**<br>


相比之下，CTLE 不限于离散时间间隔，而是在更长的时间间隔内改善信号。一个简单的 RC 网络可以作为 CTLE 高通滤波器的示例，如图 13‐30（第 494 页）所示。这用于减少由通道引起的低频失真，而不会在感兴趣的频率范围内提升高频噪声，并为下一阶段的处理清理信号。图 13‐31（第 495 页）说明了 CTLE 高通滤波器对接收信号的低频分量（例如连续的 1 或连续的 0）的衰减效应。

_图 13‐30：接收器连续时间线性均衡器 (CTLE)_

**==> picture [239 x 96] intentionally omitted <==**

**----- Start of picture text -----**<br>
R<br>Channel Input<br>C<br>**----- End of picture text -----**<br>


**第 13 章：物理层 - 电气**

_图 13‐31：接收器连续时间线性均衡器 (CTLE) 对接收信号的影响_

## **判决反馈均衡 (DFE)**

第 495 页的图 13‐32 显示了规范中描述的示例单抽头 DFE 电路，可以看到接收信号与反馈值求和，然后馈入数据"切片器"。切片器是一个 A/D 电路，它接收类似模拟的输入并将其转换为干净的、满摆幅的数字信号以供内部使用。它做出最佳猜测并确定输入是正值还是负值，并输出 +1 或 ‐1。该决策被送入只有一个抽头的 FIR 滤波器，该抽头只是按系数设置加权的延迟版本。该滤波器的输出然后被反馈并与接收信号求和，作为数据切片器的新输入。

_图 13‐32：接收器 1 抽头 DFE_

**==> picture [223 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
Output<br>Received<br>Signal<br>Slicer<br>- d1 Coefficient<br>1 UI<br>**----- End of picture text -----**<br>


## **PCI Express Technology**

规范仅描述了单抽头滤波器，但第 497 页的图 13‐33 中显示了两抽头版本以说明另一个选项。包含更多抽头的动机是为了产生更干净的输出，因为每个抽头减少了一个 UI 的噪声。因此，两个抽头进一步减少了信号中的不良分量，如图底部的脉冲响应波形所示。该版本也显示为自适应的，意味着它能够根据特定设计的标准动态修改系数值。

滤波器的系数可以是固定的，但如果它们是可调的，则允许接收器随时更改它们，只要这样做不会干扰当前操作。在第 587 页的 "Recovery.Equalization" 部分，描述了接收器预设提示（Receiver Preset Hints）由下游端口使用 EQ TS1 传递给链路上的上游端口。该预设以 dB 减小的形式给出提示，作为选择这些系数的起点。

由于规范不要求这样做，接收器选择如何进行信号补偿将是特定于实现的。行业文献指出，DFE 在处理开放眼图时更有效，这就是为什么它通常在使用线性均衡器清理输入以使 DFE 良好工作之后才使用。

**第 13 章：物理层 - 电气**

_图 13‐33：接收器 2 抽头 DFE_

**==> picture [303 x 364] intentionally omitted <==**

**----- Start of picture text -----**<br>
Output<br>Received Slicer<br>Signal<br>�<br>Adaptive<br>Coefficient<br>� Adjustment<br>- d2 - d1<br>1 UI 1 UI<br>V<br>1st tap reduction<br>2nd tap<br>reduction<br>t<br>UI UI UI UI Rx Original<br>Cursor Rx after DFE<br>**----- End of picture text -----**<br>


## **接收器特性**

第 498 页的表 13‐5 中列出了一些选定的接收器特性。第 499 页的图 13‐34 中的接收器眼图也说明了表中列出的一些参数。

## **PCI Express Technology**

_表 13‐5：通用接收器特性_

|**项目**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|**单位**|**备注**|
|---|---|---|---|---|---|
|UI|399.88<br>（最小）<br>400.12<br>（最大）|199.94<br>（最小）<br>200.06<br>（最大）|124.9625<br>（最小）<br>125.0375<br>（最大）|ps|单位间隔 = 位时间。|
|TRX‐EYE|0.4<br>（最小）|间接指定||UI|10‐12 BER 的最小眼图宽度。在更高的速率和长通道下，眼图实际上是关闭的，使得外部测量不切实际。|
|VRX‐EYE|300|120（CC）<br>100（DC）|未指定|mVpp<br>差分|CC = 公共时钟，DC = 数据时钟|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
