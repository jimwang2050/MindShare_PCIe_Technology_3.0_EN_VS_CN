## **PCI Express Technology** 

**TLP 包解封装。** 当相邻的接收器看到传入的 TLP 位流时,它需要识别并移除那些为恢复发送器核心逻辑所请求的原始信息而添加的部分。如第 64 页的图 2-17 所示,物理层 (Physical Layer) 将验证正确的 Start (起始) 和 End (结束) 或其他字符是否存在,并将它们移除,将其余的 TLP 转发到数据链路层 (Data Link Layer)。该层首先检查 LCRC (链路 CRC) 和序列号 (Sequence Number) 错误。如果未发现错误,则将这些字段从 TLP 中移除,并将其转发到事务层 (Transaction Layer)。如果接收器是交换机 (Switch),则会在事务层中评估该数据包,以查找 TLP 头 (Header) 中的路由信息,并确定应将该数据包转发到哪个端口。即使不是预期目的地,如果交换机发现 ECRC (端到端 CRC) 错误,也允许其检查并报告该错误。但是,不允许其修改 ECRC,因此目标设备也将能够检测到 ECRC 错误。 

如果目标设备具备相应能力并且已使能,则可以检查 ECRC 错误。如果此设备就是目标设备且没有错误,则会移除 ECRC 字段,留下包头和数据部分,以便转发到软件层。 

_图 2-17:TLP 解封装_ 

**==> picture [366 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
Information in core section of TLP is<br>sent to Software Layer / Device Core<br>Bit receive direction<br>Sequence<br>Start Header Data ECRC LCRC End<br>Number<br>Stripped by Transaction Layer<br>Stripped by Data Link Layer<br>Stripped by PHY Layer<br>**----- End of picture text -----**<br>

**64** 

**Chapter 2: PCIe Architecture Overview** 