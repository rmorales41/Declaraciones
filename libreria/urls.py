
from django.urls import path
from . import views
 
# asi con estos dos se maneja eel inventario
from django.conf import settings
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('',views.visor, name = 'visor'),
    path('nosotros/',views.nosotros, name='nosotros'),
    path('clientes/',views.clientes, name= 'clientes'),
    path('base',views.base, name= 'base'),
    path('visor',views.visor,name='visor'),
    path('crear',views.crear,name='crear'),
    path('editar/<int:IDD>',views.editar,name='editar'),
    path('elimina/<int:IDD>',views.elimina,name='elimina'),  
    path('asigna',views.asigna,name='asigna'),  
    path('pendiente',views.pendiente,name='pendiente'),  
    path('clientesgeneral/', views.Clientes_General, name='clientesgeneral'),
    path('clientespendientes/', views.Clientes_pendientes, name='clientespendientes'),
    path('asignaciones/<int:IDD>', views.Clientes_Funcionario, name='asignaciones'),
    path('declaracionxcliente/<int:IDD>',views.Declaracion_Cliente, name='declaracionxcliente'),
    path('asigna_declaracion_clientes',views.Asigna_Declaracion_Clientes, name='asigna_declaracion_clientes'),
    path('asigna_declaracion/<int:cliente_id>/<int:colaborador_id>',views.Asigna_Declaracion, name='asigna_declaracion'),
    path('clientes_declaraciones/',views.VsListaclientes,name ='clientes_declaraciones'),  
    path('Carga_Clientes_Sin_Declaracion/',views.VsClientessindeclaraciones,name='Carga_Clientes_Sin_Declaracion'),
    path('VsListaclientesdatos/',views.VsListaclientesdatos,name ='VsListaclientesdatos'),
    path('BuscarDeclaracionxCliente/<int:IDD>',views.VDeclaracion_Cliente_asignacion,name ='BuscarDeclaracionxCliente'),
    path('elimina_declaracion_cliente/<int:IDD>',views.velimina_declaracion_cliente,name='elimina_declaracion_cliente'),  
    path('busca_declaraciones_xclientessinasignar/<int:IDD>',views.vdeclaraciones_sin_asignar_al_cliente,name='busca_declaraciones_xclientessinasignar'),  
    path('agreganuevadeclaracion',views.vdeclaraciones_sin_asignar_al_cliente,name='agreganuevadeclaracion'),  
    path('vagregarunadeclaracion/',views.vagregarunadeclaracion,name='vagregarunadeclaracion'),   
    path('agregarclientefuncionario/',views.clienteafuncionario,name='agregarclientefuncionario'),  
    path('desasignaclienteafuncionario/<int:IDD>',views.vsdesasignaclienteafuncionario,name='desasignaclienteafuncionario'),  
    path('buscadeclaracion',views.vbuscadeclaracion,name='buscadeclaracion'),
    path('buscadeclaraciondatos/',views.vbuscadeclaraciondatos,name='buscadeclaraciondatos'),  
    path('buscadeclaraciondatosclientes/<int:IDD>',views.vbuscadeclaraciondatosclientes,name='buscadeclaraciondatosclientes'),         
    path('iniciadeclaracion/',views.viniciadeclaracion,name='iniciadeclaracion'),         
    path('dfuncionarios/',views.vsfuncionarios,name='dfuncionarios'),       
    path('funcionarioinicia/<int:idd2>/<int:idd>/',views.vsfuncionarioinicia,name='funcionarioinicia'),      
    path('declaracionxcliente_asignadas/<int:IDD>',views.vsDeclaraciones_Cliente, name='declaracionxcliente_asignadas'),      
    path('IniciaDeclaracion',views.vsDeclaraciones_Cliente, name='IniciaDeclaracion'),         
    path('ActivaDeclaracion_b/<int:idd>',views.vsActivaDeclaracion, name='ActivaDeclaracion_b'),
    path('CierraDeclaracion/<int:idd>',views.vsCierraDeclaracion, name='CierraDeclaracion'),
    path('SuspendeDeclaracion/<int:idd>',views.vsSuspendeDeclaracion, name='SuspendeDeclaracion'),
    path('StatusDeclaracion/',views.VstatusDeclaracion, name='StatusDeclaracion'),
    path('VerDeclaracion/',views.VsEstatusDeclaracion, name='VerDeclaracion'),
    path('ActivaSuspendida/<int:idd>',views.VsActivaSuspendida,name ='ActivaSuspendida'),
    path('calendario/',views.VsCalendario,name ='calendario'),
    path('ConfirmaDeclaracion/',views.VsConfirmaDeclaracion,name ='ConfirmaDeclaracion'),
    path('VerDeclaracionHistoricas/',views.VsEstatusDeclaracionHistoricas, name='VerDeclaracionHistoricas'),    
    path('Confirma/<int:idd>',views.VsConfirma, name='Confirma'),    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    