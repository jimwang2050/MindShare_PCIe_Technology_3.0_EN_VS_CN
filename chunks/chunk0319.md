|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers or**<br>**State that**<br>**must be valid**|**Power**|**Actions permitted to**<br>**Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D1|Device<br>class‐specific<br>registers<br>and PME<br>context.*|D0<br>unini‐<br>tial‐<br>ized|Config Requests and<br>Messages. Link transi‐<br>tions back to L0 to ser‐<br>vice the request.|PME Messages.**<br>Though not typi‐<br>cally permitted,<br>they would require<br>the Link to transi‐<br>tion back to L0.|
|L2‐L3||NA *||||



* This combination of Bus/Function PM states not allowed. 

- ** If PME supported in this state. 

## **D2 State—Deep Sleep** 

**Optional** . Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of 

**717** 

**PCI Ex ress Technolo p gy** 

the PCI Express Capability block; when the bit is cleared to zero, it’s safe to pro‐ ceed. This power state provides deeper power conservation than D1 but less than the D3hot state. As in D1, the Function won’t initiate Requests (except a PME Message) or act as the target of Requests other than configuration. Soft‐ ware must still be able to access the Function’s configuration registers in this state. 

Other characteristics of the D2 state include: 

- Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of the PCIe Capability block. It could happen that the Completions will never be returned and, in that case, software should wait long enough to ensure they never will be returned. 

- Link state must transition to L1 when the Device transitions to the D2 state. 

- • Configuration and Message Requests are accepted in this state, but all other Requests must be handled as Unsupported Requests and all completions may optionally be handled as Unexpected Completions. 

- If an error is caused by an incoming Request and reporting it is enabled, an Error Message may be sent while in this state. If a different type of error occurs (such as a Completion timeout), the message won’t be sent until the Device is returned to the D0 state. 

- Function may send a PME message, if supported and enabled, to notify software that it needs power restored to handle an event. 

- The Function may or may not lose its context in this state. If it does and the device supports PME messages, it must at least maintain its PME context for this purpose. 

- The Function must return to the D0 Active state to be fully operational. 

Table 16‐7 on page 719 illustrates the PM policies while in the D2 state. 

**718** 

**Chapter 16: Power Management** 

_Table 16‐7: D2 Power Management Policies_ 

|**Link**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must be**<br>**valid**|**Power**|**Actions permitted**<br>**to Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D2|Device<br>class‐specific<br>registers<br>and PME con‐<br>text. *|next higher<br>supported PM<br>state orD0<br>uninitialized.|Config Requests<br>and transactions<br>permitted by<br>device class (typi‐<br>cally none).<br>This requires the<br>Link to transition<br>back to L0|PME Messages.*<br>Though not typi‐<br>cally permitted,<br>they would require<br>the Link to transi‐<br>tion back to L0.|
|L2/L3||N/A**||||



- If PME supported in this state. 

- ** This combination of Bus/Function PM states not allowed. 

## **D3—Full Off** 

**Mandatory** . All Functions must support the D3 state. This is the deepest state and power conservation is maximized. When software writes this power state to the Device, it goes to the **D3hot** state, meaning power is still applied. Remov‐ ing power (Vcc) from the Device puts it into the **D3cold** state and the Link into L2, if a secondary power source (Vaux) is available, or L3 if it’s not. 

**D3Hot State. (Mandatory** .) Software puts a Function into D3hot by writing the appropriate value into the PowerState field of its Power Mgt Control and Status Register (PMCSR). In this state, the Function can only initiate PME or PME_TO_ACK Messages, and can only respond to configuration Requests or the PME_Turn_Off Message. Software must be able to access the Function’s configuration registers while the device is in the D3hot state, if only to be able to change the state back to D0. Other characteristics of D3hot include: 

- Before going into this state, software must ensure that all outstanding non‐posted Requests have received their associated Completions. This can be achieved by polling the Transactions Pending bit in the Device Status register of the PCIe Capability block. It could happen that the Completions will never be returned and, in that case, software should wait long enough to ensure they never will be returned. 

- The Link is forced to the L1 state when the Function changes to D3hot. 

**719** 

## **PCI Ex ress Technolo p gy** 

- The Function is allowed to send a PME message to notify PM software of its need to be returned to the fully active state (assuming it supports genera‐ tion of PM events in the D3hot state and has been enabled to do so). 

- Function context may be lost when going to this state and if the power is turned off the spec assumes all context will be lost. On the other hand, if the power never goes off before software initiates a return to D0 the context could be maintained. In earlier spec versions that wasn’t possible; changing from D3hot to D0 involved a soft reset and all the registers were re‐initial‐ ized. However, the 1.2 revision of that spec added a new capability bit called “No Soft Reset” to indicate that the Function would not do a soft reset in that case. To be able to generate PME messages in the D3hot state, a Device must maintain its PME context (see “PME Context” on page 710). 

The Function exits from the D3hot state under two circumstances: 

- If Vcc is removed from the device, it transitions from D3hot to D3cold. 

- Software can write to the PowerState field of the Function’s PMCSR register to change its PM state to D0. When programmed to exit D3hot and return to D0, the Function returns to the D0 Uninitialized PM state. A reset may or may not be required. Table 16‐8 on page 721 lists the PM policies while in the D3hot state. 

