# Introduction to async-io
import time

# def synchronous_task(task_id: int) -> str:
#     time.sleep(2)  # Blocking sleep - freezes entire program!
#     return f"Task {task_id} completed"
#
# def demo_synchronous():
#     start = time.time()
#     results = []
#     for i in range(3):
#         result = synchronous_task(i)
#         results.append(result)
#         print(f"  {result}")
#
#     elapsed = time.time() - start
#     print(f"⏱️  Total time: {elapsed:.2f}s")
#     print("❌ Problem: Each task blocked the next one!\n")
#
# demo_synchronous()


# import asyncio
#
# async def asynchronous_task(task_id: int) -> str:
#     await asyncio.sleep(2)  # Non-blocking - allows other tasks to run!
#     return f"Task {task_id} completed"
#
# async def demo_asynchronous():
#     start = time.time()
#     tasks = [asynchronous_task(i) for i in range(3)]
#     results = await asyncio.gather(*tasks)
#     for result in results:
#         print(f"  {result}")
#     elapsed = time.time() - start
#     print(f"⏱️  Total time: {elapsed:.2f}s")
#     print("✅ Success: All tasks ran concurrently!\n")
#
# asyncio.run(demo_asynchronous())


# asyncio module

import asyncio

# async def greet():
#     print("Hello...")
#     await asyncio.sleep(2)  # non-blocking sleep
#     print("...world!")
#
# asyncio.run(greet())


# async def greet(name):
#     print(f"Starting greeting for {name}")
#     await asyncio.sleep(2)
#     print(f"Hello, {name}!")
#
# async def main():
#     start = time.time()
#     await asyncio.gather(greet("Alice"), greet("Bob"), greet("Charlie"))
#     elapsed = time.time() - start
#     print(f"⏱️  Total time: {elapsed:.2f}s")
# asyncio.run(main())


# import asyncio


# async def download(url):
#     print(f"Downloading from {url}")
#     await asyncio.sleep(2)
#     print(f"Finished downloading from {url}")
#
# async def main():
#     task1 = asyncio.create_task(download("site1.com"))
#     task2 = asyncio.create_task(download("site2.com"))
#
#     print("Tasks started!")
#     await task1
#     await task2
#
# asyncio.run(main())


# Event loop


# async def download(url):
#     print(f"Downloading from {url}")
#     await asyncio.sleep(2)
#     print(f"Finished downloading from {url}")
#
# async def main():
#     # task1 = asyncio.create_task(download("site1.com"))
#     # task2 = asyncio.create_task(download("site2.com"))
#
#     print("Tasks started!")
#     await download("site1")
#     await download("site2")
#     print("Tasks Finsihed!")
#
# asyncio.run(main())
# print("EVent loop is over.")


# asyncio.wait_for - example

# async def fetch_user(user_id: int) -> dict:
#     await asyncio.sleep(2.5)
#     return {"id": user_id, "name": "Ada"}
#
#
# async def main():
#     try:
#         user = await asyncio.wait_for(fetch_user(1), timeout=1.0)
#         print("Got:", user)
#     except asyncio.TimeoutError:
#         print("fetch_user timed out and was cancelled")
#
#
# asyncio.run(main())


# Synchronization in Async code
# Race Condition example
# counter = 0  # Shared resource
# lock = asyncio.Lock()
#
# async def increment(name):
#     global counter
#     for _ in range(100):
#         async with lock:
#             temp = counter
#             await asyncio.sleep(0.001)  # Simulate I/O or delay
#             counter = temp + 1
#     print(f"{name} done")
#
# async def main():
#     await asyncio.gather(increment("Task1"), increment("Task2"))
#     print(f"Final counter value: {counter}")
#
# asyncio.run(main())

# Semaphore example
# async def download_file(file):
#     print(f"Downloading {file}...")
#     await asyncio.sleep(2)
#     print(f"{file} downloaded")
#
#
# async def main():
#     await asyncio.gather(download_file("file_1"), download_file("file_2"), download_file("file_3"),
#                          download_file("file_4"), download_file("file_5"))
#
# asyncio.run(main())


# sem = asyncio.Semaphore(3)
#
#
# async def download_file(file):
#     async with sem:
#         print(f"Downloading {file}...")
#         await asyncio.sleep(2)
#         print(f"{file} downloaded")
#
#
# async def main():
#     await asyncio.gather(download_file("file_1"), download_file("file_2"), download_file("file_3"),
#                          download_file("file_4"), download_file("file_5"))
#
#
# asyncio.run(main())


# asyncio - Queue
"""
await queue.put(item)	    Add an item to the queue (wait if full).
await queue.get()	        Remove and return an item (wait if empty).
queue.task_done()	        Signal that the fetched item is processed.
await queue.join()	        Wait until all items are processed.
queue.qsize()	            Return current size of queue.
queue.empty()/queue.full()	Check if queue is empty/full.

"""

