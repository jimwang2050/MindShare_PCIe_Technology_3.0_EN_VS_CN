# 📘 第 18 章　延迟容忍度上报 (LTR) (Chapter 18. Latency Tolerance Reporting (LTR))

**MindShare PCI Express Technology 3.0 — Comprehensive Guide to Generations 1.x, 2.x and 3.0**

> 📁 **Source chunks**: `chunks/chunk0341.md` ... `chunks/chunk0343.md`
> 🎨 **Format**: 中英对照双语 · 中文灰底 (PCIe 6.2 Spec 模板)

---

## 📑 本章目录 (Table of Contents)

- [18.1 Add-in Card Capabilities — 延迟容忍度上报 (LTR)](#sec-18-1)
- [18.3 _20_ — 延迟容忍度上报 (LTR)](#sec-18-3)

<a id="sec-18-1"></a>
## 18.1 Latency Tolerance Reporting (LTR) | 延迟容忍度上报 (LTR)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

|2|**MRL Sensor Changed**— If an MRL Sensor is implemented, this is<br>set when a MRL Sensor state change is detected. If no sensor is<br>present this bit will always be zero.|
|3|**Presence Detect Changed**— set when a change has been detected in<br>the Presence Detect State bit.|
|4|**Command Completed**— If the No Command Completed Support<br>bit in the Slot Capabilities register is 0b, then this bit is set when a<br>hot plug command has completed and the Hot Plug Controller is<br>ready to accept another command. Technically, only this last mean‐<br>ing is guaranteed: the controller is ready to accept another com‐<br>mand, regardless of whether the previous one has actually<br>completed.|
|5|**MRL Sensor State**— when set, indicates the current state of the<br>MRL sensor, if implemented: 0b = MRL Closed, 1b = MRL Open|
|6|**Presence Detect State**— this bit indicates the presence of a card in a<br>slot and is required for all Downstream Ports that implement a slot.<br>Its value is the logical “OR” of Physical Layer’s Detection logic and<br>any other side‐band detect mechanism implemented for the slot<br>(such as PRSNT1# and PRSNT2#). The big difference between them<br>is that the pins require no power to physically detect the card and<br>can thus report on it without needing the power restored, while<br>using the Physical Layer Detect logic does need power.|


_Table 19‐7: Slot Status Register Fields and Descriptions (Continued)_ 

|**Bit**<br>**Location**|**Register Name and Description**|
|---|---|
|7|**Electromechanical Interlock Status**—If an Electromechanical Inter‐<br>lock is implemented, this bit indicates whether it is engaged (1b) or<br>disengaged (0b).|
|8|**Data Link State Changed**— This bit is set when the Data Link<br>Layer Link Active bit in the Link Status register changes. In response<br>to this event, software must read the Data Link Layer Link Active bit<br>to determine whether the Link is active before sending configura‐<br>tion cycles to the hot plugged device.|


## **Add-in Card Capabilities** 

The Device Capability register, seen in Figure 19‐8 on page 873, also has fields relevant to add‐in cards that record the power reported by the Hot Plug Con‐ troller as being available to their slot. This information must be communicated automatically with a Set_Slot_Power_Limit Message whenever either of these takes place: 

- A configuration write to the Slot Capabilities register changes the Slot Power Limit Value and Slot Power Limit Scale values. 

- The Link transitions from non‐DL_UP to DL_Up status (unless the Slot Capabilities register has not yet been initialized). 

The message updates the Captured Slot Power Limit Value and Scale registers with the values in the message, making this information readily available to its device driver. 
_Figure 19‐8: Device Capabilities Register_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


## **Quiescing Card and Driver** 

## **General** 

Prior to removing a card from the system, two things must occur: the device driver must stop accessing the card, and the card must stop initiating or responding to new Requests. How this is accomplished is OS‐specific, but the following must take place: 

- The OS must stop issuing new requests to the device’s driver or instruct the driver to stop accepting new requests. 

- The driver must terminate or complete all outstanding requests. 

- The card must be disabled from generating interrupts or Requests. 

When the OS commands the driver to quiesce itself and its device, the OS must not expect the device to remain in the system (in other words, it could be removed and not replaced with an identical card). 

## **Pausing a Driver (Optional)** 

Optionally, an OS could implement a “Pause” capability to temporarily stop driver activity in the expectation that the same card will be reinserted. If the card is not reinstalled within a reasonable amount of time, however, the driver must be quiesced and then removed from memory. 

As an example, the currently‐installed card is failing or is being replaced with a later revision as an upgrade. If the operation is to appear seamless from a soft‐ ware and operational perspective, the driver would have to quiesce the device, save the current context (contents of registers, stack and instruction pointer of local micro‐controller, etc.) and turn off the power to the slot. The new card could then be installed and powered, and then, when its context is restored, it could resume normal operation where it left off. Of course, if the old card had failed, it may not be possible to simply resume operation. 

## **Quiescing a Driver That Controls Multiple Devices** 

If a driver controls multiple cards and it receives a command from the OS to quiesce its activity with respect to a specific card, it must only quiesce its activ‐ ity with that card and the card itself. 

## **Quiescing a Failed Card** 

If a card has failed, it may not be possible for the driver to complete requests previously issued to the card. In this case, the driver must detect the error, ter‐ minate the requests without completion, and attempt to reset the card. 

## **The Primitives** 

This section discusses the hot‐plug software elements and the information passed between them. For a review of the software elements and their relation‐ ships to each other, refer to Table 19‐1 on page 852. Communications between the Hot‐Plug Service within the OS and the Hot‐Plug System Driver is in the form of requests. The spec doesn’t define the exact format of these requests, but does define the basic request types and their content. Each request type issued to the Hot‐Plug System Driver by the Hot‐Plug Service is referred to as a _primi‐ tive_ . They are listed and described in Table 19‐8 on page 875. 
_Table 19‐8: The Primitives_ 

|**Primitive**|**Parameters**|**Description**|
|---|---|---|
|Query Hot‐Plug<br>System Driver|**Input**: None|Requests that the Hot‐Plug System<br>Driver return a set of Logical Slot<br>IDs for the slots it controls.|
||**Return**: Set of Logical Slot<br>IDs for slots controlled by<br>this driver.||
|Set Slot Status|**Inputs**:<br>• Logical Slot ID<br>• New slot state (on or<br>off).<br>• New Attention Indica‐<br>tor state.<br>• New Power Indicator<br>state.|This request is used to control the<br>slots and the Attention Indicator<br>associated with each slot. Good<br>completion of a request is indicated<br>by returning the Status Change Suc‐<br>cessful parameter. If a fault is<br>incurred during an attempted sta‐<br>tus change, the Hot‐Plug System<br>Driver should return the appropri‐<br>ate fault message (see middle col‐<br>umn). Unless otherwise specified,<br>the card should be left in the off<br>state.|
||**Return**: Request comple‐<br>tion status:<br>• status change successful<br>• fault—wrong frequency<br>• fault—insufficient<br>power<br>• fault—insufficient con‐<br>figuration resources<br>• fault—power fail<br>• fault—general failure||
|Query Slot<br>Status|**Input**: Logical Slot ID|This request returns the state of the<br>indicated slot (if a card is present).<br>The Hot‐Plug System Driver must<br>return the Slot Power status infor‐<br>mation.|
||**Return**:<br>• Slot state (on or off)<br>• Card power require‐<br>ments.||


_Table 19‐8: The Primitives (Continued)_ 

|**Primitive**|**Parameters**|**Description**|
|---|---|---|
|Async Notice of<br>Slot Status<br>Change|**Input**: Logical Slot ID|This is the only primitive (defined<br>by the spec) that is issued to the<br>Hot‐Plug Service by the Hot‐Plug<br>System Driver. It is sent when the<br>Driver detects an unsolicited<br>change in the state of a slot. Exam‐<br>ples would be a run‐time power<br>fault or a card installed in a previ‐<br>ously‐empty slot with no warning.|
||**Return**: none||


## **Introduction to Power Budgeting** 

The primary goal of the PCI Express power budgeting capability is to allocate power for PCI Express hot plug devices that are added to the system during runtime. This ensures that the system can allocate the proper amount of power and cooling for these devices. 

The spec states that “power budgeting capability is optional for PCI Express devices implemented in a form factor which does not require hot plug, or that are integrated on the system board.” None of the form factor specs released at the time of this writing required support for hot plug or the power budgeting capability, but these change often. 

System power budgeting is always required to support all system board devices and add‐in cards. The new capability provides mechanisms for managing the budgeting process for a hot‐plug card. Each form factor spec defines the min and max power for a given expansion slot. For example, the CEM spec limits the power an expansion card can consume prior to being fully enabled but, after it is enabled, it can consume the maximum amount of power specified for the slot. In the absence of the power budgeting capability registers, the system designer is responsible for guaranteeing that power has been budgeted cor‐ rectly and that sufficient cooling is available to support any compliant card installed into the connector. 

The spec defines the configuration registers to support the power budgeting process, but does not define the power budgeting methods and processes. The next section describes the hardware and software elements that would be involved in power budgeting, including the specified configuration registers. 
## **The Power Budgeting Elements** 

Figure 19‐10 illustrates the concept of Power Budgeting for hot plug cards. The role of each element involved in the power budgeting, allocation, and reporting process is listed and described below: 

- System Firmware for Power Management (used during boot time). 

- Power Budget Manager (used during run time). 

- Expansion Ports (to which card slots are attached). 

- Add‐in Devices (Power Budget Capable). 

## **System Firmware** 

Written by the platform designers the specific system, this is responsible for reporting system power information. The spec recommends the following power information be reported to the PCI Express power budget manager, which allocates and verifies power consumption and dissipation during runt‐ ime: 

- Total system power available. 

- Power allocated to system devices by firmware 

- Number and type of slots in the system. 

Firmware may also allocate power to PCIe devices that support the power bud‐ geting capability register set, such as a hot‐plug device used during boot time. The Power Budgeting Capability register, shown in Figure 19‐9 on page 878, contains a System Allocated bit that is hardware initialized (usually by firm‐ ware) to notify the power budget manager that power for this device has already been included in the system power allocation. If so, the Power Budget Manager still needs to read and save the power information for the hot‐plug devices that were allocated in case they are later removed during runtime. 

_Figure 19‐9: Power Budget Registers_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


## **The Power Budget Manager** 

This initializes when the OS installs and receives power‐budget information from system firmware, although the spec does not define the method for deliv‐ ering this information. This manager is responsible for allocating power for all PCI Express devices including: 

- PCI Express devices that have not already been allocated by the system (including embedded devices that support power budgeting). 

- Hot‐plugged devices installed at boot time. 

- New devices added during runtime. 

## **Expansion Ports** 

Figure 19‐10 on page 880 illustrates a hot plug port that must have the Slot Power Limit and Slot Power Scale fields within the Slot Capabilities register implemented. The firmware or power budget manager must load these fields with a value that represents the maximum amount of power supported by this Port. When software writes to these fields the Port automatically delivers a Set_Slot_Power_Limit message to the device. These fields are also written when software configures a new card that has been added as a hot plug installation. 
## Spec requirements: 

- Any Downstream Port that has a slot attached (the Slot Implemented bit in its PCIe Capabilities register is set) must implement the Slot Capabilities register. 

- Software must initialize the Slot Power Limit Value and Scale fields of the Slot Capabilities register of the Downstream Port that is connected to an add‐in slot. 

- Upstream Ports must implement the Device Capabilities register. 

- When a card is installed in a slot and software updates the power limit and scale values in the Downstream Port, that Port will automatically send the Set_Slot_Power_Limit message to the Upstream Port on the installed card. 

- The recipient of the Message must use the data payload to limit its power usage for the entire card, unless the card will never exceed the lowest value specified in the corresponding electromechanical spec. 

## **Add-in Devices** 

Expansion cards that support the power budgeting capability must include the Slot Power Limit Value and Slot Limit Scale fields within the Device Capabilities register, and the Power Budgeting Capability register set for reporting power‐ related information. 

These devices must not consume more than the lowest power specified by the form factor spec. Once power budgeting software allocates additional power via the Set_Slot_Power_Limit message, the device can consume the power that has been specified, but not until it has been configured and enabled. 

**Device Driver** —The device’s software driver is responsible for verifying that sufficient power is available for proper device operation prior to enabling it. If the power is lower than that required by the device, the device driver is respon‐ sible for reporting this to a higher software authority. 

_Figure 19‐10: Elements Involved in Power Budget_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>

## **Slot Power Limit Control** 

Software is responsible for determining the maximum power that an expansion device is allowed to consume. This allocation is based on the power partitioning within the system, thermal capabilities, etc. Knowledge of the system’s power and thermal limits comes from system firmware. The firmware or power man‐ ager is responsible for reporting the power limits to each expansion port. 

## **Expansion Port Delivers Slot Power Limit** 

Software writes to the _Slot Power Limit Value_ and _Slot Power Limit Scale_ fields of the Slot Capability register to specify the maximum power that can be con‐ sumed by the device. Software is required to specify a power value that reflects one of the maximum values defined by the spec. For example, revision 2.0 of the CEM spec defines power usage as listed in Table 19‐9. 

An interesting note about these values is that a standard‐height x1 server card is limited to 10W after a reset and is only allowed to use the full 25W after it’s been configured and enabled. Similarly, a x16 graphics card will be limited to 25W until configured and enabled to use the full 75W. 

_Table 19‐9: Maximum Power Consumption for System Board Expansion Slots_ 

||**X1 Link**|**X1 Link**|**X4/X8 Link**|**X16 Link**|**X16 Link**|
|---|---|---|---|---|---|
|Standard Height|10W<br>(max ‐<br>desktop)|25W<br>(max ‐<br>server)|25W (max)|25W<br>(max ‐<br>server)|75W<br>(max ‐<br>graph‐<br>ics card)|
|Low Profile Card|10W (max)||25W (max)|25W (max)||


In addition to the base CEM spec, two more specs have been defined for higher‐ powered devices. First is the PCIe x16 Graphics 150W‐ATX Spec 1.0, which defines a video card that’s able to draw 75W from the card connector and another 75W from a separate 3‐pin ATX power connector. The second is the PCIe 225W/300W High Power CEM Spec 1.0, which extends this by adding another 3‐pin power connector to achieve 225W, or a 4‐pin ATX connector that brings the total to 300W. 

## **PCI Express Technology** 

When the Slot Power registers are written by power budget software, the expan‐ sion port sends a Set_Slot_Power_Limit message to the expansion device. This procedure is illustrated in Figure 19‐11 on page 882. 

_Figure 19‐11: Slot Power Limit Sequence_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


1. When Hot Plug software is notified of a card insertion request, Power and Clock are restored to the slot. 

2. Hot Plug software calls configuration and power budgeting software to configure and allocate power to the device. 

3. Power budget software may interrogate the card to determine it's power requirements and characteristics. 

4. Power is then allocated based on the device's requirements and the system's capabilities 5. Power management software writes to the Slot Power Scale and Slot Power Value fields within the expansion port. 

6. Writes to these fields command the port to send the Set_Slot_Power_Limit message to convey the contents of the Slot Power fields. 

7. The slot receives the message and updates its Captured Slot Power Limit Value and Scale fields. 

8. These values limit the power that the expansion device can consume once it is enabled by its device driver. 
## **Expansion Device Limits Power Consumption** 

The device driver reads the values from the Captured Slot Power Limit and Scale fields to verify that the power available is sufficient to operate the device. Several conditions may exist: 

- Enough power is available to operate the device at full capability. In this case, the driver enables the device by writing to the configuration Com‐ mand register, permitting the device to consume power up to the limit spec‐ ified in the Power Limit fields. 

- The power available is sufficient to operate the device but not at full capa‐ bility. In this case, the driver is required to configure the device such that it consumes no more power than specified in the Power Limit fields. 

- The power available is insufficient to operate the device. In this case, the driver must not enable the card and must report the inadequate power con‐ dition to the upper software layers, which should in turn inform the end user of the problem. 

- The power available exceeds the maximum power specified by the form factor spec. This condition should not occur. but, if it does, the device is not permitted to consume power beyond the maximum permitted by the form factor. 

- The power available is less than the lowest value specified by the form fac‐ tor spec. This is a violation of the spec, which states that the expansion port “must not transmit a Set_Slot_Power_Limit Message that indicates a limit lower than the lowest value specified in the electromechanical spec for the slotʹs form factor.” 

Some expansion devices may consume less power than the lowest limit speci‐ fied for their form factor. Such devices are permitted to discard the information delivered in the Set_Slot_Power_Limit Messages. When the Slot Power Limit Value and Scale fields are read, these devices return zeros. 

## **The Power Budget Capabilities Register Set** 

These registers permit power budgeting software to allocate power more effec‐ tively based on information provided by the device through its power budget data select and data register. This feature is similar to the data select and data fields within the power management capability registers. However, the power budget registers provide more detailed information to software to aid it in determining the effects of expansion cards that are added during runtime on 

## **PCI Express Technology** 

the system power budget and cooling requirements. Through this capability, a device can report the power it consumes: 

- from each power rail 

- in various power management states 

- in different operating conditions 

These registers are not required for devices implemented on the system board or on expansion devices that do not support hot plug. Figure 19‐12 on page 884 illustrates the power budget capabilities register set and shows the data select and data field that provide the method for accessing the power budget information.

</td>
<td style="background-color:#e8e8e8">

端点和根端口都可选地允许充当 AtomicOp 请求者和完成者，这可能看起来出乎意料，因为至少在 PC 中，这种事务通常仅由中央处理器发起。但是现代系统可以包括充当协处理器的端点，在这种情况下，它需要能够使用 AtomicOps 来正确处理协议。所有三个命令都支持 32 位和 64 位操作数，而 CAS 还支持 128 位操作数。实际使用的大小将在头部的 Length 字段中给出。具有对等访问功能的路由元素（如交换机端口和根端口）将需要支持 AtomicOp 路由功能，以便能够识别和路由这些请求。

很自然地会出现一个问题，即如何指示系统（根复合体）将生成这些新命令以响应处理器活动，因为可能没有直接类似的处理器总线命令。规范建议了两种方法。首先，根可以被设计为识别特定的处理器活动，并将其解释为响应"导出" PCIe AtomicOp。其次，可以使用类似于传统配置访问所使用的方法的基于寄存器的方法。在这种情况下，一个寄存器可以给出目标地址，而另一个寄存器指定应生成的命令，两者的组合将生成请求。

可以通过 Device Capabilities 2 寄存器中三个新位的存在来识别 AtomicOp 完成者，如图 20-10（在第 899 页）所示。该寄存器的第 6 位还标识路由元素是否能够路由 AtomicOp。

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

传统 PCI 当然不理解 AtomicOps，并且没有直接的方法将它们转换为 PCI 命令。因此，PCIe-to-PCI 桥不支持 AtomicOps。如果在该总线上需要原子访问，则必须使用传统的锁定协议来完成，并且规范声明 Locked Transactions 和 AtomicOps 可以在同一平台上同时运行。

_图 20-10：Device Capabilities 2 寄存器_

**==> 图片 [356 x 280] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 24 23 22 21 20 19 14 13 12 11 10 9 8 7 6 5 4 3 0<br>RsvdP RsvdP<br>Max End-End<br>TLP Prefixes<br>End-End TLP<br>Prefix Supported<br>Extended Fmt<br>Field Supported<br>TPH Completer Supported<br>LTR Mechanism Supported<br>No RO-enabled PR-PR Passing<br>128-bit CAS Completer Supported<br>64-bit AtomicOp Completer Supported<br>32-bit AtomicOp Completer Supported<br>AtomicOp Routing Supported<br>ARI Forwarding Supported<br>Completion Timeout Disable Supported<br>Completion Timeout Ranges Supported<br>**----- 图片文字结束 -----**


## **TPH (TLP 处理提示)**

添加有关系统应如何处理目标为内存空间的 TLP 的提示可以改善延迟和流量拥塞。规范将此特殊处理基本上描述为提供关于系统中多个可能的缓存位置中的哪一个是 TLP 临时副本的最佳位置的信息。

规范指出，由于为 TPH 描述的使用与缓存相关，因此通常使用目标为不可预取内存空间 (Non-prefetchable Memory Space) 的 TLP 是不合理的。如果需要这样的使用，则必须以某种方式保证缓存此类 TLP 不会引起不良副作用。

## **TPH 示例**

**设备写入到主机读取**。为了帮助阐明 TPH 的动机，考虑第 901 页的图 20-11 所示的示例。这里端点正在将数据写入内存以供 CPU 稍后使用。序列如下：

1. 首先，端点发送一个内存写入 TLP，其中包含映射到系统内存的地址。数据包被路由到根复合体 (RC)。

2. RC 将此识别为对可缓存内存空间的访问，并在其窥探 CPU 缓存时暂停其进度。这可能导致从 CPU 的回写周期以在事务可以继续之前更新系统内存，这显示为步骤 2a。

3. 一旦任何回写完成，RC 允许写入更新系统内存。

4. 在某个时刻，端点通知 CPU 数据已传送。

5. 最后，CPU 从内存中获取数据以完成序列。

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-11：TPH 示例_

**==> 图片 [202 x 111] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
4<br>2<br>e C)\ @ 5<br>2a<br>Roo! Complex @<br>3<br>1<br>lo [ |<br>**----- 图片文字结束 -----**


此序列有效，但通过在系统中添加中间缓存有改进性能的机会。为了说明这一点，考虑第 902 页的图 20-12 中所示的示例。从端点的角度来看，操作是相同的，但知道以不同方式处理它。现在的步骤如下：

1. 端点执行相同的内存写入，但这次包括 TPH 位。写入像以前一样通过交换机转发到 RC。

2. RC 理解此内存访问必须像以前一样窥探到 CPU。但是，一旦窥探处理完毕，RC 由 TPH 位通知将此 TLP 存储在中间缓存中，而不是转到系统内存。

3. 端点通知 CPU 数据项已传送。

4. CPU 从指定地址读取，但现在数据在中间缓存中找到，因此请求不会转到系统内存。这具有我们期望从缓存设计中获得的通常好处：更快的访问时间以及减少系统内存的流量。

这是一个简单的设备写入到主机读取 (DWHR) 示例，用于说明概念，但不难想象一个更复杂的系统，具有更大的拓扑，其中可以在交换机或其他位置放置其他缓存，以实现其他目标的相同好处。

_图 20-12：带系统缓存的 TPH 示例_

**==> 图片 [108 x 75] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
3<br>2 4<br>OC @VlEl@<br>Rant Camnlayx<br>Cache<br>1<br>**----- 图片文字结束 -----**


**主机写入到设备读取**。为了说明相反方向的概念（称为主机写入到设备读取 (HWDR)），考虑第 903 页的图 20-13 中所示的示例。在此示例中，CPU 在第一步中启动一个内存写入，其地址针对 PCIe 端点。该数据包包含 TPH 位，告诉 RC 应将其存储在目标附近的中间缓存中，而不是上例中使用的 RC 中的缓存。在这种情况下，内置于交换机中的缓存用于此目的。然后在第二步中将 TLP 转发到目标端点。当数据不经常更新但经常被端点读取时，此模型是有益的。这允许通常会转到系统内存的多个内存读取由缓存处理，从而减轻从交换机到 RC 的链路以及到内存的路径的负载。

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-13：用于目标为端点的 TLP 的 TPH 使用_

**==> 图片 [353 x 326] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
1<br>ox<br>oct Complex<br>Cache<br>rl i) i<br>PCle PCle<br>Cache<br>2<br>OWN: Endpoint Bridge<br>Yi i IN orto PCI-X PCI<br>§ EndpointPCle §§ EndpointLegacy PCI/PCI-X | |<br>Device to Device. One last example is illustrated in Figure 20‐14 on page<br>904, where two Endpoints communicate with each other (called Device Read/<br>Write to Device Read/Write or D*D*) through a shared memory location that is<br>directed by TPH bits to an intermediate cache. In this case, both may update dif‐<br>ferent locations that they need to handle as "read mostly", or one Endpoint may<br>update data that the other needs to read several times. In both cases, using the<br>intermediate cache improves system performance.<br>**----- 图片文字结束 -----**


## **PCI Express Technology**

_图 20-14：端点之间的 TPH 使用_

**==> 图片 [34 x 9] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
Cache<br>**----- 图片文字结束 -----**


## **TPH 头位**

TLP 头中的几位描述了如何使用提示。首先，如图 20-15（在第 905 页）顶部中间所示，TH（TLP 提示）位报告可选的 TPH 位是否正在用于 TLP。设置后，PH（处理提示位）指示下一级信息。

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-15：TPH 头位_

**==> 图片 [339 x 115] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>At T T E<br>Byte 0 Fmt Type R TC R tr R H D P Attr AT Length<br>Last DW 1st DW<br>Byte 4 Requester ID Tag BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- 图片文字结束 -----**


当 TH 位置位时，PH 位（如图 20-15（在第 905 页）右下角所示）取代地址字段中原本保留的两个 LSB。对于 32 位地址，这些是字节 11 [1:0]，而对于所示的 64 位地址，它们是字节 15 [1:0]。其编码在第 905 页的表 20-1 中描述。这些提示由请求者根据对使用中的数据模式的了解来提供，而完成者自己很难推断出这些信息。

_表 20-1：PH 编码表_

|**PH [1:0]**|**处理提示**|**使用模型**|
|---|---|---|
|00b|双向数据结构|指示主机和设备的频繁读/写访问。|
|01b|请求者|D*D*（设备到设备传输）。指示设备的频繁读/写访问。星号表示任一设备都可以读取或写入。|
|10b|目标|DWHR，HWDR（设备到主机或主机到设备的传输）。指示主机的频繁读/写访问。|
|11b|带优先级的目标|与目标相同，但具有额外的时间重用优先级信息。指示主机的频繁读/写访问以及所访问数据的高时间局部性。|


## **PCI Express Technology**

下一级信息是 Steering Tag 字节，它提供关于系统中缓存此 TLP 的最佳位置的系统特定信息。有趣的是，此字节在头中的位置取决于请求类型。对于 Posted Memory Writes，Tag 字段被重新用作 Steering Tag（不会返回完成，因此不需要 Tag），而对于 Memory Reads，两个 Byte Enable 字段被重新用于它（可预取读取不需要字节启用）。位的含义是实现特定的，但它们需要唯一地标识系统中所需缓存的位置。

规范中描述了 TPH 的两种格式，此级别的提示信息（TH + PH + 8 位 Steering Tag），称为基线 TPH (Baseline TPH)，是第一种，并且是提供 TPH 的所有请求所必需的。第二种格式使用 TLP 前缀来扩展 Steering Tag（有关更多详细信息，请参阅第 908 页上的"TLP Prefixes"）。

## **Steering Tags**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---


<img src="figures/embedded/page0902_img2_tight.png" alt="Figure from page 902" width="700">

<a id="sec-18-3"></a>
## 18.3 Latency Tolerance Reporting (LTR) | 延迟容忍度上报 (LTR)

<table>
<thead><tr><th width="50%">🇬🇧 English</th><th width="50%" style="background-color:#e8e8e8">🇨🇳 中文</th></tr></thead>
<tbody><tr>
<td>

The power budget information is maintained within a table that consists of one or more 32‐bit entries. Each table entry contains power budget information for the different operating modes supported by the device. Each table entry is selected via the data select field, and the selected entry is then read from the data field. The index values start at zero and are implemented in sequential order. When a selected index returns all zeros in the data field, the end of the power budget table has been located. Figure 19‐13 on page 885 illustrates the format and types of information available from the data field. 

_Figure 19‐12: Power Budget Capability Registers_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>

_Figure 19‐13: Power Budget Data Field Format and Definition_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


## _**20**_ 

## _**Updates for Spec Revision 2.1**_ 

## **Previous Chapter** 

The previous chapter describes the PCI Express hot plug model. A standard usage model is also defined for all devices and form factors that support hot plug capability. Power is an issue for hot plug cards, too, and when a new card is added to a system during runtime, it’s important to ensure that its power needs don’t exceed what the system can deliver. A mechanism was needed to query the power requirements of a device before giving it permission to oper‐ ate. Power budgeting registers provide that. 

## **This Chapter** 

This chapter describes the changes and new features that were added with the 2.1 revision of the spec. Some of these topics, like the ones related to power management, are described in other chapters, but for others there wasn’t another logical place for them. In the end, it seemed best to group them all together in one chapter to ensure that they were all covered and to help clarify what features were new. 

## **The Next Chapter** 

The next section is the book appendix which includes topics such as: Debugging PCI Express Traffic using LeCroy Tools, Markets & Applications of PCI Express Architecture, Implementing Intelligent Adapters and Multi‐Host Systems with PCI Express Technology, Legacy Support for Locking and the book Glossary. 

## **Changes for PCIe Spec Rev 2.1** 

The 2.1 revision of the spec for PCIe introduced several changes to enhance per‐ formance or improve operational characteristics. It did not add another data rate and that’s why it was considered an incremental revision. The modifica‐ tions can be grouped generally into four areas of improvement: System Redun‐ dancy, Performance, Power Management, and Configuration. 

## **System Redundancy Improvement: Multi-casting** 

The Multi‐casting capability allows a Posted Write TLP to be routed to more than one destination at the same time, allowing for things like automatically making redundant copies of data or supporting multi‐headed graphics. As shown in Figure 20‐1 on page 888, a TLP sourced from one Endpoint can be routed to multiple destinations based solely on its address. In this example, data is sent to the video port for display while redundant copies of it are auto‐ matically routed to storage. There are other ways this activity could be sup‐ ported, of course, but this is very efficient in terms of Link usage since it doesn’t require a recipient to re‐send the packet to secondary locations. 

_Figure 20‐1: Multicast System Example_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


This mechanism is only supported for posted, address‐routed Requests, such as Memory Writes, that contain data to be delivered and an address that can be decoded to show which Ports should receive it. Non‐posted Requests will not be treated as Multicast even if their addresses fall within the MultiCast address range. Those will be treated as unicast TLPs just as they normally would. 

The setup for Multicast operation involves programming a new register block for each routing element and Function that will be involved, called the Multi‐ cast Capability structure. The contents of this block are shown in Figure 20‐2 on page 889, where it can be seen that they define addresses and also MCGs (Mul‐ tiCast Group numbers) that explain whether a Function should send or receive copies of an incoming TLP or whether a Port should forward them. Let’s 

**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

describe these registers next and discuss how they’re used to create Multicast operations in a system. 

_Figure 20‐2: Multicast Capability Registers_ 

|20<br>31|19|19|16|15||0||||
|---|---|---|---|---|---|---|---|---|---|
|Next Extended<br>Capability Offset||Version<br>(1h)||PCIe Extended Capability ID<br>(0012h for Multicast)||||||
||||31|||||0|Offset|
|||||PCIe Enhanced Capability Header|||||00h|
|||||Multicast Control||Multicast Capability|||04h|
|MCGs this Function||||MC_Base_Address Register|||||08h<br>0Ch|
|is allowed to receive||||||||||
|or forward||||MC_Receive||Register|||10h<br>14h|
|MCGs this Function||||||||||
|must not send|||||||||18h|
|or forward||||MC_Block_All||Register|||1Ch|
|MCGs this Function<br>must not send or||||MC_Block_Untranslated Register|||||20h<br>24h|
|forward if the address||||||||||
|Root Ports and<br>is untranslated||||MC_Overlay_BAR|||||28h<br>2Ch|
|Switch Ports||||||||||


## **Multicast Capability Registers** 

The Capability Header register at the top of the figure includes the Capability ID of 0012h, a 4‐bit Version number, and a pointer to the next capability struc‐ ture in the linked list of registers. 

## **Multicast Capability** 

This register, shown in detail in Figure 20‐3 on page 890, contains several fields. The MC_Max_Group value defines how many Multicast Groups this Function has been designed to support minus one, so that a value of zero means one 

group is supported. The Window Size Requested, which is only valid for End‐ points and reserved in Switches and Root Ports, represents the address size needed for this purpose as a power of two. 

_Figure 20‐3: Multicast Capability Register_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


Lastly, bit 15 indicates whether this Function supports regenerating the ECRC value in a TLP if forwarding it involved making address changes to it. Refer to the section called “Overlay Example” on page 895 for more detail on this. 

## **Multicast Control** 

This register, shown in Figure 20‐4 on page 890, contains the MC_Num_Group that is programmed with the number of Multicast Groups configured by soft‐ ware for use by this Function. The default number is zero, and the spec notes that programming a value here that is greater than the max value defined in the MC_Max_Group register will result in undefined behavior. The MC_Enable bit is used to enable the Multicast mechanism for this component. 

_Figure 20‐4: Multicast Control Register_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


**Cha ter 20: U dates for S ec Revision 2.1 p p p** 

## **Multicast Base Address** 

The base address register, shown in Figure 20‐5 on page 891, contains the 64‐bit starting address of the Multicast Address range for this component. The Multi‐ Cast Index Position register indicates the bit position within the address where the MultiCast Group (MCG) number is to be found. When the address of an incoming TLP falls within the MultiCast address range starting at this Base Address, the logic will offset into the address itself by the number of bit loca‐ tions given in the Index Position and interpret the next bits (up to 6 bits, allow‐ ing up to 64 groups) as the MCG number for that TLP. The MCG number, in turn, will indicate whether the Port should forward a copy of this TLP. 

_Figure 20‐5: Multicast Base Address Register_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


An example of locating the MCG within the address is shown in Figure 20‐6 on page 892. Here the Index Position value is 24, so the MCG is found in address bits 25 to 30. Interestingly, since the base address doesn’t define the lower 12 bits of the address, the MC Index Position must be 12 or greater to be valid. If it’s less than 12 and the MC_Enable bit is set, the component’s behavior will be unde‐ fined. 

## **PCI Express Technology** 

_Figure 20‐6: Position of Multicast Group Number_ 

<img src="figures/page/page0902.png" alt="Figure 19‐8: Device Capabilities Register" width="700">

<br>


## **MC Receive**

</td>
<td style="background-color:#e8e8e8">

这些值由软件编程到表中以在正常操作期间使用。规范建议该表位于 TPH Requester Capability 结构中，如图 20-16 所示（在第 906 页），但它也可以构建到 MSI-X 表中。对于给定的功能，只能使用这些表位置中的一个或另一个。位置在 Requester Capability 寄存器的 ST Table Location 字段 [10:9] 中给出，如图 20-17 所示（在第 907 页）。这 2 位的编码在第 907 页的表 20-2 中显示。

_图 20-16：TPH Requester Capability 结构_

|31|15|0<br>7|
|---|---|
|PCI Express Capabilities Register|Next Cap<br>Pointer|PCI Express<br>Cap ID (17h)|
|TPH Requester Capability Register||
|TPH Requester Control Register||
|TPH ST Table（可选）<br>（大小由 ST 条目数决定）||


**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-17：TPH Capability 和 Control 寄存器_

**==> 图片 [340 x 285] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
TPH Requester Capability Register<br>31 27 26 16 15 11 10 9 8 7 3 2 1 0<br>RsvdP ST Table Size RsvdP RsvdP<br>ST Table Location<br>Extended TPH Requester Supported<br>Device-Specific Mode Supported<br>Interrupt Vector Mode Supported<br>No ST Mode Supported<br>TPH Requester Control Register<br>31 10 9 8 7 3 2 0<br>RsvdP RsvdP<br>TPH Requester Enable<br>ST Mode Select<br>**----- 图片文字结束 -----**


_表 20-2：ST 表位置编码_

|**位 [10:9]**|**ST 表位置**|
|---|---|
|00b|不存在|
|01b|位于 Requester Capability 结构中|
|10b|位于 MSI-X 表中|
|11b|保留|


Requester Capability 寄存器在位 [26:16] 中列出 ST Table 中的条目数。每个表条目宽 2 字节，在 TPH Capability 寄存器集中实现的 ST Table 如图 20-18（在第 908 页）所示，其中突出显示了条目零。Requester Capability 寄存器还描述了请求者支持哪些 ST 模式，以及 3 个 LSB：

- **No ST** — 对 ST 位使用零。在 TPH Requester Control 寄存器的 ST Mode Select 字段中选择，值为 000b 时。

- **Interrupt Vector** — 使用中断向量号作为表的偏移量，这意味着值包含在 MSI-X 表中。（ST Mode Select 值 = 001b。）

- **Device-Specific** — 使用设备特定的方法偏移到 TPH Capability 结构中的 ST Table，因为 ST 值位于其中。这是建议的实现，尽管给定的请求如何与特定 ST 条目相关联超出了规范的范围。（ST Mode Select 值 = 010b。）

- 所有其他 ST Mode Select 编码保留供将来使用。

_图 20-18：TPH Capability ST Table_

||31|24|23|16|15|8|7|0||
|---|---|---|---|---|---|---|---|---|---|
||ST Upper Entry (1)||ST|Lower Entry (1)|ST Upper Entry (0)||ST Lower Entry (0)|||
||ST Upper Entry (3)||ST|Lower Entry (3)|ST Upper Entry (2)||ST Lower Entry (2)|||
|||||||||||
|||ST Upper Entry|ST Lower Entry|||ST Upper Entry|ST Lower Entry||
|||(Table Size)||(Table Size)||(Table Size - 1)|(Table Size - 1)|||
|||||||||||


## **TLP Prefixes**

如果需要，可以通过添加可选的 TLP 前缀来扩展 Steering Tag 位。当 TLP 给出一个或多个前缀时，头通过设置 Format 字段的最高有效位来报告它，如图 20-19（在第 909 页）所示。

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

_图 20-19：TPH 前缀指示_

**==> 图片 [344 x 126] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>Fmt At T T E<br>Byte 0 Type R TC R R Attr AT Length<br>1 0 0 tr H D P<br>Last DW 1st DW<br>Byte 4 Requester ID Tag<br>BE BE<br>Byte 8 Address [63:32]<br>Byte 12 Address [31:2] PH<br>**----- 图片文字结束 -----**


## **IDO（基于 ID 的排序）**

事务排序规则对于正确的流量流很重要，但有时不需要，并且在这些情况下可以改善延迟。特别是来自不同请求者的 TLP 之间不太可能有依赖关系，因此此功能允许软件启用它们以重新排序以提高性能。此操作的详细信息在第 301 页上名为"ID Based Ordering (IDO)"的部分中描述。

## **ARI（替代路由 ID 解释）**

此可选功能的动机是增加端点可用的功能号数。设备号在 PCI 等共享总线架构中很有用，但在点对点架构中通常不需要。因此，规范编写者选择允许设备以不同方式解释 ID 路由命令的目标。这是通过将 Device number 定义为始终为零来实现的，然后允许 Function number 使用 ID 中以前是 Device number 的 5 位。实际上，Device number 消失了，而 Function number 增加到 8 位。使用 ARI 的 TLP 的目标需要被启用以识别它，然后软件才能使用此功能，但路径中的路由元素不必意识到这一点。它们只查看总线号以确定路由。

## **电源管理改进**

有四项新增功能可提高系统有效管理电源的能力，它们在此处列出。所有这些内容均在第 16 章"电源管理"（第 703 页）中介绍。

## **DPA（动态功率分配）**

一组新的扩展配置寄存器定义了 D0 以下最多 32 个子状态。这允许软件轻松地更改设备的电源状态，而不会产生一直转到 D1 设备电源状态的延迟惩罚。有关详细信息，请参阅第 714 页的"动态功率分配 (DPA)"。

## **LTR（延迟容忍报告）**

允许端点报告它们可以容忍的延迟以响应其请求，使系统软件能够就系统响应时间和睡眠状态做出更好的选择。有关详细信息，请参阅第 784 页的"LTR（延迟容忍报告）"。

## **OBFF（优化缓冲区刷新和填充）**

类似地，允许系统报告端点应该或不应该启动 DMA 或中断流量的首选时间段，有助于协调系统睡眠时间并改善电源管理。有关详细信息，请参阅第 776 页的"OBFF（优化缓冲区刷新和填充）"。

## **ASPM 选项**

此更改只是允许设备在选择时支持无 ASPM 链路电源管理。在以前的规范版本中，对 L0s 的支持是强制性的，但现在它变为可选的。

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

## **配置改进**

添加了一些配置寄存器以改进对设备的软件可见性和控制。

## **内部错误报告**

这旨在为没有驱动程序来处理它们的设备（如交换机）提供一种标准化的方式来报告内部问题。它还添加了在错误结果时跟踪多个 TLP 头而不是像以前那样只跟踪一个的功能。本主题在第 667 页的关于错误的"内部错误"部分中介绍。

## **Resizable BAR**

这组新的扩展配置寄存器允许使用大量本地内存的设备报告它们是否可以使用更少的内存量，如果是，则可以接受的大小。知道查找它们的软件可以找到新的寄存器，如图 20-20（在第 912 页）所示，并根据系统内存和其他设备的竞争要求对它们进行编程以给出适合平台的内存大小。

这些寄存器的使用有一些规则：

1. 为避免混淆，仅当 Command 寄存器中的 Memory Enable 位已清除时，才应更改 BAR 大小。

2. 规范强烈建议功能不要通告比其有效使用的更大的 BAR。

3. 为了确保最佳性能，软件应分配将适用于系统的最大 BAR 大小。

## **PCI Express Technology**

## _图 20-20：Resizable BAR 寄存器_

**==> 图片 [363 x 166] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 20 19 16 15 0<br>Next Extended Version PCIe Extended Capability ID<br>Capability Offset (1h) (0015h for Resizable BAR)<br>31 0 Offset<br>PCIe Enhanced Capability Header 000h<br>Resizable BAR Capability Register (0) 004h<br>Register Pair<br>for each Reserved Resizable BAR Control Register (0) 008h<br>supported<br>BAR …<br>Resizable BAR Capability Register (n) n*8 +4<br>Reserved Resizable BAR Control Register (n) n*8 +8<br>**----- 图片文字结束 -----**


## **Capability Register**

此寄存器仅报告哪些 BAR 大小将适用于此功能。位 4 到 23 用于此目的，值如下所示：

- 位 4 — 1MB BAR 大小将适用于此功能

- 位 5 — 2MB

- 位 6 — 4MB

- ...

- 位 23 — 512GB 将适用于此功能

_图 20-21：Resizable BAR Capability 寄存器_

**==> 图片 [242 x 38] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 24 23 4 3 0<br>RsvdP RsvdP<br>**----- 图片文字结束 -----**


## **Control Register**

此寄存器中的 BAR Index 字段报告此大小引用的 BAR（0 到 5 是可能的）。Number of Resizable BARs 字段仅对 Control

**Cha ter 20: U dates for S ec Revision 2.1 p p p**

Register 0 定义，并对其余所有保留。它告诉六个可能的 BAR 中实际上有多少个具有可调整的大小。最后，BAR Size 字段由软件编程以指定 BAR Index 字段指示的 BAR 所需的大小（0 = 1MB，1=2MB，2=4MB，...，19=512GB）。

_图 20-22：Resizable BAR Control 寄存器_

**==> 图片 [281 x 136] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
31 13 12 8 7 5 4 3 2 0<br>RsvdP RsvdP<br>BAR Size (RW)<br>Number of Resizable<br>BARs (RO)<br>BAR Index (RO)<br>**----- 图片文字结束 -----**


一旦 Resizable 值被编程，枚举软件将能够像通常一样工作：将所有 F 写入每个 BAR 并读回它将报告所选的大小。请注意，如果大小值被更改，BAR 的内容将丢失，如果之前已设置，则需要重新编程。图 20-23（在第 914 页）突出显示了 Type 0 头的配置头空间中的 BAR 寄存器。

## _图 20-23：Type0 配置头中的 BAR_

**==> 图片 [160 x 273] 已故意省略 <==**

**----- 图片文字开始 -----**<br>
3 2 1 0 DW<br>Device Vendor 00<br>ID ID<br>Status Command 01<br>Register Register<br>Class Code Revision 02<br>ID<br>HeaderType LatencyTimer CacheLineSize 03<br>04<br>Base Address 0<br>05<br>Base Address 1<br>06<br>Base Address 2<br>07<br>Base Address 3<br>08<br>Base Address 4<br>09<br>Base Address 5<br>10<br>CardBus CIS Pointer<br>Subsystem ID SubsystemVendor ID 11<br>Expansion ROM 12<br>Base Address<br>Reserved CapabilitiesPointer 13<br>14<br>Max_Lat Min_Gnt InterruptPin InterruptLine 15<br>**----- 图片文字结束 -----**


## **简化的排序表**

</td>
</tr></tbody></table>

[⬆️ 返回目录](#-本章目录-table-of-contents)

---

> 🤖 Generated by `tools/merge_chapters.py`


<img src="figures/embedded/page0902_img3_tight.png" alt="Figure from page 902" width="700">

