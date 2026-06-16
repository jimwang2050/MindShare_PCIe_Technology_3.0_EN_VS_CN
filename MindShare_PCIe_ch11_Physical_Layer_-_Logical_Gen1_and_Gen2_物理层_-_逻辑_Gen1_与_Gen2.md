# 📘 第 11 章　物理层 - 逻辑 (Gen1 与 Gen2) (Chapter 11. Physical Layer - Logical (Gen1 and Gen2))

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0278.md` ... `chunks/chunk0284.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Physical Layer - Logical (Gen1 and Gen2)](#-本章目录-table-of-contents)

<a id="sec-11-1"></a>
## 11.1 Physical Layer - Logical (Gen1 and Gen2) | 物理层 - 逻辑 (Gen1 与 Gen2)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

**Chapter 13: Physical Layer - Electrical** 

## **Component Interfaces** 

Components from different vendors must work reliably together, so a set of parameters are specified that must be met for the interface. For 2.5 GT/s it was implied, and for 5.0 GT/s it was explicitly stated, that the characteristics of this interface are defined at the device pins. That allows a component to be charac‐ terized independently, without requiring the use of any other PCIe components. Other interfaces may be specified at a connector or other location, but those are not covered in the base spec and would be described in other form‐factor specs like the _PCI Express Card Electromechanical Spec_ . 

## **Physical Layer Electrical Overview** 

The electrical sub‐block associated with each lane, as shown in Figure 13‐1 on page 450, provides the physical interface to the Link and contains differential Transmitters and Receivers. The Transmitter delivers outbound Symbols on each Lane by converting the bit stream into two single‐ended electrical signals with opposite polarity. Receivers compare the two signals and, when the differ‐ ence is sufficiently positive or negative, generate a one or zero internally to rep‐ resent the intended serial bit stream to the rest of the Physical Layer. 

**449** 

## **PCI Ex ress Technolo p gy** 

_Figure 13‐1: Electrical Sub‐Block of the Physical Layer_ 

**==> picture [367 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Physical Layer Physical Layer<br>Tx Rx Tx Rx<br>Logical Logical<br>Tx Rx Tx Rx<br>Electrical Electrical<br>Link<br>Tx+ Tx- Rx+ Rx- CTX Tx- Tx+ Rx- Rx+<br>CTX<br>**----- End of picture text -----**<br>


When the Link is in the L0 full‐on state, the drivers apply the differential volt‐ age associated with a logical 1 and logical 0 while maintaining the correct DC common mode voltage. Receivers sense this voltage as the input stream, but if it drops below a threshold value, it’s understood to represent the Electrical Idle Link condition. Electrical Idle is entered when the Link is disabled, or when ASPM logic puts the Link into low‐power Link states such as L0s or L1 (see “Electrical Idle” on page 736 for more on this topic). 

Devices must support the Transmitter equalization methods required for each supported data rate so they can achieve adequate signal integrity. De‐emphasis is applied for 2.5 and 5.0 GT/s, and a more complex equalization process is applied for 8.0 GT/s. These are described in more detail in “Signal Compensa‐ tion” on page 468, and “Recovery.Equalization” on page 587. 

The drivers and Receivers are short‐circuit tolerant, making PCIe add‐in cards suited for hot (powered‐on) insertion and removal events in a hot‐plug environ‐ ment. The Link connecting two components is AC‐coupled by adding a capaci‐ tor in‐line, typically near the Transmitter side of the Link. This serves to de‐ 

**450** 

**Chapter 13: Physical Layer - Electrical** 

couple the DC part of the signal between the Link partners and means they don’t have to share a common power supply or ground return path, as when the devices are connected over a cable. Figure 13‐1 on page 450 illustrates the place‐ ment of this capacitor (CTX) on the Link. 

## **High Speed Signaling** 

The high‐speed signaling environment of PCIe is characterized by the drawing in Figure 13‐2 on page 451. This low‐voltage differential signaling environment is a common method used in many serial transports and one reason is for the noise rejection it provides. Electrical noise that affects one signal will also affect the other because they are on adjacent pins and their traces are very close to each other. Since both signals are influenced, as shown in Figure 13‐3 on page 452, the difference between them doesn’t change much and is therefore not seen at the receiver. 

A design goal for the 3.0 spec revision was that the 8.0 GT/s rate should still work with existing standard FR4 circuit boards and connectors, and that was achieved by changing the encoding scheme from the old 8b/10b to the new 128b/130b model to keep the frequency low. This goal will probably change with the next speed step (Gen4). 

_Figure 13‐2: Differential Transmitter/Receiver_ 

**==> picture [384 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Logic<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>VTX-CM = 0 - 3.6 V<br>ZTX = ZRX = 50 Ohms +/- 20%<br>CTX = 75 - 265 nF (Gen1 & Gen2)<br>= 176 - 265 nF (Gen3)<br>No Spec<br>**----- End of picture text -----**<br>


**451** 

## **PCI Ex ress Technolo p gy** 

_Figure 13‐3: Differential Common‐Mode Noise Rejection_ 

**==> picture [374 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
D+<br>D-<br>Reference voltage shift<br>Differential<br>voltage remains<br>+ Differential the same<br>voltage<br>Tx Rx<br>- +<br>0 V 0 V<br>-<br>Single-<br>ended<br>voltage Single-ended<br>voltage changes<br>Transient Noise<br>Tx Rx<br>+ +<br>Vcm Vcm<br>- -<br>Differential<br>voltage<br>remains same<br>**----- End of picture text -----**<br>


## **Clock Requirements** 

## **General** 

For all data rates, both Transmitter and Receiver clocks must be accurate to within +/‐ 300 ppm (parts per million) of the center frequency. In the worst case, the Transmitter and Receiver could both be off by 300 ppm in opposite direc‐ tions, resulting in a maximum difference of 600 ppm. That worst‐case model translates to a gain or loss of 1 clock every 1666 clocks and that’s the difference that a Receiver’s clock compensation logic must take into account. 

Devices are allowed to derive their clocks from an external source, and the 100 MHz Refclk is still optionally available for this purpose in the 3.0 spec. Using the Refclk permits both Link partners to readily maintain the 600 ppm accuracy even when Spread Spectrum Clocking is applied. 

**452** 

**Chapter 13: Physical Layer - Electrical** 

## **SSC (Spread Spectrum Clocking)** 

SSC is an optional technique used to modulate the clock frequency slowly over a prescribed range to spread the signal’s EMI (Electro‐Magnetic Interference) across a range of frequencies rather than allowing it all to be concentrated at the center frequency. Spreading the radiated energy helps a device or system to pass government emissions standards by staying under a threshold value, as illustrated in Figure 13‐4 on page 454. Note that the frequency of interest for the signal is only half the clock rate because two rising clock edges are needed to create one cycle on the data, as illustrated in Figure 13‐5 on page 454. For exam‐ ple, a 2.5 GT/s rate uses a bit clock of 2.5 GHz, resulting in a frequency of inter‐ est on the traces of 1.25 GHz. 

The use of SCC is not required by the spec but, if will be supported, the follow‐ ing rules apply: 

- The clock can be modulated by +0% to ‐0.5% from nominal (5000 ppm), referred to as “down spreading.” A frequency modulation envelope is not specified, but a sawtooth‐wave pattern like the one shown in Figure 13‐6 on page 455 yields good results. Note that there is a trade‐off with down spreading, because the average clock frequency will now be 0.25% lower than it would have been without SSC, resulting in a slight performance reduction. 

- The modulation rate must be between 30KHz and 33KHz. 

- The +/‐ 300 ppm requirement for clock frequency accuracy still holds and therefore so does the maximum 600 ppm variation between Link partners. The spec states that most implementations will require both Link partners to use the same clock source, although it’s not required. One way to do that would be for them to both use a modulated version of the Refclk to derive their own clocks (see “Common Refclk” on page 456). 

**453** 

## **PCI Ex ress Technolo p gy** 

_Figure 13‐4: SSC Motivation_ 

**==> picture [324 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
EMI Power Threshold<br> Ordinary Signal<br>Spread-Spectrum<br>Signal<br>range = 0.5%<br>Signal<br>Frequency<br>Frequency (GHz)<br>Emitted Power (dB)<br>**----- End of picture text -----**<br>


_Figure 13‐5: Signal Rate Less Than Half the Clock Rate_ 

**==> picture [384 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
Signal on<br>the wire<br>Tx Clock<br>**----- End of picture text -----**<br>


**454** 

**Chapter 13: Physical Layer - Electrical** 

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

**455** 

**PCI Ex ress Technolo p gy** 

**Common Refclk.** The first architecture described is one in which both Link partners make use of the same Refclk, as shown in Figure 13‐7 on page 456. There are three straightforward advantages for this implementation: 

- First, the jitter associated with the reference clock is the same for both Tx and Rx and is thus tracked and accounted for intrinsically. 

- – Second, the use of SSC will be simplest with this model because maintaining the 600 ppm separation between the Tx and Rx clocks is easy if both follow the same modulated reference. 

- Third, the Refclk remains available during low‐power Link states L0s and L1 and that allows the Receiver’s CDR to maintain a sem‐ blance of the recovered clock even in the absence of a bit stream to supply the edges in the data. That, in turn, keeps the local PLLs from drifting as much as they otherwise would, resulting in a reduced recovery time back to L0 compared to the other clocking options. 

_Figure 13‐7: Shared Refclk Architecture_ 

**==> picture [374 x 138] intentionally omitted <==**

**----- Start of picture text -----**<br>
+<br>Tx Lane in Rx<br>Register Tx directionone Rx Register<br>-<br>CDR<br>PLL<br>PLL<br>Refclk<br>**----- End of picture text -----**<br>


**Data Clocked Rx Architecture.** In this clock architecture, the Receiver doesn’t use a reference clock at all, but simply recovers the Transmitter clock from the data stream, as shown in Figure 13‐9 on page 457. This implementation is clearly the simplest of the three and would therefore ordinarily be preferred. The spec doesn’t prohibit the use of SSC in this model, but doing so would bring up two issues. First, the Receiver CDR must remain locked onto the input frequency as it modulates through a much wider range (5600 ppm instead of the usual 600 ppm), and that could require more complex logic. And second, the maximum clock frequency separation of 600ppm must still be maintained and it’s less clear how that would be done without a common reference. 

**456**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

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

**Chapter 13: Physical Layer - Electrical** 

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

**457** 

**PCI Ex ress Technolo p gy** 

## **Transmitter (Tx) Specs** 

## **Measuring Tx Signals** 

The spec notes that the methods for measuring the Tx output are limited at the higher frequencies. At 2.5 GT/s it’s possible to put a test probe very near the pins of the DUT (Device Under Test), but for the higher rates it’s necessary to use a “breakout channel” with SMA (SubMiniature version A) microwave‐type coax‐ ial connectors, as illustrated at TP1 (Test Point 1), TP2, and TP3 in Figure 13‐10 on page 458. Note that it’s necessary to have a low‐jitter clock source to the device under test, so that jitter seen at the output is only introduced by the device itself. The spec also mentions that it’s important during testing for the device to have as many of its Lanes and other outputs in use at the same time as possible, so as to best simulate a real system. 

Since the breakout channel introduces some effects to the signal, for 8.0 GT/s it’s necessary to be able to measure those effects and remove (de‐embed) them from the signal being tested. One way to accomplish this is for the test board to sup‐ ply another signal path that is very similar to the one used for the device pins. Characterizing this “replica channel” with a known signal gives the needed information about the channel, allowing its effects to be de‐embedded from the DUT signals so the signal at the component pins can be recovered. 

_Figure 13‐10: Test Circuit Measurement Channels_ 

**==> picture [294 x 159] intentionally omitted <==**

**----- Start of picture text -----**<br>
DUT<br>TP1<br>Breakout Channel<br>Low-Jitter<br>Clock Source<br>Replica Channel<br>TP2 TP3<br>**----- End of picture text -----**<br>


**458** 

**Chapter 13: Physical Layer - Electrical** 

## **Tx Impedance Requirements** 

For best accuracy, the characteristic differential impedance of the Breakout Channel should be 100  differential within 10%, with a single‐ended imped‐ ance of 50  . To match this environment, Transmitters have a differential low‐ impedance value during signaling between 80 and 120  at 2.5 GT/s, and no more than 120  at 5.0 and 8.0 GT/s. For receivers, the single‐ended impedance is 40 ‐ 60  at 2.5 or 5.0 GT/s, but for 8.0 GT/s no specific value is given. Instead, it’s simply noted that the single‐ended receiver impedance must be 50  within 20% by the time the Detect LTSSM state is entered so that the detect circuit will sense the Receiver correctly. 

Transmitters must also meet the return loss parameters RLTX‐DIFF and RLTX‐CM anytime differential signals are sent. As a very brief introduction to this termi‐ nology, “return loss” is a measure of energy transmitted through or reflected back from a transmission path. Return loss is one of several “Scattering” param‐ eters (S‐parameters) that are used to analyze high‐frequency signal environ‐ ments. When frequencies are low, a lumped‐element description is sufficient, but when they become high enough that the wavelength approaches the size of the circuit, a distributed model is needed and that’s what S‐parameters are used to represent. The spec describes a number of these to characterize a transmis‐ sion path but the details of this high‐frequency analysis are really beyond the scope of this book. 

When a signal is not being driven, as would be the case in the low‐power Link states, the Transmitter may go into a high‐impedance condition to reduce the power drain. For that case, it only has to meet the ITX‐SHORT value and the dif‐ ferential impedance is not defined. 

## **ESD and Short Circuit Requirements** 

All signals and power pins must withstand a 2000V ESD (Electro‐Static Dis‐ charge) using the Human Body Model and 500V using the Charged Device Model. For more details on these models or ESD, see the JEDEC JESE22‐A114‐A spec. 

The ESD requirement not only protects against electro‐static damage, but facili‐ tates support of surprise hot insertion and removal events (adding or removing an add‐in card while the power is on). That goal also motivates the requirement that Transmitters and Receivers be able to withstand sustained short‐circuit cur‐ rents of ITX‐SHORT (see Table 13‐5 on page 498). 

**459** 

**PCI Ex ress Technolo p gy** 

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

**460** 

**Chapter 13: Physical Layer - Electrical** 

but mentions that future spec revisions may. Therefore, it would be wise to include this functionality in new designs. 

_Figure 13‐11: Receiver Detection Mechanism_ 

**==> picture [370 x 380] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Logic Receiver Present<br>D+ CTX ZTX => Long Charge time D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>Detect<br>Logic<br>Receiver Absent<br>D+ CTX => Short Charge time<br>Transmitter<br>CTX<br>D-<br>ZTX ZTX<br>VCM<br>No Spec<br>**----- End of picture text -----**<br>


**461** 

**PCI Ex ress Technolo p gy** 

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

**462** 

**Chapter 13: Physical Layer - Electrical** 

Receiver must be able to sense an attenuated version of the signal, defined as VRX‐DIFFp‐p (see Table 13‐5 on page 498). 

_Figure 13‐12: Differential Signaling_ 

**==> picture [301 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
V+<br>D+<br>V<br>cm<br>Receiver subtracts<br>D- from D+ value to<br>arrive at differential<br>D- voltage.<br>V<br>cm<br>V-<br>**----- End of picture text -----**<br>


## **Differential Notation**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

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

**463** 

**PCI Ex ress Technolo p gy** 

_Figure 13‐13: Differential Peak‐to‐Peak (_ VDIFFp‐p _) and Peak (_ VDIFFp _) Voltages_ 

**==> picture [327 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
D+<br>V VDIFFp VDIFFp<br>CMp (Logical 1) (Logical 0)<br>D-<br>0 V<br>VDIFFp-p = 2 * max | VD+ - VD- | =  VDIFFp (Logical 1) + VDIFFp (Logical 0)<br>**----- End of picture text -----**<br>


## **Reduced-Swing Differential Voltage** 

The full‐swing voltage is needed for channels that are long or otherwise lossy, and Transmitters are required to support it. But when the signal environment is short and low loss, a high voltage is unnecessary and a power savings can be realized by reducing it. With this in mind, the spec for 2.5 GT/s and 5.0 GT/s defines another, reduced‐swing voltage for power‐sensitive systems where a short channel is being used. In this mode the voltage is reduced to about half of its full‐swing range. Support for this operation is optional, and the means for selecting it is not defined and will be implementation specific. 

The same is true for 8.0 GT/s signaling, except that in this case it’s achieved by using a limited range of coefficients. For example, the maximum boost for the reduced‐swing case is limited to 3.5 dB. As with the lower data rates, support for this voltage model is optional, but now the means of achieving it is straight‐ forward: just set the Tx coefficient values to make it happen. 

It should be noted that the Receiver voltage levels are independent of the trans‐ mitter, which is intuitively what we’d expect: the received signal always needs to meet the normal requirements and so the Transmitter and channel must be designed to guarantee that it will. 

## **Equalized Voltage** 

In the interest of maintaining a good flow in this section, this large topic is cov‐ ered separately in the section called “Signal Compensation” on page 468. 

**464** 

**Chapter 13: Physical Layer - Electrical** 

## **Voltage Margining** 

The concept of margining is that Transmitter characteristics like output voltage can be adjusted across a wide range of values during testing to determine how well it can handle a signaling environment. The 2.5 GT/s rate didn’t include this capability, but voltage margining was added with the 5.0 GT/s rate and must be implemented by Transmitters that use that rate or higher. Other parameters, like de‐emphasis or jitter can optionally be margined as well. The granularity for the margining adjustments must be controllable on a Link basis and may be controllable on a Lane basis. This control is accomplished by means of the Link Control 2 register in the PCIe Capability register block. The transmit margin field, shown in Figure 13‐14 on page 465, contains 3 bits and can thus represent 8 levels. Their values are not defined, and not all of them need to be imple‐ mented. The default value is all zeros, which represents the normal operating range. 

It’s important to note that this field is only intended for debug and compliance testing purposes during which software is only allowed to modify it during those times. At all other times, the value is required to be set to the default of all zeros. 

_Figure 13‐14: Transmit Margin Field in Link Control 2 Register_ 

**==> picture [355 x 211] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 Register<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


**465** 

**PCI Ex ress Technolo p gy** 

For 8.0 GT/s, transmitters are required to implement voltage margining and use the same field in the Link Control 2 register, but equalization adds some con‐ straints to the options because it can’t require finer coefficient or preset resolu‐ tion than the 1/24 resolution defined for normal operation. 

During Tx margining the equalization tolerance for 2.5 GT/s and 5.0 GT/s is relaxed from +/‐ 0.5 dB to +/‐ 1.0 dB. For the 8.0 GT/s rate, the tolerance is defined by the coefficient granularity and the normal equalizer tolerances spec‐ ified for the transmitter. 

## **Receiver (Rx) Specs** 

## **Receiver Impedance** 

Receivers are required to meet the RLRX‐DIFF and RLRX‐CM (see Table 13‐5 on page 498) parameters unless the device is powered down, as it would be, for example, in the L2 and L3 power states or during a Fundamental Reset. In those cases, a Receiver goes to the high impedance state and must meet the ZRX‐HIGH‐IMP‐DC‐NEG and ZRX‐HIGH‐IMP‐DC‐NEG parameters. 

(See Table 13‐5 on page 498.) 

## **Receiver DC Common Mode Voltage** 

The Receiver’s DC common mode voltage is specified to be 0V for all data rates, and that’s represented in Figure 13‐15 on page 467 by showing the signal termi‐ nations connected to ground. The CTX in‐line capacitor permits this voltage to be something different at the Transmitter, which is specified to be in the range from 0 ‐ 3.6V. That’s not as interesting when the Transmitter and Receiver are in the same enclosure and have the same power supply, but if they’re connected over a cable and reside in different machines with different power supplies it becomes more important. In that case it’s difficult to avoid reference voltage dif‐ ferences between the machines and, since the signal voltages are already small, such a difference could make the signal difficult to recognize at the Receiver. The location of this capacitor must be near the Transmitter pins when a connec‐ tor of some kind will be used but, if there’s no connector, it can be located at any convenient place on the transmission line. Although it could be integrated into a device, it’s expected that CTX will be external because it would be too big to inte‐ grate. 

**466** 

**Chapter 13: Physical Layer - Electrical** 

The drawing in Figure 13‐15 on page 467 also shows an optional set of resistors at the Receiver, labeled as “No Spec” because they are not mentioned in the spec. The story here is that Receiver designers dislike using a common‐mode voltage of zero for the simple reason that it usually requires them to implement two reference voltages, one above zero and one below it. A preferred imple‐ mentation offsets the signal entirely above or below zero, so that only one refer‐ ence voltage is needed.The circuit shown within the dotted line accomplishes this by adding a small‐value in‐line capacitor to de‐couple the DC component of the signal on the wire from that of the Receiver itself. Then, a resistor ladder serves to offset the Receiver’s common‐mode voltage in one direction or the other to accomplish the goal. 

_Figure 13‐15: Receiver DC Common‐Mode Voltage Adjustment_ 

**==> picture [384 x 273] intentionally omitted <==**

**----- Start of picture text -----**<br>
Small Big<br>Ratio of resistors<br>Big sets DC common<br>mode voltage<br>Small Big<br>Detect Big<br>Logic<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one Receiver<br>CTX ZTX direction<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX<br>VRX-CM = 0 V<br>VCM<br>No Spec<br>**----- End of picture text -----**<br>


**467** 

**PCI Ex ress Technolo p gy** 

## **Transmission Loss** 

The Transmitter drives a minimum differential peak‐to‐peak voltage VTX‐DIFFp‐p of 800 mV. The Receiver sensitivity is designed for a minimum dif‐ ferential peak‐to‐peak voltage (VRX‐DIFFp‐p) of 175 mV. This translates to a 13.2dB loss budget that a Link is designed for. Although a board designer can determine the attenuation loss budget of a Link plotted against various frequen‐ cies, the Transmitter and Receiver eye diagram measurement are the ultimate determinant of loss budget for a Link. Eye diagrams are described in “Eye Dia‐ gram” on page 485. A Transmitter that drives up to the maximum allowed dif‐ ferential peak‐to‐peak voltage of 1200 mV can compensate for a lossy Link that has worst‐case attenuation characteristics. 

## **AC Coupling** 

PCI Express requires in‐line AC‐coupling capacitors be placed on each Lane, usually near the Transmitter. The capacitors can be integrated onto the system board, or integrated into the device itself, although the large size they would need makes that unlikely. An add‐in card with a PCI Express device on it must place the capacitors on the card close to the Transmitter or integrate the capaci‐ tors into the PCIe silicon. These capacitors provide DC isolation between two devices on both ends of a Link thus simplifying device design by allowing devices to use independent power and ground planes. 

## **Signal Compensation** 

## **De-emphasis Associated with Gen1 and Gen2 PCIe** 

For 2.5 GT/s and 5.0 GT/s transmission, PCIe mandates the use of a fairly simply form of Transmitter equalization called **de‐emphasis** to reduce the effects of signal distortion along the Link transmission line. This distortion problem is always present but gets worse with increased frequency and lossy transmission lines. 

## **The Problem** 

As data rates get higher, the Unit Interval (UI ‐ bit time) becomes smaller, with the result that it’s increasingly difficult to avoid having the value in one bit time affect the value in another bit time. The channel always resists changes to the voltage level, The faster we attempt to switch voltage, the more pronounced 

**468** 

**Chapter 13: Physical Layer - Electrical** 

that effect becomes. However, when a signal has been held at the same voltage for several bit times, as when sending several bits in a row of the same polarity, the channel has more time to approach the target voltage. The resulting higher voltage makes it difficult to change to the opposite value within the required time when the polarity does change. This problem of previous bits affecting subsequent bits is referred to as **ISI** ( **inter‐symbol interference** ). 

## **How Does De-Emphasis Help?** 

De‐emphasis reduces the voltage for repeated bits in a bit stream. Although it sounds counter‐intuitive at first because this reduces the signal swing and thus the energy that reaches the Receiver, reducing the Transmitter voltage for these cases can substantially improve signal quality. Figure 13‐16 on page 469 illus‐ trates how this works by showing a Transmitter output of ‘1000010000’, where the repeated bits of the same polarity have been de‐emphasized. De‐emphasis can be thought of as a two‐tap Tx equalizer, and some rules related to it are:

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

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


**469** 

**PCI Ex ress Technolo p gy** 

## **Solution for 2.5 GT/s** 

For 2.5 GT/s, each subsequent bit transmitted after the first bit of the same polarity must be de‐emphasized by 3.5dB to accommodate this worst‐case loss budget. Of course, for low‐loss environments this is less important and for a very short path it can even make the received signal look worse. After all, de‐ emphasis is essentially distorting the transmitted signal in the opposite way of the distortion that is expected during transmission so as to cancel it out. If there turns out to be little or no distortion, then de‐emphasis will make the signal look worse. The spec doesn’t describe any way to test the signal environment or adjust the de‐emphasis level, but doesn’t prohibit a designer from developing an implementation‐specific method of doing so. 

An example of the benefit of de‐emphasis is shown in Figure 13‐17 on page 471, which is a scope capture converted into a drawing for clarity. The captures were taken from a device driving a long path and using a bit stream with several repeated bits to show the signal distortion. The trace at the top shows that the bit pattern for one side of the differential pair (also called a single‐ended signal) has 2 bits of one polarity followed by 5 bits of the opposite polarity. Five consec‐ utive bits is the worst case for 8b/10b, and this particular pattern only appears in a few characters like the COM character. The channel resists high‐speed changes but will continue to charge up if the driver keeps trying to reach a higher voltage and that can be seen in this example. When the bits aren’t repeated there isn’t time for the voltage to go as far, but repeated bits give more time for the change. The problem this creates is seen in the bit following the 5[th] in a row (highlighted in the oval), which fails to reach a good signal value dur‐ ing its UI because the voltage difference was too large to overcome in that short time. The difference between the value it reaches and the value it should have reached is shown by the line marking the level reached by other bits that aren’t experiencing as much ISI. 

In the lower half of the illustration, a de‐emphasized version of the signal is cap‐ tured and compared to the original. Here we can see that reducing the voltage for repeated bits prevents the voltage from charging up as much and results in a cleaner signal because the bits that follow are not influenced as much by the previous bits. For both the 2 consecutive bits and then the 5 consecutive bits, the over‐charging problem is reduced, which improves the timing jitter as well as the voltage levels. Consequently, the troublesome bit looks much better with de‐ emphasis turned on and the received signal approaches the normal voltage swing in that bit time. 

**470** 

**Chapter 13: Physical Layer - Electrical** 

_Figure 13‐17: Benefit of De‐emphasis at the Receiver_ 

**==> picture [358 x 283] intentionally omitted <==**

**----- Start of picture text -----**<br>
5 bits in a row<br>Without De [-] Emphasis<br>With De-Emphasis<br>**----- End of picture text -----**<br>


In Figure 13‐18 on page 472 both positive and negative versions of the differen‐ tial signal are shown so as to illustrate the resulting eye opening. The improved signal quality from de‐emphasis is clear because the eye opening at the trouble‐ some time in the lower trace is so much larger than the one without de‐empha‐ sis in the upper trace. 

**471** 

**PCI Ex ress Technolo p gy** 

_Figure 13‐18: Benefit of De‐emphasis at Receiver Shown With Differential Signals_ 

**==> picture [357 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Without De [-] Emphasis<br>With De-Emphasis<br>**----- End of picture text -----**<br>


## **Solution for 5.0 GT/s** 

As one might expect, increasing data rates exacerbates the problem of ISI because the bit times get progressively smaller, and more aggressive equaliza‐ tion techniques are needed. The change for 5.0 GT/s is incremental, and consists of providing three choices regarding the amount of de‐emphasis to be applied. 

1. When running at 2.5 GT/s speed, ‐3.5 dB de‐emphasis is required. 

2. When running at 5.0 GT/s speed, ‐6.0 dB de‐emphasis is recommended, while the use of ‐3.5 dB is optional. ‐6.0 dB de‐emphasis level is intended to compensate for the greater signal attenuation at higher frequency. As Fig‐ ure 13‐19 on page 473 suggests, a 3.5 dB reduction represents a 33% reduc‐ tion in voltage, while a 6 dB reduction represents a 50% reduction. To avoid a possible confusion, note that the dB measure of power and voltage are dif‐ ferent by a factor of two. A 3 dB reduction represents a 50% change in power but only a 25% change in voltage. 

**472** 

**Chapter 13: Physical Layer - Electrical** 

_Figure 13‐19: De‐emphasis Options for 5.0 GT/s_ 

**==> picture [288 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
2.5 GT/s 3.5 dB<br>de-emphasis<br>5.0 GT/s 6.0 dB<br>de-emphasis<br>**----- End of picture text -----**<br>


3. Normally, a Transmitter operates in the full‐swing mode and can use the entire available voltage range to help overcome signal attenuation. The volt‐ age needs to start out at a higher value to compensate for the loss, as shown in the top half of Figure 13‐20 on page 474. However, for 5.0 GT/s another option is provided called reduced‐swing mode. This is intended to support short, low‐loss signaling environments, as shown in the lower half of Figure 13‐20 on page 474, and reduces the voltage swing by about half to save power. This mode also provides the third de‐emphasis option by turning off de‐emphasis entirely, which makes sense because, as mentioned earlier, the signal distortion it creates would not be reduced by loss in the path and the resulting signal at the Receiver would look worse. 

**473** 

**PCI Ex ress Technolo p gy** 

_Figure 13‐20: Reduced‐Swing Option for 5.0 GT/s with No De‐emphasis_ 

**==> picture [376 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Full Swing (high transmission amplitude)<br>Tx<br>Transmitter Receiver<br>Long path<br>Rx<br>+ +<br>_<br>_<br>Reduced Swing (low transmission amplitude)<br>Short path<br>Transmitter Receiver Tx<br>Rx<br>+ +<br>_<br>_<br>**----- End of picture text -----**<br>


## **Solution for 8.0 GT/s - Transmitter Equalization** 

When going to the 8.0 GT/s data rate, the signal conditioning model changes significantly. Transmitter equalization becomes more complex and a handshake training procedure is used to adapt to the actual signaling environment rather than making assumptions about what will be needed. To learn more about the process of evaluating the Link, refer to the section called “Recovery.Equaliza‐ tion” on page 587. Basically, that process allows a Receiver to request that the Link partner’s Transmitter use a certain combination of coefficients and then the receiver tests how well the received signal looks and possibly proposes others if the result isn’t good enough. 

Sometimes students ask whether this model is really sufficient to achieve good error rates, since evaluating a signal across all the possible situations requires days of testing in the lab to achieve a BER of 10[‐15] or better. The answer to this has two parts. First, even with the handshake process, the coefficients will be an approximation that worked well when the training was done but may or may not work as well under other conditions. Extrapolation from a small sample size 

**474** 

**Chapter 13: Physical Layer - Electrical** 

is a necessary part of arriving at working values quickly and it works reason‐ ably well. Second, associated with 8 GT/s transfer rate, it’s only necessary to achieve a minimum BER of 10[‐12] , and that doesn’t take as long to verify as it would BER of 10[‐15] . 

## **Three-Tap Tx Equalizer Required** 

To accomplish better wave shaping at the Transmitter, the spec requires the use of a 3‐tap FIR (Finite Impulse Response) filter, meaning a filter with 3 bit‐time‐ spaced inputs. A conceptual drawing of this is shown in Figure 13‐21 on page 475, where it can be seen that the output voltage is the sum of three versions of the input: the original input, a version delayed by one bit time and a third delayed by another bit time. This type of FIR filter is often used in other SER‐ DES applications above 6.0 Gb/s, and it’s helpful for PCIe because it compen‐ sates for the fact that the channel spreads the signal across a longer time. Another way of thinking about it is that a given bit is affected by both the bit value that preceded it and the bit that comes after it. 

_Figure 13‐21: 3‐Tap Tx Equalizer_ 

**==> picture [371 x 157] intentionally omitted <==**

**----- Start of picture text -----**<br>
� Output<br>Tap (-1) Tap (0) Tap (+1)<br>C C C<br>-1 0 +1<br>Input<br>1 UI delay 1 UI delay<br>**----- End of picture text -----**<br>


With this in mind, the three inputs can be described by their timing position as “pre‐cursor” for C‐1, “cursor” for C0, and “post‐cursor” for C+1, which combine to create an output based on the upcoming input, the current value, and the pre‐ vious value. Adjusting the coefficients for the taps allows the output wave to be optimally shaped. This effect is illustrated by the pulse‐response waveform shown in Figure 13‐22 on page 476. Looking at a single pulse allows the adjust‐ ment to the signal to be more easily recognized. 

**475** 

**PCI Ex ress Technolo p gy** 

The filter shapes the output according to the coefficient values (or tap weights) assigned to each tap. The sum of the absolute value of the three coefficient mag‐ nitudes together is defined to be unity so that only two of them need to be given for the third one to be calculated. Consequently, only C‐1 and C+1 are given in the spec and C0 is always implied and is always positive. 

_Figure 13‐22: Tx 3‐Tap Equalizer Shaping of an Output Pulse_ 

**==> picture [294 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
V<br>Unmodified Signal<br>t<br>UI UI UI UI<br>Cursor<br>V<br>Pre-cursor<br>Post-cursor<br>reduction<br>reduction<br>Equalized Signal<br>t<br>UI UI UI UI<br>Cursor<br>**----- End of picture text -----**<br>


## **Pre-shoot, De-emphasis, and Boost** 

The effect of the coefficient values is to adjust the output voltage to create up to four different voltage levels to accommodate different signaling environments, as shown in Figure 13‐23 on page 477. This waveform was taken from a test device and shows a representative example, but the voltage levels depend on whether a Transmitter implements preshoot or de‐emphasis or both. 

The waveform shows the four general voltages to be transmitted, which are: maximum‐height (Vd), normal (Va), de‐emphasized (Vb), and pre‐shoot (Vc). 

**476** 

**Chapter 13: Physical Layer - Electrical**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

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
  1     0      1       0      0      1      1      1      1      1     0      1      0      1       0      1<br>Va Vb Vc Vd<br>**----- End of picture text -----**<br>


**477** 

**PCI Ex ress Technolo p gy** 

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



**478** 

**Chapter 13: Physical Layer - Electrical** 

## **Equalizer Coefficients** 

Presets allow a device to use one of 11 possible starting values to be used for the partner’s Transmitter coefficients when first training to the 8.0 GT/s data rate. This is accomplished by sending EQ TS1s and EQ TS2s during training which gives a coarse adjustment of Tx equalization as a starting point. If the signal using the preset delivers the desired 10[‐12] error rate, no further training is needed. But if the measured error rate is too high, the equalization sequence is used to fine‐tune the coefficient settings by trying different C‐1 and C+1 values and evaluating the result, repeating the sequence until the desired signal qual‐ ity or error rate is achieved. 

An 8.0 GT/s transmitter is required to report its range of supported coefficient values to its neighboring Receiver. There are some constraints on this: 

- Device must support all 11 presets as listed in Table 13‐1 on page 478. 

- Transmitters must meet the full‐swing VTX‐EIEOS‐FS signaling limits 

- Transmitters may optionally support the reduced‐swing, and if they do they must meet the VTX‐EIEOS‐RS limits 

- Coefficients must meet the boost limits (VTX‐BOOST‐FS = 8.0 dB min, VTX‐ BOOST‐RS[ = 2.5 dB min) and resolution limits (EQ] TX‐DOEFF‐RESS[= 1/24 max to] 1/63 min). 

Applying these constraints and using the maximum granularity of 1/24 creates a list of pre‐shoot, de‐emphasis, and boost values for each setting. This is pre‐ sented in a table in the spec that is partially reproduced from the spec here in Table 13‐2 on page 480. The table contains blank entries because the boost value can’t exceed 8.0 +/‐ 1.5 dB = 9.5 dB. That results in a diagonal boundary where the boost has reached 9.5 for the full‐swing case. For reduced swing, the bound‐ ary is at 3.5 dB. The 6 shaded entries along the left and top edges of the table that go as far as 4/24 are presets supported by full‐ or reduced‐swing signaling. The other 4 shaded entries are presets supported for full‐swing signaling only. 

**479** 

## **PCI Ex ress Technolo p gy** 

_Table 13‐2: Tx Coefficient Table_ 

|**PS   DE**<br>**Boost**|**PS   DE**<br>**Boost**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|**C+1**|
|---|---|---|---|---|---|---|---|---|
|||0/24|1/24|2/24|3/24|4/24|5/24|6/24|
|**C-1**|0/24|0.0   0.0<br>0.0|0.0  -0.8<br>0.8|0.0  -1.8<br>1.6|0.0  -2.5<br>2.5|0.0  -3.5<br>3.5|0.0  -4.7<br>4.7|0.0  -6.0-<br>6.0|
||1/24|0.8   0.0<br>0.8|0.8  -0.8<br>1.6|0.9  -1.7<br>2.5|1.0  -2.8<br>3.5|1.2  -3.9<br>4.7|1.3  -5.3<br>6.0|1.6  -6.8<br>7.6|
||2/24|1.6   0.0<br>1.6|1.7  -0.9<br>2.5|1.9  -1.9<br>3.5|2.2  -3.1<br>4.7|2.5  -4.4<br>6.0|2.9  -6.0<br>7.6|3.5  -8.0<br>9.5|
||3/24|2.5   0.0<br>2.5|2.8  -1.0<br>3.5|3.1  -2.2<br>4.7|3.5  -3.5<br>6.0|4.1  -5.1<br>7.6|4.9  -7.0<br>9.5|-|
||4/24|3.5   0.0<br>3.5|3.9  -1.2<br>4.7|4.4  -2.5<br>6.0|5.1  -4.1<br>7.6|6.0   -6.0<br>9.5|-|-|
||5/24|4.7   0.0<br>4.7|5.3  -1.3<br>6.0|6.0  -2.9<br>7.6|7.0  -4.9<br>9.5|-|-|-|
||6/24|6.0   0.0<br>6.0|6.8  -1.6<br>7.6|8.0   -3.5<br>9.5|-|-|-|-|



**Coefficient Example.** Let’s drill a little deeper on the coefficients by using preset number P7 from Table 13‐1 on page 478 as an example. In this entry, C‐1 = ‐0.100, and C+1 = ‐0.200, and since C0 must be positive and the sum of their absolute values must be one, it’s implied that C0 = 0.700. 

Matching these values to the table of coefficient space given in the spec is not straightforward because the coefficients are given as fractions rather than decimal values, but converting the fractions to their decimal values matches them pretty closely. The C‐1 value of 0.100 is closest to 2/24 (0.083), while C+1 at 0.200 is a little less than 5/24 (0.208). The coefficient table entry for those fractions is highlighted as one of the preset values, giving us some confidence that this is on the right track. In the preset table, P7 lists a pre‐ shoot value of 3.5 +/‐ 1 dB, and the value in the coefficient table is shown as 2.9 dB. If we correct for the difference in coefficient values, ((0.083/.1) * 3.5 = 2.9) we arrive at the same preshoot value. The difference in coefficient val‐ ues for de‐emphasis was much smaller (0.200 vs. 0.208) and so, as we might expect, both tables show this as ‐6.0 dB. 

**480** 

**Chapter 13: Physical Layer - Electrical** 

What voltages do the P7 coefficients create? Assuming a full‐swing voltage of Vd as a starting point then, according to the ratios in the preset table, the other voltages would be Va = 0.8Vd, Vb = 0.4Vd, and Vc = 0.6Vd. How well do those correspond to the values that would result from using the pre‐ shoot and de‐emphasis numbers? De‐emphasis was given as ‐6.0 dB, and we already know that represents a 50% voltage reduction, so we’d expect that Vb should be half of Va, which it is. Pre‐shoot was given as 3.5 dB meaning the ratio of Vc/Vb is 0.668, and 0.4/0.668 = 0.598Vd for Vc; very close to the 0.6Vd we expected. Last of all, the Boost value, which is the ratio of Vd/Vb, is not given in the preset table but, using the formula 20*log(Vd/ Vb), the boost from the preset values turns out to be 7.9 dB. That’s reason‐ ably close to the 7.6 dB value given in the coefficient table and gives us some confidence that the tables are consistent among themselves. 

So how are the four voltages obtained? There are essentially three program‐ mable drivers whose output is summed to derive the final signal value to be launched. If the cursor setting remains unchanged, and the pre‐ and post‐ cursor taps are negative, then the answer can be found by simply adding the taps as (C0 + C‐1 + C+1). 

- Vd = (C0 + C‐1 + C+1) = (0.700 + 0.100 + 0.200) = 1.0 * max voltage. This is the “boosted” value that results when a bit is both preceded and fol‐ lowed by bits of the opposite polarity. In all four voltages listed here, if the polarity of the bits is inverted then the values would all be negative. 

- — Va = (0.700 + (‐0.100) + 0.200) = 0.8 * max voltage. This is the value that results when a bit is preceded by the opposite polarity but followed by the same polarity, meaning it is the first in a repeated string of bits. 

- Vb = (0.700 + (‐0.100) + (‐0.200)) = 0.4 * max voltage. This is the de‐ emphasized value that results when a bit is both preceded and followed by bits of the same polarity, meaning it’s in the middle of a repeated string of bits. 

- Vc = (0.700 + 0.100 + (‐0.200)) = 0.6 * max voltage. This is the pre‐shoot value that results when a bit is preceded by the same polarity but fol‐ lowed by the opposite polarity, meaning it’s the last bit in a repeated string of bits. 

What determines when the coefficients are added or subtracted to arrive at these numbers? This turns out to be fairly simple, since it’s just a matter of the polarity of the time‐shifted pre‐ and post‐cursor inputs. This is illus‐ trated in Figure 13‐24 on page 482. The single‐ended waveform labeled “Weighted Cursor (C0)” shows the positive half of the differential bit stream currently being transmitted. If the waveforms are understood as shifting to the right with time, then the next lower trace (C+1) is the post‐cursor signal. 

**481** 

## **PCI Ex ress Technolo p gy** 

This version arrives one clock later and is weighted negatively by its coeffi‐ cient, causing it to be inverted. The top trace (C‐1) arrives a clock earlier than the cursor and is the pre‐cursor value that is also weighted negatively according to its own coefficient. 

Finally, the bottom trace shows the result of summing all three inputs to arrive at the final signal that is actually launched onto the wire. In the illus‐ tration, this is overlaid with the single‐ended output waveform from Figure 13‐23 on page 477 to show that it approximates a real capture fairly well. Some voltage calculations are shown from our previous example to demon‐ strate how the resulting voltages are obtained. 

_Figure 13‐24: Tx 3‐Tap Equalizer Output_ 

**==> picture [383 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
Weighted<br>Pre-Cursor<br>(C-1)<br>Weighted       1        0             1           0            0           1            1           1            1            1 0<br>Cursor (C0)<br>Weighted<br>Post-Cursor<br>(C+1)<br>Vd (0.7 + (-0.1) + (-0.2))<br>= 0.4<br>Vc<br>Va<br>Vb<br>Output<br>(C0 + C-1 + C+1) Vc<br>Va<br>Vd (-0.7 + (-0.1) + (0.2)) Vd<br>= - 0.6<br>(-0.7 + (0.1) + (-0.2))<br>(-0.7 + (-0.1) + (-0.2)) = - 0.8<br>= -1.0<br>**----- End of picture text -----**<br>


**482** 

**Chapter 13: Physical Layer - Electrical** 

The coefficient presets are exchanged before the Link changes to 8.0 GT/s, and then they may be updated during the Link equalization process (see “Recovery.Equalization” on page 587 for more details).

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

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

**483** 

**PCI Ex ress Technolo p gy** 

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

**484** 

**Chapter 13: Physical Layer - Electrical** 

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

**485** 

**PCI Ex ress Technolo p gy** 

_previous measured waveforms. To enhance the interpretation of the composite image, digital oscilloscopes can assign different colors to convey information on the number of occurrences of the waveforms that occupy the same pixel on the display, a process known as color‐grading. Modern digital sampling oscilloscopes include the ability to make a large number of automated measurements to fully characterize the various eye parameters.“_ 

## **Normal Eye Diagram** 

An ideal trace capture would paint an eye pattern that matched the outline shown in the center of Figure 13‐26 on page 486 labeled “Normal”. As long as the pattern resides entirely within that region, the Transmitter and Link are within tolerance. Note that the differential voltage parameters and values shown are peak voltages instead of the peak‐to‐peak voltages used in the spec, because only peak voltages can be represented in an eye diagram. Figure 13‐27 on page 488 shows a screen capture of a good eye diagram. 

_Figure 13‐26: Transmitter Eye Diagram_ 

**==> picture [354 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Overshoot<br>Normal<br>Minimum Eye<br>De-emphasized Eye<br>Eye Opening<br>Normal<br>Undershoot<br>Jitter Jitter<br>TTX-EYE<br>UI = Unit Interval<br>TX-DIFF-p-MAX TX-DIFFp-MIN<br>V V<br>**----- End of picture text -----**<br>


**486** 

**Chapter 13: Physical Layer - Electrical** 

## **Effects of Jitter** 

Jitter (timing uncertainty) is what happens when an edge arrives either before or after its ideal time, and acts to reduce signal integrity and close the eye open‐ ing. It’s caused by a variety of factors, from environmental effects to the data pattern in flight, to noise or signal attenuation that causes the signal’s voltage level to overshoot or undershoot the normal zone. At 2.5 GT/s this could be treated as a simple lumped effect, but at higher data rates it becomes a more sig‐ nificant issue and must be considered in several different parts. Aiming at this goal, the 8.0 GT/s data rate defines 5 different jitter values. The details of jitter analysis and minimization are beyond the scope of this book, but let’s at least define the terms the spec uses. Jitter is described as being in one of several cate‐ gories: 

1. Un‐correlated ‐ jitter that is not dependent on, or “correlated” to, the data pattern being transmitted. 

2. Rj ‐ Random jitter from unpredictable sources that are unbounded and usu‐ ally assumed to fit a Gaussian distribution. Often caused by electrical or thermal noise in the system. 

3. Dj ‐ Deterministic jitter that’s predictable and bounded in its peak‐to‐peak value. Often caused by EMI, crosstalk, power supply noise or grounding problems. 

4. PWJ ‐ Pulse Width Jitter ‐ uncorrelated, edge‐to‐edge, high‐frequency jitter. 5. DjDD ‐ Deterministic Jitter, using the Dual‐Dirac approximation. This model is a method of quickly estimating total jitter for a low BER without requiring the large sample size that would normally be needed. It uses a representative sample taken over a relatively short period (an hour or so) and extrapolates the curves to arrive at acceptable approximate values. 

6. DDj ‐ Data‐dependent jitter is a function of the data pattern being sent, and the spec states that this is mostly due to package loss and reflection. ISI is an example of DDj. 

Figure 13‐28 on page 488 shows a screen capture of a bad Eye Diagram at 2.5 GT/s. Since this is captured without de‐emphasis, the traces should all stay out‐ side the Minimum Eye area, shown on the screen by the trapezoid shape in the middle. This example illustrates that jitter can affect both edge arrival times and voltage levels, causing some trace instances to encroach on the keep‐out area of the diagram. 

**487** 

## **PCI Ex ress Technolo p gy** 

_Figure 13‐27: Rx Normal Eye (No De‐emphasis)_ 

_Figure 13‐28: Rx Bad Eye (No De‐emphasis)_ 

**488** 

**Chapter 13: Physical Layer - Electrical** 

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



**489** 

## **PCI Ex ress Technolo p gy** 

_Table 13‐3: Transmitter Specs (Continued)_ 

|**Item**|**2.5 GT/s.**|**5.0 GT/s**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|ITX‐SHORT|90|90|90|mA|Total single‐ended cur‐<br>rent Tx can supply when<br>shorted to ground.|
|VTX‐IDLE‐<br>DIFF‐AC‐P|0 (min)<br>20 (max)|0 (min)<br>20 (max)|0 (min)<br>20 (max)|mV|Peak differential voltage<br>under Electrical Idle state<br>of Link. Must include a<br>bandpass filter passing<br>frequencies from 10 KHz<br>to 1.25 GHz.|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

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



**490** 

**Chapter 13: Physical Layer - Electrical** 

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



**491** 

**PCI Ex ress Technolo p gy** 

## **Receiver Characteristics** 

## **Stressed-Eye Testing** 

Receivers are tested using a stressed eye technique, in which a signal with spe‐ cific problems is presented to the input pins and the BER is monitored. The spec presents these for 2.5 and 5.0 GT/s separately from 8.0 GT/s because of the dif‐ ference in the methods used, and then gives a third section that defines parame‐ ters common to all the speeds. 

## **2.5 and 5.0 GT/s** 

At 2.5 GT/s, the parameters are measured at the Receiver pins and there is an implied correlation between the margins observed and the BER. At 5.0 GT/s, receiver tolerancing is applied. This is a two‐step method in which a test board is calibrated to show the worst‐case signal margins as defined in the spec. Then, once the calibration is done, the test load is replaced by the device to be tested and its BER is observed. There are actually two sets of worst‐case numbers based on the clocking scheme: one is defined for the common‐clock architecture and another for the data‐clocked architecture. At higher speeds every element of the signal path must be carefully considered, and that’s true for the device package, too. The effects added to the signal by the package must be compre‐ hended in the testing process. 

The calibration channel itself must be designed with specific characteristics in mind, but the spec observes that a trace length of 28 inches on an FR4 PCB should suffice to create the necessary ISI. A signal generator is used to inject the Compliance Pattern with the appropriate jitter elements included. 

## **8.0 GT/s** 

The method for testing the stressed eye at 8.0 GT/s is similar, but there are some differences. One difference is that the signal can’t be evaluated at the device pin and so a replica channel is used to allow measuring the signal as it would appear at the pin if the device were an ideal termination. 

In order to evaluate the Receiver’s ability to perform equalization properly, it’s recommended that multiple calibration channels with different insertion loss characteristics be used so the receiver can be tested in more than one environ‐ ment. As with the transmitter at 8.0 GT/s, the calibration channel for the receiver consists of differential traces terminated at both ends with coaxial con‐ nectors. 

**492** 

**Chapter 13: Physical Layer - Electrical** 

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

**493** 

## **PCI Ex ress Technolo p gy** 

_Figure 13‐29: Rx Discrete‐Time Linear Equalizer (DLE)_ 

**==> picture [297 x 160] intentionally omitted <==**

**----- Start of picture text -----**<br>
Input<br>�<br>Received<br>S & H<br>Signal<br>C C<br>0 +1<br>1 UI delay 1 UI delay<br>**----- End of picture text -----**<br>


In contrast, CTLE is not limited to discrete time intervals and improves the sig‐ nal over a longer time interval. A simple RC network can serve as an example of a CTLE high‐pass filter, as shown in Figure 13‐30 on page 494. This serves to reduce the low‐frequency distortion caused by the channel without boosting the noise in the high‐frequency range of interest and cleans the signal for use at the next stage. Figure 13‐31 on page 495 illustrates the attenuation effect of CTLE high‐pass filter on the received low frequency component of a signal e.g. continuous 1s or continuous 0s. 

_Figure 13‐30: Rx Continuous‐Time Linear Equalizer (CTLE)_ 

**==> picture [239 x 96] intentionally omitted <==**

**----- Start of picture text -----**<br>
R<br>Channel Input<br>C<br>**----- End of picture text -----**<br>


**494** 

**Chapter 13: Physical Layer - Electrical** 

_Figure 13‐31: Effect of Rx Continuous‐Time Linear Equalizer (CTLE) on Received Signal_ 

## **Decision Feedback Equalization (DFE)** 

An example one‐tap DFE circuit like the one described in the spec is shown in Figure 13‐32 on page 495, where it can be seen that the received signal is summed with the feedback value and then fed into a data “slicer.” A slicer is an A/D circuit that takes the analog‐looking input and converts it into a clean, full‐ swing digital signal for internal use. It makes its best guess and decides whether the input is a positive or negative value and outputs either +1 or ‐1. This deci‐ sion is sent into an FIR filter with only one tap, which is just a delayed version weighted according to a coefficient setting. The output of this filter is then fed back and summed with the received signal for use as the new input to the data slicer. 

_Figure 13‐32: Rx 1‐Tap DFE_ 

**==> picture [223 x 130] intentionally omitted <==**

**----- Start of picture text -----**<br>
Output<br>Received<br>Signal<br>Slicer<br>- d1 Coefficient<br>1 UI<br>**----- End of picture text -----**<br>


**495** 

## **PCI Ex ress Technolo p gy** 

The spec only describes a single‐tap filter, but a two‐tap version is shown in Fig‐ ure 13‐33 on page 497 to illustrate another option. The motivation for including more taps is to create a cleaner output, since each tap reduces the noise for one more UI. Thus, two taps further reduce the undesirable components of the sig‐ nal, as shown in the pulse response waveform at the bottom of the drawing. This version is also shown as adaptive, meaning it’s able to modify the coeffi‐ cient values on the fly based on design‐specific criteria. 

The coefficients of the filter could be fixed, but if they’re adjustable the receiver is allowed to change them at any time as long as doing so doesn’t interfere with the current operation. In the section called “Recovery.Equalization” on page 587, Receiver Preset Hints are described as being delivered by the Down‐ stream Port to the Upstream Port on a Link, using EQ TS1s. The preset gives a hint, in terms of dB reduction, at a starting point for choosing these coefficients. 

Since the spec doesn’t require it, what the Receiver chooses to do regarding sig‐ nal compensation will be implementation specific. Industry literature states that DFE is more effective when working with an open eye, and that’s why it’s usu‐ ally employed after a linear equalizer that serves to clean up the input enough for DFE to work well. 

**496** 

**Chapter 13: Physical Layer - Electrical** 

_Figure 13‐33: Rx 2‐Tap DFE_ 

**==> picture [303 x 364] intentionally omitted <==**

**----- Start of picture text -----**<br>
Output<br>Received Slicer<br>Signal<br>�<br>Adaptive<br>Coefficient<br>� Adjustment<br>- d2 - d1<br>1 UI 1 UI<br>V<br>1st tap reduction<br>2nd tap<br>reduction<br>t<br>UI UI UI UI Rx Original<br>Cursor Rx after DFE<br>**----- End of picture text -----**<br>


## **Receiver Characteristics** 

Some selected Receiver characteristics are listed in Table 13‐5 on page 498. The Receiver Eye Diagram in Figure 13‐34 on page 499 also illustrates some of the parameters listed in the table. 

**497** 

## **PCI Ex ress Technolo p gy** 

_Table 13‐5: Common Receiver Characteristics_ 

|**Item**|**2.5 GT/**<br>**s.**|**5.0 GT/s.**|**8.0 GT/s**|**Units**|**Notes**|
|---|---|---|---|---|---|
|UI|399.88<br>(min)<br>400.12<br>(max)|199.94<br>(min)<br>200.06<br>(max)|124.9625<br>(min)<br>125.0375<br>(max)|ps|Unit Interval = bit time.|
|TRX‐EYE|0.4<br>(min)|Indirectly<br>specified||UI|Minimum eye width for a BER<br>or 10‐12. At higher rates and long<br>channels the eye is effectively<br>closed, making external mea‐<br>surement impractical.|
|VRX‐EYE|300|120 (CC)<br>100 (DC)|Not<br>specified|mVpp<br>diff|CC = common clocked, DC =<br>data clocked|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
