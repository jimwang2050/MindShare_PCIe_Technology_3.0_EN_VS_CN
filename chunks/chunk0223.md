## **Type 0 Configuration Request** 

If the target bus number matches the Secondary Bus Number, a Type 0 configu‐ ration read or write is forwarded to the secondary bus and: 

1. Devices on that Bus check the Device Number to see which of them is the target device. Note that Endpoints on an external Link will always be Device 0. 

2. The selected Device checks the Function Number to see which Function is selected within the device. 

3. The selected Function uses the Register Number field to select the target dword in its configuration space, and uses the First Dword Byte Enable field to select which bytes to read or write within the selected dword. 

Figure 3‐7 illustrates the Type 0 configuration read and write Request header formats. In both cases, the Type field = 00100, while the Format field indicates whether it’s a read or a write. 

**99** 