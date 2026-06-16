## **PCI Ex ress Technolo p gy** 

_Figure 2‐12: PCI Express Device Layers_ 

**==> picture [232 x 201] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>

Every PCIe interface supports the functionality of these layers, including Switch Ports, as shown in Figure 2‐13 on page 57. A question often came up in earlier classes as to whether a Switch Port needs to implement all the layers, since it’s typically only forwarding packets. The answer is yes, and the reason is that evaluating the contents of packets to determine their routing requires looking into the internal details of a packet, and that takes place in the Transaction Layer logic. 

**56** 

**Chapter 2: PCIe Architecture Overview** 

_Figure 2‐13: Switch Port Layers_ 

**==> picture [189 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer<br>Data Link Layer<br>Physical Layer<br>Switch<br>Core<br>**----- End of picture text -----**<br>

In principle, each layer communicates with the corresponding layer in the device on the other end of the Link. The upper two layers do so by organizing a string of bits into a packet, creating a pattern that is recognizable by the corre‐ sponding layer in the receiver. The packets are forwarded through the other lay‐ ers along the way to get to or from the Link. The Physical Layer also communicates directly with that layer in the other device but it does differently. 

Before we go deeper, let’s first walk through an overview to see how the layers interact. In broad terms, the contents of an outgoing request or completion packet from the device are assembled in the Transaction Layer based on infor‐ mation presented by the device core logic, which we also sometimes call the Software Layer (although the spec doesn’t use that term). That information would usually include the type of command desired, the address of the target device, attributes of the request, and so on. The newly created packet is then stored in a buffer called a Virtual Channel until it’s ready for passing to the next layer. When the packet is passed down to the Data Link Layer, additional infor‐ mation is added to the packet for error checking at the neighboring receiver, and a copy is stored locally so we can send it again if a transmission error occurs. When the packet arrives at the Physical Layer it’s encoded and transmit‐ ted differentially using all the available Lanes of the Link. 

**57** 

**PCI Ex ress Technolo p gy** 