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