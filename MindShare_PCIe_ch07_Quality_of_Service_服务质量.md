# 📘 第 7 章　服务质量 (Chapter 7. Quality of Service)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0254.md` ... `chunks/chunk0256.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [7.1 Quality of Service — 服务质量](#sec-7-1)
- [7.2 Quality of Service — 服务质量](#sec-7-2)

<a id="sec-7-1"></a>
## 7.1 Quality of Service | 服务质量

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

There are three general models for ordering transactions in a traffic flow: 

1. **Strong Ordering** : PCI Express requires strong ordering of transactions flowing through the fabric that have the same Traffic Class
(TC) assignment. Transactions that have the same TC value assigned to them are mapped to a given VC, therefore the same rules apply to
transactions within each VC. Consequently, when multiple TCs are assigned to the same VC all transac‐ tions are typically handled as a
single TC, even though no ordering rela‐ tionship exists between different TCs.

2. **Weak Ordering** : Transactions stay in sequence unless reordering would be helpful. Maintaining the strong ordering relationship
between transactions can result in all transactions being blocked due to dependencies associated with a given transaction model (e.g., The
Producer/Consumer Model). Some of the blocked transactions very likely are not related to the depen‐ dencies and can safely be reordered
ahead of blocking transactions.

3. **Relaxed Ordering** : Transactions can be reordered, but only under certain controlled conditions. The benefit is improved performance
like the weak‐ ordered model, but only when specified by software so as to avoid prob‐ lems with dependencies. The drawback is that only
some transactions will be optimized for performance. There is some overhead for software to enable transactions for Relaxed Ordering (RO).
## **Simplified Ordering Rules** 

The 2.1 revision of the spec introduced a simplified version of the Ordering Table as shown in Table 8‐1 on page 289. The table can be
segmented on a per topic basis as follows:

- Producer/Consumer rules (page 290) 

- Relaxed Ordering rules (page 296) 

- Weak Ordering rules (page 299) 

- ID Ordering rules (page 301) 

- Deadlock avoidance (page 303) 

These sections provide details associated with the ordering models, operation, rationales, conditions and requirement. 

## **Ordering Rules and Traffic Classes (TCs)** 

PCI Express ordering rules apply to transactions of the same Traffic Class (TC). Transactions moving through the fabric that have different
TCs have no order‐ ing requirement and are considered to be associated with unrelated applica‐ tions. As a result, there is no transaction
ordering related performance degradation associated with packets of different TCs.

Packets that do share the same TC may experience performance degradation as they flow through the PCIe fabric. This is because switches and
devices must support ordering rules that may require packets to be delayed or forwarded in front of packets previously sent.

As discussed in Chapter 7, entitled ʺQuality of Service,ʺ on page 245, transac‐ tions of different TC may map to the same VC. The TC‐to‐VC
mapping configu‐ ration determines which packets of a given TC map to a specific VC. Even though the transaction ordering rules apply only
to packets of the same TC, it may be simpler to design endpoint devices/switches/root complexes that apply the transaction ordering rules to
all packets within a VC even though multiple TCs are mapped to the same VC.

As one would expect, there are no ordering relationships between packets that map to different VCs no matter their TC. 

## **Ordering Rules Based On Packet Type** 

Ordering relationships defined by the PCIe spec are based on TLP type. TLPs are divided into three categories: 1) Posted, 2) Completion and
3) Non‐Posted TLPs.

The Posted category of TLPs include memory write requests (MWr) and Mes‐ sages (Msg/MsgD). Completion category of TLPs include Cpl and CplD.
Non‐ Posted category of TLPs include MRd, IORd, IOWr, CfgRd0, CfgRd1, CfgWr0 and CfgWr1.

The transaction ordering rules are described by a table in the following section “The Simplified Ordering Rules Table” on page 288. As you
will notice, the table shows TLPs listed according to the three categories mentioned above with their ordering relationships defined.

## **The Simplified Ordering Rules Table** 

The table is organized in a Row Pass Column fashion. All of the rules are sum‐ marized following the Simplified Ordering Table. Each rule or
group of rules define the actions that are required.

In Table 8‐1 on page 289, columns 2 ‐ 5 represent transactions that have previ‐ ously been delivered by a PCI Express device, while row A ‐
D represents a new transaction that has just arrived. For outbound transactions, the table specifies whether a transaction represented in
the row (A ‐ D) is allowed to pass a previ‐ ous transaction represented by the column (2 ‐ 5). A ‘No’ entry means the trans‐ action in the
row is not allowed to pass the transaction in the column. A ‘Yes’ entry means the transaction in the row must be allowed to pass the
transaction in the column to avoid a deadlock. A ‘Yes/No’ entry means a transaction in a row is allowed to pass the transaction in the
column but is not required to do so. The entries in the following have the meaning.
_Table 8‐1: Simplified Ordering Rules Table_ 

|**Row pass**<br>**Column?**<br>(Col 1)|**Row pass**<br>**Column?**<br>(Col 1)|**Posted Request**<br>(Col 2)|**Non-Posted
Request**|**Non-Posted Request**|**Completion**<br>(Col 5)|
|---|---|---|---|---|---|
||||**Read Request**<br>(Col 3)|**NPR with**<br>**Data**<br>(Col 4)||
|**Posted Request**<br>(Row A)||a) No<br>b) Y/N|Yes|Yes|a) Y/N<br>b) Yes|
|**Non-Posted** **Request**|**Read** **Request** (Row B)|a) No b) Y/N|Y/N|Y/N|Y/N|
||**NPR with**<br>**Data**<br>(Row C)|a) No<br>b) Y/N|Y/N|Y/N|Y/N|
|**Completion**<br>(Row D)||a) No<br>b) Y/N|Yes|Yes|a) Y/N<br>b) No|


- **A2a, B2a, C2a, D2a** — to enforce the Producer/Consumer model, a subse‐ quent transaction is not allowed to pass a Posted Request. 

