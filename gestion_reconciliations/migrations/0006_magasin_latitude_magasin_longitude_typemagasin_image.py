# Generated by Django 4.1.5 on 2023-02-06 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion_reconciliations', '0005_alter_magasin_chef'),
    ]

    operations = [
        migrations.AddField(
            model_name='magasin',
            name='latitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='magasin',
            name='longitude',
            field=models.FloatField(default=0.0),
        ),
        migrations.AddField(
            model_name='typemagasin',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='typemagasin/images'),
        ),
    ]