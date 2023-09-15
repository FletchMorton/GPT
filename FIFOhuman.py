class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time  # Store the remaining burst time
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.wait_time = None
        self.turnaround_time = None

def fifo_scheduler(processes, runfor):
    current_time = 0
    process_queue = []
    finished_processes = []
    unfinished_processes = []
    current_process = None  # Initialize to None

    while (current_time < runfor or process_queue or processes) and current_time <= runfor:
        # Add newly arrived processes to the queue and log the arrival time
        while processes and processes[0].arrival_time <= current_time:
            new_process = processes.pop(0)
            new_process.arrival_time = current_time
            process_queue.append(new_process)
            unfinished_processes.append(new_process)
            print(f"Time {current_time}: {new_process.pid} arrived")

        if current_process is None and process_queue:
            current_process = process_queue.pop(0)
            if current_process.start_time is None:
                current_process.start_time = current_time
                current_process.response_time = current_process.start_time - current_process.arrival_time

            print(f"Time {current_time}: {current_process.pid} selected (burst {current_process.remaining_time})")

        if current_process:
            if current_process.remaining_time > 0:
                current_process.remaining_time -= 1
                current_time += 1
            else:
                unfinished_processes.pop(0)
                current_process.finish_time = current_time
                current_process.wait_time = current_process.start_time - current_process.arrival_time
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                print(f"Time {current_time}: {current_process.pid} completed")
                finished_processes.append(current_process)
                current_process = None  # Set to None to select the next process

        else:
            print(f"Time {current_time}: Idle")
            current_time += 1  # Idle CPU time when no process is in the queue

    print(f"Finished at time {runfor}\n")

    for unfin in unfinished_processes:
        print(f"{unfin.pid} did not finish")

    print("\n")

    for process in finished_processes:
        print(f"{process.pid}\twait\t{process.wait_time}\tturnaround\t{process.turnaround_time}\tresponse\t{process.response_time}")


if __name__ == "__main__":
    # Define your list of processes with arrival times and burst times.
    processes = [
        Process(1, 0, 10),
        Process(2, 1, 5),
        Process(3, 4, 8),
        Process(4, 7, 2),
    ]

    runfor = 20  # Set the simulation run time to 20 time units
    print(f"Simulation Log (Run for {runfor} Time Units):")
    fifo_scheduler(processes, runfor)
