# Starter skeleton for Homework 3 — a toy Half-Sync/Half-Async task processor.
#
# The idea: an async layer accepts work without blocking (e.g., "receiving"
# tasks), hands them off through a queue, and a sync layer of worker
# threads processes them one at a time with simple, sequential logic. Swap
# this for Leader/Followers or Active Object if you'd rather implement one
# of those instead — the important part is demonstrating the hand-off
# structure, not this exact pattern.

import queue
import threading
import time


class TaskQueue:
    """The boundary between the async and sync layers."""

    def __init__(self):
        self._q: "queue.Queue[tuple]" = queue.Queue()

    def submit(self, task_id: str, payload: dict) -> None:
        # TODO: this is the async-layer entry point — it must return
        # immediately, never block on the task actually being processed.
        self._q.put((task_id, payload))

    def take(self, timeout=None):
        return self._q.get(timeout=timeout)


class SyncWorker(threading.Thread):
    """The sync layer: simple, sequential processing logic per task."""

    def __init__(self, task_queue: TaskQueue, worker_id: int):
        super().__init__(daemon=True)
        self.task_queue = task_queue
        self.worker_id = worker_id
        self._running = True

    def run(self):
        while self._running:
            try:
                task_id, payload = self.task_queue.take(timeout=0.5)
            except queue.Empty:
                continue
            # TODO: real processing logic goes here — keep it synchronous
            # and simple; this is the whole point of the "half-sync" side.
            print(f"worker {self.worker_id} processing {task_id}: {payload}")

    def stop(self):
        self._running = False


if __name__ == "__main__":
    tq = TaskQueue()
    workers = [SyncWorker(tq, i) for i in range(3)]
    for w in workers:
        w.start()

    # TODO: simulate a bursty async producer submitting tasks faster than
    # workers can drain them, and observe/measure queue behavior. Then try
    # documenting what changes if you swap this for Leader/Followers
    # (one thread waits on new work at a time, promoting a follower on
    # each event) instead of a fixed worker pool draining a shared queue.
    for i in range(10):
        tq.submit(f"task-{i}", {"n": i})
        time.sleep(0.05)

    time.sleep(2)
    for w in workers:
        w.stop()
