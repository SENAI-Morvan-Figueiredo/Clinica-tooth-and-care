from django.views.generic import ListView
from .models import Medico
from .models import Especialidade
from consultas.models import Consulta
from pacientes.models import Paciente
from .forms import MedicoForm
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
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medico_detail', pk=medico.pk)
    else:
        form = MedicoForm(instance=medico)
    return render(request, 'medicos/medIndex.html', {'form': form})

# Consultas de cada Médico
def consulta_medico(request, pk):
    medico = get_object_or_404(Medico, id=pk)
    consultas = Consulta.objects.filter(medico=medico).order_by('-data')
    return render(request, 'consultas/consultas_por_medico.html', {
        'medico': medico,
        'consultas': consultas
    })

# Filtro de consulta
def filtro_consultas_medico(request, pk):
    medico = get_object_or_404(Medico, id=pk)

    # Coleta os parâmetros do formulário
    nome_paciente = request.GET.get('paciente', '').strip()
    data = request.GET.get('data', '').strip()
    status = request.GET.get('status', '').strip()
    servico = request.GET.get('servico', '').strip()

    # Primeiro, restringe às consultas do médico
    consultas = Consulta.objects.filter(medico=medico)

    # Aplica os filtros adicionais
    if nome_paciente:
        consultas = consultas.filter(paciente__nome__icontains=nome_paciente)

    if data:
        consultas = consultas.filter(data__date=data)

    if status:
        consultas = consultas.filter(status=status)

    if servico:
        consultas = consultas.filter(servico__icontains=servico)

    consultas = consultas.order_by('-data')

    context = {
        'medico': medico,
        'consultas': consultas,
        'filtros': {
            'paciente': nome_paciente,
            'data': data,
            'status': status,
            'servico': servico
        }
    }
    return render(request, 'consultas/filtro_consultas_medico.html', context)

def teste(request):
    return render(request, 'medicos/medIndex.html')

def teste2(request):
    return render(request, 'medicos/medDetalhesMed.html')

def teste3(request):
    return render(request, 'medicos/medConsultas.html')