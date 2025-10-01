from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('usuarios/', views.pacientes, name="adm-pacientes"),
    path('medicos/', views.medicos, name="adm-medicos"),
    path('consultas/', views.consultas, name="adm-consultas"),
    path('detalhe-medico/<int:pk>/', views.detalhe_medico, name="adm-detalhe-medico"),
    path('detalheconsulta/<int:pk>/', views.detalhe_consulta, name="adm-detalhe-consulta"),
    #TODO: adicionar url após merge
    # path('adicionar-medico', views.AdicionarMedico.as_view(), name="adicionar-medico"),
    path('deletar-medico/<int:pk>/', views.deletar_medico, name="adm-deletar-medico"),
    path('deletar-consulta/<int:pk>/', views.deletar_consulta, name="deletar-consulta"),
]