- 包括一个 PCI Express 端点来描述锁定期间的交换机行为。

在此示例中,锁定操作正常完成。操作期间发生的步骤将在接下来的两节中描述。

## **内存读锁定操作**

第 967 页的图 E-1 说明了锁定事务系列的第一步(即获取信号量的初始内存读取):

1. CPU 由于执行针对 PCI 目标的锁定 RMW 指令的驱动程序而发起锁定序列(锁定内存读)。

2. 根端口从端口 2 发出内存读锁定请求。根复合体始终是锁定序列的源。

3. 交换机在上游端口接收锁定请求,并将该请求转发到目标出口端口(3)。交换机在将请求转发到出口端口时,必须阻止除入口端口(1)之外的端口的所有请求从出口端口发出。

4. 来自所示 PCI Express 端点到 PCI 总线的后续对等传输(交换机端口 2 到交换机端口 3)将被阻止,直到锁定被清除。请注意,锁定尚未在其他方向建立。来自 PCI Express 端点的事务可以发送到根复合体。

**965**

## **PCI Express Technology**

5. 内存读锁定请求从交换机的出口端口发送到 PCI Express-PCI 桥。该桥将实现 PCI 锁定语义(有关 PCI 锁定的详细信息,请参阅 MindShare 名为 *PCI System Architecture, Fourth Edition* 的书籍)。

6. 桥在 PCI 总线上执行内存读事务,并断言 PCI LOCK# 信号。目标内存设备将请求的信号量数据返回给桥。

7. 读数据返回到桥,并通过内存读锁定完成与数据 (CplDLk) 传递回交换机。

8. 交换机使用 ID 路由将分组向上游返回到主机处理器。当 CplDLk 分组被转发到交换机的上游端口时,它在上游方向建立锁定,以防止来自其他端口的流量被路由到上游。PCI Express 端点通过锁定操作的路径被完全阻止向交换机端口发送任何事务。请注意,未涉及锁定操作的交换机端口之间的传输将被允许(本例中未显示)。

9. 在检测到 CplDLk 分组时,根复合体知道锁定已沿其与目标设备之间的路径建立,并且完成数据被发送到 CPU。

**966**

**Appendix D**

_Figure D‐1: Lock Sequence Begins with Memory Read Lock Request_

**==> picture [368 x 388] intentionally omitted <==**

**----- Start of picture text -----**<br>
The CPU executes<br>the PCI target's device 1 CPU<br>drive that uses lock<br>Root Complex<br>Root Complex issues Root Complex receives<br>the MRdLk Request 2 9 CplDLk and returns data<br>to CPU<br>Switch forwards the Completion<br>Switch receives MRdLk and  1 to the upstream port (ID routing)<br>forwards it to the egress port (3). 3 8 and locks upstream port (1)<br>Switch blocks transactions from<br>Switch<br>other ports to egress port.<br>2 3<br>Bridge returns data using<br>PCIe endpoint issues a MenRd 4 a CplDLk transaction<br>Request targeting a PCI device,<br>7<br>but request is blocked 5<br>PCIe PCIe<br>Endpoint to<br>PCI Bridge<br>The Bridge receives the MRdLk.<br>Bridges support lock based on the<br>PCI-based requirements<br>6<br>Target The Bridge asserts LOCK and<br>Device performs the PCI Rd transaction<br>and the target returns the read data<br>MRdLk CplDLk<br>**----- End of picture text -----**<br>


## **读取数据修改并写入目标以及锁定完成**

设备驱动程序接收信号量值,对其进行修改,然后启动内存写入以更新旧版 PCI 设备内存中的信号量。第 969 页的图 E-2 说明了写序列,然后是

**967**

**PCI Express Technology**

根复合体传输的释放锁定的 Unlock 消息:

10. 根复合体跨锁定路径向目标设备发出内存写请求。

11. 交换机将事务转发到目标出口端口(3)。内存写的内存地址必须与初始内存读请求相同。

12. 桥将事务转发到 PCI 总线。

13. 目标设备接收内存写数据。

14. 一旦内存写事务从根复合体发出,它就会发送 Unlock 消息,以指示锁定路径中的交换机和任何 PCI/PCI-X 桥释放锁定。请注意,根复合体假定操作已正常完成(因为内存写入已发布,并且没有返回完成以验证成功)。

15. 交换机接收 Unlock 消息,解锁其端口,并将该消息转发到已被锁定的出口端口,以通知锁定路径中的任何其他交换机和/或桥必须清除锁定。

16. 在检测到 Unlock 消息时,桥也必须释放 PCI 总线上的锁定。

**968**

**Appendix D**

_Figure D‐2: Lock Completes with Memory Write Followed by Unlock Message_

**==> picture [369 x 414] intentionally omitted <==**

