from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import Consulta, DisponibilidadeMedico
from django.shortcuts import get_object_or_404
from medicos.models import Medico 

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
    duracao_consulta = timedelta(minutes=60) # Ajuste a duração padrão da sua consulta

    for disp in disponibilidades:
        inicio = datetime.combine(data_selecionada, disp.hora_inicio)
        fim = datetime.combine(data_selecionada, disp.hora_fim)
        
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
                    break
            
            if is_free:
                slots_livres.append({
                    'hora': slot_inicio.strftime('%H:%M'),
                    'sala': disp.sala_padrao # Retorna a sala padrão do turno
                })
            
            # Próximo slot a cada 15 minutos (para permitir marcação de 15 em 15, mas a consulta ainda dura 60 min)
            # Se você quer slots *livres* de 15 em 15 para uma consulta de 60 minutos, você avança 15 minutos
            slot_inicio += timedelta(minutes=15)

    return JsonResponse({'slots': slots_livres})