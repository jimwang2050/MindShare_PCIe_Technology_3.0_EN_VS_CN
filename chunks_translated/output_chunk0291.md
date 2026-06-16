LTSSM<br>（下游端口）<br>0 1 2 3<br>步骤 3<br>Lane # 0 1 PAD PAD<br>TS1<br>Link # N N PAD PAD<br>N N PAD PAD Link #<br>TS1<br>0 1 PAD PAD Lane #<br>0 1 2 3 步骤 4<br>（上游端口）<br>LTSSM<br>选项：一个链路 x4、x2 或 x1<br>**----- End of picture text -----**<br>


## **确认链路和 Lane 号。**

13. 由于 Lane 0 和 1 上的发送和接收链路和 Lane 号匹配，下游端口通过在这些 Lane 上发送具有相同链路和 Lane 号的 TS2 有序集来表示它已准备好结束此协商并继续到下一个状态 L0。其他 Lane 继续发送 Link 和 Lane 号都为 PAD 的 TS1。

14. 在 Lane 0 和 1 上接收到具有相同链路和 Lane 号的 TS2 后，上游端口也通过在这些 Lane 上发送回 TS2 来表示其准备好离开 Configuration 状态并继续到 L0。其他 Lane 继续发送 Link 和 Lane 号都为 PAD 的 TS1。这在第 552 页的图 14‐23 中示出。

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

- 如果支持环回的发送器被更高层指示发送 Loopback 位被断言的 TS 有序集，或者所有正在发送和接收 TS1 的 Lane 接收到 2 个连续的设置了 Loopback 位的 TS1。发送设置了该位的 TS1 的端口将成为环回主设备，而接收它们的端口将成为环回从设备。

**557**

## **PCI Express Technology**

## _退出到 "Detect 状态"_

- 如果其他条件都不成立，则在 24ms 超时后。

## **Configuration.Linkwidth.Accept**

此时，上游端口现在在其所有 Lane 上发送回具有相同链路号的 TS1 有序集。链路号源自下游端口，上游端口只是将该值反映回其所有 Lane。现在下游端口知道链路宽度（接收相同链路号的 Lane 数）并且必须开始通告 Lane 号。因此领导者（下游端口）继续发送 TS1，但现在使用指定的实际 Lane 号而不是 PAD。此外，所有这些 TS1 将具有相同的链路号。下游和上游 Lane 的详细行为概述如下：

## **下游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 下游端口现在将启动 Lane 号。如果可以从至少一组 Lane 形成链路，并且所有 Lane 都接收两个连续的 TS1 并且都看到相同的链路号，则发送保持相同链路号的 TS1 但现在也分配唯一的非 PAD Lane 号。

## _退出到 "Configuration.Lanenum.Wait"_

- 下游端口不会在 Configuration.Linkwidth.Accept 子状态中停留很长时间。一旦它从上游端口接收到指示链路宽度的必要 TS1，它就会更新所需的任何内部状态信息，开始发送如上所述的具有非 PAD Lane 号的 TS1，并立即转换到 Configuration.Lanenum.Wait 以等待来自上游端口的 Lane 号确认。

## **上游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 上游端口发送 TS1，其中在_所有_接收到具有非 PAD 链路号的 TS1 的 Lane 上的 TS1 中选择并发送一个接收到的链路号。任何剩余的检测到接收器但没有链路号的 Lane 必须发送 Link 和 Lane 号设置为 PAD 的 TS1。

## _退出到 "Configuration.Lanenum.Wait"_

- 上游端口必须响应链路邻居向其提议的 Lane 号。如果可以使用在其 TS1 上发送非 PAD 链路号并接收到两个具有相同链路号和任何非 PAD Lane 号的连续 TS1 的 Lane 形成链路，那么它应发送与相同 Lane 号分配匹配的 TS1（如果可能），或者如果需要则不同（例如使用可选的 Lane 反转）。

**558**

**第 14 章：链路初始化与训练**

## **Configuration.Lanenum.Wait**

在讨论 Configuration.Lanenum.Wait 状态之前，一些背景信息可能会有所帮助。Lane 号从零开始按顺序分配到链路可能的最大数量。例如，x8 链路将被分配 Lane 号 0 ‐ 7。端口需要支持与其具有的 Lane 数一样宽的链路和一个小至一个 Lane 的链路。Lane 将始终从 Lane 0 开始，并且必须既是顺序的又是连续的。例如，如果 x8 端口上的某些 Lane 无法工作，则可以选择将其设计为配置 x4 链路，如果是这样，它将需要使用 Lane 0‐3。作为另一个示例，如果 x8 端口的 Lane 2 无法工作，则不可能使用 Lane 0、1、3 和 4 形成 x4 链路，因为 Lane 不是连续的。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

