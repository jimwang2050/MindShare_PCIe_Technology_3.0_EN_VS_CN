Root Port 通过将其 TS1 更改为显示适合活动 Lane 的 Lane 编号,但对于看到非活动的所有 Lane 的 Link 和 Lane 编号使用 PAD 来响应。上游端口以相同的 TS1 进行响应,如图 14-65(第 636 页)所示,并且状态更改为 Config.Lanenum.Accept。此时,Root Port 更新状态位以显示检测到自主更改,并更改为 Config.Complete 子状态。

**635** 

## **PCI Ex ress Technolo p gy** 

## _Figure 14-65: 对 Lane 编号更改的响应_ 

**==> picture [344 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
g<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>State<br>Lane Lane<br>Link:PAD, Lane:PAD) TS1 (Link:0, Lane: 0) TS1 (Link:0, Lane: 0)<br>0 0 Active<br>TS1 (Link:0, Lane:0) TS1 (Link:0,  Lane:0) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>1 1 Inactive<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Lan<br>2 2 Inactive<br>e<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>Link:PAD, Lane:PAD) TS1 (Li nk:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>3 3 Inactive<br>TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD , Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>**----- End of picture text -----**<br>


在下一步中,Root Port 开始在活动 Lane 上发送 TS2,并将非活动 Lane 置于 Electrical Idle。请记住,TS2 报告组件是否"支持 upconfigure",在此示例中,两个链路伙伴都支持此能力。端点发回相同的内容:活动 Lane 上的 TS2 和非活动 Lane 上的 Electrical Idle。看到这一点,Root Port 的状态机更改为 Config.Idle,并开始在活动 Lane 上发送 Logical Idle。端点以相同的内容进行响应,链路状态变回 L0。链路现在已准备好进行正常操作,尽管带宽已降低以节省功率。

**636** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-66: 链路宽度更改 - 完成_ 

**==> picture [344 x 280] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>Upconfigure Capability = 1 Upconfigure Capability = 1 State<br>Lane Lane<br>Link:PAD, Lane:PAD) TS2 (Link:0, Lane: 0) TS2 (Link:0, Lane: 0)<br>0 0 Active<br>TS2 (Link:0, Lane:0) TS2 (Link:0,  Lane:0) TS1 (Link:PAD, Lane:PAD)<br>Upconfigure Capability = 1 Upconfigure Capability = 1<br>Electrical Idle<br>1 1 Inactive<br>Electrical Idle<br>Lan<br>2 2 Inactive<br>e<br>Electrical Idle<br>3 3 Inactive<br>**----- End of picture text -----**<br>


与动态速度更改的情况一样,软件无法发起链路宽度更改,但它可以通过设置 Link Control 寄存器(如图 14-67(第 638 页)所示)中的相应位来禁用此机制。与速度更改情况不同,未定义允许设置特定链路宽度的软件机制。

**637** 

## **PCI Ex ress Technolo p gy** 

_Figure 14-67: Link Control 寄存器_ 

## **相关配置寄存器** 

许多与链路初始化和训练相关的配置寄存器已在其内容描述时显示过,但在这里汇总它们似乎很好。

## **Link Capabilities 寄存器** 

Link Capabilities 寄存器如图 14-68(第 639 页)所示,每个位字段在以下小节中描述。

**638** 

**Chapter 14: Link Initialization & Training** 

## _Figure 14-68: Link Capabilities 寄存器_ 

