由于我们刚刚看到两种类型的不可纠正错误都需要软件关注，所以说在某些情况下最好让设备不报告其检测到的 Non-Fatal 错误听起来有违直觉，但确实存在这种情况。这些情况主要基于检测代理的角色（Requester、Completer 或中间设备）以及错误类型。问题在于多个设备可能报告由同一事件引起的错误，并且在某些平台上，发送其中一个 Non-Fatal Error Message (ERR_NONFATAL) 可能会妨碍软件正确处理错误。例如，如果端点 (Endpoint) 报告错误，将调用其设备驱动程序来对情况进行处理。但是，如果交换机 (Switch) 首先为同一事务报告错误，则可能调用系统软件进行调查，并且该软件可能不理解驱动程序要完成什么或什么才是最佳响应。

该示例说明某些检测代理并不是确定错误的最终处置的最佳代理，不应发送不可纠正的消息。相反，这样的代理可以通过 ERR_COR 向软件发出建议性通知。这避免了对不可纠正错误来源的混淆，但仍向软件提供有关所发生情况的一些信息。最终，适当的检测代理将在看到错误时发送 ERR_NONFATAL 消息。从 1.1 规范版本开始，在 PCI Express Device Capabilities 寄存器中添加了一个新字段以指示对此功能的支持，如图 15-10 在第 670 页所示。对于符合 1.1 或更高规范的每个代理，必须设置此位。

_图 15-10：Device Capabilities Register_

**==> 图片 [264 x 186] 已省略 <==**

**----- Start of picture text -----**<br>
Device Capabilities Register<br>31 28 27 26 25 18 17 16 15 14 12 11 9 8 6 5 4 3 2 0<br>RsvdP RsvdP<br>Function-Level Reset Capability<br>Captured Slot Power Limit Scale<br>Captured Slot Power Limit Value<br>Role-Based Error Reporting<br>Undefined<br>Endpoint L1 Acceptable Latency<br>Endpoint L0s Acceptable Latency<br>Extended Tag Field Supported<br>Phantom Functions Supported<br>Max Payload Size Supported<br>**----- End of picture text -----**<br>


**670**

**第 15 章：错误检测与处理**

尽管有上述原因，软件可能希望一旦中间设备检测到某些建议性错误就立即停止操作。由于较新的设备将始终执行基于角色的错误报告，因此需要一种覆盖机制。为了处理这种情况，软件可以在 AER (Advanced Error Reporting) 寄存器中将建议性错误的严重性从 Non-Fatal 升级为 Fatal。由于没有"建议性致命"的情况，如果启用，无论设备的角色如何，错误现在都将报告为致命错误 (ERR_FATAL)。

## **建议性非致命情况 (Advisory Non-Fatal Cases)**

规范列出了五种情况，其中建议性消息 (ERR_COR) 优于 ERR_NONFATAL 消息。在每种情况下，检测代理将把错误作为 Advisory Non-Fatal Error 处理。这意味着假设代理具有 AER 寄存器并已启用 ERR_COR，将通过发送 ERR_COR 来处理 Non-Fatal 条件。如果没有 AER 寄存器或未启用 ERR_COR，则不发送 Error Message。这五种情况如下：

1. Completer 发送了 UR 或 CA 状态的完成。在这种情况下，预期是 Requester 在看到违规的完成时将具有处理错误的机制，并且将是发送所需的任何 Error Message 的最佳代理。来自 Completer 的 ERR_NONFATAL 消息只会引起混淆，因此必须将其作为 Advisory Non-Fatal (ERR_COR) 处理。

   - 奇怪的是，没有 PCIe 机制供 Requester 报告它收到了具有此状态的完成。相反，将需要一种特定于设计的方法（如中断）来获得设备驱动程序的关注。当根复合体收到对 Configuration Read Request 的具有 UR 或 CA 状态的完成响应时，会发生这种情况的重要示例。在某些平台上，对此情况的响应是向软件返回全 1，以支持与 PCI 枚举（配置探测）软件的向后兼容性。

2. 中间设备检测到错误。这种情况出现在使用交换机的系统中，因为检测代理可能不是 TLP 的最终目的地。作为一个例子，考虑图 15-11 在第 672 页，显示通过中间交换机传递的被毒化数据包。TLP 被交换机视为 Non-Fatal 错误，但它只能发出 ERR_COR 消息代替（只要它已启用）。为了进一步探讨这个概念，为什么我们不希望交换机报告 ERR_NONFATAL？其中一个原因可以通过查看 AER 寄存器中的错误跟踪看出。图 15-12 在第 672 页显示了跟踪进入根端口 (Root Port) 的 Error Message 的源 ID（发送设备的 BDF）的 AER 寄存器，我们可以看到，对于

