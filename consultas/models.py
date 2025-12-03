from django.db import models
from pacientes.models import Paciente
from medicos.models import Medico

SERVICOS = [
    # 🦷 Serviços de Clínica Geral / Diagnóstico
    ("AVALIACAO", "Avaliação e Diagnóstico"),
    ("PROFILAXIA", "Profilaxia e Higiene"),
    
    # 🩹 Serviços de Odontologia Restauradora / Estética
    ("RESTAU", "Restauração Dentária"),
    ("CLAREAMENTO", "Clareamento Dental"),
    ("ESTETICA_GERAL", "Procedimento de Odontologia Estética Geral"),
    ("PROTESE", "Reabilitação Protética"),
    ("IMPLANTE", "Implante Dentário"),
    
    # 🦠 Serviços de Tratamentos Específicos
    ("CANAL", "Tratamento Endodôntico"),
    ("PERIODONTAL", "Tratamento Periodontal"),
    ("ORTODONTIA", "Instalação/Manutenção Ortodôntica"),
    
    # ✂️ Serviços Cirúrgicos
    ("EXTRACAO", "Extração Dentária Simples"),
    ("CIRURGIA_MAXILO", "Cirurgia Bucomaxilofacial Complexa"),
    
    # 👶 Serviços Pediátricos
    ("ODONTOPED", "Consulta/Tratamento Infantil"),
    
    # 🔬 Serviços de Diagnóstico Avançado
    ("RADIOLOGIA", "Exames de Imagem Odontológica"),
    ("ESTOMATO", "Avaliação de Lesões Orais"),
]

SALAS = [
    ('SALA_GERAL_1', 'Sala de Atendimento Geral 1'),
    ('SALA_GERAL_2', 'Sala de Atendimento Geral 2'),
    ('SALA_CIRURGIA_PRIN', 'Sala de Cirurgia Principal'),
    ('SALA_PROFILAXIA', 'Sala de Profilaxia e Higiene'),
    ('SALA_ORTODONTIA', 'Sala de Ortodontia'),
    ('SALA_PEDIATRICA', 'Sala Pediátrica'),
    ('SALA_ENDODONTIA', 'Sala de Endodontia'),
    ('SALA_ESTETICA', 'Sala de Estética e Clareamento'),
    ('SALA_RADIOLOGIA', 'Sala de Radiologia e Imagem'),
    ('SALA_EMERGENCIA', 'Sala de Emergência Rápida'),
]

class Consulta(models.Model):
    data = models.DateTimeField(null=False,blank=False)
    sala = models.CharField(max_length=50, choices=SALAS,null=False,blank=False)
    servico =  models.CharField(max_length=100,choices=SERVICOS,null=False,blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2,null=False,blank=False)
    status =  models.CharField(max_length=20,choices=[("marcada","Marcada"),("realizada","Realizada"),("cancelada","Cancelada"),("remarcada","Remarcada")],null=False,blank=False)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE,related_name="consultas")
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE,related_name="consultas")
    def __str__(self):
        return f"Consulta de {self.paciente} em {self.data.strftime('%d/%m/%Y %H:%M')}"

class DisponibilidadeMedico(models.Model):
    DIAS_SEMANA = [
        (0, 'Segunda-feira'),
        (1, 'Terça-feira'),
        (2, 'Quarta-feira'),
        (3, 'Quinta-feira'),
        (4, 'Sexta-feira'),
        (5, 'Sábado'),
        (6, 'Domingo'),
    ]

    medico = models.ForeignKey(Medico, on_delete=models.CASCADE, related_name='disponibilidade')
    dia_semana = models.IntegerField(choices=DIAS_SEMANA)
    hora_inicio = models.TimeField()
    hora_fim = models.TimeField()
    sala_padrao = models.CharField(max_length=50, choices=SALAS) # Adiciona a sala padrão

    class Meta:
        unique_together = ('medico', 'dia_semana', 'hora_inicio') # Evita horários duplicados no mesmo dia
        ordering = ['dia_semana', 'hora_inicio']
        verbose_name = "Disponibilidade do Médico"
        verbose_name_plural = "Disponibilidades dos Médicos"

    def __str__(self):
        return f'{self.medico} - {self.get_dia_semana_display()}: {self.hora_inicio.strftime("%H:%M")} a {self.hora_fim.strftime("%H:%M")}'
    
class Exame(models.Model):
    nome = models.CharField(max_length=255,null=False,blank=False)
    tipo = models.CharField(max_length=100,choices=[],null=False,blank=False)
    valor = models.DecimalField(max_digits=8, decimal_places=2,null=False,blank=False)
    consultas = models.ManyToManyField(Consulta, related_name="exames")
    def __str__(self):
        return self.nome
    
class Diagnostico(models.Model):
    tipo = models.CharField(max_length=100,choices=[
                # 🦷 Condições dentárias
        ("CÁRIE DENTÁRIA", "Cárie dentária"),
        ("PULPITE", "Pulpite"),
        ("ABSCESSO DENTÁRIO", "Abscesso dentário"),
        ("PERIODONTITE", "Periodontite"),
        ("GENGIVITE", "Gengivite"),
        ("HIPERSENSIBILIDADE DENTINÁRIA", "Hipersensibilidade dentinária"),

        # 😬 Problemas de oclusão e ortodontia
        ("MÁ OCLUSÃO", "Má oclusão"),
        ("APINHAMENTO DENTÁRIO", "Apinhamento dentário"),
        ("MORDIDA CRUZADA", "Mordida cruzada"),
        ("SOBREMORDIDA", "Sobremordida"),
        ("MORDIDA ABERTA", "Mordida aberta"),

        # 🦴 Alterações ósseas e articulares
        ("DISFUNÇÃO TEMPOROMANDIBULAR", "Disfunção temporomandibular (DTM)"),
        ("BRUXISMO", "Bruxismo"),
        ("PERDA ÓSSEA", "Perda óssea alveolar"),

        # 🦷 Lesões e alterações em tecidos moles
        ("ULCERAÇÃO ORAL", "Ulceração oral"),
        ("CANDIDÍASE ORAL", "Candidíase oral"),
        ("LEUCOPLASIA", "Leucoplasia"),
        ("LÍQUEN PLANO ORAL", "Líquen plano oral"),

        # 🧬 Diagnósticos gerais
        ("ALTERAÇÃO ESTÉTICA", "Alteração estética"),
        ("FRATURA DENTÁRIA", "Fratura dentária"),
        ("RETENÇÃO DE DENTE DECÍDUO", "Retenção de dente decíduo"),
        ("DENTE INCLUSO", "Dente incluso"),
        ("OUTRO", "Outro"),
    ],null=False,blank=False)
    plano_de_tratamento = models.TextField(null=False,blank=False)
    detalhes = models.TextField(null=False,blank=False)
    consulta = models.OneToOneField(Consulta, on_delete=models.CASCADE, related_name="diagnostico")
    def __str__(self):
        return f"diagnostico da {self.consulta}"
    
class Anamnese(models.Model):
    doencas_cronicas = models.TextField()
    medicamentos = models.TextField()
    queixa_principal = models.TextField()
    historico = models.TextField()
    alergia = models.TextField()
    observacao = models.TextField()
    consulta = models.ForeignKey(Consulta, on_delete=models.CASCADE, related_name="anamnese")
    def __str__(self):
        return self.queixa_principal
    
