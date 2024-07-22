from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import logout
from django.shortcuts import redirect
from ctypes import util
from datetime import date, timedelta
from datetime import datetime
import json
import subprocess
from typing import Self
from urllib import request
from django.contrib import messages
from django.forms import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
import psutil
from .models import Asignacion, Declaracion_Clientes, Historico_Declaraciones, calendario_tributario, declaracion, planillas_planilla_funcionarios,cliente_proveedor_cliente_proveedor,Historico_Declaraciones
from django.core.serializers import serialize
from django.core import serializers
from django.db.models import F,Q   
# la clase F funciona para filtrar productos mayores ejemplo productos = Producto.objects.filter(precio__gt=F('descuento'))
# la clase Q funciona para generar consultas correctas 


def login_user(request):
    if request.method=='POST':
        username = request.POST['uname']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.warning(request,'Invalid Credentials')
            return redirect('login')
    return render(request,'login.html')



# carga el diseño del formulario 
from .forms import AsignaDeclaraciones, DeclaraForm
# paginacion 
from django.core.paginator import Paginator
 
from django.db.models import Exists,OuterRef,Subquery

# vista de inicio 
def inicio(request):
    return HttpResponse("<h1>Bienvenido</h1>")

# vista base 
def base(request):
    return render(request,'paginas/base.html')

# vista Clientes
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
def pendientedeasignar(request):    
    clientes_pendientes = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Asignacion.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True)             
    return JsonResponse({'data': list(clientes_pendientes)})
  
        
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
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True)             
    
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
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True)
              
    return JsonResponse({'data':list(clientes_pendientes.values())}) 


# vista para buscar los clientes que tiene asignado el funcionario       
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

# muestra todas las declaraciones que tiene el cliente asignadas 
def vsDeclaraciones_Cliente(request,IDD):
    declaraciones_asignadas = Asignacion.objects.filter(
        IDClientes_Proveedores=IDD  # busca al funcionario
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
            IDDeclaracion_id = 13,
            correo = 0     
            )
    # actualiza estado de clientes 
    cliente.Estado = False
    cliente.save()
        
   # Envía una respuesta JSON indicando éxito
    return JsonResponse({'success': True})

# esta funcion cargo los provee
def Asigna_Declaracion_Clientes(request):
    todos_clientes = cliente_proveedor_cliente_proveedor.objects.all().order_by('Descripcion')  
    return render(request,'formas/declaracion_clientes.html',{'data':todos_clientes})    

# esta funcion solo carga la pagina declaracion_clientes
def VsListaclientes(request):     
   #return JsonResponse({'success': True})   
   return render(request,'formas/declaracion_clientes.html') 

# muestra todos los cliente en el combo donde su estado este true 
def VsListaclientesdatosa(request):
    try:
        todos_clientes = cliente_proveedor_cliente_proveedor.objects.filter(Estado=True, Tipo=True).order_by('Descripcion').values()
        return JsonResponse({'data': list(todos_clientes)})
    except Exception as e:
        return JsonResponse({'error': 'Error al obtener los datos de clientes'}, status=500) 

# debe de mostrar los clientes que no tienen asignada una declaracion 
def VsClientessindeclaraciones(request):     
    clientes_sin_declaraciones = cliente_proveedor_cliente_proveedor.objects.annotate(
        tiene_asignacion=Exists(
            Declaracion_Clientes.objects.filter(
                IDClientes_Proveedores=OuterRef('IDClientes_Proveedores')
                )
            )
        ).filter(tiene_asignacion=False,Estado = True,Tipo = True).order_by('Descripcion')
              
    return JsonResponse({'data':list(clientes_sin_declaraciones.values())}) 

