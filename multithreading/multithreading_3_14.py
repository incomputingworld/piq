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
# for t in threads:
#     t.join()
#
# print("Final counter:", counter)




# Thread Synchronization

# import threading
# import time
#
# counter = 0
# lock = threading.Lock() # Create Lock object
#
# def worker(name, increments=1000):
#     global counter
#     for _ in range(increments):
#         # with lock:  # aquire lock. Automatically release lock after executing critical section.
#         #     counter += 1    # represents critical section
#         lock.acquire()
#         counter += 1
#         lock.release()
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
# for t in threads:
#     t.join()
#
# print("Final counter:", counter)



# threading.RLock (Reentrant lock)


# import threading
#
# tree = {
#     "name": "root", "children": [
#         {"name": "a", "children": []},
#         {"name": "b", "children": [
#             {"name": "b1", "children": []},
#             {"name": "b2", "children": []},
#         ]},
#     ],
# }
#
# rlock = threading.RLock()
# def annotate_sizes(node):
#     with rlock:  # Enter critical section; same thread can re-enter this in recursion
#         size = 1  # count this node
#         for child in node.get("children", []):  # get value of the key "children"
#             size += annotate_sizes(child)  # recursive call re-acquires rlock
#         node["size"] = size
#         print(size)
#         return size
#
# # Run a worker thread to demonstrate thread-safety and reentrancy
# t = threading.Thread(target=annotate_sizes, args=(tree,))
# t.start()
# t.join()
#
# print(tree)



# import threading
#
# rLock = threading.RLock()
#
# def outer():
#     with rLock:
#         print("Outer acquired lock")
#         inner()
#
# def inner():
#     with rLock:
#         print("Inner acquired lock")
#
# t = threading.Thread(target=outer)
# t.start()
# t.join()
""""""
# import queue
# import threading
# import time

# threading.Event()

"""
Method	Description
event.is_set()	            Returns True if the event’s flag is True, else False
event.set()	                Sets the flag to True and releases all waiting threads
event.clear()	            Resets the flag to False, causing threads calling wait() to block again
event.wait(timeout=None)	Blocks the thread until the flag is True or timeout occurs
"""



# import threading
#
# event = threading.Event()
#
# def worker():
#     print(f"{threading.current_thread().name} - waiting for event... it is {event.is_set()}")
#     event.wait()  # Wait until event is set
#     print(f"{threading.current_thread().name} - Event is set ({event.is_set()}), starts processing...")
#
# t1 = threading.Thread(target=worker, name="Thread_1")
# t2 = threading.Thread(target=worker, name="Thread_2")
# t1.start()
# t2.start()
#
# # Main thread
# time.sleep(3)
# print("Main thread took 3 seconds to complete its work...")
# event.set()  # Signal the worker to start


# import threading
# import time
#
# # Shared Event object
# event = threading.Event()
#
# def controller():
#     while True:
#         print("\n[Controller] Signal ON (event set)")
#         event.set()          # Allow workers to run
#         time.sleep(1)        # Keep signal ON for 2 sec
#         print("[Controller] Signal OFF (event cleared)")
#         event.clear()        # Stop workers
#         time.sleep(3)        # Wait before next signal
#
# def worker(name):
#     while True:
#         print(f"{name} waiting for signal... it is {event.is_set()}")
#         event.wait()         # Block until signal is ON
#         print(f"{name} received signal, working...")
#         time.sleep(1)        # Simulate doing work
#         print(f"{name} done with work cycle.")
#
# # Start controller thread
# controller_thread = threading.Thread(target=controller, daemon=True)
# controller_thread.start()
#
# # Start worker threads
# for i in range(2):
#     threading.Thread(target=worker, args=(f"Worker-{i}",), daemon=True).start()
#
# # Keep main thread alive
# for _ in range(10):
#     time.sleep(1)



# threading.Semaphore()


# import threading
# import time
#
# # Allow maximum 2 threads at a time
# semaphore = threading.Semaphore(2)
#
# def worker():
#     print(f"{threading.current_thread().name} trying to acquire semaphore...")
#     with semaphore:
#         print(f"{threading.current_thread().name} acquired semaphore!")
#         time.sleep(1)  # simulate work
#         print(f"{threading.current_thread().name} releasing semaphore...")
#     print(f"{threading.current_thread().name} done.")
#
# for i in range(5):
#     t = threading.Thread(target=worker, name=f"Worker_{i+1}")
#     t.start()

