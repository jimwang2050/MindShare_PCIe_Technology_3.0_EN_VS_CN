DSP 执行与 USP 相同的操作，并通过检测背靠背 TS1 实现 10[‐4] 的 BER。在此期间，DSP 传达其 Tx 预设和 FS（Full Swing）、LF（Low Frequency）以及 Post-cursor 系数值，如 584 页 Figure 14‐32 所示。规范给出了一些必须满足的、针对一组所请求系数的附加规则，这些规则如下：

1. |C‐1| <= Floor (FS/4)，（注意：Floor 意味着向下舍入到整数值） 2. |C‐1| + C0 + |C+1| = FS

3. C0 ‐ |C‐1| ‐ |C+1| >= LF

**581**

## **PCI Ex ress Technolo p gy**

FS 表示最大电压，LF 将最小电压定义为 LF/FS。这些信息告知接收器可能的值数量，并允许系数作为整数值传达但作为小数值被理解。

作为示例，假设我们使用为 P7 预设设置定义的系数。FS 值用作参考，可以是 63 之前的任何数字，但为了便于计算，我们假设它为 30。对于 P7，C‐1 为 ‐0.1，在 TS1 中传达以表示 C‐1 的值为 3，因为 3/30 = 0.1，并且始终被视为负值。C+1 为 ‐0.2，因此将其传达为 6，因为 6/30 = 0.2 并且始终为负值。C0 为 0.7，因此它将作为 21 发送，因为 21/30 = 0.7。最后，LF 值表示可能的最小比值，对于 P7 而言，该比值为最大值的 0.4 倍。因此，LF 将被传达为 12，因为 12/30 = 0.4。

有了这些信息，让我们检查三个规则，看它们是否对 P7 情况得到满足：

1. 3 <= Floor (12/4)，这等于 3 <= 3，并且为真。

2. 3 + 21 + 6 = 30 这是真的。

3. 21 ‐ 3 ‐ 6 >= 12 这也为真，因此 P7 满足所有三个检查。

一旦下游端口确认链路工作得足够好可以继续进行（它识别出 EC = 01b 的传入 TS1），那么此阶段就完成了，它通过将其 EC = 10b 启动向 Phase 2 的变更（如图 583 页 Figure 14‐31 所示），并将下一步的控制权交回给 USP。当 USP 以 EC = 10b 响应时，两个 Port 都进入 Phase 2。作为一种愉快的替代方案，下游端口可以确定此时的信号质量已经足够好，无需进一步调整。在这种情况下，它将其 EC 设置为 00b 以退出均衡过程。

**582**

**Chapter 14: Link Initialization & Training**

_Figure 14‐31: Equalization Process: Initiating Phase 2_

**==> picture [232 x 202] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>
Downstream<br>
Port<br>
EC = 10b EC = 01b<br>
Upstream<br>
Port<br>
Endpoint<br>
**----- End of picture text -----**<br>


## **Phase 2**

信号质量已经足够好以识别 TS1，但还不足以用于运行时操作。一旦两个 Port 都进入 Phase 2，则允许上游端口为下游端口请求 Tx 设置，然后评估它们的工作效果，重复该过程直到获得当前环境下的最佳设置。为了提出请求，它更改其在 TS1 中发送的均衡信息值。如 584 页 Figure 14‐32 所示，有几个感兴趣的值：

- **Tx 预设 (Tx Preset)：** Tx 预设是对发送器设置的粗粒度调整，旨在使其进入当前信号环境的正确大致范围。上游端口设置此值，并设置 "Use Preset" 指示符（Symbol 6 的位 7）以告诉下游端口的发送器使用它。如果未设置 Use Preset 位，则表示预设应保持不变，并且应更改系数值。Tx 系数被视为细粒度调整。

**583**

## **PCI Ex ress Technolo p gy**

_Figure 14‐32: Equalization Coefficients Exchanged_

**==> picture [309 x 267] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>
7 6 5 4 3 2 1 0<br>
0<br>
Tx Preset EC<br>
1 Link #<br>
2 Lane # Use Preset Reset EIEOS<br>
Interval Count<br>
3 # FTS<br>
Symbol 7<br>
4 Rate ID<br>
7 6 5 4 3 2 1 0<br>
5 Train Ctl FS value when EC = 01b,<br>
Rsvd<br>
6 Otherwise Pre-Cursor Coefficient<br>
EQ Info<br>
Symbol 8<br>
9<br>
7 6 5 4 3 2 1 0<br>
10<br>
LF value when EC = 01b,<br>
Rsvd<br>
TS ID Otherwise Cursor Coefficient<br>
13 Symbol 9<br>
7 6 5 4 3 2 1 0<br>
14<br>
TS ID<br>
15 P [RCV] Post-Cursor Coefficient<br>
**----- End of picture text -----**<br>


