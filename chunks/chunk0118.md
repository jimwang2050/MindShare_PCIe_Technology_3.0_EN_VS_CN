## **PCI Ex ress Technolo p gy** 

_Figure 1‐12: PCI Configuration Header Type 1 (Bridge)_ 

**==> picture [362 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 1 Header<br>Primary Bus 31 23 15 7 0<br>Device ID Vendor ID 00h<br>Configuration Status Command 04h<br>Registers<br>Class Code  Rev 08h<br>Header      ID<br>BIST Header Latency Cache 0Ch<br>Type Timer Line Size<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h<br>Bridge Function Secondary Subordinate Secondary Primary 18h<br>Lat Timer Bus # Bus # Bus #<br>SecondaryStatus LimitIO BaseIO 1Ch<br>Secondary Bus (Non-Prefetchable)Memory Limit (Non-Prefetchable)Memory Base 20h<br>Memory LimitPrefetchable Memory BasePrefetchable 24h<br>Prefetchable Memory Base 28h<br>Upper 32 Bits<br>Prefetchable Memory LimitUpper 32 Bits 2Ch<br>IO Limit IO Base<br>Upper 16 Bits Upper 16 Bits 30h<br>Reserved Capability 34h<br>Pointer<br>Expansion ROM Base Address 38h<br>ControlBridge InterruptPin InterruptLine 3Ch<br>**----- End of picture text -----**<br>

**28** 

**Chapter 1: Background** 

_Figure 1‐13: PCI Configuration Header Type 0 (not a Bridge)_ 

**==> picture [350 x 264] intentionally omitted <==**

**----- Start of picture text -----**<br>
Type 0 Header<br>31 23 15 7 0<br>Device ID Vendor ID 00h<br>Configuration Status Command 04h<br>Registers<br>Class Code  Rev 08h<br>Header      ID<br>BIST Header Latency Cache 0Ch<br>Type Timer Line Size<br>Base Address 0 (BAR0) 10h<br>Base Address 1 (BAR1) 14h<br>Device Base Address 2 (BAR2) 18h<br>Base Address 3 (BAR3) 1Ch<br>Base Address 4 (BAR4) 20h<br>Base Address 5 (BAR5) 24h<br>CardBus CIS Pointer 28h<br>SubsystemDevice ID SubsystemVendor ID 2Ch<br>Expansion ROM Base Address 30h<br>Reserved Capability 34h<br>Pointer<br>Reserved 38h<br>Max Lat Min Gnt InterruptPin InterruptLine 3Ch<br>**----- End of picture text -----**<br>

Details of the configuration register space and the enumeration process are described later. For now we simply want you to become familiar with the big picture of how all the parts fit together. 