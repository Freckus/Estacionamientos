# Generated by Django 5.1.1 on 2024-09-12 18:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reserva', '0003_sucursal_costoreserva'),
    ]

    operations = [
        migrations.RenameField(
            model_name='extenduser',
            old_name='Fecha_Nacimiento',
            new_name='datebirth',
        ),
        migrations.RenameField(
            model_name='extenduser',
            old_name='Telefono',
            new_name='phono',
        ),
    ]
