- 规范指出"任何 Lane"这一规定支持前面描述的负载板使用模型，以允许设备循环遍历所有支持的测试用例。

- b) Enter Compliance 位自进入 Polling.Compliance 以来已清零 (0b)。

- c) 对于上游端口，Enter Compliance 位设置为 (1b) 并且在任何 Lane 上检测到 EIOS。此条件清零 Enter Compliance 位 (0b)。

如果数据速率不是 2.5 GT/s 或在进入 Polling.Compliance 期间设置了 Enter Compliance 位，则发送器发送 8 个连续的 EIOS 并在转换到 Polling.Active 之前进入电气空闲。在电气空闲期间，端口更改为 2.5 GT/s 并稳定 1ms 到 2ms 之间的时间。

发送多个 EIOS 有助于确保链路伙伴将检测到至少一个并在用于 Enter Compliance 寄存器位进入时退出 Polling.Compliance

**修改合规模式。** 如果 Polling.Compliance 是因为 TS1 指示而进入的，并且要么设置了 Compliance Receive 位并清除了 Loopback 位，要么 Link Control 2 寄存器中的 Enter Compliance 和 Enter Modified Compliance 位都被设置，则在所有检测到的 Lane 上发送错误状态符号清零为全零的修改合规模式。

**537**

**PCI Express Technology**

如果速率为 2.5 或 5.0 GT/s，则每个 Lane 通过查找修改合规模式的一个实例来指示对传入模式的成功锁定，然后在其发送回的修改合规模式中设置 Pattern Lock 位（8 位错误状态符号的位 7）。

- 错误状态符号不能用于锁定过程中，因为如果链路伙伴尚未锁定，它们没有意义，因此它们的含义可能是未定义的。

- 模式的一个实例定义如下所述的 4 个符号序列：K28.5、D21.5、K28.5 和 D10.2 或这些符号的补码（意味着极性反转）。

- 被测设备必须在从链路伙伴接收到修改合规模式后的 1ms 内设置其发送的修改合规模式中的 Pattern Lock 位。

- 一个 Lane 上的任何接收器错误都会将该 Lane 的错误计数递增 1，并在计数达到 127 时饱和（不会更高或回绕）。

如果速率是 8.0 GT/s

- 进入此子状态时，Error_Status 字段设置为 00h。

- 被测设备必须在从链路伙伴接收到修改合规模式后的 4ms 内设置其发送的修改合规模式中的 Pattern Lock 位。

- 每个 Lane 在实现块对齐时独立设置 Pattern Lock。之后，数据块中的符号应为 IDL (00h)，任何不匹配的符号都会将计数递增 1。接收器错误计数在 127 处饱和，并在包含在此模式中的 SOS 的最后 2 个符号中发送。

- 加扰要求照常应用于修改合规模式：种子值按 Lane 设置，EIEOS 启动 LFSR，SOS 不推进 LFSR。

- 规范指出，设备应在获取块对齐之前等待足够长的时间以确保其接收器已稳定且不会看到任何位滑动。它甚至提到设备可能希望重新验证其块对齐，然后再设置 Pattern Lock 位。

## _退出到 "Polling.Active"_

如果在进入 Polling.Compliance 时设置了 Enter Compliance 位 (1b)，并且要么 Enter Compliance 位已清零 (0b)，要么它是上游端口并在任何 Lane 上接收到 EIOS。这也会导致其 Enter Compliance 位清零 (0b)。

**538**

**第 14 章：链路初始化与训练**

如果数据速率不是 2.5 GT/s 或在进入 Polling.Compliance 期间设置了 Enter Compliance 位，则发送器发送 8 个连续的 EIOS 并在转换到 Polling.Active 之前进入电气空闲。在电气空闲期间，端口更改为 2.5 GT/s 和 ‐3.5dB 去加重，并且此时间必须介于 1ms 和 2ms 之间。

发送多个 EIOS 有助于确保链路伙伴将检测到至少一个并在用于 Enter Compliance 寄存器位进入时退出 Polling.Compliance。

## _退出到 "Detect 状态"_

如果 Link Control 2 寄存器中的 Enter Compliance 位清零 (0b) 并且设备被指示退出此子状态。

_图 14‐12：Link Control 2 寄存器的 "Enter Compliance" 位_

**==> picture [301 x 168] intentionally omitted <==**

