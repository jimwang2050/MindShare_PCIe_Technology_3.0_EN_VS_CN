## **PCI 总线发起方与目标方**

在 PCI 层级结构中,总线上的每个设备最多可包含八个功能,这些功能共享该设备的总线接口,编号为 0~7(单功能设备始终被分配功能编号 0)。每个功能都能够作为总线上事务的目标方,其中大多数还能够发起事务。这样的发起方(称为总线主设备)具有一对专用于仲裁共享 PCI 总线使用权的引脚(REQ# 和 GNT#)。如图 1-2(第 13 页)所示,请求(REQ#)引脚表示主设备需要使用总线,该信号被发送到总线仲裁器,以便与此时所有其他请求一起进行评估。仲裁器通常位于层级结构中该总线上方的桥接器中,接收来自该总线上所有可作为发起方(总线主设备)的设备的仲裁请求。仲裁器决定哪个请求者应成为总线的下一个所有者,并为该设备断言授权(GNT#)引脚。根据协议,无论何时,只要前一个事务完成且总线进入空闲状态,在此期间观察到其 GNT# 被断言的设备就被指定为下一个总线主设备,并可以开始其事务。

**12**

**第 1 章:背景**

_图 1-2:PCI 总线仲裁_

**==> picture [384 x 234] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data PortArbiter<br>PCI 33 MHz<br>Slots<br>IDE<br>CD HDD<br>USB South Bridge LogicError Ethernet SCSI REQ#<br>GNT#<br>ISA Pair<br>Boot Modem Audio Super<br>ROM Chip Chip I/O<br>COM1<br>COM2<br>**----- End of picture text -----**<br>