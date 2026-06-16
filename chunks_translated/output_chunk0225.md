## **Type 1 配置请求 (Configuration Request)**

当一个桥 (Bridge) 收到一个配置访问 (Configuration Request)，其目标总线号不匹配该桥的 Secondary Bus Number，但落在其 Secondary 与 Subordinate Bus Number 之间的范围内时，它将该报文作为 Type 1 Request 转发到其 Secondary Bus。不是桥的设备（即端点 Endpoint）会忽略 Type 1 Request，因为目标位于另一条总线上；而看到该报文的桥 (Bridge) 则会执行与下游总线范围的相同比较（请参见第 87 页的图 3-1 以及第 97 页的图 3-6）。

**100**

**第 3 章：配置概述 (Configuration Overview)**

- 如果目标总线匹配该桥的 secondary bus，则该报文从 Type 1 转换为 Type 0，并被传递到 secondary bus。该总线上本地的设备随后按前述方式检查报文头 (Header)。

- 如果目标总线不是该桥的 secondary bus，但是在其范围内，则该报文作为 Type 1 Request 转发到该桥的 secondary bus。

图 3-8 展示了 Type 1 配置读和写请求头 (Request Header) 格式。在两种情况下，Type 字段 = 00101，而 Fmt 字段指示该请求是读还是写。

_图 3-8：Type 1 配置读和写请求头 (Configuration Read and Write Request Headers)_

**==> picture [360 x 312] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R Attr R TH EP Attr AT Length<br>0 0 0 0 0 1 0 1 0 0 0 tr 0 0 0 0 D P 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 1 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R Attr R TH EP Attr AT Length<br>0 1 0 0 0 1 0 1 0 0 0 tr 0 0 0 0 D P 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>

**101**

**PCI Express Technology**
