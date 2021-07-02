from django.shortcuts import render, HttpResponse


def home(request):

    return render(request,"home.html")

def proveedores(request):

    return render(request,"proveedores.html")

def almacenes(request):

    return render(request,"almacen.html")

def resumen(request):

    return render(request,"resumen.html")

def configuracion(request):

    return render(request,"configuracion.html")

def login(request):

    return render(request,"login.html")