- 如果支持回环的发送器被更高层指示发送 Loopback 位置位的 TS 有序集，或者所有正在发送和接收 TS1 的 Lane 收到 2 个连续的 Loopback 位置位的 TS1。无论哪个端口发送带此位设置的 TS1 都将成为 Loopback 主机，而接收它们的端口将成为 Loopback 从机。

## _退出至"Detect 状态"_

- 在 24ms 超时后，如果其他条件都不成立。

**557**

**PCI Express 技术**

## **Configuration.Linkwidth.Accept**

此时，上游端口 (Upstream Port) 正在通过其所有 Lane 发送回具有相同 Link 号的 TS1 有序集。Link 号源自下游端口 (Downstream Port)，上游端口只是在所有 Lane 上将该值反射回去。现在下游端口知道链路宽度（接收相同 Link 号的 Lane 数），并且它必须开始通告 Lane 号。因此，主导方（下游端口）继续发送 TS1，但现在使用指定的实际 Lane 号代替 PAD。此外，所有这些 TS1 将具有相同的 Link 号。下游和上游 Lane 的详细行为概述如下：

## **下游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 下游端口 (Downstream Port) 现在将发起 Lane 号。如果可以由至少一组 Lane 形成链路，并且所有这些 Lane 都接收到两个连续的 TS1 并且都看到相同的 Link 号，则发送保持相同 Link 号但现在也分配唯一非 PAD 的 Lane 号的 TS1。

## _退出至"Configuration.Lanenum.Wait"_

- 下游端口 (Downstream Port) 不会在 Configuration.Linkwidth.Accept 子状态中停留很长时间。一旦它从上游端口接收到指示链路宽度的必要 TS1，它就会更新所需的任何内部状态信息，开始发送具有非 PAD Lane 号的 TS1，如上所述，并立即转换到 Configuration.Lanenum.Wait 以等待来自上游端口的 Lane 号确认。

## **上游 Lane**

## _在 Configuration.Linkwidth.Accept 期间_

- 上游端口 (Upstream Port) 发送 TS1，其中选择接收到的 Link 号之一并在**所有**接收到具有非 PAD Link 号的 TS1 的 Lane 上的 TS1 中发送回去。任何已检测到接收器但未检测到 Link 号的剩余 Lane 必须发送 Link 和 Lane 号设置为 PAD 的 TS1。

## _退出至"Configuration.Lanenum.Wait"_

- 上游端口 (Upstream Port) 必须响应链路邻居向其提议的 Lane 号。如果可以使用在其 TS1 上发送非 PAD Link 号并且接收到两个具有相同 Link 号和任何非 PAD Lane 号的连续 TS1 的 Lane 形成链路，那么它应发送匹配相同 Lane 号分配的 TS1（如果可能），或者在必要时发送不同的（例如使用可选的 Lane 反转）。

**558**

**第 14 章：链路初始化与训练**

## **Configuration.Lanenum.Wait**

在讨论 Configuration.Lanenum.Wait 状态之前，一些背景信息可能会有所帮助。Lane 号从零开始顺序分配到链路可能的最大数量。例如，x8 链路将被分配 Lane 号 0 至 7。端口需要支持与其所具有的 Lane 数一样宽的链路，且至少为一个 Lane。Lane 将始终从 Lane 0 开始，并且必须既顺序又连续。例如，如果 x8 端口上的一些 Lane 无法工作，可以选择将其设计为配置 x4 链路，如果是这种情况，则它需要使用 Lane 0-3。作为另一个示例，如果 x8 端口的 Lane 2 出现故障，则无法使用 Lane 0、1、3 和 4 来形成 x4 链路，因为 Lane 不是连续的。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

一个常见的时序考虑因素在 Configuration 子状态的规范中重复多次。这里不是为每种情况都重复它，只需注意它通常适用于上游和下游端口：

为避免将链路配置得比必要的更小，建议多 Lane 端口在看到错误或丢失某些 Lane 的块对齐 (Block Alignment) 时延迟最终的链路宽度评估。对于 8b/10b，它应至少再等待两个 TS1，而对于 128b/130b 模式，它应至少等待 34 个 TS1，但在任何情况下都不能超过 1ms。其思想是 Lane 在上电或复位后可能需要稳定时间。

## _退出至"Detect 状态"_

在 2ms 超时后，如果无法配置链路（例如：Lane 0 不工作且 Lane 反转不可用），或者如果所有 Lane 收到两个连续的 Link 和 Lane 号都为 PAD 的 TS1，则链路必须退出到 Detect 状态。

## **下游 Lane**

## _在 Configuration.Lanenum.Wait 期间_

下游端口 (Downstream Port) 将继续使用非 PAD Link 和 Lane 号发送 TS1，直到满足退出条件之一为止。

## _退出至"Configuration.Lanenum.Accept"_

如果下面列出的任一情况为真：

- 如果在所有 Lane 上都收到两个连续的 TS1，其 Link 和 Lane 号与在这些 Lane 上传输的内容匹配。

**559**

**PCI Express 技术**

- 如果任何检测到接收器的 Lane 看到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD Link 号。规范指出，这允许两个端口在相互可接受的链路宽度上达成一致。

## _退出至"Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

上游 Lane

## _在 Configuration.Lanenum.Wait 期间_

上游端口 (Upstream Port) 将继续使用非 PAD Link 和 Lane 号发送 TS1，直到满足退出条件之一为止。

## _退出至"Configuration.Lanenum.Accept"_

如果下面列出的任一情况为真：

