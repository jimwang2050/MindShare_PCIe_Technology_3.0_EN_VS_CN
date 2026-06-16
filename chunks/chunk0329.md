The LTR capability in a device is discovered using a new bit in the PCIe Device Capability 2 Register, as shown in Figure 16‐38 on page 785, and enabled in the Device Control 2 Register, illustrated in Figure 16‐39 on page 785. The spec pre‐ scribes a sequence for enabling LTR, too: devices closest to the Root must be enabled first, working down to the Endpoints. An Endpoint must not be enabled unless its associated Root Port and all intermediate switches also sup‐ port LTR and have been enabled to service it. It’s permissible for some End‐ points to support LTR while others do not. If a Root Port or switch Downstream Port receives an LTR message but doesn’t support it or hasn’t been enabled yet, the message must be treated as an Unsupported Request. It’s recommended that Endpoints send an LTR message shortly after being enabled to do so. It’s strongly recommended that Endpoints not send more than two LTR messages within any 500  s period unless required by the spec. However, if they do, Downstream Ports must properly handle them and not generate an error based on that. 

**784** 

**Chapter 16: Power Management** 

## _Figure 16‐38: LTR Capability Status_ 

**==> picture [235 x 146] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capability 2 Register<br>31 24  23  22  21  20  19  18 14  13   12  11  10  9  8   7  6  5  4  3        0<br>RsvdP RsvdP<br>Max End-End<br>TLP Prefixes<br>End-End TLP<br>Prefix Supported<br>Extended Fmt<br>Field Supported<br>TPH Completer Supported<br>LTR Mechanism Supported<br>O<br>**----- End of picture text -----**<br>


_Figure 16‐39: LTR Enable_ 

**==> picture [218 x 152] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Control 2 Register<br>15  14  13         11  10  9  8   7  6  5  4  3        0<br>RsvdP<br>End-End TLP Prefix Blocking<br>LTR Mechanism Enable<br>IDO Completion Enable<br>IDO Request Enable<br>AtomicOp Egress Blocking<br>AtomicOp Requester Enable<br>ARI Forwarding Enable<br>Completion Timeout Disable<br>Completion Timeout Value<br>**----- End of picture text -----**<br>


The target for LTR information is the Root Complex. Participating downstream devices all report their values but the Port just uses the smallest value that was reported as the latency limit for all devices accessed through that Port. The Root is not required to honor requested service latencies but is strongly encouraged to do so. 

**785** 

**PCI Ex ress Technolo p gy** 

## **LTR Messages** 

The LTR message itself has the format shown in Figure 16‐40 on page 788, where it can be seen that the Routing type 100b (point‐to‐point) and the LTR message code is 0001 0000b. Two latency values are reported, one for Requests that must be snooped and another for Requests that will not be snooped and therefore should complete more quickly. As seen in the diagram, the format for both is the same and includes the following fields: 

- Latency Value and Scale ‐ combine to give a value in the range from 1ns to about 34 seconds. Setting these fields to all zeros indicates that any delay will affect the device and thus the best possible service is requested. The meaning of the latency is defined as follows: 

   - For Read Requests, it’s the delay from sending the END symbol in the Request TLP until receiving the STP symbol in the first Completion TLP for that Request. 

   - For Write Requests, it relates to Flow Control back‐pressure. If a write has been issued but the next write can’t proceed due to a lack of Flow Control credits, the latency is the time from the last symbol of that write (END) until the first symbol of the DLLP that gives more credits (SDP). In other words, this represents the time within which the Root Port should be able to accept the next write. 

- Requirement ‐ can be set for none, or one, or both to indicate whether that latency value is required. If a device doesn’t implement one of these traffic types or has no service requirements for it, then this bit must be cleared for the associated field. If a device has reported requirements but has since been directed into a device power state lower than D0, or if its LTR Enable bit has been cleared, the device must send another LTR message reporting that these latencies are no longer required. 

## **Guidelines Regarding LTR Use** 

Endpoints have a few guidelines regarding the use of LTR: 

1. It’s recommended that they send an updated LTR message every time their service requirements change, and the spec spends some time going over examples of this. The bottom line here is that devices need to take all the delays into account when making a change to the service requirements. That accounting includes time for the reference clock to be restored if was turned off, for the Link to be brought back to L0, for the LTR message to be delivered, and for the platform to prepare to handle the new requirement. 

2. If the latency tolerance is being reduced, it’s recommended that the LTR message be sent far enough ahead of the first associated Request to ensure that the platform is ready. 

**786** 

**Chapter 16: Power Management** 

3. If the latency tolerance is being increased, then the LTR message to report that should immediately follow the final Request that used the previous latency value. 

4. To achieve the best overall platform power efficiency, it’s recommended that Endpoints buffer Requests as much as they can and then send them in bursts that are as long as the Endpoint can support. 

Multi‐Function Devices (MFDs) have a few rules of their own. For example, they must send a “conglomerated” LTR message as follows: 

1. Reported latency values must reflect the lowest values associated with any Function. The snoop and no‐snoop latencies could be associated with differ‐ ent Functions, but if none of them have a requirement for snoop or no‐snoop traffic, then the requirement bit for that type must not be set. 

2. MFDs must send a new LTR message upstream if any of the Functions changes its values in a way that affects the conglomerated value. 

