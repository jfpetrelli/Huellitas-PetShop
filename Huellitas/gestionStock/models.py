from django.db import models

# Create your models here.

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

class Marcas(models.Model):

    detalle = models.TextField(max_length = 30)
    origen = models.TextField(max_length = 30, null = True)
    web = models.TextField(max_length = 30, null = True)

    class Meta:
        verbose_name_plural = "Marcas"

class Tipos(models.Model):

    detalle = models.TextField(max_length = 30)
    fecha_vencimiento = models.DateField(null = True)
    punto_pedido = models.TextField(max_length = 30, null = True)
    stock_max = models.IntegerField(null = True)

    class Meta:
        verbose_name_plural = "Tipos"

class Tipos_Salidas(models.Model):

    detalle = models.TextField(max_length = 30, null = True)
   
    class Meta:
        verbose_name_plural = "Tipos Salidas"

class Bajas(models.Model):

    fecha = models.DateField(null = True)
    tipo = models.ForeignKey(Tipos_Salidas,  on_delete = models.CASCADE)
   
    class Meta:
        verbose_name_plural = "Bajas"

class Articulos(models.Model):

    descripcion = models.TextField(max_length = 30)
    stock = models.IntegerField()
    marca = models.ForeignKey(Marcas, on_delete = models.CASCADE)
    tipo = models.ForeignKey(Tipos, on_delete = models.CASCADE)

    class Meta:
        verbose_name_plural = "Articulos"

class Salidas(models.Model):

    id_baja = models.ForeignKey(Bajas, on_delete = models.CASCADE)
    cantidad = models.ForeignKey(Tipos_Salidas,  on_delete = models.CASCADE)
    articulo = models.ForeignKey(Articulos, on_delete = models.CASCADE)
   
    class Meta:
        verbose_name_plural = "Salidas"

class Proveedores(models.Model):

    razon_social = models.TextField(max_length = 30)
    cuit = models.TextField(max_length = 30)
    direccion = models.TextField(max_length = 30)
    telefono = models.TextField(max_length = 30)
    email = models.EmailField()
    localidad = models.ForeignKey(Localidades, on_delete = models.CASCADE)
   
    class Meta:
        verbose_name_plural = "Proveedores"

class Configuracion_Listas(models.Model):

    proveedor = models.ForeignKey(Proveedores, on_delete = models.CASCADE)
    cabecera = models.TextField(max_length = 30)
    tipo_archivo = models.TextField(max_length = 30)
   
    class Meta:
        verbose_name_plural = "Configuracion Listas"

class Configuracion_Columnas(models.Model):

    tipo_dato = models.TextField(max_length = 10)
    decimal = models.TextField(max_length = 10, null = True)
    miles = models.TextField(max_length = 10, null = True)
    columna_archivo = models.IntegerField()
    columna_bd = models.IntegerField()
    delimitador = models.TextField(max_length = 10, null = True)
    cant_caracteres = models.IntegerField(null = True)
   
    class Meta:
        verbose_name_plural = "Configuracion Columnas"

class Altas(models.Model):

    num_factura = models.IntegerField(primary_key = True)
    proveedor = models.ForeignKey(Proveedores, on_delete = models.CASCADE)
    fecha = models.DateField()

    class Meta:
        verbose_name_plural = "Altas"

class Articulos_Proveedores(models.Model):

    articulo_proveedor = models.TextField(max_length = 30)
    proveedor = models.ForeignKey(Proveedores, on_delete = models.CASCADE)
    descripcion_articulo_proveedor = models.TextField(max_length = 10, null = True)
    articulo = models.IntegerField()
    precio_costo = models.IntegerField()
    fecha_actualizacion = models.TextField(max_length = 10)
   
    class Meta:
        verbose_name_plural = "Articulos Proveedores"

class Entradas(models.Model):

    num_factura = models.ForeignKey(Altas, on_delete = models.CASCADE)
    id_articulo_proveedor = models.ForeignKey(Articulos_Proveedores, on_delete = models.CASCADE)
    cantidad = models.TextField(max_length = 10, null = True)
    precio_compra = models.IntegerField()

    class Meta:
        verbose_name_plural = "Entradas"