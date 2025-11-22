from django import forms
from django.contrib.auth import get_user_model
from .models import Medico

User = get_user_model()

class MedicoUserForm(forms.ModelForm):
    """
    Formulário combinado para editar o perfil do Medico e os dados do User associado.
    """
    username = forms.CharField(label="Nome do Médico", max_length=150)
    email = forms.EmailField(label="Email")

    class Meta:
        model = Medico
        # Inclui os campos do Medico que você quer editar
        fields = ['username', 'email', 'crm', 'cpf', 'rg', 'telefone', 'especialidades']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Pré-preenche os campos do User se estiver editando um Medico existente
        if self.instance and self.instance.pk:
            user_instance = self.instance.user
            self.fields['username'].initial = user_instance.username
            self.fields['email'].initial = user_instance.email
            
        # Opcional: Estilos Bootstrap
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'form-control rounded-lg'
            })


    def save(self, commit=True):
        """
        Sobrescreve o save para salvar nos dois modelos: User e Medico.
        """
        # 4. Obtém os dados dos campos do User antes de salvar o Medico
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')
        
        # 5. Salva (ou atualiza) o objeto User
        user = self.instance.user
        
        user.username = username
        user.email = email
        if commit:
            user.save()

        # 6. Chama o save do ModelForm para salvar o objeto Medico (que agora tem um User linkado)
        medico = super().save(commit=False)
        medico.user = user # Garante que o link está correto
        if commit:
            medico.save()
            
            # Salva o ManyToManyField de especialidades (precisa ser feito após o save inicial)
            self.save_m2m() 

        return medico