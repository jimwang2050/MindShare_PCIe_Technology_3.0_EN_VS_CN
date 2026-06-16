在 PCIe 中我们有同样的问题，但过程略有不同。首先，PCIe 功能在其暂时无法响应配置访问时，必须始终给出具有特定状态的完成，即配置请求重试状态 (Configuration Request Retry Status, CRS)。此状态仅在响应配置请求时合法，如果在响应其他请求时看到，则可以（可选地）将其视为畸形数据包 (Malformed Packet) 错误。此响应在复位后的一秒钟内才有效，因为该功能应在此时响应，如果不会则可视为故障。

根复合体处理响应配置读请求的 CRS 完成的方式是实现特定的，除了系统复位后的时间段。在该时间段内，根据其根控制寄存器 (Root Control Register) 中 CRS 软件可见性 (CRS Software Visibility) 位的设置，根复合体下一步有两个选择（参见第 108 页图 3-11）：

- 如果该位被置位且请求是对 Vendor ID 寄存器的两个字节的配置读（如枚举访问将执行的操作以发现功能是否存在），则根必须为此寄存器向主机提供 0001h 的人工值，并且对于此请求中的任何其他字节返回全 1。此 Vendor ID 不用于任何实际设备，将被软件解释为访问此设备可能存在较长延迟的指示。这可能很有用，因为软件可以选择转到另一个任务，并更好地利用原本用于等待设备响应的时间，稍后再返回查询此设备。为此，软件必须确保在复位条件后对某功能的首次访问是对 Vendor ID 两个字节的配置读。

- 对于配置写或任何其他配置读，根必须自动作为新请求重新发出配置请求。

**107**

**PCI Express 技术**

_图 3-11：PCIe 能力块中的根控制寄存器_

