
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import ValidationError
from .models import Resource, Booking
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['resource', 'start_time', 'end_time', 'is_recurring']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


def lista_recursos(request):
    recursos = Resource.objects.all()
    return render(request, 'reservas/lista.html', {'recursos': recursos})


def detalle_recurso(request, resource_id):
    recurso = get_object_or_404(Resource, pk=resource_id)
    reservas_existentes = recurso.bookings.all().order_by('start_time')   
    contexto = {
        'recurso': recurso,
        'reservas_existentes': reservas_existentes
    }
    return render(request, 'reservas/detalle.html', contexto)


@login_required
def crear_reserva(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        
        if form.is_valid():  
            reserva = form.save(commit=False)
            reserva.user = request.user
            
            try:
                reserva.save()
                messages.success(request, "¡Tu reserva se ha agendado con éxito!")
                return redirect('mis_reservas')
                
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = BookingForm()

    return render(request, 'reservas/crear_reserva.html', {'form': form})


@login_required
def mis_reservas(request):
    sus_reservas = request.user.bookings.all().order_by('-created_at')
    return render(request, 'reservas/mis_reservas.html', {'reservas': sus_reservas})

def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() 
            login(request, user) 
            messages.success(request, "¡Tu cuenta ha sido creada con éxito! Ya puedes reservar.")
            return redirect('lista_recursos')
    else:
        form = UserCreationForm()
        
    return render(request, 'reservas/registro.html', {'form': form})