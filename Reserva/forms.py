from django import forms 
from .models import Sucursal,Auto,Tarjeta,Reserva,ExtendUser,EstadoReserva
from django.contrib.auth.models import User
from django.utils import timezone, dateformat
from django.conf import settings
from pathlib import Path
from django.core.mail import EmailMessage
from django.core.exceptions import ValidationError
import re
import uuid
import os
import qrcode
from .utils import calculadora
from django.db.models import Count



###########################################################################
###########################################################################
###
#Registro usuarios
class RegisterForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['username', 'first_name', 'last_name','Telefono', 'email','date_birth','password']
        exclude=['is_superuser','date_joined','is_staff','is_active','groups', 'user_permissions','last_login']

    first_name = forms.CharField(label='Nombres',required=True, min_length=4, max_length=60,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Nombre'
                               }))
    last_name = forms.CharField(label='Apellidos',required=True, min_length=4, max_length=60,
                               widget=forms.TextInput(attrs={   
                                   'class': 'form-control',
                                   'placeholder': 'Apellidos'
                               }))
    username = forms.CharField(label='Usuario',required=True, min_length=4, max_length=60,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Nombre de Usuario'
                               }))
    email = forms.CharField(label='Correo Electrónico',required=True,
                             widget=forms.EmailInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'ejemplo@empresa.cl'
                               }))
    Telefono=forms.CharField(label='Celular',max_length=12,
                             widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Nombre de Usuario'
                               }))
    
    password = forms.CharField(label='Contraseña',required=True,
                              widget=forms.PasswordInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Contraseña'
                              }))
    password2 = forms.CharField(label='Repetir Constraseña',required=True,
                               widget=forms.PasswordInput(attrs={
                                  'class': 'form-control',
                                  'placeholder': 'Repetir Contraseña'
                              }))
    
    date_birth=forms.DateField(widget=forms.DateInput(attrs={'type':'date'}),label='Fecha Nacimiento')

    def clean_date_birth(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('date_birth')
        today = timezone.now().date()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        if age < 18:
            raise forms.ValidationError("Debe ser mayor de edad para registrarse")
        return birth_date
    #agrega los forms  y luego los def para los demas campos

    def clean_username(self):
        username=self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya se encuentra en uso')
        return username
        
    def clean_email(self):
        email=self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya se encuentra en uso')
        return email
    
    def clean(self):
        cleaned_data=super().clean()
        if cleaned_data.get('password2')!= cleaned_data.get('password'):
            self.add_error('password2', 'La contraseña no coincide')

    def guardarUsuario(self):
      #  return User.objects.create_user(
        user= User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
            first_name=self.cleaned_data.get('first_name'),
            last_name=self.cleaned_data.get('last_name'),


        )
        datauser=ExtendUser.objects.create(
            idextenuser=str(uuid.uuid4())[:20],
            Telefono=self.cleaned_data.get('Telefono'),
            accesibility=False,
            iduser=user
        )
        return user

###########################################################################
###########################################################################
#Registro extend

class RegiserExtendUser(forms.ModelForm):  
    class Meta:
        model=ExtendUser
        exclude=['idextenuser','Telefono','accesibility','accesibility','imageprofile','Fecha_Nacimiento','iduser']

    def __init__(self, user, *args, **kwargs):
        super(RegiserExtendUser, self).__init__(*args, **kwargs)
        self.user = user

    def clean_Telefono(self):
        telefono = self.cleaned_data.get('Telefono')
        if not re.match(r'^\+?\d+$', telefono):
            raise forms.ValidationError("El Teléfono solo puede contener números y opcionalmente el símbolo '+' al inicio")
        return telefono
    
    def save(self,commit=True):
        registroextenduser=super().save(commit=commit)
        if not registroextenduser.idextenuser:
            extend_id=str(uuid.uuid4())[:6]
            registroextenduser.idextenuser=extend_id
            registroextenduser.iduser=self.user

        if commit:
            registroextenduser.save()
            
        return registroextenduser


