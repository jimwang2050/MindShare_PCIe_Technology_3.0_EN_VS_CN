- 如果没有 Lane 检测到接收器，则返回到 Detect.Quiet。它们之间的循环每 12ms 重复一次，只要没有检测到接收器。

## _退出至"Polling 状态"_

- 如果在所有 Lane 上都检测到接收器，则下一个状态将是 Polling。Lane 现在必须在 0 至 3.6 V VTX‐CM‐DC 规范内驱动直流共模电压。

## _特殊情况：_

如果设备的一些但不是所有 Lane 连接到接收器（例如 x4

**524**

**第 14 章：链路初始化与训练**

设备连接到 x2 设备），则等待 12 ms 并重试。如果相同的 Lane 在第二次时检测到接收器，则退出到 Polling 状态，否则返回到 Detect.Quiet。如果转到 Polling，对于未看到接收器的 Lane 有两种可能性：

1. 如果 Lane 可以作为单独的链路运行（请参阅第 541 页的"设计具有可合并链路的设备"），请使用另一个 LTSSM 并让这些 Lane 重复检测序列。

2. 如果另一个 LTSSM 不可用，则未检测到接收器的 Lane 将不属于该链路的一部分，并且必须转换为电气空闲 (Electrical Idle)。

## **Polling 状态**

## **简介**

到此为止，链路一直处于电气空闲状态，然而在 Polling 期间，LTSSM TS1 和 TS2 在两个连接的设备之间交换。此状态的主要目的是让两个设备理解彼此的通信内容。换句话说，它们需要在彼此传输的比特流上建立位和符号锁定 (bit and symbol lock)，并解决任何极性反转问题。一旦完成此操作，每个设备都成功地接收来自其链路伙伴的 TS1 和 TS2 有序集。第 525 页图 14-9 显示了 Polling 状态机的子状态。

_图 14-9：Polling 状态机_

**==> picture [339 x 181] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Detect<br>Entry from<br>Detect<br>24 ms<br>48 ms<br>Exchange<br>1024 TS1s<br>(unless directed Polling.Active Polling.Configuration<br>to Compliance) Bit/Symbol Lock (Polarity Inversion)<br>Directed or<br>Insufficient Lanes Electrical 8 TS1, TS2 (or complement) Rx on ALL 8 TS2 Rx. 16 TS2 Tx.<br>Lanes or 24 ms timeout and ANY<br>detect Idle Exit<br>exit from Electrical Idle Lane Rx 8 TS1, TS2 and ALL Lanes<br>detect exit from Electrical Idle<br>Exit to<br>Polling.Compliance Configuration<br>**----- End of picture text -----**


**525**

**PCI Express 技术**

## **详细的 Polling 子状态**

## **Polling.Active**

## _在 Polling.Active 期间_

一旦其共模电压稳定在 Transmit Margin 字段指定的水平上，发送器将在所有检测到的 Lane 上发送最少 1024 个连续的 TS1。两个链路伙伴可以在不同时间退出 Detect 状态，因此 TS1 交换未同步。在 Gen1 速度 (2.5 GT/s) 下发送 1024 个 TS1 所需的时间为 64μs。

关于此子状态的一些注意事项：

- PAD 符号必须用于 TS1 的 Lane 和 Link Number 字段中。

- 必须通告设备支持的所有数据速率，即使它不打算使用全部。

- 接收器使用传入的 TS1 获得位锁定 (Bit Lock)（请参阅第 395 页的"实现位锁定"），然后对于较低速率为符号锁定 (Symbol Lock)（请参阅第 396 页的"实现符号锁定"），或者对于 8.0 GT/s 为块对齐 (Block Alignment)（请参阅第 438 页的"实现块对齐"）。

## _退出至"Polling.Configuration"_

- 如果在发送至少 1024 个 TS1 之后，**所有**检测到的 Lane 收到 8 个连续的训练序列（或其补码，由于极性反转），满足以下条件之一，则下一个状态为 Polling.Configuration：

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Compliance Receive 位清零为 0b (Symbol 5 的位 4)。

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Symbol 5 的 Loopback 位置为 1b。

