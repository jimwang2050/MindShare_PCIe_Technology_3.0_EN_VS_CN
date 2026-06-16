**Cha ter 18: S stem Reset p y**

## **热复位（带内复位）**

热复位通过从一个链路邻居向另一个链路邻居发送多个 TS1（其内容如图 18-2 所示）来带内传播，其中符号 5 的第 0 位置位。这些 TS1 在所有 Lane 上发送，使用先前协商的 Link 和 Lane 编号，持续 2ms。一旦发送完毕，热复位的发送器和接收器都将进入 Detect LTSSM 状态（参见第 612 页的"Hot Reset State"）。

_Figure 18-2: TS1 Ordered-Set Showing the Hot Reset Bit_

|_Figure 18-2: TS1 Ordered-Set Showing the Hot Reset Bit_|_Figure 18-2: TS1 Ordered-Set Showing the Hot Reset Bit_|_Figure 18-2: TS1 Ordered-Set Showing the Hot Reset Bit_|
|---|---|---|
||||
|**TS1**<br>TS ID<br>TS ID<br>TS ID<br>Train Ctl<br>Rate ID<br># FTS<br>Lane #<br>Link #<br>COM<br>0<br>1<br>2<br>3<br>4<br>5<br>6<br>14<br>15<br>13|K28.5<br>D0.0-D31.7, K23.7 (0-255)<br>D0.0-D31.0, K23.7 (0-31)<br># of FTS ordered sets required by<br>receiver to obtain bit and symbol lock<br>D10.2 for TS1 Identifier<br>D10.2 for TS1 Identifier<br>D10.2 for TS1 Identifier|**0** **=** **De-assert** **Disable** **Scrambling**<br>**1** **=** **Assert** **Disable** **Scrambling**<br>**Bit** **3**<br>**Reserved**<br>**Bit** **5:7**<br>**0** **=** **De-assert** **Compliance** **Receive**<br>**1** **=** **Assert** **Compliance** **Receive**<br>**Bit** **4**<br>**0** **=** **De-assert** **Loopback**<br>**1** **=** **Assert** **Loopback**<br>**Bit** **2**<br>**0** **=** **De-assert** **Disable** **Link**<br>**1** **=** **Assert** **Disable** **Link**<br>**Bit** **1**<br>**0** **=** **De-assert** **Hot** **Reset**<br>**1** **=** **Assert** **Hot** **Reset**<br>**Bit** **0**<br>Training Control|
||||


热复位由软件通过设置桥的 Bridge Control 配置寄存器中的 Secondary Bus Reset 位来发起，如图 18-5（第 840 页）所示。因此，只有包含桥的设备（如根复合体或交换机）才能执行此操作。在其上游端口上收到热复位的交换机必须将其广播到其所有下游端口并复位自身。交换机下游接收热复位的所有设备将复位自身。

## **对接收热复位的响应**

- 设备的 LTSSM 经过 Recovery 和 Hot Reset 状态，然后回到 Detect 状态，在那里开始 Link 训练过程。

- 设备的所有状态机、硬件逻辑、端口状态和配置寄存器（粘性寄存器除外）都初始化为其默认条件。

**837**

**PCI Ex ress 3.0 Technolo p gy**

## **交换机在其下游端口上生成热复位**

交换机在以下情况下在其所有下游端口上生成热复位：

- 它在其上游端口上收到热复位

- 对于交换机或桥的上游端口，如果数据链路层报告 DL_Down 状态，则效果非常类似于热复位。当上游端口由于物理层或数据链路层无法恢复的错误而失去与上游设备的连接时，可能会发生这种情况。

- 软件设置与上游端口关联的 Bridge Control 配置寄存器的 "Secondary Bus Reset" 位，如图 18-3（第 838 页）所示。

_Figure 18-3: Switch Generates Hot Reset on One Downstream Port_

