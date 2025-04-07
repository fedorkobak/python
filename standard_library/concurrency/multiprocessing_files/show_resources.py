import os
pid = os.getpid()

def show_resources():
    pid = os.getpid()
    print(os.listdir(f"/proc/{pid}/fd"))
