from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Resource(models.Model):
    RESOURCE_TYPES = [
        ('SPORT', 'Pista Deportiva'),
        ('ROOM', 'Sala de Reuniones'),
        ('EQUIP', 'Equipamiento'),
    ]
    name = models.CharField(max_length=100, verbose_name="Nombre del recurso")
    resource_type = models.CharField(max_length=10, choices=RESOURCE_TYPES, default='SPORT', verbose_name="Tipo")
    description = models.TextField(blank=True, null=True, verbose_name="Descripción")

    def __str__(self):
        return f"{self.name} ({self.get_resource_type_display()})"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', verbose_name="Usuario")
    resource = models.ForeignKey(Resource, on_delete=models.CASCADE, related_name='bookings', verbose_name="Recurso")
    start_time = models.DateTimeField(verbose_name="Fecha y hora de inicio")
    end_time = models.DateTimeField(verbose_name="Fecha y hora de fin")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creado el")
    is_recurring = models.BooleanField(default=False, verbose_name="¿Es recurrente?")
    
    def __str__(self):
        return f"Reserva de {self.user.username} - {self.resource.name}"

    def clean(self):
        #VALIDACIONES DE LAS RESERVAS:
        # Validacion 1. La hora de inicio debe ser anterior a la hora de fin
        if self.start_time and self.end_time:
            if self.start_time >= self.end_time:
                raise ValidationError("La hora de inicio debe ser anterior a la hora de fin.")

            # Validacion 2. Lógica para evitar solapamientos en el mismo recurso
            overlapping_bookings = Booking.objects.filter(  
                resource=self.resource,
                start_time__lt=self.end_time,
                end_time__gt=self.start_time
            )

            # Validacion 3. Si estamos editando una reserva, la excluimos de la búsqueda para que no choque consigo misma
            if self.pk:
                overlapping_bookings = overlapping_bookings.exclude(pk=self.pk)

            if overlapping_bookings.exists():
                raise ValidationError("Este recurso ya está reservado en el horario seleccionado. Elige otro momento.")
            
    def save(self, *args, **kwargs):
        self.full_clean()  
        super().save(*args, **kwargs)
