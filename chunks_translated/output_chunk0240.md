|TH<br>(TLP Processing Hints)|Byte 1 Bit 0|指示是否已包含 TLP Hints。有关这些 hints 的讨论，请参见第 899 页 "TPH (TLP Processing Hints)"。|
|---|---|---|

**189**

## **PCI Express Technology**

*Table 5‐5: 4DW Memory Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**||**Function**|
|---|---|---|---|
|TD<br>(TLP Digest)|Byte 2 Bit 7||如果为 1，则该 TLP 包含可选的 TLP Digest 字段。<br>一些规则：<br>所有接收方必须使用此位检查 Digest 字段是否存在<br>• TD = 1 但没有 Digest 字段的 TLP 将被视为 Malformed<br>• 如果设置了 TD 位，则接收方必须在启用时执行 ECRC 检查<br>• 如果接收方不支持可选的 ECRC 检查，则必须忽略 digest 字段|
|EP<br>(Poisoned Data)|Byte 2 Bit 6||如果为 1，则尽管事务被允许正常完成，但伴随此包的数据应被视为有错误。|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4||Bit 5=Relaxed ordering<br>。<br>当设置为 = 1 时，启用此 TLP 的 PCI‐X 宽松排序。否则使用严格的 PCI 排序。<br>Bit 4=No Snoop<br>。<br>如果为 1，则系统硬件不需要为此 TLP 触发处理器缓存窥探以保证一致性。否则需要缓存窥探。|
|Address Type [1:0]|Byte 2 Bit 3:2||此字段支持虚拟化系统的地址转换。转换协议在名为_Address Translation Services_的单独规范中描述，可以看到该字段编码如下：<br>00 = Default/Untranslated<br>01 = Translation Request<br>10 = Translated<br>11 = Reserved|

**190**

**Chapter 5: TLP Elements**

*Table 5‐5: 4DW Memory Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|TLP 数据负载传输大小，以 DW 为单位。最大为 1024 DW (4KB)，编码为：<br>00 0000 0001b = 1DW<br>00 0000 0010b = 2DW<br>.<br>.<br>11 1111 1111b = 1023 DW<br>00 0000 0000b = 1024 DW|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识 Requester 的完成返回地址：<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|这些标识 Requester 发出的每个未完成请求。默认仅使用位 4:0，允许同时进行 32 个请求。如果 Control 寄存器中的 Extended Tag 位被设置，则可以使用全部 8 位（256 个 tag）。|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|这些限定传输的最后一个 DW 中的字节。|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|这些限定数据负载的第一个 DW 中的字节。|
|Address [63:32]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0<br>Byte 10 Bit 7:0<br>Byte 11 Bit 7:0|内存传输的 64 位起始地址的高 32 位。|
|Address [31:2]|Byte 12 Bit 7:0<br>Byte 13 Bit 7:0<br>Byte 14 Bit 7:0<br>Byte 15 Bit 7:2|内存传输的 64 位起始地址的低 32 位。地址的低 2 位被保留，强制为 DW 对齐的起始地址。|

**191**

## **PCI Express Technology**

**Memory Request Notes.** 内存请求的特性包括：

1. 内存数据传输不允许跨越 4KB 边界。

2. 所有内存映射写都是 Posted（已发布）以提升性能。

3. 可以使用 32 位或 64 位寻址。

4. 数据负载大小在 0 到 1024 DW (0‐4KB) 之间。

5. 可以使用 QoS 特性，包括最多 8 个 Traffic Class。

6. 当事务目标是主内存时，可以使用 No Snoop 属性来免除系统窥探处理器缓存的需要。

7. 可以使用 Relaxed Ordering 属性来允许包路径中的设备应用宽松排序规则，以期提高性能。

## **Configuration Requests**

PCI Express 使用与 PCI 相同的 Type 0 和 Type 1 配置请求来保持向后兼容性。Type 1 周期向下游传播，直到到达其 secondary bus 与目标 bus 匹配的桥为止。在那时，配置事务由该桥从 Type 1 转换为 Type 0。桥根据先前编程的总线号寄存器（Primary、Secondary 和 Subordinate Bus Numbers）知道何时转发和转换配置周期。有关此主题的更多信息，请参见第 91 页 "Legacy PCI Mechanism" 一节。

**192**

**Chapter 5: TLP Elements**

*Figure 5‐9: 3DW Configuration Request And Header Format*

