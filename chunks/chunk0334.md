MSI (Memory Write) Transaction<br>+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 0 1 1Fmt 0 0 0 0 0Type R TC R Attr R HT DT EP Attr0 0 AT 0 0 0 0 0 0 0 0 0 1Length<br>Last DW First DW<br>Byte 4 Requester ID Tag 0 0 0 0 1 1 1 1<br>Header<br>Byte 8 MSI Message Address [63:32]<br>Byte 12 MSI Message Address [31:0] 0 0<br>Byte 16 MSI Message Data 0000h Data<br>MSI Capability Structure<br>31 16 15 8 7 0<br>Message Control Next CapabilityPointer Capability ID(05h) DW0<br>Message Address [31:0] DW1<br>Message Address [63:32] DW2<br>Message Data DW3<br>**----- End of picture text -----**<br>


## **The MSI-X Model** 

## **General** 

The 3.0 revision of the PCI spec added support for MSI‐X, which has its own capability structure. MSI‐X was motivated by a desire to alleviate three short‐ comings of MSI: 

- 32 vectors per function are not enough for some applications. 

- Having only one destination address makes static distribution of interrupts across multiple CPUs difficult. The most flexibility would be achieved if a unique address could be assigned for each vector. 

**821** 

**PCI Ex ress 3.0 Technolo p gy** 

- In several platforms, like x86‐based systems, the vector number of the inter‐ rupt indicates its priority relative to other interrupts. With MSI, a single Function could be allocated multiple interrupts, but all the interrupt vectors would be contiguous, meaning similar priority. This is not a good solution if some interrupts from this Function should be high priority and others should be low priority. A better approach would be for software to desig‐ nate a unique vector (message data value), that does not have to be contigu‐ ous, for each interrupt allocated to the Function. 

Keeping those goals in mind, it’s easy to understand the register changes that were implemented to provide more vectors with each vector being assigned a target address and message data value. 

## **MSI-X Capability Structure** 

As shown in Figure 17‐17 on page 822, the Message Control register is quite dif‐ ferent from MSI. Interestingly, even though MSI‐X can support up to 2048 vec‐ tors per Function versus the 32 for MSI, the number of configuration registers for MSI‐X is actually a little smaller than for MSI. That’s because the vector information isn’t contained here. Instead, it’s in a memory location (MMIO) pointed to by the Table BIR (Base address Indicator Register), as shown in Fig‐ ure 17‐18 on page 824. 

_Figure 17‐17: MSI‐X Capability Structure_ 

**==> picture [326 x 174] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 16 15 8 7 0<br>Message Control Next CapabilityPointer Capability ID(11h) DW0<br>Table<br>MSI-X Table Offset DW1<br>BIR<br>PBA<br>Pending Bit Array (PBA) Offset BIR DW2<br>(BIR = BAR Index Register)<br>15 14 13 11 10 0<br>Rsvd Table Size in N-1 (RO)<br>Function Mask (RW)<br>MSI-X Enable (RW)<br>**----- End of picture text -----**<br>


**822** 

**Chapter 17: Interrupt Support** 

_Table 17‐3: Format and Usage of MSI‐X Message Control Register_ 

|**Bit(s)**|**Field Name**|**Description**|
|---|---|---|
|10:0|Table Size|Read‐Only. This field indicates the number of inter‐<br>rupt messages (vectors) that this Function sup‐<br>ports. The value here is interpreted in an N‐1<br>fashion, so a value of 0 means 1 vector. A value of 7<br>means 8 vectors. Each vector has its own entry in<br>the MSI‐X Table and its own bit in the Pending Bit<br>Array.|
|13:11|Reserved|Read‐Only. Always zero.|
|14|Function Mask|Read/Write. This field provides system software an<br>easy way to mask all the interrupts from a Func‐<br>tion. If this bit is cleared, interrupts can still be<br>masked individually by setting the mask bit within<br>each vector’s MSI‐X table entry.|
|15|MSI‐X Enable|Read/Write. State after reset is 0, indicating that the<br>device’s MSI‐X capability is disabled.<br>• **0**= Function is**disabled**from using**MSI‐X**. It<br>must use MSI or INTx Messages.<br>• **1**= Function is**enabled**to use**MSI‐S**to request<br>service and won’t use MSI‐X or INTx Messages.|



**823** 

**PCI Ex ress 3.0 Technolo p gy** 

## _Figure 17‐18: Location of MSI‐X Table_ 

**==> picture [332 x 285] intentionally omitted <==**

**----- Start of picture text -----**<br>
Doubleword<br>Byte (in decimal)Number Syste Memory Address Space m Memory<br>3 2 1 0<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>BIST HeaderType LatencyTimer CacheLineSize 03<br>Base A ddress 0 04<br>Base A ddress 1 05 Table BIR = 2<br>MSI-X Table<br>Base A ddress 2 06<br>Base A ddress 3 07<br>08<br>Base A ddress 4 MSI-X Table<br>Base A ddress 5 09 Offset<br>10<br>CardBus CIS Pointer<br>Subsystem ID SubsystemVendor ID 11<br>Expansion R OM 12<br>Base Ad dress<br>Reserved Capabilities 13<br>Pointer<br>Reserved 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>Required configuration registers<br>**----- End of picture text -----**<br>


## **MSI-X Table** 

The MSI‐X Table itself is an array of vectors and addresses, as shown in Figure 17‐19 on page 825. Each entry represents one vector and contains four Dwords. DW0 and DW1 supply a unique 64‐bit address for that vector, while DW2 gives a unique 32‐bit data pattern for it. DW3 only contains one bit at present: a mask bit for that vector, allowing each vector to be independently masked off as needed. 

