## _Figure 2‐14: Detailed Block Diagram of PCI Express Device’s Layers_ 

**==> picture [338 x 344] intentionally omitted <==**

**----- Start of picture text -----**<br>
Memory, I/O, Configuration Requests, Message Requests or Completions<br>“Software (Software layer sends / receives address, transaction type, data)<br>Layer”<br>Transmit Receive<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload ECRC Header Data Payload ECRC<br>Transaction<br>Transmit Flow Control Receive<br>Layer Buffers Buffers<br>(VCs) Virtual Channel<br>(VCs)<br>Management<br>VC Arbitration Ordering<br>Link Packet DLLPs e.g. DLLPs Link Packet<br>Sequence TLP LCRC Ack/Nak CRC Ack/Nak CRC Sequence TLP LCRC<br>Data Link<br>TLP Retry De-mux<br>Layer Buffer<br>TLP Error<br>Mux Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Physical Encode Decode<br>Layer<br>Parallel-to-Serial Serial-to-Parallel<br>Link<br>Differential Driver Training Differential Receiver<br>Port<br>Link<br>**----- End of picture text -----**<br>

The receiver decodes the incoming bits in the Physical Layer, checks for errors that can be seen at this level and, if there are none, forwards the resulting packet up to the Data Link Layer. Here the packet is checked for different errors and, if there are no errors, is forwarded up to the Transaction Layer. The packet is buff‐ ered, checked for errors, and disassembled into the original information (com‐ mand, attributes, etc.) so the contents can be delivered to the device core of the receiver. Next, let’s explore in greater depth what each of the layers must do to make this process work, using Figure 2‐14 on page 58. We start at the top. 

**58** 

**Chapter 2: PCIe Architecture Overview** 