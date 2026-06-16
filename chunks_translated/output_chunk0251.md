- 10b — 4 位(16 个端口)

- 11b — 8 位(256 个端口)

配置软件为每个表加载端口编号,以实现受支持的每个 VC 所需的端口优先级。如图 7-19 (第 268 页) 所示,表的格式取决于每个条目的大小和此设计支持的阶段数。

**267**

**PCI Ex ress Technolo p gy**

_Figure 7‐19: 端口仲裁表的格式_

**==> picture [339 x 413] intentionally omitted <==**

**----- Start of picture text -----**<br>
32 阶段端口仲裁表<br>具有 4 位条目<br>31       28 27      24 23      20 19 16 15       12 11         8 7          4 3           0<br>Phase[7] Phase[6] Phase[5] Phase[4] Phase[3] Phase[2] Phase[1] Phase[0] 00h<br>Phase[15] Phase[14] Phase[13] Phase[12] Phase[11] Phase[10] Phase[9] Phase[8] 04h<br>Phase[23] Phase[22] Phase[21] Phase[20] Phase[19] Phase[18] Phase[17] Phase[16] 08h<br>Phase[31] Phase[30] Phase[29] Phase[28] Phase[27] Phase[26] Phase[25] Phase[24] 0Bh<br>1. 配置软件加载端口仲裁表。<br>2. 对表的更改自动设置端口仲裁 00b PAT 条目为 1 位(2 个端口)<br>表状态位。<br>01b PAT 条目为 2 位(4 个端口)<br>3. 软件设置 Load Port Arbitration Table 位以<br>10b PAT 条目为 4 位(16 个端口)<br>     将表内容应用于硬件。<br>4. 硬件将表内容加载到端口仲裁器,然后  11b PAT 条目为 8 位(256 个端口)<br>    在表加载完成时自动清除端口仲裁表<br>    状态位。<br>VC Resource Status Register  Port VC Capability Register 1<br>15                                       2  1  0  31                                                          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP RsvdP<br>VC Negotiation Pending  Port Arbitration Table Entry Size<br> Port Arbitration Table Status  Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>VC Resource Capability Register<br>31              26 24            19 17 16 15 8 7                     0<br>RsvdP VCID RsvdP RsvdP TC/VC Map<br>Load Port Arbitration Table<br>Port Arbitration Select<br>VC Enable<br>**----- End of picture text -----**<br>


**268**

**第 7 章:服务质量**

## **交换机仲裁示例 (Switch Arbitration Example)**

让我们考虑一个三端口交换机的示例,以说明端口和 VC 仲裁。该示例假定入口端口 0 和 1 上的数据包向上游方向移动,端口 2 是面向上游(朝向根复合体)的出口端口。在下面的讨论中请参考图 7-20 (第 270 页)。

1. 到达入口端口 0 的数据包根据端口 0 的 TC/VC 映射被放置在接收器 VC 中。如图所示,流量类 TC0 或 TC1 的 TLP 被发送到 VC0 缓冲区。携带流量类 TC3 或 TC5 的 TLP 被发送到 VC1 缓冲区。此链路上不允许使用其他 TC。顺便说一句,如果收到的数据包具有未映射到现有 VC 的 TC,它将被视为错误。

2. 到达入口端口 1 的数据包也根据 TC/VC 映射放入 VC 中,但与此端口不同。如图所示,携带流量类 TC0 的 TLP 被发送到 VC0,而携带流量类 TC2-TC4 的 TLP 被发送到 VC3。此链路上不允许使用其他 TC。

3. 在两个端口中,目标出口端口由每个数据包中的路由信息决定。例如,内存或 IO 请求 TLP 使用地址路由。

4. 所有发往出口端口 2 的数据包都提交给该端口的 TC/VC 映射逻辑。如图所示,携带流量类 TC0-TC2 的 TLP 被放入标有其入口端口号的 VC0 缓冲区,而携带流量类 TC3-TC7 的 TLP 由 VC1 管理。

5. 端口仲裁独立地应用于排队的数据包,以决定哪个端口的数据包接下来将加载到实际 VC 中。

6. 最后,VC 仲裁确定 VC 缓冲区中的事务将按何种顺序通过链路发送。

