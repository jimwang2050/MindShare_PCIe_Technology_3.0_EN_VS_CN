## **Completion with Data** 

For the second half of this discussion, refer to Figure 2‐33 on page 83. To service the memory read request, the Completer Device Core/Software Layer sends a completion with data (CplD) request down to its Transaction Layer that includes the Requester ID and Tag copied from the original memory read request, transaction type, other parts of the completion header contents and the requested data. 

_Figure 2‐33: Completion with Data Phase_ 

**==> picture [374 x 257] intentionally omitted <==**

**----- Start of picture text -----**<br>
Requester Completer<br>Receive Completion with Data Software layer Send Completion with Data<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Flow Control Transaction layer Flow Control<br>Virtual Channel Receive Virtual Channel Transmit<br>Management Buffers Management Buffers<br>per VC per VC<br>Ordering Ordering<br>Link Packet DLLP<br>Link Packet<br>Sequence TLP LCRC Sequence TLP LCRC Nak<br>Data Link layer<br>DLLP Error Retry Buffer<br>Ack/Nak CRC Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Decode Physical layer Encode<br>Serial-to-Parallel Parallel-to-Serial<br>Differential Receiver Differential Driver<br>Port Port<br>CplD TLP<br>Link<br>Ack or Nak<br>**----- End of picture text -----**<br>

**83** 