"""Routing tests for the orchestrator."""
from core.models import Task
from core.orchestrator import Orchestrator

def _task(labels):
    return Task(
        issue_number=1,
        title="Test",
        body="",
        labels=labels,
        state="open",
        html_url="https://example.com"
    )

def test_route_crypto():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    assert orch.route_task(_task(["crypto"])) == "crypto"
    assert orch.route_task(_task(["ta"])) == "crypto"

def test_route_x_growth():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    assert orch.route_task(_task(["x-growth"])) == "x_growth"

def test_route_self_improve():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    assert orch.route_task(_task(["self-improve"])) == "self_improve"

def test_route_research():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    assert orch.route_task(_task(["research"])) == "researcher"

def test_route_default_critic():
    orch = Orchestrator.__new__(Orchestrator)
    orch.agents = {}
    assert orch.route_task(_task(["task"])) == "critic"
    assert orch.route_task(_task([])) == "critic"
