from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # O campo 'username' corresponde ao nome de usuário
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', # Opcional: para classes de CSS (ex: Bootstrap)
            'placeholder': 'Email ou nome de usuário',
        })
        
        # O campo 'password' corresponde à senha
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Senha',
        })  