from . import views
from django.urls import path

urlpatterns = [
    path('medIndex/', views.index, name='medIndex'),
    path('medDetalhesMed/', views.medico_update, name='medDetalhes'),
    path('medConsultas/', views.consultas_medico, name='medConsultas'),
    path('medDiagnostico/<int:consulta_id>/', views.consulta_detalhes, name='medDiagnostico'),
    path('finalizarConsulta/<int:pk>', views.finalizar_consulta, name="finalizarConsulta"),
]