- **系数 (Coefficients)：** 由于规范要求使用 3-tap Tx 均衡器，定义了三个系数值，可以将其视为对信号脉冲的电压调整，以补偿其在通过传输介质时将经历的失真，如 585 页 Figure 14‐33 所示。这在 474 页 "Solution for 8.0 GT/s ‐ Transmitter Equalization" 一节的物理层电气部分中进行了更详细的介绍。

- **Pre-Cursor 系数：** 应用于采样点之前信号的乘数，可根据需要增强或减弱信号。

- **Cursor 系数：** 采样点乘数；始终为正。

- **Post-Cursor 系数：** 应用于采样点之后信号的乘数，可根据需要增强或减弱信号。

- 一旦信号达到所需的质量标准，上游端口通过将 EC 更改为 11b 来表示它已准备好进入下一阶段。

**584**

**Chapter 14: Link Initialization & Training**

_Figure 14‐33: 3‐Tap Transmitter Equalization_

**==> picture [251 x 238] intentionally omitted <==**

**----- Start of picture text -----**<br>
V<br>
Unmodified Signal<br>
t<br>
UI UI UI UI<br>
Cursor<br>
V<br>
Pre-cursor Post-cursor<br>
reduction reduction<br>
Equalized Signal<br>
t<br>
UI UI UI UI<br>
Cursor<br>
**----- End of picture text -----**<br>


_Figure 14‐34: Equalization Process: Adjustments During Phase 2_

**==> picture [250 x 200] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>
Evaluate Propose<br>
resulting new Tx<br>
Rx signal EQ values<br>
Endpoint<br>
**----- End of picture text -----**<br>


**585**

**PCI Ex ress Technolo p gy**

## **Phase 3**

下游端口通过发送 EC = 11b 进行响应，并且现在可以为上游端口的发送器执行相同的信号评估过程。它发送请求新设置的 TS1，方式如下：如果设置了 Use Preset 位，则定义新预设，否则将提供新系数。连续发送此内容 1μs 或直到请求已对其结果进行评估，以较晚者为准。该评估必须等待 500ns，加上通过发送逻辑传出和返回到接收逻辑的往返时间。可以测试不同的均衡设置，直到找到实现所需信号质量的一个设置为止。在该点，下游端口通过将 EC 设置为 00b 来退出均衡过程。

_Figure 14‐35: Equalization Process: Adjustments During Phase 3_

**==> picture [252 x 197] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Port<br>
Propose Evaluate<br>
new Tx<br>
resulting<br>
EQ values<br>
Rx signal<br>
Endpoint<br>
**----- End of picture text -----**<br>


## **均衡说明**

规范提到了与均衡过程相关的其他项目，如下所述：

- 所有 Lane 必须参与该过程；即使那些稍后可能在 upconfigure 事件之后才变为活动的 Lane。

- 组件用于评估传入信号并确定其链路对端应使用的均衡值的算法在规范中并未给出，属于实现特定的。

**586**

**Chapter 14: Link Initialization & Training**

- 均衡变更可以针对任意数量的 Lane 请求，并且 Lane 可以使用不同的值。

- 在细调步骤结束时（上游端口为 Phase 2，下游端口为 Phase 3），每个组件负责确保发送器设置使其满足规范要求。

- 组件必须评估调整其发送器设置的请求并采取行动。如果给出了有效值，它们必须使用这些值，并将其反映在它们发送的 TS1 中。

- 如果值不符合规则，则可以拒绝调整系数的请求。所请求的值仍会反映在发回的 TS1 中，但 Reject Coefficient Values 位将被设置。

- 组件必须存储通过此过程确定的均衡值，以供将来在 8.0 GT/s 下使用。规范并未明确说明这一点，但作者的观点是这些值将在速度更改为较低速率然后再返回到 8.0 GT/s 速率时仍然保留。这是有意义的，因为重复 EQ 过程可能需要很长时间，并且假设电气环境没有变化，所得到的值将相同。

- 组件允许随时微调其接收器，只要不会导致链路变得不可靠或进入 Recovery 状态。

## **详细的均衡子状态**

本节涵盖链路均衡期间状态机行为的详细描述。

## **Recovery.Equalization**

