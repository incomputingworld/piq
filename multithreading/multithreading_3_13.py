# Multi threading, Global Interpreter Lock (GIL) and Multiprocessing
""""""
# 1. threading.Thread - Independent thread of execution.
"""
Used  to create, start and manage a thread that runs concurrently in main program.
Syntax: threading.Thread(group=None, target=None, name=None, args=(), kwargs={}, daemon=None)

group   Reserved for future use; always None.
target	The callable (function) to be executed in the thread.
name	Thread name (optional, defaults to "Thread-N").
args	Tuple of positional arguments for target.
kwargs	Dict of keyword arguments for target.
daemon	Boolean – whether the thread is daemon (background).

Methods:
.start()	        Starts the thread’s activity (calls run() internally).
.run()              Defines the thread’s behavior (override in subclass).
.join(timeout=None)	Waits for thread to finish (optional timeout).
.is_alive()	        Checks if the thread is still active.
.setName(name)  	Set thread’s name.
.getName()	        Get thread’s name.
.daemon	            If True, thread ends when main program ends.
"""

# Simple thread example

# import threading
# import time
# import sys
#
# counter = 0
#
# print(sys._is_gil_enabled())
#
# def worker(name, increments=1000):
#     global counter
#     for _ in range(increments):
#         counter += 1
#         # tiny sleep just to make interleaving observable (optional)
#         time.sleep(0.0001)
#     print(f"{name} done")
#
#
# threads = [threading.Thread(target=worker, args=("T1",)),
#            threading.Thread(target=worker, args=("T2",)), threading.Thread(target=worker, args=("T3",))]
#
# for t in threads:
#     t.start()
#
# # for t in threads:
# #     t.join()
#
# print("Final counter:", counter)


# Threading functions
"""
threading.current_thread()      Returns a reference to the currently running Thread object.
"""

# import logging
# import threading
#
# logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")
#
# def worker():
#     t = threading.current_thread()
#     logging.info(f"[{t.name}] starting")
#     # ... work ...
#     logging.info(f"[{t.name}] done")
#
#
# thread_1 = threading.Thread(target=worker, name="worker-1")
# thread_2 = threading.Thread(target=worker, name="worker-2")
# thread_3 = threading.Thread(target=worker, name="worker-3")
#
# thread_1.start()
# thread_2.start()
# thread_3.start()

"""
threading.active_count()        Returns the number of threads currently alive, including the main thread
"""

# import threading
# import time
#
#
# def quick_task():
#     print(f"{threading.current_thread().name} - {threading.active_count()}")
#     time.sleep(0.5)
#
#
# threads = [threading.Thread(target=quick_task, name=f"quick_{i}") for i in range(5)]
# for t in threads:
#     t.start()
#
# while threading.active_count() > 1:  # >1 means threads other than main are alive
#     time.sleep(0.1)
# print("All worker threads finished")

"""
threading.enumerate()           Returns a list of all active threads.
"""

# import threading
# import time
#
#
# def heartbeat():
#     for _ in range(2):
#         alive = threading.enumerate()
#         print("Alive:", [(t.name, t.daemon) for t in alive])
#         time.sleep(.5)
#
#
# threads = [threading.Thread(target=heartbeat, name=f"quick_{i}") for i in range(3)]
#
# for t in threads:
#     t.start()


"""
threading.main_thread()         Returns a reference to the main thread of the program.
"""

# import threading
#
#
# def update_ui():
#     if threading.current_thread() is threading.main_thread():
#         print("UI updated safely in the main thread.")
#     else:
#         print("⚠️ Cannot update UI from a worker thread!")
#
#
# def worker():
#     update_ui()
#
#
# t = threading.Thread(target=worker)
# t.start()
# t.join()
# update_ui()


# DEMO: I/O-bound vs CPU-bound tasks
import threading
import time


def io_bound_task(task_id: int) -> str:
    print(f"  I/O Task {task_id} started on thread {threading.current_thread().name}")
    time.sleep(1)  # Simulates waiting for I/O
    print(f"  I/O Task {task_id} completed")
    return f"I/O Result {task_id}"


def cpu_bound_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i ** 2
    print(f"  CPU Task completed: {total}")
    return total


# def demo_sequential():
#     # I/O-bound tasks
#     print("\n🔹 I/O-Bound Tasks (sequential):")
#     start = time.time()
#     for i in range(3):
#         io_bound_task(i)
#     io_time = time.time() - start
#     print(f"⏱️  Total time: {io_time:.2f}s")
#
#     # CPU-bound tasks
#     print("\n🔹 CPU-Bound Tasks (sequential):")
#     start = time.time()
#     for i in range(3):
#         cpu_bound_task(10_000_000)
#     cpu_time = time.time() - start
#     print(f"⏱️  Total time: {cpu_time:.2f}s\n")
#
#     return io_time, cpu_time
#
# print(demo_sequential())

def demo_threading():
    # I/O-bound with threading (GOOD! ✅)
    print("\n🔹 I/O-Bound Tasks with Threading:")
    start = time.time()
    threads = []
    for i in range(3):
        thread = threading.Thread(target=io_bound_task, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    io_time = time.time() - start
    print(f"⏱️  Total time: {io_time:.2f}s")
    print(f"✅ Speed-up: ~3x faster! (3 seconds → 1 second)")

    # CPU-bound with threading (BAD! ❌)
    print("\n🔹 CPU-Bound Tasks with Threading:")
    start = time.time()
    threads = []
    for i in range(3):
        thread = threading.Thread(target=cpu_bound_task, args=(10_000_000,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    cpu_time = time.time() - start
    print(f"⏱️  Total time: {cpu_time:.2f}s")
    print(f"❌ No speed-up! (GIL prevents parallel execution)\n")

    return io_time, cpu_time

demo_threading()