OBFF is an optional hint that a system can use to inform components about optimal time windows for traffic. It’s just a hint, though, so bus‐master‐capable devices can still initiate traffic whenever they like. Of course, power consump‐ tion will be negatively affected if they do, so overriding the OBFF hints should be avoided as much as possible. The information is communicated in one of two ways: by sending messages to the Endpoints or by toggling the WAKE# pin. If both options are available, using the pin is strongly recommended because it avoids the counter‐productive step of using excess power, possibly across sev‐ eral Links, to inform a component about the current system power state. In fact, the OBFF message should only be used if the WAKE# pin is not available. 

Figure 16‐33 on page 778 gives an example showing a mix of both communica‐ tion types. Using the pin is required if it’s available, but in this example it’s not an option between the two switches. To work around this problem, the upper switch can translate the state received on the WAKE# pin into a message going downstream. It should perhaps be noted here that switches are strongly encour‐ aged to forward all OBFF indications downstream but not required to do so. It may be necessary, especially when using messages, to discard or collapse some indications and that is permitted. 

_Figure 16‐33: OBFF Signaling Example_ 

**==> picture [207 x 206] intentionally omitted <==**

**----- Start of picture text -----**<br>
Root Complex<br>WAKE#<br>Endpoint<br>Switch<br>Endpoint<br>OBFF<br>Message<br>Endpoint<br>WAKE# Switch<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


**778** 

**Chapter 16: Power Management** 

**Using the WAKE# Pin.** This pin, previously only used to inform the sys‐ tem that a component needed to have power restored, is given an extra meaning as the simplest and lowest‐power option for communicating sys‐ tem power status to PCIe components. It’s optional, and the protocol is fairly simple: the WAKE# pin toggles to communicate the system state. As seen in Figure 16‐34 on page 779, there are several transitions but only three states, which are described below: 

1. CPU Active ‐ system awake; all transactions OK. This is every compo‐ nent’s initial state. 

2. OBFF ‐ system memory path available; transfers to and from memory are OK, but other transactions should wait for a higher power state. 

3. Idle ‐ wait for a higher state before initiating. 

_Figure 16‐34: WAKE# Pin OBFF Signaling_ 

**==> picture [382 x 212] intentionally omitted <==**

**----- Start of picture text -----**<br>
Transition Event OBFF Message Code<br>Idle OBFF OBFF<br>Idle CPU Active CPU Active<br>OBFF or CPU Active Idle Idle<br>OBFF CPU Active CPU Active<br>CPU Active               OBFF OBFF<br>**----- End of picture text -----**<br>


When the CPU Active or OBFF state is indicated, it’s recommended that the platform not return to the Idle state for at least 10  s so as to give compo‐ nents enough time to deliver the packets they may have been queuing up while in the previous Idle state. However, since that timing isn’t required, it’s also recommended that Endpoints not assume they’ll have a certain amount of time in a CPU Active or OBFF window. Along the same lines, the platform is allowed to indicate that it’s going to Idle before it actually does 

**779** 

## **PCI Ex ress Technolo p gy** 

so as to give components advance notice that it’s time to finish. The case this early notice is specifically designed to avoid is having an Endpoint start a transfer just as the platform goes to Idle, causing an immediate exit from the Idle state. The spec strongly recommends that this should be the only reason for an early indication of the Idle state and also that this advance notice time should be as short as possible. 

Interestingly, the WAKE# pin can still be used for its original purpose of allowing a component to wake the system, and it’s no surprise that this might confuse other components that are monitoring that pin for OBFF information. That could result in sub‐optimal behavior in power or perfor‐ mance, but this is considered a recoverable situation so no steps were taken to guard against it. To cover all of these cases, any time the signal is unclear the default state will be CPU Active. 

**Using the OBFF Message.** As mentioned earlier, OBFF information can be communicated using a message, although it’s recommend that this only be used if the WAKE# pin is not available. These messages only flow down‐ stream from the Root. The message contents are shown in Figure 16‐35 on page 781, including the Routing type 100b (point‐to‐point) and an OBFF Code that gives the following values (all other codes are reserved): 

1. 1111b ‐ CPU Active 

2. 0001b ‐ OBFF 

3. 0000b ‐ Idle 

If a reserved code is received, components must treat it as “CPU Active.” If a Port receives an OBFF message but doesn’t support OBFF or hasn’t enabled it yet, it must treat it as an Unsupported Request (Completion sta‐ tus UR). 

**780** 

**Chapter 16: Power Management** 

_Figure 16‐35: OBFF Message Contents_ 

**==> picture [359 x 189] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Byte 0 Fmt Type R TC R At R T T E Attr AT Length<br>0 0 1 1 0  1 0 0 tr H D P<br>Message Code<br>Byte 4 Requester ID Tag 0001 0010<br>Byte 8 Reserved for Error Messages<br>OBFF<br>Byte 12 Reserved for Error Messages Code<br>Point-to-Point 0000b = Idle<br>0001b = OBFF<br>1111b  =  CPU Active<br>**----- End of picture text -----**<br>


