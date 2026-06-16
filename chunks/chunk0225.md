## **Type 1 Configuration Request** 

When a bridge sees a configuration access whose target bus number does not match its Secondary Bus Number but is in the range between its Secondary and Subordinate Bus Numbers, it forwards the packet as a Type 1 Request to its Sec‐ ondary Bus. Devices that are not bridges (Endpoints) know to ignore Type 1 Requests since the target resides on a different bus, but bridges that see it will make the same comparison of the target bus number to the range of buses downstream (see Figure 3‐1 on page 87 and Figure 3‐6 on page 97). 

**100** 

**Cha ter 3: Confi uration Overview p g** 

- If the target bus matches the Bridge’s secondary bus, the packet is converted from Type 1 to Type 0 and passed to the secondary bus. Devices local to that bus then check the packet header as previously described. 

- If the target bus is not the Bridge’s secondary bus but is within its range, the packet is forwarded to the Bridge’s secondary bus as a Type 1 Request. 

Figure 3‐8 illustrates the Type 1 configuration read and write request header formats. In both cases, the Type field = 00101, while the Fmt field indicates whether it’s a read or a write. 

_Figure 3‐8: Type 1 Configuration Read and Write Request Headers_ 

**==> picture [360 x 312] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 0 0 0 1 0 1 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 1 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 1 0 0 0 1 0 1 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>

**101** 

**PCI Ex ress Technolo p gy** 