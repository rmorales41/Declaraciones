# Generated by Django 5.0.4 on 2024-07-08 23:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0021_cliente_proveedor_cliente_proveedor_idplanilla_funcionarios'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cliente_proveedor_cliente_proveedor',
            name='IDPlanilla_Funcionarios',
        ),
    ]
