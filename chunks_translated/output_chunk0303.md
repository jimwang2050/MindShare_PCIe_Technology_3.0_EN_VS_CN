在此子状态期间，发送器将在至少 Lane 0 上发送 Beacon。请注意，此状态仅适用于上游端口，因为只有它们才能发送 Beacon。

## _退出到"Detect 状态"_

如果在某个上游端口的接收器上检测到电气空闲退出，则下一个状态将是 Detect。当然，必须已经恢复了设备的供电，相邻设备才能从电气空闲中退出。

## **热复位状态**

端口进入热复位状态，要么是因为它是一个桥，并且软件对其配置空间进行编程以向下游传播热复位（如第 837 页的"热复位（带内复位）"中所述），要么是因为端口接收到了两个连续的、Hot Reset 位被置位的 TS1。

## _热复位期间_

端口以 Hot Reset 位置位连续发送 TS1，但不更改已配置的链路和 Lane 编号。

如果交换机的上游端口进入热复位状态，则所有已配置的下游端口必须尽快转换为热复位。

## _退出到"Detect 状态"_

在发起热复位的桥中，一旦软件清除了发起热复位的配置空间位，桥端口就进入 Detect。但是，端口必须在热复位状态中保持至少 2ms。

**612**

**第 14 章：链路初始化与训练**

对于由于接收到两个连续的、Hot Reset 位置位的 TS1 而进入热复位的端口，只要它继续接收此类 TS1，它就保持在该状态。一旦端口停止接收 Hot Reset 位置位的 TS1，它将转换到 Detect 状态。但是，端口必须在热复位状态中保持至少 2ms。

## **禁用状态**

禁用的链路处于电气空闲状态，无需维持 DC 共模电压。软件通过在设备的 Link Control 寄存器中设置 Link Disable 位（请参见第 644 页的图 14‐71）来启动此操作，然后设备发送 Link Disable 位置位的 TS1。

## _禁用期间_

所有 Lane 发送 16 到 32 个 Link Disable 位置位的 TS1，发送一个 EIOS（对于 5.0 GT/s 情况为两个连续的 EIOS），然后转换到电气空闲。DC 共模电压不需要在规范范围内。

如果发送了 EIOS（对于 5.0 GT/s 情况为两个连续的 EIOS），并且在任何已配置的 Lane 上也接收到了 EIOS，则 LinkUp = 0b（假），并且 Lane 被认为是禁用的。

## _退出到"Detect 状态"_

对于上游端口，当在接收器处检测到电气空闲或者在 2ms 超时内未接收到 EIOS 时，下一个状态将是 Detect。

对于下游端口，下一个状态也将是 Detect，但只有在软件将 Link Disable 位清零至 0b 后才会发生。

## **回环状态**

回环状态是一个测试和调试功能，在正常运行期间不使用。充当回环主设备的设备可以通过发送 Loopback 位置位的 TS1 将链路伙伴置于回环从设备模式。这可以在电路中完成，从而可以使用回环状态对链路执行 BIST（Built In Self Test，内建自测试）。

一旦进入此状态，回环主设备将有效的 Symbol 发送给回环从设备，然后回环从设备将其回显。回环从设备继续执行

**613**

## **PCI Express 技术**

时钟容差补偿，因此主设备必须继续以正确的间隔插入 SOS。为了执行时钟容差补偿，回环从设备可能必须向其回传给回环主设备的 SOS 添加或删除 SKP Symbol。

回环状态在回环主设备发送 EIOS 并且接收器检测到电气空闲时退出。回环状态机如图 14‐44（第 614 页）所示，并在以下文本中描述。

_图 14‐44：回环状态机_

