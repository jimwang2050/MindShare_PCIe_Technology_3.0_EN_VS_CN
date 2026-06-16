关于 Electrical Idle 的旁注,规范的早期版本预计 Electrical Idle 将基于测量电压阈值的 squelch 检测电路。后来,随着速度增加,检测如此小的电压差异变得越来越困难。因此,较新的规范版本允许通过观察链路行为来推断 Electrical Idle,而不是实际测量电压。但是,如果未使用电压电平来检测进入 Electrical Idle,那么它也不能用于检测退出 Electrical Idle。为了处理该问题,引入了一种称为 EIEOS(Electrical Idle Exit Ordered Set)的新有序集。EIEOS 由全零和全 1 的交替字节组成,在 Lane 上产生低频时钟的效果。一旦接收器进入 Electrical Idle,它可以监视信号上的此模式以通知它链路正在退出 Electrical Idle。

_退出到"Rx_L0s.FTS"_

在接收器检测到退出 Electrical Idle 之后,下一个状态将是 Rx_L0s.FTS。

## **Rx_L0s.FTS。** 

在此子状态中,接收器已注意到退出 Electrical Idle,现在正尝试在传入的位流(实际上是 FTS 有序集)上重新建立位和符号或块锁。

_退出到"L0 状态"_

如果在 8b/10b 编码中所有已配置的 Lane 上接收到 SOS,或者在 128b/130b 编码中接收到 SDS,则下一个状态将是 L0。接收器必须能够在此之后立即接受有效数据,并且必须在离开此状态之前完成 Lane-to-Lane 去偏移。

**606** 

**Chapter 14: Link Initialization & Training** 

## _退出到"Recovery 状态"_

否则,在 N_FTS 超时后,下一个状态将是 Recovery。如果是这样,发送器也必须进入 Recovery,尽管允许完成正在进行的任何 TLP 或 DLLP。如果发生超时,规范建议增加 N_FTS 值以降低再次发生的可能性。N_FTS 超时定义如下:

对于 8b/10b,最小超时为 40 * [N_FTS + 3] * UI,而最大允许为该时间的两倍。由于每个符号需要 10 位(UI 表示一个位时间),因此这等于 (4*N_FTS + 12) 个符号。额外的 12 个符号解释为:最大大小 SOS 的 6 个 + 4 个用于可能的额外 FTS + 2 个用于符号裕度。总之,最小时间是发送所请求的 FTS 数量加上 12 个符号所需的时间,而最大时间是该时间的两倍。

如果设置了扩展同步位,则最小时间 = 2048 FTS,最大时间 = 4096 FTS。接收器将使用的实际超时值还必须考虑 2.5 GT/s 以外速度的 4 到 8 个 EIE 符号。

对于 128b/130b,超时值被给定为最小 130 * [N_FTS + 5 + 12 + Floor(N_FTS/32)] * UI,最大为该时间的两倍。值 130 * UI 意味着 130 个位时间,代表一个块,因此如果我们删除这两个值,我们可以说我们正在查看 [N_FTS + 5 + 12 + Floor(N_FTS/32)] 个块。值 [5 + Floor(N_FTS/32)] 表示在此期间需要发送的 EIEOS 数。每 32 个 FTS 之后将发送一个 EIEOS,因此 Floor(N_FTS/32) 给出该数字。另一个 5 是由第一个 EIEOS、最后一个 EIEOS、SDS、周期性 EIEOS 和当 N_FTS 能被 32 整除时发送两个 EIEOS 后跟一个 SDS 的情况下发送的额外 EIEOS 解释的。最后,值 12 表示如果设置了扩展同步位将发送的 SOS 数量。当设置了该位时,超时将使用 N_FTS = 4096。

## **L1 状态** 

此链路电源状态与 L0s 状态相比,权衡了更长的退出延迟以获得更积极的电源管理。L1 是 ASPM 的一个选项,像 L0s 一样,意味着设备可以在硬件控制下自动进入和退出此状态,无需任何软件参与。但是,与 L0s 不同,软件也能够指示上游端口发起更改为 L1,它通过将设备电源状态写入较低级别(D1、D2 或 D3)来执行此操作。L1 状态与 L0s 的不同之处还在于它影响链路的两个方向。

**607** 

## **PCI Ex ress Technolo p gy** 

_Figure 14-42: L1 状态机_ 

