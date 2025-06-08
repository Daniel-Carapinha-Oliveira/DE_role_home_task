from pytest_factoryboy import register

from apps.customers.factories import (
    CustomerFactory
)
from apps.employees.factories import EmployeeFactory

register(CustomerFactory)
register(EmployeeFactory)
