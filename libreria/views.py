from typing import Self
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from .models import Asignacion, declaracion, planillas_planilla_funcionarios,cliente_proveedor_cliente_proveedor

# carga el diseño del formulario 
from .forms import AsignaDeclaraciones, DeclaraForm
# paginacion 
from django.core.paginator import Paginator
 
from django.db.models import Exists,OuterRef

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
        
        
