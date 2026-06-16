**13. 由于 Lane 0 和 1 上的发送和接收链路和 Lane 号匹配，下游端口通过在这些 Lane 上发送具有相同链路和 Lane 号的 TS2 有序集来表示它已准备好结束此协商并继续到下一个状态 L0。其他 Lane 继续发送 Link 和 Lane 号都为 PAD 的 TS1。**

**14. 在 Lane 0 和 1 上接收到具有相同链路和 Lane 号的 TS2 后，上游端口也通过在这些 Lane 上发送回 TS2 来表示其准备好离开 Configuration 状态并继续到 L0。其他 Lane 继续发送 Link 和 Lane 号都为 PAD 的 TS1。这在第 552 页的图 14‐23 中示出。**

**551**

**PCI Express Technology**

_图 14‐23：示例 3 — 步骤 5 和 6_

**==> picture [356 x 229] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>LTSSM<br>（下游端口）<br>0 1 2 3<br>步骤 5<br>TS1<br>Lane # 0 1 PAD PAD<br>Link # N N PAD PAD<br>TS2 N N PAD PAD Link #<br>0 1 PAD PAD Lane #<br>0 1 2 3 步骤 6<br>（上游端口）<br>LTSSM<br>选项：一个链路 x4、x2 或 x1<br>**----- End of picture text -----**<br>


一旦端口接收到至少 8 个 TS2 并发送至少 16 个，它将发送一些逻辑空闲数据，然后这些 Lane 转换到 L0。其他 Lane（在此示例中为 Lane 2 和 3）转换到电气空闲，直到下一次启动链路训练过程，此时这些 Lane 将像正常一样尝试训练过程。

## **Configuration 子状态详解**

此处提供了每个子状态的详细解释，以涵盖 Configuration 的所有子状态，如第 553 页的图 14‐24 所示。鉴于前面讨论的链路训练示例，Configuration 子状态应该更容易理解。

**552**

**第 14 章：链路初始化与训练**

_图 14‐24：Configuration 状态机_

**==> picture [380 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
从 Polling 或 Recovery 进入 退出到<br>指示 Loopback<br>Config.Linkwidth.Start<br>指示 退出到<br>Config.Linkwidth.Accept Disable<br>退出到<br>Detect Config.Lanenum.Wait<br>Config.Lanenum.Accept<br>Config.Complete<br>2ms 超时 和<br>2ms 超时，未达到最大<br>和最大恢复尝试 在 Recovery 的尝试。退出到<br>已达到。 Config.Idle<br>Recovery<br>8 个空闲 Rx，Tx 16 个空闲<br>退出到 全开电源状态<br>L0 分组传输/<br>接收开始<br>**----- End of picture text -----**<br>


## **Configuration.Linkwidth.Start**

此子状态在 Polling 状态的正常完成之后（如第 527 页 "Polling.Configuration" 中所述）进入，或者如果 Recovery 状态发现自上次分配以来链路或 Lane 号已更改，因此恢复过程无法正常完成（如第 571 页 "Recovery State" 中所述）。

## **下游 Lane。**

## _在 Configuration.Linkwidth.Start 期间_

下游端口现在成为此链路上的领导者，并在所有活动 Lane 上发送具有非 PAD 链路号的 TS1（只要 LinkUp 未设置且链路宽度的向上配置未正在进行）。在 TS1 中，链路号字段从 PAD 更改为数字，而 Lane 号保持 PAD。规范中对链路号值的唯一约束是，如果支持多个链路，则它们对于每个可能的链路必须是唯一的。例如，x8 链路将在所有 8 个 Lane 上具有相同的链路号，但如果它也可以配置为两个 x4 链路，则两组 4 个 Lane 将被分配不同的链路号，例如一组为 5，另一组为 6。这些值对链路伙伴是本地的，不需要软件跟踪它们或尝试使它们在整个系统中唯一。如果 upconfigure_capable 位设置为 1b，则这些 TS1 也将在接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1 的任何非活动 Lane 上发送。

- 从 Polling 进入此子状态时，任何检测到接收器的 Lane 被视为活动。

- 从 Recovery 进入时，通过 Configuration.Complete 后成为链路一部分的任何 Lane 被视为活动 Lane。

- 必须在 TS1 中通告所有支持的数据速率，即使端口不打算使用它们。

**交叉链路。** 对于 LinkUp = 0b 且支持可选交叉链路功能的情况，所有检测到接收器的 Lane 必须发送最少 16 到 32 个具有非 PAD 链路号和 PAD Lane 号的 TS1。之后，端口将评估其接收的内容以查看是否存在交叉链路。

**向上配置链路宽度。** 如果 LinkUp = 1b 且 LTSSM 想要向上配置链路，则在当前活动 Lane、它打算激活的非活动 Lane 以及已看到传入 TS1 的 Lane 上发送 Link 和 Lane 号设置为 PAD 的 TS1。当 Lane 接收到返回的两个连续的 TS1 时，或在 1ms 后，链路号在正在发送的 TS1 中分配一个值。

- 如果激活非活动 Lane，则发送器必须等待 Tx 共模电压稳定后再退出电气空闲并发送 TS1。

- 对于将分组到链路中的 Lane，链路号必须相同。只有对于能够充当唯一链路的 Lane 组，数字才不同。

- _退出到 "如果其他条件都不成立，则 24ms 超时后。"_ 任何之前接收到至少一个具有 PAD 的 Link 和 Lane 号的 TS1 的 Lane 现在接收到两个具有匹配发送链路号的非 PAD 链路号且 Lane 号仍为 PAD 的连续 TS1 将退出到 Configuration.Linkwidth.Accept 子状态。

**554**

**第 14 章：链路初始化与训练**

## _退出到 "Configuration.Linkwidth.Start"_

- 如果此子状态接收的第一组 TS1 具有非 PAD 链路号，则可以理解存在交叉链路，并且链路邻居也表现为下游端口。为了处理这种情况，下游 Lane 更改为上游 Lane 并选择随机的交叉链路超时。下一个子状态将是相同的 Configuration.Linkwidth.Start，但 Lane 现在表现为上游 Lane。

这支持两个链路伙伴都表现为下游端口时的可选行为。这种情况的解决方案是将两者都更改为上游端口并为每个分配一个随机超时，当它到期时将其更改为下游端口。由于超时不会相同，最终一个端口被视为下游，而另一个被视为上游，然后训练可以继续进行。超时必须是随机的，以便即使连接了两个相同的设备，任何可能的死锁最终也会被打破。

如果支持交叉链路，则接收到的 TS1 序列首先具有 PAD 的链路号，后来具有匹配发送链路号的非 PAD 链路号，仅在该序列未被 TS2 中断时才有效。

## _退出到 "Disable 状态"_

如果端口被更高层指示在所有检测到的 Lane 上发送 Disable Link 位被断言的 TS1 或 TS2。通常，下游端口将启动此操作，但对于可选的交叉链路情况，它可以改为变为上游端口，然后如果在两个连续的 TS1 中设置了 Loopback 位，则 Disable 将是下一个状态。

## _退出到 "Loopback 状态"_

如果支持环回的发送器被更高层指示发送 Loopback 位被断言的 TS 有序集，或者如果正在发送 TS1 的 Lane 接收到 2 个连续的设置了 Loopback 位的 TS1。发送设置了该位的 TS1 的端口将成为环回主设备，而接收它们的端口将成为环回从设备。

**555**

**PCI Express Technology**

## _退出到 "Detect 状态"_

如果其他条件都不成立，则在 24ms 超时后。

## **上游 Lane。**

## _在 Configuration.Linkwidth.Start 期间_

上游端口现在成为此链路上的追随者，并返回发送 Link 和 Lane 号字段设置为 PAD 的 TS1 有序集。它将继续这样做，直到它开始从下游端口（领导者）接收具有非 PAD 链路号的 TS1。

上游端口在以下 Lane 上发送 Link 和 Lane 值设置为 PAD 的 TS1：a) 所有活动 Lane，b) 它想要向上配置的 Lane，以及 c) 如果 upconfigure_capable 设置为 1b，则在该子状态中已接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1 的每个非活动 Lane 上。

