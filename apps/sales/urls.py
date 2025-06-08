from django.urls import path

from .api.views import TopSalesRepByYearAPIView, TopSalesRepsOverallAPIView

urlpatterns = [
    path('api/v1/sellers/<year>/top', TopSalesRepByYearAPIView.as_view(), name='api-top-sales-rep-by-year'),
    path('api/v1/sellers/top', TopSalesRepsOverallAPIView.as_view(), name='api-top-sales-reps-overall'),
]
