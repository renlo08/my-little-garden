# Generated by Django 4.2.4 on 2024-01-19 22:21

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0002_rename_due_date_fertilization_creation_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fertilization',
            name='creation',
        ),
        migrations.RemoveField(
            model_name='fertilization',
            name='updated',
        ),
        migrations.AddField(
            model_name='activity',
            name='creation',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='activity',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
