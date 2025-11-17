from django import forms
from django.forms.widgets import SplitDateTimeWidget
import datetime
from .models import Consulta, Exame, Diagnostico, Anamnese, DisponibilidadeMedico, SERVICOS
from medicos.models import Medico

# conecta o tipo de consulta com a especialidade do médico
SERVICO_ESPECIALIDADE_MAP = {
    "AVALIACAO": "Clínico Geral",
    "LIMPEZA": "Higienização",
    "RESTAU": "Restauração",
    "CANAL": "Endodontia",
    "EXTRACAO": "Cirurgia",
    "CLAREAMENTO": "Estética",
    "APARELHO": "Ortodontia",
}

PRECOS_SERVICOS = {
    "AVALIACAO": 50.00,
    "LIMPEZA": 120.00,
    "RESTAU": 200.00,
    "CANAL": 550.00,
    "EXTRACAO": 150.00,
    "CLAREAMENTO": 800.00,
    "APARELHO": 60.00, # Manutenção
}

class ConsultaForm(forms.ModelForm):    
    servico = forms.ChoiceField(
        label='Serviço:',
        choices=SERVICOS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    medico = forms.ChoiceField(
        choices=[],  # Será preenchido via AJAX
        label='Médico:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    data = forms.ChoiceField(
        choices=[],  # Inicialmente vazio e será preenchido via AJAX
        label='Data da consulta',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    hora_consulta = forms.TimeField(
        label='Hora da Consulta',
        required=True, 
        widget=forms.HiddenInput() 
    )

    def __init__(self, *args, paciente_logado=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.paciente_logado = paciente_logado
        
        self.fields['medico'].widget.attrs.update({'class': 'form-control'})
        self.fields['servico'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        model= Consulta
        fields = ['servico', 'medico'] 
        labels = {
            'servico': 'Serviço Agendado',
            'medico': 'Médico Responsável',
        }
        widgets = {} 

    def clean(self):
        cleaned_data = super().clean()
    
        # Obter os dados do formulário
        servico = cleaned_data.get("servico")
        medico = cleaned_data.get("medico")
        data_consulta = cleaned_data.get("data")
        hora_consulta = cleaned_data.get("hora_consulta")
        sala_atendimento = cleaned_data.get("sala")

        if medico:
            try:
                medico = Medico.objects.get(id=medico)
                cleaned_data['medico'] = medico
                self.instance.medico = medico
            except Medico.DoesNotExist:
                self.add_error('medico', 'Médico inválido.')

        
        # Validação do fluxo sequencial
        if servico and not medico:
            self.add_error('medico', "Por favor, selecione um médico para o serviço escolhido.")
        
        if medico and not data_consulta:
            self.add_error('data', "Por favor, selecione uma data para a consulta.")
        
        if data_consulta and not hora_consulta:
            self.add_error('hora_consulta', "Por favor, selecione um horário para a consulta.")

        # Combinação de Data e Hora para o campo DateTimeField do modelo
        if data_consulta and hora_consulta:
            try:
                # Combina o objeto date com o objeto time
                data_hora_completa = datetime.datetime.combine(data_consulta, hora_consulta)
                
                # Verificar se a data/hora não está no passado
                if data_hora_completa < datetime.datetime.now():
                    self.add_error('data', "Não é possível agendar consultas para datas/horários passados.")
                
                # Atribui ao campo 'data' (DateTimeField) da instância do modelo
                self.instance.data = data_hora_completa
                
            except (ValueError, TypeError) as e:
                self.add_error(None, f"Erro ao combinar data e hora: {str(e)}")
        else:
            # Adiciona erros específicos se algum campo estiver faltando
            if not data_consulta:
                self.add_error('data', "A data da consulta é obrigatória.")
            if not hora_consulta:
                self.add_error('hora_consulta', "A hora da consulta é obrigatória.")

        # 2. Define o valor do serviço baseado no mapeamento
        if servico and servico in PRECOS_SERVICOS:
            self.instance.valor = PRECOS_SERVICOS[servico]
        elif servico:
            self.add_error('servico', "Serviço selecionado não possui preço definido.")
        
        if sala_atendimento:
            self.instance.sala = sala_atendimento
        elif hora_consulta:
            self.add_error(None, "Sala de atendimento não foi definida para o horário selecionado.")
        
        if data_consulta and hora_consulta and medico:
            data_hora_completa = datetime.datetime.combine(data_consulta, hora_consulta)
            
            consultas_existentes = Consulta.objects.filter(
                medico=medico,
                data=data_hora_completa,
            ).exclude(pk=self.instance.pk if self.instance.pk else None)
            
            if consultas_existentes.exists():
                self.add_error(None, f"O médico {medico} já possui uma consulta agendada para {data_hora_completa.strftime('%d/%m/%Y às %H:%M')}.")
        
        if data_consulta and hora_consulta and medico:
            dia_semana = data_consulta.weekday()  

            disponibilidade = DisponibilidadeMedico.objects.filter(
                medico=medico,
                dia_semana=dia_semana,
                hora_inicio__lte=hora_consulta,
                hora_fim__gt=hora_consulta
            ).first()
            
            if not disponibilidade:
                self.add_error('hora_consulta', f"O médico {medico} não possui disponibilidade para este horário.")
            elif sala_atendimento and disponibilidade.sala_padrao != sala_atendimento:
                pass
        
        return cleaned_data

    def save(self, commit=True):
        consulta = super().save(commit=False)
        consulta.status = 'marcada'

        if commit:
            consulta.save()

        return consulta

class ConsultaAdiar(forms.ModelForm):
    data_widget = SplitDateTimeWidget(
        date_attrs={'type': 'date', 'class': 'form-control mb-3 mx-3'},
        time_attrs={'type': 'time', 'class': 'form-control mb-3 mx-3'},
    )

    data = forms.SplitDateTimeField( 
        widget=data_widget
    )
    class Meta:
        model = Consulta
        fields = ['data']
        widgets = {}

    def save(self, commit=True):
        consulta = super().save(commit=False) 
        consulta.status = 'remarcada'
        if commit:
            consulta.save()
            
        return consulta

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['nome', 'tipo', 'valor', 'consultas']
        widgets = {}

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['tipo', 'plano_de_tratamento', 'detalhes', 'consulta']
        widgets = {}

class AnamneseForm(forms.ModelForm):
    class Meta:
        model = Anamnese
        fields = ['doencas_cronicas', 'medicamentos', 'queixa_principal', 'historico', 'alergia', 'observacao', 'paciente', 'consulta']
        widgets = {}