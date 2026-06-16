## **PCIe Functions** 

As previously discussed Functions are designed into every Device. These Func‐ tions may include hard drive interfaces, display controllers, ethernet control‐ lers, USB controllers, etc. Devices that have multiple Functions do not need to be implemented sequentially. For example, a Device might implement Func‐ tions 0, 2, and 7. As a result, when configuration software detects a multifunc‐ tion device, each of the possible Functions must be checked to learn which of them are present. Each Function also has its own configuration address space that is used to setup the resources associated with the Function. 

**86** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐1: Example System_ 

**==> picture [344 x 462] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Host/PCI<br>Bridge<br>Bus 0<br>Bus 0 Bus 0 Bus 0<br>Virtual Dev 0 Dev 1 Virtual Dev 2 Integr.<br>P2P Func 0 Func 0 P2P Func 0 EP<br>Bus 1 Bus 1 Bus 5 Bus 5<br>Dev 0 Bus 2 Bus 6 Dev 0<br>Func 0 Dev 2 Dev 1 Func 0<br>Bus 6<br>Func 0 Func 0<br>Dev 2<br>Bus 2 Func 0<br>Dev 1<br>Virtual<br>Func 0 Virtual<br>P2P<br>P2P<br>Bus 2 Bus 6 Bus 6<br>Dev 3<br>Virtual Virtual Virtual Virtual Virtual Func 0<br>P2P P2P P2P P2P P2P<br>Bus 3<br>Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 1 Function 0 Function 0 Function 0<br>Dev 0 Dev 0 Dev 0 Dev 0<br>Bus 8<br>Dev 0<br>Express Func 0<br>PCI<br>Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>Dev 1 Dev 2 Dev 3<br>Func 0 Func 0 Func 0<br>**----- End of picture text -----**<br>

**87** 

**PCI Ex ress Technolo p gy** 