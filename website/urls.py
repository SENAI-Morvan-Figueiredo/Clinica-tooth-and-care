from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='index'),
    path('teste1', views.teste, name='teste'),
    path('teste2', views.teste2, name='teste2'),
    path('get_user_type', views.get_user_type, name='get_user_type'),
]