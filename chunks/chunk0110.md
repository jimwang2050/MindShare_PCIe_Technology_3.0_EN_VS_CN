## **PCI Retry Protocol** 

When a PCI master initiates a transaction to access a target device and the target device is not ready, the target signals a transaction retry. This scenario is shown in Figure 1‐7. 

_Figure 1-7: PCI Transaction Retry Mechanism_ 

**==> picture [372 x 226] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data Port<br>1. Initiate<br>PCI 33 MHz 3. Retry<br>Slots<br>IDE<br>CD HDD<br>USB South Bridge LogicError Ethernet SCSI<br>ISA<br>Boot Modem Audio Super 2. Target device<br>ROM Chip Chip I/O not ready<br>COM1<br>COM2<br>**----- End of picture text -----**<br>

Consider the following example in which the North bridge initiates a memory read transaction to read data from the Ethernet device. The Ethernet target claims the bus cycle. However, the Ethernet target does not immediately have the data to return to the North bridge master. The Ethernet device has two choices by which to delay the data transfer. The first is to insert wait‐states in 

**21** 