## **General** 

When the spec writers were choosing how PCI‐X and, later, PCIe, would access Configuration space, there were two concerns. First, the 256‐byte space per Function limited vendors who wanted to put proprietary information there, as well as future spec writers who would need room for more standardized capa‐ bility structures. To solve that problem, the space was simply extended from 256 bytes to 4KB per Function. Secondly, when PCI was developed there were few multi‐processor systems in use. When there’s only one CPU and it’s only run‐ ning one thread, the fact that the old model takes two steps to generate one access isn’t a problem. But newer machines using multi‐core, multi‐threaded CPUs present a problem for the IO‐indirect model because there’s nothing to stop multiple threads from trying to access Configuration space at the same time. Consequently, the two‐step model will no longer work without some lock‐ ing semantics. With no locking semantics, once thread A writes a value into the 

**96** 

**Cha ter 3: Confi uration Overview p g** 

Configuration Address Port (CF8h), there is nothing to prevent thread B from overwriting that value before thread A can perform its corresponding access to the Configuration Data Port (CFCh). 

_Figure 3‐6: Multi‐Root System_ 

**==> picture [379 x 377] intentionally omitted <==**

**----- Start of picture text -----**<br>
Inter-Processor<br>Communications<br>Processor Processor<br>Root Complex Root Complex<br>Sec = 0 Host/PCI Sec = 64 Host/PCI<br>Sub = 9 Bridge Sub = 65 Bridge<br>Bus 0<br>Bus 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 9 P2P Device 0 Sec = 65Sub = 65 P2P<br>Bus 65<br>Bus 1 Bus 5<br>Function 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>Bus 2 P2P Bus 6 P2P Bus 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 Device 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 9<br>Function 0 Function 0 Function 0 Function 0<br>Bus 3 Bus 4 Bus 7 Bus 9<br>Device 0 Device 0 Device 0 Device 0<br>**----- End of picture text -----**<br>

**97** 