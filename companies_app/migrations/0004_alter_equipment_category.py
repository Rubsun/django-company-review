# Generated by Django 5.0.6 on 2024-05-24 19:29

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies_app', '0003_alter_equipment_client'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='equipments', to='companies_app.category', verbose_name='category'),
        ),
    ]
