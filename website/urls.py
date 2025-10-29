from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='index'),
    path('login', views.login_view, name="custom-login"),
    path('get_user_type', views.get_user_type, name='get_user_type'),
]