from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.db import models

class ExtendUser(models.Model):
    idextenuser=models.CharField(primary_key=True,max_length=20)
    Telefono = models.CharField(max_length=12)
    datebirth = models.DateField(null=True, blank=True)#default 0 por errores
    imageprofile=models.ImageField(upload_to='images', default='App/perfil/profile_base.jpg')
    accesibility=models.BooleanField()
    iduser=models.ForeignKey(User,null=True,blank=False, on_delete=models.RESTRICT)


class Auto(models.Model):
    IdAuto=models.CharField(primary_key=True, max_length=20)
    Marca=models.CharField(max_length=10)
    Modelo=models.CharField(max_length=10)
    Patente=models.CharField(max_length=10)
    Vin=models.CharField(max_length=25)
    is_active=models.BooleanField(default=True)
    #agregar fecha de vinculacion
    IdUser=models.ForeignKey(User,null=True,blank=False, on_delete=models.RESTRICT)
    def __str__(self):
        auto=f" {self.Marca},  {self.Modelo},  {self.Patente}"
        return auto
    
class Tarjeta(models.Model):
    IdTarjeta=models.CharField(max_length=20)
    #EncryptedCharField
    NumeroTarjeta=models.CharField(max_length=20)
    Nombre=models.CharField(max_length=50, default='0')
    FechaVencimiento=models.CharField(max_length=5)
    CVV=models.CharField(max_length=3)
    is_active=models.BooleanField(default=True)
    iduser=models.ForeignKey(User,null=True,blank=False, on_delete=models.RESTRICT)
    def __str__(self):
        tarjeta=f"Nombre: {self.Nombre}, Nro tarjeta: {self.NumeroTarjeta}, Fch Vto:{self.FechaVencimiento}"
        return (tarjeta)
    
class Sucursal(models.Model):
    IdSucursal=models.CharField(primary_key=True, max_length=20)
    NombreSucursal=models.CharField(max_length=50)
    TarifaSucursal=models.IntegerField(default=0)
    Direccion=models.CharField(max_length=50)
    CostoReserva=models.IntegerField(default=0)
    #disponible=models.BooleanField(default=True)
    #agregar capac o solo usar un filtro DISTINC()
    #capacidad=models.IntegerField(default=)

    def __str__(self):
        sucursal=f" {self.NombreSucursal},{self.Direccion}, Tarifa{self.TarifaSucursal} Por hora"
        return sucursal


class EstadoReserva(models.Model):
    EstadoReservaId=models.CharField(primary_key=True, max_length=3)
    EstadoReservaNombre=models.CharField(max_length=20)


class Reserva(models.Model):
    IdReserva=models.CharField(primary_key=True, max_length=20)
    CodigoReserva=models.CharField(max_length=20)
    FechaReserva=models.DateTimeField(auto_now_add=True)
    FechaLlegada=models.DateTimeField()
    FechaSalida=models.DateTimeField()
    LugarReserva=models.CharField(max_length=15)
    Costo=models.CharField(max_length=10)
    Penalizacion=models.BooleanField(default=False)
    qrreserva=models.ImageField(upload_to='static/images', blank=True)
    
    #agregar qr imagen
    #foreingkeys
    iduser=models.ForeignKey(User,null=True,blank=False, on_delete=models.RESTRICT)
    IdAuto=models.ForeignKey(Auto,null=True,blank=False, on_delete=models.RESTRICT)
    EstadoReservaId=models.ForeignKey(EstadoReserva,default='1',blank=False, on_delete=models.RESTRICT)
    IdSucursal=models.ForeignKey(Sucursal,null=True, blank=True, on_delete=models.RESTRICT)
    IdTarjeta=models.ForeignKey(Tarjeta,null=True, blank=True, on_delete=models.RESTRICT)
    


