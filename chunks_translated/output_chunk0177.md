## **DLLPs (数据链路层包)**

DLLP 在链路上两个相邻设备的数据链路层之间传输。事务层甚至不会感知到这些数据包的存在，因为它们只在相邻设备之间传输,不会被路由到其他地方。与 TLP 相比,它们很小(始终只有 8 个字节),这是一件好事,因为它们代表了维护链路协议的额外开销。

_图 2-24:DLLP 的起点和终点_

**==> picture [375 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>Device Device<br>Core Core<br>Transaction Transaction<br>Flow Control,  Layer  Layer<br>Ack/Nak, Etc.<br>(1) Data Data (4)<br>DLLP Core CRC Link Layer Link Layer DLLP Core CRC<br>(2) (2) (3) (3)<br>SDP DLLP Core CRC END Physical Physical SDP DLLP Core CRC END<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>
**----- End of picture text -----**<br>

**DLLP 组装。** 如图 2-24(第 73 页)所示,DLLP 源自发送端的数据链路层,由接收端的数据链路层消费。在 DLLP Core 之后附加一个 16 位 CRC,以便在接收端检查错误。DLLP 的内容被转发到物理层,物理层在数据包的开头和结尾分别附加一个 Start 和 End 字符(针对前两代 PCIe),然后使用所有可用的通道 (Lane) 对其进行编码并以差分方式通过链路 (Link) 传输。

**DLLP 拆卸。** 当物理层接收到 DLLP 时,会对比特流进行解码,并移除 Start 和 End 帧字符。数据包的其余部分被转发到数据链路层,数据链路层会检查 CRC 错误,然后根据该数据包采取适当的操作。数据链路层是 DLLP 的最终目的地,因此不会向上转发到事务层。

**73**

**PCI Ex ress Technolo p gy**
