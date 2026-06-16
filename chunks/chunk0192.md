## **PCI Ex ress Technolo p gy** 

The Transaction layer uses this information to build a MRd TLP. The details of the TLP packet format are described later, but for now it’s enough to say that a 3 DW or 4 DW header is created depending on address size (32‐bit or 64‐bit). In addition, the Transaction Layer adds the Requester ID (bus#, device#, function#) to the header so the Completer can use that to return the completion. The TLP is placed in the appropriate virtual channel buffer to wait its turn for transmis‐ sion. Once the TLP has been selected, the Flow Control logic confirms there is sufficient space available in the neighboring device’s receive buffer (VC), and then the memory read request TLP is sent to the Data Link Layer. 

The Data Link Layer adds a 12‐bit Sequence Number and a 32‐bit LCRC value to the packet. A copy of the TLP with Sequence Number and LCRC is stored in the Replay Buffer and the packet is forwarded to the Physical Layer. 

In the Physical Layer the Start and End characters are added to the packet, which is then byte striped across the available Lanes, scrambled, and 8b/10b encoded. Finally the bits are serialized on each lane and transmitted differen‐ tially across the Link to the neighbor. 

The Completer de‐serializes the incoming bit stream back into 10‐bit symbols and passes them through the elastic buffer. The 10‐bit symbols are decoded back to bytes and the bytes from all Lanes are de‐scrambled and un‐striped. The Start and End characters are detected and removed. The rest of the TLP is for‐ warded up to the Data Link Layer. 

The Completer’s Data Link Layer checks for LCRC errors in the received TLP and checks the Sequence Number for missing or out‐of‐sequence TLPs. If there’s no error, it creates an Ack that contains the same Sequence Number that was used in the read request. A 16‐bit CRC is calculated and appended to the Ack contents to create a DLLP that is sent back to the Physical Layer which adds the proper framing symbols and transmits the Ack DLLP to the Requester. 

The Requester Physical Layer receives the Ack DLLP, checks and removes the framing symbols, and forwards it up to the Data Link Layer. If the CRC is valid, it compares the acknowledged Sequence Number with the Sequence Numbers of the TLPs stored in the Replay Buffer. The stored memory read request TLP associated with the Ack received is recognized and that TLP is discarded from the Replay Buffer. If a Nak DLLP was received by the Requester instead, it would re‐send a copy of the stored memory read request TLP. Since the DLLP only has meaning to the Data Link Layer, nothing is forwarded to the Transac‐ tion Layer. 

**82** 

**Chapter 2: PCIe Architecture Overview** 

In addition to generating the Ack, the Completer’s Link Layer also forwards the TLP up to itʹs Transaction Layer. In the Completerʹs Transaction Layer, the TLP is placed in the appropriate VC receive buffer to be processed. An optional ECRC check can be performed, and if no error is found, the contents of the header (address, Requester ID, memory read transaction type, amount of data requested, traffic class etc.) are forwarded to the Completer’s Software Layer. 