# Generated by Django 5.0.4 on 2024-08-14 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0046_cliente_proveedor_cliente_proveedor_idconfiguracion_corporativo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parametros_Declaraciones',
            fields=[
                ('IDParametros_Declaraciones', models.AutoField(primary_key=True, serialize=False)),
                ('Nombre', models.CharField(max_length=255)),
                ('Ubicacion_logo', models.TextField(blank=True, null=True, verbose_name='Ubicacion_logo')),
            ],
        ),
    ]