# Producer - Consumer pattern implementation.
# import threading
# import time
# import random
#
# buffer = []
# BUFFER_SIZE = 3
#
# # Semaphore to track empty and full slots
# empty_slots = threading.Semaphore(BUFFER_SIZE)  # Controls items can be produced before the buffer is full
# full_slots = threading.Semaphore(0)  # Used for thread synchronization. Controls order of execution
# mutex = threading.Lock()  # Ensures only one thread updates this buffer.
#
# def producer():
#     while True:
#         item = random.randint(1, 100)
#         print(f"{threading.current_thread().name} waiting for empty_slots semaphore ...")
#         empty_slots.acquire()  # Wait if buffer full
#         print(f"{threading.current_thread().name} acquired empty_slots semaphore ...")
#         with mutex:
#             buffer.append(item)
#             print(f"{threading.current_thread().name} - Produced {item} | Buffer: {buffer}")
#         full_slots.release()  # Signal data added in buffer
#         time.sleep(random.random())
#
# def consumer():
#     while True:
#         print(f"{threading.current_thread().name} acquiring full_slots semaphore ...")
#         full_slots.acquire()  # Wait if buffer empty
#         print(f"{threading.current_thread().name} acquired full_slots semaphore ...")
#         with mutex:
#             item = buffer.pop(0)
#             print(f"{threading.current_thread().name} - Consumed {item} | Buffer: {buffer}")
#         empty_slots.release()  # Signal empty space available in buffer
#         time.sleep(random.random())

# for i in range(5):
#     threading.Thread(target=producer, name=f"Producer_{i+1}", daemon=True).start()
#
# for i in range(3):
#     threading.Thread(target=consumer, name=f"Consumer_{i+1}", daemon=True).start()

# for i in range(3):
#     threading.Thread(target=producer, name=f"Producer_{i+1}", daemon=True).start()
#
# for i in range(3):
#     threading.Thread(target=consumer, name=f"Consumer_{i+1}", daemon=True).start()

# for i in range(3):
#     threading.Thread(target=producer, name=f"Producer_{i+1}", daemon=True).start()
#
# for i in range(5):
#     threading.Thread(target=consumer, name=f"Consumer_{i+1}", daemon=True).start()

# time.sleep(3)


# Producer-Consumer Pattern using Event instead of Semaphore


# import threading
# import time
# import random
#
# buffer = []
# BUFFER_SIZE = 3
#
# # Semaphore to track empty and full slots
# empty_slots = threading.Semaphore(BUFFER_SIZE)  # Controls items can be produced before the buffer is full
# full_slots = threading.Event()  # Used for thread synchronization. Controls order of execution
# mutex = threading.Lock()  # Ensures only one thread updates this buffer.
#
# def producer():
#     while True:
#         item = random.randint(1, 100)
#         print(f"{threading.current_thread().name} waiting for empty_slots semaphore ...")
#         empty_slots.acquire()  # Wait if buffer full
#         print(f"{threading.current_thread().name} acquired empty_slots semaphore ...")
#         with mutex:
#             buffer.append(item)
#             print(f"{threading.current_thread().name} - Produced {item} | Buffer: {buffer}")
#         full_slots.set()  # Signal data added in buffer
#         time.sleep(random.random())
#
# def consumer():
#     while True:
#         print(f"{threading.current_thread().name} acquiring full_slots Event ...")
#         full_slots.wait()  # Wait if buffer empty
#         print(f"{threading.current_thread().name} acquired full_slots Event ...")
#         with mutex:
#             item = buffer.pop(0)
#             print(f"{threading.current_thread().name} - Consumed {item} | Buffer: {buffer}")
#         empty_slots.release()  # Signal empty space available in buffer
#         time.sleep(random.random())
#
# # for i in range(5):
# #     threading.Thread(target=producer, name=f"Producer_{i+1}", daemon=True).start()
# #
# # for i in range(3):
# #     threading.Thread(target=consumer, name=f"Consumer_{i+1}", daemon=True).start()
#
# for i in range(3):
#     threading.Thread(target=producer, name=f"Producer_{i+1}", daemon=True).start()
#
# for i in range(3):
#     threading.Thread(target=consumer, name=f"Consumer_{i+1}", daemon=True).start()
#
#
# time.sleep(3)


# threading.Condition

