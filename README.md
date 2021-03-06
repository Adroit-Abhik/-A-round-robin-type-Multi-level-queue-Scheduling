## A-round-robin-type-Multi-level-queue-Scheduling

### Problem Statement:
  Write a program for multilevel queue scheduling algorithm. There must be three queues
  generated. There must be specific range of priority associated with every queue. Now prompt the
  user to enter number of processes along with their priority and burst time. Each process must
  occupy the respective queue with specific priority range according to its priority. Apply Round
  Robin algorithm with quantum time 4 on queue with highest priority range. Apply priority
  scheduling algorithm on the queue with medium range of priority and First come first serve
  algorithm on the queue with lowest range of priority. Each and every queue should get a quantum
  time of 10 seconds. CPU will keep on shifting between queues after every 10 seconds. 

### Dependencies:
   * python 3.4 or above
   * prettytable
   * matplotlib
### Run `M1_final.py` to get the output
### Snapshot of the outputs:

   ##### gantt chart of queues execution 
   
   ![Queue gantt chart](https://github.com/Adroit-Abhik/-A-round-robin-type-Multi-level-queue-Scheduling/blob/master/gnt1.png)
   
   ##### gantt chart of queues execution 
   
   ![Process gantt chart](https://github.com/Adroit-Abhik/-A-round-robin-type-Multi-level-queue-Scheduling/blob/master/gn2.png)
