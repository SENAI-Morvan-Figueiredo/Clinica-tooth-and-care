from django.db import models
from pacientes.models import Paciente
from medicos.models import Medico

class Consulta(models.Model):
    SERVICOS = [
        ("AVALIACAO", "Avaliação"),
        ("LIMPEZA", "Limpeza"),
        ("RESTAU", "Restauração"),
        ("CANAL", "Tratamento de canal"),
        ("EXTRACAO", "Extração dentária"),
        ("CLAREAMENTO", "Clareamento"),
        ("APARELHO", "Ortodontia"),
    ]

    data = models.DateTimeField(null=False,blank=False)
    sala = models.CharField(max_length=50,null=False,blank=False)
    servico =  models.CharField(max_length=100,choices=SERVICOS,null=False,blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2,null=False,blank=False)
    status =  models.CharField(max_length=20,choices=[("marcada","Marcada"),("realizada","Realizada"),("cancelada","Cancelada"),("remarcada","Remarcada")],null=False,blank=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="consultas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name="consultas")
    def __str__(self):
        return f"Consulta de {self.paciente} em {self.data.strftime('%d/%m/%Y %H:%M')}"

    
class Exame(models.Model):
    nome = models.CharField(max_length=255,null=False,blank=False)
    tipo = models.CharField(max_length=100,choices=[],null=False,blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2,null=False,blank=False)
    consultas = models.ManyToManyField(Consulta, related_name="exames")
    def __str__(self):
        return self.nome
    
class Diagnostico(models.Model):
    tipo = models.CharField(max_length=100,choices=[],null=False,blank=False)
    plano_de_tratamento = models.TextField(null=False,blank=False)
    detalhes = models.TextField(null=False,blank=False)
    consulta = models.ManyToManyField(Consulta, related_name="diagnosticos")
    def __str__(self):
        return self.detalhes
    
class Anamnese(models.Model):
    doencas_cronicas = models.TextField()
    medicamentos = models.TextField()
    queixa_principal = models.TextField()
    historico = models.TextField()
    alergia = models.TextField()
    observacao = models.TextField()
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="anamnese")
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="anamnese")
    def __str__(self):
        return self.queixa_principal
    
