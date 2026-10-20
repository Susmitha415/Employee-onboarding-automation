import re
from pathlib import Path

def safe_folder_name(value):
    cleaned = re.sub(r'[<>:"/\|?*\x00-\x1f]', "_", value)
    cleaned = cleaned.strip(" .")

    if not cleaned:
        raise ValueError("Invalid employee folder name")

    return cleaned

def create_employee_file(output_dir, employee, content):
    folder_name = safe_folder_name(
f"{employee.employee_id}_{employee.name}"
)

    employee_folder = Path(output_dir) / folder_name
    employee_folder.mkdir(parents=True, exist_ok=True)

    output_file = employee_folder / "onboarding.txt"

    with output_file.open("w", encoding="utf-8") as file:
        file.write(content)

    return output_file