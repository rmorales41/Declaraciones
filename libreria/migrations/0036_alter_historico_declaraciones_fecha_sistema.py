# Generated by Django 5.0.4 on 2024-07-24 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0035_detalle_declaracion_tipo_fecha_recordatorio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico_declaraciones',
            name='Fecha_Sistema',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Fecha_Sistema'),
        ),
    ]
