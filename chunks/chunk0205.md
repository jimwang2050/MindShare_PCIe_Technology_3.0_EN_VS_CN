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