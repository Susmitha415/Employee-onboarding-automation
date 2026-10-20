import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_onboarding_process_generates_report_and_log():
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "src" / "main.py")],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
    )

    assert result.returncode == 0, result.stderr

    report_file = PROJECT_ROOT / "reports" / "processing_summary.txt"
    log_file = PROJECT_ROOT / "logs" / "onboarding.log"

    assert report_file.exists()
    assert log_file.exists()

    report = report_file.read_text(encoding="utf-8")
    log = log_file.read_text(encoding="utf-8")

    assert "EMPLOYEE ONBOARDING PROCESSING SUMMARY" in report
    assert "Successfully processed:" in report
    assert "Employee onboarding process started" in log