# import threading
# import time
# import random
#
# # Shared data and Condition object
# buffer = []
# BUFFER_SIZE = 5
# condition = threading.Condition()  # Uses Rlock internally
#
#
# def producer():
#     for _ in range(3):
#         item = random.randint(1, 100)
#         with condition:  # acquire lock on cond
#             while len(buffer) == BUFFER_SIZE: # Wait if buffer is full
#                 print(f"[{threading.current_thread().name}] Buffer full, waiting...")
#                 condition.wait()  # release lock & wait for a consumer to notify
#
#             buffer.append(item)  # Produce an item
#             print(f"[{threading.current_thread().name}] Produced item: {item} | Buffer: {buffer}")
#             condition.notify()  # Notify a consumer (possibly) that an item is available
#         time.sleep(random.uniform(0.5, 1))
#
#
# def consumer():
#     for _ in range(3):
#         with condition:  # acquire lock on cond
#             while not buffer: # Wait if buffer is empty
#                 print(f"[{threading.current_thread().name}] Buffer empty, waiting...")
#                 condition.wait()  # release lock & wait for producer to notify
#
#             item = buffer.pop(0)  # Consume the item
#             print(f"[{threading.current_thread().name}] Consumed item: {item} | Buffer: {buffer}")
#             condition.notify()  # Notify a producer (possibly) that space is free
#         time.sleep(random.uniform(0.5, 1))
#
#
# # Create threads
# for i in range(5):
#     producer_thread = threading.Thread(target=producer, name=f"Producer_{i+1}").start()
#
# for i in range(3):
#     consumer_thread = threading.Thread(target=consumer, name=f"Consumer_{i+1}").start()





# threading.Condition - with two separate conditions.

# import threading
# import time
# import random
#
# buffer = []
# BUFFER_SIZE = 5
# rlock = threading.RLock()
# not_full = threading.Condition(rlock)   # Consumer uses this to activate producer
# not_empty = threading.Condition(rlock)  # Producer uses this to activate consumer
#
#
# def producer():
#     print(f"[{threading.current_thread().name}] Created.")
#     for _ in range(3):
#         item = random.randint(1, 100)
#         with not_full:  # acquire lock
#             while len(buffer) >= BUFFER_SIZE: # Wait if buffer is full
#                 print(f"[{threading.current_thread().name}] Buffer full, waiting...")
#                 not_full.wait()  # release lock & wait for a consumer to notify
#
#             buffer.append(item)  # Produce an item
#             print(f"[{threading.current_thread().name}] Produced item: {item} | Buffer: {buffer}")
#             with not_empty:
#                 not_empty.notify_all()  # Notify a consumer that an item is available
#         time.sleep(random.uniform(0.3, 1))
#
#
# def consumer():
#     print(f"[{threading.current_thread().name}] Created.")
#     for _ in range(3):
#         with not_empty:  # acquire lock
#             while not buffer: # Wait if buffer is empty
#                 print(f"[{threading.current_thread().name}] Buffer empty, waiting...")
#                 not_empty.wait()  # release lock & wait for producer to notify
#
#             item = buffer.pop(0)  # Consume the item
#             print(f"[{threading.current_thread().name}] Consumed item: {item} | Buffer: {buffer}")
#             with not_full:
#                 not_full.notify_all()  # Notify a producer that space is free
#         time.sleep(random.uniform(0.5, 1.5))
#
#
# # Create threads
# for i in range(3):
#     producer_thread = threading.Thread(target=producer, name=f"Producer_{i+1}").start()
#
# for i in range(5):
#     consumer_thread = threading.Thread(target=consumer, name=f"Consumer_{i+1}").start()



# queue.Queue
"""
Queue(maxsize=0): Creates a new object of Queue.
maxsize = 0; infinite size. When maxsize > 0; queue blocks when full.

put(item, block=True, timeout=None): Adds a new item in the queue.
When block = True AND queue is full; block the thread
When block = False AND queue is full; raises queue.Full exception
When timeout is set, blocks the thread for a given time

get(block=True, timeout=None): Removes and returns an item from the queue
When block = True AND queue is empty; blocks the thread
When block = False AND queue is empty; raises queue.Empty exception
When timeout is set, blocks the thread for a given time

qsize(): Returns approximate size of queue. 
Not reliable for thread synchronization — but useful for logging/monitoring.

empty(): Returns True if queue seems empty. (Not guaranteed due to thread scheduling.)

full(): Returns True if queue seems full.

task_done(): Indicates that a consumer has completed processing one item. Used with join().

join(): Blocks until all items have been processed (task_done() called for each item).

"""


