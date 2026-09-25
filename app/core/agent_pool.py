from threading import Lock
from typing import Optional
from app.core.task_router import Agent, AgentStatus


class AgentPool:
    def __init__(self):
        self._agents: dict[str, Agent] = {}
        self._lock = Lock()

    def add_agent(self, agent: Agent) -> None:
        with self._lock:
            self._agents[agent.agent_id] = agent

    def remove_agent(self, agent_id: str) -> Optional[Agent]:
        with self._lock:
            return self._agents.pop(agent_id, None)

    def get_idle_agent(self) -> Optional[Agent]:
        with self._lock:
            for agent in self._agents.values():
                if agent.status == AgentStatus.IDLE:
                    agent.status = AgentStatus.BUSY
                    return agent
        return None

    def release_agent(self, agent_id: str) -> bool:
        with self._lock:
            agent = self._agents.get(agent_id)
            if agent:
                agent.status = AgentStatus.IDLE
                agent.current_task = None
                return True
            return False

    def get_agent(self, agent_id: str) -> Optional[Agent]:
        with self._lock:
            return self._agents.get(agent_id)

    def list_agents(self) -> list[Agent]:
        with self._lock:
            return list(self._agents.values())