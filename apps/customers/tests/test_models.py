import pytest
import string

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from apps.customers.models import Customer

pytestmark = pytest.mark.django_db


class TestCustomerModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_first_name_max_length(self, customer_factory):
        first_name = 'x' * 65
        with pytest.raises(ValidationError):
            customer_factory(first_name=first_name)

    def test_last_name_max_length(self, customer_factory):
        last_name = 'x' * 65
        with pytest.raises(ValidationError):
            customer_factory(last_name=last_name)

    def test_company_max_length(self, customer_factory):
        company = 'x' * 129
        with pytest.raises(ValidationError):
            customer_factory(company=company)

    def test_company_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.company is None

    def test_address_max_length(self, customer_factory):
        address = 'x' * 256
        with pytest.raises(ValidationError):
            customer_factory(address=address)

    def test_address_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.address is None

    def test_city_max_length(self, customer_factory):
        city = 'x' * 129
        with pytest.raises(ValidationError):
            customer_factory(city=city)

    def test_state_max_length(self, customer_factory):
        state = 'x' * 129
        with pytest.raises(ValidationError):
            customer_factory(state=state)

    def test_country_max_length(self, customer_factory):
        country = 'x' * 65
        with pytest.raises(ValidationError):
            customer_factory(country=country)

    def test_postal_code_max_length(self, customer_factory):
        postal_code = 'x' * 21
        with pytest.raises(ValidationError):
            customer_factory(postal_code=postal_code)

    def test_postal_code_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.postal_code is None

    def test_phone_max_length(self, customer_factory):
        phone = 'x' * 33
        with pytest.raises(ValidationError):
            customer_factory(phone=phone)

    def test_phone_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.phone is None

    def test_phone_char_validator(self, customer_factory):
        accepted_chars = list('0123456789 -()')
        for char in string.printable:
            if char not in accepted_chars:
                with pytest.raises(ValidationError):
                    phone = '12345' + char
                    customer_factory(phone=phone)

        customer_factory(phone='+' + '12345')

    def test_phone_minimum_char_validator(self, customer_factory):
        for length in [1, 2, 3, 4, 5]:
            chars = '1' * length
            with pytest.raises(ValidationError):
                customer_factory(phone=chars)

    def test_phone_unique_field(self, customer_factory):
        phone = '123456'
        customer_factory(phone=phone)
        with pytest.raises(ValidationError):
            customer_factory(phone=phone)

    def test_fax_max_length(self, customer_factory):
        fax = 'x' * 33
        with pytest.raises(ValidationError):
            customer_factory(fax=fax)

    def test_fax_char_validator(self, customer_factory):
        accepted_chars = list('0123456789 -()')
        for char in string.printable:
            if char not in accepted_chars:
                with pytest.raises(ValidationError):
                    fax = '12345' + char
                    customer_factory(fax=fax)

        customer_factory(fax='+' + '12345')

    def test_fax_minimum_char_validator(self, customer_factory):
        for length in [1, 2, 3, 4, 5]:
            chars = '1' * length
            with pytest.raises(ValidationError):
                customer_factory(fax=chars)

    def test_fax_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.fax is None

    def test_email_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.email is None

    def test_email_unique_field(self, customer_factory):
        email = 'example@example.com'
        customer_factory(email=email)
        with pytest.raises(ValidationError):
            customer_factory(email=email)

    def test_support_representative_field_null(self, customer_factory):
        obj = customer_factory()
        assert obj.support_representative is None

    def test_fk_support_representative_on_delete_protect(self, customer_factory, employee_factory):
        obj = employee_factory()
        customer_factory(support_representative=obj)
        with pytest.raises(IntegrityError):
            obj.delete()

    def test_str_method(self, customer_factory):
        obj = customer_factory(first_name='John', last_name='Smith')
        assert obj.__str__() == 'John Smith'

    def test_ordering(self, customer_factory):
        customers = customer_factory.create_batch(5)
        expected_order = sorted(customers, key=lambda k: (k.first_name, k.last_name))
        assert list(Customer.objects.all()) == expected_order

    def test_save_calls_full_clean(self, customer_factory, monkeypatch):
        customer = customer_factory()
        monkeypatch.setattr(customer, 'full_clean', self.fake_full_clean)
        customer.save()
        assert self.full_clean_calls == 1
