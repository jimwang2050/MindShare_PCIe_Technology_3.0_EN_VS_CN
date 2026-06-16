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