- 如果任何 Lane 收到两个连续的 TS2。

- 如果任何 Lane 收到两个连续的 TS1，其 Lane 号与 Lane 首次进入此子状态时不同，并且至少一些 Lane 看到非 PAD Link 号。

请注意，允许上游 Lane 在更改为该子状态之前等待最多 1ms，以防止接收错误或 Lane 之间的偏移影响最终的链路配置。

## _退出至"Detect 状态"_

在 2ms 超时后，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号设置为 PAD 的 TS1。

## **Configuration.Lanenum.Accept**

下游 Lane

## _在 Configuration.Lanenum.Accept 期间_

下游端口 (Downstream Port) 现在已收到具有非 PAD Link 和 Lane 号的 TS1。在此时，下游端口必须决定是否可以使用上游端口返回的 Lane 号建立链路。列出了三种可能的状态转换。

## _退出至"Configuration.Complete"_

如果收到两个连续的 TS1 具有相同的非 PAD Link 和 Lane 号，并且它们与为所有 Lane 的 TS1 中传输的 Link 和 Lane 号匹配，则上游端口已同意下游端口通告的 Link 和

**560**

**第 14 章：链路初始化与训练**

Lane 号，下一个子状态为 Configuration.Complete。或者如果接收到的 TS1 中的 Lane 号与下游端口通告的相反，如果下游端口支持 Lane 反转 (Lane Reversal)，它仍然可以继续到 Configuration.Complete，同时使用反转的 Lane 号。

规范指出，反转 Lane 条件严格定义为 Lane 0 收到具有最高 Lane 号（Lane 总数 ‐ 1）的 TS1，而最高 Lane 号收到 Lane 号为零的 TS1。可以从此了解课堂上偶尔出现的一个问题的答案：Lane 号可以混合而不是顺序吗？答案是不可以，它们必须是从 0 到 n‐1 或从 n‐1 到 0；不支持其他选项。

如果 Configuration 状态是从 Recovery 状态进入的，则可能已请求带宽更改。如果是这样，将更新状态位以报告发生的情况的性质。基本上，系统需要报告此更改是因链路无法可靠工作而发起，还是硬件只是管理链路电源。按如下方式更新位：

- 如果带宽更改是由下游端口 (Downstream Port) 由于可靠性问题而发起的，则将链路带宽管理状态 (Link Bandwidth Management Status) 位置为 1b。

- 如果带宽更改不是由下游端口发起，但在两个连续接收的 TS1 中的 Autonomous Change 位清零为 0b，则将链路带宽管理状态位置为 1b。

- 否则将链路自主带宽状态 (Link Autonomous Bandwidth Status) 位置为 1b。

## _退出至"Configuration.Lanenum.Wait"_

- 如果可以使用一些但不是所有接收两个具有相同非 PAD Link 和 Lane 号的连续 TS1 的 Lane 来形成已配置的链路，则这些 Lane 发送具有相同 Link 号和新 Lane 号的 TS1。目标是使用较小的 Lane 组来实现工作的链路。

新的 Lane 号必须从零开始并按顺序增加，以覆盖将使用的 Lane。任何未收到 TS1 的 Lane 不能成为该组的一部分，并且会扰乱 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。例如，如果有 8 个 Lane 可用，但 Lane 2 未看到传入的 TS1，则链路不能由需要 Lane 2 的组组成。因此，x8 和 x4 选项将不可用，并且仅可能使用 x1 或 x2 链路。

**561**

**PCI Express 技术**

## _退出至"Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号均为 PAD 的 TS1。

## **上游 Lane**

## _在 Configuration.Lanenum.Accept 期间_

- 上游端口 (Upstream Port) 现在已收到 TS2 或具有非 PAD Link 和 Lane 号的 TS1。在此时，上游端口必须决定是否可以使用下游端口发送的 Lane 号建立链路。列出了三种可能的状态转换。

## _退出至"Configuration.Complete"_

- 如果收到两个连续的 TS2 具有相同的非 PAD Link 和 Lane 号，并且它们与为这些 Lane 的 TS1 中传输的 Link 和 Lane 号匹配，则一切正常，下一个子状态将为 Configura‐ tion.Complete。

## _退出至"Configuration.Lanenum.Wait"_

- 如果可以使用接收两个具有相同非 PAD Link 和 Lane 号的连续 TS1 的 Lane 子集来形成已配置的链路，则这些 Lane 发送具有相同 Link 号和新 Lane 号的 TS1。目标是使用较小的 Lane 组来实现工作的链路。在这种情况下，下一个子状态将为 Configuration.Lanenum.Wait。

与下游 Lane 的情况一样，新的 Lane 号必须从零开始并按顺序增加，以覆盖将使用的 Lane。任何未收到 TS1 的 Lane 不能成为该组的一部分，并且会扰乱 Lane 编号。任何剩余的 Lane 必须发送 Link 和 Lane 设置为 PAD 的 TS1。

## _退出至"Detect 状态"_

- 如果无法配置链路，或者如果所有 Lane 收到两个连续的 Link 和 Lane 号均为 PAD 的 TS1，则下一个状态将为 Detect。

## **Configuration.Complete**

这是 Configuration 状态中唯一交换 TS2 的子状态。如前所述，TS2 的目的是在链路上的两个设备之间进行握手或确认它们已准备好进入下一状态。因此，这是对迄今为止在 TS1 中交换的 Link 和 Lane 号的最终确认。

**562**

**第 14 章：链路初始化与训练**
