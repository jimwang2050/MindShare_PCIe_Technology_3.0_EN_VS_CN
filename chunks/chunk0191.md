## **Memory Read Request** 

For the first part of the discussion, refer to Figure 2‐32 on page 81. The Requester’s Device Core or Software Layer sends a request to the Transaction Layer and includes the following information: 32‐bit or 64‐bit memory address, transaction type, amount of data to read calculated in dwords, traffic class, byte enables, attributes etc. 

_Figure 2‐32: Memory Read Request Phase_ 

**==> picture [365 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
Requester Completer<br>Send Memory Read Request Software layer Receive Memory Read Request<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header ECRC Header ECRC<br>Flow Control Transaction layer Flow Control<br>Virtual Channel Transmit Virtual Channel Receive<br>Management Buffers Management Buffers<br>per VC per VC<br>Ordering Ordering<br>Link Packet DLLP<br>Link Packet<br>Sequence TLP LCRC Nak Sequence TLP LCRC<br>Data Link layer<br>Retry Buffer DLLP. Error<br>Ack/Nak CRC Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Encode Physical layer Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Differential Driver Differential Receiver<br>Port Port<br>Ack or Nak<br>Link<br>MRd TLP<br>**----- End of picture text -----**<br>

**81** 