- **A2, D2b** —If RO is set, then a Read Completion is permitted to pass a previ‐ ously queued Memory Write or Message Request. 

- **A2b, B2b, C2b, D2b** — if the optional IDO is being used, a subsequent transaction is allowed to pass a Posted Request, as long as their
Requester IDs are different

- **A3, A4** — A Memory Write or Message Request must be allowed to pass Non‐Posted Requests to avoid deadlocks. 

- **A5a** — Posted Request is permitted but not required to pass Completions 

- **A5b** — Deadlock avoidance case. In a PCIe‐to‐PCI/PCI‐X bridge, for trans‐ actions going from PCIe to PCI or PCI‐X, a Posted Request
must be able to pass a Completion, or a deadlock may occur.

- **B3, B4, B5, C3, C4, C5,** — These cases implement weak ordering without risking any ordering related problems. 

- **D3, D4** — Completions must be allowed to pass Read and I/O or Configura‐ tion Write Requests (Non‐Posted Requests) to avoid deadlocks. 

- **D5a** — Completions with different Transaction IDs may pass each other. 

- **D5b** — Completions with the same Transaction ID are not allowed to pass each other. This ensures that multiple completions for a single
request will remain in ascending address order.

## **Producer/Consumer Model** 

This section describes the operation of the Producer/Consumer model and the associated ordering rules required for proper operation. Figure
8‐1 on page 291 simply illustrates a sample topology. Subsequent examples of this topology describe the operation of the Producer/Consumer
model with proper ordering, followed by an example of the model failing due to improper ordering.

The Producer/Consumer model is the common method for data delivery in PCI and PCIe. The model comprises five elements as depicted in Figure
8‐1:

- Producer of data 

- Memory data buffer 

- Flag semaphore indicating data has been send by the Producer 

- Consumer of data 

- Status semaphore indicating Consumer has read data 

The specification states that the Producer/Consumer model will work regard‐ less of the arrangement of all the elements involved. In this
example, the Flag and Status elements reside in the same physical device, but could be located in different devices.
_Figure 8‐1: Example Producer/Consumer Topology_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0306.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


## **Producer/Consumer Sequence — No Errors** 

Refer to Figure 8‐2 on page 293 during the following discussion. The example presumes that the Flag and Status element are cleared to start
with. These sema‐ phores are included within the same device in this example. The sequence of numbered events in the description below and
depicted in Figure 8‐2 on page 293 reflect the correct ordering in this Part 1 sequence.

## **PCI Express 3.0 Technology** 

1. In the example, a device called the **Producer** performs one or more Memory Write transactions (Posted Requests) targeting a **Data
Buffer** in memory. Some delay can occur as the data flows through Posted buffers.

2. The Consumer periodically checks the Flag by initiating a Memory Read transaction (Non‐Posted Request) to determine if data has been
delivered by the Producer.

3. The Flag semaphore is read by the device and a Memory Read Completion is returned to the Consumer, indicating that notification of data
delivery has not been performed by the Producer (Flag = 0) yet.

4. The Producer sends a Memory Write Transaction (Posted Request) to update the Flag to 1. 

5. Once again, the Consumer checks the Flag by performing the same transac‐ tion performed in step 2. 

6. When Flag semaphore is read this time, the Flag is set to 1, indicating to the Consumer, via the Completion, that all of the data has
been delivered by the Producer to memory.

7. Next, the Consumer performs a Memory Write transaction (Posted Request) to clear the Flag semaphore back to zero. 

Figure 8‐3 on page 294 continues the example in this Part 2 sequence. 

8. The Producer, having more data to send, periodically checks the Status semaphore by initiating a Memory Read transaction (Non‐Posted
Request).

9. The Status semaphore is read by the Producer and a Memory Read Comple‐ tion is returned to the Producer, indicating that the Consumer has
not read the memory buffer contents and updated Status (Status = 0).

10. The Consumer, knowing that the memory buffer has data available, per‐ forms one or more Memory Read Requests (Non‐Posted Requests) to
get the contents from the buffer.

11. Memory contents are read and returned to the Consumer. 

12. Upon completing the data transfer, the Consumer initiates a Memory Write Request (Posted Request) to set the Status semaphore to a 1. 

13. Once again, the Producer checks the Status semaphore by delivering a Memory Read Request (Non‐Posted Request). 

14. The device reads the Status and this time it is set to 1. The Completion is returned to the Producer, thereby indicating data can be
sent to Memory.

15. The Producer sends a Memory Write to Clear the Status semaphore to 0. 

16. The sequence of events starting with step 1. is repeated by the Producer. 
_Figure 8‐2: Producer/Consumer Sequence Example — Part 1_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0307.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


_Figure 8‐3: Producer/Consumer Sequence Example — Part 2_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0308.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>

## **Producer/Consumer Sequence — Errors** 

The previous example was handled correctly without a discussion of the order‐ ing rules; however it may have been apparent that race
conditions can cause the Producer/Consumer sequence to fail. Figure 8‐4 on page 296 illustrates a simple sequence to demonstrate one of
several problems that can arise without order‐ ing rules being enforced. Refer to Figure Figure 8‐4 on page 296 during the fol‐ lowing
discussion.

1. Producer performs a Memory Write request (Posted Request) to the mem‐ ory buffer. Let us assume that the memory write data is temporarily
stuck in the Switch upstream port Posted Flow Control buffer.

2. The Producer sends a Memory Write Transaction (Posted Request) to update the Flag to 1. 

3. The Consumer initiates a Memory Read Request (Non‐Posted Request) to check if the Flag has been set to 1. 

4. The contents of the Flag is returned to the Consumer via a Completion. 

5. Knowing that data has been delivered to memory, the Consumer performs a memory read request to fetch the data. However, the Consumer is
unaware that the data is temporarily stuck in a Posted Flow Control buffer due to lack of flow control credits associated with the link
between the upstream switch port and the Root Complex. Consequently, the Consumer receives old data when the Completion is returned to the
Consumer.

