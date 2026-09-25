import sys
sys.path.insert(0, '/home/longhn0710/workspace/OmniRoute-py')

from app.core.priority_queue import PriorityQueue, Task
from app.core.task_router import TaskRouter, TaskStatus, Agent, AgentStatus
from app.core.agent_pool import AgentPool


def test_priority_queue():
    pq = PriorityQueue()
    
    critical_task = Task(priority=1, task_id=1, data="critical")
    low_task = Task(priority=10, task_id=2, data="low")
    
    pq.push(critical_task, 1)
    pq.push(low_task, 10)
    
    first = pq.pop()
    assert first.priority == 1, f"Expected priority 1, got {first.priority}"
    
    second = pq.pop()
    assert second.priority == 10, f"Expected priority 10, got {second.priority}"
    
    print("✓ Priority queue test passed: CRITICAL (1) comes before LOW (10)")


def test_task_router_requeue():
    router = TaskRouter()
    task = Task(priority=5, task_id=1, data="test")
    task.status = TaskStatus.PENDING
    
    result = router.route_task(task)
    assert result == False
    
    queued_task = router._queue.pop()
    assert queued_task is not None
    assert queued_task.priority == 5
    
    print("✓ Task router re-queue test passed")


def test_task_router_race_condition():
    router = TaskRouter()
    agent = Agent("agent-1")
    router.register_agent(agent)
    
    task = Task(priority=5, task_id=1, data="test")
    task.status = TaskStatus.PENDING
    
    result = router.route_task(task)
    assert result == True
    
    assert task.status == TaskStatus.IN_PROGRESS
    assert agent.current_task == task
    assert agent.status == AgentStatus.BUSY
    
    print("✓ Task router race condition test passed")


def test_agent_pool_double_assignment():
    pool = AgentPool()
    
    agent1 = Agent("agent-1")
    agent2 = Agent("agent-2")
    pool.add_agent(agent1)
    pool.add_agent(agent2)
    
    idle_agent = pool.get_idle_agent()
    assert idle_agent is not None
    assert idle_agent.status == AgentStatus.BUSY
    
    idle_agent2 = pool.get_idle_agent()
    assert idle_agent2 is not None
    assert idle_agent2 != idle_agent
    assert idle_agent2.status == AgentStatus.BUSY
    
    idle_agent3 = pool.get_idle_agent()
    assert idle_agent3 is None
    
    print("✓ Agent pool double assignment test passed")


def test_agent_pool_no_current_task_attribute():
    pool = AgentPool()
    agent = Agent("agent-1")
    pool.add_agent(agent)
    
    idle_agent = pool.get_idle_agent()
    assert idle_agent is not None
    
    pool.release_agent("agent-1")
    
    assert agent.status == AgentStatus.IDLE
    assert agent.current_task is None
    
    print("✓ Agent pool current_task attribute test passed")


if __name__ == "__main__":
    test_priority_queue()
    test_task_router_requeue()
    test_task_router_race_condition()
    test_agent_pool_double_assignment()
    test_agent_pool_no_current_task_attribute()
    print("\n✓ All tests passed!")