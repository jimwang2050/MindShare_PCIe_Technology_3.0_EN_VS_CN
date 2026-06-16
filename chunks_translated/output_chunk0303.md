从站必须能够在接收到 EIOS 后 1ms 内检测到任何 Lane 上的 Electrical Idle。在接收到 EIOS 和实际检测到 Electrical Idle 之间,Loopback Slave 可能接收的位流未被编码方案定义,并且可以将其环回给发送器。

**617** 

## **PCI Ex ress Technolo p gy** 

## **Loopback.Exit** 

在此子状态期间,Loopback Master 发送一个 EIOS(对于仅支持 2.5 GT/s 的端口)或八个连续的 EIOS(对于支持高于 2.5 GT/s 速率的端口;对于仅支持 2.5 GT/s 的端口,也可选地发送 8 个),然后在所有 Lane 上进入 Electrical Idle 2ms。

- Loopback Master 必须在发送最后一个 EIOS 后,在 TTX-IDLE-SET-TO-IDLE[内转换到 Electrical Idle。请注意,EIOS 标记主站的]发送和比较操作的结束。Master 在接收到任何 EIOS 后接收到的任何数据都是未定义的,应予以忽略。

Loopback slave 必须在所有 Lane 上进入 Electrical Idle 2ms,但必须回显在检测到 Electrical Idle 之前接收到的所有符号,以确保 Master 将 EIOS 的到达视为逻辑发送和比较操作的结束。

## _退出到"Detect 状态"_

一旦已交换所需的 EIOS 并且 Lane 已在 Electrical Idle 中保持 2ms,下一个状态将是 Detect。

## **Dynamic Bandwidth Changes** 

更高的数据速率和更宽的 PCIe 链路提供比前几代更高的性能,但也使用更多功率。因此,2.0 规范的作者选择包括另一对电源管理机制,允许硬件动态调整链路速度和宽度。这些允许链路在需要性能时使用最高速度和最宽的链路,或者降低到较低速度或较窄的链路宽度或两者兼而有之以降低功率。与更改链路或设备电源状态相比,此方法有两个明显的优势。

首先,无论是否更改,链路始终能够通信,服务中断相对较短以进行更改。其次,节能可以更大。例如,与处于 L0s 状态下的 x16 链路相比,x16 链路作为活动 x1 链路运行几乎肯定会使用更少的功率。

其次,除了节能之外,带宽缩减还可用于解决可靠性问题。例如,可能是高速链路产生不可接受的可靠性,在这种情况下,允许任一链路组件从其通告的支持速率列表中删除有问题的速度。组件如何进行可靠性确定未指定。

**618** 

**Chapter 14: Link Initialization & Training** 

有趣的是,也允许组件进入 Recovery 状态并通告一组不同的支持速度,而不在此过程中请求速度更改。

更改链路速度或链路宽度需要重新训练链路。当链路处于 L0 状态并且需要更改速度时,需要更改速度的端口的 LTSSM 开始向其邻居发送 TS1。这样做会导致两个相关端口的 LTSSM 经过 Recovery 状态,在那里更改链路速度,然后返回 L0。

类似地,需要更改链路宽度的端口开始向其邻居发送 TS1。这样做会导致两个相关端口的 LTSSM 经过 Recovery 状态,然后经过 Configuration 状态,在那里更改链路宽度。LTSSM 最终返回到 L0,并建立新的链路宽度。

由于 LTSSM 参与动态链路带宽管理,讨论链路带宽管理的两个方面(动态链路速度更改和动态链路宽度更改)是有意义的。让我分别考虑这两个选项,从链路速度更改开始。

## **Dynamic Link Speed Changes** 

回顾一下,LTSSM 状态如图 14-45(第 620 页)所示,以便于回忆状态流。虽然根据 Gen1 规范,速度更改指示在 Polling 状态中执行,但随后的 Gen2 规范将此功能移至 Recovery 状态。

**619** 

## **PCI Ex ress Technolo p gy** 

_Figure 14-45: LTSSM 概述_ 

**==> picture [196 x 255] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>Polling<br>Configuration<br>L2 Recovery<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


在 Polling 状态期间,链路邻居之间交换 TS1,这些信息包含几种类型的信息,如图 14-46(第 621 页)所示。对我们来说,最有趣的部分是字节号 4,即 Rate Identifier。位 1、2 和 3 指示哪些数据速率可用,规范指出必须始终支持 2.5 GT/s,而如果支持 8.0 GT/s,则还必须支持 5.0 GT/s。

位 6 的含义取决于端口是面向上游还是下游,以及也取决于端口所处的 LTSSM 状态。但是,对于速度更改情况,选项会减少,因为仅来自上游端口的位才有意义,仅指示速度更改是否是自主事件。"自主"意味着端口出于其自身的硬件特定原因请求此更改,而不是由于可靠性问题。位 7 由上游端口用于请求速度更改。这些值在 TS2 中非常相似,尽管位 6 现在具有另一种含义,与我们稍后将讨论的自主链路宽度更改相关。

**620** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-46: TS1 内容_ 