The problem is avoided with ordering rules supported by virtual PCI bridges within the topology. In this example, when the Consumer
performed the Mem‐ ory Read transaction in steps 3 and 4, the Virtual PCI bridge at the upstream switch port should not allow the contents
of the flag (Completion 4) to be for‐ warded ahead of the previously posted data.

_Figure 8‐4: Producer/Consumer Sequence with Error_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0309.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


## **Relaxed Ordering** 

PCI Express supports the Relaxed Ordering (RO) mechanism added for PCI‐X. RO allows switches in the path between the Requester and Completer
to reor‐ der some transactions when doing so would improve performance.
The ordering rules that support the Producer/Consumer model may result in transactions being blocked in cases when they’re unrelated to any
Producer/ Consumer transaction sequence. To alleviate this problem, a transaction can have its RO attribute bit set, indicating that
software verifies it to be unrelated to other transactions, and that allows it to be re‐ordered ahead of other transac‐ tions. For example,
if a posted write is delayed because the target’s buffer space is unavailable, then all subsequent transactions must wait until that finally
resolves and the write is delivered. If a subsequent transaction was known by software to be unrelated to previous ones and the RO bit was
set to show that, then it could be allowed to go before the write without risking a problem.

The RO bit (bit 5 of byte 2 of dword 0 in the TLP header as shown in Figure 8‐5 on page 297) may be used by the device if its device driver
has enabled it to do so. Request packets are then allowed to use this attribute as directed by soft‐ ware when it requests that a packet be
sent. When switches or the Root Com‐ plex see a packet with this attribute bit set, they have permission to reorder it although it’s not
required that they should.

_Figure 8‐5: Relaxed Ordering Bit in a 32‐bit Header_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0310.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


## **RO Effects on Memory Writes and Messages** 

Switches and Root Complexes must observe the setting of the RO bit in transac‐ tions. Memory writes and Messages are both posted writes,
both are received into the same Posted buffer, and both are subject to the same ordering require‐ ments. When the RO bit is set, switches
handle these transactions as follows:

- Switches are permitted to reorder memory write transactions just posted ahead of previously posted memory write transactions or message
transac‐ tions. Similarly, message transactions just posted may be ordered ahead of

previously posted memory write or message transactions. Switches must also forward the RO bit unmodified. The RO bit is ignored by PCI‐X
bridges, which always forward writes in order (there would be little pur‐ pose in allowing them to go out of order anyway; if one is blocked
for some reason, the next will be blocked, too). Another difference is that message transactions had not been defined for PCI‐X, either.

- The Root Complex is permitted to reorder posted write transactions (here it makes sense because the Root could write to different areas of
memory so, if one area is busy it can write to a different one). Also, when receiving writes with RO set, the Root is permitted to write
each byte to memory in any address order.

## **RO Effects on Memory Read Transactions** 

All read transactions in PCI Express are handled as split transactions. When a device issues a memory read request with the RO bit set, the
Completer returns the requested read data in a series of one or more split completion transactions, and uses the same RO setting as in the
request. Switch behavior in this case is as follows:

1. A switch that receives a memory read with RO forwards the request in the order received, and must not reorder it ahead of memory write
transactions that were previously posted. That guarantees that all write transactions moving in the direction of the read request are pushed
ahead of the read. This is part of the Producer/Consumer example shown earlier, and software may depend on this flushing action for proper
operation. The RO bit must not be modified by the switch.

2. When the Completer receives the memory read, it fetches the requested data and delivers one or more Completions that also have the RO bit
set (its value is copied from the original request).

3. A switch receiving the Completions is allowed to re‐order them ahead of previously posted memory writes moving in the direction of the
Comple‐ tion. If the writes were blocked (for example, due to flow control), then the Completions will be allowed to go ahead of them.
Relaxed ordering in this case improves read performance. Table 8‐2 summarizes the relaxed order‐ ing behavior allowed by switches.
_Table 8‐2: Transactions That Can Be Reordered Due to Relaxed Ordering_ 

|**These Transactions with RO=1 Can Pass**|**These Transactions**|
|---|---|
|Memory Write Request|Memory Write Request|
|Message Request|Memory Write Request|
|Memory Write Request|Message Request|
|Message Request|Message Request|
|Read Completion|Memory Write Request|
|Read Completion|Message Request|


## **Weak Ordering** 

Temporary transaction blocking can occur when strong ordering rules are rigor‐ ously enforced. Modifications that don’t violate the
Producer/Consumer pro‐ gramming model can eliminate some blocking conditions and improve link efficiency. Implementing the Weakly‐Ordered
model can alleviate this problem.

## **Transaction Ordering and Flow Control** 

The motivation behind splitting VC buffers of a given number into flow con‐ trolled sub‐buffers P, NP and CPL is because it simplifies
processing of the transaction ordering rules once TLPs have been parsed or binned into their respective buffers. The transaction ordering
processing logic then applies order‐ ing rules between these three sub‐buffers or to each sub‐buffer.

Since TLPs are binned into their respective three sub‐buffers in order to process transaction ordering rules, it is necessary to define the
flow control mechanism between each virtual channel sub‐buffer (P, NP, CPL) of neighboring ports at opposite ends of the Link. In fact, you
may recall that there is an independent flow control mechanism between Header (Hdr) and Data (D) sub‐buffers of each sub‐buffer category (P,
NP, CPL) of each virtual channel number.

## **Transaction Stalls** 

Strong ordering can result in instances where all transactions are blocked due to a single full receive buffer. For example, the ordering
requirements for the Pro‐ ducer/Consumer model cannot be changed, but ordering for transactions that aren’t part of that model can. To
improve performance, let’s consider a weakly‐ ordered scheme; one that puts the minimal requirements on transaction order‐ ing.

This example depicts transmit and receive buffers associated with the delivery of transactions in a single direction for a single VC. Recall
that each of the trans‐ action types (Posted, Non‐Posted, and Completions) have independent flow control within the same VC. The numbers in
the transmit buffers show the order in which these transactions were issued, and the non‐posted receive buffer is currently full. Consider
the following sequence.

