from django.urls import include, path
from django.contrib.auth.decorators import login_required
from gestionStock import views


urlpatterns = [
    path('', views.Login.as_view(), name="login"),
    path('', views.Logout.as_view(), name="logout"),
    path('almacenes/',views.almacenes, name="Almacenes"),
    path('proveedores/', login_required(views.ProveedoresList.as_view()), name="proveedor_list"),
    path('resumen/',views.resumen, name="Resumen"),
    path('configuracion/',views.configuracion, name="Configuracion"),
    path('home/', login_required(views.Home.as_view()), name="home"),
    path('proveedores/proveedor', login_required(views.ProveedoresCreate.as_view()), name="proveedor_create"),
    path('proveedores/proveedor/<int:pk>', login_required(views.ProveedoresUpdate.as_view()), name="proveedor_update"),
    path('proveedores/proveedores_confirm_delete/<int:pk>', login_required(views.ProveedoresDelete.as_view()), name="proveedor_delete"),
]