此子状态用于执行 8.0 GT/s 及更高速率的链路均衡过程。较低速率不使用均衡，并且在这些速率生效时 LTSSM 不会进入此子状态。由于这是 PCIe 的一个新且复杂的主题，因此从高级别视图对整体均衡过程的描述在状态机详细信息之后呈现，参见 577 页 "Link Equalization Overview" 一节。但首先，让我们逐步了解子状态以查看该过程的机制。

## **下游 Lane**

下游端口从均衡过程的 Phase 1 开始。要开始此过程，需要重置几个位。在 Link Status 2 寄存器（588 页 Figure 14‐36）中，进入此子状态时清除以下位：

**587**

**PCI Ex ress Technolo p gy**

- Equalization Phase 1 Successful

- Equalization Phase 2 Successful

- Equalization Phase 3 Successful

- Link Equalization Request

- Equalization Complete

Link Control 3 寄存器的 Perform Equalization 位也被清除为 0b，内部变量 start_equalization_w_preset 也被清除。equalization_done_8GT_data_rate 变量被设置为 1b。

_Figure 14‐36: Link Status 2 Register_

**==> picture [320 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 6 5 4 3 2 1 0<br>
RsvdZ<br>
Link Equalization Request<br>
Equalization Phase 3 Successful<br>
Equalization Phase 2 Successful<br>
Equalization Phase 1 Successful<br>
Equalization Complete<br>
Current De-emphasis Level<br>
**----- End of picture text -----**<br>


_Figure 14‐37: Link Control 3 Register_

**==> picture [341 x 103] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 2 1 0<br>
RsvdP<br>
Link Equalization Request<br>
Interrupt Enable<br>
Perform Equalization<br>
**----- End of picture text -----**<br>


**588**

**Chapter 14: Link Initialization & Training**

**Phase 1 Downstream。** 在此阶段，下游端口发送 EC = 01b 的 TS1，同时使用来自 Lane Equalization Control 寄存器的预设值，并使用与 Tx 预设字段对应的 FS、LF 和 Post-cursor 系数字段。如果需要时间稳定其接收器逻辑，则允许其等待 500ns 后再评估传入的 TS1。

## _退出至 "Phase 2 Downstream"_

如果下游端口希望继续均衡过程，并且当所有已配置的 Lane 接收到两个连续的 EC = 01b 的 TS1 时，下游端口将转换到 Phase 2。此时，Port 将 Equalization Phase 1 Successful 状态位设置为 1b，并存储接收到的 TS1 LF 和 FS 值以在 Phase 3 中使用（如果下游端口计划调整上游端口的 Tx 系数）。

## _退出至 "详细的 Recovery 子状态"_

如果下游端口不希望使用 Phase 2 和 Phase 3，则它将状态位设置为 1b（Eq. Phase 1 Successful、Eq. Phase 2 Successful、Eq. Phase 3 Successful 和 Eq. Complete）。这样做的原因之一可能是它已经可以看到信号特性足够好，不需要其他阶段。

## _退出至 "Recovery.Speed"_

如果在 24ms 超时后仍未看到连续的 TS1，则下一状态为 Recovery.Speed。successful_speed_negotiation 标志被清除为 0b，Equalization Complete 状态位被设置为 1b。

**Phase 2 Downstream。** 在此阶段，下游端口发送 EC = 10b 的 TS1，并根据以下规则在每个 Lane 上独立分配系数设置：

- 如果接收到两个连续的 EC = 10b 的 TS1（上游端口已进入 Phase 2），无论是首次接收，还是具有与上次不同的预设或系数值，并且如果所请求的值是合法且受支持的，则在第二个 TS1 请求结束后的 500ns 内将 Tx 设置更改为使用它们。同时，在发送回上游端口的 TS1 中反映这些值，并将 Reject Coefficient Values 位清除为 0b。请注意，更改不得使发送器处的电压或参数违规超过 1ns。

   - a) 如果所请求的预设或系数不合法或不受支持，则不要更改 Tx 设置，但在

**589**

## **PCI Ex ress Technolo p gy**

发送的 TS1 中反映接收到的值，并将 Reject Coefficient Values 位设置为 1b（参见 590 页 Figure 14‐38）。

- 如果未看到两个连续的 TS1，则保持当前 Tx 预设和系数值。

## _退出至 "Phase 3 Downstream"_

当上游端口对更改感到满意时，它开始发送 EC = 11b 的 TS1，表明希望更改为 Phase 3。当接收到两个这样的连续 TS1 时，将 Eq. Phase 2 Successful 状态位设置为 1b 并更改为 Phase 3。

