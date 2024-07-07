from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Historico_Declaraciones


# Carga la pagina 
def VsHistorico_Movimientos(request):
   return render(request,'formas/Historico_Movimientos_Busqueda.html') 

# Busca todos los movimientos 
def VsMovimiento_Historicobusqueda(request):    
    try:                                                          
                                                
        Total_Movimientos = Historico_Declaraciones.objects.select_related(  
                    'IDClientes_Proveedores', 
                    'IDPlanilla_Funcionarios', 
                    'IDDeclaracion'
        ).order_by("-Fecha_Final")
                
                 
        tmovimientos = list(Total_Movimientos.values(
            'IDHistorico_Declaraciones',  
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',            
            'IDClientes_Proveedores__Descripcion',
            'Fecha_Asigna',
            'Fecha_Presenta',
            'Fecha_Final',            
            'Numero_Comprobante',                                    
            'IDPlanilla_Funcionarios__Nombre',  
        ))        
                                                   
        return JsonResponse(tmovimientos, safe=False)        
                                        
    except Historico_Declaraciones.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)   
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return JsonResponse({'error': str(e)}, status=500) 