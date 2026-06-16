下游端口 (Downstream Port) 如果希望继续进行均衡过程,以及当所有已配置的 Lane 接收到两个连续的 EC = 01b 的 TS1 时,将转换到 Phase 2。此时,该端口将 Equalization Phase 1 Successful 状态位置为 1b,并存储接收到的 TS1 LF 和 FS 值,以供 Phase 3 使用(如果下游端口计划调整上游端口的 Tx 系数)。

## _退出到"详细恢复子状态"_

如果下游端口不希望使用 Phase 2 和 Phase 3,则将状态位都置为 1b(Eq. Phase 1 Successful、Eq. Phase 2 Successful、Eq. Phase 3 Successful 和 Eq. Complete)。这样做的原因之一是它已经能够看到信号特性足够好,其余阶段不需要了。

## _退出到"Recovery.Speed"_

如果在 24ms 超时后未看到连续的 TS1,则下一个状态是 Recovery.Speed。successful_speed_negotiation 标志被清除为 0b,Equalization Complete 状态位被置为 1b。

**Phase 2 下游端口。** 在此阶段,下游端口发送 EC = 10b 的 TS1,并根据以下规则在每个 Lane 上独立分配系数设置:

- 如果接收到两个连续的 EC = 10b 的 TS1(上游端口已进入 Phase 2),无论是第一次收到,还是与上次预设或系数值不同,并且如果请求的值是合法且受支持的,那么在第二个 TS1 请求结束后的 500ns 内将 Tx 设置更改为使用这些值。此外,在发回上游端口的 TS1 中反映这些值,并将 Reject Coefficient Values 位清零至 0b。请注意,此更改不得导致发送器上的电压或参数非法超过 1ns。

   - a) 如果请求的预设或系数是非法或不受支持的,则不更改 Tx 设置,但在发送的 TS1 中反映接收到的值,并将 Reject Coefficient Values 位置为 1b(参见第 590 页的 Figure 14-38)。

- 如果未看到两个连续的 TS1,则保持当前的 Tx 预设和系数值。

## _退出到"Phase 3 下游端口"_

当上游端口对更改满意时,它将开始发送 EC = 11b 的 TS1,表示希望更改为 Phase 3。当接收到两个这样的连续 TS1 时,将 Eq. Phase 2 Successful 状态位置为 1b,并更改为 Phase 3。

## _退出到"Recovery.Speed"_

如果在 32ms 之后,Phase 3 的转换尚未发生,则该端口应清除 successful_speed_negotiation 标志,设置 Equalization Complete 状态位并退出到 Recovery.Speed 子状态。

_Figure 14-38: TS1 - 拒绝系数值_

**==> picture [264 x 258] intentionally omitted <==**

**----- Start of picture text -----**<br>
Symbol 6<br>7 6 5 4 3 2 1 0<br>0<br>Tx Preset EC<br>1 Link #<br>2 Lane # Use Preset Reset EIEOS<br>Interval Count<br>3 # FTS<br>Symbol 7<br>4 Rate ID<br>7 6 5 4 3 2 1 0<br>5 Train Ctl FS value when EC = 01b,<br>Rsvd<br>6 Otherwise Pre-Cursor Coefficient<br>EQ Info<br>Symbol 8<br>9<br>7 6 5 4 3 2 1 0<br>10<br>LF value when EC = 01b,<br>Rsvd<br>TS ID Otherwise Cursor Coefficient<br>13 Symbol 9<br>7 6 5 4 3 2 1 0<br>14<br>TS ID<br>15 P [RCV] Post-Cursor Coefficient<br>**----- End of picture text -----**<br>


**590** 

**Chapter 14: Link Initialization & Training** 

**Phase 3 下游端口。** 在此阶段,下游端口发送 EC = 11b 的 TS1,并开始为每个 Lane 独立评估上游端口的 Tx 设置。

在传输的 TS1 中,下游端口可以通过将 Use Preset 位置为 1b 并将 Tx Preset 字段设置为所需值来请求新的预设,或者通过将 Use Preset 位清零至 0b 并将 Pre-cursor、Cursor 和 Post-Cursor Coefficient 字段设置为所需值来请求新的系数。任何请求必须持续至少 1µs,或直到评估完成。如果要呈现新的预设或系数设置,则必须同时在所有 Lane 上发送。但是,如果给定 Lane 希望保留其当前设置,则不要求它请求新设置。

下游端口必须等待足够长的时间以确保上游发送器有机会实现请求的更改(500ns 加上逻辑的往返延迟),然后获取 Block Alignment 并评估传入的 TS1。在等待期间,预计不会有任何有用的内容来自上游端口,甚至可能是不合法的。这就是为什么之后获取 Block Alignment 是必需的原因。

如果看到两个连续的 TS1 与正在请求的相同预设或系数值匹配,并且 Reject Coefficient Values 位未设置,则请求的设置已被接受并可以评估。如果值匹配但 Reject Coefficient Values 位置为 1b,则请求的值已被上游端口拒绝且未被使用。对于这种情况,规范建议下游端口使用不同的值再试一次,但不要求这样做,也可以选择直接退出此阶段。

从请求发送之时到其评估完成之时,每个预设或系数请求所花费的总时间必须小于 2ms。对于在最终优化阶段需要更多时间的设计,可以有一个例外,但此阶段的总时间不能超过 24ms,并且该例外只能使用两次。如果接收器未识别任何传入的 TS1,则可以假设所请求的设置对该 Lane 不起作用。

## _退出到"详细恢复子状态"_

当所有已配置的 Lane 都具有最佳设置时,下一个状态将是 Recovery.RcvrLock。发生这种情况时,Equalization Phase 3 Successful 和 Equalization Complete 状态位将置为 1b。

