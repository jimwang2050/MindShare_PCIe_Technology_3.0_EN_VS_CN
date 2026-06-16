**Cha ter 18: S stem Reset p y** 

## **Hot Reset (In-band Reset)** 

A Hot Reset is propagated in‐band from one link neighbor to another by send‐ ing several TS1s (whose contents are shown in Figure 18‐2) with bit 0 of symbol 5 asserted. These TS1s are sent on all Lanes, using the previously negotiated Link and Lane numbers, for 2 ms. Once it’s been sent, the Transmitter and Receiver of the Hot Reset will both end up in the Detect LTSSM state (see “Hot Reset State” on page 612). 

_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_ 

|_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_|_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_|_Figure 18‐2: TS1 Ordered‐Set Showing the Hot Reset Bit_|
|---|---|---|
||||
|**TS1**<br>TS ID<br>TS ID<br>TS ID<br>Train Ctl<br>Rate ID<br># FTS<br>Lane #<br>Link #<br>COM<br>0<br>1<br>2<br>3<br>4<br>5<br>6<br>14<br>15<br>13|K28.5<br>D0.0-D31.7, K23.7 (0-255)<br>D0.0-D31.0, K23.7 (0-31)<br># of FTS ordered sets required by<br>receiver to obtain bit and symbol lock<br>D10.2 for TS1 Identifier<br>D10.2 for TS1 Identifier<br>D10.2 for TS1 Identifier|**0** **=** **De-assert** **Disable** **Scrambling**<br>**1** **=** **Assert** **Disable** **Scrambling**<br>**Bit** **3**<br>**Reserved**<br>**Bit** **5:7**<br>**0** **=** **De-assert** **Compliance** **Receive**<br>**1** **=** **Assert** **Compliance** **Receive**<br>**Bit** **4**<br>**0** **=** **De-assert** **Loopback**<br>**1** **=** **Assert** **Loopback**<br>**Bit** **2**<br>**0** **=** **De-assert** **Disable** **Link**<br>**1** **=** **Assert** **Disable** **Link**<br>**Bit** **1**<br>**0** **=** **De-assert** **Hot** **Reset**<br>**1** **=** **Assert** **Hot** **Reset**<br>**Bit** **0**<br>**Training Control**|
||||



A hot reset is initiated in software by setting the Secondary Bus Reset bit in a bridge’s Bridge Control configuration register, as shown in Figure 18‐5 on page 840. Consequently, only devices containing bridges, like the Root Complex or a Switch, can do this. A Switch that receives hot reset on its Upstream Port must broadcast it to all of its Downstream Ports and reset itself. All devices down‐ stream of a switch that receive the hot reset will reset themselves. 

## **Response to Receiving Hot Reset** 

- The device’s LTSSM goes through the Recovery and Hot Reset state, and then back to the Detect state, where it starts the Link Training process. 

- • All of the device’s state machines, hardware logic, port states and configura‐ tion registers (except sticky registers) initialize to their default conditions. 

**837** 

**PCI Ex ress Technolo p gy** 

## **Switches Generate Hot Reset on Downstream Ports** 

A Switch generates a hot reset on all of its Downstream Ports when: 

- It receives a hot reset on its Upstream Port 

- For a Switch or Bridge Upstream Port, if the Data Link Layer reports a DL_Down state, the effect is very similar to a hot reset. This can happen when the Upstream Port has lost its connection with an upstream device due to an error that is not recoverable by the Physical Layer or Data Link Layer. 

- Software sets the ‘Secondary Bus Reset’ bit of the Bridge Control configura‐ tion register associated with the Upstream Port, as shown in Figure 18‐3 on page 838. 

_Figure 18‐3: Switch Generates Hot Reset on One Downstream Port_ 

**==> picture [251 x 187] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>FSB<br>PCI Express<br>GFX<br>GFX Root Complex DDR<br>SDRAM<br>‘Secondary Bus Reset’<br>Bit Set<br>Switch A Switch C<br>1<br>Switch B Ethernet10Gb PCI Expressto-PCI SCSI<br>Slots<br>PCI<br>Gb<br>Add-In Ethernet S IEEE<br>IO 1394<br>COM1<br>COM2<br>**----- End of picture text -----**<br>


## **Bridges Forward Hot Reset to the Secondary Bus** 

