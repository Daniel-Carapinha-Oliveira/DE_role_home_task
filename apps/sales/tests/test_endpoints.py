import pytest
import string

from datetime import datetime
from decimal import Decimal
from django.urls import reverse
from django.utils import timezone
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestTopSalesRepByYearAPIView:
    client = APIClient()

    def test_get_year_above_9999(self):
        response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': 10000}))
        assert response.status_code in [400]
        assert response.json() == {
            'status': 'error',
            'message': 'Year must contain only digits, and be less than 9999.'
        }

    def test_get_year_is_zero(self):
        response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': 0}))
        assert response.status_code in [400]
        assert response.json() == {
            'status': 'error',
            'message': 'Year must contain only digits, and be less than 9999.'
        }

    def test_get_year_not_only_digits(self):
        all_printable_strings = string.printable
        not_accepted_values = ''.join(
            char for char in all_printable_strings if not (char.isdigit() or char == '/')
        )
        for char in not_accepted_values:
            print(char)
            response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': char}))
            assert response.status_code in [400]
            assert response.json() == {
                'status': 'error',
                'message': 'Year must contain only digits, and be less than 9999.'
            }

    def test_get_no_data_for_chosen_year(self):
        # for this test to work, there can't be any data in the Invoice table
        response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': 2009}))
        assert response.status_code in [204]

    def test_get_desired_output_for_available_year(self, invoice_factory, customer_factory, employee_factory):
        year = 2023
        aware_datetime = timezone.make_aware(datetime(year, 4, 15, 10, 30))

        employee = employee_factory(first_name='John', last_name='Smith')
        customer = customer_factory(support_representative=employee)
        invoice = invoice_factory(invoice_date=aware_datetime, customer=customer, total=200.00)

        response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': year}))

        assert response.status_code == 200
        assert response.json() == {'Sales Rep': 'John Smith', 'Total Sales': Decimal(invoice.total)}

    def test_get_multiple_employees_have_same_total_sales(self, invoice_factory, customer_factory, employee_factory):
        year = 2023
        aware_datetime = timezone.make_aware(datetime(year, 4, 15, 10, 30))

        employee1 = employee_factory(first_name='John', last_name='Smith')
        employee2 = employee_factory(first_name='Maria', last_name='Miller')
        customer1 = customer_factory(support_representative=employee1)
        customer2 = customer_factory(support_representative=employee2)
        invoice1 = invoice_factory(invoice_date=aware_datetime, customer=customer1, total=200.00)
        invoice2 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=200.00)

        response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': year}))

        expected_response = [
            {'Sales Rep': 'John Smith', 'Total Sales': Decimal(invoice1.total)},
            {'Sales Rep': 'Maria Miller', 'Total Sales': Decimal(invoice2.total)}
        ]

        sorted_expected_response = sorted(expected_response, key=lambda k: k['Sales Rep'])

        assert response.status_code == 200
        assert response.json() == sorted_expected_response

    def test_get_desired_output_for_available_year_with_two_sales_representatives(
            self,
            invoice_factory,
            customer_factory,
            employee_factory
    ):
        year = 2023
        aware_datetime = timezone.make_aware(datetime(year, 4, 15, 10, 30))

        employee1 = employee_factory()
        employee2 = employee_factory()

        customer1 = customer_factory(support_representative=employee1)
        customer2 = customer_factory(support_representative=employee2)

        invoice_factory(invoice_date=aware_datetime, customer=customer1, total=200.00)
        invoice_1 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=150.00)
        invoice_2 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=160.00)

        response = self.client.get(reverse('api-top-sales-rep-by-year', kwargs={'year': year}))

        assert response.status_code == 200
        assert response.json() == {
            'Sales Rep': f'{employee2}',
            'Total Sales': Decimal(invoice_1.total + invoice_2.total)
        }