Switches have a similar set of rules related to LTR. Basically, they collect the messages from Downstream Ports that have been enabled to use LTR and send a “conglomerated” message upstream according to the following rules: 

1. If the Switch supports LTR, it must support it on all of its Ports. 

2. The Upstream Port is allowed to send LTR messages only when the LTR Enable bit is set or shortly after software has cleared it so it can report that any previous requirements are no longer in effect. 

3. The conglomerated LTR value is based on the lowest value reported by any participating Downstream Port. If the Requirement bit is clear, or an invalid value is reported, the latency is considered effectively infinite. 

4. If any Downstream Port reports that an LTR value is required, the Require‐ ment bit will be set for that type in the LTR message forwarded upstream. 

5. The LTR values reported upstream must take into account the latency of the Switch itself. If the Switch latency changes based on its operational mode, it must not be allowed to exceed 20% of the minimum value reported on all Downstream Ports. The value reported on the Upstream Port is the mini‐ mum reported value on all the Downstream Ports minus the Switch’s own latency, although the value can’t be less than zero. 

6. If a Downstream Port goes to DL_Down status, previous latencies for that Port must be treated as invalid. If that changes the conglomerated values upstream then a new message must be sent to report that. 

7. If a Downstream Port’s LTR Enable bit is cleared, any latencies associated with that Port must be considered invalid, which may also result in a new LTR message being sent upstream. 

8. If any Downstream Ports receive new LTR values that would change the conglomerated value, the Switch must send a new LTR message upstream to report that. 

**787** 

**PCI Ex ress Technolo p gy** 

Finally, the Root Complex also has a few rules related to LTR: 

1. The RC is allowed to delay processing of a device Request as long as it satis‐ fies the service requirements. One application of this might be to buffer up several Requests from an Endpoint and service them all in a batch. 

2. If the latency requirements are updated while a series of Requests is in progress, the new values must be comprehended by the RC prior to servic‐ ing the next Request, and within less time than the previously reported latency requirements. 

_Figure 16‐40: LTR Message Format_ 

**==> picture [350 x 264] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1<br>Byte 0 Fmt Type R TC Rsv T E Attr AT Length (Reserved)<br>0 0 1 1 0  1 0 0 0 0 0 D P 0 0 0 0<br>Message Code<br>Byte 4 Requester ID Tag 0001 0000<br>Byte 8 Reserved<br>Byte 12 No-Snoop Latency Snoop Latency<br>Point-to-Point<br>15 14 13 12 10 9 0<br>Rsv [Latency] Latency Value<br>Scale<br>Requirement<br>Scale:<br>000 - x 1ns   001 - x 32 ns<br>010 - x 1K ns   011 - x 32K ns<br>100 - x 1M ns  101 - x 32M ns<br>110 - x not permitted<br>**----- End of picture text -----**<br>


**788** 

**Chapter 16: Power Management** 

## **LTR Example** 

To illustrate the concepts discussed so far, consider the example topology shown in Figure 16‐41 on page 789. Here, the Endpoint on the lower left has delivered an LTR message to the Switch reporting a Snoop Latency requirement of 1200ns. At this point, none of the other Endpoints connected to the Switch has reported an LTR value, so that becomes the conglomerated value to be reported upstream. However, the Switch has an internal latency of 50ns so that must be subtracted from the value to be reported, resulting in the Upstream Port sending an LTR message reporting 1150ns to the Root Port. 

_Figure 16‐41: LTR Example_ 

**==> picture [122 x 121] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>value<br>Conglomerate  i<br>value 1200 ns —<br>& _<br>1200 ns<br>[| Va i<br>**----- End of picture text -----**<br>


Next, the Legacy Endpoint delivers an LTR message with a large latency requirement of 5000ns, as shown in Figure 16‐42 on page 790. Since this is larger than the current conglomerate value for the Switch, no LTR message is sent for this case. 

**789** 

**PCI Ex ress Technolo p gy** 

_Figure 16‐42: LTR ‐ Change but no Update_ 

**==> picture [176 x 112] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  1150 ns<br>value<br>—<br>Conglomerate  1200 ns<br>value<br>Switch EndpointPCle<br>e ¢<br>Vl i IN 5000 ns<br>**----- End of picture text -----**<br>


In the next stage, the middle Endpoint reports its LTR value as 700ns. This is smaller than the current conglomerate value, so the Switch calculates the new value of 650ns by subtracting its internal latency and forwards that upstream as an LTR message. That makes the current latency requirement for that Root Port 650ns, as seen in Figure 16‐43 on page 791. 

Finally, the Link to the middle Endpoint stops working for some reason as shown in Figure 16‐44 on page 791, and the Switch Port reports DL_Down. Con‐ sequently, the LTR value for that Port must be considered invalid. Since its value was being used as the current conglomerate value, the conglomerate will be updated to the lowest value that is still valid, which is the 1200ns reported by the left‐most Endpoint. The Switch will then subtract its internal latency and report 1150ns to the Root Port with a new LTR message. 

**790** 

**Chapter 16: Power Management** 

_Figure 16‐43: LTR ‐ Change with Update_ 

**==> picture [107 x 150] intentionally omitted <==**

**----- Start of picture text -----**<br>
Conglomerate  650 ns<br>value<br>Conglomerate<br>value 700 ns<br>> _<br>Va i<br>ES}<br>EndpointPCle # =ndnaint§PCle<br>700 ns<br>**----- End of picture text -----**<br>