- 

- 接收到 Link 和 Lane 设置为 PAD 的 TS2。

如果以上条件均不满足，则在 24ms 超时后，如果在收到 TS1 后已发送至少 1024 个 TS1，并且**任何**检测到的 Lane 收到 8 个连续的 TS1 或 TS2 有序集（或其补码），其 Lane 和 Link 号设置为 PAD，并且以下之一为真：

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Compliance Receive (Symbol 5 的位 4) 清零为 0b。

- 接收到 Link 和 Lane 设置为 PAD 的 TS1，且 Loopback (Symbol 5 的位 2) 置为 1b。

- 接收到 Link 和 Lane 设置为 PAD 的 TS2。

**526**

**第 14 章：链路初始化与训练**

如果以上条件仍然不满足，则如果至少预定数量的检测 Lane 也检测到自进入 Polling.Active 以来至少一次退出电气空闲（这可以防止一个或多个有问题的发送器或接收器阻碍链路配置）。预定 Lane 的确切集合现在是特定于实现的，这是相对于 1.1 规范的更改，后者需要查看所有检测到的 Lane 上的电气空闲退出。

## _退出至"Polling.Compliance"_

如果 Link Control 2 寄存器中的 Enter Compliance 位置为 1b，或者如果该位在进入 Polling.Active 之前已置位，则转换到 Polling.Compliance 必须是即时的，并且在 Polling.Active 中不发送 TS1。

否则，在 24ms 超时后，如果：

- 预定集合中的所有 Lane 自进入 Polling.Active 以来未观察到退出电气空闲（表明存在被动测试负载，例如至少一个 Lane 上的电阻迫使所有 Lane 进入 Poll‐ ing.Compliance）。

- 任何检测到的 Lane 收到 8 个连续的 TS1（或其补码），其 Link 和 Lane 号设置为 PAD，Symbol 5 的 Compliance Receive 位置为 1b 且 Loopback 位清零为 0b。

## _退出至"Detect 状态"_

- 如果在 24ms 后，未满足转到 Polling.Configuration 或 Poll‐ ing.Compliance 的条件，则返回到 Detect 状态。

## **Polling.Configuration**

在此子状态下，发送器将停止发送 TS1 并开始发送 TS2，Link 和 Lane 号仍设置为 PAD。更改为发送 TS2 而不是 TS1 的目的是向链路伙伴通告此设备已准备好进入状态机中的下一状态。这是一种握手机制，以确保链路上的两个设备一起通过 LTSSM 前进。在两个设备都准备好之前，任何设备都不能进入下一状态。它们通过发送 TS2 有序集来通告它们已准备好。因此，一旦设备同时发送并接收 TS2，它就知道可以进入下一状态，因为它已准备好且其链路伙伴也已准备好。

## _在 Polling.Configuration 期间_

- 发送器在所有检测到的 Lane 上发送 Link 和 Lane 号设置为 PAD 的 TS2，并且必须通告其支持的所有数据速率，即使它不打算使用。此外，每个 Lane 的接收器必须根据需要独立反转其差分输入对的极性。有关如何完成此操作的说明，请参阅第 506 页的"概述"。Transmit Margin 字段必须重置为 000b。

**527**

## **PCI Express 技术**

## _退出至"Configuration 状态"_

在任何检测到的 Lane 上收到 8 个连续的 Link 和 Lane 设置为 PAD 的 TS2，并且自收到一个 TS2 以来已发送至少 16 个 TS2 之后，退出到 Configuration。

## _退出至"Detect 状态"_

否则，在 48ms 超时后退出到 Detect。

## _退出至 Polling.Speed（不存在的子状态）_

