import heapq
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass(order=True)
class Task:
    priority: int
    task_id: int = field(compare=False)
    data: Any = field(compare=False)


class PriorityQueue:
    def __init__(self):
        self._heap: list = []
        self._counter = 0

    def push(self, task: Task, priority: int) -> None:
        self._counter += 1
        heapq.heappush(self._heap, (priority, self._counter, task))

    def pop(self) -> Optional[Task]:
        if not self._heap:
            return None
        _, _, task = heapq.heappop(self._heap)
        return task

    def peek(self) -> Optional[Task]:
        if not self._heap:
            return None
        return self._heap[0][2]

    def __len__(self) -> int:
        return len(self._heap)

    def __bool__(self) -> bool:
        return bool(self._heap)