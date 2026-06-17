```
mov dx,0CF8h;set dx = config address port address
mov eax,80040000h;enable=1, bus 4, dev 0, func 0, DW 0
out dx,eax;IO write to set up address port
mov dx,0CFCh; set dx = config data port address
in ax,dx;2-byte read from config data port
```

1. `out` 指令从处理器生成对根复合体 (Root Complex) 主机桥中配置地址端口 (Configuration Address Port) (0CF8h) 的 IO 写，如第 92 页图 3-4 所示。

2. 主机桥将配置地址端口中指定的目标总线号 (4) 与其下游的总线范围 (0 至 10) 进行比较。目标总线落在该范围内，因此桥已被预置为下一个配置请求的目标。

3. `in` 指令生成从处理器对根复合体 (Root Complex) 主机桥中配置数据端口 (Configuration Data Port) 的 IO 读事务。这是从配置数据端口前两个位置进行的 2 字节读取。

4. 由于目标总线不是总线 0，主机/PCI 桥在总线 0 上发起 Type 1 配置读。

5. 总线 0 上的所有设备锁存该事务请求，并看到这是一个 Type 1 配置请求 (Type 1 Configuration Request)。因此，根复合体中的两个虚拟 PCI-to-PCI 桥都将 Type 1 请求中的目标总线号与各自下游的总线范围进行比较。

6. 目标总线 (4) 位于左侧桥的下游总线范围内，因此它将该数据包传递到其二级总线 (secondary bus)，但仍作为 Type 1 请求，因为目标总线不匹配二级总线号 (Secondary Bus Number)。

7. 左侧交换机的上游端口 (upstream port) 接收该数据包并将其传送到上游 PCI-to-PCI 桥。

8. 该桥确定目标总线位于其下方，但目标不是其二级总线，因此将数据包作为 Type 1 请求传递到总线 2。

9. 总线 2 上的两个桥都接收 Type 1 请求数据包。右侧桥确定目标总线匹配其二级总线号 (Secondary Bus Number)。

**102**

**第 3 章：配置概述**

10. 该桥将配置读请求传递到总线 4，但将其转换为 Type 0 配置读 (Type 0 Configuration Read) 请求，因为该数据包已到达目标总线（目标总线号匹配二级总线号）。

11. 总线 4 上的设备 0 接收该数据包，并解码目标设备、功能和寄存器号字段以在其配置空间中选择目标双字 (dword)（见第 90 页图 3-3）。

12. 第一个双字字节使能 (First Dword Byte Enable) 字段中的位 0 和位 1 被置位，因此该功能在完成包 (Completion packet) 中返回其前两个字节（本例中为 Vendor ID）。完成包使用从 Type 0 请求包中获取的请求者 ID (Requester ID) 字段路由到主机桥。

13. 读取数据的两个字节被传送到处理器，从而完成 `in` 指令的执行。Vendor ID 被放入处理器的 AX 寄存器中。

## **增强配置访问示例**

请参考第 104 页图 3-9。以下 x86 代码示例使根复合体 (Root Complex) 执行对总线 4、设备 0、功能 0、寄存器 0 (Vendor ID) 的读。在该操作能够工作之前，必须为主机桥分配一个基地址值。本例假设 256MB 对齐的增强配置内存映射范围的基地址为 E0000000h：

```
mov ax,[E0400000h];memory-mapped Config read
```

- 地址位 63:28 表示整个增强配置地址范围 256MB 对齐基地址的高 36 位（本例中为 00000000 E0000000h）。

- 地址位 27:20 选择目标总线（本例中为 4）。

- 地址位 19:15 选择总线上目标设备（本例中为 0）。

- 地址位 14:12 选择设备内的目标功能 (Function)（本例中为 0）。

- 地址位 11:2 选择所选功能配置空间内的目标双字 (dword)（本例中为 0）。

- 地址位 1:0 定义所选双字内的起始字节位置（本例中为 0）。

处理器启动从内存位置 E0400000h 开始的 2 字节内存读，该请求被根复合体 (Root Complex) 中的主机桥锁存。主机桥识别出该地址与配置指定的区域匹配，并为双字 0、功能 0、设备 0、总线 4 的前两个字节生成配置读请求 (Configuration Read Request)。其余操作与上一节中描述的相同。

**103**

## **PCI Express 技术**

_图 3-9：配置读访问示例_

**==> picture [266 x 367] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bus = 0 Bridge<br>Sub = 10<br>Bus 0<br>Pri = 0 Pri = 0<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 10 P2P<br>Bus 1 Bus 5<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 10<br>Bus 2 P2P Bus 6 P2P<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 10<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 10<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 0 Function 0 Function 0<br>Pri = 8 Express<br>Sec = 9 PCI<br>Sub = 9 Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>**----- End of picture text -----**<br>


## **枚举 - 发现拓扑**

系统复位或上电后，配置软件必须扫描 PCIe 结构以发现机器拓扑并了解结构的填充情况。在那发生之前，如第 105 页图 3-10 所示，软件唯一可以确定的事情是将会存在一个主机/PCI 桥，并且

