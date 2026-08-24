"""Multi-repo helpers – Phase 7 (status + gated write policy)."""
from __future__ import annotations
from typing import List, Dict, Any, Optional
import os

try:
    import yaml
except ImportError:
    yaml = None

def load_repo_config(path: str = "config/repos.yaml") -> Dict[str, Any]:
    default = {
        "primary": {"full_name": os.getenv("GITHUB_REPOSITORY", "AgentMindCloud/RepoMind"), "role": "os"},
        "secondary": [],
        "policy": {
            "write_targets": ["proposals/", "docs/", "skills/", "memory/", "tests/", "marketplace/"],
            "never_auto_merge": True,
            "require_human_approved_label": True,
            "cross_repo_writes": False,
            "cross_repo_comments": False,
            "satellite_writes_require_human_approved": True,
        },
    }
    if not os.path.exists(path) or yaml is None:
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
        merged = default.copy()
        for k, v in data.items():
            if v is not None:
                merged[k] = v
        return merged
    except Exception as e:
        print(f"multi_repo config load failed: {e}")
        return default

def list_secondary_repos(cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    cfg = cfg or load_repo_config()
    out = []
    for item in cfg.get("secondary") or []:
        if isinstance(item, dict) and item.get("full_name"):
            out.append(item["full_name"])
        elif isinstance(item, str):
            out.append(item)
    return out

def allowed_write_prefixes(cfg: Optional[Dict[str, Any]] = None) -> List[str]:
    cfg = cfg or load_repo_config()
    return list((cfg.get("policy") or {}).get("write_targets") or ["proposals/"])

def status_report(cfg: Optional[Dict[str, Any]] = None) -> str:
    cfg = cfg or load_repo_config()
    primary = (cfg.get("primary") or {}).get("full_name") or "unknown"
    secondary = list_secondary_repos(cfg)
    policy = cfg.get("policy") or {}
    lines = [
        "### Multi-repo status (Phase 7)",
        f"- Primary: `{primary}`",
        f"- Secondary repos: {', '.join(f'`{s}`' for s in secondary) if secondary else '_none configured_'}",
        f"- Cross-repo writes: `{policy.get('cross_repo_writes', False)}`",
        f"- Cross-repo comments: `{policy.get('cross_repo_comments', False)}`",
        f"- Never auto-merge: `{policy.get('never_auto_merge', True)}`",
        f"- Human-approved required: `{policy.get('require_human_approved_label', True)}`",
    ]
    return "\n".join(lines)

def multi_repo_status(cfg: Optional[Dict[str, Any]] = None) -> str:
    """Alias used by ResearcherAgent."""
    return status_report(cfg)

def can_write_satellite(cfg: Optional[Dict[str, Any]] = None, human_approved: bool = False) -> bool:
    cfg = cfg or load_repo_config()
    policy = cfg.get("policy") or {}
    if not policy.get("cross_repo_writes", False):
        return False
    if policy.get("satellite_writes_require_human_approved", True) and not human_approved:
        return False
    return True
