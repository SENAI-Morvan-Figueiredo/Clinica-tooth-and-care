from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponseForbidden
import logging

from medicos.models import Medico

# Create your views here.
def teste(request):
    return redirect('/medicos/medIndex/')

def teste2(request):
    return render(request, 'basedashboards.html')

def login(request):
    return redirect('/accounts/login/')

logger = logging.getLogger(__name__)

@login_required
def get_user_type(request):
    user = request.user
    #TODO: trocar para as páginas de médicos e pacientes
    if hasattr(user, 'paciente'):
        return redirect('teste')
    elif hasattr(user, 'medico'):
        return redirect('medIndex')
    elif user.is_staff:
        return redirect('dashboard')
    else:
        return HttpResponseForbidden("ERRO: 403. Você não tem permissão para acessar essa página")