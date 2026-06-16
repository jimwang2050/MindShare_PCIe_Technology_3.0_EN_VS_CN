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
