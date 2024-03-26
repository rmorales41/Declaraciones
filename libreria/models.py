from django.db import models
 

class declaracion(models.Model):
    id=models.AutoField(primary_key=True)   
    codigo = models.CharField(max_length =10, verbose_name='Código') 
    detalle = models.CharField(max_length =100 ,null =True) 
    tiempo = models.DecimalField(default = 30, max_digits = 5,decimal_places = 0,verbose_name='Tiempo') 
    estado = models.BooleanField(default = True)
    observaciones = models.TextField(blank=True, verbose_name='Observacion')
    imagen = models.ImageField(upload_to='imagenes/', null=False, verbose_name='Imagen')

    
    def __str__(self):
        fila = "Codigo: " + self.codigo + " - " + "Detalle: " + self.detalle 
        return fila 
    
    # borrar fisico de la imagen 
    def delete(self, using=None, keep_parents=False):
        self.imagen.storage.delete(self.imagen.name)
        super().delete()