# debe de mostrar solo las declaraciones asignadas al cliente 
def VDeclaracion_Cliente_asignacion(request,IDD):    
    declaraciones_asignadas = Declaracion_Clientes.objects.filter(
        IDClientes_Proveedores_id=IDD  # busca al Cliente
    ).select_related('IDDeclaracion')
    
    data = []  
    
    for declarac in declaraciones_asignadas:
        data.append({
            'iddeclaracion_clientes':declarac.IDDeclaracion_Clientes,
            'codigo':declarac.IDDeclaracion.codigo,
            'detalle':declarac.IDDeclaracion.detalle,
            'fecha':declarac.Fecha_Asigna,    
            'estado':declarac.Estado,
            'tiempo':declarac.Observacion,            
        })                     
    return JsonResponse(data, safe=False)

# Vista Elimina la declaracion del cliente 
def velimina_declaracion_cliente(request,IDD):
    decla= Declaracion_Clientes.objects.get(IDDeclaracion_Clientes=IDD)
    decla.delete()    
   # return JsonResponse({'success': True})
    return redirect('clientes_declaraciones')

# busca las declaraciones que no tiene asignado el cliente 
def vdeclaraciones_sin_asignar_al_cliente(request, IDD):
    # Obtener todas las declaraciones que no están asignadas al cliente
    declaraciones_no_asignadas = declaracion.objects.exclude(
        declaracion_clientes__IDClientes_Proveedores_id=IDD
    ).order_by('codigo').values()
    
    return JsonResponse(list(declaraciones_no_asignadas), safe=False)

