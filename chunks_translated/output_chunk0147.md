## **无公共时钟 (No Common Clock)** 

如前所述，PCIe 链路 (Link) 并不需要公共时钟，因为它采用了源同步模型 (source-synchronous model)，即由发送器 (Transmitter) 向接收器 (Receiver) 提供时钟，用于锁存传入的数据。PCIe 链路中并不包含一个转发的时钟 (forwarded clock)。相反，发送器使用 8b/10b 编码将时钟嵌入到数据流中。接收器随后从数据流中恢复 (recover) 时钟，并使用该时钟来锁存传入的数据。尽管听起来很神秘，但这个过程的实现实际上相当简单。在接收器中，PLL 电路（锁相环，参见第 45 页的图 2-5）将传入的比特流作为参考时钟 (reference clock)，并将其时序或相位与其自身以指定频率产生的输出时钟进行比较。根据该比较结果，输出时钟的频率被增大或减小，直至两者匹配。此时，PLL 即被称为"已锁定" (locked)，并且其输出（恢复）时钟的频率与发送数据时使用的时钟精确匹配。PLL 会持续地调整恢复时钟，因此由温度或电压变化所引起的发送器时钟频率的改变都将被迅速补偿。 

关于时钟恢复有一点需要注意：PLL 需要输入信号中存在电平跳变 (transitions) 才能进行相位比较。如果数据长时间没有任何跳变，PLL 可能会逐渐偏离正确的频率。为了避免这个问题，8b/10b 编码 (8b/10b Encoding) 的设计目标之一就是确保比特流中不会出现超过 5 个连续的 1 或 0（欲了解更多信息，请参见第 380 页的"8b/10b 编码"）。 

_图 2-5：简单的 PLL 框图_ 

**==> picture [350 x 120] intentionally omitted <==**

**----- Start of picture text -----**<br>
Reference<br>(incoming Recovered<br>bitstream) DetectorPhase Lo op Filter Voltage-Controlled Clock<br>Oscillator<br>Divide by N Counter<br>(to create multiples of<br>reference frequency)<br>**----- End of picture text -----**<br>

**45** 

**PCI Ex ress Technolo p gy** 

一旦时钟被恢复，它就被用于将传入数据流的比特锁存到解串器 (deserializer) 中。有时学生会有疑问：是否可以使用这个恢复的时钟来为接收器中的所有逻辑提供时钟？答案是不能。原因之一是接收器无法保证该参考时钟始终存在，因为链路 (Link) 上的低功耗状态 (low power state) 会停止数据传输。因此，接收器还必须拥有自己可以在本地生成的内部时钟。 
