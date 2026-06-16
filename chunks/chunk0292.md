4. In response to seeing non‐PAD Lane numbers coming in, the Upstream Port will verify that the incoming Lane numbers match the Lane num‐ bers they are received on. In this example, the Lanes of the Downstream and Upstream Ports are connected correctly. Because all the Lane num‐ bers match, the Upstream Port advertises its Lane numbers in the TS1s it is sending as well. When the Downstream Port sees non‐PAD Lane numbers in response, it compares the incoming numbers to the values it’s sending. If they match, all is well but, if not, then other steps will need to be taken. If some but not all Lane numbers match, then the Link width may be adjusted accordingly. If the Lanes are reversed, then the optional Lane Reversal feature will be needed. Because it’s optional, it’s possible that the Lanes have been reversed but neither device is capable of correcting it. This would be a dramatic board design error because it is possible the Link cannot be configured for operation in this case. 

**543** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐16: Example 1 ‐ Steps 3 and 4_ 

**==> picture [356 x 232] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 3<br>Lane # 0 1 2 3<br>TS1s<br>Link # N N N N<br>N N N N Link #<br>TS1s<br>0 1 2 3 Lane #<br>0 1 2 3 Step 4<br>(Upstream Port)<br>LTSSM<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Confirming Link and Lane Numbers.** 

5. Since the transmitted and received Link and Lane numbers matched on all the Lanes, the Downstream Port indicates it is ready to conclude this negotiation and proceed to the next state, L0, by sending TS2 Ordered Sets with the same Link and Lane numbers. 

6. Upon receiving TS2s with the same Link and Lane numbers, the Upstream Port also indicates its readiness to leave the Configuration state and proceed to L0 by sending TS2s back. This is shown in Figure 14‐17 on page 545. 

7. Once a Port receives at least 8 TS2s and transmits at least 16, it sends some logical idle data and then transitions to L0. 

**544** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐17: Example 1 ‐ Steps 5 and 6_ 

**==> picture [345 x 215] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 5<br>Lane # 0 1 2 3<br>TS2s<br>Link # N N N N<br>N N N N Link #<br>TS2s<br>0 1 2 3 Lane #<br>0 1 2 3 Step 6<br>LTSSM<br>(Upstream Port)<br>**----- End of picture text -----**<br>


Options: One Link x4, x2 or x1 

## **Link Configuration Example 2** 

Another example that should be covered is of a Device with 4 Downstream Lanes that is capable of being configured as a single x4 Link or a combination of two x2 Links or four x1 Links. So even a configuration of one x2 Link and two x1 Links would be just fine. An example of this type of Device can be seen in Fig‐ ure 14‐18 on page 546. 

If all four Lanes have detected a receiver and made it to the Configuration state, there are a number of connection possibilities: 

- One x4 Link 

- Two x2 Links 

- One x2 Link and two x1 Links 

- Four x1 Links 

One example method defined in the spec to determine which of the configura‐ tions are implemented is described below. 

**545** 

**PCI Ex ress Technolo p gy** 

## **Link Number Negotiation.** 

1. In this example method, the Downstream Port begins by advertising a unique Link number on each Lane. Lane 0 advertises a Link number of N, Lane 1 advertises a Link number of N+1, etc. as shown in Figure 14‐ 18 on page 546. These Link numbers are just examples, and they do not have to be sequential. Also, it is important to remember that the Down‐ stream Port does not know what it is connected to and it is this process where the Port is trying to determine the connections for each Lane. 

_Figure 14‐18: Example 2 ‐ Step 1_ 

**==> picture [298 x 239] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>Two Links x2 or x1<br>Four Links x1<br>LTSSM<br>(Downstream Port)<br>Step 1 0 1 2 3<br>Lane # PAD PAD PAD PAD<br>TS1s<br>Link # N N+1 N+2 N+3<br>PAD PAD PAD PAD Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 1 0<br>(Upstream (Upstream<br>Port) Port)<br>LTSSM LTSSM<br>Options: Options:<br>One Link x2 or x1 One Link x2 or x1<br>**----- End of picture text -----**<br>


2. Upon receiving the returned TS1s, the Downstream Port recognizes two things: all four Lanes are working and they are connected to two differ‐ ent Upstream Ports. This means there will actually be _two_ Downstream Ports. Each Downstream Port will have its own Lane 0 and Lane 1 as shown in Figure 14‐20 on page 548. 

**546** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐19: Example 2 ‐ Step 2_ 

