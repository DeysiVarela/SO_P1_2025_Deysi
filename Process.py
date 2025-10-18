# mlq_simulator.py
from collections import deque
from dataclasses import dataclass, field
import pandas as pd

@dataclass
class Process:
    pid: str
    burst: int
    arrival: int
    queue: int
    priority: int
    remaining: int = field(init=False)
    start_time: int = field(default=None)
    completion_time: int = field(default=None)
    response_time: int = field(default=None)
    waiting_time: int = field(default=0)
    turnaround_time: int = field(default=None)
    def __post_init__(self):
        self.remaining = self.burst

def parse_file(path):
    procs = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            parts = [x.strip() for x in line.split(';')]
            pid = parts[0]
            burst = int(parts[1])
            arrival = int(parts[2])
            queue = int(parts[3])
            pr = int(parts[4])
            procs.append(Process(pid, burst, arrival, queue, pr))
    return procs

def mlq_simulate(processes, q_scheme=(1,3,'SJF')):
    q1_quantum, q2_quantum, q3_policy = q_scheme
    time = 0
    processes = sorted(processes, key=lambda p: p.arrival)
    n = len(processes)
    finished = 0
    q1 = deque()
    q2 = deque()
    q3 = []
    arrived = set()
    def add_new_arrivals(t):
        for p in processes:
            if p.arrival <= t and p.pid not in arrived:
                arrived.add(p.pid)
                if p.queue == 1:
                    q1.append(p)
                elif p.queue == 2:
                    q2.append(p)
                else:
                    q3.append(p)
    timeline = []
    add_new_arrivals(0)
    while finished < n:
        add_new_arrivals(time)
        if q1:
            p = q1.popleft(); q = 1; quantum = q1_quantum
        elif q2:
            p = q2.popleft(); q = 2; quantum = q2_quantum
        elif q3:
            p = min(q3, key=lambda x: x.remaining); q3.remove(p); q = 3; quantum = None
        else:
            # advance to next arrival
            future = [p.arrival for p in processes if p.pid not in arrived]
            if not future:
                break
            time = min(future)
            add_new_arrivals(time)
            continue

        if p.start_time is None:
            p.start_time = time
            p.response_time = time - p.arrival

        if q in (1,2):
            exec_time = min(quantum, p.remaining)
        else:
            exec_time = p.remaining

        t_start = time
        time += exec_time
        p.remaining -= exec_time
        timeline.append((t_start, time, p.pid))
        add_new_arrivals(time)
        if p.remaining == 0:
            p.completion_time = time
            p.turnaround_time = p.completion_time - p.arrival
            p.waiting_time = p.turnaround_time - p.burst
            finished += 1
        else:
            if q == 1:
                q1.append(p)
            elif q == 2:
                q2.append(p)
            else:
                q3.append(p)

    rows = []
    for p in sorted(processes, key=lambda x: x.pid):
        rows.append({
            'Etiqueta': p.pid,
            'BT': p.burst,
            'AT': p.arrival,
            'Q': p.queue,
            'Pr': p.priority,
            'WT': p.waiting_time,
            'CT': p.completion_time,
            'RT': p.response_time,
            'TAT': p.turnaround_time
        })
    df = pd.DataFrame(rows)
    avg_WT = df['WT'].mean()
    avg_CT = df['CT'].mean()
    avg_RT = df['RT'].mean()
    avg_TAT = df['TAT'].mean()
    return df, (avg_WT, avg_CT, avg_RT, avg_TAT), timeline

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python Process.py <archivo_entrada>")
        sys.exit(1)
    procs = parse_file(sys.argv[1])
    df, avgs, timeline = mlq_simulate(procs, q_scheme=(1,3,'SJF'))
    print(df.to_csv(sep=';', index=False))
    print(f"Promedios: WT={avgs[0]:.2f}; CT={avgs[1]:.2f}; RT={avgs[2]:.2f}; TAT={avgs[3]:.2f}")
