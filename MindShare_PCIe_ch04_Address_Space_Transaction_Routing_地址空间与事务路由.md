# 📘 第 4 章　地址空间与事务路由 (Chapter 4. Address Space & Transaction Routing)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0170.md` ... `chunks/chunk0229.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Address Space & Transaction Routing](#-本章目录-table-of-contents)

<a id="sec-4-1"></a>
## 4.1 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

Those Completion packets also contain routing information to direct them back to the Requester, and the Requester includes its return address for this purpose in the original request. This “return address” is simply the Device ID of the Requester as it was defined for PCI, which is a combination of three things: its PCI Bus number in the system, its Device number on that bus, and its Function number within that device. This Bus, Device, and Function number information (sometimes abbreviated as BDF) is the routing information that Completions will use to get back to the original Requester. As was true for PCI‐X, a Requester can have several split transactions in progress at the same time and must be able to associate incoming completions with the correct requests. To facilitate that, another value was added to the original request called a Tag that is unique to each request. The Completer copies this transaction Tag and uses it in the Com‐ pletion so the Requester can quickly identify which Request this Completion is servicing. 

Finally, a Completer can also indicate error conditions by setting bits in the completion status field. That gives the Requester at least a broad idea of what might have gone wrong. How the Requester handles most of these errors will be determined by software and is outside the scope of the PCIe spec. 

**Locked Reads.** Locked Memory Reads are intended to support what are called Atomic Read‐Modify‐Write operations, a type of uninterruptable transac‐ tion that processors use for tasks like testing and setting a semaphore. While the test and set is in progress, no other access to the semaphore can take place or a race condition could develop. To prevent this, processors use a lock indicator (such as a separate pin on the parallel Front‐Side Bus) that prevents other trans‐ actions on the bus until the locked one is finished. What follows here is just a high level introduction to the topic. For more information on Locked transac‐ tions, refer to Appendix D called “Appendix D:  Locked Transactions” on page 963. 

As a bit of history, in the early days of PCI the spec writers anticipated cases where PCI would actually replace the processor bus. Consequently, support for things that a processor would need to do on the bus were included in the PCI spec, such as locked transactions. However, PCI was only rarely ever used this way and, in the end, much of this processor bus support was dropped. Locked cycles remained, though, to support a few special cases, and PCIe carries this mechanism forward for legacy support. Perhaps to speed migration away from its use, new PCIe devices are prohibited from accepting locked requests; it’s only legal for those that self‐identify as Legacy Devices. In the example shown in Figure 2‐19 on page 67, a Requester begins the process by sending a locked request (MRdLk). By definition, such a request is only allowed to come from the CPU, so in PCIe only a Root Port will ever initiate one of these. 

**66** 

**Chapter 2: PCIe Architecture Overview** 

The locked request is routed through the topology using the target memory address and eventually reaches the Legacy Endpoint. As the packet makes its way through each routing device (called a service point) along the way, the Egress Port for the packet is locked, meaning no other packets will be allowed in that direction until the path is unlocked. 

_Figure 2‐19: Non‐Posted Locked Read Transaction Protocol_ 