# import queue
#
# q = queue.Queue(3)  # Queue with max size of 3
#
# q.put(10)
# q.put(20)
# q.put(30)
# # q.put(40)             # Blocks the main thread. Program hangs.
# # q.put(50, timeout=1)  # Raises queue.Full exception after 1 second wait.
# # q.put_nowait(60)      # Raises queue.Full exception immediately. Non-blocking function. Does not wait
#
# print(q.get(), q.get(), q.get())
# print(q.get())            # Blocks the main thread. Program hangs.
# print(q.get(timeout=1) )  # Raises queue.Empty exception after 1 second wait.
# print(q.get_nowait())     # Raises queue.Empty exception immediately. Non-blocking function. Does not wait.




# Working of task_done() and join()

# import queue
# import threading
# import time
#
# q = queue.Queue()
#
# def worker():
#     while True:
#         item = q.get()
#         print(f"{threading.current_thread().name} - Processing {item}")
#         time.sleep(1)
#         q.task_done()  # signals completion
#
#
# # Start worker threads
# for i in range(2):
#     threading.Thread(target=worker, name=f"Worker_{i+1}", daemon=True).start()
#
# # Put tasks
# for i in range(5):
#     q.put(i)
#
# print("Waiting for all tasks to finish...")
# q.join()
# print("All tasks completed!")


# Producer Consumer Pattern using Queue


# import threading
# import queue
# import time
# import random
#
# q = queue.Queue(maxsize=3)
#
# def producer():
#     for _ in range(3):
#         item = random.randint(1, 100)
#         q.put(item)
#         print(f"{threading.current_thread().name} - produced {item} | Queue: {q.queue}")
#         time.sleep(random.random())
#
# def consumer():
#     while True:
#         item = q.get()
#         print(f"{threading.current_thread().name} - consumed {item} | Queue: {q.queue}")
#         q.task_done()
#         time.sleep(random.random() + 0.2)
#
# # Start threads
# for i in range(2):
#     threading.Thread(target=producer, name=f"Producer_{i+1}", daemon=True).start()
#
# for i in range(5):
#     threading.Thread(target=consumer, name=f"Consumer_{i+1}", daemon=True).start()
#
# q.join()



# threading.Barrier()
"""
threading.Barrier(parties, timeout=None): Creates an object of Barried class
parties: number of threads required to trip the barrier (Each thread calls barrier.wait()). All threads
    must reach barrier before all threads are released.
    When last thread reaches barrier, the barrier "trips" and all threads proceed.
timeout: Optional timeout for all waits

wait(timeout=None): Thread waits at barrier. Returns an integer index starting with 0. Used when 
    one thread must act as a leader
    
Broken Barrier: A barrier is broken when 
    a thread timesout while waiting or exits unexpectedly
    a thread calls barrier.reset() or barrier.abort()
All threads receive a BrokenBarrierError and barrier stays broken until manually reset.
    
reset(): resets barrier to initial state. All waiting threads get BrokenBarrierError
    Use when you want to restart a simulation or recover from an error

abort(): Stops barrier immediately and puts in broken state

parties: total number of participating threads

n_waiting: number of threads currently waiting at the barrier

broken: boolean variable indicating if barrier is broken 
"""

# threading.Barrier - normal flow.
# import threading
# import time
# import random
#
# barrier = threading.Barrier(parties=3)
#
# def worker():
#     name = threading.current_thread().name
#     try:
#         print(f"{name}: Stage 1 started")
#         time.sleep(random.uniform(0.5, 2))  # simulate processing
#
#         print(f"{name}: Waiting at barrier 1. Total waiting - {barrier.n_waiting}")
#         phase = barrier.wait()  # Wait at barrier. Returns 0 for the coordinator thread
#         if phase == 0:
#             print(f"{name}: I am the coordinator for Stage 1\n")
#
#         print(f"{name}: Stage 1 completed, moving to Stage 2")
#         time.sleep(random.uniform(0.5, 2))  # simulate processing
#
#
#         print(f"{name}: Waiting at barrier 2. Total waiting - {barrier.n_waiting}")
#         phase = barrier.wait()  # Second barrier
#         if phase == 1:
#             print(f"{name}: I am the coordinator for Stage 2\n")
#
#         print(f"{name}: Stage 2 completed successfully")
#
#     except threading.BrokenBarrierError:
#         print(f"{name}: Barrier is broken — exiting thread")
#
#     except Exception as e:
#         print(f"{name}: Unexpected error: {e}")
#
#
# threads = []
#
# for i in range(3):
#     t = threading.Thread(target=worker, name=f"Worker-{i+1}")
#     threads.append(t)
#     t.start()
#
# for t in threads:
#     t.join()



