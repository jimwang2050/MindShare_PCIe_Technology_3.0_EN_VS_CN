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