# esta vista agrega nuevas declaraciones al cliente 
def vagregarunadeclaracion(request):
    if request.method == 'POST':
        data = json.loads(request.body)                                
        cliente_id = data.get('clienteID', None)
        declaracion_id = data.get('declaracionID', None)                                
        if cliente_id is None or declaracion_id is None:
            return JsonResponse({'error': 'IDs de cliente o declaración faltantes'}, status=400)

        try:
            fecha_asigna = datetime.strptime(data['Fecha_Asigna'], '%d/%m/%Y').strftime('%Y-%m-%d')
            
            nueva_declaracion_cliente = Declaracion_Clientes.objects.create(
                Fecha_Asigna=fecha_asigna,
                Estado=data['Estado'],
                Observacion=data['Observacion'],
                IDClientes_Proveedores_id=cliente_id,
                IDDeclaracion_id=declaracion_id,
            )            
            return JsonResponse({'message': 'Declaración de cliente creada correctamente'}, status=201)
        except Exception as e:
            print('Error al crear la declaración de cliente:', str(e))
            return JsonResponse({'error': 'Error al crear la declaración de cliente'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
# asigna las declaraciones al funcionario 
def clienteafuncionario(request):    
    if request.method == 'POST':  
        try:                          
            data = json.loads(request.body)                                   
            clientepend_id = data.get('IDClientes_Proveedores', None) 

            # Validar la presencia de datos importantes
            if 'IDClientes_Proveedores' not in data or 'IDPlanilla_Funcionarios' not in data or 'Fecha_Asigna' not in data:
                return JsonResponse({'error': 'Campos requeridos faltantes'}, status=400)
            
            #clientepend_id  = list(cliente_proveedor_cliente_proveedor.objects.values().filter(Tipo=True).order_by('Descripcion') 
            
            #clientepend_id=list(cliente_proveedor_cliente_proveedor.objects.values().filter(estado=True).order_by('codigo')) 
            
            print('declaracion',clientepend_id)

            cliente_proveedor_instance = cliente_proveedor_cliente_proveedor.objects.filter(Tipo=1).get(pk=clientepend_id)             
            
            print('cliente',cliente_proveedor_instance)
            funcionario_id = data.get('IDPlanilla_Funcionarios', None)
            print('funcionario',funcionario_id)
            funcionario_instance = planillas_planilla_funcionarios.objects.get(pk=funcionario_id) 
             
            print(clientepend_id,funcionario_id)
            if clientepend_id is None or funcionario_id is None:
                return JsonResponse({'error': 'IDs de cliente o funcionario faltantes'}, status=400)

            fecha = datetime.strptime(data['Fecha_Asigna'], '%d/%m/%Y').strftime('%Y-%m-%d')
                    
            # Obtener todas las declaraciones del cliente cliente_proveedor_instance
            print("Cliente instancia",cliente_proveedor_instance)
            
            #Declaraciones_cliente = Declaracion_Clientes.objects.values().filter(IDClientes_Proveedores=clientepend_id)
            declaraciones_cliente = Declaracion_Clientes.objects.filter(IDClientes_Proveedores=clientepend_id)
            
            print('asignado',declaraciones_cliente)  
            # Crear las asignaciones con las declaraciones del cliente
            for declaracion in declaraciones_cliente:
                print(declaracion)
                Asignacion.objects.create(
                    Fecha_Presenta=fecha,
                    Fecha_Asigna=fecha,
                    Fecha_Proxima=fecha,
                    correo=False,
                    IDClientes_Proveedores=cliente_proveedor_instance,
                    IDPlanilla_Funcionarios=funcionario_instance,
                    IDDeclaracion=declaracion.IDDeclaracion,
                )  
            
            return JsonResponse({'message': 'Asignacion a funcionario creada correctamente'}, status=201)
        except KeyError as e:
            return JsonResponse({'error': f'Campo requerido faltante: {e}'}, status=400)
        
        except cliente_proveedor_cliente_proveedor.DoesNotExist:
            return JsonResponse({'error': 'Cliente  no encontrado'}, status=404)
        
        except planillas_planilla_funcionarios.DoesNotExist:
            return JsonResponse({'error': 'Funcionario no encontrado'}, status=404)
        
        except Exception as e:
            print('Error al crear la asignación a funcionario:', str(e))
            return JsonResponse({'error': 'Error interno al procesar la solicitud'}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    


# desasigna cliente a funcionario  quita los clientes a un funcionario  
def vsdesasignaclienteafuncionario(request, IDD):    
    try: 
        # Intenta obtener la asignación por IDClientes_Proveedores al funcionario con filter se logra no con get 
        asignacion = Asignacion.objects.filter(IDClientes_Proveedores=IDD)
        
        # Elimina la asignación encontrada
        asignacion.delete()
        
        # Devuelve una respuesta JSON de éxito
        return JsonResponse({'success': True})
    
    except ObjectDoesNotExist:
        # Si no se encuentra la asignación, devuelve un error 404
        return JsonResponse({'error': 'La asignación no existe'}, status=404)
    
    except Exception as e:
        # Para otros errores, devuelve un error 500 junto con el mensaje de error
        return JsonResponse({'error': str(e)}, status=500)
   

  
# abre el formulario de busqueda de declaracion 
def vbuscadeclaracion(request):
    return render(request,'formas/Busca_Declaracion_Clientes.html')

# abre el formulario de busqueda de declaracion --- revisar muestra todas las declaraciones -- 
def vbuscadeclaraciondatos(request):
    todas_declaraciones=list(declaracion.objects.values().filter(estado=True).order_by('codigo'))       
    return JsonResponse({'ldeclaraciones': list(todas_declaraciones)})  

# busca declaraciones asociadas a un cliente 
def vbuscadeclaraciondatosclientes(request,IDD):    
    declaraciones_asignadas = Declaracion_Clientes.objects.filter(
    IDDeclaracion=IDD  # busca declaraciones 
    ).select_related('IDClientes_Proveedores').values('IDClientes_Proveedores', 'IDClientes_Proveedores__IDClientes_Proveedores', 'IDClientes_Proveedores__Descripcion','IDClientes_Proveedores__Fecha_Ult_Movimiento','IDClientes_Proveedores__Estado')       
           
    return JsonResponse({'data': list(declaraciones_asignadas)})  
    
# activa la pantalla de activacion 
def viniciadeclaracion(request): 
    return render(request,'formas/inicia_Declaracion.html')    

#lista de funcionarios 
def vsfuncionarios(request):    
    datos_funcionario =list(planillas_planilla_funcionarios.objects.values().order_by('Nombre'))    
    return JsonResponse({'datafuncionario': list(datos_funcionario) })  
           
# busca las declaraciones que tiene asignada un cliente segun el funcionario ´prefetch_related()´
def vsfuncionarioinicia(request,idd2,idd):  
    declaraciones_cliente =Asignacion.objects.filter(
        IDClientes_Proveedores = idd2, 
        IDPlanilla_Funcionarios = idd
    ).select_related('IDDeclaracion')            

    datadeclaracion =list(declaraciones_cliente.values(
         'IDAsignacion',  
         'IDDeclaracion__codigo',  
         'IDDeclaracion__detalle', 
         'Fecha_Presenta',           
         'Fecha_Asigna', 
         'IDDeclaracion__tiempo',
         'IDPlanilla_Funcionarios',  
         'IDDeclaracion__estado',                         
         'correo', 
         'IDAsignacion',                   
         'Fecha_Proxima',
         'Iniciada',
         'Suspendida'
    ))
    
    return JsonResponse(datadeclaracion, safe =False) 

# actualiza los campos de la tabla       
def vsActivaDeclaracion(request, idd):  
    if request.method=='GET':

       try:      
         asignacion = Asignacion.objects.filter(pk=idd).first()                                                   
         declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                          
                     
         if declaracion_obj:                                                   
            # actualiza campos 
            asignacion.Iniciada = True
            asignacion.Fecha_Asigna = date.today()   
            asignacion.Fecha_Proxima = asignacion.Fecha_Presenta + timedelta(days=int(declaracion_obj.tiempo))#                                                                                               
            
            # Guarda los campos
            asignacion.save()
            #historico_declaraciones.save()
            
            return JsonResponse({'success':True})
         else:
             return JsonResponse({'success': False, 'error': 'No se encontró ninguna declaración relacionada'}) 
       except Exception as e:
           return JsonResponse({'success': False,'error': str(e)})         
    else:
           return JsonResponse({'success': False,'error': 'No se Guardaron los datos'})         



# actualiza los campos de la tabla para cerrar la declaracion 
def vsCierraDeclaracion(request, idd): 
    if request.method == 'GET':            
        try:                      
            asignacion = Asignacion.objects.filter(pk=idd).first()  
            declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                  
            if declaracion_obj:         
                # Crear registro en Historico_Declaraciones
                Historico_Declaraciones.objects.create(                                             
                    IDAsignacion=idd,
                    Fecha_Presenta=asignacion.Fecha_Presenta,
                    Fecha_Asigna=asignacion.Fecha_Asigna,
                    Fecha_Proxima=asignacion.Fecha_Proxima,
                    Fecha_Cierre=date.today(),
                    correo=False,
                    Iniciada=asignacion.Iniciada,
                    Suspendida=asignacion.Suspendida,
                    Usuario_Cierre='S/A',  
                    Numero_Comprobante='',
                    Fecha_Final=None,
                    IDClientes_Proveedores=asignacion.IDClientes_Proveedores,
                    IDPlanilla_Funcionarios=asignacion.IDPlanilla_Funcionarios,
                    IDDeclaracion=asignacion.IDDeclaracion
                )
                
                # Actualizar campos en Asignacion
                asignacion.Iniciada = False
                asignacion.Suspendida = False
                asignacion.Fecha_Presenta = asignacion.Fecha_Proxima
                
                # Guardar cambios en Asignacion
                asignacion.save()
                                
                return JsonResponse({'success': True})
        except Exception as e:        
            return JsonResponse({'success': False, 'error': str(e)})         
    else:         
        return JsonResponse({'success': False, 'error': 'No se Guardaron los datos'})
       

# suspende declaracion 
def vsSuspendeDeclaracion(request,idd):     
 if request.method=='GET':             
    try:                      
        asignacion = Asignacion.objects.filter(pk=idd).first()            
        declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                  
        if declaracion_obj:                        
         # actualiza campos         
         asignacion.Suspendida = True             
         # Guarda los campos                
         asignacion.save()        
        return JsonResponse({'success':True})
    except Exception as e:        
        return JsonResponse({'success': False,'error': str(e)})         
 else:    
        return JsonResponse({'success': False,'error': 'No se Guardaron los datos'})   
       
# salir de la aplicacion
#def exit_confirmation(request):    
    #if request.method == 'POST':
    # salida confirmada solicitud POST 
    #    return HttpResponseRedirect('/salir-confirmado/')  # Redirecciona a una página de confirmación 
    #else:        
    #    return render(request, 'formas/salir.html')

# cierra la aplicacion     
#def cerrar_aplicacion():
    # Detener el servidor de desarrollo de React
    
   # subprocess.run(["pkill", "-f", "react-scripts"])

    # Detener el servidor de desarrollo de Django
   # subprocess.run(["pkill", "-f", "runserver"])

    #if __name__ == "__main__":
    # Aquí iría tu código para iniciar la aplicación Django
    # Por ejemplo, podrías iniciar el servidor de desarrollo de Django y el servidor de desarrollo de React
    # Luego, cuando necesites cerrar la aplicación, llamas a la función cerrar_aplicacion()
    #return render(request, 'Declaraciones/libreria/templates/formas/salir.html')



# ve el Status de las declaraciones        
def VstatusDeclaracion(request):       
     # apertura el formulario de Visor de Status 
    return render(request, 'formas/Status.html')


# Ver Status de Declaracion - muestra todos los datos de las declaraciones  
def VsEstatusDeclaracion(request): 
    Total_Declaraciones = Asignacion.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).all().order_by("Fecha_Presenta")
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDDeclaracion',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__estado',
        'Iniciada',
        'Suspendida'
    ))

    return JsonResponse(datadeclaracion, safe=False)