**671**

## **PCI Ex ress Technolo p gy**

不可纠正错误只有一个可用空间。如果看到多个不可纠正的错误，则将注意到这一事实，但仅保存第一个源 ID，因为它被认为是后续错误的可能原因。因此，重要的是不可纠正的错误来自最合适的报告设备。值得注意的是，中间设备报告 ERR_COR 仍然是有帮助的，因为它允许软件确定错误最初是在哪里检测到的。

_图 15-11：基于角色的错误报告示例_

**==> 图片 [230 x 219] 已省略 <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Poisoned<br>Packet<br>ERR_COR<br>PCIe<br>PCIe Switch Endpoint<br>Endpoint<br>PCIe Legacy<br>Endpoint Endpoint<br>**----- End of picture text -----**<br>


_图 15-12：Advanced Source ID Register_

**==> 图片 [333 x 77] 已省略 <==**

**----- Start of picture text -----**<br>
Error Source Identification Register<br>of the AER Capability Structure<br>31 0<br>ERR_FATAL/NONFATAL Source ID ERR_COR Source ID<br>(ROS) (ROS)<br>ROS: Read-Only and Sticky<br>**----- End of picture text -----**<br>


**672**

**第 15 章：错误检测与处理**

作为另一个示例，清除了 UR Reporting Enable 位但没有基于角色的错误报告功能的 1.0a 设备在检测到 UR 错误（对于 posted 或 non-posted 请求）时无法报告任何错误消息。相比之下，符合 1.1 或更高版本的 Completer 如果设置了 SERR# Enable 位，则会针对错误的 posted 请求发送 ERR_NONFATAL 或 ERR_FATAL 消息，即使清除了 Unsupported Request Reporting Enable 位也是如此，以避免静默数据损坏。但它不会为收到的 non-posted 请求发送错误消息，以支持通过配置读取进行探测的 PCI 兼容配置方法。建议软件对那些不具备基于角色的错误报告功能的设备保持清空 UR Error Reporting Enable 位，但对具备该功能的设备则设置该位。这样，UR 错误会在错误的 posted 请求上报告，但不会在像配置探测事务这样的错误的 non-posted 请求上报告，并且保持了与旧软件的向后兼容性。

规范还提到，发送到根 (Root) 的被毒化的 TLP 在根充当中间代理时将以相同方式处理，但有一个例外：如果根不支持 Error Forwarding，它将无法通过 TLP 传达被毒化的错误，而必须将其报告为 Non-Fatal 错误。

3. 目标设备收到被毒化的 TLP。通常，端点会在这种情况下报告 Non-Fatal 错误，但此规则有一个例外：如果最终目标设备能够以允许继续操作的方式处理被毒化数据，则它必须将这种情况视为 Advisory Non-Fatal Error。

   - 这种行为的一个例子可能是收到已被毒化的流数据的音频设备。在这种情况下，即使已知数据已损坏，数据也可能会被接受，因为暂停音频流足够长的时间以引起软件注意并采取补救措施将是比允许声音输出中出现故障更糟糕的替代方案。

4. Requester 经历了 Completion Timeout。这与前一种情况类似；如果 Requester 有尽管出现问题仍能继续操作的方法，则它必须将其视为 Advisory Non-Fatal Error。在这种情况下，Requester 的简单解决方法将只是重新发送请求并希望这次有更好的结果。显然，只有在先前的请求没有引起任何副作用时这才有意义，但允许 Requester 根据需要执行此操作（尽管规范规定重试次数必须是有限的）。

5. 收到意外完成。这必须作为 Advisory Non-Fatal Error 处理。原因可能是由错误路由的完成引起的，并且原始 Requester 最终将报告完成超时。为了允许该其他 Requester 尝试重试失败

**673**

**PCI Ex ress Technolo p gy**

请求，看到意外完成的那一个不发送 Non-Fatal 消息是很重要的。

## **基线错误检测与处理 (Baseline Error Detection and Handling)**

本节定义了检测和报告 PCI Express 错误所需的支持。兼容设备必须包括：

- PCI 兼容支持 — 必须遵守 PCI 兼容错误控制和状态字段，以便不感知 PCI Express 的旧软件使用。

- PCI Express 错误报告 — 使用标准 PCIe 结构进行错误控制和状态，可供了解 PCI Express 的较新软件使用。

## **PCI 兼容错误报告机制 (PCI-Compatible Error Reporting Mechanisms)**

## **概述 (General)**

