# Generated by Django 4.2 on 2025-01-02 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_remove_marketingmetrics_season_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='id',
        ),
        migrations.AlterField(
            model_name='customer',
            name='name',
            field=models.CharField(max_length=255, primary_key=True, serialize=False),
        ),
    ]
