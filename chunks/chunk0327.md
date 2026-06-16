3. The corresponding split completion must push all previously posted PME messages ahead of it based on transaction ordering rules. 

4. The Root Complex cannot accept a new PME message because the queue is full, so the path is temporarily blocked. But that also means that the read completion can’t reach the Root Complex to clear the older entry in the queue. 

5. No progress can be made and deadlock occurs. 

## **The Solution** 

The problem is avoided if the Root Complex always accepts new PME mes‐ sages, even when they would overflow the queue. In this case, the Root simply discards the later PME messages. To prevent a discarded PME message from being lost permanently, a device that sends a PME message is required to mea‐ sure a time‐out interval, called the PME Service Time‐out. If the device’s PME_Status bit is not cleared with 100 ms (+ 50%/‐ 5%), it assumes its message must have been lost and it re‐issues the message. 

## **The PME Context** 

Devices that generate PME must continue to power portions of the device that are used for detecting, signaling, and handling PME events, referred to collec‐ tively as the PME context. Devices that support PME in the D3cold state use aux‐ iliary power to maintain the PME context when the main power is removed. Items that are typically part of the PME context include: 

- PME_Status bit (required) — set when a device sends a PME message and cleared by PM software. Devices that support PME in the D3cold state must implement the PME_Status bit as “sticky,” meaning that the value survives a fundamental reset. 

**771** 

## **PCI Ex ress Technolo p gy** 

- PME_Enable bit (required) — this bit must remain set to continue enabling a Function’s ability to generate PME messages and signal wakeup. Devices that support PME in the D3cold state must implement PME_Enable as “sticky,” meaning that the value survives a fundamental reset. 

- Device‐specific status information — for example, a device might preserve event status information in cases where several different types of events can trigger a PME. 

- Application‐specific information — for example, modems that initiate wakeup would preserve Caller ID information if supported. 

## **Waking Non-Communicating Links** 

When a device that supports PME in the D3cold state needs to send a PME mes‐ sage, it must first transition the Link to L0. This is sometimes referred to as a wakeup. PCI Express defines two methods of triggering the wakeup of non‐communicating Links: 

- Beacon — an in‐band indicator driven by AUX power 

- • WAKE# Signal — a sideband signal driven by AUX power 

In both cases, PM software must be notified to restore main power and the ref‐ erence clock. This also causes a fundamental reset that forces a device into the D0uninitialized state. Once the Link transitions to L0, the device sends the PME message. Since a reset is required to re‐activate the Link, devices must maintain PME context across the reset sequence described above. 

## **Beacon** 

This signaling mechanism is designed to operate on AUX power and doesn’t require much power. The beacon is simply a way of notifying the upstream component that software should be notified of the wakeup request. When switches receive a beacon on a downstream port, they in turn signal beacon on their upstream port. Ultimately, the beacon reaches the root complex, where it generates an interrupt that calls PM software. 

Some form‐factors require beacon support for waking the system while others don’t. The spec requires compliance with the form‐factor specs, and doesn’t require beacon support for devices if their form‐factor doesn’t. However, for “universal” components designed for use in a variety of form‐factors, beacon support is required. See “Beacon Signaling” on page 483 for details. 

**772** 

**Chapter 16: Power Management** 

## **WAKE#** 

PCI Express provides a sideband signal called WAKE# as a alternative to the beacon that can be routed directly to the Root or to other system logic to notify PM software. In spite of the desire to minimize the pin count of a Link, the moti‐ vation for adding this extra pin is easy to understand. The reason is that a com‐ ponent must consume auxiliary power to be able to recognize a beacon on a downstream port and then forward it to an upstream port. In a battery‐powered system auxiliary power is jealously guarded because it drains the battery even when the system isn’t doing any work. The preferred solution in that case would be to bypass as many components as possible when delivering the wakeup notification, and the WAKE# pin serves that purpose very well. On the other hand, if power is not a concern then the WAKE# pin might be considered less desirable. 

A hybrid implementation may also be used. In this case, WAKE# is sent to a switch, which in turn sends the beacon on its upstream port. The options are illustrated in Figure 16‐29 on page 774 A and B. Note that when asserted, the WAKE# signal remains low until the PME_Status bit is cleared by software. 

This signal must be implemented by ATX or ATX‐based connectors and cards as well as by the mini‐card form factor. No requirement is specified for embedded devices to use the WAKE# signal. 

**773** 

## **PCI Ex ress Technolo p gy** 

_Figure 16‐29: WAKE# Signal Implementations_ 

**==> picture [317 x 472] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>L2 State<br>(F) PM State D3<br>Switch<br>L2 State L2 State<br>PM State<br>PM State D3 PCIe D3 PCIe PM State D3<br>Endpoint (C) Endpoint<br>(D) Switch (E)<br>L2 State L2 State WAKE#<br>A Card Slots<br>Root Complex<br>L2 State<br>(F)<br>Switch PM State D3<br>Beacon signaling used from L2 State<br>switch to Root Complex.<br>PM State D3 PCIe PM StateD3 PCIe PM State D3<br>Endpoint Endpoint<br>(C)<br>(D) Switch (E)<br>L2 State WAKE#<br>B Card Slots<br>**----- End of picture text -----**<br>


