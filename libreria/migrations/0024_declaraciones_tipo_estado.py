# Generated by Django 5.0.4 on 2024-07-09 21:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0023_declaraciones_tipo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='declaraciones_tipo',
            name='Estado',
            field=models.BooleanField(default=True),
        ),
    ]
