任何复位后或由数据链路层<br>指示的初始状态<br>Disabled<br>Detect<br>训练状态<br>重新训练状态<br>外部<br>环回 电源管理状态<br>Polling<br>ASPM 状态<br>热<br>复位 其他状态<br>从<br>配置 从配置<br>或恢复<br>恢复<br>L2 恢复<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


## **LTSSM 状态概述**

以下是 11 个高级 LTSSM 状态的简要描述。

- **Detect**：复位后的初始状态。在此状态下，设备以电气方式检测链路远端是否存在接收器。这在串行传输世界中是不寻常的，但这样做是为了便于测试，我们将在下一个状态中看到。Detect 也可以从许多其他 LTSSM 状态进入，如后所述。

- **Polling**：在此状态下，发送器开始发送 TS1 和 TS2（以 2.5 GT/s 速度以实现向后兼容性），以便接收器可以使用它们完成以下操作：

   - 达到位锁定

   - 获取符号锁定或块锁定

   - 纠正 Lane 极性反转（如果需要）

   - 了解可用的 Lane 数据速率

**519**

**PCI Express Technology**

   - 如果有指示，启动合规测试序列：其工作方式是，如果在 Detect 状态中检测到接收器但未看到输入信号，则表明该设备已连接到测试负载。在这种情况下，它应发送指定的合规测试模式以方便测试。这允许测试设备快速验证电压、BER、时序和其他参数是否在容差范围内。

- **Configuration**：上游和下游组件现在在继续以 2.5 GT/s 交换 TS1 和 TS2 时扮演特定角色以完成以下操作：

   - 确定链路宽度

   - 分配 Lane 编号

   - 可选择检查 Lane 反转并纠正它

   - 去偏移 Lane 到 Lane 的时序差异

      - 从此状态，可以禁用加扰、可以进入 Disable 和 Loopback 状态，并且从 TS1 和 TS2 记录从 L0s 状态转换到 L0 状态所需的 FTS 有序集的数量。

- **L0**：这是链路的正常、完全活动状态，在此期间可以交换 TLP、DLLP 和有序集。在此状态下，链路可以以高于 2.5 GT/s 的速度运行，但只能通过重新训练（Recovery）链路并经过速度更改过程来实现。

- **Recovery**：当链路需要重新训练时进入此状态。这可能是由 L0 中的错误引起的，或从 L1 恢复到 L0，或从 L0s 恢复（如果链路未使用 FTS 序列正确训练）。在 Recovery 中，位锁定和符号/块锁定以与 Polling 状态中使用的方式类似的方式重新建立，但通常需要的时间要少得多。

- **L0s**：此 ASPM 状态旨在提供一些节能，同时提供快速恢复时间返回 L0。当一个发送器在 L0 状态时发送 EIOS 时进入。从 L0s 退出涉及发送 FTS 以快速重新获取位和符号/块锁定。

- **L1**：此状态通过权衡比 L0s 更长的恢复时间来提供更大的节能（参见第 735 页 "Active State Power Management (ASPM)"）。进入 L1 涉及两个链路伙伴之间的协商以共同进入，可以以两种方式之一发生：

   - 第一种是使用 ASPM 自动进行：上游端口中的硬件在未计划传输 TLP 或 DLLP 时可以自动协商将其链路置于 L1 状态。如果下游端口同意，则链路进入 L1。如果不同意，则上游端口将改为进入 L0s（如果启用）。

   - 第二种是电源管理软件发出命令将设备命令到低功耗状态（D1、D2 或 D3Hot）的结果。因此，上游端口通知下游端口它们必须进入 L1，下游端口确认这一点，然后它们进入 L1。

**520**

**第 14 章：链路初始化与训练**

- **L2**：在此状态下，设备的主电源被关闭以实现更大的节能。几乎所有的逻辑都关闭了，但仍有少量电源可从 Vaux 源获得，以允许设备指示唤醒事件。支持此唤醒能力的上游端口可以发送称为 Beacon 的非常低频的信号，下游端口可以将其转发到根复合体以获得系统注意（参见第 483 页 "Beacon Signaling"）。使用 Beacon 或边带 WAKE# 信号，设备可以触发系统唤醒事件以恢复主电源。[还定义了 L3 链路电源状态，但它与 LTSSM 状态无关。L3 状态是完全关闭的条件，其中 Vaux 电源不可用且无法发出唤醒事件。]

- **Loopback**：此状态用于测试，但接收器在此模式下的确切行为（例如：多少逻辑参与）未指定。基本操作足够简单：将作为 Loopback 主设备的设备发送训练控制字段中设置了 Loopback 位的 TS1 有序集到将作为 Loopback 从设备的设备。当设备看到两个连续的设置了 Loopback 位的 TS1 时，它作为 Loopback 从设备进入 Loopback 状态并回显传入的所有内容。主设备识别出它正在发送的内容现在正在被回显，发送遵循 8b/10b 编码规则的任何符号模式，从设备按发送时的确切方式回显它们，提供链路完整性的往返验证。

- **Disable**：此状态允许禁用已配置的链路。在此状态下，发送器处于电气空闲状态，而接收器处于低阻抗状态。这可能是必要的，因为链路变得不可靠或由于设备的意外移除。软件通过设置 Link Control 寄存器中的 Disable 位来命令设备执行此操作。然后设备发送 16 个 TS1，其中 TS1 训练控制字段中设置了 Disable Link 位。当接收器接收到这些 TS1 时，它们被禁用。

