from django.forms import forms
from .models import Paciente

class pacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = ['nome', 'cpf', 'rg', 'email', 'telefone', 'data_nasc', 'genero', 'endereco']