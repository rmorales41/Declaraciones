# Generated by Django 5.0.4 on 2024-07-05 23:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0019_cliente_proveedor_cliente_proveedor_tipo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaraciones_tipo_cliente',
            name='Ubicacion_Archivo',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
