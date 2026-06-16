- 如果没有 Lane 检测到接收器，则返回 Detect.Quiet。只要未检测到接收器，它们之间的循环每 12ms 重复一次。

## _退出到 "Polling 状态"_

- 如果在所有 Lane 上都检测到接收器，则下一个状态将是 Polling。Lane 现在必须在 0 ‐ 3.6 V VTX‐CM‐DC 规格范围内驱动直流共模电压。

## _特殊情况：_

如果设备的部分（但不是全部）Lane 连接到接收器（如 x4

**524**

**第 14 章：链路初始化与训练**

设备连接到 x2 设备），则等待 12 ms 并重试。如果相同的 Lane 在第二次检测到接收器，则退出到 Polling 状态，否则返回 Detect.Quiet。如果转到 Polling，则对于未看到接收器的 Lane 有两种可能性：

1. 如果 Lane 可以作为单独的链路运行（参见第 541 页 "Designing Devices with Links that can be Merged"），使用另一个 LTSSM 并让那些 Lane 重复检测序列。

2. 如果没有其他 LTSSM 可用，则未检测到接收器的 Lane 将不是链路的一部分，必须转换到电气空闲。

## **Polling 状态**

## **介绍**

到目前为止，链路一直处于电气空闲状态，但是在 Polling 期间，LTSSM TS1 和 TS2 在两个连接的设备之间交换。此状态的主要目的是让两个设备理解彼此在说什么。换句话说，他们需要在彼此传输的位流上建立位和符号锁定，并解决任何极性反转问题。一旦完成，每个设备都成功地接收来自其链路伙伴的 TS1 和 TS2 有序集。第 525 页的图 14‐9 显示了 Polling 状态机的子状态。

_图 14‐9：Polling 状态机_

