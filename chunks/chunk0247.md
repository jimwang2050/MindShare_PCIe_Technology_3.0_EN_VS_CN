**==> picture [368 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=69h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


## **FC_Update DLLP Format and Content** 

Recall that Flow Control update packets, like the Flow Control initialization packets, contain two credit fields, one for header and one for data, as shown in Figure 6‐16 on page 239. The receiver’s credit values reported in the HdrFC and DataFC fields may have been updated many times or not at all since the last update packet was sent. 

**238** 

**Chapter 6: Flow Control** 

_Figure 6‐16: Update Flow Control Packet Format and Contents_ 

## **Flow Control Update Frequency** 

The specification defines a variety of rules and suggested implementations that govern when and how often Flow Control Update DLLPs should be sent. These are motivated by a desire to: 

- Notify the transmitting device as early as possible about new credits allo‐ cated, especially if any transactions were previously blocked. 

- Establish worst‐case latency between FC Packets. 

- Balance the requirements associated with flow control operation, such as: — the need to report credits often enough to prevent transaction blocking 

- — the desire to reduce the Link bandwidth needed for FC_Update DLLPs 

- — selecting the optimum buffer size 

   - selecting the maximum data payload size 

- Detect violations of the maximum latency between Flow Control packets. 

Flow Control updates are permitted only when the Link is in the active state (L0 or L0s). All other Link states represent more aggressive power management that have longer recovery latencies. 

## **Immediate Notification of Credits Allocated** 

When a Flow Control buffer is so full that maximum‐sized packets cannot be sent, the spec requires immediate delivery of a FC_Update DLLP when more space becomes available. Two cases exist: 

**239** 

## **PCI Ex ress Technolo p gy** 

- **Maximum Packet Size = 1 Credit.** When packet transmission is blocked due to a buffer full condition for non‐infinite NPH, NPD, PH, and CPLH buffer types, an UpdateFC packet must be scheduled for Transmission when one or more credits are made available (allocated) for that buffer type. 

- **Maximum Packet Size = Max_Payload_Size.** Flow Control buffer space may decrease to the extent that a maximum‐sized packet cannot be sent for non‐infinite PD and CPLD credit types. In this case, when one or more additional credits are allocated, an Update FCP must be scheduled for transmission. 

## **Maximum Latency Between Update Flow Control DLLPs** 

The transmission frequency of Update FCPs for each FC credit type (non‐infi‐ nite) must be scheduled for transmission at least once every 30 μs (‐0%/+50%). If the Extended Sync bit within the Control Link register is set, updates must be scheduled no later than every 120 μs (‐0%/+50%). Note that Update FCPs may be scheduled for transmission more frequently than is required. 

## **Calculating Update Frequency Based on Payload Size and Link Width** 

The specification offers a formula for calculating the frequency at which update packets need to be sent for maximum data payload sizes and Link widths. The formula, shown below, defines FC Update delivery intervals in symbol times. For reference, a symbol time is defined as the time it takes to deliver one sym‐ bol: 4ns for Gen1, 2ns for Gen2, 1ns for Gen3. Table 6‐3, Table 6‐4 and Table 6‐5 show the unadjusted FC Update values for each speed. 

--------------------------------------------------------------------------------------------------------------------------------------- _MaxPayloadSize_ + _TLPOverhead_   _UpdateFactor_ **-** + _InternalDelay LinkWidth_ • **MaxPayloadSize** = The value in the Max_Payload_Size field of the Device Control register 

- **TLPOverhead** = the constant value (28 symbols) representing the additional TLP components that consume Link bandwidth (TLP Prefix, Sequence Number, Packet Header, LCRC, Framing Symbols) 

- **UpdateFactor** = the number of maximum size TLPs sent during the interval between UpdateFC Packets received. This number is intended to balance Link bandwidth efficiency and receive buffer sizes – the value varies with Max_Payload_Size and Link width 

**240** 

**Chapter 6: Flow Control** 

- **LinkWidth** = The number of Lanes the Link is using 

- **InternalDelay** = a constant value of 19 symbol times that represents the internal processing delays for received TLPs and transmitted DLLPs 

The relationship defined by the formula shows that the frequency of update packet delivery decreases as the Linkwidth increases and suggests a timer that triggers scheduling of update packets. Note that this formula does not account for delays associated with the receiver or transmitter being in the L0s power management state. 

_Table 6‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|237<br>UF=1.4|128<br>UF=1.4|73<br>UF=1.4|67<br>UF=2.5|58<br>UF=3.0|48<br>UF=3.0|33<br>UF=3.0|
|256 Bytes|416<br>FC=1.4|217<br>FC=1.4|118<br>UF=1.4|107<br>UF=2.5|90<br>UF=3.0|72<br>UF=3.0|45<br>UF=3.0|
|512 Bytes|559<br>UF=1.0|289<br>UF=1.0|154<br>UF=1.0|86<br>UF=1.0|109<br>UF=2.0|86<br>UF=2.0|52<br>UF=2.0|
|1024 Bytes|1071<br>UF=1.0|545<br>UF=1.0|282<br>UF=1.0|150<br>UF=1.0|194<br>UF=2.0|150<br>UF=2.0|84<br>UF=2.0|
|2048 Bytes|2095<br>UF=1.0|1057<br>UF=1.0|538<br>UF=1.0|278<br>UF=1.0|365<br>UF=2.0|278<br>UF=2.0|148<br>UF=2.0|
|4096 Bytes|4143<br>UF=1.0|2081<br>UF=1.0|1050<br>UF=1.0|534<br>UF=1.0|706<br>UF=2.0|534<br>UF=2.0|276<br>UF=2.0|



_Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|288<br>UF=1.4|179<br>UF=1.4|124<br>UF=1.4|118<br>UF=2.5|109<br>UF=3.0|99<br>UF=3.0|84<br>UF=3.0|
|256 Bytes|467<br>FC=1.4|268<br>FC=1.4|169<br>UF=1.4|158<br>UF=2.5|141<br>UF=3.0|123<br>UF=3.0|96<br>UF=3.0|



**241** 

## **PCI Ex ress Technolo p gy** 

_Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|512 Bytes|610<br>UF=1.0|340<br>UF=1.0|205<br>UF=1.0|137<br>UF=1.0|160<br>UF=2.0|137<br>UF=2.0|103<br>UF=2.0|
|1024 Bytes|1122<br>UF=1.0|596<br>UF=1.0|333<br>UF=1.0|201<br>UF=1.0|245<br>UF=2.0|201<br>UF=2.0|135<br>UF=2.0|
|2048 Bytes|2146<br>UF=1.0|1108<br>UF=1.0|589<br>UF=1.0|329<br>UF=1.0|416<br>UF=2.0|329<br>UF=2.0|199<br>UF=2.0|
|4096 Bytes|4194<br>UF=1.0|2132<br>UF=1.0|1101<br>UF=1.0|585<br>UF=1.0|757<br>UF=2.0|585<br>UF=2.0|327<br>UF=2.0|



_Table 6‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)_ 

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|333<br>UF=1.4|224<br>UF=1.4|169<br>UF=1.4|163<br>UF=2.5|154<br>UF=3.0|144<br>UF=3.0|129<br>UF=3.0|
|256 Bytes|512<br>FC=1.4|313<br>FC=1.4|214<br>UF=1.4|203<br>UF=2.5|186<br>UF=3.0|168<br>UF=3.0|141<br>UF=3.0|
|512 Bytes|655<br>UF=1.0|385<br>UF=1.0|250<br>UF=1.0|182<br>UF=1.0|205<br>UF=2.0|182<br>UF=2.0|148<br>UF=2.0|
|1024 Bytes|1167<br>UF=1.0|641<br>UF=1.0|378<br>UF=1.0|246<br>UF=1.0|290<br>UF=2.0|246<br>UF=2.0|180<br>UF=2.0|
|2048 Bytes|2191<br>UF=1.0|1153<br>UF=1.0|643<br>UF=1.0|374<br>UF=1.0|461<br>UF=2.0|374<br>UF=2.0|244<br>UF=2.0|
|4096 Bytes|4239<br>UF=1.0|2177<br>UF=1.0|1146<br>UF=1.0|630<br>UF=1.0|802<br>UF=2.0|630<br>UF=2.0|372<br>UF=2.0|



