## **PCI and PCI-X** 

The PCI (Peripheral Component Interface) bus was developed in the early 1990’s to address the shortcomings of the peripheral buses that were used in PCs (personal computers) at the time. The standard at the time was IBM’s AT (Advanced Technology) bus, referred to by other vendors as the ISA (Industry Standard Architecture) bus. ISA had been sufficient for the 286 16‐bit machines for which it was designed, but additional bandwidth and improved capabilities, such plug‐and‐play, were needed for the newer 32‐bit machines and their peripherals. Besides that, ISA used big connectors that had a high pin count. PC vendors recognized the need for a change and several alternate bus designs were proposed, such as IBM’s MCA (Micro‐Channel Architecture), the EISA bus (Extended ISA, proposed as an open standard by IBM competitors), and the VESA bus (Video Electronics Standards Association, proposed by video card vendors for video devices). However, all of these designs had drawbacks that prevented wide acceptance. Eventually, PCI was developed as an open standard by a consortium of major players in the PC market who formed a group called the PCISIG (PCI Special Interest Group). The performance of the newly‐devel‐ oped bus architecture was much higher than ISA, and it also defined a new set of registers within each device referred to as configuration space. These regis‐ ters allowed software to see the memory and IO resources a device needed and assign each device addresses that wouldn’t conflict with other addresses in the system. These features: open design, high speed, and software visibility and control, helped PCI overcome the obstacles that had limited ISA and other buses PCI quickly became the standard peripheral bus in PCs. 

A few years later, PCI‐X (PCI‐eXtended) was developed as a logical extension of the PCI architecture and improved the performance of the bus quite a bit. We’ll discuss the changes a little later, but a major design goal for PCI‐X was main‐ taining compatibility with PCI devices, both in hardware and software, to make migration from PCI as simple as possible. Later, the PCI‐X 2.0 revision added even higher speeds, achieving a raw data rate of up to 4 GB/s. Since PCI‐X main‐ tained hardware backward compatibility with PCI, it remained a parallel bus and inherited the problems associated with that model. That’s interesting for us because parallel buses eventually reach a practical ceiling on effective band‐ width and can’t readily be made to go faster. Going to a higher data rate with PCI‐X was explored by the PCISIG, but the effort was eventually abandoned. That speed ceiling, along with a high pin count, motivated the transition away from the parallel bus model to the new serial bus model. 

These earlier bus definitions are listed in Table 1‐1 on page 11, which shows the development over time of higher frequencies and bandwidths. One of the inter‐ 

**10** 

**Chapter 1: Background** 

esting things to note in this table is the correlation of clock frequency and the number of add‐in card slots on the bus. This was due to PCI’s low‐power signal‐ ing model, which meant that higher frequencies required shorter traces and fewer loads on the bus (see “Reflected‐Wave Signaling” on page 16). Another point of interest is that, as the clock frequency increases, the number of devices permitted on the shared bus decreases. When PCI‐X 2.0 was introduced, its high speed mandated that the bus become a point‐to‐point interconnect. 

_Table 1‐1:  Comparison of Bus Frequency, Bandwidth and Number of Slots_ 

|**Bus Type**|**Clock Frequency**|**Peak Bandwidth**<br>**32‐bit ‐ 64‐bit bus**|**Number of Card**<br>**Slots per Bus**|
|---|---|---|---|
|PCI|33 MHz|133 ‐ 266 MB/s|4‐5|
|PCI|66 MHz|266 ‐ 533 MB/s|1‐2|
|PCI‐X 1.0|66 MHz|266 ‐ 533 MB/s|4|
|PCI‐X 1.0|133 MHz|533 ‐ 1066 MB/s|1‐2|
|PCI‐X 2.0 (DDR)|133 MHz|1066 ‐ 2132 MB/s|1 (point‐to‐point bus)|
|PCI‐X 2.0 (QDR)|133 MHz|2132 ‐ 4262 MB/s|1 (point‐to‐point bus)|