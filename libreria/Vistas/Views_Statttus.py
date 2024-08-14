# ve el Status de las declaraciones junto con las fechas de los calendarios mes y año  
from urllib import request
from django.http import JsonResponse
from django.shortcuts import render
from django.db.models import F
from django.core.serializers import serialize

from libreria.models import Asignacion, Historico_Declaraciones, calendario_tributario

# busca el formulario para mostrar el mes y año de busqueda 
def Vslevanta_Stattus(request):
    return render(request,'formas/Stattus_Calendario.html') 

# busca los datos del calendario para el visor del Status de las declaraciones 
# con el calendario  tributario para ver las diferencias y los cumplimientos 
def VsDeclaracionesfinales(request,selectedYear,selectedMonth):                    
    try:                            
        an = int(selectedYear) 
        me = int(selectedMonth)        
                                                   
        # Filtrar el historial de declaraciones basadas en la fecha final que ya se procesaron en el mes 
        # especifico lista de ids 
        total_declaraciones_historial = Historico_Declaraciones.objects.filter(
            Fecha_Presenta__year=an,
            Mes=me
        ).order_by("-Fecha_Presenta")
                                   
        # Obtener Id Historico 
        historico_ids = total_declaraciones_historial.values_list('IDDeclaracion', flat=True)                                        
   
        # Obtener registros de Asignacion que no están en Historico_Declaraciones
        asignaciones_faltantes = Asignacion.objects.filter(
               Fecha_Presenta__year=an,
               Mes=me,
               IDDeclaracion__estado =True 
        ).exclude(IDDeclaracion__in=historico_ids)                        
               
        # combinar los dos resultados 
        # Primero convierte ambos QuerySets en listas
        historico_list = list(total_declaraciones_historial)         
        asignaciones_faltantes_list = list(asignaciones_faltantes)   
        
        combined_results = historico_list + asignaciones_faltantes_list                        
        combined_results.sort(key=lambda x: x.Fecha_Presenta, reverse=True)                              
                 
        # se busca en calendarios tributario la fecha de la presentacion de las mismas 
        ids_declaracion = set()
        for obj in combined_results:
            if hasattr(obj, 'IDDeclaracion') and obj.IDDeclaracion: 
               ids_declaracion.add(obj.IDDeclaracion.pk)    
       
        # filtra calendario tributario 
        calendario_tributario_records = calendario_tributario.objects.filter(
           IDDeclaracion__in=ids_declaracion,
           Fecha_Presenta__year=an,
           Fecha_Presenta__month=me
        ).values('IDDeclaracion', 'Fecha_Presenta') 
        #print('calendario',calendario_tributario_records)
                 
        # se crea dicccionario para ingresar 
        fecha_presentacion_dict = {record['IDDeclaracion']: record['Fecha_Presenta'] for record in calendario_tributario_records}                                                                     
  
      # Formatear los resultados combinados
        formatted_results = []
        for obj in combined_results:
            if isinstance(obj, Historico_Declaraciones):                
                fecha_presenta_calendario = fecha_presentacion_dict.get(obj.IDDeclaracion_id, None)
                formatted_results.append({
                    'IDHistorico_Declaraciones': obj.IDHistorico_Declaraciones,
                    'IDDeclaracion__codigo': obj.IDDeclaracion.codigo if obj.IDDeclaracion else None,
                    'IDClientes_Proveedores': str(obj.IDClientes_Proveedores) if obj.IDClientes_Proveedores else None,
                    'IDClientes_Proveedores__Descripcion': obj.IDClientes_Proveedores.Descripcion if obj.IDClientes_Proveedores else None,
                    'IDPlanilla_Funcionarios__Nombre': obj.IDPlanilla_Funcionarios.Nombre if obj.IDPlanilla_Funcionarios else None,
                    'Fecha_Presenta': obj.Fecha_Presenta.isoformat() if obj.Fecha_Presenta else None,
                    'Fecha_Cierre': obj.Fecha_Cierre.isoformat() if obj.Fecha_Cierre else None,
                    'Fecha_Final': obj.Fecha_Final.isoformat() if obj.Fecha_Final else None,
                    'Fecha_Calendario':fecha_presenta_calendario.isoformat() if fecha_presenta_calendario else None,
                    'Fecha_Sistema': obj.Fecha_Sistema.isoformat() if obj.Fecha_Sistema else None,
                    'Numero_Comprobante': obj.Numero_Comprobante,
                    'rectificativa': obj.rectificativa,
                })
            elif isinstance(obj, Asignacion):
                fecha_presenta_calendario = fecha_presentacion_dict.get(obj.IDDeclaracion_id, None)
                formatted_results.append({
                    'IDHistorico_Declaraciones': None,
                    'IDDeclaracion__codigo': obj.IDDeclaracion.codigo if obj.IDDeclaracion else None,
                    'IDClientes_Proveedores': str(obj.IDClientes_Proveedores) if obj.IDClientes_Proveedores else None,
                    'IDClientes_Proveedores__Descripcion': obj.IDClientes_Proveedores.Descripcion if obj.IDClientes_Proveedores else None,
                    'IDPlanilla_Funcionarios__Nombre': obj.IDPlanilla_Funcionarios.Nombre if obj.IDPlanilla_Funcionarios else None,
                    'Fecha_Presenta': obj.Fecha_Presenta.isoformat() if obj.Fecha_Presenta else None,
                    'Fecha_Cierre': None,
                    'Fecha_Final': None,
                    'Fecha_Calendario': fecha_presenta_calendario.isoformat() if fecha_presenta_calendario else None,
                    'Fecha_Sistema': None,
                    'Numero_Comprobante': None,
                    'rectificativa': obj.Rectificativa,
                })
                        
        # Devuelve datos         
        return JsonResponse(formatted_results, safe=False)        
                                        
    except Historico_Declaraciones.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return JsonResponse({'error': str(e)}, status=500)   