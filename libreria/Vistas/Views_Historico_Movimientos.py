from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Historico_Declaraciones


# Carga la pagina 
def VsHistorico_Movimientos(request):
   return render(request,'formas/Historico_Movimientos.html') 

# Busca la cantidad de registros que esta en el historico 
def VsMovimiento_Historico(request,selectedYear,selectedMonth):    
    try:                                                          
        ayear  = int(selectedYear)
        amonth = int(selectedMonth)
                                                
        Total_Movimientos = Historico_Declaraciones.objects.select_related(  
                    'IDClientes_Proveedores', 
                    'IDPlanilla_Funcionarios', 
                    'IDDeclaracion'
        ).filter(
            Fecha_Final__year=ayear,
            Fecha_Final__month=amonth,        
        ).order_by("-Fecha_Final")
        
        print('total ver',Total_Movimientos)
                 
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