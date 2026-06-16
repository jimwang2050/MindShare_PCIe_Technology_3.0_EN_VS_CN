# 📘 第 7 章　服务质量 (Chapter 7. Quality of Service)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0254.md` ... `chunks/chunk0256.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Quality of Service](#-本章目录-table-of-contents)

<a id="sec-7-1"></a>
## 7.1 Quality of Service | 服务质量

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

There are three general models for ordering transactions in a traffic flow: 

1. **Strong Ordering** : PCI Express requires strong ordering of transactions flowing through the fabric that have the same Traffic Class (TC) assignment. Transactions that have the same TC value assigned to them are mapped to a given VC, therefore the same rules apply to transactions within each VC. Consequently, when multiple TCs are assigned to the same VC all transac‐ tions are typically handled as a single TC, even though no ordering rela‐ tionship exists between different TCs. 

2. **Weak Ordering** : Transactions stay in sequence unless reordering would be helpful. Maintaining the strong ordering relationship between transactions can result in all transactions being blocked due to dependencies associated with a given transaction model (e.g., The Producer/Consumer Model). Some of the blocked transactions very likely are not related to the depen‐ dencies and can safely be reordered ahead of blocking transactions. 

3. **Relaxed Ordering** : Transactions can be reordered, but only under certain controlled conditions. The benefit is improved performance like the weak‐ ordered model, but only when specified by software so as to avoid prob‐ lems with dependencies. The drawback is that only some transactions will be optimized for performance. There is some overhead for software to enable transactions for Relaxed Ordering (RO). 

**286** 

**Chapter 8: Transaction Ordering** 

## **Simplified Ordering Rules** 

The 2.1 revision of the spec introduced a simplified version of the Ordering Table as shown in Table 8‐1 on page 289. The table can be segmented on a per topic basis as follows: 

- Producer/Consumer rules (page 290) 

- Relaxed Ordering rules (page 296) 

- Weak Ordering rules (page 299) 

- ID Ordering rules (page 301) 

- Deadlock avoidance (page 303) 

These sections provide details associated with the ordering models, operation, rationales, conditions and requirement. 

## **Ordering Rules and Traffic Classes (TCs)** 

PCI Express ordering rules apply to transactions of the same Traffic Class (TC). Transactions moving through the fabric that have different TCs have no order‐ ing requirement and are considered to be associated with unrelated applica‐ tions. As a result, there is no transaction ordering related performance degradation associated with packets of different TCs. 

Packets that do share the same TC may experience performance degradation as they flow through the PCIe fabric. This is because switches and devices must support ordering rules that may require packets to be delayed or forwarded in front of packets previously sent. 

As discussed in Chapter 7, entitled ʺQuality of Service,ʺ on page 245, transac‐ tions of different TC may map to the same VC. The TC‐to‐VC mapping configu‐ ration determines which packets of a given TC map to a specific VC. Even though the transaction ordering rules apply only to packets of the same TC, it may be simpler to design endpoint devices/switches/root complexes that apply the transaction ordering rules to all packets within a VC even though multiple TCs are mapped to the same VC. 

As one would expect, there are no ordering relationships between packets that map to different VCs no matter their TC. 

**287** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Ordering Rules Based On Packet Type** 

Ordering relationships defined by the PCIe spec are based on TLP type. TLPs are divided into three categories: 1) Posted, 2) Completion and 3) Non‐Posted TLPs. 

The Posted category of TLPs include memory write requests (MWr) and Mes‐ sages (Msg/MsgD). Completion category of TLPs include Cpl and CplD. Non‐ Posted category of TLPs include MRd, IORd, IOWr, CfgRd0, CfgRd1, CfgWr0 and CfgWr1. 

The transaction ordering rules are described by a table in the following section “The Simplified Ordering Rules Table” on page 288. As you will notice, the table shows TLPs listed according to the three categories mentioned above with their ordering relationships defined. 

## **The Simplified Ordering Rules Table** 

