# Generated by Django 5.0.4 on 2024-08-12 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0042_historico_declaraciones_idcalendario_tributario'),
    ]

    operations = [
        migrations.AddField(
            model_name='asignacion',
            name='Mes',
            field=models.IntegerField(default=1, verbose_name='Mes'),
        ),
    ]