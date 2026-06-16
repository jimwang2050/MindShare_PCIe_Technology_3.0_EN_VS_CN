## **PCI Ex ress Technolo p gy** 

_Figure 3‐7: Type 0 Configuration Read and Write Request Headers_ 

**==> picture [364 x 311] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 0 0 0 1 0 0 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 0 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 1 0 0 0 1 0 0 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>