1. Transaction 1 (memory read) is the next transaction to send, but there aren’t enough flow control credits so it must wait. 

2. Transaction 2 (posted memory write) is the next subsequent transaction. If strong ordering is enforced, a memory write must not pass a
previously queued read transaction.

3. This restriction applies to all subsequent transactions, too, with the result that they’re all stalled until the first one finishes. 

_Figure 8‐6: Strongly Ordered Example Results in Temporary Stall_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0311.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>

## **VC Buffers Offer an Advantage**

</td>
<td width="50%">

**PCI Exress 3.0 Technology**

_图 8-3：生产者/消费者序列示例 — 第 2 部分_

**==> 图片 [367 x 424] 已省略 <==**

**----- 图片文字开始 -----**<br>
Consumer<br>(Processor)<br>12 10<br>Root Complex P Memory<br>NP 11<br>CPL<br>P<br>NP<br>CPL<br>P Posted Request<br>NP Non-Posted
Request<br>CPL Completion<br>13 13 14<br>14 15<br>8 15 8 9<br>Producer Flag 0 1<br>Status 0
1<br>P<br>NP<br>CPL<br>P<br>NP<br>CPL<br>CPL<br>NP<br>P<br>CPL<br>NP<br>P<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL P
NP CPL P NP CPL<br>**----- 图片文字结束 -----**<br>


**第 8 章：事务排序**

## **生产者/消费者序列 — 错误**

前面的示例被正确处理，但没有讨论排序规则；然而可能已经明显的是，竞争条件可能导致生产者/消费者序列失败。第 296 页的图 8-4 展示了一个简单的序列，用于演示在没有强制执行排序规则时可能出现的几个问题之一。在以下讨论中请参考第 296 页的图 8-4。

1. 生产者执行对内存缓冲区的内存写请求（Posted 请求）。假设内存写数据暂时卡在交换机上游端口的 Posted 流控缓冲区中。

2. 生产者发送内存写事务（Posted 请求）以将 Flag 更新为 1。

3. 消费者启动内存读请求（Non-Posted 请求）以检查 Flag 是否已设置为 1。

4. Flag 的内容通过完成返回给消费者。

5. 知道数据已传送到内存后，消费者执行内存读请求以获取数据。但是，消费者不知道数据由于流控信用（与上游交换机端口和根复合体之间的链路相关联）不足而暂时卡在 Posted 流控缓冲区中。因此，当完成被返回给消费者时，消费者收到的是旧数据。

通过拓扑内虚拟 PCI 桥所支持的排序规则可以避免此问题。在本例中，当消费者在步骤 3 和 4 中执行内存读事务时，上游交换机端口的虚拟 PCI 桥不应允许 Flag 的内容（完成 4）被发送到先前已发布的数据之前。

**PCI Exress 3.0 Technology**

_图 8-4：带错误的生产者/消费者序列_

**==> 图片 [341 x 360] 已省略 <==**

**----- 图片文字开始 -----**<br>
Consumer<br>(Processor)<br>3 5 4 6<br>Root Complex P Memory<br>NP<br>CPL<br>P<br>NP<br>CPL<br>Retries Slow Delivery of data<br>P Posted
Request<br>1 NP Non-Posted Request<br>CPL Completion<br>2<br>1 2 2 3 4<br>Producer Flag 0 1<br>Status
0<br>P<br>NP<br>CPL<br>P<br>NP<br>CPL<br>CPL<br>NP<br>P<br>CPL<br>NP<br>P<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL P
NP CPL P NP CPL<br>**----- 图片文字结束 -----**<br>


## **宽松排序**

PCI Express 支持为 PCI-X 添加的宽松排序 (Relaxed Ordering, RO) 机制。RO 允许 Requester 和 Completer 之间路径上的交换机在重排序可以提升性能时重排序某些事务。

**第 8 章：事务排序**

支持生产者/消费者模型的排序规则可能导致事务在以下情况下被阻塞：它们与任何生产者/消费者事务序列无关。为了缓解这个问题，事务可以设置其 RO 属性位，指示软件已验证它与其他事务无关，并允许它被重排序到其他事务之前。例如，如果 Posted
写因为目标缓冲区空间不可用而被延迟，那么所有后续事务都必须等待，直到最终解决并传递该写。如果软件已知后续事务与先前的事务无关，并且设置了 RO 位以表明这一点，那么它可以被允许在写之前通过，而不会有产生问题的风险。

RO 位（TLP 头部第 0 双字的第 2 字节的 bit 5，如第 297 页的图 8-5
所示）可由其设备驱动程序启用了该功能的设备使用。然后，请求报文被允许在软件请求发送报文时按指示使用此属性。当交换机或根复合体看到设置了此属性位的报文时，它们有权重排序它，尽管不要求它们必须这样做。

_图 8-5：32 位头部中的宽松排序位_

**==> 图片 [322 x 97] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R Attr R HT DT EP Attr AT
Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE<br>Byte 8 Address [31:2] R<br>**----- 图片文字结束 -----**<br>


## **RO 对内存写和消息的影响**

交换机和根复合体必须观察事务中 RO 位的设置。内存写和消息都是 Posted 写，都被接收到同一 Posted 缓冲区中，并且都受相同的排序要求约束。当设置 RO 位时，交换机按以下方式处理这些事务：

- 允许交换机将刚发布的内存写事务重新排序到先前已发布的内存写事务或消息事务之前。类似地，刚发布的消息事务也可以被排序到

**PCI Exress 3.0 Technology**

先前已发布的内存写或消息事务之前。交换机还必须以未修改的方式转发 RO 位。RO 位被 PCI-X 桥忽略，它们总是按顺序转发写（允许它们乱序发送没什么意义；如果某个由于某种原因被阻塞，则下一个也会被阻塞）。另一个区别是 PCI-X 也没有定义消息事务。

