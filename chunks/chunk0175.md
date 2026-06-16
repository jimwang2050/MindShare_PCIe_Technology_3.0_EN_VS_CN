## **Flow Control** 

A typical protocol used by serial transports is to require that a transmitter only send a packet to its neighbor if there is sufficient buffer space to receive it. That cuts down on performance‐wasting events on the bus like the disconnects and retries that PCI allowed and thus removes that class of problems from the trans‐ port. The trade‐off is that the receiver must report its buffer space often enough to avoid unnecessary stalls and that reporting takes a little bandwidth of its own. In PCIe this reporting is done with DLLPs (Data Link Layer Packets), as we’ll see in the next section. The reason is to avoid a possible deadlock condi‐ tion that might occur if TLPs were used, in which a transmitter can’t get a buffer size update because its own receive buffer is full. DLLPs can always be sent and received regardless of the buffer situation, so that problem is avoided. This flow control protocol is automatically managed at the hardware level and is trans‐ parent to software. 

_Figure 2‐23: Flow Control Basics_ 

**==> picture [292 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
Buffer space available<br>TLP<br>Transmitter Receiver<br>Transmitter VC BufferReceiver<br>Flow Control DLLP<br>**----- End of picture text -----**<br>

As shown in Figure 2‐23 on page 72, the Receiver contains the VC Buffers that hold received TLPs. The Receiver advertises the size of those buffers to the Transmitters using Flow Control DLLPs. The Transmitter tracks the available space in the Receiverʹs VC Buffers and is not allowed to send more packets than the Receiver can hold. As the Receiver processes the TLPs and removes them from the buffer, it periodically sends Flow Control Update DLLPs to keep the Transmitter up‐to‐date regarding the available space. To learn more about this, see Chapter 6, entitled ʺFlow Control,ʺ on page 215. 