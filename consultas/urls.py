from django.urls import path
from . import views

urlpatterns = [
    path('api/disponibilidade/', views.get_horarios_e_salas_disponiveis, name='api_disponibilidade'),
]