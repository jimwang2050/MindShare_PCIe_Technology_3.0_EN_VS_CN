## **TLP (Transaction Layer Packet) Basics** 

A list of all of the PCIe request and completion packet types is given in Table 2‐ 3 on page 61. 

**60** 

**Chapter 2: PCIe Architecture Overview** 

_Table 2‐3: PCI Express TLP Types_ 

|**TLP Packet Types**|**Abbreviated**<br>**Name**|
|---|---|
|Memory Read Request|MRd|
|Memory Read Request ‐ Locked access|MRdLk|
|Memory Write Request|MWr|
|IO Read|IORd|
|IO Write|IOWr|
|Configuration Read (Type 0 and Type 1)|CfgRd0,<br>CfgRd1|
|Configuration Write (Type 0 and Type 1)|CfgWr0,<br>CfgWr1|
|Message Request without Data|Msg|
|Message Request with Data|MsgD|
|Completion without Data|Cpl|
|Completion with Data|CplD|
|Completion without Data ‐ associated with Locked Memory Read<br>Requests|CplLk|
|Completion with Data ‐ associated with Locked Memory Read<br>Requests|CplDLk|

TLPs originate at the Transaction Layer of a transmitter and terminate at the Transaction Layer of a receiver, as shown in Figure 2‐15 on page 62. The Data Link Layer and Physical Layer add parts to the packet as it moves through the layers of the transmitter, and then verify at the receiver that those parts were transmitted correctly across the Link. 

**61** 