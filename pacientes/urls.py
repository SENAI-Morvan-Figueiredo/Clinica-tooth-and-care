from django.urls import path
from . import views

urlpatterns = [
    path("consultas/", views.consulta_lista, name="consultas-lista"),
    path("consultas/nova/", views.consulta_criar, name="consultas-criar"),
    path("consultas/<int:consulta_id>/editar/", views.consulta_editar, name="consultas-editar"),
    path("consultas/<int:consulta_id>/excluir/", views.consulta_excluir, name="consultas-excluir"),
]