为了向后兼容，PCI Express 错误被映射到原始的 PCI 配置寄存器位，允许 PCI 兼容软件访问错误状态和控制。要从 PCI 兼容的角度了解可用的功能，请考虑配置头中 Command 和 Status 寄存器的错误相关位。一些字段定义已被修改，以反映相关的 PCIe 错误条件和报告机制。由 PCI 兼容寄存器跟踪的 PCI Express 错误包括：

- Transaction Poisoning/Error Forwarding（与 PCI 中的数据奇偶校验错误同义）

- 由 Completer 检测到的 Completer Abort (CA)（与 PCI 中的 Target Abort 同义）

- 由 Completer 检测到的 Unsupported Request (UR)（与 PCI 中的 Master Abort 同义）

如前所述，PCI 的错误报告机制是 PERR#（数据奇偶校验错误）和 SERR#（不可恢复错误）的断言。PCI Express 报告这些事件的机制是完成中的 Completion Status 值和到根的 Error Message。

**674**

**第 15 章：错误检测与处理**

## **传统 Command 和 Status 寄存器 (Legacy Command and Status Registers)**

图 15-13 在第 675 页说明了 Command 寄存器以及错误相关字段的位置。设置这些位是为了在 PCI 兼容软件的控制下启用基线错误报告。表 15-3 定义了每个位的具体作用。

_图 15-13：配置头中的 Command 寄存器_

**==> 图片 [390 x 396] 已省略 <==**

**----- Start of picture text -----**<br>
15 11 10 9 8 7 6 5 4 3 2 1 0<br>Reserved 0 0 0 0 0<br>Interrupt Disable<br>Fast Back-to-back Enable *<br>SERR# Enable<br>Stepping Control *<br>Parity Error Response<br>VGA Palette Snoop Enable *<br>Mem Write & Invalidate Enable *<br>Special Cycles *<br>Bus Master Enable<br>Memory Space Enable<br>IO Space Enable<br>* PCIe 中未使用，这些位必须设置为零<br>表 15-3：Command 寄存器中与错误相关的字段<br>Name Description<br>SERR# Enable 设置此位可启用向根复合体发送 ERR_FATAL 和 ERR_NONFATAL<br>错误消息。这些大致类似于在 PCI 中断言系统错误 (SERR#) 信号。<br>对于 Type 1 标头（桥），此位控制从辅助接口到主要接口的<br>ERR_FATAL 和 ERR_NONFATAL 错误消息的转发。<br>此字段不影响 ERR_COR 消息。<br>**----- End of picture text -----**<br>


**675**

**PCI Ex ress Technolo p gy**

_表 15-3：Command 寄存器中与错误相关的字段（续）_

|**Name**|**Description**|
|---|---|
|Parity Error<br>Response|设置此位可启用在 Status 寄存器的 Master Data<br>Parity Error 位中记录被毒化的 TLP。<br>被毒化的数据包表示坏数据，大致类似于 PCI<br>奇偶校验错误。|



图 15-14 在第 676 页说明了 Configuration Status 寄存器以及错误相关位字段的位置。表 15-4 在第 677 页定义了设置每个位的情况以及启用错误报告时设备采取的操作。

_图 15-14：配置头中的 Status 寄存器_

**==> 图片 [304 x 220] 已省略 <==**

**----- Start of picture text -----**<br>
15 14 13 12 11 10 9 8 7 6 5 4 3 2 0<br>0  0 0 R 0 1 Reserved<br>Interrupt Status<br>Capabilities List**<br>66 MHz Capable*<br>Reserved<br>Fast Back-to-back Capable*<br>Master Data Parity Error<br>DEVSEL Timing*<br>Signalled Target Abort<br>Received Target Abort<br>Received Master Abort<br>Signalled System Error<br>Detected Parity Error<br>* PCIe 中未使用，这些位必须设置为零<br>** 必须设置为 1，因为需要某些能力寄存器<br>**----- End of picture text -----**<br>


**676**

**第 15 章：错误检测与处理**

_表 15-4：Status 寄存器中与错误相关的字段_

