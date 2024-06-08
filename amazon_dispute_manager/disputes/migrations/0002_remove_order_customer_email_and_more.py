# Generated by Django 5.0.6 on 2024-06-08 19:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disputes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer_email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='customer_name',
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