The table is organized in a Row Pass Column fashion. All of the rules are sum‐ marized following the Simplified Ordering Table. Each rule or group of rules define the actions that are required. 

In Table 8‐1 on page 289, columns 2 ‐ 5 represent transactions that have previ‐ ously been delivered by a PCI Express device, while row A ‐ D represents a new transaction that has just arrived. For outbound transactions, the table specifies whether a transaction represented in the row (A ‐ D) is allowed to pass a previ‐ ous transaction represented by the column (2 ‐ 5). A ‘No’ entry means the trans‐ action in the row is not allowed to pass the transaction in the column. A ‘Yes’ entry means the transaction in the row must be allowed to pass the transaction in the column to avoid a deadlock. A ‘Yes/No’ entry means a transaction in a row is allowed to pass the transaction in the column but is not required to do so. The entries in the following have the meaning. 

**288** 

**Chapter 8: Transaction Ordering** 

_Table 8‐1: Simplified Ordering Rules Table_ 

|**Row pass**<br>**Column?**<br>(Col 1)|**Row pass**<br>**Column?**<br>(Col 1)|**Posted**<br>**Request**<br>(Col 2)|**Non-Posted Request**|**Non-Posted Request**|**Completion**<br>(Col 5)|
|---|---|---|---|---|---|
||||**Read**<br>**Request**<br>(Col 3)|**NPR with**<br>**Data**<br>(Col 4)||
|**Posted**<br>**Request**<br>(Row A)||a) No<br>b) Y/N|Yes|Yes|a) Y/N<br>b) Yes|
|**Non-Posted**<br>**Request**|**Read**<br>**Request**<br>(Row B)|a) No<br>b) Y/N|Y/N|Y/N|Y/N|
||**NPR with**<br>**Data**<br>(Row C)|a) No<br>b) Y/N|Y/N|Y/N|Y/N|
|**Completion**<br>(Row D)||a) No<br>b) Y/N|Yes|Yes|a) Y/N<br>b) No|



- **A2a, B2a, C2a, D2a** — to enforce the Producer/Consumer model, a subse‐ quent transaction is not allowed to pass a Posted Request. 

- **A2, D2b** —If RO is set, then a Read Completion is permitted to pass a previ‐ ously queued Memory Write or Message Request. 

- **A2b, B2b, C2b, D2b** — if the optional IDO is being used, a subsequent transaction is allowed to pass a Posted Request, as long as their Requester IDs are different 

- **A3, A4** — A Memory Write or Message Request must be allowed to pass Non‐Posted Requests to avoid deadlocks. 

- **A5a** — Posted Request is permitted but not required to pass Completions 

- **A5b** — Deadlock avoidance case. In a PCIe‐to‐PCI/PCI‐X bridge, for trans‐ actions going from PCIe to PCI or PCI‐X, a Posted Request must be able to pass a Completion, or a deadlock may occur. 

- **B3, B4, B5, C3, C4, C5,** — These cases implement weak ordering without risking any ordering related problems. 

- **D3, D4** — Completions must be allowed to pass Read and I/O or Configura‐ tion Write Requests (Non‐Posted Requests) to avoid deadlocks. 

- **D5a** — Completions with different Transaction IDs may pass each other. 

- **D5b** — Completions with the same Transaction ID are not allowed to pass each other. This ensures that multiple completions for a single request will remain in ascending address order. 

**289** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Producer/Consumer Model** 

This section describes the operation of the Producer/Consumer model and the associated ordering rules required for proper operation. Figure 8‐1 on page 291 simply illustrates a sample topology. Subsequent examples of this topology describe the operation of the Producer/Consumer model with proper ordering, followed by an example of the model failing due to improper ordering. 

The Producer/Consumer model is the common method for data delivery in PCI and PCIe. The model comprises five elements as depicted in Figure 8‐1: 

- Producer of data 

- Memory data buffer 

- Flag semaphore indicating data has been send by the Producer 

- Consumer of data 

- Status semaphore indicating Consumer has read data 

