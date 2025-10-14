from django.views.generic import ListView
from .models import Medico
from .models import Especialidade
from consultas.models import Consulta
from pacientes.models import Paciente
from .forms import MedicoUserForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy


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
        primeiro_medico = Medico.objects.order_by('id').first()
    except Medico.DoesNotExist:
        primeiro_medico = None

    consultas = []
    medico_encontrado = False

    if primeiro_medico:
        # 2. Se um médico for encontrado, obtenha todas as suas consultas
        consultas = Consulta.objects.filter(medico=primeiro_medico).order_by('data')
        medico_encontrado = True

    # 3. Prepara o contexto para o template
    context = {
        'primeiro_medico': primeiro_medico,
        'consultas': consultas,
        'medico_encontrado': medico_encontrado,
    }

    # 4. Renderiza o template, passando o contexto
    return render(request, 'medicos/medConsultas.html', context)

def medico_update_teste(request):
    medico = Medico.objects.first()

    if request.method == "POST":
        form = MedicoUserForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect("medIndex")  # usa o nome correto da rota
    else:
        form = MedicoUserForm(instance=medico)

    return render(request, "medicos/medDetalhesMed.html", {"form": form, "medico": medico})

def teste3(request):
    return render(request, 'medicos/medIndex.html')