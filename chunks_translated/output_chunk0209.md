## **仅由根复合体发送配置请求**

规范规定,只有根复合体 (Root Complex) 才被允许发起配置请求 (Configuration Request)。它充当系统处理器的联络员,负责将请求注入到互连网络 (Fabric) 中,并将完成报文 (Completion) 回传给处理器。发起配置事务的能力被限制为由处理器通过根复合体执行,以避免任何设备都可以更改其他设备配置时可能引发的混乱局面。

由于只有根复合体能够发起这些请求,因此它们也只能向下游 (downstream) 流动,这意味着不允许对等的 (peer-to-peer) 配置请求。这些请求根据目标设备的 ID 进行路由,即其 BDF(拓扑中的总线号 (Bus number)、该总线上的设备号 (Device number),以及该设备内的功能号 (Function number))。