###########################################################################
###########################################################################
#Registro tarjeta
class RegisterTarjetasforms(forms.ModelForm):
    class Meta:
        model=Tarjeta
        #fields='__all__'
        fields=['Nombre','NumeroTarjeta','FechaVencimiento','CVV']
        widgets={'IdTarjeta':forms.HiddenInput(), 
                 'iduser':forms.HiddenInput()}
    
    Nombre=forms.CharField(label='Nombre',required=True, min_length=12, max_length=60,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Nombre'
                               }))

    NumeroTarjeta=forms.CharField(label='N° Tarjeta',required=True, min_length=12, max_length=20,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'ingreser N° Tarjeta'
                               }))

    FechaVencimiento=forms.CharField(label='Fecha Vencimiento',required=True, min_length=5, max_length=5,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': ' Ingrese Fecha 00/00'
                               }))
    
    CVV=forms.CharField(label='CVV',required=True, min_length=3, max_length=60,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Codigo seguridad'
                               }))
     
    def __init__(self, user, *args, **kwargs):
        super(RegisterTarjetasforms, self).__init__(*args, **kwargs)
        self.user = user

    def clean_nombre_tarjeta(self):
        cleaned_data=super().clean()
        nomtarjeta=cleaned_data.get('Nombre')
        return nomtarjeta
    def clean_num_tarjeta(self):
        cleaned_data=super().clean()
        numtarjeta=cleaned_data.get('NumeroTarjeta')
        return numtarjeta
    def clean_cvv_tarjeta(self):
        cleaned_data=super().clean()
        cvv=cleaned_data.get('CVV')
        return cvv
    def clean_fvt_tarjeta(self):
        cleaned_data=super().clean()
        FVto=cleaned_data.get('FechaVencimiento')
        return FVto

        #registrotarjeta=super(RegisterForm, self).save(commit=False)
    def save(self, commit=True):
        registrotarjeta=super().save(commit=commit)
        if not registrotarjeta.IdTarjeta:
            card_id=str(uuid.uuid4())[:6]
            registrotarjeta.IdTarjeta=card_id
            registrotarjeta.iduser=self.user

        if commit:
            registrotarjeta.save()
        return registrotarjeta
            
###########################################################################
###########################################################################
#Registro vehiculos
class RegisterVehiculosforms(forms.ModelForm):
    class Meta:
        model=Auto
        #fields='__all__'
        fields=['Marca','Modelo','Patente','Vin']
        widgets={'IdAuto':forms.HiddenInput(),
                'IdUser':forms.HiddenInput()}

    Marca=forms.CharField(label='Marca',required=True, min_length=3, max_length=20,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ingrese la Marca'
                               }))
    Modelo=forms.CharField(label='Modelo',required=True, min_length=2, max_length=40,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ingresa el Modelo'
                               }))
    Patente=forms.CharField(label='Patente',required=True, min_length=6, max_length=7,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ingresa patente XXXX00'
                               }))
    Vin=forms.CharField(label='Vin',required=True, min_length=4, max_length=60,
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Ingresa Vin xxxxxx'
                               }))


    
    def __init__(self, user, *args, **kwargs):
        super(RegisterVehiculosforms, self).__init__(*args, **kwargs)
        self.user = user


    def save(self, commit=True):
        registroauto = super().save(commit=False)
        if not registroauto.IdAuto:
            auto_id=str(uuid.uuid4())[:6]
            registroauto.IdAuto=auto_id
            registroauto.IdUser = self.user
        if commit:
            registroauto.save()

        return registroauto
 
