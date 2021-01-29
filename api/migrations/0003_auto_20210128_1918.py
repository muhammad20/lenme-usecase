# Generated by Django 3.1.5 on 2021-01-28 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20210128_1636'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanoffer',
            name='accepted_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.borrower'),
        ),
        migrations.AddField(
            model_name='loanoffer',
            name='is_available',
            field=models.BooleanField(default=True),
        ),
    ]
