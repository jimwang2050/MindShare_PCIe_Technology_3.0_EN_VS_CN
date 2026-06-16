2. Group Arbitration — VCs are divided by hardware into one low‐priority group and one high‐priority group. The low‐priority group uses an arbitra‐ tion method selected by software from the available choices, while the high‐ priority group always uses strict‐priority arbitration. 

3. Hardware Fixed arbitration — scheme built into the hardware. 

**252** 

**Chapter 7: Quality of Service** 

_Figure 7‐6: VC Arbitration Example_ 

**==> picture [246 x 330] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>VC1 VC0<br>Root Complex<br>Memory<br>TC/VC Mapping<br>VC arbitration in this<br>example yields a 3 to 1<br>ratio for transmitting<br>VC1 and VC0.<br>Arbiter<br>VC1 VC0<br>TC/VC Mapping<br>Device<br>Core<br>**----- End of picture text -----**<br>


## **Strict Priority VC Arbitration** 

The default priority scheme is based on the inherent priority of VC IDs (VC0=lowest priority and VC7=highest priority). The mechanism is automatic and requires no configuration. Figure 7‐7 on page 254 illustrates a strict priority arbitration example that includes all VCs. The VC ID governs the order in which transactions are sent. The maximum number of VCs that use strict prior‐ ity arbitration cannot be greater than the value in the _Extended VC Count_ field. 

**253** 

**PCI Ex ress Technolo p gy** 