**==> picture [339 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
退出到<br>Detect<br>从 Detect<br>进入<br>24 ms<br>48 ms<br>交换<br>1024 TS1<br>（除非指示 Polling.Active Polling.Configuration<br>为合规） 位/符号锁定（极性反转）<br>指示或<br>Lane 不足 电气 8 个 TS1，TS2（或补码）Rx 在所有 8 个 TS2 Rx。16 个 TS2 Tx。<br>检测 空闲 退出 和任意<br>退出电气空闲 Lane Rx 8 个 TS1，TS2 和所有 Lane<br>检测 退出电气空闲<br>退出到<br>Polling.Compliance Configuration<br>**----- End of picture text -----**<br>


**525**

**PCI Express Technology**

## **Polling 子状态详解**

## **Polling.Active**

## _在 Polling.Active 期间_

一旦其共模电压稳定在 Transmit Margin 字段指定的电平，发送器在所有检测到的 Lane 上发送至少 1024 个连续的 TS1。两个链路伙伴可以在不同时间退出 Detect 状态，因此 TS1 交换未同步。以 Gen1 速度（2.5 GT/s）发送 1024 个 TS1 所需的时间为 64μs。

关于此子状态的一些注意事项：

- TS1 的 Lane 和 Link Number 字段中必须使用 PAD 符号。

- 必须通告设备支持的所有数据速率，即使它不打算使用所有速率。

- 接收器使用传入的 TS1 获取位锁定（参见第 395 页 "Achieving Bit Lock"），然后对于较低速率获取符号锁定（参见第 396 页 "Achieving Symbol Lock"），或者对于 8.0 GT/s 获取块对齐（参见第 438 页 "Achieving Block Alignment"）。

## _退出到 "Polling.Configuration"_

- 下一个状态是 Polling.Configuration，如果在发送至少 1024 个 TS1 之后，**所有**检测到的 Lane 接收到 8 个连续的训练序列（或其补码，由于极性反转），满足以下条件之一：

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，Compliance Receive 位清零为 0b（符号 5 的位 4）。

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，符号 5 的 Loopback 位设置为 1b。

-

- 接收到的 TS2 的 Link 和 Lane 设置为 PAD。

如果上述条件未满足，则在 24ms 超时后，如果在接收到 TS1 后发送了至少 1024 个 TS1，并且**任意**检测到的 Lane 接收到八个连续的 TS1 或 TS2 有序集（或其补码），其 Lane 和 Link 编号设置为 PAD，并且以下条件之一为真：

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，Compliance Receive（符号 5 的位 4）清零为 0b。

- 接收到的 TS1 的 Link 和 Lane 设置为 PAD，Loopback（符号 5 的位 2）设置为 1b。

- 接收到的 TS2 的 Link 和 Lane 设置为 PAD。

**526**

**第 14 章：链路初始化与训练**

如果仍然不满足上述条件，则如果至少预定数量的检测到的 Lane 也自进入 Polling.Active 以来至少检测到一次电气空闲退出（这可防止一个或多个不良发送器或接收器阻碍链路配置）。准确的预定 Lane 集是特定于实现的，这是相对于 1.1 规范的变化，该规范需要在所有检测到的 Lane 上看到电气空闲退出。

## _退出到 "Polling.Compliance"_

如果 Link Control 2 寄存器中的 Enter Compliance 位设置为 1b，或者如果在进入 Polling.Active 之前设置了此位，则更改到 Polling.Compliance 必须是立即的，并且在 Polling.Active 中不发送 TS1。

否则，在 24ms 超时后，如果：

- 自进入 Polling.Active 以来，预定集中的所有 Lane 都未看到电气空闲退出（表示被动测试负载，例如至少一个 Lane 上的电阻器，迫使所有 Lane 进入 Polling.Compliance）。

- 任何检测到的 Lane 接收到 8 个连续的 TS1（或其补码），其 Link 和 Lane 编号设置为 PAD，符号 5 的 Compliance Receive 位设置为 1b 且 Loopback 位清零为 0b。

## _退出到 "Detect 状态"_

- 如果 24ms 后，转到 Polling.Configuration 或 Polling.Compliance 的条件未满足，则返回 Detect 状态。

## **Polling.Configuration**

在此子状态中，发送器将停止发送 TS1 并开始发送 TS2，Link 和 Lane 编号仍设置为 PAD。更改为发送 TS2 而不是 TS1 的目的是向链路伙伴通告此设备已准备好继续状态机中的下一个状态。这是一种握手机制，以确保链路上的两个设备一起通过 LTSSM。在两个设备都准备好之前，任何一个设备都不能继续到下一个状态。他们通过发送 TS2 有序集来通告他们已准备好。因此，一旦设备既发送又接收 TS2，它就知道它可以继续到下一个状态，因为它已准备好，其链路伙伴也已准备好。

## _在 Polling.Configuration 期间_

- 发送器在所有检测到的 Lane 上发送 Link 和 Lane 编号设置为 PAD 的 TS2，并且必须通告它们支持的所有数据速率，即使它们不打算使用。此外，每个 Lane 的接收器必须在必要时独立反转其差分输入对的极性。有关如何执行此操作的说明，请参见第 506 页 "Overview"。Transmit Margin 字段必须重置为 000b。

**527**

## **PCI Express Technology**

## _退出到 "Configuration 状态"_

在任何检测到的 Lane 上接收到八个连续的 Link 和 Lane 设置为 PAD 的 TS2，并且自接收到一个 TS2 起已发送至少 16 个 TS2 之后，退出到 Configuration。

## _退出到 "Detect 状态"_

否则，在 48ms 超时后退出到 Detect。

## _退出到 Polling.Speed（不存在的子状态）_

作为历史回顾，Polling 的子状态自规范的 1.0 版本发布以来已发生变化。当时认为当其他速度可用时，尽快在此状态下更改为最高可用速率是有意义的。然而，更高速度的出现恰好与意识到能够出于电源管理原因在运行时向上和向下更改速度将是有利的认识相吻合。通过 Polling 状态涉及清除许多链路值，这使其成为运行时使用的一条没有吸引力的路径，因此速率更改阶段从该状态移出到 Recovery 状态。参见第 528 页的图 14‐10。

_图 14‐10：具有传统速度更改的 Polling 状态机_

**==> picture [355 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
退出到<br>Detect<br>从 Detect<br>进入<br>24 ms<br>速度更改步骤从<br>48 ms 此状态移至<br>交换 Recovery 状态<br>1024 TS1 Polling.Speed<br>（除非指示 Polling.Active Polling.Configuration （电气空闲、<br>为合规） 位/符号锁定（极性反转） 更改速度）<br>指示或<br>Lane 不足 电气 8 个 TS1，TS2（或补码）Rx 在所有 8 个 TS2 Rx。16 个 TS2 Tx。<br>检测 空闲 退出 或 24 ms 超时 和任意<br>退出电气空闲 Lane Rx 8 个 TS1，TS2 和所有 Lane<br>检测 退出电气空闲<br>退出到<br>Polling.Compliance Configuration<br>**----- End of picture text -----**<br>


如今，复位后链路始终训练到 2.5 GT/s，即使其他速度可用。如果 LTSSM 达到 L0 后有更高的速度可用，则它转换到 Recovery 并尝试更改为最高共同支持或通告的速率。支持的速度在交换的 TS1 中报告

**528**

**第 14 章：链路初始化与训练**

和 TS2，以便任一设备随后可以决定通过转换到 Recovery 状态来启动速度更改。规范仍然列出此子状态但声明它是不可达的。

## **Polling.Compliance**

此子状态仅用于测试，并使发送器发送旨在创建接近最坏情况的符号间干扰 (ISI) 和串扰条件的特定模式以便于链路分析。在此子状态中可以发送两种不同的模式，即合规模式和修改的合规模式。

**8b/10b 的合规模式。** 此模式由按顺序重复的 4 个符号组成：K28.5‐、D21.5+、K28.5+ 和 D10.2‐，其中（‐）表示负电流差或 CRD，（+）表示正 CRD（由于 CRD 是强制的，因此允许在模式开头存在差异错误）。如果链路具有多个 Lane，则四个延迟符号（在表中显示为 D，但实际上只是额外的 K28.5 符号）被注入到 Lane 0 上，两个在下一个合规模式之前，两个在之后。一旦 Lane 0 上发送了最后一个延迟符号，则四个延迟符号也在 Lane 1 上发送（同样，两个在下一个合规模式之前，两个在之后）。此过程继续进行，直到延迟符号传播通过 Lane 7。然后它们回到 Lane 0 重新开始，如第 529 页表 14‐3 所示（合规模式以灰色阴影显示）。每八个 Lane 的组都是这样的行为。移动延迟符号将确保相邻 Lane 之间的干扰并提供更好的测试条件。

_表 14‐3：8b/10b 合规模式的符号序列_

|**符号**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|



**529**

## **PCI Express Technology**

_表 14‐3：8b/10b 合规模式的符号序列（续）_

|**符号**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|6|D|K28.5+|K28.5+||D|
|7|D|D10.2|D10.2||D|
|8|K28.5‐|D|K28.5‐||K28.5‐|
|9|K21.5|D|K21.5||K21.5|
|10|K28.5+|K28.5‐|K28.5+||K28.5+|
|...|...|...|...||...|
|16|K28.5‐|K28.5‐|D||K28.5‐|
|17|K21.5|K21.5|D||K21.5|
|18|K28.5+|K28.5+|K28.5‐||K28.5+|



**128b/130b 的合规模式。** 此模式由以下 36 个块的重复序列组成：