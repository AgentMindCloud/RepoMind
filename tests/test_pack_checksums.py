"""Phase 8 – pack path + checksum helper tests."""
from marketplace.checksums import load_packs, compute_pack_checksums, verify_pack, verify_all_pack_paths

def test_packs_json_loads():
    data = load_packs()
    assert "packs" in data
    assert isinstance(data["packs"], list)
    assert len(data["packs"]) >= 1

def test_all_pack_entry_files_exist():
    assert verify_all_pack_paths() is True

def test_compute_pack_checksums_returns_actual_hashes():
    rows = compute_pack_checksums()
    assert rows
    for r in rows:
        assert r["id"]
        assert r["actual"], f"Missing file for {r['id']} at {r['path']}"
        assert len(r["actual"]) == 64

def test_verify_known_pack():
    data = load_packs()
    first_id = data["packs"][0]["id"]
    result = verify_pack(first_id)
    assert result["ok"] is True
    assert result["actual"]
