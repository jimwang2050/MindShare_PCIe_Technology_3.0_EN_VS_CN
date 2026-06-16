## **PCI-X 系统示例**

基于 Intel 7500 服务器芯片组的一个系统示例如第 32 页的图 1-15 所示。MCH 芯片包含三个额外的高性能 Hub Link 2.0 端口，这三个端口分别连接到三个 PCI-X Hub 2 桥 (P64H2)。每个

**31**

**PCI Ex ress Technolo p gy**

桥支持两条 PCI-X 总线，这些总线可以运行在最高 133MHz 的频率下。Hub Link 2.0 能够维持 PCI-X 流量所需的更高带宽需求。需要注意的是，我们遇到了与 66 MHz PCI 相同的负载问题，导致需要大量的总线来支持更多的设备，并且解决方案相对昂贵。不过现在的带宽要高得多了。

_图 1-15：基于 66 MHz/133 MHz PCI-X 总线的平台_

**==> picture [374 x 250] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor  Processor<br>FSB<br>PCI-X<br>P64H2<br>DDR SDRAM<br>Hub Link 2<br>Memory Controller Hub<br>P64H2 (Intel 7500 MCH) DDR SDRAM<br>Hub Link 2<br>P64H2<br>64-bit,<br>66MHz or 100MHz or 133MHz<br>Hub Link 1<br>IDE<br>Slots<br>USB IO Controller Hub PCI-33MHz<br>(ICH3)<br>LPC<br>IEEE<br>SCSI<br>AC'97 1394<br>Link<br>Boot<br>Ethernet ROM<br>**----- End of picture text -----**<br>