## **总线比较与数据端口使用** 

根复合体 (Root Complex) 内部的主桥 (Host Bridge)（如图 3-5 所示，位于第 95 页）实现了一个 Secondary Bus Number 寄存器和一个 Subordinate Bus Number 寄存器。Secondary Bus Number 是紧邻该桥下方的总线编号。Subordinate Bus Number 是位于该桥下游的目标总线编号。 

在单一根复合体 (Root Complex) 系统中，该桥的 Secondary Bus Number 寄存器可能被硬连线为 0，可能是一个读/写寄存器（复位时强制为 0），或者它可能仅隐式地知道第一个可访问的总线将是 Bus 0。如果配置地址端口 (Configuration Address Port)（参见第 92 页图 3-4）中的第 31 位被设置为 1b，则该桥会将目标总线编号与其下游存在的总线范围进行比较。 

当看到一个请求 (Request) 时，桥会评估目标总线编号是否在下游总线编号的范围内，即从 Secondary Bus Number 的值到 Subordinate Bus Number 的值（含两端）。如果目标总线与 Secondary Bus 匹配，则该总线被作为目标，请求将作为 Type 0 配置请求 (Type 0 Configuration Request) 传递。当设备看到 Type 0 请求时，它们知道该总线上本地的设备是目标设备（而不是该总线下游某条下级总线上的设备）。 

如果目标总线号大于桥的 Secondary Bus Number，但小于或等于桥的 Subordinate Bus Number，则该请求将作为 Type 1 配置请求 (Type 1 configuration request) 在桥的次级总线上转发。Type 1 配置访问的含义是：尽管该请求必须穿越此总线，但它的目标并不是该总线上的设备。相反，该请求将

**93** 
