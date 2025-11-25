from django import forms
from django.db import transaction
from .models import Paciente, GENERO_CHOICES, Endereco
from allauth.account.forms import SignupForm
from datetime import datetime

class PacienteSignupForm(SignupForm):
    """
    Formulário de cadastro que herda do allauth.SignupForm e 
    adiciona os campos Paciente (exceto 'nome' para se adequar ao model atual).
    """

    first_name = forms.CharField(
        max_length=150, 
        label=('Nome'), 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    last_name = forms.CharField(
        max_length=150, 
        label=('Sobrenome'), 
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    cpf = forms.CharField(
        max_length=14, 
        label='CPF', 
        widget=forms.TextInput(attrs={'placeholder': 'Ex: 000.000.000-00', 'class': 'form-control'})
    )
    
    rg = forms.CharField(
        max_length=20, 
        label='RG', 
        widget=forms.TextInput(attrs={"placeholder": "00.000.000-0",'class': 'form-control'})
    )
    
    telefone = forms.CharField(
        max_length=15, 
        label='Telefone', 
        widget=forms.TextInput(attrs={'placeholder': 'Ex: (00) 00000-0000', 'class': 'form-control'})
    )
    
    cep = forms.CharField(
        max_length=9,
        label='CEP',
        widget=forms.TextInput(attrs={'placeholder': 'Ex: 01000-000', "class": "form-control"})
    )

    logradouro = forms.CharField(
        max_length=255,
        label="Rua",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    numero = forms.CharField(
        max_length=10,
        label="Número",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    
    complemento = forms.CharField(
        required=False,
        max_length=100,
        label="Complemento",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    bairro = forms.CharField(
        max_length=255,
        label="Bairro",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    cidade = forms.CharField(
        max_length=255,
        label="Cidade",
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        label='Gênero', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    ano_atual = datetime.now().year
    data_nasc = forms.DateField(
        label='Data de Nascimento', 
        widget=forms.SelectDateWidget(
            attrs={"class": "form-control"},
            years=range(1900, ano_atual)
            )
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
            genero=self.cleaned_data['genero']
        )

        Endereco.objects.create(
            paciente=paciente,
            cep=self.cleaned_data['cep'],
            logradouro=self.cleaned_data['logradouro'],
            numero=self.cleaned_data['numero'],
            complemento=self.cleaned_data['complemento'],
            bairro=self.cleaned_data['bairro'],
            cidade=self.cleaned_data['cidade']
        )
        
        return user
