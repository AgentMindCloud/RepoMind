"""Entry point for GitHub Actions and local runs."""
import os
import sys
import argparse
from core.github_client import GitHubClient
from core.llm import LLMClient
from core.orchestrator import Orchestrator
from core.models import Task

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

        print(f"RepoMind runner ready. Registered agents: {list(orch.agents.keys())}")

        if args.issue:
            task = github.get_task(args.issue) if hasattr(github, "get_task") else Task(
                issue_number=args.issue, title=f"Issue #{args.issue}", body="", labels=["task"]
            )
            print(f"Processing issue #{task.issue_number}: {task.title}")
            result = orch.run_task_sync(task)
            print("Result:", result.summary)
        else:
            tasks = github.get_open_tasks(labels=["task", "agent", "critic", "crypto", "x-growth"])
            print(f"Found {len(tasks)} candidate tasks")
            for t in tasks[:5]:  # safety limit
                print(f"→ #{t.issue_number} {t.title}")
                result = orch.run_task_sync(t)
                print("  ", result.summary)
    except Exception as e:
        print(f"Runner error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
