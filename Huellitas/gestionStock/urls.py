from django.urls import include, path
from django.contrib.auth.decorators import login_required
from gestionStock import views


urlpatterns = [
    path('home/', login_required(views.Home.as_view()), name="home"),
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
    #LISTA ARTICULOS PROVEEDORES
    path('artprov/',login_required(views.art_prov), name="art_prov"),
    path('artprov/configuracion',login_required(views.configuracion), name="configuracion"),
    path('artprov/configuracion_list',login_required(views.ConfigurarList.as_view()), name="configuracion_list"),
    path('artprov/configuracion_list_confirm_delete/<int:pk>', login_required(views.ConfigurarListDelete.as_view()), name="configurar_list_delete"),
    path('artprov/configuracion/vinculado',login_required(views.vincular_configuracion), name="vincular_configuracion"),
    path('artprov/importar',login_required(views.importar_lista), name="importar_lista"),




    path('resumen/',views.resumen, name="Resumen"),
    
    ### ELIMINAR ####
    path('lista/',login_required(views.tem_articulos.as_view()), name="lista"),
]
