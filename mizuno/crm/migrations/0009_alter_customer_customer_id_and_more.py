# Generated by Django 4.2 on 2025-01-02 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0008_customer_id_alter_customer_customer_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='customer_ID',
            field=models.IntegerField(default=1, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='rfmanalysis',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crm.customer'),
        ),
    ]
