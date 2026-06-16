- **Credits Received counter (optional)** — 跟踪接收到 Flow Control 缓冲区的所有 TLP 的总信用数。当流控正常运行时，CREDITS_RECEIVED 计数应等于或小于 CREDIT_ALLOCATED 计数。如果此测试结果为 false，则表示发生了流控缓冲区溢出并检测到错误。规范建议实现此可选机制，并指出此处的失败将被视为致命错误。

*Figure 6‐9: Types and Format of Flow Control DLLPs*

**==> picture [374 x 125] intentionally omitted <==**

**----- Start of picture text -----**<br>
+0 +1 +2 +3<br>7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0 7 6 5 4 3 2 1 0<br>V[2:0]<br>Byte 0 x x x x 0 VC ID R DataFCHdrFC R DataFCDataFC<br>Byte 4 16 Bit CRC<br>1000  Update Posted<br>1001  Update Non Posted<br>1010  Update Completion<br>**----- End of picture text -----**<br>


**229**

**PCI Express Technology**

## **Flow Control Example**

以下示例描述了 non‐posted header Flow Control 缓冲区，并试图在多种情况下捕获流控实现的细微差别。Flow Control 的讨论以一系列基本阶段描述如下：

**Stage One** — 初始化后立即发送一个事务并进行跟踪，以解释计数器和寄存器的基本操作。

**Stage Two** — 发送方比接收方处理事务的速度更快，缓冲区变满。

**Stage Three** — 当计数器回绕到零时，机制仍然有效，但有几个问题需要考虑。

**Stage Four** — 缓冲区溢出的可选接收方错误检查。

## **Stage 1 — Flow Control Following Initialization**

一旦流控初始化完成，设备就准备好进行正常操作。在我们的示例中，Flow Control 缓冲区为 2KB。我们正在描述 non‐posted header 缓冲区，每个信用为 5 dwords 或 20 字节。这意味着有 102d (66h) 个 Flow Control 单位可用。第 231 页的图 6‐10 说明了所涉及的元素，包括流控初始化后每个计数器和寄存器中的值。

当发送方准备好发送 TLP 时，它必须首先检查 Flow Control 信用。我们的示例很简单，因为 non‐posted header 是唯一正在发送的包，它始终只需要一个 Flow Control 信用，并且我们还假设事务中不包含数据。

使用无符号算术（2 的补码）进行 header 信用检查，并且必须满足以下公式：

**==> picture [193 x 13] intentionally omitted <==**

将图 6‐10 中的值代入：

66_h – (00_h + 01_h) _mod_ 2[8] ≤ 2[8] / 2  66_h – 01_h mod 256 ≤ 80_h

**230**

**Chapter 6: Flow Control**

*Figure 6‐10: Flow Control Elements Following Initialization*

**==> picture [376 x 294] intentionally omitted <==**

**----- Start of picture text -----**<br>
PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 00h CL = 66h<br>FC<br>Incr Check<br>Buffer<br>Link Packet optional incr<br>Control<br>incr CrRcv=00h CrAl=66h<br>(NP Hdr)<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>CrAl = Credits Allocated<br>CC = Credits Consumed<br>CrRcv = Credits Received<br>CL = Credit Limit<br>PTLP = Pending TLP<br>**----- End of picture text -----**<br>


在这种情况下，将当前 CREDITS_CONSUMED 计数 (CC) 与 PTLP 所需信用相加，以确定 CREDITS_REQUIRED (CR)，即 00h + 01h = 01h。从 CREDIT_LIMIT 计数 (CL) 中减去 CREDITS_REQUIRED 计数以确定是否有足够的信用。

以下描述包含对 2 的补码减法的简要回顾。当使用 2 的补码执行减法时，要减去的数字被取反（1 的补码），然后加 1（2 的补码）。然后将此值添加到我们要从中减去的数字。由于加法而产生的任何进位都将被丢弃。

**231**

**PCI Express Technology**

信用检查：

```
CL 01100110b (66h) - CR 00000001b (01h) = n
```

CR 转换为 2 的补码：

`00000001b` (CR) `11111110b` (CR 取反) `11111110b + 1 11111111b` (2 的补码)

将 2 的补码加到 CL 上：

```
01100110 (CL)
11111111(2 的补码 of CR)
01100101 = 65h (carry bit is dropped)
```

结果是否 <= 80h？是的。如果减法结果等于或小于最大值的一半（用 modulo 256 计数器跟踪为 128），那么我们知道接收方缓冲区中有足够的空间，可以发送此包。仅使用一半的计数器值的决定避免了潜在的计数别名问题。请参见第 234 页 "Stage 3 — Counters Roll Over"。