# threading.Barrier - Reset.
# import threading
#
# barrier = threading.Barrier(parties=3)
#
# def worker():
#     name = threading.current_thread().name
#     try:
#         print(f"{name}: Started and waiting at barrier")
#         barrier.wait()
#         print(f"{name}: Passed the barrier")
#     except threading.BrokenBarrierError:
#         print(f"{name}: Barrier broken due to reset()")
#
#
# threads = []
#
# for i in range(2):
#     t = threading.Thread(target=worker, name=f"Worker-{i+1}")
#     threads.append(t)
#     t.start()
#
# time.sleep(2)
# print("\nMain thread: Calling barrier.reset() to unblock waiting threads\n")
# barrier.reset()

# for t in threads:
#     t.join()



#threading.Barrier - abort
# import threading
#
# barrier = threading.Barrier(parties=3)
#
# def worker():
#     name = threading.current_thread().name
#     try:
#         print(f"{name}: Started and waiting at barrier")
#         barrier.wait()
#         print(f"{name}: Passed the barrier")
#     except threading.BrokenBarrierError:
#         print(f"{name}: Barrier aborted!")
#
#
# threads = []
#
# for i in range(2):
#     t = threading.Thread(target=worker, name=f"Worker-{i+1}")
#     threads.append(t)
#     t.start()
#
# time.sleep(2)
# print("\nMain thread: Calling barrier.abort() to break the barrier\n")
# barrier.abort()
#
# for t in threads:
#     t.join()



# threading.Barrier - timeout
# import threading
# import random
#
# barrier = threading.Barrier(parties=3)
#
# def worker(delay=False):
#     name = threading.current_thread().name
#     try:
#         print(f"{name}: Started and waiting at barrier")
#         if delay:
#             time.sleep(4)
#         else:
#             time.sleep(random.uniform(0.5, 2))
#         barrier.wait(timeout=2.5)
#         print(f"{name}: Passed the barrier")
#     except threading.BrokenBarrierError:
#         print(f"{name}: Barrier broken or timeout!")
#
# threads = [
#     threading.Thread(target=worker, name=f"Worker-1"),
#     threading.Thread(target=worker, name=f"Worker-2", args=(True,)),
#     threading.Thread(target=worker, name=f"Worker-3")]
#
# for t in threads:
#     t.start()
#
# for t in threads:
#     t.join()




#threading Barrier - Example

# import threading
#
# ROWS = 10000
# COLS = 10000
# matrix = [[0]*COLS for _ in range(ROWS)]
#
# threads = 4
# barrier = threading.Barrier(threads)
#
# def process_slice(tid):
#     start = (ROWS // threads) * tid
#     end   = (ROWS // threads) * (tid + 1)
#     print(f"Thread_{tid} - Starting Row: {start}, Ending Row: {end}")
#     for r in range(start, end):
#         for c in range(COLS):
#             matrix[r][c] = r + c
#     print(f"Thread {tid} done. Waiting at barrier...")
#     barrier.wait()
#
#     if barrier.wait() == 0:
#         print("All slices processed — now post-processing!")
#
#
# threads_list = [threading.Thread(target=process_slice, args=(i,)) for i in range(threads)]
#
# for t in threads_list:
#     t.start()
#
# for t in threads_list:
#     t.join()
#
# for row in range(10):
#     print(matrix[row])
#
# for row in range(991,1000):
#     print(matrix[row])




# Retrieve data from threads - Using Shared data + lock
# import threading
#
# counter = 0
# fiftieth_value = {"T1": [], "T2": [], "T3": []}
# lock = threading.Lock()
#
# def worker(name, increments=1000):
#     global counter
#     for i in range(increments):
#         with lock:
#             counter += 1
#         if i % 100 == 0:
#             with lock:
#                 fiftieth_value[name].append(counter)
#         time.sleep(0.0001)
#     print(f"{name} done")
#
# threads = [threading.Thread(target=worker, args=(f"T{i+1}",)) for i in range(3)]
#
# for t in threads:
#     t.start()
#
# for t in threads:
#     t.join()
#
# print("Final counter:", counter)
# for key, value in fiftieth_value.items():
#     print(key, value)




