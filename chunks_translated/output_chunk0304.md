**Chapter 14: Link Initialization & Training** 

第 626 页。请注意,有两种情况:自主和带宽管理。自主意味着更改不是由可靠性问题引起的,而带宽管理意味着是。

_Figure 14-51: 速度更改 - 第 3 部分_ 

**==> picture [336 x 243] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 0<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>TS2 TS2 TS2 EIOSTS2<br>SSS<br>Root PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>EIOSTS2 TS2 TS2 TS2<br>Autonomous Change = 1<br>Root Complex Config Space<br>Link Autonomous Bandwidth Status bit = 1<br>i<br>Figure 14‐52: Bandwidth Change Status Bits<br>**----- End of picture text -----**<br>


**625** 

## **PCI Ex ress Technolo p gy** 

_Figure 14-53: Bandwidth Notification Capability_ 

_Figure 14-54: Bandwidth Change Notification Bits_ 

**626** 

**Chapter 14: Link Initialization & Training** 

一旦到达 Recovery.Speed 子状态,链路将在两个方向上置于 Electrical Idle 条件,并且内部更改速度。所选速度将是 TS1 和 TS2 的 Rate ID 字段中报告的最高共同支持的速度。在此示例中,结果为 5.0 GT/s,因此将更改为该速度。经过一段时间后,链路邻居都转换回 Recovery.RcvrLock 并通过再次发送 TS1 退出 Electrical Idle,如图 14-55(第 627 页)所示。当上游端口看到它们返回时,它转换为 Recovery.RcvrCfg 并开始发送 TS2,类似于之前。但是,这次未设置 Speed Change 位。最终,从未设置 Speed Change 位的下游端口也看到了 TS2 返回,此时状态机转换到 Recovery.Idle,然后返回 L0。

如果速度更改由于某种原因失败,则不允许组件在返回 L0 后至少 200ms 或直到链路伙伴通告支持更高速度之前(以先到者为准)再尝试该速度或更高的速度。

_Figure 14-55: 速度更改完成_ 

**==> picture [364 x 193] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 0<br>Entry Entry<br>Speed Speed<br>Exit to L0 Exit to L0<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 0<br>TS21 TS21 TS21 TS21<br>Root PCIe<br>Link Speed = 5.0 GT/s<br>Complex Endpoint<br>TS21 TS21 TS21 TS21<br>Speed_Change = 0<br>**----- End of picture text -----**<br>


## **速度更改的软件控制** 

软件无法控制硬件何时做出更改速度的决定,但可以限制或禁用此功能。限制它是通过设置 Link Control 2 Register(如图 14-56(第 628 页)所示)中的 Target Link Speed 值来实现的。这充当上游端口可用速度的上限,它将尝试维持该值或两个链路邻居都支持的最高速度,以较低者为准。软件还可以通过在上游组件中设置 Target Link Speed 然后设置 Link Control 寄存器(如图 14-57(第 629 页)所示)中的 Retrain Link 位来强制使用特定速度。如前所述,任何基于硬件的链路速度或宽度更改都会通过 Link Bandwidth Notification Mechanism 通知软件。最后,可以通过设置 Hardware Autonomous Speed Disable 位来禁用速度更改机制。

_Figure 14-56: Link Control 2 寄存器_ 

**628** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-57: Link Control 寄存器_ 

## **Dynamic Link Width Changes** 

用于更改链路速度的相同基本操作也可用于更改链路宽度,尽管由于涉及更多 LTSSM 步骤,该序列稍微更复杂。在启用链路宽度更改之前,软件需要注意的一件重要事情是链路邻居是否支持从窄链路恢复到宽链路(称为 Upconfiguring the Link)。设备在训练期间发送的 TS2 的 Rate ID 字段的位 6 中报告此能力,如图 14-58(第 630 页)所示。如果组件不支持此功能,则意味着更改到较窄的链路宽度将是单向事件,并且仅适用于链路上存在可靠性问题的情况。

**629** 

## **PCI Ex ress Technolo p gy** 

_Figure 14-58: TS2 内容_ 

