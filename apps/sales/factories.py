import factory

from django.utils import timezone

from apps.sales.models import Invoice, InvoiceLine


class InvoiceFactory(factory.django.DjangoModelFactory):
    invoice_date = factory.Faker(
        'date_time_between',
        start_date='-50y',
        end_date='-20y',
        tzinfo=timezone.get_current_timezone()
    )
    total = factory.Faker('pydecimal', left_digits=8, right_digits=2, positive=True)

    class Meta:
        model = Invoice


class InvoiceLineFactory(factory.django.DjangoModelFactory):
    unit_price = factory.Faker('pydecimal', left_digits=3, right_digits=2, positive=True)
    quantity = factory.Faker('random_int', min=1, max=100)
    invoice = factory.SubFactory('apps.sales.factories.InvoiceFactory')
    track = factory.SubFactory('apps.music.factories.TrackFactory')

    class Meta:
        model = InvoiceLine
