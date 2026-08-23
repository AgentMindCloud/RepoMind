"""Basic tests for core models."""
from core.models import Task, ActionResult, AgentRole, SkillContract, SafetyLevel

def test_task_creation():
    t = Task(issue_number=1, title="Test", body="Body", labels=["task"])
    assert t.issue_number == 1
    assert "task" in t.labels

def test_action_result():
    r = ActionResult(success=True, summary="ok")
    assert r.success is True

def test_agent_role():
    role = AgentRole(name="critic", system_prompt="Review everything")
    assert role.max_iterations == 5 or role.max_iterations > 0

if __name__ == "__main__":
    test_task_creation()
    test_action_result()
    test_agent_role()
    print("Basic model tests passed")
