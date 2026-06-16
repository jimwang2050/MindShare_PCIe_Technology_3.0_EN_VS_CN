## **PCI-X System Example** 

An example of an Intel 7500 server chipset‐based system is shown in Figure 1‐15 on page 32. The MCH chip includes three additional high‐performance Hub Link 2.0 ports that are connected to three PCI‐X Hub 2 bridges (P64H2). Each 

**31** 

**PCI Ex ress Technolo p gy** 

bridge supports two PCI‐X buses that can run at frequencies up to 133MHz. The Hub Link 2.0 can sustain the higher bandwidth requirements for PCI‐X traffic. Note that we have the same loading problem that we did for 66‐MHz PCI, resulting in a large number of buses needed to support more devices and a rela‐ tively expensive solution. The bandwidth is much higher now, though. 

_Figure 1‐15: 66 MHz/133 MHz PCI‐X Bus Based Platform_ 

**==> picture [374 x 250] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>FSB<br>PCI-X<br>P64H2<br>DDR SDRAM<br>Hub Link 2<br>Memory Controller Hub<br>P64H2 (Intel 7500 MCH) DDR SDRAM<br>Hub Link 2<br>P64H2<br>64-bit,<br>66MHz or 100MHz or 133MHz<br>Hub Link 1<br>IDE<br>Slots<br>USB IO Controller Hub PCI-33MHz<br>(ICH3)<br>LPC<br>IEEE<br>SCSI<br>AC’97 1394<br>Link<br>Boot<br>Ethernet ROM<br>**----- End of picture text -----**<br>