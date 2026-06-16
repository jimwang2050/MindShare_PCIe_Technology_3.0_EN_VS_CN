## **PCI-X Transactions** 

Figure 1‐16 on page 33 shows an example of a PCI‐X burst memory read trans‐ action. Note that PCI‐X does not allow Wait States after the first data phase. This is possible because the transfer size is now provided to the target device in the Attribute phase of the transaction, so the target devices knows exactly what is going to be required of him. In addition, most PCI‐X bus cycles are bursts and data is generally transferred in blocks of 128 Bytes. These features allow for more efficient bus utilization and device buffer management. 

**32** 

**Chapter 1: Background** 

_Figure 1‐16: Example PCI‐X Burst Memory Read Bus Cycle_ 

**==> picture [386 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
Idle<br>AddressPhase AttributePhase ResponsePhase PhaseData PhaseData PhaseData PhaseData TurnaroundCycle<br>1 2 3 4<br>1 2 3 4 5 6 7 8 9 10<br>CLK<br>FRAME#<br>AD[31:0] Address ATTR Data-0 Data-1 Data-2 Data-3<br>C/BE#[3:0] Cmd ATTR<br>IRDY#<br>TRDY#<br>DEVSEL# DecodeA<br>Next tolast<br>transfer<br>**----- End of picture text -----**<br>