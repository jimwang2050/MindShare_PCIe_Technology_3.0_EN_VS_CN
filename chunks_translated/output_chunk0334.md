MSI (Memory Write) Transaction<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 1 1Fmt 0 0 0 0 0Type R TC R Attr R HT DT EP Attr0 0 AT 0 0 0 0 0 0 0 0 0 1Length<br>Last DW First DW<br>Byte 4 Requester ID Tag 0 0 0 0 1 1 1 1<br>Header<br>Byte 8 MSI Message Address [63:32]<br>Byte 12 MSI Message Address [31:0] 0 0<br>Byte 16 MSI Message Data 0000h Data<br>MSI Capability Structure<br>31 16 15 8 7 0<br>Message Control Next CapabilityPointer Capability ID(05h) DW0<br>Message Address [31:0] DW1<br>Message Address [63:32] DW2<br>Message Data DW3<br>**----- End of picture text -----**<br>


## **MSI-X 模型**

## **概述**

PCI 规范的 3.0 版增加了对 MSI-X 的支持，MSI-X 具有其自己的能力结构。MSI-X 的动机是希望缓解 MSI 的三个缺点：

- 每个 Function 32 个向量不足以用于某些应用程序。

- 仅有一个目标地址使得跨多个 CPU 静态分配中断变得困难。如果可以为每个向量分配唯一地址，则可以实现最大的灵活性。

**821**

**PCI Ex ress 3.0 Technolo p gy**

- 在某些平台（如基于 x86 的系统）中，中断的向量号指示其相对于其他中断的优先级。使用 MSI，可以为单个 Function 分配多个中断，但所有中断向量将是连续的，这意味着类似的优先级。如果来自该 Function 的某些中断应为高优先级而其他应为低优先级，则这不是一个好的解决方案。更好的方法是让软件为分配给该 Function 的每个中断指定一个唯一的向量（消息数据值），该值不必是连续的。

考虑到这些目标，很容易理解为每个向量分配目标地址和消息数据值以提供更多向量而实现的寄存器更改。

## **MSI-X 能力结构**

如图 17-17（第 822 页）所示，消息控制寄存器与 MSI 大不相同。有趣的是，即使 MSI-X 每个 Function 可以支持多达 2048 个向量，而 MSI 为 32 个，但 MSI-X 的配置寄存器数量实际上比 MSI 略少。这是因为向量信息不包含在此处。相反，它位于由 Table BIR（基地址指示符寄存器）指向的内存位置 (MMIO) 中，如图 17-18（第 824 页）所示。

_Figure 17-17: MSI-X Capability Structure_

