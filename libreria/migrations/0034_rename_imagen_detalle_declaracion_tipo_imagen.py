# Generated by Django 5.0.4 on 2024-07-22 17:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0033_rename_numero_aurotizado_detalle_declaracion_tipo_numero_autorizado'),
    ]

    operations = [
        migrations.RenameField(
            model_name='detalle_declaracion_tipo',
            old_name='imagen',
            new_name='Imagen',
        ),
    ]