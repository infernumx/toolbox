#!/usr/bin/env python3

from __future__ import annotations
from threading import Thread, Event
from typing import Any
import random
import time


class TimedVariable:
    def __init__(self, var: Any = None, *, time_period: int, expected_value: Any):
        self.var: Any = var
        self.time_period: int = time_period
        self.expected_value: Any = expected_value
        self.stop_event: Event = Event()
        self.fire_event: Event = Event()
        self.running_event: Event = Event()

    def timer(self) -> None:
        # 'Fallback' thread to ensure the stop event is set after the maximum time
        time.sleep(self.time_period)
        self.stop_event.set()

    def worker(self) -> None:
        # Worker thread to continuously check the variable and set the fire event if the value is correct
        while not self.stop_event.is_set():
            if self.var == self.expected_value:
                self.fire_event.set()
                self.stop_event.set()
                self.running_event.clear()
                break

    def set_value(self, var: Any) -> None:
        self.var = var

    def should_stop(self) -> bool:
        return self.stop_event.is_set()

    def should_fire(self) -> bool:
        return self.fire_event.is_set()

    def start(self) -> TimedVariable:
        if self.running_event.is_set():
            raise RuntimeError("Already running")

        worker_thread: Thread = Thread(
            target=self.worker,
            daemon=True,
        )
        timer_thread: Thread = Thread(target=self.timer, daemon=True)

        worker_thread.start()
        timer_thread.start()

        self.running_event.set()

        return self

    def reset(self) -> None:
        self.stop_event.clear()
        self.fire_event.clear()
        self.running_event.clear()

    def __enter__(self) -> TimedVariable:
        return self.start()

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.reset()


if __name__ == "__main__":
    with TimedVariable(time_period=1, expected_value=3) as timed_var:
        while not timed_var.should_stop():
            timed_var.set_value(random.randint(0, 10))
            print(f"Value: {timed_var.var}")
            time.sleep(0.1)

        if timed_var.should_fire():
            print("Fire event is set")
        else:
            print("Fire event is not set")
