# Generated by Django 5.0.6 on 2024-05-24 19:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies_app', '0002_alter_equipment_options_alter_review_client_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies_app.client'),
        ),
    ]