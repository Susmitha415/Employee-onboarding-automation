from datetime import datetime
from employee import Employee

REQUIRED_FIELDS = [
"employee_id",
"name",
"department",
"role",
"joining_date",
"manager",
]

def validate_employee(record, seen_ids):
    errors = []


# Validate required fields
    for field in REQUIRED_FIELDS:
        value = record.get(field)

        if value is None or not str(value).strip():
            errors.append(f"Missing required field: {field}")

# Validate employee ID
    employee_id = str(
        record.get("employee_id") or ""
    ).strip()

    if employee_id:
        if employee_id in seen_ids:
            errors.append(
                f"Duplicate employee ID: {employee_id}"
            )
        else:
            seen_ids.add(employee_id)

    # Validate joining date
    joining_date = None
    date_value = str(
        record.get("joining_date") or ""
    ).strip()

    if date_value:
        try:
            joining_date = datetime.strptime(
                date_value, "%Y-%m-%d"
            ).date()
        except ValueError:
            errors.append(
                "Invalid joining date. Use YYYY-MM-DD."
            )

    # Reject invalid records
    if errors:
        return None, errors

    # Create employee object
    employee = Employee(
        employee_id=employee_id,
        name=str(record["name"]).strip(),
        department=str(record["department"]).strip(),
        role=str(record["role"]).strip(),
        joining_date=joining_date,
        manager=str(record["manager"]).strip(),
    )

    return employee, []