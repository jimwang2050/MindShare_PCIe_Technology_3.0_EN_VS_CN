## **Differential Signals** 

Each Lane uses differential signaling, sending both a positive and negative ver‐ sion (D+ and D‐) of the same signal as shown in Figure 2‐4 on page 44. This dou‐ bles the pin count, of course, but that’s offset by two clear advantages over single‐ended signaling that are important for high speed signals: improved noise immunity and reduced signal voltage. 

The differential receiver gets both signals and subtracts the negative voltage from the positive one to find the difference between them and determine the value of the bit. Noise immunity is built in to the differential design because the paired signals are on adjacent pins of each device and their traces must also be routed very near each other to maintain the proper transmission line imped‐ ance. Consequently, anything that affects one signal will also affect the other by about the same amount and in the same direction. The receiver is looking at the difference between them and the noise doesn’t really change that difference, so the result is that most noise affecting the signals doesn’t affect the receiver’s ability to accurately distinguish the bits. 

_Figure 2‐4: Differential Signaling_ 

**==> picture [301 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
V+<br>D+<br>V<br>cm<br>Receiver subtracts<br>D- from D+ value to<br>arrive at differential<br>D- voltage.<br>V<br>cm<br>V-<br>**----- End of picture text -----**<br>

**44** 

**Chapter 2: PCIe Architecture Overview** 