# Retrieve data from threads - using queue.Queue
# import threading
#
# counter = 0
# fiftieth_value = queue.Queue()
# lock = threading.Lock()
#
# def worker(name, increments=1000):
#     global counter
#     for i in range(increments):
#         with lock:
#             counter += 1
#         if i % 100 == 0:
#             with lock:
#                 fiftieth_value.put({name: f"{name}", "Index": i, "Value": counter})
#         time.sleep(0.0001)
#     print(f"{name} done")
#
# threads = [threading.Thread(target=worker, args=(f"T{i+1}",)) for i in range(3)]
#
# for t in threads:
#     t.start()
#
# for t in threads:
#     t.join()
#
# print("Final counter:", counter)
# while not fiftieth_value.empty():
#     print(fiftieth_value.get())




# Retrieve data from threads - using Thread Subclass
# import threading
#
# counter = 0
# lock = threading.Lock()
# fiftieth_value = queue.Queue()
#
# class MyThread(threading.Thread):
#     def __init__(self, name, increments=1000):
#         super().__init__()
#         self.name = name
#         self.increments = increments
#         self.snapshot = []
#
#     def run(self):
#         global counter
#         for i in range(self.increments):
#             with lock:
#                 counter +=1
#             if i % 100 == 0:
#                 with lock:
#                     self.snapshot.append({self.name: f"{self.name}", "Index": i, "Value": counter})
#             time.sleep(0.0001)
#         print(f"{self.name}: Done")
#
#
#     def get_snapshot(self):
#         with lock:
#             return self.snapshot[:]
#
#
# t1 = MyThread("T1")
# t2 = MyThread("T2")
#
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# t1_output = t1.get_snapshot()
# t2_output = t2.get_snapshot()
#
# print("Final counter:", counter)
# for t1_out, t2_out in zip(t1_output, t2_output):
#     print(t1_out, " : ", t2_out)




# Retrieve data from threads using
# Shared data + lock
# queue.Queue
# Thread Subclass



# Exception Management


# When thread consumes Exception and shares final result with main thread.

# import threading
# import logging
# import time
# import random
#
#
# N = 6
# done_events = [threading.Event() for _ in range(N)]  # Event objects. One for each thread
# status = {}  # Captures thread's final status.
# lock = threading.Lock()  # lock object while updating thread's final status
#
# logging.basicConfig(level=logging.INFO, format="%(threadName)s: %(message)s")  # logging object
#
# def worker(task_id, done_event, status_dict, lock):
#     try:
#         logging.info(f"start task={task_id}")
#         time.sleep(random.uniform(0.1, 0.4))
#
#         if task_id % 3 == 0:  # Codition to raise exception when thread ID is 0 and divisible by 3
#             raise RuntimeError(f"On {task_id}")
#
#         with lock:
#             status_dict[task_id] = "ok"
#         logging.info(f"done task={task_id}")
#     except Exception as exc:
#         logging.exception(f"worker failed task={task_id}: {exc}")
#         with lock:
#             status_dict[task_id] = f"Exception: {exc}"
#     finally:
#         done_event.set()  # Set an event indicating thread updated its final status.
#
#
# threads = []
# for i in range(N):
#     threads.append(
#         threading.Thread( target=worker, name=f"worker-{i}", args=(i, done_events[i], status, lock)))
#
#
# for t in threads:
#     t.start()
#
# # main thread waits for all to signal completion
# for ev in done_events:
#     ev.wait()
#
# for t in threads:
#     t.join()
#
# print("aggregate status:", status)  # contains per-task success/errors



# When thread passes Exception object to the main thread for handling

# import threading
# import logging
# import time
# import random
#
#
# N = 6
# done_events = [threading.Event() for _ in range(N)]  # Event objects. One for each thread
# status = {}  # Captures thread's final status.
# lock = threading.Lock()  # lock object while updating thread's final status
#
# logging.basicConfig(level=logging.INFO, format="%(threadName)s: %(message)s")  # logging object
#
# def worker(task_id, done_event, status_dict, lock):
#     try:
#         logging.info(f"start task={task_id}")
#         time.sleep(random.uniform(0.1, 0.4))
#
#         if task_id % 3 == 0:  # Codition to raise exception when thread ID is 0 and divisible by 3
#             raise RuntimeError(f"On {task_id}")
#
#         with lock:
#             status_dict[task_id] = "ok"
#         logging.info(f"done task={task_id}")
#     except Exception as exc:
#         logging.exception(f"worker failed task={task_id}: {exc}")
#         with lock:
#             # status_dict[task_id] = f"Exception: {exc}"
#             status_dict[task_id] = exc
#     finally:
#         done_event.set()  # Set an event indicating thread updated its final status.
#
#
# threads = []
# for i in range(N):
#     threads.append(
#         threading.Thread( target=worker, name=f"worker-{i}", args=(i, done_events[i], status, lock)))
#
#
# for t in threads:
#     t.start()
#
# # main thread waits for all to signal completion
# for ev in done_events:
#     ev.wait()
#
# for t in threads:
#     t.join()
#
# for key, value in status.items():
#     if isinstance(value, RuntimeError):
#         # main thread consumes or re-raises the error
#         print(f"Thread-{key}, raised Exception")
#     else:
#         print(f"Thread-{key}, value")




