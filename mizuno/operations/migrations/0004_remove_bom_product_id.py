# Generated by Django 4.2 on 2025-01-02 13:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_remove_task_task_id_alter_bom_material_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bom',
            name='product_ID',
        ),
    ]
