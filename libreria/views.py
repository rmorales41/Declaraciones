from django.http import HttpResponse
from django.shortcuts import render, redirect

from .models import declaracion
# carga el diseño del formulario 
from .forms import DeclaraForm

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
    datos_decla = declaracion.objects.all()
   # print(datos_decla)
    return render(request, 'formas/visor.html', {'dvisor': datos_decla})

# vista Crear 
def crear(request):
    dato_formulario = DeclaraForm(request.POST or None, request.FILES or None)
    if dato_formulario.is_valid():
       dato_formulario.save()     
       return redirect('visor')
    return render(request,'formas/crear.html', {'var_formulario': dato_formulario })

# vista Editar 
def editar(request):
    return render(request,'formas/editar.html')

# Vista Excluir 
def excluir(request):
    return render(request,'formas/excluir.html')
