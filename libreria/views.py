<<<<<<< Updated upstream
from typing import Self
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
=======
from datetime import date
import datetime
from typing import Self
from urllib import request
from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
>>>>>>> Stashed changes
from .models import Asignacion, declaracion, planillas_planilla_funcionarios,cliente_proveedor_cliente_proveedor

# carga el diseño del formulario 
from .forms import AsignaDeclaraciones, DeclaraForm
# paginacion 
from django.core.paginator import Paginator
 
<<<<<<< Updated upstream
from django.db.models import Exists,OuterRef
=======
from django.db.models import Exists,OuterRef,Subquery
>>>>>>> Stashed changes

# vista de inicio 
def inicio(request):
    return HttpResponse("<h1>Bienvenido</h1>")

# vista base 
def base(request):
    return render(request,'paginas/base.html')

# vusta Clientes
def clientes(request):
    return render(request,'paginas/clientes.html')
# vista nosotros
def nosotros(request):
    return render(request, 'paginas/nosotros.html')


# vista visor
def visor(request):
    datos_decla = declaracion.objects.all().order_by('codigo')  
    # es el listado general y la cantidad por pagina 
    paginator = Paginator(datos_decla,8)            
    # crear variable page si no existe se pone 1
    pagina = request.GET.get("page") or 1   
    # el posts es la vista como tal de datos_decla a posts que es igual a publicaciones por pagina  
    posts   = paginator.get_page(pagina) 
    # se hace para saber la cantidad de paginas variable 
    pagina_actual  = int(pagina)
    # se define la cantidad de paginas con range en la variable paginas inicia en 1  
    paginas = range(1,posts.paginator.num_pages + 1)    
   # Paginacion se ve la cantidad de objetos en lista  
    return render(request, 'formas/visor.html', {'dvisor': posts,"paginas":paginas,"pagina_actual":pagina_actual})
    

# vista Crear 
def crear(request):
    dato_formulario = DeclaraForm(request.POST or None, request.FILES or None)
    if dato_formulario.is_valid():         
        dato_formulario.save()                                  
        messages.success(request,'Creado Correctamente')
        return redirect('visor')      
    return render(request,'formas/crear.html', {'var_formulario': dato_formulario })   

# vista Editar 
def editar(request, IDD):
    decla = declaracion.objects.get(IDDeclaracion = IDD)
    dato_formulario = DeclaraForm(request.POST or None, request.FILES or None, instance = decla )
    if dato_formulario.is_valid() and request.POST: 
        dato_formulario.save()
        messages.success(request,'Modificado Correctamente')
        return redirect('visor')
    return render(request,'formas/editar.html',{'var_formulario': dato_formulario})

# Vista Eliminar
def elimina(request,IDD):
    decla= declaracion.objects.get(IDDeclaracion=IDD)
    decla.delete()    
    return redirect('visor')

# busca todos los clientes que no tenga asignada a un funcionario 
def pendiente(request):
    # clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.all().order_by('Descripcion')  * todos
    # ids_asignacion = Asignacion.objects.values('IDClientes_Proveedores')
    # clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.exclude(ID__in=Subquery(ids_asignacion))
    # busca los clientes que no tienen asignacion 
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Asignacion.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True)             
    
    # es el listado general y la cantidad por pagina 
    paginator = Paginator(clientes_pendientes,8)  
              
    # crear variable page si no existe se pone 1
    pagina = request.GET.get("page") or 1   
    # el posts es la vista como tal de datos_decla a posts que es igual a publicaciones por pagina  
    posts   = paginator.get_page(pagina) 
    # se hace para saber la cantidad de paginas variable 
    pagina_actual  = int(pagina)
    # se define la cantidad de paginas con range en la variable paginas inicia en 1  
    paginas = range(1,posts.paginator.num_pages + 1)    
    # Paginacion se ve la cantidad de objetos en lista  
    return render(request, 'formas/pendientes.html', {'cvisor': posts,"paginas":paginas,"pagina_actual":pagina_actual})    

<<<<<<< Updated upstream
# Filtrar los registros de cliente_proveedor_cliente_proveedor que no tienen asignaciones
# Excluir aquellos registros de cliente_proveedor_cliente_proveedor que estén en Asignacion
# clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.exclude(ID__in=Subquery(ids_asignacion))






