import pytest

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from apps.sales.models import Invoice, InvoiceLine

pytestmark = pytest.mark.django_db


class TestInvoiceModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_billing_address_max_length(self, invoice_factory):
        billing_address = 'x' * 256
        with pytest.raises(ValidationError):
            invoice_factory(billing_address=billing_address)

    def test_billing_address_field_null(self, invoice_factory):
        obj = invoice_factory()
        assert obj.billing_address is None

    def test_billing_city_max_length(self, invoice_factory):
        billing_city = 'x' * 129
        with pytest.raises(ValidationError):
            invoice_factory(billing_city=billing_city)

    def test_billing_city_field_null(self, invoice_factory):
        obj = invoice_factory()
        assert obj.billing_city is None

    def test_billing_state_max_length(self, invoice_factory):
        billing_state = 'x' * 129
        with pytest.raises(ValidationError):
            invoice_factory(billing_state=billing_state)

    def test_billing_state_field_null(self, invoice_factory):
        obj = invoice_factory()
        assert obj.billing_state is None

    def test_billing_country_max_length(self, invoice_factory):
        billing_country = 'x' * 65
        with pytest.raises(ValidationError):
            invoice_factory(billing_country=billing_country)

    def test_billing_country_field_null(self, invoice_factory):
        obj = invoice_factory()
        assert obj.billing_country is None

    def test_billing_postal_code_max_length(self, invoice_factory):
        billing_postal_code = 'x' * 21
        with pytest.raises(ValidationError):
            invoice_factory(billing_postal_code=billing_postal_code)

    def test_billing_postal_code_field_null(self, invoice_factory):
        obj = invoice_factory()
        assert obj.billing_postal_code is None

    def test_total_accepts_only_zero_and_positive(self, invoice_factory):
        with pytest.raises(ValidationError):
            invoice_factory(total=-1.2)

    def test_fk_customer_on_delete_protect(self, invoice_factory, customer_factory):
        obj = customer_factory()
        invoice_factory(customer=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_customer_field_null(self, invoice_factory):
        obj = invoice_factory()
        assert obj.customer is None

    def test_str_method(self, invoice_factory):
        obj = invoice_factory()
        assert obj.__str__() == obj.invoice_date.strftime('%Y-%m-%d %H:%M:%S')

    def test_ordering(self, invoice_factory):
        tracks = invoice_factory.create_batch(5)
        expected_order = sorted(tracks, key=lambda k: k.invoice_date, reverse=True)
        assert list(Invoice.objects.all()) == expected_order

    def test_save_calls_full_clean(self, invoice_factory, monkeypatch):
        invoice = invoice_factory()
        monkeypatch.setattr(invoice, 'full_clean', self.fake_full_clean)
        invoice.save()
        assert self.full_clean_calls == 1


class TestInvoiceLineModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_unit_price_accepts_only_zero_and_positive(self, invoice_line_factory):
        with pytest.raises(ValidationError):
            invoice_line_factory(unit_price=-1.2)

    def test_quantity_positive_number(self, invoice_line_factory):
        with pytest.raises(ValidationError):
            invoice_line_factory(quantity=-1)

    def test_quantity_integer_number(self, invoice_line_factory):
        track = invoice_line_factory.build(quantity=1.2)
        with pytest.raises(ValidationError):
            track.full_clean()

    def test_fk_invoice_on_delete_protect(self, invoice_line_factory, invoice_factory):
        obj = invoice_factory()
        invoice_line_factory(invoice=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_fk_track_on_delete_protect(self, invoice_line_factory, track_factory):
        obj = track_factory()
        invoice_line_factory(track=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_str_method(self, invoice_line_factory):
        obj = invoice_line_factory()
        assert obj.__str__() == f'{obj.invoice} - {obj.track}'

    def test_ordering(self, invoice_line_factory):
        tracks = invoice_line_factory.create_batch(5)
        expected_order = sorted(tracks, key=lambda k: k.id)
        assert list(InvoiceLine.objects.all()) == expected_order

    def test_save_calls_full_clean(self, invoice_line_factory, monkeypatch):
        invoice_line = invoice_line_factory()
        monkeypatch.setattr(invoice_line, 'full_clean', self.fake_full_clean)
        invoice_line.save()
        assert self.full_clean_calls == 1