**----- Start of picture text -----**<br>
Link Control 2 寄存器<br>15 12 11 10 9 7 6 5 4 3 0<br>Compliance Preset/<br>De-emphasis<br>Compliance SOS<br>Enter Modified Compliance<br>Transmit Margin<br>Selectable De-emphasis<br>Hardware Autonomous<br>Speed Disable<br>Enter Compliance<br>Target Link Speed<br>**----- End of picture text -----**<br>


## **Configuration 状态**

最初，Configuration 状态以 2.5 GT/s 速率执行链路和 Lane 编号；但是，存在允许 5 GT/s 和 8 GT/s 设备也从 Recovery 状态进入 Configuration 状态的规定。从 Recovery 到 Configuration 的转换主要是为了对多 Lane 设备的链路宽度进行动态更改。动态更改仅支持 5 GT/s 和 8 GT/s 设备。因此，这些设备的详细状态转换出现在从第 552 页开始的详细 Configuration 子状态描述中。

**539**

**PCI Express Technology**

## **Configuration 状态 — 概述**

此状态的主要目标是发现端口是如何连接的并为其分配 Lane 编号。例如，8 个 Lane 可能可用但只有 2 个处于活动状态，或者 Lane 可以拆分为多个链路，例如两个 x4 链路。与其他状态不同，端口具有取决于它们是面向上游还是下游的已定义角色。因此，这些子状态的描述分为下游 Lane 和上游 Lane 的行为。下游端口（向下游发送的端口）在此链路上扮演"领导者"角色，以完成链路初始化过程中的其余状态。上游端口（向上游发送的端口）扮演"追随者"角色。领导者或下游端口将向上游端口指定链路和 Lane 编号，上游端口将简单地以其被告知的相同值进行回复，除非存在冲突，我们将在本节中看到这一点。链路和 Lane 编号在此期间交换的 TS1 的字段中报告，如第 540 页的图 14‐13 中再次所示。这些字段包含 PAD 符号作为占位符，直到分配实际值。

_图 14‐13：TS1/TS2 中的链路和 Lane 编号编码_

**==> picture [292 x 213] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM K28.5<br>1 Link # 0 - 255 = D0.0 - D31.7，PAD = K23.7<br>2 Lane # 0 - 31 = D0.0 - D17.1，PAD = K23.7<br>3 # FTS 接收器恢复 L0s 所需的 FTS 数量<br>4 Rate ID 位 1 必须设置，表示支持 2.5 GT/s<br>5 Train Ctl<br>6 TS ID 或更改到 8.0 GT/s 时的均衡信息，否则<br>9 EQ Info TS1 或 TS2 标识符<br>10<br>TS1 标识符 = D10.2<br>TS ID<br>TS2 标识符 = D5.2<br>15<br>**----- End of picture text -----**<br>


**540**

**第 14 章：链路初始化与训练**

## **设计具有可合并链路的设备**

设计人员根据性能和成本要求选择在给定链路上实现多少 Lane。窄链路可以选择性地组合成更宽的链路，宽链路可以选择性地拆分为多个较窄的链路。第 541 页的图 14‐14 显示了具有一个上游端口和四个 x2 下游端口的交换机。在此示例中，它们还可以分组为两个 x4 链路。作为提醒，规范要求每个端口还必须支持作为 x1 链路运行。

如图的左侧所示，交换机内部由一个上游逻辑桥和四个下游逻辑桥组成。每个端口需要一个桥，因此支持 4 个下游端口需要 4 个下游桥。但是，如果端口按图的右侧所示组合，则某些桥只是未使用。在链路训练期间，每个下游端口的 LTSSM 确定实际实现的连接选项。

_图 14‐14：组合 Lane 以形成更宽的链路（链路合并）_

**==> picture [378 x 204] intentionally omitted <==**

**----- Start of picture text -----**<br>
x8<br>x8<br>交换机 交换机<br>虚拟 虚拟<br>PCI PCI<br>桥 0 桥 0<br>或<br>虚拟 虚拟 虚拟 虚拟 虚拟 虚拟<br>PCI PCI PCI PCI PCI PCI<br>桥 1 桥 2 桥 3 桥 4 桥 1 桥 2<br>x2 x2 x2 x2<br>x4 x4<br>**----- End of picture text -----**<br>


**541**

**PCI Express Technology**

## **Configuration 状态 — 训练示例**

## **介绍**

在 Configuration 状态中，链路和 Lane 编号过程由下游端口"领导者"（例如，根端口或交换机下游端口）启动。端点和交换机上游端口不启动，但响应。它们是"追随者"。现在让我们考虑一些示例以使概念更容易理解。