**==> picture [286 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>Two Links x2 or x1<br>Four Links x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Lane # 0 PAD PAD PAD<br>TS1s<br>Link # N N+1 N+2 N+3<br>N N N+2 N+2 Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 1 0 Step 2<br>(Upstream (Upstream<br>Port) Port)<br>LTSSM LTSSM<br>Options: Options:<br>One Link x2 or x1 One Link x2 or x1<br>**----- End of picture text -----**<br>


## **Lane Number Negotiation.** 

3. The process continues now for each Link independently but they’ll take the same steps as before to determine the Lane numbers: the Down‐ stream Ports will advertise their Lane numbers in the TS1s. It is also important to note that the Downstream Ports begin advertising the sin‐ gle returned Link number for all Lanes of the Link. The Link on the left is advertising a Link number of N for both Lanes and the Link on the right is advertising N+2. 

4. In this example, the Lane numbers of the Link on the left match between the Downstream and Upstream Port. However, for the Link on the right, the Lane numbers of the Downstream Port are reversed from the connected Upstream Port. The Upstream Port realizes this and if it supports Lane Reversal, it will implement that internally and reply back with the same Lane numbers that were advertised by the Down‐ stream Port, as shown in Figure 14‐20. If the Upstream Port did not sup‐ port Lane Reversal, it would have advertised its own Lane numbers in 

**547** 

## **PCI Ex ress Technolo p gy** 

   - the returned TS1s and then the Downstream Port would have realized the issue and had a chance to implement Lane Reversal. 

5. Lane Reversal can optionally be handled by either Port. If the Upstream Port detects this case and supports Lane Reversal, it simply makes the Lane assignment change internally and returns TS1s with the proper Lane numbers. As a result, the Downstream Port is unaware that there was ever an issue. If the Upstream Port is unable to handle Lane Rever‐ sal though, then the Downstream Port will see the incoming Lane num‐ bers in reverse order. If it supports Lane Reversal, it will then correct the numbering and begin sending TS2s with the new Lane numbers. 

_Figure 14‐20: Example 2 ‐ Steps 3, 4 and 5_ 

**==> picture [370 x 245] intentionally omitted <==**

**----- Start of picture text -----**<br>
Step 3<br>LTSSM LTSSM<br>(Downstream (Downstream<br>Port) Port)<br>0 1 0 1<br>Step 4<br>Lane # 0 1 0 1<br>TS1s<br>Link # N N N+2 N+2<br>N N N+2 N+2 Link #<br>TS1s<br>0 1 0 1 Lane #<br>0 1 1 0 Step 5<br>(Upstream (Upstream<br>Lane Reversal<br>Port) Port)<br>LTSSM LTSSM<br>**----- End of picture text -----**<br>


## **Confirming Link and Lane Numbers.** 

6. The Downstream Ports receive the TS1s with the Link and Lane num‐ bers that match what was advertised so each Port, independently, starts sending TS2s as a notification that it is ready to proceed to the L0 state with the negotiated settings. 

**548** 

**Chapter 14: Link Initialization & Training** 

7. The Upstream Ports receive the TS2s with no Link and Lane number changes and start transmitting TS2s in return with the same values. 

8. Once each Port receives at least 8 TS2s and transmits at least 16 TS2s, it sends some logical idle data and then transitions to L0. The Upstream Port of the Link on the right is implementing Lane Reversal internally. 

## **Link Configuration Example 3: Failed Lane** 

Finally, let’s consider what happens if one of the Lanes isn’t working properly. Consider an example in which Lane 2 of the Upstream Port is not functioning well as shown in Figure 14‐21 on page 550. It’s important to note that the Lane isn’t physically broken because if it were it wouldn’t have detected a Receiver and wouldn’t be considered for inclusion in the Link. However, even though the Lane is attached, either the Transmitter or Receiver (or both) of Lane 2 on the Upstream Port is not getting the job done. 

In cases like this, it is likely that the link training process will take considerably longer because most of the state transitions wait to proceed to the next state until ALL Lanes are ready for the next state, OR if a subset of Lanes are ready and a timeout condition has occurred. 

The steps below indicate a way this situation could be handled when transition‐ ing through the substates of the Configuration state machine. 

## **Link Number Negotiation.** 

9. Even though the Lane 2 Receiver on the Upstream Port is having issues, the Downstream Port is going to take the same process upon entering the Configuration state. The Downstream Port sends TS1s on all Lanes with the Link number N and with the Lane number set to PAD. 

10. Lanes 0, 1 and 3 all received the TS1s with the non‐PAD Link number, so those Lanes send TS1s back to the Downstream Port. However, Lane 2 of the Upstream Port did not successfully receive the TS1s with the non‐PAD Link number, so its Transmitter continues sending TS1s with PAD in the Link and Lane number fields as shown in Figure 14‐21 on page 550. 

**549** 

## **PCI Ex ress Technolo p gy** 

_Figure 14‐21: Example 3 ‐ Steps 1 and 2_ 

**==> picture [356 x 241] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 1<br>Lane # PAD PAD PAD PAD<br>TS1s<br>Link # N N N N<br>N N PAD N Link #<br>TS1s<br>PAD PAD PAD PAD Lane #<br>0 1 2 3 Step 2<br>LTSSM<br>(Upstream Port)<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Lane Number Negotiation.** 

11. Once the Downstream Port has received the TS1s with the same Link number on Lanes 0, 1 and 3, it waits until the required timeout period hoping that Lane 2 will start working. When that doesn’t happen, the Downstream Port realizes that it will only be able to train as a x2 Link. After accepting this fact, the Downstream Port will advertise its Lane numbers for Lanes 0 and 1, but Lanes 2 and 3 go back to send PADs in the Link and Lane number fields. 

12. When the Upstream Port receives the TS1s on Lanes 0 and 1 with the advertised Lane numbers and it sees that Lane 3 has gone back to receiving PAD TS1s, it advertises its Lane number for Lanes 0 and 1 but all the other Lanes start (or continue) sending TS1s with PAD set in both the Lane and Link number fields as shown in Figure 14‐22 on page 551. 

**550** 

**Chapter 14: Link Initialization & Training** 

_Figure 14‐22: Example 3 ‐ Steps 3 and 4_ 

**==> picture [356 x 240] intentionally omitted <==**

**----- Start of picture text -----**<br>
Options: One Link x4, x2 or x1<br>LTSSM<br>(Downstream Port)<br>0 1 2 3<br>Step 3<br>Lane # 0 1 PAD PAD<br>TS1s<br>Link # N N PAD PAD<br>N N PAD PAD Link #<br>TS1s<br>0 1 PAD PAD Lane #<br>0 1 2 3 Step 4<br>LTSSM<br>(Upstream Port)<br>Options: One Link x4, x2 or x1<br>**----- End of picture text -----**<br>


## **Confirming Link and Lane Numbers.** 
