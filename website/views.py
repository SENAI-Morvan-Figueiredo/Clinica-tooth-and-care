from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login
from django.conf import settings
from django.http import HttpResponseForbidden
import logging

from .forms import CustomLoginForm

def home(request):
    return render(request, 'website/home.html')

def login_view(request):
    if request.method == 'POST':
        # Instancia o formulário com os dados do POST e o request
        form = CustomLoginForm(request, data=request.POST) 
        if form.is_valid():
            # Autentica e loga o usuário
            user = form.get_user()
            login(request, user)
            # Redireciona para a URL de sucesso após o login
            return redirect(settings.LOGIN_REDIRECT_URL) 
        else:
            return render(request, 'registration/login.html', {"form": form})
    else:
        form = CustomLoginForm()
    
    return render(request, 'registration/login.html', {"form": form})

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