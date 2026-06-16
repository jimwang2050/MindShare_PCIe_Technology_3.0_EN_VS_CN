设备中的 LTR 能力通过 PCIe Device Capability 2 寄存器中的一位来发现，如图 16-38（第 785 页）所示，并在 Device Control 2 寄存器中启用，如图 16-39（第 785 页）所示。规范还规定了启用 LTR 的序列：必须先启用最接近根的设备，然后向下到端点。除非关联的根端口和所有中间交换机也支持 LTR 并已启用以服务它，否则不得启用端点。某些端点支持 LTR 而其他端点不支持是允许的。如果根端口或交换机下游端口收到 LTR 消息但不支持它或尚未启用它，则该消息必须被视为不支持的请求。建议端点在启用后不久发送 LTR 消息。强烈建议端点在任何 500μs 期间内发送的 LTR 消息不超过两条，除非规范要求。但是，如果它们这样做了，下游端口必须正确处理它们，并且不应基于此产生错误。

**784**

**第 16 章：电源管理**

## _图 16-38：LTR 能力状态_

**==> picture [235 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capability 2 Register<br>
31 24  23  22  21  20  19  18 14  13   12  11  10  9  8   7  6  5  4  3        0<br>
RsvdP RsvdP<br>
Max End-End<br>
TLP Prefixes<br>
End-End TLP<br>
Prefix Supported<br>
Extended Fmt<br>
Field Supported<br>
TPH Completer Supported<br>
LTR Mechanism Supported<br>
O<br>
**----- End of picture text -----**<br>


_Figure 16-39: LTR Enable_

**==> picture [218 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Control 2 Register<br>
15  14  13         11  10  9  8   7  6  5  4  3        0<br>
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
**----- End of picture text -----**<br>


LTR 信息的目标是根复合体 (Root Complex)。参与的下游设备都会报告其值，但端口仅使用所报告的最小值作为通过该端口访问的所有设备的延迟限制。根不需要遵守请求的服务延迟，但强烈鼓励这样做。

**785**

**PCI Ex ress Technolo p gy**

## **LTR 消息**

LTR 消息本身具有图 16-40（第 788 页）所示的格式，从图中可以看出，路由类型 100b（点对点）以及 LTR 消息代码为 0001 0000b。报告两个延迟值，一个用于必须侦听的请求，另一个用于不会被侦听因此应更快完成的请求。从图中可以看出，两者的格式相同，并包括以下字段：

- 延迟值和比例 — 组合给出范围从 1ns 到约 34 秒的值。将这些字段设置为全零表示任何延迟都会影响设备，因此请求最好的服务。延迟的含义定义如下：

   - 对于读请求，它是从请求 TLP 发送 END 符号到接收该请求的第一个完成 TLP 的 STP 符号之间的延迟。

   - 对于写请求，它与流控背压有关。如果已发出写但由于缺少流控信用而无法进行下一次写，则延迟是从该写的最后一个符号 (END) 到给予更多信用的 DLLP 的第一个符号 (SDP) 的时间。换句话说，这表示根端口应能接受下一次写的时间。

- Requirement（要求）— 可以为无、一个或两个设置，以指示是否需要该延迟值。如果设备未实现这些流量类型之一或对其没有服务要求，则该位必须为相关字段清零。如果设备已报告要求但此后被定向到低于 D0 的设备电源状态，或者其 LTR Enable 位已被清除，则设备必须发送另一条 LTR 消息，报告这些延迟不再需要。

## **关于 LTR 使用的指南**

端点有一些关于 LTR 使用的指南：

1. 建议它们在每次服务要求发生变化时发送更新的 LTR 消息，规范花了一些时间讨论了相关示例。这里的要点是，设备在对服务要求进行更改时需要考虑所有延迟。该计算包括恢复参考时钟（如果已关闭）所需的时间、将 Link 恢复到 L0 所需的时间、传递 LTR 消息所需的时间，以及平台准备处理新要求所需的时间。

2. 如果正在降低延迟容忍度，则建议在第一个相关请求之前足够早地发送 LTR 消息，以确保平台已准备好。

**786**

**第 16 章：电源管理**

3. 如果正在增加延迟容忍度，则报告该情况的 LTR 消息应紧跟在使用先前延迟值的最后一个请求之后。

4. 为实现最佳的整体平台电源效率，建议端点尽可能多地缓冲请求，然后以端点可以支持的尽可能长的突发方式发送它们。

多功能设备 (MFD) 有一些自己的规则。例如，它们必须按如下方式发送"合并"的 LTR 消息：

1. 报告的延迟值必须反映与任何 Function 关联的最低值。侦听和非侦听延迟可以与不同的 Function 相关联，但如果它们都没有对侦听或非侦听流量的要求，则该类型的 Requirement 位不得置位。

2. 如果任何 Function 以影响合并值的方式更改其值，则 MFD 必须向上游发送新的 LTR 消息。

交换机也有类似的一组与 LTR 相关的规则。基本上，它们从已启用 LTR 的下游端口收集消息，并根据以下规则向上游发送"合并"消息：

1. 如果交换机支持 LTR，则它必须在其所有端口上都支持 LTR。

2. 只有在设置了 LTR Enable 位时，或在软件清除它之后不久以报告任何先前的要求不再有效时，才允许上游端口发送 LTR 消息。

3. 合并的 LTR 值基于任何参与的下游端口报告的最低值。如果 Requirement 位清零或报告了无效值，则延迟被认为是有效地无限的。

4. 如果任何下游端口报告需要 LTR 值，则 Requirement 位将针对上游转发的 LTR 消息中的该类型置位。

5. 上游报告的 LTR 值必须考虑交换机本身的延迟。如果交换机延迟根据其操作模式而变化，则必须确保不超过所有下游端口报告的最小值的 20%。在上游端口上报告的值是所有下游端口报告的最小值减去交换机自身的延迟，但该值不能小于零。

6. 如果下游端口进入 DL_Down 状态，则该端口的先前延迟必须被视为无效。如果这改变了上游的合并值，则必须发送新消息以报告。

7. 如果下游端口的 LTR Enable 位被清除，则与该端口关联的任何延迟都必须被视为无效，这也可能导致向上游发送新的 LTR 消息。

8. 如果任何下游端口接收到会更改合并值的新 LTR 值，则交换机必须向上游发送新的 LTR 消息以报告。

**787**

**PCI Ex ress Technolo p gy**

最后，根复合体 (RC) 也有关于 LTR 的一些规则：

1. RC 可以延迟处理设备请求，只要它满足服务要求。一个应用可能是缓冲来自端点的多个请求并批量处理它们。

2. 如果在多个请求进行时更新了延迟要求，则新值必须在 RC 处理下一个请求之前被理解，并且时间应少于先前报告的延迟要求。

_Figure 16-40: LTR Message Format_

**==> picture [350 x 264] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1<br>
Byte 0 Fmt Type R TC Rsv T E Attr AT Length (Reserved)<br>
0 0 1 1 0  1 0 0 0 0 0 D P 0 0 0 0<br>
Message Code<br>
Byte 4 Requester ID Tag 0001 0000<br>
Byte 8 Reserved<br>
Byte 12 No-Snoop Latency Snoop Latency<br>
Point-to-Point<br>
15 14 13 12 10 9 0<br>
Rsv [Latency] Latency Value<br>
Scale<br>
Requirement<br>
Scale:<br>
000 - x 1ns   001 - x 32 ns<br>
010 - x 1K ns   011 - x 32K ns<br>
100 - x 1M ns  101 - x 32M ns<br>
110 - x not permitted<br>
**----- End of picture text -----**<br>


**788**

**第 16 章：电源管理**

## **LTR 示例**

为了说明到目前为止讨论的概念，请考虑图 16-41（第 789 页）中所示的示例拓扑。这里，左下角的端点已向交换机传送了一条 LTR 消息，报告侦听延迟要求为 1200ns。此时，连接到交换机的其他端点都未报告 LTR 值，因此这将成为要向上游报告的合并值。但是，交换机的内部延迟为 50ns，因此必须从要报告的值中减去该值，结果上游端口向上游发送一条 LTR 消息，报告 1150ns 给根端口。

_Figure 16-41: LTR Example_

**==> picture [122 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>
value<br>
Conglomerate  i<br>
value 1200 ns —<br>
& _<br>
1200 ns<br>
[| Va i<br>
**----- End of picture text -----**<br>


接下来，遗留端点传送了一条 LTR 消息，延迟要求较大，为 5000ns，如图 16-42（第 790 页）所示。由于这大于交换机的当前合并值，因此不会为此情况发送 LTR 消息。

**789**

**PCI Ex ress Technolo p gy**

_Figure 16-42: LTR ‐ Change but no Update_

**==> picture [176 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>
value<br>
—<br>
Conglomerate  1200 ns<br>
value<br>
Switch EndpointPCle<br>
e ¢<br>
Vl i IN 5000 ns<br>
**----- End of picture text -----**<br>


在下一阶段，中间的端点将其 LTR 值报告为 700ns。这小于当前合并值，因此交换机通过减去其内部延迟来计算新值 650ns，并将其作为 LTR 消息转发到上游。这使得该根端口的当前延迟要求为 650ns，如图 16-43（第 791 页）所示。

最后，到中间端点的链路因某种原因停止工作，如图 16-44（第 791 页）所示，并且交换机端口报告 DL_Down。因此，该端口的 LTR 值必须被视为无效。由于其值被用作当前合并值，因此合并值将更新为仍然有效的最低值，即最左侧端点报告的 1200ns。然后交换机将减去其内部延迟，并通过新的 LTR 消息向根端口报告 1150ns。

**790**

**第 16 章：电源管理**

_Figure 16-43: LTR ‐ Change with Update_

**==> picture [107 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  650 ns<br>
value<br>
Conglomerate<br>
value 700 ns<br>
> _<br>
Va i<br>
ES}<br>
EndpointPCle # =ndnaint§PCle<br>
700 ns<br>
**----- End of picture text -----**<br>
