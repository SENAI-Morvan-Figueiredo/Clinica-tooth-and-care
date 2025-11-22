from django import forms
from django.forms.widgets import SplitDateTimeWidget
import datetime
from .models import Consulta, Exame, Diagnostico, Anamnese, DisponibilidadeMedico, SERVICOS
from medicos.models import Medico

SERVICO_ESPECIALIDADE_MAP = {
    # Clínica Geral / Diagnóstico
    "AVALIACAO": "Clínico Geral",
    "PROFILAXIA": "Clínico Geral", # Substitui 'LIMPEZA'
    
    # Odontologia Restauradora / Estética
    "RESTAU": "Clínico Geral", # Restaurações Simples
    "CLAREAMENTO": "Odontologia Estética",
    "ESTETICA_GERAL": "Odontologia Estética",
    "PROTESE": "Prótese Dentária",
    "IMPLANTE": "Implantodontia",
    
    # Tratamentos Específicos
    "CANAL": "Endodontia",
    "PERIODONTAL": "Periodontia",
    "ORTODONTIA": "Ortodontia",
    
    # Cirúrgicos / Bucomaxilo
    "EXTRACAO": "Cirurgia Bucomaxilofacial", # Substitui 'Cirurgia'
    "CIRURGIA_MAXILO": "Cirurgia Bucomaxilofacial",
    
    # Pediátricos
    "ODONTOPED": "Odontopediatria",
    
    # Diagnóstico Avançado
    "RADIOLOGIA": "Radiologia Odontológica",
    "ESTOMATO": "Estomatologia",
}

PRECOS_SERVICOS = {
    # Clínica Geral / Diagnóstico
    "AVALIACAO": 50.00,
    "PROFILAXIA": 150.00,
    
    # Odontologia Restauradora / Estética
    "RESTAU": 220.00,
    "CLAREAMENTO": 850.00,
    "ESTETICA_GERAL": 400.00,
    "PROTESE": 1500.00,
    "IMPLANTE": 3000.00,
    
    # Tratamentos Específicos
    "CANAL": 650.00,
    "PERIODONTAL": 350.00,
    "ORTODONTIA": 80.00, # Manutenção
    
    # Cirúrgicos / Bucomaxilo
    "EXTRACAO": 180.00,
    "CIRURGIA_MAXILO": 900.00,
    
    # Pediátricos
    "ODONTOPED": 160.00,
    
    # Diagnóstico Avançado
    "RADIOLOGIA": 100.00,
    "ESTOMATO": 250.00,
}

class ConsultaForm(forms.ModelForm):    
    servico = forms.ChoiceField(
        label='Serviço:',
        choices=SERVICOS,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    medico = forms.ModelChoiceField(
        queryset=Medico.objects.all(),
        label='Médico:',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    data = forms.DateField(
        label="Data:",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    
    sala = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    hora_consulta = forms.TimeField(
        label='Hora da Consulta:',
        required=True, 
        widget=forms.Select(attrs={"class": "form-control"}) 
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['medico'].choices = [('', '--- Escolha o Médico ---')] # Opção inicial vazia
        self.fields['data'].choices = [('', '--- Escolha a Data ---')]
        self.fields['hora_consulta'].choices = [('', '--- Escolha a hora ---')]

    class Meta:
        model= Consulta
        fields = ['servico', 'medico', 'data', 'hora_consulta', 'sala'] 
        widgets = {} 

    def clean(self):
        cleaned_data = super().clean()
    
        # Obter os dados do formulário
        servico = cleaned_data.get("servico")
        medico = cleaned_data.get("medico")
        data_consulta = cleaned_data.get("data")
        hora_consulta = cleaned_data.get("hora_consulta")
        sala_atendimento = cleaned_data.get("sala")

        # Combina o objeto date com o objeto time
        try:
            data_hora_completa = datetime.datetime.combine(data_consulta, hora_consulta)
        except (ValueError, TypeError) as e:
                self.add_error(None, f"Erro ao checar data e hora")
        # Validação do fluxo sequencial
        if servico and not medico:
            self.add_error('medico', "Por favor, selecione um médico para o serviço escolhido.")
        
        if medico and not data_consulta:
            self.add_error('data', "Por favor, selecione uma data para a consulta.")
        
        if data_consulta and hora_consulta:
            # Verificar se a data/hora não está no passado
            if data_hora_completa < datetime.datetime.now():
                self.add_error('data', "Não é possível agendar consultas para datas/horários passados.")
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
        
        # O campo 'sala' é preenchido pelo JS no HiddenInput
        sala_atendimento = cleaned_data.get("sala")
        if sala_atendimento:
            self.instance.sala = sala_atendimento
        elif hora_consulta:
            self.add_error(None, "Sala de atendimento não foi definida para o horário selecionado.")
        
        if data_consulta and hora_consulta and medico:
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

        # adiciona o tipo datetime no campo DateTime do modelo
        data = self.cleaned_data.get('data')
        hora = self.cleaned_data.get('hora_consulta')
        data_hora_completa = datetime.datetime.combine(data, hora)

        consulta.data = data_hora_completa

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