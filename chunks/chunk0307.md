This chapter describes the operation of the Link Training and Status State Machine (LTSSM) of the Physical Layer. The initialization process of the Link is described from Power‐On or Reset until the Link reaches fully‐operational L0 state during which normal packet traffic occurs. In addition, the Link power management states L0s, L1, L2, and L3 are discussed along with the state transi‐ tions. The Recovery state, during which bit lock, symbol lock or block lock are re‐established is described. Link speed and width change for Link bandwidth management is also discussed. 

## **This Chapter** 

Although care is always taken to minimize errors they can’t be eliminated, so detecting and reporting them is an important consideration. This chapter dis‐ cusses error types that occur in a PCIe Port or Link, how they are detected, reported, and options for handling them. Since PCIe is designed to be backward compatible with PCI error reporting, a review of the PCI approach to error han‐ dling is included as background information. Then we focus on PCIe error han‐ dling of correctable, non‐fatal and fatal errors. 

## **The Next Chapter** 

The next chapter provides an overall context for the discussion of system power management and a detailed description of PCIe power management, which is compatible with the _PCI Bus PM Interface Spec_ and the _Advanced Configuration and Power Interface_ (ACPI). PCIe defines extensions to the PCI‐PM spec that focus primarily on Link Power and event management. 

**647** 

**PCI Ex ress Technolo p gy** 

## **Background** 

Software backward compatibility with PCI is an important feature of PCIe, and that’s accomplished by retaining the PCI configuration registers that were already in place. PCI verified the correct parity on each transmission phase of the bus to check for errors. Detected errors were recorded in the Status register and could optionally be reported with either of two side‐band signals: PERR# (Parity Error) for a potentially recoverable parity fault during data transmis‐ sion, and SERR# (System Error) for a more serious problem that was usually not recoverable. These two types can be categorized as follows: 

- Ordinary data parity errors — reported via PERR# 

- Data parity errors during multi‐task transactions (special cycles) — reported via SERR# 

- Address and command parity errors — reported via SERR# 

- • Other types of errors (device‐specific) — reported via SERR# 

How the errors should be handled was outside the scope of the PCI spec and might include hardware support or device‐specific software. As an example, a data parity error on a read from memory might be recovered in hardware by detecting the condition and simply repeating the Request. That would be a safe step if the memory contents weren’t changed by the failed operation. 

As shown in Figure 15‐1 on page 649, both error pins were typically connected to the chipset and used to signal the CPU in a consumer PC. These machines were very cost sensitive, so they didn’t usually have the budget for much in the way of error handling. Consequently, the resulting error reporting signal chosen was the NMI (Non‐Maskable Interrupt) signal from the chipset to the processor that indicated significant system trouble requiring immediate attention. Most consumer PCs didn’t include an error handler for this condition, so the system would simply be stopped to avoid corruption and the BSOD (Blue Screen Of Death) would inform the operator. An example of an SERR# condition would be an address parity mismatch seen during the command phase of a transaction. This is a potentially destructive case because the wrong target might respond. If that happened and SERR# reported it, recovery would be difficult and would probably require significant software overhead. (To learn more about PCI error handling, refer to MindShare’s book _PCI System Architecture_ .) 

PCI‐X uses the same two error reporting signals but defines specific error han‐ dling requirements depending on whether device‐specific error handling soft‐ ware is present. If such a handler is not present, then all parity errors are reported with SERR#. 

**648** 

**Chapter 15: Error Detection and Handling** 

## _Figure 15‐1: PCI Error Handling_ 

**==> picture [370 x 221] intentionally omitted <==**