**==> picture [260 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Directed and Remain in<br>EIOS Tx & Rx TTX-IDLE-MIN Electrical Idle<br>= 20 ns L1.Idle<br>L1.Entry<br>(Electrical Idle)<br>Tx in Electrical Idle Tx Directed or<br>Rx sees Electrical Idle Exit<br>Exit to<br>Recovery<br>**----- End of picture text -----**<br>


由于进入 Electrical Idle 可能表示链路伙伴希望进入 L0s、L1 或 L2,因此通过让两个伙伴事先同意何时将进入 L1 来处理应将哪个作为下一个状态。握手通知他们伙伴已准备好,因此可以安全地继续。有关此工作原理的更多详细信息,请参阅第 733 页的"Link Power Management 简介"部分。第 608 页的 Figure 14-42 显示了 L1 状态机,将在以下部分中描述。

## **L1.Entry** 

要使上游端口进入此状态,它必须向其链路伙伴发送进入 L1 的请求,并收到可以进入 L1 状态的确认。请求进入 L1 的原因可能是由于 ASPM 或软件参与。一旦接收到 L1 请求确认,上游端口将进入 L1.Entry 子状态。

要使下游端口进入此状态,它必须从上游端口接收 L1 进入请求,并向该请求发送肯定响应。然后下游端口等待接收 Electrical Idle Ordered Set (EIOS) 并让其接收 Lane 下降至 Electrical Idle。此时,下游端口进入 L1.Entry 子状态。

**608** 

**Chapter 14: Link Initialization & Training** 

## _在 L1.Entry 期间_

所有已配置的发送器发送一个 EIOS 并进入 Electrical Idle,同时保持适当的 DC 共模电压。

## _退出到"L1.Idle"_

下一个状态将在 TTX-IDLE-MIN 超时(20ns)后是 L1.Idle。此时间旨在确保发送器已建立 Electrical Idle 条件。

## **L1.Idle** 

在此子状态期间,发送器保持处于 Electrical Idle 状态。

对于 2.5 GT/s 以外的速率,LTSSM 必须在此子状态中保持至少 40ns。在规范中,此延迟被称为"用于补偿逻辑电平中的延迟,以防链路进入 L1 后立即退出时使能 Electrical Idle 检测电路"。

## _退出到"Recovery 状态"_

当发送器被指示更改或任何接收器检测到退出 Electrical Idle 时,下一个状态将是 Recovery。离开 L1 的原因包括需要传递 DLLP 或 TLP,或希望更改链路宽度或速度。如果需要速度更改,则允许端口将 directed_speed_change 变量设置为 1b,并且必须将 changed_speed_recovery 变量清零至 0b。可选地,端口可以退出 L1,然后通过将 directed_speed_change 设置为 1b 并从 L0 进入 Recovery 来稍后启动速度更改。

## **L2 状态** 

这是比 L1 更深的电源状态,具有更长的退出延迟。当其设备置于 D3Cold 电源状态并且已完成的相应链路握手后,电源管理软件指示上游端口发起进入 L2(链路的两个方向都进入 L2)。

一旦系统了解到一切就绪,主电源将被关闭。断电后,链路电源状态将变为 L2 或 L3,具体取决于是否可获得称为 VAUX(辅助电压)的辅助电源。如果存在 VAUX,则链路进入 L2;如果不存在,则进入 L3。

L2 的动机是使用 VAUX 提供的小功率来通知系统何时发生需要恢复链路电源的事件。

**609** 

## **PCI Ex ress Technolo p gy** 

有两种标准方式设备可以通知系统此类事件。一种是称为 WAKE# 引脚的边带信号,另一种是称为"Beacon"的带内信号。L2 状态对于 WAKE# 是不需要的,但如果要使用可选的 Beacon,则是必需的。规范明确指出,以 5.0 或 8.0 GT/s 运行的设备不需要支持 Beacon,因此这似乎是旧版支持,仅对以 2.5 GT/s 运行的设备有意义。有关链路唤醒选项的更多详细信息,请参阅第 772 页的"Waking Non-Communicating Links"。

如果支持,Beacon 是低频(30 KHz - 500 MHz)带内信号,支持唤醒功能的上游端口必须能够在至少 Lane 0 上发送它,下游端口必须能够接收它。像交换机这样的中间设备,如果在下游端口上接收到 Beacon,必须将其转发到其上游端口。Beacon 的最终目的地是根复合体 (Root Complex),因为这是系统电源控制逻辑预期所在的位置。

进入 Electrical Idle 的发送器可能表示希望进入任何低功耗链路状态(L0s、L1 或 L2),因此需要一种区分它们的方法。对于 L2,这通过让链路伙伴事先同意将通过使用握手序列来进入 L2 来处理,以确保它们都已准备好。有关此工作原理的更多详细信息,请参阅第 733 页的"Link Power Management 简介"部分。第 611 页的 Figure 14-43 显示了 L2 进入和退出状态机,将在以下文本中描述。

**610** 

**Chapter 14: Link Initialization & Training** 

_Figure 14-43: L2 状态机_ 

**==> picture [349 x 227] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from L0<br>Directed, and<br>EIOS both sent<br>and received Upstream Tx<br>sends Beacon<br>Upstream Port directed to send Beacon,<br>L2.Idle or Downstream Port detects Beacon<br>(Electrical Idle, L2.TransmitWake<br>No DC CMV)<br>Rx termination enabled,<br>Rx looking for  Upstream Rx detects<br>Electrical Idle Exit Electrical Idle Exit<br>Root Port detects Beacon,<br>or Upstream Port sees<br>Electrical Idle Exit Exit to<br>Detect<br>**----- End of picture text -----**<br>


## **L2.Idle** 

要进入此子状态,链路两端的所有必要握手过程必须已经发生,并且端口已发送和接收到所需的 EIOS。

所有已配置的发送器必须保持处于 Electrical Idle 状态至少 TTX-IDLE-MIN 超时(20ns)。但是,由于主电源现在将被关闭,因此它们不需要将 DC 共模电压保持在规范范围内。接收器在 20ns 超时到期之前不会开始寻找 Electrical 退出条件。所有接收器终端必须保持处于低阻抗条件下的使能状态。

## _退出到"L2.TransmitWake"_

如果上游端口被指示发送 Beacon(Beacon 始终且仅指向上游到根复合体),则下一个状态将是 L2.TransmitWake。

**611** 

**PCI Ex ress Technolo p gy** 

如果交换机的下游端口检测到 Beacon,则它必须指示交换机的上游端口退出到 L2.TransmitWake 并开始发送 Beacon。

## _退出到"Detect 状态"_

一旦主电源恢复,下一个状态将是 Detect。

如果此端口具有主电源,但它在任何"预定的"Lane 上检测到退出 Electrical Idle,这意味着那些可以协商为 Lane 0 的 Lane(多 Lane 链路必须具有至少两个预定的 Lane),则下一个状态将是 detect。当这种情况发生在交换机上游端口时,交换机还必须将其下游端口转换为 Detect。

## **L2.TransmitWake**
