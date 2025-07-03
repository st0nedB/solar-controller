from dataclasses import dataclass
from datetime import time
from typing import Callable, List

@dataclass(order=True)
class TimeSlot:
    start: time
    end: time
    action: Callable[[], None]  # Action is a function to be called

    def overlaps(self, other: "TimeSlot") -> bool:
        return not (self.end <= other.start or self.start >= other.end)


class Schedule:
    def __init__(self):
        self.slots: List[TimeSlot] = []

    def add_slot(self, slot: TimeSlot):
        for existing in self.slots:
            if slot.overlaps(existing):
                raise ValueError("TimeSlot overlaps with existing slot")
        self.slots.append(slot)
        self.slots.sort()  # Keeps slots in time order

    def run(self, current_time: time):
        for slot in self.slots:
            if slot.start <= current_time < slot.end:
                slot.action()
                break  # Assume only one action per time
