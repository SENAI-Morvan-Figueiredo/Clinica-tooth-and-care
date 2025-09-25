from django.forms import forms
from .models import Paciente

class PacienteForm(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            "nome",
            "cpf",
            "rg",
            "email",
            "telefone",
            "data_nasc",
            "genero",
            "endereco",
        ]
        
        widgets = {
            "data_nasc": forms.DateInput(attrs={"type": "date"}),  # input tipo calendário
            "genero": forms.Select(),  # já usa GENREO_CHOICES do model
        }