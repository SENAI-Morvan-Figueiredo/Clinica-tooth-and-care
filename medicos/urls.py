from . import views
from django.urls import path

urlpatterns = [
    path('medIndex/', views.index, name='medIndex'),
    path('medDetalhesMed/', views.medico_update_teste, name='medDetalhesMed'),
    path('medConsultas/', views.consultas_primeiro_medico, name='medConsultas'),
]
