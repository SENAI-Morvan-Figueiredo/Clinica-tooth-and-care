from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from datetime import date, timedelta, datetime
from django.utils import timezone

from consultas.models import Consulta
from consultas.forms import ConsultaForm, SERVICO_ESPECIALIDADE_MAP
from medicos.models import Medico
from .models import Paciente
from .forms import PacienteEditForm
from consultas.models import DisponibilidadeMedico


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

    return redirect('paciente-consultas')

#-------------------------- views para o form de criar Consultas -------------------------
def carrega_medicos(request):
    servico = request.GET.get('servico')
    especialidade_nome = SERVICO_ESPECIALIDADE_MAP.get(servico)
    medicos = Medico.objects.none()
    if especialidade_nome:
        medicos = Medico.objects.filter(especialidades__nome=especialidade_nome)
        lista_medicos = list(medicos.values('id', 'user__first_name', 'user__last_name'))

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

def get_horarios_e_salas_disponiveis(request):
    medico_id = request.GET.get('medico_id')
    data_str = request.GET.get('data') 

    if not medico_id or not data_str:
        return JsonResponse({'error': 'Médico e Data são obrigatórios'}, status=400)

    try:
        medico = get_object_or_404(Medico, pk=medico_id)
        data_selecionada = datetime.strptime(data_str, '%Y-%m-%d').date()
    except Exception as e:
        return JsonResponse({'error': f'Dados inválidos: {e}'}, status=400)

    dia_semana = data_selecionada.weekday() 
    
    disponibilidades = DisponibilidadeMedico.objects.filter(
        medico=medico, 
        dia_semana=dia_semana
    )

    horarios_ocupados = Consulta.objects.filter(
        medico=medico, 
        data__date=data_selecionada # Filtra consultas existentes naquele dia
    ).values_list('data', flat=True) # Pega apenas o campo data (que é DateTimeField)

    slots_livres = []
    duracao_consulta = timedelta(minutes=60) 

    for disp in disponibilidades:
        inicio_naive = datetime.combine(data_selecionada, disp.hora_inicio)
        fim_naive = datetime.combine(data_selecionada, disp.hora_fim)
        
        inicio = timezone.make_aware(inicio_naive)
        fim = timezone.make_aware(fim_naive)

        slot_inicio = inicio
        while slot_inicio + duracao_consulta <= fim:
            slot_fim = slot_inicio + duracao_consulta
            
            # Verificar se o slot está livre (sem sobreposição com horarios_ocupados)
            is_free = True
            for ocupado_dt in horarios_ocupados:
                # Ocupado_dt é um datetime.datetime
                
                # Definir o final do slot ocupado, se a duração for de 60 min
                ocupado_fim = ocupado_dt + duracao_consulta 
                
                # Checar sobreposição
                if (slot_inicio < ocupado_fim) and (ocupado_dt < slot_fim):
                    is_free = False
                    continue
            
            if is_free:
                slots_livres.append({
                    'hora': slot_inicio.strftime('%H:%M'),
                    'sala': disp.sala_padrao # Retorna a sala padrão do turno
                })
            
            # Avança para o próximo slot, que deve ser a duração da consulta
            slot_inicio += duracao_consulta

    return JsonResponse({'slots': slots_livres})


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

    if request.method == "POST":
        form = PacienteEditForm(request.POST)
        
        if form.is_valid():
            form.paciente_instance = paciente
            form.save()

        messages.success(request, "Informações atualizadas com sucesso!")
        return redirect('informacoes-pessoais')
    else:
        form = PacienteEditForm(paciente_instance=paciente)

    context = {
        "paciente": paciente,
        "editing": editing,
        "consultas": consultas,
        "form": form
    }
    return render(request, "paciente/consulta/historico_paciente.html", context)