If a bridge such as a PCI Express‐to‐PCI(‐X) bridge detects a hot reset on its Upstream Port, it must assert the PRST# signal on its secondary PCI(‐X) bus, as illustrated in Figure 18‐4 on page 839. 

## **Software Generation of Hot Reset** 

Software generates a Hot Reset on a specific port by writing a 1 followed by 0 to the ‘Secondary Bus Reset’ bit in the Bridge Control register of that associated 

**838** 

**Cha ter 18: S stem Reset p y** 

port’s configuration header (see Figure 18‐5 on page 840). Consider the example shown in Figure 18‐3 on page 838. Software sets the ‘Secondary Bus Reset’ regis‐ ter of Switch A’s left Downstream Port, causing it to send TS1 Ordered Sets with the Hot Reset bit set. Switch B receives this Hot Reset on its Upstream Port and forwards it to all its Downstream Ports. 

_Figure 18‐4: Switch Generates Hot Reset on All Downstream Ports_ 

**==> picture [277 x 210] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor Processor<br>FSB<br>PCI Express<br>GFX<br>GFX Root Complex<br>DDR<br>SDRAM<br>‘Secondary Bus Reset’<br>1<br>Bit is Set<br>Switch A Switch C<br>Switch B Ethernet10Gb PCI Expressto-PCI SCSI<br>Slots<br>PRST#<br>PCI<br>Gb<br>Add-In Ethernet S IEEE<br>IO 1394<br>COM1<br>COM2<br>**----- End of picture text -----**<br>


If software sets the Secondary Bus Reset bit of a Switch’s Upstream Port, then the switch generates a hot reset on all of its Downstream Ports, as shown in Fig‐ ure 18‐4 on page 839. Here, software sets the Secondary Bus Reset bit in Switch C’s Upstream Port, causing it to send TS1s with the Hot Reset bit set on all its Downstream Ports. The PCIe‐to‐PCI bridge receives this Hot Reset and for‐ wards it on to the PCI bus by asserting PRST#. 

Setting the Secondary Bus Reset bit causes a Port’s LTSSM to transition to the Recovery state (for more on the LTSSM, see “Overview of LTSSM States” on page 519) where it generates the TS1s with the Hot Reset bit set. The TS1s are generated continuously for 2 ms and then the Port exits to the Detect state where it is ready to start the Link training process. 

**839** 

**PCI Ex ress Technolo p gy** 

The receiver of the Hot Reset TS1s (always downstream) will go to the Recovery state, too. When it sees two consecutive TS1s with the Hot Reset bit set, it goes to the Hot Reset state for a 2ms timeout and then exits to Detect. Both Upstream and Downstream Ports are initialized and end up in the Detect state, ready to begin Link training. If the downstream device is also a Switch or Bridge, it for‐ wards the Hot Reset to its Downstream Ports as well, as shown in Figure 18‐3 on page 838. 

_Figure 18‐5: Secondary Bus Reset Register to Generate Hot Reset_ 

