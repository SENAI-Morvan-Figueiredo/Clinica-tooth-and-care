# bibliotecas do django
from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest, JsonResponse
from django.contrib.auth.models import User
from django.views.generic import CreateView

# módulos do projeto
from pacientes.models import Paciente
from medicos.models import Medico, Especialidade
from medicos.forms import MedicoUserForm
from consultas.models import Consulta
from django.utils import timezone

# outras bibliotecas
from datetime import datetime, timedelta, time
import json

#------------------- funções auxiliares -------------------------
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

# --------------------------list views--------------------
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
    
def consultas(request):
    if request.method == 'GET':
        consultas = Consulta.objects.all()

        context = {
            "consultas": consultas, 
            "servicos": Consulta.SERVICOS
            }

        return render(request, 'appadmin/admConsultas.html', context)

#----------------------- detail views-------------------------

def detalhe_consulta(request, pk):
    if request.method == 'GET':
        consulta = get_object_or_404(Consulta, pk=pk)

        return render(request, 'appadmin/consultaDetalhe.html', {"consulta": consulta})

def detalhe_medico(request, pk):
    medico = get_object_or_404(Medico, pk=pk)
    consultas = Consulta.objects.filter(medico=medico)

    return render(request, 'appadmin/medicoDetalhe.html', {'medico': medico, 'consultas': consultas})

def detalhe_paciente(request, pk):
    paciente = get_object_or_404(Paciente, pk=pk)
    consultas = Consulta.objects.filter(paciente=paciente)

    return render(request, "appadmin/pacienteDetalhe.html", {"paciente": paciente, "consultas": consultas})

#---------------------create views-----------------------  
def adicionar_medico(request):
    if request.method == 'POST':
        form = MedicoUserForm(request.POST)

        if form.is_valid():

            new_name = form.cleaned_data["username"]
            new_email = form.cleaned_data["email"]

            user = User.objects.create(
                username=new_name,
                email=new_email
            )

            new_cpf = form.cleaned_data["cpf"]
            new_rg = form.cleaned_data["rg"]
            new_crm = form.cleaned_data["crm"]
            new_telefone = form.cleaned_data["telefone"]

            Medico.objects.create(
                user=user,
                cpf=new_cpf,
                rg=new_rg,
                crm=new_crm,
                telefone=new_telefone
            )

            return redirect('adm-medicos')

    else:
        form = MedicoUserForm

    return render(request, 'appadmin/medicoCriar.html', {"form": form})


#------------------------delete views--------------------------
#TODO: garantir que o usuário é válido

def deletar_medico(request, pk=-1):
    if request.method == 'POST':        
        try:
            data = json.loads(request.body)
            medico_ids = data.get('medico_ids') # procura a chave "medico_ids" no body

            if not medico_ids or not isinstance(medico_ids, list):
                return HttpResponseBadRequest(
                    "Requisição inválida. Conteúdo recebido não está correto"
                )
            
            # busca todos os médicos da lista
            medicos_deletar = Medico.objects.filter(pk__in=medico_ids)
            users_ids = medicos_deletar.values_list('user_id', flat=True)
            usuarios_deletar = User.objects.filter(pk__in=users_ids)

            count, _ = usuarios_deletar.delete() # deleta os usuários dos médicos

            return JsonResponse(
                {"status": "sucesso",
                "mensagem": f"{count} médico(s) excluído(s) com sucesso!"},
                status=200
            )

        except json.JSONDecodeError:
            # Lidar com erro se o corpo não for um JSON válido
            return HttpResponseBadRequest("Corpo da requisição deve ser um JSON válido.")
        except Exception as e:
            # Lidar com outros erros (erro de banco de dados, etc.)
            return JsonResponse({
                'status': 'erro',
                'mensagem': f'Ocorreu um erro ao excluir os médicos: {str(e)}'
            }, status=500)
    else:
        if pk == -1:
            return HttpResponseBadRequest("id inválido.")

        medico = Medico.objects.get(pk=pk)
        # Consegue o usuário
        user_id = medico.user.pk
        user = User.objects.get(pk=user_id)
        user.delete() # deleta o usuário
        
        return redirect('adm-medicos')

def deletar_consulta(request, pk):
    try:
        consulta = Consulta.objects.get(pk=pk)

        consulta.delete()   

        return redirect('adm-consultas')
    except Exception as e:
        print("Erro:", str(e))
        return redirect('adm-consultas')

def deletar_paciente(request, pk=-1):
    if request.method == 'POST':        
        try:
            data = json.loads(request.body)
            p_ids = data.get('p_ids') # procura a chave "p_ids" no body

            if not p_ids or not isinstance(p_ids, list):
                return HttpResponseBadRequest(
                    "Requisição inválida. Conteúdo recebido não está correto"
                )
            
            # busca todos os médicos da lista
            pacientes_deletar = Medico.objects.filter(pk__in=p_ids)
            users_ids = pacientes_deletar.values_list('user_id', flat=True)
            usuarios_deletar = User.objects.filter(pk__in=users_ids)

            count, _ = usuarios_deletar.delete() # deleta os usuários dos médicos

            return JsonResponse(
                {"status": "sucesso",
                "mensagem": f"{count} pacientes(s) excluído(s) com sucesso!"},
                status=200
            )

        except json.JSONDecodeError:
            # Lidar com erro se o corpo não for um JSON válido
            return HttpResponseBadRequest("Corpo da requisição deve ser um JSON válido.")
        except Exception as e:
            # Lidar com outros erros (erro de banco de dados, etc.)
            return JsonResponse({
                'status': 'erro',
                'mensagem': f'Ocorreu um erro ao excluir os pacientes: {str(e)}'
            }, status=500)
    else:
        if pk == -1:
            return HttpResponseBadRequest("id inválido.")

        pacientes = Paciente.objects.get(pk=pk)
        # Consegue o usuário
        user_id = pacientes.user.pk
        user = User.objects.get(pk=user_id)
        user.delete() # deleta o usuário
        
        return redirect('adm-pacientes')