# ThreadPoolExecutor

# from concurrent.futures import ThreadPoolExecutor, as_completed
# import threading
# import time
#
# counter = 0
# lock = threading.Lock()  # shared lock
#
# def worker(name, increments=1000):
#     global counter
#     for _ in range(increments):
#         with lock:  # acquire/release around critical section
#             counter += 1
#         time.sleep(0.0001)
#     print(f"{name} done")
#     return name  # optional return for observability
#
# # use max_workers=3 to mimic the three threads
# with ThreadPoolExecutor(max_workers=3) as ex:
#     futures = [ex.submit(worker, "T1"), ex.submit(worker, "T2"), ex.submit(worker, "T3")]
#
#     # wait for completion and propagate any exceptions
#     for fut in as_completed(futures):
#         _ = fut.result()  # re-raises if worker failed
#
# print("Final counter:", counter)



# ThreadPoolExecutor - Few more details


# ThreadPoolExecutor - without context manager
# from concurrent.futures import ThreadPoolExecutor, as_completed
# import threading
# import time
#
# counter = 0
# lock = threading.Lock()  # shared lock
#
# def worker(name, increments=1000):
#     global counter
#     if name == "T4":
#         raise RuntimeError("T4 raised exception")
#     for _ in range(increments):
#         with lock:  # acquire/release around critical section
#             counter += 1
#         time.sleep(0.0001)
#     # print(f"{name} done")
#     return f"{name} done"  # optional return for observability
#
# # use max_workers=3 to mimic the three threads
# ex = ThreadPoolExecutor(max_workers=3)
# futures = [ex.submit(worker, "T1"), ex.submit(worker, "T2"),
#            ex.submit(worker, "T3"), ex.submit(worker, "T4")]
#
# ex.shutdown(wait=True)
#
# for fut in as_completed(futures):
#     if fut.exception():
#         print(f"Exception is {fut.exception()}")
#     else:
#         print(fut.result())  # re-raises if worker failed
#
# print("Final counter:", counter)




# ThreadPoolExecutor - without context manager and no suhtdown()


# from concurrent.futures import ThreadPoolExecutor, as_completed
# import threading
# import time
#
# counter = 0
# lock = threading.Lock()  # shared lock
#
# def worker(name, increments=1000):
#     global counter
#     if name == "T4":
#         raise RuntimeError("T4 raised exception")
#     for _ in range(increments):
#         with lock:  # acquire/release around critical section
#             counter += 1
#         time.sleep(0.0001)
#     # print(f"{name} done")
#     return f"{name} done"  # optional return for observability
#
# # use max_workers=3 to mimic the three threads
# ex = ThreadPoolExecutor(max_workers=3)
# futures = [ex.submit(worker, "T1"), ex.submit(worker, "T2"),
#            ex.submit(worker, "T3"), ex.submit(worker, "T4")]
#
# # ex.shutdown(wait=True)
#
# for fut in as_completed(futures):
#     if fut.exception():
#         print(f"Exception is {fut.exception()}")
#     else:
#         print(fut.result())  # re-raises if worker failed
#
# print("Final counter:", counter)



# Interview Question#1
# Implement a thread safe Least Recently Used (LRU) cache. Should be accessible by multiple threads
# Support get(), put() and proper eviction.