**==> picture [374 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Doubleword<br>Number<br>Byte (in decimal)<br>15 12 11 10 9 8 7 6 5 4 3 2 1 0 3 2 1 0<br>Reserved 2.2 2.2 2.2 2.2 DeviceID VendorID 00<br>Status Command 01<br>Discard Timer SERR# Enable Register Register<br>Discard Timer Status Class Code Revision 02<br>ID<br>Secondary Discard TimeoutPrimary Discard Timeout BISTBase Add ress 0HeaderType LatencyTimer CacheLineSize 0304<br>Fast Back-to-Back Enable<br>Secondary Bus Reset Base Add ress 1 05<br>Master Abort Mode Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>VGA Enable Secondary I/O I/O 07<br>ISA Enable Status Limit Base<br>SERR# Enable MemoryLimit MemoryBase 08<br>Parity Error Response Prefetchable Prefetchable 09<br>Memory Limit Memory Base<br>Prefetchable Ba se 10<br>Upper 3 2 Bits<br>Prefetchable L imit 11<br>Upper 3 2 Bits<br>I/O Limit I/O Base 12<br>Upper 16 Bits Upper 16 Bits<br>Reserved CapabilityPointer 13<br>Expansion R OM Base Address 14<br>Bridge Interrupt Interrupt 15<br>Control Pin Line<br>Required configuration registers<br>**----- End of picture text -----**<br>


## **Software Can Disable the Link** 

Software can also disable a Link, forcing it to go into Electrical Idle and remain there until further notice. The reason for mentioning that at this point is that disabling the Link also has the effect of causing a Hot Reset on downstream components. Disabling is accomplished by setting the Link Disable bit in the Link Control Register of the Downstream Port, shown in Figure 18‐6 on page 841. That causes the Port to go to the Recovery LTSSM state and begin sending TS1s with the Disable bit set. Since this can only be controlled for Downstream Ports if the Link has been disabled, this bit is reserved for Upstream Ports (such as Endpoints or Switch Upstream Ports). 

**840** 

**Cha ter 18: S stem Reset p y** 

## _Figure 18‐6: Link Control Register_ 

**==> picture [346 x 306] intentionally omitted <==**

**----- Start of picture text -----**<br>
15 12 11 10 9 8 7 6 5 4 3 2 1 0<br>RsvdP<br>Link Autonomous Bandwidth<br>Interrupt Enable<br>Link Bandwidth Management<br>Interrupt Enable<br>Hardware Autonomous<br>Width Disable<br>Enable Clock<br>Power Management<br>Extended Synch<br>Common Clock<br>Configuration<br>Retrain Link<br>Link Disable<br>Read Completion<br>Boundary Control<br>RsvdP<br>Active State<br>PM Control<br>**----- End of picture text -----**<br>


When the Upstream Port recognizes incoming TS1s with the Disabled bit set, its Physical Layer signals LinkUp=0 (false) to the Link Layer and all the Lanes go to Electrical Idle. After a 2ms timeout, an Upstream Port will go to Detect, but a Downstream Port will remain in the Disabled LTSSM state until directed to exit from it (such as by clearing the Link Disable bit), so the Link will remain dis‐ abled and will not attempt training until then. 

**841** 

**PCI Ex ress Technolo p gy** 

## _Figure 18‐7: TS1 Ordered‐Set Showing Disable Link Bit_ 

**==> picture [366 x 172] intentionally omitted <==**

**----- Start of picture text -----**<br>
TS1 Training Control<br>Bit 0 0 = De-assert Hot Reset<br>0 COM K28.5<br>1 = Assert Hot Reset<br>1 Link # D0.0-D31.7, K23.7 (0-255)<br>2 Lane # D0.0-D31.0, K23.7 (0-31) Bit 1 0 = De-assert Disable Link<br># of FTS ordered sets required by<br>3 # FTS receiver to obtain bit and symbol lock 1 = Assert Disable Link<br>4 Rate ID<br>5 Train Ctl Bit 2 0 = De-assert Loopback<br>6 1 = Assert Loopback<br>TS ID D10.2 for TS1 Identifier Bit 3 0 = De-assert Disable Scrambling<br>1 = Assert Disable Scrambling<br>13<br>14 TS ID D10.2 for TS1 Identifier Bit 4 0 = De-assert Compliance Receive<br>15 TS ID D10.2 for TS1 Identifier 1 = Assert Compliance Receive<br>Bit 5:7 Reserved<br>**----- End of picture text -----**<br>


## **Function Level Reset (FLR)** 

The FLR capability allows software to reset just one Function within a multi‐ function device without affecting the Link that is shared by them all. Its imple‐ mentation is strongly recommended but isn’t required, so software would need to confirm its availability before attempting to use it by examining the Device Capabilities register, as shown in Figure 18‐8 on page 843. If the Function‐Level Reset Capability bit is set, then an FLR can be initiated by simply setting the Ini‐ tiate Function‐Level Reset bit in the Device Control Register as shown in Figure 18‐9 on page 843. 

**842** 

**Cha ter 18: S stem Reset p y** 

_Figure 18‐8: Function‐Level Reset Capability_ 

## _Figure 18‐9: Function‐Level Reset Initiate Bit_ 

**843** 

The spec mentions a few examples that motivate the addition of FLR: 

1. It can happen that software controlling a Function encounters a problem and is no longer operating correctly. Preventing data corruption necessi‐ tates a reset of that Function, but if other Functions within that device are still working properly it would nice to be able to reset just the one having trouble. 
