# Generated by Django 4.2 on 2025-01-10 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0020_alter_marketingmetrics_quarter_growth_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='avg_customer_years',
            field=models.FloatField(default=3),
        ),
        migrations.AlterField(
            model_name='customer',
            name='avg_purchase_interval',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='avg_purchase_value',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='lifetime_value',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
