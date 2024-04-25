from django.db import models
 
    
class declaracion(models.Model):
    IDDeclaracion=models.AutoField(primary_key=True)   
    codigo = models.CharField(max_length =10, verbose_name='Código', unique=True) 
    detalle = models.CharField(max_length =100 ,null =True) 
    tiempo = models.DecimalField(default = 30, max_digits = 5,decimal_places = 0,verbose_name='Tiempo') 
    estado = models.BooleanField(default = True)
    observaciones = models.TextField(blank=True, verbose_name='Observacion')
    imagen = models.ImageField(upload_to='imagenes/', null=True, verbose_name='Imagen')

    
    def __str__(self):
        fila = "Codigo: " + self.codigo + " - " + "Detalle: " + self.detalle 
        return fila 
    
    # borrar fisico de la imagen 
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()
        
class planillas_planilla_funcionarios(models.Model):
    IDPlanilla_Funcionarios = models.AutoField(primary_key=True)
    Nombre = models.CharField(max_length=20)
    
class cliente_proveedor_cliente_proveedor(models.Model):    
    IDClientes_Proveedores = models.AutoField(primary_key=True)
    Descripcion = models.CharField(max_length=180) 
    Direccion = models.TextField(null=True)
    Email =  models.CharField(max_length=250, null = True) 
    Fecha_Ult_Movimiento = models.DateTimeField(null=True)  
    Estado = models.BooleanField(default=True)
    
    def __str__(self):
        return "{}".format(self.nombre)
                      
class Asignacion(models.Model):
    IDAsignacion = models.AutoField(primary_key=True)
    Fecha_Presenta = models.DateField(blank=True,null=True, verbose_name='Fecha_Presenta')
    Fecha_Asigna = models.DateField(blank=True,null=True, verbose_name='Fecha_Asigna')
    Fecha_Proxima = models.DateField(blank=True,null=True, verbose_name='Fecha_Proxima')
<<<<<<< Updated upstream
=======
    correo =models.BooleanField(default=False)
>>>>>>> Stashed changes
      
    # llaves foraneas 
    IDClientes_Proveedores = models.ForeignKey(cliente_proveedor_cliente_proveedor, on_delete=models.CASCADE) 
    IDPlanilla_Funcionarios = models.ForeignKey(planillas_planilla_funcionarios, on_delete=models.CASCADE)
    IDDeclaracion = models.ForeignKey(declaracion, null=False, blank=False,  on_delete=models.CASCADE)           
    
    def __str__(self):
        return "{}".format(self.descripcion)