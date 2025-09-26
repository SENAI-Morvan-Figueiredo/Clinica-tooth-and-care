from . import views
from django.urls import path

urlpatterns = [
    path('medDetalhesMed/<int:pk>', views.medico_detail, name='medDetalhesMed'),
]