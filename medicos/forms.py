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
        
        widgets = {
            "nome": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Nome completo"
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "exemplo@dominio.com"
            }),
            "cpf": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "000.000.000-00"
            }),
            "rg": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número do RG"
            }),
            "crm": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Número do CRM"
            }),
            "telefone": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "(99) 99999-9999"
            }),
            "especialidades": forms.CheckboxSelectMultiple(),  
            # ou forms.SelectMultiple(attrs={"class": "form-control"}) para <select multiple>
        }