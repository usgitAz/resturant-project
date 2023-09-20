# Generated by Django 4.2.5 on 2023-09-20 08:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0003_alter_usermodel_role'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor_name', models.CharField(max_length=100)),
                ('vendor_license', models.FileField(upload_to='vendor/license')),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('vendor_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserProfileModel', to='accounts.userprofilemodel')),
                ('vendoruser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='UserModel', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
