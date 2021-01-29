from api.models import *
from api.serializers import *
import datetime
from api.lenme import *
from dateutil.relativedelta import relativedelta

class BorrowersController:
    def get_borrowers(self):
        borrowers = Borrower.objects.all()
        return BorrowerSerializer(borrowers, many=True)

class LoanOffersController:
    def get_offers(self):
        loan_offers = LoanOffer.objects.all()
        return LoanOfferSerializer(loan_offers, many=True)

    def get_available_offers(self):
        available_loan_offers = LoanOffer.objects.filter(is_available=True)
        return LoanOfferSerializer(available_loan_offers, many=True)

    def accept_offer(self, offer_id, borrower_id):
        accepted_offer = LoanOffer.objects.get(id=offer_id)
        if not accepted_offer.is_available:
            return None
        investor = InvestorController().get_investor_from_offer(accepted_offer.investor_id.id)
        if investor.balance >= accepted_offer.amount_in_dollars + LENME_FEE:
            accepted_offer.accepted_by = Borrower(id=borrower_id)
            accepted_offer.is_available = False
            accepted_offer.save()
            loan = LoanController().create(borrower_id, accepted_offer, investor)
            loan_serializer = LoanSerializer(data=loan)
            if loan_serializer.is_valid():
                loan = loan_serializer.save()
            else:
                ## TODO: Clean Up
                return None

            # calculating number of months from the payment total period
            no_months = accepted_offer.payment_period_in_days // 30

            # calculating total interest in decimals
            total_interest_amount = accepted_offer.annual_percentage_interest_rate * no_months / (12 * 100)

            #calculating monthly amount to be paid
            monthly_payment_amount = (1 + total_interest_amount) * (accepted_offer.amount_in_dollars / no_months)
            scheduledPaymentController = ScheduledPaymentController()

            #increment date by 1 month for each payment
            today = datetime.date.today()
            scheduled_payments = []
            for i in range(no_months):
                deadline = today + relativedelta(months=i+1)
                scheduled_payment = scheduledPaymentController.create(monthly_payment_amount, loan, deadline)
                scheduled_payments.append(scheduled_payment)
                serializer = ScheduledPaymentSerializer(data=scheduled_payment)
                if serializer.is_valid():
                    id = serializer.save().id
                    scheduled_payments[i]['id'] = id
            return scheduled_payments
        return None

class InvestorController:
    def get_investor_from_offer(self, investor_id):
        try:
            return Investor.objects.get(id=investor_id)
        except:
            return None

class LoanController:
    def get_loans(self):
        return LoanSerializer(Loan.objects.all(), many=True)

    def create(self, borrower_id, offer, investor):
        loan = {
            'borrower_id': borrower_id,
            'investor_id': investor.id,
            'amount_in_dollars': offer.amount_in_dollars,
            'payment_period_in_days': offer.payment_period_in_days,
            'annual_percentage_interest_rate': offer.annual_percentage_interest_rate,
            'status': LOAN_STATUS_FUNDED,
            'date_funded': datetime.date.today()
        }
        return loan

    def check_loan_fully_paid(self, id):
        unpaid = ScheduledPaymentController().get_unpaid(id)
        if len(unpaid) == 0:
            Loan.objects.update(id=id, status=LOAN_STATUS_COMPLETED)
        else:
            Loan.objects.update(id=id, status=LOAN_STATUS_FUNDED)

class LoanRequestsController:
    def request_loan(self, data):
        loan_request = LoanRequestSerializer(data=data)
        if loan_request.is_valid():
            if not LoanRequest.objects.filter(borrower_id=data['borrower_id']):
                loan_request.save()
            return LoanOffersController().get_available_offers()
        return None

class ScheduledPaymentController:
    def create(self, amount_in_dollars, loan, deadline):
        scheduled_payment = {
            'deadline': deadline,
            'loan_id': loan.id,
            'amount_in_dollars': amount_in_dollars
        }
        return scheduled_payment

    def get(self, id):
        try:
            scheduled_payment = ScheduledPayment.objects.get(id=id)
            return scheduled_payment
        except:
            return None

    def mark_as_paid(self, id):
        scheduled_payment = self.get(id)
        if not scheduled_payment == None:
            scheduled_payment.is_paid = True
            scheduled_payment.save()
            return True
        return False

    def get_unpaid(self, loan_id):
        return ScheduledPayment.objects.filter(loan_id=loan_id, is_paid=False)

class LoanPaymentController:
    def create(self, scheduled_payment_id):
        loan_payment = {
            'payment_date': datetime.date.today(),
            'scheduled_payment_id': scheduled_payment_id,
            'payment_confirmed': True
        }
        return loan_payment
    
    def get_from_scheduled_payment(self, scheduled_payment_id):
        try:
            return LoanPayment.objects.filter(scheduled_payment_id=scheduled_payment_id)
        except:
            return None

    def pay(self, scheduled_payment_id):
        loan_payment = self.get_from_scheduled_payment(scheduled_payment_id)
        if not len(loan_payment) == 0:
            return 'already paid!'
        scheduledPaymentController = ScheduledPaymentController()
        scheduled_payment = scheduledPaymentController.get(scheduled_payment_id)
        loan_payment = self.create(scheduled_payment_id)
        if not scheduled_payment == None:
            if scheduledPaymentController.mark_as_paid(scheduled_payment.id):
                    serializer = LoanPaymentSerializer(data=loan_payment)
                    if serializer.is_valid(raise_exception=True):
                        serializer.save()
                        LoanController().check_loan_fully_paid(scheduled_payment.loan_id.id)
                        return serializer.data
                    