- A PCI Express endpoint is included to describe Switch behavior during lock. 

In this example, the locked operation completes normally. The steps that occur during the operation are described in the two sections that follow. 

## **The Memory Read Lock Operation** 

Figure E‐1 on page 967 illustrates the first step in the Locked transaction series (i.e., the initial memory read to obtain the semaphore): 

1. The CPU initiates the locked sequence (a Locked Memory Read) as a result of a driver executing a locked RMW instruction that targets a PCI target. 

2. The Root Port issues a Memory Read Lock Request from port 2. The Root Complex is always the source of a locked sequence. 

3. The Switch receives the lock request on its upstream port and forwards the request to the target egress port (3). The switch, upon forwarding the request to the egress port, must block all requests from ports other than the ingress port (1) from being sent from the egress port. 

4. A subsequent peer‐to‐peer transfer from the illustrated PCI Express end‐ point to the PCI bus (switch port 2 to switch port 3) would be blocked until the lock is cleared. Note that the lock is not yet established in the other direction. Transactions from the PCI Express endpoint could be sent to the Root Complex. 

**965** 

## **PCI Express Technology** 

5. The Memory Read Lock Request is sent from the Switch’s egress port to the PCI Express‐to‐PCI Bridge. This bridge will implement PCI lock semantics (See the MindShare book entitled _PCI System Architecture, Fourth Edition_ , for details regarding PCI lock). 

6. The bridge performs the Memory Read transaction on the PCI bus with the PCI LOCK# signal asserted. The target memory device returns the requested semaphore data to the bridge. 

7. Read data is returned to the Bridge and is delivered back to the Switch via a Memory Read Lock Completion with Data (CplDLk). 

8. The switch uses ID routing to return the packet upstream towards the host processor. When the CplDLk packet is forwarded to the upstream port of the Switch, it establishes a lock in the upstream direction to prevent traffic from other ports from being routed upstream. The PCI Express endpoint is completely blocked from sending any transaction to the Switch ports via the path of the locked operation. Note that transfers between Switch ports not involved in the locked operation would be permitted (not shown in this example). 

9. Upon detecting the CplDLk packet, the Root Complex knows that the lock has been established along the path between it and the target device, and the completion data is sent to the CPU. 

**966** 

**A endix D pp** 

_Figure D‐1: Lock Sequence Begins with Memory Read Lock Request_ 

**==> picture [368 x 388] intentionally omitted <==**

**----- Start of picture text -----**<br>
The CPU executes<br>the PCI target's device 1 CPU<br>drive that uses lock<br>Root Complex<br>Root Complex issues Root Complex receives<br>the MRdLk Request 2 9 CplDLk and returns data<br>to CPU<br>Switch forwards the Completion<br>Switch receives MRdLk and  1 to the upstream port (ID routing)<br>forwards it to the egress port (3). 3 8 and locks upstream port (1)<br>Switch blocks transactions from<br>Switch<br>other ports to egress port.<br>2 3<br>Bridge returns data using<br>PCIe endpoint issues a MenRd 4 a CplDLk transaction<br>Request targeting a PCI device,<br>7<br>but request is blocked 5<br>PCIe PCIe<br>Endpoint to<br>PCI Bridge<br>The Bridge receives the MRdLk.<br>Bridges support lock based on the<br>PCI-based requirements<br>6<br>Target The Bridge asserts LOCK and<br>Device performs the PCI Rd transaction<br>and the target returns the read data<br>MRdLk CplDLk<br>**----- End of picture text -----**<br>


## **Read Data Modified and Written to Target and Lock Completes** 

The device driver receives the semaphore value, alters it, and then initiates a memory write to update the semaphore within the memory of the legacy PCI device. Figure E‐2 on page 969 illustrates the write sequence followed by the 

**967** 

**PCI Express Technology** 

Root Complex’s transmission of the Unlock message that releases the lock: 

10. The Root Complex issues the Memory Write Request across the locked path to the target device. 

11. The Switch forwards the transaction to the target egress port (3). The mem‐ ory address of the Memory Write must be the same as the initial Memory Read request. 

12. The bridge forwards the transaction to the PCI bus. 

13. The target device receives the memory write data. 

14. Once the Memory Write transaction is sent from the Root Complex, it sends an Unlock message to instruct the Switches and any PCI/PCI‐X bridges in the locked path to release the lock. Note that the Root Complex presumes the operation has completed normally (because memory writes are posted and no Completion is returned to verify success). 

15. The Switch receives the Unlock message, unlocks its ports and forwards the message to the egress port that was locked to notify any other Switches and/ or bridges in the locked path that the lock must be cleared. 

16. Upon detecting the Unlock message, the bridge must also release the lock on the PCI bus. 

**968** 

**A endix D pp** 

_Figure D‐2: Lock Completes with Memory Write Followed by Unlock Message_ 

**==> picture [369 x 414] intentionally omitted <==**

