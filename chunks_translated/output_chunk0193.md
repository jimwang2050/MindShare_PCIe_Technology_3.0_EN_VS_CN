## **带数据的完成 (Completion with Data)** 

在本讨论的后半部分,请参阅第 83 页的图 2-33。为了服务该内存读请求,完成器设备核心/软件层会向其事务层发送一个带数据的完成 (CplD) 请求,该请求包含从原始内存读请求中复制的请求者 ID 和 Tag 字段、事务类型、完成包头内容的其他部分以及所请求的数据。

_图 2-33:带数据的完成阶段 (Completion with Data Phase)_ 

**==> 图片 [374 x 257] 已被有意省略 <==**

**----- 图片文字开始 -----**<br>
请求者 (Requester) 完成器 (Completer)<br>接收 带数据的完成 (Receive Completion with Data) 软件层 发送 带数据的完成 (Send Completion with Data)<br>事务层包 (TLP) 事务层包 (TLP)<br>包头 数据净载荷  ECRC 包头 数据净载荷  ECRC<br>流控 (Flow Control) 事务层 流控 (Flow Control)<br>虚通道 (VC) 接收 虚通道 (VC) 发送<br>管理 管理<br>缓冲区 缓冲区<br>每 VC 每 VC<br>排序 排序<br>链路 DLLP<br>链路包 (Link Packet)<br>序列号 TLP LCRC 序列号 TLP LCRC NAK<br>数据链路层<br>DLLP 错误 重试缓冲区 (Retry Buffer)<br>Ack/Nak CRC 校验<br>物理包 (Physical Packet) 物理包 (Physical Packet)<br>链路包起始 链路包结束 链路包起始 链路包结束<br>解码 物理层 编码<br>串并转换 并串转换<br>差分接收器 (Receiver) 差分发送器 (Driver)<br>端口 (Port) 端口 (Port)<br>CplD TLP<br>链路 (Link)<br>Ack 或 Nak<br>**----- 图片文字结束 -----**<br>

**83** 
