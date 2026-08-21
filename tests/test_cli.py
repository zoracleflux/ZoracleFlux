import json
from pathlib import Path

from zoracleflux.cli import main


def test_check_json_passes(capsys, monkeypatch):
    monkeypatch.chdir(Path(__file__).parents[1])
    assert main(["check", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "passed"
    assert result["network"] is False


def test_external_source_is_parsed_not_executed(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    source = tmp_path / "untrusted.py"
    source.write_text('def f():\n    """@relation idempotent"""\n    raise RuntimeError\n', encoding="utf-8")
    assert main(["check", "--source", str(source), "--json"]) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "not-executed"
    assert result["analysis"]["executed"] is False


def test_side_effect_source_is_never_run(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    marker = tmp_path / "must-not-exist"
    source = tmp_path / "side_effect.py"
    source.write_text(
        f'def f():\n    """@relation idempotent"""\n    open({str(marker)!r}, "w").write("bad")\n',
        encoding="utf-8",
    )
    assert main(["check", "--source", str(source), "--json"]) == 2
    assert not marker.exists()


def test_path_escape_is_rejected(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert main(["generate", "--output", "..\\outside.py", "--json"]) == 2
    assert json.loads(capsys.readouterr().out)["status"] == "error"


def test_safe_local_pilot_uses_sqlite_only(capsys, monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)
    assert main(["pilot", "--database", "pilot.sqlite3", "--runs", "2", "--json"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "passed"
    assert len(result["runs"]) == 2
    assert result["runs"][0]["network_calls"] == 0
    assert (tmp_path / "pilot.sqlite3").exists()
