from . import views
from django.urls import path

urlpatterns = [
    path('medIndex/', views.teste, name='medIndex'),
    path('medDetalhesMed/', views.teste2, name='medDetalhesMed'),
    path('medConsultas/', views.teste3, name='medConsultas'),
]