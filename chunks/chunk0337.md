2. In a virtualized environment, where applications can migrate from one piece of hardware to another, it’s important that when an application is moved off a Function that the Function doesn’t retain any information about what it was doing. This prevents information used by one application that might be considered confidential from becoming visible to the new one running on that Function. The simplest way to clean up after migrating the previous application is simply to reset the Function. 

3. When software is rebuilding a software stack for a Function, it is sometimes necessary to first put the Function into an uninitialized state. As before, avoiding a reset of all Functions sharing the Link is desirable. 

Another feature doesn’t appear in the list of cases in the spec but is still a moti‐ vating factor in its own right. While a conventional reset will re‐initialize every‐ thing within the device, it does not require that all external activity, such as traffic on a network interface, must cease right away. FLR adds this requirement and is the only reset that does. 

FLR resets the Function’s internal state and registers, making it quiescent, but doesn’t affect any sticky bits, or hardware‐initialized bits, or link‐specific regis‐ ters like Captured Power, ASPM Control, Max_Payload_Size or Virtual Channel registers. If an outstanding Assert INTx interrupt message was sent, a corre‐ sponding Deassert INTx message must be sent, unless that interrupt was shared by another Function internally that still has it asserted. All external activity for that Function is required to cease when an FLR is received. 

## **Time Allowed** 

A Function must complete an FLR within 100ms. However, software may need to delay initiating an FLR if there are any outstanding split completions that haven’t yet been returned (indicated by the fact that the Transactions Pending bit remains set in the Device Status register). In that case, software must either wait for them to finish before initiating the FLR, or wait 100ms after FLR before attempting to re‐initialize the Function. If this isn’t managed, a potential data corruption problem arises: a Function may have split transactions outstanding but a reset causes it to lose track of them. If they are returned later they could be 

**Cha ter 18: S stem Reset p y** 

mistaken for responses to new requests that have been issued since the FLR. To avoid this problem, the spec recommends that software should: 

1. Coordinate with other software that might access the Function to ensure it doesn’t attempt access during the FLR. 

2. Clear the entire Command register, thereby quiescing the Function. 

3. Ensure that previously‐requested Completions have been returned by poll‐ ing the Transactions Pending bit in the Device Status register until it’s cleared or waiting long enough to be sure the Completions won’t ever be returned. How long would be long enough? If Completion Timeouts are being used, wait for the timeout period before sending the FLR. If Comple‐ tion Timeouts are disabled, then wait at least 100ms. 

4. Initiate the FLR and wait 100ms. 

5. Set up the Function’s configuration registers and enable it for normal opera‐ tion. 

When the FLR has completed, regardless of the timing, the Transaction Pending bit must be cleared. 

## **Behavior During FLR** 

The spec writers chose to describe the behavior of a Function reset in fairly broad terms so as not to preclude any internal steps that designers might wish to take. The following behaviors are listed in the spec: 

- The Function must not appear to an external interface as though it was an initialized adapter with an active host. The steps to ensure that all activity on external interfaces is terminated will be design specific. An example would be a network adapter that must not respond to requests that would require an active host during this time. 

- The Function must not retain any software‐readable state that might include secret information left behind by some previous use of the Func‐ tion. For example, any internal memory must be cleared or randomized. 

- The Function must be configurable as normal by the next driver. 

- The Function must return a completion for the configuration write that caused the FLR and then initiate the FLR. 

While an FLR is in progress: 

- Any requests that arrive are allowed to be silently discarded without log‐ ging them or signaling an error. Flow control credits must be updated to maintain the link operation, though. 

**845** 

## **PCI Ex ress Technolo p gy** 

- Incoming completions can be treated as Unexpected Completions or silently discarded without logging them or signaling an error. 

- The FLR itself must be completed within the time described above, but fur‐ ther initialization after that could take longer. If a configuration Request comes in before initialization is completed, the Function must return a com‐ pletion with CRS (Configuration Retry Status) status. Once a completion is returned with any other status, a CRS status will not be legal again until the Function is reset again. 

## **Reset Exit** 

After exiting the reset state, Link Training and Initialization must begin within 20 ms. Devices may exit the reset state at different times, since reset signaling is asynchronous, but must begin training within this time. 

To allow reset components to perform internal initialization, system software must wait for at least 100 ms from the end of a reset before attempting to send Configuration Requests to them. If software initiates a configuration request to a device after the 100 ms wait time, but the device still hasn’t finished its self‐ini‐ tialization, it returns a Completion with status CRS. Since configuration Requests can only be initiated by the CPU, the Completion will be returned to the Root Complex. In response, the Root may re‐issue the configuration Request automatically or make the failure visible to software. The spec also states that software should only use 100ms wait periods if CRS Software Visibility has been enabled, since long timeouts or processor stalls may otherwise result. 

