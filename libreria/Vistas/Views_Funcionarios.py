from django.db.models import Count,Max,OuterRef,Exists
from django.http import JsonResponse
from django.shortcuts import render

from libreria.models import Asignacion, cliente_proveedor_cliente_proveedor, planillas_planilla_funcionarios


def VsCargaformula(request):
    return render(request,'formas/Visor_Funcionarios.html')  


def VsVisor_Funcionarios(request):
    try:  
        conteo = Asignacion.objects.values(            
            'IDPlanilla_Funcionarios',
            'IDPlanilla_Funcionarios__Nombre'
        ).annotate(
            total_asignaciones = Count('IDPlanilla_Funcionarios')
        ).order_by('IDPlanilla_Funcionarios')                         
        
        datos_conteo = list(conteo)
               
        # Retornar los datos como JsonResponse
        return JsonResponse(datos_conteo, safe=False)

    except Exception as e:
        print(f"Error en la vista VsVisor_Funcionarios: {e}")
        return JsonResponse({'error': str(e)}, status=500)
    

def Vsasignadasafuncionario(request):
    return render(request,'formas/asignadas_Funcionario.html')      

# toma la lista de los colaboradores del sistema 
def VsListaColaboradores(request):    
    try:  
        Funcionarios_Lista = planillas_planilla_funcionarios.objects.values(                        
        ).filter(
            Estado = True 
        ).order_by('Nombre')                         
        
        datos = list(Funcionarios_Lista)               
        # Retornar los datos como JsonResponse        
        return JsonResponse(datos, safe=False)
    except Exception as e:
        print(f"Error en la vista VsVisor_Funcionarios: {e}")
        return JsonResponse({'error': str(e)}, status=500)

# busca los clientes segun el colaborador seleccionado 
def VsListaColaboradoresyclientes(request, IDD):   
    try:            
        # Filtrar la lista de funcionarios basada en IDD
        Funcionarios_Lista = Asignacion.objects.filter(
            IDPlanilla_Funcionarios=IDD
        ).values(            
            'IDClientes_Proveedores__IDClientes_Proveedores',  # ID del proveedor
            'IDClientes_Proveedores__Descripcion',  # Descripción del proveedor
            'IDClientes_Proveedores__Direccion',  # Dirección del proveedor
            'IDClientes_Proveedores__Fecha_Ult_Movimiento',  # Fecha última de movimiento del proveedor
        ).annotate(
            max_id=Max('IDClientes_Proveedores')  # Usamos Max para agrupar los resultados
        ).order_by('IDClientes_Proveedores__Descripcion')
        
        datos = list(Funcionarios_Lista)
        
        # Retornar los datos como JsonResponse        
        return JsonResponse(datos, safe=False)

    except Exception as e:
        print(f"Error en la vista VsListaColaboradoresyclientes: {e}")
        return JsonResponse({'error': str(e)}, status=500)
  
# Muestra la pagina de clientes y a quien estan asignados 
def Vsclienteyfuncionario(request):
    return render(request,'formas/asignadas_Clientes.html')      

# Muestra todos los clientes y a quien estan asignados    
def VsDetalleClienteColaborador(request):
    try:
        # Obtener todos los clientes proveedores con los datos solicitados y la información de asignación
        funcionarios_lista = cliente_proveedor_cliente_proveedor.objects.filter(
            Tipo=True
        ).values(
            'IDClientes_Proveedores',
            'Descripcion',
            'Fecha_Ult_Movimiento',
            asignado=Exists(
                Asignacion.objects.filter(
                    IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).order_by('Descripcion')

        # Convertir el queryset en una lista de diccionarios
        datos = list(funcionarios_lista)

        # Retornar los datos como JsonResponse
        return JsonResponse(datos, safe=False)

    except Exception as e:
        error_msg = f"Error en la vista VsDetalleClienteColaborador: {str(e)}"
        print(error_msg)  # Registrar el error en los registros de la aplicación
        return JsonResponse({'error': error_msg}, status=500)


# Carga la pagina de EStado de Declaraciones 
def VsdeclaraEstado(request):
    return render(request,'formas/Estado_Cuenta_Declaracion.html')   

# ver datos de los clientes 
def VsListadeclaraClientes(request):
    try:
        todos_clientes = cliente_proveedor_cliente_proveedor.objects.filter(Estado=True, Tipo=True).order_by('Descripcion').values()        
        return JsonResponse({'data': list(todos_clientes)})
    except Exception as e:
        return JsonResponse({'error': 'Error al obtener los datos de clientes'}, status=500) 