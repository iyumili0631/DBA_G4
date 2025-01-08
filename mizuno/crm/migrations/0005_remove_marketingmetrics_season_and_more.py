# Generated by Django 4.2 on 2025-01-01 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0004_alter_customer_lifetime_value'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='marketingmetrics',
            name='season',
        ),
        migrations.RemoveField(
            model_name='marketingmetrics',
            name='seasonal_growth_rate',
        ),
        migrations.RemoveField(
            model_name='marketingmetrics',
            name='seasonal_sales',
        ),
        migrations.AddField(
            model_name='marketingmetrics',
            name='quarter',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='marketingmetrics',
            name='quarter_growth_rate',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='marketingmetrics',
            name='quarter_sales',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='marketingmetrics',
            name='year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
