## **内存读请求** 

在讨论的第一部分,请参考第 81 页的图 2‐32。请求者的设备内核或软件层向事务层发送请求,并包含以下信息:32 位或 64 位内存地址、事务类型、以双字 (dword) 计算的待读取数据量、流量类 (TC)、字节使能 (Byte Enable)、属性 (Attr) 等。 

_图 2‐32:内存读请求阶段_ 

**==> 图片 [365 x 246] 故意省略 <==**

**----- 图片文字开始 -----**<br>
请求者 完成者 (Completer)<br>发送内存读请求 软件层 接收内存读请求<br>事务层包 (TLP) 事务层包 (TLP)<br>包头 (Header) ECRC 包头 (Header) ECRC<br>流控 (Flow Control) 事务层 流控 (Flow Control)<br>虚通道 (VC) 发送 虚通道 (VC) 接收<br>管理 管理<br>缓冲区 (Buffers) 缓冲区 (Buffers)<br>每 VC 每 VC<br>排序 (Ordering) 排序 (Ordering)<br>链路 数据链路层包 (DLLP)<br>链路包<br>序列号 TLP LCRC Nak 序列号 TLP LCRC<br>数据链路层<br>重传缓冲区 (Retry Buffer) DLLP. 错误<br>确认/否认 (Ack/Nak) CRC 校验<br>物理包 物理包<br>链路包开始 链路包结束 链路包开始 链路包结束<br>编码 (Encode) 物理层 解码 (Decode)<br>并转串 串转并<br>差分驱动器 差分接收器<br>端口 端口<br>确认或否认 (Ack 或 Nak)<br>链路 (Link)<br>MRd TLP<br>**----- 图片文字结束 -----**<br>

**81** 
