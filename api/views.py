from api.serializers import *
from rest_framework.response import Response
from api.models import *
from rest_framework.decorators import api_view
from .controllers import *
from rest_framework import status

@api_view(['GET'])
def get_borrowers(request):
    if request.method == 'GET':
        return Response(BorrowersController().get_borrowers().data)

@api_view(['GET'])
def get_loans(request):
    if request.method == 'GET':
        return Response(LoanController().get_loans().data)

@api_view(['GET'])
def loan_offers_list(request):
    if request.method == 'GET':
      controller = LoanOffersController()
      return Response(controller.get_offers().data)

@api_view(['POST'])
def request_loan(request):
    if request.method == 'POST':
        available_loan_offers = LoanRequestsController().request_loan(request.data)
        if available_loan_offers == None:
            return Response('fail', status=status.HTTP_400_BAD_REQUEST)
        return Response(available_loan_offers.data)

@api_view(['POST'])
def accept_offer(request):
    if request.method == 'POST':
        scheduled_payments = LoanOffersController().accept_offer(request.data.get("offer_id"), request.data.get("borrower_id"))
    if scheduled_payments == None:
        return Response('fail', status=status.HTTP_400_BAD_REQUEST)
    return Response(scheduled_payments)

@api_view(['POST'])
def pay_scheduled_payment(request):
    if request.method == 'POST':
        payment_confirmation = LoanPaymentController().pay(request.data.get("scheduled_payment_id"))
        if payment_confirmation == None:
            return Response('Not payed')
        return Response(payment_confirmation)
        