**591** 

**PCI Ex ress Technolo p gy** 

_退出到"Recovery.Speed"_

否则,经过 24ms 超时(容差为 -0 或 +2ms)后,下一个状态将是 Recovery.Speed,successful_speed_negotiation 标志被清零至 0b,而 Equalization Complete 状态位置为 1b。

## **上游 Lane** 

上游端口从均衡过程的 Phase 0 开始,必须重置若干内部位。在 Link Status 2 寄存器(第 588 页的 Figure 14-36)中,以下位在进入此子状态时被清除:

- Equalization Phase 1 Successful 

- Equalization Phase 2 Successful 

- Equalization Phase 3 Successful 

- Link Equalization Request 

- Equalization Complete 

Link Control 3 寄存器的 Perform Equalization 位也被清零至 0b,内部变量 start_equalization_w_preset 也被清零。变量 equalization_done_8GT_data_rate 被置为 1b。

**Phase 0 上游端口。** 在此阶段,上游端口发送 EC = 00b 的 TS1,同时使用在进入此状态之前的 EQ TS2 中传递的 Tx Preset 值。正在发送的 TS1 中的均衡信息字段必须显示预设值以及与该预设对应的 Pre-cursor、Cursor 和 Post-cursor 系数字段。注意,如果 Lane 在 EQ TS2 中接收到保留或不受支持的 Tx Preset 值,或者根本没有收到 EQ TS2,则 Tx Preset 字段和系数值由该 Lane 的设备特定方法选择。

_退出到"Phase 1 上游端口"_

当所有已配置的 Lane 收到两个连续的 EC = 01b 的 TS1,表明它们可以识别始终以该值开始的来自下游端口的 TS1 时,下一个阶段是 Phase 1。

在 TS1 中接收到的均衡值 LF 和 FS 必须被存储并用于 Phase 2,如果上游端口计划调整下游端口的 Tx 系数的话。

上游端口在进入 Phase 0 之后,在评估传入的 TS1 之前可以等待 500ns,以便其接收器逻辑有时间稳定。

**592** 

**Chapter 14: Link Initialization & Training** 

## _退出到"Recovery.Speed"_

如果在 12ms 超时内未识别出传入的 TS1,则 LTSSM 将转换到 Recovery.Speed,清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 1 上游端口。** 在此阶段,上游端口发送 EC = 01b 的 TS1,同时使用在 Phase 0 中确定的发送器设置。这些 TS1 包含当前正在使用的 FS、LF 和 Post-cursor Coefficient 值。

## _退出到"Phase 2 上游端口"_

如果所有已配置的 Lane 接收到两个连续的 EC = 10b 的 TS1,表明下游端口希望转到 Phase 2,则下一个阶段将是 Phase 2,并且此端口将设置 Equalization Phase 1 Successful 状态位。

_退出到"详细恢复子状态"_

如果所有已配置的 Lane 接收到两个连续的 EC = 00b 的 TS1,这意味着下游端口已决定均衡过程已经完成,并希望跳过剩余的阶段。在这种情况下,下一个状态将是 Recovery.RcvrLock,并且 Equalization Phase 1 Successful 和 Equalization Complete 状态位置为 1b。

## _退出到"Recovery.Speed"_

否则,经过 12ms 超时后,LTSSM 将转换到 Recovery.Speed,清除 successful_speed_negotiation 标志并设置 Equalization Complete 状态位。

**Phase 2 上游端口。** 在此阶段,上游端口发送 EC = 10b 的 TS1,并开始为下游端口寻找最佳 Tx 值的过程。请记住,设置是为每个 Lane 独立确定的。过程如下:

在传输的 TS1 中,上游端口可以通过在正在发送的 TS1 的 Transmitter Preset 字段中放入合法值并将 Use Preset 位置为 1b 来请求新的预设,以告诉下游端口开始使用它。或者,通过在这些字段中放入合法值并将 Use Preset 位清零至 0b 来请求新系数,以便下游端口加载它们而不是预设字段。一旦发出请求,必须重复

**593** 

**PCI Ex ress Technolo p gy** 

至少 1µs,或直到评估完成。如果要呈现新的预设或系数设置,则必须同时在所有 Lane 上发送。但是,如果给定 Lane 希望保留其当前设置,则不要求它请求新设置。

上游端口必须等待足够长的时间以确保下游发送器有机会实现请求的更改(500ns 加上逻辑的往返延迟),然后获取 Block Alignment 并评估传入的 TS1。在等待期间,预计不会有任何有用的内容来自下游端口,甚至可能是不合法的。这就是为什么之后获取 Block Alignment 是必需的原因。

当接收到包含与正在发送的均衡字段相同且 Reject Coefficient Values 位未设置(0b)的 TS1 时,则该设置已被接受并可以评估。如果均衡字段匹配但 Reject Coefficient Values 位置为 1b,则该设置已被拒绝。在这种情况下,规范建议上游端口请求不同的均衡设置,但这不是必需的。

从请求发送之时到其评估完成之时,每个预设或系数请求所花费的总时间必须小于 2ms。对于在最终优化阶段需要更多时间的设计,可以有一个例外,但此阶段的总时间不能超过 24ms,并且该例外只能使用两次。如果接收器未识别任何传入的 TS1,则可以假设所请求的设置对该 Lane 不起作用。

_退出到"Phase 3 上游端口"_

如果所有已配置的 Lane 都具有最佳设置,则下一个阶段是 Phase 3。发生这种情况时,Equalization Phase 2 Successful 状态位将置为 1b。
