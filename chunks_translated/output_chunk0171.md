## **Posted 写事务（Posted Writes）** 

**内存写（Memory Writes）。** 内存写始终是 Posted 类型的,永远不会收到完成报文。一旦请求被发送出去,请求者（Requester）不会等待任何反馈就可以继续发起下一个请求,因此也不会花费时间或带宽来返回完成报文。因此,Posted 写比 Non-Posted 请求更快、更高效,能够提升系统性能。如第 69 页的图 2-21 所示,报文通过其目标内存地址在系统中路由,最终到达完成者（Completer）。一旦某条链路（Link）成功发送了该请求,则该事务在该链路上即告完成,该链路便可被其他报文使用。最终,完成者接收数据,该事务才真正彻底完成。当然,这种方式也有一个权衡:由于不会发送任何完成报文,因此也就没有办法将错误报告给请求者。如果完成者遇到错误,它可以记录该错误,并向根复合体（Root Complex）发送一条消息以通知系统软件有关该错误的信息,但请求者本身不会看到该错误。 

_图 2-21:Posted 内存写事务协议_ 

**==> picture [335 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
处理器<br>请求者（Requester）：<br>步骤 1:根复合体（Root Complex）<br>      发起 MWr 请求<br>
根复合体（Root Complex）<br>
DDR<br>SDRAM<br>
MWr<br>
交换机 A 交换机 C<br>
MWr<br>
交换机 B 端点 端点 端点<br>
MWr<br>
完成者（Completer）：<br>
端点 端点<br>
步骤 2:端点接收 MWr<br>
**----- End of picture text -----**<br>

**69** 