**104**

**第 3 章：配置概述**

该桥的二级侧上将存在总线号 0。请注意，桥的上游侧称其为主总线 (primary bus)，而下游侧称为二级总线 (secondary bus)。扫描 PCI Express 结构以发现其拓扑的过程称为 _枚举过程_。

_图 3-10：启动时的拓扑视图_

**==> picture [238 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex has bus<br>number zero assigned.<br>Processor The remaining topology<br>have yet to be discovered<br>and numbered.<br>Host/PCI<br>Bridge<br>Bus 0<br>? ? ? ? ? ? ? ?<br>**----- End of picture text -----**<br>


## **发现功能的存在或缺失**

处理器上执行的配置软件通常通过读取其 Vendor ID 寄存器来发现功能 (Function) 的存在。PCI-SIG 为每个供应商分配一个唯一的 16 位值，该值被硬连线到该供应商设计的每个功能的 Vendor ID 寄存器中。通过在系统中所有可能的总线、设备和功能号组合中读取该寄存器，枚举软件可以搜索整个拓扑以了解哪些设备存在。此过程相当简单，但可能出现两个问题：目标设备可能不存在，或者目标设备存在但未准备好响应。这两种情况的处理如下所述。

## **设备不存在**

在发现过程中，目标设备实际上不存在于系统中的情况可能发生多次，正确理解这一点非常重要。在 PCI 中，配置读请求 (Configuration Read Request) 将在总线上超时并产生主中止 (Master Abort) 错误条件。由于没有设备驱动总线且所有信号都被上拉，总线上的数据位将被视为全 1，并成为所看到的数据值。得到的 Vendor ID 为 FFFFh 是保留值。如果枚举软件看到读取的该结果，则表明设备不存在。由于这不是真正的错误条件，因此在枚举过程中主中止 (Master Abort) 不会被报告为错误。

**105**

## **PCI Express 技术**

对于 PCIe，对不存在的设备的配置读请求 (Configuration Read Request) 将导致目标设备上方的桥返回具有 UR (Unsupported Request) 状态的无数据完成包 (Completion)。为了与传统枚举模型向后兼容，当在枚举期间看到此完成包时，根复合体 (Root Complex) 向处理器返回全 1 (FFFFh) 作为数据。请注意，枚举软件依赖于在探测系统中功能 (Function) 的存在时，对返回 Unsupported Request 的配置读请求接收全 1 的值。

重要的是要避免在这种情况下意外地报告错误。尽管此超时或 UR 结果在运行时将被视为错误，但它是预期结果，在枚举期间不视为错误。为帮助避免这种混淆，设备通常要到稍后才会被启用以发出错误信号。对于 PCIe，记录此事件仍然可能很有用，这就是为什么 PCIe 能力寄存器块 (Capability register block) 中提供了第四个"错误"状态位，称为不支持请求状态 (Unsupported Request Status) 位（有关更多详细信息，请参阅第 678 页的"启用/禁用错误报告"）。这允许记录此条件但不将其标记为错误，这很重要，因为检测到的错误可能会停止枚举过程以调用系统错误处理程序。错误处理软件在此期间可能只具有有限的能力，因此可能难以解决问题。枚举软件在这种情况下可能会失败，因为它通常编写为在操作系统或其他错误处理软件可用之前执行。为避免此风险，在枚举期间通常不应报告错误。

## **设备未就绪**

可能出现的另一个问题是目标设备存在但尚未准备好响应配置访问。由于设备准备访问所需的时间，配置存在一个时序考虑因素。如果数据速率为 5.0 GT/s 或更低，则软件必须在复位后等待 100ms 才能发起配置请求 (Configuration Request)。如果速率高于 5.0 GT/s (Gen3 速度)，则软件必须等待链路训练完成 (Link training) 后 100ms 才能尝试此操作。较高速度需要更长延迟的原因是 Gen3 均衡过程 (Equalization Process) 在链路训练 (Link training) 期间可能需要很长时间（约 50ms 的数量级；有关此主题的更多信息，请参阅第 577 页的"链路均衡概述"）。

如 PCI 2.3 规范所定义，初始化时间 (Initialization Time, Trhfa - 复位高电平到首次访问的时间) 从 RST# 解除置位时开始，并在 2[25] 个 PCI 时钟后完成。

**106**

**第 3 章：配置概述**

这相当于整整一秒钟，在该时间内该功能 (Function) 正在为其首次配置访问做准备，并且该值已作为 1.0s (+50%/‐0%) 沿用至 PCIe。功能可以使用该时间通过从外部串行 EEPROM 加载内容来填充其配置寄存器，例如，这可能需要一段时间才能加载，并且该功能在完成之前将无法成功访问。在 PCI 中，如果在功能准备就绪之前看到配置访问，它有三种选择：忽略请求、重试请求或接受请求但推迟其响应直到完全准备好。最后一种响应可能会给热插拔 (Hot-plug) 系统带来麻烦，因为共享总线可能会停滞一秒钟，直到请求解析完成。