###########################################################################
###########################################################################
#Reseva
class Reservaforms(forms.ModelForm):
    
    class Meta:
        model = Reserva
        fields = ['FechaLlegada', 'FechaSalida', 'LugarReserva']
        widgets = {
            'idReserva': forms.HiddenInput(),
            'Idsusucrsal': forms.HiddenInput,
            'IdUser': forms.HiddenInput(),
            'IdAuto': forms.HiddenInput(),
            'IdSucursal': forms.HiddenInput(),
            'FechaSalida': forms.HiddenInput(),
            'IdTarjeta': forms.HiddenInput(),
            'IdAuto': forms.HiddenInput()
        }
                
    def __init__(self, user, *args, **kwargs):
        super(Reservaforms, self).__init__(*args, **kwargs)
        self.user = user

        self.fields['FechaLlegada'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})#step:600 cintervalo de 6segundos
        self.fields['FechaSalida'].widget = forms.DateTimeInput(attrs={'type': 'datetime-local'})

        self.fields['autosusuarios'] = forms.ModelChoiceField(queryset=Auto.objects.filter(IdUser=user.id,is_active=True), label="Autos")
        #self.fields['autosusuarios'] = forms.ModelChoiceField(queryset=Auto.objects.filter(IdUser=user.id), label="Autos")
        self.fields['autosusuarios'].widget.attrs['class'] = 'from-RadioSelect'

        #self.fields['tarjetasusuarios'] = forms.ModelChoiceField(queryset=Tarjeta.objects.filter(iduser=user.id), label="Tarjetas")
        self.fields['tarjetasusuarios'] = forms.ModelChoiceField(queryset=Tarjeta.objects.filter(iduser=user.id,is_active=True), label="Tarjetas")
        self.fields['tarjetasusuarios'].widget.attrs['class'] = 'from-select'

        #self.fields['Sucursal'] = forms.ModelChoiceField(queryset=Sucursal.objects.all(), label="Sucursal")
        self.fields['Sucursal'] = forms.ModelChoiceField(queryset= Sucursal.objects.annotate(num_reservas=Count('reserva')).filter(num_reservas__lt=3))
        self.fields['Sucursal'].widget.attrs['class'] = 'from-select'

        self.fields['LugarReserva'] = forms.CharField(
            label='lugar',
            required=True,
            min_length=3,
            max_length=20,
            widget=forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese lugar estacionamiento'
            })
        )

    def clean_time_reserv(self):
        cleaned_data = super().clean()
        llegada = cleaned_data.get('FechaLlegada')
        datetimenow = timezone.now().date()
        if llegada< datetimenow:
            raise forms.ValidationError("Debe una hora posterior")
        return llegada

    def save(self, commit=True):
        reserva = super().save(commit=False)
       #agregado
        if reserva.FechaSalida>timezone.now():
            est_reserva=EstadoReserva.objects.get(EstadoReservaId=2)
            reserva.EstadoReservaId=est_reserva
        #agregado
        if not reserva.IdReserva:
            reserva_id=str(uuid.uuid4())[:6]
            reservacod=str(uuid.uuid4())[:20]
            reserva.IdReserva=reserva_id
            diff=reserva.FechaSalida-reserva.FechaLlegada
            diff_hours=int(diff.total_seconds()/60)
            hours =f"cantidad de horitas{diff_hours}"
            print(hours)
            reserva.CodigoReserva=reservacod
            reserva.iduser = self.user
            reserva.IdAuto=self.cleaned_data.get('autosusuarios')
            reserva.IdSucursal=self.cleaned_data.get('Sucursal')
            reserva.IdTarjeta=self.cleaned_data.get('tarjetasusuarios')
            sucursal = self.cleaned_data.get('Sucursal')
            tarfreserv=sucursal.CostoReserva
            minvalue = sucursal.TarifaSucursal 

            reserva.Costo=(diff_hours*minvalue)+tarfreserv
        if commit:
            reserva.save()
        random_name = str(uuid.uuid4())[:8]

        image_name = f"{random_name}_qr.png"
        image_path = os.path.join(settings.MEDIA_ROOT, 'images', image_name)
        url = f'http://127.0.0.1:8000/mostrar/{reserva_id}'
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")
        qr_image.save(image_path)
        reserva.qrreserva = image_path
        
        if commit:
            reserva.save()
        return reserva
    

###########################################################################
###########################################################################
#class FinalizarReserva():
#mostrar el reserva ticket por qr
#al apretar en boton cambiar estado a finalizado 
#mostrar costo
# mostrar el ticket o enviar mail ym essage
#
#class cambiartarjeta
#formulario activarla/ is_active con checkbox
# lo mismo con uato
# filtrar si tiene registros de + de 5 una sucursal no sea mostrada
    