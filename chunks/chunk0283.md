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