7. 请注意,VC 仲裁器仅在存在足够流控信用时才选择要传输的数据包。

**269**

**PCI Ex ress Technolo p gy**

_Figure 7‐20: 交换机中的仲裁示例_

**==> picture [357 x 208] intentionally omitted <==**

**----- Start of picture text -----**<br>
交换机 (Switch)<br>(1)<br>TC0,1TC3,5  VC0VC1 0 入口的 IngressMappingTC/VCPort 0 TC0,1TC3,5 INRESS EGRESS (5)端口仲裁:VC0出口端口 2<br>FC Buffer VC0 FC Buffer VC1<br>TLP1 RoutingTLP2 Routing TCTC TLP4 RoutingTLP3 Routing TCTC (4) 数据包Port 0 VC0VC0 ARB (6)<br>出口端口 2<br>到  端口 1 TC/VC VC 仲裁 (7)<br>(2) 确定出口端口(使用路由信息) (3) 到  端口 2到  端口 3 出口的 EgressMappingTC/VCPort 2 VC0VC1 ARB 2 TC0-2TC3-7 VC0VC1<br>TC2-4TC0   VC0VC3 1 入口的 IngressMappingTC/VCPort 1 TC2-4TC0 TC0-2=>VC0TC3-7=>VC1 (5)端口仲裁:VC1出口端口 2<br>FC Buffers VC0 FC Buffers VC3 数据包Port 1 VC1 ARB<br>TLP3 Routing TLP4 Routing VC1<br>TLP1 Routing TLP2 Routing<br>确定出口端口(使用路由信息) (3) 到  端口 0到  端口 2到  端口 3 此逻辑为每个出口端口复制<br>**----- End of picture text -----**<br>


## **多功能端点中的仲裁 (Arbitration in Multi-Function Endpoints)**

为将在具有多个功能的设备中实现 QoS 的端点这种特殊情况,定义了一组称为多功能虚拟通道 (MFVC, Multi-Function Virtual Channel) 功能的寄存器。毫不奇怪,这种情况在内部呈现出交换机端口必须处理的相同仲裁问题。

规范中描述了此仲裁的两种情况。在第一种情况中,如图 7-21 (第 271 页) 所示,有两个功能,但只有功能 0 包含 VC Capability 寄存器,此处所做的分配对所有功能隐式相同。对于此选项,功能之间的仲裁将以某种厂商特定的方式处理。这是最简单的方法,但不包括用于定义来自不同功能的请求之间优先级的标准结构,因此它不支持 QoS。

**270**

**第 7 章:服务质量**

_Figure 7‐21: 简单的多功能仲裁_