Support for OBFF is indicated via the Device Capability 2 register (Figure 16‐36 on page 782), and enabled using the Device Control 2 register (Figure 16‐37 on page 783). Note that both the pin and message options may be available. However, the pin method is preferred because it is the lower power option. 

Note that there are two variations for enabling a component to forward OBFF messages, and the difference between them has to do with handling a targeted Link that’s not in L0. In Variation A, the message will only be sent if the Link is in L0. If it’s not, the message is simply dropped to avoid the cost of waking the Link. This is preferred for Downstream Ports when the Device below it is not expected to have time‐critical communication requirements and can indicate its need for non‐urgent attention by simply returning the Link to L0. For Variation B, the message will always be for‐ warded and the Link will be returned to L0. This variation is preferred when the downstream Device can benefit from timely notification of the platform state. 

**781** 

## _Figure 16‐36: OBFF Support Indication_ 

**==> picture [364 x 231] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Capability 2 Register<br>31 24  23  22  21  20  19 18 14  13   12  11  10  9  8   7  6  5  4  3        0<br>[eee] o vem<br>RsvdP RsvdP<br>[eee] “ TET<br>Za<br>See om [os] ||<br>eee] os Max End-End<br>TLP Prefixes<br>om<br>ede End-End TLP<br>ow Prefix Supported<br>owno Extended Fmt<br>ow Field Supported<br>ow<br>TPH Completer Supported<br>[see omJo LTR Mechanism Supported<br>No RO-enabled PR-PR Passing<br>128-bit CAS Completer Supported<br>OBFF Support<br>64-bit AtomicOp Completer Supported<br>00 – Not supported 32-bit AtomicOp Completer Supported<br>AtomicOp Routing Supported<br>01 – Message only<br>ARI Forwarding Supported<br>10 – WAKE# only<br>Completion Timeout Disable Supported<br>11 – Both Completion Timeout Ranges Supported<br>**----- End of picture text -----**<br>


When using WAKE#, enabling any Root Port to assert it is considered a glo‐ bal enable unless there are multiple WAKE# signals, in which case only those associated with that Port are affected. When using the OBFF message, enabling a Root Port only enables the messages on that Port. The expecta‐ tion in the spec is that all Root Ports would normally be enabled if any of them are, so as to ensure that the whole platform was enabled. However, selectively enabling some Ports and not others is permitted. 

When enabling Ports for OBFF, the spec recommends that all Upstream Ports be enabled before Downstream Ports, and Root Ports be enabled last of all. For unpopulated hot plug slots this isn’t possible. For that case enabling OBFF using the WAKE# pin to the slot is permitted, but it’s recom‐ mended that the Downstream Port above the slot not be enabled to deliver OBFF messages. 

**Chapter 16: Power Management** 

## _Figure 16‐37: OBFF Enable Register_ 

**==> picture [236 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device Control 2 Register<br>15  14  13 11  10  9  8   7  6  5  4  3        0<br>RsvdP<br>End-End TLP Prefix Blocking<br>LTR Mechanism Enable<br>IDO Completion Enable<br>IDO Request Enable<br>AtomicOp Egress Blocking<br>AtomicOp Requester Enable<br>ARI Forwarding Enable<br>Completion Timeout Disable<br>Completion Timeout Value<br>OBFF Enable<br>00 – Disabled<br>01 – Enabled with Message signaling Variation A<br>10 – Enabled with Message signaling Variation B<br>11 – Enabled using WAKE# signaling<br>**----- End of picture text -----**<br>


Finally, let’s refer back to the earlier example in Figure 16‐33 on page 778 to consider what these registers might look like for that case. The Downstream Port of the switch that connects to the lower switch will have a value for OBFF Support of 01b ‐ Message Only, while its Upstream Port might have a value of 11b ‐ Both. These values might be hard coded into the device or hardware initialized in some other fashion to make them visible to software after a reset. The Downstream Port would need to have an OBFF Enable value of 01b or 10b ‐ Enabled with Message variation A or B so it could deliver an OBFF message. The Upstream Port would expect to have an OBFF Enable value of 11b ‐ Enabled with WAKE# signaling. The spec points out that when a switch is configured to use the different methods when going from one Port to another, it’s required to make the translation and for‐ ward the indications. 

**783** 

**PCI Ex ress Technolo p gy** 

## **LTR (Latency Tolerance Reporting)** 

The second new feature added to improve PM efficiency is called Latency Toler‐ ance Reporting (LTR). This optional capability allows devices to report the delay they can tolerate when requesting service from the platform so that PM policies for platform resources like main memory can take that into consider‐ ation. If software supports it, this provides good performance for devices when they need it and lower power for the system when they don’t need a fast response. One simple way of using this information would be to allow the sys‐ tem to postpone waking up to service a request as long as the latency tolerance was still met. 

The meaning of “latency tolerance” is not made explicitly clear in the spec, but some things are mentioned that might play into it. For example, the latency tol‐ erance may affect acceptable performance or it may impact whether the compo‐ nent will function properly at all. Clearly, such a distinction would make a big difference in designing a PM policy. Similarly, the device may use buffering or other techniques to compensate for latency sensitivity and knowledge of that would be useful for software. 

## **LTR Registers** 
