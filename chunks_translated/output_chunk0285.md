|VRX‐DIFF‐PP‐CC|175<br>（最小）<br>1200<br>（最大）|120（最小）<br>1200（最大）|间接指定|mV|公共时钟接收器的峰峰值差分电压灵敏度。|
|VRX‐DIFF‐PP‐DC|175<br>（最小）<br>1200<br>（最大）|100（最小）<br>1200（最大）|间接指定|mV|数据时钟接收器的峰峰值差分电压灵敏度。|
|VRX‐IDLE‐DET‐DIFFp‐p|65（最小）175（最大）|||mV|接收器引脚处的电气空闲检测阈值。|
|ZRX‐DIFF‐DC|80<br>（最小）<br>120<br>（最大）|由 RLRX‐DIFF 覆盖||Ω|在较高频率下，阻抗不能再用集总值表示，必须更详细地描述。|
|ZRX‐‐DC|40<br>（最小）<br>60<br>（最大）|40（最小）<br>60（最大）|由 RLRX‐CM 限定|Ω|接收器检测所需的直流阻抗。|



**498**

**第 13 章：物理层 - 电气**

_表 13‐5：通用接收器特性（续）_

|**项目**|**2.5 GT/s**|**5.0 GT/s**|**8.0 GT/s**|**单位**|**备注**|
|---|---|---|---|---|---|
|LRX‐SKEW|20|8|6|ns|接收器必须能够纠正的最大 Lane 到 Lane 偏移。|
|RLRX‐‐DIFF|10<br>（最小）|10（最小）<br>，频率 0.05 ‐<br>1.25 GHz，<br>8（最小）<br>，频率 >1.25 ‐<br>2.5 GHz|10（最小）<br>，频率 0.05 ‐<br>1.25 GHz，<br>8（最小）<br>，频率 >1.25 ‐<br>2.5 GHz，<br>5（最小）<br>，频率 >2.5 ‐<br>4.0 GHz|dB|Rx 封装 + Si 差分回波损耗|
|RLRX‐‐CM|6（最小）|6（最小）|6（最小）<br>，频率 0.05 ‐<br>2.5 GHz，<br>5（最小）<br>，频率 >2.5 ‐ 4<br>GHz|dB|共模 Rx 回波损耗|



_图 13‐34：2.5 GT/s 接收器眼图_

**==> picture [305 x 171] intentionally omitted <==**

**----- Start of picture text -----**<br>
V = 88 mV<br>VRX-CM-DC= 0 V RX-DIFFp-MIN<br>TRX-EYE-MIN = 0.4 UI<br>**----- End of picture text -----**<br>


**499**

**PCI Express Technology**

## **链路电源管理状态**

第 500 页的图 13‐35 至第 504 页的图 13‐39 说明了物理层在各种电源管理状态下的电气状态，并描述了几个特性。其中之一是 Tx 和 Rx 终端，有时实现为有源逻辑

_图 13‐35：L0 全开链路状态_

**==> picture [375 x 253] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>ON direction ON<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM High or Low  VRX-CM = 0 V Low impedance ON<br>impedance termination termination<br>ON<br> 传输和接收正在进行<br> 推荐功耗预算约 80 mW 每 Lane<br> 链路的一个方向可以处于 L0，而另一侧处于 L0s<br> 发送器和接收器时钟 PLL 开启<br> 发送器开启，接收器开启<br> 发送器处为低阻抗终端<br>无规格<br>**----- End of picture text -----**<br>


**500**

**第 13 章：物理层 - 电气**

## _图 13‐36：L0s 低功耗链路状态_

**==> picture [368 x 176] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect 保持在 0 - 3.6 V 直流共模电压<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>ON direction ON<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM 高或低阻抗终端 VRX-CM = 0 V 低阻抗终端 ON<br>ON<br> 发送器保持电气空闲电压 (VTX-DIFFp < 20 mV) 和直流共模电压 (VTX-CM-DC 0 – 3.6 V)<br>无规格<br>**----- End of picture text -----**<br>


- 推荐功耗预算 ≤ 每 Lane 20 mW

- 推荐退出延迟 < 50 ns，但设计人员表示更现实的数字似乎是 1 us-2 us

- 链路的一个方向可以处于 L0s，而另一个处于 L0

- 发送器和接收器时钟 PLL 开启，但 Rx 时钟失去同步

- 发送器开启，接收器开启 → 发送器处为高或低阻抗终端

**501**

## **PCI Express Technology**

## _图 13‐37：L1 低功耗链路状态_