class TestTopSalesRepsOverallAPIView:
    client = APIClient()

    @pytest.fixture
    def valid_expected_response_one_year(self, invoice_factory, customer_factory, employee_factory):
        year = 2023
        aware_datetime = timezone.make_aware(datetime(year, 4, 15, 10, 30))

        employee1 = employee_factory()
        employee2 = employee_factory()

        customer1 = customer_factory(support_representative=employee1)
        customer2 = customer_factory(support_representative=employee2)

        invoice_factory(invoice_date=aware_datetime, customer=customer1, total=200.00)
        invoice_1 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=150.00)
        invoice_2 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=160.00)

        expected_response = [
            {"Sales Rep": f"{employee2}", "Total Sales": Decimal(invoice_1.total + invoice_2.total), "Year": int(year)}
        ]

        return expected_response

    @pytest.fixture
    def valid_expected_response_one_year_repeated_totals(self, invoice_factory, customer_factory, employee_factory):
        year = 2023
        aware_datetime = timezone.make_aware(datetime(year, 4, 15, 10, 30))

        employee1 = employee_factory(first_name='Maria', last_name='Miller')
        employee2 = employee_factory(first_name='John', last_name='Smith')

        customer1 = customer_factory(support_representative=employee1)
        customer2 = customer_factory(support_representative=employee2)

        # 2023
        invoice_1 = invoice_factory(invoice_date=aware_datetime, customer=customer1, total=400.00)
        invoice_2 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=200.00)
        invoice_3 = invoice_factory(invoice_date=aware_datetime, customer=customer2, total=200.00)

        expected_response = [
            {"Sales Rep": f"{employee1}", "Total Sales": Decimal(invoice_1.total), "Year": int(year)},
            {"Sales Rep": f"{employee2}", "Total Sales": Decimal(invoice_2.total + invoice_3.total), "Year": int(year)},
        ]

        return expected_response

    @pytest.fixture
    def valid_expected_response_to_test_ordering(self, invoice_factory, customer_factory, employee_factory):
        aware_datetime_2023 = timezone.make_aware(datetime(2023, 4, 15, 10, 30))
        aware_datetime_2019 = timezone.make_aware(datetime(2019, 4, 15, 10, 30))
        aware_datetime_2024 = timezone.make_aware(datetime(2024, 4, 15, 10, 30))

        employee1 = employee_factory(first_name='Josh', last_name='Smith')
        employee2 = employee_factory(first_name='Maria', last_name='Jones')
        employee3 = employee_factory(first_name='Stan', last_name='Miller')

        customer1 = customer_factory(support_representative=employee1)
        customer2 = customer_factory(support_representative=employee2)
        customer3 = customer_factory(support_representative=employee3)

        # 2023
        # top sales_rep = "Josh Smith", total = 400.00
        invoice_factory(invoice_date=aware_datetime_2023, customer=customer1, total=200.00)
        invoice_factory(invoice_date=aware_datetime_2023, customer=customer1, total=200.00)
        invoice_factory(invoice_date=aware_datetime_2023, customer=customer2, total=350.00)

        # 2019
        # top sales_rep = "Stan Miller", total = 600.00
        invoice_factory(invoice_date=aware_datetime_2019, customer=customer1, total=200.00)
        invoice_factory(invoice_date=aware_datetime_2019, customer=customer3, total=600.00)
        invoice_factory(invoice_date=aware_datetime_2019, customer=customer1, total=350.00)

        # 2024
        # top sales_rep = "Maria Jones", total = 350.00
        invoice_factory(invoice_date=aware_datetime_2024, customer=customer3, total=200.00)
        invoice_factory(invoice_date=aware_datetime_2024, customer=customer1, total=200.00)
        invoice_factory(invoice_date=aware_datetime_2024, customer=customer2, total=350.00)

        # not associated
        invoice_factory(invoice_date=aware_datetime_2024, customer=None, total=1000.00)

    def test_order_by_invalid(self):
        url = reverse('api-top-sales-reps-overall')
        order_by = 'invalid'
        response = self.client.get(f"{url}?order_by={order_by}")
        expected_response = {
            'status': 'error',
            'message': 'Invalid "order" and/or "order_by" chosen. Choose one of the options available.',
            'accepted values for "order_by"': 'sales_rep; total_sales; year.',
            'accepted values for "order"': 'asc; desc.',
        }
        assert response.status_code == 400
        assert response.json() == expected_response

    def test_order_invalid(self):
        url = reverse('api-top-sales-reps-overall')
        order = 'invalid'
        response = self.client.get(f"{url}?order={order}")
        expected_response = {
            'status': 'error',
            'message': 'Invalid "order" and/or "order_by" chosen. Choose one of the options available.',
            'accepted values for "order_by"': 'sales_rep; total_sales; year.',
            'accepted values for "order"': 'asc; desc.',
        }
        assert response.status_code == 400
        assert response.json() == expected_response

    def test_get_no_data(self):
        # for this test to work, there can't be any data in the Invoice table
        response = self.client.get(reverse('api-top-sales-reps-overall'))
        assert response.status_code in [204]

    def test_get_desired_output_for_available_year_with_two_sales_representatives(
            self, valid_expected_response_one_year
    ):
        expected_response = valid_expected_response_one_year

        response = self.client.get(reverse('api-top-sales-reps-overall'))

        assert response.status_code == 200
        assert response.json() == expected_response

    def test_get_desired_output_for_available_year_with_two_sales_reps_and_repeated_totals(
            self, valid_expected_response_one_year_repeated_totals
    ):
        expected_response = valid_expected_response_one_year_repeated_totals

        response = self.client.get(reverse('api-top-sales-reps-overall'))

        # for each year, sort by name
        response_sorted = sorted(response.json(), key=lambda x: (x['Year'], x['Sales Rep']))
        expected_response_sorted = sorted(expected_response, key=lambda x: (x['Year'], x['Sales Rep']))

        assert response.status_code == 200
        assert response.json() == expected_response

    @pytest.mark.parametrize("order_by,order,expected", [
        ("total_sales", "asc", [
            {"Sales Rep": "Maria Jones", "Total Sales": 350, "Year": 2024},
            {"Sales Rep": "Josh Smith", "Total Sales": 400, "Year": 2023},
            {"Sales Rep": "Stan Miller", "Total Sales": 600, "Year": 2019},
        ]),
        ("total_sales", "desc", [
            {"Sales Rep": "Stan Miller", "Total Sales": 600, "Year": 2019},
            {"Sales Rep": "Josh Smith", "Total Sales": 400, "Year": 2023},
            {"Sales Rep": "Maria Jones", "Total Sales": 350, "Year": 2024},
        ]),
        ("year", "asc", [
            {"Sales Rep": "Stan Miller", "Total Sales": 600, "Year": 2019},
            {"Sales Rep": "Josh Smith", "Total Sales": 400, "Year": 2023},
            {"Sales Rep": "Maria Jones", "Total Sales": 350, "Year": 2024},
        ]),
        ("year", "desc", [
            {"Sales Rep": "Maria Jones", "Total Sales": 350, "Year": 2024},
            {"Sales Rep": "Josh Smith", "Total Sales": 400, "Year": 2023},
            {"Sales Rep": "Stan Miller", "Total Sales": 600, "Year": 2019},
        ]),
        ("sales_rep", "desc", [
            {"Sales Rep": "Stan Miller", "Total Sales": 600, "Year": 2019},
            {"Sales Rep": "Maria Jones", "Total Sales": 350, "Year": 2024},
            {"Sales Rep": "Josh Smith", "Total Sales": 400, "Year": 2023},
        ]),
        ("sales_rep", "asc", [
            {"Sales Rep": "Josh Smith", "Total Sales": 400, "Year": 2023},
            {"Sales Rep": "Maria Jones", "Total Sales": 350, "Year": 2024},
            {"Sales Rep": "Stan Miller", "Total Sales": 600, "Year": 2019},
        ]),
    ])
    def test_ordering_parametrized(self, valid_expected_response_to_test_ordering, order_by, order, expected):
        url = reverse('api-top-sales-reps-overall')
        response = self.client.get(f"{url}?order_by={order_by}&order={order}")
        assert response.status_code == 200
        assert response.json() == expected
