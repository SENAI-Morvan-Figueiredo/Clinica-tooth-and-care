from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
import logging

from medicos.models import Medico

# Create your views here.
def teste(request):
    return render(request, 'base.html')

def teste2(request):
    return render(request, 'basedashboards.html')

def login(request):
    return redirect('/accounts/login/')

logger = logging.getLogger(__name__)

@login_required
def get_user_type(request):
    user = request.user
    
    if user.paciente:
        return redirect('teste')
    elif user.medico:
        return redirect('teste2')
    else:
        return redirect('appadmin/medicos')