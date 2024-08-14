import json
from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Asignacion


def VsParametros(request):       
       return render(request,'formas/Parametros.html')
   

def VsAjuste_Declaracion(request):
       try:
        # Obtener las asignaciones de todos los clientes esto va a permitir ajustar el mes que el sistema 
        # va controlando 
        asignaciones_lista = Asignacion.objects.filter(            
        ).values(
            'IDAsignacion',
            'IDClientes_Proveedores__Descripcion',
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'Mes',
            'Mes'
        ).order_by('Mes')

        # Convertir el queryset en una lista de diccionarios
        datos = list(asignaciones_lista)
        
        # Retornar los datos como JsonResponse
        return render(request,'formas/Ajuste_Declaraciones.html',{'var_asignaciones': datos}) 
       

       except Exception as e:
         error_msg = f"Error en la vista VsAjuste_Declaracion: {str(e)}"
         print(error_msg)  # Registrar el error en los registros de la aplicación
         return JsonResponse({'error': error_msg}, status=500)

def VsConfirmaMes(request,idd):   
    if request.method == 'POST':
        try:
            # se obtiene el objeto de asigna 
            asignaciones = Asignacion.objects.get(pk=idd)
            # ver los datos recibidos en el json 
            data =json.loads(request.body.decode('utf-8'))            
            # se obtienen los datos                                
            mescambio = data.get('mesdato')                                   
            # Actualizar los campos en el objeto historico_declaracion
            Asignacion.Mes = data.get('mescambio')              
            # Guardar los cambios en la base de datos
            Asignacion.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'}) 