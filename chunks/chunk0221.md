## **Some Rules** 

A Root Complex is not required to support an access to enhanced configuration memory space if it crosses a dword address boundary (straddles two adjacent memory dwords). Nor are they required to support the bus locking protocol that some processor types use for an atomic, or uninterrupted series of com‐ mands. Software should avoid both of these situations when accessing configu‐ ration space unless it is known that the Root Complex does support them. 

_Table 3‐1: Enhanced Configuration Mechanism Memory‐Mapped Address Range_ 

|**Memory Address Bit Field**|**Description**|
|---|---|
|A[63:28]|Upper bits of the 256MB‐aligned base address of the<br>256MB memory‐mapped address range allocated<br>for the Enhanced Configuration Mechanism.<br>The manner in which the base address is allocated is<br>implementation‐specific. It is supplied to the OS by<br>system firmware (typically through the ACPI<br>tables).|
|A[27:20]|Target Bus Number (0 ‐ 255).|
|A[19:15]|Target Device Number (0 ‐ 31).|
|A[14:12]|Target Function Number (0 ‐ 7).|

**98** 

**Cha ter 3: Confi uration Overview p g** 

_Table 3‐1: Enhanced Configuration Mechanism Memory‐Mapped Address Range (Continued)_ 

|**Memory Address Bit Field**|**Description**|
|---|---|
|A[11:2]|A[11:2] this range can address one of 1024 dwords,<br>whereas the legacy method is limited to only<br>address one of 64 dwords.|
|A[1:0]|Defines the access size and the Byte Enable setting.|