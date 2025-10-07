from django import forms
from django.forms.widgets import SplitDateTimeWidget 
from .models import Consulta, Exame, Diagnostico, Anamnese

class ConsultaForm(forms.ModelForm):
    class Meta:
        model= Consulta
        fields = ['data', 'sala', 'servico', 'valor', 'status', 'paciente', 'medico']
        widgets = {}

class ConsultaAdiar(forms.ModelForm):
    class Meta:
        model= Consulta
        fields = ['data', 'medico']
        # widgets = {
        #     'data': forms.SplitDateTimeWidget(
        #         # Definindo os widgets internos para Data e Hora
        #         date_attrs={'type': 'date'},
        #         time_attrs={'type': 'time'},
        #     )
        # }

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