from django.db import models
from django.utils import timezone
from Huellitas import settings

# Create your models here.
TIPO_CHOICES= [
    ('Alimento', 'Alimento'),
    ('Ropa', 'Ropa'),
    ('Accesorio', 'Accesorio')
    ]

class Paises(models.Model):

    nombre = models.TextField(max_length = 30)

    class Meta:
        verbose_name_plural = "Paises"

class Provincias(models.Model):

    nombre = models.TextField(max_length = 30)
    pais = models.ForeignKey(Paises, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = "Provincias"

class Localidades(models.Model):

    nombre = models.TextField(max_length = 30)
    provincia = models.ForeignKey(Provincias, on_delete = models.CASCADE)
    cod_postal = models.TextField(max_length = 30, null = True)

    class Meta:
        verbose_name_plural = "Localidades"

    def __str__(self):
        return self.nombre

class Proveedores(models.Model):

    razon_social = models.TextField(max_length = 30)
    cuit = models.TextField(max_length = 30)
    direccion = models.TextField(max_length = 30, blank = True, default = "")
    telefono = models.TextField(max_length = 30, blank = True, default = "")
    email = models.EmailField(blank = True, default = "")
    localidad = models.ForeignKey(Localidades, on_delete = models.CASCADE, null= True)
   
    class Meta:
        verbose_name_plural = "Proveedores"

    def __str__(self):
        return self.razon_social



class Articulos(models.Model):

    descripcion = models.TextField(max_length = 30)
    stock = models.IntegerField()
    marca = models.TextField(max_length = 30, null= True)
    tipo = models.TextField(max_length = 30, null= True, choices = TIPO_CHOICES)
    articulo_proveedor = models.TextField(max_length = 30, blank = True, default = "", null = True)
    proveedor = models.ForeignKey(Proveedores, on_delete = models.CASCADE, blank = True, default = "")
    precio_costo = models.DecimalField(max_digits=7, decimal_places=2)
    precio_vta = models.DecimalField(max_digits=7, decimal_places=2)
    fecha_actualizacion = models.DateField(default=timezone.now)

    class Meta:
        verbose_name_plural = "Articulos"



class Configuracion_Listas(models.Model):

    proveedor = models.ForeignKey(Proveedores, on_delete = models.CASCADE)
    cabecera = models.TextField(max_length = 30)
    tipo_archivo = models.TextField(max_length = 30)
    delimitador = models.TextField(max_length = 1, null= True)
   
    class Meta:
        verbose_name_plural = "Configuracion Listas"

class Configuracion_Columnas(models.Model):

    decimal = models.TextField(max_length = 10, blank = True, null = True)
    miles = models.TextField(max_length = 10, blank = True, null = True)
    columna_archivo = models.TextField(max_length = 10)
    columna_bd = models.TextField(max_length = 10)
    lista = models.ForeignKey(Configuracion_Listas, on_delete = models.CASCADE,null= True)
   
    class Meta:
        verbose_name_plural = "Configuracion Columnas"
