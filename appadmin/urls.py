from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admusuarios/', views.pacientes, name="adm-pacientes"),
    path('admmedicos/', views.medicos, name="adm-medicos"),
    path('admconsultas/', views.consultas, name="adm-consultas"),
]