- 允许根复合体重排序 Posted 写事务（这是有道理的，因为根可以写入不同的内存区域，所以如果一个区域忙，它可以写入另一个区域）。此外，当收到设置了 RO 的写时，根被允许以任何地址顺序将每个字节写入内存。

## **RO 对内存读事务的影响**

PCI Express 中的所有读事务都作为分离事务处理。当设备发出带有 RO 位置位的内存读请求时，Completer 会以一系列一个或多个分离完成事务返回所请求的读数据，并使用与请求中相同的 RO 设置。在这种情况下交换机的行为如下：

1. 收到带有 RO 的内存读的交换机按接收顺序转发请求，并且不得将其重新排序到先前已发布的内存写事务之前。这保证了在读请求方向上移动的所有写事务都被推到读之前。这是前面展示的生产者/消费者示例的一部分，软件可能依赖此刷新操作来正确运行。RO 位不得被交换机修改。

2. 当 Completer 收到内存读时，它获取所请求的数据并交付一个或多个也设置了 RO 位的完成（其值从原始请求复制）。

3. 收到 Completions 的交换机被允许将它们重新排序到沿完成方向移动的先前已发布的内存写之前。如果写被阻塞（例如，由于流控），则完成将被允许在它们之前。完成方向的宽松排序改善了读性能。表 8-2 总结了交换机允许的宽松排序行为。

**第 8 章：事务排序**

_表 8-2：由于宽松排序而可被重排序的事务_

|**带 RO=1 的事务可通过**|**这些事务**|
|---|---|
|内存写请求|内存写请求|
|消息请求|内存写请求|
|内存写请求|消息请求|
|消息请求|消息请求|
|读完成|内存写请求|
|读完成|消息请求|


## **弱排序**

当严格强制执行强排序规则时，可能会发生临时的事务阻塞。不违反生产者/消费者编程模型的修改可以消除一些阻塞情况并提高链路效率。实现弱排序模型可以缓解此问题。

## **事务排序和流控**

将给定数量的 VC 缓冲区拆分为流控子缓冲区 P、NP 和 CPL 的动机是因为它在 TLP 被解析或分类到其各自缓冲区后简化了事务排序规则的处理。事务排序处理逻辑然后在这些三个子缓冲区之间或对每个子缓冲区应用排序规则。

由于 TLP
被分类到其各自的三个子缓冲区中以处理事务排序规则，因此有必要在链路两端的相邻端口的每个虚通道子缓冲区（P、NP、CPL）之间定义流控机制。事实上，您可能记得，每个虚通道编号的每个子缓冲区类别（P、NP、CPL）的头部（Hdr）和数据（D）子缓冲区之间存在独立的流控机制。

**PCI Exress 3.0 Technology**

## **事务停顿**

强排序可能导致由于单个满接收缓冲区而使所有事务被阻塞的情况。例如，不能更改生产者/消费者模型的排序要求，但不属于该模型的事务的排序可以更改。为了提高性能，让我们考虑一个弱排序方案；一个对事务排序施加最小要求的方案。

本例描绘了与单个 VC 单个方向事务传递相关联的发送和接收缓冲区。回想一下，每种事务类型（Posted、Non-Posted 和 Completions）在同一 VC 内都具有独立的流控。发送缓冲区中的数字表示这些事务发出的顺序，Non-Posted
接收缓冲区当前已满。考虑以下序列。

1. 事务 1（内存读）是下一个要发送的事务，但没有足够的流控信用，因此它必须等待。

2. 事务 2（Posted 内存写）是下一个后续事务。如果强制执行强排序，则内存写不得通过先前排队的读事务。

3. 此限制也适用于所有后续事务，结果是它们都被暂停，直到第一个事务完成。

_图 8-6：强排序示例导致临时停顿_

**==> 图片 [300 x 178] 已省略 <==**

**----- 图片文字开始 -----**<br>
Numbers indicate the<br>order of transactions<br>pending transfer<br>Posted<br>7 4 2<br>Non-Posted Non-Posted<br>5 1<br>Completions
Completions<br>8 6 3<br>Tx Rx<br>Rx Tx<br>Posted<br>Full<br>**----- 图片文字结束 -----**<br>


**第 8 章：事务排序**

## **VC 缓冲区的优势**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

<a id="sec-7-2"></a>
## 7.2 Quality of Service | 服务质量

<table>
<thead><tr><th>🇬🇧 English</th><th style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td width="50%">

Transaction ordering is managed within Virtual Channel buffers. These buffers are grouped into Posted, Non‐Posted, and Completion
transactions, and flow control is managed independently for each group. That makes weak ordering more useful because, as in our example,
even if one buffer was full, others could still have space available.

## **ID Based Ordering (IDO)** 

Another opportunity for optimizing ordering and improving performance is related to the nature of traffic streams. Packets from different
requesters are very unlikely to have dependencies; after all, one device could hardly know when the other had finished certain steps based
on ordering because they could have different paths to their shared resource. Bearing this in mind, the 2.1 revi‐ sion of the PCIe spec
introduced what is called ID‐based Ordering to improve performance.

## **The Solution** 

If the packet source isn’t taken into account for transaction ordering then perfor‐ mance can suffer, as shown in Figure 8‐7 on page 302. In
the illustration, trans‐ action 1 makes it way to the upstream port of the switch but is blocked from further progress by a buffer‐full
condition for that packet type in the Root port (which would be indicated by insufficient Flow Control credits). To use the spec
terminology, packets from the same Requester are called a TLP stream. In this example, the path shown for Transaction 1 might include
several TLPs as part of a TLP stream. Transaction 2 then arrives at the same egress port and is also blocked from moving forward because it
must stay in order with Transaction 1. Since the packets came from different sources, (different TLP streams) this delay is almost certainly
unnecessary; it’s very unlikely they could have depen‐ dencies between them, but the normal ordering model doesn’t take this into account.
To get improved performance, we need another option.