**==> picture [368 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Type 1<br> Configuration Request<br>Switch<br>Type 0<br> Configuration Request Configuration Request TLP<br>Framing Sequence Framing<br>PCIe Header Data Digest LCRC<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 0 1 0 xType R 0 0 0TC R Attr0 R TH0 DT EP Attr0 0 0 0AT 0 0 0 0 0 0 0 0 0 1Length<br>Byte 4 Requester ID Tag Last DW BE0 0 0 0 1st DWBE<br>Byte 8 Bus Number Device Func Rsvd Ext Reg Register R<br>Function Number with ARI Number Number<br>**----- End of picture text -----**<br>


在第 193 页的图 5‐9 中，显示了一个 Type 1 配置周期向下游传播，并由该总线的桥将其转换为 Type 0（通过改变 Type 字段的位 0 实现）。请注意，与 PCI 不同的是，一个链路上只能驻留一个下游设备。因此，不需要 IDSEL 或其他硬件指示来告知设备应该认领 Type 0 周期；任何在其上游链路上看到的 Type 0 配置周期都将被理解为针对该设备。

**Definitions Of Configuration Request Header Fields.** 第 194 页的表 5‐6 描述了图 5‐9 中所示的配置请求头中每个字段的位置和用途。

**193**

## **PCI Express Technology**

*Table 5‐6: Configuration Request Header Fields*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|始终是 3DW 头<br>000b = configuration read (no data)<br>010b = configuration write (with data)|
|Type [4:0]|Byte 0 Bit 4:0|00100b = Type 0 Config Request<br>00101b = Type 1 Config Request|
|TC [2:0]<br>(Transfer Class)|Byte 1 Bit 6:4|对于 Config 请求，Traffic Class 必须为零，确保这些包永远不会干扰任何高优先级包。|
|Attr [2]<br>(Attributes)|Byte 1 Bit 2|对于 Config 请求，这些位被保留且必须为零。|
|TH<br>(TLP Processing Hints)|Byte 1 Bit 0||
|TD<br>(TLP Digest)|Byte 2 Bit 7|指示 TLP 末端存在 digest 字段（1 DW）。|
|EP<br>(Poisoned Data)|Byte 2 Bit 6|指示数据负载已被 poison。|
|Attr [1:0]<br>(Attributes)|Byte 2 Bit 5:4|在配置请求中，Relaxed Ordering 和 No Snoop 位始终 = 0。|
|AT [1:0]<br>(Address Type)|Byte 2 Bit 3:2|对于配置请求，Address Type 被保留且必须为零。|
|Length [9:0]|Byte 2 Bit 1:0<br>Byte 3 Bit 7:0|对于配置请求，DW 中的数据负载大小始终 = 1。Byte Enables 限定 DW 中的字节，任何组合都是合法的。|

**194**

**Chapter 5: TLP Elements**

*Table 5‐6: Configuration Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Requester ID [15:0]|Byte 4 Bit 7:0<br>Byte 5 Bit 7:0|标识 Requester 的完成返回地址：<br>Byte 4, 7:0 = Bus Number<br>Byte 5, 7:3 = Device Number<br>Byte 5, 2:0 = Function Number|
|Tag [7:0]|Byte 6 Bit 7:0|这些位标识 Requester 发出的未完成请求。默认情况下，仅使用位 4:0（同时 32 个未完成事务），但如果 Control 寄存器中的 Extended Tag 位设置为 = 1，则可以使用全部 8 位（256 个 tag）。|
|Last BE [3:0]<br>(Last DW Byte Enables)|Byte 7 Bit 7:4|这些限定传输的最后一个数据 DW 中的字节。由于配置请求只能是一个 DW 大小，这些位必须为零。|
|1st DW BE [3:0]<br>(First DW Byte Enables)|Byte 7 Bit 3:0|这些高有效位限定传输的第一个数据 DW 中的字节。对于配置请求，任何位组合都是有效的（包括没有任何 active 的情况）。|
|Completer ID [15:0]|Byte 8 Bit 7:0<br>Byte 9 Bit 7:0|标识正在通过此配置周期访问的 Completer。<br>Byte 8, 7:0 = Bus Number<br>Byte 9, 7:3 = Device Number<br>Byte 9, 2:0 = Function Number|
|Ext Register Number<br>[3:0]<br>(Extended Register<br>Number)|Byte 10 Bit 3:0|这些提供用于访问扩展配置空间的 DW 空间的高 4 位。它们与 Register Number 组合形成访问 1024 DW (4096 字节) 空间所需的 10 位地址。对于 PCI 兼容的配置空间，此字段必须为零。|

**195**

## **PCI Express Technology**

*Table 5‐6: Configuration Request Header Fields (Continued)*

|**Field Name**|**Header Byte/Bit**|**Function**|
|---|---|---|
|Register Number [5:0]|Byte 11 Bit 7:0|作为配置 DW 空间的低 8 位，这些指定寄存器号。最低两位始终为零，强制 DW 对齐访问。|

**Configuration Request Notes.** 配置请求始终使用 3DW 头格式，并根据目标 Bus、Device 和 Function 号进行路由。所有设备在收到 Type 0 配置写周期时都会从请求中的目标号"捕获"自己的 Bus 和 Device 号。之所以这样做，是因为它们以后在发出自己的请求时需要将其用作 Requester ID。

## **Completions**

除非出现错误阻止，否则预期 Non‐posted 请求会有完成响应。例如 Memory、IO 或 Configuration Read 请求通常会产生带数据的完成。另一方面，IO 或 Configuration Write 请求通常会产生不带数据的完成，仅报告事务的状态。

完成中的许多字段使用与相应请求相同的值，包括 Traffic Class、Attribute 位以及原始 Requester ID（用于将完成路由回 Requester）。第 197 页的图 5‐10 显示了为 Non‐posted 请求返回的完成及其使用的 3DW 头格式。完成还在头中提供 Completer ID。Completer ID 在正常操作期间并不重要，但在系统调试期间知道完成来自何处可能对错误诊断有用。

**196**

**Chapter 5: TLP Elements**

*Figure 5‐10:  3DW Completion Header Format*

**==> picture [364 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Switch<br>Non-Posted<br>Request Completion TLP<br>PCIe Framing Sequence Header Data Digest LCRC Framing<br>(STP) Number (End)<br>Endpoint<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 x 0Fmt 0 1 0 1 0Type R TC R Attr R TH0 DT EP Attr 0 0AT Length<br>Byte 4 Completer ID Compl.Status MCB Byte Count<br>Byte 8 Requester ID Tag R Lower Address<br>**----- End of picture text -----**<br>


**Definitions Of Completion Header Fields.** 第 197 页的表 5‐7 描述了完成头中每个字段的位置和用途。

*Table 5‐7: Completion Header Fields*

|**Field Name**|**Header**<br>**Byte/Bit**|**Function**|
|---|---|---|
|Fmt [2:0]<br>(Format)|Byte 0 Bit 7:5|包格式（始终是 3DW 头）<br>000b = Completion without data (Cpl)<br>010b = Completion with data (CplD)|