import prettytable
import matplotlib.pyplot as plt


class Process:
    def __init__(self, priority, arrival_time, pid, burst_time):
        self.priority = priority
        self.arrival_time = arrival_time
        self.pid = pid
        self.burst_time = burst_time
        self.res_at = arrival_time
        self.waiting_time = 0
        self.remaining_time = self.burst_time
        self.turnaround_time = 0
        self.starting_times = []
        self.end_times = []

    def print_starting_times(self):
        print(self.starting_times)

    def print_ending_times(self):
        print(self.end_times)

    def calc_turnaround_time(self):
        self.turnaround_time = self.end_times[-1] - self.arrival_time
        return self.turnaround_time

    def calc_waiting_time(self):
        self.waiting_time = self.turnaround_time - self.burst_time
        return self.burst_time


class Queue:
    def __init__(self):
        self.processes = []
        self.priority_range = []
        self.starting_times = []
        self.ending_times = []
        self.total_burst_time = 0
        self.limiting_time = 0

    def intialize(self, process, prior):
        self.processes.append(process)
        self.priority_range.append(prior)
        self.processes.sort(key=lambda x: x.arrival_time)
        self.total_burst_time = sum([p.burst_time for p in self.processes])
        self.limiting_time = self.processes[-1].arrival_time

    def print_queue(self):
        table = prettytable.PrettyTable(
            ['PID', 'Priority', 'Burst Time', 'Arrival Time'])
        processes = self.processes
        for i in range(len(processes)):
            table.add_row([processes[i].pid, processes[i].priority, processes[i].burst_time,
                           processes[i].arrival_time])
        print(table)

    def print_table(self):
        table = prettytable.PrettyTable(
            ['PID', 'Priority', 'Burst Time', 'Arrival Time', 'Turnaround Time', 'Waiting Time'])
        processes = self.processes
        tat = 0
        twt = 0
        for i in range(len(processes)):
            table.add_row([processes[i].pid, processes[i].priority, processes[i].burst_time,
                           processes[i].arrival_time, processes[i].calc_turnaround_time(),
                           processes[i].calc_waiting_time()])
            tat += processes[i].turnaround_time
            twt += processes[i].waiting_time

        print(table)
        print("Average Turnaround Time of the processes is: ", tat / len(processes))
        print("Average Waiting Time of the processes is: ", twt / len(processes))


q1 = Queue()
q2 = Queue()
q3 = Queue()
total_queue = Queue()
shifting_time = 10
current_time = 0
counter = 0
quantum = 10


def get_input(n):
    for i in range(n):
        print("Enter details for Process No." + str(i+1))
        at = int(input("arrival time: "))
        pid = input("PID: ")
        priority = int(input("Priority (1-9): "))
        bt = int(input('Burst Time: '))
        p = Process(priority, at, pid, bt)
        if p.priority in range(0, 4):
            q1.intialize(p, p.priority)
            total_queue.intialize(p, p.priority)
        elif p.priority in range(4, 7):
            q2.intialize(p, p.priority)
            total_queue.intialize(p, p.priority)
        else:
            q3.intialize(p, p.priority)
            total_queue.intialize(p, p.priority)