|**Error-Related Bit**|**Description**|
|---|---|
|Detected Parity Error|由接收到被毒化 TLP 的端口设置。无论 Parity Error Response<br>位的状态如何，都会更新此状态位。|
|Signalled System Error|由已使用 ERR_FATAL 或 ERR_NONFATAL 报告了 Uncorrectable<br>Error 并且 Command 寄存器中的 SERR# Enable 位已设置的端口设置。|
|Received Master Abort|由收到具有 UR (Unsupported Request) 状态的完成的 Requester 设置。<br>这被认为类似于 PCI master abort，因为目标未"声明事务"。|
|Received Target Abort|由收到具有 CA (Completer Abort) 状态的完成的 Requester 设置。<br>这类似于 PCI target abort，因为目标有编程违规或内部错误状态。|
|Signaled Target Abort|由将请求（posted 或 non-posted）作为 Completer Abort 处理的 Completer 设置。<br>如果是非发布请求，则会发送具有 CA 完成状态的完成。|
|Master Data Parity Error|对于 Type 0 标头（例如 Endpoints），如果设置了 Command 寄存器中的 Parity Error Response 位<br>并且它发起了被毒化的请求或收到了被毒化的完成，则设置此位。<br>对于 Type 1 标头（例如 Switches 和 Root Ports），如果设置了 Command 寄存器中的 Parity Error Response 位<br>并且它发起了向上游移动的被毒化请求或收到了向下游移动的被毒化完成，则设置此位。|



## **基线错误处理 (Baseline Error Handling)**

基线功能需要使用 PCI Express Capability 结构。这些寄存器包括错误检测和处理字段，相对于仅使用 PCI 兼容错误处理所能实现的，它们提供了关于错误性质以及是否报告它的更细粒度。

**677**

**PCI Ex ress Technolo p gy**

图 15-15 在第 678 页说明了 PCI Express Capability 结构。这些寄存器中的一些提供以下支持：

- 启用/禁用错误报告（错误消息生成）

- 提供错误状态

- 提供链路训练状态和发起链路重新训练

_图 15-15：PCI Express Capability 结构_

**==> 图片 [336 x 315] 已省略 <==**