## **链路配置示例 1**

第 543 页图 14‐15 中所示的设备都支持实现 x4、x2 或 x1 Lane 大小的单个链路。Lane 编号分配由设备内部固定，必须从零开始按顺序排列。物理 Lane 编号显示在设备框内，报告的或逻辑的 Lane 编号由 TS 有序集报告。通常，这些将是相同的，但并非在每种情况下都如此。

## **链路号协商。**

1. 由于此示例中只有一个链路可能，下游端口（向下游发送的端口）对所有 Lane 发送使用相同链路号 _N_ 的 TS1，Lane 号为 PAD。

2. 在此 Configuration 状态中，上游端口开始发送 Link 和 Lane 号字段中带有 PAD 的 TS1，但在接收到来自下游端口的带有非 PAD 链路号的 TS1 后，上游端口在所有连接的 Lane 上以反映相同链路号 _N_ 和 Lane 号字段的 PAD 进行响应。基于此响应，下游 LTSSM 识别出四个 Lane 已响应并使用与正在发送的相同的链路号，因此所有 4 个 Lane 将被配置为一个链路。链路号本身是特定于实现的值，不存储在任何定义的配置寄存器中，也与端口号或任何其他值无关。

**542**

**第 14 章：链路初始化与训练**

_图 14‐15：示例 1 — 步骤 1 和 2_

