# Generated by Django 5.0.4 on 2024-06-10 21:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0016_calendario_tributario'),
    ]

    operations = [
        migrations.CreateModel(
            name='Historico_Declaraciones',
            fields=[
                ('IDHistorico_Declaraciones', models.AutoField(primary_key=True, serialize=False)),
                ('IDAsignacion', models.IntegerField(blank=True, verbose_name='IDAsignacion')),
                ('Fecha_Presenta', models.DateField(blank=True, null=True, verbose_name='Fecha_Presenta')),
                ('Fecha_Asigna', models.DateField(blank=True, null=True, verbose_name='Fecha_Asigna')),
                ('Fecha_Proxima', models.DateField(blank=True, null=True, verbose_name='Fecha_Proxima')),
                ('Fecha_Cierre', models.DateField(blank=True, null=True, verbose_name='Fecha_Cierre')),
                ('correo', models.BooleanField(default=False)),
                ('Iniciada', models.BooleanField(default=False)),
                ('Suspendida', models.BooleanField(default=False)),
                ('Usuario_Cierre', models.CharField(max_length=100)),
                ('Numero_Comprobante', models.CharField(max_length=50)),
                ('Fecha_Final', models.DateTimeField(blank=True, null=True, verbose_name='Fecha_Final')),
                ('IDClientes_Proveedores', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.cliente_proveedor_cliente_proveedor')),
                ('IDDeclaracion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.declaracion')),
                ('IDPlanilla_Funcionarios', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='libreria.planillas_planilla_funcionarios')),
            ],
        ),
    ]
