# Generated by Django 4.2 on 2025-01-02 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0006_remove_product_id_alter_product_product_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='product_name',
            field=models.CharField(max_length=255),
        ),
    ]