The specification states that the Producer/Consumer model will work regard‐ less of the arrangement of all the elements involved. In this example, the Flag and Status elements reside in the same physical device, but could be located in different devices. 

**290** 

**Chapter 8: Transaction Ordering** 

_Figure 8‐1: Example Producer/Consumer Topology_ 

**==> picture [346 x 348] intentionally omitted <==**

**----- Start of picture text -----**<br>
Consumer<br>(Processor)<br>P<br>Root Complex NP<br>CPL<br>P Memory<br>NP<br>CPL<br>P Posted<br>NP Non-Posted<br>PCIe Switch CPL Completion<br>Flag<br>Producer<br>Status<br>P<br>NP<br>CPL<br>P<br>NP<br>CPL<br>CPL<br>NP<br>P<br>CPL<br>NP<br>P<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>**----- End of picture text -----**<br>


## **Producer/Consumer Sequence — No Errors** 

Refer to Figure 8‐2 on page 293 during the following discussion. The example presumes that the Flag and Status element are cleared to start with. These sema‐ phores are included within the same device in this example. The sequence of numbered events in the description below and depicted in Figure 8‐2 on page 293 reflect the correct ordering in this Part 1 sequence. 

**291** 

## **PCI Ex ress 3.0 Technolo p gy** 

1. In the example, a device called the **Producer** performs one or more Memory Write transactions (Posted Requests) targeting a **Data Buffer** in memory. Some delay can occur as the data flows through Posted buffers. 

2. The Consumer periodically checks the Flag by initiating a Memory Read transaction (Non‐Posted Request) to determine if data has been delivered by the Producer. 

3. The Flag semaphore is read by the device and a Memory Read Completion is returned to the Consumer, indicating that notification of data delivery has not been performed by the Producer (Flag = 0) yet. 

4. The Producer sends a Memory Write Transaction (Posted Request) to update the Flag to 1. 

5. Once again, the Consumer checks the Flag by performing the same transac‐ tion performed in step 2. 

6. When Flag semaphore is read this time, the Flag is set to 1, indicating to the Consumer, via the Completion, that all of the data has been delivered by the Producer to memory. 

7. Next, the Consumer performs a Memory Write transaction (Posted Request) to clear the Flag semaphore back to zero. 

Figure 8‐3 on page 294 continues the example in this Part 2 sequence. 

8. The Producer, having more data to send, periodically checks the Status semaphore by initiating a Memory Read transaction (Non‐Posted Request). 

9. The Status semaphore is read by the Producer and a Memory Read Comple‐ tion is returned to the Producer, indicating that the Consumer has not read the memory buffer contents and updated Status (Status = 0). 

10. The Consumer, knowing that the memory buffer has data available, per‐ forms one or more Memory Read Requests (Non‐Posted Requests) to get the contents from the buffer. 

11. Memory contents are read and returned to the Consumer. 

12. Upon completing the data transfer, the Consumer initiates a Memory Write Request (Posted Request) to set the Status semaphore to a 1. 

13. Once again, the Producer checks the Status semaphore by delivering a Memory Read Request (Non‐Posted Request). 

14. The device reads the Status and this time it is set to 1. The Completion is returned to the Producer, thereby indicating data can be sent to Memory. 

15. The Producer sends a Memory Write to Clear the Status semaphore to 0. 

16. The sequence of events starting with step 1. is repeated by the Producer. 

**292** 

**Chapter 8: Transaction Ordering** 

_Figure 8‐2: Producer/Consumer Sequence Example — Part 1_ 

**==> picture [353 x 389] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-7-2"></a>
## 7.2 Quality of Service | 服务质量

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Consumer<br>(Processor)<br>2 3<br>7<br>5 6<br>Root Complex P Memory<br>NP<br>CPL<br>P<br>NP<br>CPL<br>P Posted Request<br>1 NP Non-Posted Request<br>CPL Completion<br>4<br>7 5<br>1 4 4 2 3 6<br>Producer  Flag 0    1<br>Status 0<br>P<br>NP<br>CPL<br>P<br>NP<br>CPL<br>CPL<br>NP<br>P<br>CPL<br>NP<br>P<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>**----- End of picture text -----**<br>