**==> picture [330 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>PCIe<br>Bridge<br>Switch Endpoint<br>to PCI<br>PCI<br>PCIe PCIe Legacy<br>Endpoint Endpoint Endpoint<br>MRdLk<br>CplDLk<br>CplDLk<br>MRdLk<br>**----- End of picture text -----**<br>

When the Completer receives the packet and decodes its contents, it gathers the data and creates one or more Locked Completions with data. These Comple‐ tions are routed back to the Requester using the Requester ID, and each Egress Port they pass through is then locked, too. 

If the Completer encounters a problem, it returns a locked completion packet without data (the original read should have resulted in data so if there isn’t any we know there’s been a problem) and the status field will indicate something about the error. The Requester will understand that to mean that the lock did not succeed and so the transaction will be cancelled and software will need to decide what to do next. 

**67** 

**PCI Ex ress Technolo p gy** 

**IO and Configuration Writes.** Figure 2‐20 on page 68 illustrates a non‐ posted IO write transaction. Like a locked request, an IO cycle can also legally target only a Legacy Endpoint. The request is routed through the Switches based on the IO address until it reaches the target Endpoint. When the Compl‐ eter receives the request, it accepts the data and returns a single completion packet without data that confirms reception of the packet. The status field in the completion would report whether an error had occurred and, if so, the Requester’s software would handle it. 

If the completion reports no errors the Requester knows that the write data has been successfully delivered and the next step in the sequence of instructions for that Completer is now permitted. And that really summarizes the motivation for the non‐posted write: unlike a memory write, it’s not enough to know that the data **will** get to the destination sometime in the future. Instead, the next step can’t logically take place until we know that it **has** gotten there. As with locked cycles, non‐posted writes can only come from the processor. 

_Figure 2‐20: Non‐Posted Write Transaction Protocol_ 

**==> picture [346 x 275] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Requester<br>Step 1: Root Initiates IOWr<br>Step 4: Root receives Cpl Root Complex<br>IOWr Cpl System<br>Memory<br>Switch A Switch C<br>IOWr<br>Cpl<br>Switch B Endpoint Endpoint Endpoint<br>IOWr Cpl<br>Completer<br>Legacy<br>Step 2: Endpoint receives IOWr<br>Endpoint<br>Endpoint Step 3: Endpoint writes data, returns Cpl<br>**----- End of picture text -----**<br>

**68** 

**Chapter 2: PCIe Architecture Overview**

</td>
<td style="background-color:#e8e8e8">

## **PCI Express Technology** 

这些完成报文（Completion）也包含用于将报文路由回请求者（Requester）的路由信息，请求者会在原始请求中提供其返回地址作为此用途。该"返回地址"实际上就是请求者按照 PCI 定义的设备 ID（Device ID），由三部分组成：其在系统中的 PCI 总线号（Bus number）、在该总线上的设备号（Device number）以及该设备内的功能号（Function number）。此总线号、设备号和功能号信息（有时缩写为 BDF）就是完成报文用来返回原始请求者的路由信息。与 PCI-X 一样，请求者可以同时有多个拆分事务（split transaction）正在进行，并且必须能够将收到的完成报文与正确的请求相对应。为便于实现这一点，在原始请求中又新增了一个称为 Tag（标签）的值，每个请求都有唯一的 Tag。完成者（Completer）会复制该事务 Tag 并在完成报文中使用，请求者便可以快速识别该完成报文所服务的是哪一个请求。

最后，完成者还可以通过在完成状态字段中设置相应位来指示错误情况。这使请求者至少能够大致了解可能发生了什么错误。请求者如何处理这些错误大多由软件决定，并不在 PCIe 规范的范围之内。

**锁定读（Locked Reads）。** 锁定内存读（Locked Memory Read）用于支持所谓的原子读-修改-写（Atomic Read-Modify-Write）操作，这是一类不可中断的事务，处理器在诸如测试并设置信号量之类的任务中会用到。在测试与设置进行期间，不能同时访问该信号量，否则可能产生竞态条件（race condition）。为防止此类问题，处理器会使用一个锁指示器（例如并行前端总线（Front-Side Bus）上的一个独立引脚），在该锁定事务完成之前禁止总线上的其他事务。此处仅给出该主题的高层次介绍。关于锁定事务的更多信息，请参阅附录 D 即第 963 页的"附录 D：锁定事务（Locked Transactions）"。

从历史的角度来看，在 PCI 的早期，规范编写者预见到 PCI 可能会取代处理器总线的情况。因此，PCI 规范中纳入了处理器在总线上可能需要执行的操作的支持，例如锁定事务。然而，PCI 实际很少以这种方式使用，最终其处理器总线支持的大部分内容都被废弃了。尽管如此，锁定周期（locked cycles）被保留下来以支持少数特殊场景，并且 PCIe 沿用了此机制以提供遗留兼容。或许是为了加快停止使用该机制，PCIe 规定新设备不得接受锁定请求；只有那些自标识为遗留设备（Legacy Devices）的设备才被允许这样做。在第 67 页图 2-19 所示的示例中，请求者通过发送一个锁定请求（MRdLk）来启动该流程。根据定义，此类请求只能来自 CPU，因此在 PCIe 中只有根端口（Root Port）才会发起这类请求。

**66** 

**第 2 章：PCIe 架构概述** 

锁定请求会基于目标内存地址通过拓扑进行路由，并最终到达遗留端点。当报文沿路经过每个路由设备（称为服务点（service point））时，该报文所在的出端口（Egress Port）会被锁定，意味着在该路径解锁之前不会允许其他报文沿该方向通过。

_图 2-19：非 Posted 锁定读事务协议_ 

**==> picture [330 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>PCIe<br>Bridge<br>Switch Endpoint<br>to PCI<br>PCI<br>PCIe PCIe Legacy<br>Endpoint Endpoint Endpoint<br>MRdLk<br>CplDLk<br>CplDLk<br>MRdLk<br>**----- End of picture text -----**<br>

当完成者收到报文并解码其内容后，便会收集数据并生成一个或多个带数据的锁定完成报文（Locked Completions with data）。这些完成报文使用请求者 ID（Requester ID）路由回请求者，并且它们经过的每个出端口也都将被锁定。

如果完成者遇到问题，它会返回一个不带数据的锁定完成报文（原始读操作本应返回数据，如果没有数据则说明存在问题），并且状态字段会指示相应的错误信息。请求者会将此理解为锁定未成功，进而取消该事务，并由软件决定下一步该如何处理。

**67** 

**PCI Express Technology** 

**IO 和配置写（IO and Configuration Writes）。** 第 68 页的图 2-20 展示了一个非 Posted IO 写事务（non-posted IO write transaction）。与锁定请求类似，IO 周期在合法情况下也只能以遗留端点为目标。该请求基于 IO 地址通过交换机（Switch）进行路由，直到到达目标端点。完成者收到请求后，接收数据并返回一个不带数据的完成报文，以确认报文已被接收。完成报文中的状态字段会报告是否发生错误；如果发生错误，则由请求者的软件负责处理。

如果完成报文报告无错误，则请求者便知道写数据已成功送达，并且该完成者后续指令序列的下一条指令可以执行。这正概括了非 Posted 写（non-posted write）的动机：与内存写（memory write）不同，仅知道数据**将会**在将来的某个时刻到达目标位置是不够的；只有当我们确认数据**已经**到达之后，下一步操作才能在逻辑上继续进行。与锁定周期一样，非 Posted 写也只能由处理器发起。

_图 2-20：非 Posted 写事务协议_ 

**==> picture [346 x 275] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Requester<br>Step 1: Root Initiates IOWr<br>Step 4: Root receives Cpl Root Complex<br>IOWr Cpl System<br>Memory<br>Switch A Switch C<br>IOWr<br>Cpl<br>Switch B Endpoint Endpoint Endpoint<br>IOWr Cpl<br>Completer<br>Legacy<br>Step 2: Endpoint receives IOWr<br>Endpoint<br>Endpoint Step 3: Endpoint writes data, returns Cpl<br>**----- End of picture text -----**<br>

**68** 

**第 2 章：PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-2"></a>
## 4.2 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Posted Writes** 

**Memory Writes.** Memory writes are always posted and never receive com‐ pletions. Once the request has been sent, the Requester doesn’t wait for any feedback before going on to the next request, and no time or bandwidth is spent returning a completion. As a result, posted writes are faster and more efficient than non‐posted requests and improve system performance. As shown in Fig‐ ure 2‐21 on page 69, the packet is routed through the system using its target memory address to the Completer. Once a Link has successfully sent the request, that transaction is finished on that Link and its available for other pack‐ ets. Eventually, the Completer accepts the data and the transaction is truly fin‐ ished. Of course, one trade‐off with this approach is that, since no Completion packets are sent, there’s also no means for reporting errors back to the Requester. If the Completer encounters an error, it can log it and send a Message to the Root to inform system software about the error, but the Requester won’t see it. 

_Figure 2‐21: Posted Memory Write Transaction Protocol_ 

**==> picture [335 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Requester:<br>Step 1: Root Complex<br>      initiates MWr request<br>Root Complex<br>DDR<br>SDRAM<br>MWr<br>Switch A Switch C<br>MWr<br>Switch B Endpoint Endpoint Endpoint<br>MWr<br>Completer:<br>Endpoint Endpoint<br>Step 2: Endpoint receives MWr<br>**----- End of picture text -----**<br>

**69**

</td>
<td style="background-color:#e8e8e8">

## **Posted 写事务（Posted Writes）** 

**内存写（Memory Writes）。** 内存写始终是 Posted 类型的,永远不会收到完成报文。一旦请求被发送出去,请求者（Requester）不会等待任何反馈就可以继续发起下一个请求,因此也不会花费时间或带宽来返回完成报文。因此,Posted 写比 Non-Posted 请求更快、更高效,能够提升系统性能。如第 69 页的图 2-21 所示,报文通过其目标内存地址在系统中路由,最终到达完成者（Completer）。一旦某条链路（Link）成功发送了该请求,则该事务在该链路上即告完成,该链路便可被其他报文使用。最终,完成者接收数据,该事务才真正彻底完成。当然,这种方式也有一个权衡:由于不会发送任何完成报文,因此也就没有办法将错误报告给请求者。如果完成者遇到错误,它可以记录该错误,并向根复合体（Root Complex）发送一条消息以通知系统软件有关该错误的信息,但请求者本身不会看到该错误。 

_图 2-21:Posted 内存写事务协议_ 

**==> picture [335 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
处理器<br>请求者（Requester）：<br>步骤 1:根复合体（Root Complex）<br>      发起 MWr 请求<br>
根复合体（Root Complex）<br>
DDR<br>SDRAM<br>
MWr<br>
交换机 A 交换机 C<br>
MWr<br>
交换机 B 端点 端点 端点<br>
MWr<br>
完成者（Completer）：<br>
端点 端点<br>
步骤 2:端点接收 MWr<br>
**----- End of picture text -----**<br>

**69**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-3"></a>
## 4.3 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

**Message Writes.** Interestingly, unlike the other requests we’ve looked at so far, there are several possible routing methods for messages, and a field within the message indicates which type to use. For example, some messages are posted write requests that target a specific Completer, others are broadcast from the Root to all Endpoints, while still others sent from an Endpoint are automati‐ cally routed to the Root. To learn more about the different types of routing refer to Chapter 4, entitled ʺAddress Space & Transaction Routing,ʺ on page 121. 

Messages are useful in PCIe to help achieve a design goal of lowering the pin count. They eliminate the need for the side‐band signals that PCI used to report things like interrupts, power management events, and errors because they can report that information in a packet over the normal data path.

</td>
<td style="background-color:#e8e8e8">

## **PCI Express 技术**

**消息写（Message Writes）。** 有趣的是，与我们迄今为止看到的其他请求不同，消息有几种可能的路由方法，并且消息中的一个字段指示应使用哪种类型。例如，有些消息是发布到特定 Completer 的 Posted 写请求，有些是从根复合体 (Root Complex) 广播到所有端点 (Endpoint) 的，而从端点 (Endpoint) 发送的其他消息则会自动路由到根复合体 (Root)。要了解更多关于不同路由类型的信息，请参阅第 121 页第 4 章"地址空间与事务路由"。

消息在 PCIe 中很有用，有助于实现降低引脚 (Pin) 数的设计目标。它们消除了对 PCI 曾经用于报告中断 (Interrupt)、电源管理事件 (Power Management Events) 和错误 (Error) 等内容的边带 (Sideband) 信号的需要，因为它们可以通过正常的数据路径以报文的形式报告这些信息。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-4"></a>
## 4.4 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Quality of Service (QoS)** 

PCIe was designed from its inception to be able to support time‐sensitive trans‐ actions for applications like streaming audio or video where data delivery must be timely in order to be useful. This is referred to as providing Quality of Ser‐ vice and is accomplished by the addition of a few things. First, each packet is assigned a priority by software by setting a 3‐bit field within it called Traffic Class (TC). Generally speaking, assigning a higher‐numbered TC to a packet is expected to give it a higher priority in the system. Second, multiple buffers, called Virtual Channels (VC), are built into the hardware for each port and a packet is placed into the appropriate buffer based on its TC. Third, since a port now has multiple buffers with packets available for transmission at a given time, arbitration logic is needed to select among the VCs. Finally, Switches must select between competing input ports for access to the VCs of a given output port. This is called Port Arbitration and can be hardware assigned or software programmable. All of these hardware pieces must be in place to allow a system to prioritize packets. If properly programmed and set up, such a system can even provide guaranteed service for a given path. 

To illustrate the concept, consider Figure 2‐22 on page 71, in which a video cam‐ era and SCSI device both need to send data to system DRAM. The difference is that the camera data is time critical; if the transmission path to the target device is unable to keep up with its bandwidth, frames will get dropped. The system needs to be able to guarantee a bandwidth that’s at least as high as the camera or the captured video may appear choppy. At the same time, the SCSI data needs to be delivered without errors, but how long it takes is not as important. Clearly, then, when both a video data packet and a SCSI packet need to be sent at the same time, the video traffic should have a higher priority. QoS refers to the abil‐ ity of the system to assign different priorities to packets and route them through the topology with deterministic latencies and bandwidth. For more detail on QoS, refer to Chapter 7, entitled ʺQuality of Service,ʺ on page 245. 

**70** 

**Chapter 2: PCIe Architecture Overview** 

_Figure 2‐22: QoS Example_ 

**==> picture [368 x 314] intentionally omitted <==**

**----- Start of picture text -----**<br>
Intel Processor<br>System<br>Memory<br>PCIe<br>Uncore<br>GFX<br>QPI<br>IOH Root Complex<br>10 Gb<br>LAN Switch Ethernet Switch Fibre<br>Endpoint Channel<br>Endpoint Endpoint<br>10 Gb PCI Express SAS/SATA<br>Add-In Switch Ethernet to-PCI<br>RAID<br>Endpoint Endpoint<br>Endpoint<br>PCI<br>Add-In EthernetGb IEEE Slots<br>Isochronous Ordinary 1394<br>Traffic Endpoint Endpoint Traffic<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

## **服务质量 (QoS)**

PCIe 从设计之初就能够支持对时间敏感的事务,例如流式音频或视频等应用,这些应用要求数据必须及时传递才有意义。这被称为提供服务质量 (Quality of Service),它通过增加一些机制来实现。首先,软件会为每个报文分配一个优先级,即通过设置报文内一个称为流量类 (TC, Traffic Class) 的 3 位字段。一般来说,为报文分配编号更高的 TC 意味着它在系统中具有更高的优先级。其次,硬件为每个端口内置了多个缓冲区,称为虚通道 (VC, Virtual Channel),报文会根据其 TC 被放入相应的缓冲区。第三,由于一个端口现在有多个缓冲区同时有待发送的报文,因此需要仲裁逻辑在各个 VC 之间进行选择。最后,交换机 (Switch) 必须在竞争访问某一输出端口 VC 的多个输入端口之间进行选择。这称为端口仲裁 (Port Arbitration),可以由硬件分配,也可以由软件编程设定。所有这些硬件组件必须到位,系统才能对报文进行优先级排序。如果得到正确的编程和配置,这样的系统甚至可以为给定路径提供有保证的服务。

为了说明这一概念,请参阅第 71 页的图 2‐22,在该图中,摄像机和 SCSI 设备都需要向系统 DRAM 发送数据。不同之处在于,摄像机数据是时间敏感的;如果到目标设备的传输路径无法跟上其带宽,帧就会被丢弃。系统需要能够保证至少与摄像机带宽一样高的传输速率,否则采集到的视频可能会出现卡顿。同时,SCSI 数据需要无误地交付,但交付所需的时间并不那么重要。显然,当视频数据报文和 SCSI 报文需要在同一时刻发送时,视频流量应具有更高的优先级。QoS 指的是系统为报文分配不同优先级、并以确定性延迟和带宽将它们通过拓扑进行路由的能力。有关 QoS 的更多详细信息,请参阅第 245 页第 7 章"服务质量 (Quality of Service)"。

**70**

**第 2 章:PCIe 架构概述**

_图 2‐22:QoS 示例_

**==> picture [368 x 314] intentionally omitted <==**

**----- Start of picture text -----**<br>
Intel 处理器<br>系统<br>内存<br>PCIe<br>Uncore<br>GFX<br>QPI<br>IOH 根复合体 (Root Complex)<br>10 Gb<br>LAN 交换机 以太网交换机 光纤<br>端点 (Endpoint) 通道<br>端点 (Endpoint) 端点 (Endpoint)<br>10 Gb PCI Express SAS/SATA<br>扩展卡 以太网转 PCI<br>RAID<br>端点 (Endpoint) 端点 (Endpoint)<br>端点 (Endpoint)<br>PCI<br>扩展卡 千兆以太网 IEEE 插槽<br>等时 常规 1394<br>流量 端点 (Endpoint) 端点 (Endpoint) 流量<br>
**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-5"></a>
## 4.5 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Transaction Ordering** 

Within a VC, the packets normally all flow through in the same order in which they arrived, but there are exceptions to this general rule. PCI Express protocol inherits the PCI transaction‐ordering model, including support for relaxed‐ ordering cases added with the PCI‐X architecture. These ordering rules guaran‐ tee that packets using the same traffic class will be routed through the topology in the correct order, preventing potential deadlock or live‐lock conditions. An interesting point to note is that, since ordering rules only apply within a VC and packets that use different TCs may not get mapped into the same VC, packets using different TCs are understood by software to have no ordering relation‐ ship. This ordering is maintained in the VCs within the transaction layer. 

**71** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

## **事务排序**

在 VC（虚通道）内部，数据包通常按照其到达的相同顺序流转，但这一通用规则也存在例外。PCI Express 协议继承了 PCI 的事务排序模型，包括 PCI-X 架构所新增的松散排序（Relaxed Ordering）支持。这些排序规则保证了使用相同流量类（TC, Traffic Class）的数据包能够以正确的顺序通过拓扑进行路由，从而避免潜在的死锁或活锁情况。值得注意的一点是，由于排序规则仅在 VC 内部适用，并且使用不同 TC 的数据包未必会被映射到同一个 VC，因此软件层面理解使用不同 TC 的数据包之间不存在排序关系。该排序在事务层（Transaction Layer）内的各个 VC 中得以维护。

**71**

**PCI Ex ress Technolo p gy**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-6"></a>
## 4.6 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Flow Control** 

A typical protocol used by serial transports is to require that a transmitter only send a packet to its neighbor if there is sufficient buffer space to receive it. That cuts down on performance‐wasting events on the bus like the disconnects and retries that PCI allowed and thus removes that class of problems from the trans‐ port. The trade‐off is that the receiver must report its buffer space often enough to avoid unnecessary stalls and that reporting takes a little bandwidth of its own. In PCIe this reporting is done with DLLPs (Data Link Layer Packets), as we’ll see in the next section. The reason is to avoid a possible deadlock condi‐ tion that might occur if TLPs were used, in which a transmitter can’t get a buffer size update because its own receive buffer is full. DLLPs can always be sent and received regardless of the buffer situation, so that problem is avoided. This flow control protocol is automatically managed at the hardware level and is trans‐ parent to software. 

_Figure 2‐23: Flow Control Basics_ 

**==> picture [292 x 107] intentionally omitted <==**

**----- Start of picture text -----**<br>
Buffer space available<br>TLP<br>Transmitter Receiver<br>Transmitter VC BufferReceiver<br>Flow Control DLLP<br>**----- End of picture text -----**<br>

As shown in Figure 2‐23 on page 72, the Receiver contains the VC Buffers that hold received TLPs. The Receiver advertises the size of those buffers to the Transmitters using Flow Control DLLPs. The Transmitter tracks the available space in the Receiverʹs VC Buffers and is not allowed to send more packets than the Receiver can hold. As the Receiver processes the TLPs and removes them from the buffer, it periodically sends Flow Control Update DLLPs to keep the Transmitter up‐to‐date regarding the available space. To learn more about this, see Chapter 6, entitled ʺFlow Control,ʺ on page 215.

</td>
<td style="background-color:#e8e8e8">

## **流控 (Flow Control)** 

串行传输常用的一种典型协议是：发送器只有在邻居端有足够的缓冲空间来接收数据包时,才向其发送数据包。这可以减少总线上诸如 PCI 所允许的断开连接和重试之类的浪费性能的事件,从而将这类问题从传输中消除。其代价是,接收器必须足够频繁地报告其缓冲空间,以避免不必要的停顿,而该报告本身会占用一点带宽。在 PCIe 中,该报告通过 DLLP (数据链路层包 (Data Link Layer Packet, DLLP)) 来完成,我们将在下一节中看到这一点。这样做是为了避免在使用 TLP 时可能发生的死锁条件——在那种情况下,发送器因自身接收缓冲区已满而无法获取缓冲区大小更新。DLLP 无论缓冲区状况如何都可以被发送和接收,因此该问题得以避免。此流控协议在硬件层面自动管理,对软件透明。

_图 2‐23:流控基础_

**==> 图片 [292 x 107] 故意省略 <==**

**----- 图片文字开始 -----**<br>
可用的缓冲空间<br>TLP<br>发送器 接收器<br>发送器 VC 缓冲区 接收器<br>流控 DLLP<br>**----- 图片文字结束 -----**<br>

如图 2‐23 第 72 页所示,接收器包含用于存放所接收 TLP 的 VC 缓冲区。接收器使用流控 DLLP 向发送器通告这些缓冲区的大小。发送器跟踪接收器 VC 缓冲区中的可用空间,且不允许发送超过接收器可容纳数量的报文。当接收器处理 TLP 并将其从缓冲区中移除时,它会周期性地发送流控更新 DLLP,以使发送器随时了解可用空间。如需了解更多相关信息,请参阅第 215 页第 6 章“流控 (Flow Control)”。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-7"></a>
## 4.7 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Data Link Layer** 

This logic is responsible for Link management and performs three major func‐ tions: TLP error correction, flow control, and some Link power management. It accomplishes these by generating DLLPs as shown in Figure 2‐24 on page 73. 

**72** 

**Chapter 2: PCIe Architecture Overview**

</td>
<td style="background-color:#e8e8e8">

## **数据链路层 (Data Link Layer)** 

该逻辑负责链路 (Link) 管理,并执行三个主要功能:TLP 错误纠正、流控 (Flow Control) 以及部分链路 (Link) 电源管理 (Power Management)。它通过生成 DLLP(如图 2-24 所示,见第 73 页)来完成这些功能。 

**72** 

**第 2 章:PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-8"></a>
## 4.8 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **DLLPs (Data Link Layer Packets)** 

DLLPs are transferred between Data Link Layers of the two neighboring devices on a Link. The Transaction Layer is not even aware of these packets, which only travel between neighboring devices and are not routed anywhere else. They are small (always just 8 bytes) compared to TLPs, and that’s a good thing because they represent overhead for maintaining Link protocol. 

_Figure 2‐24: DLLP Origin and Destination_ 

**==> picture [375 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>Device Device<br>Core Core<br>Transaction Transaction<br>Flow Control,  Layer  Layer<br>Ack/Nak, Etc.<br>(1) Data Data (4)<br>DLLP Core CRC Link Layer Link Layer DLLP Core CRC<br>(2) (2) (3) (3)<br>SDP DLLP Core CRC END Physical Physical SDP DLLP Core CRC END<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>**----- End of picture text -----**<br>

**DLLP Assembly.** As shown in Figure 2‐24 on page 73, a DLLP originates at the Data Link Layer of the transmitter and is consumed by the Data Link Layer of the receiver. A 16‐bit CRC is added to the DLLP Core to check for errors at the receiver. The DLLP contents are forwarded to the Physical Layer which appends a Start and End character to the packet (for the first two generations of PCIe), and then encodes and differentially transmits it over the Link using all the available lanes. 

**DLLP Disassembly.** When a DLLP is received by the Physical Layer, the bit stream is decoded and the Start and End frame characters are removed. The rest of the packet is forwarded to the Data Link Layer, which checks for CRC errors and then takes the appropriate action based on the packet. The Data Link Layer is the destination for the DLLP, so it isn’t forwarded up to the Transaction Layer. 

**73** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

## **DLLPs (数据链路层包)**

DLLP 在链路上两个相邻设备的数据链路层之间传输。事务层甚至不会感知到这些数据包的存在，因为它们只在相邻设备之间传输,不会被路由到其他地方。与 TLP 相比,它们很小(始终只有 8 个字节),这是一件好事,因为它们代表了维护链路协议的额外开销。

_图 2-24:DLLP 的起点和终点_

**==> picture [375 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>Device Device<br>Core Core<br>Transaction Transaction<br>Flow Control,  Layer  Layer<br>Ack/Nak, Etc.<br>(1) Data Data (4)<br>DLLP Core CRC Link Layer Link Layer DLLP Core CRC<br>(2) (2) (3) (3)<br>SDP DLLP Core CRC END Physical Physical SDP DLLP Core CRC END<br>Layer Layer<br>(RX) (TX) (RX) (TX)<br>
**----- End of picture text -----**<br>

**DLLP 组装。** 如图 2-24(第 73 页)所示,DLLP 源自发送端的数据链路层,由接收端的数据链路层消费。在 DLLP Core 之后附加一个 16 位 CRC,以便在接收端检查错误。DLLP 的内容被转发到物理层,物理层在数据包的开头和结尾分别附加一个 Start 和 End 字符(针对前两代 PCIe),然后使用所有可用的通道 (Lane) 对其进行编码并以差分方式通过链路 (Link) 传输。

**DLLP 拆卸。** 当物理层接收到 DLLP 时,会对比特流进行解码,并移除 Start 和 End 帧字符。数据包的其余部分被转发到数据链路层,数据链路层会检查 CRC 错误,然后根据该数据包采取适当的操作。数据链路层是 DLLP 的最终目的地,因此不会向上转发到事务层。

**73**

**PCI Ex ress Technolo p gy**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-9"></a>
## 4.9 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Ack/Nak Protocol** 

The error correction function, illustrated in Figure 2‐25 on page 74, is provided through a hardware‐based automatic retry mechanism. As shown in Figure 2‐26 on page 75, an LCRC and Sequence Number are added to each outgoing TLP and checked at the receiver. The transmitter’s Replay Buffer holds a copy of every TLP that has been sent until receipt at the neighboring device has been confirmed. That confirmation takes the form of an Ack DLLP (positive acknowl‐ edgement) sent by the Receiver with the Sequence Number of the last good TLP it has seen. When the Transmitter sees the Ack, it flushes the TLP with that Sequence Number out of the Replay Buffer, along with all the TLPs that were sent before the one that was acknowledged. 

If the Receiver detects a TLP error, it drops the TLP and returns a Nak to the Transmitter, which then replays all unacknowledged TLPs in hopes of a better result the next time. Since detected errors are almost always transient events, a replay will very often correct the problem. This process is often referred to as the Ack/Nak protocol. 

_Figure 2‐25: Data Link Layer Replay Mechanism_ 

**==> picture [314 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
From To<br>Transaction Layer Transaction Layer<br>Tx Rx<br>Data Link Layer<br>Link Packet DLLP DLLP Link Packet<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux<br>Error<br>Mux Check<br>Tx Rx<br>Link<br>**----- End of picture text -----**<br>

**74** 

**Chapter 2: PCIe Architecture Overview** 

_Figure 2‐26: TLP and DLLP Structure at the Data Link Layer_ 

**==> picture [368 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Sequence ID Header Data Payload  ECRC LCRC<br>AND<br>DLLP<br>DLLP Type Misc. CRC<br>**----- End of picture text -----**<br>

The basic form of a DLLP is also shown in Figure 2‐26 on page 75, and consists of a 4‐byte DLLP type field that may include some other information and a 2‐ byte CRC. 

Figure 2‐27 on page 76 shows an example of a memory read going across a Switch. In general, the steps for this case would be as follows: 

1. **Step 1a** : Requester sends a memory read request and saves a copy in its Replay Buffer. Switch receives the MRd TLP and checks the LCRC and Sequence Number. 

   - Step 1b: No error is seen, so the Switch returns an Ack DLLP to Requester. In response, Requester discards its copy of the TLP from the Replay Buffer. 

2. **Step 2a** : Switch forwards the MRd TLP to the correct Egress Port using memory address for its routing and saves a copy in the Egress Port’s Replay Buffer. The Completer receives the MRd TLP and checks for errors. **Step 2b** : No error is seen, so the Completer returns an Ack DLLP to the Switch. Switch Port purges its copy of the MRd TLP from its Replay Buffer. 

3. **Step 3a** : As the final destination of the request, the Completer checks the optional ECRC field in MRd TLP. No errors are seen so the request is passed to the core logic. Based on the command, the device fetches the requested data and returns a Completion with Data TLP (CplD) while saving a copy in its Replay Buffer. Switch receives CplD TLP and checks for errors. **Step 3b** : No error is seen, so the Switch returns an Ack DLLP to the Compl‐ eter. Completer discards its copy of the CplD TLP from its Replay Buffer. 

4. **Step 4a** : Switch decodes the Requester ID field in CplD TLP and routes the packet to the correct Egress Port, saving a copy in the Egress Port’s Replay Buffer. Requester receives CplD TLP and checks for errors. **Step 4b** : No error is seen, so the Requester returns Ack DLLP to Switch. Switch discards its copy of the CplD TLP from its Replay Buffer. Requester checks the optional ECRC field and finds no error, so data is passed up to the core logic. 

**75**

</td>
<td style="background-color:#e8e8e8">

## **Ack/Nak 协议**

第 74 页图 2-25 所示的纠错功能由一种基于硬件的自动重试机制提供。如第 75 页图 2-26 所示，每个发出的 TLP 都会附加一个 LCRC（链路 CRC）和序列号（Sequence Number），由接收方进行校验。发送器（Transmitter）的重放缓冲区（Replay Buffer）会保存每一个已发送 TLP 的副本，直到相邻设备确认已成功接收。该确认由接收器（Receiver）发送一个 Ack DLLP（ACK DLLP，确认 DLLP）实现，其中包含其所见到的最后一个正确 TLP 的序列号。当发送器看到该 Ack 后，便将该序列号对应的 TLP 以及所有在它之前已发送的 TLP 一并从重放缓冲区中清除。

如果接收器检测到 TLP 错误，它会丢弃该 TLP，并向发送器返回一个 Nak，随后发送器会重放所有未被确认的 TLP，希望在下一次能够得到正确结果。由于被检测到的错误几乎都是瞬态事件，重放通常能够纠正该问题。该过程通常被称为 Ack/Nak 协议。

_图 2-25：数据链路层重放机制_

**==> picture [314 x 169] intentionally omitted <==**

**----- Start of picture text -----**<br>
From To<br>事务层（Transaction Layer） 事务层（Transaction Layer）<br>Tx Rx<br>数据链路层（Data Link Layer）<br>链路（Link）包 DLLP DLLP 链路（Link）包<br>Sequence TLP LCRC ACK /NAK ACK /NAK Sequence TLP LCRC<br>Replay<br>Buffer De-mux<br>Error<br>Mux Check<br>Tx Rx<br>Link<br>**----- End of picture text -----**<br>

**74**

**第 2 章：PCIe 架构概述**

_图 2-26：数据链路层处 TLP 和 DLLP 的结构_

**==> picture [368 x 101] intentionally omitted <==**

**----- Start of picture text -----**<br>
事务层包（TLP, Transaction Layer Packet）<br>序列号 ID（Sequence ID） 包头（Header） 数据有效负载（Data Payload）  ECRC LCRC<br>AND<br>DLLP<br>DLLP Type Misc. CRC<br>**----- End of picture text -----**<br>

DLLP 的基本形式同样在第 75 页图 2-26 中展示，它由一个 4 字节的 DLLP Type 字段（可能包含一些其他信息）和一个 2 字节的 CRC 组成。

第 76 页图 2-27 给出了一个跨交换机（Switch）的内存读操作示例。一般来说，本例的步骤如下：

1. **步骤 1a**：请求者（Requester）发送一个内存读请求，并将其副本保存在重放缓冲区中。交换机接收到该 MRd TLP，并检查其 LCRC 和序列号。

   - 步骤 1b：由于未检测到错误，交换机向请求者返回一个 Ack DLLP。作为响应，请求者从重放缓冲区中丢弃该 TLP 的副本。

2. **步骤 2a**：交换机根据内存地址进行路由，将该 MRd TLP 转发到正确的下游端口（Egress Port），并将其副本保存在该下游端口的重放缓冲区中。完成器（Completer）收到 MRd TLP 后进行错误检查。**步骤 2b**：未检测到错误，因此完成器向交换机返回 Ack DLLP。交换机端口从其重放缓冲区中清除该 MRd TLP 的副本。

3. **步骤 3a**：作为该请求的最终目的地，完成器检查 MRd TLP 中的可选 ECRC 字段。未检测到错误，因此该请求被传递至核心逻辑。设备根据该命令获取所请求的数据，并返回一个带数据的完成报文 TLP（CplD），同时将副本保存在重放缓冲区中。交换机收到 CplD TLP 后进行错误检查。**步骤 3b**：未检测到错误，因此交换机向完成器返回 Ack DLLP。完成器从重放缓冲区中丢弃该 CplD TLP 的副本。

4. **步骤 4a**：交换机解码 CplD TLP 中的请求者 ID（Requester ID）字段，并将该报文路由到正确的下游端口，同时将副本保存在该下游端口的重放缓冲区中。请求者收到 CplD TLP 后进行错误检查。**步骤 4b**：未检测到错误，因此请求者向交换机返回 Ack DLLP。交换机从重放缓冲区中丢弃该 CplD TLP 的副本。请求者检查可选的 ECRC 字段，未发现错误，于是数据被上送至核心逻辑。

**75**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-10"></a>
## 4.10 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

_Figure 2‐27: Non‐Posted Transaction with Ack/Nak Protocol_ 

**==> picture [384 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
1a. Request 2a. Request<br>4b. Ack 3b. Ack<br>Requester Switch Completer<br>1b. Ack 2b. Ack<br>4a. Completion 3a. Completion<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

## **PCI Express Technology**

_图 2‐27：使用 Ack/Nak 协议的 Non-Posted 事务_

**==> picture [384 x 104] intentionally omitted <==**

**----- Start of picture text -----**<br>
1a. Request 2a. Request<br>4b. Ack 3b. Ack<br>Requester 交换机 Completer<br>1b. Ack 2b. Ack<br>4a. Completion 3a. Completion<br>**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-11"></a>
## 4.11 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Flow Control** 

The second major Link Layer function is Flow Control. Following power‐up or Reset, this mechanism is initialized by the Data Link Layer automatically in hardware and then updated during run‐time. An overview of this was already presented in the section on TLPs so that won’t be repeated here. To learn more about this topic, see Chapter 6, entitled ʺFlow Control,ʺ on page 215.

</td>
<td style="background-color:#e8e8e8">

1 ## **流控 (Flow Control)** 

2 第二个主要的链路层功能是流控 (Flow Control)。在上电或复位后,该机制由数据链路层 (Data Link Layer) 在硬件中自动初始化,然后在运行时更新。其概述已在 TLP 章节中介绍,此处不再重复。要了解有关此主题的更多信息,请参阅第 215 页的第 6 章"Flow Control"。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-12"></a>
## 4.12 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Power Management** 

Finally, the Link Layer participates in power management, as well, because DLLPs are used to communicate the requests and handshakes associated with Link and system power states. For a detailed discussion on this topic, refer to Chapter 16, entitled ʺPower Management,ʺ on page 703.

</td>
<td style="background-color:#e8e8e8">

## **电源管理 (Power Management)** 

最后，链路层同样也参与电源管理 (Power Management)，这是因为 DLLP 被用于传递与链路 (Link) 和系统电源状态相关的请求与握手过程。有关该主题的详细讨论，请参阅第 16 章《电源管理 (Power Management)》，位于第 703 页。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-13"></a>
## 4.13 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Physical Layer**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-14"></a>
## 4.14 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **General** 

The Physical Layer is the lowest hierarchical layer for PCIe as shown in Figure 2‐14 on page 58. Both TLP and DLLP type packets are forwarded down from the Data Link Layer to the Physical Layer for transmission over the Link and for‐ warded up to the Data Link Layer at the Receiver. The spec divides the Physical Layer discussion into two portions: a logical part and an electrical part, and we’ll preserve that split here as well. The Logical Physical Layer contains the digital logic associated with preparing the packets for serial transmission on the Link and reversing that process for inbound packets. The Electrical Physical Layer is the analog interface of the Physical Layer that connects to the Link and consists of differential drivers and receivers for each lane. 

**76** 

**Chapter 2: PCIe Architecture Overview**

</td>
<td style="background-color:#e8e8e8">

## **概述** 

物理层是 PCIe 层级结构中最低的一层，如图 2‐14（第 58 页）所示。TLP 和 DLLP 类型的分组都从数据链路层向下转发到物理层，以便在链路上传输，并在接收端向上转发给数据链路层。规范将物理层的讨论分为两部分：逻辑部分和电气部分，我们在这里也保留这种划分方式。逻辑物理层包含与分组准备用于链路上串行传输相关的数字逻辑，以及对入站分组的逆向处理过程。电气物理层是物理层连接到链路的模拟接口，由每个通道的差分驱动器和接收器组成。 

**76** 

**第 2 章：PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-15"></a>
## 4.15 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Physical Layer - Logical** 

TLPs and DLLPs from the Data Link Layer are clocked into a buffer in the Phys‐ ical Layer, where Start and End characters are added to facilitate detection of the packet boundaries at the receiver. Since the Start and End characters appear on both ends of a packet they are also called “framing” characters. The framing characters are shown appended to a TLP and DLLP in Figure 2‐28 on page 77, which also shows the size of each field. 

_Figure 2‐28: TLP and DLLP Structure at the Physical Layer_ 

**==> picture [366 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transaction Layer Packet (TLP)<br>Start Sequence Header Data Payload  ECRC LCRC End<br>1B 2B 3-4 DW 0-1024 DW 1DW 1DW 1B<br>DLLP<br>Start DLLP Type Misc. CRC End<br>1B 2B 1B<br>1DW<br>**----- End of picture text -----**<br>

Within this layer, each byte of a packet is split out across all of the lanes in use for the Link in a process called byte striping. Effectively, each lane operates as an independent serial path across the Link and their data is all aggregated back together at the receiver. Each byte is scrambled to reduce repetitive patterns on the transmission line and reduce EMI (electro‐magnetic interference) seen on the Link. For the first two generations of PCIe (Gen1 and Gen2 PCIe), the 8‐bit characters are encoded into 10‐bit “symbols” using what is called 8b/10b encod‐ ing logic. This encoding adds overhead to the outgoing data stream, but also adds a number of useful characteristics (for more on this, see “8b/10b Encod‐ ing” on page 380). Gen3 Physical Layer logic when transmitting at Gen3 speed, does not encode the packet bytes using 8b/10b encoding. Rather another encod‐ ing scheme referred to as 128b/130b encoding is employed with the packet bytes scrambled transmitted. The 10b symbols on each Lane (Gen1 and Gen2) or the packet bytes on each Lane (Gen3) are then serialized and clocked out differen‐ tially on each Lane of the Link at 2.5 GT/s (Gen1), or 5 GT/s (Gen2) or 8 GT/s (Gen3). 

**77**

</td>
<td style="background-color:#e8e8e8">

## **物理层 - 逻辑**

来自数据链路层 (Data Link Layer) 的 TLP 和 DLLP 被时钟送入物理层 (Physical Layer) 中的一个缓冲区,在该缓冲区中,会在包的两端添加起始 (Start) 和结束 (End) 字符,以便于在接收端检测包的边界。由于起始和结束字符出现在包的两端,因此它们也被称为"成帧 (framing)"字符。图 2‐28 (第 77 页) 中展示了附加在 TLP 和 DLLP 上的成帧字符,同时还显示了每个字段的大小。

_图 2‐28:物理层处的 TLP 和 DLLP 结构_

**==> 图片 [366 x 150] 已省略 <==**

**----- 图片文字起始 -----**<br>
事务层包 (TLP)<br>起始 序列号 包头 数据载荷  ECRC LCRC 结束<br>1B 2B 3-4 DW 0-1024 DW 1DW 1DW 1B<br>DLLP<br>起始 DLLP 类型 杂项 CRC 结束<br>1B 2B 1B<br>1DW<br>**----- 图片文字结束 -----**<br>

在该层内,数据包的每个字节都会通过一种称为字节拆分 (byte striping) 的过程分配到链路 (Link) 正在使用的所有通道 (Lane) 上。实际上,每条通道都作为一条穿越链路的独立串行路径运行,它们的数据在接收端被重新聚合在一起。每个字节都会被加扰 (scrambling),以减少传输线上的重复模式,并降低链路上观察到的 EMI (电磁干扰)。对于 PCIe 的前两代 (Gen1 和 Gen2 PCIe),8 位字符会通过所谓的 8b/10b 编码 (encoding) 逻辑编码为 10 位的"符号 (symbols)"。这种编码会给输出数据流带来一定的开销,但同时也带来了一些有用的特性 (更多相关内容,请参见第 380 页的"8b/10b 编码")。Gen3 物理层逻辑在以 Gen3 速率传输时,并不使用 8b/10b 编码对包的字节进行编码,而是采用另一种称为 128b/130b 编码 的方案,并对包字节进行加扰后传输。每条通道上的 10b 符号 (Gen1 和 Gen2) 或每条通道上的包字节 (Gen3),随后被串行化,并以 2.5 GT/s (Gen1)、5 GT/s (Gen2) 或 8 GT/s (Gen3) 的速率,以差分方式在链路的每条通道上时钟输出。

**77**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-16"></a>
## 4.16 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

Receivers clock in the packet bits at the trained clock speeds as they arrive on all lanes. If 8b/10b is in use (at Gen1 and Gen2 mode), the serial bit stream of the packet is converted into 10‐bit symbols using a deserializer so it’s ready for 8b/ 10b decoding. However, before decoding, the symbols pass through an elastic buffer, a clever device that compensates for the slight difference in frequency between the internal clocks of two connected devices. Next, the 10‐bit symbol stream is decoded back to the proper 8‐bit characters via an 8b/10b decoder. Gen3 Physical Layer logic, when receiving serial bit stream of the packet at Gen3 speed, will convert it into a byte stream using a deserializer that has estab‐ lished block lock. The byte stream is passed through an elastic buffer which does clock tolerance compensation. The 8b/10b decoder stage is skipped given packets clocked at Gen3 speeds are not 8b/10b encoded. The 8‐bit characters on all lanes are de‐scrambled, the bytes from all the lanes are un‐striped back into a single character stream and, finally, the original data stream from the Transmit‐ ter is recovered.

</td>
<td style="background-color:#e8e8e8">

## **PCI Express 技术**

接收器 (Receiver) 以训练后的时钟速率,把所有通道 (Lane) 上到达的报文比特锁存进来。如果使用了 8b/10b 编码(在 Gen1 和 Gen2 模式下),报文的串行比特流会通过解串器 (SerDes) 转换为 10 比特符号,以便送入 8b/10b 解码器。然而,在解码之前,这些符号会先经过一个弹性缓冲区(elastic buffer)——一种巧妙设计的器件,用于补偿两个互连设备内部时钟之间细微的频率差异。接着,10 比特符号流会通过 8b/10b 解码器被还原为正确的 8 比特字符。Gen3 物理层 (Physical Layer) 逻辑在以 Gen3 速率接收报文的串行比特流时,会利用已建立块锁定 (block lock) 的解串器把它转换为字节流。该字节流会穿过一个弹性缓冲区以完成时钟容差补偿。由于以 Gen3 速率锁存的报文并未经过 8b/10b 编码,因此会跳过 8b/10b 解码阶段。随后,所有通道上的 8 比特字符会被解扰 (De-scrambling),来自各通道的字节被反向去条带化 (un-striped) 合并为单一的字符流,最终恢复出由发送器 (Transmitter) 发出的原始数据流。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-17"></a>
## 4.17 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Link Training and Initialization** 

Another responsibility of the Physical Layer is the initialization and training process on the Link. In this fully automatic process, several steps are taken to prepare the Link for normal operation, which involves determining the status of several optional conditions. For example, the Link width can be from one lane to 32 lanes, and multiple speeds might be available. The training process will discover these options and go through a state machine sequence to resolve the best combination. In that process, several things are checked or established to ensure proper and optimal operation, such as: 

- Link width 

- Link data rate 

- Lane reversal ‐ Lanes connected in reverse order 

- Polarity inversion ‐ Lane polarity connected backward 

- Bit lock per Lane ‐ Recovering the transmitter clock 

- Symbol lock per Lane ‐ Finding a recognizable position in the bit‐stream 

- Lane‐to‐Lane de‐skew within a multi‐Lane Link.

</td>
<td style="background-color:#e8e8e8">

## **链路训练与初始化** 

物理层（Physical Layer）的另一项职责是链路（Link）上的初始化和训练过程。在这个全自动化的过程中，需要执行多个步骤来为链路的正常运行做好准备，其中涉及到确定多个可选条件的状态。例如，链路宽度可以从一条通道（Lane）到 32 条通道不等，并且可能有多种速率可用。训练过程将发现这些选项，并通过状态机序列来确定最佳组合。在该过程中，会检查或建立多个事项以确保正确且最优的运行，例如：

- 链路宽度 

- 链路数据速率 

- 通道反转 ‐ 通道以相反的顺序连接 

- 极性反转 ‐ 通道极性反向连接 

- 每条通道的比特锁定 ‐ 恢复发送器（Transmitter）时钟 

- 每条通道的符号锁定 ‐ 在比特流中找到一个可识别的位置 

- 多通道链路（Link）内通道与通道之间的去偏斜（de-skew）。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-18"></a>
## 4.18 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Physical Layer - Electrical** 

The physical sender and receiver on a Link are connected with an AC‐coupled Link as shown in Figure 2‐29 on page 79. The term “AC‐coupled” simply means that a capacitor resides physically in the path between the devices and serves to pass the high‐frequency (AC) component of the signal while blocking the low‐ frequency (DC) part. Many serial transports use this approach because it allows the common mode voltage (the level at which the positive and negative versions 

**78** 

**Chapter 2: PCIe Architecture Overview** 

of the signal cross) to be different at the transmitter and receiver, meaning they’re not required to have the same reference voltage. This isn’t a big issue if the two devices are nearby and in the same box, but if they were in different buildings it would be very difficult for them to have a common reference volt‐ age that was precisely the same. 

_Figure 2‐29: Physical Layer Electrical_ 

**==> picture [347 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
CTX ZTX<br>+ +<br>ZTX ZRX<br>Transmitter Link Receiver<br>CTX ZTX ZRX<br>- -<br>ZTX<br>Zvtt Vtt<br>Transmitter is AC coupled to receiver<br>DC common-mode impedance is 50 Ohms<br>Differential impedance is 100 Ohms<br>Coupling capacitor is between 75-200 nF<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

## **物理层 - 电气** 

链路 (Link) 上的物理发送器与接收器之间采用交流耦合 (AC-coupled) 连接,如图 2-29(第 79 页)所示。"交流耦合"一词意味着在两个器件之间的物理路径上有一个电容,它的作用是让信号的高频(交流)分量通过,同时阻挡低频(直流)分量。许多串行传输都采用这种方式,因为它允许发送器与接收器使用不同的共模电压(即信号正负两端交叉的电平),也就是说它们不必使用相同的参考电压。如果两个器件在空间上很近、位于同一机箱内,这不会带来太大的问题;但如果它们位于不同的建筑物内,要让它们拥有精确相同的公共参考电压就会非常困难。 

_图 2-29:物理层电气_ 

**==> picture [347 x 161] intentionally omitted <==**

**----- Start of picture text -----**<br>
CTX ZTX<br>+ +<br>ZTX ZRX<br>发送器 链路 接收器<br>CTX ZTX ZRX<br>- -<br>ZTX<br>Zvtt Vtt<br>发送器与接收器之间采用交流耦合<br>直流共模阻抗为 50 欧姆<br>差分阻抗为 100 欧姆<br>耦合电容范围为 75-200 nF<br>**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-19"></a>
## 4.19 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Ordered Sets** 

The last type of traffic sent between devices uses only the Physical Layers. Although easily recognized by the receiver, this information is not technically in the form of a packet because it doesn’t have Start and End characters, for exam‐ ple. Instead, it’s organized into what are called Ordered Sets that originate at the Transmitter’s Physical Layer terminate at the Receiver’s Physical Layer, as shown in Figure 2‐30 on page 80. For Gen1 and Gen2 data rates, an Ordered Set starts with a single COM character followed by three or more other characters that define the information to be sent. The nomenclature for the type of charac‐ ters used in PCIe is discussed in more detail in “Character Notation” on page 382; for now it’s enough to say that the COM character has characteristics that make it work well for this purpose. Ordered Sets are always a multiple of 4 bytes in size, and an example is shown in Figure 2‐31 on page 80. In Gen3 mode of operation, the Ordered Set format is different from Gen1/Gen2 described above. Details to be covered in Chapter 14, entitled ʺLink Initialization & Train‐ ing,ʺ on page 505. Ordered Sets always terminate at the neighboring device and are not routed through the PCIe fabric. 

**79**

</td>
<td style="background-color:#e8e8e8">

## **有序集(Ordered Sets)**

设备之间发送的最后一种流量类型仅使用物理层 (Physical Layer)。尽管接收器很容易识别这些信息,但由于它并不具备起始字符和结束字符等形式,因此从严格意义上来说它并不是以数据包的形式存在的。相反,它被组织成所谓的"有序集(Ordered Sets)",由发送器 (Transmitter) 的物理层产生,并在接收器 (Receiver) 的物理层终止,如图 2-30(第 80 页)所示。对于 Gen1 和 Gen2 数据速率,有序集以单个 COM 字符开始,后面跟着三个或更多其他字符,这些字符定义了要发送的信息。PCIe 中所用字符类型的命名法将在第 382 页的"字符表示法(Character Notation)"中详细讨论;目前只需要知道 COM 字符具有使其非常适合此用途的特性即可。有序集的大小始终是 4 字节的整数倍,示例如图 2-31(第 80 页)所示。在 Gen3 工作模式下,有序集的格式不同于上文所述的 Gen1/Gen2。相关详情将在第 505 页第 14 章"链路初始化与训练(Link Initialization & Training)"中介绍。有序集始终在相邻设备处终止,不会通过 PCIe Fabric 进行路由转发。

**79**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-20"></a>
## 4.20 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

_Figure 2‐30: Ordered Sets Origin and Destination_ 

**==> picture [339 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Ordered Set Physical Layer Physical Layer Ordered Set<br>Transmitted Received<br>(RX) (TX) (RX) (TX)<br>Link<br>**----- End of picture text -----**<br>

Ordered Sets are used in the Link Training process, as described in Chapter 14, entitled ʺLink Initialization & Training,ʺ on page 505. They’re also used to com‐ pensate for the slight differences between the internal clocks of the transmitter and receiver, a process called clock tolerance compensation. Finally, Ordered Sets are used to indicate entry into or exit from a low power state on the Link. 

_Figure 2‐31: Ordered‐Set Structure_ 

**==> picture [205 x 73] intentionally omitted <==**

**----- Start of picture text -----**<br>
COM Identifier Identifier Identifier<br>**----- End of picture text -----**<br>

**80** 

**Chapter 2: PCIe Architecture Overview**

</td>
<td style="background-color:#e8e8e8">

## **PCI Ex ress Technolo p gy** 

_图 2‐30:有序集的源与目的_

**==> picture [339 x 233] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe 设备 A PCIe 设备 B<br>
设备核心 设备核心<br>
PCIe 核心 PCIe 核心<br>
硬件/软件 硬件/软件<br>
接口 接口<br>
事务层 事务层<br>
数据链路层 数据链路层<br>
有序集 物理层 物理层 有序集<br>
发送 接收<br>
(RX) (TX) (RX) (TX)<br>
链路 (Link)<br>
**----- End of picture text -----**<br>

有序集用于链路训练过程中,如第 14 章(标题为"链路初始化与训练",第 505 页)所述。它们还用于补偿发送器与接收器内部时钟之间的微小差异,这一过程称为时钟容差补偿。最后,有序集还用于指示链路进入或退出低功耗状态。 

_图 2‐31:有序集结构_

**==> picture [205 x 73] intentionally omitted <==**

**----- Start of picture text -----**<br>
COM 标识符 标识符 标识符<br>
**----- End of picture text -----**<br>

**80** 

**第 2 章:PCIe 架构概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-21"></a>
## 4.21 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Protocol Review Example** 

At this point, let’s review the overall Link protocol by using an example to illus‐ trate the steps that take place from the time a Requester initiates a memory read request until it obtains the requested data from a Completer.

</td>
<td style="background-color:#e8e8e8">

## **协议回顾示例**

在这一点上,让我们通过一个示例来回顾整体链路 (Link) 协议,以说明从请求者 (Requester) 发起内存读请求,直到从完成者 (Completer) 获取所请求数据这一过程中所发生的各个步骤。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-22"></a>
## 4.22 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Memory Read Request** 

For the first part of the discussion, refer to Figure 2‐32 on page 81. The Requester’s Device Core or Software Layer sends a request to the Transaction Layer and includes the following information: 32‐bit or 64‐bit memory address, transaction type, amount of data to read calculated in dwords, traffic class, byte enables, attributes etc. 

_Figure 2‐32: Memory Read Request Phase_ 

**==> picture [365 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>
Requester Completer<br>Send Memory Read Request Software layer Receive Memory Read Request<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header ECRC Header ECRC<br>Flow Control Transaction layer Flow Control<br>Virtual Channel Transmit Virtual Channel Receive<br>Management Buffers Management Buffers<br>per VC per VC<br>Ordering Ordering<br>Link Packet DLLP<br>Link Packet<br>Sequence TLP LCRC Nak Sequence TLP LCRC<br>Data Link layer<br>Retry Buffer DLLP. Error<br>Ack/Nak CRC Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Encode Physical layer Decode<br>Parallel-to-Serial Serial-to-Parallel<br>Differential Driver Differential Receiver<br>Port Port<br>Ack or Nak<br>Link<br>MRd TLP<br>**----- End of picture text -----**<br>

**81**

</td>
<td style="background-color:#e8e8e8">

## **内存读请求** 

在讨论的第一部分,请参考第 81 页的图 2‐32。请求者的设备内核或软件层向事务层发送请求,并包含以下信息:32 位或 64 位内存地址、事务类型、以双字 (dword) 计算的待读取数据量、流量类 (TC)、字节使能 (Byte Enable)、属性 (Attr) 等。 

_图 2‐32:内存读请求阶段_ 

**==> 图片 [365 x 246] 故意省略 <==**

**----- 图片文字开始 -----**<br>
请求者 完成者 (Completer)<br>发送内存读请求 软件层 接收内存读请求<br>事务层包 (TLP) 事务层包 (TLP)<br>包头 (Header) ECRC 包头 (Header) ECRC<br>流控 (Flow Control) 事务层 流控 (Flow Control)<br>虚通道 (VC) 发送 虚通道 (VC) 接收<br>管理 管理<br>缓冲区 (Buffers) 缓冲区 (Buffers)<br>每 VC 每 VC<br>排序 (Ordering) 排序 (Ordering)<br>链路 数据链路层包 (DLLP)<br>链路包<br>序列号 TLP LCRC Nak 序列号 TLP LCRC<br>数据链路层<br>重传缓冲区 (Retry Buffer) DLLP. 错误<br>确认/否认 (Ack/Nak) CRC 校验<br>物理包 物理包<br>链路包开始 链路包结束 链路包开始 链路包结束<br>编码 (Encode) 物理层 解码 (Decode)<br>并转串 串转并<br>差分驱动器 差分接收器<br>端口 端口<br>确认或否认 (Ack 或 Nak)<br>链路 (Link)<br>MRd TLP<br>**----- 图片文字结束 -----**<br>

**81**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-23"></a>
## 4.23 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

The Transaction layer uses this information to build a MRd TLP. The details of the TLP packet format are described later, but for now it’s enough to say that a 3 DW or 4 DW header is created depending on address size (32‐bit or 64‐bit). In addition, the Transaction Layer adds the Requester ID (bus#, device#, function#) to the header so the Completer can use that to return the completion. The TLP is placed in the appropriate virtual channel buffer to wait its turn for transmis‐ sion. Once the TLP has been selected, the Flow Control logic confirms there is sufficient space available in the neighboring device’s receive buffer (VC), and then the memory read request TLP is sent to the Data Link Layer. 

The Data Link Layer adds a 12‐bit Sequence Number and a 32‐bit LCRC value to the packet. A copy of the TLP with Sequence Number and LCRC is stored in the Replay Buffer and the packet is forwarded to the Physical Layer. 

In the Physical Layer the Start and End characters are added to the packet, which is then byte striped across the available Lanes, scrambled, and 8b/10b encoded. Finally the bits are serialized on each lane and transmitted differen‐ tially across the Link to the neighbor. 

The Completer de‐serializes the incoming bit stream back into 10‐bit symbols and passes them through the elastic buffer. The 10‐bit symbols are decoded back to bytes and the bytes from all Lanes are de‐scrambled and un‐striped. The Start and End characters are detected and removed. The rest of the TLP is for‐ warded up to the Data Link Layer. 

The Completer’s Data Link Layer checks for LCRC errors in the received TLP and checks the Sequence Number for missing or out‐of‐sequence TLPs. If there’s no error, it creates an Ack that contains the same Sequence Number that was used in the read request. A 16‐bit CRC is calculated and appended to the Ack contents to create a DLLP that is sent back to the Physical Layer which adds the proper framing symbols and transmits the Ack DLLP to the Requester. 

The Requester Physical Layer receives the Ack DLLP, checks and removes the framing symbols, and forwards it up to the Data Link Layer. If the CRC is valid, it compares the acknowledged Sequence Number with the Sequence Numbers of the TLPs stored in the Replay Buffer. The stored memory read request TLP associated with the Ack received is recognized and that TLP is discarded from the Replay Buffer. If a Nak DLLP was received by the Requester instead, it would re‐send a copy of the stored memory read request TLP. Since the DLLP only has meaning to the Data Link Layer, nothing is forwarded to the Transac‐ tion Layer. 

**82** 

**Chapter 2: PCIe Architecture Overview** 

In addition to generating the Ack, the Completer’s Link Layer also forwards the TLP up to itʹs Transaction Layer. In the Completerʹs Transaction Layer, the TLP is placed in the appropriate VC receive buffer to be processed. An optional ECRC check can be performed, and if no error is found, the contents of the header (address, Requester ID, memory read transaction type, amount of data requested, traffic class etc.) are forwarded to the Completer’s Software Layer.

</td>
<td style="background-color:#e8e8e8">

## **PCI Express 技术**

事务层（Transaction Layer）使用这些信息来构建一个 MRd TLP（事务层包）。TLP 报文格式的细节稍后描述,但目前只需知道:根据地址大小(32 位或 64 位),会创建一个 3 DW 或 4 DW 的包头（Header）。此外,事务层会将请求者 ID（Requester ID,即总线号、设备号、功能号）添加到包头中,以便完成者（Completer）使用该 ID 返回完成报文（Completion）。TLP 被放入相应的虚通道（VC）缓冲区中,等待轮到自己发送。一旦该 TLP 被选中,流控（Flow Control）逻辑会确认相邻设备的接收缓冲区（VC）中有足够的空间,然后内存读请求 TLP 被发送到数据链路层（Data Link Layer）。

数据链路层在报文上附加一个 12 位的序列号（Sequence Number）和一个 32 位的 LCRC（链路 CRC）值。带有序列号和 LCRC 的 TLP 副本被存储在重放缓冲区（Replay Buffer）中,然后该报文被转发到物理层（Physical Layer）。

在物理层,起始字符和结束字符被添加到报文中,然后在可用通道（Lanes）之间进行字节分条（byte striped）、加扰（scrambled）以及 8b/10b 编码（encoding）。最后,比特在每个通道上被串行化,并通过链路（Link）以差分方式传输到对端设备。

完成者（Completer）将传入的比特流反串行化回 10 位符号,并将它们通过弹性缓冲区。10 位符号被解码回字节,所有通道的字节经过解扰（de-scrambled）和去分条（un-striped）处理。检测并移除起始字符和结束字符。TLP 的其余部分被向上转发到数据链路层。

完成者的数据链路层检查所接收 TLP 中的 LCRC 错误,并检查序列号以发现缺失或乱序的 TLP。如果没有错误,它会创建一个包含与读请求中所用相同序列号的 Ack（确认）。计算 16 位 CRC 并将其附加到 Ack 内容中,形成 DLLP（数据链路层包）,该 DLLP 被发送回物理层,由物理层添加适当的成帧符号（framing symbols）并将 Ack DLLP 传输给请求者（Requester）。

请求者的物理层接收 Ack DLLP,检查并移除成帧符号,然后将其向上转发到数据链路层。如果 CRC 有效,它会将所确认的序列号与重放缓冲区中存储的 TLP 的序列号进行比较。识别出与所接收 Ack 相关联的已存储内存读请求 TLP,并将该 TLP 从重放缓冲区中丢弃。如果请求者接收到的是 Nak DLLP,则它会重新发送所存储的内存读请求 TLP 的副本。由于 DLLP 仅对数据链路层有意义,因此不会向事务层转发任何内容。

**82**

**第 2 章:PCIe 架构概述**

除了生成 Ack 之外,完成者的链路层（Link Layer）还将 TLP 向上转发到其事务层。在完成者的事务层中,TLP 被放入相应的 VC 接收缓冲区中以进行处理。可以执行可选的 ECRC（端到端 CRC）检查,如果未发现错误,则包头的内容(地址、请求者 ID、内存读事务类型、请求的数据量、流量类（TC, Traffic Class)等)被转发到完成者的软件层。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-24"></a>
## 4.24 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Completion with Data** 

For the second half of this discussion, refer to Figure 2‐33 on page 83. To service the memory read request, the Completer Device Core/Software Layer sends a completion with data (CplD) request down to its Transaction Layer that includes the Requester ID and Tag copied from the original memory read request, transaction type, other parts of the completion header contents and the requested data. 

_Figure 2‐33: Completion with Data Phase_ 

**==> picture [374 x 257] intentionally omitted <==**

**----- Start of picture text -----**<br>
Requester Completer<br>Receive Completion with Data Software layer Send Completion with Data<br>Transaction Layer Packet (TLP) Transaction Layer Packet (TLP)<br>Header Data Payload  ECRC Header Data Payload  ECRC<br>Flow Control Transaction layer Flow Control<br>Virtual Channel Receive Virtual Channel Transmit<br>Management Buffers Management Buffers<br>per VC per VC<br>Ordering Ordering<br>Link Packet DLLP<br>Link Packet<br>Sequence TLP LCRC Sequence TLP LCRC Nak<br>Data Link layer<br>DLLP Error Retry Buffer<br>Ack/Nak CRC Check<br>Physical Packet Physical Packet<br>Start Link Packet End Start Link Packet End<br>Decode Physical layer Encode<br>Serial-to-Parallel Parallel-to-Serial<br>Differential Receiver Differential Driver<br>Port Port<br>CplD TLP<br>Link<br>Ack or Nak<br>**----- End of picture text -----**<br>

**83**

</td>
<td style="background-color:#e8e8e8">

## **带数据的完成 (Completion with Data)** 

在本讨论的后半部分,请参阅第 83 页的图 2-33。为了服务该内存读请求,完成器设备核心/软件层会向其事务层发送一个带数据的完成 (CplD) 请求,该请求包含从原始内存读请求中复制的请求者 ID 和 Tag 字段、事务类型、完成包头内容的其他部分以及所请求的数据。

_图 2-33:带数据的完成阶段 (Completion with Data Phase)_ 

**==> 图片 [374 x 257] 已被有意省略 <==**

**----- 图片文字开始 -----**<br>
请求者 (Requester) 完成器 (Completer)<br>接收 带数据的完成 (Receive Completion with Data) 软件层 发送 带数据的完成 (Send Completion with Data)<br>事务层包 (TLP) 事务层包 (TLP)<br>包头 数据净载荷  ECRC 包头 数据净载荷  ECRC<br>流控 (Flow Control) 事务层 流控 (Flow Control)<br>虚通道 (VC) 接收 虚通道 (VC) 发送<br>管理 管理<br>缓冲区 缓冲区<br>每 VC 每 VC<br>排序 排序<br>链路 DLLP<br>链路包 (Link Packet)<br>序列号 TLP LCRC 序列号 TLP LCRC NAK<br>数据链路层<br>DLLP 错误 重试缓冲区 (Retry Buffer)<br>Ack/Nak CRC 校验<br>物理包 (Physical Packet) 物理包 (Physical Packet)<br>链路包起始 链路包结束 链路包起始 链路包结束<br>解码 物理层 编码<br>串并转换 并串转换<br>差分接收器 (Receiver) 差分发送器 (Driver)<br>端口 (Port) 端口 (Port)<br>CplD TLP<br>链路 (Link)<br>Ack 或 Nak<br>**----- 图片文字结束 -----**<br>

**83**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-25"></a>
## 4.25 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

The Transaction layer uses this information to build the CplD TLP, which always has a 3 DW header (it uses ID routing and never needs a 64‐bit address). It also adds its own Completer ID to the header. This packet is also placed into the appropriate VC transmit buffer and, once selected, the flow control logic verifies that sufficient space is available at the neighboring device to receive this packet and, once confirmed, forwards the packet down to the Data Link Layer. 

As before, the Data Link Layer adds a 12‐bit Sequence Number and a 32‐bit LCRC to the packet. A copy of the TLP with Sequence Number and LCRC is stored in the Replay Buffer and the packet is forwarded to the Physical Layer. 

As before, the Physical Layer adds a Start and End character to the packet, byte stripes it across the available lanes, scrambles it, and 8b/10b encodes it. Finally, the CplD packet is serialized on all lanes and transmitted differentially across the Link to the neighbor. 

The Requester converts the incoming serial bit stream back to 10‐bit symbols and passes them through the elastic buffer. The 10‐bit symbols are decoded back to bytes, de‐scrambled and un‐striped. The Start and End characters are detected and removed and the resultant TLP is sent up to the Data Link Layer. 

As before, the Data Link Layer checks for LCRC errors in the received CplD TLP and checks the Sequence Number for missing or out‐of‐sequence TLPs. If there are no errors, it creates an Ack DLLP which contains the same Sequence Number as the CplD TLP used. A 16‐bit CRC is added to the Ack DLLP and it’s sent back to the Physical Layer which adds the proper framing symbols and transmits the Ack DLLP to the Completer. 

The Completer Physical Layer checks and removes the framing symbols from the Ack DLLP and sends the remainder up to the Data Link Layer which checks the CRC. If there are no errors, it compares the Sequence Number with the Sequence Numbers for the TLPs stored in the Replay Buffer. The stored CplD TLP associated with the Ack received is recognized and that TLP is discarded from the Replay Buffer. If a Nak DLLP was received by the Completer instead, it would re‐send a copy of the stored CplD TLP. 

In the meantime, the Requester Transaction Layer receives the CplD TLP in the appropriate virtual channel buffer. Optionally, the Transaction layer can check for an ECRC error. If there are no errors, it forwards the header contents and data payload, including the Completion Status, to the Requester Software Layer, and we’re done. 

**84**

</td>
<td style="background-color:#e8e8e8">

## **PCI Express 技术**

事务层使用此信息来构建 CplD TLP，它始终具有 3 DW 的包头（它使用 ID 路由，并且永远不需要 64 位地址）。它还会在包头中添加自己的 Completer ID（完成者 ID）。该报文也会被放入适当的 VC（虚通道）发送缓冲区中，一旦被选中，流控（Flow Control）逻辑会验证相邻设备是否有足够的空间来接收该报文，并在确认后将报文向下传递到数据链路层。

与之前一样，数据链路层向报文添加一个 12 位的序列号（Sequence Number）和一个 32 位的 LCRC（链路 CRC）。带有序列号和 LCRC 的 TLP 副本被存储在重放缓冲区（Replay Buffer）中，然后该报文被转发到物理层。

与之前一样，物理层向报文添加 Start（起始）和 End（结束）字符，将其按字节拆分到可用通道（Lane）上，对其进行加扰（Scrambling），并进行 8b/10b 编码。最后，CplD 报文在所有通道上序列化，并通过链路（Link）以差分方式传输到相邻设备。

请求者将传入的串行比特流转换回 10 位符号，并通过弹性缓冲区（elastic buffer）。10 位符号被解码回字节，进行解扰（De-scrambling）并取消字节拆分。检测并移除 Start 和 End 字符，然后将得到的 TLP 向上发送到数据链路层。

与之前一样，数据链路层检查接收到的 CplD TLP 中的 LCRC 错误，并检查序列号以检测是否有丢失或乱序的 TLP。如果无误，它会创建一个 Ack DLLP（确认 DLLP），其中包含与该 CplD TLP 相同的序列号。将 16 位 CRC 添加到 Ack DLLP，并将其发送回物理层，物理层为其添加适当的成帧符号，并将该 Ack DLLP 传输给完成者。

完成者的物理层检查并移除 Ack DLLP 中的成帧符号，并将其余部分向上发送到数据链路层，由数据链路层检查 CRC。如果无误，它会将序列号与重放缓冲区中存储的 TLP 的序列号进行比较。识别出与所接收的 Ack 相对应的已存储 CplD TLP，并将该 TLP 从重放缓冲区中丢弃。如果完成者收到的是 Nak DLLP（否认 DLLP），它将重新发送已存储 CplD TLP 的副本。

与此同时，请求者的事务层在适当的虚通道缓冲区中接收 CplD TLP。事务层可以选择性地检查 ECRC（端到端 CRC）错误。如果无误，它会将包头内容和数据有效负载（包括完成状态）转发到请求者软件层，至此完成整个过程。

**84**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-26"></a>
## 4.26 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## _**3**_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-27"></a>
## 4.27 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## _**Configuration Overview**_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-28"></a>
## 4.28 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **The Previous Chapter** 

The previous chapter provides a thorough introduction to the PCI Express architecture and is intended to serve as an “executive level” overview. It intro‐ duces the layered approach to PCIe port design described in the spec. The vari‐ ous packet types are introduced along with the transaction protocol.

</td>
<td style="background-color:#e8e8e8">

## **上一章**

上一章对 PCI Express 架构进行了全面的介绍，旨在作为"高管层"级别的概览。它介绍了规范中描述的 PCIe 端口设计的分层方法。各种报文类型与事务协议一同被引入。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-29"></a>
## 4.29 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **This Chapter** 

This chapter provides an introduction to configuration in the PCIe environ‐ ment. This includes the space in which a Function’s configuration registers are implemented, how a Function is discovered, how configuration transactions are generated and routed, the difference between PCI‐compatible configuration space and PCIe extended configuration space, and how software differentiates between an Endpoint and a Bridge.

</td>
<td style="background-color:#e8e8e8">

## **本章内容**

本章介绍了 PCIe 环境中的配置 (Configuration) 相关内容。其中包括 Function 的配置寄存器 (Configuration Registers) 所处的地址空间、如何发现 Function、如何生成与路由配置事务 (Configuration Transaction)、PCI 兼容配置空间 (PCI-Compatible Configuration Space) 与 PCIe 扩展配置空间 (Extended Configuration Space) 之间的差异，以及软件如何区分端点 (Endpoint) 和桥 (Bridge)。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-30"></a>
## 4.30 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **The Next Chapter** 

The next chapter describes the purpose and methods of a function requesting memory or IO address space through Base Address Registers (BARs) and how software initializes them. The chapter describes how bridge Base/Limit registers are initialized, thus allowing switches to route TLPs through the PCIe fabric.

</td>
<td style="background-color:#e8e8e8">

## **下一章**

下一章描述设备(功能)通过基址寄存器 (BAR) 请求内存或 IO 地址空间的目的与方法,以及软件如何初始化它们。本章将介绍桥的 Base/Limit 寄存器是如何被初始化的,从而使交换机 (Switch) 能够通过 PCIe Fabric 路由 TLP。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-31"></a>
## 4.31 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Definition of Bus, Device and Function** 

Just as in PCI, every PCIe Function is uniquely identified by the Device it resides within and the Bus to which the Device connects. This unique identifier is commonly referred to as a ‘BDF’. Configuration software is responsible for detecting every Bus, Device and Function (BDF) within a given topology. The following sections discuss the primary BDF characteristics in the context of a sample PCIe topology. Figure 3‐1 on page 87 depicts a PCIe topology that high‐ 

**85** 

**PCI Ex ress Technolo p gy** 

lights the Buses, Devices and Functions implemented in a sample system. Later in this chapter the process of assigning Bus and Device Numbers is explained.

</td>
<td style="background-color:#e8e8e8">

## **总线、设备与功能的定义**

与 PCI 一样，每个 PCIe 功能 (Function) 都通过其所在的设备 (Device) 以及该设备所连接的总线 (Bus) 来唯一标识。这个唯一标识通常被称为"BDF"。配置软件负责在给定的拓扑 (Topology) 中检测每一个总线、设备和功能 (BDF)。下面的章节将在一个示例 PCIe 拓扑的背景下讨论 BDF 的主要特性。第 87 页的图 3-1 展示了一个 PCIe 拓扑，该拓扑高亮

**85**

**PCI Express 技术**

显示了示例系统中实现的总线、设备和功能。本章稍后将解释分配总线号和设备号的过程。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-32"></a>
## 4.32 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCIe Buses** 

Up to 256 Bus Numbers can be assigned by configuration software. The initial Bus Number, Bus 0, is typically assigned by hardware to the Root Complex. Bus 0 consists of a Virtual PCI bus with integrated endpoints and Virtual PCI‐to‐PCI Bridges (P2P) which are hard‐coded with a Device number and Function num‐ ber. Each P2P bridge creates a new bus that additional PCIe devices can be con‐ nected to. Each bus must be assigned a unique bus number. Configuration software begins the process of assigning bus numbers by searching for bridges starting with Bus 0, Device 0, Function 0. When a bridge is found, software assigns the new bus a bus number that is unique and larger than the bus num‐ ber the bridge lives on. Once the new bus has been assigned a bus number, soft‐ ware begins looking for bridges on the new bus before continuing scanning for more bridges on the current bus. This is referred to as a “depth first search” and is described in detail in “Enumeration ‐ Discovering the Topology” on page 104.

</td>
<td style="background-color:#e8e8e8">

## **PCIe 总线**

配置软件最多可以分配 256 个总线号。初始的总线号——总线 0，通常由硬件分配给根复合体 (Root Complex)。总线 0 由一个虚拟 PCI 总线组成，其中集成了端点 (Endpoint) 以及硬编码了设备号和功能号的虚拟 PCI-to-PCI 桥 (P2P)。每个 P2P 桥都会创建一条新的总线，可以连接其他的 PCIe 设备。每条总线必须分配一个唯一的总线号。配置软件从总线 0、设备 0、功能 0 开始搜索桥，从而启动总线号的分配过程。当找到一个桥时，软件会为该桥所连的新总线分配一个唯一且大于该桥所在总线号的总线号。一旦为新总线分配了总线号，软件便会在继续扫描当前总线上更多桥之前，先开始在新总线上查找桥。这一过程被称为"深度优先搜索"，详细内容将在第 104 页的"枚举 —— 发现拓扑结构"中描述。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-33"></a>
## 4.33 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCIe Devices** 

PCIe permits up to 32 device attachments on a single PCI bus, however, the point‐to‐point nature of PCIe means only a single device can be attached directly to a PCIe link and that device will always end up being Device 0. Root Complexes and Switches have Virtual PCI buses which do allow multiple Devices being “attached” to the bus. Each Device must implement Function 0 and may contain a collection of up to eight Functions. When two or more Func‐ tions are implemented the Device is called a multi‐function device.

</td>
<td style="background-color:#e8e8e8">

## **PCIe 设备** 

PCIe 允许在单个 PCI 总线上最多挂载 32 个设备，然而，由于 PCIe 采用点对点（point‐to‐point）拓扑结构，一条 PCIe 链路（Link）只能直接连接一个设备，并且该设备始终会被编号为设备 0。根复合体（Root Complex）和交换机（Switch）内部具有虚拟 PCI 总线，这些虚拟总线上确实允许"挂载"多个设备。每个设备必须实现功能 0，并且可以包含最多八个功能的集合。当实现两个或更多功能时，该设备被称为多功能（multi‐function）设备。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-34"></a>
## 4.34 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCIe Functions** 

As previously discussed Functions are designed into every Device. These Func‐ tions may include hard drive interfaces, display controllers, ethernet control‐ lers, USB controllers, etc. Devices that have multiple Functions do not need to be implemented sequentially. For example, a Device might implement Func‐ tions 0, 2, and 7. As a result, when configuration software detects a multifunc‐ tion device, each of the possible Functions must be checked to learn which of them are present. Each Function also has its own configuration address space that is used to setup the resources associated with the Function. 

**86** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐1: Example System_ 

**==> picture [344 x 462] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Host/PCI<br>Bridge<br>Bus 0<br>Bus 0 Bus 0 Bus 0<br>Virtual Dev 0 Dev 1 Virtual Dev 2 Integr.<br>P2P Func 0 Func 0 P2P Func 0 EP<br>Bus 1 Bus 1 Bus 5 Bus 5<br>Dev 0 Bus 2 Bus 6 Dev 0<br>Func 0 Dev 2 Dev 1 Func 0<br>Bus 6<br>Func 0 Func 0<br>Dev 2<br>Bus 2 Func 0<br>Dev 1<br>Virtual<br>Func 0 Virtual<br>P2P<br>P2P<br>Bus 2 Bus 6 Bus 6<br>Dev 3<br>Virtual Virtual Virtual Virtual Virtual Func 0<br>P2P P2P P2P P2P P2P<br>Bus 3<br>Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 1 Function 0 Function 0 Function 0<br>Dev 0 Dev 0 Dev 0 Dev 0<br>Bus 8<br>Dev 0<br>Express Func 0<br>PCI<br>Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>Dev 1 Dev 2 Dev 3<br>Func 0 Func 0 Func 0<br>**----- End of picture text -----**<br>

**87** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

## **PCIe 功能 (Function)**

如前所述,每个 Device(设备)中都设计有 Function(功能)。这些 Function 可以包括硬盘接口、显示控制器、以太网控制器、USB 控制器等。具有多个 Function 的 Device 不需要按顺序实现。例如,一个 Device 可能实现 Function 0、2 和 7。因此,当配置软件检测到多功能 (multifunction) 设备时,必须检查每个可能的 Function 以了解其中哪些 Function 存在。每个 Function 也都有自己的配置地址空间,用于设置与该 Function 关联的资源。

**86**

**第 3 章:配置概述**

_图 3-1:示例系统_

**==> picture [344 x 462] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>根复合体 (Root Complex)<br>主桥 (Host/PCI Bridge)<br>Bus 0<br>Bus 0 Bus 0 Bus 0<br>Virtual Dev 0 Dev 1 Virtual Dev 2 Integr.<br>P2P Func 0 Func 0 P2P Func 0 EP<br>Bus 1 Bus 1 Bus 5 Bus 5<br>Dev 0 Bus 2 Bus 6 Dev 0<br>Func 0 Dev 2 Dev 1 Func 0<br>Bus 6<br>Func 0 Func 0<br>Dev 2<br>Bus 2 Func 0<br>Dev 1<br>Virtual<br>Func 0 Virtual<br>P2P<br>P2P<br>Bus 2 Bus 6 Bus 6<br>Dev 3<br>Virtual Virtual Virtual Virtual Virtual Func 0<br>P2P P2P P2P P2P P2P<br>Bus 3<br>Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 1 Function 0 Function 0 Function 0<br>Dev 0 Dev 0 Dev 0 Dev 0<br>Bus 8<br>Dev 0<br>Express Func 0<br>PCI<br>Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>Dev 1 Dev 2 Dev 3<br>Func 0 Func 0 Func 0<br>**----- End of picture text -----**<br>

**87**

**PCI Express 技术**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-35"></a>
## 4.35 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Configuration Address Space** 

The first PCs required users to set switches and jumpers to assign resources for each card installed and this frequently resulted in conflicting memory, IO and interrupt settings. The subsequent IO architectures, Extended ISA (EISA) and the IBM PS2 systems, were the first to implemented plug and play architectures. In these architectures configuration files were shipped with each plug‐in card that allowed system software to assign basic resources. PCI extended this capa‐ bility by implementing standardized configuration registers that permit generic shrink‐wrapped OSs to manage virtually all system resources. Having a stan‐ dard way to enable error reporting, interrupt delivery, address mapping and more, allows one entity, the configuration software, to allocate and configure the system resources which virtually eliminates resource conflicts. 

PCI defines a dedicated block of configuration address space for each Function. Registers mapped into the configuration space allow software to discover the existence of a Function, configure it for normal operation and check the status of the Function. Most of the basic functionality that needs to be standardized is in the header portion of the configuration register block, but the PCI architects realized that it would beneficial to standardize optional features, called capabil‐ ity structures (e.g. Power Management, Hot Plug, etc.). The PCI‐Compatible configuration space includes 256 bytes for each Function.

</td>
<td style="background-color:#e8e8e8">

## **配置地址空间** 

早期的 PC 要求用户通过设置开关和跳线来为每块已安装的卡分配资源,这种方式经常导致内存、IO 和中断设置发生冲突。随后的 IO 架构——扩展 ISA (EISA) 和 IBM PS2 系统——是首批实现即插即用架构的体系。在这些架构中,每块即插即用卡都会附带配置文件,系统软件借此可分配基本资源。PCI 通过实现标准化的配置寄存器扩展了这一能力,使得通用的通用包装 (shrink-wrapped) 操作系统能够管理几乎所有的系统资源。借助启用错误报告、中断传递、地址映射等功能的标准化方式,作为单一实体的配置软件可以分配和配置系统资源,从而几乎消除了资源冲突。 

PCI 为每个功能 (Function) 定义了一段专用的配置地址空间块。映射到该配置空间中的寄存器允许软件发现功能 (Function) 的存在,对其进行正常操作的配置,并检查该功能 (Function) 的状态。需要标准化的大部分基本功能位于配置寄存器块的头部 (Header) 部分,但 PCI 架构师们意识到将可选特性——称为能力结构 (Capability Structure)(例如电源管理 (Power Management)、热插拔 (Hot Plug) 等)——标准化也会带来裨益。PCI 兼容 (PCI-Compatible) 的配置空间为每个功能 (Function) 提供 256 字节。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-36"></a>
## 4.36 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI-Compatible Space** 

Refer to Figure 3‐2 on page 89 during the following discussion. The 256 bytes of PCI‐compatible configuration space was so named because it was originally designed for PCI. The first 16 dwords (64 bytes) of this space are the configura‐ tion header (Header Type 0 or Header Type 1). Type 0 headers are required for every Function except for the bridge functions that use a Type 1 header. The remaining 48 dwords are used for optional registers including PCI capability structures. For PCIe Functions, some capability structures are required. For example, PCIe Functions must implement the following Capability Structures: 

- PCI Express Capability 

- Power Management 

- MSI and/or MSI‐X 

**88** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐2: PCI Compatible Configuration Register Space_ 

**==> picture [376 x 263] intentionally omitted <==**

**----- Start of picture text -----**<br>
256-Byte Type 0 Header Type 1 Header<br>Configuration Register Byte Doubleword Byte Doubleword<br>Space (per Function) 3 2 1 0 3 2 1 0<br>Device ID Vendor ID 00 Device ID Vendor ID 00<br>Status Command 01 Status Command 01<br>64-Bytes<br>PCI Configuration Class Code RevisionID 02 Class Code RevisionID 02<br>Header Space BIST HeaderType LatencyTimer Cache LineSize 03 BIST HeaderType LatencyTimer Cache LineSize 03<br>Base Address 0 04 Base Address 0 04<br>Base Address 1 05 Base Address 1 05<br>Base Address 2 06 Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>Base Address 3 07 Secondary Status I/O Limit I/O Base 07<br>Base Address 4 08 Memory Limit Memory Base 08<br>Base Address 5 09 Prefetchable Prefetchable 09<br>192-Bytes Memory Limit Memory Base<br>Capability CardBus CIS Pointer 10 Prefetchable Base - Upper 32-bits 10<br>Structures Subsystem ID SubsystemVendor ID 11 Prefetchable Limit - Upper 32-bits 11<br>Expansion ROM Base Address 12 Upper 16-bitsI/O Limit Upper 16-bitsI/O Base 12<br>Reserved CapabilitiesPointer 13 Reserved CapabilitiesPointer 13<br>Reserved 14 Expansion ROM Base Address 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 Bridge Control InterruptPin InterruptLine 15<br>Required Config Registers<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

## **PCI 兼容空间**

在接下来的讨论中,请参阅第 89 页的图 3‐2。256 字节的 PCI 兼容配置空间之所以这样命名,是因为它最初是为 PCI 设计的。该空间的前 16 个双字(64 字节)是配置头部(头部类型 0 或头部类型 1)。除了使用类型 1 头部的桥功能(桥 (Bridge))外,所有功能(端点 (Endpoint))都必须实现类型 0 头部。剩余的 48 个双字用于可选寄存器,包括 PCI 能力结构。对于 PCIe 功能(端点 (Endpoint)),某些能力结构是必需的。例如,PCIe 功能(端点 (Endpoint))必须实现以下能力结构:

- PCI Express 能力结构 (Capability)

- 电源管理 (Power Management)

- MSI (消息信号中断) 和/或 MSI-X (扩展消息信号中断)

**88**

**第 3 章:配置概述**

_图 3‐2:PCI 兼容配置寄存器空间_

**==> picture [376 x 263] intentionally omitted <==**

**----- Start of picture text -----**<br>
256-Byte Type 0 Header Type 1 Header<br>Configuration Register Byte Doubleword Byte Doubleword<br>Space (per Function) 3 2 1 0 3 2 1 0<br>Device ID Vendor ID 00 Device ID Vendor ID 00<br>Status Command 01 Status Command 01<br>64-Bytes<br>PCI Configuration Class Code RevisionID 02 Class Code RevisionID 02<br>Header Space BIST HeaderType LatencyTimer Cache LineSize 03 BIST HeaderType LatencyTimer Cache LineSize 03<br>Base Address 0 04 Base Address 0 04<br>Base Address 1 05 Base Address 1 05<br>Base Address 2 06 Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>Base Address 3 07 Secondary Status I/O Limit I/O Base 07<br>Base Address 4 08 Memory Limit Memory Base 08<br>Base Address 5 09 Prefetchable Prefetchable 09<br>192-Bytes Memory Limit Memory Base<br>Capability CardBus CIS Pointer 10 Prefetchable Base - Upper 32-bits 10<br>Structures Subsystem ID SubsystemVendor ID 11 Prefetchable Limit - Upper 32-bits 11<br>Expansion ROM Base Address 12 Upper 16-bitsI/O Limit Upper 16-bitsI/O Base 12<br>Reserved CapabilitiesPointer 13 Reserved CapabilitiesPointer 13<br>Reserved 14 Expansion ROM Base Address 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 Bridge Control InterruptPin InterruptLine 15<br>Required Config Registers<br>**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-37"></a>
## 4.37 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Extended Configuration Space** 

Refer to Figure 3‐3 on page 90 during this discussion. When PCIe was intro‐ duced, there was not enough room in the original 256‐byte configuration region to contain all the new capability structures needed. So the size of configuration space was expanded from 256 bytes per function to 4KB, called the Extended Configuration Space. The 960‐dword Extended Configuration area is only accessible using the Enhanced configuration mechanism and is therefore not visible to legacy PCI software. It contains additional optional Extended Capabil‐ ity registers for PCIe such as those listed in Figure 3‐3 (not a complete list). 

**89** 

**PCI Ex ress Technolo p gy** 

_Figure 3‐3: 4KB Configuration Space per PCI Express Function_ 

**==> picture [372 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
Config Header Byte Dword<br>3 2 1 0<br>PCI Config Hdr Offset 000h Device IDStatus CommandVendor ID 0001<br>16 DWs Class Code RevisionID 02<br>PCI-Compatible space is PCI Device-specific Offset 040h BIST HeaderType LatencyTimer Cache LineSize 03<br>accessible by legacy Base Address 0 04<br>& New Capability<br>PCI software or PCIe  register sets Base Address 1 05<br>Enhanced Configuration Base Address 2 06<br>Access Mechanism Base Address 3 07<br>48 DWs Base Address 4 08<br>Offset 100h Base Address 5 09<br>CardBus CIS Pointer 10<br>PCIe ExtendedConfiguration Expansion ROM Base AddressSubsystem ID SubsystemVendor ID 1112<br>Register Space Reserved CapabilitiesPointer 13<br>Capability registersOptional Extended Max_Lat Min_GntReservedInterruptPin InterruptLine 1415<br>implemented in this space,<br>such as: PCIe Capability Structure<br>PCIe Extended space is<br>must be implemented in<br>only accessible by PCIe<br>- Advanced Error Reporting this register space<br>Enhanced Configuration - Virtual Channels<br>Access Mechanism<br>- Device Serial Number<br>- Power Budgeting<br>960 DWs Offset FFFh<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

## **扩展配置空间**

在本节讨论中请参考第 90 页的图 3-3。当 PCIe 推出时,原有的 256 字节配置区域已经没有足够的空间来容纳所有所需的新能力结构。因此配置空间的大小从每个功能 256 字节扩展到了 4KB,称为扩展配置空间(Extended Configuration Space)。960 个双字的扩展配置区域只能通过增强配置机制访问,因此对传统 PCI 软件不可见。它包含 PCIe 所需的额外可选扩展能力寄存器,如图 3-3 中所列(并非完整列表)。

**89**

**PCI Express 技术**

_图 3-3:每个 PCI Express 功能的 4KB 配置空间_

**==> picture [372 x 318] intentionally omitted <==**

**----- Start of picture text -----**<br>
配置头 字节 双字<br>
3 2 1 0<br>
PCI 配置头 偏移 000h 设备 ID 状态 命令 厂商 ID 0001<br>
16 个双字 类代码 修订版本 ID 02<br>
PCI 兼容空间是 PCI 设备特定 偏移 040h BIST 头类型 延迟定时器 高速缓存行大小 03<br>
可由传统软件和新的能力 通过传统 PCI 软件访问 或 PCIe 增强配置 基址寄存器 0 04<br>
寄存器集 访问机制 基址寄存器 1 05<br>
基址寄存器 2 06<br>
48 个双字 基址寄存器 3 07<br>
偏移 100h 基址寄存器 4 08<br>
基址寄存器 5 09<br>
CardBus CIS 指针 10<br>
PCIe 扩展配置 扩展 ROM 基址 子系统 ID 子系统厂商 ID 11 12<br>
寄存器空间 保留 能力指针 13<br>
能力寄存器 此空间中实现的<br>
可选扩展 最大延迟 最小授权 保留 中断引脚 中断线 14 15<br>
例如:PCIe 能力结构<br>
PCIe 扩展空间必须在此寄存器<br>
- 高级错误报告 空间中实现,仅可通过<br>
- 虚通道(VC) PCIe 增强配置访问机制访问<br>
- 设备序列号<br>
- 功率预算<br>
960 个双字 偏移 FFFh<br>
**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-38"></a>
## 4.38 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Host-to-PCI Bridge Configuration Registers**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-39"></a>
## 4.39 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **General** 

The Host‐to‐PCI bridge’s configuration registers don’t have to be accessible using either of the configuration mechanisms mentioned in the previous sec‐ tion. Instead, itʹs typically implemented as device‐specific registers in memory address space, which is known by the platform firmware. However, its configu‐ ration register layout and usage must adhere to the standard Type 0 template defined by the PCI 2.3 specification. 

**90** 

**Cha ter 3: Confi uration Overview p g**

</td>
<td style="background-color:#e8e8e8">

## **概述**

Host‐to‐PCI 桥的配置寄存器不必通过上一节中提到的任一配置机制来访问。相反，它通常作为内存地址空间中的设备特定寄存器实现，这一点平台固件是知道的。然而，其配置寄存器的布局和使用必须遵循 PCI 2.3 规范定义的标准 Type 0 模板。

**90**

**第 3 章：配置概述**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-40"></a>
## 4.40 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Only the Root Sends Configuration Requests** 

The specification states that only the Root Complex is permitted to originate Configuration Requests. It acts as the system processor’s liaison to inject Requests into the fabric and pass Completions back. The ability to originate configuration transactions is restricted to the processor through the Root Com‐ plex to avoid the anarchy that could result if any device had the ability to change the configuration of other devices. 

Since only the Root can initiate these requests, they also can only move down‐ stream, which means that peer‐to‐peer Configuration Requests are not allowed. The Requests are routed based on the target device’s ID, meaning its BDF (Bus number in the topology, Device number on that bus, and Function number within that Device).

</td>
<td style="background-color:#e8e8e8">

## **仅由根复合体发送配置请求**

规范规定,只有根复合体 (Root Complex) 才被允许发起配置请求 (Configuration Request)。它充当系统处理器的联络员,负责将请求注入到互连网络 (Fabric) 中,并将完成报文 (Completion) 回传给处理器。发起配置事务的能力被限制为由处理器通过根复合体执行,以避免任何设备都可以更改其他设备配置时可能引发的混乱局面。

由于只有根复合体能够发起这些请求,因此它们也只能向下游 (downstream) 流动,这意味着不允许对等的 (peer-to-peer) 配置请求。这些请求根据目标设备的 ID 进行路由,即其 BDF(拓扑中的总线号 (Bus number)、该总线上的设备号 (Device number),以及该设备内的功能号 (Function number))。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-41"></a>
## 4.41 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Generating Configuration Transactions** 

Processors are generally unable to perform configuration read and write requests directly because they can only generate memory and IO requests. That means the Root Complex will need to translate certain of those accesses into configuration requests in support of this process. Configuration space can be accessed using either of two mechanisms: 

- The legacy PCI configuration mechanism, using IO‐indirect accesses. 

- The enhanced configuration mechanism, using memory‐mapped accesses.

</td>
<td style="background-color:#e8e8e8">

## **生成配置事务** 

处理器通常无法直接执行配置读和写请求，因为它们只能生成内存和 I/O 请求。这意味着根复合体 (Root Complex) 需要将这些访问中的某些转换为配置请求以支持此过程。可以使用以下两种机制之一来访问配置空间 (Configuration Space)： 

- 传统 PCI 配置机制，使用 IO 间接访问。 

- 增强型配置机制，使用内存映射访问。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-42"></a>
## 4.42 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Legacy PCI Mechanism** 

The PCI spec defined an IO‐indirect method for instructing the system (the Root Complex or its equivalent) to perform PCI configuration accesses. As it hap‐ pened, the dominant PC processors (Intel x86) were only designed to address 64KB of IO address space. By the time PCI was defined, this limited IO space had become badly cluttered and only a few address ranges remained available: 0800h ‐ 08FFh and 0C00h ‐ 0CFFh. Consequently, it wasn’t feasible to map the configuration registers for all the possible Functions directly into IO space. At the same time, memory address space was also limited in size and mapping all of configuration space into memory address space was not seen as a good solu‐ tion either. So the spec writers chose a commonly‐used solution to this problem, use indirect address mapping instead. To do this, one register holds the target 

**91**

</td>
<td style="background-color:#e8e8e8">

## **传统 PCI 机制** 

PCI 规范定义了一种 IO 间接方法，用于指示系统（根复合体 (Root Complex) 或其等效组件）执行 PCI 配置访问。事实情况是，当时主流的 PC 处理器（Intel x86）只能寻址 64KB 的 IO 地址空间。在 PCI 被定义之时，这个有限的 IO 空间已经变得非常拥挤，只剩下少数可用的地址范围：0800h - 08FFh 和 0C00h - 0CFFh。因此，不太可能将所有可能的 Function 的配置寄存器直接映射到 IO 空间中。与此同时，内存地址空间的大小也有限，将整个配置空间映射到内存地址空间同样不被视为一个好的解决方案。于是规范制定者选择了一种常用的解决方案，即采用间接地址映射。为此，使用一个寄存器来保存目标

**91**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-43"></a>
## 4.43 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

address, while a second holds the data going to or coming from the target. A write to the address register, followed by a read or write to the data register, causes a single read or write transaction to the correct internal address for the target function. This solves the problem of limited address space nicely, but it means that two IO accesses are needed to create one configuration access. 

The PCI‐Compatible mechanism uses two 32‐bit IO ports in the Host bridge of the Root Complex. They are the **Configuration Address Port** , at IO addresses 0CF8h ‐ 0CFBh, and the **Configuration Data Port** , at IO addresses 0CFCh ‐ CFFh. 

Accessing a Functionʹs PCI‐compatible configuration registers is accomplished by first writing the target Bus, Device, Function and dword numbers into the Configuration Address Port, setting its Enable bit in the process. Secondly, a one‐, two‐, or four‐byte IO read or write is sent to the Configuration Data Port. The host bridge in the Root Complex compares the specified target bus to the range of buses that exist downstream of the bridge. If the target bus is within that range, the bridge initiates a configuration read or write request (depending on whether the IO access to the Configuration Data Port was a read or a write).

</td>
<td style="background-color:#e8e8e8">

## **PCI Express Technology** 

地址,另一个保存发往目标或来自目标的数据。对地址寄存器执行写操作,随后对数据寄存器执行读或写操作,会向目标功能的相应内部地址发起一次读或写事务。这巧妙地解决了地址空间有限的问题,但这意味着完成一次配置访问需要两次 IO 访问。

PCI 兼容 (PCI-Compatible) 机制使用根复合体 (Root Complex) 主桥 (Host Bridge) 中的两个 32 位 IO 端口。它们是 **配置地址端口 (Configuration Address Port)**,位于 IO 地址 0CF8h - 0CFBh,以及 **配置数据端口 (Configuration Data Port)**,位于 IO 地址 0CFCh - 0CFFh。

访问功能的 PCI 兼容配置寄存器的过程如下:首先将目标总线 (Bus)、设备 (Device)、功能 (Function) 和双字 (dword) 编号写入配置地址端口,并在此过程中设置其使能位 (Enable bit)。其次,向配置数据端口发起一次 1 字节、2 字节或 4 字节的 IO 读或写操作。根复合体中的主桥将所指定的目标总线与其下游总线范围进行比较。如果目标总线在该范围内,则桥将发起一次配置读或写请求 (具体取决于对配置数据端口的 IO 访问是读还是写)。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-44"></a>
## 4.44 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Configuration Address Port** 

The Configuration Address Port only latches information when the processor performs a full 32‐bit write to the port, as shown in Figure 3‐4, and a 32‐bit read from the port returns its contents. The information written to the Configuration Address Port must conform to the following template (illustrated in Figure 3‐4) and described on the facing page. 

_Figure 3‐4: Configuration Address Port at 0CF8h_ 

**==> picture [339 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 30 24 23 16 15 11 10 8 7 2 1 0<br>Reserved Bus Device Function Doubleword 0 0<br>Number Number Number<br>Register pointer (64 DW)<br>Should always be zeros<br>Enable Configuration Space Mapping<br>1 = enabled<br>**----- End of picture text -----**<br>

**92** 

**Cha ter 3: Confi uration Overview p g** 

- Bits **[1:0]** are hard‐wired, read‐only and must return **zeros** when read. The location is dword aligned and no byte‐specific offset is allowed. 

- Bits **[7:2]** identify the **target dword** (also called the Register Number) in the target Functionʹs PCI‐compatible configuration space. This mechanism is limited to the compatible configuration space (i.e., the first 64 doublewords of a Function’s configuration space). 

- Bits **[10:8]** identify the **target Function** number (0 ‐ 7) within the target device. 

- Bits **[15:11]** identify the **target Device** number (0 ‐ 31). 

- Bits **[23:16]** identify the **target Bus** number (0 ‐ 255). 

- Bits **[30:24]** are **reserved** and must be zero. 

- Bit **[31]** must be set to 1b to enable translation of the subsequent IO access to the Configuration Data Port into a configuration access. If bit 31 is zero and an IO read or write is sent to the Configuration Data Port, the transaction is treated as an ordinary IO Request.

</td>
<td style="background-color:#e8e8e8">

## **配置地址端口** 

如**图 3-4** 所示，配置地址端口仅在处理器对该端口执行完整的 32 位写操作时才会锁存信息，而对该端口执行 32 位读操作则会返回其内容。写入配置地址端口的信息必须遵循如下模板（示于图 3-4 中），其详细说明见对面页面。

_图 3-4：位于 0CF8h 的配置地址端口_ 

**==> 图片 [339 x 129] 故意省略 <==**

**----- 图片文字开始 -----**<br>
31 30 24 23 16 15 11 10 8 7 2 1 0<br>保留 总线号 设备号 功能号 双字 0 0<br>编号 编号 编号<br>寄存器指针（64 个 DW）<br>应始终为零<br>使能配置空间映射<br>1 = 使能<br>
**----- 图片文字结束 -----**<br>

**92** 

**第 3 章：配置概述** 

- 位 **[1:0]** 为硬连线、只读位，读时必须返回**零**。该位置是双字对齐的，不允许使用字节特定的偏移量。 

- 位 **[7:2]** 用于标识目标功能（Function）PCI 兼容配置空间内的**目标双字**（也称为寄存器编号）。该机制仅限于兼容配置空间（即功能配置空间的前 64 个双字）。 

- 位 **[10:8]** 用于标识目标设备内的**目标功能**编号（0 ‐ 7）。 

- 位 **[15:11]** 用于标识**目标设备**编号（0 ‐ 31）。 

- 位 **[23:16]** 用于标识**目标总线**编号（0 ‐ 255）。 

- 位 **[30:24]** 为**保留位**，必须为零。 

- 位 **[31]** 必须置 1b，以使能后续对配置数据端口的 IO 访问转换为配置访问。如果位 31 为零，并且向配置数据端口发送了 IO 读或写请求，则该事务将被视为普通的 IO 请求。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-45"></a>
## 4.45 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Bus Compare and Data Port Usage** 

The Host Bridge within the Root Complex, shown in Figure 3‐5 on page 95, implements a Secondary Bus Number register and a Subordinate Bus Number register. The Secondary Bus Number is the bus number of the bus immediately beneath the bridge. The Subordinate Bus Number is the target bus number that lives downstream of the bridge. 

In a single Root Complex system, the bridge may have a Secondary Bus Num‐ ber register that is hardwired to 0, a read/write register that reset forces to 0, or it may just implicitly know that the first accessible bus will be Bus 0. If bit 31 in the Configuration Address Port (see Figure 3‐4 on page 92) is set to 1b, the bridge will compare the target bus number to the range of buses that exists downstream. 

When a Request is seen, the Bridge evaluates whether the target bus number is within the range of bus numbers downstream, from the value of the Secondary Bus number to the Subordinate Bus number, inclusive. If the target bus matches the Secondary Bus, then that bus is targeted and the Request is passed through as a Type 0 Configuration Request. When devices see a Type 0 Request, they know that a device local to that bus is the target device (rather than one on a subordinate bus downstream). 

If the target bus is larger than the bridge’s Secondary Bus number, but less than or equal to the bridge’s Subordinate Bus number, the Request will be forwarded as a Type 1 configuration request on the bridge’s secondary bus. A Type 1 con‐ figuration access is understood to mean that, even though the Request has to go across this bus, it does not target a device on this bus. Instead, the request will 

**93**

</td>
<td style="background-color:#e8e8e8">

## **总线比较与数据端口使用** 

根复合体 (Root Complex) 内部的主桥 (Host Bridge)（如图 3-5 所示，位于第 95 页）实现了一个 Secondary Bus Number 寄存器和一个 Subordinate Bus Number 寄存器。Secondary Bus Number 是紧邻该桥下方的总线编号。Subordinate Bus Number 是位于该桥下游的目标总线编号。 

在单一根复合体 (Root Complex) 系统中，该桥的 Secondary Bus Number 寄存器可能被硬连线为 0，可能是一个读/写寄存器（复位时强制为 0），或者它可能仅隐式地知道第一个可访问的总线将是 Bus 0。如果配置地址端口 (Configuration Address Port)（参见第 92 页图 3-4）中的第 31 位被设置为 1b，则该桥会将目标总线编号与其下游存在的总线范围进行比较。 

当看到一个请求 (Request) 时，桥会评估目标总线编号是否在下游总线编号的范围内，即从 Secondary Bus Number 的值到 Subordinate Bus Number 的值（含两端）。如果目标总线与 Secondary Bus 匹配，则该总线被作为目标，请求将作为 Type 0 配置请求 (Type 0 Configuration Request) 传递。当设备看到 Type 0 请求时，它们知道该总线上本地的设备是目标设备（而不是该总线下游某条下级总线上的设备）。 

如果目标总线号大于桥的 Secondary Bus Number，但小于或等于桥的 Subordinate Bus Number，则该请求将作为 Type 1 配置请求 (Type 1 configuration request) 在桥的次级总线上转发。Type 1 配置访问的含义是：尽管该请求必须穿越此总线，但它的目标并不是该总线上的设备。相反，该请求将

**93**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-46"></a>
## 4.46 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

be forwarded downstream by one of the Bridges on this bus, whose Secondary and Subordinate bus number range contains the target bus number. For that reason, only Bridge devices pay attention to Type 1 configuration Requests. See “Configuration Requests” on page 99 for additional information regarding Type 0 and Type 1 configuration Requests.

</td>
<td style="background-color:#e8e8e8">

## **PCI Express 技术** 

由该总线上某一个桥 (Bridge) 向下游转发,该桥的 Secondary 和 Subordinate 总线号范围包含目标总线号。出于这个原因,只有桥设备才会关注 Type 1 配置请求 (Configuration Request)。有关 Type 0 和 Type 1 配置请求的更多信息,请参阅第 99 页的"配置请求 (Configuration Requests)"。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-47"></a>
## 4.47 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Single Host System** 

The information written to the Configuration Address Port is latched by the Host/PCI bridge within the Root Complex, as shown in Figure 3‐1 on page 87. If bit 31 is 1b and the target bus is within the downstream range of bus numbers, the bridge translates a subsequent processor access targeting its Configuration Data Port into a configuration request on bus 0. The processor then initiates an IO read or write transaction to the Configuration Data Port at 0CFCh. This causes the bridge to generate a Configuration Request that is a read when the IO access to the Configuration Data Port was a read, or a Configuration write if the IO access was a write. It will be a Type 0 configuration transaction if the tar‐ get bus is bus 0, or a Type 1 for another bus within the range, or not forwarded at all if the target bus is outside of the range. 

**94** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐5: Single‐Root System_ 

**==> picture [327 x 449] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bus 0 Sec = 0 Bridge<br>Sub = 9<br>Pri = 0 Pri = 0<br>P2P Sec = 1 Device 0 Device 1 Sec = 5 P2P<br>Sub = 4 Sub = 9<br>Bus 1 Bus 1 Bus 5 Bus 5<br>Device 0 Device 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P Sec = 6<br>P2P<br>Sub = 4 Sub = 9<br>Bus 2 P2P Bus 6 P2P<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 9<br>Function 0 Function 0 Function 0 Function 0<br>Bus 3 Bus 4 Bus 7 Bus 9<br>Device 0 Device 0 Device 0 Device 0<br>**----- End of picture text -----**<br>

**95** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

## **单主机系统**

写入配置地址端口 (Configuration Address Port) 的信息由根复合体 (Root Complex) 内的主桥/PCI 桥 (Host/PCI Bridge) 锁存,如第 87 页图 3‐1 所示。如果 bit 31 为 1b,且目标总线位于总线号的下游范围内,则该桥会将处理器随后访问其配置数据端口 (Configuration Data Port) 的操作转换为总线 0 上的配置请求。随后,处理器启动对 0CFCh 处配置数据端口的 IO 读或写事务。这会使桥生成一个配置请求:如果对配置数据端口的 IO 访问是读操作,则为配置读;如果 IO 访问是写操作,则为配置写。如果目标总线是总线 0,则该事务为 Type 0 配置事务;如果是范围内另一条总线,则为 Type 1 配置事务;若目标总线不在范围内,则根本不转发。

**94**

**第 3 章:配置概述**

_图 3‐5:单根系统 (Single-Root System)_

**==> 图片 [327 x 449] 已省略 <==**

**----- 图片文字开始 -----**<br>
处理器 (Processor)<br>
根复合体 (Root Complex)<br>
主桥/PCI (Host/PCI)<br>
总线 0 (Bus 0) Sec = 0 桥 (Bridge)<br>
Sub = 9<br>
Pri = 0 Pri = 0<br>
P2P Sec = 1 设备 0 (Device 0) 设备 1 (Device 1) Sec = 5 P2P<br>
Sub = 4 Sub = 9<br>
总线 1 (Bus 1) 总线 1 (Bus 1) 总线 5 (Bus 5) 总线 5 (Bus 5)<br>
设备 0 (Device 0) 设备 0 (Device 0)<br>
Pri = 1 Pri = 5<br>
Sec = 2 P2P Sec = 6<br>
P2P<br>
Sub = 4 Sub = 9<br>
总线 2 (Bus 2) P2P 总线 6 (Bus 6) P2P<br>
Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>
Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>
Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>
总线 3 (Bus 3) 总线 4 (Bus 4) 总线 7 (Bus 7) 总线 8 (Bus 8) 总线 9 (Bus 9)<br>
功能 0 (Function 0) 功能 0 (Function 0) 功能 0 (Function 0) 功能 0 (Function 0)<br>
总线 3 (Bus 3) 总线 4 (Bus 4) 总线 7 (Bus 7) 总线 9 (Bus 9)<br>
设备 0 (Device 0) 设备 0 (Device 0) 设备 0 (Device 0) 设备 0 (Device 0)<br>
**----- 图片文字结束 -----**<br>

**95**

**PCI Express 技术**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-48"></a>
## 4.48 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Multi-Host System** 

If there are multiple Root Complexes (refer to Figure 3‐6 on page 97), the Con‐ figuration Address and Data ports can be duplicated at the same IO addresses in each of their respective Host/PCI bridges. In order to prevent contention, only one of the bridges responds to the processorʹs accesses to the configuration ports. 

1. When the processor initiates the IO write to the Configuration Address Port, the host bridges are configured so that only one will actively partici‐ pate in the transaction. 

2. During enumeration, software discovers and numbers all the buses under the active bridge. When that’s done, it enables the inactive host bridge and assigns a bus number to it that is outside the range already assigned to the active bridge and continues the enumeration process. Both host bridges see the Requests, but since they have non‐overlapping bus numbers they only respond to the appropriate bus number requests and so there’s no conflict. 

3. Accesses to the Configuration Address Port go to both host bridges after that, and a subsequent read or write access to the Configuration Data Port is only accepted by the host/PCI bridge that is the gateway to the target bus. This bridge responds to the processor’s transaction and the other ignores it. 

   - If the target bus is the Secondary Bus, the bridge converts the access to a Type 0 configuration access. 

   - Otherwise, it converts it into a Type 1 configuration access.

</td>
<td style="background-color:#e8e8e8">

## **多主机系统**

如果存在多个根复合体 (Root Complex)（参见第 97 页的图 3‐6），则配置地址端口和数据端口可以在每个各自的主桥 (Host/PCI Bridge) 中以相同的 IO 地址进行复制。为了防止冲突，只有其中一个桥会对处理器访问配置端口的请求作出响应。

1. 当处理器发起对配置地址端口的 IO 写操作时，主桥被配置为只有其中一个桥会主动参与该事务。

2. 在枚举 (Enumeration) 过程中，软件发现并对处于激活状态的桥下的所有总线进行编号。完成此操作后，它启用非激活的主桥，并为其分配一个已分配给激活桥范围之外的 总线号，然后继续枚举过程。两个主桥都会看到这些请求，但由于它们的总线号不重叠，因此它们只对相应总线号的请求作出响应，所以不会产生冲突。

3. 此后，对配置地址端口的访问会同时到达两个主桥，而随后对配置数据端口的读或写访问只会被通往目标总线的主/PCI 桥所接受。该桥会响应处理器的事务，而另一个则忽略它。

   - 如果目标总线是 Secondary Bus（次级总线），则该桥将该访问转换为 Type 0 配置 (端点) 访问。

   - 否则，它将该访问转换为 Type 1 配置 (桥) 访问。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-49"></a>
## 4.49 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Enhanced Configuration Access Mechanism**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-50"></a>
## 4.50 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **General** 

When the spec writers were choosing how PCI‐X and, later, PCIe, would access Configuration space, there were two concerns. First, the 256‐byte space per Function limited vendors who wanted to put proprietary information there, as well as future spec writers who would need room for more standardized capa‐ bility structures. To solve that problem, the space was simply extended from 256 bytes to 4KB per Function. Secondly, when PCI was developed there were few multi‐processor systems in use. When there’s only one CPU and it’s only run‐ ning one thread, the fact that the old model takes two steps to generate one access isn’t a problem. But newer machines using multi‐core, multi‐threaded CPUs present a problem for the IO‐indirect model because there’s nothing to stop multiple threads from trying to access Configuration space at the same time. Consequently, the two‐step model will no longer work without some lock‐ ing semantics. With no locking semantics, once thread A writes a value into the 

**96** 

**Cha ter 3: Confi uration Overview p g** 

Configuration Address Port (CF8h), there is nothing to prevent thread B from overwriting that value before thread A can perform its corresponding access to the Configuration Data Port (CFCh). 

_Figure 3‐6: Multi‐Root System_ 

**==> picture [379 x 377] intentionally omitted <==**

**----- Start of picture text -----**<br>
Inter-Processor<br>Communications<br>Processor Processor<br>Root Complex Root Complex<br>Sec = 0 Host/PCI Sec = 64 Host/PCI<br>Sub = 9 Bridge Sub = 65 Bridge<br>Bus 0<br>Bus 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 9 P2P Device 0 Sec = 65Sub = 65 P2P<br>Bus 65<br>Bus 1 Bus 5<br>Function 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>Bus 2 P2P Bus 6 P2P Bus 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 Device 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 9<br>Function 0 Function 0 Function 0 Function 0<br>Bus 3 Bus 4 Bus 7 Bus 9<br>Device 0 Device 0 Device 0 Device 0<br>**----- End of picture text -----**<br>

**97**

</td>
<td style="background-color:#e8e8e8">

## **概述** 

当规范制定者决定 PCI‐X 以及后来的 PCIe 如何访问配置空间 (Configuration Space) 时,他们面临两个考虑。首先,每个 Function (功能) 仅有 256 字节的空间,这限制了希望在该处放置专有信息的厂商,以及未来需要更多空间来容纳标准化能力结构 (Capability Structure) 的规范制定者。为了解决这个问题,空间直接从每个 Function 256 字节扩展到了 4KB。其次,在制定 PCI 规范时,使用中的多处理器系统还很少。当只有一个 CPU 且它只运行一个线程时,旧模型需要两步才能产生一次访问这一事实并不是问题。但使用多核、多线程 CPU 的较新机器对 IO‐间接 (IO-indirect) 模型提出了一个问题,因为没有任何机制能阻止多个线程同时尝试访问配置空间。因此,如果不加入某种锁机制 (locking semantics),这种两步模型将无法继续工作。如果没有锁机制,一旦线程 A 向

**96**

**第 3 章:配置概述**

配置地址端口 (Configuration Address Port,CF8h) 写入一个值,就无法阻止线程 B 在线程 A 能够对配置数据端口 (Configuration Data Port,CFCh) 执行相应访问之前覆盖该值。

_图 3‐6:多根系统 (Multi‐Root System)_ 

**==> 图片 [379 x 377] 故意省略 <==**

**----- 图片文字开始 -----**<br>
处理器间<br>通信<br>处理器 处理器<br>根复合体 (Root Complex) 根复合体 (Root Complex)<br>Sec = 0 主机/PCI 桥 (Host/PCI Bridge) Sec = 64 主机/PCI 桥 (Host/PCI Bridge)<br>Sub = 9 Sub = 65<br>总线 (Bus) 0<br>总线 (Bus) 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 设备 (Device) 0 设备 (Device) 1 Sec = 5Sub = 9 P2P 设备 (Device) 0 Sec = 65Sub = 65 P2P<br>总线 (Bus) 65<br>总线 (Bus) 1 总线 (Bus) 5<br>功能 (Function) 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>总线 (Bus) 2 P2P 总线 (Bus) 6 P2P 总线 (Bus) 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 设备 (Device) 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>总线 (Bus) 3 总线 (Bus) 4 总线 (Bus) 7 总线 (Bus) 8 总线 (Bus) 9<br>功能 (Function) 0 功能 (Function) 0 功能 (Function) 0 功能 (Function) 0<br>总线 (Bus) 3 总线 (Bus) 4 总线 (Bus) 7 总线 (Bus) 9<br>设备 (Device) 0 设备 (Device) 0 设备 (Device) 0 设备 (Device) 0<br>**----- 图片文字结束 -----**<br>

**97**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-51"></a>
## 4.51 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

To solve this new problem, the spec writers decided to take a different approach. Rather than try to conserve address space, they would create a single‐ step, uninterruptable process by mapping all of configuration space into mem‐ ory addresses. That allows a single command sequence, since one memory request in the specified address range will generate one Configuration Request on the bus. The trade‐off now is address size. Mapping 4KB per Function for all the possible implementations requires allocating 256MB of memory address space. The difference in that regard today is that modern architectures typically support anywhere between 36 and 48 bits of physical memory address space. With these memory address space sizes, 256MB is insignificant. 

To handle this mapping, each Function’s 4KB configuration space starts at a 4KB‐aligned address within the 256MB memory address space set aside for con‐ figuration access, and the address bits now carry the identifying information about which Function is targeted (refer to Table 3‐1 on page 98).

</td>
<td style="background-color:#e8e8e8">

## **PCI Express Technology**

为了解决这个新问题,规范制定者决定采用一种不同的方法。他们不再试图节约地址空间,而是创建一个单步、不可中断的过程,将所有配置空间映射到内存地址中。这样只需要一条命令序列,因为在指定地址范围内的一个内存请求将在总线上产生一个配置请求(Configuration Request)。现在权衡的代价是地址大小。为所有可能的实现按每个功能(Function)映射 4KB,需要分配 256MB 的内存地址空间。当今的不同之处在于,现代架构通常支持 36 到 48 位的物理内存地址空间。有了这些内存地址空间大小,256MB 显得微不足道。

为了处理这种映射,每个功能(Function)的 4KB 配置空间从为配置访问而保留的 256MB 内存地址空间内的一个 4KB 对齐地址开始,并且地址位现在承载了关于哪个功能被寻址的标识信息(请参阅第 98 页的表 3-1)。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-52"></a>
## 4.52 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Some Rules** 

A Root Complex is not required to support an access to enhanced configuration memory space if it crosses a dword address boundary (straddles two adjacent memory dwords). Nor are they required to support the bus locking protocol that some processor types use for an atomic, or uninterrupted series of com‐ mands. Software should avoid both of these situations when accessing configu‐ ration space unless it is known that the Root Complex does support them. 

_Table 3‐1: Enhanced Configuration Mechanism Memory‐Mapped Address Range_ 

|**Memory Address Bit Field**|**Description**|
|---|---|
|A[63:28]|Upper bits of the 256MB‐aligned base address of the<br>256MB memory‐mapped address range allocated<br>for the Enhanced Configuration Mechanism.<br>The manner in which the base address is allocated is<br>implementation‐specific. It is supplied to the OS by<br>system firmware (typically through the ACPI<br>tables).|
|A[27:20]|Target Bus Number (0 ‐ 255).|
|A[19:15]|Target Device Number (0 ‐ 31).|
|A[14:12]|Target Function Number (0 ‐ 7).|

**98** 

**Cha ter 3: Confi uration Overview p g** 

_Table 3‐1: Enhanced Configuration Mechanism Memory‐Mapped Address Range (Continued)_ 

|**Memory Address Bit Field**|**Description**|
|---|---|
|A[11:2]|A[11:2] this range can address one of 1024 dwords,<br>whereas the legacy method is limited to only<br>address one of 64 dwords.|
|A[1:0]|Defines the access size and the Byte Enable setting.|

</td>
<td style="background-color:#e8e8e8">

## **一些规则**

如果对增强配置内存空间的访问跨越了 dword 地址边界（横跨两个相邻的内存 dword），则不要求根复合体 (Root Complex) 必须支持此类访问。同样，也不要求根复合体支持某些处理器类型用于原子或不间断命令序列的总线锁定协议。软件在访问配置空间时应避免这两种情况，除非已知该根复合体支持这些特性。

_表 3‐1：增强配置机制内存映射地址范围_

|**内存地址位域**|**描述**|
|---|---|
|A[63:28]|为增强配置机制分配的 256MB 内存映射地址范围的<br>256MB 对齐基地址的高位。基地址的分配方式<br>由具体实现决定，由系统固件（通常通过 ACPI 表）<br>提供给操作系统。|
|A[27:20]|目标总线号（0 ‐ 255）。|
|A[19:15]|目标设备号（0 ‐ 31）。|
|A[14:12]|目标功能号（0 ‐ 7）。|

**98**

**第 3 章：配置概述**

_表 3‐1：增强配置机制内存映射地址范围（续）_

|**内存地址位域**|**描述**|
|---|---|
|A[11:2]|A[11:2] 这一范围可寻址 1024 个 dword 之一，<br>而传统方法仅限于寻址 64 个 dword 之一。|
|A[1:0]|定义访问大小和字节使能 (Byte Enable) 设置。|

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-53"></a>
## 4.53 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Configuration Requests** 

Two request types, Type 0 or Type 1, may be generated by bridges in response to a configuration access. The type used depends on whether the target Bus number matches the bridge’s Secondary Bus Number, as described below.

</td>
<td style="background-color:#e8e8e8">

## **配置请求** 

桥设备在响应配置访问时,可生成两种类型的请求:Type 0 或 Type 1。所用类型取决于目标总线号是否与桥的 Secondary Bus Number(次级总线号)相匹配,具体说明如下。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-54"></a>
## 4.54 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Type 0 Configuration Request** 

If the target bus number matches the Secondary Bus Number, a Type 0 configu‐ ration read or write is forwarded to the secondary bus and: 

1. Devices on that Bus check the Device Number to see which of them is the target device. Note that Endpoints on an external Link will always be Device 0. 

2. The selected Device checks the Function Number to see which Function is selected within the device. 

3. The selected Function uses the Register Number field to select the target dword in its configuration space, and uses the First Dword Byte Enable field to select which bytes to read or write within the selected dword. 

Figure 3‐7 illustrates the Type 0 configuration read and write Request header formats. In both cases, the Type field = 00100, while the Format field indicates whether it’s a read or a write. 

**99**

</td>
<td style="background-color:#e8e8e8">

## **Type 0 配置请求 (Configuration Request)** 

如果目标总线号与 Secondary Bus Number（次级总线号）匹配,则 Type 0 配置读或写将被转发到次级总线,并:

1. 该总线上的设备会检查 Device Number(设备号)字段,以确定哪个设备是目标设备。请注意,外部链路 (Link) 上的端点 (Endpoint) 始终是 Device 0。

2. 被选中的设备会检查 Function Number(功能号)字段,以确定在该设备内选择了哪个功能。

3. 被选中的功能使用 Register Number(寄存器号)字段来选择其配置空间中的目标双字 (dword),并使用 First Dword Byte Enable(第一个双字字节使能)字段来选择在所选双字内读取或写入哪些字节。

图 3-7 展示了 Type 0 配置读和写请求头格式。在这两种情况下,Type 字段 = 00100,而 Format 字段则指示是读还是写。

**99**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-55"></a>
## 4.55 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **PCI Ex ress Technolo p gy** 

_Figure 3‐7: Type 0 Configuration Read and Write Request Headers_ 

**==> picture [364 x 311] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 0 0 0 1 0 0 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 0 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 1 0 0 0 1 0 0 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

## **PCI Express 技术**

_图 3-7:Type 0 配置读写请求包头_

**==> picture [364 x 311] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 0 0 0 1 0 0 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 0 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 1 0 0 0 1 0 0 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-56"></a>
## 4.56 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Type 1 Configuration Request** 

When a bridge sees a configuration access whose target bus number does not match its Secondary Bus Number but is in the range between its Secondary and Subordinate Bus Numbers, it forwards the packet as a Type 1 Request to its Sec‐ ondary Bus. Devices that are not bridges (Endpoints) know to ignore Type 1 Requests since the target resides on a different bus, but bridges that see it will make the same comparison of the target bus number to the range of buses downstream (see Figure 3‐1 on page 87 and Figure 3‐6 on page 97). 

**100** 

**Cha ter 3: Confi uration Overview p g** 

- If the target bus matches the Bridge’s secondary bus, the packet is converted from Type 1 to Type 0 and passed to the secondary bus. Devices local to that bus then check the packet header as previously described. 

- If the target bus is not the Bridge’s secondary bus but is within its range, the packet is forwarded to the Bridge’s secondary bus as a Type 1 Request. 

Figure 3‐8 illustrates the Type 1 configuration read and write request header formats. In both cases, the Type field = 00101, while the Fmt field indicates whether it’s a read or a write. 

_Figure 3‐8: Type 1 Configuration Read and Write Request Headers_ 

**==> picture [360 x 312] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 0 0 0 1 0 1 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 1 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 1 0 0 0 1 0 1 0 0 0 tr H D P 0 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>

**101** 

**PCI Ex ress Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

## **Type 1 配置请求 (Configuration Request)**

当一个桥 (Bridge) 收到一个配置访问 (Configuration Request)，其目标总线号不匹配该桥的 Secondary Bus Number，但落在其 Secondary 与 Subordinate Bus Number 之间的范围内时，它将该报文作为 Type 1 Request 转发到其 Secondary Bus。不是桥的设备（即端点 Endpoint）会忽略 Type 1 Request，因为目标位于另一条总线上；而看到该报文的桥 (Bridge) 则会执行与下游总线范围的相同比较（请参见第 87 页的图 3-1 以及第 97 页的图 3-6）。

**100**

**第 3 章：配置概述 (Configuration Overview)**

- 如果目标总线匹配该桥的 secondary bus，则该报文从 Type 1 转换为 Type 0，并被传递到 secondary bus。该总线上本地的设备随后按前述方式检查报文头 (Header)。

- 如果目标总线不是该桥的 secondary bus，但是在其范围内，则该报文作为 Type 1 Request 转发到该桥的 secondary bus。

图 3-8 展示了 Type 1 配置读和写请求头 (Request Header) 格式。在两种情况下，Type 字段 = 00101，而 Fmt 字段指示该请求是读还是写。

_图 3-8：Type 1 配置读和写请求头 (Configuration Read and Write Request Headers)_

**==> picture [360 x 312] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Configuration Read<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R Attr R TH EP Attr AT Length<br>0 0 0 0 0 1 0 1 0 0 0 tr 0 0 0 0 D P 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>Type 1 Configuration Write<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R Attr R TH EP Attr AT Length<br>0 1 0 0 0 1 0 1 0 0 0 tr 0 0 0 0 D P 0 0 0 0 0 0 0 0 0 0 0 0 1<br>Last BE 1st DW<br>Byte 4 Requester ID Tag 0 0 0 0 BE<br>Device Function<br>Byte 8 Bus Number R Register Number R<br>Number Number<br>**----- End of picture text -----**<br>

**101**

**PCI Express Technology**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-57"></a>
## 4.57 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

## **Example PCI-Compatible Configuration Access** 

Refer to Figure 3‐9 on page 104. To illustrate the concept of generating a Config‐ uration Request using the legacy CF8h/CFCh mechanism, consider the follow‐ ing x86 assembly code sample, which will cause the Root Complex to perform a 2‐byte read from Bus 4, Device 0, Function 0, Register 0 (Vendor ID).

</td>
<td style="background-color:#e8e8e8">

## **PCI 兼容的配置访问示例**

参见第 104 页的图 3-9。为了说明使用传统 CF8h/CFCh 机制生成配置请求的概念，请参考以下的 x86 汇编代码示例，它会使根复合体 (Root Complex) 从总线 4、设备 0、功能 0、寄存器 0（Vendor ID）执行一个 2 字节的读取操作。

```
mov dx,0CF8h;将 dx 设为配置地址端口地址
mov eax,80040000h;enable=1,bus 4, dev 0, func 0, DW 0
out dx,eax;IO 写以设置地址端口
mov dx,0CFCh;将 dx 设为配置数据端口地址
in ax,dx;从配置数据端口进行 2 字节读取
```

1. `out` 指令从处理器生成一个 IO 写，目标是根复合体 Host 桥 (Host Bridge) 中的配置地址端口 (0CF8h)，如第 92 页图 3-4 所示。

2. Host 桥将配置地址端口中指定的目标总线号（4）与其下游的总线范围（0 到 10）进行比较。目标总线落在该范围内，因此该桥已准备好接收下一个配置请求的目标。

3. `in` 指令从处理器生成一个 IO 读事务，目标是根复合体 Host 桥中的配置数据端口 (Configuration Data Port)。这是从配置数据端口中前两个位置进行的 2 字节读取。

4. 由于目标总线不是总线 0，Host/PCI 桥在总线 0 上发起 Type 1 配置读。

5. 总线 0 上的所有设备都会锁存该事务请求，并发现它是一个 Type 1 配置请求。因此，根复合体中的两个虚拟 PCI-to-PCI 桥 (Virtual PCI-to-PCI Bridge) 都会将 Type 1 请求中的目标总线号与其各自下游的总线范围进行比较。

6. 目标总线（4）位于左侧桥下游的总线范围内，因此它将该数据包传递到其二级总线 (Secondary Bus)，但仍作为 Type 1 请求传递，因为目标总线与其二级总线号不匹配。

7. 左侧交换机的上游端口 (Upstream Port) 接收该数据包并将其传递给上游的 PCI-to-PCI 桥 (P2P)。

8. 该桥确定目标总线位于其下游，但并非以其二级总线为目标，因此它将该数据包作为 Type 1 请求传递到总线 2。

9. 总线 2 上的两个桥都接收到 Type 1 请求数据包。右侧桥确定目标总线与其二级总线号匹配。

**102**

**第 3 章：配置概述**

10. 该桥将配置读请求传递到总线 4，但因为数据包已到达目标总线（目标总线号与二级总线号匹配），因此将其转换为 Type 0 配置读请求。

11. 总线 4 上的设备 0 接收该数据包，并解码目标设备、功能和寄存器号字段，以选择其配置空间中目标双字（参见第 90 页图 3-3）。

12. 第一个双字字节使能 (First Dword Byte Enable) 字段的 bit 0 和 bit 1 被置位，因此该功能在其完成包 (Completion) 中返回前两个字节（本例中为 Vendor ID）。完成包使用从 Type 0 请求包中获取的 Requester ID 字段路由到 Host 桥。

13. 这两个字节的读数据被传送给处理器，从而完成 `in` 指令的执行。Vendor ID 被放入处理器的 AX 寄存器中。

## **增强型配置访问示例**

参见第 104 页的图 3-9。下面的 x86 代码示例使根复合体执行从总线 4、设备 0、功能 0、寄存器 0（Vendor ID）的读取。在此工作之前，必须已为 Host 桥分配了基地址值。本例假设增强型配置的 256MB 对齐基地址的内存映射范围为 E0000000h：

```
mov ax,[E0400000h];内存映射配置读
```

- 地址位 63:28 表示整体增强型配置地址范围 256MB 对齐基地址的高 36 位（本例中为 00000000 E0000000h）。

- 地址位 27:20 选择目标总线（本例中为 4）。

- 地址位 19:15 选择总线上的目标设备（本例中为 0）。

- 地址位 14:12 选择设备内的目标功能（本例中为 0）。

- 地址位 11:2 选择所选功能配置空间内的目标双字（本例中为 0）。

- 地址位 1:0 定义所选双字内的起始字节位置（本例中为 0）。

处理器发起从内存地址 E0400000h 开始的 2 字节内存读，由根复合体中的 Host 桥锁存。Host 桥识别出该地址与指定的配置区域相匹配，并为 dword 0、功能 0、设备 0、总线 4 的前两个字节生成配置读请求。后续的操作与上一节中描述的相同。

**103**

## **PCI Express 技术**

_图 3-9：配置读访问示例_

**==> picture [266 x 367] intentionally omitted <==**

**----- Start of picture text -----**<br>
处理器<br>根复合体<br>Host/PCI<br>总线 = 0 桥<br>Sub = 10<br>总线 0<br>Pri = 0 Pri = 0<br>P2P Sec = 1Sub = 4 设备 0 设备 1 Sec = 5Sub = 10 P2P<br>总线 1 总线 5<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 10<br>总线 2 P2P 总线 6 P2P<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 10<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 10<br>总线 3 总线 4 总线 7 总线 8 总线 10<br>功能 0 功能 0 功能 0 功能 0<br>Pri = 8 Express<br>Sec = 9 PCI<br>Sub = 9 桥<br>PCI 总线 总线 9<br>PCI PCI PCI<br>设备 设备 设备<br>**----- End of picture text -----**<br>


## **枚举 - 发现拓扑**

系统复位或上电后，配置软件必须扫描 PCIe 互连结构以发现机器拓扑并了解该结构的填充情况。在此发生之前，如图 3-10（第 105 页）所示，软件唯一能确定的是将存在一个 Host/PCI 桥，并且总线号 0 将位于该桥的二级侧。请注意，桥设备的上游侧称其为主总线 (Primary Bus)，而下游侧称为二级总线 (Secondary Bus)。扫描 PCI Express 互连结构以发现其拓扑的过程称为_枚举过程_。

_图 3-10：启动时的拓扑视图_

**==> picture [238 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
根复合体分配<br>了总线号 0。<br>处理器 其余的拓扑<br>尚待发现<br>和编号。<br>Host/PCI<br>桥<br>总线 0<br>? ? ? ? ? ? ? ?<br>**----- End of picture text -----**<br>


## **发现功能的存在或缺失**

处理器上执行的配置软件通常通过读取其 Vendor ID 寄存器来发现某功能 (Function) 的存在。PCI-SIG 为每个供应商分配一个唯一的 16 位值，并将其硬连线到该供应商设计的每个功能的 Vendor ID 寄存器中。通过在系统中所有可能的总线、设备和功能号组合中读取此寄存器，枚举软件可以搜索整个拓扑以了解哪些设备存在。此过程相当简单，但可能会出现两个问题：目标设备可能不存在，或者它存在但尚未准备好响应。这两种情况的处理方法将在下面描述。

## **设备不存在**

在发现过程中，目标设备实际上不存在于系统中的情况会发生多次，需要正确理解。在 PCI 中，配置读请求将在总线上超时并生成 Master Abort 错误条件。由于没有设备驱动总线并且所有信号都被上拉，总线上的数据位将被视为全 1，并将成为所看到的数据值。得到的 Vendor ID FFFFh 是保留的。如果枚举软件看到读取的这个结果，它就知道该设备不存在。由于这实际上不是错误情况，因此 Master Abort 在枚举过程中不会被报告为错误。

对于 PCIe，对不存在设备的配置读请求将导致目标设备上方的桥返回带有 UR（不支持的请求，Unsupported Request）状态的不带数据的完成 (Completion)。为了与传统的枚举模型向后兼容，当在枚举期间看到此完成时，根复合体向处理器返回全 1（FFFFh）作为数据。请注意，枚举软件依赖于在探测系统中功能是否存在时，对返回不支持请求的配置读请求接收到全 1 的值。

重要的是避免在此情况下意外地报告错误。即使在运行时此超时或 UR 结果将被视为错误，但在枚举期间它是一个预期结果，不被视为错误。为了帮助避免这种混淆，设备通常在稍后才被启用报告错误。对于 PCIe 而言，对该事件作记录可能仍然有用，这就是为什么在 PCIe 能力寄存器块 (PCIe Capability Register Block) 中提供了第四个"错误"状态位，称为不支持的请求状态 (Unsupported Request Status)（有关更多信息，请参阅第 678 页的"启用/禁用错误报告"）。这允许在不对其标记为错误的情况下记录此条件，这很重要，因为检测到的错误可能会停止枚举过程以调用系统错误处理程序。此时错误处理软件可能功能有限，因此难以解决问题。在这种情况下枚举软件可能会失败，因为它通常被编写为在操作系统或其他错误处理软件可用之前执行。为了避免此风险，通常不应在枚举期间报告错误。

## **设备未就绪**

可能出现的另一个问题是目标设备存在但尚未准备好响应配置访问。由于设备准备访问所需的时间，配置存在时序考虑。如果数据速率为 5.0 GT/s 或更低，则软件必须在复位后等待 100ms 才能发起配置请求。如果速率高于 5.0 GT/s（Gen3 速度），则软件必须等到链路训练 (Link Training) 完成后 100ms 才能尝试此操作。高速率需要更长延迟的原因是 Gen3 链路训练期间的均衡 (Equalization) 过程可能需要很长时间（大约 50ms；有关此主题的更多信息，请参阅第 577 页的"链路均衡概述"）。

按照 PCI 2.3 规范中的定义，初始化时间（Trhfa - 从复位解除到首次访问的时间）从 RST# 解除置位开始，并在 2[25] 个 PCI 时钟后结束。

**106**

**第 3 章：配置概述**

总计为整整一秒钟，在此期间该功能正在准备其首次配置访问，并且该值已作为 1.0s（+50%/-0%）沿用到 PCIe。功能可以使用该时间通过从外部串行 EEPROM 加载内容来填充其配置寄存器。例如，这可能需要一段时间才能加载，并且该功能在完成之前将无法准备好进行成功的访问。在 PCI 中，如果在功能就绪之前收到配置访问，它有三个选择：忽略请求、重试请求，或接受请求但推迟传递其响应直到完全就绪。最后一种响应可能会给热插拔系统带来麻烦，因为共享总线可能最终会停滞一秒钟，直到请求得到解决。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-58"></a>
## 4.58 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

```
movdx,0CF8h;set dx = config address port address
moveax,80040000h;enable=1, bus 4, dev 0, func 0, DW 0
outdx,eax;IO write to set up address port
movdx,0CFCh; set dx = config data port address
inax,dx;2-byte read from config data port
```

1. The out instruction generates an IO write from the processor targeting the Configuration Address Port in the Root Complex Host bridge (0CF8h), as shown in Figure 3‐4 on page 92. 

2. The Host bridge compares the target bus number (4) specified in the Con‐ figuration Address Port to the range of buses (0‐through‐10) that reside downstream. The target bus falls within the range, so the bridge is primed with the destination of the next configuration request. 

3. The in instruction, generates an IO read transaction from the processor tar‐ geting the Configuration Data Port in the Root Complex Host bridge. It’s a 2‐byte read from the first two locations in the Configuration Data Port. 

4. Since the target bus is not bus 0, the Host/PCI bridge initiates a Type 1 Con‐ figuration read on bus 0. 

5. All of the devices on bus 0 latch the transaction request and see that it’s a Type 1 Configuration Request. As a result, both of the virtual PCI‐to‐PCI bridges in the Root Complex compare the target bus number in the Type 1 request to the range of buses downstream from each of them. 

6. The destination bus (4) is within the range of buses downstream of the left‐ hand bridge, so it passes the packet through to its secondary bus, but as a Type 1 request because the destination bus doesn’t match the Secondary Bus Number. 

7. The upstream port on the left‐hand switch receives the packet and delivers it to the upstream PCI‐to‐PCI bridge. 

8. The bridge determines that the destination bus resides beneath it, but is not targeting its secondary bus, so it passes the packet to bus 2 as a Type 1 request. 

9. Both of the bridges on bus 2 receive the Type 1 request packet. The right‐ hand bridge determines that the destination bus matches its Secondary Bus Number. 

**102** 

**Cha ter 3: Confi uration Overview p g** 

10. The bridge passes the configuration read request through to bus 4, but con‐ verts into a Type 0 Configuration Read request because the packet has reached the destination bus (target bus number matches the secondary bus number). 

11. Device 0 on bus 4 receives the packet and decodes the target Device, Func‐ tion, and Register Number fields to select the target dword in its configura‐ tion space (see Figure 3‐3 on page 90). 

12. Bits 0 and 1 in the First Dword Byte Enable field are asserted, so the Func‐ tion returns its first two bytes, (Vendor ID in this case) in the Completion packet. The Completion packet is routed to the Host bridge using the Requester ID field obtained from the Type 0 request packet. 

13. The two bytes of read data are delivered to the processor, thus completing the execution of the “in“ instruction. The Vendor ID is placed in the proces‐ sor’s AX register. 

## **Example Enhanced Configuration Access** 

Refer to Figure 3‐9 on page 104. The following x86 code sample causes the Root Complex to perform a read from Bus 4, Device 0, Function 0, Register 0 (Vendor ID). Before this will work, the Host Bridge must have been assigned a base address value. This example assumes that the 256MB‐aligned base address of the Enhanced Configuration memory‐mapped range is E0000000h: 

```
movax,[E0400000h];memory-mapped Config read
```

- Address bits 63:28 indicate the upper 36 bits of the 256MB‐aligned base address of the overall Enhanced Configuration address range (in this case, 00000000 E0000000h). 

- Address bits 27:20 select the target bus (in this case, 4). 

- Address bits 19:15 select the target device (in this case, 0) on the bus. 

- Address bits 14:12 select the target Function (in this case, 0) within the device. 

- Address bits 11:2 selects the target dword (in this case, 0) within the selected Function’s configuration space. 

- Address bits 1:0 define the start byte location within the selected dword (in this case, 0). 

The processor initiates a 2‐byte memory read starting from memory location E0400000h, and this is latched by the Host Bridge in the Root Complex. The Host Bridge recognizes that the address matches the area designated for Con‐ figuration and generates a Configuration read Request for the first two bytes in dword 0, Function 0, device 0, bus 4. The remainder of the operation is the same as that described in the previous section. 

**103** 

## **PCI Ex ress Technolo p gy** 

_Figure 3‐9: Example Configuration Read Access_ 

**==> picture [266 x 367] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bus = 0 Bridge<br>Sub = 10<br>Bus 0<br>Pri = 0 Pri = 0<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 10 P2P<br>Bus 1 Bus 5<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 10<br>Bus 2 P2P Bus 6 P2P<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 10<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 10<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 0 Function 0 Function 0<br>Pri = 8 Express<br>Sec = 9 PCI<br>Sub = 9 Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>**----- End of picture text -----**<br>


## **Enumeration - Discovering the Topology** 

After a system reset or power up, configuration software has to scan the PCIe fabric to discover the machine topology and learn how the fabric is populated. Before that happens, as shown in Figure 3‐10 on page 105, the only thing that software can know for sure is that there will be a Host/PCI bridge and that bus 

**104** 

**Cha ter 3: Confi uration Overview p g** 

number 0 will be on the secondary side of that bridge. Note that the upstream side of a bridge device is called its primary bus, while the downstream side is referred to as its secondary bus. The process of scanning the PCI Express fabric to discover its topology is referred to as the _enumeration process_ . 

_Figure 3‐10: Topology View At Startup_ 

**==> picture [238 x 164] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex has bus<br>number zero assigned.<br>Processor The remaining topology<br>have yet to be discovered<br>and numbered.<br>Host/PCI<br>Bridge<br>Bus 0<br>? ? ? ? ? ? ? ?<br>**----- End of picture text -----**<br>


## **Discovering the Presence or Absence of a Function** 

The configuration software executing on the processor normally discovers the existence of a Function by reading from its Vendor ID register. A unique 16‐bit value is assigned to each vendor by the PCI‐SIG and is hardwired into the Ven‐ dor ID register of each Function designed by that vendor. By reading this regis‐ ter in all of the possible combinations of Bus, Device, and Function numbers in the system, enumeration software can search through the entire topology to learn which devices are present. This process is fairly simple, but there are two problems that can arise: a targeted device may not be present, or it may be present but unprepared to respond. Handling these two cases is described next. 

## **Device not Present** 

It can happen several times during the process of discovery that the targeted device doesn’t actually exist in the system and when that happens it needs to be understood correctly. In PCI, the Configuration Read Request would timeout on the bus and generate a Master Abort error condition. Since no device was driv‐ ing the bus and all the signals were pulled up, the data bits on the bus would be 

**105** 

## **PCI Ex ress Technolo p gy** 

seen as all ones and that would become the data value seen. The resulting Ven‐ dor ID of FFFFh is reserved. If enumeration software saw that result for the read, it understood that the device wasn’t present. Since this wasn’t really an error condition, the Master Abort would not be reported as an error during the enumeration process. 

For PCIe, a Configuration Read Request to a non‐existent device will result in the bridge above the target device returning a Completion without data that has a status of UR (Unsupported Request). For backward compatibility with the leg‐ acy enumeration model, the Root Complex returns all ones (FFFFh) to the pro‐ cessor for the data when this Completion is seen during enumeration. Note that enumeration software depends on receiving a value of all 1s for a Configuration Read Request that returns an Unsupported Request when probing for the exist‐ ence of Functions in the system. 

It’s important to avoid accidentally reporting an error for this case. Even though this timeout or UR result would be seen as an error during runtime, it’s an expected result that isn’t considered an error during enumeration. To help avoid confusion on this, devices are usually not enabled to signal errors until later. For PCIe it may still be useful to make a note of this event, and that’s why a fourth “error” status bit, called Unsupported Request Status is given in the PCIe Capa‐ bility register block (refer to “Enabling/Disabling Error Reporting” on page 678 for more on this). That allows this condition to be noted without marking it as an error, and that’s important because a detected error might stop the enumera‐ tion process to call the system error handler. The error handling software might have only limited capabilities during this time and thus have trouble resolving the problem. The enumeration software could fail in that case, since it’s typically written to execute before the OS or other error handling software is available. To avoid this risk, errors should not normally be reported during enumeration. 

## **Device not Ready** 

Another problem that can arise is that the targeted device is present but isn’t ready to respond to a configuration access. There is a timing consideration for configuration because of the time it takes devices to prepare for access. If the data rate is 5.0 GT/s or less, software must wait 100ms after reset before initiat‐ ing a Configuration Request. If the rate is higher than 5.0 GT/s (Gen3 speed), software must wait until 100ms after Link training completes before attempting this. The reason for the longer delay for the higher speeds is that the Gen3 Equalization Process during Link training can take a long time (on the order of 50ms; see “Link Equalization Overview” on page 577 for more on this topic). 

As defined in the PCI 2.3 spec, Initialization Time (Trhfa ‐ Time from Reset High to First Access) begins when RST# is deasserted and completes 2[25] PCI clocks 

**106** 

**Cha ter 3: Confi uration Overview p g** 

later. That works out to one full second during which the Function is preparing for its first configuration access and that value has been carried forward for PCIe as 1.0s (+50%/‐0%). A Function could use that time to populate its configu‐ ration registers by loading the contents from an external serial EEPROM, for example. That might take a while to load and the Function would be unpre‐ pared for a successful access until it finished. In PCI, if a configuration access was seen before the Function was ready, it had three choices: ignore the Request, Retry the Request, or accept the Request but postpone delivering its response until it was fully ready. That last response could cause trouble for Hot‐ plug systems because the shared bus could end up being stalled for one second until the Request resolved.

</td>
<td style="background-color:#e8e8e8">

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

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-59"></a>
## 4.59 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

In PCIe we have the same problem, but the process is a little different now. First, PCIe Functions must always give a Completion with a specific status when they are temporarily unable to respond to a configuration access, which is the Con‐ figuration Request Retry Status (CRS). This status is only legal in response to a configuration request and may optionally be considered a Malformed Packet error if seen in response to other Requests. This response is also only valid for the one second after reset because the Function is supposed to respond by then and can be considered broken if it won’t. 

The way the Root Complex handles a CRS Completion in response to a Config‐ uration Read Request is implementation specific, except for the period follow‐ ing a system reset. During that time, there are two options for what the Root will do next, based on the setting of the CRS Software Visibility bit in its Root Control Register, shown in Figure 3‐11 on page 108: 

- If the bit is set and the Request was a Configuration Read to both bytes of the Vendor ID register (as an enumeration access would do to discover the presence of a Function), the Root must give the host an artificial value of 0001h for this register, and all 1’s for any additional bytes in this Request. This Vendor ID is not used for any real devices and will be interpreted by software as an indication of a potentially lengthy delay in accessing this device. This can be helpful because software could choose to go on to another task and make better use of the time that would otherwise be spent waiting for the device to respond, returning to query this device later. For this to work, software must ensure that its first access to a Function after a reset condition is a Configuration Read of both bytes of the Vendor ID. 

- For configuration writes or any other configuration reads, the Root must automatically re‐issue the Configuration Request again as a new request. 

**107** 

**PCI Ex ress Technolo p gy** 

_Figure 3‐11: Root Control Register in PCIe Capability Block_ 

**==> picture [360 x 163] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 5 4 3 2 1 0<br>RsvdP<br>CRS Software Visibility Enable<br>PME Interrupt Enable<br>System Error on Fatal Error Enable<br>System Error on Non-Fatal Error Enable<br>System Error on Correctable Error Enable<br>**----- End of picture text -----**<br>


## **Determining if a Function is an Endpoint or Bridge** 

A critical part of the enumeration process is being able to determine if a func‐ tion is a bridge or an endpoint. As seen in Figure 3‐12 on page 108, the lower 7 bits of the Header Type register (offset 0Eh in config space header) identify the basic category of the Function, and three values are defined: 

- 0 = not a bridge (Endpoint in PCIe) 

- 1 = PCI‐to‐PCI bridge (abbreviated as P2P) connecting two buses 

- 2 = CardBus bridge (legacy interface not often used today) 

In Figure 3‐1 on page 87, the Header Type field (DW3, byte 2) in each of the Vir‐ tual P2Ps would return a value of 1, as would the PCI Express‐to‐PCI bridge (Bus 8, Device 0), while the Endpoints would return a Header Type of zero. 

_Figure 3‐12: Header Type Register_ 

**==> picture [189 x 84] intentionally omitted <==**

**----- Start of picture text -----**<br>
7   6                                0<br>Header Type<br>Configuration Header Format<br>0 = single-function device<br>1 = multi-fuction device<br>**----- End of picture text -----**<br>


**108** 

**Cha ter 3: Confi uration Overview p g** 

## **Single Root Enumeration Example** 

Now that we’ve discussed the basic elements involved in the enumeration pro‐ cess, let’s walk through an example of the process. Figure 3‐13 on page 113 illus‐ trates an example system after the buses and devices have been enumerated. The discussion that follows assumes that the configuration software uses either of the two configuration access mechanisms defined in this chapter to achieve this result. At startup time, the configuration software executing on the proces‐ sor performs enumeration as described below. 

1. Software updates the Host/PCI bridge Secondary Bus Number to zero and the Subordinate Bus Number to 255. Setting this to the max value means that it won’t have to be changed again until all the bus numbers down‐ stream have been identified. For the moment, buses 0 through 255 are iden‐ tified as being downstream. 

2. Starting with Device 0 (bridge A), the enumeration software attempts to read the Vendor ID from Function 0 in each of the 32 possible devices on bus 0. If a valid Vendor ID is returned from Bus 0, Device 0, Function 0, the device exists and contains at least one Function. If not, go on to probe bus 0, device 1, Function 0. 

3. The Header Type field in this example (Figure 3‐12 on page 108) contains the value one (01h) indicating this is a PCI‐to‐PCI bridge. The Multifunction bit (bit 7) in the Header Type register is 0, indicating that Function 0 is the only Function in this bridge. _The spec doesn’t preclude implementing multiple Functions within this Device and each of these Functions, in turn, could represent other virtual PCI‐to‐PCI bridges or even non‐bridge functions._ 

4. Now that software has found a bridge, performs a series of configuration writes to set the bridge’s bus number registers as follows: 

   - Primary Bus Number Register = 0 

   - Secondary Bus Number Register = 1 

   - Subordinate Bus Number Register = 255 

   - The bridge is now aware that the number of the bus directly attached downstream is 1 (Secondary Bus Number = 1) and that the largest bus num‐ ber downstream of it is 255 (Subordinate Bus Number = 255). 

5. Enumeration software must perform a depth‐first search. Before proceed‐ ing to discover additional Devices/Functions on bus 0, it must proceed to search bus 1. 

6. Software reads the Vendor ID of Bus 1, Device 0, Function 0, which targets bridge C in our example. A valid Vendor ID is returned, indicating that Device 0, Function 0 exists on Bus 1. 

7. The Header Type field in the Header register contains the value one (0000001b) indicating another PCI‐to‐PCI bridge. As before, bit 7 is a 0, indi‐ 

**109** 

**PCI Ex ress Technolo p gy** 

cating that bridge C is a single‐function device. 

8. Software now performs a series of configuration writes to set bridge C’s bus number registers as follows: 

   - Primary Bus Number Register = 1 

   - Secondary Bus Number Register = 2 

   - Subordinate Bus Number Register = 255 

9. Continuing the depth‐first search, a read is performed from bus 2, device 0, Function 0’s Vendor ID register. The example assumes that bridge D is Device 0, Function 0 on Bus 2. 

10. A valid Vendor ID is returned, indicating bus 2, device 0, Function 0 exists. 

11. The Header Type field in the Header register contains the value one (0000001b) indicating that this is a PCI‐to‐PCI bridge, and bit 7 is a 0, indi‐ cating that bridge D is a single‐function device. 

12. Software now performs a series of configuration writes to set bridge D’s bus number registers as follows: 

   - Primary Bus Number Register = 2 

   - Secondary Bus Number Register = 3 

   - Subordinate Bus Number Register = 255 

13. Continuing the depth‐first search, a read is performed from bus 3, device 0, Function 0’s Vendor ID register. 

14. A valid Vendor ID is returned, indicating bus 3, device 0, Function 0 exists. 

15. The Header Type field in the Header register contains the value zero (0000000b) indicating that this is an Endpoint function. Since this is an end‐ point and not a bridge, it has a Type 0 header and there are no PCI‐compat‐ ible buses beneath it. This time, bit 7 is a 1, indicating that this is a multifunction device. 

16. Enumeration software performs accesses to the Vendor ID of all 8 possible functions in bus 3, device 0 and determines that only Function 1 exists in addition to Function 0. Function 1 is also an Endpoint (Type 0 header), so there are no additional buses beneath this device. 

17. Enumeration software continues scanning across on bus 3 to look for valid functions on devices 1 ‐ 31 but does not find any additional functions. 

18. Having found every function there was to find downstream of bridge D, enumeration software updates bridge D, with the real Subordinate Bus Number of 3. Then it backs up one level (to bus 2) and continues scanning across on that bus looking for valid functions. The example assumes that bridge E is device 1, Function 0 on bus 2. 

19. A valid Vendor ID is returned, indicating that this Function exists. 

20. The Header Type field in bridge E’s Header register contains the value one (0000001b) indicating that this is a PCI‐to‐PCI bridge, and bit 7 is a 0, indi‐ cating a single‐function device. 

**110** 

**Cha ter 3: Confi uration Overview p g** 

21. Software now performs a series of configuration writes to set bridge E’s bus number registers as follows: 

   - Primary Bus Number Register = 2 

   - Secondary Bus Number Register = 4 

   - Subordinate Bus Number Register = 255 

22. Continuing the depth‐first search, a read is performed from bus 4, device 0, Function 0’s Vendor ID register. 

23. A valid Vendor ID is returned, indicating that this Function exists. 

24. The Header Type field in the Header register contains the value zero (0000000b) indicating that this is an Endpoint device, and bit 7 is a 0, indi‐ cating that this is a single‐function device. 

25. Enumeration software scans bus 4 to look for valid functions on devices 1 ‐ 31 but does not find any additional functions. 

26. Having reached the bottom of this tree branch, enumeration software updates the bridge above that bus, E in this case, with the real Subordinate Bus Number of 4. It then backs up one level (to bus 2) and moves on to read the Vendor ID of the next device (device 2). The example assumes that devices 2 ‐ 31 are not implemented on bus 2, so no additional devices are discovered on bus 2. 

27. Enumeration software updates the bridge above bus 2, C in this case, with the real Subordinate Bus Number of 4 and backs up to the previous bus (bus 1) and attempts to read the Vendor ID of the next device (device 1). The example assumes that devices 1 ‐ 31 are not implemented on bus 1, so no additional devices are discovered on bus 1. 

28. Enumeration software updates the bridge above bus 1, A in this case, with the real subordinate Bus Number of 4. and backs up to the previous bus (bus 0) and moves on to read the Vendor ID of the next device (device 1). The example assumes that bridge B is device 1, function 0 on bus 0. 

29. In the same manner as previously described, the enumeration software dis‐ covers bridge B and performs a series of configuration writes to set bridge B’s bus number registers as follows: 

   - Primary Bus Number Register = 0 

   - Secondary Bus Number Register = 5 

   - Subordinate Bus Number Register = 255 

30. Bridge F is then discovered and a series of configuration writes are per‐ formed to set its bus number registers as follows: 

   - Primary Bus Number Register = 5 

   - Secondary Bus Number Register = 6 

   - Subordinate Bus Number Register = 255 

31. Bridge G is then discovered and a series of configuration writes are per‐ formed to set its bus number registers as follows: 

**111** 

**PCI Ex ress Technolo p gy** 

   - Primary Bus Number Register = 6 

   - Secondary Bus Number Register = 7 

   - Subordinate Bus Number Register = 255 

32. A single‐function Endpoint device is discovered at bus 7, device 0, function 0, so the Subordinate Bus Number of Bridge G is updated to 7. 

33. Bridge H is then discovered and a series of configuration writes are per‐ formed to set its bus number registers as follows: 

   - Primary Bus Number Register = 6 

   - Secondary Bus Number Register = 8 

   - Subordinate Bus Number Register = 255

</td>
<td style="background-color:#e8e8e8">

34. 发现桥 J 并执行一系列配置写入以设置其总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 8

   - Secondary Bus Number 寄存器 = 9

   - Subordinate Bus Number 寄存器 = 255

35. 总线 9 上的所有设备及其各自的功能均被发现，并且它们都不是桥，因此桥 H 和 J 的 Subordinate Bus Number 被更新为 9。

36. 然后发现桥 I 并执行一系列配置写入以设置其总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 6

   - Secondary Bus Number 寄存器 = 10

   - Subordinate Bus Number 寄存器 = 255

37. 在总线 10、设备 0、功能 0 处发现单功能端点设备。

38. 由于软件已到达 PCIe 拓扑所需的树结构的此分支的底部，桥 B、F 和 I 的 Subordinate Bus Number 寄存器被更新为 10，Host/PCI 桥的 Subordinate Bus Number 寄存器也是如此。

编码到每个桥的 Primary、Secondary 和 Subordinate Bus Number 字段中的最终值可以在第 104 页图 3-9 中找到。

**112**

**第 3 章：配置概述**

_图 3-13：单根系统_

**==> picture [322 x 443] intentionally omitted <==**

**----- Start of picture text -----**<br>
处理器<br>根复合体<br>Host/PCI<br>桥<br>总线 0<br>总线 0 总线 0<br>虚拟 虚拟<br>A 设备 0 设备 1 B<br>P2P 功能 0 功能 0 P2P<br>总线 1<br>总线 5<br>虚拟<br>虚拟<br>P2P C P2P F<br>总线 2 总线 6<br>D 虚拟P2P E 虚拟P2P G 虚拟P2P H 虚拟P2P I 虚拟P2P<br>总线 3<br>总线 4 总线 7 总线 8 总线 10<br>功能 0 功能 1 功能 0 功能 0 功能 0<br>设备 0 设备 0 设备 0 设备 0<br>总线 8<br>设备 0<br>Express 功能 0<br>J PCI<br>桥<br>PCI 总线 总线 9<br>PCI PCI PCI<br>设备 设备 设备<br>设备 1 设备 2 设备 3<br>功能 0 功能 0 功能 0<br>**----- End of picture text -----**<br>


**113**

**PCI Express Technology**

## **多根枚举示例**

## **概述**

考虑第 116 页图 3-14 中所示的多根系统。在此系统中，每个根复合体：

- 在相同的 IO 地址实现配置地址端口和配置数据端口（基于 x86 的系统）。

- 实现增强型配置机制 (Enhanced Configuration Mechanism)。

- 包含一个 Host/PCI 桥。

- 在配置软件已知的单独地址上实现二级总线号和下属总线号寄存器。

在图中，每个根复合体都是芯片组成员，其中一个被指定为到总线 0 的桥（主根复合体），而另一个被指定为到总线 255 的桥（次根复合体）。

## **多根枚举过程**

在枚举图 3-14（第 116 页）中左侧树结构期间，次根复合体中的 Host/PCI 桥忽略所有配置访问，因为目标总线号不大于 9。请注意，尽管已被检测和编号，总线 8 上没有连接设备。一旦该枚举过程完成，枚举软件将执行以下步骤以枚举次根复合体：

1. 枚举软件将次根复合体的 Host/PCI 桥中的 Secondary 和 Subordinate Bus Number 值更改为本例中的总线 64。（值 64 和 128 通常用作多根系统中的起始总线号，但这只是一个软件约定。没有 PCI 或 PCIe 规则要求该配置。在本例中，从总线号 10 开始次根复合体也没有任何问题。）

2. 枚举软件然后在总线 64 上开始搜索并发现连接到下游根端口 (Root Port) 的桥。

3. 执行一系列配置写入以设置其总线号寄存器，如下所示：

   - Primary Bus Number 寄存器 = 64

   - Secondary Bus Number 寄存器 = 65

   - Subordinate Bus Number 寄存器 = 255

**114**

**第 3 章：配置概述**

该桥现在知道直接连接到其下游侧的总线号为 65（Secondary Bus Number = 65），而距其最远的下游总线号为 65（Subordinate Bus Number = 65）。

4. 在总线 65 上发现设备 0 仅实现功能 0，进一步搜索发现总线 65 上没有其他设备，因此搜索过程向上一级总线移动。

5. 在总线 64 上继续枚举，没有发现其他设备，因此 Host/PCI 的 Subordinate Bus Number 被更新为 65。

6. 至此完成了枚举过程。

**115**

## **PCI Express Technology**

_图 3-14：多根系统_

**==> picture [374 x 389] intentionally omitted <==**

**----- Start of picture text -----**<br>
处理器间<br>通信<br>处理器 处理器<br>根复合体 根复合体<br>Sec = 0 Host/PCI Sec = 64 Host/PCI<br>Sub = 9 桥 Sub = 65 桥<br>总线 0<br>总线 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 设备 0 设备 1 Sec = 5Sub = 9 P2P 设备 0 Sec = 65Sub = 65 P2P<br>总线 65<br>总线 1 总线 5<br>功能 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>总线 2 P2P 总线 6 P2P 总线 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 设备 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>总线 3 总线 4 总线 7 总线 8 总线 9<br>功能 0 功能 0 功能 0 功能 0<br>总线 3 总线 4 总线 7 总线 9<br>设备 0 设备 0 设备 0 设备 0<br>**----- End of picture text -----**<br>


## **热插拔注意事项**

在热插拔环境中，即可以在运行时添加或移除插入式卡的环境，第 116 页图 3-14 中由总线号 8 说明的情况可能会引起麻烦。如果系统已被枚举并正在运行中，然后将卡插入总线 8 而该卡上有一个桥，则可能会出现问题。该桥需要为其二级和下属总线号分配高于其主总线上总线号且完全包含在内的总线号。原因是总线号必须在新卡上游桥的二级和下属总线号范围内。

一种方法是为驻留在总线号 8 上的桥分配所需的总线号，并将当前总线号 9 增加到比先前总线号大 1 的数字，从而为新总线腾出空间。可以在运行时对总线号进行交换，但有经验的人说很难使其很好地工作。

对于此潜在问题有一个更简单的解决方案：只要发现未填充的插槽，就留出总线号间隔。例如，当分配了总线 8 但随后在其下方看到开放插槽时，将下一个发现的总线号给定一个更高的数字，如 19 而不是 9，以便为这些插入情况的解决留出空间。然后，如果添加了带桥的卡，则新总线号可以分配为总线 9 而不会引起任何麻烦。在大多数情况下，留下总线号间隔不会有问题，因为系统总共可以分配 256 个总线号。

## **MindShare Arbor：调试/验证/分析和学习软件工具**

## **概述**

MindShare Arbor 是一个计算机系统调试、验证、分析和学习工具，允许用户读取和写入任何内存、IO 或配置空间地址。这些地址空间的数据可以以清晰和信息丰富的方式查看。

本书作者决定不在信号章节中包含所有配置寄存器的详细描述。寄存器在本书的相关章节中与它们相关的地方进行描述。

代替本书中的配置寄存器空间描述章节，MindShare Arbor 是一个优秀的参考学习工具，可以快速了解在 PCI、PCI-X 和 PCI Express 设备中实现的配置寄存器和结构。

**117**

## **PCI Express Technology**

所有寄存器和字段定义都符合最新版本的 PCI Express 规范。还有几种其他类型的结构（例如 x86 MSR、ACPI、USB、NVM Express）也可以使用 MindShare Arbor 查看（或将很快推出）。

请访问 www.mindshare.com/arbor 下载 MindShare Arbor 的免费试用版。

_图 3-15：MindShare Arbor 的部分屏幕截图_

**118**

**第 3 章：配置概述**

## **MindShare Arbor 功能列表**

- 描述 PCIe 3.0 规范中包含的所有配置寄存器

- 扫描系统中所有 PCI 可见功能的配置空间，并以易于阅读的格式显示每个这些寄存器的描述

- 直接访问任何内存或 IO 地址

- 写入任何配置空间位置、内存地址或 IO 地址

- 以解码格式查看标准和非标准结构

   - 包括对标准 PCI、PCI-X 和 PCI Express 结构的解码信息

   - 包括对某些基于 x86 的结构和设备特定寄存器的解码信息

- 创建您自己的基于 XML 的解码文件以驱动 Arbor 的显示

   - 为配置空间、内存地址空间和 IO 空间中的结构创建解码文件

- 保存系统扫描以供稍后查看或在其它系统上查看

   - 保存的系统扫描基于 XML 且为开放格式

- 已包含或即将推出的新功能：

   - 扫描之间的差异检查

   - 对非法或非最佳设置的扫描后处理

   - 用于自动化的脚本支持

   - x86 结构（MSR、分页、段、中断表等）的解码

   - ACPI 结构的解码

   - USB 结构的解码

   - NVM Express 结构的解码

**119**

**PCI Express Technology**

**120**

## _**4 地址空间与事务路由**_

## **上一章**

上一章提供了 PCI Express 环境中配置的简介。这包括实现功能配置寄存器的空间、如何发现功能、如何生成和路由配置事务、PCI 兼容配置空间与 PCIe 扩展配置空间之间的差异，以及软件如何区分端点和桥。

## **本章**

本章描述了功能通过基地址寄存器 (BAR) 请求地址空间（内存地址空间或 IO 地址空间）的目的和方法，以及软件必须如何在所有桥中设置 Base/Limit 寄存器以将 TLP 从源端口路由到正确的目标端口。还讨论了 PCIe 中 TLP 路由的一般概念，包括基于地址的路由、基于 ID 的路由和隐式路由。

## **下一章**

下一章详细描述了事务层包 (TLP) 的内容。我们描述了 TLP 包类型的使用、格式和定义以及它们相关字段的详细信息。

## **我需要一个地址**

几乎所有设备都有软件（以及可能的其他设备）需要能够访问的内部寄存器或存储位置。这些内部位置可以控制设备的行为、报告设备的状态，或者可以是为设备处理保存数据的位置。无论内部寄存器/存储的目的是什么，重要的是能够从设备外部访问它们。

**121**

**PCI Express Technology**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-4-60"></a>
## 4.60 Address Space & Transaction Routing | 地址空间与事务路由

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

34. Bridge J is discovered and a series of configuration writes are performed to set bridge its bus number registers as follows: 

   - Primary Bus Number Register = 8 

   - Secondary Bus Number Register = 9 

   - Subordinate Bus Number Register = 255 

35. All devices and their respective Functions on bus 9 are discovered and none of them are bridges, so the Subordinate Bus Number of bridges H and J are updated to 9. 

36. Bridge I is then discovered and a series of configuration writes are per‐ formed to set its bus number registers as follows: 

   - Primary Bus Number Register = 6 

   - Secondary Bus Number Register = 10 

   - Subordinate Bus Number Register = 255 

37. A single‐function Endpoint device is discovered at bus 10, device 0, func‐ tion 0. 

38. Since software has reached the bottom of this branch of the tree structure required for PCIe topologies, the Subordinate Bus Number registers for bridges B, F, and I are updated to 10, and so is the Host/PCI bridge’s Subor‐ dinate Bus Number register. 

The final values encoded into each bridge’s Primary, Secondary and Subordi‐ nate Bus Number fields can be found in Figure 3‐9 on page 104. 

**112** 

**Cha ter 3: Confi uration Overview p g** 

_Figure 3‐13: Single‐Root System_ 

**==> picture [322 x 443] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Root Complex<br>Host/PCI<br>Bridge<br>Bus 0<br>Bus 0 Bus 0<br>Virtual Virtual<br>A Dev 0 Dev 1 B<br>P2P Func 0 Func 0 P2P<br>Bus 1<br>Bus 5<br>Virtual<br>Virtual<br>P2P C P2P F<br>Bus 2 Bus 6<br>D VirtualP2P E VirtualP2P G VirtualP2P H VirtualP2P I VirtualP2P<br>Bus 3<br>Bus 4 Bus 7 Bus 8 Bus 10<br>Function 0 Function 1 Function 0 Function 0 Function 0<br>Dev 0 Dev 0 Dev 0 Dev 0<br>Bus 8<br>Dev 0<br>Express Func 0<br>J PCI<br>Bridge<br>PCI Bus Bus 9<br>PCI PCI PCI<br>Device Device Device<br>Dev 1 Dev 2 Dev 3<br>Func 0 Func 0 Func 0<br>**----- End of picture text -----**<br>


**113** 

**PCI Ex ress Technolo p gy** 

## **Multi-Root Enumeration Example** 

## **General** 

Consider the Multi‐Root System shown in Figure 3‐14 on page 116. In this sys‐ tem, each Root Complex: 

- Implements the Configuration Address Port and the Configuration Data Port at the same IO addresses (an x86‐based system). 

- Implements the Enhanced Configuration Mechanism. 

- Contains a Host/PCI bridge. 

- Implements the Secondary Bus Number and Subordinate Bus Number reg‐ isters at separate addresses known to the configuration software. 

In the illustration, each Root Complex is a chipset member and one of them is designated as the bridge to bus 0 (the primary Root Complex) while the other is designated as the bridge to bus 255 (secondary Root Complex). 

## **Multi-Root Enumeration Process** 

During enumeration of the left‐hand tree structure in Figure 3‐14 on page 116, the Host/PCI bridge in the secondary Root Complex ignores all configuration accesses because the targeted bus number is no greater than 9. Note that, although detected and numbered, Bus 8 has no device attached. Once that enu‐ meration process has been completed, the enumeration software takes the fol‐ lowing steps to enumerate the secondary Root Complex: 

1. The enumeration software changes the Secondary and Subordinate Bus Number values in the secondary Root Complex’s Host/PCI bridge to bus 64 in this example. (The values of 64 and 128 are commonly used as the start‐ ing bus number in multi‐root systems, but this is just a software convention. There are no PCI or PCIe rules requiring that configuration. There would be nothing wrong with starting the secondary Root Complex’s bus numbers at 10 in this example.) 

2. Enumeration software then starts searching on bus 64 and discovers the bridge attached to the downstream Root Port. 

3. A series of configuration writes are performed to set its bus number regis‐ ters as follows: 

   - Primary Bus Number Register = 64 

   - Secondary Bus Number Register = 65 

   - Subordinate Bus Number Register = 255 

**114** 

**Cha ter 3: Confi uration Overview p g** 

The bridge is now aware that the number of the bus directly attached to its downstream side is 65 (Secondary Bus Number = 65) and the number of the bus farthest downstream of it is 65 (Subordinate Bus Number = 65). 

4. Device 0 is discovered on Bus 65 that implements a only Function 0, and further searching reveals no other Devices are present on Bus 65, so the search process moves back up one Bus level. 

5. Enumeration continues on bus 64 and no additional devices are discovered, so the Host/PCI’s Subordinate Bus Number is updated to 65. 

6. This completes the enumeration process. 

**115** 

## **PCI Ex ress Technolo p gy** 

_Figure 3‐14: Multi‐Root System_ 

**==> picture [374 x 389] intentionally omitted <==**

**----- Start of picture text -----**<br>
Inter-Processor<br>Communications<br>Processor Processor<br>Root Complex Root Complex<br>Sec = 0 Host/PCI Sec = 64 Host/PCI<br>Sub = 9 Bridge Sub = 65 Bridge<br>Bus 0<br>Bus 64<br>Pri = 0 Pri = 0 Pri = 64<br>P2P Sec = 1Sub = 4 Device 0 Device 1 Sec = 5Sub = 9 P2P Device 0 Sec = 65Sub = 65 P2P<br>Bus 65<br>Bus 1 Bus 5<br>Function 0<br>Pri = 1 Pri = 5<br>Sec = 2 P2P P2P Sec = 6<br>Sub = 4 Sub = 9<br>Bus 2 P2P Bus 6 P2P Bus 65<br>Pri = 2 P2P Pri = 2 Pri = 6 P2P Pri = 6 Pri = 6 Device 0<br>Sec = 3 Sec = 4 Sec = 7 Sec = 8 Sec = 9<br>Sub = 3 P2P Sub = 4 Sub = 7 Sub = 8 Sub = 9<br>Bus 3 Bus 4 Bus 7 Bus 8 Bus 9<br>Function 0 Function 0 Function 0 Function 0<br>Bus 3 Bus 4 Bus 7 Bus 9<br>Device 0 Device 0 Device 0 Device 0<br>**----- End of picture text -----**<br>


## **Hot-Plug Considerations** 

In a hot‐plug environment, meaning one in which add‐in cards can be added or removed during runtime, the situation illustrated by Bus number 8 in Figure 3‐ 

**116** 

**Cha ter 3: Confi uration Overview p g** 

14 on page 116 can potentially cause trouble. A problem can occur if the system has been enumerated and is up and running and then a card is plugged into Bus 8 that has a bridge on it. The bridge would need to have bus numbers assigned for its Secondary and Subordinate Bus Numbers that are higher than the bus number on its primary bus and completely inclusive. The reason is that the bus numbers have to be within the Secondary and Subordinate Bus Numbers of the bridge upstream of the new card. 

One approach is to assign the Bus number(s) required for the bridge residing on Bus number 8 and increment the current Bus number 9 to a number than is one greater than the previous bus number, thereby making room for the new bus(s). Swizzling the bus numbers around during runtime can be done, but experi‐ enced people say it’s hard to get it to work very well. 

There is a simpler solution to this potential problem: simply leave a bus number gap whenever an unpopulated slot is found. For example, when Bus 8 is assigned but then an open slot is seen below it, give the next discovered bus a higher number, like 19 instead of 9, so as to leave room for these add‐in situa‐ tions to be resolved easily. Then, if a card with a bridge is added, the new bus number can be assigned as Bus 9 without causing any trouble. In most cases, leaving a bus number gap will not be an issue since the system can assign up to 256 bus numbers in total. 

## **MindShare Arbor: Debug/Validation/Analysis and Learning Software Tool** 

## **General** 

MindShare Arbor is a computer system debug, validation, analysis and learning tool that allows the user to read and write any memory, IO or configuration space address. The data from these address spaces can be viewed in a clean and informative style. 

The book authors made a decision to not include detailed descriptions of all configuration registers summarized in a signal chapter. Rather, registers are described through out the book in associated chapters where they are relevant. 

In lieu of a configuration register space description chapter in this book, Mind‐ Share Arbor is an excellent reference learning tool to quickly understand config‐ uration registers and structures implemented in PCI, PCI‐X and PCI Express 

**117** 

## **PCI Ex ress Technolo p gy** 

devices. All the register and field definitions are up‐to‐date with the latest ver‐ sion of the PCI Express spec. Several other types of structures (e.g. x86 MSRs, ACPI, USB, NVM Express) can also be viewed with MindShare Arbor (or will be coming soon). 

Visit www.mindshare.com/arbor to download a free trial version of MindShare Arbor. 

_Figure 3‐15: Partial Screenshot of MindShare Arbor_ 

**118** 

**Cha ter 3: Confi uration Overview p g** 

## **MindShare Arbor Feature List** 

- Description of all config registers included in the PCIe 3.0 spec 

- Scan config space for all PCI‐visible functions in system and a description of every one of these registers displayed in an easily readable format 

- Directly access any memory or IO address 

- Write to any config space location, memory address or IO address 

- View standard and non‐standard structures in a decoded format 

   - Decode info included for standard PCI, PCI‐X and PCI Express struc‐ tures 

   - Decode info included for some x86‐based structures and device‐specific registers 

- Create your own XML‐based decode files to drive Arborʹs display 

   - Create decode files for structures in config space, memory address space and IO space 

- Save system scans for viewing later or on other systems 

   - Saved system scans are XML‐based and open‐format 

- New features that are either already in or coming soon: 

   - Difference checking between scans 

   - Post‐processing scans for illegal or non‐optimal settings 

   - Scripting support for automation 

   - Decode for x86 structures (MSRs, paging, segmentation, interrupt tables, etc.) 

   - Decode for ACPI structures 

   - Decode for USB structures 

   - Decode for NVM Express structures 

**119** 

**PCI Ex ress Technolo p gy** 

**120** 

## _**4 Address Space & Transaction Routing**_ 

## **The Previous Chapter** 

The previous chapter provides an introduction to configuration in the PCI Express environment. This includes the space in which a Function’s configura‐ tion registers are implemented, how a Function is discovered, how configura‐ tion transactions are generated and routed, the difference between PCI‐ compatible configuration space and PCIe extended configuration space, and how software differentiates between an Endpoint and a Bridge. 

## **This Chapter** 

This chapter describes the purpose and methods of a function requesting address space (either memory address space or IO address space) through Base Address Registers (BARs) and how software must setup the Base/Limit regis‐ ters in all bridges to route TLPs from a source port to the correct destination port. The general concepts of TLP routing in PCI Express are also discussed, including address‐based routing, ID‐based routing and implicit routing. 

## **The Next Chapter** 

The next chapter describes Transaction Layer Packet (TLP) content in detail. We describe the use, format, and definition of the TLP packet types and the details of their related fields. 

## **I Need An Address** 

Almost all devices have internal registers or storage locations that software (and potentially other devices) need to be able to access. These internal locations may control the device’s behavior, report the status of the device, or may be a loca‐ tion to hold data for the device to process. Regardless of the purpose of the internal registers/storage, it is important to be able to access them from outside 

**121** 

**PCI Express Technology**

</td>
<td style="background-color:#e8e8e8">

即设备本身。这意味着这些内部位置需要是_可寻址的_。软件必须能够使用将访问目标设备内适当内部位置的地址来执行读或写操作。为了使其工作，这些内部位置需要从系统支持的地址空间之一分配地址。

PCI Express 支持与 PCI 完全相同的三个地址空间：

- 配置空间

- 内存空间

- IO 空间

## **配置空间**

正如我们在第 1 章中看到的，配置空间是随 PCI 引入的，以允许软件以标准化的方式控制和检查设备的状态。PCI Express 被设计为与 PCI 软件向后兼容，因此仍支持配置空间并用于与 PCI 相同的原因。有关配置空间（用途、如何访问、大小、内容等）的更多信息，请参见第 3 章。

尽管配置空间最初旨在保存标准化的结构（PCI 定义的头、能力结构等），但 PCIe 设备将设备特定的寄存器映射到其配置空间是非常常见的。在这种情况下，映射到配置空间的设备特定寄存器通常是控制、状态或指针寄存器，而不是数据存储位置。

## **内存和 IO 地址空间**

## **概述**

在 PC 的早期，IO 设备中的内部寄存器/存储通过 IO 地址空间访问（由 Intel 定义）。然而，由于与 IO 地址空间相关的几个限制和不良效果（我们不在这里详述），该地址空间很快失去了软硬件供应商的青睐。这导致 IO 设备的内部寄存器/存储被映射到内存地址空间（通常称为内存映射 IO 或 MMIO）。然而，由于早期软件被编写为使用 IO 地址空间来访问 IO 设备上的内部寄存器/存储，因此通常的做法是将同一组设备特定寄存器映射到内存地址空间和 IO 地址空间。这允许新软件使用内存地址空间（MMIO）访问设备的内部位置，同时允许传统（旧）软件继续运行，因为它仍然可以使用 IO 地址空间访问设备的内部寄存器。

不依赖传统软件或具有传统兼容性问题的新设备通常仅通过内存地址空间（MMIO）映射内部寄存器/存储，而不请求 IO 地址空间。事实上，PCI Express 规范实际上并不鼓励使用 IO 地址空间，表明它仅出于传统原因而受到支持，并可能在规范的未来版本中被弃用。

通用内存和 IO 映射如图 4-1（第 125 页）所示。内存映射的大小是系统可以使用的地址范围（通常由 CPU 可寻址范围决定）的函数。PCIe 中 IO 映射的大小限制为 32 位（4GB），尽管在使用 Intel 兼容（x86）处理器的许多计算机中，仅使用较低的 16 位（64KB）。PCIe 可以支持高达 64 位的内存地址。

图 4-1 中的映射示例仅显示由端点声明的 MMIO 和 IO 空间，但该能力并非端点独有。交换机和根复合体通常也具有通过 MMIO 和 IO 地址访问的设备特定寄存器。

## **可预取与非可预取内存空间**

图 4-1 显示了由 PCIe 设备声明的两种不同类型的 MMIO：可预取 MMIO（P-MMIO）和非可预取 MMIO（NP-MMIO）。重要的是描述可预取和非可预取内存空间之间的区别。可预取空间具有两个非常明确的属性：

- 读取没有副作用

- 允许写合并

将 MMIO 区域定义为可预取允许该区域中的数据被推测性地预先获取，以预期请求者可能很快需要比实际请求更多的数据。能够安全地进行这种轻微的数据缓存是因为读取数据不会更改目标设备上的任何状态信息。也就是说，读取位置的行为没有副作用。例如，如果请求者请求从地址读取 128 字节，则完成者也可以预取接下来的 128 字节，以便在被请求时手头有它以努力提高性能。但是，如果请求者从未请求额外的数据，则完成者最终将不得不

**123**

## **PCI Express Technology**

丢弃它以释放缓冲区空间。如果读取数据的操作更改了该地址处的值（或者有其他副作用），则将无法恢复丢弃的数据。然而，对于可预取空间，读取没有副作用，因此始终可以稍后返回并获取它，因为原始数据仍将存在。

您可能想知道什么样的内存空间可能有读取副作用？一个示例是一个内存映射状态寄存器，它被设计为在读取时自动清除自身，以节省程序员在读取状态后显式清除位的额外步骤。

进行此区分对于 PCI 比 PCIe 更重要，因为该总线协议中的事务不包含传输大小。当交换数据的设备位于同一总线上时，这不是问题，因为存在实时握手以指示请求者何时完成并且不再需要更多数据，因此知道字节计数并不那么重要。但是当传输必须跨过桥时并不那么容易，因为对于读取，桥需要在另一条总线上收集数据时猜测字节计数。猜错传输大小会增加延迟并降低性能，因此获得预取许可可能非常有帮助。这就是为什么在 PCI 中将内存空间指定为可预取的概念是有帮助的。由于 PCIe 请求确实包含传输大小，因此它不如以前那么有趣，但为了向后兼容而保留。

**124**

**第 4 章：地址空间与事务路由**

_图 4-1：通用内存和 IO 地址映射_

**==> picture [300 x 354] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>根复合体 系统<br>内存<br>(DRAM)<br>交换机<br>内存映射<br>2 [32] 或 2 [64]<br>MMIO<br>传统 PCIe<br>(可预取)<br>端点 端点<br>MMIO (NP) MMIO (P)<br>MMIO<br>IO MMIO (NP) (非可预取)<br>PCIe 功能的寄存器<br>和缓冲区可能映射到 IO 和<br>内存地址空间<br>2 [32] IO 映射 系统<br>内存<br>(DRAM)<br>IO<br>端口<br>2 [16]<br>0 0<br>**----- End of picture text -----**<br>


**125**

**PCI Express Technology**

## **基地址寄存器 (BAR)**

## **概述**

系统中每个设备在所需地址空间的量和类型方面可能具有不同的要求。例如，一个设备可能有 256 字节的内部寄存器/存储，应该可以通过 IO 地址空间访问，而另一个设备可能有 16KB 的内部寄存器/存储，应该可以通过 MMIO 访问。

基于 PCI 的设备不允许自行决定应使用哪些地址来访问其内部位置，这由系统软件（即 BIOS 和 OS 内核）决定。因此，设备必须为系统软件提供一种确定设备地址空间需求的方法。一旦软件了解了设备在地址空间方面的需求，那么假设该请求可以满足，软件将简单地为该设备分配适当类型（IO、NP-MMIO 或 P-MMIO）的可用地址范围。

这一切都是通过配置空间头中的基地址寄存器 (BAR) 实现的。如第 127 页图 4-2 所示，Type 0 头有六个可用的 BAR（每个为 32 位大小），而 Type 1 头只有两个 BAR。Type 1 头存在于所有桥设备中，这意味着每个交换机端口和根复合体端口都有一个 Type 1 头。Type 0 头存在于端点等非桥设备中。这方面的一个示例如第 128 页图 4-3 所示。

系统软件必须首先确定设备请求的地址空间的大小和类型。设备设计者知道应通过 IO 或 MMIO 访问的内部寄存器/存储的总体大小。设备设计者还知道访问这些寄存器时设备将如何行为（即读取是否有副作用）。这将决定应请求可预取 MMIO（读取没有副作用）还是非可预取 MMIO（读取有副作用）。知道此信息后，设备设计者将 BAR 的低几位硬编码为特定值，以指示所请求地址空间的类型和大小。

BAR 的高位可由软件写入。一旦系统软件检查 BAR 的低几位以确定所请求的地址空间的大小和类型，系统软件随后将分配给该设备的地址范围的基地址写入 BAR 的高位。由于单个

**126**

**第 4 章：地址空间与事务路由**

端点（Type 0 头）有六个 BAR，因此最多可以发出六个不同的地址空间请求。但是，这在现实世界中并不常见。大多数设备将请求 1-3 个不同的地址范围。

并非所有 BAR 都必须实现。如果设备不需要所有 BAR 来映射其内部寄存器，则额外的 BAR 被硬编码为全 0，通知软件这些 BAR 未实现。

_图 4-2：配置空间中的 BAR_

**==> picture [386 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 头 Type 1 头<br>31 23 15 7 0 31 23 15 7 0<br>设备 ID 厂商 ID 00h 设备 ID 厂商 ID 00h<br>状态 命令 04h 状态 命令 04h<br>类代码   修订 08h 类代码   修订 08h<br>      ID       ID<br>BIST 头 延迟 缓存 0Ch BIST 头 延迟 缓存 0Ch<br>类型 定时器 行大小 类型 定时器 行大小<br>基地址 0 (BAR0) 10h 基地址 0 (BAR0) 10h<br>基地址 1 (BAR1) 14h 基地址 1 (BAR1) 14h<br>基地址 2 (BAR2) 18h 二级延迟定时器 下属总线号 二级总线号 主总线号 18h<br>基地址 3 (BAR3) 1Ch 二级状态 IO 上限 IO 基址 1Ch<br>基地址 4 (BAR4) 20h (非可预取)内存上限 (非可预取)内存基址 20h<br>可预取 可预取<br>基地址 5 (BAR5) 24h 内存上限 内存基址 24h<br>CardBus CIS 指针 28h 可预取内存基址 28h<br>高 32 位<br>子系统设备 ID 子系统厂商 ID 2Ch 可预取内存上限高 32 位 2Ch<br>IO 上限 IO 基址<br>扩展 ROM 基址 30h 高 16 位 高 16 位 30h<br>保留 能力 34h 保留 能力 34h<br>指针 指针<br>保留 38h 扩展 ROM 基址 38h<br>最大延迟 最小授权 中断引脚 中断线 3Ch 桥控制 中断引脚 中断线 3Ch<br>**----- End of picture text -----**<br>


一旦对 BAR 进行了编程，就可以通过编程到 BAR 中的地址范围访问设备内的内部寄存器或本地内存。每当设备看到其地址映射到其 BAR 之一的请求时，它都将接受该请求，因为它是目标。

**127**

**PCI Express Technology**

_图 4-3：PCI Express 设备及 Type 0 和 Type 1 头的使用_

**==> picture [278 x 256] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>根复合体 系统<br>内存<br>P2P (DRAM)<br>Type 1 头<br>P2P（虚拟 PCI-PCI 桥）<br>交换机<br>Type 0 头<br>PCIe PCIe<br>端点 端点<br>P2P P2P<br>**----- End of picture text -----**<br>


## **BAR 示例 1：32 位内存地址空间请求**

第 130 页图 4-4 显示了设置 BAR 的基本步骤，在本例中，它是请求 4KB 的非可预取内存 (NP-MMIO) 块。在图中，BAR 在配置过程中的三个点显示：

1. 在图 4-4 的 (1) 中，我们看到 BAR 的未初始化状态。设备设计者已固定低几位以指示大小和类型，但高位（可读写）显示为 X，表示它们的值未知。系统软件将首先向每个 BAR 写入全 1（使用配置写入）以设置所有可写位。（当然，硬编码的低位不受任何配置写入的影响。）BAR 的第二个视图，

**128**

**第 4 章：地址空间与事务路由**

如图 4-4 的 (2) 所示，显示了配置软件向其写入全 1 后的样子。

写入全 1 是为了确定最低有效可写位是哪一位。该位位置指示所请求地址空间的大小。在本例中，最低有效可写位是 bit 12，因此此 BAR 正在请求 2[12]（或 4KB）的地址空间。如果最低有效可写位是 bit 20，那么 BAR 将请求 2[20]（或 1MB）的地址空间。

2. 在向 BAR 写入全 1 后，软件转而读取每个 BAR 的值，从 BAR0 开始，以确定所请求地址空间的类型和大小。第 129 页表 4-1 总结了本例中 BAR0 配置读取的结果。

3. 此过程的最后一步是系统软件在知道所请求地址空间的大小和类型后为 BAR0 分配一个地址范围。BAR 的第三个视图，在图 4-4 的 (3) 中，显示了软件写入所分配地址块的起始地址后的样子。在本例中，起始地址是 F900_0000h。

此时 BAR0 的配置完成。一旦软件在 Command 寄存器（偏移 04h）中启用内存地址解码，此设备将接受其收到的从 F900_0000h - F900_0FFFh（大小为 4KB）范围内的任何内存请求。

_表 4-1：向 BAR 写入全 1 后读取 BAR 的结果_

|**BAR 位**|**含义**|
|---|---|
|0|读为 0b，表示内存请求。由于这是内存请求，<br>bit 3:1 也具有编码含义。|
|2:1|读为 00b 表示目标仅支持解码 32 位<br>地址|
|3|读为 0b，表示请求用于非可预取内存（意味着<br>读取确实有副作用）；NP-MMIO|
|11:4|读为全 0，表示请求的大小（这些位被硬<br>编码为 0）|
|31:12|读为全 1，因为软件尚未用起始地址对高位<br>进行编程。由于 bit 12 是最低有效可写位，<br>所请求的内存大小为 212= 4KB。|



**129**

**PCI Express Technology**

_图 4-4：32 位非可预取内存 BAR 设置_

## **Type 0 头**

**==> picture [364 x 286] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 23 15 7 0<br>
设备 ID 厂商 ID 00h 未初始化的 BAR<br>
31 12 4 3 2 1 0<br>
状态 命令 04h<br>
XXXX XXXX XXXX XXXX XXXX 00000000 0 0 0 0 (1)<br>
类代码   修订 08h<br>
      ID<br>
BIST 头 延迟 缓存 0Ch BAR 写入全 1<br>
类型 定时器 行大小 31 12 4 3 2 1 0<br>
基地址 0 (BAR0) 10h 1111 1111 1111 1111 1111 00000000 0 0 0 0 (2)<br>
基地址 1 (BAR1) 14h<br>
基地址 2 (BAR2) 18h BAR 写入基地址<br>
31 12 4 3 2 1 0<br>
基地址 3 (BAR3) 1Ch 1111 1001 0000 0000 0000 00000000 0 0 0 0 (3)<br>
基地址 4 (BAR4) 20h (F) (9) (0) (0) (0)<br>
基地址 5 (BAR5) 24h 0 = 内存请求1 = IO 请求<br>
CardBus CIS 指针 28h 00 = 32 位解码<br>
10 = 64 位解码<br>
子系统设备 ID 子系统厂商 ID 2Ch 0 = 非可预取1 = 可预取<br>
扩展 ROM 基址 30h<br>
4KB 对齐的起始地址的<br>
保留 能力指针 34h 高 20 位（低 12 位假定为 = 0）<br>
(F900 0000h)<br>
保留 38h<br>
本例：<br>
最大延迟 最小授权 中断引脚 中断线 3Ch - 4KB 非可预取内存<br>
- 地址范围必须低于 4GB（32 位解码）<br>
注意：如果内存地址分配在 4GB 边界以下，<br>
在以该设备为目标时必须使用 3DW 头。<br>**----- End of picture text -----**<br>


## **BAR 示例 2：64 位内存地址空间请求**

在前一个示例中，我们看到 BAR0 用于请求非可预取内存地址空间 (NP-MMIO)。在本例中，如图 4-5（第 132 页）所示，BAR1 和 BAR2 用于请求 64MB 块的可预取内存地址空间。这里使用两个连续的 BAR 是因为该设备为此请求支持 64 位地址，这意味着软件可以在 4GB 地址边界之上分配所请求的地址空间

**130**

**第 4 章：地址空间与事务路由**

如果它愿意（但这不是必需的）。由于地址可以是 64 位地址，因此必须将两个连续的 BAR 一起使用。

与之前一样，BAR 在配置过程中的三个点显示：

1. 在图 4-5 的 (1) 中，我们看到 BAR 对的未初始化状态。设备设计者已硬编码较低 BAR（本例中为 BAR1）的低几位以指示请求类型和大小，而较高 BAR（BAR2）的所有位都是可读写的。系统软件的第一步是向每个 BAR 写入全 1。在图 4-5 的 (2) 中，我们看到在向其写入全 1 后的 BAR。

2. 如前一示例所述，系统软件已评估了 BAR0。因此软件的下一步是读取下一个 BAR（BAR1）并评估它以查看设备是否正在请求其他地址空间。一旦读取了 BAR1，软件就会意识到正在请求更多地址空间，并且此请求是针对可预取内存地址空间的，可以在 64 位地址范围内的任何位置分配。由于它支持 64 位地址，因此下一个连续的 BAR（本例中为 BAR2）被视为 BAR1 的高 32 位。因此软件现在也读取 BAR2 的内容。但是，软件不会以与 BAR1 相同的方式评估 BAR2 的低几位，因为它知道 BAR2 仅仅是 BAR1 中启动的 64 位地址请求的高 32 位。第 132 页表 4-2 总结了这些配置读取的结果。

3. 此过程的最后一步是系统软件在知道所请求地址空间的大小和类型后为 BAR 分配一个地址范围。BAR 的第三个视图，在图 4-5 的 (3) 中，显示了在软件使用两次配置写入来对所分配范围的 64 位起始地址进行编程之后的结果。在本例中，较高 BAR（BAR 对中的地址位 33）的 bit 1 被置位，较低 BAR（BAR 对中的地址位 30）的 bit 30 被置位以指示起始地址 2_4000_0000h。两个 BAR 中的所有其他可写位都被清除。

此时，BAR 对（BAR1 和 BAR2）的配置完成。一旦软件在 Command 寄存器（偏移 04h）中启用内存地址解码，此设备将接受其收到的从 2_4000_0000h - 2_43FF_FFFFh（大小为 64MB）范围内的任何内存请求。

**131**

**PCI Express Technology**

_图 4-5：64 位可预取内存 BAR 设置_

## **Type 0 头**

**==> picture [375 x 269] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 23 15 7 0 未初始化的 BAR 对<br>
设备 ID 厂商 ID 00h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>
状态 命令 04h XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XXXX XX 00 0000 0000 0000 0000 0000 1 1 0 0 (1)<br>
BAR n+1 BAR n<br>
类代码   修订 08h<br>
      ID<br>
BIST 头 延迟 缓存 0Ch<br>
类型 定时器 行大小 BAR 对写入全 1<br>
基地址 0 (BAR0) 10h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>
基地址 1 (BAR1) 14h 1111 1111 1111 1111 1111 1111 1111 1111 1111 11 00 0000 0000 0000 0000 0000 1 1 0 0 (2)<br>
基地址 2 (BAR2) 18h<br>
基地址 3 (BAR3) 1Ch<br>
BAR 对写入基地址<br>
基地址 4 (BAR4) 20h 31 (BAR 2) 0 31 26 (BAR 1) 4 3 2 1 0<br>
基地址 5 (BAR5) 24h 0000 0000 0000 0000 0000 0000 0000 0010 0100 00 00 0000 0000 0000 0000 0000 1 1 0 0 (3)<br>
CardBus CIS 指针 28h (0) (0) (0) (0) (0) (0) (0) (2) (4) (0) 0 = 非可预取<br>
子系统设备 ID 子系统厂商 ID 2Ch 1 = 可预取00 = 32 位解码<br>
10 = 64 位解码<br>
扩展 ROM 基址 30h<br>
0 = 内存请求<br>
保留 能力 34h 1 = IO 请求<br>
指针<br>
保留 38h 64MB 对齐的起始地址的<br>
高 38 位（低位假定为 = 0）<br>
(0000 0002 4000 0000h)<br>
最大延迟 最小授权 中断引脚 中断线 3Ch<br>
本例：<br>
- 64MB 可预取内存<br>
- 地址范围可在 4GB 边界之上（64 位解码）<br>**----- End of picture text -----**<br>


_表 4-2：向两个 BAR 写入全 1 后读取 BAR 对的结果_

|**BAR**|**BAR 位**|**含义**|
|---|---|---|
|低|0|读为 0b，表示内存请求。由于这是内存请求，bit 3:1 也具有编码含义。|
|低|2:1|读为 10b 表示目标支持 64 位地址解码器，并且下一个连续的 BAR 包含地址信息的高 32 位。|



**132**

**第 4 章：地址空间与事务路由**

_表 4-2：向两个 BAR 写入全 1 后读取 BAR 对的结果（续）_

|**BAR**|**BAR 位**|**含义**|
|---|---|---|
|低|3|读为 1b，表示请求用于可预取内存（意味着读取没有副作用）；P-MMIO|
|低|25:4|读为全 0，表示请求的大小（这些位被硬编码为 0）|
|低|31:26|读为全 1，因为软件尚未用起始地址对高位进行编程。请注意，由于 bit 26 是最低有效可写位，因此内存地址空间请求大小为 226，即 64MB。|
|高|31:0|读为全 1。这些位将用作系统软件编程的 64 位起始地址的高 32 位。|



## **BAR 示例 3：IO 地址空间请求**

从前两个示例继续，此相同功能也正在请求 IO 空间，如图 4-6（第 134 页）所示。在图中，请求的 BAR（本例中为 BAR3）在配置过程中的三个点显示：

1. 在图 4-6 的 (1) 中，我们看到 BAR 的未初始化状态。系统软件先前已向每个 BAR 写入全 1，并已评估了 BAR0，然后是 BAR1 和 BAR2。现在软件将使用 BAR3 查看此设备是否正在请求其他地址空间。图 4-6 的状态 (2) 显示了在写入全 1 之后 BAR3 的状态。

2. 软件现在读取 BAR3 以评估请求的大小和类型。第 134 页表 4-3 总结了此配置读取的结果。

3. 现在软件知道这是对 256 字节 IO 地址空间的请求，最后一步是使用正在分配给此设备的 IO 地址范围的基地址对 BAR 进行编程，特别是此 BAR。图 4-6 的状态 (3) 显示了此步骤之后 BAR 的状态。在我们的示例中，设备起始地址为 16KB，因此写入 bit 14 得到的基址为 4000h；所有其他高位都被清除。

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
