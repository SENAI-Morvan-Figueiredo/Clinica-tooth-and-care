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

class PacienteEditForm(forms.Form):
    """
    Formulário de edição de dados do paciente, abrangendo os campos do User,
    Paciente e Endereco, removendo os campos de senha.
    """ 
    # Campos do User
    first_name = forms.CharField(
        max_length=150, 
        label=('Nome'), 
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Nome"}),
    )
    last_name = forms.CharField(
        max_length=150, 
        label=('Sobrenome'), 
        widget=forms.TextInput(attrs={'class': 'form-control', "placeholder": "Sobrenome"})
    )
    email = forms.EmailField(
        label=('E-mail'),
        # O email é apenas para visualização e não deve ser alterado diretamente aqui
        widget=forms.EmailInput(attrs={'class': 'form-control', 'readonly': 'readonly'})
    )
    # Campos do Paciente
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
            years=range(1900, ano_atual + 1)
            )
    )
    # Campos do Endereco
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

    def __init__(self, *args, **kwargs):
        # Recebe a instância do paciente para preencher o formulário
        self.paciente_instance = kwargs.pop('paciente_instance', None)
        super().__init__(*args, **kwargs)
        
        if self.paciente_instance:
            # Preenche os campos do formulário com os dados existentes
            self.fields['first_name'].initial = self.paciente_instance.user.first_name
            self.fields['last_name'].initial = self.paciente_instance.user.last_name
            self.fields['email'].initial = self.paciente_instance.user.email
            self.fields['cpf'].initial = self.paciente_instance.cpf
            self.fields['rg'].initial = self.paciente_instance.rg
            self.fields['telefone'].initial = self.paciente_instance.telefone
            self.fields['genero'].initial = self.paciente_instance.genero
            self.fields['data_nasc'].initial = self.paciente_instance.data_nasc
            
            # Tenta obter a instância de Endereco
            try:
                self.endereco_instance = Endereco.objects.get(paciente=self.paciente_instance)
            except Endereco.DoesNotExist:
                self.endereco_instance = None
            
            if self.endereco_instance:
                self.fields['cep'].initial = self.endereco_instance.cep
                self.fields['logradouro'].initial = self.endereco_instance.logradouro
                self.fields['numero'].initial = self.endereco_instance.numero
                self.fields['complemento'].initial = self.endereco_instance.complemento
                self.fields['bairro'].initial = self.endereco_instance.bairro
                self.fields['cidade'].initial = self.endereco_instance.cidade

    @transaction.atomic
    def save(self):
        """
        Salva os dados nos modelos User, Paciente e Endereco.
        """
        if not self.paciente_instance:
            raise Exception("Instância de Paciente não fornecida para edição.")

        # 1. Atualiza o User
        user = self.paciente_instance.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()

        # 2. Atualiza o Paciente
        self.paciente_instance.cpf = self.cleaned_data['cpf']
        self.paciente_instance.rg = self.cleaned_data['rg']
        self.paciente_instance.telefone = self.cleaned_data['telefone']
        self.paciente_instance.data_nasc = self.cleaned_data['data_nasc']
        self.paciente_instance.genero = self.cleaned_data['genero']
        self.paciente_instance.save()

        # 3. Atualiza ou Cria o Endereco
        try:
            endereco = Endereco.objects.get(paciente=self.paciente_instance)
        except Endereco.DoesNotExist:
            endereco = Endereco(paciente=self.paciente_instance)
            
        endereco.cep = self.cleaned_data['cep']
        endereco.logradouro = self.cleaned_data['logradouro']
        endereco.numero = self.cleaned_data['numero']
        endereco.complemento = self.cleaned_data['complemento']
        endereco.bairro = self.cleaned_data['bairro']
        endereco.cidade = self.cleaned_data['cidade']
        endereco.save()
        
        return self.paciente_instance
