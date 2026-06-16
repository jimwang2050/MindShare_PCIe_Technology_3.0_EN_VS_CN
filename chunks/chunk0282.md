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