# import random
# import time
# import threading
#
# from typing import Any
# from collections import OrderedDict
# from concurrent.futures import ThreadPoolExecutor
#
# class ThreadSafeLRUCache:
#
#     def __init__(self, capacity: int):
#         self.cache = OrderedDict()      # Data structure to store data
#         self.capacity = capacity        # Capacity of the data structure
#         self.lock = threading.Lock()    # lock object to make cache access is thread safe
#         self.hits = 0                   # for stats - number of hits. Key found in DS
#         self.misses = 0                 # for stats - number of misses. Key not found in DS
#         self.puts = 0                   # for stats - counts total no of elements added in cache
#
#     def get(self, key: str) -> Any:
#         with self.lock:
#             if key not in self.cache:
#                 self.misses += 1
#                 return None
#
#             self.cache.move_to_end(key)  # Move to end (most recently used)
#             self.hits += 1
#             return self.cache[key]
#
#     def put(self, key: str, value: Any):
#         with self.lock:
#             if key in self.cache:
#                 self.cache.move_to_end(key)  # Update existing key (most recently used)
#             else:
#                 if len(self.cache) >= self.capacity:
#                     lru_key, _ = self.cache.popitem(last=False)  # Evict LRU (first item)
#                     print(f"    Evicted LRU key: {lru_key}")
#
#             self.cache[key] = value
#             self.puts += 1
#
#     def get_stats(self) -> dict:
#         with self.lock:
#             return {
#                 "size": len(self.cache),
#                 "capacity": self.capacity,
#                 "hits": self.hits,
#                 "misses": self.misses,
#                 "hit_rate": self.hits / (self.hits + self.misses) if (self.hits + self.misses) > 0 else 0,
#                 "puts": self.puts
#             }
#
#
#
# cache = ThreadSafeLRUCache(capacity=5)
#
#
# def worker(worker_id: int):
#     for i in range(10):
#         key = f"key{random.randint(0, 7)}"
#
#         if random.random() < 0.5: # 50-50 chance of read and write
#             value = cache.get(key)  # read value from the cache
#             if value:
#                 print(f"  Worker {worker_id}: Cache HIT for {key}")
#             else:
#                 print(f"  Worker {worker_id}: Cache MISS for {key}")
#         else:  # write value to the cache
#             cache.put(key, f"value-{worker_id}-{i}")
#             print(f"  Worker {worker_id}: Put {key}")
#
#         time.sleep(0.01)
#
#
#
# def test_question_1():
#     print("\n🔹 5 workers accessing cache concurrently:\n")
#     N = 5
#
#     with ThreadPoolExecutor(max_workers=N) as executor:
#         for i in range(N):
#             executor.submit(worker, i)
#
# test_question_1()
#
# stats = cache.get_stats()
# print(f"\n📊 Cache Statistics:")
# print(f"   Size: {stats['size']}/{stats['capacity']}")
# print(f"   Hits: {stats['hits']}")
# print(f"   Misses: {stats['misses']}")
# print(f"   Hit Rate: {stats['hit_rate']:.2%}")
# print(f"   Total puts: {stats['puts']}")




# Interview Question#2
# Implement parallel merge sort. Use threads to sort large arrays. Decide on the threshold when use
# regular merge sort.


import random
import time
from concurrent.futures import ThreadPoolExecutor
from typing import List

def merge(left: List[int], right: List[int]) -> List[int]:
    result = []
    i, j = 0, 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_sequential(arr: List[int]) -> List[int]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort_sequential(arr[:mid])
    right = merge_sort_sequential(arr[mid:])
    return merge(left, right)


def merge_sort_parallel(arr: List[int], threshold: int = 10000) -> List[int]:
    if len(arr) <= threshold:
        return merge_sort_sequential(arr)

    mid = len(arr) // 2

    future_left = executor.submit(merge_sort_parallel, arr[:mid], threshold)
    future_right = executor.submit(merge_sort_parallel, arr[mid:], threshold)

    left = future_left.result()
    right = future_right.result()

    return merge(left, right)


# Generate test data
size = 1_00_00_00
arr = [random.randint(1, 1_00_00_00) for _ in range(size)]

print(f"\n🔹 Sorting array of {size} elements:\n")

# Sequential
print("Sequential merge sort:")
arr_copy = arr.copy()
start = time.time()
sorted_seq = merge_sort_sequential(arr_copy)
seq_time = time.time() - start
print(f"  ⏱️  Time: {seq_time:.2f}s")

# Parallel
executor = ThreadPoolExecutor(max_workers=30)
print("\nParallel merge sort:")
arr_copy = arr.copy()
start = time.time()
sorted_par = merge_sort_parallel(arr_copy, threshold=5_00_00)
# executor.shutdown(wait=True)
par_time = time.time() - start
print(f"  ⏱️  Time: {par_time:.2f}s")
# Verify correctness
print(f"\n✅ Results match: {sorted_seq == sorted_par}")
print(f"✅ Speedup: {seq_time / par_time:.2f}x")










