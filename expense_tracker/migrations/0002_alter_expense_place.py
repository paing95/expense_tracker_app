# Generated by Django 5.1.6 on 2025-02-18 19:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expense_tracker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='expense_tracker.place'),
        ),
    ]
