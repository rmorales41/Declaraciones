# Generated by Django 5.0.4 on 2024-07-09 21:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0022_remove_cliente_proveedor_cliente_proveedor_idplanilla_funcionarios'),
    ]

    operations = [
        migrations.CreateModel(
            name='Declaraciones_Tipo',
            fields=[
                ('IDDeclaraciones_Tipo', models.AutoField(primary_key=True, serialize=False)),
                ('Descipcion', models.CharField(max_length=120)),
                ('Institucion', models.CharField(max_length=180)),
                ('Observacion', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='declaraciones_tipo_cliente',
            name='IDDeclaraciones_Tipo',
            field=models.ForeignKey(default=2008, on_delete=django.db.models.deletion.CASCADE, to='libreria.declaraciones_tipo'),
            preserve_default=False,
        ),
    ]