from django.db import models
from django.contrib.auth.models import User

class Especialidade(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='medico')
    cpf = models.CharField(max_length=14, null=False, blank=False, unique=True)  # 000.000.000-00
    rg = models.CharField(max_length=20, null=False, blank=False, unique=True)
    crm = models.CharField(max_length=20, null=False, blank=False, unique=True)
    telefone = models.CharField(max_length=20, null=False, blank=False)
    ativo = models.BooleanField(default=True)

    especialidades = models.ManyToManyField(
        Especialidade,
        related_name="medicos"  # permite acessar os médicos a partir da especialidade
    )

    def __str__(self):
        return self.user.username