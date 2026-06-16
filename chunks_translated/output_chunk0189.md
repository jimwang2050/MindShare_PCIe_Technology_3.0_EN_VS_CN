## **PCI Ex ress Technolo p gy** 

_图 2‐30:有序集的源与目的_

**==> picture [339 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe 设备 A PCIe 设备 B<br>
设备核心 设备核心<br>
PCIe 核心 PCIe 核心<br>
硬件/软件 硬件/软件<br>
接口 接口<br>
事务层 事务层<br>
数据链路层 数据链路层<br>
有序集 物理层 物理层 有序集<br>
发送 接收<br>
(RX) (TX) (RX) (TX)<br>
链路 (Link)<br>
**----- End of picture text -----**<br>

有序集用于链路训练过程中,如第 14 章(标题为"链路初始化与训练",第 505 页)所述。它们还用于补偿发送器与接收器内部时钟之间的微小差异,这一过程称为时钟容差补偿。最后,有序集还用于指示链路进入或退出低功耗状态。 

_图 2‐31:有序集结构_

**==> picture [205 x 73] intentionally omitted <==**

**----- Start of picture text -----**<br>
COM 标识符 标识符 标识符<br>
**----- End of picture text -----**<br>

**80** 

**第 2 章:PCIe 架构概述**