import factory

from apps.customers.models import Customer


class CustomerFactory(factory.django.DjangoModelFactory):
    first_name = factory.Sequence(lambda n: f'first_name{n}')
    last_name = factory.Sequence(lambda n: f'last_name{n}')
    city = factory.Sequence(lambda n: f'city{n}')
    state = factory.Sequence(lambda n: f'state{n}')
    country = factory.Sequence(lambda n: f'country{n}')

    class Meta:
        model = Customer
