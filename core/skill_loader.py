"""Dynamic skill loader for RepoMind."""
from pathlib import Path
from typing import Dict, Any, Optional, Callable
import importlib.util

class SkillLoader:
    def __init__(self, skills_root: str = "skills"):
        self.skills_root = Path(skills_root)
        self._cache: Dict[str, Any] = {}

    def list_skills(self) -> list[str]:
        skills = []
        if not self.skills_root.exists():
            return skills
        for category in self.skills_root.iterdir():
            if category.is_dir() and category.name != "__pycache__":
                for skill in category.iterdir():
                    if skill.is_dir() and (skill / "SKILL.md").exists():
                        skills.append(f"{category.name}/{skill.name}")
        return skills

    def load_contract(self, skill_path: str) -> Dict[str, Any]:
        md_path = self.skills_root / skill_path / "SKILL.md"
        if not md_path.exists():
            return {}
        return {"name": skill_path, "path": str(md_path)}

    def load_implementation(self, skill_path: str) -> Optional[Callable]:
        impl_path = self.skills_root / skill_path / "implementation.py"
        if not impl_path.exists():
            return None
        spec = importlib.util.spec_from_file_location("skill_impl", impl_path)
        if spec is None or spec.loader is None:
            return None
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        for name in ["generate_thread", "scan", "run", "main", "execute"]:
            if hasattr(module, name):
                return getattr(module, name)
        return None