规范中针对 Configuration 子状态重复了许多次的常见时序注意事项。这里不是在每种情况下重复它，只需注意它通常适用于上游和下游端口：

为了避免配置比必要的更小的链路，建议在某些 Lane 上看到错误或丢失块对齐的多 Lane 端口延迟最终链路宽度评估。对于 8b/10b，它应至少再等待两个 TS1，而对于 128b/130b 模式，它应至少等待 34 个 TS1，但任何情况下都不能超过 1ms。其想法是 Lane 在上电或复位后可能需要稳定时间。

## _退出到 "Detect 状态"_

在 2ms 超时后，如果无法配置链路（例如：Lane 0 不工作且 Lane 反转不可用），或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号中都带有 PAD 的 TS1，则链路必须退出到 Detect 状态。

## **下游 Lane**

## _在 Configuration.Lanenum.Wait 期间_

下游端口将继续传输具有非 PAD 链路和 Lane 号的 TS1，直到满足退出条件之一。

## _退出到 "Configuration.Lanenum.Accept"_

如果满足下列任一情况：

- 如果在所有 Lane 上接收到两个连续的 TS1，其链路和 Lane 号与在这些 Lane 上发送的内容匹配。

**559**

## **PCI Express Technology**

- 如果任何检测到接收器的 Lane 接收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD 链路号。规范指出，这允许两个端口就相互可接受的链路宽度达成一致。

## _退出到 "Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

上游 Lane

## _在 Configuration.Lanenum.Wait 期间_

上游端口将继续传输具有非 PAD 链路和 Lane 号的 TS1，直到满足退出条件之一。

## _退出到 "Configuration.Lanenum.Accept"_

如果满足下列任一情况：

- 如果任何 Lane 接收到两个连续的 TS2。

- 如果任何 Lane 接收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD 链路号。

请注意，允许上游 Lane 在更改为该子状态之前等待最多 1ms，以防止接收错误或 Lane 之间的偏移影响最终链路配置。

## _退出到 "Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 接收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

## **Configuration.Lanenum.Accept**

下游 Lane

## _在 Configuration.Lanenum.Accept 期间_

下游端口现在已接收到具有非 PAD 链路和 Lane 号的 TS1。在这一点上，下游端口必须决定是否可以使用上游端口返回的 Lane 号建立链路。三个可能的状态转换在下面列出。

## _退出到 "Configuration.Complete"_

如果接收到两个连续的 TS1 具有相同的非 PAD 链路和 Lane 号，并且它们与所有 Lane 的 TS1 中传输的链路和 Lane 号匹配，则上游端口已同意下游端口通告的链路和

**560**

**第 14 章：链路初始化与训练**

Lane 号，下一个子状态是 Configuration.Complete。或者如果接收到的 TS1 中的 Lane 号与下游端口通告的相反，如果下游端口支持 Lane 反转，它仍然可以使用反转的 Lane 号继续到 Configuration.Complete。

规范指出，反转 Lane 条件严格定义为 Lane 0 接收具有最高 Lane 号（Lane 总数 ‐ 1）的 TS1，并且最高 Lane 号接收 Lane 号为零的 TS1。可以从中理解的是，课堂上偶尔出现的问题的答案：Lane 号是否可以混合而不是顺序的？答案是不可以的，它们必须是从 0 到 n‐1 或从 n‐1 到 0；不支持其他选项。

如果 Configuration 状态是从 Recovery 状态进入的，则可能已请求带宽更改。如果是这样，状态位将更新以报告发生的情况的性质。基本上，系统需要报告此更改是由于链路工作不可靠而启动，还是因为硬件只是在管理链路功率。位更新如下：

- 如果带宽更改是由下游端口因可靠性问题而启动的，则链路带宽管理状态位设置为 1b。

- 如果带宽更改不是由下游端口启动，但两个连续接收的 TS1 中的 Autonomous Change 位清零为 0b，则链路带宽管理状态位设置为 1b。

- 否则，链路自动带宽状态位设置为 1b。

## _退出到 "Configuration.Lanenum.Wait"_

- 如果可以使用部分（但不是全部）接收两个连续的具有相同非 PAD 链路和 Lane 号的 TS1 的 Lane 形成配置的链路，则这些 Lane 使用相同的链路号和新的 Lane 号发送 TS1。目标是使用较小的 Lane 组来实现工作的链路。

