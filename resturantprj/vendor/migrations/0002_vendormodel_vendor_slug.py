# Generated by Django 4.2.5 on 2023-09-27 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendormodel',
            name='vendor_slug',
            field=models.SlugField(max_length=100, null=True),
        ),
    ]