- 从 Polling 进入此子状态时，任何检测到接收器的 Lane 被视为活动。

- 从 Recovery 进入时，通过 Configuration.Complete 后成为链路一部分的任何 Lane 被视为活动 Lane。如果转换不是由 LTSSM 超时引起的，则如果发送器确实计划因自动原因更改链路宽度，则发送器必须将 TS1 符号 4 位 6 的 Autonomous Change 位设置为 1b。

- 必须在 TS1 中通告所有支持的数据速率，即使端口不打算使用它们。

**交叉链路。** 对于 LinkUp = 0b 且支持可选交叉链路功能的情况，所有检测到接收器的 Lane 必须发送最少 16 到 32 个 Link 和 Lane 值设置为 PAD 的 TS1。之后，端口将评估其接收的内容以查看是否存在交叉链路。

_退出到 "如果其他条件都不成立，则 24ms 超时后。"_

- 如果_任何_ Lane 接收到两个具有非 PAD 链路号和 PAD Lane 号的连续 TS1，则此端口转换到 Configuration.Linkwidth.Accept 子状态，其中为这些 Lane 选择一个接收到的链路号，并在_所有_接收到具有非 PAD 链路号的 TS1 的 Lane 上使用该链路号和 PAD Lane 号发送 TS1。任何剩余的检测到接收器但没有链路号的 Lane 必须发送 Link 和 Lane 号设置为 PAD 的 TS1。

- 如果正在向上配置链路，LTSSM 等待直到它在以下情况下接收到两个具有非 PAD 链路号和 PAD Lane 号的连续 TS1：a) 它想要激活的所有非活动 Lane，或 b) 在进入此子状态后 1ms 内的任何

**556**

**第 14 章：链路初始化与训练**

Lane，以较早者为准。之后，它使用所选链路号以及 PAD Lane 号发送 TS1。

- 为了避免配置比必要的更小的链路，建议在某些 Lane 上看到错误或丢失块对齐的多 Lane 链路延迟此接收器评估。对于 8b/10b 编码，它应至少再等待两个 TS1，而对于 128b/130b 编码，它应至少等待 34 个 TS1，但任何情况下都不能超过 1ms。

- 激活非活动 Lane 后，发送器必须等待 Tx 共模电压稳定后再退出电气空闲并发送 TS1。

## _退出到 "Configuration.Linkwidth.Start"_

- 交叉链路超时后，发送 16 到 32 个 Link 和 Lane 值设置为 PAD 的 TS2。上游 Lane 更改为下游 Lane，下一个子状态将是相同的 Configuration.Linkwidth.Start，但这次 Lane 表现为下游 Lane。对于连接在一起的两个上游端口的情况，此可选行为允许其中一个最终作为下游端口担任领导角色。

## _退出到 "Disable 状态"_

如果满足以下任一条件：

- 任何正在发送 TS1 的 Lane 也接收到 Disable Link 位被断言的 TS1。

- 支持可选交叉链路，并且所有正在发送和接收 TS1 的 Lane 在两个连续的 TS1 中接收 Disable Link 位，或者交叉链路端口被更高层指示在所有检测到接收器的 Lane 上的 TS1 和 TS2 中断言 Disable 位。

## _退出到 "Loopback 状态"_