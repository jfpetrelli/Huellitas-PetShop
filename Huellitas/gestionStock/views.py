from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, CreateView, TemplateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q
from gestionStock.models import Proveedores, Localidades, Articulos
from gestionStock.forms import ProveedoresForm, ArticulosForm
from django.contrib.auth.views import LoginView, LogoutView
import openpyxl

#LOGIN-LOGOUT
class Login(LoginView):
    template_name = 'login.html'

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class Logout(LogoutView):

    def dispatch(self, request, *args, **kwargs):
        print(request.user)
        return super().dispatch(request, *args, **kwargs)

#HOME
class Home(TemplateView):
    template_name = "home.html"


#PROVEEDORES
class ProveedoresList(ListView):
    model = Proveedores
    queryset = model.objects.all()
    context_object_name = "proveedores"
    template_name = "proveedores.html"
    paginate_by = 5

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        if query:
            object_list = Proveedores.objects.filter(
                Q(razon_social__icontains=query) | Q(cuit__icontains=query)
            )
        else:
            object_list = Proveedores.objects.all()
        return object_list

class ProveedoresUpdate(UpdateView):
    model = Proveedores
    template_name = "proveedor.html"
    form_class = ProveedoresForm
    success_url = reverse_lazy('proveedor_list')

class ProveedoresCreate(CreateView):
    model = Proveedores
    form_class = ProveedoresForm
    template_name = "proveedor.html"
    success_url = reverse_lazy('proveedor_list')

class ProveedoresDelete(DeleteView):
    model = Proveedores
    template_name = "proveedores_confirm_delete.html"
    success_url = reverse_lazy('proveedor_list')


##ALMACENES
class ArticulosList(ListView):
    model = Articulos
    queryset = model.objects.all()
    context_object_name = "articulos"
    template_name = "almacen.html"
    paginate_by = 5

    def get_queryset(self): # new
        query = self.request.GET.get('buscar')
        if query:
            object_list = Articulos.objects.filter(
                Q(descripcion__icontains  =query))
        else:
            object_list = Articulos.objects.all()
        return object_list

class ArticuloUpdate(UpdateView):
    model = Articulos
    template_name = "articulo.html"
    form_class = ArticulosForm
    success_url = reverse_lazy('articulo_list')

class ArticuloCreate(CreateView):
    model = Articulos
    form_class = ArticulosForm
    template_name = "articulo.html"
    success_url = reverse_lazy('articulo_list')

class ArticuloDelete(DeleteView):
    model = Articulos
    template_name = "articulo_confirm_delete.html"
    success_url = reverse_lazy('articulo_list')


def resumen(request):

    return render(request,"resumen.html")

def configuracion(request):
    if "GET" == request.method:
        return render(request,"configuracion.html")
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        # getting a particular sheet by name out of many sheets
        worksheet = wb["Sheet1"]
        print(worksheet)

        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        count = 0
        for row in worksheet.iter_rows():
            count += 1
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
            if count == 5:
                break
        return render(request,"configuracion.html", {"excel_data":excel_data})



def login(request):

    return render(request,"login.html")



    