def roundrobin(processes, t):
    sequence = []
    time = t[0]
    final_time = t[1]
    qt = 4
    while True:
        flag = True
        for i in range(len(processes)):
            if processes[i].res_at <= time:
                if processes[i].res_at <= qt:
                    if processes[i].remaining_time > 0:
                        flag = False
                        processes[i].starting_times.append(time)
                        if processes[i].remaining_time > qt:
                            if time + qt > final_time:
                                processes[i].remaining_time -= (final_time - time)
                                processes[i].res_at = final_time
                                time = final_time
                                processes[i].end_times.append(time)
                                flag = True
                                break
                            else:
                                time += qt
                                processes[i].end_times.append(time)
                                processes[i].remaining_time -= qt
                                processes[i].res_at += qt
                                sequence.append(processes[i].pid)
                        else:
                            if time + processes[i].remaining_time > final_time:
                                processes[i].remaining_time -= (final_time - time)
                                processes[i].res_at = final_time
                                time = final_time
                                processes[i].end_times.append(time)
                                flag = True
                                break
                            else:
                                time += processes[i].remaining_time
                                processes[i].end_times.append(time)
                                processes[i].waiting_time = time - processes[i].burst_time - processes[i].arrival_time
                                processes[i].remaining_time = 0
                                sequence.append(processes[i].pid)

                elif processes[i].res_at > qt:
                    for j in range(len(processes)):
                        if processes[j].res_at < processes[i].res_at:
                            if processes[j].remaining_time > 0:
                                flag = False
                                processes[j].starting_times.append(time)
                                if processes[j].remaining_time > qt:
                                    if time + qt > final_time:
                                        processes[j].remaining_time -= (final_time - time)
                                        processes[j].res_at = final_time
                                        time = final_time
                                        processes[j].end_times.append(time)
                                        flag = True
                                        break
                                    else:
                                        time += qt
                                        processes[j].end_times.append(time)
                                        processes[j].remaining_time -= qt
                                        processes[j].res_at += qt
                                        sequence.append(processes[j].pid)
                                else:
                                    if time + processes[j].remaining_time > final_time:
                                        processes[j].remaining_time -= (final_time - time)
                                        processes[j].res_at = final_time
                                        time = final_time
                                        processes[j].end_times.append(time)
                                        flag = True
                                        break
                                    else:
                                        time += processes[j].remaining_time
                                        processes[j].end_times.append(time)
                                        processes[j].waiting_time = time - processes[j].burst_time - processes[
                                            j].arrival_time
                                        processes[j].remaining_time = 0
                                        sequence.append(processes[i].pid)

                    if processes[i].remaining_time > 0:
                        flag = False
                        processes[i].starting_times.append(time)
                        if processes[i].remaining_time > qt:
                            if time + qt > final_time:
                                processes[i].remaining_time -= (final_time - time)
                                processes[i].res_at = final_time
                                time = final_time
                                processes[i].end_times.append(time)
                                flag = True
                                break
                            else:
                                time += qt
                                processes[i].end_times.append(time)
                                processes[i].remaining_time -= qt
                                processes[i].res_at += qt
                                sequence.append(processes[i].pid)
                        else:
                            if time + processes[i].remaining_time > final_time:
                                processes[i].remaining_time -= (final_time - time)
                                processes[i].res_at = final_time
                                time = final_time
                                processes[i].end_times.append(time)
                                flag = True
                                break
                            else:
                                time += processes[i].remaining_time
                                processes[i].end_times.append(time)
                                processes[i].waiting_time = time - processes[i].burst_time - processes[i].arrival_time
                                processes[i].remaining_time = 0
                                sequence.append(processes[i].pid)

            elif processes[i].res_at > time:
                time += 1
                i -= 1
        if flag:
            break


def fcfs(processes, t):
    total_time = t[1] - t[0]
    cur_time = t[0]
    for i in range(len(processes)):
        if processes[i].arrival_time <= cur_time and processes[i].remaining_time != 0:
            if processes[i].remaining_time > total_time:
                processes[i].starting_times.append(cur_time)
                processes[i].remaining_time -= total_time
                processes[i].end_times.append(t[1])
                break
            elif processes[i].remaining_time < total_time:
                processes[i].starting_times.append(cur_time)
                cur_time += processes[i].remaining_time
                total_time -= processes[i].remaining_time
                processes[i].end_times.append(cur_time)
                processes[i].remaining_time = 0
            else:
                processes[i].remaining_time = 0
                processes[i].starting_times.append(cur_time)
                processes[i].end_times.append(t[1])
                break

        elif processes[i].arrival_time > cur_time:
            cur_time += 1
            i -= 1


def scheduler(queueues):
    rem_bt = [0]*n
    lt = [0]*n
    st = queueues[0].processes[0].arrival_time
    for i in range(len(queueues)):
        rem_bt[i] = queueues[i].total_burst_time
        lt[i] = queueues[i].limiting_time
    t = st
    while 1:
        done = True
        for i in range(len(rem_bt)):
            if rem_bt[i] > 0:
                done = False
                if rem_bt[i] > quantum or lt[i] > t:
                    queueues[i].starting_times.append(t)
                    t += quantum
                    queueues[i].ending_times.append(t)
                    rem_bt[i] -= quantum
                    if rem_bt[i] < 0:
                        rem_bt[i] = 0
                else:
                    queueues[i].starting_times.append(t)
                    t = t + rem_bt[i]
                    queueues[i].ending_times.append(t)
                    rem_bt[i] = 0

        if done:
            break


