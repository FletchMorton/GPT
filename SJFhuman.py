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

def preemptive_sjf_scheduler(processes, runfor):
    current_time = 0
    process_queue = []
    finished_processes = [] # Student Created
    unfinished_processes = [] # Student Created
    current_process = None  # Initialize to None

    while (current_time < runfor or process_queue or processes) and current_time <= runfor:
        # Add newly arrived processes to the queue and log the arrival time
        while processes and processes[0].arrival_time <= current_time:
            new_process = processes.pop(0)
            new_process.arrival_time = current_time
            process_queue.append(new_process)
            unfinished_processes.append(new_process) # Student Created
            print(f"Time {current_time}: {new_process.pid} arrived") # Edited for formatting

        # Sort the process queue based on remaining time
        process_queue.sort(key=lambda x: x.remaining_time)

        # Select the process
        if process_queue:
            if current_process is None:
                current_process = process_queue[0]
                if current_process.start_time is None:
                    current_process.start_time = current_time
                    current_process.response_time = current_process.start_time - current_process.arrival_time

                print(f"Time {current_time}: {current_process.pid} selected (burst {current_process.remaining_time})")

            elif process_queue[0].remaining_time < current_process.remaining_time:
                # Preempt the current process if a shorter one arrives
                print(f"Time {current_time}: {current_process.pid} preempted by {process_queue[0].pid}")
                process_queue.append(current_process)
                current_process = process_queue[0]
                if current_process.start_time is None:
                    current_process.start_time = current_time
                print(f"Time {current_time}: {current_process.pid} selected (burst {current_process.remaining_time})")

            if current_process.remaining_time > 0:
                current_process.remaining_time -= 1
                current_time += 1
                # Check if the process has completed
                if current_process.remaining_time == 0:
                    unfinished_processes.pop(0) # Student Created
                    current_process.finish_time = current_time
                    current_process.wait_time = current_process.start_time - current_process.arrival_time
                    current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                    print(f"Time {current_time}: {current_process.pid} completed")
                    finished_processes.append(current_process) # Student Created
                    process_queue.pop(0)  # Remove completed process from the queue
                    current_process = None

        else:
            print(f"Time {current_time}: Idle")
            current_time += 1

    # Student Intervention: I reworked the method by which processes were considered finished/unfinished. As such, code was removed here

    print(f"Finished at time {runfor}\n")

    for unfin in unfinished_processes:
        print(f"{unfin.pid} did not finish")

    print("\n")

    for process in finished_processes:
        print(f"{process.pid}\twait\t{process.wait_time}\tturnaround\t{process.turnaround_time}\tresponse\t{process.response_time}")


if __name__ == "__main__":
    # Define your list of processes with arrival times and burst times.
    processes = [
        Process(1, 0, 5),
        Process(2, 1, 4),
        Process(3, 4, 2),
    ]

    runfor = 20  # Set the simulation run time to 20 time units
    print(f"Simulation Log (Run for {runfor} Time Units):")
    preemptive_sjf_scheduler(processes, runfor)
