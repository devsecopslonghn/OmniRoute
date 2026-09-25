from enum import Enum
from typing import Optional
from app.core.priority_queue import PriorityQueue, Task


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    OFFLINE = "offline"


class Agent:
    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.status = AgentStatus.IDLE
        self.current_task: Optional[Task] = None

    def assign_task(self, task: Task) -> None:
        self.current_task = task
        self.status = AgentStatus.BUSY


class TaskRouter:
    def __init__(self):
        self._queue = PriorityQueue()
        self._agents: dict[str, Agent] = {}

    def register_agent(self, agent: Agent) -> None:
        self._agents[agent.agent_id] = agent

    def route_task(self, task: Task) -> bool:
        agent = self._find_available_agent()
        if agent is None:
            self._queue.push(task, task.priority)
            return False

        task.status = TaskStatus.IN_PROGRESS
        agent.assign_task(task)
        return True

    def _find_available_agent(self) -> Optional[Agent]:
        for agent in self._agents.values():
            if agent.status == AgentStatus.IDLE:
                return agent
        return None

    def requeue_task(self, task: Task) -> None:
        self._queue.push(task, task.priority)