# import random
#
# async def producer(queue):
#     for i in range(10):
#         item = f"Task-{i}"
#         await asyncio.sleep(random.uniform(0.1, 0.5))
#         await queue.put(item)
#         print(f"🧑‍🍳 Produced {item}")
#
#
# async def consumer(queue, name):
#     while True:
#         item = await queue.get()
#         print(f"🍽️  {name} - Consumed {item}")
#         await asyncio.sleep(random.uniform(0.2, 0.6))
#         queue.task_done()
#
#
# async def main():
#     queue = asyncio.Queue()
#
#     # Start one producer and one consumer
#     producer_task = asyncio.create_task(producer(queue))
#     consumer_task = asyncio.create_task(consumer(queue, "Q1"))
#     consumer_task1 = asyncio.create_task(consumer(queue,"Q2"))
#
#
#
#     await producer_task
#     await queue.join()  # Wait for all items to be processed
#     consumer_task.cancel()
#     consumer_task1.cancel()
#
#
# asyncio.run(main())


# asyncio.event
"""
set()	    Sets the internal flag to True and wakes up all waiting tasks.
clear()	    Resets the flag to False. Tasks that call wait() will block again.
is_set()	Returns True if the flag is currently set, else False.
wait()	    Coroutine that blocks until the flag is set. Returns immediately if already set.
"""

# async def waiter(event, name):
#     print(f" {name} - Waiting for event to be set...")
#     await event.wait()  # wait until someone sets the event
#     print(f" {name} - Event is set! Proceeding...")
#
#
# async def setter(event):
#     print("Setter started. Doing some work...")
#     await asyncio.sleep(3)
#     print("Setting the event now!")
#     event.set()
#
#
# async def main():
#     event = asyncio.Event()
#
#     # Two tasks waiting for the event
#     w1 = asyncio.create_task(waiter(event, "W1"))
#     w2 = asyncio.create_task(waiter(event, "W2"))
#
#     # One task that will set the event
#     s = asyncio.create_task(setter(event))
#
#     await asyncio.gather(w1, w2, s)
#
#
# asyncio.run(main())
#


# Interview Questions

"""
Build a webcrawler that visits URL(s) concurrently. Max N at a time.
You have to ensure that you do not visit the same URL twice.
Ensure that you do not go beyond a certain depth.
Extract data and pages from each URL.
"""

# import asyncio
# from typing import List
# import random
# import time
#
#
# class AsyncWebCrawler:
#     def __init__(self, max_concurrent: int = 10, max_depth: int = 3):
#         self.max_concurrent = max_concurrent    # Cuncurrency level
#         self.max_depth = max_depth              # Depth
#         self.visited = set()                    # URLs visited
#         self.semaphore = asyncio.Semaphore(max_concurrent)
#         self.results = []                       # URLs processed
#
#
#     async def fetch_page(self, url: str) -> List[str]:
#         wait_prd = random.uniform(.3, 2)
#         print(f"{url} - await asyncio.sleep({wait_prd})")  # Info - Sleep time of each URL
#         await asyncio.sleep(wait_prd)  # Simulates page fetch
#         num_links = random.randint(2, 5)  # Simulate finding 2-5 links
#         links = [f"{url}/page{i}" for i in range(num_links)]
#         return links
#
#
#     async def crawl_url(self, url: str, depth: int):
#         if depth > self.max_depth:
#             return
#         if url in self.visited:
#             return
#
#         self.visited.add(url)
#         print(f"  {'  ' * depth}🕷️  Crawling: {url} (depth: {depth})")
#
#         try:
#             tasks = []
#             # ✅ Semaphore ONLY around fetch - release immediately
#             async with self.semaphore:
#                 links = await asyncio.wait_for(self.fetch_page(url), timeout=1.5)
#
#             self.results.append({"url": url, "depth": depth, "links_found": len(links)})
#
#             # Spawn children (parent no longer holds semaphore)
#             if depth < self.max_depth:
#                 for link in links:
#                     if link not in self.visited:
#                         tasks.append(self.crawl_url(link, depth + 1))
#             if tasks:
#                 print(f"Queuing {len(tasks)} more tasks")
#                 await asyncio.gather(*tasks, return_exceptions=True)
#
#         except asyncio.TimeoutError:
#             print(f"  {'  ' * depth}⚠️  Timeout: {url}")
#         except Exception as e:
#             print(f"  {'  ' * depth}❌ Error crawling {url}: {e}")
#
#     async def crawl(self, start_url: str):
#         await self.crawl_url(start_url, depth=0)
#
#
# async def crawl_sites():
#     crawler = AsyncWebCrawler(max_concurrent=5, max_depth=2)
#
#     start_url = "https://example.com"
#     print(f"Starting crawl from: {start_url}\n")
#
#     start = time.time()
#     await crawler.crawl(start_url)
#     elapsed = time.time() - start
#
#     print(f"\n✅ Crawl completed in {elapsed:.2f}s")
#     print(f"   Pages visited: {len(crawler.visited)}")
#     print(f"   Pages processed: {len(crawler.results)}")
#     for result in crawler.results:
#         print(result)
#
#
# asyncio.run(crawl_sites())