Devices are allowed a full 1.0 second (‐0%/+50%) after a reset before they must give a proper response to a configuration request. Consequently, the system must be careful to wait that long before deciding that an unresponsive device is broken. This value is inherited from PCI and the reason for this lengthy delay may be that some devices implement configuration space as a local memory that must be initialized before it can be seen correctly by configuration software. Its initialization may involve copying the necessary information from a slow serial EEPROM, and so it might take some time. 

**846** 

## _**19 Hot Plug and Power Budgeting**_ 

## **The Previous Chapter** 

The previous chapter describes three types of resets defined for PCIe: Funda‐ mental reset (consisting of cold and warm reset), hot reset, and function‐level reset (FLR). The use of a side‐band reset PERST# signal to generate a system reset is discussed, and so is the in‐band TS1 based Hot Reset described. 

## **This Chapter** 

This chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it’s important to ensure that its power needs don’t exceed what the system can deliver. A mechanism was needed to query the power requirements of a device before giving it permission to operate. Power budgeting registers provide that. 

## **The Next Chapter** 

The next chapter describes the changes and new features that were added with the 2.1 revision of the spec. Some of these topics, like the ones related to power management, are described in earlier chapters, but for others there wasn’t another logical place for them. In the end, it seemed best to group them all together in one chapter to ensure that they were all covered and to help clarify what features are new. 

**847** 

**PCI Ex ress Technolo p gy** 

## **Background** 

Some systems using PCIe require high availability or non‐stop operation. Online service suppliers require computer systems that experience downtimes of just a few minutes a year or less. There are many aspects to building such sys‐ tems, but equipment reliability is clearly important. To facilitate these goals PCIe supports the Hot Plug/Hot Swap solutions for add‐in cards that provide three important capabilities: 

1. a method of replacing failed expansion cards without turning the system off 2. keeping the O/S and other services running during the repair 3. shutting down and restarting software associated with a failed device 

Prior to the widespread acceptance of PCI, many proprietary Hot Plug solu‐ tions were developed to support this type of removal and replacement of expansion cards. The original PCI implementation did not support hot removal and insertion of cards, but two standardized solutions for supporting this capa‐ bility in PCI have been developed. The first is the Hot Plug PCI Card used in PC Server motherboard and expansion chassis implementations. The other is called Hot Swap and is used in CompactPCI systems based on a passive PCI back‐ plane implementation. 

In both solutions, control logic is used to electrically isolate the card logic from the shared PCI bus. Power, reset, and clock are controlled to ensure an orderly power down and power up of cards as they are removed and replaced, and sta‐ tus and power LEDs inform the user when it’s safe to change a card. 

Extending hot plug support to PCI Express cards is an obvious step, and designers have incorporated some Hot Plug features as “native” to PCIe. The spec defines configuration registers, Hot Plug Messages, and procedures to sup‐ port Hot Plug solutions. 

## **Hot Plug in the PCI Express Environment** 

PCIe Hot Plug is derived from the 1.0 revision of the Standard Hot Plug Con‐ troller spec (SHPC 1.0) for PCI. The goals of PCI Express Hot Plug are to: 

- Support the same “Standardized Usage Model” as defined by the Standard Hot Plug Controller spec. This ensures that the PCI Express hot plug is identical from the user perspective to existing implementations based on the SHPC 1.0 spec 

**848** 

**Chapter 19: Hot Plug and Power Budgeting** 

- Support the same software model implemented by existing operating sys‐ tems. However, an OS using a SHPC 1.0 compliant driver won’t work with PCI Express Hot Plug controllers because they have a different program‐ ming interface. 

The registers necessary to support a Hot Plug Controller are integrated into individual Root and Switch Ports. Under Hot Plug software control, these con‐ trollers and the associated port interface must control the card interface signals to ensure orderly power down and power up as cards are changed. To accom‐ plish that, they’ll need to: 

- Assert and deassert the PERST# signal to the PCI Express card connector 

- • Remove or apply power to the card connector. 

- Selectively turn on or off the Power and Attention Indicators associated with a specific card connector to draw the user’s attention to the connector and indicate whether power is applied to the slot. 

- Monitor slot events (e.g. card removal) and report them to software via interrupts. 

PCI Express Hot‐Plug (like PCI) is designed as a “no surprises” Hot‐Plug meth‐ odology. In other words, the user is not normally allowed to install or remove a PCI Express card without first notifying the system. Software then prepares both the card and slot and finally indicates to the operator the status of the hot plug process and notification that installation or removal may now be per‐ formed. 

## **Surprise Removal Notification** 