**==> picture [380 x 262] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect 保持在 0 - 3.6 V 直流共模电压<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>ON direction ON<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM 高或低阻抗终端 VRX-CM = 0 V 低阻抗终端 可能关闭<br>可能关闭<br> 发送器保持电气空闲电压和直流共模电压<br> 推荐功耗预算 ≤ 每 Lane 5 mW<br> 推荐退出延迟 < 10 微秒（可能更大）<br> 链路的两个方向必须同时处于 L1<br> 发送器和接收器时钟 PLL 可能关闭，但设备的时钟开启<br> 发送器开启，接收器开启<br> 发送器处为高或低阻抗终端<br>无规格<br>**----- End of picture text -----**<br>


**502**

**第 13 章：物理层 - 电气**

_图 13‐38：L2 低功耗链路状态_

**==> picture [378 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect 发送器很可能关闭，<br>不维持直流值<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>OFF direction OFF<br>CTX ZTX<br>-<br>D- D-<br>ZTX ZTX ZRX ZRX Clock<br>Clock Source<br>Source VCM 高或低  VRX-CM = 0 V 高阻抗 OFF<br>阻抗终端 终端<br>OFF<br>信标的低频   发送器保持电气空闲电压，但不要求保持<br>开启 直流共模电压。最有可能关闭。<br> 推荐功耗预算 ≤ 每 Lane 1 mW<br> 推荐退出延迟 < 12 - 50 毫秒<br> 链路的两个方向处于 L2<br> 发送器和接收器时钟 PLL 关闭，设备的时钟关闭<br> 发送器中信标的低频时钟开启<br> 设备主电源关闭，但 Vaux 开启<br> 发送器关闭，接收器关闭<br> 发送器处为高或低阻抗终端，接收器处为高阻抗<br>无规格<br>**----- End of picture text -----**<br>


**503**

## **PCI Express Technology**

## _图 13‐39：L3 链路关闭状态_

**==> picture [366 x 261] intentionally omitted <==**

**----- Start of picture text -----**<br>
Detect 直流共模电压关闭<br>D+ CTX ZTX D+<br>+<br>Lane in<br>Transmitter one  Receiver<br>OFF direction OFF<br>CTX ZTX<br>-<br>D- D-<br>Clock<br>ZTX ZTX ZRX ZRX<br>Clock 高阻抗  高阻抗 Source<br>Source VCM 终端 VRX-CM = 0 V 终端 OFF<br>OFF<br>信标的低频   发送器不保持直流共模电压<br>关闭   推荐功耗预算：零<br> 在电源开启后，推荐的 L3 -> L0 退出延迟 < 12 - 50 毫秒<br> 链路的两个方向处于 L3<br> 发送器和接收器时钟 PLL 关闭，设备的时钟关闭<br> 发送器中信标的低频时钟关闭<br> 设备主电源关闭，Vaux 关闭<br> 发送器和接收器关闭<br> 发送器和接收器处为高阻抗终端<br>无规格<br>**----- End of picture text -----**<br>


**504**

## _**14 链路初始化与训练**_

## **上一章**

上一章描述了物理层到链路的电气接口，包括差分发送器和接收器的一些低级特性。本章还讨论了对信号均衡的需求以及用于实现它的方法。本章结合了 Gen1、Gen2 和 Gen3 速度的电气发送器和接收器特性。

## **本章**

本章描述了物理层链路训练和状态状态机 (LTSSM) 的操作。链路的初始化过程从上电或复位开始描述，直到链路在正常数据包传输发生期间达到完全可操作的 L0 状态。此外，还讨论了链路电源管理状态 L0s、L1、L2 和 L3 以及状态转换。描述了在链路训练期间重新建立位锁定、符号锁定或块锁定的恢复状态。还讨论了用于链路带宽管理的链路速度和宽度变化。

## **下一章**

下一章讨论 PCIe 端口或链路中发生的错误类型、如何检测、报告以及处理它们的选项。由于 PCIe 被设计为向后兼容 PCI 错误报告，因此包括对 PCI 错误处理方法的回顾作为背景信息。然后我们将重点关注可纠正、非致命和致命错误的 PCIe 错误处理。

**505**

**PCI Express Technology**

## **概述**

链路初始化和训练是由物理层控制的基于硬件（非软件）的过程。该过程配置和初始化设备的链路和端口，以便正常的分组流量在链路上进行。

_图 14‐1：链路训练和状态状态机位置_

**==> picture [380 x 338] intentionally omitted <==**

**----- Start of picture text -----**<br>
内存、I/O、配置 R/W 请求或消息请求或完成<br>（软件层发送/接收地址/事务类型/数据/消息索引）<br>软件层<br>发送 接收<br>事务层包 (TLP) 事务层包 (TLP)<br>标头 数据有效负载  ECRC 标头 数据有效负载  ECRC<br>事务层<br>流控<br>发送 接收<br>虚拟通道<br>缓冲区 缓冲区<br>管理<br>每 VC 每 VC<br>排序<br>链路包 DLLPs 例如 DLLPs 链路包<br>序列 TLP LCRC ACK/NAK CRC ACK/NAK CRC 序列 TLP LCRC<br>数据链路层 TLP 重放 解复用<br>缓冲区<br>TLP 错误<br>复用 检查<br>物理包 物理包<br>开始 链路包 结束 开始 链路包 结束<br>物理层 编码 解码<br>并串转换 链路 串并转换<br>差分驱动器 训练 差分接收器<br>(LTSSM)<br>端口<br>**----- End of picture text -----**<br>


**506**

**第 14 章：链路初始化与训练**

完整的训练过程在复位后由硬件自动启动，并由 LTSSM（链路训练和状态状态机）管理，如第 506 页图 14‐1 所示。

在链路初始化和训练过程中配置了几件事。让我们考虑一下它们是什么并预先定义一些术语。

- **位锁定 (Bit Lock)**：当链路训练开始时，接收器的时钟尚未与输入信号的发送时钟同步，无法可靠地采样输入位。在链路训练期间，接收器 CDR（时钟数据恢复）逻辑使用输入位流作为时钟参考来重新创建发送器的时钟。一旦从流中恢复时钟，就可以说接收器已获得位锁定 (Bit Lock)，然后能够对输入位进行采样。有关位锁定机制的更多信息，请参见第 395 页 "Achieving Bit Lock"。

- **符号锁定 (Symbol Lock)**：对于 8b/10b 编码（用于 Gen1 和 Gen2），下一步是获取符号锁定。这是一个类似的问题，因为接收器现在可以看到各个位，但不知道 10 位符号的边界在哪里。随着 TS1 和 TS2 的交换，接收器在位流中搜索可识别的模式。一个用于此目的的简单模式是 COM 符号。其独特的编码使其易于识别，其到达显示了符号和有序集的边界，因为 TS1 或 TS2 必须正在进行中。有关详细信息，请参见第 396 页 "Achieving Symbol Lock"。

**507**

## **PCI Express Technology**

- **块锁定 (Block Lock)**：对于 8.0 GT/s（Gen3），该过程与符号锁定略有不同，因为不使用 8b/10b 编码，所以没有 COM 字符。但是，接收器仍然需要在输入位流中找到可识别的分组边界。解决方案是在训练序列中包含更多 EIEOS（电气空闲退出有序集）的实例，并使用它来定位边界。EIEOS 可识别为 00h 和 FFh 字节交替的模式，并且它定义了块边界，因为根据定义，当该模式结束时，下一个块必须开始。

- **链路宽度**：具有多个 Lane 的设备可能能够使用不同的链路宽度。例如，具有 x2 端口的设备可以连接到具有 x4 端口的设备。在链路训练期间，两个设备的物理层测试链路并将宽度设置为最高公共值。

- **Lane 反转**：多 Lane 设备端口上的 Lane 从 Lane 0 开始按顺序编号。通常，一个设备端口的 Lane 0 连接到相邻设备端口的 Lane 0，Lane 1 连接到 Lane 1，依此类推。然而，有时希望能够逻辑上反转 Lane 编号以简化布线并允许 Lane 直接连接而不必交叉（参见第 508 页的图 14‐2）。只要一台设备支持可选的 Lane 反转功能，这就可以工作。该情况在链路训练期间被检测到，并且一台设备必须在内部反转其 Lane 编号。由于规范不要求支持此功能，因此板设计人员将需要在以相反顺序连接 Lane 之前验证至少一台连接的设备支持此功能。

_图 14‐2：Lane 反转示例（支持可选）_

**==> picture [352 x 205] intentionally omitted <==**

**----- Start of picture text -----**<br>
示例 1 示例 2<br>设备均不支持 Lane 反转 设备 B 支持 Lane 反转<br>设备 A 设备 A<br>（上游设备） （上游设备）<br>0 1 2 3 0 1 2 3 0 1 2 3 0 1 2 3<br>反转后的<br>Lane<br>0 1 2 3 0 1 2 3<br>3 2 1 0 3 2 1 0 3 2 1 0 3 2 1 0 反转前的<br>Lane<br>设备 B 设备 B<br>反转<br>（下游设备） （下游设备）<br>走线必须交叉以正确连接 Lane， 增加复杂性和成本。 Lane 反转允许 Lane<br>编号直接匹配。<br>**----- End of picture text -----**<br>

- **极性反转**：两台设备的 D+ 和 D‐ 差分对端子也可以根据需要进行反转，以使板布局和布线更容易。每个接收器 Lane 必须独立检查此情况并在训练期间根据需要进行自动纠正，如第 509 页的图 14‐3 所示。为此，接收器查看传入 TS1 或 TS2 的符号 6 到 15。如果在 TS1 中收到 D21.5 而不是 D10.2，或在 TS2 中收到 D26.5 而不是预期的 D5.2，则该 Lane 的极性反转，必须进行纠正。与 Lane 反转不同，此功能的支持是强制性的。

**508**

**第 14 章：链路初始化与训练**

_图 14‐3：极性反转示例（支持必需）_

**==> picture [270 x 128] intentionally omitted <==**

**----- Start of picture text -----**<br>
设备 A<br>（上游设备）<br>D+ D- D+ D-<br>极性反转后<br>D- D+<br>极性反转后<br>D+ D-<br>极性反转前<br>D- D+ D- D+<br>设备 B<br>（下游设备）<br>**----- End of picture text -----**<br>


- **链路数据速率**：复位后，链路初始化和训练将始终使用默认的 2.5Gbit/s 数据速率以实现向后兼容性。如果有更高的数据速率可用，它们会在此过程中通告，训练完成后，设备将自动通过快速重新训练更改为最高共同支持的速率。

- **Lane 到 Lane 去偏移**：走线长度变化和其他因素会导致多 Lane 链路的并行位流在不同时间到达接收器，这个问题称为信号偏移 (signal skew)。接收器需要通过根据需要延迟早期到达的位来补偿此偏移以对齐位流（参见第 442 页 "Lane‐to‐Lane Skew"）。他们必须自动纠正较大的偏移（在 2.5GT/s 时允许 20ns 的到达时间差），这使板设计人员免于创建等长走线的困难约束。结合极性反转和 Lane 反转，这大大简化了板设计人员创建可靠的高速链路的任务。

## **链路训练中的有序集**

## **概述**

所有不同类型的物理层有序集在第 388 页 "Ordered sets" 一节中描述。训练序列 TS1 和 TS2 在训练过程中值得关注。它们在 Gen1 或 Gen2 模式下的格式如图 14‐4（第 510 页）所示，而在 Gen3 操作模式下，它们如图 14‐5（第 511 页）所示。以下是其内容的详细描述。

**509**

## **PCI Express Technology**

_图 14‐4：Gen1 或 Gen2 模式下的 TS1 和 TS2 有序集_

**==> picture [281 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 COM K28.5<br>1 Link # 0 - 255 = D0.0 - D31.7，PAD = K23.7<br>2 Lane # 0 - 31 = D0.0 - D17.1，PAD = K23.7<br>3 # FTS 接收器恢复 L0s 所需的 FTS 数量<br>4 Rate ID 位 1 必须设置，表示支持 2.5 GT/s<br>5 Train Ctl<br>6 TS ID 或更改到 8.0 GT/s 时的均衡信息，否则<br>9 EQ Info TS1 或 TS2 标识符<br>10<br>TS1 标识符 = D10.2<br>TS ID<br>TS2 标识符 = D5.2<br>15<br>**----- End of picture text -----**<br>


## **TS1 和 TS2 有序集**

如图所示，TS1 和 TS2 由 16 个符号组成。它们在 LTSSM 的 Polling、Configuration 和 Recovery 状态期间交换，在第 518 页 "Link Training and Status State Machine (LTSSM)" 中描述。这些符号的描述如下，并在第 514 页的表 14‐1（TS1）和第 516 页的表 14‐2（TS2）中进行了总结。

为了使描述更短更易读，术语 "Gen1" 将用于指示 2.5 GT/s 的数据速率，"Gen2" 用于指示 5.0 GT/s 的数据速率，"Gen3" 用于指示 8.0 GT/s 的数据速率。另请注意，链路和 Lane 编号中使用的 PAD 字符在较低数据速率下由 K23.7 字符表示，但在 Gen3 下表示为数据字节 F7h。在我们的讨论中，PAD 类型之间的区别并不重要，将仅隐含表示。

**510**

**第 14 章：链路初始化与训练**

_图 14‐5：Gen3 操作模式下的 TS1 和 TS2 有序集块_

**==> picture [295 x 218] intentionally omitted <==**

**----- Start of picture text -----**<br>
0 TS1 = 1Eh，TS2 = 2Dh<br>1 Link # 0 - 31，PAD = F7h<br>2 Lane # 0 - 31，PAD = F7h<br>3 # FTS 接收器恢复 L0s 所需的 FTS 数量<br>4 Rate ID 位 3 表示支持 8.0 GT/s<br>5 Train Ctl<br>6<br>均衡预设<br>EQ Info<br>和系数或 TS2<br>9<br>10<br>TS1 标识符 = 4Ah<br>TS ID<br>TS2 标识符 = 45h<br>13<br>14 TS ID TS1、TS2 或<br>15 DC 平衡符号<br>**----- End of picture text -----**<br>


第 514 页的表 14‐1 和第 516 页的表 14‐2 是 TS1 和 TS2 内容的摘要。16 个 TS1/TS2 符号的更详细描述如下：

- **符号 0**：

- 对于 **Gen1 或 Gen2**，任何有序集的第一个符号是 K28.5（COM）字符。接收器使用此字符获取符号锁定。由于它必须同时出现在所有 Lane 上，因此它对于 Lane 的去偏移也很有用。

- 对于 **Gen3**，有序集由必须在块之前出现的 2 位同步头标识（图中未显示），之后的第一个符号指示将跟随哪个有序集。对于 TS1，第一个符号是 1Eh，对于 TS2，是 2Dh。

- **符号 1（Link #）**：在 Polling 状态中，此字段包含 PAD 符号，但在其他状态中分配了链路编号。

- **符号 2（Lane #）**：在 Polling 状态中，此字段包含 PAD 符号，但在其他状态中分配了 Lane 编号。

- **符号 3（N_FTS）**：表示接收器在以当前速度退出 L0s 电源状态以达到 L0 状态时所需的快速训练序列的数量。发送器将发送至少那么多

**511**

## **PCI Express Technology**

FTS 以退出 L0s。所需的时间量取决于需要的数量和正在使用的数据速率。例如，在 2.5 GT/s 时，每个符号需要 4ns，因此，如果需要 200 个 FTS，则所需时间为 200 FTS * 每个 FTS 4 个符号 * 4ns/符号 = 3200 ns。如果发送器设备中设置了 Extended Synch 位，则必须发送总共 4096 个 FTS。这个大数字旨在为外部链路监控工具提供足够的时间来获取位和符号锁定，因为其中一些工具在这方面可能很慢。

- **符号 4（Rate ID）**：设备报告它们支持的数据速率，以及一些用于硬件发起的带宽更改的更多信息。2.5 GT/s 速率必须始终受支持，链路在复位后将始终自动训练到该速度，以便较新的组件保持与较旧组件的向后兼容性。如果支持 8.0 GT/s，还要求 5.0 GT/s 必须可用。此符号中的其他信息包括以下内容：

- **自动更改**：如果设置，则任何请求的带宽更改都是为了电源管理原因而发起的。如果请求了更改但未设置此位，则在更高速度或更宽链路上检测到不可靠的操作，并且请求更改以解决该问题。

- **可选去加重**

   - **上游端口**设置此位以指示它们在 5.0 GT/s 时所需去加重的级别。它们如何做出此选择是特定于实现的。在 Recovery.RcvrCfg 状态中，它们在内部注册接收到的此位的值（规范将其描述为存储在 select_deemphasis 变量中）。

   - **下游端口和根端口**：在 Polling.Compliance 状态中，select_deemphasis 变量必须设置为与该位的接收值匹配。在 Recovery.RcvrCfg 状态中，发送器将其 TS2 中的此位设置为与 Link Control 2 寄存器中的 Selectable De‐emphasis 字段匹配。由于该寄存器位是硬件初始化的，预期它在启动时由固件或绑定选项分配给最佳值。

   - 在 5.0 GT/s 的环回模式下，从设备的去加重值由主设备发送的 TS1 中的该位分配。

- **链路向上配置能力**：报告宽度减小后的宽链路是否能够恢复到宽状态。如果链路的两端在 Configuration.Complete 期间都报告了此情况，则此事实被内部记录（例如，upconfigure_capable 位被设置）。

- **符号 5（Training Control）**：传达特殊条件，例如热复位、启用环回模式、禁用链路、禁用加扰。

**512**

**第 14 章：链路初始化与训练**

- **符号 6‐9（均衡控制）**：