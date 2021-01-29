# Generated by Django 3.1.5 on 2021-01-28 16:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loan',
            name='borrower_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.borrower'),
        ),
        migrations.AddField(
            model_name='loan',
            name='date_funded',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='loan',
            name='investor_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.investor'),
        ),
        migrations.AddField(
            model_name='loanrequest',
            name='borrower_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.borrower'),
        ),
        migrations.CreateModel(
            name='ScheduledPayment',
            fields=[
                ('id', models.CharField(max_length=60, primary_key=True, serialize=False)),
                ('deadline', models.DateField(null=True)),
                ('loan_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.loan')),
            ],
        ),
        migrations.CreateModel(
            name='LoanPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('payment_date', models.DateField(null=True)),
                ('payment_confirmed', models.BooleanField(default=False)),
                ('scheduled_payment_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.scheduledpayment')),
            ],
        ),
        migrations.CreateModel(
            name='LoanOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_in_dollars', models.FloatField()),
                ('payment_period_in_days', models.PositiveIntegerField()),
                ('annual_percentage_interest_rate', models.FloatField()),
                ('investor_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.investor')),
            ],
        ),
    ]
