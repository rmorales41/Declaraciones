# Generated by Django 5.0.4 on 2024-05-22 23:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0012_rename_iddeclaracion_id_declaracion_clientes_iddeclaracion'),
    ]

    operations = [
        migrations.AddField(
            model_name='planillas_planilla_funcionarios',
            name='Estado',
            field=models.BooleanField(default=True),
        ),
    ]
