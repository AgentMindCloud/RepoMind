"""Phase 8 – multi-repo policy tests."""
from core.multi_repo import load_repo_config, can_write_satellite, status_report, allowed_write_prefixes

def test_default_config_loads():
    cfg = load_repo_config()
    assert "primary" in cfg or "policy" in cfg

def test_satellite_writes_disabled_by_default():
    assert can_write_satellite(human_approved=False) is False
    # Even with human_approved, cross_repo_writes defaults false
    assert can_write_satellite(human_approved=True) is False

def test_status_report_is_string():
    text = status_report()
    assert isinstance(text, str)
    assert "Primary" in text or "primary" in text.lower() or "Multi-repo" in text

def test_allowed_write_prefixes_include_safe_paths():
    prefixes = allowed_write_prefixes()
    assert any(p.startswith("proposals") or p.startswith("skills") or p.startswith("memory") for p in prefixes)
