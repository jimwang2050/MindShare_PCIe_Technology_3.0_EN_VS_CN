## **Physical Layer - Logical** 

TLPs and DLLPs from the Data Link Layer are clocked into a buffer in the Phys‐ ical Layer, where Start and End characters are added to facilitate detection of the packet boundaries at the receiver. Since the Start and End characters appear on both ends of a packet they are also called “framing” characters. The framing characters are shown appended to a TLP and DLLP in Figure 2‐28 on page 77, which also shows the size of each field. 

_Figure 2‐28: TLP and DLLP Structure at the Physical Layer_ 

**==> picture [366 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Start Sequence Header Data Payload  ECRC LCRC End<br>1B 2B 3-4 DW 0-1024 DW 1DW 1DW 1B<br>DLLP<br>Start DLLP Type Misc. CRC End<br>1B 2B 1B<br>1DW<br>**----- End of picture text -----**<br>

Within this layer, each byte of a packet is split out across all of the lanes in use for the Link in a process called byte striping. Effectively, each lane operates as an independent serial path across the Link and their data is all aggregated back together at the receiver. Each byte is scrambled to reduce repetitive patterns on the transmission line and reduce EMI (electro‐magnetic interference) seen on the Link. For the first two generations of PCIe (Gen1 and Gen2 PCIe), the 8‐bit characters are encoded into 10‐bit “symbols” using what is called 8b/10b encod‐ ing logic. This encoding adds overhead to the outgoing data stream, but also adds a number of useful characteristics (for more on this, see “8b/10b Encod‐ ing” on page 380). Gen3 Physical Layer logic when transmitting at Gen3 speed, does not encode the packet bytes using 8b/10b encoding. Rather another encod‐ ing scheme referred to as 128b/130b encoding is employed with the packet bytes scrambled transmitted. The 10b symbols on each Lane (Gen1 and Gen2) or the packet bytes on each Lane (Gen3) are then serialized and clocked out differen‐ tially on each Lane of the Link at 2.5 GT/s (Gen1), or 5 GT/s (Gen2) or 8 GT/s (Gen3). 

**77** 