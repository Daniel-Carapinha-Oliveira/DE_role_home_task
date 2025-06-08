import pytest
import string

from django.core.exceptions import ValidationError

from apps.employees.models import Employee

pytestmark = pytest.mark.django_db


class TestEmployeeModel:
    def setup_method(self):
        self.full_clean_calls = 0

    def fake_full_clean(self):
        self.full_clean_calls += 1

    def test_first_name_max_length(self, employee_factory):
        first_name = 'x' * 65
        with pytest.raises(ValidationError):
            employee_factory(first_name=first_name)

    def test_last_name_max_length(self, employee_factory):
        last_name = 'x' * 65
        with pytest.raises(ValidationError):
            employee_factory(last_name=last_name)

    def test_title_max_length(self, employee_factory):
        title = 'x' * 256
        with pytest.raises(ValidationError):
            employee_factory(title=title)

    def test_birthdate_field_null(self, employee_factory):
        obj = employee_factory()
        assert obj.birthdate is None

    def test_address_max_length(self, employee_factory):
        address = 'x' * 256
        with pytest.raises(ValidationError):
            employee_factory(address=address)

    def test_city_max_length(self, employee_factory):
        city = 'x' * 129
        with pytest.raises(ValidationError):
            employee_factory(city=city)

    def test_state_max_length(self, employee_factory):
        state = 'x' * 129
        with pytest.raises(ValidationError):
            employee_factory(state=state)

    def test_country_max_length(self, employee_factory):
        country = 'x' * 65
        with pytest.raises(ValidationError):
            employee_factory(country=country)

    def test_postal_code_max_length(self, employee_factory):
        postal_code = 'x' * 21
        with pytest.raises(ValidationError):
            employee_factory(postal_code=postal_code)

    def test_phone_max_length(self, employee_factory):
        phone = 'x' * 33
        with pytest.raises(ValidationError):
            employee_factory(phone=phone)

    def test_phone_char_validator(self, employee_factory):
        accepted_chars = list('0123456789 -()')
        for char in string.printable:
            if char not in accepted_chars:
                with pytest.raises(ValidationError):
                    phone = '12345' + char
                    employee_factory(phone=phone)

        employee_factory(phone='+' + '12345')

    def test_phone_minimum_char_validator(self, employee_factory):
        for length in [1, 2, 3, 4, 5]:
            chars = '1' * length
            with pytest.raises(ValidationError):
                employee_factory(phone=chars)

    def test_phone_unique_field(self, employee_factory):
        phone = '123456'
        employee_factory(phone=phone)
        with pytest.raises(ValidationError):
            employee_factory(phone=phone)

    def test_fax_max_length(self, employee_factory):
        fax = 'x' * 33
        with pytest.raises(ValidationError):
            employee_factory(fax=fax)

    def test_fax_char_validator(self, employee_factory):
        accepted_chars = list('0123456789 -()')
        for char in string.printable:
            if char not in accepted_chars:
                with pytest.raises(ValidationError):
                    fax = '12345' + char
                    employee_factory(fax=fax)

        employee_factory(fax='+' + '12345')

    def test_fax_minimum_char_validator(self, employee_factory):
        for length in [1, 2, 3, 4, 5]:
            chars = '1' * length
            with pytest.raises(ValidationError):
                employee_factory(fax=chars)

    def test_fax_field_null(self, employee_factory):
        obj = employee_factory()
        assert obj.fax is None

    def test_email_unique_field(self, employee_factory):
        email = 'example@example.com'
        employee_factory(email=email)
        with pytest.raises(ValidationError):
            employee_factory(email=email)

    def test_reports_to_field_null(self, employee_factory):
        obj = employee_factory()
        assert obj.reports_to is None

    def test_fk_reports_to_on_delete_set_null(self, employee_factory):
        obj = employee_factory()
        employee = employee_factory(reports_to=obj)
        obj.delete()
        employee.refresh_from_db()
        assert not employee.reports_to

    def test_str_method(self, employee_factory):
        obj = employee_factory(first_name='John', last_name='Smith')
        assert obj.__str__() == 'John Smith'

    def test_ordering(self, employee_factory):
        employees = employee_factory.create_batch(5)
        expected_order = sorted(employees, key=lambda k: (k.first_name, k.last_name))
        assert list(Employee.objects.all()) == expected_order

    def test_save_calls_full_clean(self, employee_factory, monkeypatch):
        employee = employee_factory()
        monkeypatch.setattr(employee, 'full_clean', self.fake_full_clean)
        employee.save()
        assert self.full_clean_calls == 1