**==> picture [251 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>
FSB<br>
PCI Express<br>
GFX<br>
GFX Root Complex DDR<br>
SDRAM<br>
'Secondary Bus Reset'<br>
Bit Set<br>
Switch A Switch C<br>
1<br>
Switch B Ethernet10Gb PCI Expressto-PCI SCSI<br>
Slots<br>
PCI<br>
Gb<br>
Add-In Ethernet S IEEE<br>
IO 1394<br>
COM1<br>
COM2<br>
**----- End of picture text -----**<br>


## **桥将热复位转发到辅助总线**

如果诸如 PCI Express-to-PCI(-X) 桥之类的桥在其上游端口上检测到热复位，则它必须在其辅助 PCI(-X) 总线上断言 PRST# 信号，如图 18-4（第 839 页）所示。

## **软件生成热复位**

软件通过向关联端口的配置头中的 Bridge Control 寄存器的 "Secondary Bus Reset" 位写入 1 后跟 0，在特定端口上生成热复位。

**838**

**Cha ter 18: S stem Reset p y**

端口的配置头（参见第 840 页的图 18-5）。考虑图 18-3（第 838 页）中所示的示例。软件设置 Switch A 的左侧下游端口的 "Secondary Bus Reset" 寄存器，导致它发送设置了热复位位的 TS1 有序集。Switch B 在其上游端口上接收此热复位并将其转发到其所有下游端口。

_Figure 18-4: Switch Generates Hot Reset on All Downstream Ports_

**==> picture [277 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>
FSB<br>
PCI Express<br>
GFX<br>
GFX Root Complex<br>
DDR<br>
SDRAM<br>
'Secondary Bus Reset'<br>
1<br>
Bit is Set<br>
Switch A Switch C<br>
Switch B Ethernet10Gb PCI Expressto-PCI SCSI<br>
Slots<br>
PRST#<br>
PCI<br>
Gb<br>
Add-In Ethernet S IEEE<br>
IO 1394<br>
COM1<br>
COM2<br>
**----- End of picture text -----**<br>


如果软件设置交换机的上游端口的 Secondary Bus Reset 位，则交换机会在其所有下游端口上生成热复位，如图 18-4（第 839 页）所示。这里，软件设置 Switch C 的上游端口的 Secondary Bus Reset 位，导致它在其所有下游端口上发送设置了热复位位的 TS1。PCIe-to-PCI 桥接收此热复位并通过断言 PRST# 将其转发到 PCI 总线。

设置 Secondary Bus Reset 位会导致端口的 LTSSM 转换到 Recovery 状态（有关 LTSSM 的更多信息，请参见第 519 页的"Overview of LTSSM States"），其中它生成设置了热复位位的 TS1。TS1 持续生成 2ms，然后端口退出到 Detect 状态，在那里它已准备好开始 Link 训练过程。

**839**

**PCI Ex ress 3.0 Technolo p gy**

热复位 TS1 的接收者（始终是下游）也将进入 Recovery 状态。当它看到两个连续的设置了热复位位的 TS1 时，它将进入 Hot Reset 状态 2ms 超时，然后退出到 Detect。上游和下游端口都被初始化并最终处于 Detect 状态，准备开始 Link 训练。如果下游设备也是交换机或桥，它也会将热复位转发到其下游端口，如图 18-3（第 838 页）所示。

_Figure 18-5: Secondary Bus Reset Register to Generate Hot Reset_

**==> picture [374 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Doubleword<br>
Number<br>
Byte (in decimal)<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0 3 2 1 0<br>
Reserved 2.2 2.2 2.2 2.2 DeviceID VendorID 00<br>
Status Command 01<br>
Discard Timer SERR# Enable Register Register<br>
Discard Timer Status Class Code Revision 02<br>
ID<br>
Secondary Discard TimeoutPrimary Discard Timeout BISTBase Add ress 0HeaderType LatencyTimer CacheLineSize 0304<br>
Fast Back-to-Back Enable<br>
Secondary Bus Reset Base Add ress 1 05<br>
Master Abort Mode Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>
VGA Enable Secondary I/O I/O 07<br>
ISA Enable Status Limit Base<br>
SERR# Enable MemoryLimit MemoryBase 08<br>
Parity Error Response Prefetchable Prefetchable 09<br>
Memory Limit Memory Base<br>
Prefetchable Ba se 10<br>
Upper 3 2 Bits<br>
Prefetchable L imit 11<br>
Upper 3 2 Bits<br>
I/O Limit I/O Base 12<br>
Upper 16 Bits Upper 16 Bits<br>
Reserved CapabilityPointer 13<br>
Expansion R OM Base Address 14<br>
Bridge Interrupt Interrupt 15<br>
Control Pin Line<br>
Required configuration registers<br>
**----- End of picture text -----**<br>


## **软件可以禁用 Link**

软件还可以禁用 Link，强制其进入电气空闲状态并保持在那里，直到另行通知。在此处提及这一点的原因是，禁用 Link 还具有导致下游组件发生热复应的效果。禁用是通过设置下游端口的 Link Control 寄存器中的 Link Disable 位来实现的，如图 18-6（第 841 页）所示。这会导致端口进入 Recovery LTSSM 状态并开始发送设置了禁用位的 TS1。由于只能为下游端口控制这一点（如果 Link 已禁用），因此此位保留用于上游端口（例如端点或交换机的上游端口）。

**840**

**Cha ter 18: S stem Reset p y**

## _Figure 18-6: Link Control Register_

**==> picture [346 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>
RsvdP<br>
Link Autonomous Bandwidth<br>
Interrupt Enable<br>
Link Bandwidth Management<br>
Interrupt Enable<br>
Hardware Autonomous<br>
Width Disable<br>
Enable Clock<br>
Power Management<br>
Extended Synch<br>
Common Clock<br>
Configuration<br>
Retrain Link<br>
Link Disable<br>
Read Completion<br>
Boundary Control<br>
RsvdP<br>
Active State<br>
PM Control<br>
**----- End of picture text -----**<br>


当上游端口识别传入的设置了禁用位的 TS1 时，其物理层向链路层发出 LinkUp=0（假），并且所有 Lane 都进入电气空闲状态。2ms 超时后，上游端口将进入 Detect，但下游端口将保持在禁用的 LTSSM 状态，直到被指示退出该状态（例如通过清除 Link Disable 位），因此 Link 将保持禁用状态，并且在此之前不会尝试训练。

**841**

**PCI Ex ress 3.0 Technolo p gy**

## _Figure 18-7: TS1 Ordered-Set Showing Disable Link Bit_

**==> picture [366 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
TS1 Training Control<br>
Bit 0 0 = De-assert Hot Reset<br>
0 COM K28.5<br>
1 = Assert Hot Reset<br>
1 Link # D0.0-D31.7, K23.7 (0-255)<br>
2 Lane # D0.0-D31.0, K23.7 (0-31) Bit 1 0 = De-assert Disable Link<br>
# of FTS ordered sets required by<br>
3 # FTS receiver to obtain bit and symbol lock 1 = Assert Disable Link<br>
4 Rate ID<br>
5 Train Ctl Bit 2 0 = De-assert Loopback<br>
6 1 = Assert Loopback<br>
TS ID D10.2 for TS1 Identifier Bit 3 0 = De-assert Disable Scrambling<br>
1 = Assert Disable Scrambling<br>
13<br>
14 TS ID D10.2 for TS1 Identifier Bit 4 0 = De-assert Compliance Receive<br>
15 TS ID D10.2 for TS1 Identifier 1 = Assert Compliance Receive<br>
Bit 5:7 Reserved<br>
**----- End of picture text -----**<br>


## **功能级复位 (FLR)**

FLR 功能允许软件仅复位多功能设备中的一个 Function，而不影响它们共享的 Link。强烈建议但不要求实现它，因此软件需要在尝试使用它之前通过检查 Device Capabilities 寄存器来确认其可用性，如图 18-8（第 843 页）所示。如果设置了 Function-Level Reset Capability 位，则可以通过简单设置 Device Control 寄存器中的 Initiate Function-Level Reset 位来启动 FLR，如图 18-9（第 843 页）所示。

**842**

**Cha ter 18: S stem Reset p y**

_Figure 18-8: Function-Level Reset Capability_

## _Figure 18-9: Function-Level Reset Initiate Bit_

**843**

规范提到了一些示例，这些示例激发了添加 FLR 的动机：

1. 软件控制 Function 时可能会遇到问题，并且不再正常运行。防止数据损坏需要复位该 Function，但如果该设备中的其他 Function 仍在正常工作，那么仅复位有问题的那个就好了。