**293** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 8‐3: Producer/Consumer Sequence Example — Part 2_ 

**==> picture [367 x 424] intentionally omitted <==**

**----- Start of picture text -----**<br>
Consumer<br>(Processor)<br>12 10<br>Root Complex P Memory<br>NP 11<br>CPL<br>P<br>NP<br>CPL<br>P Posted Request<br>NP Non-Posted Request<br>CPL Completion<br>13 13 14<br>14 15<br>8 15 8 9<br>Producer Flag 0    1<br>Status 0     1<br>P<br>NP<br>CPL<br>P<br>NP<br>CPL<br>CPL<br>NP<br>P<br>CPL<br>NP<br>P<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>**----- End of picture text -----**<br>


**294** 

**Chapter 8: Transaction Ordering** 

## **Producer/Consumer Sequence — Errors** 

The previous example was handled correctly without a discussion of the order‐ ing rules; however it may have been apparent that race conditions can cause the Producer/Consumer sequence to fail. Figure 8‐4 on page 296 illustrates a simple sequence to demonstrate one of several problems that can arise without order‐ ing rules being enforced. Refer to Figure Figure 8‐4 on page 296 during the fol‐ lowing discussion. 

1. Producer performs a Memory Write request (Posted Request) to the mem‐ ory buffer. Let us assume that the memory write data is temporarily stuck in the Switch upstream port Posted Flow Control buffer. 

2. The Producer sends a Memory Write Transaction (Posted Request) to update the Flag to 1. 

3. The Consumer initiates a Memory Read Request (Non‐Posted Request) to check if the Flag has been set to 1. 

4. The contents of the Flag is returned to the Consumer via a Completion. 

5. Knowing that data has been delivered to memory, the Consumer performs a memory read request to fetch the data. However, the Consumer is unaware that the data is temporarily stuck in a Posted Flow Control buffer due to lack of flow control credits associated with the link between the upstream switch port and the Root Complex. Consequently, the Consumer receives old data when the Completion is returned to the Consumer. 

The problem is avoided with ordering rules supported by virtual PCI bridges within the topology. In this example, when the Consumer performed the Mem‐ ory Read transaction in steps 3 and 4, the Virtual PCI bridge at the upstream switch port should not allow the contents of the flag (Completion 4) to be for‐ warded ahead of the previously posted data. 

**295** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 8‐4: Producer/Consumer Sequence with Error_ 

**==> picture [341 x 360] intentionally omitted <==**

**----- Start of picture text -----**<br>
Consumer<br>(Processor)<br>3 5 4 6<br>Root Complex P Memory<br>NP<br>CPL<br>P<br>NP<br>CPL<br>Retries Slow Delivery of data<br>P Posted Request<br>1 NP Non-Posted Request<br>CPL Completion<br>2<br>1 2 2 3 4<br>Producer  Flag 0 1<br>Status 0<br>P<br>NP<br>CPL<br>P<br>NP<br>CPL<br>CPL<br>NP<br>P<br>CPL<br>NP<br>P<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL<br>P NP CPL P NP CPL P NP CPL P NP CPL<br>**----- End of picture text -----**<br>


## **Relaxed Ordering** 

PCI Express supports the Relaxed Ordering (RO) mechanism added for PCI‐X. RO allows switches in the path between the Requester and Completer to reor‐ der some transactions when doing so would improve performance. 

**296** 

**Chapter 8: Transaction Ordering** 

The ordering rules that support the Producer/Consumer model may result in transactions being blocked in cases when they’re unrelated to any Producer/ Consumer transaction sequence. To alleviate this problem, a transaction can have its RO attribute bit set, indicating that software verifies it to be unrelated to other transactions, and that allows it to be re‐ordered ahead of other transac‐ tions. For example, if a posted write is delayed because the target’s buffer space is unavailable, then all subsequent transactions must wait until that finally resolves and the write is delivered. If a subsequent transaction was known by software to be unrelated to previous ones and the RO bit was set to show that, then it could be allowed to go before the write without risking a problem. 