**==> picture [368 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link # Rate Identifier<br>Bit 0 Reserved, = 0<br>2 Lane #<br>Bit 1 Indicates 2.5 GT/s support<br>3 # FTS<br>Bit 2 Indicates 5.0 GT/s support<br>4 Rate ID<br>Bit 3 Indicates 8.0 GT/s support<br>5 Train Ctl<br>Bit 3:5 Reserved, = 0<br>6 Bit 6 Autonomous Change / Link Up-<br>configure Capability / Selectable De-<br>TS ID<br>emphasis<br>13 Bit 7 Speed Change<br>14 TS ID<br>15 TS ID<br>**----- End of picture text -----**<br>


## **链路宽度更改示例** 

考虑图 14-59(第 631 页)中连接到端点 (千兆以太网设备) 的 Root Port 的示例。只有上游端口将发起此更改,并且它像之前一样通过进入 Recovery 状态来开始。但是,这次未设置 Speed Change 位。为了确定新的链路宽度是什么,上游端口将需要告诉下游端口从 Recovery 状态转换为 Configuration 状态,然后再返回 L0,如图 14-60(第 631 页)所示。Configuration 状态中有几个子状态,其简化版本如图 14-61(第 632 页)所示。我们将介绍该序列,以清楚地了解步骤的工作原理。

**630** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-59: 链路宽度更改示例_ 

**==> picture [199 x 190] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root  Ethernet<br>Complex Device<br>Lane Lane<br>0 0<br>1 1<br>2 Lan2<br>e<br>3 3<br>**----- End of picture text -----**<br>


_Figure 14-60: 链路宽度更改 LTSSM 序列_ 

**==> picture [183 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Polling<br>Configuration<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


**631** 

## **PCI Ex ress Technolo p gy** 

_Figure 14-61: 简化的 Configuration 子状态_ 

**==> picture [136 x 351] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry from<br>Polling or Recovery<br>Config.Linkwidth.Start<br>Config.Linkwidth.Accept<br>Config.Lanenum.Wait<br>Config.Lanenum.Accept<br>Config.Complete<br>Config.Idle<br>Exit to<br>L0<br>**----- End of picture text -----**<br>


与之前一样,上游端口通过进入 Recovery 并发送 TS1 来启动此过程。这些未设置 Speed Change 位,如第 631 页的 Figure 14-59 中突出显示的示例所示,其中以太网设备在其上游端口上启动此过程。作为响应,下游端口发回 TS1,也清除了 Speed Change 位。Link 和 Lane 编号仍显示为与上次训练链路时未更改。参考第 622 页的 Figure 14-48,下一个状态是 Recovery.RcvrCfg,在该状态中链路伙伴交换 TS2。

**632** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-62: 链路宽度更改 - 开始_ 

**==> picture [296 x 299] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex<br>Device<br>Lane Lane<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:0) TS1 (Link:0, Lane:0)<br>0 0<br>TS1 (Link:0, Lane:0) TS1 (Link:0,  Lane:0) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:1) TS1 (Link:0, Lane:1)<br>1 1<br>TS1 (Link:0, Lane:1) TS1 (Link:0,  Lane:1) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:2) TS1 (Link:0, Lane:2)<br>Lan<br>2 2<br>e<br>TS1 (Link:0, Lane:2) TS1 (Link:0,  Lane:2) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>ink:PAD, Lane:PAD) TS1 (Link:0, Lane:3) TS1 (Link:0, Lane:3)<br>3 3<br>TS1 (Link:0, Lane:3) TS1 (Link:0,  Lane:3) TS1 (Link:PAD, Lan<br>Speed Change = 0 Speed Change = 0<br>**----- End of picture text -----**<br>


由于未请求速度更改,因此下一个状态是 Recovery.Idle。在该状态下,端口通常发送逻辑空闲符号(全零),下游端口会这样做,如图 14-63(第 634 页)所示。但是,上游端口被指示更改链路宽度,因此它不会发送预期的 Idle 符号。相反,它发送 Link 和 Lane 编号均为 PAD 的 TS1。下游端口识别出先前配置的 Lane 现在的 Lane 编号为 PAD,这会导致其转换为第一个 Configuration 子状态:Config.Linkwidth.Start。

**633** 

## **PCI Ex ress Technolo p gy** 

## _Figure 14-63: 链路宽度更改 - Recovery.Idle_ 

**==> picture [311 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex<br>Device<br> (Link:PAD, L ane:PAD)Lane Idle Data Idle Data Lane<br>0 0<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>1 1<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>Lan<br>2 2<br>e<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br> (Link:PAD, L ane:PAD) Idle Data Idle Data<br>3 3<br>TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:P<br>Speed Change = 0 Speed Change = 0<br>**----- End of picture text -----**<br>


下游端口现在通过发送具有原始协商的 Link 编号但所有 Lane 编号为 PAD 的 TS1 来启动下一步,如图 14-64(第 635 页)所示。上游端口在其希望"活动"的 Lane 上以匹配的 TS1 进行响应,但在其希望处于非活动状态的 Lane 上以 Link 和 Lane 编号均为 PAD 进行响应。当下游端口看到此响应时,它将转换为 Config.Linkwidth.Accept 子状态。请注意,这些 TS1 设置了 Autonomous Change 位。

**634** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-64: 标记活动 Lane_ 

**==> picture [335 x 293] intentionally omitted <==**

**----- Start of picture text -----**<br>
Gigabit<br>Root<br>Ethernet<br>Complex Desired<br>Device<br>Lane State<br>Lane Lane<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>0 0 Active<br>TS1 (Link:0, Lane:PAD) TS1 (Link:0, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>1 1 Inactive<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>Lan<br>2 2 Inactive<br>e<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>k:PAD, Lane:PAD) TS1 (Link:0, Lane: PAD) TS1 (Link:0, Lane: PAD)<br>3 3 Inactive<br>TS1 (L ink:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD) TS1 (Link:PAD, Lane:PAD)<br>Autonomous Change = 1 Autonomous Change = 1<br>**----- End of picture text -----**<br>
