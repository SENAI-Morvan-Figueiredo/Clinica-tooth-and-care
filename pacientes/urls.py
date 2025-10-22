# consultas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('agendar/', views.agendar_consulta, name='agendar-consulta'),
    path('', views.consulta_lista, name='consultas-lista'),
    path('nova/', views.consulta_criar, name='consultas-criar'),
    path('<int:consulta_id>/edit/', views.consulta_editar, name='consultas-editar'),
    path('<int:consulta_id>/excluir/', views.consulta_excluir, name='consultas-excluir'),
]
