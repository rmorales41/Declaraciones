# Generated by Django 5.0.4 on 2024-05-07 17:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0009_rename_estado_declaracion_clientes_estado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='declaracion_clientes',
            name='IDPlanilla_Funcionarios',
        ),
    ]
