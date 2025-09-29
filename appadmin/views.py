from django.shortcuts import render
from pacientes.models import Paciente
from medicos.models import Medico, Especialidade
from consultas.models import Consulta
from django.utils import timezone

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
    
