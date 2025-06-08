from decimal import Decimal
from django.db.models import Sum, F, Window, Value
from django.db.models.functions import ExtractYear, Rank, Concat
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.employees.models import Employee


class TopSalesRepByYearAPIView(APIView):
    """
    API view that returns the top sales representative and their total sales for a given year.

    Query Parameters:
        year (str): The year for which to retrieve sales data, passed as a URL parameter.

    Returns:
        - 400 Bad request: if the year does not contain only digits, or is greater than 9999.
        - 200 OK: JSON objects containing 'Sales Rep' (sales representative name) and 'Total Sales'.
        - 204 No Content: If no data is available to fulfill the request.
    """
    http_method_names = ['get']

    def get(self, request: Request, year: str) -> Response:
        if not year.isdigit() or int(year) >= 10000 or int(year) == 0:
            return Response(
                {'status': 'error', 'message': 'Year must contain only digits, and be less than 9999.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        top_sales_reps = (
            Employee.objects.filter(customers__invoices__invoice_date__year=int(year))
            .annotate(total_sales=Sum('customers__invoices__total'))
            .order_by('-total_sales')
        )

        if top_sales_reps:
            top_sales_reps_list = []
            # get top value
            top_value = top_sales_reps[0].total_sales
            # Filter reps who have the same top sales value
            top_sales_reps = top_sales_reps.filter(total_sales=top_value)

            if len(top_sales_reps) > 1:
                for rep in top_sales_reps:
                    top_sales_reps_list.append(
                        {'Sales Rep': str(rep.first_name + ' ' + rep.last_name),
                         'Total Sales': Decimal(rep.total_sales)}
                    )

                return Response(top_sales_reps_list, status=status.HTTP_200_OK)

            else:
                top_sales_reps = top_sales_reps.first()

                return Response(
                    {'Sales Rep': str(top_sales_reps), 'Total Sales': Decimal(top_sales_reps.total_sales)},
                    status=status.HTTP_200_OK
                )

        return Response(status=status.HTTP_204_NO_CONTENT)


class TopSalesRepsOverallAPIView(APIView):
    """
    API endpoint to retrieve the top sales representative per year with their total sales.

    Query Parameters:
        - order_by (str): Field to order by. One of 'sales_rep', 'total_sales', or 'year'. Defaults to 'year'.
        - order (str): Sorting order. Either 'asc' for ascending or 'desc' for descending. Defaults to 'asc'.

    Returns:
        - 400 Bad request: if "order_by" and/or "order" have invalid values — not "sales_rep", "total_sales", or "year"
        for "order_by", and not "asc" or "desc" for "order".
        - 200 OK: List of JSON objects containing 'Sales Rep' (sales representative name), 'Total Sales', and 'Year'.
        - 204 No Content: If no data is available to fulfill the request.
    """
    http_method_names = ['get']

    def get(self, request: Request) -> Response:
        order_by = request.GET.get('order_by')
        order = request.GET.get('order')

        if not order_by:
            order_by = 'year'
        if not order:
            order = 'asc'

        if order not in ['asc', 'desc'] or order_by not in ['sales_rep', 'total_sales', 'year']:
            return Response(
                {
                    'status': 'error',
                    'message': 'Invalid "order" and/or "order_by" chosen. Choose one of the options available.',
                    'accepted values for "order_by"': 'sales_rep; total_sales; year.',
                    'accepted values for "order"': 'asc; desc.',
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        order = '-' if order == 'desc' else ''

        order_parameter = order + order_by

        top_sales_reps_per_year = (
            Employee.objects.filter(customers__invoices__invoice_date__isnull=False)
            .annotate(year=ExtractYear('customers__invoices__invoice_date'))
            .annotate(total_sales=Sum('customers__invoices__total'))
            .annotate(rank=Window(expression=Rank(), partition_by=[F('year')], order_by=F('total_sales').desc()))
            .filter(rank=1)
            .annotate(sales_rep=Concat(F('first_name'), Value(' '), F('last_name')))
            .order_by(order_parameter)
        )

        if top_sales_reps_per_year:
            result_list = []
            for sales_rep in top_sales_reps_per_year:
                result_list.append(
                    {
                        'Sales Rep': f"{sales_rep}",
                        'Total Sales': Decimal(sales_rep.total_sales),
                        'Year': int(sales_rep.year)
                    }
                )

            return Response(result_list, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)