**----- Start of picture text -----**<br>
The CPU executes<br>the PCI target's device CPU<br>drive that uses lock<br>Root Complex<br>Root Complex issues Root Complex sends<br>the Mem Write Request 10 14 Unlock message<br>1<br>Switch receives MemWt and  Switch receives the Unlock<br>forwards it to the egress port (3) 11 15 message and unlocks the<br>Switch ports in the locked path<br>2 3<br>Bridge releases lock<br>due to Unlock message<br>16<br>PCIe PCIe<br>12<br>Endpoint to<br>PCI Bridge<br>The Bridge receives the MemWt<br>performs the equivalent PCI<br>transaction<br>13<br>Target Target device receives the<br>Device PCI write data thereby<br>completing the operation<br>MemWt Unlock message<br>**----- End of picture text -----**<br>


**969**

**PCI Express Technology**

## **不成功锁定的通知**

当初始内存读锁定请求接收到没有数据的完成分组 (CplLk) 时,锁定事务系列被中止。这意味着锁定序列必须终止,因为没有返回数据。这可能是由与内存读事务相关联的错误引起的,或者目标设备正忙而无法在此刻响应。

## **锁定规则摘要**

以下是适用于根复合体、交换机和桥的排序规则列表。

## **与锁定事务的发起和传播相关的规则**

- 以成功完成以外的状态完成的锁定请求不会建立锁定。

- 无论与锁定序列关联的任何完成的状态如何,所有锁定序列和尝试的锁定序列必须通过传输 Unlock 消息来终止。

- MRdLk、CplDLk 和 Unlock 语义仅允许默认流量类别 (TC0)。

- 在单个层次结构域内,一次只能进行一个锁定事务序列尝试。

- 任何未参与锁定序列的设备必须忽略 Unlock 消息。

锁定事务序列通过 PCI Express 结构的发起和传播按如下方式执行:

- 锁定事务序列以 MRdLk 请求开始:

   - 与锁定事务序列关联的任何后续读取也必须使用 MRdLk 请求。

   - 任何成功的 MRdLk 请求的完成使用 CplDLk 完成类型,或不成功请求的 CplLk 完成类型。

**970**

**Appendix D**

- 如果与锁定序列关联的任何读取未成功完成,则请求者必须假定锁定的原子性不再得到保证,并且请求者和完成者之间的路径不再被锁定。

- 与锁定序列关联的所有写入必须使用 MWr 请求。

- Unlock 消息用于指示锁定序列的结束。交换机通过锁定的出口端口传播 Unlock 消息。

- 在接收到 Unlock 消息时,如果旧版端点或桥处于锁定状态,则必须解锁自身。如果它未锁定,或者接收方是不支持锁定的 PCI Express 端点或桥,则 Unlock 消息将被忽略并丢弃。

## **与交换机相关的规则**

交换机必须从其他事务中检测与锁定序列关联的事务,以防止其他事务干扰锁定并可能导致死锁。以下规则涵盖了如何完成此操作。请注意,锁定访问仅限于 TC0,它始终映射到 VC0。

- 当交换机将 MRdLk 请求从入口端口传播到出口端口时,它必须阻止映射到默认虚拟通道 (VC0) 的所有请求被传播到出口端口。如果在该入口端口接收到寻址不同出口端口的后续 MRdLk 请求,则交换机的行为未定义。请注意,PCI Express 不支持这种拆分锁定访问,并且软件不得导致此类锁定访问。此类访问可能导致系统死锁。

- 当第一个 MRdLk 请求的 CplDLk 返回时,如果完成指示成功完成状态,则交换机必须阻止来自所有其他端口的所有请求被传播到锁定访问涉及的任一端口,但映射到出口端口上除 VC0 之外的通道的请求除外。

- 锁定序列涉及的两个端口必须保持阻塞,直到交换机接收到 Unlock 消息(在接收初始 MRdLk 请求的入口端口)

   - Unlock 消息必须转发到锁定的出口端口。

   - Unlock 消息可以广播到所有其他端口。

   - 入口端口在 Unlock 消息到达时解除阻塞,而被阻塞的出口端口在 Unlock 消息从出口端口传出后被解除阻塞。未参与锁定访问的端口不受 Unlock 消息的影响

**971**

**PCI Express Technology**

## **与 PCI Express/PCI 桥相关的规则**

PCI Express/PCI 桥的要求类似于对交换机的要求,只是因为这些桥仅使用 TC0 和 VC0,所以在锁定访问期间所有其他流量都被阻塞。PCI 总线侧的要求在 MindShare 书籍 *PCI System Architecture, Fourth Edition* 中描述。

## **与根复合体相关的规则**

允许根复合体 (Root Complex) 作为请求者支持锁定事务。如果支持锁定事务,根复合体必须遵循已描述的规则来执行锁定访问。根复合体用于连接到主机处理器 FSB (Front-Side Bus) 的机制超出了规范的范围。

## **与旧版端点相关的规则**

允许旧版端点支持锁定访问,尽管不鼓励使用。如果支持锁定访问,则旧版端点必须按如下方式处理它们:

- 当旧版端点以成功完成状态传输锁定事务系列访问的第一个读取请求的第一个完成时,它变为锁定状态:

   - 如果完成状态不是成功完成,则旧版端点不会变为锁定状态。

   - 一旦锁定,旧版端点必须保持锁定,直到它收到 Unlock 消息。