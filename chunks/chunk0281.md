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
