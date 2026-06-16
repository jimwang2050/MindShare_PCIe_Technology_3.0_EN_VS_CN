## **PCI Function Configuration Register Space** 

Each PCI function contains up to 256 bytes of configuration space. The first 64 bytes of each functionʹs configuration space contains a structure called the Header, while the remaining 192 Bytes support optional functionality. System configuration is first performed by Boot ROM firmware. After the OS loads, it may reconfigure the system and rearrange resource assignments, with the result that the process of system configuration may be done twice. 

There are two basic classes of PCI functions as defined by their header types. A Type 1 header identifies a function that is a bridge (as shown in Figure 1‐12 on page 28) and creates another bus in the topology, while a Type 0 header indi‐ cates a function that is NOT a bridge (as shown in Figure 1‐13 on page 29). This header type information is contained in a field by the same name in dword 3, byte 2, and should be one of the first things software checks when discovering which functions exist in the system (a process called “enumeration”). 

**27** 