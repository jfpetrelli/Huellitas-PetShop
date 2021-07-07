from django.urls import include, path
from gestionStock import views

urlpatterns = [
    path('', views.login, name="Login"),
    path('almacenes/',views.almacenes, name="Almacenes"),
    path('proveedores/', views.ProveedoresList.as_view(), name="proveedor_list"),
    path('resumen/',views.resumen, name="Resumen"),
    path('configuracion/',views.configuracion, name="Configuracion"),
    path('home/', views.Home.as_view(), name="home"),
    path('proveedores/proveedor', views.ProveedoresCreate.as_view(), name="proveedor_create"),
    path('proveedores/proveedor/<int:pk>', views.ProveedoresUpdate.as_view(), name="proveedor_update"),
    path('proveedores/<int:pk>', views.ProveedoresDelete.as_view(), name="proveedor_delete"),
]