# Interview Question - 2
"""
Design and implement an async circuit breaker pattern in Python that protects against 
cascading failures when calling unreliable external services. 
Your solution should prevent repeated calls to failing services, 
allow automatic recovery testing, and handle concurrent requests safely.
"""
import random

class CircuitBreakerState:
    CLOSED = "CLOSED"  # Normal operation
    OPEN = "OPEN"  # Failing, reject requests
    HALF_OPEN = "HALF_OPEN"  # Testing if service recovered


class AsyncCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 10.0,
                 half_open_max_calls: int = 3):
        # count of calls that can fail before circuit breaker opens
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout        # min time required for self recovery
        self.half_open_max_calls = half_open_max_calls  # max calls that can go when circuit is half open

        self.state = CircuitBreakerState.CLOSED         # initial state
        self.failure_count = 0                          # count of failed calls
        self.success_count = 0                          # count of successful calls
        self.last_failure_time = None                   # time when last call failed. Used during recovery
        self.half_open_calls = 0                        # counts calls when circuit is half open

        self.lock = asyncio.Lock()                      # lock object for concurrency

    async def call(self, func, *args, **kwargs):
        async with self.lock:
            if (self.state == CircuitBreakerState.OPEN
                    and self.last_failure_time
                    and time.time() - self.last_failure_time >= self.recovery_timeout):
                self.state = CircuitBreakerState.HALF_OPEN
                self.half_open_calls = 0
                print("  🔄 Circuit breaker: OPEN -> HALF_OPEN (testing recovery)")

            # Reject if circuit is OPEN
            if self.state == CircuitBreakerState.OPEN:
                raise Exception("Circuit breaker is OPEN - request rejected")

            # Limit calls in HALF_OPEN state
            if self.state == CircuitBreakerState.HALF_OPEN:
                if self.half_open_calls >= self.half_open_max_calls:
                    raise Exception("Circuit breaker HALF_OPEN - max test calls reached")
                self.half_open_calls += 1

        try:
            result = await func(*args, **kwargs)

            # Success - update state
            async with self.lock:
                self.success_count += 1

                if self.state == CircuitBreakerState.HALF_OPEN:
                    # Successful test call
                    if self.half_open_calls >= self.half_open_max_calls:
                        # All test calls succeeded - close circuit
                        self.state = CircuitBreakerState.CLOSED
                        self.failure_count = 0
                        print("  ✅ Circuit breaker: HALF_OPEN -> CLOSED (recovered!)")

            return result

        except Exception as e:
            async with self.lock:
                self.failure_count += 1
                self.last_failure_time = time.time()

                if self.state == CircuitBreakerState.HALF_OPEN:
                    self.state = CircuitBreakerState.OPEN
                    print("  ❌ Circuit breaker: HALF_OPEN -> OPEN (still failing)")

                elif self.failure_count >= self.failure_threshold:
                    self.state = CircuitBreakerState.OPEN
                    print(f"  🚨 Circuit breaker: CLOSED -> OPEN ({self.failure_count} failures)")

            raise



async def flaky_service(fail_probability: float = 0.5):
    await asyncio.sleep(0.1)
    if random.random() < fail_probability:
        raise Exception("Service failure")
    return "Success"


async def test_circuit_breaker():
    breaker = AsyncCircuitBreaker(failure_threshold=3, recovery_timeout=2.0, half_open_max_calls=2)

    print("Calling flaky service (70% failure rate)...\n")

    print("Phase 1: Triggering failures...")
    for i in range(10):
        try:
            result = await breaker.call(flaky_service, fail_probability=0.5)
            print(f"  ✅ Call {i}: {result}")
        except Exception as e:
            print(f"  ❌ Call {i}: {e}")

        await asyncio.sleep(0.2)

    # Phase 2: Wait for recovery timeout
    print("\n⏳ Waiting for recovery timeout (2 seconds)...")
    await asyncio.sleep(3)

    # Phase 3: Test recovery (HALF_OPEN state)
    print("\nPhase 2: Testing recovery (service improved to 20% failure)...")
    for i in range(5):
        try:
            result = await breaker.call(flaky_service, fail_probability=0.2)
            print(f"  ✅ Call {i}: {result}")
        except Exception as e:
            print(f"  ❌ Call {i}: {e}")

        await asyncio.sleep(0.2)

    print(f"\n📊 Final state: {breaker.state}")
    print(f"   Successes: {breaker.success_count}")
    print(f"   Failures: {breaker.failure_count}")

asyncio.run(test_circuit_breaker())














