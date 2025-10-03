from django import forms
from .models import Consulta, Exame, Diagnostico, Anamnese

class ConsultaForm(forms.ModelForm):
    class Meta:
        model= Consulta
        Fields = ['data', 'sala', 'servico', 'valor', 'status', 'paciente', 'medico']
        widgets = {}

class ConsultaAdiar(forms.ModelForm):
    class Meta:
        model= Consulta
        Fields = ['data', 'medico']
        widgets = {}

class ExameForm(forms.ModelForm):
    class Meta:
        model = Exame
        fields = ['nome', 'tipo', 'valor', 'consultas']
        widgets = {}

class DiagnosticoForm(forms.ModelForm):
    class Meta:
        model = Diagnostico
        fields = ['tipo', 'plano_de_tratamento', 'detalhes', 'consultas']
        widgets = {}

class AnamneseForm(forms.ModelForm):
    class Meta:
        model = Anamnese
        fields = ['doencas_cronicas', 'medicamentos', 'queixa_principal', 'historico', 'alergia', 'observacao', 'paciente', 'consulta']
        widgets = {}