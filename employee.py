from dataclasses import dataclass
from datetime import date

@dataclass
class Employee:
    employee_id: str
    name: str
    department: str
    role: str
    joining_date: date
    manager: str

    def to_dict(self):
        return {
            "employee_id": self.employee_id,
            "name": self.name,
            "department": self.department,
            "role": self.role,
            "joining_date": self.joining_date.isoformat(),
            "manager": self.manager,
        }