# suspende las declaraciones que el funcionario esta trabajando 
def VsActivaSuspendida(request,idd):
    if request.method=='GET':

       try:      
         asignacion = Asignacion.objects.filter(pk=idd).first()                                                   
         declaracion_obj = declaracion.objects.filter(IDDeclaracion=asignacion.IDDeclaracion.IDDeclaracion).first()                          
                     
         if declaracion_obj:                                                   
            # actualiza campos 
            asignacion.Suspendida = False                         
            # Guarda los campos
            asignacion.save()
            return JsonResponse({'success':True})
         else:
             return JsonResponse({'success': False, 'error': 'No se encontró ninguna declaración relacionada'}) 
       except Exception as e:
           return JsonResponse({'success': False,'error': str(e)})         
    else:
           return JsonResponse({'success': False,'error': 'No se Guardaron los datos'})  
       
# carga el calendario tributario        
def VsCalendario(request): 
    return render(request,'formas/calendario.html')    

# carga el confirmador de declaraciones
def VsConfirmaDeclaracion(request): 
    return render(request,'formas/Confirma_Declaraciones.html')    

# Ver Status de Declaracion - muestra todos los datos de las declaraciones filtra si el numero de comprobante
# es vacio o nulo
def VsEstatusDeclaracionHistoricas(request): 
    Total_Declaraciones = Historico_Declaraciones.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).filter(
        Q(Numero_Comprobante__isnull=True) | Q(Numero_Comprobante='')
    ).order_by("Fecha_Cierre")             
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDHistorico_Declaraciones',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'IDClientes_Proveedores__IDClientes_Proveedores',
        'IDClientes_Proveedores__Descripcion',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'Fecha_Cierre',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__estado'                
    ))

    return JsonResponse(datadeclaracion, safe=False)

