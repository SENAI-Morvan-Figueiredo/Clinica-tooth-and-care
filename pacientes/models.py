from django.db import models
from django.contrib.auth.models import User

GENERO_CHOICES = [
    ("M", "Masculino"),
    ("F", "Feminino"),
    ("O", "Outro"),
]

# Create your models here.
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    cpf = models.CharField(null=False, blank=False, unique=True)
    rg = models.CharField(null=False, blank=False, unique=True)
    telefone = models.CharField(null=False, blank=False)
    data_nasc = models.DateField(null=False, blank=False)
    genero = models.CharField(choices=GENERO_CHOICES, max_length=1)
    endereco = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.user.username