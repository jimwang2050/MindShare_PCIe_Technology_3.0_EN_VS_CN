## **PCIe 功能 (Function)**

如前所述,每个 Device(设备)中都设计有 Function(功能)。这些 Function 可以包括硬盘接口、显示控制器、以太网控制器、USB 控制器等。具有多个 Function 的 Device 不需要按顺序实现。例如,一个 Device 可能实现 Function 0、2 和 7。因此,当配置软件检测到多功能 (multifunction) 设备时,必须检查每个可能的 Function 以了解其中哪些 Function 存在。每个 Function 也都有自己的配置地址空间,用于设置与该 Function 关联的资源。

**86**

**第 3 章:配置概述**

_图 3-1:示例系统_

**==> picture [344 x 462] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>根复合体 (Root Complex)<br>主桥 (Host/PCI Bridge)<br>Bus 0<br>Bus 0 Bus 0 Bus 0<br>Virtual Dev 0 Dev 1 Virtual Dev 2 Integr.<br>P2P Func 0 Func 0 P2P Func 0 EP<br>Bus 1 Bus 1 Bus 5 Bus 5<br>Dev 0 Bus 2 Bus 6 Dev 0<br>Func 0 Dev 2 Dev 1 Func 0<br>Bus 6<br>Func 0 Func 0<br>Dev 2<br>Bus 2 Func 0<br>Dev 1<br>Virtual<br>Func 0 Virtual<br>P2P<br>P2P<br>Bus 2 Bus 6 Bus 6<br>Dev 3<br>Virtual Virtual Virtual Virtual Virtual Func 0<br>P2P P2P P2P P2P P2P<br>Bus 3<br>Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 1 Function 0 Function 0 Function 0<br>Dev 0 Dev 0 Dev 0 Dev 0<br>Bus 8<br>Dev 0<br>Express Func 0<br>PCI<br>Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>Dev 1 Dev 2 Dev 3<br>Func 0 Func 0 Func 0<br>**----- End of picture text -----**<br>

**87**

**PCI Express 技术**