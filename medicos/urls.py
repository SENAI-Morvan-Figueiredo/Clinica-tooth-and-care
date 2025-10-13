from . import views
from django.urls import path

urlpatterns = [
    path('medIndex/', views.teste, name='medIndex'),
    path('medDetalhesMed/', views.medico_update_teste, name='medDetalhesMed'),
    path('medConsultas/', views.teste3, name='medConsultas'),
]