from django.db import models

class Especialidade(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return self.nome

class Medico(models.Model):
    nome = models.CharField(max_length=255, null=False, blank=False)
    email = models.EmailField(max_length=255, null=False, blank=False, unique=True)
    cpf = models.CharField(max_length=14, null=False, blank=False, unique=True)  # 000.000.000-00
    rg = models.CharField(max_length=20, null=False, blank=False, unique=True)
    crm = models.CharField(max_length=20, null=False, blank=False, unique=True)
    telefone = models.CharField(max_length=20, null=False, blank=False)

    especialidades = models.ManyToManyField(
        Especialidade,
        related_name="medicos"  # permite acessar os médicos a partir da especialidade
    )

    def __str__(self):
        return self.nome
    


