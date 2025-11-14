from django import forms
from django.forms.widgets import SelectDateWidget, SplitDateTimeWidget
import datetime
from .models import Consulta, Exame, Diagnostico, Anamnese

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
    data = forms.DateField(
        label='Data da consulta',
        widget=SelectDateWidget(
            empty_label=("Ano", "Mês", "Dia") 
        )
    )

    hora_consulta = forms.TimeField(
        label='Hora da Consulta',
        required=True, 
        widget=forms.HiddenInput() 
    )

    sala = forms.ChoiceField(
        label='Sala de Atendimento',
        choices=Consulta.SALAS,
        required=True, 
        widget=forms.HiddenInput()
    )

    def __init__(self, *args, paciente_logado=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.paciente_logado = paciente_logado
        
        # Ajusta a renderização dos campos do modelo
        self.fields['medico'].widget.attrs.update({'class': 'form-control'})
        self.fields['servico'].widget.attrs.update({'class': 'form-control'})
        # O campo 'hora_consulta' e 'sala' usam HiddenInput, então não precisam de classe

    class Meta:
        model= Consulta
        # Adicione 'sala' aqui, pois é um campo do modelo que será validado e salvo
        fields = ['servico', 'medico', 'sala'] 
        labels = {
            'servico': 'Serviço Agendado',
            'medico': 'Médico Responsável',
        }
        # Não precisa de 'data' nem 'hora_consulta' em 'widgets' pois já foram definidos acima
        widgets = {} 

    def clean(self):
        cleaned_data = super().clean()
        
        # O campo 'data' (DateField) está no cleaned_data
        data_consulta = cleaned_data.get("data") 
        # O campo 'hora_consulta' (TimeField) está no cleaned_data
        hora_consulta = cleaned_data.get("hora_consulta")
        # O campo 'sala' (CharField/ChoiceField) está no cleaned_data
        sala_atendimento = cleaned_data.get("sala")
        
        # 1. Combinação de Data e Hora
        if data_consulta and hora_consulta:
            # Combina o objeto date com o objeto time
            data_hora_completa = datetime.datetime.combine(data_consulta, hora_consulta)
            
            # Atribui ao campo 'data' (DateTimeField) da instância do modelo
            self.instance.data = data_hora_completa
        else:
            # Adiciona erro se a data ou a hora estiverem faltando, quebrando o fluxo.
            # Se 'data' ou 'hora_consulta' não estiverem presentes, o Formulário já deve ter validado com erro
            # mas reforçamos a verificação para garantir a combinação correta.
            if not data_consulta:
                self.add_error('data', "A data da consulta é obrigatória.")
            if not hora_consulta:
                # O campo 'hora_consulta' é um TimeField no Formulário e o Select no template
                # é o que realmente define seu valor (via JS).
                self.add_error('hora_consulta', "A hora da consulta é obrigatória.")

        # 2. Define o valor do serviço (já estava correto)
        servico = cleaned_data.get("servico")
        if servico and servico in PRECOS_SERVICOS:
            self.instance.valor = PRECOS_SERVICOS[servico]
        
        # 3. Garante que a sala seja definida na instância do modelo
        if sala_atendimento:
            self.instance.sala = sala_atendimento
        
        return cleaned_data

    def save(self, commit=True):
        consulta = super().save(commit=False)
        consulta.status = 'marcada'

        # O 'paciente' é setado nas views, mas se for necessário garantir aqui
        # if self.paciente_logado:
        #     consulta.paciente = self.paciente_logado

        if commit:
            consulta.save()

        return consulta
    
# ... (as outras classes de forms permanecem inalteradas)

class ConsultaAdiar(forms.ModelForm):
    data_widget = SplitDateTimeWidget( # widget para usar no campo
        date_attrs={'type': 'date', 'class': 'form-control mb-3 mx-3'},
        time_attrs={'type': 'time', 'class': 'form-control mb-3 mx-3'},
    )
    # cria o campo para evitar o DateTimeField comum
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