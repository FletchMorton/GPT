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
    current_process = None  # Initialize to None
    all_processes_completed = False  # Flag to track if all processes are completed

    while (current_time < runfor or process_queue or processes) and current_time <= runfor:
        # Add newly arrived processes to the queue and log the arrival time
        while processes and processes[0].arrival_time <= current_time:
            new_process = processes.pop(0)
            new_process.arrival_time = current_time
            process_queue.append(new_process)
            print(f"Time {current_time}: {new_process.pid} arrived (burst {new_process.remaining_time})")

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
                    current_process.finish_time = current_time
                    current_process.wait_time = current_process.start_time - current_process.arrival_time
                    current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                    print(f"Time {current_time}: {current_process.pid} completed")
                    process_queue.pop(0)  # Remove completed process from the queue
                    current_process = None

        else:
            print(f"Time {current_time}: Idle")
            current_time += 1

    # Check if any processes did not finish
    unfinished_processes = [process.pid for process in processes if process.finish_time is None]
    if unfinished_processes:
        print(f"The following processes did not finish: {', '.join(map(str, unfinished_processes))}")

    # Check if all processes finished within the time frame
    all_finished = all(process.finish_time is not None for process in processes)
    if all_finished:
        print(f"Finished at time {runfor}")

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