The RO bit (bit 5 of byte 2 of dword 0 in the TLP header as shown in Figure 8‐5 on page 297) may be used by the device if its device driver has enabled it to do so. Request packets are then allowed to use this attribute as directed by soft‐ ware when it requests that a packet be sent. When switches or the Root Com‐ plex see a packet with this attribute bit set, they have permission to reorder it although it’s not required that they should. 

_Figure 8‐5: Relaxed Ordering Bit in a 32‐bit Header_ 

**==> picture [322 x 97] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R Attr R HT DT EP Attr AT Length<br>Byte 4 Requester ID Tag Last DWBE 1st DWBE<br>Byte 8 Address [31:2] R<br>**----- End of picture text -----**<br>


## **RO Effects on Memory Writes and Messages** 

Switches and Root Complexes must observe the setting of the RO bit in transac‐ tions. Memory writes and Messages are both posted writes, both are received into the same Posted buffer, and both are subject to the same ordering require‐ ments. When the RO bit is set, switches handle these transactions as follows: 

- Switches are permitted to reorder memory write transactions just posted ahead of previously posted memory write transactions or message transac‐ tions. Similarly, message transactions just posted may be ordered ahead of 

**297** 

**PCI Ex ress 3.0 Technolo p gy** 

previously posted memory write or message transactions. Switches must also forward the RO bit unmodified. The RO bit is ignored by PCI‐X bridges, which always forward writes in order (there would be little pur‐ pose in allowing them to go out of order anyway; if one is blocked for some reason, the next will be blocked, too). Another difference is that message transactions had not been defined for PCI‐X, either. 

- The Root Complex is permitted to reorder posted write transactions (here it makes sense because the Root could write to different areas of memory so, if one area is busy it can write to a different one). Also, when receiving writes with RO set, the Root is permitted to write each byte to memory in any address order. 

## **RO Effects on Memory Read Transactions** 

All read transactions in PCI Express are handled as split transactions. When a device issues a memory read request with the RO bit set, the Completer returns the requested read data in a series of one or more split completion transactions, and uses the same RO setting as in the request. Switch behavior in this case is as follows: 

1. A switch that receives a memory read with RO forwards the request in the order received, and must not reorder it ahead of memory write transactions that were previously posted. That guarantees that all write transactions moving in the direction of the read request are pushed ahead of the read. This is part of the Producer/Consumer example shown earlier, and software may depend on this flushing action for proper operation. The RO bit must not be modified by the switch. 

2. When the Completer receives the memory read, it fetches the requested data and delivers one or more Completions that also have the RO bit set (its value is copied from the original request). 

3. A switch receiving the Completions is allowed to re‐order them ahead of previously posted memory writes moving in the direction of the Comple‐ tion. If the writes were blocked (for example, due to flow control), then the Completions will be allowed to go ahead of them. Relaxed ordering in this case improves read performance. Table 8‐2 summarizes the relaxed order‐ ing behavior allowed by switches. 

**298** 

**Chapter 8: Transaction Ordering** 

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

Temporary transaction blocking can occur when strong ordering rules are rigor‐ ously enforced. Modifications that don’t violate the Producer/Consumer pro‐ gramming model can eliminate some blocking conditions and improve link efficiency. Implementing the Weakly‐Ordered model can alleviate this problem. 

## **Transaction Ordering and Flow Control** 

The motivation behind splitting VC buffers of a given number into flow con‐ trolled sub‐buffers P, NP and CPL is because it simplifies processing of the transaction ordering rules once TLPs have been parsed or binned into their respective buffers. The transaction ordering processing logic then applies order‐ ing rules between these three sub‐buffers or to each sub‐buffer. 

