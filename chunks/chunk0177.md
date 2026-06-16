## **DLLPs (Data Link Layer Packets)** 

DLLPs are transferred between Data Link Layers of the two neighboring devices on a Link. The Transaction Layer is not even aware of these packets, which only travel between neighboring devices and are not routed anywhere else. They are small (always just 8 bytes) compared to TLPs, and that’s a good thing because they represent overhead for maintaining Link protocol. 

_Figure 2‐24: DLLP Origin and Destination_ 

**==> picture [375 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>Device Device<br>Core Core<br>Transaction Transaction<br>Flow Control,  Layer  Layer<br>Ack/Nak, Etc.<br>(1) Data Data (4)<br>DLLP Core CRC Link Layer Link Layer DLLP Core CRC<br>(2) (2) (3) (3)<br>SDP DLLP Core CRC END Physical Physical SDP DLLP Core CRC END<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>**----- End of picture text -----**<br>

**DLLP Assembly.** As shown in Figure 2‐24 on page 73, a DLLP originates at the Data Link Layer of the transmitter and is consumed by the Data Link Layer of the receiver. A 16‐bit CRC is added to the DLLP Core to check for errors at the receiver. The DLLP contents are forwarded to the Physical Layer which appends a Start and End character to the packet (for the first two generations of PCIe), and then encodes and differentially transmits it over the Link using all the available lanes. 

**DLLP Disassembly.** When a DLLP is received by the Physical Layer, the bit stream is decoded and the Start and End frame characters are removed. The rest of the packet is forwarded to the Data Link Layer, which checks for CRC errors and then takes the appropriate action based on the packet. The Data Link Layer is the destination for the DLLP, so it isn’t forwarded up to the Transaction Layer. 

**73** 

**PCI Ex ress Technolo p gy** 