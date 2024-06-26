# Generated by Django 5.0.6 on 2024-05-24 19:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='equipment',
            options={'ordering': ['title', 'size'], 'verbose_name': 'equipment', 'verbose_name_plural': 'equipments'},
        ),
        migrations.AlterField(
            model_name='review',
            name='client',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='companies_app.client'),
        ),
        migrations.AlterField(
            model_name='review',
            name='equipment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='companies_app.equipment'),
        ),
    ]
