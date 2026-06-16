## **PCI Ex ress Technolo p gy** 

_Figure 2‐15: TLP Origin and Destination_ 

**==> picture [290 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>TransmittedTLP Transaction Layer Transaction Layer ReceivedTLP<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>

**TLP Packet Assembly.** An illustration of the parts of a finished TLP as it is sent over the Link is shown in Figure 2‐16 on page 63, where it can be seen that different parts of the packet are added in each of the layers. To make it easier to recognize how the packet gets constructed, the different parts of the TLP are color coded to indicate which layer is responsible for them: red for Transaction Layer, blue for Data Link Layer, and green for the Physical Layer. 

The device core sends the information required to assemble the core section of the TLP in the Transaction Layer. Every TLP will have a header, although some, like a read request, won’t contain data. An optional End‐to‐End CRC (ECRC) field may be calculated and appended to the packet. CRC stands for Cyclic Redundancy Check (or Code) and is employed by almost all serial architectures for the simple reason that it’s simple to implement and provides very robust error detection capability. The CRC also detects “burst errors,” or string of repeated mistaken bits, up to the length of the CRC value (32 bits for PCIe). Since this type of error is likely to be encountered when sending a long string of bits, this characteristic is very useful for serial transports. The ECRC field is passed unchanged through any service points (“service point” usually refers to a Switch or Root Port that has TLP routing options) between the sender and receiver of the packet, making it useful for verifying at the destination that there were no errors anywhere along the way. 

**62** 

**Chapter 2: PCIe Architecture Overview** 

For transmission, the core section of the TLP is forwarded to the Data Link Layer, which is responsible to append a Sequence Number and another CRC field called the Link CRC (LCRC). The LCRC is used by the neighboring receiver to check for errors and report the results of that check back to the trans‐ mitter for every packet sent on that Link. The thoughtful reader may wonder why the ECRC would be helpful if the mandatory LCRC check already verifies error‐free transmission across the Link. The reason is that there is still a place where transmission errors aren’t checked, and that is within devices that route packets. A packet arrives and is checked for errors on one port, the routing is checked, and when it’s sent out on another port a new LCRC value is calculated and added to it. The internal forwarding between ports could encounter an error that isn’t checked as part of the normal PCIe protocol, and that’s why ECRC is helpful. 

Finally, the resulting packet is forwarded to the Physical Layer where other characters are added to the packet to let the receiver know what to expect. For the first two generations of PCIe, these were control characters added to the beginning and end of the packet. For the third generation, control characters are no longer used but other bits are appended to the blocks that give the needed information about the packets. The packet is then encoded and differentially transmitted on the Link using all of the available lanes. 

_Figure 2‐16: TLP Assembly_ 

**==> picture [278 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Information in core section of TLP comes<br>from Software Layer / Device Core<br>Bit transmit direction<br>Sequence<br>Start Header Data ECRC LCRC End<br>Number<br>Created by Transaction Layer<br>Appended by Data Link Layer<br>Appended by PHY Layer<br>**----- End of picture text -----**<br>

**63** 