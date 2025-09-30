from django.shortcuts import render
from pacientes.models import Paciente
from medicos.models import Medico, Especialidade
from consultas.models import Consulta
from django.utils import timezone
from datetime import datetime, timedelta, time

# Create your views here.
def dashboard(request):
    if request.method == 'GET':
        qtd_pacientes = Paciente.objects.count()
        medicos_ativos = Medico.objects.all().prefetch_related("especialidades")
        hoje = timezone.now().date()
        proximas_consultas = Consulta.objects.filter(data__date=hoje)
        especialidades = Especialidade.objects.all()

        context = {
            'qtd_pacientes': qtd_pacientes,
            'medicos_ativos': medicos_ativos,
            'proximas_consultas': proximas_consultas,
            'especialidades': especialidades
        }
        return render(request, "appadmin/dashboard.html", context) 
    
def pacientes(request):
    if request.method == 'GET':
        pacientes = Paciente.objects.all()

        return render(request, "appadmin/admPacientes.html", {"pacientes": pacientes})

def medicos(request):
    if request.method == 'GET':
        medicos = Medico.objects.all()

        return render(request, "appadmin/admMedicos.html", {"medicos": medicos})
    
def gerar_slots_de_tempo(hora_inicio, hora_fim, intervalo_minutos):
    # Combina a hora com a data de hoje para criar objetos datetime iteráveis
    data_hoje = datetime.today().date()
    inicio_dt = datetime.combine(data_hoje, hora_inicio)
    fim_dt = datetime.combine(data_hoje, hora_fim)
    
    slots = []
    tempo_atual = inicio_dt
    
    # Itera enquanto o tempo atual for menor ou igual ao tempo final
    while tempo_atual <= fim_dt:
        # Adiciona a hora formatada à lista
        slots.append(tempo_atual.strftime('%H:%M'))
        
        # Avança para o próximo slot
        tempo_atual += timedelta(minutes=intervalo_minutos)
        
    return slots

def consultas(request):
    if request.method == 'GET':
        consultas = Consulta.objects.all()
        horarios = gerar_slots_de_tempo(time(6, 0), time(20, 0), 15) # consegue todos os horários de consultas

        context = {
            "consultas": consultas, 
            "horarios": horarios,
            "servicos": Consulta.SERVICOS
            }

        return render(request, 'appadmin/admConsultas.html', context)