from abc import ABC, abstractmethod
from typing import Optional
from .models import AgentRole, Task, ActionResult

class BaseAgent(ABC):
    def __init__(self, role: AgentRole, github=None, skills=None, memory=None, llm=None):
        self.role = role
        self.github = github
        self.skills = skills
        self.memory = memory
        self.llm = llm
        self.iteration = 0

    @abstractmethod
    async def perceive(self, task: Task) -> dict:
        """Read task + memory + context."""
        pass

    @abstractmethod
    async def plan(self, perception: dict) -> list:
        """Decide next actions."""
        pass

    @abstractmethod
    async def act(self, plan: list, task: Task) -> ActionResult:
        """Execute plan (call skills, write files, open PR, comment)."""
        pass

    async def reflect(self, result: ActionResult) -> None:
        """Optional: write lessons to memory."""
        pass

    async def run(self, task: Task) -> ActionResult:
        self.iteration = 0
        perception = await self.perceive(task)
        while self.iteration < self.role.max_iterations:
            self.iteration += 1
            plan = await self.plan(perception)
            result = await self.act(plan, task)
            await self.reflect(result)
            if result.success:
                return result
            perception["last_result"] = result.model_dump()
        return ActionResult(success=False, summary="Max iterations reached")
