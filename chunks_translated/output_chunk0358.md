除了捕获和显示 PCI 配置空间的头和能力结构外,Arbor 还可以检查每个字段的设置是否有错误(例如违反规范)和非最佳值(例如 PCIe 链路训练到低于其最大能力)。MindShare Arbor 内置了数十个这样的检查,可以对任何系统扫描(实时或保存的)运行。任何错误或警告都会被标记并显示,以便轻松评估和调试。MindShare Arbor 允许用户创建自己的规则检查以应用于系统扫描。这些规则检查可以针对 PCI 配置空间、内存空间或 IO 空间中的任何结构或结构集。规则检查以 JavaScript 编写。(即将支持 Python。)

## **写入能力**

MindShare Arbor 提供了一个非常简单的界面来直接编辑 PCI 配置空间、内存地址空间或 IO 地址空间中的寄存器。这可以在解码视图中完成,因此您可以看到每一位的含义,或者只需将十六进制值写入目标位置即可。

## **保存系统扫描 (XML)**

执行系统扫描后,MindShare Arbor 允许将该系统扫描的数据(PCI 配置空间、内存空间和 IO 空间)全部保存在单个文件中,以便稍后查看或发送给同事。这些 Arbor 系统扫描文件(.ARBSYS 文件)中的扫描数据是基于 XML 的,可以使用任何文本编辑器或 Web 浏览器查看。甚至使用其他工具执行的扫描也可以轻松转换为 Arbor XML 格式,并使用 MindShare Arbor 进行评估。

## **ARBOR**

**==> picture [9 x 6] intentionally omitted <==**

**----- Start of picture text -----**<br>
BY<br>**----- End of picture text -----**<br>

## **查看、编辑和验证计算机配置设置的终极工具**

**==> picture [246 x 277] intentionally omitted <==**

**----- Start of picture text -----**<br>
从扫描、实时系统<br>| SaaS 解码数据<br>应用标准和<br>自定义规则检查<br>直接编辑配置、<br>内存和 IO 空间<br>**----- End of picture text -----**<br>

## **功能列表**

- 扫描系统中所有 PCI 可见功能的配置空间

- 运行标准和自定义规则检查以查找错误和非最佳设置

- 写入任何配置空间位置、内存地址或 IO 地址

- 以解码格式查看标准和非标准结构

- 导入其他工具(例如 lspci)的原始扫描数据以在 Arbor 的解码格式中查看

- 解码信息包括标准 PCI、PCI-X 和 PCI Express 结构

- 解码信息包括一些基于 x86 的结构和设备特定寄存器

- 为配置空间、内存地址空间和 IO 空间中的结构创建解码文件

- 保存系统扫描以供以后或其他系统查看

**==> picture [104 x 24] intentionally omitted <==**

**----- Start of picture text -----**<br>
一切由开放格式 XML 驱动<br>**----- End of picture text -----**<br>

- 所有解码文件和保存的系统扫描都是基于 XML 的开放格式

## **即将推出**

x86 结构的解码视图(MSR、ACPI、分页、虚拟化等)

**mindshare.com  |  800.633.1440  |  training@mindshare.com**
