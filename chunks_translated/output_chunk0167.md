## **PCI Express 技术**

_图 2-15：TLP 的源端与目的端_

**==> picture [290 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>TransmittedTLP Transaction Layer Transaction Layer ReceivedTLP<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>Link<br>
**----- End of picture text -----**<br>

**TLP 数据包组装。** 关于已完成的 TLP 在链路上发送时各组成部分的示意图，请参见第 63 页的图 2-16，从中可以看出数据包的不同部分在每一层中添加。为了更容易识别数据包是如何构建的，TLP 的不同部分用颜色编码以指示负责该部分的层：事务层为红色，数据链路层为蓝色，物理层为绿色。

设备核心在事务层中发送组装 TLP 核心部分所需的信息。每个 TLP 都有一个包头（Header），尽管某些 TLP（如读请求）不包含数据。可以选择性地计算并附加一个端到端 CRC（ECRC）字段。CRC 代表循环冗余校验（Cyclic Redundancy Check 或 Code），几乎所有串行架构都采用它，原因很简单——它易于实现，并提供非常强大的错误检测能力。CRC 还能检测"突发错误"，即重复的误位串，其长度可达 CRC 值的长度（PCIe 中为 32 位）。由于在发送长串比特时很可能遇到此类错误，因此这一特性对串行传输非常有用。ECRC 字段在发送端和接收端之间的任何服务点（"服务点"通常指具有 TLP 路由选项的交换机或根端口）保持不变地传递，这使得它在目的地验证沿途没有发生错误时非常有用。

**62**

**第 2 章：PCIe 架构概述**

对于传输，TLP 的核心部分被转发到数据链路层，数据链路层负责附加一个序列号（Sequence Number）和另一个称为链路 CRC（LCRC）的 CRC 字段。LCRC 由相邻的接收器用于检查错误，并将该检查的结果针对该链路上发送的每个数据包报告回发送器。细心的读者可能会想，既然强制的 LCRC 检查已经验证了链路上无错误的传输，为什么 ECRC 仍然有用呢？原因是仍存在一处未检查传输错误的地方，那就是在路由数据包的设备内部。数据包在一个端口到达并被检查错误，检查路由，然后当从另一端口发出时，会计算并添加一个新的 LCRC 值。端口之间的内部转发可能会遇到未作为常规 PCIe 协议一部分被检查的错误，这就是 ECRC 之所以有用的原因。

最后，生成的数据包被转发到物理层，在那里会将其他字符添加到数据包中，以让接收器知道会发生什么。对于 PCIe 的前两代，这些是添加在数据包开头和结尾的控制字符。对于第三代，不再使用控制字符，但会在块上附加其他比特，以提供关于数据包所需的信息。然后，数据包使用所有可用的通道（Lane）进行编码并以差分方式在链路上传输。

_图 2-16：TLP 组装_

**==> picture [278 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Information in core section of TLP comes<br>from Software Layer / Device Core<br>
Bit transmit direction<br>
Sequence<br>
Start Header Data ECRC LCRC End<br>
Number<br>
Created by Transaction Layer<br>
Appended by Data Link Layer<br>
Appended by PHY Layer<br>
**----- End of picture text -----**<br>

**63**
