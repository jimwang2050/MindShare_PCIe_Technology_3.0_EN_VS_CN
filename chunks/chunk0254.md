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