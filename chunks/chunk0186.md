## **Link Training and Initialization** 

Another responsibility of the Physical Layer is the initialization and training process on the Link. In this fully automatic process, several steps are taken to prepare the Link for normal operation, which involves determining the status of several optional conditions. For example, the Link width can be from one lane to 32 lanes, and multiple speeds might be available. The training process will discover these options and go through a state machine sequence to resolve the best combination. In that process, several things are checked or established to ensure proper and optimal operation, such as: 

- Link width 

- Link data rate 

- Lane reversal ‐ Lanes connected in reverse order 

- Polarity inversion ‐ Lane polarity connected backward 

- Bit lock per Lane ‐ Recovering the transmitter clock 

- Symbol lock per Lane ‐ Finding a recognizable position in the bit‐stream 

- Lane‐to‐Lane de‐skew within a multi‐Lane Link. 