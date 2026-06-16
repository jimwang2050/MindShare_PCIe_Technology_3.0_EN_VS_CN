# 📘 第 99 章　附录 (Chapter 99. Appendices)

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0348.md` ... `chunks/chunk0356.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [Appendices](#-本章目录-table-of-contents)

<a id="sec-99-1"></a>
## 99.1 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Care should be taken when selecting an interposer as the probe circuitry varies by vendor and by requirements imposed by the max PCIe link speed. For exam‐ ple, a Gen3 slot interposer should contain probe circuitry which allows the dynamic link training process to pass properly through the probe. The LeCroy Gen3 slot interposer uses linear circuits to maintain the shape of the waveform as it passes through the probe. This allows pre‐emphasis of the transmitter to be dynamically changed during link training while allowing the receiver to quan‐ tify the impact of a new setting (either positive or negative impact). 

_Figure A‐2: LeCroy PCI Express Slot Interposer x16_ 

LeCroy also offers a family of other dedicated interposers for form factors such as ExpressCard, XMC, Mini Card, Express Module, AMC, etc. Some of these interposers are shown in Figure 3 on page 923. For a complete list of these inter‐ posers please refer to the LeCroy website: www.lecroy.com as this list is con‐ stantly growing. 

**922** 

**A endix A pp** 

_Figure A‐3: LeCroy XMC, AMC, and Mini Card Interposers_ 

For debugging PCIe links which cannot benefit from a dedicated interposer, a mid‐bus probe shown in Figure 4 on page 923 is the next best option. A mid‐bus probe involves placement of an industry standard probe geometry on the PCB. Each PCIe lane is routed to a pair of pads on the footprint which can be probed using a mid‐bus probe head. These probes use spring pins or C clips for provid‐ ing solder free mechanical attachment between the system under test and the protocol analyzer. 

_Figure A‐4: LeCroy PCI Express Gen3 Mid‐Bus Probe_ 

**923** 

## **PCI Ex ress Technolo p gy** 

As a last resort, a flying lead probe shown in Figure 5 on page 924 may be used to attach the protocol analyzer to the system under test. This involves soldering a resistive tap circuit and connector pins to the PCIe traces. This circuitry is typ‐ ically soldered to the AC coupling caps of the PCIe link as they are often the only place to access the traces. Once the probe circuitry is soldered to the PCB, the analyzer probe can be connected and removed as needed. This approach can be used on virtually any PCIe link, however the robustness of the connec‐ tion is limited by the skill of the technician adding the probe. 

_Figure A‐5: LeCroy PCI Express Gen2 Flying Lead Probe_ 

## **Viewing Traffic Using the PETracer Application** 

## **CATC Trace Viewer** 

The primary way to view PCI Express traffic with the LeCroy PETracer applica‐ tion is the CATC Trace view. This view takes each recorded packet and breaks it down into different packet fields to highlight the important values contained in this packet. A mixture of colors and text are used to visually categorize and explain the purpose of each packet. Errors are highlighted in red such as shown in Figure 6 on page 925. Warnings are highlighted in yellow making it easy to identify areas of traffic or fields in a packet which are non‐compliant. 

**924** 

**A endix A pp** 

## _Figure A‐6: TLP Packet with ECRC Error_ 

In addition to decoding and visually breaking down each packet, a hierarchical display allows logical grouping of related packets. For example, in “Link Level” mode, TLP packets are grouped with their respective ACK packet. Each TLP is identified as either implicitly or explicitly ACK’d or NAK’d. An example of a ACK DLLP is shown in Figure 7 on page 925 along with the ACK’d TLP. 

_Figure A‐7: “Link Level” Groups TLP Packets with their Link Layer Response_ 

In “Split‐Level” mode shown in Figure 8 on page 926, the CATC Trace view combines split transactions. For example, a single TLP read can be grouped with 1 or more completion TLPs to logically show large data transfers as a sin‐ gle line in the trace. The amount of data, starting address, as well as perfor‐ mance metrics are provided for each split level transaction. This allows the user to bypass the details of how large memory transactions are broken into multiple TLP packets and rather focus on the contents of the data. If the user wishes to see the details of the split transaction, the hierarchical display can show the link level and/or packet level breakdown of all the packets which make up this split transaction. This “drill‐down” approach to traffic analysis allows the user to start from a high level view of what’s happening on the bus and drill down only in the areas of traffic which are interesting to the user. 

**925** 

**PCI Ex ress Technolo p gy** 

_Figure A‐8: “Split Level” Groups Completions with Associated Non‐Posted Request_ 

The CATC trace view also supports “Compact‐View” shown in Figure 9 on page 927. In this view, packets which are sent repeatedly are collapsed into a single cell. This is very useful for collapsing Training Sequences or Flow Control Initialization packets. The software algorithms which perform this collapse are smart enough to collapse any SKIP ordered sets as well. This creates a very compact view of the link training process allowing the user to examine changes in the link training packets without scrolling through hundreds of packets. 

**926** 

**A endix A pp** 

_Figure A‐9: “Compact View” Collapses Related Packets for Easy Viewing of Link Training_ 

## **LTSSM Graphs** 

To further enhance the “drill‐down” traffic viewing approach, the PETracer application includes an LTSSM graph view as shown in Figure 10 on page 928. When this graph is invoked, the SW parses through the trace to find the link training sections and infers the state of the Link Training and Status State Machine (LTSSM). The result is a graph which breaks down the LTSSM state transitions in a very high level view. This graph allows the user to immediately see if the link went into a recovery state. If so, the user can easily identify which side of the link initiated the recovery, how many times it entered recovery, and even if the link speed or link width decreased because of the recovery. 

The LTSSM graph is also an active link back into the trace file. For example, if the user clicks on the entry to recovery, the trace file will be navigated to that location in the trace file. This would allow the user to perhaps see if the recov‐ ery was caused by repeated NAKs or for some other reason such as loss of block alignment. 

**927** 

In short, when users are debugging issues related to link training, speed change, or low power state transitions, the LTSSM is affected. By examining the LTSSM graph, the user can easily identify whether these link state changes occurred, where they occurred, and navigate directly to them for faster analysis. 

_Figure A‐10: LTSSM Graph Shows Link State Transitions Across the Trace_ 

## **Flow Control Credit Tracking** 

Flow control credit tracking is particularly problematic in PCI express. The flow control update packets do not show the number of credits each endpoint has, rather it shows how many credits in total have been used. This means that each endpoint must keep a running counter of credits for each type. There are a num‐ ber of scenarios where credits can be lost, and if this occurs, the link will eventu‐ ally be unable to transmit data due to lack of credits. Such problems are very difficult to identify and debug. 

The LeCroy PETracer application has a credit tracking SW tool shown in Figure 11 on page 929 to aid in this debug. If the trace contains FC‐Init packets, it will walk through the trace and show the amount of remaining credits per virtual channel buffer type after each TLP and FC‐Update. 

FC‐Init packets are sent once after link training. Because of this, the PETracer application has the ability for the user to set initial credit values at some point in 

**A endix A pp** 

the trace and the SW will calculate the relative credit values for the remaining packets. Even if the initial credit values are set improperly by the user, having the ability to see the relative credits is often enough to catch a flow control issue. 

_Figure A‐11: Flow Control Credit Tracking_ 

## **Bit Tracer** 

Some debug situations are not solved by a drill down approach to examining the traffic. For example if the link settings are incorrect, the recording is often unreadable. What if a device is not properly scrambling the traffic, or the 10 bit symbols are sent in reverse order? For this scenario, a tool which focuses on analysis between the waveform view of the scope and the CATC Trace view is needed. This is where the BitTracer view shown in Figure 12 on page 930 is most powerful. 

The BitTracer view allows the user to see raw traffic exactly as it was seen on the link. The software allows the user to see the traffic as 10 bit symbols, scrambled bytes, or unscrambled bytes. Invalid symbols and incorrect running disparity are highlighted in red. 

**929** 

## **PCI Ex ress Technolo p gy** 

To further determine what may be wrong with the traffic, the BitTracer tool adds a powerful list of post processing features which can modify the traffic. For example, post capture; the user can invert the polarity of a given lane. Once applied, the user can see if the 10 bit symbols are now represented properly in the trace. If this cleans up the trace, it’s an indication that the recording settings for the Analyzer hardware need to be changed. 

_Figure A‐12: BitTracer View of Gen2 Traffic_ 

In addition, the lane ordering can be modified. This is useful for determining if lane reversal is causing a bad capture. If the traffic has excessive lane to lane skew, the BitTracer software allows the user to re‐align the traffic. For Gen3 traf‐ fic, this skew can be applied 1 bit at a time. This essentially allows the user to fix the 130 bit block alignment post capture. 

After applying changes to the data, all or just a portion of the data can be exported into the standard CATC Trace view for higher level analysis. This workflow is very powerful for debugging low level issues during early bring‐ up. Let’s say for example, the user’s device trains the link properly, and then suddenly applies polarity inversion to 1 lane. This is a clear violation of the spec and will cause the link to retrain. If this traffic is captured with the BitTracer tool, the user could easily identify this as the problem. Additionally, the portion of the traffic before and after the inversion could be exported into separate trace files and examined in the CATC Trace view. 

**930** 

**A endix A pp** 

## **Analysis overview** 

As you can see, different traffic views can be beneficial for debugging certain failure conditions. LeCroy supports import of PCIe traffic from many sources into its highly sophisticated PEtracer software. Whether the source is RTL simu‐ lation, an oscilloscope capture, or a dedicated protocol analyzer capture, PETracer has a rich set of traffic views and reports which allow the user to best understand the health and state of their PCIe link. 

## **Traffic generation** 

## **Pre-Silicon** 

For stimulating a PCI Express endpoint in simulation, dedicated verification IP can be purchased from a number of vendors. This IP will test for basic function‐ ality as well as perform a number of PCIe compliance checks. It is certainly in the interest of the ASIC developer to find and fix these issues before tapeout, and this is where the value of these tools comes from. If the PCIe design is implemented in an FPGA where mask costs are not an issue, it may be more cost effective to perform these compliance checks in hardware with a dedicated traffic generation tool such as the LeCroy PETrainer or LeCroy PTC card. 

## **Post-Silicon** 

## **Exerciser Card**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-2"></a>
## 99.2 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

To thoroughly test the PCIe compliance and overall robustness of a PCIe design post‐silicon, a dedicated Exerciser card such as the LeCroy PETrainer shown in Figure 13 on page 932 is used. This card allows the user to generate a wide range of compliant and non‐compliant traffic. For example, if you place your PCIe card in a standard motherboard, you may be limited in the size of the TLP packets it will see. A dedicated Exerciser card can generate TLP packets across the entire legal range of packet sizes. 

Secondly, if you would like to test that a card issues a NAK in response to a TLP with a bad LCRC, it would not possible with the card connected to compliant devices. They do not transmit bad packets. An Exerciser card can create a TLP with a bad LCRC, improper header values, or end the TLP with an EDB symbol. 

**931** 

## **PCI Ex ress Technolo p gy** 

If you would like to test that your card properly replay’s a packet when it receives a NAK, this can be done with an Exerciser. Perhaps you would like to issue 4 NAKs in a row to a certain TLP so that link recovery is initiated. This behavior is all quite easy to program into the exerciser card. 

The number of test cases and failure scenarios is limited only by the number of scripts you write. Once written, these scripts can be re‐used for testing new ver‐ sions of your design. The Analyzer SW can record these sessions and use script‐ ing to determine if the response was correct. A number of LeCroy customers have created large libraries of regression tests using these tools. 

_Figure A‐13: LeCroy Gen3 PETrainer Exerciser Card_ 

## **PTC card** 

The PCI SIG has published a specific list of compliance tests which all “Compli‐ ant” devices must pass. The LeCroy Protocol Test Card (PTC) is the hardware used to perform these tests at the PCI SIG Compliance workshops. Users can purchase a PTC card from LeCroy shown in Figure 14 on page 933 to pre‐test their devices to ensure they will pass PCI SIG compliance testing. 

The LeCroy PTC is used to test root complex or endpoint devices at x1 link widths. Link speeds can be either Gen1 or Gen2. 

**932** 

**A endix A pp** 

_Figure A‐14: LeCroy Gen2 Protocol Test Card (PTC)_ 

## **Conclusion** 

Today, the PCIe developer has access to a wide range of tools to help debug their PCIe design. Thanks to the wide adoption of the PCIe standard, many of these tools are designed specifically for PCIe debug and include features which address the challenges many PCIe devices face. 

For more information about the LeCroy PCIe tool offerings, please visit the LeCroy website www.lecroy.com 

**933** 

**PCI Ex ress Technolo p gy** 

**934** 

## _**Appendix B:**_ 

## _**Markets & Applications for PCI Express**_ 

Akber Kazmi (Senior Director Marketing, PLX Technology, Inc.) 

## **Introduction** 

Since its definition in the early 1990s, PCI has emerged as the most successful interconnect technology ever used in computers. Originally intended for per‐ sonal computer systems, the PCI architecture has expanded into virtually every computing platform category, including servers, storage, communications, and a wide range of embedded control applications. Most important, each advance‐ ment in PCI bus speed and width provided backward compatibility. 

As successful as the PCI architecture was, there was a limit to what could be accomplished with a multi‐drop, parallel, shared‐bus interconnect technology. A number of issues ‐‐ clock skew, high pin count, trace routing restrictions in printed circuit boards (PCB), bandwidth and latency requirements, physical scalability, and the need to support Quality of Service (QoS) within a system for a wide variety of applications ‐‐ lead to the definition of the PCI Expressª (PCIe) architecture. 

PCIe was the natural successor to PCI, and was developed to provide the advantages of a state‐of‐the‐art, high‐speed serial interconnect technology with a packet‐based layered architecture, but maintain backward‐compatibility with the large PCI software infrastructure. The key goal was to provide an opti‐ mized, universal interconnect solution for a wide variety of future platforms, including desktop, server, workstation, storage, communications, and embed‐ ded systems. 

**935** 

## **PCI Ex ress 3.0 Technolo p gy** 

After its introduction in 2001, PCIe has gone through three generations of enhancements. In the first generation (Gen1), signaling rate was set at 2.5 GT/s and later enhanced to 5 GT/s (Gen2) and eventually 8 GT/s (Gen3). The PCIe specification allows combining of 2, 4, 8, 12, 16 or 32 lanes into a single port. However, products available today do not support 12‐ and 32‐lane‐wide ports. It is important to note that all PCIe Gen2 and Gen3 devices are required to be backward‐compatible in speed with that of the previous generation. 

The industry has launched and has fully embraced PCIe Gen3 products, while at the same time the PCI Special Interest Group (PCI‐SIG) is analyzing signaling rate (speed) for Gen4. The goal for PCIe Gen4 is to double the speed of Gen3, to 16 GT/s. 

PCIe switches are available in an array of sizes, ranging from 3 to 96 lanes, and 3 to 24 ports where each port could be one, two, four, eight or 16 lanes wide. A Gen3 single lane would provide 1GB/s of bandwidth, while a 16‐lane port offers 16GB bandwidth in each direction. Additionally, PCIe switch vendors, such as PLX Technology, have added features and enhancement to their products that are not part of PCIe specifications but enable them to differentiate their prod‐ ucts and add value for the system designers. These features deliver ease of use, higher performance, fail‐over, error detection, error isolation, and field‐upgrad‐ ability. 

On‐chip features include non‐transparent (NT) bridging, peer‐to‐peer commu‐ nication, Hot‐Plug, direct memory access (DMA), and error checking/recovery. Additionally debug features such as packet generation, receiver‐eye measure‐ ment, traffic monitoring, and error injection in live traffic offer significant value to the designers, enabling early system bring‐up. Many of these features can also be used for run‐time performance improvements and monitoring. 

Features included in next generation of PCIe switches are: 

- **NT bridging:** Allows two hosts/CPUs to be connected to the same PCIe switch while electrically and logically isolated. The NT bridging functions is broadly used in systems requiring isolation of two active CPUs or two CPUs where one is active and other is passive. The NT functionality allows the exchange of heartbeat between the two host CPUs to enable fail‐over if one of them fails. 

**936** 

**Chapter : Appendix B: Markets & Applications for PCI** 

- **DMA:** An on‐chip DMA controller in a PCIe switch offers significant value to the designers as it enables them to spare CPU cycles to move data between peers and the CPU to/from I/Os. The CPU’s reduced effort in mov‐ ing data boosts overall performance of the system as the spared CPU cycles can be used to run applications rather than managing data I/O. 

- **Error Isolation:** Users can program triggers for certain error events and response by the switch. The response of switch can also be programmed to ignore, trigger a host interrupt, bring the port with errors down, or bring the entire switch down. 

- **Packet Generation:** Generally, it is difficult to generate traffic that saturates a PCIe port without the use of expensive packet generator equipment. PCIe switches now have the ability to saturate any PCIe port with desired traffic, such as transaction layer packets, to check the performance and robustness of the system. 

## **PCI Express IO Virtualization Solutions** 

The PCIe technology was initially defined as a single‐host interconnect technol‐ ogy but in last few years new standards have been developed that make PCIe suitable for multi‐host systems as a switch fabric technology for data centers and enterprise IT applications. The presence of native PCIe interfaces (ports) on x86 CPUs and servers platforms has enabled designers to use PCIe as backplane and fabric technology for small to mid‐size server clusters. 

In 2007, the PCI‐SIG released the Single‐Root I/O Virtualization (SR‐IOV) speci‐ fication that enables sharing of a single physical resource such as a network interface card or host bus adapter in a PCIe system among multiple virtual machines running on one host. This is the simplest approach to sharing resources or I/O devices among different applications or virtual machines. 

The PCI‐SIG followed by completing, in 2008, work on its Multi‐Root I/O Virtu‐ alization (MR‐IOV) specification that extends the use of PCIe technology from a single‐root domain to a multi‐root domain. The MR‐IOV specification enables the use of a single I/O device by multiple hosts and multiple system images simultaneously, as illustrated in Figure 0‐1 on page 938. This illustration shows a multi‐host environment where MR‐IOV capable NIC and HBA are shared across multiple servers or virtual machines via an MR‐IOV switch. 

**937** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 0‐1:  MR‐IOV Switch Usage_ 

In order to implement MR‐IOV specifications, three components of the system need to be developed – MR‐IOV PCIe switches, endpoints, and management software. All three of these components must be available simultaneously and work seamlessly. Unfortunately, four years after the specification was devel‐ oped, there is not a single silicon vendor that has MR‐IOV capable PCIe switch or end‐points. PCIe switch vendors are offering solutions that provide capabili‐ ties defined for MR‐IOV through vendor‐defined features and utilizing avail‐ able SR‐IOV end‐points. 

## **Multi-Root (MR) PCIe Switch Solution** 

PCIe switch vendors have created switches that offer implementation of multi‐ host function through non‐transparent bridging and multi‐root (MR) capabili‐ ties. These MR switches allow multiple hosts to be connected to a single switch‐ ing device, which can be portioned under user control in such a way that each host will be connected to a desired set of downstream ports of the switch. 

In the MR switches, one of the hosts acts as the master and assigns I/Os to other host ports. Each host operates independently of other hosts and controls down‐ stream devices in its domain. Figure 0‐2 on page 939 illustrates the internal architecture of an MR switch, in which particular sets of downstream ports are associated to particular host ports under management control. 

**938** 

**Chapter : Appendix B: Markets & Applications for PCI** 

_Figure 0‐2:  MR‐IOV Switch Internal Architecture_ 

## **PCIe Beyond Chip-to-Chip Interconnect** 

In early stages of PCIe deployments the technology was used as a chip‐to‐chip interconnect but now broad availability of PCIe interfaces on CPUs, chipsets and IOs and broad adoption of these components is pushing it beyond tradi‐ tional applications. In a new generation of applications, PCIe is used in system backplanes, switch fabrics, cabling systems, storage/IO expansion, IO virtual‐ ization, high‐performance computing (HPC), and server clusters. Figure 0‐3 on page 940 illustrates use of PCIe in a data center for high performance compute application where servers in a rack are clustered through a top‐of‐rack (TOR) PCIe switch fabric box. The TOR PCIe switch can be connected to the network through Ethernet and to local storage and compute resources through PCIe links. 

PCIe connections out‐side the box depend on PCIe copper or optical cables that the leader in the industry are introducing at lower cost. The PCIe TOR fabric is suitable for server/compute clustering and may replace InfiniBand as the eco‐ system for PCIe as fabric grows. 

**939** 

## **PCI Ex ress 3.0 Technolo p gy** 

_Figure 0‐3:  PCIe in a Data Center for HPC Applications_ 

## **SSD/Storage IO Expansion Boxes**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-3"></a>
## 99.3 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Recently, the industry has converged towards PCIe as the unified interconnect technology for enterprise storage and solid state drive (SSD) applications. The NVM HCI, an industry consortium, has released a specification called NVM Express (NVMe) that uses PCIe to provide the bandwidth needed for SSD applications. Additionally, a T10 committee has embarked on defining SCSI over PCIe (SOP) protocol to take advantage of PCIe technology capabilities for high‐performance storage applications. Furthermore, the SATA consortium recently announced that it would use PCIe as the interconnect for its next‐gen‐ eration SATA specification called SATA Express (SATAe). 

## **PCIe in SSD Modules for Servers** 

Traditionally, enterprise SSD modules have shipped with SAS, SATA and Fibre Channel interfaces but due to the above‐mentioned developments, a large majority of SSD controller, module and system suppliers have introduced prod‐ ucts with PCIe interfaces. Most SSD controllers peak their performance and capacity due to a heavy load of managing flash. In high‐performance applica‐ tions, multiple SSD controllers (or ASICs) are used and aggregated through a PCIe switch. Figure 0‐4 on page 941 shows a basic usage of a PCIe switch in an SSD add‐in card that applies to any card or module form factor. 

**940** 

**Chapter : Appendix B: Markets & Applications for PCI** 

_Figure 0‐4:  PCIe Switch Application in an SSD Add‐In Card_ 

For large data center applications, the SSD add‐in cards are installed in server motherboards as shown in Figure 0‐5 on page 941 and IO expansion boxes (Fig‐ ure 6) aggregated through PCIe switches. In server motherboard designs, PCIe switches are utilized to create more ports/slots that accommodate additional SSD modules to support the application’s needs. 

_Figure 0‐5:  Server Motherboard Use PCIe Switches_ 

In addition to providing connectivity, PCIe switches can be used for providing redundancy and failover through NT bridging and MR functionality. The MR switches support 1+N failover capability, in which one server/host communi‐ cates with N number of servers to check the heartbeat and initiate a failover if one of them fails. One of the servers illustrated in Figure 0‐6 on page 942 can be used as backup for the others in 1+N failover scheme. 

**941** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 0‐6:  Server Failover in 1 + N Failover Scheme_ 

## **Conclusion** 

PCIe interconnect technology has become a serious contender for many high‐ end applications beyond chip–to‐chip interconnect and is expected to be uti‐ lized in external I/O sharing, server clustering, I/O expansion and TOR switch‐ ing. The current 8 GT/s and next‐generation (Gen4) 16 GT/s line rates, the ability to aggregate multiple lanes in single high‐bandwidth ports, fail‐over capabili‐ ties, embedded DMA for data transfers, and IO sharing/virtualization provide capabilities that are at least equal to, if not superior to, interfaces such as Infini‐ Band and Ethernet. 

**942** 

## _**Appendix C:**_ 

_**Implementing Intelligent Adapters and Multi‐Host Systems With PCI Express Technology**_ 

## **Jack Regula, Danny Chi, Tim Canepa (PLX Technology, Inc. )** 

## **Introduction** 

Intelligent adapters, host failover mechanisms and multiprocessor systems are three usage models that are common today, and expected to become more prev‐ alent as market requirements for next generation systems. Despite the fact that each of these was developed in response to completely different market demands, all share the common requirement that systems that utilize them require multiple processors to co‐exist within the system. This appendix out‐ lines how PCI Express can address these needs through non‐transparent bridg‐ ing. 

Because of the widespread popularity of systems using intelligent adapters, host failover and multihost technologies, PCI Express silicon vendors must pro‐ vide a means to support them. This is actually a relatively low risk endeavor; given that PCI Express is software compatible with PCI, and PCI systems have long implemented distributed processing. The most obvious approach, and the one that PLX espouses, is to emulate the most popular implementation used in the PCI space for PCI Express. This strategy allows system designers to use not only a familiar implementation but one that is a proven methodology, and one 

**943** 

## **PCI Ex ress 3.0 Technolo p gy** 

that can provide significant software reuse as they migrate from PCI to PCI Express.This paper outlines how multiprocessor PCI Express systems will be implemented using industry standard practices established in the PCI para‐ digm. We first, however, will define the different usage models, and review the successful efforts in the PCI community to develop mechanisms to accommo‐ date these requirements. Finally, we will cover how PCI Express systems will utilize non‐transparent bridging to provide the functionality needed for these types of systems. 

## **Usage Models** 

## **Intelligent Adapters** 

Intelligent adapters are typically peripheral devices that use a local processor to offload tasks from the host. Examples of intelligent adapters include RAID con‐ trollers, modem cards, and content processing blades that perform tasks such as security and flow processing. Generally, these tasks are either computationally onerous or require significant I/O bandwidth if performed by the host. By add‐ ing a local processor to the endpoint, system designers can enjoy significant incremental performance. In the RAID market, a significant number of products utilize local intelligence for their I/O processing. 

Another example of intelligent adapters is an ecommerce blade. Because gen‐ eral purpose host processors are not optimized for the exponential mathematics necessary for SSL, utilizing a host processor to perform an SSL handshake typi‐ cally reduces system performance by over 90%. Furthermore, one of the requirements for the SSL handshake operation is a true random number genera‐ tor. Many general purpose processors do not have this feature, so it is actually difficult to perform SSL handshakes without dedicated hardware. Similar examples abound throughout the intelligent adapter marketplace; in fact, this usage model is so prevalent that for many applications it has become the de facto standard implementation. 

## **Host Failover** 

Host failover capabilities are designed into systems that require high availabil‐ ity. High availability has become an increasingly important requirement, espe‐ cially in storage and communication platforms. The only practical way to ensure that the overall system remains operational is to provide redundancy for 

**944** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

all components. Host failover systems typically include a host based system attached to several endpoints. In addition, a backup host is attached to the sys‐ tem and is configured to monitor the system status. When the primary host fails, the backup host processor must not only recognize the failure, but then take steps to assume primary control, remove the failed host to prevent addi‐ tional disruptions, reconstitute the system state, and continue the operation of the system without losing any data. 

## **Multiprocessor Systems** 

Multiprocessor systems provide greater processing bandwidth by allowing multiple computational engines to simultaneously work on sections of a com‐ plex problem. Unlike systems utilizing host failover, where the backup proces‐ sor is essentially idle, multiprocessor systems utilize all the engines to boost computational throughput. This enables a system to reach performance levels not possible by using only a single host processor. Multiprocessor systems typi‐ cally consist of two or more complete sub‐systems that can pass data between themselves via a special interconnect. A good example of a multihost system is a blade server chassis. Each blade is a complete subsystem, often replete with its own CPU, Direct Attached Storage, and I/O. 

## **The History Multi-Processor Implementations Using PCI** 

To better understand the implementation proposed for PCI Express, one needs to first understand the PCI implementation. 

PCI was originally defined in 1992 for personal computers. Because of the nature of PCs at that time, the protocol architects did not anticipate the need for multiprocessors. Therefore, they designed the system assuming that the host processor would enumerate the entire memory space. Obviously, if another pro‐ cessor is added, the system operation would fail as both processors would attempt to service the system requests. 

1Several methodologies were subsequently invented to accommodate the requirement for multiprocessor capabilities using PCI. The most popular imple‐ mentation, and the one discussed in this paper for PCI Express, is the use of non‐transparent bridging between the processing subsystems to isolate their memory spaces.[1] 

**945** 

## **PCI Ex ress 3.0 Technolo p gy** 

Because the host does not know the system topology when it is first powered up or reset, it must perform discovery to learn what devices are present and then map them into the memory space. To support standard discovery and configu‐ ration software, the PCI specification defines a standard format for Control and Status Registers (CSRs) of compliant devices. The standard PCI‐to‐PCI bridge CSR header, called a Type 1 header, includes primary, secondary and subordi‐ nate bus number registers that, when written by the host, define the CSR addresses of devices on the other side of the bridge. Bridges that employ a Type 1 CSR header are called transparent bridges. 

A Type 0 header is used for endpoints. A Type 0 CSR header includes base address registers (BARs) used to request memory or I/O apertures from the host. Both Type 1 and Type 0 headers include a class code register that indicates what kind of bridge or endpoint is represented, with further information avail‐ able in a subclass field and in device ID and vendor ID registers. The CSR header format and addressing rules allow the processor to search all the branches of a PCI hierarchy, from the host bridge down to each of its leaves, reading the class code registers of each device it finds as it proceeds, and assign‐ ing bus numbers as appropriate as it discovers PCI‐to‐PCI bridges along the way. At the completion of discovery, the host knows which devices are present and the memory and I/O space each device requires to function. These concepts are illustrated in Figure C ‐ 0‐1. 

1. Unless explicitly noted, the architecture for multiprocessor systems using PCI and PCI Express are similar and may be used interchangeably. 

**946** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

_Figure 0‐1: Enumeration Using Transparent Bridges_ 

## **Implementing Multi-host/Intelligent Adapters in PCI Express Base Systems** 

Up to this point, our discussions have been limited to one processor with one memory space. As technology progressed, system designers began developing end points with their own native processors built in. The problem that this caused was that both the host processor and the intelligent adapter would, upon power up or reset, attempt to enumerate the entire system, causing sys‐ tem conflict and ultimately a non‐functional system.[1] 

1. While we are using an intelligent endpoint as the examples, we should note that a similar problem exists for multi-host systems. 

**947** 

## **PCI Ex ress 3.0 Technolo p gy**

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-4"></a>
## 99.4 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

To get around this, architects designed non‐transparent bridges. A non‐trans‐ parent PCI‐to‐PCI Bridge, or PCI Express‐to‐PCI Express Bridge, is a bridge that exposes a Type 0 CSR header on both sides and forwards transactions from one side to the other with address translation, through apertures created by the BARs of those CSR headers. Because it exposes a Type 0 CSR header, the bridge appears to be an endpoint to discovery and configuration software, eliminating potential discovery software conflicts. Each BAR on each side of the bridge cre‐ ates a tunnel or window into the memory space on the other side of the bridge. To facilitate communication between the processing domains on each side, the non‐transparent bridge also typically includes doorbell registers to send inter‐ rupts from each side of the bridge to the other, and scratchpad registers accessi‐ ble from both sides. 

A non‐transparent bridge is functionally similar to a transparent bridge in that both provide a path between two independent PCI buses (or PCI Express links). The key difference is that when a non‐transparent bridge is used, devices on the downstream side of the bridge (relative to the system host) are not visible from the upstream side. This allows an intelligent controller on the downstream side to manage the devices in its local domain, while at the same time making them appear as a single device to the upstream controller. The path between the two buses allows the devices on the downstream side to transfer data directly to the upstream side of the bus without directly involving the intelligent controller in the data movement. Thus transactions are forwarded across the bus unfettered just as in a PCI‐to‐PCI Bridge, but the resources responsible are hidden from the host, which sees a single device. 

Because we now have two memory spaces, the PCI Express system needs to translate addresses of transactions that cross from one memory space to the other. This is accomplished via Translation and Limit Registers associated with the BAR. See “Address Translation” on page 958 for a detailed description; Fig‐ ure C‐0‐2 on page 949 provides a conceptual rendering of Direct Address Trans‐ lation. Address translation can be done by Direct Address Translation (essentially replacement of the data under a mask), table lookup, or by adding an offset to an address. Figure C‐0‐3 on page 950 shows Table Lookup Transla‐ tion used to create multiple windows spread across system memory space for packet originated in a local I/O processor’s domain, as well as Direct Address Translation used to create a single window in the opposite direction. 

**948** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

_Figure 0‐2: Direct Address Translation_ 

**949** 

**PCI Ex ress 3.0 Technolo p gy** 

_Figure 0‐3: Look Up Table Translation Creates Multiple Windows_ 

## **Example: Implementing Intelligent Adapters in a PCI Express Base System** 

Intelligent adapters will be pervasive in PCI Express systems, and will likely be the most widely used example of systems with “multiple processors”. 

Figure C‐0‐4 on page 951 illustrates how PCI Express systems will implement intelligent adapters. The system diagram consists of a system host, a root com‐ plex (the PCI Express version of a Northbridge), a three port switch, an example endpoint, and an intelligent add‐in card. Similar to the system architecture, the add‐in card contains a local host, a root complex, a three port switch, and an 

**950** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

example endpoint. However we should note two significant differences: the intelligent add‐in card contains an EEPROM, and one port of the switch con‐ tains a back to back non‐transparent bridge. 

_Figure 0‐4: Intelligent Adapters in PCI and PCI Express Systems_ 

Upon power up, the system host will begin enumerating to determine the topol‐ ogy. It will pass through the Root Complex and enter the first switch (Switch A). Upon entering the topmost port, it will see a transparent bridge, so it will know to continue to enumerate. The host will then poll the leftmost port and, upon finding a Type 0 CSR header, will consider it an endpoint and explore no deeper along that branch of the PCI hierarchy. The host will then use the information in the endpoint’s CSR header to configure base and limit registers in bridges and BARs in endpoints to complete the memory map for this branch of the system. 

**951** 

## **PCI Ex ress 3.0 Technolo p gy** 

The host will then explore the rightmost port of Switch A and read the CSR header registers associated with the top port of Switch B. Because this port is a non‐transparent bridge, the host finds a Type 0 CSR header. The host processor therefore believes that this is an endpoint and explores no deeper along that branch of the PCI hierarchy. The host reads the BARs of the top port of Switch B to determine the memory requirements for windows into the memory space on the other side of the bridge. The memory space requirements can be preloaded from an EEPROM into the BAR Setup Registers of Switch B’s non‐transparent port or can be configured by the processor that is local to Switch B prior to allowing the system host to complete discovery. 

Similar to the host processor power up sequence, the local host will also begin enumerating its own system. Like the system host processor, it will allocate memory for end points and continue to enumerate when it encounters a trans‐ parent bridge. When the host reaches the topmost port of Switch B, it sees a non‐transparent bridge with a Type 0 CSR header. Accordingly, it reads the BARs of the CSR header to determine the memory aperture requirements, then terminates discovery along this branch of its PCI tree. Again, the memory aper‐ ture information can be supplied by an EEPROM, or by the system host. 

Communication between the two processor domains is achieved via a mailbox system and doorbell interrupts. The doorbell facility allows each processor to send interrupts to the other. The mailbox facility is a set of dual ported registers that are both readable and writable by both processors. Shared memory mapped mechanisms via the BARs may also be used for inter‐processor com‐ munication. 

## **Example: Implementing Host Failover in a PCI Express System** 

Figure C‐0‐5 on page 953 illustrates how most PCI Express systems will imple‐ ment host failover. The primary host processor in this illustration is on the left side of the diagram, with the backup host on the right side of the diagram. Like most systems with which we are familiar, the host processor connects to a root complex. In turn, the root complex routes its traffic to the switch. In this exam‐ ple, the switch has two ports to end points in addition to the upstream port for the primary host we have just described. Furthermore, this system also has another processor, which is connected to the switch via another root complex. 

**952** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

_Figure 0‐5: Host Failover in PCI and PCI Express Systems_ 

The switch ports to both processors need to be configurable to behave either as a transparent bridge or a non‐transparent bridge. An EEPROM or strap pins on the switch can be used to initially bootstrap this configuration. 

Under normal operation, upon power up, the primary host begins to enumerate the system. In our example, as the primary host processor begins its discovery protocol through the fabric, it discovers the two end points, and their memory requirements, by sizing their BARs. When it gets to the upper right port, it finds a Type 0 CSR header. This signifies to the primary host processor that it should not attempt discovery on the far side of the associated switch port. As in the previous example, the BARs associated with the non‐transparent switch port may have been configured by EEPROM load prior to discovery or might be con‐ figured by software running on the local processor. 

**953** 

## **PCI Ex ress 3.0 Technolo p gy** 

Again, similar to the previous example, the backup processor powers up and begins to enumerate. In this example, the backup processor chipset consists of the root complex and the backup processor only. It discovers the non‐transpar‐ ent switch port and terminates its discovery there. It is keyed by EEPROM loaded Device ID and Vendor ID registers to load an appropriate driver. 

During the course of normal operation, the host processor performs all of its normal duties as it actively manages the system. In addition, it will send mes‐ sages to the backup processor called heartbeat messages. Heartbeat messages are indications of the continued good health of the originating processor. A heartbeat message might be as simple as a doorbell interrupt assertion, but typ‐ ically would include some data to reduce the possibility of a false positive. Checkpoint and journal messages are alternative approaches to providing the backup processor with a starting point, should it need to take over. In the jour‐ nal methodology, the backup is provided with a list or journal of completed transactions (in the application specific sense, not in the sense of bus transac‐ tions). In the checkpoint methodology, the backup is periodically provided with a complete system state from which it can restart if necessary. The heartbeat’s job is to provide the means by which the backup processor verifies that the host processor is still operational. Typically this data provides the latest activities and the state of all the peripherals. 

If the backup processor fails to receive timely heartbeat messages, it will begin assuming control. One of its first tasks is to demote the primary port to prevent the failed processor from interacting with the rest of the system. This is accom‐ plished by reprogramming the CSRs of the switch using a memory mapped view of the switch’s CSRs provided via a BAR in the non‐transparent port. To take over, the backup processor reverses the transparent/non‐transparent modes at both its port and the primary processor’s port and takes down the link to the primary processor. After cleaning up any transactions left in the queues or left in an incomplete state as a result of the host failure, the backup processor reconfigures the system so that it can serve as the host. Finally, it uses the data in the checkpoint or journal messages to restart the system. 

**954** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

## **Example: Implementing Dual Host in a PCI Express Base System** 

Figure C‐0‐6 on page 955 illustrates how PCI Express systems might implement a dual host system[1] . In this example, the leftmost blocks are a typically com‐ plete system, with the rightmost blocks being a separate subsystem. As previ‐ ously discussed, connecting the leftmost and rightmost diagram is a set of non‐ transparent bridges. 

_Figure 0‐6: Dual Host in a PCI and PCI Express System_ 

Upon power up, both processors will begin enumerating. As before, the hosts will search out the endpoints by reading the CSR and then allocate memory 

1. Back to back non-transparent (NT) ports are unnecessary but occur as a result of the use of identical single board computers for both hosts. A transparent backplane fabric would typically be interposed between the two NT ports. 

**955** 

## **PCI Ex ress 3.0 Technolo p gy** 

appropriately. When the hosts encounter the non‐transparent bridge port in each of their private switches, they will assume it is an endpoint and, using the data in the EEPROM, allocate resources. Both systems will use the doorbell and mailbox registers described above to communicate with each other.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-5"></a>
## 99.5 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

2 The dual‐host system model may be extended to a fully redundant dual star system by using additional switches to dual‐port the hosts and line cards into a redundant fabric as shown in Figure C‐0‐7 on page 957. This is particularly attractive to vendors who employ chassis based systems for their flexibility, scalability and reliability. 

Two host cards are shown. Host A is the primary host of Fabric A and the sec‐ ondary host of Fabric B. Similarly, Host B is the primary host of Fabric B and the secondary host of Fabric A. 

Each host is connected to the fabric it serves via a transparent bridge/switch port and to the fabric for which it provides only backup via a non‐transparent bridge/switch port. These non‐transparent ports are used for host‐to‐host com‐ munications and also support cross‐domain peer‐to‐peer transfers where address maps do not allow a more direct connection. 

**956** 

## **Chapter : Appendix C:  Implementing Intelligent Adapt-** 

_Figure 0‐7: Dual‐Star Fabric_ 

## **Summary** 

Through non‐transparent bridging, PCI Express Base offers vendors the ability to integrate intelligent adapters and multi‐host systems into their next genera‐ tion designs. This appendix demonstrated how these features will be deployed using de‐facto standard techniques adopted in the PCI environment and showed how they would be utilized for various applications. Because of this, we can expect this methodology to become the industry standard in the PCI Express paradigm. 

**957** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Address Translation** 

This section provides an in‐depth description of how systems that use non‐ transparent bridges communicate using address translation. We provide details about the mechanism by which systems determine not only the size of the mem‐ ory allocated, but also about how memory pointers are employed. Implementa‐ tions using both Direct Address Translation as well as Lookup Table Based Address Translation are discussed. By using the same standardized architec‐ tural implementation of non transparent bridging popularized in the PCI para‐ digm into the PCI Express environment, interconnect vendors can speed market adoption of PCI Express into markets requiring intelligent adapters, host failover and multihost capabilities. 

The transparent bridge uses base and limit registers in I/O space, non‐prefetch‐ able memory space, and prefetchable memory space to map transactions in the downstream direction across the bridge. All downstream devices are required to be mapped in contiguous address regions such that a single aperture in each space is sufficient. Upstream mapping is done via inverse decoding relative to the same registers. A transparent bridge does not translate the addresses of for‐ warded transactions/packets. 

The non‐transparent bridges use the standard set of BARs in their Type 0 CSR header to define apertures into the memory space on the other side of the bridge. There are two sets of BARs: one on the Primary side and one on the Sec‐ ondary. BARs define resource apertures that allow the forwarding of transac‐ tions to the opposite (other side) interface. 

For each BAR bridge there exists a set of associated control and setup registers usually writable from the other side of the bridge. Each BAR has a “setup” reg‐ ister, which defines the size and type of its aperture, and an address translation register. Some bars also have a limit register that can be used to restrict its aper‐ ture’s size. These registers need to be programmed prior to allowing access from outside the local subsystem. This is typically done by software running on a local processor or by loading the registers from EEPROM. 

In PCI Express, the Transaction ID fields of packets passing through these aper‐ tures are also translated to support Device ID routing. These Device IDs are used to route completions to non‐posted requests and ID routed messages. 

The transparent bridge forwards CSR transactions in the downstream direction according to the secondary and subordinate bus number registers, converting Type 1 CSRs to Type 0 CSRs as required. The non‐transparent bridge accepts only those CSR transactions addressed to it and returns an unsupported request response to all others. 

**958** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

## **Direct Address Translation** 

The addresses of all upstream and downstream transactions are translated (except BARs accessing CSRs). With the exception of the cases in the following two sections, addresses that are forwarded from one interface to the other are translated by adding a Base Address to their offset within the BAR that they landed in as seen in Figure C‐0‐8 on page 959. The BAR Base Translation Regis‐ ters are used to set up these base translations for the individual BARs. 

_Figure 0‐8: Direct Address Translation_ 

## **Lookup Table Based Address Translation** 

Following the de facto standard adopted by the PCI community, PCI Express should provide several BARs for the purposes of allocating resources. All BARs contain the memory allocation; however, in accordance with PCI industry con‐ ventions, BAR 0 contains the CSR information whereas BAR1 contains I/O information, BAR 2 and BAR 3 are utilized for Lookup Table Based Translation. BAR 4 and BAR 5 are utilized for Direct Address Translations. 

On the secondary side, BAR3 uses a special lookup table based address transla‐ tion for transactions that fall inside its window as seen in Figure C‐0‐9 on page 960. The lookup table provides more flexibility in secondary bus local addresses 

**959** 

**PCI Ex ress 3.0 Technolo p gy** 

to primary bus addresses. The location of the index field with the address bus is programmable to adjust aperture size. 

_Figure 0‐9: Lookup Table Based Translation_ 

## **Downstream BAR Limit Registers** 

The two downstream BARs on the primary side (BAR2/3 and BAR4/5) also have Limit registers, programmable from the local side, to further restrict the size of the window they expose, as seen in Figure C‐0‐10 on page 961. BARs can only be assigned memory resources in “power of two” granularity. The limit regis‐ ters provide a means to obtain better granularity by “capping” the size of the BAR within the “power of two” granularity. Only transactions below the Limit registers are forwarded to the secondary bus. Transactions above the limit are discarded or return 0xFFFFFFFF, or a master abort equivalent packet, on reads. 

**960** 

**Chapter : Appendix C:  Implementing Intelligent Adapt-** 

_Figure 0‐10: Use of Limit Register_ 

## **Forwarding 64bit Address Memory Transactions** 

Certain BARs can be configured to work in pairs to provide the base address and translation for transactions containing 64‐bit addresses. Transactions that hit within these 64‐bit BARs are forwarded using Direct Address Translation. As in the case of 32 bit transactions, when a memory transaction is forwarded from the primary to the secondary bus, the primary address can be mapped to another address in the secondary bus domain. The mapping is performed by substituting a new base address for the base of the original address. 

A 64‐bit BAR pair on the system side of the bridge is used to translate a window of 64‐bit addresses in packets originated on the system side of the bridge down below 232 in local space. 

**961** 

**PCI Ex ress 3.0 Technolo p gy** 

**962** 

## _**Appendix D:**_ 

## _**Locked Transactions**_ 

## **Introduction** 

Native PCI Express implementations do not support the old lock protocol. Sup‐ port for Locked transaction sequences only exists to support legacy device soft‐ ware executing on the host processor that performs a locked RMW (read‐ modify‐write) operation on a memory location in a legacy PCI device. This chapter defines the protocol defined by PCI Express for this legacy support of locked access sequences that target legacy devices. Failure to support lock may result in deadlocks. 

## **Background** 

PCI Express supports atomic or uninterrupted transaction sequences (usually described as an atomic read‐modify‐write sequence) for legacy devices only. Native PCIe devices don’t support this at all and will return a Completion with UR (Unsupported Request) status if they receive a locked Request. 

Locked operations consist of the basic RMW sequence, that is: 

1. One or more memory reads from the target location to obtain the value. 2. The modification of the data in a processor register. 

3. One or more writes to write the modified value back to the target memory location. 

This transaction sequence must be performed such that no other accesses are permitted to the target locations (or device) during the locked sequence. This requires blocking other transactions during the operation. This can potentially result in deadlocks and poor performance. 

**963** 

**PCI Express Technology** 

The devices required to support locked sequences are: 

- The Root Complex. 

- Any Switches in the path to a Legacy Device that may be the target of a locked transaction series. 

- PCIe‐to‐PCI Bridge or PCIe‐to‐PCI‐X Bridge. 

- Any Legacy Device whose driver issues locked transactions to memory residing within the legacy device. 

Locking in the PCI environment is achieved by the use of the LOCK# signal. The equivalent functionality in PCIe is accomplished by using a specific Request that emulates the LOCK# signal functionality. 

## **The PCI Express Lock Protocol** 

The only source of lock supported by PCI Express is the system processor acting through the Root Complex. A locked operation is performed between a Root Port and the Legacy Endpoint. In most systems, the legacy device is typically a PCI Express‐to‐PCI or PCI Express‐to‐PCI‐X bridge. Only one locked sequence at a time is supported for a given hierarchical path. 

Locked transactions are constrained to use only Traffic Class 0 and Virtual Channel 0. Transactions with other TC values that map to a VC other than zero are permitted to traverse the fabric without regard to the locked operation, but transactions that map to VC0 are affected by the lock rules described here. 

## **Lock Messages — The Virtual Lock Signal** 

PCI Express defines the following transactions that, together, act as a virtual wire and replace the LOCK# signal. 

- **Memory Read Lock Request** (MRdLk) — Originates a locked sequence. The first MRdLk transaction blocks other Requests in VC0 from reaching the target device. One or more of these locked read requests may be issued during the sequence. 

- **Memory Read Lock Completion with Data** (CplDLk) — Returns data and confirms that the path to the target is locked. A successful read Completion that returns data for the first Memory Read Lock request results in the path between the Root Complex and the target device being locked. That is, transactions traversing the same path from other ports are blocked from reaching either the root port or the target port. Transactions being routed in buffers for VC1‐VC7 are unaffected by the lock. 

**964** 

**A endix D pp** 

- **Memory Read Lock Completion without Data** (CplLK) — A Completion without a data payload indicates that the lock sequence cannot complete currently and the path remains unlocked. 

- **Unlock Message** — An unlock message is issued by the Root Complex from the locked root port. This message unlocks the path between the root port and the target port. 

## **The Lock Protocol Sequence — an Example** 

This section explains the PCI Express lock protocol by example. The example includes the following devices: 

- The Root Complex that initiates the Locked transaction series on behalf of the host processor. 

- A Switch in the path between the root port and targeted legacy endpoint. 

- A PCI Express‐to‐PCI Bridge in the path to the target. 

- The target PCI device who’s Device Driver initiated the locked RMW.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-6"></a>
## 99.6 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- A PCI Express endpoint is included to describe Switch behavior during lock. 

In this example, the locked operation completes normally. The steps that occur during the operation are described in the two sections that follow. 

## **The Memory Read Lock Operation** 

Figure E‐1 on page 967 illustrates the first step in the Locked transaction series (i.e., the initial memory read to obtain the semaphore): 

1. The CPU initiates the locked sequence (a Locked Memory Read) as a result of a driver executing a locked RMW instruction that targets a PCI target. 

2. The Root Port issues a Memory Read Lock Request from port 2. The Root Complex is always the source of a locked sequence. 

3. The Switch receives the lock request on its upstream port and forwards the request to the target egress port (3). The switch, upon forwarding the request to the egress port, must block all requests from ports other than the ingress port (1) from being sent from the egress port. 

4. A subsequent peer‐to‐peer transfer from the illustrated PCI Express end‐ point to the PCI bus (switch port 2 to switch port 3) would be blocked until the lock is cleared. Note that the lock is not yet established in the other direction. Transactions from the PCI Express endpoint could be sent to the Root Complex. 

**965** 

## **PCI Express Technology** 

5. The Memory Read Lock Request is sent from the Switch’s egress port to the PCI Express‐to‐PCI Bridge. This bridge will implement PCI lock semantics (See the MindShare book entitled _PCI System Architecture, Fourth Edition_ , for details regarding PCI lock). 

6. The bridge performs the Memory Read transaction on the PCI bus with the PCI LOCK# signal asserted. The target memory device returns the requested semaphore data to the bridge. 

7. Read data is returned to the Bridge and is delivered back to the Switch via a Memory Read Lock Completion with Data (CplDLk). 

8. The switch uses ID routing to return the packet upstream towards the host processor. When the CplDLk packet is forwarded to the upstream port of the Switch, it establishes a lock in the upstream direction to prevent traffic from other ports from being routed upstream. The PCI Express endpoint is completely blocked from sending any transaction to the Switch ports via the path of the locked operation. Note that transfers between Switch ports not involved in the locked operation would be permitted (not shown in this example). 

9. Upon detecting the CplDLk packet, the Root Complex knows that the lock has been established along the path between it and the target device, and the completion data is sent to the CPU. 

**966** 

**A endix D pp** 

_Figure D‐1: Lock Sequence Begins with Memory Read Lock Request_ 

**==> picture [368 x 388] intentionally omitted <==**

**----- Start of picture text -----**<br>
The CPU executes<br>the PCI target's device 1 CPU<br>drive that uses lock<br>Root Complex<br>Root Complex issues Root Complex receives<br>the MRdLk Request 2 9 CplDLk and returns data<br>to CPU<br>Switch forwards the Completion<br>Switch receives MRdLk and  1 to the upstream port (ID routing)<br>forwards it to the egress port (3). 3 8 and locks upstream port (1)<br>Switch blocks transactions from<br>Switch<br>other ports to egress port.<br>2 3<br>Bridge returns data using<br>PCIe endpoint issues a MenRd 4 a CplDLk transaction<br>Request targeting a PCI device,<br>7<br>but request is blocked 5<br>PCIe PCIe<br>Endpoint to<br>PCI Bridge<br>The Bridge receives the MRdLk.<br>Bridges support lock based on the<br>PCI-based requirements<br>6<br>Target The Bridge asserts LOCK and<br>Device performs the PCI Rd transaction<br>and the target returns the read data<br>MRdLk CplDLk<br>**----- End of picture text -----**<br>


## **Read Data Modified and Written to Target and Lock Completes** 

The device driver receives the semaphore value, alters it, and then initiates a memory write to update the semaphore within the memory of the legacy PCI device. Figure E‐2 on page 969 illustrates the write sequence followed by the 

**967** 

**PCI Express Technology** 

Root Complex’s transmission of the Unlock message that releases the lock: 

10. The Root Complex issues the Memory Write Request across the locked path to the target device. 

11. The Switch forwards the transaction to the target egress port (3). The mem‐ ory address of the Memory Write must be the same as the initial Memory Read request. 

12. The bridge forwards the transaction to the PCI bus. 

13. The target device receives the memory write data. 

14. Once the Memory Write transaction is sent from the Root Complex, it sends an Unlock message to instruct the Switches and any PCI/PCI‐X bridges in the locked path to release the lock. Note that the Root Complex presumes the operation has completed normally (because memory writes are posted and no Completion is returned to verify success). 

15. The Switch receives the Unlock message, unlocks its ports and forwards the message to the egress port that was locked to notify any other Switches and/ or bridges in the locked path that the lock must be cleared. 

16. Upon detecting the Unlock message, the bridge must also release the lock on the PCI bus. 

**968** 

**A endix D pp** 

_Figure D‐2: Lock Completes with Memory Write Followed by Unlock Message_ 

**==> picture [369 x 414] intentionally omitted <==**

**----- Start of picture text -----**<br>
The CPU executes<br>the PCI target's device CPU<br>drive that uses lock<br>Root Complex<br>Root Complex issues Root Complex sends<br>the Mem Write Request 10 14 Unlock message<br>1<br>Switch receives MemWt and  Switch receives the Unlock<br>forwards it to the egress port (3) 11 15 message and unlocks the<br>Switch ports in the locked path<br>2 3<br>Bridge releases lock<br>due to Unlock message<br>16<br>PCIe PCIe<br>12<br>Endpoint to<br>PCI Bridge<br>The Bridge receives the MemWt<br>performs the equivalent PCI<br>transaction<br>13<br>Target Target device receives the<br>Device PCI write data thereby<br>completing the operation<br>MemWt Unlock message<br>**----- End of picture text -----**<br>


**969** 

**PCI Express Technology** 

## **Notification of an Unsuccessful Lock** 

A locked transaction series is aborted when the initial Memory Read Lock Request receives a Completion packet with no data (CplLk). This means that the locked sequence must terminate because no data was returned. This could result from an error associated with the memory read transaction, or perhaps the target device is busy and cannot respond at this time. 

## **Summary of Locking Rules** 

Following is a list of ordering rules that apply to the Root Complex, Switches, and Bridges. 

## **Rules Related To the Initiation and Propagation of Locked Transactions** 

- Locked Requests which are completed with a status other than Successful Completion do not establish lock. 

- Regardless of the status of any of the Completions associated with a locked sequence, all locked sequences and attempted locked sequences must be terminated by the transmission of an Unlock Message. 

- MRdLk, CplDLk and Unlock semantics are allowed only for the default Traffic Class (TC0). 

- Only one locked transaction sequence attempt may be in progress at a given time within a single hierarchy domain. 

- Any device which is not involved in the locked sequence must ignore the Unlock Message. 

The initiation and propagation of a locked transaction sequence through the PCI Express fabric is performed as follows: 

- A locked transaction sequence is started with a MRdLk Request: 

   - Any successive reads associated with the locked transaction sequence must also use MRdLk Requests. 

   - The Completions for any successful MRdLk Request use the CplDLk Completion type, or the CPlLk Completion type for unsuccessful Requests. 

**970** 

**A endix D pp** 

- If any read associated with a locked sequence is completed unsuccessfully, the Requester must assume that the atomicity of the lock is no longer assured, and that the path between the Requester and Completer is no longer locked. 

- All writes associated with a locked sequence must use MWr Requests. 

- The Unlock Message is used to indicate the end of a locked sequence. A Switch propagates Unlock Messages through the locked Egress Port. 

- Upon receiving an Unlock Message, a legacy Endpoint or Bridge must unlock itself if it is in a locked state. If it is not locked, or if the Receiver is a PCI Express Endpoint or Bridge which does not support lock, the Unlock Message is ignored and discarded. 

## **Rules Related to Switches** 

Switches must detect transactions associated with locked sequences from other transactions to prevent other transactions from interfering with the lock and potentially causing deadlock. The following rules cover how this is done. Note that locked accesses are limited to TC0, which is always mapped to VC0. 

- When a Switch propagates a MRdLk Request from an Ingress Port to the Egress Port, it must block all Requests which map to the default Virtual Channel (VC0) from being propagated to the Egress Port. If a subsequent MRdLk Request is received at this Ingress Port addressing a different Egress Port, the behavior of the Switch is undefined. Note that this sort of split‐lock access is not supported by PCI Express and software must not cause such a locked access. System deadlock may result from such accesses. 

- When the CplDLk for the first MRdLk Request is returned, if the Comple‐ tion indicates a Successful Completion status, the Switch must block all Requests from all other Ports from being propagated to either of the Ports involved in the locked access, except for Requests which map to channels other than VC0 on the Egress Port. 

- The two Ports involved in the locked sequence must remain blocked until the Switch receives the Unlock Message (at the Ingress Port which received the initial MRdLk Request) 

   - The Unlock Message must be forwarded to the locked Egress Port. 

   - The Unlock Message may be broadcast to all other Ports. 

   - The Ingress Port is unblocked once the Unlock Message arrives, and the Egress Port(s) which were blocked are unblocked following the trans‐ mission of the Unlock Message out of the Egress Port(s). Ports that were not involved in the locked access are unaffected by the Unlock Message 

**971** 

**PCI Express Technology** 

## **Rules Related To PCI Express/PCI Bridges** 

The requirements for PCI Express/PCI Bridges are similar to those for Switches, except that, because these Bridges only use TC0 and VC0, all other traffic is blocked during the locked access. Requirements on the PCI bus side are described in the MindShare book, _PCI System Architecture, Fourth Edition._ 

## **Rules Related To the Root Complex** 

A Root Complex is permitted to support locked transactions as a Requester. If locked transactions are supported, a Root Complex must follow the rules already described to perform a locked access. The mechanism(s) used by the Root Complex to interface to the host processor’s FSB (Front‐Side Bus) are out‐ side the scope of the spec. 

## **Rules Related To Legacy Endpoints** 

Legacy Endpoints are permitted to support locked accesses, although their use is discouraged. If locked accesses are supported, legacy Endpoints must handle them as follows: 

- The legacy Endpoint becomes locked when it transmits the first Completion for the first read request of the locked transaction series access with a Suc‐ cessful Completion status: 

   - If the completion status is not Successful Completion, the legacy End‐ point does not become locked. 

   - Once locked, the legacy Endpoint must remain locked until it receives the Unlock Message.

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-7"></a>
## 99.7 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

- While locked, a legacy Endpoint must not issue any Requests using Traffic Classes which map to the default Virtual Channel (VC0). Note that this requirement applies to all possible sources of Requests within the Endpoint, in the case where there is more than one possible source of Requests. Requests may be issued using TCs which map to VCs other than VC0. 

## **Rules Related To PCI Express Endpoints** 

Native PCI Express Endpoints do not support lock. A PCI Express Endpoint must treat a MRdLk Request as an Unsupported Request. 

**972** 

## _**Glossary**_ 

|**Term**|**Definition**|
|---|---|
|128b/130b Encoding|This isn’t encoding in the same sense as 8b/10b. Instead,<br>the transmitter sends information in Blocks that consist<br>of 16 raw bytes in a row, preceded by a 2‐bit Sync field<br>that indicates whether the Block is to be considered as a<br>Data Block or an Ordered Set Block. This scheme was<br>introduced with Gen3, primarily to allow the Link band‐<br>width to double without doubling the clock rate. It pro‐<br>vides better bandwidth utilization but sacrifices some<br>benefits that 8b/10b provided for receivers.|
|8b/10b Encoding|Encoding scheme developed many years ago that’s used<br>in many serial transports today. It was designed to help<br>receivers recover the clock and data from the incoming<br>signal, but it also reduces available bandwidth at the<br>receiver by 20%. This scheme is used with the earlier<br>versions of PCIe: Gen1 and Gen2.|
|ACK/NAK Protocol|The Acknowledge/Negative Acknowledge mechanism<br>by which the Data Link Layer reports whether TLPs<br>have experienced any errors during transmission. If so, a<br>NAK is returned to the sender to request a replay of the<br>failed TLPs. If not, an ACK is returned to indicate that<br>one or more TLPs have arrived safely.|
|ACPI|Advanced Configuration and Power Interface. Specifies<br>the various system and device power states.|
|ACS|Access Control Services.|



**973** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|ARI|Alternative Routing‐ID Interpretation; optional feature<br>that allows Endpoints to have more Functions that the 8<br>allowed normally.|
|ASPM|Active State Power Management: When enabled, this<br>allows hardware to make changes to the Link power<br>state from L0 to L0s or L1 or both.|
|AtomicOps|Atomic Operations; three new Requests added with the<br>2.1 spec revision. These carry out multiple operations<br>that are guaranteed to take place without interruption<br>within the target device.|
|Bandwidth Management|Hardware‐initiated changes to Link speed or width for<br>the purpose of power conservation or reliability.|
|BAR|Base Address Register. Used by Functions to indicate the<br>type and size of their local memory and IO space.|
|Beacon|Low‐frequency in‐band signal used by Devices whose<br>main power has been shut off to signal that an event has<br>occurred for which they need to have the power<br>restored. This can be sent across the Link when the Link<br>is in the L2 state.|
|BER|Bit Error Rate or Ratio; a measure of signal integrity<br>based on the number of transmission bit errors seen<br>within a time period|
|Bit Lock|The process of acquiring the transmitter’s precise clock<br>frequency at the receiver. This is done in the CDR logic<br>and is one of the first steps in Link Training.|
|Block|The 130‐bit unit sent by a Gen3 transmitter, made up of a<br>2‐bit Sync Field followed by a group of 16 bytes.|



**974** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Block Lock|Finding the Block boundaries at the Receiver when<br>using 128b/130b encoding so as to recognize incoming<br>Blocks. The process involves three phases. First, search<br>the incoming stream for an EIEOS (Electrical Idle Exit<br>Ordered Set) and adjust the internal Block boundary to<br>match it. Next, search for the SDS (Start Data Stream)<br>Ordered Set. After that, the receiver is locked into the<br>Block boundary.|
|Bridge|A Function that acts as the interface between two buses.<br>Switches and the Root Complex will implement bridges<br>on their Ports to enable packet routing, and a bridge can<br>also be made to connect between different protocols,<br>such as between PCIe and PCI.|
|Byte Striping|Spreading the output byte stream across all available<br>Lanes. All available Lanes are used whenever sending<br>bytes.|
|CC|Credits Consumed: Number of credits already used by<br>the transmitter when calculating Flow Control.|
|CDR|Clock and Data Recovery logic used to recover the<br>Transmitter clock from the incoming bit stream and then<br>sample the bits to recognize patterns. For 8b/10b, that<br>pattern, found in the COM, FTS, and EIEOS symbols,<br>allows the logic to acquire Symbol Lock. For 128b/130b<br>the EIEOS sequence is used to acquire Block Lock by<br>going through the three phases of locking.|
|Character|Term used to describe the 8‐bit values to be communi‐<br>cated between Link neighbors. For Gen1 and Gen2, these<br>are a mix of ordinary data bytes (labeled as D characters)<br>and special control values (labeled as K characters). For<br>Gen3 there are no control characters because 8b/10b<br>encoding is no longer used. In that case, the characters<br>all appear as data bytes.|



**975** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|CL|Credit Limit: Flow Control credits seen as available from<br>the transmitter’s perspective. Checked to verify whether<br>enough credits are available to send a TLP.|
|Control Character|These are special characters (labeled as “K” characters)<br>used in 8b/10b encoding that facilitate Link training and<br>Ordered Sets. They are not used in Gen3, where there is<br>no distinction between characters.|
|Correctable Errors|Errors that are corrected automatically by hardware and<br>don’t require software attention.|
|CR|Credits Required ‐ this is the sum of CC and PTLP.|
|CRC|Cyclic Redundancy Code; added to TLPs and DLLPs to<br>allow verifying error‐free transmission. The name means<br>that the patterns are cyclic in nature and are redundant<br>(they don’t add any extra information). The codes don’t<br>contain enough information to permit automatic error<br>correction, but provide robust error detection.|
|Cut‐Through Mode|Mechanism by which a Switch allows a TLP to pass<br>through, forwarded from an ingress Port to an egress<br>Port without storing it first to check for errors. This<br>involves a risk, since the TLP may be found to have<br>errors after part of it has already been forwarded to the<br>egress Port. In that case, the end of the packet is modi‐<br>fied in the Data Link Layer to have an LCRC value that is<br>inverted from what it should be, and also modified at<br>the Physical Layer to have an End Bad (EDB) framing<br>symbol for 8b/10b encoding or an EDB token for 128b/<br>130b encoding. The combination tells the receiver that<br>the packet has been nullified and should be discarded<br>without sending an ACK/NAK response.|
|Data Characters|Characters (labeled as “D” characters) that represent<br>ordinary data and are distinguished from control char‐<br>acters in 8b/10b. For Gen3, there is no distinction<br>between characters.|



**976** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Data Stream|The flow of data Blocks for Gen3 operation. The stream<br>is entered by an SDS (Start of Data Stream Ordered Set)<br>and exited with an EDS (End of Data Stream token).<br>During a Data Stream, only data Blocks or the SOS are<br>expected. When any other Ordered Sets are needed, the<br>Data Stream must be exited and only re‐entered when<br>more data Blocks are ready to send. Starting a Data<br>Stream is equivalent to entering the L0 Link state, since<br>Ordered Sets are only sent while in other LTSSM states,<br>like Recovery.|
|De‐emphasis|The process of reducing the transmitter voltage for<br>repeated bits in a stream. This has the effect of de‐<br>emphasizing the low‐frequency components of the sig‐<br>nal that are known to cause trouble in a transmission<br>medium and thus improves the signal integrity at the<br>receiver.|
|Digest|Another name for the ECRC (End‐to‐End CRC) value<br>that can optionally be appended to a TLP when it’s cre‐<br>ated in the Transaction Layer.|
|DLCMSM|Data Link Control and Management State Machine;<br>manages the Link Layer training process (which is pri‐<br>marily Flow Control initialization).|
|DLLP|Data Link Layer Packet. These are created in the Data<br>Link Layer and are forwarded to the Physical Layer but<br>are not seen by the Transaction Layer.|
|DPA|Dynamic Power Allocation; a new set of configuration<br>registers with the 2.1 spec revision that defines 32 power<br>substates under the D0 device power state, making it<br>easier for software to control device power options.|
|DSP (Downstream Port)|Port that faces downstream, like a Root Port or a Switch<br>Downstream Port. This distinction is meaningful in the<br>LTSSM because the Ports have assigned roles during<br>some states.|



**977** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|ECRC|End‐to‐End CRC value, optionally appended to a TLP<br>when it’s created in the Transaction Layer. This enables a<br>receiver to verify reliable packet transport from source to<br>destination, regardless of how many Links were crossed<br>to get there.|
|Egress Port|Port that has outgoing traffic.|
|Elastic Buffer|Part of the CDR logic, this buffer enables the receiver to<br>compensate for the difference between the transmitter<br>and receiver clocks.|
|EMI|Electro‐Magnetic Interference: the emitted electrical<br>noise from a system. For PCIe, both SSC and scrambling<br>are used to attack it.|
|Endpoint|PCIe Function that is at the bottom of the PCI Inverted‐<br>Tree structure.|
|Enumeration|The process of system discovery in which software reads<br>all of the expected configuration locations to learn which<br>PCI‐configurable Functions are visible and thus present<br>in the system.|
|Equalization|The process of adjusting Tx and Rx values to compen‐<br>sate for actual or expected signal distortion through the<br>transmission media. For Gen1 and Gen2, this takes the<br>form of Tx De‐emphasis. For Gen3, an active evaluation<br>process is introduced to test the signaling environment<br>and adjust the Tx settings accordingly, and optional Rx<br>equalization is mentioned.|
|Flow Control|Mechanism by which transmitters avoid the risk of hav‐<br>ing packets rejected at a receiver due to lack of buffer<br>space. The receiver sends periodic updates about avail‐<br>able buffer space and the transmitter verifies that<br>enough is available before attempting to send a packet.|
|FLR|Function‐Level Reset|



**978** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Framing Symbols|The “start” and “end” control characters used in 8b/10b<br>encoding that indicate the boundaries of a TLP or DLLP.|
|Gen1|Generation 1, meaning designs created to be compliant<br>with the 1.x version of the PCIe spec.|
|Gen1, Gen2, Gen3|Abbreviations for the revisions of the PCIe spec. Gen1 =<br>rev 1.x, Gen2 = rev 2.x, and Gen3 = rev 3.0|
|Gen2|Generation 2, meaning designs created to be compliant<br>with the 2.x version of the PCIe spec.|
|Gen3|Generation 3, meaning designs created to be compliant<br>with the 3.x version of the PCIe spec.|
|IDO|ID‐based Ordering; when enabled, this allows TLPs<br>from different Requesters to be forwarded out of order<br>with respect to each other. The goal is to improve latency<br>and performance.|
|Implicit Routing|TLPs whose routing is understood without reference to<br>an address or ID. Only Message requests have the option<br>to use this type of routing.|
|Ingress Port|Port that has incoming traffic.|
|ISI|Inter‐Symbol Interference; the effect on one bit time that<br>is caused by the recent bits that preceded it.|

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-8"></a>
## 99.8 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|Lane|The two differential pairs that allow a transmit and<br>receive path of one bit between two Ports. A Link can<br>consist of just one Lane or it may contain as many as 32<br>Lanes.|
|Lane‐to‐Lane Skew|Difference in arrival times for bits on different Lanes.<br>Receivers are required to detect this and correct it inter‐<br>nally.|
|Legacy Endpoint|An Endpoint that carries any of three legacy items for‐<br>ward: support for IO transactions, support for local 32‐<br>bit‐only prefetchable memory space, or support for the<br>locked transactions.|



**979** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|LFSR|Linear‐Feedback Shift Register; creates a pseudo‐ran‐<br>dom pattern used to facilitate scrambling.|
|Link|Interface between two Ports, made up of one or more<br>Lanes.|
|LTR|Latency‐Tolerance Reporting; mechanism that allows<br>devices to report to the system how quickly they need to<br>get service when they send a Request. Longer latencies<br>afford more power management options to the system.|
|LTSSM|Link Training and Status State Machine; manages the<br>training process for the Physical Layer.|
|Non‐posted Request|A Request that expects to receive a Completion in<br>response. For example, any read request would be non‐<br>posted.|
|Non‐prefetchable<br>Memory|Memory that exhibits side effects when read. For exam‐<br>ple, a status register that automatically self‐clears when<br>read. Such data is not safe to prefetch since, if the<br>requester never requested the data and it was discarded,<br>it would be lost to the system. This was an important<br>distinction for PCI bridges, which had to guess about the<br>data size on reads. If they knew it was safe to specula‐<br>tively read ahead in the memory space, they could guess<br>a larger number and achieve better efficiency. The dis‐<br>tinction is much less interesting for PCIe, since the exact<br>byte count for a transfer is included in the TLP, but<br>maintaining it allows backward compatibility.|
|Nullified Packet|When a transmitter recognizes that a packet has an error<br>and should not have been sent, the packet can be “nulli‐<br>fied”, meaning it should be discarded and the receiver<br>should behave as if it had never been sent. This problem<br>can arise when using “cut‐through” operation on a<br>Switch.|



**980** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|OBFF|Optimized Buffer Flush and Fill; mechanism that allows<br>the system to tell devices about the best times to initiate<br>traffic. If devices send requests during optimal times<br>and not during other times system power management<br>will be improved.|
|Ordered Sets|Groups of Symbols sent as Physical Layer communica‐<br>tion for Lane management. These often consist of just<br>control characters for 8b/10b encoding. They are created<br>in the Physical Layer of the sender and consumed in the<br>Physical Layer of the receiver without being visible to<br>the other layers at all.|
|PCI|Peripheral Component Interface. Designed to replace<br>earlier bus designs used in PCs, such as ISA.|
|PCI‐X|PCI eXtended. Designed to correct the shortcomings of<br>PCI and enable higher speeds.|
|PME|Power Management Event; message from a device indi‐<br>cating that power‐related service is needed.|
|Poisoned TLP|Packet whose data payload was known to be bad when<br>it was created. Sending the packet with bad data can be<br>helpful as an aid to diagnosing the problem and deter‐<br>mining a solution for it.|
|Polarity Inversion|The receiver’s signal polarity is permitted to be con‐<br>nected backwards to support cases when doing so<br>would simplify board layout. The receiver is required to<br>detect this condition and internally invert the signal to<br>correct it during Link Training.|
|Port|Input/output interface to a PCIe Link.|
|Posted Request|A Request packet for which no completion is expected.<br>There are only two such requests defined by the spec:<br>Memory Writes and Messages.|



**981** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|Prefetchable Memory|Memory that has no side‐effects as a result of being read.<br>That property makes it safe to prefetch since, if it’s dis‐<br>carded by the intermediate buffer, it can always be read<br>again later if needed. This was an important distinction<br>for PCI bridges, which had to guess about the data size<br>on reads. Prefetchable space allowed speculatively read‐<br>ing more data and gave a chance for better efficiency.<br>The distinction is much less interesting for PCIe, since<br>the exact byte count for a transfer is included in the TLP,<br>but maintaining it allows backward compatibility.|
|PTLP|Pending TLP ‐ Flow Control credits needed to send the<br>current TLP.|
|QoS|Quality of Service; the ability of the PCIe topology to<br>assign different priorities for different packets. This<br>could just mean giving preference to packets at arbitra‐<br>tion points, but in more complex systems, it allows mak‐<br>ing bandwidth and latency guarantees for packets.|
|Requester ID|The configuration address of the Requester for a transac‐<br>tion, meaning the BDF (Bus, Device, and Function num‐<br>ber) that corresponds to it. This will be used by the<br>Completer as the return address for the resulting com‐<br>pletion packet.|
|Root Complex|The components that act as the interface between the<br>CPU cores in the system and the PCIe topology. This can<br>consist of one or more chips and may be simple or com‐<br>plex. From the PCIe perspective, it serves as the root of<br>the inverted tree structure that backward‐compatibility<br>with PCI demands.|
|Run Length|The number of consecutive ones or zeros in a row. For<br>8b/10b encoding the run length is limited to 5 bits. For<br>128b/130b, there is no defined limit, but the modified<br>scrambling scheme it uses is intended to compensate for<br>that.|



**982** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Scrambling|The process of randomizing the output bit stream to<br>avoid repeated patterns on the Link and thus reduce<br>EMI. Scrambling can be turned off for Gen1 and Gen2 to<br>allow specifying patterns on the Link, but it cannot be<br>turned off for Gen3 because it does other work at that<br>speed and the Link is not expected to be able to work<br>reliably without it.|
|SOS|Skip Ordered Set ‐ used to compensate for the slight fre‐<br>quency difference between Tx and Rx.|
|SSC|Spread‐Spectrum Clocking. This is a method of reducing<br>EMI in a system by allowing the clock frequency to vary<br>back and forth across an allowed range. This spreads the<br>emitted energy across a wider range of frequencies and<br>thus avoids the problem of having too much EMI energy<br>concentrated in one particular frequency.|
|Sticky Bits|Status bits whose value survives a reset. This characteris‐<br>tic is useful for maintaining status information when<br>errors are detected by a Function downstream of a Link<br>that is no longer operating correctly. The failed Link<br>must be reset to gain access to the downstream Func‐<br>tions, and the error status information in its registers<br>must survive that reset to be available to software.|
|Switch|A device containing multiple Downstream Ports and<br>one Upstream Port that is able to route traffic between its<br>Ports.|
|Symbol|Encoded unit sent across the Link. For 8b/10b these are<br>the 10‐bit values that result from encoding, while for<br>128b/130b they’re 8‐bit values.|
|Symbol Lock|Finding the Symbol boundaries at the Receiver when<br>using 8b/10b encoding so as to recognize incoming Sym‐<br>bols and thus the contents of packets.|
|Symbol time|The time it takes to send one symbol across the Link ‐<br>4ns for Gen1, 2ns for Gen2, and 1ns for Gen3.|



**983** 

## **PCI Ex ress Technolo p gy** 

|**Term**|**Definition**|
|---|---|
|TLP|Transaction Layer Packet. These are created in the Trans‐<br>action Layer and passed through the other layers.|
|Token|Identifier of the type of information being delivered dur‐<br>ing a Data Stream when operating at Gen3 speed.|
|TPH|TLP Processing Hints; these help system routing agents<br>make choices to improve latency and traffic congestion.|
|UI|Unit Interval; the time it takes to send one bit across the<br>Link ‐ 0.4ns for Gen1, 0.2ns for Gen2, 0.125ns for Gen3|
|Uncorrectable Errors|Errors that can’t be corrected by hardware and thus will<br>ordinarily require software attention to resolve. These<br>are divided into Fatal errors ‐ those that render further<br>Link operation unreliable, and Non‐fatal errors ‐ those<br>that do not affect the Link operation in spite of the prob‐<br>lem that was detected.|
|USP|Upstream Port, meaning a Port that faces upstream, as<br>for an Endpoint or a Switch Upstream Port. This distinc‐<br>tion is meaningful in the LTSSM because the Ports have<br>assigned roles during Configuration and Recovery.|



**984** 

**Glossar y** 

|**Term**|**Definition**|
|---|---|
|Variables|A number of flags are used to communicate events and<br>status between hardware layers. These are specific to<br>state transitions in the hardware are not usually visible<br>to software. Some examples:<br>—<br>LinkUp ‐ Indication from the Physical Layer to the<br>Data Link Layer that training has completed and<br>the Physical Layer is now operational.<br>—<br>idle_to_rlock_transitioned ‐ This counter tracks<br>the number of times the LTSSM has transitioned<br>from Configuration.Idle to the Recovery.RcvrLock<br>state. Any time the process of recognizing TS2s to<br>leave Configuration doesn’t work, the LTSSM tran‐<br>sitions to Recovery to take appropriate steps. If it<br>still doesn’t work after 256 passes through Recovery<br>(counter reaches FFh), then it goes back to Detect to<br>start over. It may be that some Lanes are not work‐<br>ing.|
|WAKE#|Side‐band pin used to signal to the system that the<br>power should be restored. It’s used instead of the Beacon<br>in systems where power conservation is an important<br>consideration.|



**985** 

**PCI Ex ress Technolo p gy** 

**986** 

## _**Numerics**_ 

128b/130b 43 128b/130b Encoding 973 1x Packet Format 374, 375 3DW Header 152 3-Tap Transmitter Equalization 585 4DW Headers 152 4x Packet Format 374 8.0 GT/s 410 8b/10b 42 8b/10b Decoder 367 8b/10b Encoder 366 8b/10b Encoding 973 

## _**A**_ 

AC Coupling 468 ACK 318 Ack 311 ACK DLLP 75, 312 ACK/NAK DLLP 312 ACK/NAK Latency 328 ACK/NAK Protocol 318, 320, 329, 973 Ack/Nak Protocol 74 ACKD_SEQ Count 323 ACKNAK_Latency_Timer 328, 343 ACPI 711, 973 ACPI Driver 706 ACPI Machine Language 712 ACPI Source Language 712 ACPI spec 705 ACPI tables 712 ACS 973 Active State Power Management 405, 735 Address Routing 158 Address Space 121 Address Translation 958, 959 Advanced Correctable Error Reporting 690 Advanced Correctable Error Status 689 Advanced Correctable Errors 688 Advanced Error Reporting 685 Advanced Source ID Register 697 Advanced Uncorrectable Error Handling 691 Advanced Uncorrectable Error Status 691 Aggregate Bandwidth 408 Alternative Routing-ID Interpretation 909 AML 712 AML token interpreter 712 Arbitration 20, 270 Arbor 117 Architecture Overview 39 ARI 909, 974 ASL 712 ASPM 735, 742, 910, 974 ASPM Exit Latency 756, 757 Assert_INTx messages 806 Async Notice of Slot Status Change 876 

AtomicOp 150 AtomicOps 897, 974 Attention Button 854, 862 Attention Indicator 854, 859 Aux_Current field 726 

## _**B**_

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

<a id="sec-99-9"></a>
## 99.9 Appendices | 附录

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

Bandwidth 42 Bandwidth Congestion 281 Bandwidth Management 974 BAR 126, 960, 974 Base Address Registers 126 Base and Limit Registers 136 BDF 85 Beacon 483, 772, 974 BER 974 BIOS 712, 853 Bit Lock 78, 395, 507, 742, 974 Bit Tracer 929 Block 974 Block Alignment 435 Block Encoding 410 Block Lock 507, 975 Boost 476 Bridge 975 Bus 85 Bus Master 20 Bus Number register 93 Byte Count Modified 201 Byte Enables 181 Byte Striping 371, 372, 373, 975 byte striping 371 Byte Striping logic 365 Byte Un-Striping 402 _**C**_ Capabilities List bit 818 Capabilities Pointer register 713 Capability ID 713, 814 Capability Structures 88 Card Connector Power Switching Logic 854 Card Insertion 855 Card Insertion Procedure 857 Card Present 854 Card Removal 855 Card Removal Procedure 856 Card Reset Logic 854 CC 975 CDR 435, 437, 975 Character 79, 366, 975 CL 976 Class driver 706 Clock Requirements 452 Code Violation 400 Coefficients 584 Cold Reset 834 

COM 386 Common-Mode Noise Rejection 452 Completer 33 Completer Abort 664 Completion Packet 197 Completion Status 200 Completion Time-out 665 Completion TLP 184 Completions 196, 218 Compliance Pattern 537 Compliance Pattern - 8b/10b 529 Configuration 85 Configuration Address Port 92, 93 Configuration Address Space 88 Configuration Cycle Generation 26 Configuration Data Port 92, 93 Configuration Headers 50 Configuration Read 151 Configuration Read Access 104 Configuration Register Space 27, 89 Configuration Registers 90 Configuration Request Packet 193 Configuration Requests 99, 192 Configuration Space 122 Configuration State 520, 540 Configuration Status Register 676 Configuration Status register 713 Configuration Transactions 91 Configuration Write 151 Configuration.Complete 562 Configuration.Idle 566 Configuration.Lanenum.Accept 560 Configuration.Lanenum.Wait 559 Configuration.Linkwidth.Accept 558 Configuration.Linkwidth.Start 553 Congestion Avoidance 897 Continuous-Time Linear Equalization 493 Control Character 976 Control Character Encoding 386 Control Method 712 Conventional Reset 834 Correctable Errors 651, 976 CR 976 CRC 976 CRD 383 Credit Allocated Count 229 Credit Limit counter 228 CREDIT_ALLOCATED 229 Credits Consumed counter 228 Credits Received Counter 229 CREDITS_RECEIVED 229 CTLE 493, 494 Current Running Disparity 383 Cursor Coefficient 584 Cut-Through 354 Cut-Through Mode 976 

_**D**_ D0 709, 710, 714, 734 D0 Active 714 D0 Uninitialized 714 D1 709, 710, 716, 734 D1_Support bit 725 D2 709, 710, 717, 734 D2_Support bit 725 D3 709, 710, 719 D3cold 721, 734 D3hot 719, 734 Data Characters 976 Data Link Layer 55, 72 Data Link Layer Packet 72 Data Link Layer Packet Format 310 Data Link Layer Packets 73 Data Poisoning 660 Data Register 731 Data Stream 977 Data_Scale field 729 Data_Select field 729 DC Common Mode 462 DC Common Mode Voltage 466 DC Common-Mode Voltage 467 Deadlock Avoidance 303 Deassert_INTx messages 806 Debugging PCIe Traffic 917 Decision Feedback Equalization 495 De-emphasis 450, 468, 469, 471, 476, 977 De-Scrambler 367 Deserializer 395 De-Skew 399 Detect State 519, 522 Detect.Active 524 Detect.Quiet 523 Device 85 Device Capabilities 2 Register 899 Device Capabilities Register 873 Device Context 709 Device Core 59 Device core 55 Device Driver 706 device driver 853 Device Layers 54 Device PM States 713 device PM states 709 Device Status Register 681 Device-Specific Initialization (DSI) bit 727 DFE 493, 495, 497 Differential Driver 389 Differential Receiver 393, 435, 451 Differential Signaling 463 Differential Signals 44 Differential Transmitter 451 Digest 180, 977 Direct Address Translation 949 

Disable State 521, 613 Discrete Time Linear Equalizer 493 Discrete-Time Linear Equalizer 494 Disparity 383 Disparity Error Detection 400 DLCMSM 977 DLE 493, 494 DLL 437 DLLP 73, 170, 238, 308, 311, 977 DLLP Elements 307 DMA 937 DPA 910, 977 Driver Characteristics 489 DSI bit 727 DSP 977 D-State Transitions 722 Dual Simplex 363 Dual-Simplex 40 Dual-Star Fabric 957 Dynamic Bandwidth Changes 618 Dynamic Link Speed Changes 619 Dynamic Link Width Changes 629 Dynamic Power Allocation 910 

## _**E**_ 

ECRC 63, 180, 978 ECRC Generation and Checking 657 EDB 373, 387 Egress Port 978 EIE 387 EIEOS 389, 739, 740 EIOS 388, 737 Elastic Buffer 366, 435, 978 Electrical Idle 388, 736, 738, 741 Electrical Idle Exit Ordered Set 389 Electrical Idle Ordered Set 388 EMI 77, 978 Encoding 410 END 373, 387 Endpoint 978 End-to-End CRC 180 Enhanced Configuration Access Mechanism 96 Enumeration 51, 104, 978 Equalization 474, 978 Equalization - Phase 0 578 Equalization - Phase 1 581 Equalization - Phase 2 583 Equalization - Phase 3 586 Equalization Control 513 Equalization Control Registers 579 Equalizer 475 Equalizer Coefficients 479 Error Classifications 651 Error Handling 282, 699 Error Isolation 937 Error Messages 209, 668 

ESD 459 ESD standards 448 Exerciser Card 931 Extended Configuration Space 89 Eye Diagram 486 

## _**F**_ 

Failover 942, 944, 952 FC Initialization 223 FC Initialization Sequence 223 FC_Init1 224 FC_Init2 225 FC_Update 238 First DW Byte Enables 178, 181 Flow Control 72, 76, 215, 217, 299, 928, 978 Flow Control Buffer 217, 229 Flow Control Buffers 217 Flow Control Credits 216, 219 Flow Control Elements 227, 231 Flow Control Initialization 227, 230, 237 Flow Control Packet 239 Flow Control Packet Format 314 Flow Control Update Frequency 239 Flow Control Updates 237 FLR 842, 844, 845, 978 Flying Lead Probe 924 Format Field 179 Framing Symbols 171, 979 FTS 387 FTS Ordered Set 388 FTSOS 388 Function 85 Function Level Reset 842, 843 Function PM State Transitions 722 Function State Transition Delays 724 Fundamental Reset 834 

## _**G**_ 

Gen1 43, 77, 979 Gen2 43, 77, 979 Gen3 44, 77, 407, 979 Gen3 products 936 

## _**H**_ 

handler 712 Hardware Based Fixed Arbitration 256 Hardware Fixed VC Arbitration 257 Hardware-Fixed Port Arbitration 265 Header Type 0 29 Header Type 1 28 Header Type/Format Field 178 High Speed Signaling 451 host/PCI bridge 94 Hot Plug 847, 852 

Hot Plug Controller 863 Hot Plug Elements 852 Hot Plug Messages 211 Hot Reset 839 Hot Reset State 521, 612 Hot-Plug 116, 853 Hot-Plug Controller 853, 864 hot-plug primitives 874 Hot-Plug Service 852 Hot-Plug System Driver 852 HPC Applications 940 Hub Link 32 

## _**I**_ 

ID Based Ordering 301 ID Routing 155 ID-based Ordering 301, 909, 979 IDL 387 IDO 301, 302, 909, 979 IEEE 1394 Bus Driver 711 Ignored Messages 211 Implicit Routing 148, 979 In-band Reset 837 Infinite Credits 221 Infinite Flow Control Credits 219 Ingress Port 979 InitFC1-Cpl 312 InitFC1-NP 311 InitFC1-P DLLP 311 InitFC2-Cpl 312 InitFC2-NP 312 InitFC2-P 312 Intelligent Adapters 943, 944, 951 Internal Error Reporting 911 Interrupt Disable 803 Interrupt Latency 829 interrupt latency 829 Interrupt Line Register 802 Interrupt Pin Register 801 Interrupt Status 804 Inter-symbol Interference 469 INTx Interrupt Messages 206 INTx Interrupt Signaling 206 INTx Message Format 807 INTx# Pins 800 INTx# Signaling 803 IO 126 IO Address Spaces 122 IO Range 141 IO Read 151 IO Requests 184 IO Virtualization 937 IO Write 151 ISI 979 Isochronous Packets 279 Isochronous Support 272 Isochronous Transaction Support 272 

## _**J**_ 

Jitter 485, 487 

## _**L**_ 

L0 State 500, 520, 568 L0s 744 L0s Receiver State Machine 605 L0s State 520, 603, 744 L0s Transmitter State Machine 603 L1 ASPM 736, 747 L1 ASPM Negotiation 748 L1 ASPM State 747 L1 State 520, 607, 760 L2 State 521, 609, 767 L2/L3 Ready 767 L2/L3 Ready state 763, 764 Lane 40, 78, 365, 979 Lane # 511 Lane Number Negotiation 543, 547 Lane Reversal 507 Lane-Level Encoding 410 Lane-to-Lane de-skew 78 Lane-to-Lane Skew 979 Last DW Byte Enables 178, 181 Latency Tolerance Reporting 910 LCRC 63, 325, 329 LeCroy 922, 923, 933 LeCroy Tools 917 Legacy Endpoint 816, 979 Legacy Endpoints 972 LFSR 980 Link 40, 980 Link # 511 Link Capabilities 2 Register 640 Link Capability Register 743 Link Configuration - Failed Lane 549 Link Control 841 Link Data Rate 509 Link data rate 78 Link Equalization 577 Link Errors 683 Link Flow Control-Related Errors 666 Link Number Negotiation 542, 546 Link Power Management 733 Link Status Register 641 Link Training and Initialization 78 Link Training and Status State Machine (LTSSM) 518 Link Upconfigure Capability 512 Link Width 507 Link width 78 Link Width Change 570 Link Width Change Example 630 Lock 964 Locked Reads 66 Locked Transaction 209 

Locked Transactions 963 Logic Analyzer 921 Logical Idle Sequence 370 Loopback Master 615 Loopback Slave 616 Loopback State 521, 613 Loopback.Active 617 Loopback.Entry 614 Loopback.Exit 618 Low-priority VC Arbitration 255 LTR 784, 910, 980 LTR Messages 786 LTR Registers 784 LTSSM 507, 518, 839, 927, 980 

## _**M**_ 

Malformed TLP 666 Memory Address Space 122 Memory Read 150 Memory Read Lock 150 Memory Request Packet 188 Memory Requests 188 Memory Write 150 Memory Writes 69 Message 151 Message Address Register 816 Message Address register 816, 818 Message Control Register 814 Message Control register 814, 818 Message Data register 817, 818 Message Request Packet 203 Message Requests 70, 203 Message Writes 70 Messages 148 Mid-Bus Probe 923 MindShare Arbor 117 Miniport Driver 706 MMIO 123 Modified Compliance Pattern 537 Modified Compliance Pattern - 8b/10b 532 MR-IOV 937, 939 MSI Capability Register 812 MSI Configuration 817 Multicast 893, 896 Multicast Capabilities 163 Multicast Capability Registers 889 Multi-casting 888 Multi-Function Arbitration 272 Multi-Host System 96 Multi-Host Systems 943 Multiple Message Capable field 818 Multiple Messages 820 Multi-Root 938 Multi-Root Enumeration 114 Multi-Root System 97, 116 

## _**N**_ 

N_FTS 511 Nak 311 NAK_SCHEDULED Flag 327 namespace 712 Native PCI Express Endpoints 972 NEXT_RCV_SEQ 313, 326, 341 Noise 485 Non-Posted 150 non-posted 60 Non-posted Request 980 Non-Posted Transactions 65, 218 Non-prefetchable 123 Non-prefetchable Memory 980 Non-Prefetchable Range 139 North Bridge 21 NP-MMIO 126, 139 NT bridging 936 Nullified Packet 388, 689, 980 

## _**O**_ 

OBFF 776, 910, 981 OBFF Messages 213 OnNow Design Initiative 707 Optimized Buffer Flush and Fill 776, 910, 981 Optimized Buffer Flush and Fill Messages 213 Ordered Sets 981 Ordered-Sets 370 Ordering Rules 287 Ordering Rules Table 288, 289 Ordering Table 914 Oscilloscope 919 

## _**P**_ 

Packet Format 151 Packet Generation 937 Packet-Based Protocol 169 Packet-based Protocol 46 PAD 386 Pause command 853, 874 Pausing a Driver 874 PCI 981 PCI Bus Driver 706, 707, 711 PCI Bus PM Interface Specification 705 PCI Express 39 PCI PM 705 PCI power management 647, 703, 793 PCI Transaction Model 18 PCI-Based System 11 PCI-Compatible Error Reporting 674 PCIe System 53, 54 PCI-X 981 PERST# 835, 849 PETracer 918, 924

</td>
<td style="background-color:#e8e8e8">

⚠️ TODO: 翻译未完成 / Translation pending

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`
