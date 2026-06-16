## **Introduction to Device Layers** 

PCIe defines a layered architecture as illustrated in Figure 2‐12 on page 56. The layers can be considered as being logically split into two parts that operate inde‐ pendently because they each have a transmit side for outbound traffic and a receive side for inbound traffic. The layered approach has some advantages for hardware designers because, if the logic is partitioned carefully, it can be easier to migrate to new versions of the spec by changing one layer of an existing design while leaving the others unaffected. Even so, it’s important to note that the layers simply define interface responsibilities and a design is not required to be partitioned according to the layers to be compliant with the spec. The goal in 

**54** 

**Chapter 2: PCIe Architecture Overview** 

this section is to describe the responsibilities of each layer and the flow of events involved in accomplishing a data transfer. 

The device layers as shown in Figure 2‐12 on page 56 consist of: 

- **Device core and interface to Transaction Layer.** The core implements the main functionality of the device. If the device is an endpoint, it may consist of up to 8 functions, each function implementing its own configuration space. If the device is a switch, the switch core consists of packet routing logic and an internal bus for accomplishing this goal. If the device is a root, the root core implements a virtual PCI bus 0 on which resides all the chipset embedded endpoints and virtual bridges. 

- **Transaction Layer.** This layer is responsible for Transaction Layer Packet (TLP) creation on the transmit side and TLP decoding on the receive side. This layer is also responsible for Quality of Service functionality, Flow Con‐ trol functionality and Transaction Ordering functionality. All these four Transaction Layer functions are described in book **Part two** . 

- **Data Link Layer.** This layer is responsible for Data Link Layer Packet (DLLP) creation on the transmit side and decoding on the receive side. This layer is also responsible for Link error detection and correction. This Data Link Layer function is referred to as the Ack/Nak protocol. Both these Data Link Layer functions are described in book **Part Three** . 

- **Physical Layer.** This layer is responsible for Ordered‐Set packet creation on the transmit side and Ordered‐Set packet decoding on the receive side. This layer processes all three types of packets (TLPs, DLLPs and Ordered‐Sets) to be transmitted on the Link and processes all types of packets received from the Link. Packets are processed on the transmit side by byte striping logic, scramblers, 8b/10b encoders (associated with Gen1/Gen2 protocol) or 128b/130b encoders (associated with Gen3 protocol) and packet serializers. The packet is finally differentially clocking out on all Lanes at the trained Link speed. On the receive Physical Layer, packet processing consists of serially receiving differentially encoded bits and converting to digital for‐ mat and then deserializing the incoming bit‐stream. The is done at a clock rate derived from a recovered clock from the CDR (Clock and Data Recov‐ ery) circuit. The received packets are processed by elastic buffers, 8b/10b decoders (associated with Gen1/Gen2 protocol) or 128b/130b decoders (associated with Gen3 protocol), de‐scramblers and byte un‐striping logic. Finally, the Link Training and Status State Machine (LTSSM) of the Physical Layer is responsible for Link Initialization and Training. All these Physical Layer functions are described in book **Part Four** . 

**55** 