Since TLPs are binned into their respective three sub‐buffers in order to process transaction ordering rules, it is necessary to define the flow control mechanism between each virtual channel sub‐buffer (P, NP, CPL) of neighboring ports at opposite ends of the Link. In fact, you may recall that there is an independent flow control mechanism between Header (Hdr) and Data (D) sub‐buffers of each sub‐buffer category (P, NP, CPL) of each virtual channel number. 

**299** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Transaction Stalls** 

Strong ordering can result in instances where all transactions are blocked due to a single full receive buffer. For example, the ordering requirements for the Pro‐ ducer/Consumer model cannot be changed, but ordering for transactions that aren’t part of that model can. To improve performance, let’s consider a weakly‐ ordered scheme; one that puts the minimal requirements on transaction order‐ ing. 

This example depicts transmit and receive buffers associated with the delivery of transactions in a single direction for a single VC. Recall that each of the trans‐ action types (Posted, Non‐Posted, and Completions) have independent flow control within the same VC. The numbers in the transmit buffers show the order in which these transactions were issued, and the non‐posted receive buffer is currently full. Consider the following sequence. 

1. Transaction 1 (memory read) is the next transaction to send, but there aren’t enough flow control credits so it must wait. 

2. Transaction 2 (posted memory write) is the next subsequent transaction. If strong ordering is enforced, a memory write must not pass a previously queued read transaction. 

3. This restriction applies to all subsequent transactions, too, with the result that they’re all stalled until the first one finishes. 

_Figure 8‐6: Strongly Ordered Example Results in Temporary Stall_ 

**==> picture [300 x 178] intentionally omitted <==**

**----- Start of picture text -----**<br>
Numbers indicate the<br>order of transactions<br>pending transfer<br>Posted<br>7 4 2<br>Non-Posted Non-Posted<br>5 1<br>Completions Completions<br>8 6 3<br>Tx Rx<br>Rx Tx<br>Posted<br>Full<br>**----- End of picture text -----**<br>


**300** 

**Chapter 8: Transaction Ordering** 

## **VC Buffers Offer an Advantage**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-7-3"></a>
## 7.3 Quality of Service | 服务质量

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Transaction ordering is managed within Virtual Channel buffers. These buffers are grouped into Posted, Non‐Posted, and Completion transactions, and flow control is managed independently for each group. That makes weak ordering more useful because, as in our example, even if one buffer was full, others could still have space available. 

## **ID Based Ordering (IDO)** 

Another opportunity for optimizing ordering and improving performance is related to the nature of traffic streams. Packets from different requesters are very unlikely to have dependencies; after all, one device could hardly know when the other had finished certain steps based on ordering because they could have different paths to their shared resource. Bearing this in mind, the 2.1 revi‐ sion of the PCIe spec introduced what is called ID‐based Ordering to improve performance. 

## **The Solution** 

If the packet source isn’t taken into account for transaction ordering then perfor‐ mance can suffer, as shown in Figure 8‐7 on page 302. In the illustration, trans‐ action 1 makes it way to the upstream port of the switch but is blocked from further progress by a buffer‐full condition for that packet type in the Root port (which would be indicated by insufficient Flow Control credits). To use the spec terminology, packets from the same Requester are called a TLP stream. In this example, the path shown for Transaction 1 might include several TLPs as part of a TLP stream. Transaction 2 then arrives at the same egress port and is also blocked from moving forward because it must stay in order with Transaction 1. Since the packets came from different sources, (different TLP streams) this delay is almost certainly unnecessary; it’s very unlikely they could have depen‐ dencies between them, but the normal ordering model doesn’t take this into account. To get improved performance, we need another option. 

The solution is simple: allow packets to be reordered if they don’t use the same Requester ID (or Completer ID, for Completion packets). This optional capabil‐ ity allows software to enable a device to use IDO and a switch port can recog‐ nize that the packets are part of different TLP streams. This is done by setting the enable bits in Device Control 2 Register. 

**301** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 8‐7: Different Sources are Unlikely to Have Dependencies_ 

**==> picture [151 x 145] intentionally omitted <==**

