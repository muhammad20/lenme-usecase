from django.db import models

LOAN_STATUS_FUNDED = 'FD'
LOAN_STATUS_COMPLETED = 'CD'

class Investor(models.Model):
    balance = models.FloatField()

class Borrower(models.Model):
    pass

class Loan(models.Model):
    class LoanStatus(models.TextChoices):
        FUNDED = LOAN_STATUS_FUNDED,
        COMPLETED = LOAN_STATUS_COMPLETED

    amount_in_dollars = models.FloatField()
    payment_period_in_days = models.PositiveIntegerField()
    annual_percentage_interest_rate = models.FloatField()
    status = models.CharField(max_length=2, choices=LoanStatus.choices)
    borrower_id = models.ForeignKey('Borrower', on_delete=models.DO_NOTHING)
    investor_id = models.ForeignKey('Investor', on_delete=models.DO_NOTHING)
    date_funded = models.DateField(null=True)

class LoanRequest(models.Model):
    amount_in_dollars = models.FloatField()
    payment_period_in_days = models.PositiveIntegerField()
    borrower_id = models.ForeignKey('Borrower', on_delete=models.DO_NOTHING)

class LoanOffer(models.Model):
    amount_in_dollars = models.FloatField()
    payment_period_in_days = models.PositiveIntegerField()
    annual_percentage_interest_rate = models.FloatField()
    investor_id = models.ForeignKey('Investor', on_delete=models.DO_NOTHING)
    accepted_by = models.ForeignKey('Borrower', on_delete=models.DO_NOTHING, null=True, blank=True)
    is_available = models.BooleanField(default=True)

class ScheduledPayment(models.Model):
    loan_id = models.ForeignKey('Loan', on_delete=models.CASCADE)
    deadline = models.DateField(null=True)
    amount_in_dollars = models.FloatField()
    is_paid = models.BooleanField(default=False)

class LoanPayment(models.Model):
    scheduled_payment_id = models.ForeignKey('ScheduledPayment', on_delete=models.CASCADE)
    payment_date = models.DateField(null=True)
    payment_confirmed = models.BooleanField(default=False)