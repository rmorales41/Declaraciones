
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
    path('editar',views.editar,name='editar'),
    path('excluir',views.excluir,name='excluir'),    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
