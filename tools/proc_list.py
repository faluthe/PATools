import os

def get_proc_list(filter=""):
    proc_list = []

    for pid in os.listdir("/proc"):
        if pid.isdigit():
            try:
                with open(os.path.join("/proc", pid, "comm"), "r") as f:
                    comm = f.read().strip()
                    if filter in comm:
                        proc_list.append((comm, int(pid)))
            except:
                continue

    # Sort by process name
    proc_list.sort(key=lambda x: x[0].lower())

    return proc_list