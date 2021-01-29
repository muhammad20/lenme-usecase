from django.test import TestCase, Client
from .models import Borrower, Investor, LoanOffer
from .serializers import *
from django.core import serializers

class LenmeTestCase(TestCase):
    def setUp(self):

        #create initial objects for the test case
        Borrower.objects.create()
        investor = Investor.objects.create(balance=10000)
        LoanOffer.objects.create(
            amount_in_dollars=5000,
            payment_period_in_days=180,
            annual_percentage_interest_rate=15,
            investor_id=investor
        )

    def test_general_flow(self):
        c = Client()

        # Returns only available offers
        response = c.post('/request-loan/', {
                "amount_in_dollars": 5000.0,
                "borrower_id": 1,
                "payment_period_in_days": 180
        })

        self.assertEqual(len(response.data), 1)

        # The only available offer by investor with id=1
        offer = response.data[0]

        #accept the offer by the only investor
        borrower = c.get('/borrowers/').data[0]

        # Accepting the offer makes the offer unavailable
        # Returns scheduled payments to be pait for fulfillment
        # Creates a loan object with status='Funded'
        scheduled_payments = c.post('/accept-offer/', {
            'offer_id': offer['id'],
            'borrower_id': borrower['id']
        }).data

        self.assertEqual(len(scheduled_payments), 6)

        # Get The only created loan and check its status
        loans = c.get('/loans/').data
        self.assertEqual(len(loans), 1)
        self.assertEqual(loans[0]['status'], LOAN_STATUS_FUNDED)

        # simulate paying the scheduled payments
        for scheduled_payment in scheduled_payments:
           confirmation = c.post('/pay/', {
               "scheduled_payment_id": scheduled_payment['id']
           })

        # Get The only created loan and check its status
        loans = c.get('/loans/').data
        self.assertEqual(len(loans), 1)
        self.assertEqual(loans[0]['status'], LOAN_STATUS_COMPLETED)


        






