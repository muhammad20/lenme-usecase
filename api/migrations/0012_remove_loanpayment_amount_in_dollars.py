# Generated by Django 3.1.5 on 2021-01-29 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20210129_0143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='loanpayment',
            name='amount_in_dollars',
        ),
    ]
