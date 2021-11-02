from django import forms
from gestionStock.models import Proveedores, Articulos, Configuracion_Listas, Tmp_Orden_Compra

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
            'articulo_proveedor',
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
            'articulo_proveedor': 'Art. Proveedor',
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
            'articulo_proveedor': forms.TextInput(attrs={'class':'form-control'}),
            'stock': forms.NumberInput(attrs={'class':'form-control'}),
            'marca': forms.TextInput(attrs={'class':'form-control'}),
            'tipo': forms.Select(attrs={'class':'form-control'}),
            'precio_costo': forms.NumberInput(attrs={'class':'form-control'}),
            'precio_vta': forms.NumberInput(attrs={'class':'form-control'}),
            'fecha_actualizacion': forms.DateInput(attrs={'class':'form-control','type':'date','required': False}),
            'proveedor': forms.Select(attrs={'class':'form-control','required': False}),

        }


class ConfiguracionListForm(forms.ModelForm):

    class Meta:
        model = Configuracion_Listas

        fields = [
            'proveedor',
            'cabecera',
            'tipo_archivo',
            'delimitador',
        ]

        labels = {
            'proveedor': 'Proveedor',
            'cabecera': 'Cabecera',
            'tipo_archivo': 'Tipo Archivo',
            'delimitador': 'Delimitador',
        }

        widgets = {
            'proveedor': forms.TextInput(attrs={'class':'form-control'}),
            'cabecera': forms.TextInput(attrs={'class':'form-control'}),
            'tipo_archivo': forms.TextInput(attrs={'class':'form-control'}),
            'delimitador': forms.TextInput(attrs={'class':'form-control'}),

        }


class OrdenCompraForm(forms.ModelForm):
    class Meta:
        model = Tmp_Orden_Compra

        fields = [
            'descripcion',
            'articulo_proveedor',
            'cantidad',
            'precio_costo',
            'proveedor',
        ]

        labels = {
            'descripcion': 'Descripcion',
            'articulo_proveedor': 'Codigo Proveedor',
            'cantidad': 'Cantidad',
            'precio_costo': 'Costo',
            'proveedor': 'Proveedor',

        }

        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'articulo_proveedor': forms.TextInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_costo': forms.NumberInput(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-control', 'required': False}),
        }