**==> picture [315 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link #<br>Rate Identifier<br>2 Lane # Bit 0 Reserved, = 0<br>3 # FTS Bit 1 Indicates 2.5 GT/s support<br>4 Rate ID Bit 2 Indicates 5.0 GT/s support<br>5 Train Ctl Bit 3 Indicates 8.0 GT/s support<br>6 Bit 4:5 Reserved, = 0<br>TS ID Bit 6 Autonomous Change / Selectable De-<br>13 emphasis<br>14 TS ID Bit 7 Speed Change<br>15 TS ID<br>**----- End of picture text -----**<br>


_Figure 14-47: TS2 内容_ 

**==> picture [316 x 177] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM<br>1 Link # Rate Identifier<br>Bit 0 Reserved, = 0<br>2 Lane #<br>Bit 1 Indicates 2.5 GT/s support<br>3 # FTS<br>Bit 2 Indicates 5.0 GT/s support<br>4 Rate ID<br>Bit 3 Indicates 8.0 GT/s support<br>5 Train Ctl<br>Bit 4:5 Reserved, = 0<br>6<br>Bit 6 Autonomous Change / Link Up-<br>TS ID configure Capability / Selectable De-<br>13 emphasis<br>14 TS ID Bit 7 Speed Change<br>15 TS ID<br>**----- End of picture text -----**<br>


**621** 

## **PCI Ex ress Technolo p gy** 

## **上游端口发起速度更改** 

速度更改必须由上游端口(面向上游的端口)发起,并通过转换到 Recovery 状态来完成。Recovery 状态的子状态如图 14-48(第 622 页)所示,本次讨论中感兴趣的部分由椭圆突出显示。此处后面的讨论是整个速度更改过程的相对较高级别的概述,不会深入到 LTSSM 操作的详细信息。要了解更多信息,请参阅第 571 页的"Recovery State"讨论。

_Figure 14-48: Recovery 子状态_ 

**==> picture [342 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Recovery.Speed<br>Entry from Loopback Exit to<br>L1, L0, L0s Configuration<br>Recovery.Equalization<br>Recovery.RcvrLock Recovery.Idle Exit to<br>(bit/symbol re-lock) Recovery.RcvrCfg (Send idle data) Disabled<br>Exit to Hot<br>Exit to Exit to Reset<br>Configuration Detect<br>Exit to L0<br>**----- End of picture text -----**<br>


## **速度更改示例** 

为了说明该过程,请考虑图 14-49(第 623 页)中所示的速度更改示例。请注意,在此示例中已删除 Equalization 子状态以使图表更简单且更易于理解。该示例显示了从 2.5 GT/s 到 5.0 GT/s 的更改,因此无论如何不使用 Equalization 子状态。更改为 8.0 GT/s 将经历相同的过程,但只需在该过程结束时添加通过 Equalization 子状态的一次行程。要

**622** 

**Chapter 14: Link Initialization & Training** 

要了解有关均衡过程的更多信息,请参阅第 587 页的"Recovery.Equalization"。

此示例中的端点 (Endpoint) (只能具有上游端口)显示连接到根复合体 (Root Complex),后者只能具有下游端口。只有上游端口可以启动速度更改过程,它这样做是因为其 _Directed Speed Change_ 标志之前已根据某些硬件特定条件设置。要启动序列,它将其 LTSSM 更改为 Recovery 状态,进入 Recovery.RcvrLock 子状态,并发送 Speed Change 位为 1 且列出其将支持的速率的 TS1,如图 14-49(第 623 页)所示。当下游端口看到传入的 TS1 时,它也更改为 Recovery 状态并开始发回 TS1。由于 Speed Change 位已在传入的 TS1 中设置,这将在 Root Port 中设置 _Directed Speed Change_ 标志,并且传出的 TS1 也将设置该位。链路将尝试使用的速度将是最高共同支持的速度,因此,如果设备希望使用较低速度,它只需在此时不将较高速度列为受支持。

_Figure 14-49: 速度更改 - 已发起_ 

**==> picture [336 x 196] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 0 Directed Speed Change = 1<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 1<br>TS1 TS1 TS1 TS1<br>Root PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>TS1 TS1 TS1 TS1<br>Speed_Change = 1<br>**----- End of picture text -----**<br>


当上游端口检测到返回的 TS1 时,其状态机更改为 Recovery.RcvrCfg 子状态,并开始发送仍设置了 Speed Change 位的 TS2,如图 14-50(第 624 页)所示。这些

**623** 

## **PCI Ex ress Technolo p gy** 

如果此更改不是由链路上的可靠性问题引起的,则 TS2 现在还将设置 Autonomous Change 位。当下游端口看到传入的 TS2 时,它也更改为 Recovery.RcvrCfg 子状态,并返回设置了 Speed Change 位的 TS2。但是,在 Recovery 期间,下游端口的 TS2 中的 Autonomous Change 位是保留的。

_Figure 14-50: 速度更改 - 第 2 部分_ 

**==> picture [371 x 230] intentionally omitted <==**

**----- Start of picture text -----**<br>
Directed Speed Change = 1 Directed Speed Change = 1<br>Entry Entry<br>Speed Speed<br>RcvrLock RcvrCfg RcvrLock RcvrCfg<br>Speed_Change = 1<br>TS2 TS2 TS2 TS2<br>Root  PCIe<br>Link Speed = 2.5 GT/s<br>Complex Endpoint<br>TS2 TS2 TS2 TS2<br>Speed_Change = 1<br>Autonomous Change = 1<br>**----- End of picture text -----**<br>


一旦每个端口看到 8 个连续的 Speed Change 位设置的 TS2,它们就知道下一步将是进入 Recovery.Speed 子状态,如图 14-51(第 625 页)所示。此时,下游端口需要记录传入 TS2 中的 Autonomous Change 位的设置。为支持此操作,已将一些额外字段添加到 PCIe Capability 寄存器中。

链路带宽更改的状态位在 Link Status 寄存器中找到,如图 14-52(第 625 页)所示。如果设备能够并已启用,状态更改还可用于生成中断以将这些事件通知软件。该功能由 Link Bandwidth Notification Capable 位报告,如图 14-53(第 626 页)所示,并通过 Link Control 寄存器中的 Interrupt Enable 位启用,如图 14-54 所示,

**624**
