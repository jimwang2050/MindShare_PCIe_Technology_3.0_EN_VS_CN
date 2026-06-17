在选择插接板 (interposer) 时需要谨慎,因为不同厂商以及最大 PCIe 链路速度所施加的不同要求会导致探针电路有所差异。例如,Gen3 插槽插接板应包含允许动态链路训练过程正确通过探针的探针电路。LeCroy Gen3 插槽插接板使用线性电路来保持波形在通过探针时的形状。这允许在链路训练期间动态改变发送端的预加重,同时允许接收端量化新设置的影响(无论是正面影响还是负面影响)。

_Figure A‐2: LeCroy PCI Express Slot Interposer x16_

LeCroy 还提供了一系列用于其他外形规格(如 ExpressCard、XMC、Mini Card、Express Module、AMC 等)的专用插接板。其中部分插接板如图 3 第 923 页所示。如需这些插接板的完整列表,请参阅 LeCroy 网站:www.lecroy.com,因为该列表在不断扩充。

**922**

**Appendix A**

_Figure A‐3: LeCroy XMC, AMC, and Mini Card Interposers_

对于无法使用专用插接板进行调试的 PCIe 链路,第 923 页图 4 所示的中段总线探针 (mid-bus probe) 是次优选择。中段总线探针涉及在 PCB 上放置一个业界标准的探针几何结构。每条 PCIe 通道被路由到封装上一对焊盘,可以使用中段总线探针头对其进行探测。这些探针使用弹簧针或 C 夹在被测系统与协议分析仪之间提供免焊接的机械连接。

_Figure A‐4: LeCroy PCI Express Gen3 Mid‐Bus Probe_

**923**

## **PCI Express Technology**

作为最后手段,可以使用第 924 页图 5 所示的飞线探针 (flying lead probe) 将协议分析仪连接到被测系统。这涉及将一个电阻式分流电路和连接器引脚焊接到 PCIe 走线上。由于 PCIe 链路的交流耦合电容通常是唯一可以接触到走线的地方,因此该电路通常焊接到交流耦合电容上。一旦探针电路焊接到 PCB 上,分析仪探针就可以根据需要进行连接和移除。这种方法几乎可以用于任何 PCIe 链路,但连接的稳固性受限于添加探针的技术人员的技能。

_Figure A‐5: LeCroy PCI Express Gen2 Flying Lead Probe_

## **使用 PETracer 应用程序查看流量**

## **CATC Trace 查看器**

使用 LeCroy PETracer 应用程序查看 PCI Express 流量的主要方式是 CATC Trace 视图。该视图对每个记录的分组进行解析,将其分解为不同的分组字段,以突出该分组中包含的重要值。混合使用颜色和文本,以便直观地对每个分组进行分类并解释其用途。错误以红色高亮显示,如第 925 页图 6 所示。警告以黄色高亮显示,便于识别流量或分组字段中不符合规范的部分。

**924**

**Appendix A**

## _Figure A‐6: TLP Packet with ECRC Error_

除了对每个分组进行解码和直观分解之外,层次化显示还可以对相关分组进行逻辑分组。例如,在 "Link Level" (链路级) 模式下,TLP 分组与其对应的 ACK 分组被分组在一起。每个 TLP 被标识为隐式或显式 ACK 或 NAK。第 925 页图 7 显示了一个 ACK DLLP 的示例以及被 ACK 的 TLP。

_Figure A‐7: "Link Level" Groups TLP Packets with their Link Layer Response_

在第 926 页图 8 所示的 "Split‐Level" (拆分级) 模式下,CATC Trace 视图组合了拆分事务。例如,单个 TLP 读操作可以与一个或多个完成 TLP 分组在一起,以便在跟踪中以单行逻辑地显示大数据传输。每个拆分级事务都提供数据量、起始地址以及性能指标。这允许用户绕过大型内存事务如何被分解为多个 TLP 分组的细节,而专注于数据的内容。如果用户希望查看拆分事务的细节,层次化显示可以显示构成该拆分事务的所有分组的链路级和/或分组级细分。这种 "drill-down" (向下钻取) 的流量分析方法允许用户从总线上的高级视图入手,仅在其感兴趣的流量区域进行深入分析。

**925**

## **PCI Express Technology**

_Figure A‐8: "Split Level" Groups Completions with Associated Non‐Posted Request_

CATC trace 视图还支持第 927 页图 9 所示的 "Compact‐View" (紧凑视图)。在该视图中,重复发送的分组被折叠为单个单元格。这对于折叠训练序列 (Training Sequences) 或流量控制初始化 (Flow Control Initialization) 分组非常有用。执行此折叠的软件算法也足够智能,可以折叠任何 SKIP 有序集。这创建了一个非常紧凑的链路训练过程视图,允许用户检查链路训练分组中的变化,而不必滚动浏览数百个分组。

**926**

**Appendix A**

_Figure A‐9: "Compact View" Collapses Related Packets for Easy Viewing of Link Training_

## **LTSSM 图形**

