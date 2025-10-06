from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.pacientes, name="adm-pacientes"),
    path('medicos/', views.medicos, name="adm-medicos"),
    path('consultas/', views.consultas, name="adm-consultas"),
    path('detalhe-medico/<int:pk>/', views.detalhe_medico, name="adm-detalhe-medico"),
    path('detalhe-consulta/<int:pk>/', views.detalhe_consulta, name="adm-detalhe-consulta"),
    path('detalhe-paciente/<int:pk>/', views.detalhe_paciente, name="adm-detalhe-paciente"),
    path('adicionar-medico', views.adicionar_medico, name="adicionar-medico"),
    path('deletar-medico/<int:pk>/', views.deletar_medico, name="adm-deletar-medico"),
    path('deletar-consulta/<int:pk>/', views.deletar_consulta, name="deletar-consulta"),
    path('deletar-paciente/<int:pk>/', views.deletar_paciente, name="adm-deletar-paciente")
]