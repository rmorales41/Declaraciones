# Generated by Django 5.0.4 on 2024-06-18 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0017_historico_declaraciones'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calendario_tributario',
            name='IDClientes_Proveedores',
        ),
        migrations.RemoveField(
            model_name='calendario_tributario',
            name='IDPlanilla_Funcionarios',
        ),
    ]
