## **Problems with the Common Clock Approach of PCI and PCI-X 1.0 Parallel Bus Model** 

An issue that becomes clear when trying to migrate a bus like PCI to higher speeds is that parallel bus designs have some inherent limitations. Figure 1‐18 on page 36 helps illustrate these. These designs use a common or distributed clock, in which data is driven out on one clock edge and latched in on the next clock edge so that the total timing budget is the time for one clock period. Natu‐ rally, the higher the frequency, the smaller the clock period and thus the smaller the timing budget. 

_Figure 1‐18: Inherent Problems in a Parallel Design_ 

**==> picture [383 x 203] intentionally omitted <==**

**----- Start of picture text -----**<br>
Flight Time<br>Transmitter<br>Receiver<br>Incorrect<br>Transmission<br>Media sampling<br>due to skew<br>Common Clock Common Clock<br>**----- End of picture text -----**<br>

The first issue to note is signal skew. When multiple data bits are sent at once, they experience slightly different delays and arrive at slightly different times at the receiver. If that difference is too large, incorrect signal sampling with clock may occur at the receiver as shown in the diagram. A second issue is clock skew between multiple devices. The arrival time of the common clock at one device is not precisely the same as the arrival time at the other which further reduces the timing budget. Finally, a third issue relates to the time it takes for the signal to 

**36** 

**Chapter 1: Background** 

propagate from a transmitter to a receiver, called the flight time. The clock period or timing budget must be greater than the signal flight time. To ensure this, the board design is required to implement signal traces that are short enough such that signal propagation delays are smaller than the clock period. In many board designs, this short signal traces may not be realistic enough to design for. 

To further improve performance in spite of these limitations, a couple of tech‐ niques can be used. First, the existing protocol can be streamlined and made more efficient. And second, the bus model can be changed to a source synchro‐ nous clocking model where the bus signal and clock (strobe) are driven at the same time on signals that experience equal propagation delay. This is the approach taken by PCI‐X 2.0 protocol. 