**----- Start of picture text -----**<br>
Write Buffer Root<br>Full<br>ey<br>Switch<br>ty a ONO<br>®<br>Posted Write<br>| [7] [le ma"<br>sd Cle fl PCle ff Legacy<br>**----- End of picture text -----**<br>


## **When to use IDO** 

The spec highly recommends that both IDO and RO be used whenever safely possible. For example, it should be safe for Endpoints to use IDO for all TLPs when communicating directly with only one other entity, such as the Root Com‐ plex. On the other hand, it would not be safe to use it if the Endpoint is commu‐ nicating with multiple agents. An example failure case for this from the spec begins with one device doing a DMA write to memory and then doing a peer‐ to‐peer write to a flag in another device. When the second device receives the flag, it also initiates a DMA write to the same area of memory. Normally, the two DMA operations would stay in order, but with IDO that ordering can’t be guaranteed because upstream devices will see them as coming from different device IDs. Similarly, it would not be safe to use RO with packets that are involved in control traffic. 

For Completers, if IDO is enabled it’s recommended that it be used for all Com‐ pletions unless there is a specific reason not to do so. 

**302** 

**Chapter 8: Transaction Ordering** 

## **Software Control** 

Software can enable the use of IDO for Requests or Completions from a given port by setting the appropriate bits in its Device Control 2 Register. As with RO, there are no capability bits to let software find out what the device supports, just enable bits, so software would need to know by some other means that the device was capable of doing this. These bits enable the use of IDO for that packet type, but software must still decide whether each individual packet will have its IDO bit set. A new attribute bit in the header indicates whether a TLP is using IDO, as shown in Figure 8‐8 on page 303. This brings up another related point: Completions normally inherit all the attribute bits of the Request that generated them, but this may not be true for IDO, since this can be enabled independently by the Completer. In other words, Completions may use IDO even if the Request that initiated them did not. 

_Figure 8‐8: IDO Attribute in 64‐bit Header_ 

**==> picture [313 x 127] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 0 x 1 Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] R<br>**----- End of picture text -----**<br>


## **Deadlock Avoidance** 

Because the PCI bus employs delayed transactions or because PCI Express memory read request may be blocked due to lack of flow control credits, several deadlock scenarios can develop. These deadlock avoidance rules are included in PCI Express ordering to ensure that no deadlocks occur regardless of topol‐ ogy. Adhering to the ordering rules prevent problems when boundary condi‐ tions develop due to unanticipated topologies (e.g., two PCI Express to PCI bridges connected across the PCI Express fabric). Refer to the MindShare book entitled _PCI System Architecture, Fourth Edition (_ published by Addison‐Wesley) for a detailed explanation of the scenarios that are the basis for the PCI Express 

**303** 

## **PCI Ex ress 3.0 Technolo p gy** 

ordering rules related to deadlock avoidance. Table 8‐1 on page 289 lists the deadlock avoidance ordering rules which are identified as entries A3, A4, D3, D4 and A5b. Note that avoiding the deadlocks involves “Yes” entries in each of these 5 cases. If blocking occurs due to lack of flow control credits associated with the Non‐Posted Request buffer identified in column 3 or 4, the Posted Requests associated with row A or the Completions associated with row D must be moved ahead of the Non‐Posted Requests specified in the column 3 or 4 where the “Yes” entry exists. Note also that the “Yes” entry in A5b applies only to PCI Express to PCI or PCI‐X Bridges. 

Essentially, this deadlock avoidance rule can be summarized as “later arriving Memory Write Requests or Completions must be allowed to pass earlier blocked Non‐Posted Requests otherwise a deadlock could result”. 

**304** 

## Part Three: 

Data Link Layer 

## _**9**_ 

## _**DLLP Elements**_ 

## **The Previous Chapter** 

The previous chapter discussed the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI, and the Producer/ Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible dead‐ lock conditions that must be avoided, but did not include any means to avoid the performance problems that could result. 

## **This Chapter** 