新的 Lane 号必须从零开始并按顺序递增以覆盖将使用的 Lane。任何不接收 TS1 的 Lane 不能成为组的一部分，并将破坏 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。例如，如果 8 个 Lane 可用，但 Lane 2 看不到传入的 TS1，则链路不能由需要 Lane 2 的组组成。因此，x8 和 x4 选项将不可用，只有 x1 或 x2 链路是可能的。

**561**

## **PCI Express Technology**

## _退出到 "Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 接收到两个连续的具有 PAD 的链路和 Lane 号的 TS1。

## **上游 Lane**

## _在 Configuration.Lanenum.Accept 期间_

- 上游端口现在已接收到具有非 PAD 链路和 Lane 号的 TS2 或 TS1。在这一点上，上游端口必须决定是否可以使用下游端口发送的 Lane 号建立链路。三个可能的状态转换在下面列出。

## _退出到 "Configuration.Complete"_

- 如果接收到两个连续的 TS2 具有相同的非 PAD 链路和 Lane 号，并且它们与这些 Lane 的 TS1 中传输的链路和 Lane 号匹配，则一切正常，下一个子状态将是 Configuration.Complete。

## _退出到 "Configuration.Lanenum.Wait"_

- 如果可以使用接收两个连续的具有相同非 PAD 链路和 Lane 号的 TS1 的 Lane 的子集形成配置的链路，则这些 Lane 使用相同的链路号和新的 Lane 号发送 TS1。目标是使用较小的 Lane 组来实现工作的链路。在这种情况下，下一个子状态将是 Configuration.Lanenum.Wait。

与下游 Lane 的情况一样，新的 Lane 号必须从零开始并按顺序递增以覆盖将使用的 Lane。任何不接收 TS1 的 Lane 不能成为组的一部分，并将破坏 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

## _退出到 "Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 接收到两个连续的具有 PAD 的链路和 Lane 号的 TS1，则下一个状态将是 Detect。

## **Configuration.Complete**

这是 Configuration 状态中交换 TS2 的唯一子状态。如前所述，TS2 的目的是一种握手或确认，即链路上的两个设备已准备好继续到下一个状态。因此这是 TS1 中交换的链路和 Lane 号的最终确认

**562**

**第 14 章：链路初始化与训练**

应注意的是，允许设备在进入此子状态时更改其支持的数据速率和向上配置能力，但不能在其中更改。这是因为设备从这些 TS2 中通告的内容记录其链路伙伴的能力，如本节所述。

## **下游 Lane**

## _在 Configuration.Complete 期间_

使用与接收到的 TS1 匹配的链路和 Lane 号发送 TS2。如果端口支持使用 Lane 0 的 x1 链路并能够向上配置链路，则 TS2 可以设置 Upconfigure Capability 位。

对于 8b/10b 编码，离开此子状态时必须完成 Lane 去偏移。此外，如果所有配置的 Lane 看到两个连续的设置了 Disable Scrambling 位的 TS2，则将禁用加扰。发送这些的端口还必须禁用加扰。请注意，由于加扰对信号完整性有必要贡献，因此在 128b/130b 模式下不能禁用加扰。

下游端口正在发送 TS2 并监视返回的 TS2。供将来参考，记录从传入 TS2 的 N_FTS 字段中退出 L0s 状态时必须发送的 FTS 数。

## _退出到 "Configuration.Idle"_

当所有发送 TS2 的 Lane 接收 8 个 TS2，具有匹配的链路和 Lane 号（非 PAD）、匹配的速率标识符以及所有链路中匹配的 Link Upconfigure Capability 位时，下一个状态将是 Configuration.Idle。在接收到一个 TS2 之后，还必须发送至少 16 个 TS2。

如果设备支持大于 2.5 GT/s 的速率，则它必须记录在任何已配置 Lane 上接收到的速率标识符，并且这将覆盖任何先前记录的值。用于跟踪 Recovery 中速度更改的变量 "changed_speed_recovery" 被清零。

变量 "upconfigure_capable" 在以下情况下设置为 1b：如果设备发送 Link Upconfigure Capability 设置为 1b 的 TS2 并接收 8 个连续的设置了相同位的 TS2。否则，它被清零。

未配置为链路一部分的任何 Lane 不再与正在进行的 LTSSM 关联，并且必须是以下之一：

- 与新的 LTSSM 关联，或

- 转换到电气空闲

   - a) 如果那些 Lane 之前已通过 L0 配置为链路的一部分，并且 LinkUp 仍设置为 1b，则出现特殊情况

**563**

**PCI Express Technology**