## _退出至 "Recovery.Speed"_

如果在 32ms 之后，尚未发生到 Phase 3 的转换，则 Port 应清除 successful_speed_negotiation 标志，设置 Equalization Complete 状态位并退出到 Recovery.Speed 子状态。

_Figure 14‐38: TS1s ‐ Rejecting Coefficient Values_

**==> picture [264 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>
7 6 5 4 3 2 1 0<br>
0<br>
Tx Preset EC<br>
1 Link #<br>
2 Lane # Use Preset Reset EIEOS<br>
Interval Count<br>
3 # FTS<br>
Symbol 7<br>
4 Rate ID<br>
7 6 5 4 3 2 1 0<br>
5 Train Ctl FS value when EC = 01b,<br>
Rsvd<br>
6 Otherwise Pre-Cursor Coefficient<br>
EQ Info<br>
Symbol 8<br>
9<br>
7 6 5 4 3 2 1 0<br>
10<br>
LF value when EC = 01b,<br>
Rsvd<br>
TS ID Otherwise Cursor Coefficient<br>
13 Symbol 9<br>
7 6 5 4 3 2 1 0<br>
14<br>
TS ID<br>
15 P [RCV] Post-Cursor Coefficient<br>
**----- End of picture text -----**<br>


**590**

**Chapter 14: Link Initialization & Training**

**Phase 3 Downstream。** 在此阶段，下游端口发送 EC = 11b 的 TS1，并开始为每个 Lane 独立评估上游 Tx 设置的过程。

在发送的 TS1 中，下游端口可以通过将 Use Preset 位设置为 1b 并将 Tx 预设字段设置为所需值来请求新预设，或者通过将 Use Preset 位清除为 0b 并将 Pre-cursor、Cursor 和 Post-Cursor 系数字段设置为所需值来请求新系数。任何一种请求都必须连续发送至少 1μs 或直到评估完成。如果要提供新的预设或系数设置，则必须在所有 Lane 上同时发送。但是，如果某个 Lane 希望保留其当前设置，则不需要该 Lane 请求新设置。

下游端口必须等待足够长的时间以确保上游发送器有机会实现所请求的更改（500ns 加上逻辑的往返延迟），然后获取 Block Alignment 并评估传入的 TS1。在等待期间，预计不会从上游端口收到任何有用的内容，甚至可能不合法。这就是为什么在那段时间之后获取 Block Alignment 是必需的。

如果看到两个连续的 TS1 与正在请求的相同预设或系数值匹配，并且未设置 Reject Coefficient Values 位，则所请求的设置已被接受并可以评估。如果值匹配但 Reject Coefficient Values 位设置为 1b，则所请求的值已被上游端口拒绝并且未在使用中。对于这种情况，规范建议下游端口使用不同的值重试，但不要求这样做，并且可以选择简单地退出此阶段。

对预设或系数请求所花费的总时间（从发送请求到完成评估）必须小于 2ms。对于在最终优化阶段需要更多时间的设计，可提供例外，但此阶段的总时间不能超过 24ms，并且例外只能使用两次。如果接收器无法识别任何传入的 TS1，则可以假定所请求的设置对该 Lane 不起作用。

## _退出至 "详细的 Recovery 子状态"_

当所有已配置的 Lane 都具有其最佳设置时，下一状态将为 Recovery.RcvrLock。发生这种情况时，Equalization Phase 3 Successful 和 Equalization Complete 状态位将被设置为 1b。

**591**

**PCI Ex ress Technolo p gy**

_退出至 "Recovery.Speed"_

否则，在 24ms 超时后（容差为 ‐0 或 +2ms），下一状态将为 Recovery.Speed，successful_speed_negotiation 标志被清除为 0b，同时 Equalization Complete 状态位被设置为 1b。

## **上游 Lane**

上游端口从均衡过程的 Phase 0 开始，并且必须重置几个内部位。在 Link Status 2 寄存器（588 页 Figure 14‐36）中，进入此子状态时清除以下位：

- Equalization Phase 1 Successful

- Equalization Phase 2 Successful

- Equalization Phase 3 Successful

- Link Equalization Request

- Equalization Complete

Link Control 3 寄存器的 Perform Equalization 位也被清除为 0b，内部变量 start_equalization_w_preset 也被清除。equalization_done_8GT_data_rate 变量被设置为 1b。

**Phase 0 Upstream。** 在此阶段，上游端口发送 EC = 00b 的 TS1，同时使用在进入此状态之前在 EQ TS2 中传递的 Tx 预设值。正在发送的 TS1 中的均衡信息字段必须显示预设值以及与该预设对应的 Pre-cursor、Cursor 和 Post-cursor 系数字段。请注意，如果 Lane 在 EQ TS2 中接收到保留的或不受支持的 Tx 预设值，或者根本没有接收到 EQ TS2，则该 Lane 的 Tx 预设字段和系数值由设备特定的方法选择。

_退出至 "Phase 1 Upstream"_

当所有已配置的 Lane 接收到两个连续的 EC = 01b 的 TS1 时，表明它们能够识别来自下游端口的 TS1（下游端口始终以此值开始），则下一阶段为 Phase 1。

如果上游端口计划调整下游端口的 Tx 系数，则必须存储在 TS1 中接收到的均衡值 LF 和 FS 以在 Phase 2 期间使用。

上游端口可以在进入 Phase 0 之后等待 500ns 再评估传入的 TS1，以使其接收器逻辑有时间稳定。

**592**

**Chapter 14: Link Initialization & Training**

## _退出至 "Recovery.Speed"_

如果在 12ms 超时内未识别传入的 TS1，则 LTSSM 将转换到 Recovery.Speed，清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 1 Upstream。** 在此阶段，上游端口发送 EC = 01b 的 TS1，同时使用在 Phase 0 中确定的发送器设置。这些 TS1 包含 FS、LF 和 Post-cursor 系数值以及当前正在使用的内容。

## _退出至 "Phase 2 Upstream"_

如果所有已配置的 Lane 接收到两个连续的 EC = 10b 的 TS1，表明下游端口希望进入 Phase 2，则下一阶段将为 Phase 2，并且此 Port 将设置 Equalization Phase 1 Successful 状态位。

_退出至 "详细的 Recovery 子状态"_

如果所有已配置的 Lane 接收到两个连续的 EC = 00b 的 TS1，则意味着下游端口已确定均衡过程已经完成，并希望跳过剩余阶段。在这种情况下，下一状态将为 Recovery.RcvrLock，并且 Equalization Phase 1 Successful 和 Equalization Complete 状态位被设置为 1b。

## _退出至 "Recovery.Speed"_

否则，在 12ms 超时后，LTSSM 将转换到 Recovery.Speed，清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 2 Upstream。** 在此阶段，上游端口发送 EC = 10b 的 TS1，并开始为下游端口寻找最佳 Tx 值的过程。回想一下，每个 Lane 的设置是独立确定的。过程如下：

在发送的 TS1 中，上游端口可以通过在正在发送的 TS1 的 Transmitter Preset 字段中放置合法值并将 Use Preset 位设置为 1b 来告诉下游端口开始使用它，以请求新预设。或者，通过在这些字段中放置合法值并将 Use Preset 位清除为 0b 来请求新系数，以便下游端口加载它们而不是预设字段。一旦发出请求，必须重复

**593**

**PCI Ex ress Technolo p gy**

至少 1μs 或直到评估完成。如果要提供新的预设或系数设置，则必须在所有 Lane 上同时发送。但是，如果某个 Lane 希望保留其当前设置，则不需要该 Lane 请求新设置。

上游端口必须等待足够长的时间以确保下游发送器有机会实现所请求的更改（500ns 加上逻辑的往返延迟），然后获取 Block Alignment 并评估传入的 TS1。在等待期间，预计不会从下游端口收到任何有用的内容，甚至可能不合法。这就是为什么在那段时间之后获取 Block Alignment 是必需的。

当接收到包含与正在发送的相同均衡字段的 TS1 并且 Reject Coefficient Values 位未设置（0b）时，则该设置已被接受并且现在可以评估。如果均衡字段匹配但 Reject Coefficient Values 位被设置（1b），则该设置已被拒绝。在这种情况下，规范建议上游端口请求不同的均衡设置，但这不是必需的。

对预设或系数请求所花费的总时间（从发送请求到完成评估）必须小于 2ms。对于在最终优化阶段需要更多时间的设计，可提供例外，但此阶段的总时间不能超过 24ms，并且例外只能使用两次。如果接收器无法识别任何传入的 TS1，则可以假定所请求的设置对该 Lane 不起作用。

_退出至 "Phase 3 Upstream"_

如果所有已配置的 Lane 都具有其最佳设置，则下一阶段为 Phase 3。发生这种情况时，Equalization Phase 2 Successful 状态位将被设置为 1b。
