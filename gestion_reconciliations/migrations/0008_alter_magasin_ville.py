# Generated by Django 4.1.5 on 2023-02-10 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_reconciliations', '0007_alter_magasin_type_magasin_alter_typemagasin_libelle'),
    ]

    operations = [
        migrations.AlterField(
            model_name='magasin',
            name='ville',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mags', to='gestion_reconciliations.ville'),
        ),
    ]