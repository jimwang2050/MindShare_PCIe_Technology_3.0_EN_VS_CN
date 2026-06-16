## **PCI Ex ress Technolo p gy** 

**TLP Packet Disassembly.** When the neighboring receiver sees the incom‐ ing TLP bit stream, it needs to identify and remove the parts that were added to recover the original information requested by the core logic of the transmitter. As shown in Figure 2‐17 on page 64, the Physical Layer will verify that the proper Start and End or other characters are present and remove them, for‐ warding the remainder of the TLP to the Data Link Layer. This layer first checks for LCRC and Sequence Number errors. If no errors are found, it removes those fields from the TLP and forwards it to the Transaction Layer. If the receiver is a Switch, the packet is evaluated in the Transaction Layer to find the routing information in the header of the TLP and determine to which port the packet should be forwarded. Even when it’s not the intended destination, a Switch is allowed to check and report an ECRC error if it finds one. However, it’s not allowed to modify the ECRC, so the targeted device will be able to detect the ECRC error as well. 

The target device can check ECRC errors if it’s capable and was enabled. If this is the target device and there was no error, the ECRC field is removed, leaving the header and data portion of the packet to be forwarded to the Software Layer. 

_Figure 2‐17: TLP Disassembly_ 

**==> picture [366 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
Information in core section of TLP is<br>sent to Software Layer / Device Core<br>Bit receive direction<br>Sequence<br>Start Header Data ECRC LCRC End<br>Number<br>Stripped by Transaction Layer<br>Stripped by Data Link Layer<br>Stripped by PHY Layer<br>**----- End of picture text -----**<br>

**64** 

**Chapter 2: PCIe Architecture Overview** 