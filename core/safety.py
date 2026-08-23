"""Safety enforcement for RepoMind – Constitution checks."""
import yaml
from pathlib import Path
from typing import List

class SafetyGuard:
    def __init__(self, constitution_path: str = "contracts/constitution.yaml"):
        path = Path(constitution_path)
        if path.exists():
            with open(path) as f:
                self.constitution = yaml.safe_load(f)
        else:
            self.constitution = {"articles": {}}

    def check_no_secrets(self, content: str) -> bool:
        forbidden = ["API_KEY=", "SECRET=", "xai-", "sk-", "Bearer ", "PRIVATE_KEY"]
        return not any(f in content for f in forbidden)

    def check_pr_allowed(self, files_changed: List[str], labels: List[str]) -> bool:
        core_touched = any(
            f.startswith("core/") or f.startswith("contracts/") or f.startswith(".github/")
            for f in files_changed
        )
        if core_touched and "human-approved" not in labels and "approved" not in labels:
            return False
        return True

    def max_iterations(self, default: int = 8) -> int:
        return default
