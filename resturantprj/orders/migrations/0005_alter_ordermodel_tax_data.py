# Generated by Django 4.2.5 on 2023-10-10 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_ordermodel_total_data_ordermodel_vendors'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='tax_data',
            field=models.JSONField(blank=True, help_text="Data format: {'tax_type':{'tax_percentage':'tax_amount'}}", null=True),
        ),
    ]
