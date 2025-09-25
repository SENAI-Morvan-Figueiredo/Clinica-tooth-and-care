from django.db import models

GENERO_CHOICES = [
    ("M", "Masculino"),
    ("F", "Feminino"),
    ("O", "Outro"),
]

# Create your models here.
class Paciente(models.Model):
    nome = models.CharField(max_length=200, null=False, blank=False)
    cpf = models.CharField(null=False, blank=False, unique=True)
    rg = models.CharField(null=False, blank=False, unique=True)
    email = models.EmailField(null=False, blank=False, unique=True)
    telefone = models.CharField(null=False, blank=False)
    data_nasc = models.DateField(null=False, blank=False)
    genero = models.CharField(choices=GENERO_CHOICES, max_length=1)
    endereco = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nome