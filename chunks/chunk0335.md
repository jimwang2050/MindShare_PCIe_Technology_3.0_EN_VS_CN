Local Local<br>APIC APIC<br>CPU CPU<br>4<br>Memory<br>3<br>North Bridge<br>PCI Bus<br>Bridge<br>Write Buffer<br>South Bridge<br>1<br>2<br>PCI Bus<br>Interrupt Controller<br>(IO APIC)<br>Device<br>**----- End of picture text -----**<br>


## **Interrupt Latency** 

The time from signaling an interrupt until software services the device is referred to as the interrupt latency. In spite of its advantages, MSI, like other interrupt delivery mechanisms, does not provide interrupt latency guarantees. 

## **MSI May Result In Errors** 

Because MSIs are delivered as Memory Write transactions, an error associated with delivery of an MSI is treated the same as any other Memory Write error condition. See “ECRC Generation and Checking” on page 657 for treatment of ECRC errors, as one example. The concern, of course, is that if an error results in the MSI packet being unrecognized then no interrupt will be seen by the proces‐ sor. How this condition would be handled is outside the scope of the PCIe spec. 

**829** 

**PCI Ex ress 3.0 Technolo p gy** 

## **Some MSI Rules and Recommendations** 

1. It is the intent of the spec that mutually‐exclusive messages will be assigned to Functions by system software and that each message will be converted to an exclusive interrupt on delivery to the processor. 

2. More than one MSI capability register set per Function is prohibited. 

3. A read of the Message Address register produces undefined results. 

4. Reserved registers and bits are read‐only and always return zero when read. 

5. System software can modify Message Control register bits, but the device itself is prohibited from doing so. In other words, modifying the bits by a “back door” mechanism is not allowed. 

6. At a minimum, a single message will be assigned to each device (assuming software supports and plans to use MSI in the system). 

7. System software must not write to the upper half of the dword that contains the Message Data register. 

8. If the device writes the same message multiple times, only one of those messages is guaranteed to be serviced. If all of them must be serviced, the device must not generate the same message again until the previous one has been serviced. 

9. If a device has more than one message assigned, and it writes a series of dif‐ ferent messages, it is guaranteed that all of them will be serviced. 

## **Special Consideration for Base System Peripherals** 

Interrupts may also originate in embedded legacy hardware, such as an IO Con‐ troller Hub or Super IO device. Some of the typical legacy devices required in such systems include: 

- Serial ports 

- Parallel ports 

- Keyboard and Mouse Controller 

- System Timer 

- IDE controllers 

These devices typically require a specific IRQ line into a PIC or IO APIC, which allows legacy software to interact with them correctly. 

Using the INTx messages does not guarantee that the devices will receive the IRQ assignment they require. The following example illustrates a system that will support the proper legacy interrupt assignment. 

**830** 

**Chapter 17: Interrupt Support** 

## **Example Legacy System** 

Figure 17‐23 on page 831 shows a older PCI Express system that includes an IO Controller Hub (ICH) attached to the Root Complex via a proprietary Hub link. The IO APIC embedded within the ICH can generate an MSI when it receives an interrupt request at its inputs. In such an implementation, software can assign the legacy vector number to each input to ensure that the correct legacy software will be called. 

The advantage of this approach is that existing hardware can be used to support the legacy requirements of a PCIe platform. This system also requires that the MSI subsystem be configured for use during the boot sequence. The example illustrated eliminates the need for INTx messages unless a PCIe expansion device incorporates a PCI Express‐to‐PCI Bridge. 

_Figure 17‐23: PCI Express System with PCI‐Based IO Controller Hub_ 

**==> picture [361 x 282] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>PCI Express<br>GFX<br>PCI Express Root Complex DDR<br>Links SDRAM<br>Hub Link<br>IDE<br>CD HDD IO Controller Hub<br>MSI<br>USB 2.0 Interrupt 4 INTA# - INTD#<br>Controller<br>LPC (APIC) PCI - 33MHz<br>1<br>Serial Interrupts Timer<br>S IEEE Slots<br>IO AC’97 1394<br>COM1 Link<br>COM2<br>Modem Audio Boot<br>Codec Codec Ethernet ROM<br>RouterInterrupt<br>**----- End of picture text -----**<br>


**831** 

**PCI Ex ress 3.0 Technolo p gy** 

**832** 

## _**18**_ 

## _**System Reset**_ 

## **The Previous Chapter** 

The previous chapter describes the different ways that PCIe Functions can gen‐ erate interrupts. The old PCI model used pins for this, but sideband signals are undesirable in a serial model so support for the inband MSI (Message Signaled Interrupt) mechanism was made mandatory. The PCI INTx# pin operation can still be emulated using PCIe INTx messages for software backward compatibil‐ ity reasons. Both the PCI legacy INTx# method and the newer versions of MSI/ MSI‐X are described. 

## **This Chapter** 

This chapter describes the four types of resets defined for PCIe: cold reset, warm reset, hot reset, and function‐level reset. The use of a side‐band reset PERST# signal to generate a system reset is discussed, and so is the in‐band TS1 used to generate a Hot Reset. 

## **The Next Chapter** 

The next chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it’s important to ensure that its power needs don’t exceed what the system can deliver. A mechanism was needed to query and control the power requirements of a device, Power Budgeting provides this. 

## **Two Categories of System Reset** 

