# Generated by Django 3.2.3 on 2021-10-18 15:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionStock', '0017_alter_articulos_fecha_actualizacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='articulos',
            name='fecha_actualizacion',
        ),
    ]
