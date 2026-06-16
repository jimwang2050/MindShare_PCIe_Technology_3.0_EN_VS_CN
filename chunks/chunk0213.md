## **Configuration Address Port** 

The Configuration Address Port only latches information when the processor performs a full 32‐bit write to the port, as shown in Figure 3‐4, and a 32‐bit read from the port returns its contents. The information written to the Configuration Address Port must conform to the following template (illustrated in Figure 3‐4) and described on the facing page. 

_Figure 3‐4: Configuration Address Port at 0CF8h_ 

**==> picture [339 x 129] intentionally omitted <==**

**----- Start of picture text -----**<br>
31 30 24 23 16 15 11 10 8 7 2 1 0<br>Reserved Bus Device Function Doubleword 0 0<br>Number Number Number<br>Register pointer (64 DW)<br>Should always be zeros<br>Enable Configuration Space Mapping<br>1 = enabled<br>**----- End of picture text -----**<br>

**92** 

**Cha ter 3: Confi uration Overview p g** 

- Bits **[1:0]** are hard‐wired, read‐only and must return **zeros** when read. The location is dword aligned and no byte‐specific offset is allowed. 

- Bits **[7:2]** identify the **target dword** (also called the Register Number) in the target Functionʹs PCI‐compatible configuration space. This mechanism is limited to the compatible configuration space (i.e., the first 64 doublewords of a Function’s configuration space). 

- Bits **[10:8]** identify the **target Function** number (0 ‐ 7) within the target device. 

- Bits **[15:11]** identify the **target Device** number (0 ‐ 31). 

- Bits **[23:16]** identify the **target Bus** number (0 ‐ 255). 

- Bits **[30:24]** are **reserved** and must be zero. 

- Bit **[31]** must be set to 1b to enable translation of the subsequent IO access to the Configuration Data Port into a configuration access. If bit 31 is zero and an IO read or write is sent to the Configuration Data Port, the transaction is treated as an ordinary IO Request. 