(See Figure 7‐5 on page 251.) Furthermore, if the designer has chosen strict pri‐ ority arbitration for all VCs supported, the _Low Priority Extended VC Count_ field of Port VC Capability Register 1 is hardwired to zero. (See Figure 7‐8 on page 255. 

_Figure 7‐7: Strict Priority Arbitration_ 

|VC Resources|Priority Order|Priority Order|
|---|---|---|
|8th VC|VC7|Highest|
|7th VC|VC6||
|6th VC|VC5||
|5th VC|VC4||
|4th VC|VC3||
|3rd VC|VC2||
|2nd VC|VC1||
|1st VC|VC0|Lowest|
||||



Strict priority requires that higher‐numbered VCs always get precedence over lower‐priority VCs. For example, if all eight VCs are governed by strict priority, then packets in VC0 can only be sent when no other VCs have packets pending. This achieves the goal of giving the highest priority packets very high band‐ width with minimal latencies. However, strict priority has the potential to starve low‐priority channels for bandwidth, so care must be taken to ensure this doesn’t happen. The spec requires that high priority traffic be regulated to avoid starvation, and gives two possible methods of regulation: 

- The originating port can restrict the injection rate of high priority packets to allow more bandwidth for lower priority transactions. 

- Switches can regulate multiple traffic flows at the egress port. This method may limit the throughput from high bandwidth applications and devices that attempt to exceed the limitations of the available bandwidth. 

A device designer may also limit the number of VCs that participate in strict priority by splitting the VCs into a low‐priority group and a high‐priority group as discussed in the next section. 

**254** 

**Chapter 7: Quality of Service** 

## **Group Arbitration** 

Figure 7‐8 illustrates the _Low Priority Extended VC Count_ field within VC Capa‐ bility Register 1. This read‐only field specifies a VC ID that identifies the upper limit of the low‐priority arbitration group for this device. For example, if this value is 4, then VC0‐VC4 are members of the low‐priority group and VC5‐VC7 are in the high‐priority group. Note that a _Low Priority Extended VC Count_ of 7 means that no strict priority is used. 

_Figure 7‐8: Low‐Priority Extended VCs_ 

**==> picture [333 x 339] intentionally omitted <==**

**----- Start of picture text -----**<br>
  31               24  23           16  15                                      0<br>PCI Express Extended Capability Header 00h<br>Port VC Capability Register 1  04h<br>Port VC Capability Register 2  08h<br>Port VC Status Register  Port VC Control Register  0Ch<br>PAT Offset VC0 Resource Capability Register  10h<br>VC0 Resource Control Register  14h<br>VC0 Resource Status Reg  Reserved 18h<br>PAT Offset VCn Resource Capability Register  10h+(n*0Ch)<br>VCn Resource Control Register  14h+(n*0Ch)<br>VCn Resource Status Reg  Reserved 18h+(n*0Ch)<br>n = one of the extended VCs<br>31          12 11 10 9 8 7  6     4 3  2     0<br>RsvdP<br>Port Arbitration Table Entry Size<br>Reference Clock<br>RsvdP<br>Low Priority Extended VC Count<br>RsvdP<br>Extended VC Count<br>**----- End of picture text -----**<br>


**255** 

**PCI Ex ress Technolo p gy** 

As depicted in Figure 7‐10 on page 257, the high‐priority VCs continue to use strict priority arbitration, while the low‐priority arbitration group uses one of the other arbitration methods supported by the device. VC Capability Register 2 reports which alternate methods are supported for this group, as shown in Fig‐ ure 7‐9, and the VC Control Register permits selection of the method to be used. The low‐priority arbitration schemes include: 

- Hardware Based Fixed Arbitration 

- Weighted Round Robin Arbitration (WRR) 

_Figure 7‐9: VC Arbitration Capabilities_ 

**==> picture [304 x 162] intentionally omitted <==**

**----- Start of picture text -----**<br>
31                     24  23                            8 7                        0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>7                       4   3     2     1     0<br>RsvdP<br>WRR with 128 Phases (011b)<br>WRR with 64 Phases (010b)<br>WRR with 32 Phases (001b)<br>Hardware Fixed Arbitration Scheme (000b)<br>**----- End of picture text -----**<br>


**==> picture [193 x 86] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Control Register<br>15                                 4  3     1 0<br>RsvdP<br>VC Arbitration Select (000b-111b)<br>Load VC Arbitration Table<br>**----- End of picture text -----**<br>


**256** 

**Chapter 7: Quality of Service** 

_Figure 7‐10: VC Arbitration Priorities_ 

|VC Resources|VC IDs|||Split Priority||
|---|---|---|---|---|---|
|||||Highest||
|8th VC|VC7|||||
|7th VC|VC6||High-Priority (Strict Priority Scheme)|||
|5th VC<br>6th VC|VC5<br>VC4|||Low-Priority VC ID = 4||
|4th VC|VC3|||||
|3rd VC|VC2||Low-Priority (Alternate Priority Scheme)<br>(Selected by Software)|||
|||||||
|2nd VC|VC1|||||
|1st VC|VC0|||Lowest||



## **Hardware Fixed Arbitration Scheme** 

This selection defines a hardware‐based method and requires no additional software setup. This method can be anything the hardware designer chooses to build in, and could be based on anticipated loading or band‐ width needs for the device. A simple example might be an ordinary round robin sequence, in which each VC gets an equal turn at sending packets during the rotation. 

## **Weighted Round Robin Arbitration Scheme** 

This is a scheme in which some VCs can be weighted more (given higher priority) than others by giving them more entries in the sequence than oth‐ ers. The spec defines three WRR options, each with a different number of entries (called phases). The table size is selected by writing the correspond‐ ing value in to the _VC Arbitration Select_ field of the Port VC Control Register (see Figure 7‐9 on page 256). Each entry in the table represents one phase that software loads with a low priority VC number. The VC arbiter will repeatedly scan all table entries in a sequential fashion and send packets from the VC specified in the table entries. Once a packet has been sent, the 

**257** 

**PCI Ex ress Technolo p gy** 

arbiter immediately proceeds to the next phase. Figure 7‐11 on page 258 shows an example of a WRR arbitration table with 64 entries. 

_Figure 7‐11: WRR VC Arbitration Table_ 

**==> picture [165 x 259] intentionally omitted <==**

**----- Start of picture text -----**<br>
Phase VC ID<br>0 VC 4<br>1 VC 3<br>2 255 (16KB)VC 2<br>3 VC 1<br>4 VC 4<br>5 VC 3<br>6 VC 0<br>7 64 (4KB)VC 4<br>8 VC 3<br>9 128 (8KB)VC 2<br>10 VC 1<br>1111 VC 4<br>621 VC 3<br>632 VC 0<br>Arbitration Logic Scans Table Entries<br>**----- End of picture text -----**<br>


## **Setting up the Virtual Channel Arbitration Table** 

The location of the VC Arbitration Table (VAT) in configuration space is given as an offset from the base address of the VC Capability Structure, as shown in Figure 7‐12 on page 259. 

As shown in Figure 7‐13 on page 260, each entry in the VAT is a 4‐bit field that identifies the VC number of the buffer that is scheduled to deliver data during that phase. The table length is selected by the arbitration option shown in Figure 7‐9 on page 256. 

**258** 

**Chapter 7: Quality of Service** 

_Figure 7‐12: VC Arbitration Table Offset and Load VC Arbitration Table Fields_ 

**==> picture [331 x 385] intentionally omitted <==**

**----- Start of picture text -----**<br>
Port VC Capability Register 2<br>31                     24  23                                             8 7                      0<br>VC Arbitration RsvdP VC Arbitration<br>Table Offset Capability<br>0d<br>Header<br>CapPtr<br>63d<br>PCICompatible<br>PCIe Cap Structure (CapID=10h) Space<br>255d<br>PCIEXEnhancedCapabilityRegister<br>PortVCCapRegister1 ExtVCCnt<br>VATOffset PortVCCapRegister2<br>PortVCStatusReg PortVCControlReg<br>PAT0Offset VC0 Resource Cap Reg<br>VC Resource Control Register PCIEXExtended<br>VC Resource Status Reg Reserved CapabilitySpace<br>PATnOffset VCn Resource Cap Reg<br>VC Resource Control Register<br>VC Resource Status Reg Reserved<br>VC Arbitration Table (VAT)<br>4095d<br>**----- End of picture text -----**<br>


The table is loaded by configuration software to achieve the desired priority order for the virtual channels. Hardware sets the _VC Arbitration Table Status_ bit whenever any changes are made to the table, giving software a way to verify whether changes have been made but not yet applied to the hard‐ ware. Once the table is loaded, software sets the _Load VC Arbitration Table_ bit 

**259** 

## **PCI Ex ress Technolo p gy** 

in the Port VC Control register. That causes hardware to load, or apply, the new values to the VC Arbiter. Hardware clears the _VC Arbitration Table Sta‐ tus_ bit when table loading is complete, signaling to software that loading has finished. This method is probably motivated by the desire to change the table contents during run time without disruption. The problem is that con‐ figuration writes are only able to update a dword at a time and are rela‐ tively slow transactions, which means it could take a long time to finish making changes, during which the table is only partially updated. That, in turn, could result in unexpected behavior by the device as it continues to operate during this time. To avoid that, this mechanism allows software to complete all the changes to the table and then apply them all at once to the hardware arbiter. 

_Figure 7‐13: Loading the VC Arbitration Table Entries_ 

|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|32 Phase Virtual Channel Arbitration Table|||||||||
|---|---|---|---|---|---|---|---|---|---|---|---|
|31       28 27      24 23      20 19<br>16 15       12 11|8||7|4|3|||0||||
|Phase[2]<br>Phase[3]<br>Phase[4]<br>Phase[5]<br>Phase[6]<br>Phase[7]|||Phase[1]||Phase[0]||||||00h|
|Phase[10]<br>Phase[11]<br>Phase[12]<br>Phase[13]<br>Phase[14]<br>Phase[15]|||Phase[9]||Phase[8]||||||04h|
|Phase[18]<br>Phase[19]<br>Phase[20]<br>Phase[21]<br>Phase[22]<br>Phase[23]|||Phase[17]||Phase[16]||||||08h|
|Phase[26]<br>Phase[27]<br>Phase[28]<br>Phase[29]<br>Phase[30]<br>Phase[31]|||Phase[25]||Phase[24]|||||0Ch||
|<br>1. Configuration Software loads the VC Arbitration Table.<br>2. The VC Arbitration Table Status bit is set when any|3||2|1||0||||||
|table  entry is updated.|RsvdP|||VC ID||||||||
|3. Software sets the Load VC Arbitration Table bit.||||||||||||
|4. Hardware applies table contents to VC Arbiter.||||||||||||
|5. Hardware clears the VC Arbitration Table status bit||||||||||||