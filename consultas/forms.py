from django import forms
from django.forms.widgets import SplitDateTimeWidget 
from .models import Consulta, Exame, Diagnostico, Anamnese

class ConsultaForm(forms.ModelForm):
    class Meta:
        model= Consulta
        fields = ['data', 'sala', 'servico', 'valor', 'status', 'paciente', 'medico']
        widgets = {}

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