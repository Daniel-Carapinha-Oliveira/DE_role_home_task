from pytest_factoryboy import register

from apps.customers.factories import CustomerFactory
from apps.employees.factories import EmployeeFactory
from apps.music.factories import TrackFactory
from apps.sales.factories import (
    InvoiceFactory,
    InvoiceLineFactory
)

register(CustomerFactory)
register(EmployeeFactory)
register(TrackFactory)
register(InvoiceFactory)
register(InvoiceLineFactory)