The specification recognizes that the formula will be inadequate for many appli‐ cations such as those that stream large blocks of data. These applications may require buffer sizes larger than the minimum specified, as well as a more sophisticated update policy in order to optimize performance and reduce 

**242** 

**Chapter 6: Flow Control** 

power consumption. Because a given solution is dependent on the particular requirements of an application, no definition for such policies is provided. 

## **Error Detection Timer — A Pseudo Requirement** 

The specification defines an optional time‐out mechanism for Flow Control packets that is highly recommended and may become a requirement in future versions of the specification. The maximum latency between FC packets for a given credit type is 120μs, and this timeout has a maximum limit of 200μs. A separate timer is implemented for each FC credit type (P, NP, Cpl), and each timer is reset when a FC Update DLLP of the corresponding type is received. Note that a timer associated with infinite FC credit values must not report an error. 

Apart from the infinite case, a timeout implies a serious problem with the Link. If it occurs, the Physical Layer is signaled to go into the Recovery state and retrain the Link in hopes of clearing the error condition. Timer characteristics include: 

- Operates only when the Link is in an active state (L0 or L0s). 

- Max time limited to 200 μs (‐0%/+50%) 

- Timer is reset when any Init or Update FCP is received, or optionally by receipt of any DLLP. 

- Timeout forces the Physical Layer to enter Link Training and Status State Machine (LTSSM) Recovery state. 

**243** 

**PCI Ex ress Technolo p gy** 

**244** 

_**7**_ 

## _**Quality of Service**_ 

## **The Previous Chapter** 

The previous chapter discusses the purposes and detailed operation of the Flow Control Protocol. Flow control is designed to ensure that transmitters never send Transaction Layer Packets (TLPs) that a receiver can’t accept. This prevents receive buffer over‐runs and eliminates the need for PCI‐style inefficiencies like disconnects, retries, and wait‐states. 

## **This Chapter** 

This chapter discusses the mechanisms that support Quality of Service and describes the means of controlling the timing and bandwidth of different pack‐ ets traversing the fabric. These mechanisms include application‐specific soft‐ ware that assigns a priority value to every packet, and optional hardware that must be built into each device to enable managing transaction priority. 

## **The Next Chapter** 

The next chapter discusses the ordering requirements for transactions in a PCI Express topology. These rules are inherited from PCI. The Producer/Consumer programming model motivated many of them, so its mechanism is described here. The original rules also took into consideration possible deadlock condi‐ tions that must be avoided. 

## **Motivation** 

Many computer systems today don’t include mechanisms to manage band‐ width for peripheral traffic, but there are some applications that need it. One example is streaming video across a general‐purpose data bus, that requires data be delivered at the right time. In embedded guidance control systems timely delivery of video data is also critical to system operation. Foreseeing those needs, the original PCIe spec included Quality of Service (QoS) mecha‐ nisms that can give preference to some traffic flows. The broader term for this is 

**245** 

**PCI Ex ress Technolo p gy** 
