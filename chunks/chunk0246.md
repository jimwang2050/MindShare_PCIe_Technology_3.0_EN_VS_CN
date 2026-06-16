- **Credits Received counter (optional)** — tracks the total credits of all TLPs received into the Flow Control buffer. When flow control is functioning properly, the CREDITS_RECEIVED count should be equal to or less than the CREDIT_ALLOCATED count. If this test ever becomes false, a flow con‐ trol buffer overflow has occurred and an error is detected. The spec recom‐ mends that this optional mechanism be implemented and notes that a failure here will be considered a fatal error. 

_Figure 6‐9: Types and Format of Flow Control DLLPs_ 

**==> picture [374 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataFCHdrFC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>1000  Update Posted<br>1001  Update Non Posted<br>1010  Update Completion<br>**----- End of picture text -----**<br>


**229** 

**PCI Ex ress Technolo p gy** 

## **Flow Control Example** 

The following example describes the non‐posted header Flow Control buffer, and attempts to capture the nuances of the flow control implementation in sev‐ eral situations. The discussion of Flow Control is described with a series of basic stages as follows: 

**Stage One** — Immediately following initialization a transaction is transmitted and tracked to explain the basic operation of the counters and registers. 

**Stage Two** — The transmitter sends transactions faster than the receiver can process them and the buffer becomes full. 

**Stage Three** — When counters roll over to zero, the mechanism still works but there are a couple of issues to consider. 

**Stage Four** — The optional receiver error check for a buffer overflow. 

## **Stage 1 — Flow Control Following Initialization** 

Once flow control initialization has completed, the devices are ready for normal operation. The Flow Control buffer in our example is 2KB in size. We’re describ‐ ing the non‐posted header buffer, and each credit is 5 dwords in size or 20 bytes. That means 102d (66h) Flow Control units are available. Figure 6‐10 on page 231 illustrates the elements involved, including the values that would be in each counter and register following flow control initialization. 

When the transmitter is ready to send a TLP, it must first check Flow Control credits. Our example is simple because a non‐posted header is the only packet being sent and it always requires just one Flow Control credit, and we are also assuming that no data is included in the transaction. 

The header credit check is made using unsigned arithmetic (2’s complement), and must satisfy the following formula: 

**==> picture [193 x 13] intentionally omitted <==**

Substituting values from Figure 6‐10 yields: 

66 _h_ –  00 _h_ + 01 _h_  _mod_ 2[8]  2[8]  2 66 _h_ –01 _h mod_ 256  80 _h_ 

**230** 

**Chapter 6: Flow Control** 

_Figure 6‐10: Flow Control Elements Following Initialization_ 

**==> picture [376 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 00h CL = 66h<br>FC<br>Incr Check<br>Buffer<br>Link Packet optional incr<br>Control<br>incr CrRcv=00h CrAl=66h<br>(NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>CrAl = Credits Allocated<br>CC = Credits Consumed<br>CrRcv = Credits Received<br>CL = Credit Limit<br>PTLP = Pending TLP<br>**----- End of picture text -----**<br>


In this case, the current CREDITS_CONSUMED count (CC) is added to the PTLP credits required, to determine the CREDITS_REQUIRED (CR), and that gives 00h + 01h = 01h. The CREDITS_REQUIRED count is subtracted from the CREDIT_LIMIT count (CL) to determine whether or not sufficient credits are available. 

The following description incorporates a brief review of 2’s complement sub‐ traction. When performing subtraction using 2’s complement the number to be subtracted is complemented (1’s complement) and 1 is added (2’s complement). This value is then added to the number from which we wish to subtract. Any carry due to the addition is dropped. 

**231** 

**PCI Ex ress Technolo p gy** 

Credit Check: 

```
CL 01100110b (66h) - CR 00000001b (01h) = n
```

CR is converted to 2’s complement: 

`00000001b` (CR) `11111110b` (CR inverted) `11111110b +1 11111111b` (2’s complement) 

2’s complement added to CL: 

```
01100110 (CL)
11111111(2’s complement of CR)
01100101 = 65h (carry bit is dropped)
```

Is result <= 80h? Yes. If the subtraction result is equal to or less than half the max value, which is tracked with a modulo 256 counter (128), then we know there is sufficient space in the receiver buffer and this packet can be sent. The decision to use only half the counter value avoids a potential count alias problem. See “Stage 3 — Counters Roll Over” on page 234. 

_Figure 6‐11: Flow Control Elements After First TLP Sent_ 

**==> picture [370 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 01h CL = 66h FC<br>Incr Check Buffer<br>Link Packet optional incr<br>Control (NP Hdr)<br>incr CrRcv=01h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


**232** 

**Chapter 6: Flow Control** 

## **Stage 2 — Flow Control Buffer Fills Up** 

Assume now that the receiver has been unable to remove transactions from the Flow Control buffer for some time. Perhaps the device core logic was tempo‐ rarily busy and unable to process transactions. Eventually, the Flow Control buffer becomes completely full, as shown in Figure 6‐12 on page 234. If the transmitter wishes to send another TLP and checks the Flow Control credits: 

Credit Limit (CL)= 66h Credits Required (CR) = 67h 

## `CL 01100110` (66) 

`CR 10011001` (add 2’s complement of 67h) 

`11111111 = FFh<=80h` (not true; don’t send packet) 

This channel is blocked until an Update Flow Control DLLP is received with a new CREDIT_LIMIT value of 67h or greater. When the new valued is loaded into the CL register the transmitter credit check will pass the test and a TLP can be sent. 

- `CL 01100111` (67) 

- `CR 10011001` add 2’s complement of 67 

   - `00000000 = 00h<=80h` (true, send transaction 

**233** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐12: Flow Control Elements with Flow Control Buffer Filled_ 

**==> picture [376 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>CC = 66h CL = 66h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


## **Stage 3 — Counters Roll Over** 

Since the Credit Limit (CL) and Credits Required (CR) counts only increment upward, they eventually roll over back to zero. When CL rolls over and CR has not, the credit check (CL‐CR) results in a small CL value and a large CR value. However, what might appear to be a problem is not when using unsigned arith‐ metic. As described in the previous examples the results are handled correctly when performing 2’s complement subtraction. Figure 6‐13 on page 235 shows the CL and CR counts before and after CL rollover along with the 2’s comple‐ ment results. 

**234** 

**Chapter 6: Flow Control** 

## _Figure 6‐13: Flow Control Rollover Problem_ 

**==> picture [368 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Before CL Rollover After CL Rollover<br>FFh<br>NTS = FF8h (4088d)CL = F8h AS = FE8h (4072d)CR = F8h<br>Available<br>Credit Available<br>NTS<br>Credit is the<br>AS = FE8h (4072d)CR = E8h Rollover<br>sum of these<br>two parts<br>NTS = FF8h (4088d)CL = 08h<br>00h<br>Using 2's complement: Using 2's complement:<br>  CL 11111000 (F8h)   CL 00001000 (08h)<br>+ CR 00011000 (E8h 2’s complement) + CR 00001000 (F8h 2’s complement)<br>  =  00010000 (0Fh)   =  00010000 (0Fh)<br>**----- End of picture text -----**<br>


## **Stage 4 — FC Buffer Overflow Error Check** 

Although it’s optional to do so, the specification recommends implementation of the FC buffer overflow error checking mechanism. Figure 6‐14 on page 236 shows the elements associated with the overflow error check that include: 

- Credits Received (CR) counter 

- Credits Allocated (CA) counter 

- Error Check Logic 

This permits the receiver to track Flow Control credits in the same manner as the transmitter. If flow control is working correctly, the transmitter’s Credits Consumed count will never exceed its Credit Limit, and the receiver’s Credits Received count will never exceed its Credits Allocated count. 

**235** 

**PCI Ex ress Technolo p gy** 

An overflow condition is detected if the following formula evaluates true. Note that the field size is either 8 (headers) or 12 (data): 

**==> picture [161 x 12] intentionally omitted <==**

If it does evaluate true, then more credits have been sent to the FC buffer than were available and an overflow has occurred. Note that the 1.0a version of the specification defines the equation as  rather than > as shown above. That appears to be an error, because when CA = CR no overflow condition exists. 

_Figure 6‐14: Buffer Overflow Error Check_ 

**==> picture [350 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=67h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


**236** 

**Chapter 6: Flow Control** 

## **Flow Control Updates** 

The receiver must regularly update its neighboring device with Flow Control credits that become available when transactions are removed from the buffer. Figure 6‐15 on page 238 illustrates an example where the transmitter was previ‐ ously blocked from sending header transactions because the buffer was full. In the illustration, the receiver has just removed three headers from the Flow Con‐ trol buffer. More space is now available, but the neighboring device is unaware of this. As headers are removed from the buffer, the CREDITS_ALLOCATED count increments from 66h to 69h. This new count is reported to the CREDIT_LIMIT register of the neighboring device using a Flow Control update packet. Once the credit limit has been updated, transmission of additional TLPs can proceed. 

An interesting note here is that the update reports the actual value of the Cred‐ its Allocated register. It would have worked to report just the change in the reg‐ ister, as perhaps “+3 credits on NP Headers” for example, but that represents a potential problem. To understand the risk, consider what would happen if the DLLP containing that increment information was lost for some reason. There is no replay mechanism for DLLPs; if an error occurs the packet is simply dropped. In this case, the increment information would be lost without a means of recovering it. 

If, on the other hand, the actual value of the register is reported instead and the DLLP fails, the next DLLP that succeeds will get the counters back in synchroni‐ zation. In that case some time might be wasted if the transmitter is waiting on the FC credits before it can send the next TLP, but no information is lost. 

**237** 

**PCI Ex ress Technolo p gy** 

_Figure 6‐15: Flow Control Update Example_ 
