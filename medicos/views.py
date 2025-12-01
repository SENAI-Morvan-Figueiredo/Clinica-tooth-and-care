from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseServerError
from .models import Medico, Especialidade
from consultas.models import Consulta, Paciente
from .forms import MedicoUserForm, MedicoEditForm
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from datetime import date # Importe a classe date

from django.contrib import messages
from consultas.models import  Diagnostico, Anamnese
from consultas.forms import DiagnosticoForm, AnamneseForm


# ✅ Detalhar médico
@login_required
def medico_detail(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    return render(request, 'medicos/medIndex.html', {'medico': medico})

# ✅ Editar médico
@login_required
def medico_update(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    if request.method == "POST":
        form = MedicoEditForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect('medico_detail', pk=medico.pk)
    else:
        form = MedicoEditForm(instance=medico)
    return render(request, 'medicos/medIndex.html', {'form': form})

# Consultas de cada Médico
@login_required
def consultas_medico(request):
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

@login_required
def medico_update(request):
    user = request.user
    medico = Medico.objects.get(user=user)

    if request.method == "POST":
        form = MedicoEditForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return redirect("medIndex")  # usa o nome correto da rota
    else:
        form = MedicoEditForm(instance=medico)

    return render(request, "medicos/medDetalhes.html", {"form": form, "medico": medico})


@login_required
def index(request):
    # user = request.user
    # medico = Medico.objects.get(user=user)
    medico = Medico.objects.first()

    # Obtém a data de hoje
    hoje = date.today() 

    consultas = Consulta.objects.filter(
        medico=medico, 
        data__gte=hoje,
        status__in=['marcada', 'remarcada']
    ).order_by('data')
    
    return render(request, 'medicos/medIndex.html', context={"medico": medico, "consultas": consultas})

@login_required
def consulta_detalhes(request, consulta_id):
    consulta = get_object_or_404(Consulta, id=consulta_id)
    diagnostico = consulta.diagnostico
    anamnese = consulta.anamnese.first()  # cada consulta tem uma anamnese

    # Inicialização dos formulários
    diagnostico_form = DiagnosticoForm()
    anamnese_form = AnamneseForm()

    # Processamento de POST (salvar dados)
    if request.method == 'POST':
        if 'submit_diagnostico' in request.POST:
            diagnostico_form = DiagnosticoForm(request.POST)
            if diagnostico_form.is_valid():
                novo_diag = diagnostico_form.save(commit=False)
                novo_diag.consulta = consulta
                novo_diag.save()
                messages.success(request, 'Diagnóstico adicionado com sucesso!')
                return redirect('medDiagnostico', consulta_id=consulta.id)

        elif 'submit_anamnese' in request.POST:
            anamnese_form = AnamneseForm(request.POST)
            if anamnese_form.is_valid():
                nova_anamnese = anamnese_form.save(commit=False)
                nova_anamnese.consulta = consulta
                nova_anamnese.paciente = consulta.paciente
                nova_anamnese.save()
                messages.success(request, 'Anamnese registrada com sucesso!')
                return redirect('medDiagnostico', consulta_id=consulta.id)

    context = {
        'consulta': consulta,
        'diagnostico': diagnostico,
        'anamnese': anamnese,
        'diagnostico_form': diagnostico_form,
        'anamnese_form': anamnese_form,
    }

    return render(request, 'medicos/medDiagnostico.html', context)

@login_required
def finalizar_consulta(request, pk):
    try:
        # Encontra e modifica a consulta
        consulta = Consulta.objects.get(pk=pk)
        consulta.status = 'realizada'
        # Salva as alterações
        consulta.save()
    except Consulta.DoesNotExist as e: 
        return HttpResponseBadRequest('Consulta não encontrada.')
    except Exception as e:
        return HttpResponseServerError("Erro em finalizar consulta.")
    
    return redirect('medConsultas')