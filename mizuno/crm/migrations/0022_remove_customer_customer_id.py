# Generated by Django 4.2 on 2025-01-10 18:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_alter_customer_avg_customer_years_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='customer_ID',
        ),
    ]