*Figure 6‐11: Flow Control Elements After First TLP Sent*

**==> picture [370 x 225] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>VC0<br>CC = 01h CL = 66h FC<br>Incr Check Buffer<br>Link Packet optional incr<br>Control (NP Hdr)<br>incr CrRcv=01h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


**232**

**Chapter 6: Flow Control**

## **Stage 2 — Flow Control Buffer Fills Up**

假设现在接收方已经有一段时间无法从 Flow Control 缓冲区中移除事务。也许设备核心逻辑暂时忙碌，无法处理事务。最终，Flow Control 缓冲区变得完全填满，如第 234 页的图 6‐12 所示。如果发送方希望发送另一个 TLP 并检查 Flow Control 信用：

Credit Limit (CL)= 66h Credits Required (CR) = 67h

## `CL 01100110` (66)

`CR 10011001` (加 67h 的 2 的补码)

`11111111 = FFh <= 80h` (不正确；不发送包)

此通道被阻塞，直到收到具有 67h 或更大的新 CREDIT_LIMIT 值的 Update Flow Control DLLP。当新值被加载到 CL 寄存器中时，发送方信用检查将通过测试，并且可以发送 TLP。

- `CL 01100111` (67)

- `CR 10011001` 加 67 的 2 的补码

   - `00000000 = 00h <= 80h` (true, send transaction

**233**

**PCI Express Technology**

*Figure 6‐12: Flow Control Elements with Flow Control Buffer Filled*

**==> picture [376 x 278] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Send<br>Buffer CL-CR < 2 [8] /2<br>(VC0) Error<br>CC = 66h CL = 66h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Packets<br>Transaction Link<br>**----- End of picture text -----**<br>


## **Stage 3 — Counters Roll Over**

由于 Credit Limit (CL) 和 Credits Required (CR) 计数仅向上递增，它们最终会回绕到零。当 CL 回绕而 CR 没有回绕时，信用检查 (CL‐CR) 导致 CL 值较小而 CR 值较大。然而，使用无符号算术时看似的问题实际上并不存在。如前所述的示例所示，在执行 2 的补码减法时，结果会被正确处理。第 235 页的图 6‐13 显示了 CL 回绕前后以及 2 的补码结果的 CL 和 CR 计数。

**234**

**Chapter 6: Flow Control**

## *Figure 6‐13: Flow Control Rollover Problem*

**==> picture [368 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Before CL Rollover After CL Rollover<br>FFh<br>NTS = FF8h (4088d)CL = F8h AS = FE8h (4072d)CR = F8h<br>Available<br>Credit Available<br>NTS<br>Credit is the<br>AS = FE8h (4072d)CR = E8h Rollover<br>sum of these<br>two parts<br>NTS = FF8h (4088d)CL = 08h<br>00h<br>Using 2's complement: Using 2's complement:<br>  CL 11111000 (F8h)   CL 00001000 (08h)<br>+ CR 00011000 (E8h 2's complement) + CR 00001000 (F8h 2's complement)<br>  =  00010000 (0Fh)   =  00010000 (0Fh)<br>**----- End of picture text -----**<br>


## **Stage 4 — FC Buffer Overflow Error Check**

虽然可以选择性地执行此操作，但规范建议实现 FC 缓冲区溢出错误检查机制。第 236 页的图 6‐14 显示了与溢出错误检查相关联的元素，包括：

- Credits Received (CR) counter

- Credits Allocated (CA) counter

- Error Check Logic

这允许接收方以与发送方相同的方式跟踪 Flow Control 信用。如果流控工作正常，发送方的 Credits Consumed 计数永远不会超过其 Credit Limit，接收方的 Credits Received 计数永远不会超过其 Credits Allocated 计数。

**235**

**PCI Express Technology**

如果以下公式评估为 true，则检测到溢出情况。请注意，字段大小为 8（headers）或 12（data）：

**==> picture [161 x 12] intentionally omitted <==**

如果它确实评估为 true，则表示发送到 FC 缓冲区的信用超过了可用信用，因此发生了溢出。请注意，规范的 1.0a 版本将等式定义为 ≥ 而不是如上所示的 >。这似乎是一个错误，因为当 CA = CR 时不存在溢出情况。

*Figure 6‐14: Buffer Overflow Error Check*

**==> picture [350 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=67h CrAl=66h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


**236**

**Chapter 6: Flow Control**

## **Flow Control Updates**

接收方必须定期使用在从事务中移除缓冲区时可用的 Flow Control 信用来更新其相邻设备。第 238 页的图 6‐15 说明了一个示例，其中发送方先前因为缓冲区已满而无法发送 header 事务。在图示中，接收方刚刚从 Flow Control 缓冲区中移除了三个 headers。现在有更多空间可用，但相邻设备不知道这一点。随着 headers 从缓冲区中移除，CREDITS_ALLOCATED 计数从 66h 增加到 69h。该新计数使用 Flow Control update 包报告给相邻设备的 CREDIT_LIMIT 寄存器。一旦更新了信用限制，就可以继续传输其他 TLP。

这里一个有趣的注意点是，update 报告了 Credits Allocated 寄存器的实际值。仅报告寄存器的变化也可以工作，例如"+3 credits on NP Headers"，但这代表了一个潜在问题。要了解此风险，请考虑如果包含增量信息的 DLLP 因某种原因丢失会发生什么情况。没有 DLLPs 的重传机制；如果发生错误，包将被简单丢弃。在这种情况下，增量信息将丢失而无法恢复。

另一方面，如果报告了寄存器的实际值并且 DLLP 失败，则下一个成功的 DLLP 将使计数器重新同步。在这种情况下，如果发送方正在等待 FC 信用才能发送下一个 TLP，则可能会浪费一些时间，但不会丢失任何信息。

**237**

**PCI Express Technology**

*Figure 6‐15: Flow Control Update Example*

**==> picture [368 x 248] intentionally omitted <==**

**----- Start of picture text -----**<br>
Device A Device B<br>PTLP<br>Transactions CC+PTLP=CR<br>Pending<br>Buffer Send CL-CR < 2 [8] /2 xxxxxxxxxxxxxxxxxxxxxxxxxx<br>(VC0) Error xxxxxxxxxxxxx<br>CC = 66h CL = 69h<br>Incr Check<br>Link Packet optional incr<br>Control<br>incr CrRcv=66h CrAl=69h<br>optional<br>Link Packet<br>Control<br>transmit receive transmit receive<br>FC Update<br>Transaction Link<br>**----- End of picture text -----**<br>


## **FC_Update DLLP Format and Content**

回想一下，Flow Control update 包与 Flow Control 初始化包一样，包含两个信用字段，一个用于 header，一个用于 data，如第 239 页的图 6‐16 所示。接收方的 HdrFC 和 DataFC 字段中报告的信用值可能自上次发送 update 包以来已更新多次或根本没有更新。

**238**

**Chapter 6: Flow Control**

*Figure 6‐16: Update Flow Control Packet Format and Contents*

## **Flow Control Update Frequency**

规范定义了多种规则和建议的实现，用于管理何时以及多久发送一次 Flow Control Update DLLPs。这些规则的动机是：

- 尽可能早地通知发送设备有关新分配的信用，特别是如果任何事务先前被阻塞。

- 建立 FC Packets 之间的最坏情况延迟。

- 平衡与流控操作相关的要求，例如：— 需要足够频繁地报告信用以防止事务阻塞

- — 减少 FC_Update DLLPs 所需的链路带宽的愿望

- — 选择最佳缓冲区大小

   - 选择最大数据负载大小

- 检测 Flow Control 包之间最大延迟的违反。

仅当链路处于活动状态 (L0 或 L0s) 时才允许 Flow Control 更新。所有其他链路状态表示更积极的电源管理，具有更长的恢复延迟。

## **Immediate Notification of Credits Allocated**

当 Flow Control 缓冲区已满到无法发送最大大小的包时，规范要求在有更多空间可用时立即交付 FC_Update DLLP。存在两种情况：

**239**

**PCI Express Technology**

- **Maximum Packet Size = 1 Credit.** 当由于 non‐infinite NPH、NPD、PH 和 CPLH 缓冲区类型的缓冲区已满条件导致包传输被阻塞时，必须在为一个或多个该缓冲区类型分配信用时调度 UpdateFC 包进行传输。

- **Maximum Packet Size = Max_Payload_Size.** Flow Control 缓冲区空间可能减少到无法为 non‐infinite PD 和 CPLD 信用类型发送最大大小的包的程度。在这种情况下，当分配一个或多个额外信用时，必须调度 Update FCP 进行传输。

## **Maximum Latency Between Update Flow Control DLLPs**

每个 FC 信用类型（non‐infinite）的 Update FCP 的传输频率必须调度为至少每 30 μs (‐0%/+50%) 传输一次。如果 Control Link 寄存器中的 Extended Sync 位被设置，则更新必须调度为不超过每 120 μs (‐0%/+50%) 传输一次。请注意，Update FCPs 的调度传输频率可以比要求更频繁。

## **Calculating Update Frequency Based on Payload Size and Link Width**

规范提供了一个公式，用于根据最大数据负载大小和链路宽度计算需要发送 update 包的频率。该公式（如下所示）以 symbol time 定义 FC Update 传递间隔。作为参考，symbol time 定义为传递一个 symbol 所需的时间：Gen1 为 4ns，Gen2 为 2ns，Gen3 为 1ns。表 6‐3、表 6‐4 和表 6‐5 显示了每种速度的未调整 FC Update 值。

---------------------------------------------------------------------------------------------------------------------------------------（_MaxPayloadSize_ + _TLPOverhead_） × _UpdateFactor_ / **MaxPayloadSize** = Device Control 寄存器的 Max_Payload_Size 字段中的值

- **TLPOverhead** = 常量值（28 个 symbol），表示消耗链路带宽的附加 TLP 组件（TLP Prefix、Sequence Number、Packet Header、LCRC、Framing Symbols）

- **UpdateFactor** = 在两次收到的 UpdateFC 包之间发送的最大大小 TLP 的数量。此数字旨在平衡链路带宽效率和接收缓冲区大小 – 该值随 Max_Payload_Size 和 Link 宽度而变化

**240**

**Chapter 6: Flow Control**

- **LinkWidth** = 链路正在使用的 Lane 数

- **InternalDelay** = 19 个 symbol time 的常量值，表示已接收 TLP 和已发送 DLLP 的内部处理延迟

该公式定义的关系显示，update 包传递的频率随 Linkwidth 的增加而降低，并建议使用一个触发 update 包调度的计时器。请注意，此公式未考虑与接收方或发送方处于 L0s 电源管理状态相关的延迟。

*Table 6‐3: Gen1 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|237<br>UF=1.4|128<br>UF=1.4|73<br>UF=1.4|67<br>UF=2.5|58<br>UF=3.0|48<br>UF=3.0|33<br>UF=3.0|
|256 Bytes|416<br>FC=1.4|217<br>FC=1.4|118<br>UF=1.4|107<br>UF=2.5|90<br>UF=3.0|72<br>UF=3.0|45<br>UF=3.0|
|512 Bytes|559<br>UF=1.0|289<br>UF=1.0|154<br>UF=1.0|86<br>UF=1.0|109<br>UF=2.0|86<br>UF=2.0|52<br>UF=2.0|
|1024 Bytes|1071<br>UF=1.0|545<br>UF=1.0|282<br>UF=1.0|150<br>UF=1.0|194<br>UF=2.0|150<br>UF=2.0|84<br>UF=2.0|
|2048 Bytes|2095<br>UF=1.0|1057<br>UF=1.0|538<br>UF=1.0|278<br>UF=1.0|365<br>UF=2.0|278<br>UF=2.0|148<br>UF=2.0|
|4096 Bytes|4143<br>UF=1.0|2081<br>UF=1.0|1050<br>UF=1.0|534<br>UF=1.0|706<br>UF=2.0|534<br>UF=2.0|276<br>UF=2.0|

*Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|288<br>UF=1.4|179<br>UF=1.4|124<br>UF=1.4|118<br>UF=2.5|109<br>UF=3.0|99<br>UF=3.0|84<br>UF=3.0|
|256 Bytes|467<br>FC=1.4|268<br>FC=1.4|169<br>UF=1.4|158<br>UF=2.5|141<br>UF=3.0|123<br>UF=3.0|96<br>UF=3.0|

**241**

## **PCI Express Technology**

*Table 6‐4: Gen2 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times) (Continued)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|512 Bytes|610<br>UF=1.0|340<br>UF=1.0|205<br>UF=1.0|137<br>UF=1.0|160<br>UF=2.0|137<br>UF=2.0|103<br>UF=2.0|
|1024 Bytes|1122<br>UF=1.0|596<br>UF=1.0|333<br>UF=1.0|201<br>UF=1.0|245<br>UF=2.0|201<br>UF=2.0|135<br>UF=2.0|
|2048 Bytes|2146<br>UF=1.0|1108<br>UF=1.0|589<br>UF=1.0|329<br>UF=1.0|416<br>UF=2.0|329<br>UF=2.0|199<br>UF=2.0|
|4096 Bytes|4194<br>UF=1.0|2132<br>UF=1.0|1101<br>UF=1.0|585<br>UF=1.0|757<br>UF=2.0|585<br>UF=2.0|327<br>UF=2.0|

*Table 6‐5: Gen3 Unadjusted AckNak_LATENCY_TIMER Values (Symbol Times)*

|**Max Payload**|**x1**<br>**Link**|**x2**<br>**Link**|**x4**<br>**Link**|**x8**<br>**Link**|**x12**<br>**Link**|**x16**<br>**Link**|**x32**<br>**Link**|
|---|---|---|---|---|---|---|---|
|128 Bytes|333<br>UF=1.4|224<br>UF=1.4|169<br>UF=1.4|163<br>UF=2.5|154<br>UF=3.0|144<br>UF=3.0|129<br>UF=3.0|
|256 Bytes|512<br>FC=1.4|313<br>FC=1.4|214<br>UF=1.4|203<br>UF=2.5|186<br>UF=3.0|168<br>UF=3.0|141<br>UF=3.0|
|512 Bytes|655<br>UF=1.0|385<br>UF=1.0|250<br>UF=1.0|182<br>UF=1.0|205<br>UF=2.0|182<br>UF=2.0|148<br>UF=2.0|
|1024 Bytes|1167<br>UF=1.0|641<br>UF=1.0|378<br>UF=1.0|246<br>UF=1.0|290<br>UF=2.0|246<br>UF=2.0|180<br>UF=2.0|
|2048 Bytes|2191<br>UF=1.0|1153<br>UF=1.0|643<br>UF=1.0|374<br>UF=1.0|461<br>UF=2.0|374<br>UF=2.0|244<br>UF=2.0|
|4096 Bytes|4239<br>UF=1.0|2177<br>UF=1.0|1146<br>UF=1.0|630<br>UF=1.0|802<br>UF=2.0|630<br>UF=2.0|372<br>UF=2.0|

规范认识到该公式对于许多应用（例如那些流式传输大数据块的应用）可能是不够的。这些应用可能需要比指定的最小值更大的缓冲区大小，以及更复杂的 update 策略，以优化性能并降低

**242**

**Chapter 6: Flow Control**

功耗。由于给定解决方案取决于应用程序的特定要求，因此没有为这些策略提供定义。

## **Error Detection Timer — A Pseudo Requirement**

规范为 Flow Control 包定义了一个可选的超时机制，该机制是强烈建议的，并且可能在规范的未来版本中成为要求。对于给定信用类型，FC 包之间的最大延迟为 120μs，并且此超时的最大限制为 200μs。为每个 FC 信用类型（P、NP、Cpl）实现一个单独的计时器，并在收到相应类型的 FC Update DLLP 时重置每个计时器。请注意，与 infinite FC 信用值关联的计时器不得报告错误。

除了 infinite 情况外，超时意味着链路存在严重问题。如果发生这种情况，物理层被发信号以进入 Recovery 状态并重新训练链路，以期清除错误情况。计时器特性包括：

- 仅当链路处于活动状态 (L0 或 L0s) 时才操作。

- 最长时间限制为 200 μs (‐0%/+50%)

- 收到任何 Init 或 Update FCP 时，计时器被重置，或可选地通过收到任何 DLLP 重置。

- 超时强制物理层进入 Link Training and Status State Machine (LTSSM) Recovery 状态。

**243**

**PCI Express Technology**

**244**

_**7**_

## _**Quality of Service**_

## **The Previous Chapter**

上一章讨论了 Flow Control 协议的目的和详细操作。流控旨在确保发送方永远不会发送接收方无法接受的 Transaction Layer Packets (TLPs)。这可以防止接收缓冲区溢出，并消除了 PCI 风格的低效（如 disconnect、retry 和 wait‐state）的需要。

## **This Chapter**

本章讨论支持 Quality of Service 的机制，并描述了控制穿越 fabric 的不同包的时序和带宽的方法。这些机制包括为每个包分配优先级值的应用特定软件，以及必须构建在每个设备中以管理事务优先级的可选硬件。

## **The Next Chapter**

下一章讨论了 PCI Express 拓扑中事务的排序要求。这些规则是从 PCI 继承的。Producer/Consumer 编程模型激励了其中许多规则，因此此处描述了其机制。原始规则还考虑了必须避免的潜在死锁条件。

## **Motivation**

如今的许多计算机系统不包括管理外围流量的带宽的机制，但有些应用程序需要它。一个例子是跨通用数据总线流式传输视频，需要按时交付数据。在嵌入式制导控制系统中，及时交付视频数据对于系统操作也是至关重要的。预见到这些需求，原始的 PCIe 规范包括可以优先考虑某些流量的 Quality of Service (QoS) 机制。这个更广泛的术语是

**245**

**PCI Express Technology**
