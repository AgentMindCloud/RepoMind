"""Basic tests for Orchestrator routing."""
from core.models import Task
from core.orchestrator import Orchestrator

def test_route_crypto():
    orch = Orchestrator.__new__(Orchestrator)  # skip full init
    orch.agents = {}
    task = Task(issue_number=1, title="Scan BTC", body="", labels=["crypto", "ta"])
    assert orch.route_task(task) == "crypto"

def test_route_x_growth():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    task = Task(issue_number=2, title="Thread", body="", labels=["x-growth"])
    assert orch.route_task(task) == "x_growth"

def test_route_self_improve():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    task = Task(issue_number=3, title="Improve", body="", labels=["self-improve"])
    assert orch.route_task(task) == "self_improve"

def test_route_default_critic():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    task = Task(issue_number=4, title="Generic", body="", labels=["task"])
    assert orch.route_task(task) == "critic"
