import json
from django.http import JsonResponse
from django.shortcuts import render
from psutil import users
from django.contrib.auth.models import User


from libreria.models import Asignacion, Parametros_Declaraciones

# levanta pagina
def VsParametros(request):       
       return render(request,'formas/Parametros.html')
   
# muestra todas las asignaciones realizadas para que pueda ver el mes que esta en proceso 
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


# Permite confirmar el cambio de mes de las declaraciones asignadas del modelo de seguridad 
def VsConfirmaMes(request,idd):       
    if request.method == 'POST':   
        try:                               
            asignacion = Asignacion.objects.get(pk=idd)     # se obtiene el objeto de la tabla Asignacion             
            data =json.loads(request.body.decode('utf-8'))  # ver los datos recibidos en el json                                
            mescambio = data.get('mesdato')                 # se obtienen los datos                                                          
            asignacion.Mes = mescambio                      # Actualizar los campos de la tabla asignacion                           
            asignacion.save()                               # Guardar los cambios en la base de datos

            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'}) 
    

# muestra los datos de la linea de parametros 
def VsParametrosDatos(request):
   
    if request.method == 'GET':           
        try:                                               
                # muestra los datos de parametros 
                Total_parametro = Parametros_Declaraciones.objects.all()                                                                                                   
                tparametro = list(Total_parametro.values(     
                        'IDParametros_Declaraciones',
                        'Nombre',
                        'Ubicacion_logo',         
                        'Usuario',
                        'Clave',
                        'Nombre_Base',
                        'Puerto',
                        'Server',
                        'IDCia',    
                        'Ubicacion_logo',
                    ))                                                                  
      
                if tparametro:
                        return JsonResponse(tparametro, safe=False)  # safe=False permite listas
                else:
                        return JsonResponse({'success': False, 'error': 'No se encontraron parámetros'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo GET'})
                
# Actualiza los datos del parametro 
def VsParametrosConfirma(request,IDreg):   
    if request.method == 'POST':   
        try:                               
            vparametros = Parametros_Declaraciones.objects.get(pk=IDreg)   
            data =json.loads(request.body.decode('utf-8'))  # ver los datos recibidos en el json                                
                              
            vnombre = data.get('nombre')                 # se obtienen los datos                                                          
            vbase = data.get('basedatos')
            vpuerto = data.get('puerto')
            vserver = data.get('server')
            vusuario = data.get('usuario')
            vclave = data.get('clave')
            vidc = data.get('idcia')
            vubicacion_logo = data.get('inputGroupFile04')
            
            vparametros.Nombre = vnombre                      # Actualizar los campos de la tabla asignacion                           
            vparametros.Nombre_Base = vbase
            vparametros.Puerto = vpuerto
            vparametros.Server = vserver
            vparametros.Usuario = vusuario
            vparametros.Clave = vclave
            vparametros.IDCia = vidc    
            
             # Validar vubicacion_logo 
            if vubicacion_logo not in [None, '', 'None']:
                vparametros.Ubicacion_logo = vubicacion_logo            
                                      
            vparametros.save()                               # Guardar los cambios en la base de datos
            
            #return JsonResponse(vparametros, safe=False)  
            
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    else:
        return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo POST'}) 
   
   
# registro de Usuarios del Sistema 
def VsRusuarios(request):   
        return render(request,'formas/Usuarios.html')

# Muestra todos los usuarios para verlos en la pantalla     
def VsBuscaUsuarios(request):
       print('llegue')
       if request.method == 'GET':           
        try:                                               
                # muestra los datos de parametros 
                Total_usuarios = User.objects.all()                                                                                                   
                tusuarios = list(Total_usuarios.values(     
                        'id',
                        'username',
                        'first_name',         
                        'last_name',
                        'email',
                        'is_active',                        
                    ))                                                                  
                print('datos',tusuarios)
                if tusuarios:
                        return JsonResponse(tusuarios, safe=False)  
                else:
                        return JsonResponse({'success': False, 'error': 'No se encontraron los usuarios'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
       else:
            return JsonResponse({'success': False, 'error': 'La solicitud no es de tipo GET'})