**----- Start of picture text -----**<br>
31 15 7 0<br>PCI Express Capabilities Register Next Cap Pointer PCI ExpressCap ID DW0<br>Device Capabilities Register DW1<br>Device Status Device Control DW2<br>{<br>Link Capabilities DW3<br>Link Status Link Control DW4<br>{<br>Slot Capabilities DW5<br>Slot Status Slot Control DW6<br>{<br>Root Capability Root Control DW7<br>Root Status DW8<br>{<br>{<br>Device Capabilities 2 DW9<br>Device Status 2 Device Control 2 DW10<br>{<br>Link Capabilities 2 DW11<br>Link Status 2 Link Control 2 DW12<br>{<br>Slot Capabilities 2 DW13<br>Slot Status 2 Slot Control 2 DW14<br>{<br>仅 Gen2 及更高版本的设备<br>ks Pstro<br>niL ll<br>h A<br>Solst tiswe<br>h<br>ti civ<br>w e<br>str str D<br>o o r<br>P P x o<br>t tc<br>Roo elpmo Cello<br>C t<br>t n<br>o e<br>o v<br>R E<br>ks Pstro<br>niL llA<br>h<br>Solst tiswe<br>h<br>ti civ<br>w e<br>str D<br>o<br>P<br>**----- End of picture text -----**<br>


## **启用/禁用错误报告 (Enabling/Disabling Error Reporting)**

Device Control 寄存器允许软件启用四种错误事件的三种不同 Error Message 的生成，Device Status 寄存器允许软件查看检测到的错误。四种错误情况是：

**678**

**第 15 章：错误检测与处理**

- Correctable Errors

- Non-Fatal Errors

- Fatal Errors

- Unsupported Request Errors

请注意，此处识别的唯一特定错误是 Unsupported Request。虽然 Unsupported Request 在技术上是 Non-Fatal 错误的子集，并且在报告时甚至通过 ERR_NONFATAL 消息发出信号，但它有自己的启用和状态位。这是因为在系统枚举期间将发生 Unsupported Request（每当尝试从系统中实际不存在的函数读取配置空间时），但它们不得报告为错误。枚举软件可能具有非常有限的错误处理能力，如果需要停止并处理错误，它可能会失败。因此，软件不希望在 UR 情况下生成错误消息，但希望了解可能检测到的任何其他 Non-Fatal 错误。（有关枚举期间 Unsupported Request 的更多详细信息，请参见第 105 页的"发现 Function 的存在或不存在"部分。）

表 15-5 在第 679 页列出了每种错误类型及其关联的错误分类。

_表 15-5：错误的默认分类_

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Correctable|Receiver Error|Physical|
|Correctable|Bad TLP|Link|
|Correctable|Bad DLLP|Link|
|Correctable|Replay Number Rollover|Link|
|Correctable|Replay Timer Timeout|Link|
|Correctable|Advisory Non-Fatal Error|Transaction|
|Correctable|Corrected Internal Error||
|Correctable|Header Log Overflow|Transaction|
|Uncorrectable - Non Fatal|Poisoned TLP Received|Transaction|
|Uncorrectable - Non Fatal|ECRC Check Failed|Transaction|



**679**

**PCI Ex ress Technolo p gy**

_表 15-5：错误的默认分类（续）_

|**Classification & Severity**|**Name of Error**|**Layer Detected**|
|---|---|---|
|Uncorrectable - Non Fatal|Unsupported Request|Transaction|
|Uncorrectable - Non Fatal|Completion Timeout|Transaction|
|Uncorrectable - Non Fatal|Completer Abort|Transaction|
|Uncorrectable - Non Fatal|Unexpected Completion|Transaction|
|Uncorrectable - Non Fatal|ACS Violation|Transaction|
|Uncorrectable - Non Fatal|MC Blocked TLP|Transaction|
|Uncorrectable - Non Fatal|AtomicOps Egress Blocked|Transaction|
|Uncorrectable - Non Fatal|TLP Prefix Blocked|Transaction|
|Uncorrectable - Fatal|Uncorrectable Internal Error<br>(optional)||
|Uncorrectable - Fatal|Surprise Down (optional)|Link|
|Uncorrectable - Fatal|Receiver Overflow (optional)|Transaction|
|Uncorrectable - Fatal|DLL Protocol Error|Link|
|Uncorrectable - Fatal|Receiver Overflow|Transaction|
|Uncorrectable - Fatal|Flow Control Protocol Error|Transaction|
|Uncorrectable - Fatal|Malformed TLP|Transaction|



**Device Control Register.** 在 Device Control 寄存器（如图 15-16 在第 681 页所示）中设置位可启用发送相应的 Error Message 以报告错误。Unsupported Request 错误被指定为 Non-Fatal 错误，并通过 Non-Fatal Error Message 报告，但仅当设置了 _UR Reporting Enable_ 位时。

为了使函数实际发送错误消息，需要在 Device Control 寄存器中设置相应的启用位，或对于 Fatal 和 Non-Fatal 错误，应设置 SERR# Enable。对于 Uncorrectable Errors，如果 Command Register 中的 SERR# Enable 位已设置或 Device Control 寄存器中相应的启用位已设置，则将发送适当的错误消息（ERR_FATAL 或 ERR_NONFATAL）。

**680**

**第 15 章：错误检测与处理**

对于 Correctable Errors，函数仅当 Device Control 寄存器中的 _Correctable Error Reporting Enable_ 位已设置时才会发送 ERR_COR 消息。无法通过 PCI 兼容机制控制启用 ERR_COR 消息，这很合理，因为在 PCI 中，没有可纠正错误的概念。

_图 15-16：与错误处理相关的 Device Control 寄存器字段_

**==> 图片 [357 x 231] 已省略 <==**

**----- Start of picture text -----**<br>
15 14 12 11 10 9 8 7 5 4 3 2 1 0<br>Bridge Config. Retry Enable/<br>Initiate Function-Level Reset<br>Max Read Request Size<br>Enable No Snoop<br>Aux Power PM Enable<br>Phantom Functions Enable<br>Extended Tag Field Enable<br>Max Payload Size<br>Enable Relaxed Ordering<br>Unsupported Request<br>Reporting Enable<br>Fatal Error Reporting Enable<br>Non-Fatal Error<br>Reporting Enable<br>Correctable Error<br>Reporting Enable<br>**----- End of picture text -----**<br>


**Device Status Register.** 每当检测到与其分类关联的错误时，Device Status 寄存器（如图 15-17 在第 682 页所示）中的错误状态位即被设置，无论 Device Control 寄存器中错误报告启用位的设置如何。由于 Unsupported Request 错误被视为 Non-Fatal 错误，因此当这些错误发生时，_Non-Fatal Error Detected_ 状态位和 _Unsupported Request Detected_ 状态位都将被设置。与其他几个状态位一样，这些是"粘性的"（Sticky）（其值不会通过重置事件清除，因此即使需要重置才能使链路正常工作以读取状态，它们也可用于诊断问题）。

**681**

**PCI Ex ress Technolo p gy**

_图 15-17：与错误处理相关的 Device Status 寄存器位字段_

**==> 图片 [337 x 160] 已省略 <==**

**----- Start of picture text -----**<br>
15 6 5 4 3 2 1 0<br>RsvdZ<br>Transactions Pending<br>Aux Power Detected<br>Unsupported Request Detected<br>Fatal Error Detected<br>Non-Fatal Error Detected<br>Correctable Error Detected<br>**----- End of picture text -----**<br>


## **根对错误消息的响应 (Root's Response to Error Message)**