**==> picture [368 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
Entry<br>
from Configuration<br>
Or Recovery<br>
Slave: Enter Electrical<br>
Master sends valid Idle for 2ms<br>
Master sends Master receives Symbols - Master: Tx EIOSs<br>
Identical TS1's; Slave required to and enter Electrical<br>
TS1s w/ Loopback Slave has retransmit exactly Slave: Directed or  Idle for 2 ms<br>
bit set entered 4 EIOS seen<br>
Loopback Master: Directed<br>
Loopback.Entry Loopback.Active Loopback.Exit<br>
Timeout less than<br>
100 ms Exit to<br>
Detect<br>
**----- End of picture text -----**<br>


## **Loopback.Entry**

此子状态的典型行为是回环主设备发送 Loopback 位置位的 TS1，直到它开始看到这些 TS1 被返回。一旦回环主设备看到 Loopback 位被置位的 TS1 被返回，它就知道其链路伙伴现在正在充当回环从设备，并简单地重复其接收到的所有内容。

在此子状态期间，链路不被认为是活动的（LinkUp = 0b）。此外，TS1 和 TS2 中使用的链路和 Lane 编号将被接收器忽略。规范对 128b/130b 编码的 Lane 编号的使用做了一个有趣的观察。事实证明，每个 Lane 使用不同的种子值用于其加扰器（参见第 430 页的"加扰"）。因此，如果在进入回环模式之前尚未协商 Lane 编号，则链路伙伴可能具有不同的 Lane 分配，因此将无法识别传入的 Symbol。这可以通过在指导主设备进入回环状态之前等待 Lane 编号协商完成，或者通过指导主设备在 Loopback.Entry 期间设置 Compliance Receive 位，或通过其他方法来避免。

**614**

**第 14 章：链路初始化与训练**

## **Loopback Master:**

在此子状态中，回环主设备将连续发送 Loopback 位置位的 TS1。主设备还可以在 TS1 中置位 Compliance Receive 位，以帮助当一个或两个端口在速率变化后难以获得位锁定、Symbol 锁定或块对齐时进行测试。如果该位被置位，则在此状态期间不得清除。

如果此子状态是从 Configuration.Linkwidth.Start 进入的，请检查当前使用的速率是否是两个链路伙伴共同支持的最高速率。如果不是：

- 更改为最高公共速率。发送 16 个 Loopback 位置位的 TS1，后跟一个 EIOS（如果当前速率为 5.0 GT/s，则为两个 EIOS），然后进入电气空闲状态 1ms。在空闲期间，将速率更改为共同支持的最高速率。

- 如果最高公共速率为 5.0 GT/s，则从设备的 Tx 去加重由主设备在 TS1 中将其 Selectable De‐emphasis 位设置为所需的值（1b = ‐3.5 dB，0b = ‐6 dB）来控制。

- 对于 5.0 GT/s 及更高的数据速率，主设备的发送器可以选择任何其想要的去加重设置，无论它发送给从设备的设置如何。

- 潜在问题：如果在链路已经训练到 L0 且 LinkUp = 1b 之后进入回环，则一个端口可能从 Recovery 进入回环，而其伙伴从 Configuration 进入。如果发生这种情况，后一个端口可能尝试更改速率，而从 Recovery 进入的端口不会更改，从而导致结果未定义的情况。规范指出测试设置必须避免此类冲突情况。

## _退出到"Loopback.Active"_

在 2ms 之后，如果 Compliance Receive 位在发出的 TS1 中被置位，或者在设计特定数量的 Lane 上接收到两个连续的、Loopback 位置位且 Compliance Receive 位未在发出的 TS1 中置位的 TS1，则下一个状态将是 Loopback.Active。

请注意，如果更改了速率，则主设备必须确保已发送了足够的 TS1，以便从设备能够在进入 Loopback.Active 状态之前获得 Symbol 锁定或块对齐。

**615**

**PCI Express 技术**

## _退出到"Loopback.Exit"_

如果进入 Loopback.Active 的两个条件均未满足，则在小于 100ms 的设计特定超时之后，下一个状态将是 Loopback.Exit。

## **Loopback Slave:**

此子状态通过接收 Loopback 位置位的两个连续的 TS1 进入。

如果此子状态是从 Configuration.Linkwidth.Start 进入的，请检查当前使用的速率是否是两个链路伙伴共同支持的最高速率。如果不是：

- 更改为最高公共速率。发送一个 EIOS（如果当前速率为 5.0 GT/s，则为两个 EIOS），然后进入电气空闲状态 2ms。在空闲期间，将速率更改为共同支持的最高速率。

- 如果最高公共速率为 5.0 GT/s，则根据接收到的 TS1 中的 Selectable De‐emphasis 位设置发送器的去加重（1b = ‐3.5 dB，0b = ‐6 dB）。

- 如果最高公共速率为 8.0 GT/s 并且：

   - a) EQ TS1 指导从设备进入此状态，则使用它们指定的 Tx 预设设置。

   - b) 常规 TS1 指导从设备进入此状态，则允许从设备使用其默认发送器设置。

## _退出到"Loopback.Active"_

如果在指导从设备进入此状态的传入 TS1 中设置了 Compliance Receive 位，则下一个状态将是 Loopback.Active。从设备无需等待特定边界即可发送回送数据，并允许截断任何进行中的有序集。

否则，从设备发送链路和 Lane 编号设置为 PAD 的 TS1，并且如果满足以下条件，则下一个状态将是 Loopback.Active：

- 速率为 2.5 或 5.0 GT/s，并且在所有 Lane 上获得了 Symbol 锁定。

- 速率为 8.0 GT/s，并且在所有活动 Lane 上看到两个连续的 TS1。通过评估和应用 TS1 中给定的值来处理均衡，只要它们受支持并且 EC 值对于端口的方向是适当的（下行端口为 10b，

**616**

**第 14 章：链路初始化与训练**

上行端口为 11b）。可选地，端口可以接受这两个 EC 值中的任何一个以应对此情况。如果应用了设置，则必须在接收后 500ns 内生效，并且不得导致发送器在任何电气规范上违规超过 1ns。与 Recovery.Equalization 中的过程相比，一个重要的区别是从设备正在发送的 TS1 中不会回显新设置。— 对于 8b/10b，从设备必须仅在 Symbol 边界上转换为回送数据，但允许截断任何进行中的有序集。对于 128b/130b，没有指定何时可以发送回送数据的边界，但仍允许截断任何进行中的有序集。

## **Loopback.Active**

在此子状态期间，回环主设备发送有效的编码数据，并且在其准备退出回环之前不应发送 EIOS。回环从设备不加修改地回显接收到的信息（即使编码被确定为无效），但根据 Polling 状态确定的极性反转可能除外。从设备还继续执行时钟容差补偿。这意味着必须根据需要添加或删除 SKP，但不要求所有 Lane 都发送相同数量。

## _退出到"Loopback.Exit"_

对于回环主设备，如果被指导，则下一个状态将是 Loopback.Exit。

对于回环从设备，如果以下两个条件中的任何一个为真，则下一个状态将是 Loopback.Exit：

- 从设备被指示退出，或者在任何 Lane 上看到四个连续的 EIOS。

- 可选地，如果当前速率为 2.5 GT/s，并且接收到 EIOS 或在任何 Lane 上检测到或推断出电气空闲。如果任何已配置的 Lane 在 128 μs 内未检测到电气空闲退出，则可以推断为电气空闲。
