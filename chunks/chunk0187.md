## **Physical Layer - Electrical** 

The physical sender and receiver on a Link are connected with an AC‐coupled Link as shown in Figure 2‐29 on page 79. The term “AC‐coupled” simply means that a capacitor resides physically in the path between the devices and serves to pass the high‐frequency (AC) component of the signal while blocking the low‐ frequency (DC) part. Many serial transports use this approach because it allows the common mode voltage (the level at which the positive and negative versions 

**78** 

**Chapter 2: PCIe Architecture Overview** 

of the signal cross) to be different at the transmitter and receiver, meaning they’re not required to have the same reference voltage. This isn’t a big issue if the two devices are nearby and in the same box, but if they were in different buildings it would be very difficult for them to have a common reference volt‐ age that was precisely the same. 

_Figure 2‐29: Physical Layer Electrical_ 

**==> picture [347 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
CTX ZTX<br>+ +<br>ZTX ZRX<br>Transmitter Link Receiver<br>CTX ZTX ZRX<br>- -<br>ZTX<br>Zvtt Vtt<br>Transmitter is AC coupled to receiver<br>DC common-mode impedance is 50 Ohms<br>Differential impedance is 100 Ohms<br>Coupling capacitor is between 75-200 nF<br>**----- End of picture text -----**<br>