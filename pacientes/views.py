from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, timedelta
from django.utils import timezone

from consultas.models import Consulta
from consultas.forms import ConsultaForm, SERVICO_ESPECIALIDADE_MAP
from medicos.models import Medico, Especialidade
from .models import Paciente


# ===================== CONSULTAS =====================

@login_required
def consulta_lista(request):
    """
    Lista todas as consultas do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    consultas = Consulta.objects.filter(paciente=paciente, status__in=['marcada', 'remarcada']).order_by("-data")
    form = ConsultaForm()

    contexto = {
        "consultas": consultas,
        "form": form,
        "paciente": paciente,
        "today": timezone.now().date(),
    }
    return render(request, "paciente/consulta/crud.html", contexto)

@login_required
def cancelar_consulta(request, pk):
    try:
        consulta = Consulta.objects.get(pk=pk)
    except Consulta.DoesNotExist:
        messages.error(request, "Consulta não encontrada.")
        return redirect('paciente-consultas')

    consulta.status = 'cancelada'
    consulta.save()

    with open('teste.txt', 'a') as p:
        p.write(f'status: {consulta.status}')

    return redirect('paciente-consultas')

#-------------------------- views para o form de criar Consultas -------------------------
def carrega_medicos(request):
    servico = request.GET.get('servico')
    especialidade_nome = SERVICO_ESPECIALIDADE_MAP.get(servico)
    medicos = Medico.objects.none()
    if especialidade_nome:
        medicos = Medico.objects.filter(especialidades__nome=especialidade_nome)
        lista_medicos = list(medicos.values('id', 'user__first_name', 'user__last_name'))

    with open('teste.txt', 'a') as p:
        p.write(f'nome: {especialidade_nome} medicos: {lista_medicos}\n')

    return JsonResponse(lista_medicos, safe=False)

def carrega_datas(request):
    medico_id = request.GET.get('medico_id')

    try:
        medico = Medico.objects.get(id=medico_id)
    except Medico.DoesNotExist:
        return JsonResponse([], safe=False)
    
    # Gera as datas para os próximos 30 dias
    start_date = timezone.now().date()
    end_date = start_date + timedelta(days=30)
    dates_available = []
    for single_date in (start_date + timedelta(n) for n in range((end_date - start_date).days)):
        # Verifica o dia da semana
        day_of_week = single_date.weekday()
        # Verifica se o médico tem disponibilidade nesse dia da semana
        if medico.disponibilidade.filter(dia_semana=day_of_week).exists():
            dates_available.append(single_date.strftime("%Y-%m-%d"))

    return JsonResponse(dates_available, safe=False)

def medicos_por_servico(request):
    servico = request.GET.get('servico')
    especialidade_nome = SERVICO_ESPECIALIDADE_MAP.get(servico)
    
    if not especialidade_nome:
        return JsonResponse({'medicos': []})
    
    especialidade = Especialidade.objects.filter(nome=especialidade_nome).first()
    if not especialidade:
        return JsonResponse({'medicos': []})
    
    medicos = Medico.objects.filter(especialidades=especialidade)
    medicos_data = [{'id': medico.id, 'nome': f"Dr. {medico.user.first_name} {medico.user.last_name}"} for medico in medicos]
    
    return JsonResponse({'medicos': medicos_data})

@login_required
def consulta_criar_ou_editar(request, consulta_id=None):
    """
    Cria ou edita uma consulta para o paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    consulta = None
    if consulta_id:
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=paciente)

    if request.method == "POST":
        form = ConsultaForm(request.POST, instance=consulta)
        if form.is_valid():
            consulta = form.save(commit=False)
            consulta.paciente = paciente
            consulta.save()
            messages.success(request, f"Consulta {'atualizada' if consulta_id else 'agendada'} com sucesso!")
            return redirect("paciente-consultas")
        else:
            messages.error(request, "Erro ao salvar consulta. Verifique os dados.")
    else:
        form = ConsultaForm(instance=consulta)

    consultas = Consulta.objects.filter(paciente=paciente, status__in=['marcada', 'remarcada']).order_by("-data")

    return render(request, "paciente/consulta/crud.html", {
        "form": form,
        "consultas": consultas,
        "consulta": consulta,
        "consulta_editando": bool(consulta_id),
        "paciente": paciente,
        "today": timezone.now().date(),
    })

@login_required
def consulta_excluir(request, consulta_id):
    """
    Exclui uma consulta do paciente logado.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
        consulta = get_object_or_404(Consulta, id=consulta_id, paciente=paciente)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    consulta.delete()
    messages.success(request, "Consulta excluída com sucesso!")
    return redirect("paciente-consultas")

# ===================== INFORMAÇÕES PESSOAIS =====================

@login_required
def informacoes_pessoais(request):
    """
    Exibe/edita informações pessoais do paciente.
    """
    try:
        paciente = Paciente.objects.get(user=request.user)
    except Paciente.DoesNotExist:
        messages.error(request, "Paciente não encontrado.")
        return redirect('/')

    editing = request.GET.get('edit', 'false').lower() == 'true'
    consultas = Consulta.objects.filter(paciente=paciente).order_by("-data")

    if request.method == "POST" and editing:
        # Atualiza os campos do paciente
        paciente.nome = request.POST.get('nome')
        paciente.data_nasc = request.POST.get('data_nascimento')
        paciente.genero = request.POST.get('sexo')
        paciente.cpf = request.POST.get('cpf')
        paciente.rg = request.POST.get('rg')
        paciente.endereco = request.POST.get('endereco')
        paciente.telefone = request.POST.get('telefone')
        paciente.user.email = request.POST.get('email')
        paciente.user.save()
        paciente.save()
        messages.success(request, "Informações atualizadas com sucesso!")
        return redirect('informacoes-pessoais')

    context = {
        "paciente": paciente,
        "editing": editing,
        "consultas": consultas,
    }
    return render(request, "paciente/consulta/historico_paciente.html", context)
