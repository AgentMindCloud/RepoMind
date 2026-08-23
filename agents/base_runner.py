"""Entry point for GitHub Actions / local runs."""
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
        print("GITHUB_TOKEN not set")
        sys.exit(1)

    github = GitHubClient(token=token, repo_full_name=args.repo)
    llm = LLMClient()
    orch = Orchestrator(github=github, llm=llm)

    if args.issue:
        task = github.get_task(args.issue)
        print(f"Processing issue #{task.issue_number}: {task.title}")
        result = orch.run_task_sync(task)
        print(result.summary)
    else:
        tasks = github.get_open_tasks(labels=["task", "agent"])
        print(f"Found {len(tasks)} open tasks")
        for t in tasks[:3]:  # limit for safety
            print(f"→ #{t.issue_number} {t.title}")
            result = orch.run_task_sync(t)
            print("  ", result.summary)

if __name__ == "__main__":
    main()
