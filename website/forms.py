from django.contrib.auth.forms import AuthenticationForm
from allauth.account.forms import SignupForm
from django import forms
from django.utils.translation import gettext_lazy as _

class CustomSignupForm(SignupForm):
    password = forms.CharField(
        label=_("Senha"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=_("A senha deve ter no mínimo 8 caracteres e incluir letras, números e símbolos."),
    )

    password2 = forms.CharField(
        label=_("Confirmação de Senha"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if 'login' in self.fields:
             self.fields['login'].widget.attrs.update({
                'class': 'form-control', 
                'placeholder': 'Email ou nome de usuário',
            })
        elif 'username' in self.fields:
            self.fields['username'].widget.attrs.update({
                'class': 'form-control', 
                'placeholder': 'Nome de Usuário',
            })
        
        self.fields['password'].widget.attrs.update({'placeholder': 'Sua Senha'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirme sua Senha'})