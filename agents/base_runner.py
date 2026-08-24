"""Entry point for GitHub Actions and local runs."""
import os
import sys
import argparse
from core.github_client import GitHubClient
from core.llm import LLMClient
from core.orchestrator import Orchestrator
from core.models import Task

def self_check(github, llm, orch) -> list:
    """Lightweight startup diagnostics."""
    notes = []
    notes.append(f"Registered agents: {list(orch.agents.keys())}")
    notes.append(f"XAI_API_KEY set: {bool(os.getenv('XAI_API_KEY'))}")
    notes.append(f"GITHUB_TOKEN set: {bool(os.getenv('GITHUB_TOKEN'))}")
    notes.append(f"Repo: {getattr(github, 'repo_name', 'unknown')}")
    try:
        # cheap call
        _ = github.repo.name
        notes.append("GitHub API: ok")
    except Exception as e:
        notes.append(f"GitHub API: error ({e})")
    return notes

def main():
    parser = argparse.ArgumentParser(description="RepoMind base runner")
    parser.add_argument("--issue", type=int, help="Issue number to process")
    parser.add_argument("--repo", type=str, default=os.getenv("GITHUB_REPOSITORY", "AgentMindCloud/RepoMind"))
    args = parser.parse_args()

    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN not set – cannot proceed")
        sys.exit(1)

    try:
        github = GitHubClient(token=token, repo_full_name=args.repo)
        llm = LLMClient()
        orch = Orchestrator(github=github, llm=llm)

        for line in self_check(github, llm, orch):
            print(f"[self-check] {line}")

        if args.issue:
            task = github.get_task(args.issue)
            print(f"Processing issue #{task.issue_number}: {task.title} | labels={task.labels}")
            result = orch.run_task_sync(task)
            print("Result:", result.summary)
        else:
            # Also respect ISSUE_NUMBER from Actions env
            env_issue = os.getenv("ISSUE_NUMBER")
            if env_issue and str(env_issue).isdigit():
                task = github.get_task(int(env_issue))
                print(f"Processing issue #{task.issue_number}: {task.title} | labels={task.labels}")
                result = orch.run_task_sync(task)
                print("Result:", result.summary)
            else:
                labels = ["task", "agent", "critic", "crypto", "x-growth", "self-improve", "research"]
                tasks = github.get_open_tasks(labels=labels)
                print(f"Found {len(tasks)} candidate tasks")
                for t in tasks[:5]:
                    print(f"→ #{t.issue_number} {t.title}")
                    result = orch.run_task_sync(t)
                    print("  ", result.summary)
    except Exception as e:
        print(f"Runner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
