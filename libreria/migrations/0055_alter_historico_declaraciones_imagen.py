# Generated by Django 5.0.4 on 2024-08-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0054_historico_declaraciones_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historico_declaraciones',
            name='imagen',
            field=models.ImageField(null=True, upload_to='imagenes/acuse', verbose_name='Imagen'),
        ),
    ]
