from datetime import datetime
from enum import Enum

from pydantic import BaseModel
from pydantic_ai import ModelRetry, RunContext
from pydantic_ai.toolsets import FunctionToolset

from apps.ai.types import UserDependencies
from pegasus.apps.employees.models import Employee

# Create DepartmentEnum dynamically from Django model choices
DepartmentEnum = Enum("DepartmentEnum", {value.upper(): value for value, _ in Employee.DEPARTMENT_CHOICES}, type=str)


class EmployeeData(BaseModel):
    """Employee information."""

    id: int | None = None
    created_at: datetime
    updated_at: datetime
    name: str
    department: DepartmentEnum
    salary: int

    @classmethod
    def from_employee(cls, employee: Employee) -> "EmployeeData":
        return cls(
            id=employee.id,
            created_at=employee.created_at,
            updated_at=employee.updated_at,
            name=employee.name,
            department=DepartmentEnum(employee.department),
            salary=employee.salary,
        )


async def list_employees(ctx: RunContext["UserDependencies"]) -> list[EmployeeData]:
    """List all employees.

    Args:
        user: The logged in user.
    """
    employees = []
    async for employee in Employee.objects.filter(user=ctx.deps.user).aiterator():
        employees.append(employee)
    return [EmployeeData.from_employee(employee) for employee in employees]


def create_employee(ctx: RunContext["UserDependencies"], employee_data: EmployeeData) -> EmployeeData:
    """Create an employee.

    Args:
        employee_data: The employee data.
    """
    employee = Employee.objects.create(user=ctx.deps.user, **employee_data.model_dump(exclude={"id"}))
    return EmployeeData.from_employee(employee)


def update_employee(ctx: RunContext["UserDependencies"], employee_data: EmployeeData) -> EmployeeData:
    """Update an employee.

    Args:
        employee_data: The employee data.
    """
    if employee_data.id is None:
        raise ModelRetry("Employee ID is required") from None
    try:
        employee = Employee.objects.get(id=employee_data.id, user=ctx.deps.user)
    except Employee.DoesNotExist:
        raise ModelRetry(f"Employee with ID {employee_data.id} does not exist") from None

    employee.name = employee_data.name
    employee.department = employee_data.department.value
    employee.salary = employee_data.salary
    employee.save()
    return EmployeeData.from_employee(employee)


def delete_employee(ctx: RunContext["UserDependencies"], employee_id: int) -> EmployeeData:
    """Delete an employee.

    Args:
        employee_id: The employee ID.
    """
    try:
        employee = Employee.objects.get(id=employee_id, user=ctx.deps.user)
    except Employee.DoesNotExist:
        raise ModelRetry(f"Employee with ID {employee_id} does not exist") from None
    data = EmployeeData.from_employee(employee)
    employee.delete()
    return data


employee_toolset = FunctionToolset(
    tools=[
        list_employees,
        create_employee,
        update_employee,
        delete_employee,
    ]
)
