# Generated by Django 3.1.5 on 2021-01-28 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20210128_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='loanrequest',
            name='borrower_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.borrower'),
        ),
    ]