- **热复位**：软件可以通过设置 Bridge Control 寄存器中的 Secondary Bus Reset 位来复位链路。这会导致桥接器的下游端口发送 TS1，其中 TS1 训练控制字段中设置了 Hot Reset 位（参见第 837 页 "Hot Reset (In‐band Reset)"）。当接收器看到两个连续的设置了 Hot Reset 位的 TS1 时，它必须复位其设备。

## **介绍、示例和状态/子状态**

本章的其余部分涵盖了 LTSSM 的每个状态。根据给定状态的复杂性，讨论可能包括介绍、一般背景和/或伴随状态/子状态详细讨论的示例。在某些情况下，读者可以选择跳过详细覆盖并跳到介绍性材料。每个部分都组织得便于这些选项。

**521**

## **PCI Express Technology**

每个设备必须以 2.5 GT/s 的基本速率执行初始链路训练。图 14‐7 突出显示了初始训练序列中涉及的状态。能够在 5.0 或 8.0 GT/s 运行的设备必须转换到 Recovery 状态以将速度更改为所选择的较高速率。

_图 14‐7：以 2.5 Gb/s 进行初始链路训练所涉及的状态_

**==> picture [304 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
任何复位后或由数据链路层<br>指示的初始状态<br>Disabled<br>Detect<br>训练状态<br>重新训练状态<br>外部<br>环回 电源管理状态<br>Polling<br>ASPM 状态<br>热<br>复位 其他状态<br>从<br>配置 从配置<br>或恢复<br>恢复<br>L2 恢复<br>L1 L0 L0s<br>**----- End of picture text -----**<br>


## **Detect 状态**

## **介绍**

图 14‐8 表示与 Detect 状态相关联的两个子状态和转换。与 Detect 状态相关联的操作由每个

**522**

**第 14 章：链路初始化与训练**

发送器在检测链路对端接收器存在性的过程中执行。由于只有两个子状态并且它们相当简单，我们将直接进入子状态讨论。

_图 14‐8：Detect 状态机_

**==> picture [288 x 188] intentionally omitted <==**

**----- Start of picture text -----**<br>
从复位进入。<br>也从 Disabled、<br>Loopback、L2、Polling、<br>Configuration 或<br>Recovery 进入<br>链路上无电气<br>空闲或<br>12 ms 超时 检测到<br>接收器<br>Detect.Quiet Detect.Active<br>未检测到<br>12 ms 充电或<br>直流共模<br>电压稳定<br>退出到<br>Polling<br>**----- End of picture text -----**<br>


## **Detect 子状态详解**

## **Detect.Quiet**

此子状态是任何复位（功能级复位除外）或上电事件后的初始状态，必须在复位后 20 ms 内进入。如果无法前进，也会从其他状态进入此子状态（参见第 523 页图 14‐8 中可能进入 Detect.Quiet 的状态）。此子状态的属性如下所列：

- 发送器从电气空闲开始（但直流共模电压不必在正常指定的范围内）。

- 预期的数据速率设置为 2.5 GT/s (Gen1)。如果在进入此子状态时设置为其他速率，则 LTSSM 必须在此子状态中保持 1ms，然后再将速率更改为 Gen1。

- 物理层的状态位 (LinkUp = 0) 通知数据链路层链路未运行。LinkUp 状态位是一个内部状态位

**523**

## **PCI Express Technology**

- （在标准配置空间中找不到），还指示物理层何时完成链路训练（LinkUp=1），从而通知数据链路层和流控初始化开始其链路初始化部分（有关详细信息，请参见第 223 页 "The FC Initialization Sequence"）。

- • 通过将四个 Link Status 2 寄存器位设置为零来清除任何先前的均衡（Eq.）状态：Eq. Phase 1 Successful、Eq. Phase 2 Successful、Eq. Phase 3 Successful、Eq. Complete。

- 变量：

   - 几个变量被清零：(directed_speed_change=0b, upconfigure_capable=0b, equalization_done_8GT_data_rate=0b, idle_to_rlock_transitioned=00h)。select_deemphasis 变量设置取决于端口类型：对于上游端口，由硬件选择，而对于下游端口，它采用 Link Control 2 寄存器中 Selectable Preset/De‐emphasis 字段的值。

   - 由于这些变量是从 2.0 规范版本开始定义的，为早期规范版本设计的设备将没有这些变量，并将表现得好像 directed_speed_change 和 upconfigure_capable 设置为 0b 且 idle_to_rlock_transitioned 设置为 FFh。

## _退出到 "Detect.Active"_

下一个子状态是 Detect.Quiet，经过 12 ms 超时后或当任何 Lane 退出电气空闲时。

## **Detect.Active**

此子状态从 Detect.Quiet 进入。此时发送器通过设置合法范围内的任何值的直流共模电压然后更改它来测试每个 Lane 上是否连接了接收器。检测逻辑观察变化率，即线路电压充电所用的时间，并将其与预期时间进行比较，例如没有接收器终端时所需的时间。如果连接了接收器，充电时间将更长，从而易于识别。有关此过程的更多详细信息，请参见第 460 页 "Receiver Detection"。为简化后续讨论，在此子状态期间检测到接收器的 Lane 称为"已检测 Lane"。

## _退出到 "Detect.Quiet"_