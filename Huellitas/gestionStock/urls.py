from django.urls import include, path
from django.contrib.auth.decorators import login_required
from gestionStock import views


urlpatterns = [
    #LOGIN-LOGOUT
    path('', views.Login.as_view(), name="login"),
    path('logout/', views.Logout.as_view(), name="logout"),
    #PROVEEDORES
    path('proveedores/', login_required(views.ProveedoresList.as_view()), name="proveedor_list"),
    path('proveedores/proveedor', login_required(views.ProveedoresCreate.as_view()), name="proveedor_create"),
    path('proveedores/proveedor/<int:pk>', login_required(views.ProveedoresUpdate.as_view()), name="proveedor_update"),
    path('proveedores/proveedores_confirm_delete/<int:pk>', login_required(views.ProveedoresDelete.as_view()), name="proveedor_delete"),
    #ALMACENES
    path('almacenes/',login_required(views.ArticulosList.as_view()), name="articulo_list"),
    path('almacenes/articulo', login_required(views.ArticuloCreate.as_view()), name="articulo_create"),
    path('almacenes/articulo/<int:pk>', login_required(views.ArticuloUpdate.as_view()), name="articulo_update"),
    path('almacenes/articulo_confirm_delete/<int:pk>', login_required(views.ArticuloDelete.as_view()), name="articulo_delete"),
    


    path('resumen/',views.resumen, name="Resumen"),
    path('artprov/',views.art_prov, name="art_prov"),
    path('artprov/configuracion',views.configuracion, name="configuracion"),
    path('home/', login_required(views.Home.as_view()), name="home"),
    
]
