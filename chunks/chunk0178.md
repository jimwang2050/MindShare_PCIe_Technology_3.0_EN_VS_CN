## **Ack/Nak Protocol** 

The error correction function, illustrated in Figure 2‐25 on page 74, is provided through a hardware‐based automatic retry mechanism. As shown in Figure 2‐26 on page 75, an LCRC and Sequence Number are added to each outgoing TLP and checked at the receiver. The transmitter’s Replay Buffer holds a copy of every TLP that has been sent until receipt at the neighboring device has been confirmed. That confirmation takes the form of an Ack DLLP (positive acknowl‐ edgement) sent by the Receiver with the Sequence Number of the last good TLP it has seen. When the Transmitter sees the Ack, it flushes the TLP with that Sequence Number out of the Replay Buffer, along with all the TLPs that were sent before the one that was acknowledged. 

If the Receiver detects a TLP error, it drops the TLP and returns a Nak to the Transmitter, which then replays all unacknowledged TLPs in hopes of a better result the next time. Since detected errors are almost always transient events, a replay will very often correct the problem. This process is often referred to as the Ack/Nak protocol. 

_Figure 2‐25: Data Link Layer Replay Mechanism_ 

**==> picture [314 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
From To<br>Transaction Layer Transaction Layer<br>Tx Rx<br>Data Link Layer<br>Link Packet DLLP DLLP Link Packet<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux<br>Error<br>Mux Check<br>Tx Rx<br>Link<br>**----- End of picture text -----**<br>

**74** 

**Chapter 2: PCIe Architecture Overview** 

_Figure 2‐26: TLP and DLLP Structure at the Data Link Layer_ 

**==> picture [368 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Sequence ID Header Data Payload  ECRC LCRC<br>AND<br>DLLP<br>DLLP Type Misc. CRC<br>**----- End of picture text -----**<br>

The basic form of a DLLP is also shown in Figure 2‐26 on page 75, and consists of a 4‐byte DLLP type field that may include some other information and a 2‐ byte CRC. 

Figure 2‐27 on page 76 shows an example of a memory read going across a Switch. In general, the steps for this case would be as follows: 

1. **Step 1a** : Requester sends a memory read request and saves a copy in its Replay Buffer. Switch receives the MRd TLP and checks the LCRC and Sequence Number. 

   - Step 1b: No error is seen, so the Switch returns an Ack DLLP to Requester. In response, Requester discards its copy of the TLP from the Replay Buffer. 

2. **Step 2a** : Switch forwards the MRd TLP to the correct Egress Port using memory address for its routing and saves a copy in the Egress Port’s Replay Buffer. The Completer receives the MRd TLP and checks for errors. **Step 2b** : No error is seen, so the Completer returns an Ack DLLP to the Switch. Switch Port purges its copy of the MRd TLP from its Replay Buffer. 

3. **Step 3a** : As the final destination of the request, the Completer checks the optional ECRC field in MRd TLP. No errors are seen so the request is passed to the core logic. Based on the command, the device fetches the requested data and returns a Completion with Data TLP (CplD) while saving a copy in its Replay Buffer. Switch receives CplD TLP and checks for errors. **Step 3b** : No error is seen, so the Switch returns an Ack DLLP to the Compl‐ eter. Completer discards its copy of the CplD TLP from its Replay Buffer. 

4. **Step 4a** : Switch decodes the Requester ID field in CplD TLP and routes the packet to the correct Egress Port, saving a copy in the Egress Port’s Replay Buffer. Requester receives CplD TLP and checks for errors. **Step 4b** : No error is seen, so the Requester returns Ack DLLP to Switch. Switch discards its copy of the CplD TLP from its Replay Buffer. Requester checks the optional ECRC field and finds no error, so data is passed up to the core logic. 

**75** 