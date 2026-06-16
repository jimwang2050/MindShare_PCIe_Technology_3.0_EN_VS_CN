OBFF 是一个可选的提示，系统可以使用它来通知组件关于流量的最佳时间窗口。然而，它只是一个提示，因此能够进行总线主控的设备仍然可以随时发起流量。当然，如果它们这样做，功耗将受到负面影响，因此应尽可能避免覆盖 OBFF 提示。信息通过以下两种方式之一传达：通过向端点发送消息或通过切换 WAKE# 引脚。如果两种选择都可用，则强烈建议使用引脚，因为它避免了使用过多功率的反向步骤——可能跨多条 Link 来通知组件当前系统电源状态。事实上，仅当 WAKE# 引脚不可用时才应使用 OBFF 消息。

第 778 页的图 16-33 给出了一个混合使用两种通信类型的示例。如果 WAKE# 引脚可用，则必须使用，但在本例中，两台交换机之间没有该选项。为了解决此问题，上游交换机可以将 WAKE# 引脚上接收到的状态转换为向下游发送的消息。这里也许应该指出，强烈鼓励交换机将所有 OBFF 指示转发到下游，但不要求这样做。可能有必要，特别是在使用消息时，丢弃或合并某些指示，这是允许的。

_图 16-33：OBFF 信令示例_

