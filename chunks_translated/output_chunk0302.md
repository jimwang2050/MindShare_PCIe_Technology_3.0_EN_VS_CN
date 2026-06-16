在此子状态期间,发送器将在至少 Lane 0 上发送 Beacon。请注意,此状态仅适用于上游端口,因为只有它们才能发送 Beacon。

## _退出到"Detect 状态"_

如果在任何上游端口的接收器上检测到退出 Electrical Idle,则下一个状态将是 Detect。当然,必须已经恢复了设备的电源,以便邻居退出 Electrical Idle。

## **Hot Reset 状态** 

由于以下任一原因,端口将进入 Hot Reset 状态:它是一个桥接器并且软件对其配置空间进行了编程以向下游传播 Hot Reset,如第 837 页的"Hot Reset(带内复位)"中所述;或者由于端口接收到两个连续的 Hot Reset 位为 1 的 TS1。

## _在 Hot Reset 期间_

端口持续传输 Hot Reset 位设置的 TS1,但不更改已配置的 Link 和 Lane 编号。

如果交换机的上游端口进入 Hot Reset 状态,则所有已配置的下游端口必须尽快转换为 Hot Reset。

## _退出到"Detect 状态"_

在发起 Hot Reset 的桥接器中,一旦软件清除启动 Hot Reset 的配置空间位,桥接端口将进入 Detect。但是,该端口必须保持在 Hot Reset 状态至少 2ms。

**612** 

**Chapter 14: Link Initialization & Training** 

对于由于接收到两个连续的 Hot Reset 位为 1 的 TS1 而进入 Hot Reset 的端口,只要它继续接收此类 TS1,它就会保持此状态。一旦端口停止接收 Hot Reset 位为 1 的 TS1,它将转换到 Detect 状态。但是,该端口必须保持在 Hot Reset 状态至少 2ms。

## **Disable 状态** 

禁用的链路处于 Electrical Idle 状态,不必保持 DC 共模电压。软件通过设置设备的 Link Control 寄存器中的 Link Disable 位(参见第 644 页的 Figure 14-71)来启动此操作,然后设备发送 Disable Link 位为 1 的 TS1。

## _在 Disable 期间_

所有 Lane 发送 16 到 32 个 Disable Link 位为 1 的 TS1,发送一个 EIOS(对于 5.0 GT/s 情况为两个连续的 EIOS),然后转换到 Electrical Idle。DC 共模电压不需要在规范范围内。

如果已发送 EIOS(对于 5.0 GT/s 情况为两个连续的 EIOS)并且在任何已配置的 Lane 上也接收到 EIOS,则 LinkUp = 0b(False),并且 Lane 被认为是禁用的。

## _退出到"Detect 状态"_

对于上游端口,当在接收器处检测到 Electrical Idle,或在 2ms 超时内未接收到 EIOS 时,下一个状态将是 Detect。

对于下游端口,下一个状态也将是 Detect,但要等到软件将 Link Disable 位清零至 0b 之后。

## **Loopback 状态** 

Loopback 状态是在正常操作期间不使用的测试和调试功能。作为 Loopback 主站的设备可以通过发送 Loopback 位为 1 的 TS1 将链路伙伴置于 Loopback 从站模式。这可以在线完成,从而允许使用 Loopback 状态对链路执行 BIST(Built In Self Test)的可能性。

一旦处于此状态,Loopback 主站将有效符号发送给 Loopback 从站,然后 Loopback 从站回显它们。Loopback 从站继续执行

**613** 

## **PCI Ex ress Technolo p gy** 

时钟容差补偿,因此主站必须继续以正确的间隔插入 SOS。要执行时钟容差补偿,Loopback 从站可能必须向回显给 Loopback 主站的 SOS 添加或删除 SKP 符号。

当 Loopback 主站发送 EIOS 并且接收器检测到 Electrical Idle 时,Loopback 状态退出。Loopback 状态机如图 14-44(第 614 页)所示,并在以下文本中描述。

_Figure 14-44: Loopback 状态机_ 

