## **PCI Configuration Cycle Generation** 

Since IO address space is limited, the legacy model was designed to be very conservative with addresses. The common way of doing that in IO space was to have one register for pointing to an internal location, and a second one for read‐ ing or writing the data. In PCI configuration that involves two steps. 

Step 1: The CPU generates an IO write to the Address Port at IO address CF8h in the North Bridge to give the address of the configuration register to be accessed. This address, shown in Figure 1‐11 on page 27, consists primarily of the three things that locate a PCI function within the topology: which bus we want to access out of the 256 possible, which device on that bus out of the 32 possible, and which function within that device out of the 8 possible. The only other information needed is to identify which of the 64 dwords (256 bytes) in that function’s configuration space is to be accessed. 

**26** 

**Chapter 1: Background** 

Step 2: The CPU generates either an IO read or IO write to the Data Port at loca‐ tion CFCh in the North Bridge. Based on that, the North Bridge then generates a configuration read or configuration write transaction to the PCI bus specified in the Address Port. 

_Figure 1‐11: Configuration Address Register_ 

**==> picture [374 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
0CFBh 0CFAh 0CF9h 0CF8h<br>31 30 24 23 16 15 11 10 8 7 2 1 0<br>Reserved Bus Device Function Doubleword 0 0<br>Number Number Number<br>Register pointer (64 DW)<br>Should always be zeros<br>Enable Configuration Space Mapping<br>1 = enabled<br>**----- End of picture text -----**<br>