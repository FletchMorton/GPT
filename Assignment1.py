# Information about the process
class Process:
    def __init__(self, pid, arrival_time, burst_time):
        self.pid = pid                      # Name of the process
        self.arrival_time = arrival_time    # When the process arrived in the scheduler
        self.burst_time = burst_time        # How long the process will take to complete
        self.remaining_time = burst_time    # Store the remaining burst time
        self.start_time = None              # When the process was selected for execution
        self.finish_time = None             # When the process finished
        self.response_time = None           # Amount of time between arrival_time and start_time
        self.wait_time = 0                  # How long the process had to wait to regain the CPU
        self.turnaround_time = None         # Amount of time between start_time and finish_time
        self.selected_time = None           # When was the process last selected for CPU time

# FIFO
def fifo_scheduler(processes, runfor):
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
                unfinished_processes.pop(0) # Student Created
                current_process.finish_time = current_time
                # Deleted wait_time, as it was unnecessary in this scheduler
                current_process.turnaround_time = current_process.finish_time - current_process.arrival_time
                print(f"Time {current_time}: {current_process.pid} finished")
                finished_processes.append(current_process) # Student Created
                current_process = None  # Set to None to select the next process

        else:
            print(f"Time {current_time}: Idle")
            current_time += 1  # Idle CPU time when no process is in the queue

    # Student Intervention: I reworked the method by which processes were considered finished/unfinished. As such, code was removed here

    print(f"Finished at time {runfor}\n")

    for unfin in unfinished_processes:
        print(f"{unfin.pid} did not finish")

    print("\n")

    for process in finished_processes:
        print(f"{process.pid}\twait\t{process.wait_time}\tturnaround\t{process.turnaround_time}\tresponse\t{process.response_time}")


#SJF
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
                    print(f"Time {current_time}: {current_process.pid} finished")
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


#RR
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
                print(f"Time {current_time}: {current_process.pid} finished")

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


# Main
if __name__ == "__main__":

    # What is being detected when reading the file
    directives = {
        "processcount": None,
        "runfor": 0,
        "use": None,
        "quantum": 0,
        "process": [None, 0, 0],
        "end": False
    }

    # Variables
    processes = []
    processcount = None
    runfor = 0
    use = None
    quantum = 0
    end = False
    file_path = "inp.txt"

    # Read the file and collection information
    with open(file_path, 'r') as file:
        # For each line within the file
        for line in file:
            # Ignore comments starting with '#' and strip leading/trailing whitespace
            line = line.split('#')[0].strip()
            
            # Split the line by whitespace to separate directive and value
            parts = line.split()

            # For directives that only have a singular value associated with it
            if len(parts) == 2:
                directive, value = parts[0], parts[1]
                if directive in directives:
                    # Assign the value to the corresponding directive
                    directives[directive] = value

            # This is the end statement. Flip the flag
            elif len(parts) == 1:
                directive = parts[0]
                if directive in directives:
                    if directive == "end":
                        directives[directive] = True

            # This is a process. Set the subdirectives within the process (name, arrival_time, burst_time)
            elif len(parts) > 2:
                directive, name, arrival, burst = parts[0], parts[2], parts[4], parts[6]
                if directive in directives:
                    processes.append(Process(name, int(arrival), int(burst)))

            # This must be some type of error
            else:
                print("There was an issue with the file formatting.")


    # Add the collected information to their respective values
    for directive in directives:
        match directive:
            case "processcount":
                processcount = directives[directive]
                print(f"{processcount} processes")
            case "runfor":
                runfor = int(directives[directive])
            case "quantum":
                quantum = int(directives[directive])
            case "use":
                use = directives[directive]
            case "end":
                end = directives[directive]
    
    # Execute the requested scheduling algorithm
    match use:
        case "fifo":
            print("Using First In First Out")
            fifo_scheduler(processes, runfor)
        case "sjf":
            print("Using preemptive Shortest Job First")
            preemptive_sjf_scheduler(processes, runfor)
        case "rr":
            print("Using preemptive Round Robin")
            round_robin_scheduler(processes, quantum)