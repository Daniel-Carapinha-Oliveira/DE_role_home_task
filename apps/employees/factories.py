import factory

from django.utils import timezone

from apps.employees.models import Employee


class EmployeeFactory(factory.django.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: f'first_name{n}')
    last_name = factory.Sequence(lambda n: f'last_name{n}')
    title = factory.Sequence(lambda n: f'title{n}')
    hire_date = factory.Faker(
        'date_time_between',
        start_date='-10y',
        end_date='now',
        tzinfo=timezone.get_current_timezone()
    )
    address = factory.Sequence(lambda n: f'address{n}')
    city = factory.Sequence(lambda n: f'city{n}')
    state = factory.Sequence(lambda n: f'state{n}')
    country = factory.Sequence(lambda n: f'country{n}')
    postal_code = factory.Sequence(lambda n: f'postal_code{n}')
    phone = factory.Sequence(lambda n: str(n).zfill(9))
    email = factory.Sequence(lambda n: f'user{n}@example.com')

    class Meta:
        model = Employee
