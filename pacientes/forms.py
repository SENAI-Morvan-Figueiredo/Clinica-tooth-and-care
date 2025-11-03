from django import forms
from django.db import transaction
from .models import Paciente, GENERO_CHOICES
from allauth.account.forms import SignupForm

class PacienteSignupForm(SignupForm):
    """
    Formulário de cadastro que herda do allauth.SignupForm e 
    adiciona os campos Paciente (exceto 'nome' para se adequar ao model atual).
    """

    first_name = forms.CharField(
        max_length=150, 
        label=('Nome'), 
        widget=forms.TextInput(attrs={'placeholder': ('Nome'), 'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150, 
        label=('Sobrenome'), 
        widget=forms.TextInput(attrs={'placeholder': ('Sobrenome'), 'class': 'form-control'})
    )

    cpf = forms.CharField(
        max_length=14, 
        label='CPF', 
        widget=forms.TextInput(attrs={'placeholder': 'CPF', 'class': 'form-control'})
    )
    
    rg = forms.CharField(
        max_length=20, 
        label='RG', 
        widget=forms.TextInput(attrs={'placeholder': 'RG', 'class': 'form-control'})
    )
    
    telefone = forms.CharField(
        max_length=15, 
        label='Telefone', 
        widget=forms.TextInput(attrs={'placeholder': 'Telefone', 'class': 'form-control'})
    )
    
    endereco = forms.CharField(
        max_length=255, 
        label='Endereço Completo', 
        widget=forms.TextInput(attrs={'placeholder': 'Endereço Completo', 'class': 'form-control'})
    )
    
    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        label='Gênero', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    data_nasc = forms.DateField(
        label='Data de Nascimento', 
        widget=forms.DateInput(attrs={"type": "date", 'class': 'form-control'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'class': 'form-control'})
        
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'senha'})
            self.fields['password1'].label = ('Senha')
        
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirme a senha'})
            self.fields['password2'].label = ("Confirme sua senha")

    @transaction.atomic
    def save(self, request):
        
        user = super(PacienteSignupForm, self).save(request)
        
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save() # Salva as alterações no objeto User

        paciente = Paciente.objects.create(
            user=user,
            cpf=self.cleaned_data['cpf'],
            rg=self.cleaned_data['rg'],
            telefone=self.cleaned_data['telefone'],
            data_nasc=self.cleaned_data['data_nasc'],
            genero=self.cleaned_data['genero'],
            endereco=self.cleaned_data['endereco'],
        )
        
        return user