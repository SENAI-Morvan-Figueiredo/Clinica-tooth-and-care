"""
URL configuration for tooth_n_care project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from appadmin import views as adm_views
from pacientes import views as api_pacientes


urlpatterns = [
    path('admin/', admin.site.urls),

    # rotas do app
    path('', include('website.urls')),
    path('medico/', include('medicos.urls')),
    path('consulta/', include('consultas.urls')),
    path('paciente/', include('pacientes.urls')),
    path('appadmin/', include('appadmin.urls')),
    path('deletar-medicos/', adm_views.deletar_medico, name="deletar-medicos"),
    path('desativar-medicos/', adm_views.desativar_medicos, name="desativar-medicos"),
    path('deletar-pacientes/', adm_views.deletar_paciente, name="deletar-pacientes"),
    
    #allauth
    path('accounts/', include('allauth.urls')),

    # APIs
    path('api/carrega_medicos/', api_pacientes.carrega_medicos, name='carrega_medicos'),
    path('api/carrega_datas/', api_pacientes.carrega_datas, name='carrega_datas'),
    path('api/medicos-por-servico/', api_pacientes.medicos_por_servico, name='medicos-por-servico'),
]
