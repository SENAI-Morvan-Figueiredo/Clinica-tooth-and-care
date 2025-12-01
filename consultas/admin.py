from django.contrib import admin
from .models import Consulta, Exame, Diagnostico, Anamnese

# Register your models here.
@admin.register(Consulta)
class ConsultaAdmin(admin.ModelAdmin):
    list_display = ['data', 'sala', 'servico', 'valor', 'status', 'paciente', 'medico']
    list_filter = ['data', 'sala', 'servico', 'paciente', 'medico']
    search_fields = ['paciente', 'medico']

    fieldsets = (
        ('Detalhes da Consulta', {
            'fields': ('data', 'sala', 'servico', 'valor', 'status')
        }),
        ('Médico e Paciente', {
            'fields': ('medico', 'paciente')
        })
    )

@admin.register(Exame)
class ExameAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'valor']
    list_filter = ['tipo']

@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ['tipo', 'plano_de_tratamento', 'detalhes']
    list_filter = ['tipo']

@admin.register(Anamnese)
class AnamneseAdmin(admin.ModelAdmin):
    list_display = ['doencas_cronicas', 'medicamentos', 'queixa_principal', 'historico', 'alergia', 'observacao', 'consulta']
    list_filter = ['consulta']