**----- Start of picture text -----**<br>
The CPU executes<br>the PCI target's device CPU<br>drive that uses lock<br>Root Complex<br>Root Complex issues Root Complex sends<br>the Mem Write Request 10 14 Unlock message<br>1<br>Switch receives MemWt and  Switch receives the Unlock<br>forwards it to the egress port (3) 11 15 message and unlocks the<br>Switch ports in the locked path<br>2 3<br>Bridge releases lock<br>due to Unlock message<br>16<br>PCIe PCIe<br>12<br>Endpoint to<br>PCI Bridge<br>The Bridge receives the MemWt<br>performs the equivalent PCI<br>transaction<br>13<br>Target Target device receives the<br>Device PCI write data thereby<br>completing the operation<br>MemWt Unlock message<br>**----- End of picture text -----**<br>


**969** 

**PCI Express Technology** 

## **Notification of an Unsuccessful Lock** 

A locked transaction series is aborted when the initial Memory Read Lock Request receives a Completion packet with no data (CplLk). This means that the locked sequence must terminate because no data was returned. This could result from an error associated with the memory read transaction, or perhaps the target device is busy and cannot respond at this time. 

## **Summary of Locking Rules** 

Following is a list of ordering rules that apply to the Root Complex, Switches, and Bridges. 

## **Rules Related To the Initiation and Propagation of Locked Transactions** 

- Locked Requests which are completed with a status other than Successful Completion do not establish lock. 

- Regardless of the status of any of the Completions associated with a locked sequence, all locked sequences and attempted locked sequences must be terminated by the transmission of an Unlock Message. 

- MRdLk, CplDLk and Unlock semantics are allowed only for the default Traffic Class (TC0). 

- Only one locked transaction sequence attempt may be in progress at a given time within a single hierarchy domain. 

- Any device which is not involved in the locked sequence must ignore the Unlock Message. 

The initiation and propagation of a locked transaction sequence through the PCI Express fabric is performed as follows: 

- A locked transaction sequence is started with a MRdLk Request: 

   - Any successive reads associated with the locked transaction sequence must also use MRdLk Requests. 

   - The Completions for any successful MRdLk Request use the CplDLk Completion type, or the CPlLk Completion type for unsuccessful Requests. 

**970** 

**A endix D pp** 

- If any read associated with a locked sequence is completed unsuccessfully, the Requester must assume that the atomicity of the lock is no longer assured, and that the path between the Requester and Completer is no longer locked. 

- All writes associated with a locked sequence must use MWr Requests. 

- The Unlock Message is used to indicate the end of a locked sequence. A Switch propagates Unlock Messages through the locked Egress Port. 

- Upon receiving an Unlock Message, a legacy Endpoint or Bridge must unlock itself if it is in a locked state. If it is not locked, or if the Receiver is a PCI Express Endpoint or Bridge which does not support lock, the Unlock Message is ignored and discarded. 

## **Rules Related to Switches** 

Switches must detect transactions associated with locked sequences from other transactions to prevent other transactions from interfering with the lock and potentially causing deadlock. The following rules cover how this is done. Note that locked accesses are limited to TC0, which is always mapped to VC0. 

- When a Switch propagates a MRdLk Request from an Ingress Port to the Egress Port, it must block all Requests which map to the default Virtual Channel (VC0) from being propagated to the Egress Port. If a subsequent MRdLk Request is received at this Ingress Port addressing a different Egress Port, the behavior of the Switch is undefined. Note that this sort of split‐lock access is not supported by PCI Express and software must not cause such a locked access. System deadlock may result from such accesses. 

- When the CplDLk for the first MRdLk Request is returned, if the Comple‐ tion indicates a Successful Completion status, the Switch must block all Requests from all other Ports from being propagated to either of the Ports involved in the locked access, except for Requests which map to channels other than VC0 on the Egress Port. 

- The two Ports involved in the locked sequence must remain blocked until the Switch receives the Unlock Message (at the Ingress Port which received the initial MRdLk Request) 

   - The Unlock Message must be forwarded to the locked Egress Port. 

   - The Unlock Message may be broadcast to all other Ports. 

   - The Ingress Port is unblocked once the Unlock Message arrives, and the Egress Port(s) which were blocked are unblocked following the trans‐ mission of the Unlock Message out of the Egress Port(s). Ports that were not involved in the locked access are unaffected by the Unlock Message 

**971** 

**PCI Express Technology** 

## **Rules Related To PCI Express/PCI Bridges** 

The requirements for PCI Express/PCI Bridges are similar to those for Switches, except that, because these Bridges only use TC0 and VC0, all other traffic is blocked during the locked access. Requirements on the PCI bus side are described in the MindShare book, _PCI System Architecture, Fourth Edition._ 

## **Rules Related To the Root Complex** 

A Root Complex is permitted to support locked transactions as a Requester. If locked transactions are supported, a Root Complex must follow the rules already described to perform a locked access. The mechanism(s) used by the Root Complex to interface to the host processor’s FSB (Front‐Side Bus) are out‐ side the scope of the spec. 

## **Rules Related To Legacy Endpoints** 

Legacy Endpoints are permitted to support locked accesses, although their use is discouraged. If locked accesses are supported, legacy Endpoints must handle them as follows: 

- The legacy Endpoint becomes locked when it transmits the first Completion for the first read request of the locked transaction series access with a Suc‐ cessful Completion status: 

   - If the completion status is not Successful Completion, the legacy End‐ point does not become locked. 

   - Once locked, the legacy Endpoint must remain locked until it receives the Unlock Message. 