The solution is simple: allow packets to be reordered if they don’t use the same Requester ID (or Completer ID, for Completion packets).
This optional capabil‐ ity allows software to enable a device to use IDO and a switch port can recog‐ nize that the packets are part of
different TLP streams. This is done by setting the enable bits in Device Control 2 Register.

_Figure 8‐7: Different Sources are Unlikely to Have Dependencies_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0312.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


## **When to use IDO** 

The spec highly recommends that both IDO and RO be used whenever safely possible. For example, it should be safe for Endpoints to use IDO
for all TLPs when communicating directly with only one other entity, such as the Root Com‐ plex. On the other hand, it would not be safe to
use it if the Endpoint is commu‐ nicating with multiple agents. An example failure case for this from the spec begins with one device doing
a DMA write to memory and then doing a peer‐ to‐peer write to a flag in another device. When the second device receives the flag, it also
initiates a DMA write to the same area of memory. Normally, the two DMA operations would stay in order, but with IDO that ordering can’t be
guaranteed because upstream devices will see them as coming from different device IDs. Similarly, it would not be safe to use RO with
packets that are involved in control traffic.

For Completers, if IDO is enabled it’s recommended that it be used for all Com‐ pletions unless there is a specific reason not to do so. 
## **Software Control** 

Software can enable the use of IDO for Requests or Completions from a given port by setting the appropriate bits in its Device Control 2
Register. As with RO, there are no capability bits to let software find out what the device supports, just enable bits, so software would
need to know by some other means that the device was capable of doing this. These bits enable the use of IDO for that packet type, but
software must still decide whether each individual packet will have its IDO bit set. A new attribute bit in the header indicates whether a
TLP is using IDO, as shown in Figure 8‐8 on page 303. This brings up another related point: Completions normally inherit all the attribute
bits of the Request that generated them, but this may not be true for IDO, since this can be enabled independently by the Completer. In
other words, Completions may use IDO even if the Request that initiated them did not.

_Figure 8‐8: IDO Attribute in 64‐bit Header_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0313.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


## **Deadlock Avoidance** 

Because the PCI bus employs delayed transactions or because PCI Express memory read request may be blocked due to lack of flow control
credits, several deadlock scenarios can develop. These deadlock avoidance rules are included in PCI Express ordering to ensure that no
deadlocks occur regardless of topol‐ ogy. Adhering to the ordering rules prevent problems when boundary condi‐ tions develop due to
unanticipated topologies (e.g., two PCI Express to PCI bridges connected across the PCI Express fabric). Refer to the MindShare book
entitled _PCI System Architecture, Fourth Edition (_ published by Addison‐Wesley) for a detailed explanation of the scenarios that are the
basis for the PCI Express

## **PCI Express 3.0 Technology** 

ordering rules related to deadlock avoidance. Table 8‐1 on page 289 lists the deadlock avoidance ordering rules which are identified as
entries A3, A4, D3, D4 and A5b. Note that avoiding the deadlocks involves “Yes” entries in each of these 5 cases. If blocking occurs due to
lack of flow control credits associated with the Non‐Posted Request buffer identified in column 3 or 4, the Posted Requests associated with
row A or the Completions associated with row D must be moved ahead of the Non‐Posted Requests specified in the column 3 or 4 where the “Yes”
entry exists. Note also that the “Yes” entry in A5b applies only to PCI Express to PCI or PCI‐X Bridges.

Essentially, this deadlock avoidance rule can be summarized as “later arriving Memory Write Requests or Completions must be allowed to pass
earlier blocked Non‐Posted Requests otherwise a deadlock could result”.

## Part Three: 

Data Link Layer 

## _**9**_ 

## _**DLLP Elements**_ 

## **The Previous Chapter** 

The previous chapter discussed the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI, and
the Producer/ Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into
consideration possible dead‐ lock conditions that must be avoided, but did not include any means to avoid the performance problems that
could result.

## **This Chapter** 

In this chapter we describe the other major category of packets, _Data Link Layer Packets_ (DLLPs). We describe the use, format, and
definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power management,
flow control mechanism and can even be used for vendor‐defined purposes.

## **The Next Chapter** 

The following chapter describes a key feature of the Data Link Layer: an auto‐ matic, hardware‐based mechanism for ensuring reliable
transport of TLPs across the Link. Ack DLLPs confirm good reception of TLPs while Nak DLLPs indicate a transmission error. We describe the
normal rules of operation when no TLP or DLLP error is detected as well as error recovery mechanisms associ‐ ated with both TLP and DLLP
errors.

## **General** 

The Data Link Layer can be thought of as managing the lower level Link proto‐ col. Its primary responsibility is to assure the integrity of
TLPs moving between devices, but it also plays a part in TLP flow control, Link initialization and power management, and conveys information
between the Transaction Layer above it and the Physical Layer below it.

In performing these jobs, the Data Link Layer exchanges packets with its neigh‐ bor known as Data Link Layer Packets (DLLPs). DLLPs are
communicated between the Data Link Layers of each device. Figure 9‐1 on page 308 illustrates a DLLP exchanged between devices.

_Figure 9‐1: Data Link Layer Sends A DLLP_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0314.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

<br>


## **DLLPs Are Local Traffic** 

DLLPs have a simple packet format and are a fixed size, 8 bytes total, including the framing bytes. Unlike TLPs, they carry no target or
routing information because they are only used for nearest‐neighbor communications and don’t get routed at all. They’re also not seen by the
Transaction Layer since they’re not part of the information exchanged at that level.
## **Receiver handling of DLLPs** 

When DLLPs are received, several rules apply: 

1. They’re immediately processed at the Receiver. In other words, their flow cannot be controlled the way it is for TLPs (DLLPs are not
subject to flow control).

2. They’re checked for errors; first at the Physical Layer, and then at the Data Link Layer. The 16‐bit CRC included with the packet is
checked by calculat‐ ing what the CRC should be and comparing it to the received value. DLLPs that fail this check are discarded. How will
the Link recover from this error? DLLPs still arrive periodically, and the next one of that type that succeeds will update the missing
information.

