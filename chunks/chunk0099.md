## **PCI Bus Initiator and Target** 

In a PCI hierarchy each device on the bus may contain up to eight functions that all share the bus interface for that device, numbered 0‐7 (a single‐function device is always assigned function number 0). Every function is capable of act‐ ing as a target for transactions on the bus, and most will also be able to initiate transactions. Such an initiator (called a Bus Master) has a pair of pins (REQ# and GNT#) dedicated to arbitrating for use of the shared PCI bus. As shown in Fig‐ ure 1‐2 on page 13, a Request (REQ#) pin indicates that the master needs to use the bus and is sent to the bus arbiter for evaluation against all the other requests at that moment. The arbiter is often located in the bridge that is hierarchically above the bus and receives arbitration requests from all the devices that can act as initiators (Bus Masters) on that bus. The arbiter decides which requester should be the next owner of the bus and asserts the Grant (GNT#) pin for that device. According to the protocol, whenever the previous transaction finishes and the bus goes idle, whichever device sees its GNT# asserted at that time is designated as the next Bus Master and can begin its transaction. 

**12** 

**Chapter 1: Background** 

_Figure 1‐2: PCI Bus Arbitration_ 

**==> picture [384 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data PortArbiter<br>PCI 33 MHz<br>Slots<br>IDE<br>CD HDD<br>USB South Bridge LogicError Ethernet SCSI REQ#<br>GNT#<br>ISA Pair<br>Boot Modem Audio Super<br>ROM Chip Chip I/O<br>COM1<br>COM2<br>**----- End of picture text -----**<br>