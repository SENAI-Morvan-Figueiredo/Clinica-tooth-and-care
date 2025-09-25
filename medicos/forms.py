from django import forms
from .models import Medico, Especialidade

class MedicoForm(forms.ModelForm):
    class Meta:
        model = Medico
        fields = [
            "nome",
            "email",
            "cpf",
            "rg",
            "crm",
            "telefone",
            "especialidades",
        ]