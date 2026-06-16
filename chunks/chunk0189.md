## **PCI Ex ress Technolo p gy** 

_Figure 2‐30: Ordered Sets Origin and Destination_ 

**==> picture [339 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Ordered Set Physical Layer Physical Layer Ordered Set<br>Transmitted Received<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>

Ordered Sets are used in the Link Training process, as described in Chapter 14, entitled ʺLink Initialization & Training,ʺ on page 505. They’re also used to com‐ pensate for the slight differences between the internal clocks of the transmitter and receiver, a process called clock tolerance compensation. Finally, Ordered Sets are used to indicate entry into or exit from a low power state on the Link. 

_Figure 2‐31: Ordered‐Set Structure_ 

**==> picture [205 x 73] intentionally omitted <==**

**----- Start of picture text -----**<br>
COM Identifier Identifier Identifier<br>**----- End of picture text -----**<br>

**80** 

**Chapter 2: PCIe Architecture Overview** 