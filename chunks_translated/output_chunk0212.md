## **PCI Express Technology** 

地址,另一个保存发往目标或来自目标的数据。对地址寄存器执行写操作,随后对数据寄存器执行读或写操作,会向目标功能的相应内部地址发起一次读或写事务。这巧妙地解决了地址空间有限的问题,但这意味着完成一次配置访问需要两次 IO 访问。

PCI 兼容 (PCI-Compatible) 机制使用根复合体 (Root Complex) 主桥 (Host Bridge) 中的两个 32 位 IO 端口。它们是 **配置地址端口 (Configuration Address Port)**,位于 IO 地址 0CF8h - 0CFBh,以及 **配置数据端口 (Configuration Data Port)**,位于 IO 地址 0CFCh - 0CFFh。

访问功能的 PCI 兼容配置寄存器的过程如下:首先将目标总线 (Bus)、设备 (Device)、功能 (Function) 和双字 (dword) 编号写入配置地址端口,并在此过程中设置其使能位 (Enable bit)。其次,向配置数据端口发起一次 1 字节、2 字节或 4 字节的 IO 读或写操作。根复合体中的主桥将所指定的目标总线与其下游总线范围进行比较。如果目标总线在该范围内,则桥将发起一次配置读或写请求 (具体取决于对配置数据端口的 IO 访问是读还是写)。
