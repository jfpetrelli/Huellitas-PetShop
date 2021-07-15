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
        ]

        labels = {
            'descripcion': 'Articulo',
            'stock': 'Stock',
            'marca': 'Marca',
            'tipo': 'Tipo',
        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'marca': forms.Select(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
        }
