2. 组仲裁 (Group Arbitration) — VC 由硬件划分为一个低优先级组和一个高优先级组。低优先级组使用由软件从可用选项中选择的仲裁方法,而高优先级组则始终使用严格优先级仲裁 (Strict Priority)。

3. 硬件固定仲裁 (Hardware Fixed arbitration) — 内置于硬件中的方案。

**252**

**第 7 章:服务质量 (Quality of Service)**

_Figure 7‐6: VC 仲裁示例_

**==> picture [246 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>VC1 VC0<br>根复合体 (Root Complex)<br>内存<br>TC/VC 映射<br>本例中的 VC 仲裁<br>产生 3:1 的比例<br>用于传输 VC1 和 VC0<br>仲裁器 (Arbiter)<br>VC1 VC0<br>TC/VC 映射<br>设备<br>核心<br>**----- End of picture text -----**<br>


## **严格优先级 VC 仲裁 (Strict Priority VC Arbitration)**

默认的优先级方案基于 VC ID 的固有优先级 (VC0=最低优先级,VC7=最高优先级)。该机制是自动的,无需配置。图 7-7 (第 254 页) 展示了一个包含所有 VC 的严格优先级仲裁示例。VC ID 决定了事务发送的顺序。使用严格优先级仲裁的最大 VC 数量不能大于 _Extended VC Count_ 字段的值。

**253**

**PCI Ex ress Technolo p gy**

(参见第 251 页的图 7-5。)此外,如果设计者已对所有受支持的 VC 选择了严格优先级仲裁,则 Port VC Capability Register 1 的 _Low Priority Extended VC Count_ 字段被硬连线为零。(参见第 255 页的图 7-8。)

_Figure 7‐7: 严格优先级仲裁_

|VC 资源|优先级顺序|优先级顺序|
|---|---|---|
|第 8 个 VC|VC7|最高|
|第 7 个 VC|VC6||
|第 6 个 VC|VC5||
|第 5 个 VC|VC4||
|第 4 个 VC|VC3||
|第 3 个 VC|VC2||
|第 2 个 VC|VC1||
|第 1 个 VC|VC0|最低|
||||



严格优先级要求高编号的 VC 始终优先于低优先级 VC。例如,如果所有八个 VC 都由严格优先级管理,则只有当没有其他 VC 有待发数据包时,VC0 中的数据包才能被发送。这实现了以最小延迟为最高优先级数据包提供非常高带宽的目标。然而,严格优先级有可能使低优先级通道的带宽出现饥饿,因此必须谨慎处理以确保这种情况不会发生。规范要求调节高优先级流量以避免饥饿,并给出了两种可能的调节方法:

- 发起端口可以限制高优先级数据包的注入速率,以便为低优先级事务提供更多带宽。

- 交换机可以在出口端口调节多个流量流。该方法可能会限制来自高带宽应用和试图超出可用带宽限制的设备的吞吐量。

设备设计者还可以通过将 VC 拆分为低优先级组和高优先级组来限制参与严格优先级的 VC 数量,具体将在下一节中讨论。

**254**

**第 7 章:服务质量**

## **组仲裁 (Group Arbitration)**

图 7-8 展示了 VC Capability Register 1 中的 _Low Priority Extended VC Count_ 字段。该只读字段指定一个 VC ID,用于标识本设备低优先级仲裁组的上限。例如,如果该值为 4,则 VC0-VC4 是低优先级组的成员,VC5-VC7 属于高优先级组。注意 _Low Priority Extended VC Count_ 为 7 表示不使用严格优先级。

_Figure 7‐8: 低优先级扩展 VC_

**==> picture [333 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header 00h<br>Port VC Capability Register 1  04h<br>Port VC Capability Register 2  08h<br>Port VC Status Register  Port VC Control Register  0Ch<br>PAT Offset VC0 Resource Capability Register  10h<br>VC0 Resource Control Register  14h<br>VC0 Resource Status Reg  Reserved 18h<br>PAT Offset VCn Resource Capability Register  10h+(n*0Ch)<br>VCn Resource Control Register  14h+(n*0Ch)<br>VCn Resource Status Reg  Reserved 18h+(n*0Ch)<br>n = one of the extended VCs<br>31          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP<br>Port Arbitration Table Entry Size<br>Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>**----- End of picture text -----**<br>


**255**

**PCI Ex ress Technolo p gy**

如图 7-10 (第 257 页) 所示,高优先级 VC 继续使用严格优先级仲裁,而低优先级仲裁组使用该设备支持的其他仲裁方法之一。VC Capability Register 2 报告了该组支持哪些替代方法,如图 7-9 所示,VC Control Register 允许选择要使用的方法。低优先级仲裁方案包括:

- 基于硬件的固定仲裁 (Hardware Based Fixed Arbitration)

- 加权轮询仲裁 (Weighted Round Robin Arbitration, WRR)

_Figure 7‐9: VC 仲裁能力_

**==> picture [304 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                     24  23                            8 7                        0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>7                       4   3     2     1     0<br>RsvdP<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>**----- End of picture text -----**<br>


**==> picture [193 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Control Register<br>15                                 4  3     1 0<br>RsvdP<br>VC Arbitration Select (000b-111b)<br>Load VC Arbitration Table<br>**----- End of picture text -----**<br>


**256**

**第 7 章:服务质量**

_Figure 7‐10: VC 仲裁优先级_

|VC 资源|VC ID|||分割优先级||
|---|---|---|---|---|---|
|||||最高||
|第 8 个 VC|VC7|||||
|第 7 个 VC|VC6||高优先级(严格优先级方案)|||
|第 5 个 VC<br>第 6 个 VC|VC5<br>VC4|||低优先级 VC ID = 4||
|第 4 个 VC|VC3|||||
|第 3 个 VC|VC2||低优先级(替代优先级方案)<br>(由软件选择)|||
|第 2 个 VC|VC1|||||
|第 1 个 VC|VC0|||最低||


## **硬件固定仲裁方案 (Hardware Fixed Arbitration Scheme)**

此选择定义了一种基于硬件的方法,无需额外的软件设置。该方法可以是硬件设计者选择构建的任何方案,可以基于设备的预期负载或带宽需求。一个简单的例子可能是普通的轮询序列,其中每个 VC 在轮转过程中有平等的发送数据包机会。

## **加权轮询仲裁方案 (Weighted Round Robin Arbitration Scheme)**

在此方案中,某些 VC 可以被赋予比其他的更高的权重(给予更高的优先级),方法是在序列中给予它们比其他 VC 更多的条目。规范定义了三种 WRR 选项,每种具有不同数量的条目(称为阶段 phase)。表大小通过在 Port VC Control Register 的 _VC Arbitration Select_ 字段中写入相应的值来选择(参见第 256 页的图 7-9)。表中的每个条目表示一个阶段,软件用低优先级 VC 编号加载该阶段。VC 仲裁器将以顺序方式反复扫描所有表条目,并从表条目中指定的 VC 发送数据包。一旦数据包被发送,仲裁器立即继续到下一阶段。

**257**

**PCI Ex ress Technolo p gy**

图 7-11 (第 258 页) 展示了具有 64 个条目的 WRR 仲裁表示例。

_Figure 7‐11: WRR VC 仲裁表_

**==> picture [165 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Phase VC ID<br>0 VC 4<br>1 VC 3<br>2 255 (16KB)VC 2<br>3 VC 1<br>4 VC 4<br>5 VC 3<br>6 VC 0<br>7 64 (4KB)VC 4<br>8 VC 3<br>9 128 (8KB)VC 2<br>10 VC 1<br>1111 VC 4<br>621 VC 3<br>632 VC 0<br>Arbitration Logic Scans Table Entries<br>**----- End of picture text -----**<br>


## **设置虚拟通道仲裁表 (Setting up the Virtual Channel Arbitration Table)**

VC 仲裁表 (VAT) 在配置空间中的位置以 VC Capability Structure 的基地址作为偏移给出,如图 7-12 (第 259 页) 所示。

如图 7-13 (第 260 页) 所示,VAT 中的每个条目都是一个 4 位字段,标识在该阶段被调度传送数据的缓冲区的 VC 编号。表长度由图 7-9 (第 256 页) 所示的仲裁选项选择。

**258**

**第 7 章:服务质量**

_Figure 7‐12: VC 仲裁表偏移和加载 VC 仲裁表字段_

**==> picture [331 x 385] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Capability Register 2<br>31                     24  23                                             8 7                      0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>0d<br>Header<br>CapPtr<br>63d<br>PCICompatible<br>PCIe Cap Structure (CapID=10h) Space<br>255d<br>PCIEXEnhancedCapabilityRegister<br>PortVCCapRegister1 ExtVCCnt<br>VATOffset PortVCCapRegister2<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VC0 Resource Cap Reg<br>VC Resource Control Register PCIEXExtended<br>VC Resource Status Reg Reserved CapabilitySpace<br>PATnOffset VCn Resource Cap Reg<br>VC Resource Control Register<br>VC Resource Status Reg Reserved<br>VC Arbitration Table (VAT)<br>4095d<br>**----- End of picture text -----**<br>


表由配置软件加载,以实现虚拟通道所需的优先级顺序。每当对表进行任何更改时,硬件都会设置 _VC Arbitration Table Status_ 位,为软件提供一种方法来验证是否已进行更改但尚未应用于硬件。表加载完成后,软件设置 _Load VC Arbitration Table_ 位

**259**

## **PCI Ex ress Technolo p gy**

在 Port VC Control 寄存器中。这会导致硬件将新值加载(或应用)到 VC 仲裁器。表加载完成时,硬件清除 _VC Arbitration Table Status_ 位,向软件发出加载完成的信号。这种方法的动机可能是希望在运行时更改表内容而不会造成中断。问题在于配置写入一次只能更新一个 dword,并且是相对较慢的事务,这意味着完成更改可能需要很长时间,在此期间表仅部分更新。这反过来又可能导致设备在操作过程中出现意外行为。为避免这种情况,此机制允许软件完成对表的所有更改,然后一次性将所有更改应用到硬件仲裁器。

_Figure 7‐13: 加载 VC 仲裁表条目_

|32 阶段虚拟通道仲裁表|32 阶段虚拟通道仲裁表|32 阶段虚拟通道仲裁表|32 阶段虚拟通道仲裁表|||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|31       28 27      24 23      20 19<br>16 15       12 11|8||7|4|3|||0||||
|Phase[2]<br>Phase[3]<br>Phase[4]<br>Phase[5]<br>Phase[6]<br>Phase[7]|||Phase[1]||Phase[0]||||||00h|
|Phase[10]<br>Phase[11]<br>Phase[12]<br>Phase[13]<br>Phase[14]<br>Phase[15]|||Phase[9]||Phase[8]||||||04h|
|Phase[18]<br>Phase[19]<br>Phase[20]<br>Phase[21]<br>Phase[22]<br>Phase[23]|||Phase[17]||Phase[16]||||||08h|
|Phase[26]<br>Phase[27]<br>Phase[28]<br>Phase[29]<br>Phase[30]<br>Phase[31]|||Phase[25]||Phase[24]|||||0Ch||
|<br>1. 配置软件加载 VC 仲裁表。<br>2. 当任何|3||2|1||0||||||
|表条目被更新时设置 VC 仲裁表状态位。|RsvdP|||VC ID||||||||
|3. 软件设置 Load VC Arbitration Table 位。||||||||||||
|4. 硬件将表内容应用于 VC 仲裁器。||||||||||||
|5. 硬件清除 VC 仲裁表状态位。||||||||||||
