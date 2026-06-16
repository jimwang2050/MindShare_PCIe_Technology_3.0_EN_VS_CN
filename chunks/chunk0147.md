## **No Common Clock** 

As mentioned earlier, a common clock is not required for a PCIe Link because it uses a source‐synchronous model, meaning the transmitter supplies the clock to the receiver to use in latching the incoming data. A PCIe Link does not include a forwarded clock. Instead, the transmitter embeds the clock into the data stream using 8b/10b encoding. The receiver then recovers the clock from the data stream and uses it to latch the incoming data. As mysterious as this might sound, the process by which this is done is actually fairly straightforward. In the receiver, a PLL circuit (Phase‐Locked Loop, see Figure 2‐5 on page 45) takes the incoming bit stream as a reference clock and compares its timing, or phase, to that of an output clock that it has created with a specified frequency. Based on the result of that comparison, the output clock’s frequency is increased or decreased until a match is obtained. At that point the PLL is said to be locked, and the output (recovered) clock frequency precisely matches the clock that was used to transmit the data. The PLL continually adjusts the recovered clock, so changes in temperature or voltage that affect the transmitter clock frequency will always be quickly compensated. 

One thing to note regarding clock recovery is that the PLL does need transitions on the input in order to make its phase comparison. If a long time goes by with‐ out any transitions in the data, the PLL could begin to drift away from the cor‐ rect frequency. To prevent that problem, one of the design goals of 8b/10b encoding is ensure no more than 5 consecutive ones or zeroes in a bit‐stream (to learn more on this, refer to “8b/10b Encoding” on page 380). 

_Figure 2‐5: Simple PLL Block Diagram_ 

**==> picture [350 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
Reference<br>(incoming Recovered<br>bitstream) DetectorPhase Lo op Filter Voltage-Controlled Clock<br>Oscillator<br>Divide by N Counter<br>(to create multiples of<br>reference frequency)<br>**----- End of picture text -----**<br>

**45** 

**PCI Ex ress Technolo p gy** 

Once the clock has been recovered it’s used to latch the bits of the incoming data stream into the deserializer. Sometimes students wonder whether this recov‐ ered clock can be used to clock all the logic in the receiver, but it turns out that the answer is no. One reason is that a receiver can’t count on this reference always being present, because low power states on the Link involve stopping data transmission. Consequently, the receiver must also have it’s own internal clock that can be locally generated. 