为了进一步增强 "drill-down" 流量查看方法,PETracer 应用程序包含一个 LTSSM 图形视图,如第 928 页图 10 所示。当调用该图形时,软件会解析跟踪以查找链路训练部分,并推断链路训练和状态状态机 (LTSSM) 的状态。其结果是一个以非常高级的视图分解 LTSSM 状态转换的图形。该图形允许用户立即查看链路是否进入了恢复状态。如果进入恢复状态,用户可以轻松识别链路的哪一侧发起了恢复、进入恢复的次数,甚至是否由于恢复导致链路速度或链路宽度降低。

LTSSM 图形也是回到跟踪文件的活动链接。例如,如果用户单击进入恢复状态的条目,跟踪文件将导航到跟踪文件中该位置。这将允许用户查看恢复是否是由重复的 NAK 引起的,还是由于块对齐丢失等其他原因。

**927**

简而言之,当用户调试与链路训练、速率变化或低功耗状态转换相关的问题时,LTSSM 会受到影响。通过检查 LTSSM 图形,用户可以轻松识别这些链路状态变化是否发生、在何处发生,并直接导航到它们以加快分析速度。

_Figure A‐10: LTSSM Graph Shows Link State Transitions Across the Trace_

## **流控制信用跟踪**

在 PCI Express 中,流控制信用跟踪特别具有挑战性。流控制更新分组并不显示每个端点拥有的信用数量,而是显示已使用的信用总数。这意味着每个端点必须为每种类型保持一个运行信用计数器。在许多场景中信用可能会丢失,如果发生这种情况,链路最终将由于缺乏信用而无法传输数据。这类问题非常难以识别和调试。

LeCroy PETracer 应用程序具有第 929 页图 11 所示的信用跟踪软件工具,以协助进行此调试。如果跟踪包含 FC-Init 分组,它将遍历跟踪并在每个 TLP 和 FC-Update 之后显示每个虚拟通道缓冲区类型的剩余信用量。

FC-Init 分组在链路训练之后发送一次。因此,PETracer 应用程序允许用户

**Appendix A**

在跟踪中的某个位置设置初始信用值,软件将计算剩余分组的相对信用值。即使用户设置初始信用值不正确,能够查看相对信用通常足以发现流控制问题。

_Figure A‐11: Flow Control Credit Tracking_

## **Bit Tracer**

某些调试情况无法通过对流量的向下钻取方法来解决。例如,如果链路设置不正确,记录通常无法读取。如果设备没有正确地对流量加扰,或者 10 bit 符号以相反的顺序发送,该怎么办?对于这种情况,需要一种专注于示波器的波形视图与 CATC Trace 视图之间分析的工具。这正是第 930 页图 12 所示的 BitTracer 视图最强大的地方。

BitTracer 视图允许用户查看链路上看到的原始流量。软件允许用户将流量视为 10 bit 符号、加扰字节或未加扰字节。无效符号和不正确的运行差异 (Running Disparity) 以红色高亮显示。

**929**

## **PCI Express Technology**

为了进一步确定流量可能出现的问题,BitTracer 工具添加了一系列强大的后处理功能,可以修改流量。例如,在采集后,用户可以反转给定通道的极性。一旦应用,用户可以查看 10 bit 符号现在是否在跟踪中正确表示。如果这清理了跟踪,则表明分析仪硬件的记录设置需要更改。

_Figure A‐12: BitTracer View of Gen2 Traffic_

此外,还可以修改通道排序。这对于确定通道反转是否导致不良捕获非常有用。如果流量存在过大的通道间偏移 (skew),BitTracer 软件允许用户重新对齐流量。对于 Gen3 流量,该偏移可以一次 1 bit 地应用。这实质上允许用户在采集后修复 130 bit 块对齐。

在对数据应用更改后,所有或仅一部分数据可以导出到标准 CATC Trace 视图中,以进行更高级别的分析。该工作流对于在早期 bring-up 期间调试低级问题非常强大。举例来说,假设用户的设备正确训练了链路,然后突然对 1 个通道应用极性反转。这明显违反规范,将导致链路重新训练。如果使用 BitTracer 工具捕获该流量,用户可以轻松将此识别为问题。此外,反转前后的流量部分可以导出到单独的跟踪文件中,并在 CATC Trace 视图中进行检查。

**930**

**Appendix A**

## **分析概述**

如您所见,不同的流量视图对于调试某些故障条件是有益的。LeCroy 支持从许多来源将 PCIe 流量导入其高度复杂的 PEtracer 软件。无论是 RTL 仿真、示波器捕获还是专用协议分析仪捕获,PETracer 都拥有一套丰富的流量视图和报告,允许用户最好地了解其 PCIe 链路的健康状况和状态。

## **流量生成**

## **流片前 (Pre-Silicon)**

为了在仿真中激励 PCI Express 端点,可以从许多供应商处购买专用验证 IP。该 IP 将测试基本功能并执行许多 PCIe 一致性检查。ASIC 开发人员当然有兴趣在 tapeout 之前发现并修复这些问题,这正是这些工具的价值所在。如果 PCIe 设计在 FPGA 中实现,其中掩模成本不是问题,那么使用 LeCroy PETrainer 或 LeCroy PTC 卡等专用流量生成工具在硬件中执行这些一致性检查可能更具成本效益。

## **流片后 (Post-Silicon)**

## **Exerciser 卡**