The PCI Express spec describes four types of reset mechanisms. Three of these were part of the earlier revisions of the PCIe spec and are collectively referred to now as **Conventional Resets,** and two of them are called Fundamental Resets. The fourth category and method, added with the 2.0 spec revision, is called the **Function Level Reset** . 

**833** 

**PCI Ex ress Technolo p gy** 

## **Conventional Reset** 

## **Fundamental Reset** 

A Fundamental Reset is handled in hardware and resets the entire device, re‐ initializing every state machine and all the hardware logic, port states and con‐ figuration registers. The exception to this rule is a group of some configuration register fields that are identified as “sticky”, meaning they retain their contents unless all power is removed. This makes them very useful for diagnosing prob‐ lems that require a reset to get a Link working again, because the error status survives the reset and is available to software afterwards. If main power is removed but Vaux is available, that will also maintain the sticky bits, but if both main power and Vaux are lost, the sticky bits will be reset along with everything else. 

A Fundamental Reset will occur on a system‐wide reset, but it can also be done for individual devices. 

Two types of Fundamental Reset are defined: 

- **Cold Reset** : The result when the main power is turned on for a device. Cycling the power will cause a cold reset. 

- **Warm Reset (optional):** Triggered by a system‐specific means without shut‐ ting off main power. For example, a change in the system power status might be used to initiate this. The mechanism for generating a Warm Reset is not defined by the spec, so the system designer will choose how this is done. 

When a Fundamental Reset occurs: 

- For positive voltages, receiver terminations are required to meet the ZRX‐HIGH‐IMP‐DC‐POS parameter. At 2.5 GT/s, this is no less than 10 K  . At the higher speeds it must be no less than 10 K  for voltages below 200mv, and 20 K  for voltages above 200mv. These are the values when the termi‐ nations are not powered. 

- Similarly for negative voltages, the ZRX‐HIGH‐IMP‐DC‐NEG parameter, the value is a minimum of 1 K  in every case. 

- Transmitter terminations are required to meet the output impedance ZTX‐DIFF‐DC from 80 to 120  for Gen1 and max of 120  for Gen2 and Gen3, but may place the driver in a high impedance state. 

- The transmitter holds a DC common mode voltage between 0 and 3.6 V. 

**834** 

**Cha ter 18: S stem Reset p y** 

When exiting from a Fundamental Reset: 

- The receiver single‐ended terminations must be present when receiver ter‐ minations are enabled so that Receiver Detect works properly (40‐60  for Gen1 and Gen2, and 50  for Gen3. By the time Detect is entered, the common‐mode impedance must be within the proper range of 50   

- must re‐enable its receiver terminations ZRX‐DIFF‐DC of 100  within 5 ms of Fundamental Reset exit, making it detectable by the neighbor’s transmitter during training. 

- The transmitter holds a DC common mode voltage between 0 and 3.6 V. 

Two methods of delivering a Fundamental Reset are defined. First, it can be sig‐ naled with an auxiliary side‐band signal called PERST# (PCI Express Reset). Second, when PERST# is not provided to an add‐in card or component, a Fun‐ damental Reset is generated autonomously by the component or add‐in card when the power is cycled. 

## **PERST# Fundamental Reset Generation** 

A central resource device such as a chipset in the PCI Express system provides this reset. For example, the IO Controller Hub (ICH) chip in Figure 18‐1 on page 836 may generate PERST# based on the status of the system power supply ‘POWERGOOD’ signal, since this indicates that the main power is turned on and stable. If power is cycled off, POWERGOOD toggles and causes PERST# to assert and deassert., resulting in a Cold Reset. The system may also provide a method of toggling PERST# by some other means to accomplish a Warm Reset. 

The PERST# signal feeds all PCI Express devices on the motherboard including the connectors and graphics controller. Devices may choose to use PERST# but are not required to do so. PERST# also feeds the PCIe‐to‐PCI‐X bridge shown in the figure. Bridges always forward a reset on their primary (upstream) bus to their secondary (downstream) bus, so the PCI‐X bus sees RST# asserted. 

## **Autonomous Reset Generation** 

A device must be designed to generate its own reset in hardware upon applica‐ tion of main power. The spec doesn’t describe how this would be done, so a self‐ reset mechanism can be built into the device or added as external logic. For example, an add‐in card that detects Power‐On may use that event to generate a local reset to its device. The device must also generate an autonomous reset if it detects its power go outside of the limits specified. 

**835** 

**PCI Ex ress Technolo p gy** 

## **Link Wakeup from L2 Low Power State** 

As an example of the need for an autonomous reset, a device whose main power has been turned off as part of a power management policy may be able to request a return to full power if it was designed to signal a wakeup. When power is restored, the device must be reset. The power controller for the system may assert the PERST# pin to the device, as shown in Figure 18‐1 on page 836, but if it doesn’t, or if the device doesn’t support PERST#, the device must auton‐ omously generate its own Fundamental Reset when it senses main power re‐ applied. 

_Figure 18‐1: PERST# Generation_ 

**==> picture [299 x 315] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>FSB<br>GFX Root Complex<br>DDR<br>PCI Express SDRAM<br>GFX<br>PCI Express<br>POWERGOOD PRST#<br>PCI<br>IO Controller Hub<br>(ICH) IEEE<br>1394<br>PERST#<br>Add-In Add-In<br>Switch<br>PCI Express<br>PCI Express Link<br>SCSI<br>to-PCI-X<br>PRST#<br>PCI-X<br>Gigabit<br>Ethernet<br>**----- End of picture text -----**<br>


**836** 