# Confirma las declaraciones cerradas y presentadas para archivo          
def VsConfirma(request, idd):     
    if request.method == 'POST':
        try:
            # se obtiene el objeto historico 
            historico_declaracion = Historico_Declaraciones.objects.get(pk=idd)
            # ver los datos recidos en el json 
            data =json.loads(request.body.decode('utf-8'))
            #print('datos recibido',data )            
            # se obtienen los datos                                
            correo = data.get('correo')           
                        
            # Actualizar los campos en el objeto historico_declaracion
            historico_declaracion.Numero_Comprobante = data.get('numero_comprobante')  
            historico_declaracion.Fecha_Final = data.get('fecha_cierre')
            historico_declaracion.correo = True if correo =='Si' else False 
                                          
            # Guardar los cambios en la base de datos
            historico_declaracion.save()

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'})

# levanta el formulario para la declaracion historico cerrada 
def VsDeclaracionesConfirmadasCerradas(request):       
        return render(request,'formas/Declaraciones_Confirmadas.html')   
    
# Muestra las declaraciones cerradas y archivadas     
def VsDeclaracionesConfirmadasCerradasAplicadas(request):        
    Total_Declaraciones = Historico_Declaraciones.objects.select_related(
        'IDClientes_Proveedores', 
        'IDPlanilla_Funcionarios', 
        'IDDeclaracion'
    ).filter(
        Q(Numero_Comprobante__isnull = False) & ~Q(Numero_Comprobante='')
    ).order_by("-Fecha_Cierre")
                   
    
    datadeclaracion = list(Total_Declaraciones.values(
        'IDHistorico_Declaraciones',  # Acceder al ID de la declaración relacionada
        'IDDeclaracion__codigo',
        'IDDeclaracion__detalle',
        'IDClientes_Proveedores__IDClientes_Proveedores',
        'IDClientes_Proveedores__Descripcion',
        'Fecha_Asigna',
        'Fecha_Presenta',
        'Fecha_Cierre',
        'IDPlanilla_Funcionarios__Nombre',  # Acceder al nombre del funcionario
        'IDDeclaracion__estado',
        'correo',
        'Numero_Comprobante',
        'Fecha_Final'                
    ))
    print('Detalle Encontrado',Total_Declaraciones)
    return JsonResponse(datadeclaracion, safe=False)