**==> picture [207 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>
WAKE#<br>
Endpoint<br>
Switch<br>
Endpoint<br>
OBFF<br>
Message<br>
Endpoint<br>
WAKE# Switch<br>
Endpoint Endpoint<br>
**----- End of picture text -----**<br>


**778**

**第 16 章：电源管理**

**使用 WAKE# 引脚。** 该引脚先前仅用于通知系统组件需要恢复电源，现在又被赋予了额外的含义，作为向 PCIe 组件传达系统电源状态的最简单、最低功耗的选项。它是可选的，协议相当简单：WAKE# 引脚切换以传达系统状态。如第 779 页的图 16-34 所示，存在多个转换但只有三个状态，描述如下：

1. CPU Active（CPU 活动）— 系统唤醒；所有事务 OK。这是每个组件的初始状态。

2. OBFF — 系统内存路径可用；与内存之间的传输 OK，但其他事务应等待更高的电源状态。

3. Idle（空闲）— 在发起之前等待更高的状态。

_图 16-34：WAKE# 引脚 OBFF 信令_

**==> picture [382 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transition Event OBFF Message Code<br>
Idle OBFF OBFF<br>
Idle CPU Active CPU Active<br>
OBFF or CPU Active Idle Idle<br>
OBFF CPU Active CPU Active<br>
CPU Active               OBFF OBFF<br>
**----- End of picture text -----**<br>


当指示 CPU Active 或 OBFF 状态时，建议平台至少 10μs 后不要返回到 Idle 状态，以便为组件提供足够的时间来传递它们可能在先前 Idle 状态期间排队的包。然而，由于不需要该时序，也建议端点不要假设它们将在 CPU Active 或 OBFF 窗口中拥有一定的时间。同样，平台被允许在实际进入 Idle 之前指示它将进入 Idle

**779**

## **PCI Ex ress Technolo p gy**

以便提前通知组件是时候完成了。设计此提前通知具体要避免的情况是：端点恰好在平台进入 Idle 时开始传输，导致立即退出 Idle 状态。规范强烈建议这应该是提前指示 Idle 状态的唯一原因，并且此提前通知时间应尽可能短。

有趣的是，WAKE# 引脚仍然可以用于其原始目的，即允许组件唤醒系统，并且毫不奇怪，这可能会使正在监视该引脚以获取 OBFF 信息的其他组件感到困惑。这可能导致电源或性能方面的次优行为，但这种情况被认为是可恢复的，因此没有采取任何措施来防范它。为了涵盖所有这些情况，每当信号不清楚时，默认状态将是 CPU Active。

**使用 OBFF 消息。** 如前所述，OBFF 信息可以使用消息来传达，但建议仅在 WAKE# 引脚不可用时使用。这些消息仅从根向下游流动。消息内容如图 16-35（第 781 页）所示，包括路由类型 100b（点对点）以及给出以下值的 OBFF 代码（所有其他代码保留）：

1. 1111b — CPU Active

2. 0001b — OBFF

3. 0000b — Idle

如果收到保留代码，组件必须将其视为"CPU Active"。如果端口收到 OBFF 消息但不支持 OBFF 或尚未启用 OBFF，则必须将其视为不支持的请求（完成状态 UR）。

**780**

**第 16 章：电源管理**

_图 16-35：OBFF 消息内容_

**==> picture [359 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>
0 0 1 1 0  1 0 0 tr H D P<br>
Message Code<br>
Byte 4 Requester ID Tag 0001 0010<br>
Byte 8 Reserved for Error Messages<br>
OBFF<br>
Byte 12 Reserved for Error Messages Code<br>
Point-to-Point 0000b = Idle<br>
0001b = OBFF<br>
1111b  =  CPU Active<br>
**----- End of picture text -----**<br>


通过 Device Capability 2 寄存器（图 16-36，第 782 页）指示 OBFF 支持，并通过 Device Control 2 寄存器（图 16-37，第 783 页）启用 OBFF。请注意，引脚和消息选项都可能可用。但是，首选引脚方法，因为它是较低功耗的选项。

注意，启用组件以转发 OBFF 消息有两种变体，它们之间的区别在于处理不在 L0 中的目标 Link。在变体 A 中，仅当 Link 处于 L0 时才会发送消息。如果不是，则简单地丢弃该消息以避免唤醒 Link 的成本。当下面的设备预期没有时间紧迫的通信要求并可以通过简单地将 Link 返回到 L0 来指示其对非紧急关注的需要时，对于下游端口而言这是优选的。对于变体 B，消息将始终被转发，并且 Link 将返回到 L0。当下游设备可以从平台状态的及时通知中受益时，此变体是优选的。

**781**

## _图 16-36：OBFF 支持指示_

**==> picture [364 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capability 2 Register<br>
31 24  23  22  21  20  19 18 14  13   12  11  10  9  8   7  6  5  4  3        0<br>
[eee] o vem<br>
RsvdP RsvdP<br>
[eee] “ TET<br>
Za<br>
See om [os] ||<br>
eee] os Max End-End<br>
TLP Prefixes<br>
om<br>
ede End-End TLP<br>
ow Prefix Supported<br>
owno Extended Fmt<br>
ow Field Supported<br>
ow<br>
TPH Completer Supported<br>
[see omJo LTR Mechanism Supported<br>
No RO-enabled PR-PR Passing<br>
128-bit CAS Completer Supported<br>
OBFF Support<br>
64-bit AtomicOp Completer Supported<br>
00 – Not supported 32-bit AtomicOp Completer Supported<br>
AtomicOp Routing Supported<br>
01 – Message only<br>
ARI Forwarding Supported<br>
10 – WAKE# only<br>
Completion Timeout Disable Supported<br>
11 – Both Completion Timeout Ranges Supported<br>
**----- End of picture text -----**<br>


当使用 WAKE# 时，启用任何根端口来断言它被视为全局启用，除非有多个 WAKE# 信号，在这种情况下，只有与该端口相关的那些信号才会受到影响。当使用 OBFF 消息时，仅启用根端口仅在该端口上启用消息。规范中的期望是：如果任何根端口被启用，则通常所有根端口都会被启用，以确保整个平台都已启用。但是，允许有选择地启用某些端口而不启用其他端口。

启用 OBFF 端口时，规范建议先启用所有上游端口，然后再启用下游端口，并最后启用根端口。对于未填充的热插拔插槽，这是不可能的。对于这种情况，允许使用插槽的 WAKE# 引脚启用 OBFF，但建议不要启用插槽上方下游端口以传送 OBFF 消息。

**第 16 章：电源管理**

## _图 16-37：OBFF 启用寄存器_

**==> picture [236 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Control 2 Register<br>
15  14  13 11  10  9  8   7  6  5  4  3        0<br>
RsvdP<br>
End-End TLP Prefix Blocking<br>
LTR Mechanism Enable<br>
IDO Completion Enable<br>
IDO Request Enable<br>
AtomicOp Egress Blocking<br>
AtomicOp Requester Enable<br>
ARI Forwarding Enable<br>
Completion Timeout Disable<br>
Completion Timeout Value<br>
OBFF Enable<br>
00 – Disabled<br>
01 – Enabled with Message signaling Variation A<br>
10 – Enabled with Message signaling Variation B<br>
11 – Enabled using WAKE# signaling<br>
**----- End of picture text -----**<br>


最后，让我们回到第 778 页图 16-33 中的早期示例，以考虑这些寄存器在该情况下可能是什么样子。连接到下交换机的交换机的下游端口的 OBFF Support 值为 01b — 仅消息，而其上游端口的值可能为 11b — 两者。这些值可能被硬编码到设备中或以其他方式由硬件初始化，以使其在复位后对软件可见。下游端口需要具有 01b 或 10b 的 OBFF Enable 值 — 启用了消息变体 A 或 B，以便它可以传递 OBFF 消息。上游端口将期望具有 11b 的 OBFF Enable 值 — 启用了 WAKE# 信令。规范指出，当交换机配置为从一个端口到另一个端口使用不同的方法时，需要进行翻译并转发指示。

**783**

**PCI Ex ress Technolo p gy**

## **LTR（延迟容忍报告）**

为提高 PM 效率而添加的第二个新特性称为延迟容忍报告（Latency Tolerance Reporting, LTR）。此可选功能允许设备在从平台请求服务时报告它们可容忍的延迟，以便像主存这样的平台资源的 PM 策略可以考虑这一点。如果软件支持，则当设备需要时提供良好的性能，而当它们不需要快速响应时则降低系统功耗。使用此信息的一个简单方法是允许系统在仍然满足延迟容忍度的情况下，推迟唤醒以服务请求。

规范中并未明确说明"延迟容忍"的含义，但提到了可能起作用的某些事项。例如，延迟容忍可能影响可接受的性能，或者可能影响组件是否能够正常运行。显然，这样的区别在设计 PM 策略时会产生很大的不同。同样，设备可以使用缓冲或其他技术来补偿延迟敏感性，了解这一点对于软件来说将是有用的。

## **LTR 寄存器**
