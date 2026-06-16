## **单主机系统**

写入配置地址端口 (Configuration Address Port) 的信息由根复合体 (Root Complex) 内的主桥/PCI 桥 (Host/PCI Bridge) 锁存,如第 87 页图 3‐1 所示。如果 bit 31 为 1b,且目标总线位于总线号的下游范围内,则该桥会将处理器随后访问其配置数据端口 (Configuration Data Port) 的操作转换为总线 0 上的配置请求。随后,处理器启动对 0CFCh 处配置数据端口的 IO 读或写事务。这会使桥生成一个配置请求:如果对配置数据端口的 IO 访问是读操作,则为配置读;如果 IO 访问是写操作,则为配置写。如果目标总线是总线 0,则该事务为 Type 0 配置事务;如果是范围内另一条总线,则为 Type 1 配置事务;若目标总线不在范围内,则根本不转发。

**94**

**第 3 章:配置概述**

_图 3‐5:单根系统 (Single-Root System)_

**==> 图片 [327 x 449] 已省略 <==**

**----- 图片文字开始 -----**<br>
处理器 (Processor)<br>
根复合体 (Root Complex)<br>
主桥/PCI (Host/PCI)<br>
总线 0 (Bus 0) Sec = 0 桥 (Bridge)<br>
Sub = 9<br>
Pri = 0 Pri = 0<br>
P2P Sec = 1 设备 0 (Device 0) 设备 1 (Device 1) Sec = 5 P2P<br>
Sub = 4 Sub = 9<br>
总线 1 (Bus 1) 总线 1 (Bus 1) 总线 5 (Bus 5) 总线 5 (Bus 5)<br>
设备 0 (Device 0) 设备 0 (Device 0)<br>
Pri = 1 Pri = 5<br>
Sec = 2 P2P Sec = 6<br>
P2P<br>
Sub = 4 Sub = 9<br>
总线 2 (Bus 2) P2P 总线 6 (Bus 6) P2P<br>
Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>
Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>
Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>
总线 3 (Bus 3) 总线 4 (Bus 4) 总线 7 (Bus 7) 总线 8 (Bus 8) 总线 9 (Bus 9)<br>
功能 0 (Function 0) 功能 0 (Function 0) 功能 0 (Function 0) 功能 0 (Function 0)<br>
总线 3 (Bus 3) 总线 4 (Bus 4) 总线 7 (Bus 7) 总线 9 (Bus 9)<br>
设备 0 (Device 0) 设备 0 (Device 0) 设备 0 (Device 0) 设备 0 (Device 0)<br>
**----- 图片文字结束 -----**<br>

**95**

**PCI Express 技术**
