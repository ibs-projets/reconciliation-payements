# Generated by Django 4.1.5 on 2023-02-23 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_reconciliations', '0011_utilisateur_adresse_utilisateur_ville_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='est_connecte',
            field=models.BooleanField(default=False),
        ),
    ]
