from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Reserva import views
from django.contrib.auth import authenticate, login 
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.empty),
    path('admin/', admin.site.urls),
    path('main/', views.mainpage),
    path('perfil/',views.profile),
    path('sucursales/', views.sucursales),
    path('reservas/', views.reservaest),
    path('reserva/<str:IdReserva>', views.reservaindividual, name='Ver_reserva'),
   #path('main/',views.reservaest),
    path('historial/', views.historial),
    path('register/', views.registrarusuario),
    path('tarjetas/',views.tarjetas),
    path('tarjetas/agregar',views.registatarjeta),
    path('tarjetas/eliminar/<int:id>/', views.eliminartarjeta, name='eliminar_tarjeta'),
    path('vehiculos/', views.autos),
    path('vehiculos/agregar', views.registrarvehiculo),
    path('vehiculos/eliminar/<str:IdAuto>/', views.eliminarauto, name='eliminar_auto'),
    path('ingresar/',views.ingresar),
    path('error/', views.error),
    path('logout/', views.salir),
    path('test/', views.img)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)