def Queue3_runner(q3):
    for t in zip(q3.starting_times, q3.ending_times):
        process_to_run = []
        for p in q3.processes:
            if p.arrival_time in range(t[1]) and p.remaining_time != 0:
                process_to_run.append(p)
        print(f'Queue3 runs from {t[0]} to {t[1]}')
        roundrobin(process_to_run, t)


def Queue2_runner(q):
    q.processes.sort(key=lambda x: x.priority, reverse= True)
    for t in zip(q.starting_times, q.ending_times):
        process_to_run = []
        for p in q.processes:
            if p.arrival_time in range(t[1]) and p.remaining_time != 0:
                process_to_run.append(p)
        # print(process_to_run)
        # print(t)
        print(f'Queue2 runs from {t[0]} to {t[1]}')
        fcfs(process_to_run, t)


def Queue1_runner(q):
    for t in zip(q.starting_times, q.ending_times):
        process_to_run = []
        for p in q.processes:
            if p.arrival_time in range(t[1]) and p.remaining_time != 0:
                process_to_run.append(p)
        # print(process_to_run)
        # print(t)
        print(f'Queue1 runs from {t[0]} to {t[1]}')
        fcfs(process_to_run, t)


def gantt_chart_queue(jobs):
    t = []
    for q in jobs:
        tl = []
        for times in zip(q.starting_times, q.ending_times):
            tl.append((times[0], times[1]-times[0]))
        t.append(tl)
    n = len(t)
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 50)
    gnt.set_xlim(0, 160)
    gnt.set_xlabel('Queue switching science start')
    gnt.set_ylabel('Queue')
    gnt.set_yticks([15, 25, 35])
    gnt.set_yticklabels(['Queue1', 'Queue2', 'Queue3'])
    gnt.grid(True)
    gnt.broken_barh(t[0], (30, 9), facecolors=('tab:orange'))
    gnt.broken_barh(t[1], (20, 9), facecolors=('tab:red'))
    gnt.broken_barh(t[2], (10, 9), facecolors=('tab:blue'))
    plt.show()


def gantt_chart_process(processes):
    t = []
    pids = []
    height = 10
    i = 15
    pos = []
    for p in processes:
        tl = []
        for times in zip(p.starting_times, p.end_times):
            tl.append((times[0], times[1]-times[0]))
        pids.append(p.pid)
        pos.append(i)
        i += 10
        t.append(tl)
    n = len(t)
    fig, gnt = plt.subplots()
    gnt.set_ylim(0, 50)
    gnt.set_xlim(0, 200)
    gnt.set_xlabel('Processes running science start')
    gnt.set_ylabel('Process')
    gnt.set_yticks(pos)
    gnt.set_yticklabels(pids)
    gnt.grid(True)
    for i in range(n):
        gnt.broken_barh(t[i], (height, 9), facecolors=('tab:blue'))
        height += 10
    plt.show()
    plt.savefig('gantt2.png')


n = int(input("Enter total number of processes: "))
get_input(n)
scheduler([q3, q2, q1])
if len(q1.processes) > 0:
    print("\n\t\tQueue1 (Priority range[1, 3])")
    q1.print_queue()
    Queue1_runner(q1)
if len(q2.processes) > 0:
    print("\n\t\tQueue2 (Priority range[4, 6])")
    q2.print_queue()
    Queue2_runner(q2)
if len(q3.processes) > 0:
    print("\n\t\tQueue3 (Priority range[7, 9])")
    q3.print_queue()
    Queue3_runner(q3)

gantt_chart_queue([q3, q2, q1])
print("\n=======================================\n")
total_queue.print_table()
gantt_chart_process(total_queue.processes)


'''
q1.print_queue()
scheduler([q3, q2, q1])
print(q1.starting_times)
print(q1.ending_times)
q2.print_queue()
print(q2.starting_times)
print(q2.ending_times)
q3.print_queue()
print(q3.starting_times)
print(q3.ending_times)
Queue3_runner(q3)
Queue2_runner(q2)
Queue1_runner(q1)
print("\n +++++++++++++++++++++++++++++++++ \n")
for p in q3.processes:
    p.print_starting_times()
    p.print_ending_times()
print("\n +++++++++++++++++++++++++++++++++ \n")
for p in q2.processes:
    p.print_starting_times()
    p.print_ending_times()
print("\n +++++++++++++++++++++++++++++++++ \n")
for p in q1.processes:
    p.print_starting_times()
    p.print_ending_times()
'''