# Generated by Django 4.1.5 on 2023-02-03 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_reconciliations', '0002_typemagasin_code_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='typemagasin',
            name='responsable',
        ),
    ]
