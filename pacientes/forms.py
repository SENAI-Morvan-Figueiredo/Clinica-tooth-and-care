from django import forms
from .models import Paciente, GENERO_CHOICES
from allauth.account.forms import SignupForm

class PacienteSignupForm(SignupForm):
    """
    Formulário de cadastro que herda do allauth.SignupForm e 
    adiciona os campos Paciente (exceto 'nome' para se adequar ao model atual).
    """

        
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
    
    # 2. Corrigido: Usando GENERO_CHOICES diretamente.
    genero = forms.ChoiceField(
        choices=GENERO_CHOICES,
        label='Gênero', 
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    data_nasc = forms.DateField(
        label='Data de Nascimento', 
        widget=forms.DateInput(attrs={"type": "date", 'class': 'form-control'})
    )

    # Para ajustar os campos já existentes
    def __init__(self, *args, **kwargs):
        #  Chama o construtor da classe base (SignupForm)
        super().__init__(*args, **kwargs)
        # Email
        if 'email' in self.fields:
            self.fields['email'].widget.attrs.update({'class': 'form-control'})
        
        # Senha (e Confirmação de Senha)
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({'class': 'form-control'})
        
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({'class': 'form-control'})

    def save(self, request):
        
        # Chama o save() do formulário base para criar o objeto User (email, senha)
        user = super(PacienteSignupForm, self).save(request)

        # Cria e popula o objeto Paciente
        paciente = Paciente.objects.create(
            user=user,
            # Campo 'nome' removido, pois não existe no modelo Paciente fornecido
            cpf=self.cleaned_data['cpf'],
            rg=self.cleaned_data['rg'],
            # O modelo Paciente não tem campo email, mas se tivesse, seria: 
            # email=user.email,
            telefone=self.cleaned_data['telefone'],
            data_nasc=self.cleaned_data['data_nasc'],
            genero=self.cleaned_data['genero'],
            endereco=self.cleaned_data['endereco'],
        )
        
        return user