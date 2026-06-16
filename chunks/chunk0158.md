## **PCI Ex ress Technolo p gy** 

_Figure 2‐7: Configuration Headers_ 

**==> picture [374 x 244] intentionally omitted <==**

**----- Start of picture text -----**<br>
Header Type 0 Header Type 1<br>256-Byte (used by endpoints) DW (used by bridges) DW<br>Configuration Space<br>(per function) DeviceID VendorID 00 DeviceID VendorID 00<br>RegisterStatus CommandRegister 01 RegisterStatus CommandRegister 01<br>64-Byte Class Code RevisionID 02 Class Code RevisionID 02<br>PCI ConfigurationHeader Space BIST Base Address 0HeaderType LatencyTimer CacheLineSize 0304 BISTBase Address 0HeaderType LatencyTimer CacheLineSize 0304<br>Base Address 1 05 Base Address 1 05<br>Base Address 2 06 Latency TimerSecondary Bus NumberSubordinate Bus NumberSecondary Bus NumberPrimary 06<br>Base Address 3 07 SecondaryStatus LimitI/O BaseI/O 07<br>Base Address 4 08 MemoryLimit MemoryBase 08<br>Function-Specific192-Byte CardBus CIS PointerBase Address 5 0910 Memory LimitPrefetchablePrefetchable BaseUpper 32 BitsMemory BasePrefetchable 0910<br>Configuration Subsystem ID SubsystemVendor ID 11 Prefetchable LimitUpper 32 Bits 11<br>Header Space Expansion ROM 12 I/O Limit I/O Base 12<br>Base Address Upper 16 Bits Upper 16 Bits<br>Reserved CapabilitiesPointer 13 Reserved CapabilityPointer 13<br>Reserved 14 Expansion ROM Base Address 14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15 ControlBridge InterruptPin InterruptLine 15<br>**----- End of picture text -----**<br>

To illustrate the way the system appears to software, consider the example topology shown in Figure 2‐8 on page 51. As before, the Root resides at the top of the hierarchy. The Root can be quite complex internally, but it will usually implement an internal bus structure and several bridges to fan out the topology to several ports. That internal bus will appear to configuration software as PCI bus number zero and the PCIe Ports will appear as PCI‐to‐PCI bridges. This internal structure is not likely to be an actual PCI bus, but it will appear that way to software for this purpose. Since this bus is internal to the Root, its actual logical design doesn’t have to conform to any standard and can be vendor spe‐ cific. 

**50** 

**Chapter 2: PCIe Architecture Overview** 

_Figure 2‐8: Topology Example_ 

**==> picture [345 x 191] intentionally omitted <==**

**----- Start of picture text -----**<br>
Host<br>CPU Bridge<br>Internal Bus 0<br>Root Complex<br>Memory<br>PCI-PCI PCI-PCI PCI-PCI<br>Bridge Bridge Bridge<br>PCIe<br>Switch Endpoint PCIe<br>Bridge<br>to PCI<br>or PCI-X<br>PCIe PCIe Legacy<br>PCI/PCI-X<br>Endpoint Endpoint Endpoint<br>**----- End of picture text -----**<br>

In a similar way, the internal organization of a Switch, shown in Figure 2‐9 on page 52, will appear to software as simply a collection of bridges sharing a com‐ mon bus. A major advantage of this approach is that it allows transaction rout‐ ing to take place in the same way it did for PCI. Enumeration, the process by which configuration software discovers the system topology and assigns bus numbers and system resources, works the same way, too. We’ll see some exam‐ ples of how enumeration works later, but once it’s been completed the bus num‐ bers in the system will have all been assigned in a manner like that shown in Figure 2‐9 on page 52. 

**51** 

**PCI Ex ress Technolo p gy** 

_Figure 2‐9: Example Results of System Enumeration_ 

**==> picture [264 x 270] intentionally omitted <==**

**----- Start of picture text -----**<br>
PCI-PCI<br>Bridge<br>Internal Bus 2<br>PCI-PCI PCI-PCI PCI-PCI<br>Bridge Bridge Bridge<br>CPU<br>Root Complex<br>(internal bus 0) Memory<br>Bus 1 Bus 6 Bus 7<br>PCIe Bus 3 Switch EndpointPCIe BridgePCIe<br>Endpoint to PCI<br>Bus 4 Bus 5 or PCI-X<br>PCIe Legacy<br>Endpoint Endpoint PCI/PCI-X<br>Bus 8<br>Legend<br>Downstream port<br>Upstream port<br>**----- End of picture text -----**<br>