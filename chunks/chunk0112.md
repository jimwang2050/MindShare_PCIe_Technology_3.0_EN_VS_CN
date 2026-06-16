## **PCI Disconnect Protocol** 

When a PCI master initiates a transaction to access a target device and if the tar‐ get device is able to transfer at least one doubleword of data but cannot com‐ plete the entire data transfer, it disconnects the transaction at the point at which it cannot continue. This scenario is illustrated in Figure 1‐8 on page 23. 

Consider the following example in which the North bridge initiates a burst memory read transaction to read data from the Ethernet device. The Ethernet target device claims the bus cycle and transfers some data, but then runs out of data to transfer. The Ethernet device has two choices to delay the data transfer. The first option is to insert wait‐states during the current data phase while wait‐ ing for additional data to arrive. If the target needs to insert only a few wait‐ states, then the data is still transferred efficiently. If however the target device requires more time (the PCI specification allows maximum of 8 clocks in the data phase), then the target device must signal a disconnect. To do this the tar‐ get asserts STOP# in the middle of the bus cycle to tell the master to end the bus cycle prematurely. A disconnect results in some data transferred, while a retry does not. Disconnect frees the bus from long periods of wait states. The discon‐ nected master waits a minimum of 2 clocks before once again arbitrating for use of the bus and continuing the bus cycle at the disconnected address. During the time that the Bus Master is disconnected, the arbiter may grant the bus to other requesting masters so that the PCI bus is utilized more efficiently. By the time the disconnected master is granted the bus and continues the bus cycle, hope‐ fully the target is ready to continue the data transfer until it is completed. Oth‐ erwise, the target once again retries or disconnects the master’s bus cycle and the process is repeated until the master successfully transfers all its data. 

**22** 

**Chapter 1: Background** 

_Figure 1-8: PCI Transaction Disconnect Mechanism_ 

**==> picture [352 x 214] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data Port<br>1. Initiate<br>3. Disconnect<br>PCI 33 MHz<br>Slots<br>IDE<br>CD HDD<br>USB South Bridge LogicError Ethernet SCSI<br>ISA<br>2. Some data<br>Boot Modem Audio Super<br>ROM Chip Chip I/O transferred<br>COM1<br>COM2<br>**----- End of picture text -----**<br>