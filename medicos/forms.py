from django import forms
from django.contrib.auth import get_user_model
from .models import Medico, Especialidade
from consultas.models import DisponibilidadeMedico, SALAS
from datetime import datetime, time
CARGA_HORARIAS = {
    "manha": "Manhã",
    "tarde": "Tarde",
    "integral": "Integral"
}

ESPECIALIDADE_SALAS_MAP = {
    "Clínico Geral": "SALA_GERAL_1",
    "Odontopediatria": "SALA_PEDIATRICA",
    "Ortodontia": "SALA_ORTODONTIA",
    "Endontia": "SALA_ENDONTIA",
    "Periodontia": "SALA_PROFILAXIA",
    "Implantodontia": "SALA_CIRURGIA_PRIN",
    "Cirurgia Bucomaxilofacial": "SALA_CIRURGIA_PRIN",
    "Estomatologia": "SALA_GERAL_2",
    "Prótese Dentária": "SALA_ESTETICA",
    "Radiologia Odontológica": "SALA_RADIOLOGIA",
    "Odontologia Estética": "SALA_ESTETICA"
}

User = get_user_model()

class MedicoUserForm(forms.ModelForm):
    """
    Formulário combinado para editar o perfil do Medico e os dados do User associado.
    """
    ESPECIALIDADES_CHOICES = {}

    nome = forms.CharField(label="Nome do Médico", max_length=150)
    sobrenome = forms.CharField(max_length=150)
    email = forms.EmailField(label="Email")
    carga_horaria = forms.ChoiceField(
        label="Carga Horária",
        choices=CARGA_HORARIAS   
    )

    class Meta:
        model = Medico
        # Inclui os campos do Medico que você quer editar
        fields = ['nome', 'sobrenome', 'email', 'crm', 'cpf', 'rg', 'telefone', 'especialidades', 'carga_horaria']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['especialidades'].widget = forms.CheckboxSelectMultiple(
            attrs={'class': 'form-check-input'}
        )
        self.fields['especialidades'].queryset = Especialidade.objects.all()

        # Pré-preenche os campos do User se estiver editando um Medico existente
        if self.instance and self.instance.pk:
            user_instance = self.instance.user
            self.fields['username'].initial = user_instance.username
            self.fields['email'].initial = user_instance.email
            
        # Opcional: Estilos Bootstrap
        for field_name in self.fields:
            if field_name != "especialidades":
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-control rounded-lg'
                })
            else:
                self.fields[field_name].widget.attrs.update({
                    'class': 'form-check'
                })


    def save(self, commit=True):
        """
        Sobrescreve o save para salvar nos dois modelos: User e Medico.
        """
        # 4. Obtém os dados dos campos do User antes de salvar o Medico
        nome = self.cleaned_data.get('nome')
        sobrenome = self.cleaned_data.get('sobrenome')
        
        username = f"Dr. {nome} {sobrenome}"

        email = self.cleaned_data.get('email')
        
        # 5. Salva (ou atualiza) o objeto User
        user = User.objects.create(
            first_name = nome,
            last_name = sobrenome,
            username = username,
            email = email
        )

        if commit:
            user.save()

        # 6. Chama o save do ModelForm para salvar o objeto Medico (que agora tem um User linkado)
        try:
            medico = super().save(commit=False)
            medico.user = user # Garante que o link está correto
            if commit:
                medico.save()
                
                # Salva o ManyToManyField de especialidades (precisa ser feito após o save inicial)
                self.save_m2m() 
        except Exception as e:
            User.objects.delete(pk=user.pk)
            self.add_error(None, f"Erro em criar o perfil do médico")

        carga_horaria = self.cleaned_data.get('carga_horaria')
        if carga_horaria == 'manha':
            hora_inicio = time(8)
            hora_fim=time(12)            
        elif carga_horaria == "tarde":
            hora_inicio = time(12, 30)
            hora_fim = time(18)
        elif carga_horaria == "integral":
            hora_inicio = time(9)
            hora_fim = time(16)

        try:
            for i in range(7):
                DisponibilidadeMedico.objects.create(
                medico=medico,
                dia_semana=DisponibilidadeMedico.DIAS_SEMANA[i][0],
                hora_inicio=hora_inicio,
                hora_fim=hora_fim,
                sala_padrao=ESPECIALIDADE_SALAS_MAP[medico.especialidades.all()[0].nome]
                )
        except Exception as e:
            User.objects.get(pk=user.pk).delete()

            self.add_error(None, f"Erro em criar os horários do médico")


        return medico
    
class MedicoEditForm(forms.ModelForm):
    username = forms.CharField(label="Nome", max_length=150)
    email = forms.EmailField(label="Email")

    class Meta:
        model = Medico
        fields = ['username', 'email', 'crm', 'cpf', 'rg', 'telefone']

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
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']

        user = self.instance.user

        user.username = username
        user.email = email
        if commit:
            user.save()

        medico = super().save(commit=False)
        medico.user = user
        if commit:
            medico.save()
            self.save_m2m() 