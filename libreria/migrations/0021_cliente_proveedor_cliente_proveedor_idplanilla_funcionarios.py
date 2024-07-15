import django.db.models.deletion
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('libreria', '0020_declaraciones_tipo_cliente_ubicacion_archivo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente_proveedor_cliente_proveedor',
            name='IDPlanilla_Funcionarios',  # Cambia este nombre por uno apropiado
            field=models.ForeignKey(
                to='libreria.planillas_planilla_funcionarios',  # Asegúrate de que esto apunte a la tabla correcta
                on_delete=django.db.models.deletion.CASCADE,  # O el tipo de eliminación adecuado.
                null=True,  # Permitir valores NULL
            ),
            preserve_default=False,  # Revisa si necesitas mantener el valor predeterminado
        ),
    ]
