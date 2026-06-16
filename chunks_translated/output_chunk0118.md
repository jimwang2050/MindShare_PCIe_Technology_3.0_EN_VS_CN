## **PCI Express 技术**

_图 1‐12：PCI 配置头类型 1（桥）_

**==> picture [362 x 265] intentionally omitted <==**

**----- Start of picture text -----**<br>
类型 1 头<br>主总线 31 23 15 7 0<br>设备 ID 供应商 ID 00h<br>配置 状态 命令 04h<br>寄存器<br>类代码 修订版 08h<br>头     ID<br>BIST 头 延迟 缓存 0Ch<br>类型 定时器 行大小<br>基址 0 (BAR0) 10h<br>基址 1 (BAR1) 14h<br>桥功能 副总线 从属总线 主总线 18h<br>延迟定时器 编号 # 编号 # 编号 #<br>副状态 限值 基址 1Ch<br>副总线（非预取）内存限值（非预取）内存基址 20h<br>内存限值 可预取内存基址 可预取 24h<br>可预取内存基址 28h<br>上限 32 位<br>可预取内存限值 上限 32 位 2Ch<br>IO 限值 IO 基址<br>上限 16 位 上限 16 位 30h<br>保留 能力 34h<br>指针<br>扩展 ROM 基址 38h<br>控制 桥 中断引脚 中断线 3Ch<br>**----- End of picture text -----**<br>

**28**

**第 1 章：背景**

_图 1‐13：PCI 配置头类型 0（非桥）_

**==> picture [350 x 264] intentionally omitted <==**

**----- Start of picture text -----**<br>
类型 0 头<br>31 23 15 7 0<br>设备 ID 供应商 ID 00h<br>配置 状态 命令 04h<br>寄存器<br>类代码 修订版 08h<br>头     ID<br>BIST 头 延迟 缓存 0Ch<br>类型 定时器 行大小<br>基址 0 (BAR0) 10h<br>基址 1 (BAR1) 14h<br>设备基址 2 (BAR2) 18h<br>基址 3 (BAR3) 1Ch<br>基址 4 (BAR4) 20h<br>基址 5 (BAR5) 24h<br>CardBus CIS 指针 28h<br>子系统设备 ID 子系统供应商 ID 2Ch<br>扩展 ROM 基址 30h<br>保留 能力 34h<br>指针<br>保留 38h<br>最大延迟 最小授权 中断引脚 中断线 3Ch<br>**----- End of picture text -----**<br>

配置寄存器空间的详细内容和枚举过程将在后面描述。现在，我们只是想让你熟悉所有这些部分如何组合在一起的全局概览。
