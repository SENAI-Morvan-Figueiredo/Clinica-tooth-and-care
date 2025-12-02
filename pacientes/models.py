from django.db import models
from django.contrib.auth.models import User

GENERO_CHOICES = [
    ("M", "Masculino"),
    ("F", "Feminino"),
    ("N", "Prefiro não informar"),
]

# Create your models here.
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente')
    nome = models.CharField(max_length=100)
    cpf = models.CharField(null=False, blank=False, unique=True)
    rg = models.CharField(null=False, blank=False, unique=True)
    telefone = models.CharField(null=False, blank=False)
    data_nasc = models.DateField(null=False, blank=False)
    genero = models.CharField(choices=GENERO_CHOICES, max_length=1)
    
    def __str__(self):
        return self.user.username 
    
class Endereco(models.Model):
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
        related_name='endereco'            
    )
    cep = models.CharField(max_length=9, verbose_name='CEP')
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=255)
    cidade = models.CharField(max_length=255)
                