# busca la fecha donde se quieren sacar las declaraciones 
def VsBuscaporfecha(request, fecha):
  
    try:                
        Total_Declaracion = calendario_tributario.objects.filter(Fecha_Presenta=fecha).order_by("-Fecha_Presenta")
        
        datadeclaracion = list(Total_Declaracion.values(
            'IDCalendario_tributario',            
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'IDDeclaracion__tiempo',
            'IDDeclaracion__observaciones'
        ))
     
        return JsonResponse(datadeclaracion, safe=False)
    
    except Exception as e:
        # Manejo genérico de errores, imprime el error en la consola del servidor
        print('Error en consulta:', e)
        return JsonResponse({'error': str(e)}, status=500)

# realiza la inclusion de la nueva declaracion al calendario de declaraciones     
def VsAgregaDeclaracionCalendario(request,fch):
    if request.method == 'POST':     
           
        data = json.loads(request.body.decode('utf-8')) 
        #print('Fecha recibida',fch,data)                                                                                                    
        #declaracion_obj = declaracion.objects.get(id=declaracion_id)        
        declaracion_id = data.get('IDDeclaracion', None)                 
        observaciones = data.get('Observaciones',None)                                   
        
        try:       
            # Verificar si existe una instancia válida de declaracion con el ID proporcionado            
            declaracion_instance = declaracion.objects.get(IDDeclaracion=declaracion_id)
            print('ver',declaracion_instance)
            # Verificar si ya existe una entrada en calendario_tributario con esta declaración
            if calendario_tributario.objects.filter(
                IDDeclaracion=declaracion_instance,
                Fecha_Presenta = fch).exists():
                                
                return JsonResponse({'error': 'Esta declaración ya está incluida en el calendario'}, status=400)                      
    
            
            nueva_declaracion_calendario = calendario_tributario.objects.create(
                Fecha_Presenta=fch,                
                Observaciones=observaciones,
                IDDeclaracion=declaracion_instance,
            )     
                                                   
            
            return JsonResponse({'message': 'Declaración incluida'}, status=201)
        except Exception as e:  
            print('Error:', str(e))          
            return JsonResponse({'error': 'Error al crear al asignar la declaración '}, status=500)
    else:
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
# elimina la declaracion del calendario tributario
def VsCalendario_Tributario_lineaBorra(request,linea):  
    try:                       
        decla= calendario_tributario.objects.get(IDCalendario_tributario=linea)    
        decla.delete()    
        return JsonResponse({'message': 'Eliminado correctamente'}, status=200)
    except calendario_tributario.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)   
    
