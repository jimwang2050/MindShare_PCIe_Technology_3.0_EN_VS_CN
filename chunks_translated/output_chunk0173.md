## **服务质量 (QoS)**

PCIe 从设计之初就能够支持对时间敏感的事务,例如流式音频或视频等应用,这些应用要求数据必须及时传递才有意义。这被称为提供服务质量 (Quality of Service),它通过增加一些机制来实现。首先,软件会为每个报文分配一个优先级,即通过设置报文内一个称为流量类 (TC, Traffic Class) 的 3 位字段。一般来说,为报文分配编号更高的 TC 意味着它在系统中具有更高的优先级。其次,硬件为每个端口内置了多个缓冲区,称为虚通道 (VC, Virtual Channel),报文会根据其 TC 被放入相应的缓冲区。第三,由于一个端口现在有多个缓冲区同时有待发送的报文,因此需要仲裁逻辑在各个 VC 之间进行选择。最后,交换机 (Switch) 必须在竞争访问某一输出端口 VC 的多个输入端口之间进行选择。这称为端口仲裁 (Port Arbitration),可以由硬件分配,也可以由软件编程设定。所有这些硬件组件必须到位,系统才能对报文进行优先级排序。如果得到正确的编程和配置,这样的系统甚至可以为给定路径提供有保证的服务。

为了说明这一概念,请参阅第 71 页的图 2‐22,在该图中,摄像机和 SCSI 设备都需要向系统 DRAM 发送数据。不同之处在于,摄像机数据是时间敏感的;如果到目标设备的传输路径无法跟上其带宽,帧就会被丢弃。系统需要能够保证至少与摄像机带宽一样高的传输速率,否则采集到的视频可能会出现卡顿。同时,SCSI 数据需要无误地交付,但交付所需的时间并不那么重要。显然,当视频数据报文和 SCSI 报文需要在同一时刻发送时,视频流量应具有更高的优先级。QoS 指的是系统为报文分配不同优先级、并以确定性延迟和带宽将它们通过拓扑进行路由的能力。有关 QoS 的更多详细信息,请参阅第 245 页第 7 章"服务质量 (Quality of Service)"。

**70**

**第 2 章:PCIe 架构概述**

_图 2‐22:QoS 示例_

**==> picture [368 x 314] intentionally omitted <==**

**----- Start of picture text -----**<br>
Intel 处理器<br>系统<br>内存<br>PCIe<br>Uncore<br>GFX<br>QPI<br>IOH 根复合体 (Root Complex)<br>10 Gb<br>LAN 交换机 以太网交换机 光纤<br>端点 (Endpoint) 通道<br>端点 (Endpoint) 端点 (Endpoint)<br>10 Gb PCI Express SAS/SATA<br>扩展卡 以太网转 PCI<br>RAID<br>端点 (Endpoint) 端点 (Endpoint)<br>端点 (Endpoint)<br>PCI<br>扩展卡 千兆以太网 IEEE 插槽<br>等时 常规 1394<br>流量 端点 (Endpoint) 端点 (Endpoint) 流量<br>
**----- End of picture text -----**<br>