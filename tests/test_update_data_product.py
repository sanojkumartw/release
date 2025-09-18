import pytest
import subprocess
from scripts.update_data_product import update_data_product

class TestUpdateDataProduct:
    def test_up_to_date(self, monkeypatch, capsys):
        """Project already up-to-date (cruft check passes)."""

        def mock_run(cmd, capture_output=False, text=False, check=False):
            class MockResult:
                returncode = 0
                stdout = "Already up to date"
                stderr = ""
            return MockResult()

        monkeypatch.setattr(subprocess, "run", mock_run)

        update_data_product(".", "sample_product")
        captured = capsys.readouterr()

        assert "up to date" in captured.out.lower()

    def test_needs_update_successful(self, monkeypatch, capsys):
        """Project behind template, update succeeds."""

        calls = []

        def mock_run(cmd, capture_output=False, text=False, check=False):
            calls.append(cmd)
            if "check" in cmd:
                class MockResult:
                    returncode = 1
                    stdout = "Out of date"
                    stderr = ""
                return MockResult()
            if "update" in cmd:
                return subprocess.CompletedProcess(cmd, 0)

        monkeypatch.setattr(subprocess, "run", mock_run)

        update_data_product(".", "sample_product")
        captured = capsys.readouterr()

        assert "updates found" in captured.out.lower()
        assert "successfully updated" in captured.out.lower()
        assert any("update" in c for c in calls)

    def test_update_fails(self, monkeypatch, capsys):
        """Update command fails with CalledProcessError."""

        def mock_run(cmd, capture_output=False, text=False, check=False):
            if "check" in cmd:
                class MockResult:
                    returncode = 1
                    stdout = "Out of date"
                    stderr = ""
                return MockResult()
            if "update" in cmd:
                raise subprocess.CalledProcessError(
                    returncode=1, cmd=cmd, stderr="Update failed"
                )

        monkeypatch.setattr(subprocess, "run", mock_run)

        with pytest.raises(SystemExit):
            update_data_product(".", "sample_product")

        captured = capsys.readouterr()
        assert "error during update process" in captured.out.lower()
        assert "update failed" in captured.out.lower()