**==> picture [252 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Function 0 厂商特定 (Vendor-Specific)<br>仲裁<br>VC 内部链路<br>功能 (Capability)<br>0002h<br>出口端口<br>Function 1<br>内部链路<br>**----- End of picture text -----**<br>


如果需要 QoS 支持,则在 VC0 中实现 MFVC,并且每个功能都有其自己唯一的一组 VC Capability 寄存器。为保持软件向后兼容性,规范规定 _不使用_ MFVC 的设备的 VC Capability ID 必须为 0002h,而 _使用_ MFVC 结构的设备的 VC Capability ID 必须为 0009h。

图 7-22 (第 272 页) 展示了 MFVC 寄存器块以及端点中具有两个功能且其端口支持两个 VC 的示例框图。每个功能都有一个事务层 (Transaction Layer) 和自己的 VC Capability 寄存器,但未实现较低的层。相反,它们连接到共享端口的事务层(后者具有所有层)。共享硬件接口当然会导致成本降低,而添加 MFVC 允许这些功能处理等时流量。

从图中可以看出,MFVC 寄存器仅驻留在功能 0 中,并定义要用于此接口的 VC 和仲裁方法。MFVC 寄存器看起来与 VC capability 寄存器非常相似,并支持 VC 仲裁和功能仲裁。由于来自多个功能的数据包可以同时尝试访问同一 VC,因此功能仲裁决定它们之间的优先级。到现在为止,您应该对此很熟悉了,因为它与端口仲裁的概念相同,甚至使用相同的仲裁选项,包括 TBWRR。VC 仲裁选项也与单功能 VC 寄存器中的相同。

**271**

**PCI Ex ress Technolo p gy**

_Figure 7‐22: 多功能仲裁中的 QoS 支持_

**==> picture [330 x 336] intentionally omitted <==**

**----- Start of picture text -----**<br>
Extended Capability Header Cnt<br>Port VC Capability 1 Ext. VC Count<br>VAT Offset Port VC Capability 2<br>Port VC Status Port VC Control<br>Func 0 Offset VC Resource Cap (0)<br>VC Resource Control (0)<br>VC Resource Status (0) RsvdP<br>Func n Offset VC Resource Cap (n)<br>VC Resource Control (n)<br>VC Resource Status (n) RsvdP<br>VC Arbitration Table (VAT)<br>Function Arbitration Table 0<br>Function Arbitration Table n<br>Function<br>Function 0 仲裁器<br>MFVC 端口 1<br>功能 VC0<br>0008h 内部链路<br>端口 2 VC0 VC 仲裁器<br>VC<br>功能 VC0<br>0009h<br>出口<br>端口<br>Function 1<br>端口 1<br>VC7<br>内部链路<br>VC 端口 2 VC7<br>功能 VC7<br>0009h<br>TC/VC 映射<br>**----- End of picture text -----**<br>


## **等时支持 (Isochronous Support)**

如前所述,并非每台机器或应用程序都需要等时支持,但有些机器或应用程序没有它就无法工作。由于 PCIe 从一开始就设计为支持它,让我们考虑一下要使其工作需要满足哪些条件。

**272**

**第 7 章:服务质量**

## **时序就是一切 (Timing is Everything)**

考虑图 7-23 (第 274 页) 所示的示例,此处需要同步连接但无法实现。相反,我们用等时机制模拟同步路径。在此示例中,等时性定义了在每个服务间隔 (Service Interval) 内将传送的数据量,以实现所需的服务。以下顺序描述了该操作:

1. 同步源(摄像机和 PCI Express 接口)在第一个相等的服务间隔 (SI 1) 期间将数据累积在缓冲区 A 中。

2. 摄像机在下一个服务间隔 (SI 2) 期间通过通用总线传送所有累积的数据,同时在缓冲区 B 中累积下一块数据。

   - 显然,系统必须能够保证缓冲区 A 的全部内容可以在服务间隔内传送,无论链路上是否有其他流量在传输。这是通过为时间敏感的数据包分配高优先级并编程仲裁方案来实现的,以便在与其他流量竞争时优先处理这些数据包。另请注意,只要所有数据都在时间窗口内传送,那么它确切何时到达并不重要。它可以分散在整个间隔内,也可以集中在一个位置内。只要它在服务间隔内全部传送,仍然可以满足保证。

3. 在 SI 2 期间,磁带录像机接收并缓冲传入数据,然后可以在 SI 3 期间将其传送到存储器进行记录。摄像机在 SI 3 期间将缓冲区 B 卸载到链路上,同时将新数据累积到缓冲区 A 中,如此循环往复。

**273**

**PCI Ex ress Technolo p gy**

_Figure 7‐23: 等时事务的示例应用_

**==> picture [298 x 281] intentionally omitted <==**

**----- Start of picture text -----**<br>
摄像机 (Camera)<br>SI 1 数据累积<br>在缓冲区 A 中<br>SI 2 从缓冲区 A 传送数据<br>同时下一批数据<br>在缓冲区 B 中累积<br>SI 3 从缓冲区 B 传送数据<br>同时下一批数据<br>在缓冲区 A 中累积<br>PCI Express<br>接口<br>SI 1 SI 2 SI 3<br>服务间隔 (SI)<br>SI 2 数据接收到<br>缓冲区 A<br>SI 3 从缓冲区 A 传送数据<br>到存储器<br>同时数据接收到<br>缓冲区 B<br>存储器 (例如:磁带)<br>缓冲区 A 缓冲区 B<br>缓冲区 A 缓冲区 B<br>**----- End of picture text -----**<br>


## **时序如何定义 (How Timing is Defined)**
