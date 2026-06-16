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
