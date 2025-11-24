from django.urls import path
from . import views

urlpatterns = [
    path('', views.consulta_lista, name='paciente-consultas'),
    path('infoPessoal/', views.informacoes_pessoais, name='informacoes-pessoais'),
    path('agendar/', views.consulta_criar_ou_editar, name='agendar-consulta'),
    path('<int:consulta_id>/edit/', views.consulta_criar_ou_editar, name='consultas-editar'),
    path('<int:consulta_id>/excluir/', views.consulta_excluir, name='consultas-excluir'),
    path('<int:pk>/cancelar_consulta/', views.cancelar_consulta, name="cancelar-consulta")
]
