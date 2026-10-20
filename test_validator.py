import sys
from pathlib import Path
from datetime import date

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

sys.path.insert(0, str(SRC_DIR))

from validator import validate_employee


def valid_record():
    return {
        "employee_id": "EMP100",
        "name": "Rahul Sharma",
        "department": "IT",
        "role": "Developer",
        "joining_date": "2026-10-19",
        "manager": "Anil Kumar",
    }


def test_valid_employee():
    employee, errors = validate_employee(valid_record(), set())

    assert errors == []
    assert employee is not None
    assert employee.employee_id == "EMP100"


def test_missing_required_field():
    record = valid_record()
    record["role"] = ""

    employee, errors = validate_employee(record, set())

    assert employee is None
    assert any("role" in error for error in errors)


def test_invalid_joining_date():
    record = valid_record()
    record["joining_date"] = "19-10-2026"

    employee, errors = validate_employee(record, set())

    assert employee is None
    assert any("Invalid joining date" in error for error in errors)


def test_duplicate_employee_id():
    record = valid_record()

    employee, errors = validate_employee(
        record, {"EMP100"}
    )

    assert employee is None
    assert any("Duplicate employee ID" in error for error in errors)


def test_unique_employee_id_is_accepted():
    record = valid_record()
    record["employee_id"] = "EMP200"

    employee, errors = validate_employee(record, set())

    assert errors == []
    assert employee is not None
    assert employee.employee_id == "EMP200"