**824** 

**Chapter 17: Interrupt Support** 

_Figure 17‐19: MSI‐X Table Entries_ 

|DW3||DW2|DW1|DW0||
|---|---|---|---|---|---|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 0|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 1|
|Vector Control||Message Data|Upper Address|Lower Address|Entry 2|
|….||….|….|….||
|….||….|….|….||
|Vector Control||Message Data|Upper Address|Lower Address|Entry N-1|
|Bit 0 is||vector Mask Bit (R/W)||||



## **Pending Bit Array** 

In much the same way, the Pending Bit Array is also located within a memory address. It can use the same BIR value (same BAR) as the MSI‐X Table with a different offset, or it could use a different BAR altogether. The array, shown in Figure 17‐20, simply contains a bit for every vector that will be used. If the event to trigger that interrupt occurs but its Mask Bit has been set, then an MSI‐X transaction will not be sent. Instead, the corresponding pending bit is set. Later, if that vector is unmasked and the pending bit is still set, the interrupt will be generated at that time. 

**825** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 17‐20: Pending Bit Array_ 

**==> picture [211 x 116] intentionally omitted <==**

**----- Start of picture text -----**<br>
DW1 DW0<br>Pending Bits 0 - 63 QW 0<br>Pending Bits 64 - 127 QW 1<br>Pending Bits 128 - 191<br>….<br>….<br>Pending Bits QW (N-1)/64<br>**----- End of picture text -----**<br>


## **Memory Synchronization When Interrupt Handler Entered** 

## **The Problem** 

There is a potential problem with any interrupt scheme when data is being delivered. For example, if the device has previously sent data and wants to report that with an interrupt, a unexpected delay on data delivery could allow the interrupt to arrive too soon. That might happen in the bridge data buffer shown in Figure 17‐21 on page 827, and the result is a race condition. The steps are similar to our earlier discussion (see “The Legacy Model” on page 796): 

1. The function writes a data block toward memory. The write completes on the local bus as a posted transaction, meaning that the sender has finished all it needed to do and the transaction is considered completed. 

2. An interrupt is delivered to notify software that some requested data is now present in memory. However, the data has been delayed in the bridge for some reason. 

3. The interrupt vector is fetched as before. 

4. The ISR starting address is fetched and control is passed to it. 

5. The ISR reads from the target memory buffer but the data payload still hasn’t been delivered so it fetches stale data, possibly causing an error. 

**826** 

**Chapter 17: Interrupt Support** 

_Figure 17‐21: Memory Synchronization Problem_ 

**==> picture [268 x 199] intentionally omitted <==**

**----- Start of picture text -----**<br>
INTR<br>CPU 5 Memory<br>Memory Buffer<br>4 Interrupt Service<br>Routine (ISR)<br>North Bridge<br>Interrupt Table (ISR<br>3 starting addresses)<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>1<br>PCI Bus<br>2<br>Interrupt Controller<br>(PIC) INTA#<br>Device<br>**----- End of picture text -----**<br>


## **One Solution** 

One way to alleviate this problem takes advantage of PCI transaction ordering rules. If the ISR first sends a read request to the device that initiated the inter‐ rupt before it attempts to fetch the data, the resulting read completion will fol‐ low the same path back to the CPU that any write data would have taken from that device to get to memory. Transaction ordering rules guarantee that a read result in a bridge cannot pass a posted write going in the same direction, so the end result is that the data will get written into memory before the read result will be allowed to reach the CPU. Therefore, if the ISR waits for the read com‐ pletion to arrive before proceeding, it can be sure that any data will have been delivered to memory and thus the race condition is avoided. Since the read is basically being used as a data flush mechanism, it isn’t necessary for it to return any data. In that case the read can be zero length and the data returned is dis‐ carded. For that reason, this type of read is sometimes called a “dummy read.” 

## **An MSI Solution** 

MSI can simplify this process, although there are some requirements for it to work (refer to Figure 17‐22 on page 829). If the system allows the device to gen‐ 

**827** 

**PCI Ex ress 3.0 Technolo p gy** 

erate its own MSI writes rather than going through an intermediary like an IO APIC, then the following example can take place: 

1. The device writes the payload data toward memory and it is absorbed by the write buffer in the bridge. 

2. The device believes the data has been delivered and signals an interrupt to notify the CPU. In this case, an MSI is sent and uses the same path as the data. Since both data and MSI appear as memory writes to the bridge, the normal transaction ordering rules will keep them in the correct sequence. 

3. The payload data is delivered to memory, freeing the path through the bridge for the MSI write. 

4. The MSI write is delivered to the CPU Local APIC and the software now knows that the payload data is available. 

## **Traffic Classes Must Match** 

An important point must be stressed here, however. Both the data and MSI must use the same Traffic Class for this to work. Recall that packets that have been assigned different TC values may end up being mapped into different Vir‐ tual Channels, and that packets in different VCs have no ordering relationship. If the data were mapped to VC0 and the MSI was mapped to VC1, then the sys‐ tem would be unaware of any ordering relationship between them and unable to enforce memory coherency automatically. 

If giving both packets the same TC is not possible, the system would need to use the “dummy read” method instead and the TC of the read request would need to match the TC of the data write packet. It should be clear that even if the same TC is used for both, the use of the Relaxed Ordering bit must be avoided. We’re counting on the transaction ordering rules to achieve memory synchronization, so they must not be relaxed. 

**828** 

**Chapter 17: Interrupt Support** 

_Figure 17‐22: MSI Delivery_ 

**==> picture [280 x 246] intentionally omitted <==**

**----- Start of picture text -----**<br>