3. Unlike TLPs, there’s no acknowledgement protocol for DLLPs. Instead, the spec defines time‐out mechanisms to facilitate recovery from
failed DLLPs.

4. If there are no errors, the DLLP type is determined and passed to the appro‐ priate internal logic to manage: 

 - Ack/Nak notification of TLP status 

 - Flow Control notification of buffer space available 

 - Power Management settings 

 - Vendor specific information 

## **Sending DLLPs** 

## **General** 

These packets originate at the Data Link Layer and are passed to the Physical Layer. If 8b/10b encoding is in use (Gen1 and Gen2 mode),
framing symbols will be added to both ends of the DLLP at this level before the packet is sent. In Gen3 mode, a SDP token of two bytes is
added to the front end of the DLLP, but no END is added to the end of the DLLP. Figure 9‐2 on page 310 shows a generic (Gen1/Gen2) DLLP in
transit, showing the framing symbols and the general contents of the packet.

_Figure 9‐2: Generic Data Link Layer Packet Format_ 

<img src="figures/chapter_07_Quality_of_Service/page/page0315.png" alt="Figure 8‐1: Example Producer/Consumer Topology" width="700">

</td>
<td width="50%">

事务排序在虚通道缓冲区中进行管理。这些缓冲区被分组为 Posted、Non-Posted 和 Completion 事务，并且每个组独立管理流控。这使得弱排序更有用，因为与我们的示例一样，即使一个缓冲区已满，其他缓冲区仍可能有可用空间。

## **基于 ID 的排序 (IDO)**

另一个优化排序和提升性能的机会与流量流的性质相关。不同 Requester 的报文很可能没有依赖关系；毕竟，一个设备几乎不可能知道另一个设备何时完成了某些步骤（基于排序），因为它们到达其共享资源可能有不同的路径。考虑到这一点，PCIe 规范的 2.1 版本引入了所谓的基于 ID
的排序 (ID-based Ordering) 以提升性能。

## **解决方案**

如果不考虑事务排序的报文源，则性能可能会受到影响，如第 302 页的图 8-7 所示。在该图中，事务 1 设法到达交换机的上游端口，但由于根端口中该报文类型的缓冲区已满（这将由流控信用不足指示）而无法进一步进展。使用规范术语，来自同一 Requester 的报文称为 TLP 流
(TLP stream)。在此示例中，事务 1 所示的路径可能包括作为 TLP 流一部分的几个 TLP。然后事务 2 到达同一出口端口，也被阻止向前移动，因为它必须与事务 1 保持顺序。由于报文来自不同的源（不同的 TLP
流），这种延迟几乎肯定是不必要的；它们之间很可能没有依赖关系，但普通的排序模型没有考虑到这一点。为了获得更好的性能，我们需要另一个选项。

解决方案很简单：如果报文不使用相同的 Requester ID（或完成报文的 Completer ID），则允许重排序报文。此可选功能允许软件启用设备以使用 IDO，并且交换机端口可以识别报文属于不同的 TLP 流。这是通过在 Device Control 2 Register
中设置启用位来完成的。

**PCI Exress 3.0 Technology**

_图 8-7：不同来源不太可能有依赖关系_

**==> 图片 [151 x 145] 已省略 <==**

