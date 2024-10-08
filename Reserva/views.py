from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import Sucursal,Auto,Tarjeta,Reserva,ExtendUser
from .forms import RegisterForm,RegisterVehiculosforms,RegisterTarjetasforms,RegiserExtendUser,Reservaforms
from django.contrib import messages
import time 
#sesion id
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
#img
from django.conf import settings
from django.conf.urls.static import static
#filtros
from django.db.models import Count
###########################################################################



###########################################################################
###########################################################################
###########################################################################
#usuario
def registrarusuario(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.guardarUsuario()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('/ingresar/')
    return render(request, 'templatesApp/register.html', {'form': form})


def ingresar(request):
    username1=request.POST.get('username')
    password1=request.POST.get('password')
    txt="username:{0} y password:{1}"
    print(txt.format(username1, password1))
    user=authenticate(username=username1, password=password1)
    if user:
        login(request, user)
        messages.success(request, 'Bienvenidos {}'.format(user.username))
        request.session['user'] = username1
        request.session['clave'] = password1
        return redirect('/main/')
    else:
        if username1 is None and password1 is None:
            pass
        else:
            messages.error(request, 'Usuario o Contraseña incorrectos')
            #time.sleep(10)
            return redirect('/ingresar/')
    return render(request,'templatesApp/login.html',{ })


def salir(request):
    logout(request)
    messages.success(request,'Sesión finalizada correctamente')
    return redirect('/ingresar/')

###########################################################################
###########################################################################
#tarjeta

@login_required
def tarjetas(request):
    tarjeta = Tarjeta.objects.filter(iduser=request.user)
    #tarjform = tarjetasform()  # Ensure the form is correctly imported and instantiated
    data = {'tarjeta': tarjeta}#, 'tarjform': tarjform}

    return render(request, 'templatesApp/tarjetas.html', data)

@login_required
def registatarjeta(request):
    form=RegisterTarjetasforms(request.user, request.POST or None)
    if request.method== 'POST' and form.is_valid():
        card=form.save()
        if card:
           messages.success(request, 'Tarjeta creada exitosamente')
        return redirect('/tarjetas/')
    return render(request, 'templatesApp/agregartarjeta.html', {'form': form})

@login_required
def eliminartarjeta(request, id):
    tarjetas = Tarjeta.objects.filter(id=id)
    tarjetas.update(is_active=0)
    messages.success(request, 'Tarjeta Eliminada')
    return redirect ('/main/')
###########################################################################
###########################################################################
#vehiculos

@login_required   
def autos(request):
    autos=Auto.objects.filter(IdUser=request.user)
    data={'auto':autos }
    return render(request, 'templatesApp/vehiculos.html', data)

@login_required
def registrarvehiculo(request):
    form = RegisterVehiculosforms(request.user, request.POST or None)
    if request.method =='POST' and form.is_valid():
        auto=form.save()
        if auto:
            messages.success(request,'Vehiculo agregado exitosamente')
        return redirect('/vehiculos/')
    return render(request, 'templatesApp/agregarvehiculo.html',{'form': form})

@login_required
def eliminarauto(request, IdAuto):
    #vehiculo = Auto.objects.filter(IdUser=request.user)
    vehiculos = Auto.objects.filter(IdAuto=IdAuto)
    vehiculos.update(is_active=0)
    messages.success(request, 'Vehiculo Eliminada')
    return redirect ('/main/')

###########################################################################
###########################################################################
#Reserva

def reservaest(request):
    form=Reservaforms(request.user, request.POST or None)
    if request.method=='POST'and form.is_valid():
        reserv=form.save()
        if reserv:
            messages.success(request, 'Reserva creada exitosamente')
        return redirect('/main/')
    return render(request, 'templatesApp/reservas.html',{'form': form})
        

@login_required  
def historialreservas(request):
    reservas=Reserva.objects.filter(iduser=request.user)
    data={'reservas':reservas}
    return render(request, 'templatesApp/historialreserva.html',data)

@login_required  
def reservaindividual(request, IdReserva):
    reservas=Reserva.objects.filter(IdReserva=IdReserva)
    data={'reservas':reservas}
    return render(request,'templatesApp/Reserva.html',data)
###########################################################################
###########################################################################
#varios
@login_required  
def sucursales(request):
    sucursal = Sucursal.objects.annotate(num_reservas=Count('reserva')).filter(num_reservas__lt=4)
    data={'sucursal':sucursal}
    return render(request, 'templatesApp/sucursales.html', data)


#    form=RegisterTarjetasforms
@login_required  
def mainpage(request):
    return render(request, 'templatesApp/main.html')

@login_required  
def profile(request):
    extenduser = ExtendUser.objects.get(iduser=request.user)
    print(extenduser)
    data={'extenduser':[extenduser]}
    #return render(request, 'templatesApp/perfil.html',data)
    return render(request, 'templatesApp/perfil.html',data) 

@login_required  
def historial(request):
    reservas=Reserva.objects.filter(iduser=request.user)
    autos=Auto.objects.filter(IdUser=request.user)
    sucursal=Sucursal.objects.all()
    data={'reservas':reservas,'autos':autos,'sucursal':sucursal}
    return render(request, 'templatesApp/historialreserva.html',data)

def error(request):
    return render(request, 'templatesApp/sucursales.html')


def empty(request):
    logout(request)
    return redirect('/ingresar/')
###########################################################################
###########################################################################

#def registatarjeta(request):
#    form=RegisterAutosform(request.POST or None)
#    if request.method== 'POST' and form.is_valid():
 #       card=form.save()
#        if card:
        #    messages.success(request, 'Tarjeta creada exitosamente')
        #    return redirect('/tarjetas/')
#    return render(request, 'templatesApp/agregartarjeta.html', {'form': form})

#def registrarusuario(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.guardarUsuario()
        if user:
            login(request, user)
            messages.success(request, 'Usuario creado exitosamente')
            return redirect('/ingresar/')
    return render(request, 'templatesApp/register.html', {'form': form})#backup 

###########################################################################
###########################################################################
#TEST
def img(request):
    reservas=Reserva.objects.filter(iduser=request.user)
    autos=Auto.objects.filter(IdUser=request.user)
    sucursal=Sucursal.objects.all()
    data={'reservas':reservas,'autos':autos,'sucursal':sucursal}
    return render (request, 'templatesApp/imgtest.html',data)

#def historial(request):
    #return render(request, 'templatesApp/historialreserva.html',data)
#img=Reserva.objects.filter(iduser=request.user)
    #data={'img':img}