**720** 

**Chapter 16: Power Management** 

_Table 16‐8: D3hot Power Management Policies_ 

|**Bus**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must**<br>**be valid**|**Power**|**Actions permitted**<br>**to Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L1|D3hot|PME con‐<br>text. **|next higher<br>supported PM<br>state orD0<br>uninitialized.|PCI Express config<br>transactions<br>& PME_Turn_Off<br>broadcast<br>message***<br>(These can only<br>occur after the Link<br>transitions back to<br>its L0 state.|PME message**<br>PME_TO_ACK<br>message***<br>PM_Enter_L23<br>DLLP***<br>(These can occur<br>only after the Link<br>returns to L0)|
|L2/L3<br>Ready||L2/L3 Ready entered following the PME_Turn_Off handshake sequence, which<br>prepares a device for power removal***||||
|L2/L3||NA *||||



- This combination of Bus/Function PM states not allowed. 

** If PME supported in this state. 

*** See “L2/L3 Ready Handshake Sequence” on page 764 for details regarding the sequence. 

**D3Cold State. Mandatory** . Every PCI Express Function enters the D3Cold PM state upon removal of power (Vcc) from the Function. When power is restored, the device must be reset or generate an internal reset, taking it from D3Cold to D0 Uninitialized. A Function capable of generating a PME must maintain PME context while in this state and when transitioning to the D0 state. Since power was removed to arrive at this state, the Function must have an auxiliary power source available if it is to maintain the PME context. Then, when the device goes to D0 Uninitialized, it can generate a PME message to inform the system of a wakeup event, if it’s capable and enabled to do so. For more on auxiliary power, refer to “Auxiliary Power” on page 775. 

Table 16‐9 on page 722 illustrates the PM policies while in the D3Cold state. 

**721** 

## **PCI Ex ress Technolo p gy** 

_Table 16‐9: D3cold Power Management Policies_ 

|**Bus**<br>**PM**<br>**State**|**Function**<br>**PM**<br>**State**|**Registers**<br>**and/or State**<br>**that must be**<br>**valid**|**Power**|**Actions**<br>**permitted to**<br>**Function**|**Actions permitted**<br>**by Function**|
|---|---|---|---|---|---|
|L2|D3cold|PME<br>context*|AUX<br>Power|Bus reset only|Signal Beacon<br>or WAKE#**|
|L3||None|||None|



- If PME supported in this state. 

** The method used to signal a wake to restore clock and power depends on the form factor. 

## **Function PM State Transitions** 

Figure 16‐6 illustrates the PM state transitions for a PCIe Function. Table 16‐10 on page 723 provides a description of each transition. Table 16‐11 on page 724 illustrates the transitions from one state to another from both a hardware and a software perspective. 

_Figure 16‐6: PCIe Function D‐State Transitions_ 

**==> picture [192 x 195] intentionally omitted <==**

**----- Start of picture text -----**<br>
Power On<br>Reset D0<br>Un-initialized<br>D0<br>Active<br>D3<br>D1 D2<br>Hot<br>D3<br>Vcc Cold<br>Removed<br>**----- End of picture text -----**<br>


**722** 

**Chapter 16: Power Management** 

_Table 16‐10: Description of Function State Transitions_ 

|**From State**|**To State**|**Description**|
|---|---|---|
|D0<br>Uninitialized|D0 Active|Function has been completely configured and<br>enabled by its driver.|
|D0 Active|D1|Software writes the PMCSR PowerState to D1.|
||D2|Software writes the PMCSR PowerState to D2.|
||D3hot|Software writes the PMCSR PowerState to D3hot.|
|D1|D0 Active|Software writes the PMCSR PowerState to D0.|
||D2|Software writes the PMCSR PowerState to D2.|
||D3hot|Software writes the PMCSR PowerState to D3hot.|
|D2|D0 Active|Software writes the PMCSR PowerState to D0.|
||D3hot|Software writes the PMCSR PowerState to D3hot.|
|D3hot|D3cold|Power is removed from the Function.|
||D0<br>Uninitialized|Software writes the PMCSR PowerState to D0.|
|D3cold|D0<br>Uninitialized|Power is restored to the Function.|



**723** 

**PCI Ex ress Technolo p gy** 

_Table 16‐11: Function State Transition Delays_ 

|**Initial State**|**Next**<br>**State**|**Minimum software‐guaranteed delays**|
|---|---|---|
|D0|D1|0|
|D0 or D1|D2|200s from new state setting to first access (including<br>config accesses).|
|D0, D1, or D2|D3hot|10ms from new state setting to first access.|
|D1|D0|0|
|D2|D0|200s from new state setting to first access.|
|D3hot|D0|10ms from new state setting to first access.|
|D3cold|D0||



## **Detailed Description of PCI-PM Registers** 

The _PCI Bus PM Interface spec_ defines the PM registers (see Figure 16‐7) that are implemented in PCIe Functions. Configuration software can determine the PM capabilities and control its properties. 

_Figure 16‐7: PCI Function’s PM Registers_ 
