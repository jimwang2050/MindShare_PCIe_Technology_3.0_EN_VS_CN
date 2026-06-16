## **PCI Express 技术** 

与许多高速串行传输协议一样,PCIe 使用双向连接,能够同时发送和接收信息。所采用的模型称为双单工 (dual-simplex) 连接,因为每个接口都具有一条单工发送路径和一条单工接收路径,如图 2-1 (第 40 页) 所示。由于两个方向同时允许流量传输,两个设备之间的通信路径在技术上是全双工的,但规范使用"双单工"这一术语,因为它更准确地描述了实际存在的通信通道。 

_图 2-1:双单工链路_ 

**==> picture [384 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Packet<br>PCIe PCIe<br>Device Device<br>Link (1 to 32 lanes wide)<br>A B<br>Packet<br>**----- End of picture text -----**<br>

设备之间这条路径称为**链路 (Link)**,由一个或多个发送和接收对组成。每一对称为**通道 (Lane)**,规范允许一条链路包含 1、2、4、8、12、16 或 32 条通道。通道的数量称为链路宽度 (Link Width),用 x1、x2、x4、x8、x16 和 x32 表示。关于在特定设计中使用多少通道的权衡是直截了当的:更多的通道会增加链路的带宽,但同时也会增加其成本、空间占用和功耗。更多相关信息,请参阅第 46 页的"链路与通道"。 

_图 2-2:一条通道_ 

**==> picture [257 x 142] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transmitter Receiver<br>Receiver Transmitter<br>One  lane<br>**----- End of picture text -----**<br>

**40** 

**第 2 章:PCIe 架构概述** 