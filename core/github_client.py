"""GitHub client for RepoMind – Issues, PRs, files, comments."""
from typing import List, Optional, Dict, Any
from github import Github, GithubException
from github.Repository import Repository
from github.Issue import Issue
from .models import Task
import os

class GitHubClient:
    def __init__(self, token: Optional[str] = None, repo_full_name: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GITHUB_TOKEN required")
        self.gh = Github(self.token)
        self.repo_name = repo_full_name or os.getenv("GITHUB_REPOSITORY", "AgentMindCloud/RepoMind")
        self.repo: Repository = self.gh.get_repo(self.repo_name)

    def get_open_tasks(self, labels: Optional[List[str]] = None) -> List[Task]:
        issues = self.repo.get_issues(state="open", labels=labels or [])
        tasks = []
        for issue in issues:
            if issue.pull_request:  # skip PRs
                continue
            tasks.append(Task(
                issue_number=issue.number,
                title=issue.title,
                body=issue.body or "",
                labels=[l.name for l in issue.labels],
                state=issue.state,
                html_url=issue.html_url
            ))
        return tasks

    def get_task(self, number: int) -> Task:
        issue = self.repo.get_issue(number)
        return Task(
            issue_number=issue.number,
            title=issue.title,
            body=issue.body or "",
            labels=[l.name for l in issue.labels],
            state=issue.state,
            html_url=issue.html_url
        )

    def comment_on_issue(self, number: int, body: str) -> None:
        issue = self.repo.get_issue(number)
        issue.create_comment(body)

    def create_issue(self, title: str, body: str, labels: Optional[List[str]] = None) -> int:
        issue = self.repo.create_issue(title=title, body=body, labels=labels or [])
        return issue.number

    def create_or_update_file(self, path: str, content: str, message: str, branch: str = "main") -> str:
        try:
            # Try update
            contents = self.repo.get_contents(path, ref=branch)
            result = self.repo.update_file(path, message, content, contents.sha, branch=branch)
        except GithubException:
            # Create new
            result = self.repo.create_file(path, message, content, branch=branch)
        return result["commit"].sha

    def create_pull_request(self, title: str, body: str, head: str, base: str = "main") -> str:
        pr = self.repo.create_pull(title=title, body=body, head=head, base=base)
        return pr.html_url

    def add_labels(self, number: int, labels: List[str]) -> None:
        issue = self.repo.get_issue(number)
        issue.add_to_labels(*labels)