In this chapter we describe the other major category of packets, _Data Link Layer Packets_ (DLLPs). We describe the use, format, and definition of the DLLP packet types and the details of their related fields. DLLPs are used to support Ack/Nak protocol, power management, flow control mechanism and can even be used for vendor‐defined purposes. 

## **The Next Chapter** 

The following chapter describes a key feature of the Data Link Layer: an auto‐ matic, hardware‐based mechanism for ensuring reliable transport of TLPs across the Link. Ack DLLPs confirm good reception of TLPs while Nak DLLPs indicate a transmission error. We describe the normal rules of operation when no TLP or DLLP error is detected as well as error recovery mechanisms associ‐ ated with both TLP and DLLP errors. 

## **General** 

The Data Link Layer can be thought of as managing the lower level Link proto‐ col. Its primary responsibility is to assure the integrity of TLPs moving between devices, but it also plays a part in TLP flow control, Link initialization and power management, and conveys information between the Transaction Layer above it and the Physical Layer below it. 

**307** 

**PCI Ex ress Technolo p gy** 

In performing these jobs, the Data Link Layer exchanges packets with its neigh‐ bor known as Data Link Layer Packets (DLLPs). DLLPs are communicated between the Data Link Layers of each device. Figure 9‐1 on page 308 illustrates a DLLP exchanged between devices. 

_Figure 9‐1: Data Link Layer Sends A DLLP_ 

**==> picture [342 x 298] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCIe Device A PCIe Device B<br>Device Core Device Core<br>PCIe Core  PCIe Core<br>Hardware/Software Hardware/Software<br>Interface Interface<br>Transaction Layer Transaction Layer<br>Data Link Layer Data Link Layer<br>Physical Layer Physical Layer<br>(RX) (TX) (RX) (TX)<br>Framing C Framing<br>DLLP R<br>(SDP) C (END)<br>**----- End of picture text -----**<br>


## **DLLPs Are Local Traffic** 

DLLPs have a simple packet format and are a fixed size, 8 bytes total, including the framing bytes. Unlike TLPs, they carry no target or routing information because they are only used for nearest‐neighbor communications and don’t get routed at all. They’re also not seen by the Transaction Layer since they’re not part of the information exchanged at that level. 

**308** 

**Chapter 9: DLLP Elements** 

## **Receiver handling of DLLPs** 

When DLLPs are received, several rules apply: 

1. They’re immediately processed at the Receiver. In other words, their flow cannot be controlled the way it is for TLPs (DLLPs are not subject to flow control). 

2. They’re checked for errors; first at the Physical Layer, and then at the Data Link Layer. The 16‐bit CRC included with the packet is checked by calculat‐ ing what the CRC should be and comparing it to the received value. DLLPs that fail this check are discarded. How will the Link recover from this error? DLLPs still arrive periodically, and the next one of that type that succeeds will update the missing information. 

3. Unlike TLPs, there’s no acknowledgement protocol for DLLPs. Instead, the spec defines time‐out mechanisms to facilitate recovery from failed DLLPs. 

4. If there are no errors, the DLLP type is determined and passed to the appro‐ priate internal logic to manage: 

   - Ack/Nak notification of TLP status 

   - Flow Control notification of buffer space available 

   - Power Management settings 

   - Vendor specific information 

## **Sending DLLPs** 

## **General** 

These packets originate at the Data Link Layer and are passed to the Physical Layer. If 8b/10b encoding is in use (Gen1 and Gen2 mode), framing symbols will be added to both ends of the DLLP at this level before the packet is sent. In Gen3 mode, a SDP token of two bytes is added to the front end of the DLLP, but no END is added to the end of the DLLP. Figure 9‐2 on page 310 shows a generic (Gen1/Gen2) DLLP in transit, showing the framing symbols and the general contents of the packet. 

**309** 

**PCI Ex ress Technolo p gy** 

_Figure 9‐2: Generic Data Link Layer Packet Format_ 

**==> picture [360 x 313] intentionally omitted <==**

**----- Start of picture text -----**<br>

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
