from django.views.generic import ListView
from .models import Medico
from .models import Especialidade
from consultas.models import Consulta
from pacientes.models import Paciente
from .forms import MedicoUserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from datetime import date # Importe a classe date


# ✅ Detalhar médico
def medico_detail(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    return render(request, 'medicos/medIndex.html', {'medico': medico})

# ✅ Editar médico
def medico_update(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == "POST":
        form = MedicoUserForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medico_detail', pk=medico.pk)
    else:
        form = MedicoUserForm(instance=medico)
    return render(request, 'medicos/medIndex.html', {'form': form})

# Consultas de cada Médico

def consultas_primeiro_medico(request):
    # 1. Tenta obter o primeiro médico do banco de dados (ordenando por id para garantir consistência)
    try:
        user = request.user
        medico = Medico.objects.get(user=user)
    except Medico.DoesNotExist:
        medico = None

    consultas = []
    medico_encontrado = False

    if medico:
        # 2. Se um médico for encontrado, obtenha todas as suas consultas
        consultas = Consulta.objects.filter(medico=medico).order_by('data')
        medico_encontrado = True

    # 3. Prepara o contexto para o template
    context = {
        'medico': medico,
        'consultas': consultas,
        'medico_encontrado': medico_encontrado,
    }

    # 4. Renderiza o template, passando o contexto
    return render(request, 'medicos/medConsultas.html', context)

def medico_update_teste(request):
    user = request.user
    medico = Medico.objects.get(user=user)

    if request.method == "POST":
        form = MedicoUserForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect("medIndex")  # usa o nome correto da rota
    else:
        form = MedicoUserForm(instance=medico)

    return render(request, "medicos/medDetalhesMed.html", {"form": form, "medico": medico})


def index(request):
    # user = request.user
    # medico = Medico.objects.get(user=user)
    medico = Medico.objects.first()

    # Obtém a data de hoje
    hoje = date.today() 

    consultas = Consulta.objects.filter(
        medico=medico, 
        data__gte=hoje 
    ).order_by('data')
    
    return render(request, 'medicos/medIndex.html', context={"medico": medico, "consultas": consultas})

def diagnostico(request, pk):

    return render(request, 'medicos/medDiagnostico.html')