# levanta el formulario para el calendario tributario ve todo lo calendarizado por año y mes 
def VsCalendarioTributario(request):    
    return render(request,'formas/Calendario_Tributario.html')       
 
# busca las declaraciones del año solicitado 
def VsBuscadeclaracionxan(request, anSeleccionada):
   # an_Selecionado = int(anSeleccionada) # convierte el año        
    try:                  
        an = int(anSeleccionada) 
                         
        
        Total_Declaraciones = calendario_tributario.objects.filter(Fecha_Presenta__year = an
        ).order_by("-Fecha_Presenta")  
          
        print('total',Total_Declaraciones) 
        
            
        datadeclaracion = list(Total_Declaraciones.values(
            'IDCalendario_tributario',            
            'IDDeclaracion__codigo',
            'IDDeclaracion__detalle',
            'Fecha_Presenta'            
        ))
     
             
        return JsonResponse(datadeclaracion, safe=False)        
                                        
    except calendario_tributario.DoesNotExist:
        return JsonResponse({'error': 'El objeto no existe'}, status=404)
    except ValueError:
        return JsonResponse({'error': 'El año proporcionado no es válido'}, status=400)
    except Exception as e:
        print(f"Error: {e}")  # Imprime el error en la consola
        return JsonResponse({'error': str(e)}, status=500)   
    
# Salir del Sistema 
#def VsSalirSistema(request): 
    return render(request, 'formas/Salida.html')



# cierra todos los procesos abiertos 
#def exit_application_old(request):   
    try:
        # Obtener todos los procesos que contienen "runserver"
        for proc in util.process_iter(['pid', 'name']):
            if 'runserver' in proc.info['name']:
                proc.kill()
                print(f"Servidor con PID {proc.info['pid']} cerrado correctamente.")
        
        print("Servidor(es) cerrado(s) correctamente.")
    except Exception as e:
        print(f"Error al cerrar el servidor: {e}")

    return redirect('/')

# cierra solo este proceso 
#def exit_application_old1(request):   
    try:
        # Iterar sobre todos los procesos
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'python' in proc.info['name'].lower() and 'runserver' in proc.cmdline():
                # Verificar que sea el proceso correcto
                if '--noreload' in proc.cmdline() or '--nothreading' in proc.cmdline():
                    proc.kill()
                    subprocess.run(["pkill", "-f", "runserver"])
                    print(f"Servidor con PID {proc.info['pid']} cerrado correctamente.")
                    break  # Salir del bucle después de cerrar el proceso
        
        print("Servidor cerrado correctamente.")
    except Exception as e:
        print(f"Error al cerrar el servidor: {e}")

    return redirect('/')

#def exit_application_old1(request):   
    try:
        # Iterar sobre todos los procesos
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            if 'python' in proc.info['name'].lower() and 'runserver' in proc.cmdline():
                # Verificar que sea el proceso correcto
                if '--noreload' in proc.cmdline() or '--nothreading' in proc.cmdline():
                    proc.kill()
                    subprocess.run(["pkill", "-f", "runserver"])
                    print(f"Servidor con PID {proc.info['pid']} cerrado correctamente.")
                    break  # Salir del bucle después de cerrar el proceso
        
        print("Servidor cerrado correctamente.")
    except Exception as e:
        print(f"Error al cerrar el servidor: {e}")

    return redirect('/')

#def exit_application(request):   


    logout(request)    
    return redirect('/')

#@login_required
#def perfil(request):
    # Vista de ejemplo protegida, solo accesible por usuarios autenticados
    return render(request, 'perfil.html')



# busca las declaraciones del año solicitado 
def VsReasignadeclaracion(request):    
     return render(request,'formas/Calendario_Tributario_Reasigna.html')       
 
 
 
 