**==> picture [360 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 5 4 3 2 1 0<br>RsvdP<br>CRS 软件可见性使能<br>PME 中断使能<br>系统致命错误使能<br>系统不可纠正错误使能<br>系统可纠正错误使能<br>**----- End of picture text -----**<br>


## **确定功能是端点还是桥**

枚举过程的关键部分是能够确定功能是桥还是端点。如第 108 页图 3-12 所示，Header Type 寄存器（配置空间头中的偏移 0Eh）的低 7 位标识该功能的基本类别，定义了三个值：

- 0 = 不是桥（在 PCIe 中为端点 (Endpoint)）

- 1 = PCI-to-PCI 桥 (P2P)，连接两条总线

- 2 = CardBus 桥（传统接口，今天不常使用）

在第 87 页图 3-1 中，每个虚拟 P2P 中的 Header Type 字段（DW3，byte 2）将返回值 1，PCI Express-to-PCI 桥（总线 8，设备 0）也是，而端点将返回零的 Header Type。

_图 3-12：Header Type 寄存器_

**==> picture [189 x 84] intentionally omitted <==**

**----- Start of picture text -----**<br>
7   6                                0<br>Header Type<br>配置头格式<br>0 = 单功能设备<br>1 = 多功能设备<br>**----- End of picture text -----**<br>


**108**

**第 3 章：配置概述**

## **单根枚举示例**

现在我们已经讨论了枚举过程中涉及的基本元素，让我们通过一个示例过程走一遍。第 113 页图 3-13 说明了对总线和设备进行枚举之后的示例系统。下面的讨论假设配置软件使用本章中定义的两种配置访问机制中的任何一种来实现此结果。在启动时，处理器上执行的配置软件按如下所述执行枚举。

1. 软件将 Host/PCI 桥的二级总线号 (Secondary Bus Number) 更新为零，将下属总线号 (Subordinate Bus Number) 更新为 255。将其设置为最大值意味着在识别出所有下游总线号之前不必再次更改它。此时，总线 0 到 255 被标识为下游。

2. 从设备 0（桥 A）开始，枚举软件尝试从总线 0 上 32 个可能设备的每个功能 0 读取 Vendor ID。如果从总线 0、设备 0、功能 0 返回有效的 Vendor ID，则该设备存在并至少包含一个功能。如果没有，请继续探测总线 0、设备 1、功能 0。

3. 在本例中（图 3-12，第 108 页），Header Type 字段包含值一（01h），表示这是 PCI-to-PCI 桥。Header Type 寄存器中的多功能位（bit 7）为 0，表示功能 0 是该桥中唯一的功能。_规范并不排除在此设备内实现多个功能，并且这些功能中的每一个又可以代表其他虚拟 PCI-to-PCI 桥，甚至是非桥功能。_

4. 现在软件已找到一个桥，执行一系列配置写入以设置桥的总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 0

   - Secondary Bus Number 寄存器 = 1

   - Subordinate Bus Number 寄存器 = 255

   - 该桥现在知道直接连接在下游的总线号为 1（Secondary Bus Number = 1），其下游的最大总线号为 255（Subordinate Bus Number = 255）。

5. 枚举软件必须执行深度优先搜索。在继续发现总线 0 上的其他设备/功能之前，它必须继续搜索总线 1。

6. 软件读取总线 1、设备 0、功能 0 的 Vendor ID，这在本例中针对桥 C。返回有效的 Vendor ID，表明总线 1 上存在设备 0、功能 0。

7. Header 寄存器中的 Header Type 字段包含值一（0000001b），表示另一个 PCI-to-PCI 桥。和之前一样，bit 7 为 0，

**109**

**PCI Express Technology**

表示桥 C 是单功能设备。

8. 软件现在执行一系列配置写入以设置桥 C 的总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 1

   - Secondary Bus Number 寄存器 = 2

   - Subordinate Bus Number 寄存器 = 255

9. 继续进行深度优先搜索，从总线 2、设备 0、功能 0 的 Vendor ID 寄存器执行读取。本例假设桥 D 是总线 2 上的设备 0、功能 0。

10. 返回有效的 Vendor ID，表明总线 2、设备 0、功能 0 存在。

11. Header 寄存器中的 Header Type 字段包含值一（0000001b），表示这是 PCI-to-PCI 桥，bit 7 为 0，表示桥 D 是单功能设备。

12. 软件现在执行一系列配置写入以设置桥 D 的总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 2

   - Secondary Bus Number 寄存器 = 3

   - Subordinate Bus Number 寄存器 = 255

13. 继续进行深度优先搜索，从总线 3、设备 0、功能 0 的 Vendor ID 寄存器执行读取。

14. 返回有效的 Vendor ID，表明总线 3、设备 0、功能 0 存在。

15. Header 寄存器中的 Header Type 字段包含值零（0000000b），表示这是一个端点功能。由于这是端点而不是桥，它具有 Type 0 头，并且其下面没有 PCI 兼容的总线。这次，bit 7 为 1，表示这是多功能设备。

16. 枚举软件对总线 3、设备 0 上所有 8 个可能功能进行 Vendor ID 访问，并确定除了功能 0 之外只有功能 1 存在。功能 1 也是端点（Type 0 头），因此此设备下没有其他总线。

17. 枚举软件继续在总线 3 上扫描以查找设备 1 - 31 上的有效功能，但没有找到其他功能。

18. 在找到桥 D 下游的每个功能后，枚举软件将桥 D 更新为真实的 Subordinate Bus Number 3。然后它向上一级（回到总线 2），并继续在该总线上扫描以查找有效功能。本例假设桥 E 是总线 2 上的设备 1、功能 0。

19. 返回有效的 Vendor ID，表明此功能存在。

20. 桥 E 的 Header 寄存器中的 Header Type 字段包含值一（0000001b），表示这是 PCI-to-PCI 桥，bit 7 为 0，表示单功能设备。

**110**

**第 3 章：配置概述**

21. 软件现在执行一系列配置写入以设置桥 E 的总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 2

   - Secondary Bus Number 寄存器 = 4

   - Subordinate Bus Number 寄存器 = 255

22. 继续进行深度优先搜索，从总线 4、设备 0、功能 0 的 Vendor ID 寄存器执行读取。

23. 返回有效的 Vendor ID，表明此功能存在。

24. Header 寄存器中的 Header Type 字段包含值零（0000000b），表示这是端点设备，bit 7 为 0，表示这是单功能设备。

25. 枚举软件扫描总线 4 以查找设备 1 - 31 上的有效功能，但没有找到其他功能。

26. 在到达该树分支的底部后，枚举软件将本例中该总线上方的桥 E 更新为真实的 Subordinate Bus Number 4。然后它向上一级（回到总线 2），并继续读取下一个设备（设备 2）的 Vendor ID。本例假设总线 2 上未实现设备 2 - 31，因此没有在总线 2 上发现其他设备。

27. 枚举软件将总线 2 上方的桥（本例中为 C）更新为真实的 Subordinate Bus Number 4，并返回到上一级总线（总线 1），并尝试读取下一个设备（设备 1）的 Vendor ID。本例假设总线 1 上未实现设备 1 - 31，因此没有在总线 1 上发现其他设备。

28. 枚举软件将总线 1 上方的桥（本例中为 A）更新为真实的 Subordinate Bus Number 4，并返回到上一级总线（总线 0），并继续读取下一个设备（设备 1）的 Vendor ID。本例假设桥 B 是总线 0 上的设备 1、功能 0。

29. 以与之前描述的相同方式，枚举软件发现桥 B 并执行一系列配置写入以设置桥 B 的总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 0

   - Secondary Bus Number 寄存器 = 5

   - Subordinate Bus Number 寄存器 = 255

30. 然后发现桥 F 并执行一系列配置写入以设置其总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 5

   - Secondary Bus Number 寄存器 = 6

   - Subordinate Bus Number 寄存器 = 255

31. 然后发现桥 G 并执行一系列配置写入以设置其总线号寄存器，如下所示：

**111**

**PCI Express Technology**

   - Primary Bus Number 寄存器 = 6

   - Secondary Bus Number 寄存器 = 7

   - Subordinate Bus Number 寄存器 = 255

32. 在总线 7、设备 0、功能 0 处发现单功能端点设备，因此桥 G 的 Subordinate Bus Number 被更新为 7。

33. 然后发现桥 H 并执行一系列配置写入以设置其总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 6

   - Secondary Bus Number 寄存器 = 8

   - Subordinate Bus Number 寄存器 = 255
