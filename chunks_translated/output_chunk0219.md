## **概述** 

当规范制定者决定 PCI‐X 以及后来的 PCIe 如何访问配置空间 (Configuration Space) 时,他们面临两个考虑。首先,每个 Function (功能) 仅有 256 字节的空间,这限制了希望在该处放置专有信息的厂商,以及未来需要更多空间来容纳标准化能力结构 (Capability Structure) 的规范制定者。为了解决这个问题,空间直接从每个 Function 256 字节扩展到了 4KB。其次,在制定 PCI 规范时,使用中的多处理器系统还很少。当只有一个 CPU 且它只运行一个线程时,旧模型需要两步才能产生一次访问这一事实并不是问题。但使用多核、多线程 CPU 的较新机器对 IO‐间接 (IO-indirect) 模型提出了一个问题,因为没有任何机制能阻止多个线程同时尝试访问配置空间。因此,如果不加入某种锁机制 (locking semantics),这种两步模型将无法继续工作。如果没有锁机制,一旦线程 A 向

**96**

**第 3 章:配置概述**

配置地址端口 (Configuration Address Port,CF8h) 写入一个值,就无法阻止线程 B 在线程 A 能够对配置数据端口 (Configuration Data Port,CFCh) 执行相应访问之前覆盖该值。

_图 3‐6:多根系统 (Multi‐Root System)_ 

**==> 图片 [379 x 377] 故意省略 <==**

**----- 图片文字开始 -----**<br>
处理器间<br>通信<br>处理器 处理器<br>根复合体 (Root Complex) 根复合体 (Root Complex)<br>Sec = 0 主机/PCI 桥 (Host/PCI Bridge) Sec = 64 主机/PCI 桥 (Host/PCI Bridge)<br>Sub = 9 Sub = 65<br>总线 (Bus) 0<br>总线 (Bus) 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 设备 (Device) 0 设备 (Device) 1 Sec = 5Sub = 9 P2P 设备 (Device) 0 Sec = 65Sub = 65 P2P<br>总线 (Bus) 65<br>总线 (Bus) 1 总线 (Bus) 5<br>功能 (Function) 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>总线 (Bus) 2 P2P 总线 (Bus) 6 P2P 总线 (Bus) 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 设备 (Device) 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>总线 (Bus) 3 总线 (Bus) 4 总线 (Bus) 7 总线 (Bus) 8 总线 (Bus) 9<br>功能 (Function) 0 功能 (Function) 0 功能 (Function) 0 功能 (Function) 0<br>总线 (Bus) 3 总线 (Bus) 4 总线 (Bus) 7 总线 (Bus) 9<br>设备 (Device) 0 设备 (Device) 0 设备 (Device) 0 设备 (Device) 0<br>**----- 图片文字结束 -----**<br>

**97**
