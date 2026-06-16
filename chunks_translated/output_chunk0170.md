## **PCI Express Technology** 

这些完成报文（Completion）也包含用于将报文路由回请求者（Requester）的路由信息，请求者会在原始请求中提供其返回地址作为此用途。该"返回地址"实际上就是请求者按照 PCI 定义的设备 ID（Device ID），由三部分组成：其在系统中的 PCI 总线号（Bus number）、在该总线上的设备号（Device number）以及该设备内的功能号（Function number）。此总线号、设备号和功能号信息（有时缩写为 BDF）就是完成报文用来返回原始请求者的路由信息。与 PCI-X 一样，请求者可以同时有多个拆分事务（split transaction）正在进行，并且必须能够将收到的完成报文与正确的请求相对应。为便于实现这一点，在原始请求中又新增了一个称为 Tag（标签）的值，每个请求都有唯一的 Tag。完成者（Completer）会复制该事务 Tag 并在完成报文中使用，请求者便可以快速识别该完成报文所服务的是哪一个请求。

最后，完成者还可以通过在完成状态字段中设置相应位来指示错误情况。这使请求者至少能够大致了解可能发生了什么错误。请求者如何处理这些错误大多由软件决定，并不在 PCIe 规范的范围之内。

**锁定读（Locked Reads）。** 锁定内存读（Locked Memory Read）用于支持所谓的原子读-修改-写（Atomic Read-Modify-Write）操作，这是一类不可中断的事务，处理器在诸如测试并设置信号量之类的任务中会用到。在测试与设置进行期间，不能同时访问该信号量，否则可能产生竞态条件（race condition）。为防止此类问题，处理器会使用一个锁指示器（例如并行前端总线（Front-Side Bus）上的一个独立引脚），在该锁定事务完成之前禁止总线上的其他事务。此处仅给出该主题的高层次介绍。关于锁定事务的更多信息，请参阅附录 D 即第 963 页的"附录 D：锁定事务（Locked Transactions）"。

从历史的角度来看，在 PCI 的早期，规范编写者预见到 PCI 可能会取代处理器总线的情况。因此，PCI 规范中纳入了处理器在总线上可能需要执行的操作的支持，例如锁定事务。然而，PCI 实际很少以这种方式使用，最终其处理器总线支持的大部分内容都被废弃了。尽管如此，锁定周期（locked cycles）被保留下来以支持少数特殊场景，并且 PCIe 沿用了此机制以提供遗留兼容。或许是为了加快停止使用该机制，PCIe 规定新设备不得接受锁定请求；只有那些自标识为遗留设备（Legacy Devices）的设备才被允许这样做。在第 67 页图 2-19 所示的示例中，请求者通过发送一个锁定请求（MRdLk）来启动该流程。根据定义，此类请求只能来自 CPU，因此在 PCIe 中只有根端口（Root Port）才会发起这类请求。

**66** 

**第 2 章：PCIe 架构概述** 

锁定请求会基于目标内存地址通过拓扑进行路由，并最终到达遗留端点。当报文沿路经过每个路由设备（称为服务点（service point））时，该报文所在的出端口（Egress Port）会被锁定，意味着在该路径解锁之前不会允许其他报文沿该方向通过。

_图 2-19：非 Posted 锁定读事务协议_ 

**==> picture [330 x 228] intentionally omitted <==**

**----- Start of picture text -----**<br>
CPU<br>Root Complex<br>Memory<br>PCIe<br>Bridge<br>Switch Endpoint<br>to PCI<br>PCI<br>PCIe PCIe Legacy<br>Endpoint Endpoint Endpoint<br>MRdLk<br>CplDLk<br>CplDLk<br>MRdLk<br>**----- End of picture text -----**<br>

当完成者收到报文并解码其内容后，便会收集数据并生成一个或多个带数据的锁定完成报文（Locked Completions with data）。这些完成报文使用请求者 ID（Requester ID）路由回请求者，并且它们经过的每个出端口也都将被锁定。

如果完成者遇到问题，它会返回一个不带数据的锁定完成报文（原始读操作本应返回数据，如果没有数据则说明存在问题），并且状态字段会指示相应的错误信息。请求者会将此理解为锁定未成功，进而取消该事务，并由软件决定下一步该如何处理。

**67** 

**PCI Express Technology** 

**IO 和配置写（IO and Configuration Writes）。** 第 68 页的图 2-20 展示了一个非 Posted IO 写事务（non-posted IO write transaction）。与锁定请求类似，IO 周期在合法情况下也只能以遗留端点为目标。该请求基于 IO 地址通过交换机（Switch）进行路由，直到到达目标端点。完成者收到请求后，接收数据并返回一个不带数据的完成报文，以确认报文已被接收。完成报文中的状态字段会报告是否发生错误；如果发生错误，则由请求者的软件负责处理。

如果完成报文报告无错误，则请求者便知道写数据已成功送达，并且该完成者后续指令序列的下一条指令可以执行。这正概括了非 Posted 写（non-posted write）的动机：与内存写（memory write）不同，仅知道数据**将会**在将来的某个时刻到达目标位置是不够的；只有当我们确认数据**已经**到达之后，下一步操作才能在逻辑上继续进行。与锁定周期一样，非 Posted 写也只能由处理器发起。

_图 2-20：非 Posted 写事务协议_ 

**==> picture [346 x 275] intentionally omitted <==**

**----- Start of picture text -----**<br>
Processor<br>Requester<br>Step 1: Root Initiates IOWr<br>Step 4: Root receives Cpl Root Complex<br>IOWr Cpl System<br>Memory<br>Switch A Switch C<br>IOWr<br>Cpl<br>Switch B Endpoint Endpoint Endpoint<br>IOWr Cpl<br>Completer<br>Legacy<br>Step 2: Endpoint receives IOWr<br>Endpoint<br>Endpoint Step 3: Endpoint writes data, returns Cpl<br>**----- End of picture text -----**<br>

**68** 

**第 2 章：PCIe 架构概述** 