**----- Start of picture text -----**<br>
NMI<br>Processor<br>FSB<br>Graphics<br>NorthNorthBridgBridge<br>(Intel 440(Intel 440 ) S DRAM<br>Address Port Data Port<br>PCI 33 MHz<br>Slots<br>CD HDD IDE PERR#<br>Error<br>South Bridge Logic<br>USB SERR#<br>ISA<br>Ethernet SCSI<br>Boot Modem Audio Super<br>ROM Chip Chip I/O<br>COM1<br>COM2<br>**----- End of picture text -----**<br>


PCI‐X 2.0 uses source‐synchronous clocking to achieve faster data rates (up to 4GB/s). This bus targeted high‐end enterprise systems because it was generally too expensive for consumer machines. Since these high‐performance systems also require high availability, the spec writers chose to improve the error han‐ dling by adding Error‐Correcting Code (ECC) support. ECC allows more robust error detection and enables correction of single‐bit errors on the fly. ECC is very helpful in minimizing the impact of transmission errors. (To learn more about PCI‐X error handling, see MindShare’s book _PCI‐X System Architecture_ .) 

PCIe maintains backward compatibility with these legacy mechanisms by using the error status bits in the legacy configuration registers to record error events in PCIe that are analogous to those of PCI. That lets legacy software see PCIe error events in terms that it understands, and allows it to operate with PCIe hardware. See “PCI‐Compatible Error Reporting Mechanisms” on page 674 for the details of these registers. 

**649** 

**PCI Ex ress Technolo p gy** 

## **PCIe Error Definitions** 

The spec uses four general terms regarding errors, defined here: 

1. **Error Detection** ‐ the process of determining that an error exists. Errors are discovered by an agent as a result of a local problem, such as receiving a bad packet, or because it received a packet signaling an error from another device (like a poisoned packet). 

2. **Error Logging** ‐ setting the appropriate bits in the architected registers based on the error detected as an aid for error‐handling software. 

3. **Error Reporting** ‐ notifying the system that an error condition exists. This can take the form of an error Message being delivered to the Root Complex, assuming the device is enabled to send error messages. The Root, in turn, can send an interrupt to the system when it receives an error Message. 

4. **Error Signaling** ‐ the process of one agent notifying another of an error con‐ dition by sending an error Message, or sending a Completion with a UR (Unsupported Request) or CA (Completer Abort) status, or poisoning a TLP (also known as error forwarding). 

## **PCIe Error Reporting** 

Two error reporting levels are defined for PCIe. The first is a Baseline capability required for all devices. This includes support for legacy error reporting as well as basic support for reporting PCIe errors. The second is an optional Advanced Error Reporting Capability that adds a new set of configuration registers and tracks many more details about which errors have occurred, how serious they are and in some cases, can even record information about the packet that caused the error. 

## **Baseline Error Reporting** 

Two sets of configuration registers are required in all devices in support of Baseline error reporting. These are described in detail in “Baseline Error Detec‐ tion and Handling” on page 674 and are summarized here: 

- PCI‐compatible Registers — these are the same registers used by PCI and provide backward compatibility for existing PCI‐compatible software. To make this work, PCIe errors are mapped to PCI‐compatible errors, making them visible to the legacy software. 

**650** 

**Chapter 15: Error Detection and Handling** 

- PCI Express Capability Registers — these registers will only be useful to newer software that is aware of PCIe, but they provide more error informa‐ tion specifically for PCIe software. 

## **Advanced Error Reporting (AER)** 

This optional error reporting mechanism includes a new and dedicated set of configuration registers that give error handling software more information to work with in diagnosing and recovering from problems. The AER registers are mapped into the extended configuration space and provide much more infor‐ mation about the nature of any errors. See “Advanced Error Reporting (AER)” on page 685 for a detailed description of these registers. 

## **Error Classes** 

Errors fall into two general categories based on whether hardware is able to fix the problem or not, Correctable and Uncorrectable. The Uncorrectable category is further subdivided based on whether software can fix the problem, Non‐fatal and Fatal. 

- Correctable errors — automatically handled by hardware 

- Uncorrectable errors 

- Non‐fatal — handled by device‐specific software; Link is still operational and recovery without data loss may be possible 

- Fatal — handled by system software; Link or Device is not working prop‐ erly and recovery without data loss is unlikely 

Based on these classes, error handling software can be partitioned into separate handlers to perform the actions required. Such actions might range from simply monitoring the frequency of Correctable errors to resetting the entire system in the event of a Fatal error. Regardless of the type of error, software may arrange for the system to be notified of all errors to allow tracking and logging them. 

## **Correctable Errors** 

Correctable errors are, by definition, automatically corrected in hardware. They may impact performance by adding latency and consuming bandwidth, but if all goes well, recovery is automatic and fast because it doesn’t depend on soft‐ ware intervention, and no information is lost in the process. These errors aren’t 

**651** 

**PCI Ex ress Technolo p gy** 

required to be reported to software, but doing so could allow software to track error trends that might indicate that some devices are showing signs of immi‐ nent failure. 

## **Uncorrectable Errors** 

Errors that can’t be automatically corrected in hardware are called Uncorrect‐ able, and these are either Non‐fatal or Fatal in severity. 

## **Non-fatal Uncorrectable Errors** 

Non‐fatal errors indicate that information has been lost but the cause was likely something other than the integrity of a Link or Device. A packet failed some‐ where, but the Link continues to function correctly and other packets are unaf‐ fected. Since the Link is still working, recovery of the lost information may be possible, but will depend on implementation‐specific software to handle it. An example of this error type would be a Completion timeout, in which a Request was sent but no Completion was returned within the allowed time. Somewhere there was an issue, but it could be something as simple as a random bit error within a Switch that caused the Completion to be routed incorrectly. An attempt at recovery for this case could be as simple as re‐issuing the Request. 

## **Fatal Uncorrectable Errors** 
