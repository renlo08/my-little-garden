# Generated by Django 4.2.4 on 2024-01-18 22:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gardens', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fertilizationinline',
            name='garden',
        ),
        migrations.DeleteModel(
            name='Activity',
        ),
        migrations.DeleteModel(
            name='FertilizationInline',
        ),
    ]
