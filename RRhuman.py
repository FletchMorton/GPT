class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.remaining_time = burst_time # Store the remaining burst time
        self.start_time = None
        self.finish_time = None
        self.response_time = None
        self.wait_time = 0
        self.turnaround_time = None
        self.selected_time = None

def round_robin_scheduler(processes, time_quantum):
    current_time = 0
    process_queue = []
    finished_processes = [] # Student Created
    unfinished_processes = [] # Student Created
    current_process = None  # Initialize to None

    while True:
        # Add newly arrived processes to the queue and log the arrival time
        while processes and processes[0].arrival_time <= current_time:
            new_process = processes.pop(0)
            new_process.arrival_time = current_time
            process_queue.append(new_process)
            unfinished_processes.append(new_process) # Student Created
            print(f"Time {current_time}: {new_process.pid} arrived") #Edited for formatting

        if process_queue:
            current_process = process_queue.pop(0)
            if current_process.start_time is None:
                current_process.start_time = current_time
                current_process.response_time = current_process.start_time - current_process.arrival_time
                current_process.selected_time = current_time

            print(f"Time {current_time}: {current_process.pid} selected (burst {current_process.remaining_time})")

            if current_process.remaining_time <= time_quantum:
                current_time += current_process.remaining_time

                # Student generated to implement wait time correctly
                for process in unfinished_processes:
                    if process is not current_process and process.selected_time is not None:
                        if process.selected_time < current_time:
                            process.wait_time += current_process.remaining_time
                            print(f"{process.pid} is waiting for {current_process.remaining_time}")

                unfinished_processes.pop(0) # Student Created
                current_process.finish_time = current_time
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                current_process.remaining_time = 0
                finished_processes.append(current_process) # Student Created
                print(f"Time {current_time}: {current_process.pid} completed")

            else:
                current_time += time_quantum

                # Student generated to implement wait time correctly
                for process in unfinished_processes:
                    if process is not current_process and process.selected_time is not None:
                        if process.selected_time < current_time:
                            process.wait_time += time_quantum
                            print(f"{process.pid} is waiting for {time_quantum}")

                current_process.remaining_time -= time_quantum
                process_queue.append(current_process)
                print(f"Time {current_time}: {current_process.pid} (remaining burst {current_process.remaining_time})")

        elif processes:
            # No processes in the queue, but some are waiting to arrive
            current_time += 1
            print(f"Time {current_time}: Idle")

        else:
            # No processes in the queue or waiting to arrive
            print(f"Finished at time {current_time}\n")
            break

    # Student Intervention: I reworked the method by which processes were considered finished/unfinished. As such, code was removed here

    for unfin in unfinished_processes:
        print(f"{unfin.pid} did not finish")

    print("\n")

    for process in finished_processes:
        print(f"{process.pid}\twait\t{process.wait_time}\tturnaround\t{process.turnaround_time}\tresponse\t{process.response_time}")


if __name__ == "__main__":
    # Define your list of processes with arrival times and burst times.
    processes = [
        Process(1, 0, 8),
        Process(2, 1, 4),
        Process(3, 2, 9),
        Process(4, 3, 5),
    ]

    time_quantum = 3  # Set the time quantum for Round Robin
    print(f"Simulation Log (Time Quantum = {time_quantum}):")
    round_robin_scheduler(processes, time_quantum)