# asigna funcionarios 
#def asigna(request):      
  
    datos_funcionario=list(planillas_planilla_funcionarios.objects.values().order_by('Nombre'))
       
    if (len(datos_funcionario)>0):
        data={'message':"Success",'Funcionarios':datos_funcionario}
      
    else:
        data={'message':'No encontrado'}    
    return render(request,'formas/asignacion.html')     
    return JsonResponse(data) # responde los datos     
  
# asigna funcionarios 
def asigna(request):    
    datos_funcionario =planillas_planilla_funcionarios.objects.all().order_by('Nombre')  
    return render(request,'formas/asignacion.html',{'var_Funcionarios': datos_funcionario})        

# busca de clientes por id 
def asignaciones(request, clientes_id):
    clientes=list(cliente_proveedor_cliente_proveedor.objects.filter(clientes_id=cliente_proveedor_cliente_proveedor.IDClientes_Proveedores).values())
    if (len(clientes)>0):
        data ={'message': "Success",'clientes':clientes}
    else:
        data ={'message': "No existe"}
    
    return JsonResponse(data)

# vista para traer todos los clientes 
def Clientes_General(request):
    todos_clientes=list(cliente_proveedor_cliente_proveedor.objects.values())
    
    if (len(todos_clientes)<0):
        data={'message':"Success",'todos':todos_clientes}
    else:
        data={'message': 'No hay datos'}
    return JsonResponse(data)
        
        
=======
  
# asigna funcionarios 
def asigna(request):    
    datos_funcionario =planillas_planilla_funcionarios.objects.all().order_by('Nombre')      
    return render(request,'formas/asignacion.html',{'var_Funcionarios': datos_funcionario})        


# vista para traer todos los clientes 
def Clientes_General(request):
    todos_clientes=list(cliente_proveedor_cliente_proveedor.objects.values())     
    return JsonResponse({'data': list(todos_clientes)})
        
        
# vista para traer los clientes que aun no estan asignados 
def Clientes_pendientes(request):     
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Asignacion.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True)
              
    return JsonResponse({'data':list(clientes_pendientes.values())}) 


# vista para buscar los clientes segun el funcionario       
def Clientes_Funcionario(request,IDD):
    
    clientes_funcionario = Asignacion.objects.filter(
        IDPlanilla_Funcionarios_id=IDD  # busca al funcionario
    ).annotate(
        tiene_asignacion=Exists(
            cliente_proveedor_cliente_proveedor.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores_id')
            )
        ),
        Descripcion=Subquery(
            cliente_proveedor_cliente_proveedor.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores_id')                
            ).values('Descripcion')[:1]
        )
    )
        
    return JsonResponse({'data':list(clientes_funcionario.values())}) 

# es la vista para cargar las declaraciones que tiene asignadas cada cliente segun el funcionario 
def Declaracion_Cliente(request,IDD):
    declaraciones_asignadas = Asignacion.objects.filter(
        IDPlanilla_Funcionarios_id=IDD  # busca al funcionario
    ).select_related('IDDeclaracion')
    
    data = []  
    
    for asignacion in declaraciones_asignadas:
        data.append({
            'iddeclaracion':asignacion.IDDeclaracion.IDDeclaracion,
            'detalle':asignacion.IDDeclaracion.detalle,    
            'codigo':asignacion.IDDeclaracion.codigo,
            'tiempo':asignacion.IDDeclaracion.tiempo,
            'estado':asignacion.IDDeclaracion.estado,
            'presentada':asignacion.Fecha_Presenta,
            'asignada':asignacion.Fecha_Asigna,
        })
                                 
    return JsonResponse(data, safe=False)

# guarda los datos en la tabla asigna 
def Asigna_Declaracion(request,cliente_id,colaborador_id):
    # Obtener instancias de los modelos necesarios
    cliente = get_object_or_404(cliente_proveedor_cliente_proveedor, pk=cliente_id)
    colaborador = get_object_or_404(planillas_planilla_funcionarios, pk=colaborador_id)
    # crea un nuevo registro en la tabla asignacion 
    Asigna = Asignacion.objects.create(                                             
            Fecha_Asigna = date.today(),
            IDClientes_Proveedores_id = cliente_id,
            IDPlanilla_Funcionarios_id = colaborador_id,
            i
            correo = 0     
            )
    # actualiza estado de clientes 
    cliente.Estado = False
    cliente.save()
>>>>>>> Stashed changes
