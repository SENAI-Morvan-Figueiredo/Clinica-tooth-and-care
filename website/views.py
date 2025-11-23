from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.conf import settings
from django.http import HttpResponseForbidden
import logging

def home(request):
    return render(request, 'website/home.html')

logger = logging.getLogger(__name__)

@login_required
def get_user_type(request):
    user = request.user

    if hasattr(user, 'paciente'):
        return redirect('paciente-consultas')
    elif hasattr(user, 'medico'):
        return redirect('medIndex')
    elif user.is_staff:
        return redirect('dashboard')
    else:
        return HttpResponseForbidden("ERRO: 403. Você não tem permissão para acessar essa página")