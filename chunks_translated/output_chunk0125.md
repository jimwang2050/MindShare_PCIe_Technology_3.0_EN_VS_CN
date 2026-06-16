## **PCI-X 事务**

第 33 页的图 1‐16 显示了一个 PCI‐X 突发内存读事务的示例。请注意，PCI‐X 不允许在第一个数据相位之后插入等待状态。这是可行的，因为传输大小现在已在事务的 Attribute（属性）相位中提供给目标设备，所以目标设备确切地知道对其有什么要求。此外，大多数 PCI‐X 总线周期都是突发传输，并且数据通常以 128 字节块的形式传输。这些特性可以更高效地利用总线，并更好地管理设备缓冲。

**32**

**第 1 章：背景**

_图 1‐16：PCI‐X 突发内存读总线周期示例_

**==> picture [386 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
Idle（空闲）<br>Address Phase（地址相位）Attribute Phase（属性相位）Response Phase（响应相位）Data Phase（数据相位）Data Phase（数据相位）Data Phase（数据相位）Data Phase（数据相位）Turnaround Cycle（转向周期）<br>1 2 3 4<br>1 2 3 4 5 6 7 8 9 10<br>CLK<br>FRAME#<br>AD[31:0] Address（地址） ATTR Data-0 Data-1 Data-2 Data-3<br>C/BE#[3:0] Cmd ATTR<br>IRDY#<br>TRDY#<br>DEVSEL# DecodeA<br>Next to last transfer（倒数第二次传输）<br>**----- End of picture text -----**<br>