**----- 图片文字开始 -----**<br>
Write Buffer Root<br>Full<br>ey<br>Switch<br>ty a ONO<br>®<br>Posted Write<br>| [7] [le ma"<br>sd Cle fl PCle ff Legacy<br>**----- 图片文字结束
-----**<br>


## **何时使用 IDO**

规范强烈建议只要安全可行，就同时使用 IDO 和 RO。例如，当端点仅与一个其他实体（例如根复合体）直接通信时，对所有 TLP 使用 IDO 应该是安全的。另一方面，如果端点正在与多个代理通信，则使用它就不安全了。规范中此失败情况的一个示例开始于一个设备执行对内存的 DMA
写，然后执行对另一设备中标志 (flag) 的对等 (peer-to-peer) 写。当第二个设备收到标志时，它也会启动对同一内存区域的 DMA 写。通常，两个 DMA 操作会保持顺序，但使用 IDO 时，由于上游设备将它们视为来自不同的设备 ID，因此无法保证该排序。类似地，将
RO 用于涉及控制流量的报文也是不安全的。

对于 Completer，如果启用了 IDO，则建议将其用于所有 Completions，除非有特定原因不这样做。

**第 8 章：事务排序**

## **软件控制**

软件可以通过在端口的 Device Control 2 Register 中设置适当的位来启用 IDO 用于来自给定端口的请求或完成。与 RO 一样，没有能力位 (capability bits)
让软件查明设备支持什么，只有启用位，因此软件需要通过其他方式知道设备能够执行此操作。这些位启用了该报文类型对 IDO 的使用，但软件仍必须决定每个单独的报文是否会设置其 IDO 位。头部中的新属性位指示 TLP 是否正在使用 IDO，如第 303 页的图 8-8
所示。这引出了另一个相关的点：Completions 通常会继承生成它们的 Request 的所有属性位，但对于 IDO 来说情况可能并非如此，因为这可以由 Completer 独立启用。换句话说，Completions 可能会使用 IDO，即使发起它们的 Request
没有使用。

_图 8-8：64 位头部中的 IDO 属性_

**==> 图片 [313 x 127] 已省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr
AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- 图片文字结束
-----**<br>


## **死锁避免**

由于 PCI 总线使用延迟事务，或者由于 PCI Express 内存读请求可能因流控信用不足而被阻塞，可能会出现多种死锁场景。这些死锁避免规则包含在 PCI Express 排序中，以确保无论拓扑如何都不会发生死锁。遵守排序规则可以防止由于意外拓扑（例如跨 PCI
Express 交换网络连接的两个 PCI Express 到 PCI 桥）而出现的边界条件问题。请参考 MindShare 出版的标题为《_PCI System Architecture, Fourth Edition_》（由 Addison-Wesley 出版）的书，获取构成
PCI Express 死锁避免相关排序规则基础的场景的详细说明

## **PCI Exress 3.0 Technology**

排序规则。表 8-1（第 289 页）列出了死锁避免排序规则，这些规则被标识为 A3、A4、D3、D4 和 A5b 条目。请注意，避免死锁涉及这 5 种情况中的每一种的"Yes"条目。如果由于与第 3 列或第 4 列中标识的 Non-Posted
请求缓冲区相关的流控信用不足而发生阻塞，则与行 A 关联的 Posted 请求或与行 D 关联的 Completions 必须移到第 3 列或第 4 列中指定存在"Yes"条目的 Non-Posted 请求之前。另请注意，A5b 中的"Yes"条目仅适用于 PCI Express
到 PCI 或 PCI-X 桥。

基本上，此死锁避免规则可以总结为"必须允许后到达的内存写请求或完成通过先前被阻塞的 Non-Posted 请求，否则可能导致死锁"。

## 第三部分：

数据链路层

## _**9**_

## _**DLLP 元素**_

## **上一章**

上一章讨论了 PCI Express 拓扑中事务的排序要求。这些规则是从 PCI 继承而来的，生产者/消费者编程模型激发了其中的许多规则，因此此处描述了其机制。原始规则还考虑了必须避免的可能死锁条件，但不包括避免可能导致的性能问题的任何手段。

## **本章**

在本章中，我们描述另一类主要的数据包——数据链路层包 (Data Link Layer Packets, DLLP)。我们描述 DLLP 报文类型的使用、格式和定义以及其相关字段的详细信息。DLLP 用于支持 Ack/Nak
协议、电源管理、流控机制，甚至可以用于供应商自定义目的。

## **下一章**

下一章描述数据链路层的一个关键特性：一种基于硬件的自动机制，用于确保 TLP 跨链路的可靠传输。Ack DLLP 确认 TLP 的良好接收，而 Nak DLLP 指示传输错误。我们将描述在未检测到 TLP 或 DLLP 错误时的正常操作规则，以及与 TLP 和 DLLP
错误相关联的错误恢复机制。

## **概述**

数据链路层可以被认为管理着较低级别的链路协议。它的主要职责是确保在设备之间移动的 TLP 的完整性，但它也参与 TLP 流控、链路初始化和电源管理，并在其上方的传输层和下方的物理层之间传递信息。

在执行这些工作时，数据链路层与被称为数据链路层包 (Data Link Layer Packets, DLLP) 的邻居交换包。DLLP 在每个设备的数据链路层之间进行通信。第 308 页的图 9-1 说明了设备之间交换的 DLLP。

_图 9-1：数据链路层发送 DLLP_

**==> 图片 [342 x 298] 已省略 <==**

**----- 图片文字开始 -----**<br>
PCIe Device A PCIe Device B<br>
Device Core Device Core<br>
PCIe Core PCIe Core<br>
Hardware/Software Hardware/Software<br>
Interface Interface<br>
Transaction Layer Transaction Layer<br>
Data Link Layer Data Link Layer<br>
Physical Layer Physical Layer<br>
(RX) (TX) (RX) (TX)<br>
Framing C Framing<br>
DLLP R<br>
(SDP) C (END)<br>
**----- 图片文字结束 -----**<br>


## **DLLP 是本地流量**

DLLP 具有简单的报文格式，固定大小为 8 字节，包括成帧字节。与 TLP 不同，它们不携带目标或路由信息，因为它们仅用于最近邻通信，根本不被路由。事务层也看不到它们，因为它们不属于在该层交换的信息。

**第 9 章：DLLP 元素**

## **DLLP 的接收方处理**

收到 DLLP 时，有几条规则适用：

1. 它们在接收方立即被处理。换句话说，它们的流不能像 TLP 那样被控制（DLLP 不受流控影响）。

2. 检查它们是否有错误；首先在物理层，然后是数据链路层。通过计算 CRC 应该是什么并将其与接收到的值进行比较来检查随包附带的 16 位 CRC。未能通过此检查的 DLLP 将被丢弃。链路将如何从此错误中恢复？DLLP 仍会定期到达，该类型的下一个成功的 DLLP
将更新丢失的信息。

3. 与 TLP 不同，DLLP 没有确认协议。相反，规范定义了超时机制以促进从失败的 DLLP 中恢复。

4. 如果没有错误，则确定 DLLP 类型并传递给适当的内部逻辑进行管理：

 - Ack/Nak 通知 TLP 状态

 - 流控通知可用缓冲区空间

 - 电源管理设置

 - 供应商特定信息

## **发送 DLLP**

## **概述**

这些报文源自数据链路层，并传递给物理层。如果使用 8b/10b 编码（Gen1 和 Gen2 模式），将在 DLLP 的两端添加成帧符号，然后再发送包。在 Gen3 模式下，两个字节的 SDP 标记被添加到 DLLP 的前端，但不添加 END 添加到 DLLP 的末尾。第 310
页的图 9-2 显示了一个传输中的通用（Gen1/Gen2）DLLP，显示了成帧符号和包的常规内容。

_图 9-2：通用数据链路层包格式_

**==> 图片 [360 x 313] 已省略 <==**

**----- 图片文字开始 -----**<br>
Device A Device B<br>
Device Core Device Core<br>
PCI-XP Core PCI-XP Core<br>
Hardware/Software Hardware/Software<br>
Interface Interface<br>
Transaction Layer Transaction Layer<br>
Data Link Layer Data Link Layer<br>
Physical Layer Physical Layer<br>
(RX) (TX) (RX) (TX)<br>
Framing C Framing<br>
DLLP R<br>
(SDP) C (END)<br>
+0 +1 +2 +3<br>
7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>
Byte 0 DLLP Type (Fields Vary With DLLP Type)<br>
Byte 4 16 Bit CRC<br>
**----- 图片文字结束 -----**<br>

</td>
</tr></tbody></table>

[⬆️ 返回目录](#本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
