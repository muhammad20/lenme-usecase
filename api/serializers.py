from rest_framework import serializers

from .models import *

class InvestorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investor
        fields = ['id', 'balance']

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = ['id']

class LoanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Loan
        fields = [
        'amount_in_dollars', 
        'payment_period_in_days', 
        'annual_percentage_interest_rate',
        'status',
        'borrower_id',
        'investor_id',
        'date_funded'
        ]

class LoanRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRequest
        fields = [
            'amount_in_dollars',
            'payment_period_in_days',
            'borrower_id'
        ]

class LoanOfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanOffer
        fields = [
            'amount_in_dollars',
            'id',
            'payment_period_in_days',
            'annual_percentage_interest_rate',
            'investor_id',
            'accepted_by',
            'is_available'
        ]

class ScheduledPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduledPayment
        fields = ['id', 'loan_id', 'deadline', 'amount_in_dollars', 'is_paid']

class LoanPaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanPayment
        fields = [
            'scheduled_payment_id',
            'payment_date',
            'payment_confirmed'
        ]