**774** 

**Chapter 16: Power Management** 

## **Auxiliary Power** 

Devices that support PME in the D3cold state must support the wakeup sequence and are allowed by the PCI‐PM spec to consume the maximum auxil‐ iary current of 375 mA (otherwise only 20mA). The amount of current they need is reported in the _Aux_Current_ field of the PM Capability registers. Auxiliary power is enabled when the _PME_Enable_ bit is set within the PMCSR register. 

PCI Express extends the use of auxiliary power beyond the limitations given by PCI‐PM. Now, any Device may consume the maximum auxiliary current if enabled by setting the _Aux Power PM Enable_ bit of the Device Control register, illustrated in Figure 16‐30 on page 775. This gives devices the opportunity to support other things like SM Bus while in a low power state. As in PCI‐PM the amount of current consumed by a device is reported in the _Aux_Current_ field in the PMC register. 

_Figure 16‐30: Auxiliary Current Enable for Devices Not Supporting PMEs_ 

|||15|14|12|11|10|9|8|7|5|4|3|2|1|0|
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
|||||||||||||||||
|Bridge Config. Retry Enable/||||||||||||||||
|Initiate Function-Level Reset||||||||||||||||
|Max Read Request Size||||||||||||||||
||Enable No Snoop|||||||||||||||
||Aux Power PM Enable|||||||||||||||
|Phantom Functions Enable||||||||||||||||
|Extended Tag Field Enable||||||||||||||||
||Max Payload Size|||||||||||||||
|Enable Relaxed Ordering||||||||||||||||
||Unsupported Request|||||||||||||||
||Reporting Enable|||||||||||||||
|Fatal|Error Reporting Enable|||||||||||||||
||Non-Fatal Error|||||||||||||||
||Reporting Enable|||||||||||||||
||Correctable Error|||||||||||||||
||Reporting Enable|||||||||||||||



**775** 

**PCI Ex ress Technolo p gy** 

## **Improving PM Efficiency** 

## **Background** 

As processors and other system components acquire better power management mechanisms, peripherals like PCIe components start to appear as a bigger con‐ tributor to power consumption in PC systems. Earlier generations of PCIe allowed some software and hardware power management, but coordinating PM decisions with the system was not a high priority and consequently soft‐ ware visibility and control was limited. 

One problem that can arise from this lack of coordination happens when the system goes into a sleep state but the devices remain operational. Such devices can initiate interrupts or DMA traffic that would require the system to wake up to handle them, even thought they were low‐priority events, and thus defeat the goal of power conservation. 

It can also happen that the system is unaware of how long the devices can afford to wait from the time they request system service (like a memory read) until they get a response. Without that information, software is often forced to assume that the response time must always be minimal and therefore power management policies can’t afford enough time to do much. However, if the sys‐ tem was aware of time windows when a fast response was not needed, it could be more aggressive with power management and stay in a low power state for a longer time without risking performance problems. The 2.1 spec revision added two new features to address these problems. 

## **OBFF (Optimized Buffer Flush and Fill)** 

The first of these mechanisms is Optimized Buffer Flush and Fill, which pro‐ vides a mechanism for Endpoints to be made aware of the system power state and therefore the best times to do data transfers to and from the system. 

## **The Problem** 

The problem with bus‐master capable devices is that if they’re not aware of the system power status, they may initiate transactions at times when it would be better to wait. The diagram in Figure 16‐31 on page 777 illustrates the problem in simple terms: there are many components initiating events and as a result, 

**776** 

**Chapter 16: Power Management** 

the times without activity when the system is idle and can go to sleep are few and short‐lived. In contrast, Figure 16‐32 on page 777 illustrates an improve‐ ment in which the same events are grouped and serviced together so that the times when the system is idle enough to go to sleep are both more frequent and of longer duration. Clearly, this would result in better power conservation and fortunately, it’s not difficult to implement. PCIe components simply need to understand what they should do based on the system power state, and they’ll need a way to learn what that state currently is. 

_Figure 16‐31: Poor System Idle Time_ 

**==> picture [310 x 135] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Idle System Idle<br>Window Window<br>System Events<br>Endpoint A<br>Events<br>Endpoint B<br>Events<br>Endpoint C<br>Events<br>Time<br>**----- End of picture text -----**<br>


_Figure 16‐32: Improved System Idle Time_ 

**==> picture [327 x 158] intentionally omitted <==**

**----- Start of picture text -----**<br>
System Idle System Idle System Idle<br>Window Window Window<br>System Events<br>Endpoint A<br>Events<br>Endpoint B<br>Events<br>Endpoint C<br>Events<br>Time<br>LTR could also be used to inform system software of acceptable latency for<br>the endpoints between accesses, suggesting a limit on this idle time.<br>**----- End of picture text -----**<br>


**777** 

**PCI Ex ress Technolo p gy** 

## **The Solution** 
