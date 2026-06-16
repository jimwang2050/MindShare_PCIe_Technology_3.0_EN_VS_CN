## **Single Host System** 

The information written to the Configuration Address Port is latched by the Host/PCI bridge within the Root Complex, as shown in Figure 3‐1 on page 87. If bit 31 is 1b and the target bus is within the downstream range of bus numbers, the bridge translates a subsequent processor access targeting its Configuration Data Port into a configuration request on bus 0. The processor then initiates an IO read or write transaction to the Configuration Data Port at 0CFCh. This causes the bridge to generate a Configuration Request that is a read when the IO access to the Configuration Data Port was a read, or a Configuration write if the IO access was a write. It will be a Type 0 configuration transaction if the tar‐ get bus is bus 0, or a Type 1 for another bus within the range, or not forwarded at all if the target bus is outside of the range. 

**94** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐5: Single‐Root System_ 

**==> picture [327 x 449] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bus 0 Sec = 0 Bridge<br>Sub = 9<br>Pri = 0 Pri = 0<br>P2P Sec = 1 Device 0 Device 1 Sec = 5 P2P<br>Sub = 4 Sub = 9<br>Bus 1 Bus 1 Bus 5 Bus 5<br>Device 0 Device 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P Sec = 6<br>P2P<br>Sub = 4 Sub = 9<br>Bus 2 P2P Bus 6 P2P<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 9<br>Function 0 Function 0 Function 0 Function 0<br>Bus 3 Bus 4 Bus 7 Bus 9<br>Device 0 Device 0 Device 0 Device 0<br>**----- End of picture text -----**<br>

**95** 

**PCI Ex ress Technolo p gy** 