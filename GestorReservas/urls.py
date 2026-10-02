from django.contrib import admin
from django.urls import path, include
# Importamos las vistas directamente desde la carpeta de tu app (ej: 'reservas')
from reservas.views import lista_recursos, detalle_recurso, crear_reserva, mis_reservas, registrar_usuario  

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lista_recursos, name='lista_recursos'),
    path('reservas/recursos/<int:resource_id>/', detalle_recurso, name='detalle_recurso'),
    path('reservas/nueva-reserva/', crear_reserva, name='crear_reserva'),
    path('reservas/mis-reservas/', mis_reservas, name='mis_reservas'),
    path('registro/', registrar_usuario, name='registrar_usuario'),
    path('accounts/', include('django.contrib.auth.urls')),
]

