# Generated by Django 3.2.3 on 2021-07-05 12:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionStock', '0006_auto_20210628_0111'),
    ]

    operations = [
        migrations.RenameField(
            model_name='proveedores',
            old_name='mail',
            new_name='email',
        ),
    ]
