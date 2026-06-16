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