**==> picture [298 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>LTSSM<br>（下游端口）<br>0 1 2 3<br>步骤 1<br>Lane # PAD PAD PAD PAD<br>TS1<br>Link # N N N N<br>N N N N Link #<br>TS1<br>PAD PAD PAD PAD Lane #<br>0 1 2 3 步骤 2<br>（上游端口）<br>LTSSM<br>选项：一个链路 x4、x2 或 x1<br>**----- End of picture text -----**<br>


## **Lane 号协商。**

3. 下游端口现在开始发送具有相同链路号的 TS1，但为连接的 Lane 分配 Lane 号 0、1、2 和 3，如图 14‐16（第 544 页）所示。

4. 响应于传入的非 PAD Lane 号，上游端口将验证传入的 Lane 号是否与接收它们的 Lane 号匹配。在此示例中，下游和上游端口的 Lane 连接正确。因为所有 Lane 号都匹配，上游端口也在其发送的 TS1 中通告其 Lane 号。当下游端口看到响应中的非 PAD Lane 号时，它将传入的编号与其正在发送的值进行比较。如果它们匹配，一切都很好，但如果不匹配，则需要采取其他步骤。如果一些（但不是全部）Lane 号匹配，则可以相应地调整链路宽度。如果 Lane 反转，则将需要可选的 Lane 反转功能。因为它是可选的，所以 Lane 可能已反转但任一设备都无法纠正它。这将是一个严重的板设计错误，因为在这种情况下可能无法配置链路以进行操作。

**543**

## **PCI Express Technology**

_图 14‐16：示例 1 — 步骤 3 和 4_

**==> picture [356 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>LTSSM<br>（下游端口）<br>0 1 2 3<br>步骤 3<br>Lane # 0 1 2 3<br>TS1<br>Link # N N N N<br>N N N N Link #<br>TS1<br>0 1 2 3 Lane #<br>0 1 2 3 步骤 4<br>（上游端口）<br>LTSSM<br>选项：一个链路 x4、x2 或 x1<br>**----- End of picture text -----**<br>


## **确认链路和 Lane 号。**

5. 由于所有 Lane 上的发送和接收链路和 Lane 号匹配，下游端口通过发送具有相同链路和 Lane 号的 TS2 有序集来表示它已准备好结束此协商并继续到下一个状态 L0。

6. 在接收到具有相同链路和 Lane 号的 TS2 后，上游端口也通过发送回 TS2 来表示其准备好离开 Configuration 状态并继续到 L0。这在第 545 页的图 14‐17 中示出。

7. 一旦端口接收到至少 8 个 TS2 并发送至少 16 个，它将发送一些逻辑空闲数据，然后转换到 L0。

**544**

**第 14 章：链路初始化与训练**

_图 14‐17：示例 1 — 步骤 5 和 6_

**==> picture [345 x 215] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>LTSSM<br>（下游端口）<br>0 1 2 3<br>步骤 5<br>Lane # 0 1 2 3<br>TS2<br>Link # N N N N<br>N N N N Link #<br>TS2<br>0 1 2 3 Lane #<br>0 1 2 3 步骤 6<br>LTSSM<br>（上游端口）<br>**----- End of picture text -----**<br>


选项：一个链路 x4、x2 或 x1

## **链路配置示例 2**

应涵盖的另一个示例是具有 4 个下游 Lane 的设备，该设备能够配置为单个 x4 链路或两个 x2 链路或四个 x1 链路的组合。因此，即使一个 x2 链路和两个 x1 链路的配置也可以。此类设备的示例如第 546 页的图 14‐18 所示。

如果所有四个 Lane 都检测到接收器并达到 Configuration 状态，则有许多连接可能性：

- 一个 x4 链路

- 两个 x2 链路

- 一个 x2 链路和两个 x1 链路

- 四个 x1 链路

规范中定义的一种示例方法，用于确定实现哪些配置，如下所述。

**545**

**PCI Express Technology**

## **链路号协商。**

1. 在此示例方法中，下游端口开始通过在每个 Lane 上通告唯一的链路号。Lane 0 通告链路号 N，Lane 1 通告链路号 N+1，依此类推，如第 546 页的图 14‐18 所示。这些链路号只是示例，它们不必是连续的。同样重要的是要记住下游端口不知道它连接到的是什么，并且在此过程中端口正在尝试确定每个 Lane 的连接。

_图 14‐18：示例 2 — 步骤 1_

**==> picture [298 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>两个链路 x2 或 x1<br>四个链路 x1<br>LTSSM<br>（下游端口）<br>步骤 1 0 1 2 3<br>Lane # PAD PAD PAD PAD<br>TS1<br>Link # N N+1 N+2 N+3<br>PAD PAD PAD PAD Link #<br>TS1<br>PAD PAD PAD PAD Lane #<br>0 1 1 0<br>（上游 （上游<br>端口） 端口）<br>LTSSM LTSSM<br>选项： 选项：<br>一个链路 x2 或 x1 一个链路 x2 或 x1<br>**----- End of picture text -----**<br>


2. 在接收到返回的 TS1 时，下游端口识别出两件事：所有四个 Lane 都正常工作并且它们连接到两个不同的上游端口。这意味着实际上将有_两个_下游端口。每个下游端口将有自己的 Lane 0 和 Lane 1，如图 14‐20（第 548 页）所示。

**546**

**第 14 章：链路初始化与训练**

_图 14‐19：示例 2 — 步骤 2_

**==> picture [286 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>两个链路 x2 或 x1<br>四个链路 x1<br>LTSSM<br>（下游端口）<br>0 1 2 3<br>Lane # 0 PAD PAD PAD<br>TS1<br>Link # N N+1 N+2 N+3<br>N N N+2 N+2 Link #<br>TS1<br>PAD PAD PAD PAD Lane #<br>0 1 1 0 步骤 2<br>（上游 （上游<br>端口） 端口）<br>LTSSM LTSSM<br>选项： 选项：<br>一个链路 x2 或 x1 一个链路 x2 或 x1<br>**----- End of picture text -----**<br>


## **Lane 号协商。**

3. 该过程现在为每个链路独立继续，但它们将采用与之前相同的步骤来确定 Lane 号：下游端口将在 TS1 中通告其 Lane 号。还需要注意的是，下游端口开始为链路的 Lane 通告单个返回的链路号。左侧的链路正在为两个 Lane 通告链路号 N，右侧的链路正在通告 N+2。

4. 在此示例中，链路上左侧的下游和上游端口的 Lane 号匹配。但是，对于右侧的链路，下游端口的 Lane 号与连接的上游端口的 Lane 号相反。上游端口意识到这一点，如果它支持 Lane 反转，它将在内部实现并回复与下游端口通告的相同的 Lane 号，如图 14‐20 所示。如果上游端口不支持 Lane 反转，它将在中通告其自己的 Lane 号

**547**

## **PCI Express Technology**

- 返回的 TS1，然后下游端口将意识到该问题并有机会实现 Lane 反转。

5. Lane 反转可以由任一端口可选地处理。如果上游端口检测到此情况并支持 Lane 反转，它只需在内部进行 Lane 分配更改，并使用正确的 Lane 号返回 TS1。因此，下游端口不知道曾经存在问题。如果上游端口无法处理 Lane 反转，那么下游端口将看到按相反顺序的传入 Lane 号。如果它支持 Lane 反转，那么它将纠正编号并开始使用新的 Lane 号发送 TS2。

_图 14‐20：示例 2 — 步骤 3、4 和 5_

**==> picture [370 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
步骤 3<br>LTSSM LTSSM<br>（下游 （下游<br>端口） 端口）<br>0 1 0 1<br>步骤 4<br>Lane # 0 1 0 1<br>TS1<br>Link # N N N+2 N+2<br>N N N+2 N+2 Link #<br>TS1<br>0 1 0 1 Lane #<br>0 1 1 0 步骤 5<br>（上游 （上游<br>Lane 反转<br>端口） 端口）<br>LTSSM LTSSM<br>**----- End of picture text -----**<br>


## **确认链路和 Lane 号。**

6. 下游端口接收具有通告的链路和 Lane 号的 TS1，因此每个端口独立地开始发送 TS2，作为通知它已准备好以协商的设置继续到 L0 状态。

**548**

**第 14 章：链路初始化与训练**

7. 上游端口接收没有链路和 Lane 号更改的 TS2，并开始以相同值发送回 TS2。

8. 一旦每个端口接收到至少 8 个 TS2 并发送至少 16 个 TS2，它将发送一些逻辑空闲数据，然后转换到 L0。右侧链路的上游端口正在内部实现 Lane 反转。

## **链路配置示例 3：失败的 Lane**

最后，让我们考虑一下其中一个 Lane 无法正常工作的情况。考虑上游端口的 Lane 2 无法正常工作的示例，如图 14‐21（第 550 页）所示。需要注意的是，Lane 并没有物理损坏，因为如果物理损坏，它将无法检测到接收器，也不会被考虑包含在链路中。但是，即使 Lane 已连接，上游端口的 Lane 2 的发送器或接收器（或两者）也无法完成工作。

在这种情况下，链路训练过程很可能需要更长的时间，因为大多数状态转换在所有 Lane 都准备好下一个状态之前等待继续到下一个状态，或者如果一部分 Lane 已准备好并且已发生超时条件。

以下步骤指示了在通过 Configuration 状态机的子状态转换时可以处理这种情况的方法。

## **链路号协商。**

9. 即使上游端口上的 Lane 2 接收器出现问题，下游端口也将在进入 Configuration 状态时采用相同的过程。下游端口在所有 Lane 上发送 TS1，链路号为 N，Lane 号设置为 PAD。

10. Lane 0、1 和 3 都接收了具有非 PAD 链路号的 TS1，因此这些 Lane 将 TS1 发送回下游端口。但是，上游端口的 Lane 2 未成功接收具有非 PAD 链路号的 TS1，因此其发送器继续发送 Link 和 Lane 号字段中带有 PAD 的 TS1，如图 14‐21（第 550 页）所示。

**549**

## **PCI Express Technology**

_图 14‐21：示例 3 — 步骤 1 和 2_

**==> picture [356 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>LTSSM<br>（下游端口）<br>0 1 2 3<br>步骤 1<br>Lane # PAD PAD PAD PAD<br>TS1<br>Link # N N N N<br>N N PAD N Link #<br>TS1<br>PAD PAD PAD PAD Lane #<br>0 1 2 3 步骤 2<br>LTSSM<br>（上游端口）<br>选项：一个链路 x4、x2 或 x1<br>**----- End of picture text -----**<br>


## **Lane 号协商。**

11. 一旦下游端口在 Lane 0、1 和 3 上接收到具有相同链路号的 TS1，它将等待所需的超时期望 Lane 2 开始工作。当这种情况没有发生时，下游端口意识到它只能训练为 x2 链路。在接受此事实后，下游端口将通告 Lane 0 和 1 的 Lane 号，但 Lane 2 和 3 返回以在 Link 和 Lane 号字段中发送 PAD。

12. 当上游端口在 Lane 0 和 1 上接收到具有通告的 Lane 号的 TS1，并且它看到 Lane 3 已返回到接收 PAD TS1 时，它通告 Lane 0 和 1 的 Lane 号，但所有其他 Lane 开始（或继续）在 Lane 和 Link 号字段中发送设置为 PAD 的 TS1，如图 14‐22（第 551 页）所示。

**550**

**第 14 章：链路初始化与训练**

_图 14‐22：示例 3 — 步骤 3 和 4_

**==> picture [356 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
选项：一个链路 x4、x2 或 x1<br>