**==> picture [332 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 24 23 22 21 20 19 18 17 15 14 12 1110 9 4 3 0<br>Port Number<br>RsvdP<br>ASPM Optionality Compliance<br>Link Bandwidth<br>Notification Capability<br>Data Link Layer Link Active<br>Reporting Capable<br>Surprise Down Error<br>Reporting Capable<br>Clock Power Management<br>L1 Exit Latency<br>L0s Exit Latency<br>Active State<br>Link PM Support<br>Maximum Link Width<br>Max Link Speed<br>**----- End of picture text -----**<br>


## **Max Link Speed [3:0]** 

这指示此端口的最大链路速度,并作为指向 Link Capabilities 2 寄存器 Supported Link Speeds Vector 中对应于最大链路速度的位位置的指针给出。已定义的编码为:

- 0001b - Supported Link Speeds Vector 字段位 0 

- 0010b - Supported Link Speeds Vector 字段位 1 

- 0011b - Supported Link Speeds Vector 字段位 2 

- 0100b - Supported Link Speeds Vector 字段位 3 

- 0101b - Supported Link Speeds Vector 字段位 4 

- 0110b - Supported Link Speeds Vector 字段位 5 

- 0111b - Supported Link Speeds Vector 字段位 6 

所有其他编码均保留。共享上游端口的多功能设备必须在所有 Function 中的此字段中报告相同的值。此寄存器为只读。

**639** 

## **PCI Ex ress Technolo p gy** 

## **Maximum Link Width[9:4]** 

此字段指示 PCI Express 链路的最大宽度。定义的值有:

- 00 0000b: 保留 

- 00 0001b: x1 

- 00 0010b: x2 

- 00 0100b: x4 

- 00 1000b: x8 

- 00 1100b: x12 

- 01 0000b: x16 

- 10 0000b: x32 

所有其他编码均保留。共享上游端口的多功能设备必须在所有 Function 中的此字段中报告相同的值。此寄存器为只读。

## **Link Capabilities 2 寄存器** 

Link Capabilities 寄存器如图 14-68(第 639 页)所示,并显示 Link Capabilities 寄存器中的 Max Link Speed 字段所指向的 Supported Link Speeds Vector。此字段的值为:

- 位 0 = 2.5 GT/s 

- 位 1 = 5.0 GT/s 

- 位 2 = 8.0 GT/s 

- 位 6:3 RsvdP(保留并保留)。

_Figure 14-69: Link Capabilities 2 寄存器_ 

**==> picture [329 x 113] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 9    8   7 1 0<br>RsvdP<br>Crosslink Supported<br>Supported Link<br>Speeds Vector<br>RsvdP<br>**----- End of picture text -----**<br>


**640** 

**Chapter 14: Link Initialization & Training** 

## **Link Status 寄存器** 

Link Status 寄存器如图 14-39(第 597 页)所示。

## **Current Link Speed[3:0]:** 

此只读字段指示当前链路速度。当链路首次训练到 L0 时,速度始终为 2.5 GT/s。之后,如果可获得更高的共同支持的速度,LTSSM 将进入 Recovery 并尝试更改为该速度。此字段中的值与 Link Capabilities 寄存器中显示的 Max Link Speed 编码相同:

- 0001b - Supported Link Speeds Vector 字段位 0 

- 0010b - Supported Link Speeds Vector 字段位 1 

- 0011b - Supported Link Speeds Vector 字段位 2 

- 0100b - Supported Link Speeds Vector 字段位 3 

- 0101b - Supported Link Speeds Vector 字段位 4 

- 0110b - Supported Link Speeds Vector 字段位 5 

- 0111b - Supported Link Speeds Vector 字段位 6 

所有其他编码均保留。

请注意,当链路未启动时(LinkUp = 0b),此字段的值是未定义的。

## **Negotiated Link Width[9:4]** 

此字段指示链路宽度协商的结果。有七种可能的宽度,所有其他编码均保留。已定义的编码为:

- 00 0001b: 对于 x1。 

- 00 0010b: 对于 x2。 

- 00 0100b: 对于 x4。 

- 00 1000b: 对于 x8。 

- 00 1100b: 对于 x12。 

- 01 0000b: 对于 x16。 

- 10 0000b: 对于 x32。 

所有其他编码均保留。请注意,当链路未启动时(LinkUp = 0b),此字段的值是未定义的。

**641** 

## **PCI Ex ress Technolo p gy** 

## **Undefined[10]** 

当前未定义,此位在早期规范版本中由硬件在发生链路训练错误时设置。它在 LTSSM 成功进入 L0 时被清除。规范指出,软件可以向此位写入任何值,但必须忽略从中读取的任何值。

## **Link Training[11]** 

此只读位指示 LTSSM 正在训练过程中。从技术上讲,它意味着 LTSSM 处于 Configuration 或 Recovery 状态,或者 Retrain Link 位已写入 1b 但链路训练尚未开始。当 LTSSM 退出 Configuration 或 Recovery 状态时,此位由硬件清除。由于这必须在链路训练进行时对软件可见,因此它仅对面向下游的端口有意义。因此,对于端点、桥接器上游端口和交换机上游端口,此位不适用并保留。对于它们,此位必须硬连线为 0b。

_Figure 14-70: Link Status 寄存器_ 

**==> picture [381 x 173] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 4 3 0<br>Link Autonomous<br>Bandwidth Status<br>Link Bandwidth<br>Management Status<br>Data Link Layer<br>Link Active<br>Slot Clock<br>Configuration<br>Link Training<br>Undefined<br>Negotiated<br>Link Width<br>Current Link Speed<br>**----- End of picture text -----**<br>


## **Link Control 寄存器** 

Link Control 寄存器如图 14-71(第 644 页)所示,其中有三个字段对我们来说是有意义的。

**642** 

**Chapter 14: Link Initialization & Training** 

## **Link Disable** 

当设置为 1 时,链路被禁用。直观地说,此位不适用,对于端点、桥接器上游端口和交换机上游端口是保留的,因为即使链路被禁用,它也必须可由软件访问。写入此位后,任何读取立即反映写入的值,与链路状态无关。清除此位后,软件必须小心遵守有关 Conventional Reset 后首次 Configuration 读取的时序要求(参见第 846 页的"Reset Exit")。

## **Retrain Link** 

只要认为有必要,例如用于错误恢复,此位允许软件发起链路重新训练。该位不适用于端点设备以及桥接器和交换机的上游端口,并为其保留。当设置为 1b 时,这将在 Configuration 写入请求完成返回之前将 LTSSM 定向到 Recovery 状态。

## **Extended Synch** 

就其对训练的影响而言,此位用于大幅延长两种情况下的时间,以帮助较慢的外部测试或分析硬件在链路恢复正常通信之前与之同步。其中一种是在退出 L0s 时,设置此位强制在进入 L0 之前传输 4096 个 FTS。另一种情况是在进入 Recovery.RcvrCfg 之前的 Recovery 状态中,它强制传输 1024 个 TS1。

**643** 

## **PCI Ex ress Technolo p gy** 

## _Figure 14-71: Link Control 寄存器_ 

**==> picture [313 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


**644** 

## Part Five: 

# Additional System Topics 

## _**15 Error Detection and Handling**_ 

## **The Previous Chapter**