作为历史回顾，自规范 1.0 版本发布以来，Polling 的子状态已发生变化。当时认为，当其他速度可用时，应尽快在此状态下更改为最高可用速率。然而，更高速度的出现恰好伴随着这样的认识：在运行时出于电源管理原因同时更改更高和更低速度将是有利的。通过 Polling 状态涉及清除许多链路值，这使其成为运行时使用的不具吸引力的路径，因此速率更改阶段已从该状态移出到 Recovery 状态。请参阅第 528 页图 14-10。

_图 14-10：具有旧式速度更改的 Polling 状态机_

**==> picture [355 x 186] intentionally omitted <==**

**----- Start of picture text -----**<br>
Exit to<br>Detect<br>Entry from<br>Detect<br>24 ms<br>Speed change step was<br>48 ms moved from this state to<br>Exchange Recovery state<br>1024 TS1s Polling.Speed<br>(unless directed Polling.Active Polling.Configuration (E lect ri c a l Idle ,<br>to Compliance) Bit/Symbol Lock (Polarity Inversion) Ch a ng e Spee d)<br>Directed or<br>Insufficient Lanes Electrical 8 TS1, TS2 (or complement) Rx on ALLLanes or 24 ms timeout and ANY 8 TS2 Rx. 16 TS2 Tx.<br>detect Idle Exit<br>exit from Electrical Idle Lane Rx 8 TS1, TS2 and ALL Lanes<br>detect exit from Electrical Idle<br>Exit to<br>Polling.Compliance Configuration<br>**----- End of picture text -----**


如今，链路在复位后始终训练到 2.5 GT/s，即使其他速度可用。如果在 LTSSM 达到 L0 后有更高速率可用，则它转换到 Recovery 并尝试更改为最高共同支持或通告的速率。支持的速度在交换的 TS1 中报告。

**528**

**第 14 章：链路初始化与训练**

和 TS2，以便任一设备随后都可以通过转换到 Recovery 状态来决定发起速度更改。规范仍列出此子状态，但声明它现在不可达。

## **Polling.Compliance**

此子状态仅用于测试，并导致发送器发送旨在产生接近最坏情况的符号间干扰 (Inter‐Symbol Interference, ISI) 和串扰条件的特定模式，以促进对链路的分析。在此子状态下可以发送两种不同的模式：Compliance Pattern 和 Modified Compliance Pattern。

**8b/10b 的合规模式。** 此模式由按顺序重复的 4 个符号组成：K28.5‐、D21.5+、K28.5+ 和 D10.2‐，其中 (‐) 表示负电流运行差异 (CRD)，(+) 表示正 CRD（由于强制 CRD，模式开头可以存在差异错误）。如果链路有多个 Lane，则四个延迟符号（显示为 D，但实际上只是其他 K28.5 符号）被注入到 Lane 0 上，在下一个合规模式之前两个，在合规模式之后两个。最后一个延迟符号在 Lane 0 上发送后，四个延迟符号也在 Lane 1 上发送（同样，在下一个合规模式之前两个，在之后两个）。此过程继续进行，直到延迟符号传播通过 Lane 7。然后它们返回到从 Lane 0 重新开始，如第 529 页表 14-3 所示（合规模式以灰色阴影显示）。每组八个 Lane 都以这种方式表现。移动延迟符号将确保相邻 Lane 之间的干扰，并提供更好的测试条件。

_表 14-3：8b/10b 合规模式的符号序列_

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
|---|---|---|---|---|---|
|0|D|K28.5‐|K28.5‐||D|
|1|D|K21.5|K21.5||D|
|2|K28.5‐|K28.5+|K28.5+||K28.5‐|
|3|K21.5|D10.2|D10.2||K21.5|
|4|K28.5+|K28.5‐|K28.5‐||K28.5+|
|5|D10.2|K21.5|K21.5||D10.2|



**529**

## **PCI Express 技术**

_表 14-3：8b/10b 合规模式的符号序列（续）_

|**Symbol**|**Lane 0**|**Lane 1**|**Lane 2**|**...**|**Lane 8**|
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