**==> picture [368 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>from Configuration<br>Or Recovery<br>Slave: Enter Electrical<br>Master sends valid Idle for 2ms<br>Master sends Master receives Symbols - Master: Tx EIOSs<br>Identical TS1’s; Slave required to and enter Electrical<br>TS1s w/ Loopback Slave has retransmit exactly Slave: Directed or  Idle for 2 ms<br>bit set entered 4 EIOS seen<br>Loopback Master: Directed<br>Loopback.Entry Loopback.Active Loopback.Exit<br>Timeout less than<br>100 ms Exit to<br>Detect<br>**----- End of picture text -----**<br>


## **Loopback.Entry** 

此子状态的典型行为是 Loopback Master 发送 Loopback 位置 1 的 TS1,直到它开始看到那些返回的 TS1。一旦 Loopback Master 看到返回的 Loopback 位为 1 的 TS1,它就知道其链路伙伴现在正在作为 Loopback Slave 运行,只是简单地重复它接收到的所有内容。

在此子状态中,链路不被视为处于活动状态(LinkUp = 0b)。此外,TS1 和 TS2 中使用的 Link 和 Lane 编号被接收器忽略。规范对 128b/130b 编码的 Lane 编号的使用进行了有趣的观察。事实证明,每个 Lane 对其加扰器使用不同的种子值(参见第 430 页的"加扰")。因此,如果 Lane 编号在进入 Loopback 模式之前尚未协商,则链路伙伴可能具有不同的 Lane 分配,因此将无法识别传入的符号。这可以通过在指

**614** 

**Chapter 14: Link Initialization & Training** 

定 Master 进入 Loopback 状态之前等待 Lane 编号协商完成,或者通过指示 Master 在 Loopback.Entry 期间设置 Compliance Receive 位,或通过其他方法来避免。

## **Loopback Master:** 

在此子状态中,Loopback Master 将持续发送 Loopback 位置 1 的 TS1。Master 还可以在 TS1 中置位 Compliance Receive 位以帮助测试,当一个或两个端口在速率更改后难以获取位锁、符号锁或块对齐时。如果设置了该位,则在此状态期间不得清除它。

如果此子状态是从 Configuration.Linkwidth.Start 进入的,请检查正在使用的速度是否为两个链路伙伴共同支持的最高速率。如果不是:

- 更改为最高共同速度。发送 16 个 Loopback 位置 1 的 TS1,后跟一个 EIOS(如果当前速度为 5.0 GT/s,则为两个 EIOS),然后进入 Electrical Idle 1ms。在空闲期间,将速度更改为最高共同支持的速率。

- 如果最高共同速率为 5.0 GT/s,则从站的 Tx 去加重由 Master 通过将其 TS1 中的 Selectable De-emphasis 位设置为所需值来控制(1b = -3.5 dB,0b = -6 dB)。

- 对于 5.0 GT/s 及更高的数据速率,Master 的发送器可以选择其想要的任何去加重设置,无论它发送给从站的设置如何。

- 潜在问题:如果在链路已经训练到 L0 并且 LinkUp = 1b 之后进入 Loopback,则一个端口可能从 Recovery 进入 Loopback,而伙伴从 Configuration 进入。如果发生这种情况,后一个端口可能尝试更改速度,而从 Recovery 进入的端口则不会,从而导致结果未定义的情况。规范指出,测试设置必须避免此类冲突情况。

## _退出到"Loopback.Active"_

下一个状态将在 2ms 后是 Loopback.Active,前提是 TS1 中的 Compliance Receive 位已设置,或者在设计特定数量的 Lane 上接收到两个连续的 Loopback 位为 1 的 TS1 并且 TS1 中的 Compliance Receive 位未设置。

请注意,如果速度已更改,Master 必须确保已发送足够的 TS1,以便从站能够在进入 Loopback.Active 状态之前获取符号锁或块对齐。

**615** 

## **PCI Ex ress Technolo p gy** 

## _退出到"Loopback.Exit"_

如果不满足进入 Loopback.Active 的任一条件,则下一个状态将在小于 100ms 的设计特定超时后是 Loopback.Exit。

## **Loopback Slave:** 

此子状态通过接收两个连续的 Loopback 位为 1 的 TS1 来进入。

如果此子状态是从 Configuration.Linkwidth.Start 进入的,请检查正在使用的速度是否为两个链路伙伴共同支持的最高速度。如果不是:

- 更改为最高共同速度。发送一个 EIOS(如果当前速度为 5.0 GT/s,则为两个 EIOS),然后进入 Electrical Idle 2ms。在空闲期间,将速度更改为最高共同支持的速率。

- 如果最高共同速率为 5.0 GT/s,则根据接收到的 TS1 中的 Selectable De-emphasis 位设置发送器的去加重(1b = -3.5 dB,0b = -6 dB)。

- 如果最高共同速率为 8.0 GT/s,并且:

   - a) EQ TS1 指示从站进入此状态,则使用它们指定的 Tx Preset 设置。

   - b) 普通 TS1 指示从站进入此状态,则允许从站使用其默认发送器设置。

## _退出到"Loopback.Active"_

如果将指示从站进入此状态的传入 TS1 中的 Compliance Receive 位置 1,则下一个状态将是 Loopback.Active。从站不需要等待特定边界来发送环回数据,并且允许截断任何正在进行的有序集。

否则,从站发送 Link 和 Lane 编号设置为 PAD 的 TS1,并且下一个状态将是 Loopback.Active,前提是:

- 速率为 2.5 或 5.0 GT/s,并且所有 Lane 上获取了符号锁。

- 速率为 8.0 GT/s,并且在所有活动 Lane 上看到两个连续的 TS1。通过评估和应用 TS1 中给定的值来处理均衡,只要它们受支持并且 EC 值适合端口方向(下游端口为 10b,

**616** 

**Chapter 14: Link Initialization & Training** 

上游端口为 11b)。可选地,端口可以接受此情况下的任一 EC 值。如果应用了设置,则它们必须在接收后 500ns 内生效,并且不得导致发送器在任何电气规范上违规超过 1ns。与 Recovery.Equalization 中的过程相比的一个显着差异是,从站正在发送的 TS1 中不回显新设置。– 对于 8b/10b,从站必须仅在符号边界上转换为环回数据,但允许截断任何正在进行的有序集。对于 128b/130b,未指定何时可以发送环回数据的边界,并且仍然允许截断任何正在进行的有序集。

## **Loopback.Active** 

在此子状态期间,Loopback Master 发送有效的编码数据,并且在准备退出 Loopback 之前不应发送 EIOS。Loopback Slave 在不修改的情况下回显接收到的信息(即使编码被确定为无效),可能的例外是反转极性,正如在 Polling 状态中确定的那样。从站还继续执行时钟容差补偿。这意味着必须根据需要添加或删除 SKP,但不要求所有 Lane 发送相同数量。

## _退出到"Loopback.Exit"_

对于 Loopback master,如果被指示,下一个状态将是 Loopback.Exit。

对于 Loopback slave,如果以下两个条件之一为真,则下一个状态将是 Loopback.Exit:

- 从站被指示退出,或在任何 Lane 上看到四个连续的 EIOS。

- 可选地,如果当前速度为 2.5 GT/s,并且接收到 EIOS 或在任何 Lane 上检测到或推断出 Electrical Idle。如果任何已配置的 Lane 在 128µs 内未检测到退出 Electrical Idle,则可以推断 Electrical Idle。
