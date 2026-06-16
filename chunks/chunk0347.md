This change simplifies the Transaction Ordering Table by reducing the number of entries in the table. Essentially, it no longer distinguishes between comple‐ tions for reads or completions for non‐posted writes. The motivation for this was to reduce the number of cases that needed to be tested. For more on this, see the section called “The Simplified Ordering Rules Table” on page 288. 

**914** 

# Appendices 

## _**Appendix A:**_ 

## _**Debugging PCIe Traffic with LeCroy Tools**_ 

## Christoper Webb, LeCroy Corporation 

## **Overview** 

The transition of IO bus architecture from PCI to PCI Express had a large impact on developers with respect to types of tools required for validation and debug. 

With parallel buses such as PCI, a waveform view of the signals shows enough information for the developer to interpret the state of the bus. A user could visually examine a waveform and mentally decode the type of transactions, how much data is transferred, and even the content of that transfer. 

Since PCI Express packet traffic is both encoded and scrambled, examining a waveform view of the traffic provides very little information about the state of the link. The speed of the link can be inferred from the width of the bit times, and the width of the link can be inferred by the number of active lanes. How‐ ever, the user cannot visually interpret the symbol alignment, let alone the packets themselves. 

A new class of tools evolved to help developers visualize the state of their now serial links. These tools perform the de‐serialization, decoding, and de‐scram‐ bling for the users. At first glance this would seem to be enough for the devel‐ oper. But for PCI Express specifically, other complications such as flow control credits, lane‐to‐lane skew, polarity inversion, and lane reversal must also be comprehended by these tools as part of understanding PCIe protocol. 

Both pre‐ and post‐silicon debug share a common need for tools. In this appen‐ dix chapter, we describe some of the product offerings available for debugging PCI Express interconnects, both from a pre and post silicon perspective. 

**917** 

**PCI Ex ress Technolo p gy** 

## **Pre-silicon Debugging** 

## **RTL Simulation Perspective** 

In RTL simulation, looking at a waveform view of an FPGA or an ASIC signal is the most common way to debug. By showing internal state machine states, monitoring IO as it moves through the device, or seeing the state of control sig‐ nals; a waveform view is quite powerful. But, as we discussed above, a PCI express link is not understandable when shown as a waveform. Additional pro‐ cessing or decoding must be done to make sense of this new link. To augment the simulation tools, a PCI Express Bus Monitor is typically added to address this need. 

## **PCI Express RTL Bus Monitor** 

A PCI Express Bus monitor is a piece of code which users insert in their RTL simulation to help monitor the state of their PCIe link. At minimum, this moni‐ tor will output text based log files with information about link state changes and types of packet activity. More complex monitors will perform real time compliance checking. A number of vendors provide purchasable IP which per‐ form this exact function. The emphasis however is typically on compliance. Less functionality is provided with respect to visualization of things such as flow control credits, link utilization, or link training debug. 

## **RTL vector export to PETracer Application** 

LeCroy has partnered with a number of the leading PCIe verification IP vendors to create tools to further enhance the visualization and analysis of pre‐silicon PCIe traffic. This involves using the vendors Bus Monitor to export raw symbol traffic into the same PETracer application used by the dedicated PCIe Analyzer hardware. SimPASS PE is LeCroy’s solution to supporting this export. 

More information about LeCroy’s PETracer application and its features are described in the section “As a last resort, a flying lead probe shown in Figure 5 on page 924 may be used to attach the protocol analyzer to the system under test. This involves soldering a resistive tap circuit and connector pins to the PCIe traces. This circuitry is typically soldered to the AC coupling caps of the PCIe link as they are often the only place to access the traces. Once the probe cir‐ 

**918** 

**A endix A pp** 

cuitry is soldered to the PCB, the analyzer probe can be connected and removed as needed. This approach can be used on virtually any PCIe link, however the robustness of the connection is limited by the skill of the technician adding the probe.” on page 924. 

## **Post-Silicon Debug** 

## **Oscilloscope** 

Use of an oscilloscope for debugging a PCIe link is typically focused on the elec‐ trical validation of the link. The most common usage is examining an eye pat‐ tern with a mask overlay for determining electrical compliance. A lesser known compliance check is to examine the entry and exit of electrical idle state to see if the link goes to the common mode voltage within the required time periods after an electrical idle ordered set is transmitted. These are 2 examples of PCIe compliance checking which are best performed using an oscilloscope such as shown in Figure 1 on page 920. 

With the addition of dynamic link training for 8.0 GT/s operation, devices must now train the transmitter emphasis during the Recovery.EQ LTSSM sub‐state. The goal is to set the transmitter EQ to provide the best signal eye to the receiver. Monitoring this dynamic equalization process is another example where the use of an oscilloscope is quite powerful. With a real time oscilloscope, the user can capture this process and see the impact on the waveform as trans‐ mitter settings are changed. This allows the user to verify that the transmitter is indeed acting on the coefficient change requests, but it also allows the user to determine if the receiver has properly chosen the correct setting. 