从那以后。如果链路具有向上配置能力，它们必须保持与同一 LTSSM 关联。对于这种情况，还建议那些 Lane 保持其接收器终端开启，因为如果链路被向上配置，它们将再次成为链路的一部分。如果终端未保持开启，则它们必须在 LTSSM 进入 Recovery.RcvrCfg 状态时一直通过 Configuration.Complete 打开。但是，通过此过程，之前不是链路一部分的 Lane 不能成为其一部分。

- b) 对于可选交叉链路，接收器终端必须介于 ZRX‐HIGH‐IMP‐DC‐POS 和 ZRX‐HIGH‐IMP‐DC‐NEG 之间。

- c) 如果 LTSSM 返回 Detect，这些 Lane 将再次与其关联。

- d) 在 Lane 进入电气空闲之前不需要 EIOS，并且转换不必在符号或有序集边界上发生。

## 在 2ms 超时后：

_退出到 "Configuration.Idle"_

如果 idle_to_rlock_transitioned 变量小于 FFh **且**当前数据速率为 8.0 GT/s，则下一个状态是 Configuration.Idle。

在此转换中，变量 "changed_speed_recovery" 被清零。此外，如果至少一个 Lane 看到八个具有匹配链路和 Lane 号（非 PAD）的连续 TS2，则变量 "upconfigure_capable" 可以更新，尽管不需要这样做。如果发送和接收的 Link Upconfigure Capability 位为 1b，则将其设置为 1b，否则清零。

未配置链路一部分的 Lane 不与正在进行的 LTSSM 关联，并具有与上面列出的非超时情况相同的要求。

_退出到 "Detect 状态"_

否则，下一个状态是 Detect。

## **上游 Lane**

_在 Configuration.Complete 期间_

使用与接收到的 TS2 匹配的链路和 Lane 号发送 TS2。如果端口支持使用 Lane 0 的 x1 链路并能够向上配置链路，则 TS2 可以设置 Upconfigure Capability 位。

**564**

**第 14 章：链路初始化与训练**

对于 8b/10b 编码，离开此子状态时必须完成 Lane 去偏移。此外，如果所有配置的 Lane 看到两个连续的设置了 Disable Scrambling 位的 TS2，则将禁用加扰。发送这些的端口还必须禁用加扰。请注意，由于加扰对信号完整性有必要贡献，因此在 128b/130b 模式下不能禁用加扰。

在此子状态中，上游端口正在从下游端口接收 TS2，供将来参考，应记录从传入 TS2 中的 N_FTS 字段值退出 L0s 状态时必须发送的 FTS 数。

## _退出到 "Configuration.Idle"_

当所有发送 TS2 的 Lane 接收 8 个 TS2，具有匹配的链路和 Lane 号（非 PAD）、匹配的速率标识符以及所有链路中匹配的 Link Upconfigure Capability 位时，下一个状态将是 Configuration.Idle。在接收到一个 TS2 之后，还必须发送至少 16 个 TS2。

如果设备支持大于 2.5 GT/s 的速率，则它必须记录在任何已配置 Lane 上接收到的速率标识符，并且这将覆盖任何先前记录的值。用于跟踪 Recovery 中速度更改的变量 "changed_speed_recovery" 被清零。

变量 "upconfigure_capable" 在以下情况下设置为 1b：如果设备发送 Link Upconfigure Capability 设置为 1b 的 TS2 并接收 8 个连续的设置了相同位的 TS2。否则，它被清零。

未配置为链路一部分的任何 Lane 不再与正在进行的 LTSSM 关联，并且必须是以下之一：

- 可选择与新的交叉链路 LTSSM 关联（如果支持此功能），或

- 转换到电气空闲

   - a) 如果那些 Lane 之前已通过 L0 配置为链路的一部分，并且 LinkUp 自那时起仍设置为 1b，则出现特殊情况。如果链路具有向上配置能力，它们必须保持与同一 LTSSM 关联。对于这种情况，还建议那些 Lane 保持其接收器终端开启，因为如果链路被向上配置，它们将再次成为链路的一部分。如果它们未保持开启，则它们必须在 LTSSM 进入 Recovery.RcvrCfg 状态时一直通过 Configuration.Complete 打开。但是，通过此过程，之前不是链路一部分的 Lane 不能成为其一部分。

**565**

## **PCI Express Technology**

- b) 接收器终端必须介于 ZRX‐HIGH‐IMP‐DC‐POS 和 ZRX‐

   - HIGH‐IMP‐DC‐NEG 之间。

- c) 如果 LTSSM 返回 Detect，这些 Lane 将再次与其关联。

- d) 在 Lane 进入电气空闲之前不需要 EIOS，并且转换不必在符号或有序集边界上发生。

## 在 2ms 超时后：

