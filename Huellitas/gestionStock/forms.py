from django import forms
from gestionStock.models import Proveedores, Articulos

class ProveedoresForm(forms.ModelForm):

    class Meta:
        model = Proveedores

        fields = [
            'razon_social',
            'cuit',
            'direccion',
            'telefono',
            'email',
            'localidad',
        ]

        labels = {
            'razon_social': 'Razon Social',
            'cuit': 'CUIT',
            'direccion': 'Direccion',
            'telefono': 'Telefono',
            'email': 'Correo',
            'localidad': 'Localidad',
        }

        widgets = {
            'razon_social': forms.TextInput(attrs={'class':'form-control'}),
            'cuit': forms.TextInput(attrs={'class':'form-control'}),
            'direccion': forms.TextInput(attrs={'class':'form-control'}),
            'telefono': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'localidad': forms.Select(attrs={'class':'form-control'}),

        }


class ArticulosForm(forms.ModelForm):


    class Meta:
        model = Articulos

        fields = [
            'descripcion',
            'stock',
            'marca',
            'tipo',
            'precio_costo',
            'precio_vta',
            'fecha_actualizacion',
            'proveedor',
        ]

        labels = {
            'descripcion': 'Articulo',
            'stock': 'Stock',
            'marca': 'Marca',
            'tipo': 'Tipo',
            'precio_costo': 'Costo',
            'precio_vta': 'Precio Venta',
            'fecha_actualizacion': 'Ultima Actualizacion',
            'proveedor': 'Proveedor',


        }
        
        
        widgets = {
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'marca': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'precio_costo': forms.NumberInput(attrs={'class':'form-control'}),
            'precio_vta': forms.NumberInput(attrs={'class':'form-control'}),
            'fecha_actualizacion': forms.DateInput(attrs={'class':'form-control','type':'date','required': False}),
            'proveedor': forms.Select(attrs={'class':'form-control','required': False}),

        }


