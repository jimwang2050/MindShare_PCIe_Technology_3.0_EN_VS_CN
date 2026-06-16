## **Type 0 配置请求 (Configuration Request)** 

如果目标总线号与 Secondary Bus Number（次级总线号）匹配,则 Type 0 配置读或写将被转发到次级总线,并:

1. 该总线上的设备会检查 Device Number(设备号)字段,以确定哪个设备是目标设备。请注意,外部链路 (Link) 上的端点 (Endpoint) 始终是 Device 0。

2. 被选中的设备会检查 Function Number(功能号)字段,以确定在该设备内选择了哪个功能。

3. 被选中的功能使用 Register Number(寄存器号)字段来选择其配置空间中的目标双字 (dword),并使用 First Dword Byte Enable(第一个双字字节使能)字段来选择在所选双字内读取或写入哪些字节。

图 3-7 展示了 Type 0 配置读和写请求头格式。在这两种情况下,Type 字段 = 00100,而 Format 字段则指示是读还是写。

**99**