## _退出到 "Configuration.Idle"_

如果 idle_to_rlock_transitioned 变量小于 FFh **且**当前数据速率为 8.0 GT/s，则下一个状态是 Configuration.Idle。

在此转换中，变量 "changed_speed_recovery" 被清零。此外，如果至少一个 Lane 看到八个具有匹配链路和 Lane 号（非 PAD）的连续 TS2，则变量 "upconfigure_capable" 可以更新，尽管不需要这样做。如果发送和接收的 Link Upconfigure Capability 位为 1b，则将其设置为 1b，否则清零。

未配置链路一部分的 Lane 不与正在进行的 LTSSM 关联，并具有与上面列出的非超时情况相同的要求。

## _退出到 "Detect 状态"_

否则，下一个状态是 Detect。

## **Configuration.Idle**

## _在 Configuration.Idle 期间_

在此子状态中，发送器正在发送空闲数据并等待接收空闲数据的最小数量，以便此链路可以转换到 L0。在此期间，物理层向上层报告链路处于运行状态（Linkup = 1b）。

对于 8b/10b 编码，发送器在所有已配置 Lane 上发送空闲数据。空闲数据只是被加扰和编码的数据零。

对于 128b/130b 编码，发送器在所有已配置 Lane 上发送一个 SDS 有序集，后跟空闲数据符号。Lane 0 上的第一个空闲符号是数据流的第一个符号。

**566**

**第 14 章：链路初始化与训练**

## _退出到 "L0 状态"_

如果使用 8b/10b 编码，则下一个状态是 L0，如果在所有已配置 Lane 上接收到 8 个连续的空闲数据符号时间，并且在接收到一个空闲符号之后发送了 16 个符号时间的空闲数据。

如果使用 128b/130b，则下一个状态是 L0，如果在所有已配置 Lane 上接收到 8 个连续的空闲数据，在接收到一个空闲符号之后发送了 16 个空闲，并且此状态不是通过 Configuration.Complete 的超时进入的。

- 数据流处理开始之前必须完成 Lane 到 Lane 去偏移。

- 必须在数据块中接收空闲符号。

- 如果软件自上次从 Recovery 或 Configuration 转换到 L0 以来在 Link Control 寄存器中设置了 Retrain Link 位，则下游端口必须将 Link Status 寄存器中的 Link Bandwidth Management 位设置为 1b，以指示此更改不是硬件发起的（自动）。

- 转换到 L0 时，变量 "idle_to_rlock_transitioned" 清零为 00h。

## 在 2ms 超时后：

## _退出到 "Recovery 子状态详解"_

如果 idle_to_rlock_transitioned 变量小于 FFh，则下一个状态是 Recovery (Recovery.RcvrLock)。然后：

- a) 对于 8.0 GT/s，idle_to_rlock_transitioned 递增 1。

- b) 对于 2.5 或 5.0 GT/s，将 idle_to_rlock_transitioned 设置为 FFh。

- c) 注意：此变量计算 LTSSM 因序列未工作而从此状态转换到 Recovery 状态的次数。问题可能是均衡尚未正确调整或所选速度根本不起作用，Recovery 状态将采取措施解决这些问题。此变量限制这些尝试的次数以避免无限循环。如果在进行此操作 256 次（当计数达到 FFh 时）后链路仍不工作，则返回 Detect 并重新开始，希望获得更好的结果。

_退出到 "Detect 状态"_

否则（即 idle_to_rlock = FFh），下一个状态是 Detect。

**567**

**PCI Express Technology**

## **L0 状态**

这是正常的、完全运行的链路状态，在此期间逻辑空闲、TLP 和 DLLP 在链路邻居之间交换。L0 在链路训练过程结束后立即实现。物理层还通过设置 LinkUp 变量来通知上层链路已准备好运行。此外，变量 idle_to_rlock_transitioned 清零为 00h。

## _退出到 "Recovery 状态"_

如果指示链路速度或链路宽度的变化，或者如果链路伙伴通过转到 Recovery 或电气空闲来启动此操作，则下一个状态将是 Recovery。让我们在下面的讨论中更详细地考虑这三种情况中的每一种。

## **速度更改**

规范中描述了将导致自动速度更改的两种条件。

第一种是当两个伙伴都支持高于 2.5 GT/s 的速率并且链路处于活动状态（数据链路层报告 DL_Active），或者当一个伙伴在其 TS 有序集中请求速度更改时。例如，如果注意到更高速率并且软件写入 Retrain Link 位并在将 Target Link Speed 字段（参见第 569 页的图 14‐26）设置为与当前速率不同的速率之后，下游端口将启动速度更改。