For logical debug of the link, the oscilloscope is most useful when the link is x1 or x2 as you are limited by the number channels the scope can acquire. The first method of examining PCIe traffic is a waveform view. As with the RTL wave‐ form viewer, there is little to understand about the state of the link without SW help to perform 8b/10b decoding and de‐scrambling. Fortunately, more advanced oscilloscopes have SW packages that perform these duties. For this to work properly, the scope must have deep capture buffers and must see the SKIP ordered sets so that they can decipher the byte alignment and synchronize the de‐scrambler LFSR. 

The LeCroy Oscilloscope can overlay PCIe symbols right onto the waveform for enhanced visibility of the traffic. An additional text based listing of the packet symbols can be displayed on the screen as an additional method of examining the waveform. 

**919** 

## **PCI Ex ress Technolo p gy** 

LeCroy recently announced a SW package called ProtoSync for their oscillo‐ scope line which allows the user to export the captured waveform into the PETracer application. This is the same SW package that the protocol analyzer uses which includes a wide range of post processing capabilities described below. The PETracer software can run independently on the scope hardware, often on a second monitor. This allows time correlated comparison of the physi‐ cal layer data presented by the scope waveform alongside the logic layer pre‐ sentation of data presented by the PETracer software. 

Capture of the 8.0 GT/s dynamic link equalization on the oscilloscope and exporting this traffic to the PETracer application is a prime example where this solution is most powerful. The user can navigate PETracer to the link training packet where the TX coefficient change request has been sent, then identify where this coefficient change was applied in the scope SW. The user can then measure the time it takes for the coefficient change to be applied and compare this to the timing required in the PCIe spec. 

_Figure A‐1: LeCroy Oscilloscope with ProtoSync Software Option_ 

## **Protocol Analyzer** 

A growing trend in debugging PCIe links is to use a dedicated protocol analysis tool. What separates a protocol analyzer from a logic analyzer is that it is built to support a specific protocol such as PCIe. From a hardware perspective, a PCIe protocol analyzer is optimized for acquiring and storing PCIe traffic. This starts from the dedicated PCIe interposer probes, continues to the cabling choice, and caries through into the internal hardware components. For recover‐ ing PCIe traffic, specialized clock and data recovery circuits are used which can handle the electrical idle transitions, spread spectrum modulation, as well as 

**920** 

**A endix A pp** 

handle the run lengths found in 128b/130b encoding. Sophisticated equalization circuits are used to recover the signal eye prior to deserialization. Without com‐ prehending the complexities of PCIe recovery, the Analyzer hardware would not be optimized for recovering complex traffic such as speed switching, dynamic link widths, and low power states such as L0s. 

In addition to choosing appropriate hardware components for recovering PCIe traffic, a protocol analyzer includes logic circuitry which is PCIe specific. This logic must infer the state of the PCIe link and follow it during various LTSSM state changes. Once the link state is being properly followed, dedicated packet inspection circuits perform data matching against incoming packets to look for events programmed by the user. These matchers are used for filtering of traffic as well as performing the trigger functionality needed for stopping the traffic capture. A mixture of these traffic filters as well as deep trace buffers (often 4GB to 8GB in size) allow the user to capture significantly longer traffic scenarios than would be possible without a protocol analyzer. 

Finally, the most important piece of a protocol analyzer is the software GUI. By optimizing the traffic views, post processing reports, and hardware controls with a dedicated PCI Express software tool; a very comprehensive set of PCI express specific analysis can be performed. 

## **Logic Analyzer** 

Some logic analyzers offer PCIe specific software packages. This software will read the PCI express capture from the logic analyzer hardware and perform some amount of post processing of this data. This analysis includes the basics such as decoding, de‐scrambling, and decoding of the traffic. These SW tools do not perform many of the rich post processing features offered by dedicated pro‐ tocol analyzer software, however. 

## **Using a Protocol Analyzer Probing Option** 

To record your PCIe traffic you must first find the best method for probing it. PCIe started as an add‐in card form factor for desktop PC’s and servers, but has since proliferated into a dizzying array of standard and non‐standard form fac‐ tors. For the standard form factors, the best probe option is a dedicated inter‐ poser. 

An Interposer is a dedicated piece of hardware which includes probe circuitry required for passing a copy of the PCIe traffic to the Analyzer hardware for cap‐ ture and analysis. These interposers are designed specifically for the mechanical 

**921** 

## **PCI Ex ress Technolo p gy** 

and electrical environments for which they are placed. The most common inter‐ poser is a “Slot Interposer” such as shown in Figure 2 on page 922. This inter‐ poser is used for probing standard CEM compliant PCIe add‐in cards. 
