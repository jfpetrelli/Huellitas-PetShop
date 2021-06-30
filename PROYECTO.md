# Huellitas PetShop

## Descripción del proyecto

Desarrollaremos un sistema web de inventarios automatizado para un petshop.

## Modelo de Dominio

![Modelo de Dominio](/documentacion/Modelodedominio.png)

## Bosquejo de Arquitectura

### Maqueta 1
![Modelo de Dominio](/documentacion/maqueta1.png)

### Maqueta 2
![Modelo de Dominio](/documentacion/maqueta2.png)

### Maqueta 3
![Modelo de Dominio](/documentacion/maqueta3.png)

## Requerimientos

### Funcionales

+ Ingresar al sistema con un login y contraseña.
+ Ingresar, modificar y eliminar un artículo.
+ Ingresar, modificar y eliminar un proveedor.
+ Alta y baja de stock con archivos.
+ Generar configuración de las diferentes listas de los proveedores.
+ Generar informes de movimientos de mercadería.
+ Informar antigüedad de artículos en inventario.
+ Registrar motivo de baja de sock.
+ Relacionar artículos de los diferentes proveedores con artículos propios.

### No Funcionales

+ Mantenibilidad
    + El sistema deberá estar estructurado con un modelo de 3 capas.
+ Seguridad
    + El sistema trabajará de forma local.
    + El sistema deberá realizar de forma diaria backups de los datos.
+ Usabilidad
    + El sistema podrá trabajar desde cualquier dispositivo que esté conectado en la red local.
+ Disponibilidad
    + El sistema será capaz de registrar al mismo momento alta y baja de stock.



## Reglas de Negocio

+ Los artículos de tipo alimento tienen 3 meses de almacenamiento, luego pasan a estado de oferta.
+ Todos los lunes se emitirá un informe con los artículos próximos a vencer.
+ Todos los artículos que se ofrecen a la venta deben estar previamente cargados, si se ofrece un artículo de la lísta de proveedor que no está cargado, se deberá realizar el alta y luego se podrá generar la venta.
+ Los artículos deben pertenecer a un tipo.
+  Cada lista de proveedor tiene una única configuración de lectura, esta configuración solamente podrá ser modificada por el administrador.
+ En el alta de stock, el artículo tiene que estar previamente cargado.
+ Cuando un típo de artículo llega al stock mínimo, se disparará un mail al administrador informando la situación.
 

### Portability

**Obligatorios**

- El sistema debe funcionar correctamente en múltiples navegadores (Sólo Web).
- El sistema debe ejecutarse desde un único archivo .py llamado app.py (Sólo Escritorio).

### Security

**Obligatorios**

- Todas las contraseñas deben guardarse con encriptado criptográfico (SHA o equivalente).
- Todas los Tokens / API Keys o similares no deben exponerse de manera pública.

### Maintainability

**Obligatorios**

- El sistema debe diseñarse con la arquitectura en 3 capas. (Ver [checklist_capas.md](checklist_capas.md))
- El sistema debe utilizar control de versiones mediante GIT.
- El sistema debe estar programado en Python 3.8 o superior.

### Reliability

### Scalability

**Obligatorios**

- El sistema debe funcionar desde una ventana normal y una de incógnito de manera independiente (Sólo Web).
  - Aclaración: No se debe guardar el usuario en una variable local, deben usarse Tokens, Cookies o similares.

### Performance

**Obligatorios**

- El sistema debe funcionar en un equipo hogareño estándar.

### Reusability

### Flexibility

**Obligatorios**

- El sistema debe utilizar una base de datos SQL o NoSQL

## Stack Tecnológico

  + Python 3.8
  + Django 3.2 

### Capa de Datos

+ SQLITE3
+ ORM : Django

### Capa de Negocio

+ Pandas/Numpy - manejo de datos y carga de archivos.
+ Smptlib - envios de mails.
+ Matplotlib - generar graficos.
+ Otros.

### Capa de Presentación

+ HTML
+ Bootstrap