from api.views import *
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('loan-offers/', loan_offers_list),
    path('request-loan/', request_loan),
    path('accept-offer/', accept_offer),
    path('pay/', pay_scheduled_payment),
    path('borrowers/', get_borrowers),
    path('loans/', get_loans)
]

urlpatterns = format_suffix_patterns(urlpatterns)