**==> picture [326 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 8 7 0<br>
Message Control Next CapabilityPointer Capability ID(11h) DW0<br>
Table<br>
MSI-X Table Offset DW1<br>
BIR<br>
PBA<br>
Pending Bit Array (PBA) Offset BIR DW2<br>
(BIR = BAR Index Register)<br>
15 14 13 11 10 0<br>
Rsvd Table Size in N-1 (RO)<br>
Function Mask (RW)<br>
MSI-X Enable (RW)<br>
**----- End of picture text -----**<br>


**822**

**第 17 章：中断支持**

_Table 17-3: Format and Usage of MSI-X Message Control Register_

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|10:0|Table Size|Read-Only. This field indicates the number of inter‐<br>rupt messages (vectors) that this Function sup‐<br>ports. The value here is interpreted in an N-1<br>fashion, so a value of 0 means 1 vector. A value of 7<br>means 8 vectors. Each vector has its own entry in<br>the MSI-X Table and its own bit in the Pending Bit<br>Array.|
|13:11|Reserved|Read-Only. Always zero.|
|14|Function Mask|Read/Write. This field provides system software an<br>easy way to mask all the interrupts from a Func‐<br>tion. If this bit is cleared, interrupts can still be<br>masked individually by setting the mask bit within<br>each vector's MSI-X table entry.|
|15|MSI-X Enable|Read/Write. State after reset is 0, indicating that the<br>device's MSI-X capability is disabled.<br>• **0**= Function is**disabled**from using**MSI-X**. It<br>must use MSI or INTx Messages.<br>• **1**= Function is**enabled**to use**MSI-S**to request<br>service and won't use MSI-X or INTx Messages.|


**823**

**PCI Ex ress 3.0 Technolo p gy**

## _Figure 17-18: Location of MSI-X Table_

**==> picture [332 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
Doubleword<br>
Byte (in decimal)Number Syste Memory Address Space m Memory<br>
3 2 1 0<br>
Device Vendor 00<br>
ID ID<br>
Status Command 01<br>
Register Register<br>
Class Code Revision 02<br>
ID<br>
BIST HeaderType LatencyTimer CacheLineSize 03<br>
Base A ddress 0 04<br>
Base A ddress 1 05 Table BIR = 2<br>
MSI-X Table<br>
Base A ddress 2 06<br>
Base A ddress 3 07<br>
08<br>
Base A ddress 4 MSI-X Table<br>
Base A ddress 5 09 Offset<br>
10<br>
CardBus CIS Pointer<br>
Subsystem ID SubsystemVendor ID 11<br>
Expansion R OM 12<br>
Base Ad dress<br>
Reserved Capabilities 13<br>
Pointer<br>
Reserved 14<br>
Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>
Required configuration registers<br>
**----- End of picture text -----**<br>


## **MSI-X 表**

MSI-X 表本身是一个向量和地址数组，如图 17-19（第 825 页）所示。每个条目代表一个向量，包含四个双字。DW0 和 DW1 为该向量提供唯一的 64 位地址，而 DW2 提供唯一的 32 位数据模式。DW3 当前仅包含一位：该向量的屏蔽位，允许根据需要独立屏蔽每个向量。

**824**

**第 17 章：中断支持**

_Figure 17-19: MSI-X Table Entries_

|DW3||DW2|DW1|DW0||
|---|---|---|---|---|---|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 0|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 1|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 2|
|….||….|….|….||
|….||….|….|….||
|Vector Control||Message Data|Upper Address|Lower Address|Entry N-1|
|Bit 0 is||vector Mask Bit (R/W)||||


## **挂起位数组**

类似地，挂起位数组 (Pending Bit Array) 也位于内存地址中。它可以使用与 MSI-X 表相同的 BIR 值（同一 BAR）和不同的偏移量，也可以使用完全不同的 BAR。如图 17-20 所示，该数组仅包含将要使用的每个向量的一位。如果触发该中断的事件发生但其屏蔽位已被设置，则不会发送 MSI-X 事务。相反，相应的挂起位被设置。之后，如果取消屏蔽该向量并且挂起位仍被设置，则将在那时生成中断。

**825**

**PCI Ex ress 3.0 Technolo p gy**

_Figure 17-20: Pending Bit Array_

**==> picture [211 x 116] intentionally omitted <==**

**----- Start of picture text -----**<br>
DW1 DW0<br>
Pending Bits 0 - 63 QW 0<br>
Pending Bits 64 - 127 QW 1<br>
Pending Bits 128 - 191<br>
….<br>
….<br>
Pending Bits QW (N-1)/64<br>
**----- End of picture text -----**<br>


## **进入中断处理程序时的内存同步**

## **问题**

任何中断方案在数据传递时都存在潜在的问题。例如，如果设备以前发送过数据并希望通过中断报告该数据，则数据传递的意外延迟可能导致中断过早到达。这可能发生在第 827 页的图 17-21 中所示的桥数据缓冲区中，结果是竞态条件。步骤与我们之前的讨论类似（参见第 796 页的"The Legacy Model"）：

1. Function 向内存写入一个数据块。该写入作为 Posted 事务在本地总线上完成，这意味着发送方已完成其所有需要执行的操作，并且该事务被视为已完成。

2. 传递中断以通知软件某些请求的数据现在存在于内存中。但是，数据由于某种原因在桥中被延迟。

3. 中断向量照常被取回。

4. 取回 ISR 起始地址并将控制权传递给它。

5. ISR 从目标内存缓冲区读取但数据有效负载尚未传递，因此它取回了过时的数据，可能导致错误。

**826**

**第 17 章：中断支持**

_Figure 17-21: Memory Synchronization Problem_

**==> picture [268 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTR<br>
CPU 5 Memory<br>
Memory Buffer<br>
4 Interrupt Service<br>
Routine (ISR)<br>
North Bridge<br>
Interrupt Table (ISR<br>
3 starting addresses)<br>
PCI Bus<br>
Bridge<br>
Write Buffer<br>
South Bridge<br>
1<br>
PCI Bus<br>
2<br>
Interrupt Controller<br>
(PIC) INTA#<br>
Device<br>
**----- End of picture text -----**<br>


## **一种解决方案**

缓解此问题的一种方法是利用 PCI 事务排序规则。如果 ISR 首先向发起中断的设备发送读请求，然后再尝试获取数据，则生成的读完成将沿着任何写数据从该设备返回到内存所经过的相同路径返回到 CPU。事务排序规则保证桥中的读结果不能通过同一方向的 Posted 写，因此最终结果是数据将在允许读结果到达 CPU 之前被写入内存。因此，如果 ISR 等待读完成的到达再继续，则可以确保任何数据都将被传递到内存，从而避免了竞态条件。由于读基本上被用作数据刷新机制，因此它不需要返回任何数据。在这种情况下，读可以是零长度，并且返回的数据被丢弃。因此，这种读有时称为"虚拟读 (dummy read)"。

## **MSI 解决方案**

MSI 可以简化此过程，尽管要使其工作需要满足一些要求（请参考第 829 页的图 17-22）。如果系统允许设备

**827**

**PCI Ex ress 3.0 Technolo p gy**

生成自己的 MSI 写入，而不是通过 IO APIC 之类的中介，则可以发生以下示例：

1. 设备将有效负载数据写入内存，并被桥中的写缓冲区吸收。

2. 设备认为数据已传递，并发出中断以通知 CPU。在这种情况下，发送 MSI 并使用与数据相同的路径。由于数据和 MSI 在桥中均显示为内存写入，因此正常的事务排序规则将使它们保持正确的顺序。

3. 有效负载数据被传递到内存，从而释放通过桥的 MSI 写入的路径。

4. MSI 写入被传递到 CPU 本地 APIC，软件现在知道有效负载数据可用。

## **流量类必须匹配**

但是，这里必须强调一个重要点。数据和 MSI 必须使用相同的流量类才能正常工作。请记住，已分配不同 TC 值的包最终可能会被映射到不同的虚拟通道中，并且不同 VC 中的包没有排序关系。如果数据映射到 VC0 而 MSI 映射到 VC1，则系统将不知道它们之间的任何排序关系，并且无法自动强制执行内存一致性。

如果不可能为两个包提供相同的 TC，则系统将需要改用"虚拟读"方法，并且读请求的 TC 需要匹配数据写包的 TC。应该清楚的是，即使对两者使用相同的 TC，也必须避免使用 Relaxed Ordering 位。我们依靠事务排序规则来实现内存同步，因此不能放宽它们。

**828**

**第 17 章：中断支持**

_Figure 17-22: MSI Delivery_

**==> picture [280 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
